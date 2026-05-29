#!/usr/bin/env node
/**
 * retry-proxy.js — 智谱 API 重试代理（v2）
 *
 * 架构：
 *   Claude Code → http://localhost:3458 → retry-proxy → https://open.bigmodel.cn
 *                     ↑ 代理层指数退避重试，对 Claude Code 完全透明
 *
 * 功能：
 *   - 429/400(code:1234)/500/502/503/504 → 代理层直接指数退避重试
 *   - 正常请求零延迟透传（支持流式 SSE）
 *   - /health 健康检查端点
 *   - 可通过环境变量配置重试参数
 *
 * 参考：Ref/API限流问题--本地代理/zhipu_proxy.py
 *
 * 用法：
 *   node retry-proxy.js                              # 默认端口 3458
 *   node retry-proxy.js --port 3459                  # 自定义端口
 *   node retry-proxy.js --target http://localhost:xx  # 测试用
 *
 * 环境变量：
 *   PROXY_RETRY_MAX=6          最大重试次数
 *   PROXY_RETRY_BASE_SEC=2     初始退避秒数
 *   PROXY_RETRY_MAX_SEC=60     退避上限秒数
 *   PROXY_RETRY_JITTER_SEC=0.3 随机抖动秒数
 */

const http = require("http");
const https = require("https");
const { URL } = require("url");

// ═══════════════════════════════════════════════════════════
// 配置（环境变量 > 默认值）
// ═══════════════════════════════════════════════════════════

function envInt(name, def) {
  const v = process.env[name];
  if (!v || v.trim() === "") return def;
  const n = parseInt(v, 10);
  return isNaN(n) ? def : n;
}
function envFloat(name, def) {
  const v = process.env[name];
  if (!v || v.trim() === "") return def;
  const n = parseFloat(v);
  return isNaN(n) ? def : n;
}

const DEFAULT_PORT = 3458;
const DEFAULT_TARGET = "https://open.bigmodel.cn";

const args = process.argv.slice(2);
let PORT = DEFAULT_PORT;
let TARGET = DEFAULT_TARGET;
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--port" && args[i + 1]) PORT = parseInt(args[i + 1], 10);
  if (args[i] === "--target" && args[i + 1]) TARGET = args[i + 1];
}

const targetUrl = new URL(TARGET);
const isTargetHttps = targetUrl.protocol === "https:";
const forwardModule = isTargetHttps ? https : http;
const defaultPort = isTargetHttps ? 443 : 80;

const CFG = {
  retryMax: envInt("PROXY_RETRY_MAX", 6),
  retryBaseSec: envFloat("PROXY_RETRY_BASE_SEC", 2),
  retryMaxSec: envFloat("PROXY_RETRY_MAX_SEC", 60),
  retryJitterSec: envFloat("PROXY_RETRY_JITTER_SEC", 0.3),
};

// ═══════════════════════════════════════════════════════════
// 可重试错误判定（参考 zhipu_proxy.py 的 should_retry）
// ═══════════════════════════════════════════════════════════

const RETRYABLE_STATUS = new Set([429, 500, 502, 503, 504]);
const RETRYABLE_CODES = new Set(["1234", "1235", "1305"]);
const RETRYABLE_MESSAGES = [
  "网络错误",
  "network error",
  "rate limit",
  "访问量过大",
  "capacity",
  "速率限制",
  "请稍后重试",
];

function shouldRetry(statusCode, body) {
  // 1. 状态码直接可重试
  if (RETRYABLE_STATUS.has(statusCode)) return true;

  // 400 需要检查 body 内容
  if (statusCode === 400) {
    try {
      const json = JSON.parse(body);
      const error = json.error || {};
      const code = String(error.code || "").trim();
      const msg = (error.message || "").toLowerCase();

      if (RETRYABLE_CODES.has(code)) return true;
      if (RETRYABLE_MESSAGES.some((m) => msg.includes(m.toLowerCase())))
        return true;
    } catch {}
  }

  return false;
}

// ═══════════════════════════════════════════════════════════
// 请求转发（带指数退避重试）
// ═══════════════════════════════════════════════════════════

function forwardRequest(clientReq, clientRes) {
  const options = {
    hostname: targetUrl.hostname,
    port: targetUrl.port || defaultPort,
    path: targetUrl.pathname.replace(/\/$/, "") + clientReq.url,
    method: clientReq.method,
    headers: { ...clientReq.headers, host: targetUrl.host },
  };
  delete options.headers["transfer-encoding"];

  // 收集请求体
  const bodyChunks = [];
  clientReq.on("data", (chunk) => bodyChunks.push(chunk));
  clientReq.on("end", () => {
    const body = Buffer.concat(bodyChunks);
    attemptForward(options, body, clientRes, 0, CFG.retryBaseSec);
  });
}

