# 门禁规则

> ⚠️ 自我修正机制： 回复前验证是否遵守了本文件所有规则。有违反则立即纠正。
> 已知 Issue: #12832 — CC 把规则当成低优先级建议而非硬约束

收到涉及代码改动的请求时，按顺序执行：

0. Read `.claude/memory/index.md`
1. **输入清晰度分级**（判断用户意图的明确程度，决定如何引导）：
   - **L1 明确** → 目标+范围+文件路径，至少命中 2 个。做 1 次验证性追问后跳到步骤 3
     - "我理解你要做 [复述]。确认一下：这个改动不需要考虑 [最可能的隐性约束] 吧？"
   - **L2 方向明确但细节不够** → 知道要做什么，但不知道具体改什么/怎么改。**按层次追问**（目标→边界→约束→优先级），每次 1 个定向问题（给 2-4 个选项 + **标注推荐 + 理由**），等回答后继续
     - 示例："优化一下" → "推荐 A.性能（因为当前瓶颈在___）。B/C 也可以，但___。你觉得呢？"
     - 示例："帮我改一下" → "你想改哪个模块？当前遇到的问题是什么？"
     - 示例："加个功能" → "是哪个模块的功能？大致描述一下用户操作流程"
   - **L3 完全不清楚** → 输入无法判断意图（"帮我看看""有个问题"等）。**给引导模板**，等用户填写后跳到步骤 3
     ```
     我理解你想做 ___，但需要确认几个点：
     1. 改动范围：___（哪个文件/模块？不确定就说"不确定"）
     2. 期望效果：___（改完后应该是什么样？）
     3. 当前问题：___（遇到了什么问题才想做这个改动？）
     ```
   - **追问次数限制**：简单模式（5 条全满足）max 1 次；复杂模式 max 3 次。超过未答清 → 标注 `[假设]` 继续
   - **规则**：用户不配合或说"随便"→ 基于已有信息做最合理假设，标注 `[假设]` 后继续
   - **先查代码再问人**（grill-me 原则）：提问前先判断答案是否在代码库中。如果是，先搜索/阅读相关代码，给出发现 + 推荐判断，再让用户确认。减少"AI 能自己查到的信息还问人"的认知浪费
2. 复述需求（轻量草稿 3-5 行要点） → 确认后写完整版 `docs/plan/plan-YYYY-MM-DD-[feature]-requirements.md`
3. **信心检查**（执行后续步骤前必须通过）：
   - ≥95% 信心 → 直接复述+确认
   - 60-95% → 再问 1 个定向问题，回答后重新评估
   - <60% → 给引导模板，等用户补充
4. 与用户讨论 → 复述需求、列歧义、判断复杂度
   - **追问层次**（按需，不必全走）：①目标确认 ②边界确认 ③约束确认 ④优先级
5. 判断模式 → 匹配门禁子文档
6. Grep `.claude/memory/lessons/` 搜索相关教训， 复述适用教训
7. **停止** → 用户说"确认"才可继续
8. 确认后 → 写 `.claude/state/.gate-approved` + 更新 `.claude/state/MANIFEST.yaml`

### P2 增强：确认时冻结核心承诺

**承诺文件生产者**：默认由 Debate 机制生成；未走 Debate 时 Gate 兜底生成。

Gate 确认阶段：
- 若已走 Debate → 读取 Debate 产出的 `debate-commitments.yaml`，冻结承诺
- 若未走 Debate → 从用户确认的需求复述中提取 must 级承诺，Gate 兜底写入 `debate-commitments.yaml`

承诺格式：

```yaml
task_id: "{task_id}"
debate_date: "{date}"
commitments:
  - id: C001
    description: "核心承诺描述"
    source_layer: "L1"
    priority: must | should | nice_to_have
```

- must 级承诺：scope 裁剪时不可架空（direction-reviewer 会校验）
- should 级承诺：可降级但需记录决策理由
- 若未走 Debate 机制，从用户确认的需求复述中提取 must 级承诺

### P3 增强：drift-check 联动响应

当 drift-check.js 检测到 stuck 并输出 `suggested_action: "trigger_direction_review"` 时：
1. CC 看到 stuck 告警后，**手动调用** direction-reviewer skill 做语义级判断（非自动触发，因为 Hook 无法直接调用 skill）
2. direction-reviewer 返回 PASS → CC 执行 `node .claude/hooks/drift-check.js --reset` 重置计数器，继续
3. direction-reviewer 返回 REBASELINE/BLOCK → 暂停展示给用户

