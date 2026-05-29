# 项目记忆系统（.claude/memory/）

> 三层架构中的 **Layer 2 · 项目记忆层**。
> 进 git，团队共享，CC 自动读写。

---

## 定位

| 层级 | 位置 | 职责 | 维护者 |
|------|------|------|--------|
| Layer 1 个人层 | `~/.claude/projects/<hash>/MEMORY.md` | 个人行为约束 | 用户 + CC |
| **Layer 2 项目记忆** | **`.claude/memory/`**（本目录） | **项目知识、经验教训、变更记忆** | **CC 自动读写** |
| Layer 3 规范层 | `.claude/rules/` | 静态规范、项目约束 | 人工维护 |

**核心原则**：
- 写入只写 `.claude/memory/`，不写 `.claude/rules/`
- 检索用 `Grep { pattern: "关键词", path: ".claude/memory/" }`
- 体积控制：<300 行正常追加，≥300 行提示清理，≥500 行建议拆分

---

## 目录结构

```
.claude/memory/
├── lessons/              ← 踩坑经验（高频使用）
│   ├── codex.md              Codex 调用经验
│   └── workflow.md           工作流教训
├── context/              ← Changelog AI 轨（与 docs/changes/ 同名，内容不同）
│   └── 0001-日期-hash-标题.md    结构化变更记忆（frontmatter + 技术决策 + 边界 + 注意事项）
├── decisions/            ← 架构决策（按需写入）
├── constraints/          ← 项目约束发现（按需写入）
├── patterns/             ← 可复用实现模式（按需写入）
├── prompts/              ← 成功 Prompt 模板（经验证后沉淀）
├── user-prefs.md         ← 用户偏好（沟通风格、技术偏好、工作习惯）
├── debug-history.md      ← Bug 根因记录（按需创建）
├── architecture-decisions.md  ← 架构决策摘要（按需创建）
└── index.md              ← 索引文件（自动维护）
```

---

## 写入触发（自动，无需用户指令）

| 触发时机 | 写入目标 | 来源 |
|----------|---------|------|
| Bug 修复完成 | `debug-history.md` 或 `lessons/` | debug workflow |
| 架构决策完成 | `decisions/` 或 `architecture-decisions.md` | plan workflow |
| Review 通过 + 提交后 | `context/序号-日期-hash-标题.md` | changelog 双轨 |
| Prompt 成功输出 | `prompts/` | constants.md Prompt 沉淀规则 |
| 用户纠正 AI 错误 | `lessons/` | memory skill |
| 用户说"记住/下次注意" | 对应主题文件 | memory skill |
| 发现可复用模式 | `patterns/` | memory skill |
| 发现非显而易见约束 | `constraints/` | memory skill |

---

## 审计机制

- **触发**：用户说"审计记忆" / 每月提醒
- **步骤**：Glob 列出所有文件 → Read 检查过时/矛盾条目 → 列出建议 → 等用户确认
- **绝不自动删除**，只归档到 `archive/`

---

## 与其他目录的关系

| 目录 | 关系 |
|------|------|
| `.claude/rules/` | 规范层（人工维护），本目录是知识层（CC 自动） |
| `.claude/skills/memory/` | 记忆操作技能定义（协议），本目录是数据 |
| `docs/changes/` | Changelog 人看轨，本目录 `context/` 是 AI 看轨 |
| `ref/记忆与优化/` | 参考文档，不影响本目录运行 |

---

## 配套文件

- 技能定义：`.claude/skills/memory/skill.md`
- 工作流引用：`.claude/workflows/claude-workflow-constants.md`（Prompt 沉淀规则）
- 主入口路由：`CLAUDE.md`（门禁 Step 4.5）
