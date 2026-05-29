# Tavily MCP Plugin

AI-native web search and extraction via [Tavily API](https://tavily.com).

## 文件结构

```
.claude/plugins/tavily/
├── .claude-plugin/marketplace.json    # 插件市场元数据
├── README.md                          # 本文件
└── plugins/tavily/
    ├── .claude-plugin/plugin.json     # 插件定义（含 MCP 配置模板）
    ├── config.json                    # API Key + 工具清单
    └── skills/tavily-search/SKILL.md  # 使用说明
```

## 配置位置

| 项 | 位置 |
|----|------|
| API Key | `.claude/plugins/tavily/plugins/tavily/config.json` |
| MCP 注册 | 全局 `~/.claude.json` → `mcpServers.tavily` |
| 使用说明 | `.claude/plugins/tavily/plugins/tavily/skills/tavily-search/SKILL.md` |

## 安装/更新 Key

1. 编辑 `config.json` 中的 `api_key`
2. 同步更新全局配置：
   ```bash
   claude mcp add tavily -e TAVILY_API_KEY=<new-key> -- npx -y tavily-mcp
   ```
