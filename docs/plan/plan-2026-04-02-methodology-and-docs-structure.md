# 框架升级修改计划

> 状态：待确认 | 涉及文件：~11 个 | 新增 skill：1 个（doc-ref）
>
> 来源：视频方法论内化 + BMAD 文档结构 + `ref/记忆与优化/框架升级修改计划.md`

---

## 一、视频方法论内化（6 原则 → 4 文件修改）

### 原则提炼（来自 `ref/VibeCoding案例/00.编程方法论`）

| # | 原则 | 核心要点 | 对应当前流程缺口 |
|---|------|---------|----------------|
| 1 | **框架先行，AI 填逻辑** | 先设计接口/边界/数据结构，让 AI 填充实现细节 | plan skill 缺少"接口与边界定义"强制步骤 |
| 2 | **先跑通再优化（90→100）** | 第一轮只求功能正确，后续迭代打磨质量 | workflows.md 强调"小步实现"但缺少迭代节奏 |
| 3 | **Prompt = 可复用资产** | 高质量 prompt 模板沉淀、版本化、跨会话复用 | 无沉淀规则，每次重写 prompt |
| 4 | **上下文质量 = 输出质量** | 调用 AI 前验证上下文完整性，垃圾进垃圾出 | 缺少"输入质量门禁"，只检查了 Context 容量 |
| 5 | **善后工程师视角** | AI 生成代码完成后，以"善后工程师"身份重点检查 AI 弱点 | review skill 缺少 AI 代码专有检查视角 |
| 6 | **意图驱动开发** | 用自然语言表达"要什么"而非"怎么做"，执行交给 AI | 已有（CC=大脑，Codex=双手），无需额外修改 |

---

### 修改 1：`.claude/workflows/claude-workflow-constants.md`

> 新增 2 个规则节

- [ ] **新增节：「Codex 调用前上下文检查门禁」**（在 Context 健康检查之后）
  - 位置：`constants.md` 现有「Context 健康检查门禁」节之后
  - 内容：
    ```markdown
    ## Codex 调用前上下文检查门禁

    > 原则：垃圾进垃圾出。调用 Codex 前必须验证输入质量。

    调用 Codex 生成代码前，CC 必须确认以下 4 项已注入 Context：
    1. 技术栈版本（语言版本、主要依赖版本）
    2. 相关文件路径（要改的文件、要读的文件）
    3. 已有模式（项目里同类功能的现有实现方式）
    4. 约束边界（不能改什么、不能引入什么）

    如有缺失，先从 scan.db / doc-ref skill / CODEBASE_MAP.md 补充，再调用。
    ```

- [ ] **新增节：「Prompt 沉淀规则」**
  - 位置：`constants.md` 末尾
  - 内容：
    ```markdown
    ## Prompt 沉淀规则

    > 原则：高质量 Prompt 是可复用资产，不是一次性消耗品。

    1. 成功的 Codex Prompt 模板（输出质量高、无需大改）→ 保存到 `.claude/memory/prompts/`
    2. 文件命名：`[场景]-prompt.md`（如 `code-review-prompt.md`、`refactor-prompt.md`）
    3. 每个模板包含：场景说明 + 输入占位符 + 约束清单 + 输出格式要求
    4. 后续同类任务优先引用已有模板，不重复编写
    5. 模板经 3 次以上验证有效 → 标记为 `[STABLE]`
    6. 失败的 Prompt（输出偏差大、需多轮纠偏）→ 写入 `.claude/memory/lessons/` 记录原因
    ```

- [ ] **创建目录 `.claude/memory/prompts/`**（如果不存在）

---

### 修改 2：`.claude/rules/workflows.md`

> 新增开发节奏节 + changelog 自动生成规则

