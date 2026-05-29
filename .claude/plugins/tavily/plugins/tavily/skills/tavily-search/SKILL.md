---
name: tavily-search
description: 通过 Tavily MCP 进行网页搜索、内容提取、网站爬取和深度研究
---

# Tavily Search Skill

## 前置条件

Tavily MCP 服务需在全局 `~/.claude.json` 的 `mcpServers` 中配置：
```json
{
  "tavily": {
    "command": "npx",
    "args": ["-y", "tavily-mcp"],
    "env": { "TAVILY_API_KEY": "<your-key>" },
    "type": "stdio"
  }
}
```

API Key 存放在 `.claude/plugins/tavily/plugins/tavily/config.json`。

## 工具选择

| 场景 | 工具 | 说明 |
|------|------|------|
| 搜索摘要/关键词 | `mcp__tavily__tavily_search` | 支持 basic/advanced/fast/ultra-fast |
| 从 URL 提取内容 | `mcp__tavily__tavily_extract` | 支持 basic/advanced 深度 |
| 爬取网站多页 | `mcp__tavily__tavily_crawl` | 可配置 depth/breadth/domain |
| 生成网站地图 | `mcp__tavily__tavily_map` | 站点结构分析 |
| 深度研究 | `mcp__tavily__tavily_research` | 多源综合（mini/pro/auto） |

## 调用示例

### 搜索
```
mcp__tavily__tavily_search({
  query: "Python Pillow TIFF support",
  search_depth: "advanced",
  max_results: 5
})
```

### 提取网页
```
mcp__tavily__tavily_extract({
  urls: ["https://docs.python.org/3/library/struct.html"],
  extract_depth: "advanced"
})
```

### 深度研究
```
mcp__tavily__tavily_research({
  input: "Compare SQLite vs DuckDB for embedded analytics",
  model: "auto"
})
```

## 与 web-access skill 的关系

| | Tavily MCP | web-access (CDP) |
|--|--|--|
| 适合 | 搜索资料、提取摘要 | 登录态操作、爬动态页面 |
| 重量 | API 调用，轻 | 启动浏览器，重 |
| 登录态 | 无 | 有 |
| 默认选择 | IDE 中搜索资料 | 需要交互/登录时 |
