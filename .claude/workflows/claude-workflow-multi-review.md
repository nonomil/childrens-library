# claude-workflow-multi-review｜多专家评审流程

> 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束
> 触发条件：用户明确要求“多专家评审 / 多视角审查 / 并行审查 / 3 路 review / 红队蓝队式评审”，或 `expert_review_strategy` 命中自动升级条件
> 入口：从 `CLAUDE.md` 场景路由跳转至此
> 定位：这是 `claude-workflow-review.md` 的高级分支，不替代普通 review，而是在高风险或高价值场景下复用 `review + parallel + taskctl` 做受控并行评审

---

## 核心结论

> **多专家评审的重点不是“多开几个子代理”，而是“让多个 reviewer 以固定视角、固定边界、固定输出格式并行工作”。**

相比“直接让 LLM 自己开多个子代理去看”，本流程更可控，因为它把下面 5 件事显式化了：

1. **谁来审**：每个 reviewer 的视角固定，不允许三个 reviewer 做同一件事
2. **审什么**：输入范围固定，默认只读，不允许 reviewer 直接改源码
3. **产出到哪**：每路 reviewer 必须写独立 `review.md` 或报告，不抢同一份总结
4. **谁仲裁**：Coordinator 统一收敛结论，负责定最终优先级
5. **后续怎么走**：若需要修复，回到已有 `review / parallel / complex` 主线，不在 review 阶段直接偷改代码

---

## 什么时候该用这个流程

### 显式触发

用户说了以下任意表达时，直接进入本流程：

- “多专家评审”
- “多视角审查”
- “并行审查”
- “开 3 个 reviewer”
- “从不同角度评审代码 / 算法 / 文档”
- “红队蓝队式 review”

### 自动升级触发

当 `expert_review_strategy=auto_on_high_risk` 时，命中以下任一条件也应从普通 `review` 升级到本流程：

1. 同时存在 **代码 + 算法规格 / 设计文档 / 关键配置** 需要联审
2. 目标改动涉及 **高风险文件**：公共 API、schema、安全模块、核心配置
3. 用户要求“全面审查 / 深度审查 / 从多个角度确认”
4. 普通 review 已出现明显分歧，且需要第二、第三视角来仲裁

### 不适用的情况

- 只是一个小 diff 的普通 code review
- 目标是“尽快改完”，不是“高置信度判断对不对”
- reviewer 必须直接改同一份源码或同一段总结

---

## 与现有流程的关系

| 目标 | 走哪个流程 | 说明 |
|---|---|---|
| 普通单路 review | `claude-workflow-review.md` | 默认路径 |
| 多视角并行审查 | **本文档** | review 的高级版 |
| 多任务并行开发 | `claude-workflow-parallel.md` | 强调执行，不是评审 |
| 审完后要修复 | 回到 `claude-workflow-review.md` 或 `claude-workflow-complex.md` | 本流程不直接改代码 |

**一句话分工：**

- `review.md` 解决“怎么审”
- `parallel.md` 解决“怎么并行”
- `taskctl.py` 解决“怎么登记、控边界、排顺序”
- **本文档**解决“怎么把这三者组合成可控的多专家评审”

---

## Phase 0：模式判断与视角选择

### Step 0.1 读取偏好

读取 `.claude/preferences.json`：

- `review_strategy`
- `parallel_strategy`
- `collaboration_mode`
- `expert_review_strategy`

推荐默认：

```json
{
  "review_strategy": "auto_gate",
  "parallel_strategy": "auto",
  "collaboration_mode": "normal",
  "expert_review_strategy": "manual"
}
```

### Step 0.2 选择执行模式

本流程推荐默认：

- **控制面**：`advanced`
- **执行隔离**：`patch`

原因：

- 评审任务通常以**只读输入 + 独立输出文档**为主，不需要默认拉起 worktree
- 但它天然是 **3 路并行 + Coordinator 收敛**，所以控制面通常应升级到 `advanced`

只有命中下面情况才建议升级执行隔离：

| 条件 | 推荐策略 |
|---|---|
| reviewer 只读源码、只写各自报告 | `patch` |
| reviewer 需要独立跑不同测试或工具链 | `worktree` |
| reviewer 需要分批叠加评审修复 | `stack` |

### Step 0.3 选择专家视角（两种模式）

> **核心原则**：不要一上来就硬编码固定视角（安全/架构/性能）。评审专家的方向应该由项目特点和改动内容决定，而不是套模板。

先让 CC 判断进入哪种模式，再确定 2~4 个互补视角。

#### 模式 A：AI 自主选专家（默认）

**触发条件**：用户没有指定专家方向，或说”帮我多专家评审”但没说具体视角

**流程**：

