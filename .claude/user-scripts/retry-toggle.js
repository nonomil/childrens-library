#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const { spawn, execSync } = require("child_process");
const os = require("os");

var PROXY_PORT = 3458;
var HOME = os.homedir();
var SETTINGS = path.join(HOME, ".claude", "settings.json");
var BACKUP = path.join(HOME, ".claude", "settings.json.retry-proxy-backup");
var PID_FILE = path.join(HOME, ".claude", "retry-proxy.pid");
var LOG_FILE = path.join(HOME, ".claude", "retry-proxy.log");
var OUT_LOG = path.join(HOME, ".claude", "retry-proxy.out.log");
var PROXY_SCRIPT = path.join(__dirname, "retry-proxy.js");

function log(m) { console.log("[retry-toggle] " + m); }
function readJSON(f) { return JSON.parse(fs.readFileSync(f, "utf8")); }
function writeJSON(f, o) { fs.writeFileSync(f, JSON.stringify(o, null, 2)); }

function sleep(ms) {
  var t = Date.now();
  while (Date.now() - t < ms) {}
}

function getPidOnPort(port) {
  try {
    if (process.platform !== "win32") return null;
    var out = execSync("netstat -ano | findstr \":" + port + " \"", {
      encoding: "utf8", stdio: ["pipe", "pipe", "pipe"]
    });
    var lines = out.split("\n").filter(function(l) {
      return l.indexOf("LISTENING") >= 0;
    });
    for (var i = 0; i < lines.length; i++) {
      var m = lines[i].trim().match(/\s+(\d+)\s*$/);
      if (m) return parseInt(m[1], 10);
    }
  } catch (e) {}
  return null;
}

function isProxyHealthy() {
  try {
    execSync("curl -sf http://localhost:" + PROXY_PORT + "/health", {
      stdio: "pipe", timeout: 1500
    });
    return true;
  } catch (e) { return false; }
}

function isProxyProcess(pid) {
  try {
    var out = execSync("wmic process where \"ProcessId=" + pid + "\" get CommandLine /format:list", {
      encoding: "utf8", stdio: ["pipe", "pipe", "pipe"]
    });
    return out.indexOf("retry-proxy.js") >= 0;
  } catch (e) { return false; }
}

function killPid(pid) {
  try { execSync("taskkill /PID " + pid + " /F /T", { stdio: "pipe" }); } catch (e) {}
}

function baseUrl(s) {
  try { var u = new URL(s); return u.protocol + "//" + u.host; } catch (e) { return ""; }
}

function startProxy(target) {
  log("Starting proxy -> " + target);
  var cmd = "start /b \"\" \"" + process.execPath + "\" \"" + PROXY_SCRIPT +
    "\" --port " + PROXY_PORT + " --target " + target +
    " > \"" + OUT_LOG + "\" 2> \"" + LOG_FILE + "\"";
  spawn("cmd", ["/c", cmd], { windowsHide: true, detached: false, stdio: "ignore" });

  for (var i = 0; i < 15; i++) {
    sleep(400);
    if (isProxyHealthy()) {
      var pid = getPidOnPort(PROXY_PORT);
      if (pid) fs.writeFileSync(PID_FILE, String(pid));
      log("Proxy started (port " + PROXY_PORT + ")" + (pid ? " PID: " + pid : ""));
      return;
    }
  }
  log("WARNING: health check not passed within 6s");
  var pid2 = getPidOnPort(PROXY_PORT);
  if (pid2) fs.writeFileSync(PID_FILE, String(pid2));
}