function attemptForward(options, body, clientRes, attempt, waitSec) {
  const proxyReq = forwardModule.request(options, (proxyRes) => {
    const statusCode = proxyRes.statusCode;
    const contentType = (proxyRes.headers["content-type"] || "").toLowerCase();
    const isStreaming = contentType.includes("text/event-stream");

    // 可重试 + 非流式 + 未耗尽重试次数
    if (
      !isStreaming &&
      shouldRetry(statusCode, "") && // 先按状态码快速判断
      attempt < CFG.retryMax
    ) {
      // 收集 body 做精确判断
      const chunks = [];
      proxyRes.on("data", (c) => chunks.push(c));
      proxyRes.on("end", () => {
        const respBody = Buffer.concat(chunks).toString("utf8");

        if (shouldRetry(statusCode, respBody)) {
          const delay =
            Math.min(waitSec, CFG.retryMaxSec) +
            Math.random() * CFG.retryJitterSec;
          log(
            `${statusCode} attempt ${attempt + 1}/${CFG.retryMax}, retry in ${delay.toFixed(1)}s`
          );

          setTimeout(() => {
            attemptForward(
              options,
              body,
              clientRes,
              attempt + 1,
              waitSec * 2
            );
          }, delay * 1000);
          return;
        }

        // 不可重试的内容，原样返回
        sendResponse(clientRes, statusCode, proxyRes.headers, respBody);
      });
      return;
    }

    // 429/400 + 非流式 + 已耗尽重试：也收集 body 精确判断一次
    if (!isStreaming && (statusCode === 429 || statusCode === 400)) {
      const chunks = [];
      proxyRes.on("data", (c) => chunks.push(c));
      proxyRes.on("end", () => {
        const respBody = Buffer.concat(chunks).toString("utf8");
        if (shouldRetry(statusCode, respBody) && attempt < CFG.retryMax) {
          const delay =
            Math.min(waitSec, CFG.retryMaxSec) +
            Math.random() * CFG.retryJitterSec;
          log(
            `${statusCode} attempt ${attempt + 1}/${CFG.retryMax}, retry in ${delay.toFixed(1)}s`
          );
          setTimeout(() => {
            attemptForward(
              options,
              body,
              clientRes,
              attempt + 1,
              waitSec * 2
            );
          }, delay * 1000);
          return;
        }
        sendResponse(clientRes, statusCode, proxyRes.headers, respBody);
      });
      return;
    }

    // 正常响应（含流式）：直接透传
    clientRes.writeHead(statusCode, proxyRes.headers);
    proxyRes.pipe(clientRes);
  });

  proxyReq.on("error", (err) => {
    // 网络错误也重试
    if (attempt < CFG.retryMax) {
      const delay =
        Math.min(waitSec, CFG.retryMaxSec) +
        Math.random() * CFG.retryJitterSec;
      log(
        `network error attempt ${attempt + 1}/${CFG.retryMax}, retry in ${delay.toFixed(1)}s: ${err.message}`
      );
      setTimeout(() => {
        attemptForward(options, body, clientRes, attempt + 1, waitSec * 2);
      }, delay * 1000);
      return;
    }

    log("proxy error (retries exhausted): " + err.message);
    const errBody = JSON.stringify({
      type: "error",
      error: {
        type: "api_error",
        message: "Proxy error (retries exhausted): " + err.message,
      },
    });
    sendResponse(clientRes, 502, { "Content-Type": "application/json" }, errBody);
  });

  proxyReq.write(body);
  proxyReq.end();
}

function sendResponse(clientRes, statusCode, headers, body) {
  if (typeof body === "string") {
    const buf = Buffer.from(body, "utf8");
    clientRes.writeHead(statusCode, {
      ...headers,
      "Content-Length": buf.length,
    });
    clientRes.end(buf);
  } else {
    clientRes.writeHead(statusCode, headers);
    clientRes.end(body);
  }
}

// ═══════════════════════════════════════════════════════════
// 代理服务器
// ═══════════════════════════════════════════════════════════

const server = http.createServer((clientReq, clientRes) => {
  // 健康检查端点
  if (clientReq.method === "GET" && /^\/health/.test(clientReq.url)) {
    const health = JSON.stringify({
      status: "ok",
      target: TARGET,
      retry_max: CFG.retryMax,
      retry_base_sec: CFG.retryBaseSec,
      retry_max_sec: CFG.retryMaxSec,
      retryable_status: [...RETRYABLE_STATUS],
      retryable_codes: [...RETRYABLE_CODES],
    });
    clientRes.writeHead(200, { "Content-Type": "application/json" });
    clientRes.end(health);
    return;
  }

  forwardRequest(clientReq, clientRes);
});

server.listen(PORT, () => {
  log("proxy started: http://localhost:" + PORT + " -> " + TARGET);
  log(
    "retry: max=" +
      CFG.retryMax +
      ", base=" +
      CFG.retryBaseSec +
      "s, cap=" +
      CFG.retryMaxSec +
      "s"
  );
  log(
    "retryable: status=" +
      [...RETRYABLE_STATUS].join("/") +
      " codes=" +
      [...RETRYABLE_CODES].join("/")
  );
  // PID for toggle script
  console.log(JSON.stringify({ pid: process.pid, port: PORT }));
});

server.on("error", (err) => {
  if (err.code === "EADDRINUSE") {
    log("port " + PORT + " in use, try --port");
    process.exit(1);
  }
  log("server error: " + err.message);
});

function log(msg) {
  const ts = new Date().toISOString().slice(11, 19);
  process.stderr.write("[retry-proxy " + ts + "] " + msg + "\n");
}