1. **项目扫描**：CC 分析目标代码库的技术栈、业务领域、核心风险点
   - 如果有 code-review-graph 知识图谱 → 用 `get_architecture_overview` 获取结构
   - 如果没有 → 用 Glob/Grep 扫描文件结构和关键 import
   - 读取 README / 项目说明，理解业务领域

2. **风险画像**：根据分析结果，生成该项目的风险画像（1-2 句话概括）

3. **头脑风暴**：CC 提出 2~3 套互补的视角拆分方案，每套方案标注：
   - 每个视角的审查重点
   - 为什么选这个视角（与项目风险的关系）
   - 推荐的审查文件范围

4. **选择最优方案**：选互补性最强、与项目风险最匹配的一组

5. **输出评审计划**：向用户展示选定的视角和理由，标注 `[AI 自主选择]`

**示例**（工业检测软件）：

```
风险画像：工业检测软件，核心风险是数值精度（直接影响产品质量判定）
         和大图像处理的内存管理（8GB 工控机场景）

方案 A（通用视角）：安全 + 架构 + 性能
  - 问题：通用安全视角对工业检测价值低，不如算法精度视角

方案 B（领域匹配视角）：
  Reviewer-A: 数值精度与算法正确性 ← 匹配核心风险
  Reviewer-B: 内存与图像处理效率   ← 匹配工控机资源约束
  Reviewer-C: GUI 健壮性与操作员体验 ← 匹配产线工人使用场景
  - 优势：每个视角直击项目真实风险

选定：方案 B
```

#### 模式 B：用户指定专家方向

**触发条件**：
- 用户明确说了评审方向（如”从安全和性能角度审”）
- 用户指定了 Skill（如”用 algorithm-spec-review 和 cpp-build 技能审”）
- 用户提供了自定义的专家角色描述

**流程**：

1. **解析用户意图**：提取用户指定的专家方向/Skill 名称
2. **映射到具体视角**：
   - 如果指定了 Skill → 按 Skill 的 SKILL.md 描述定义审查范围
   - 如果指定了方向词 → 映射为具体审查维度
3. **补充缺失视角**（如果用户指定的视角 < 2 个）：
   - CC 补充 1~2 个互补视角，标注 `[AI 补充]`
   - 向用户确认后再执行
4. **输出评审计划**：向用户展示最终的视角组合，标注 `[用户指定]` 和 `[AI 补充]`

**常见方向词映射表**：

| 用户说的 | 映射为 |
|---------|--------|
| 安全 / security | 输入验证、权限、注入、OWASP Top 10 |
| 性能 / performance | 内存、CPU、IO、并发、延迟 |
| 架构 / architecture | 分层、职责单一、DRY、接口设计 |
| 算法 / algorithm | 数值精度、边界条件、数学正确性 |
| 可维护性 / maintainability | 命名、函数长度、复杂度、文档 |
| 测试 / testing | 覆盖率、边界测试、回归风险 |
| 安全合规 / compliance | 数据保护、审计日志、配置完整性 |
| 并发 / concurrency | 竞态条件、死锁、线程安全 |

#### 专家技能参考库（索引）

> 详细检查项已拆分为独立 skills，按需加载。以下仅保留速查索引。
> 调用方式：确定专家后读取对应 `.claude/skills/reviewer-xxx/SKILL.md`

##### A. 项目类型 → 推荐视角速查

| 项目类型 | 首选专家 | 次选专家 | 第三专家 |
|---------|---------|---------|---------|
| Web 应用 | 安全专家 | 高级工程师 | 性能工程师 |
| 算法/科学计算 | 机器视觉专家 | 性能工程师 | QA 工程师 |
| 嵌入式/工控 | 嵌入式专家 | C++ 专家 | 安全专家 |
| 数据库/存储 | 高级工程师 | 性能工程师 | QA 工程师 |
| CLI/工具 | 高级工程师 | QA 工程师 | 性能工程师 |
| ML/AI 管道 | 机器视觉专家 | 性能工程师 | QA 工程师 |
| 桌面 GUI | 高级工程师 | 性能工程师 | QA 工程师 |
| 库/SDK | 高级工程师 | 安全专家 | QA 工程师 |
| C++ 系统 | C++ 专家 | 性能工程师 | 安全专家 |
| 图像处理/机器视觉 | 机器视觉专家 | 性能工程师 | C++ 专家 |

##### B. 专家 Skill 索引

