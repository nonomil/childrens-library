---
name: smoke-test
description: Use when 需要验证 Codex 自身工作流是否闭环，围绕 AGENTS.md、docs/plan、taskctl、.codex/hooks、.codex/skills 和 .mcp.json 做本地冒烟测试。
layer: domain
tags: [codex, smoke-test, taskctl, hooks]
domain: testing
---

# Codex 主流程冒烟测试

这个技能只验证 Codex 自身主流程，不把外部 Claude bridge-lite 当默认前置条件。核心目标是确认：入口文档、控制面、hooks runtime、技能目录、MCP 配置和本地测试链路都能在当前项目或 `Codex_Template` 中独立跑通。

## 触发方式

- 用户说“smoke test”“联通自检”“验证 Codex_Template 是否能独立跑”
- 导出完成后，需要确认 `Codex_Template` 自己是闭环的
- 切到新目录后，需要快速判断当前 Codex 主流程有没有断

## 先看什么

1. `AGENTS.md`
2. `.codex/AGENTS.md`
3. `docs/plan/README.md`
4. `.codex/hooks.json`
5. `.mcp.json`

## 最小通过标准

### 1. 启动与入口

- 能执行 Windows bootstrap 前置检查
- `AGENTS.md`、`.codex/AGENTS.md`、`ENTRYPOINTS.md` 存在
- `docs/plan/PLAN.md`、`docs/plan/tasks/`、`docs/plan/MERGE_QUEUE.yaml` 存在

### 2. 控制面 CLI

```bash
python scripts/taskctl.py --help
python scripts/taskctl.py route -h
python scripts/taskctl.py review-split -h
python scripts/taskctl.py review-aggregate -h
```

这些命令至少要能正常打印帮助，说明当前任务控制面可进入。

### 3. Codex hooks runtime

- `.codex/hooks.json` 存在
- `.codex/hooks/runtime/` 与 `.codex/hooks/packs/` 非空
- `.codex/hooks/tests/` 能正常执行

```bash
python -m pytest .codex/hooks/tests -q
```

### 4. 控制面与守卫脚本

```bash
python -m pytest .claude/scripts/tests -q
```

这里覆盖：

- `taskctl`
- `queue_guard`
- `task_scope_guard`
- `doc_conflict_guard`
- `gate_exit_check`
- revision / graphify 相关脚本

### 5. Codex-native 技能与 MCP 配置

- `.codex/skills/README.md` 存在
- `.codex/skills/plan/`、`review/`、`execute/`、`smoke-test/` 存在
- `.mcp.json` 存在

可选补充检查：

```bash
uvx code-review-graph --help
```

## 推荐执行顺序

```bash
node -e "console.log(require('os').homedir())"
node <home_path>/.codex/superpowers/.codex/superpowers-codex bootstrap
python scripts/taskctl.py --help
python scripts/taskctl.py route -h
python -m pytest .claude/scripts/tests -q
python -m pytest .codex/hooks/tests -q
uvx code-review-graph --help
```

## 输出建议

建议按下表汇总：

| 模块 | 检查项 | 结果 | 备注 |
|------|--------|------|------|
| 入口 | `AGENTS.md` / `.codex/AGENTS.md` / `ENTRYPOINTS.md` | PASS/FAIL | ... |
| 控制面 | `scripts/taskctl.py` 帮助与路由命令 | PASS/FAIL | ... |
| hooks | `.codex/hooks.json` + `.codex/hooks/tests` | PASS/FAIL | ... |
| 技能 | `.codex/skills/` 关键目录 | PASS/FAIL | ... |
| MCP | `.mcp.json` / `uvx code-review-graph --help` | PASS/FAIL | ... |

## 非默认范围

以下内容只有用户明确要求时才纳入当前 smoke test：

- `bridge-lite` 的真实外部 Claude provider 调用
- `claude-code-mcp` / `claude-cli-direct` 的 runtime 探测
- 任何依赖外部账号、网络或第三方 CLI 状态的检查

## 不要这样做

- 不要再把旧 `pipeline` 状态文件当 smoke test 起点
- 不要再依赖旧插件式 setup/status 命令或旧 MCP 检测入口当 Codex 主线检测入口
- 不要把外部 bridge-lite 失败误判成 Codex 本地主流程失败
