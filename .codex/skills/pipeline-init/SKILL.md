---
name: pipeline-init
description: Pipeline 初始化，补齐治理文件、建立状态协议并确认 Codex 可用性
---

# Pipeline 初始化技能

## 触发方式

以下任一条件激活：

- 用户说"初始化 pipeline" / "初始化流水线"
- 用户首次提出开发需求且 `pipeline/state.json` 不存在
- `orchestrate` 技能检测到 pipeline 不存在时自动调用

## 执行步骤

### Step 1：扫描项目

执行最小必要扫描，确认：

- 项目名
- 技术栈
- 主要源码目录
- 构建命令
- 测试命令

向用户展示扫描摘要，再继续初始化。

### Step 2：补齐 `AGENTS.md`

如果项目根目录不存在 `AGENTS.md`，生成最小可用版本。

要求：

- 不要留下占位语
- 必须包含协作模式、文件所有权、状态协议、统一结果标签、安全规则
- 写明双路径调用：插件优先 + MCP 备选

最小骨架：

```markdown
# {项目名} 协作规范

## 协作模式
- Claude Code：主控 + 审查
- Codex：实现 + 测试
- 调用路径：插件优先（codex-plugin-cc）+ MCP 备选

## 项目信息
- 项目名：{推断结果}
- 技术栈：{推断结果}
- 构建命令：{推断结果}
- 测试命令：{推断结果}

## 文件所有权
- pipeline/plan.md：Claude 写，Codex 读
- pipeline/state.json：Claude 写，Codex 读
- pipeline/review_log.md：Claude 写，Codex 读
- pipeline/test_report.md：Claude 写，Codex 读

## 状态协议
- phase: idle/planning/reviewing_plan/executing/reviewing_code/testing/reporting/done
- task status: planned/pending/in_progress/completed/blocked
```

### Step 3：初始化 Pipeline

创建 `pipeline/` 目录（如不存在），写入初始文件。

1. `pipeline/state.json`

```json
{
  "version": "1.1",
  "project": "{项目名}",
  "phase": "idle",
  "requirement": "",
  "plan_version": 0,
  "plan_ready": false,
  "codex_mode": "",
  "build_command": "{推断结果}",
  "test_command": "{推断结果}",
  "tasks": [],
  "pending_tasks": [],
  "completed_tasks": [],
  "blocked_tasks": [],
  "review_rounds": {},
  "last_updated": "{当前日期}"
}
```

2. `pipeline/plan.md`（空模板）
3. `pipeline/review_log.md`（空模板）
4. `pipeline/test_report.md`（空模板）

### Step 4：确认 Codex 可用性

按 CLAUDE.md 强制门禁 Step 3 的三层决策逻辑执行：

1. 检测插件是否可用（尝试 `/codex:setup`）
2. 检测 MCP 是否可用（检查 `mcp__codex__codex` 工具）
3. 根据检测结果：
   - 插件可用 → 推荐 `codex_mode: "plugin"`
   - 仅 MCP 可用 → 推荐 `codex_mode: "mcp"`
   - 都不可用 → `codex_mode: "none"`，CC 独立完成
4. 将选择写入 `pipeline/state.json.codex_mode`

### Step 5：输出初始化结果

向用户展示：

```text
已初始化：
- AGENTS.md
- pipeline/state.json
- pipeline/plan.md
- pipeline/review_log.md
- pipeline/test_report.md

已确认：
- 项目名
- 技术栈
- 构建命令 / 测试命令
- Codex 调用方式：plugin / mcp / none

下一步：
直接提出需求，协作流水线会按默认模式启动。
```