| 专家 | Skill | 触发关键词 | 来源 |
|------|-------|-----------|------|
| C++ 专家 | `reviewer-cpp-expert` | C++/内存/RAII/指针/MISRA | C++ Core Guidelines, MISRA, AUTOSAR |
| 高级工程师 | `reviewer-senior-engineer` | 架构/SOLID/设计模式/Tech Lead | addyosmani, VoltAgent |
| 机器视觉专家 | `reviewer-vision-expert` | 图像/OpenCV/精度/相机标定 | OpenCV, 工业视觉实践 |
| 安全专家 | `reviewer-security-expert` | OWASP/注入/认证/加密 | OWASP Top 10, ASVS |
| 性能工程师 | `reviewer-performance-engineer` | 性能/延迟/SIMD/并发/剖析 | addyosmani, cfregly |
| 嵌入式专家 | `reviewer-embedded-expert` | 嵌入式/实时/看门狗/WCET | IEC 61508, ISO 26262 |
| QA 工程师 | `reviewer-qa-engineer` | 测试/覆盖率/边界/fuzz/回归 | addyosmani, TestRail |

##### C. 加载规则

- **Phase 0 选定专家后**，读取对应 `reviewer-xxx/SKILL.md` 获取完整检查项
- **每个 reviewer subagent** 初始化时加载对应 skill 作为系统提示词
- **未选中的专家不加载**，节省 tokens

#### 输出格式（两种模式通用）

无论哪种模式，最终都要输出以下评审计划，**等用户确认后才创建 reviewer 任务**：

```
评审计划
├── 目标：[一句话]
├── 项目风险画像：[1-2 句]
├── 模式：[AI 自主选择 / 用户指定]
├── 视角：
│   ├── Reviewer-A: [视角名称] — [审查重点] — 文件范围: [...]
│   ├── Reviewer-B: [视角名称] — [审查重点] — 文件范围: [...]
│   └── Reviewer-C: [视角名称] — [审查重点] — 文件范围: [...]
├── 收敛规则：任一 HIGH → 必须修复
└── 等待用户确认...
```

---

## Phase 1：Coordinator 建立评审控制面

### Step 1.1 创建总任务

先创建一个总评审任务，用来承载：

- 范围说明
- 评审目标
- 最终汇总结论
- reviewer 分配表

例如：

```bash
python scripts/taskctl.py create \
  --title "多专家评审：支付模块改造" \
  --owner claude-main \
  --mode patch \
  --branch review/payment-refactor \
  --topic multi-review-payment \
  --path docs/plan \
  --path src/payment \
  --path tests/payment
```

### Step 1.2 创建 2~3 个 reviewer 子任务

每个 reviewer 子任务都必须：

- 写清 `owner_agent`
- 写清**只读输入范围**
- 写清**允许写入的输出路径**
- 明确自己的评审视角

推荐做法：

- 源码、规格、文档目录只读
- `docs/plan/tasks/Txxx-*/review.md` 或独立报告目录可写

也就是说，reviewer 的 `allowed_paths` 应优先指向 **报告产物**，而不是源文件本身。

推荐优先使用 `taskctl.py review-split` 自动生成三路 reviewer 骨架：

```bash
python scripts/taskctl.py review-split \
  --title "支付模块多专家评审" \
  --topic payment-review \
  --review-kind code \
  --source-path src/payment/ \
  --source-path tests/payment/
```

这个命令会自动：

- 固定拆成 3 路 reviewer 任务
- 默认使用 `advanced` 所需字段
- 使用 `.claude/taskctl.json` 的默认审批目标
- 让 reviewer 只写各自任务目录下的 `review.md` 等交付文档

### Step 1.3 默认走 advanced

多专家评审一旦进入真正并行阶段，推荐直接执行：

```bash
python scripts/taskctl.py upgrade-advanced --task T201
python scripts/taskctl.py upgrade-advanced --task T202
python scripts/taskctl.py upgrade-advanced --task T203
```

目的不是为了复杂而复杂，而是为了明确：

- `lane_key`
- `approval_target`
- reviewer 自己的输出写入边界

---

## Phase 2：并行评审执行

### 核心原则

1. **输入尽量只读**
2. **每路 reviewer 只写自己的报告**
3. **不允许 reviewer 直接修代码**
4. **每路 reviewer 必须独立产出结论**

### 推荐执行模板

```text
Reviewer A
  任务：功能正确性
  输入：变更文件 + plan.md + acceptance.md
  输出：T201/review.md

Reviewer B
  任务：测试与回归缺口
  输入：变更文件 + 测试文件 + 验证命令
  输出：T202/review.md

Reviewer C
  任务：架构与边界一致性
  输入：变更文件 + project-overview / 相关设计文档
  输出：T203/review.md
```

### 审查粒度要求

每路 reviewer 的结论必须包含：

- 发现的问题
- 问题级别
- 证据来源
- 是否阻塞
- 建议动作

至少要区分：

- `blocker`
- `major`
- `minor`
- `question`

---

## Phase 3：Coordinator 收敛与仲裁

### Step 3.1 收集三路结论

Coordinator 统一读取：