- [ ] **新增节：「开发节奏：三轮迭代原则」**（在"核心开发循环"之后）
  - 位置：`workflows.md` 现有「核心开发循环」节之后
  - 内容：
    ```markdown
    ## 开发节奏：三轮迭代原则

    > 原则：先跑通再优化。90 分的功能 > 0 分的完美设计。

    ### 第一轮（功能可用）
    Codex 生成可运行的版本，不强求完美：
    - 验收标准：主路径跑通，核心功能可用
    - 不检查：代码风格、边界情况、性能
    - 不允许：跳过测试、破坏现有功能

    ### 第二轮（质量审查）
    CC + Codex 联合 review：
    - 验收标准：边界情况覆盖、安全性、向后兼容
    - 修复 review 发现的问题

    ### 第三轮（打磨，可选）
    按需执行，非必须：
    - 适用：核心模块、公开 API、高频路径
    - 内容：性能优化、文档完善、测试补全
    ```

- [ ] **修改「开始新任务前」节**，增加第 5 条：
  ```
  5. 设计接口与边界：明确函数签名、数据结构、模块边界后再动手（框架先行）
  ```

- [ ] **新增节：「Changelog 自动生成规则」**（在"提交规范"之后）
  - 内容：
    ```markdown
    ## Changelog 自动生成规则

    > review 通过且提交成功后，自动触发 changelog 双轨生成。

    **双轨设计**：同一改动生成两份文档，服务两个读者。

    | | `docs/changes/` 人看 | `.claude/memory/context/` AI 看 |
    |--|--|--|
    | 读者 | 开发者、PM、运维 | 下一次 AI 会话 |
    | 核心问题 | 改了什么？影响我吗？ | 为什么这样做？下次要注意什么？ |
    | 长度 | 简短，30 秒可读 | 详细，覆盖边界和决策 |
    | 格式 | Release Note 风格 | 结构化 frontmatter + 分节 |
    | 生成时机 | review 通过 + 提交后自动生成 | review 通过 + 提交后自动生成 |

    **人看版**（`docs/changes/YYYY-MM-DD-[title].md`）：
    - 一句话：新增/改了什么
    - 升级注意（Breaking Changes）
    - 验证方法

    **AI 看版**（`.claude/memory/context/YYYY-MM-DD-[title].md`）：
    - frontmatter：date / type / module / tags / git_commits
    - 技术决策（为什么选方案 A）
    - 引入的新模式（新增了什么类/函数/约定）
    - 已知边界情况
    - 下次改动注意
    - 关联文件列表
    ```

---

### 修改 3：`.claude/skills/review/SKILL.md`

> 新增"善后工程师"审查视角（针对 AI 生成代码的弱点）

- [ ] **在「审核标准」中新增第 7 条**：
  ```
  7. **善后工程师视角**：AI 生成代码通常在边界输入、错误处理、长尾情况有弱点，需要重点检查
  ```

- [ ] **新增节：「善后工程师审查清单」**（在「审核输出格式」之前）
  - 内容：
    ```markdown
    ## 善后工程师视角（AI 生成后必查）

    > AI 生成的代码通常在以下地方需要人工补强。这些不要让 Codex 自己检查自己，由 CC 驱动确认。

    - [ ] 边界输入（空值、超大值、非法格式）
    - [ ] 错误处理（网络超时、文件不存在、并发冲突）
    - [ ] 长尾情况（低概率但高影响的场景）
    - [ ] 向后兼容（老调用方是否受影响）
    - [ ] 日志和可观测性（出了问题能不能查）
    ```

---

### 修改 4：`.claude/skills/plan/SKILL.md`

> 强化"框架先行"，新增接口定义步骤

- [ ] **在「执行流程」步骤 1 和步骤 2 之间插入新步骤**：
  ```markdown
  1.5 **框架先行：接口与边界定义**
      - 定义函数签名（入参/出参/异常）
      - 定义模块间的调用契约
      - 定义数据结构
      - 标注模块边界：哪些是公开接口、哪些是内部实现

      **核心原则**：不要让 Codex 同时设计接口和实现，容易跑偏。接口由 CC 和用户确认，实现由 Codex 负责。
  ```

- [ ] **在「执行流程」步骤末尾新增**：
  ```markdown
  10. 实现完成后对照接口定义做 diff 检查，确认 Codex 实现与设计接口一致
  ```

