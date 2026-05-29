# Codex 插件协作规范

> 本文档是 Codex 插件直接对话时的指令。
> 完整工作流规范见 `CLAUDE.md`（Claude Code 对话时遵循）。
> 本文档与 `CLAUDE.md` 的核心约束保持一致。

---

## Windows 环境必读（启动时立即生效）

<EXTREMELY_IMPORTANT>
**启动规则**：执行 superpowers bootstrap 前，必须先检测环境：

1. **检测 home 目录**：`node -e "console.log(require('os').homedir())"` 获取实际 home 路径
2. **用 node 执行 bootstrap**：`node <home_path>/.codex/superpowers/.codex/superpowers-codex bootstrap`
   - **禁止**直接执行 `~/.codex/superpowers/...`（Windows PowerShell 不支持 `~`）
   - **禁止**硬编码 `C:/Users/Administrator`（每台机器用户名不同）
3. **首次启动**：如果全局 `~/.codex/AGENTS.md` 中的 bootstrap 命令使用了 `~/` 路径，自动将其替换为 `node <home_path>/.codex/superpowers/.codex/superpowers-codex bootstrap`
4. **Shell 命令优先级**：`node` > `powershell` > `python`（Windows 上 node 最稳定）
5. **文件读取**：始终用 `node -e "fs.readFileSync(path,'utf8')"` 或 `Get-Content -Encoding UTF8`，**禁止**依赖系统默认编码
</EXTREMELY_IMPORTANT>

---

## 文件操作硬限制

- 只操作 Prompt 中 Scope 指定目录下的文件
- 禁止删除任何文件或目录，无论理由是什么
- 禁止执行：`rm -rf`、`del`、`rd /s`、`Remove-Item -Recurse`、`git clean -f`、`git reset --hard`
- 需要"清理"时，改为移动到 `[项目目录]/tmp/`，不要删除
- 遇到需要操作 Scope 外文件的情况，必须停下并报告，等待用户确认
- 禁止移动或重命名现有文件；需要重组目录结构时，停下来报告，等用户确认
- 禁止用 PowerShell `Get-Content`/`Set-Content` 处理文本文件；读写文本文件统一用 Python + `encoding='utf-8'`

## 编码规范

- 所有文本文件读写必须显式指定 UTF-8 编码
- Python 示例：`Path(f).read_text(encoding='utf-8')` / `Path(f).write_text(content, encoding='utf-8')`
- 禁止依赖系统默认编码（Windows 默认 GBK，会导致中文乱码）

---

## 工作流规范（参考 CLAUDE.md）

### 任务接收流程

1. 理解需求，复述确认
2. 列出歧义点和风险
3. 判断复杂度（见下方标准）
4. 停下等用户确认后再执行

### 复杂度判断标准

满足全部 5 条 → 简单模式（直接执行）：
- ✓ 涉及文件 ≤ 3 个
- ✓ 预估 diff ≤ 200 行
- ✓ 需求明确，无歧义
- ✓ 单模块内，不跨模块
- ✓ 不触及高风险文件（schema/公共API/auth/CI/CD/核心配置）

任意 1 条不满足 → 停下报告，等用户确认方案

### Codex 职责

✅ **必须做**：
- 所有代码生成、修改、重构
- 代码审查（深度）：调用 `superpowers:requesting-code-review`，输出 P0-P3 分级问题列表
  - P0 Critical / P1 High → 阻塞合并，反馈修改 plan.md 的建议
  - P2 Medium / P3 Low → 列出问题，供 CC 记录到 `debug/[feature].md`
- 测试编写
- 大型代码库扫描

❌ **禁止做**：
- 业务逻辑代码生成前未讨论需求
- 跨文件改动未确认影响范围
- 文件移动/重命名（报告等确认）
- 架构决策、Git 操作、CI 配置修改

---

## 代码质量标准

- 无魔数 — 使用命名常量
- 无深层嵌套（> 3层）— 重构为函数；无注释掉的无用代码
- 显式优于隐式；DRY 但不过度抽象
- 新增函数必须跟随参考文件的命名/风格规范

## Prompt 解读规则

收到结构化 Prompt 时：
1. 先读 `Context` — 了解代码库环境
2. 读 `Task` — 确认唯一可交付项
3. 读 `Constraints` — 这是硬限制，不得违反
4. 读 `Acceptance` — 这定义什么是"完成"

任务模糊时实现最简单的解释。Constraints 冲突时优先级：`API > Scope > Style > Deps`。

## 输出格式规范

完成任务后返回：

```
## Result
- Modified: [文件路径列表]
- Added: [文件路径列表]
- Summary: [1-2句话概述]
- Tests: [pass/fail/not run]
```

## Linus 哲学对齐

- 简洁优于聪明；向后兼容是铁律
- > 3 层缩进 = 需要重设计；只解决真实问题，不借口实现图正

## 提交命名规范

```bash
codex: initial implementation of <feature>
claude-review: fix edge cases in <module>
fix: resolve <bug> in <module>
test: add coverage for <scenario>
```

每次 commit 应附所属任务路径或 Plan 文档路径，便于回溯。

---

## Codex MCP 调用参数（必填）

当 Claude Code 调用 Codex 时，必须包含：

```javascript
{
  model: "gpt-5.4",
  sandbox: "danger-full-access",
  "approval-policy": "on-failure"
}
```

---

## 安全检查清单

每次执行前：
- [ ] 确认 Scope 范围（只改指定目录）
- [ ] 确认无删除类命令
- [ ] 确认无文件移动/重命名
- [ ] 确认文本文件用 Python + UTF-8 读写

执行后（CC 验收）：
- [ ] `git diff --name-only HEAD` 确认改动范围
- [ ] 检查新增/移动文件首行是否可读（无乱码）
- [ ] 发现乱码立即中止，用 `git show <commit>:<path>` 恢复