- `T201/review.md`
- `T202/review.md`
- `T203/review.md`

如果已经用 `taskctl.py review-split` 建好 reviewer 任务，推荐直接用 `taskctl.py review-aggregate` 做第一轮收敛，而不是手工拷贝三份 `review.md`：

```bash
python scripts/taskctl.py review-aggregate \
  --review-task T201 \
  --review-task T202 \
  --review-task T203 \
  --target-task T200
```

如果当前还没有总任务，也可以先落到独立报告：

```bash
python scripts/taskctl.py review-aggregate \
  --review-task T201 \
  --review-task T202 \
  --review-task T203 \
  --output docs/plan/reports/payment-review-summary.md \
  --title "支付模块多专家评审汇总"
```

### Step 3.2 去重和分歧标记

不是所有 reviewer 说的问题都要机械相加。Coordinator 需要把结果分成 3 类：

1. **共识问题**：多路 reviewer 都指出
2. **单路高价值问题**：只有一路指出，但证据充分
3. **分歧问题**：reviewer 之间判断不同，需要人工或主会话仲裁

### Step 3.3 输出总报告

总报告建议写入总任务的 `review.md`，结构推荐：

```markdown
# 多专家评审汇总

## 共识问题

## 单路高价值问题

## 分歧与仲裁建议

## 最终结论
- approved
- changes_requested
- blocked
```

`review-aggregate` 当前的自动收敛规则是：

- 相同问题被 2 路及以上 reviewer 提到，归入“共识问题”
- 只被 1 路提到但严重程度为 `blocker / major`，归入“单路高价值问题”
- reviewer 最终结论不一致时，归入“分歧问题”
- 最终汇总结论优先尊重 reviewer 的明确结论；缺失结论会直接把总结果降为 `blocked`

---

## Phase 4：评审之后怎么走

### 如果结论是 `approved`

回到原流程：

- 普通改动：继续 `claude-workflow-review.md` 的收尾
- 多任务联动：继续 `claude-workflow-parallel.md` 的 queue / merge

### 如果结论是 `changes_requested`

不要在 review 线程里直接改源码。

正确做法：

1. 由 Coordinator 把问题整理成修复任务
2. 重新登记 `taskctl` 任务
3. 进入普通开发 / complex / parallel 主线去修

### 如果结论是 `blocked`

说明当前输入本身就不适合继续执行，常见情况包括：

- 规格不清
- 验证证据缺失
- 关键上下文冲突

此时应：

- 回到 plan / spec 阶段
- 或触发 research / largebase / algorithm-spec-review

---

## 为什么它比“直接开多个子代理”更可控

| 对比项 | 直接开多个子代理 | 多专家评审工作流 |
|---|---|---|
| 视角控制 | 容易重复 | 先头脑风暴，再固定视角 |
| 写入边界 | 容易踩同一份文件 | reviewer 默认只写各自报告 |
| 结论收敛 | 容易口头漂移 | Coordinator 有固定汇总动作 |
| 后续修复 | 容易边审边改 | review 与 fix 显式拆开 |
| 审计留痕 | 弱 | `taskctl + review.md + queue` 全留痕 |

**结论：**

- 如果你只是想“快点多看几眼”，直接开多个子代理可以。
- 如果你想把它做成模板能力、稳定复用、可回溯，那就应该走本文档这种受控工作流。

---

## 推荐默认策略

如果你想让模板既不过重，又能随时升级，推荐默认值如下：

```json
{
  "expert_review_strategy": "manual"
}
```

含义：

- 平时不自动触发
- 用户说“多专家评审”时才进入
- 高风险项目可以在仓库级改成 `auto_on_high_risk`

可选值建议：

| 值 | 行为 |
|---|---|
| `manual` | 仅用户显式要求时触发（默认） |
| `auto_on_high_risk` | 高风险或多材料联审时自动升级 |
| `always` | 只要进入 review 就默认先走多专家评审 |

---

## 与多 Agent 协作文档的对应关系

- 视角拆分与控制面解释：见 `docs/多Agent协作/07 — Coordinator、并行改文档与并行审查说明.md`
- `normal / advanced` 与 Happy Path：见 `docs/多Agent协作/06 — 模式路由与 Happy Path.md`
- Coordinator 状态推进：见 `docs/多Agent协作/04 — Coordinator 流程.md`

---

## 最小执行建议

如果当前要马上落地，不必先做全自动调度。最小可用版本就是：

1. 新增本文档
2. 在 `CLAUDE.md` 路由表里加“多专家评审”
3. 在偏好里加 `expert_review_strategy`
4. 由 Coordinator 通过 `taskctl.py review-split` 一次生成 reviewer 任务骨架
5. 等稳定后，再考虑脚本化生成 reviewer 骨架
