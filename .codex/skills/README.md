# 技能文件指南

本目录包含 Claude Code + Codex 协作流水线中使用的自定义技能。

> 技能分为两侧：`.claude/skills/`（Claude Code 主控侧）和 `.codex/skills/`（Codex 执行侧）。

---

## Claude Code 侧技能（`.claude/skills/`）

### 流水线核心

| 技能 | 触发方式 | 说明 |
|------|---------|------|
| `orchestrate` | "跑流水线" / "orchestrate" | 7 步流水线总调度（规划→审查→实现→审核→测试→报告→完成） |
| `plan` | "生成计划" / "拆任务" | 需求拆解为独立任务单元，标注负责 agent 和依赖关系 |
| `plan-checklist` | 计划清单 | 将讨论结论沉淀为可执行计划文档和打钩清单 |
| `review` | "审查当前改动" / "review" | 审核代码逻辑、安全性、向后兼容，输出 PASS/FAIL |
| `report` | "生成测试报告" / "汇总结果" | 汇总任务状态、审核记录、测试结果，生成最终报告 |
| `pipeline-init` | "初始化 pipeline" | 创建 pipeline/ 目录 + state.json，检测 Codex 可用性 |
| `smoke-test` | "联通自检" / "smoke test" | 验证 Codex 插件/MCP/CLI 连通性 |

### 代码库扫描与文档

| 技能 | 触发方式 | 说明 |
|------|---------|------|
| `largebase-structured-scan` | "先扫描" / "结构化扫描" / "大型代码库" | 大型代码库结构化扫描（8 子命令），输出 00-06 扫描包 + scan.db + 项目综述 |
| `doc-gen` | "看不懂/解释/总结/报告/方案/变更/扫描报告" | 结构化文档生成，5 种模式：explain·report·change·design·scan，图表优先排版 |
| `doc-sync` | 文档同步 | 代码变更后系统性同步文档 |
| `project-init` | `/project-init` | 分析项目结构，生成 claude-template.md |

### 日常工具

| 技能 | 触发方式 | 说明 |
|------|---------|------|
| `commit` | `/commit` | 规范化 git commit，生成 Conventional Commits 消息 |
| `changelog` | `/changelog` | 基于近期提交生成或更新 CHANGELOG |
| `git` | `/git` | Git 版本管理（save/checkpoint/history/restore/status） |
| `memory` | "记忆/回忆/remember" / Grep `.claude/memory/` | 跨会话 Markdown 记忆系统（CC 原生，零外部依赖） |

---

## Codex 侧技能（`.codex/skills/`）

### 流水线执行

| 技能 | 说明 |
|------|------|
| `execute` | 执行 Claude Code 下发的实现任务，返回结构化结果 |
| `test` | 运行测试套件，修复失败用例（最多 2 轮） |

### 通用工具

| 技能 | 说明 |
|------|------|
| `memory-system` | 跨会话语义搜索记忆（SQLite + 向量 + 全文混合搜索） |
| `windows-shell-fallback` | Windows 环境命令失败排查与回退指南 |
| `doc-sync` | 代码变更后系统性同步文档的规范流程 |
| `plan-checklist` | 将讨论结论沉淀为可执行计划文档和打钩清单 |
| `cpp-build` | C++ 项目编译（CMake / MSBuild） |
| `cpp-unit-test` | C++ 单元测试（Google Test / CTest） |

### 专业领域

| 技能 | 说明 |
|------|------|
| `industrial-ui-design` | 工业 UI 设计规范（Qt/PySide/PyQt），含参考手册 |
| `ui-ux-design-guide` | UI/UX 设计指南（配色、字体、图表、UX 规范） |
| `algorithm-spec-review` | 算法规格包审查，核对规格与实现一致性 |
| `ui-screenshot-audit` | Web 应用截图审查，生成带证据的 Markdown 报告 |

---

## 流水线调用路径

所有 Codex 调用支持双路径（由 CLAUDE.md 强制门禁 Step 3 确定）：

**插件路径**（CLI / VS Code 终端）：
```text
/codex:review --background        # 审查
/codex:adversarial-review          # 对抗审查
/codex:rescue <任务描述>           # 执行任务
/codex:status                      # 查看状态
/codex:result                      # 读取结果
```

**MCP 路径**（VS Code 扩展 / Desktop App）：
```javascript
mcp__codex__codex({ model: "gpt-5.4", sandbox: "danger-full-access",
  "approval-policy": "on-failure", prompt: "..." })
```

**CLI 兜底**（插件和 MCP 均不可用时）：
```bash
codex exec -m gpt-5.4 "..."
```

---

## 流水线状态协议

文件位置：`pipeline/state.json`

阶段：`idle` → `planning` → `reviewing_plan` → `executing` → `reviewing_code` → `testing` → `reporting` → `done`

任务状态：`planned` → `pending` → `in_progress` → `completed` / `blocked`

---

## 技能管理

### 添加新技能
1. 在对应目录下创建 `[name]/SKILL.md`
2. 包含 frontmatter：`name` 和 `description`
3. 在本文档中记录

### 文件命名约定
- `.claude/skills/`：使用 `SKILL.md`（大写）
- `.codex/skills/`：使用 `SKILL.md`（大写）或 `skill.md`（小写均可）

---

## 相关文档

- `../workflows/claude-workflow-constants.md` — 全局约束与 Codex 调用规范
- `../workflows/claude-workflow-complex.md` — 复杂开发工作流
- `../README.md` — .claude 目录完整指南
- `../../pipeline/state.json` — 流水线状态文件
