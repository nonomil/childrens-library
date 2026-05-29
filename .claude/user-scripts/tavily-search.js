#!/usr/bin/env node
/**
 * tavily-search.js — zero-dep Tavily search (bypasses npx/npm corruption)
 *
 * Usage:
 *   node tavily-search.js "search query"
 *   node tavily-search.js "query" --depth advanced --max 5
 *   node tavily-search.js "query" --json
 *
 * API Key source (priority):
 *   1. env var TAVILY_API_KEY
 *   2. project .mcp.json -> tavily.env.TAVILY_API_KEY
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "--help" || args[0] === "-h") {
  console.log('Usage: node tavily-search.js "query" [--depth basic|advanced] [--max N] [--json]');
  process.exit(0);
}

const query = args[0];
let depth = "basic";
let maxResults = 5;
let rawJson = false;

for (let i = 1; i < args.length; i++) {
  if (args[i] === "--depth" && args[i + 1]) { depth = args[++i]; }
  else if (args[i] === "--max" && args[i + 1]) { maxResults = parseInt(args[++i], 10); }
  else if (args[i] === "--json") { rawJson = true; }
}

function getApiKey() {
  if (process.env.TAVILY_API_KEY) return process.env.TAVILY_API_KEY;
  const mcpPath = path.join(process.cwd(), ".mcp.json");
  if (fs.existsSync(mcpPath)) {
    try {
      const mcp = JSON.parse(fs.readFileSync(mcpPath, "utf8"));
      return (mcp.mcpServers && mcp.mcpServers.tavily && mcp.mcpServers.tavily.env && mcp.mcpServers.tavily.env.TAVILY_API_KEY) || "";
    } catch (e) {}
  }
  return "";
}

const apiKey = getApiKey();
if (!apiKey) {
  console.error("[tavily-search] ERROR: TAVILY_API_KEY not found in env or .mcp.json");
  process.exit(1);
}

const payload = JSON.stringify({
  api_key: apiKey,
  query: query,
  max_results: maxResults,
  search_depth: depth,
  include_answer: true,
});

const req = https.request("https://api.tavily.com/search", {
  method: "POST",
  headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(payload) },
}, function(res) {
  let body = "";
  res.on("data", function(c) { body += c; });
  res.on("end", function() {
    try {
      const data = JSON.parse(body);
      if (rawJson) {
        console.log(JSON.stringify(data, null, 2));
        return;
      }
      if (data.answer) {
        console.log("\n## Answer\n" + data.answer + "\n");
      }
      const results = data.results || [];
      for (let i = 0; i < results.length; i++) {
        const item = results[i];
        console.log("### " + item.title);
        console.log("URL: " + item.url);
        console.log(item.content.substring(0, 800));
        console.log("---\n");
      }
      if (results.length === 0) {
        console.log("[tavily-search] No results found.");
      }
    } catch (e) {
      console.error("[tavily-search] Parse error:", e.message);
      console.error("Raw response:", body.substring(0, 500));
    }
  });
});

req.on("error", function(e) {
  console.error("[tavily-search] Request failed:", e.message);
});

req.write(payload);
req.end();
