---
name: codex-toolkit
description: 将项目 .claude/ 配置转换为 Codex CLI 兼容格式。支持插件市场和项目级转换。触发信号："导出 Codex"/"部署到 Codex"/"codex export"/"codex deploy"。
layer: ondemand
tags: [codex, export, deploy, agents]
---

# Codex Toolkit — .claude/ → Codex CLI 转换

将 `.claude/` 目录中的技能、代理、上下文转换为 Codex CLI 兼容的 `.agents/` 格式。

> **SSOT 原则:** Claude Code 侧为唯一真实来源，本技能只读不写。

## 两种模式

### 模式 A：项目级导出（codex-export）
直接扫描项目 `.claude/` 目录，转换为 `.agents/` 格式。适用于单个项目。

流程：Scan → Classification → Transform → Context Integration → Generation → Metadata

### 模式 B：插件市场部署（deploy-to-codex）
从 `.claude-plugin/marketplace.json` 读取插件配置，批量转换并生成 AGENTS.md。适用于插件分发。

流程：Discovery → Scan → Classification → Transform → Agent Conversion → Generation → AGENTS.md → Metadata

## 互換性分类

| 分类 | 含义 | 处理方式 |
|------|------|---------|
| PORTABLE | 完全兼容 | 直接转换 |
| PARTIAL | 部分 MCP 依赖 | 添加 CLI 回退说明 |
| MCP_ONLY | 仅 MCP 可用 | 参考用，添加警告 |
| DELEGATION_ONLY | 仅 Task/子代理 | 跳过，记录到非支持列表 |

## 触发判断

- 用户说"导出 Codex"/"codex export" → 模式 A
- 用户说"部署到 Codex"/"codex deploy" → 模式 B
- 存在 `.claude-plugin/marketplace.json` → 自动选模式 B
- 否则 → 模式 A

## 变换规则

### Frontmatter 处理
- **保持**：name, description
- **删除**：allowed-tools, user-invocable, model, disable-model-invocation, context, argument-hint
- **添加**：AUTO-GENERATED 注释（在 frontmatter 之后，不在之前）

### Body 处理
- 技能引用替换：`/skill-name` → `$skill-name`
- MCP_ONLY：文件开头添加警告 banner
- PARTIAL：MCP section 前插入 CLI 回退提示

## 输出

- `.agents/skills/{name}/SKILL.md` — 转换后的技能
- `.agents/AGENTS.md` — 技能目录（模式 B）
- `.agents/.codex-deploy-metadata.json` — 元数据

## 约束
- 只读不写源文件
- 每次执行覆盖之前的输出
- 生成后提供统计摘要