- [ ] **在「任务拆解原则」中新增**：
  ```
  - 接口未定义的任务不得进入实现阶段（框架先行原则）
  - 数据结构设计优先于逻辑实现（好的数据结构让代码自然简单）
  ```

---

## 二、文档体系重设计

### 当前问题

- `docs/scan/` 下按日期堆叠，没有语义分类
- `tasks/lessons.md` 是平铺文本，无结构
- 没有 PRD/需求/架构层级
- changelog 缺失或混在 git log 里
- AI 上下文记忆和人类文档混在一起

### 目标目录结构

```
docs/
├── plan/                    # [保留] 任务计划（已有）
├── scan/                    # [保留] 代码库扫描产物（已有）
├── changes/                 # [新增] 给人看的 changelog
│   ├── CHANGELOG.md         #   主文档：版本历史，人工可读
│   └── YYYY-MM-DD-[title].md  # 分文档：每次改动的发布说明
├── prd/                     # [新增] 产品/功能需求文档
│   ├── index.md             #   PRD 索引
│   ├── goals.md             #   目标与背景
│   └── [feature]-prd.md    #   按功能拆分的 PRD
├── arch/                    # [新增] 架构决策记录
│   └── [topic]-adr.md      #   ADR 格式（背景/决策/后果）
├── api/                     # [新增] 本地 API 文档库索引（配合 doc-ref skill）
│   ├── index.md             #   文档库总索引
│   └── [sdk-name]/          #   各 SDK/API 文档片段
├── CODEBASE_MAP.md          # [已有]
└── project-overview.md      # [已有]

.claude/memory/              # AI 专用记忆，不在 docs/ 下
├── lessons/                 # [已有] 踩坑经验（平铺）
├── prompts/                 # [新增] 成功 Prompt 模板
└── context/                 # [新增] 给 AI 看的结构化变更记忆
    └── YYYY-MM-DD-[title].md   # 与 changes/ 同名，内容完全不同
```

### Changelog 双轨设计详情

**两份文档，服务两个读者，格式完全不同。**

#### 轨道 A：`docs/changes/` — 给人看

**目的**：团队成员快速了解"改了什么、影响什么、能不能升级"

**主文档 `CHANGELOG.md`**，按版本/里程碑归组：

```markdown
## 2026-04 Sprint 3

- **#42** feat: 用户登录模块，JWT + refresh token 双 token 方案 → [详情](./0042-2026-04-02-abc1234-user-auth.md)
- **#43** fix: 修复内存泄漏，auth 模块 session 对象未释放 → [详情](./0043-2026-04-03-def5678-fix-memory-leak.md)
```

**分文档** `0042-2026-04-02-abc1234-user-auth.md`（Release Note 风格）：

```markdown
# 用户登录模块

**日期**：2026-04-02 | **类型**：feat | **影响范围**：src/auth/, tests/auth/

## 新增了什么
JWT + refresh token 双 token 登录方案，支持 token 自动续期。

## 升级注意（Breaking Changes）
- 需要部署 Redis，refresh token 不支持内存存储
- 环境变量新增 `JWT_SECRET` 和 `REDIS_URL`，部署前必须配置

## 验证方法
登录后检查响应体包含 `access_token` 和 `refresh_token` 两个字段。
```

> 特点：**简洁**，人能 30 秒读完，聚焦"对我有什么影响"。不写实现细节。

#### 轨道 B：`.claude/memory/context/` — 给 AI 看

**目的**：新会话启动时注入，让 AI 知道"这个项目踩过什么坑、做过什么决策"

**分文档** `.claude/memory/context/2026-04-02-user-auth.md`（结构化记忆片段）：