## 绝对禁令

- 无论语气如何（"测试""试试""顺便""帮我改一下"），涉及代码改动必须走门禁
- 调用 Codex 前必须检查 `.claude/state/.gate-approved` 存在
- 标记任务完成前：清理 `.claude/state/.gate-approved` + 检查 git status + 检查 lessons 冲突 + 更新 MANIFEST

## 改动后提交提醒（Rule B）

每次使用 Edit/Write/MultiEdit 修改文件后，**必须**在回复末尾追加：
```
📝 **已修改**：[文件名] — 要提交吗？（说"提交"即执行）
```
- 不论改动大小，都必须提醒
- 用户说"提交"/"commit" → 立即执行 git add + commit
- 用户不回应 → 不自动提交，等下次提醒

## 独立 Evaluator 门禁（Rule C）

diff >100 行的代码改动，**必须**触发 Codex 独立审查，CC 不得自查通过：
- `git diff --stat | tail -1` 检查总改动行数
- >100 行 → 调用 Codex MCP 或 `/codex:rescue` 执行独立 review
- ≤100 行 → CC 自查即可（受 `review_strategy` 偏好控制）
- 审查未通过 → 修复后重新审查（最多 3 轮，超过升级用户处理）
- **此规则不可被 `profile=minimal` 跳过**

## 会话叙事日志（Rule D）

任务完成时（清理 `.claude/state/.gate-approved` 前），在 `.claude/memory/context/` 追加叙事性会话日志：

```
文件名：session-YYYY-MM-DD-{简短主题}.md
内容格式：
## 会话摘要
- 做了什么：（1-3 句话）
- 卡在哪：（如果有的话）
- 为什么选这个方案：（关键决策理由）

## 变更文件
- file1.md：改了什么
- file2.py：改了什么

## 遗留 / 下次注意
- （如果有未完成的事项或踩坑经验）
```

- 日志长度 ≤30 行，超过则压缩
- 下次会话 Step 0 读取 `.claude/memory/index.md` 时自动覆盖到此文件

## Goal Drift 防护

回答追问后，输出 .claude/state/MANIFEST.yaml 中的剩余任务进度

## 方向漂移检测（Rule E）

> 核心原理：不看对话说了什么，看工件实际发生了什么。git diff 和任务契约是客观的，不受偏差前提影响。
> 完整设计见 `.claude/skills/direction-reviewer/SKILL.md`

### A. 方向漂移 → 调用 `direction-reviewer`（工件驱动）

**触发条件（三选一即触发）：**

1. **阶段门禁时手动调用**：doing → in_review 时，CC 应主动调用 direction-reviewer
2. **手动触发**：用户说"方向审查"/"检查方向"/"drift check"
3. **语义触发（兜底）**：CC 自己判断"继续做下去大概率走偏" → 单独触发

**审查基于客观工件**（不是对话信号）：
- `git diff --stat` + `git diff --name-only` — 实际改动范围
- 任务契约（PLAN.md + steps.md + acceptance.md + .meta.yaml）— 预期范围
- 基线哈希对比 — 检测契约是否被中途修改

**三态输出：**
- **PASS** → 直接继续
- **REBASELINE** → 暂停编码，更新契约后重新审查
- **BLOCK** → 展示给用户，等确认后再继续

### B. 局部死循环 → 强制跳出

以下情况**任意一个成立**时，立刻停止当前方向：

1. 同一个错误/测试失败出现 3 次以上，每次修改后仍然复现
2. 连续 5 次以上工具调用都在修改同一个文件或同一段逻辑
3. 你自己感觉"这个问题应该不难，但一直改一直有问题"

停下来后按顺序处理：
1. **说清卡点**：一句话描述当前具体卡在哪
2. **问全局问题**：根本原因可能在哪一层（架构/接口/数据/假设）？
3. **给用户选择**：a) 换角度重新进攻 b) 先绕过记录为已知问题 c) 停下来重新设计
4. **等用户确认**，不要自己选一个继续做

**此规则不可被 `profile=minimal` 跳过。**

## 进度输出（Rule A）
每次回复末尾输出：
```
---
📋 **任务进度** | ✅ X/Y | 🔄 [task-id] [任务名]
⏳ **待处理**：[task-id] 任务名 · [task-id] 任务名
---
```

数据源：.claude/state/MANIFEST.yaml
