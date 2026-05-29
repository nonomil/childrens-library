# workflow-constants.md — 全局核心约束

此文档只保留所有 workflow 都会共享的最小常驻规则。
为降低按需加载成本，项目配置与偏好、运行治理、工具生态已拆分到独立子文档：

- `claude-workflow-config.md`
- `claude-workflow-governance.md`
- `claude-workflow-ecosystem.md`

模板共享配置入口是 `.claude/settings.json`，`.claude/settings.local.json` 只用于本机覆写。

---

## 1. Codex 调用核心约束（不可变）

> 具体 Prompt 结构、上下文注入和 Prompt 资产规则见 `claude-workflow-governance.md`。

### 路径 A：codex-plugin-cc（插件，推荐）

适用环境：CLI 终端 / VS Code 扩展 / Desktop App（安装后需重启 Claude Code）

AI 可直接调用的命令：

```text
/codex:rescue <任务描述>
/codex:status
/codex:result
```

AI 触发 review 时，统一走封装脚本：

```bash
bash .claude/scripts/codex-review.sh
bash .claude/scripts/codex-review.sh adversarial
```

脚本失败时，自动降级到路径 B（MCP）。

### 路径 B：MCP（通用）

适用环境：VS Code 扩展 / CLI 终端 / Desktop App

首次调用：

```javascript
mcp__codex__codex({
  model: "gpt-5.4",
  sandbox: "danger-full-access",
  "approval-policy": "on-failure",
  reasoning: "high" | "medium" | "low",
  prompt: "<结构化 Prompt>"
})
```

后续调用：

```javascript
mcp__codex__codex-reply({
  threadId: "<保存的 ID>",
  prompt: "<下一步>"
})
```

### 必填参数（两路径共用）

| 参数 | 值 | 说明 |
|------|----|------|
| `model` | `gpt-5.4` | 模型 |
| `sandbox` | `danger-full-access` | 权限 |
| `approval-policy` | `on-failure` | 审批策略 |
| `reasoning` | `high / medium / low` | 按任务类型选择 |

`reasoning` 选择规则：

| 任务类型 | 推理强度 |
|---------|----------|
| 代码审查 / Bug 根因分析 / 实施计划编写 | `high` |
| 复杂重构 / 跨模块改动 | `medium` |
| 直接编码 / 小改动 / 并行执行子任务 | `low` |

---

## 2. 文件操作边界与删除禁令（不可变）

风险原则：

- `danger-full-access` 是调用权限，不等于允许无边界文件操作
- 每次调用都必须同时依赖 Prompt 约束、Hook 拦截、CC 验收三层防护

CC 发给 Codex 的 Prompt 必须包含：

```text
Scope: Only modify files under [当前 worktree 绝对路径]
Forbidden: Do not modify, delete, or move files outside this directory
Forbidden: Do not run rm -rf, del, rd /s, Remove-Item -Recurse, git clean -f, git reset --hard
Forbidden: Do not modify .git/ or config files outside project root
```

CC 验收命令：

```bash
git diff --name-only HEAD
```

验收规则：
- 改动文件必须全部位于本次任务 Scope 内
- 发现范围外改动，立即中止，不得 commit
- 删除类命令由 Hook 统一以 exit code `2` 阻断

---

## 3. Git 安全与角色边界（不可变）

### 禁止操作（未获用户明确批准）

- `git stash`
- `git reset --hard`
- `git push --force`
- `git checkout .`
- `git clean -f`

### 必须执行的门禁

创建 worktree 前：

```bash
git status --short
```

合并前：

```bash
git diff --stat [base-branch]...HEAD
```

并行任务额外门禁：

```bash
python .claude/scripts/verify_parallel_scope.py \
  --table docs/development/[feature]-impact-scope.md \
  --task [task-id] \
  --base [MAIN_BRANCH]
```

### 角色边界

| 角色 | 必须做 | 不应承担 |
|------|--------|----------|
| CC（Claude Code） | 规划、搜索、决策、复杂度判断、工作流路由、代码审查 | 复杂业务代码生成、跨文件大改 |
| Codex | 代码生成、修改、重构、深度代码审查、测试编写、大型代码库扫描 | 需求裁决、工作流路由 |

---

## 4. 工作流路由优先级与确认门禁（不可变）

路由优先级从高到低：

1. Debug
2. 对抗式协作
3. 多专家评审
4. Code Review
5. C++ Build
6. C++ Test
7. 研究调研
8. 大型代码库
9. 并行开发
10. 复杂开发
11. 简单开发

规则：
- 优先级高的流程优先匹配
- 一旦命中，不再检查低优先级
- 复杂开发不能吞掉专用流程

用户确认词：

| 词 | 含义 | 后续行动 |
|----|------|----------|
| “确认” / “开始” / “可以” | 同意当前方案 | 进入执行阶段 |
| “不用扫描，直接改” | 跳过 Phase 0 | 直接进入 Phase 1 |
| “先扫一下” / “先了解结构” | 触发扫描 | 执行扫描 |
| “直接开始” | 跳过所有预检 | 仅简单模式允许 |

强制门禁：

| 门禁 | 触发条件 | 处理 |
|------|---------|------|
| 需求讨论 | 任何新任务 | 必须复述需求、列出歧义、等用户确认 |
| 复杂度判断 | 任何新任务 | 必须判断并说明走哪个流程 |
| 创建 worktree | 任何分支工作 | 必须先 `git status`，处理脏仓 |
| 合并前确认 | 任何 merge / PR | 必须输出变更摘要，等用户确认 |
| 扫描质量检查 | largebase 扫描完成 | 必须验证 00-06 产物完整性 |

---

## 5. 引用与按需加载规则

工作流文档应优先引用本文档或按需子文档，不复制长规则。

推荐引用方式：

```markdown
> 参见 `claude-workflow-constants.md` 中的「Codex 调用核心约束」
> 参见 `claude-workflow-config.md` 中的「用户偏好」
> 参见 `claude-workflow-governance.md` 中的「验证完成门禁」
```

按需子文档索引：

| 文档 | 何时加载 |
|------|----------|
| `claude-workflow-config.md` | 初始化、迁移、并行协作、偏好分流 |
| `claude-workflow-governance.md` | 验证收口、lessons、Prompt 资产、context 治理 |
| `claude-workflow-ecosystem.md` | 调研插件 / Skill / Hook 叠加方案 |

---

## 版本历史

- 2025-02-26：初版，统一全局硬约束
- 2026-04-07：将项目配置、运行治理、工具生态从 constants 拆分为按需子文档
- 2026-04-07：明确 `.claude/settings.json` 为共享入口，`.claude/settings.local.json` 为本机覆写