```markdown
---
date: 2026-04-02
type: feat
module: auth
tags: [jwt, redis, session, security]
git_commits: [abc1234, def5678]
---

# 用户登录模块 — AI 上下文记忆

## 技术决策
- 选择双 token 方案而非单 token，原因：单 token 过期时间两难
- refresh token 必须存 Redis，不能存内存（重启即失效）

## 引入的新模式
- `JWTManager`：统一管理 token 生成/验证/刷新
- `RefreshTokenStore`：Redis 存储层抽象

## 已知边界情况
- 并发刷新 token 时有竞争窗口，用 Redis SET NX 加锁

## 下次改动注意
- 加登出功能需要实现 token 黑名单
- 修改 token 结构前先检查所有 `JWTManager.decode()` 调用方

## 关联文件
- 实现：`src/auth/jwt_manager.py`, `src/auth/token_store.py`
- 测试：`tests/auth/test_jwt.py`
```

> 特点：**结构化、可检索**，frontmatter 做索引，AI 按 tags/module/date 过滤加载。写的是"决策理由"和"下次要注意什么"，不是功能描述。

#### 生成规则

> review 通过且提交成功后，自动触发 changelog 双轨生成。人看版聚焦影响，AI 看版聚焦决策和约束。两份文档同名，路径不同。

---

### PRD 工作流（参考 BMAD，适配当前框架）

| BMAD 步骤 | 当前框架 | 建议补充 |
|-----------|---------|---------|
| 故事背景/目标 | CLAUDE.md 门禁讨论 | 新增 `docs/prd/goals.md` 模板 |
| PRD 生成 | 无 | 新增 `prd` 触发词：AI 先判断输入是否明确，不明确时引导补充关键信息后再生成 |
| 功能拆解 | plan skill | 输出到 `docs/prd/[feature]-prd.md` |
| 子任务 | complex workflow Steps | 输出到 `docs/plan/` |
| 执行 | Codex | 不变 |
| 验收记录 | 无 | 输出到 `docs/changes/` changelog |

---

## 三、新增 doc-ref Skill（替代 Context7）

### 功能

按需从 npm/pip 官方文档拉取最新 API 说明注入上下文，解决"AI 不知道你用的版本的具体 API"问题。

### 实现方案

做成本地 skill：**doc-ref**（文档库检索）

```
.claude/skills/doc-ref/
├── SKILL.md          # skill 定义和触发条件
└── index.md          # 已索引的文档库列表
```

- [ ] **创建 `doc-ref/SKILL.md`**

**触发条件**：任何涉及外部 API/SDK/框架的任务开始前，或用户说"参考 [库名] 文档"

**工作方式**：
1. 查 `docs/api/index.md`，看有没有本地索引
2. 有 → 直接读取对应片段注入上下文
3. 没有 → 触发 research workflow 联网搜索 + 抓取官方文档 → 保存到 `docs/api/[sdk-name]/` → 建立索引
4. 调用 Codex 时自动附带相关文档片段作为 Context

**触发提示词**：
```
参考 [库名 v版本号] 文档，给 [模块] 加 [功能]
索引 [SDK名] 文档到本地
更新 [库名] 文档索引到最新版本
```

**本地文档库结构**：
```
docs/api/
├── index.md                     # 库名 | 版本 | 索引时间 | 本地路径
├── fastapi-0.110/
│   ├── routing.md               # 只存项目用到的部分，不是全量文档
│   └── dependencies.md
└── opencv-4.9/
    └── imgproc.md
```

> 和 Context7 的区别：Context7 是实时联网拉取，doc-ref 是本地缓存+按需更新。离线可用，且可以放内部 SDK、私有 API 文档。

---

## 四、修改清单（打勾计划）