function doEnable() {
  console.log("");
  log("=== Enable Retry Proxy ===");
  if (!fs.existsSync(PROXY_SCRIPT)) { log("ERROR: " + PROXY_SCRIPT + " not found"); process.exit(1); }
  if (!fs.existsSync(SETTINGS)) { log("ERROR: " + SETTINGS + " not found"); process.exit(1); }

  var cfg = readJSON(SETTINGS);
  var cur = (cfg.env && cfg.env.ANTHROPIC_BASE_URL) || "";
  var target = baseUrl(cur) || "https://open.bigmodel.cn";

  if (!fs.existsSync(BACKUP)) {
    fs.copyFileSync(SETTINGS, BACKUP);
    log("Backed up: " + BACKUP);
  } else {
    log("Backup exists, skipping");
  }

  var pidOnPort = getPidOnPort(PROXY_PORT);
  if (pidOnPort && isProxyHealthy()) {
    log("Proxy already running (PID: " + pidOnPort + ")");
  } else if (pidOnPort) {
    log("ERROR: port " + PROXY_PORT + " occupied by PID " + pidOnPort);
    log("Free the port first, or: node retry-toggle.js disable");
    process.exit(1);
  } else {
    startProxy(target);
  }

  if (cfg.env && cfg.env.ANTHROPIC_BASE_URL) {
    cfg.env.ANTHROPIC_BASE_URL = cfg.env.ANTHROPIC_BASE_URL.replace(
      /^https?:\/\/[^\/]+/, "http://localhost:" + PROXY_PORT
    );
    cfg.env.CLAUDE_CODE_MAX_RETRIES = "10";
    writeJSON(SETTINGS, cfg);
    log("Config: " + cfg.env.ANTHROPIC_BASE_URL);
  }

  console.log("");
  log("Enabled! Restart Claude Code / VS Code to apply.");
  log("Emergency: node retry-toggle.js disable");
  console.log("");
}

function doDisable() {
  console.log("");
  log("=== Disable Retry Proxy ===");
  var killed = false;
  var pidOnPort = getPidOnPort(PROXY_PORT);

  if (pidOnPort) {
    killPid(pidOnPort);
    log("Stopped (PID: " + pidOnPort + ")");
    killed = true;
  }

  if (fs.existsSync(PID_FILE)) {
    try {
      var pid = parseInt(fs.readFileSync(PID_FILE, "utf8").trim(), 10);
      if (pid && pid !== pidOnPort && isProxyProcess(pid)) {
        killPid(pid);
        log("Stopped (PID: " + pid + ")");
        killed = true;
      }
    } catch (e) {}
    try { fs.unlinkSync(PID_FILE); } catch (e) {}
  }

  if (!killed) log("Proxy not running");

  if (fs.existsSync(BACKUP)) {
    fs.copyFileSync(BACKUP, SETTINGS);
    fs.unlinkSync(BACKUP);
    log("Config restored from backup");
  } else if (fs.existsSync(SETTINGS)) {
    var cfg = readJSON(SETTINGS);
    if (cfg.env && cfg.env.ANTHROPIC_BASE_URL) {
      cfg.env.ANTHROPIC_BASE_URL = cfg.env.ANTHROPIC_BASE_URL.replace(
        /^http:\/\/localhost:\d+/, "https://open.bigmodel.cn"
      );
      writeJSON(SETTINGS, cfg);
      log("URL restored: " + cfg.env.ANTHROPIC_BASE_URL);
    }
  }

  console.log("");
  log("Disabled! Restart Claude Code / VS Code to apply.");
  console.log("");
}

function doStatus() {
  console.log("");
  console.log("=== Retry Proxy Status ===");
  var ok = isProxyHealthy();
  var pid = getPidOnPort(PROXY_PORT);

  if (ok) log("Proxy: RUNNING (port " + PROXY_PORT + ")" + (pid ? " PID: " + pid : ""));
  else if (pid) log("Proxy: PORT OCCUPIED, health failed (PID: " + pid + ")");
  else log("Proxy: NOT RUNNING");

  log("Config: " + (fs.existsSync(BACKUP) ? "PROXY MODE" : "DIRECT MODE"));

  if (fs.existsSync(SETTINGS)) {
    try {
      var cfg = readJSON(SETTINGS);
      console.log("  URL: " + ((cfg.env && cfg.env.ANTHROPIC_BASE_URL) || "not set"));
    } catch (e) { console.log("  URL: read error"); }
  }
  console.log("");
}

function showUsage() {
  console.log("");
  console.log("API Retry Proxy Toggle");
  console.log("  node retry-toggle.js enable   - start proxy + switch config");
  console.log("  node retry-toggle.js disable  - stop proxy + restore config");
  console.log("  node retry-toggle.js status   - show state");
  console.log("");
}

var cmd = (process.argv[2] || "").toLowerCase();
if (cmd === "enable" || cmd === "on" || cmd === "1") doEnable();
else if (cmd === "disable" || cmd === "off" || cmd === "0") doDisable();
else if (cmd === "status" || cmd === "show" || cmd === "s") doStatus();
else showUsage();
