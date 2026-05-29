# Skill 门禁协议（skill-gate-protocol）

> 解决的问题：AI agent 执行技能时只读 SKILL.md 前半部分，跳过后半部分的验证门禁，
> 导致产出不达标（如 largebase-structured-scan 跳过 doc-gen 校验，产出纯表格无图表）。

---

## 核心规则：MANDATORY GATES 摘要块

每个含验证步骤的 SKILL.md，**必须**在 frontmatter 之后、正文标题之前（第 8-9 行之间）
插入 `## MANDATORY GATES` 摘要块：

```markdown
## MANDATORY GATES

> 执行本技能前，必须先输出本摘要块全部内容作为确认。未输出 = 未开始。

| # | 门禁点 | 位置 | 通过条件 |
|---|--------|------|----------|
| G1 | [必须读取的章节] | Step X | 输出 `[OK] xxx` |
| G2 | [验证命令] | Step Y | 退出码 = 0 |
| G3 | [校验清单] | Step Z | 全部 checklist 通过 |
```

**规则**：
- 摘要块不超过 8 行（含标题和规则行）
- 门禁点数量 2-5 条，按执行顺序排列
- "位置"指向 SKILL.md 内的章节锚点（如 `### Step 2`）
- 执行时 agent 必须 echo-back 摘要块内容，否则视为未启动

---

## 三层防护机制

### 第一层：首因效应（Front-Loading）

问题根因：AI agent 对长文档存在"注意力衰减"，只重视前 50 行。
对策：把最关键的门禁信息放到最前面。

**实施**：MANDATORY GATES 摘要块放在 SKILL.md 第 8 行（frontmatter 后第一行），
让 agent 在读取任何步骤前先看到全部约束。

### 第二层：Echo-Back 协议

执行技能前，agent **必须输出**以下内容：

```
[技能名] 门禁确认：
- 已读取章节：[列出读到的所有 ## 和 ### 标题]
- 门禁点：[复述摘要块中每个 G1/G2/G3 的通过条件]
- 状态：[READY / BLOCKED: 原因]
```

**规则**：
- 未输出 echo-back = 未开始执行，任何产出视为无效
- echo-back 中遗漏章节 = agent 未读完 SKILL.md，必须补读
- BLOCKED 状态必须说明原因并等待用户决策

### 第三层：程序化验证（Programmatic Gate）

有 `verify` 脚本或可执行校验命令的技能，用退出码做硬门禁：

```bash
# 示例：largebase-structured-scan
python .claude/skills/largebase-structured-scan/scan.py verify --dir ... --mode M4
```

**规则**：
- 退出码非 0 = 终止流程，不得进入下一步
- 验证命令写在摘要块的 G 行中
- 无程序化验证的技能，用 checklist 代替（agent 逐项输出 `[PASS]`/`[FAIL]`）

---

## 实施指南

### 给现有 SKILL.md 添加门禁

1. 确认该 SKILL.md 是否有验证/校验步骤（见下方检查清单）
2. 找到所有 `硬门禁`、`校验`、`验证`、`verify` 关键词所在行
3. 提取每个验证的：触发位置、通过条件、失败后果
4. 压缩为摘要块，插入 frontmatter 之后
5. 在 SKILL.md 末尾追加 echo-back 提示（1 行即可）

### 摘要块格式模板

```markdown
## MANDATORY GATES

> 执行前必须 echo-back 本块。未输出 = 未开始。

| # | 门禁点 | 位置 | 通过条件 |
|---|--------|------|----------|
| G1 | 读取完整步骤列表 | 全文 | 输出所有 section 标题 |
| G2 | [具体验证] | Step X | [条件] |
```

### 优先级

- **立即加**：有 verify 脚本或多步骤校验的技能
- **按需加**：步骤简单但容易遗漏细节的技能
- **不加**：单步骤、无验证、无分支的简单技能

---

## 检查清单：哪些技能需要加门禁

| 技能 | 需要门禁 | 原因 / 建议添加内容 |
|------|---------|---------------------|
| largebase-structured-scan | **必须** | 已出问题。G1: echo-back 全部 section 标题；G2: scan.py verify 退出码=0；G3: doc-gen 校验清单逐项通过 |
| doc-gen | **必须** | 有校验清单（第 484 行）。G1: 读取校验清单章节；G2: 图表数量达标；G3: SVG/Mermaid 规范通过 |
| algorithm-spec-review | **必须** | 7 阶段流程。G1: echo-back 7 个阶段标题；G2: 置信度阈值检查；G3: 反幻觉校验通过 |
| review | **建议** | 有四阶段审查流程。G1: 读取完整审查标准；G2: severity 分级正确应用 |
| orchestrate | **建议** | 多步骤调度。G1: 读取全部 Step 标题；G2: 状态文件读写顺序正确 |
| pipeline-init | **建议** | 初始化流程有依赖。G1: 读取 Codex 可用性检测步骤；G2: 状态文件创建确认 |
| commit | 可选 | 步骤简单但有约束。建议加 G1: Breaking Change 检测不遗漏 |
| plan | 可选 | 三层计划架构。建议加 G1: 确认读取了 acceptance.md 约束 |
| execute | 可选 | 简单执行+返回。风险低 |
| changelog | 不需要 | 单流程，无分支 |
| smoke-test | 不需要 | 纯检测，无产出校验 |
| memory | 不需要 | 搜索/追加操作，无验证步骤 |
| doc-ref | 不需要 | 索引检索，无验证步骤 |
| doc-sync | 不需要 | 步骤简单，有清单但风险低 |
| git | 不需要 | 工具型，无验证步骤 |
| graphify | 可选 | 有输出目录规范。建议加 G1: 确认输出路径符合规范 |
| plan-checklist | 不需要 | 单一功能 |
| cpp-build / cpp-unit-test | 可选 | 有编译/测试验证。建议加 G1: 编译/测试通过才继续 |
| screenshot-report | 不需要 | 简单截图流程 |
| reviewer-*（6 个） | 不需要 | 审查视角技能，无验证门禁 |
| windows-shell-fallback | 不需要 | 故障排查参考 |
| industrial-ui-design | 可选 | 有验证清单（第 37 行）。建议加 G1: 验证清单通过 |
| ui-ux-design-guide | 不需要 | 参考指南 |
| ui-screenshot-audit | 不需要 | 流程简单 |
| memory-system | 不需要 | 底层系统，无验证步骤 |
| project-init | 不需要 | 初始化参考 |
| report | 不需要 | 汇总型 |
| codex-toolkit | 不需要 | 转换工具 |
| career.skill | 不需要 | 非代码任务 |

---

## 与现有门禁的关系

本协议**不替代** `.claude/rules/gate.md`（项目级门禁），而是补充技能级的细粒度防护：

- `gate.md`：管"要不要开始做"（需求确认、复杂度判断）
- `skill-gate-protocol.md`：管"做了有没有做对"（步骤完整性、产出校验）

两者独立生效，互不覆盖。
