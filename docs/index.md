# 项目文档导航

> docs/ 目录总索引，链接到所有子目录。

---

## 目录结构

| 目录 | 用途 | 读者 |
|------|------|------|
| [plan/](plan/) | 开发计划文档 | 开发者、AI |
| [scan/](scan/) | 代码库扫描产物 | AI |
| [changes/](changes/) | 变更记录（Changelog） | 开发者、PM、运维 |
| [prd/](prd/) | 产品需求文档 | 开发者、PM |
| [arch/](arch/) | 架构决策记录（ADR） | 开发者 |
| [api/](api/) | 本地 API 文档库 | AI |

## 根级文档

| 文件 | 说明 |
|------|------|
| `CODEBASE_MAP.md` | 代码库结构地图（扫描产物） |
| `project-overview.md` | 项目综述（面向人类读者） |

## AI 专用记忆（不在 docs/ 下）

| 路径 | 用途 |
|------|------|
| `.claude/memory/lessons/` | 踩坑经验 |
| `.claude/memory/prompts/` | 成功 Prompt 模板 |
| `.claude/memory/context/` | AI 上下文变更记忆（与 changes/ 同名、内容不同） |
