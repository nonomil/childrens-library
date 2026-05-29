---
name: smoke-test
description: 验证 Codex 插件/MCP 连通性，确认协作流程可用
---

# 联通自检技能

## 触发方式

以下任一条件激活：

- 用户说"联通自检" / "smoke test" / "测试连通性"
- `pipeline-init` 完成后用户要求验证
- 用户要求确认 Codex 是否可用

## 执行步骤

### Step 1：确认项目状态

1. 读取 `pipeline/state.json`
2. 如文件不存在，先调用 `pipeline-init` 技能
3. 记录当前 `phase` 和 `codex_mode`

### Step 2：检测插件路径

如果 `codex_mode` 为 `plugin`：

- 执行 `/codex:setup` 检查插件状态
- 执行 `/codex:status` 查看后台任务
- 尝试最小调用验证连通性

记录结果。

### Step 3：检测 MCP 路径

如果 `codex_mode` 为 `mcp`：

- 调用 `mcp__codex__codex` 发送最小 prompt
- 检查返回是否正常
- 记录 threadId

记录结果。

### Step 4：检测 CLI 兜底

- 检查 `codex` CLI 是否安装：`codex --version`
- 检查是否已登录：`codex whoami`
- 记录结果

### Step 5：输出检测结果

```text
## 联通自检结果

| 检测项 | 状态 | 详情 |
|--------|------|------|
| codex-plugin-cc 插件 | ✅/❌ | ... |
| MCP (mcp__codex__codex) | ✅/❌ | ... |
| Codex CLI | ✅/❌ | ... |
| 当前模式 | plugin/mcp/none | ... |

结论：PASS / FAIL
```

## 常见问题处理

- 插件不可用 → 建议 `npm install -g @openai/codex && codex login`
- MCP 超时 → 检查 `codex mcp-server` 进程是否在运行
- CLI 未安装 → 提示安装命令