| # | 文件 | 操作 | 内容 | 优先级 | 状态 |
|---|------|------|------|--------|------|
| **P1：核心流程（影响每次开发）** |||||
| 1 | `constants.md` | 修改 | 加「上下文输入质量门禁」+ 「Prompt 沉淀规则」 | P1 | ☐ |
| 2 | `workflows.md` | 修改 | 加「三轮迭代开发节奏」+ 「开始新任务前」增加第 5 条 | P1 | ☐ |
| 3 | `plan/SKILL.md` | 修改 | 加「框架先行：接口与边界定义」步骤 + 任务拆解新增 2 条 | P1 | ☐ |
| 4 | `review/SKILL.md` | 修改 | 加「善后工程师审查清单」 | P1 | ☐ |
| **P2：新能力** |||||
| 5 | `doc-ref/SKILL.md` | 新建 | doc-ref skill 定义 | P2 | ☐ |
| 6 | `docs/api/index.md` | 新建 | 文档库索引 | P2 | ☐ |
| **P3：文档结构 + 工作流集成** |||||
| 7 | `docs/changes/CHANGELOG.md` | 新建 | 主 changelog，追加式，编号格式：序号-日期-hash | P3 | ☐ |
| 8 | `docs/changes/README.md` | 新建 | changes 目录说明 | P3 | ☐ |
| 9 | `docs/prd/index.md` | 新建 | PRD 索引 | P3 | ☐ |
| 10 | `docs/prd/goals.md` | 新建 | 目标与背景模板 | P3 | ☐ |
| 11 | `docs/prd/README.md` | 新建 | prd 目录说明 | P3 | ☐ |
| 12 | `docs/arch/README.md` | 新建 | arch 目录说明 + ADR 模板 | P3 | ☐ |
| 13 | `docs/api/README.md` | 新建 | api 目录说明 | P3 | ☐ |
| 14 | `workflows.md` | 修改 | 加「Changelog 自动生成规则」 | P3 | ☐ |
| 15 | `CLAUDE.md` | 修改 | 加 PRD 触发词路由 + doc-ref skill 触发条件 | P3 | ☐ |
| 16 | `.claude/memory/prompts/` | 新建目录 | 沉淀成功 Prompt 模板 | P3 | ☐ |
| 17 | `.claude/memory/context/` | 新建目录 | AI 上下文记忆 | P3 | ☐ |

---

## 五、验收标准

### 方法论内化验收

- [ ] 4 个文件（constants/workflows/review/plan）修改完成，无断裂引用
- [ ] constants.md：上下文质量门禁有 4 项必检清单 + Prompt 沉淀规则有保存/标记流程
- [ ] workflows.md：三轮迭代节奏清晰 + 框架先行第 5 条 + Changelog 双轨规则
- [ ] review skill：善后工程师清单聚焦 AI 代码弱点（边界/错误/长尾/兼容/可观测）
- [ ] plan skill：接口定义步骤有 3 步流程（定义→确认→对照检查）

### 文档结构验收

- [ ] `docs/changes/` + `docs/prd/` + `docs/arch/` + `docs/api/` 目录创建
- [ ] 每个子目录有 `README.md` 说明该文件夹用途、文档格式、生成时机
- [ ] `.claude/memory/prompts/` + `.claude/memory/context/` 目录创建
- [ ] `doc-ref/SKILL.md` 定义完整，触发词和流程清晰
- [ ] `docs/api/index.md` 索引模板可用
- [ ] CLAUDE.md 路由表已更新 PRD（智能引导）和 doc-ref 触发条件
- [ ] changelog 编号格式：`序号-日期-hash-标题.md`

---

## 六、执行顺序

```
Phase A：P1 核心流程修改（#1-4）
  ↓
Phase B：P2 新能力（#5-6）
  ↓
Phase C：P3 文档结构 + 工作流集成（#7-13）
```

Phase A 可立即开始；Phase B 和 C 依赖 A 中 constants.md 的上下文门禁规则。

---

## 七、已确认决策

| # | 问题 | 决策 |
|---|------|------|
| 1 | doc-ref skill 文档更新频率 | **手动触发**（用户说"索引/更新文档"时执行） |
| 2 | changelog 编号格式 | **序号-时间-git hash**（如 `0042-2026-04-02-abc1234-user-auth.md`） |
| 3 | PRD workflow 交互方式 | **智能引导**：AI 先判断用户输入是否足够明确，不明确时引导补充关键信息后再生成 |
| 4 | docs/arch/ ADR 文档 | **现在就加**，初始放 README 说明 + ADR 模板 |
