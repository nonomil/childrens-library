# 工作流规范

> 无 paths 限制，所有文件类型均加载。

## 核心开发循环

每次任务遵循以下顺序，不跳步：

```
理解需求 → 阅读相关代码 → 制定方案 → 小步实现 → 运行测试 → Code Review → 提交
```

**单次 diff 不超过 200 行**。超过时拆分为多个独立 PR / commit。

## 子代理执行模式（subagent_execution）

> 适用于小上下文模型（如 GLM 5.1），将执行阶段委托给子代理，主代理只保留规划+审查，减少主上下文膨胀和压缩频率。

### 触发条件（三选一即激活）

1. `preferences.json` 中 `subagent_execution` = `"on"` — 始终启用
2. 用户说"子代理执行"/"subagent 执行"/"委托子代理" — 当次会话自动切换为 on（写入 preferences）
3. 项目初始化时用户选择"主代理+子代理"模式

### 激活后的行为

| 阶段 | 主代理（CC） | 子代理（Agent tool） |
|------|-------------|---------------------|
| 门禁 | ✅ 需求讨论、追问、确认 | — |
| 规划 | ✅ 写计划、拆任务 | — |
| **执行** | ❌ 不直接写代码 | ✅ 读文件、写代码、运行测试 |
| Review | ✅ 审查子代理报告 + git diff | — |
| 提交 | ✅ git add/commit | — |

### 子代理调用模板

```
Agent({
  description: "执行 {task_id} {task_name}",
  prompt: "你是执行代理。任务：{plan_steps}。文件范围：{allowed_paths}。
          完成后报告：1.改了哪些文件 2.改了什么 3.测试结果 4.遗留问题。
          报告控制在 200 字以内。",
  isolation: "worktree"  # 可选，需要隔离时用
})
```

### 关键约束

- 子代理完成后，主代理**必须**读 git diff 验证实际改动，不能只信报告
- 子代理报告 ≤200 字，防止反向膨胀主上下文
- 如果子代理失败/返回过长，回退到主代理内联执行

## 开发节奏：三轮迭代原则

> 原则：先跑通再优化。90 分的功能 > 0 分的完美设计。

### 第一轮（功能可用）
CC 直接编写可运行的版本，不强求完美：
- 验收标准：主路径跑通，核心功能可用
- 不检查：代码风格、边界情况、性能
- 不允许：跳过测试、破坏现有功能

### 第二轮（质量审查）
CC 自查 + 可选 Codex review：
- 验收标准：边界情况覆盖、安全性、向后兼容
- 修复 review 发现的问题

### 第三轮（打磨，可选）
按需执行，非必须：
- 适用：核心模块、公开 API、高频路径
- 内容：性能优化、文档完善、测试补全

## 开始新任务前

1. 阅读相关模块的现有代码，理解当前模式
2. 检查是否有同类实现可复用，不重复造轮子
3. 确认影响范围：改动是否会波及其他模块
4. 大型改动（>100 行）先写方案文档，确认后再实现
5. 设计接口与边界：明确函数签名、数据结构、模块边界后再动手（框架先行）

## 路由补充：CV 混合代码库

满足任意一条时，优先加载 `.claude/workflows/claude-workflow-cv-codebase.md`：
- 项目同时包含 C++ 与 Python 主体代码
- 需求命中 `pybind11 / Cython / pipeline / TensorRT / ONNX / 跨语言`
- 涉及推理后端替换、跨层重构、机器视觉主链路改动

优先级补充：
- 若同时命中“大型代码库”和“CV 混合代码库”，优先进入 `claude-workflow-cv-codebase.md`
- `claude-workflow-cv-codebase.md` 内部再复用 `claude-workflow-largebase.md` 的扫描包规范
- 若用户明确要求“创建知识图谱/graphify”，在该流程内按需触发 Graphify，但跨语言调用链仍以 Cartographer 为准

## 实现阶段

- 先写接口 / 类型定义，再写实现，最后写测试（或 TDD：先写测试）
- 每实现一个逻辑单元，立即运行相关测试，不等到全部写完再跑
- 遇到不确定的设计决策：记录为 `// TODO: 待确认 - <问题描述>`，不拍脑袋定下来
- 不在实现过程中顺手重构不相关代码（分离关注点，避免混淆 diff）

## Code Review 检查项

提交前自查：

**正确性**
- [ ] 逻辑覆盖了正常路径、边界条件、错误路径
- [ ] 没有明显的 off-by-one 或空指针风险
- [ ] 异常 / 错误有处理，不静默失败

**代码质量**
- [ ] 命名清晰，见名知意，无魔法数字（用常量代替）
- [ ] 函数职责单一，无超过 50 行的函数（Python）/ 无超过 80 行的函数（C++）
- [ ] 无重复代码（DRY），共用逻辑已提取

**安全**
- [ ] 外部输入已验证
- [ ] 无硬编码 secrets
- [ ] 资源已正确释放

**测试**
- [ ] 新增逻辑有对应测试
- [ ] 测试覆盖了异常路径
- [ ] 本地测试全部通过

## Debug 工作流

1. 最小化复现：构造能稳定触发 bug 的最小输入
2. 添加日志 / 断言定位边界：从哪步开始数据不符合预期
3. 假设 → 验证 → 排除，逐步缩小范围
4. 找到根因后，先写回归测试，再修复
5. 修复后确认回归测试通过，检查类似模式是否有其他 bug

## 子任务分发（Claude Code 多 Agent）

适合分发给 subagent 的任务：
- 并行的独立模块实现（无相互依赖）
- 大规模文件扫描 / 分析
- 专项 Review（安全审查、性能分析）

不适合分发的任务：
- 跨模块有依赖的实现（顺序执行更安全）
- 需要持续上下文积累的调试

## 提交规范（Conventional Commits）

```
<type>(<scope>): <summary>

[可选 body：解释 why，不是 what]
[可选 footer：Breaking change、关联 issue]
```

type 选项：`feat` / `fix` / `refactor` / `test` / `docs` / `chore` / `perf`

示例：
```
feat(merger): 支持 TIFF 格式输入

fix(file_manager): 修复 Windows 路径自然排序错误 (#42)

refactor(batch): 拆分批量调度器，降低单函数复杂度
```

- summary 用祈使句，首字母小写，不加句号
- 单次 commit 只做一件事；不把格式修改和逻辑修改混在同一个 commit

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

**编号格式**：`序号-日期-hash-标题.md`（如 `0042-2026-04-02-abc1234-user-auth.md`）

**人看版**（`docs/changes/`）：
- 一句话：新增/改了什么
- 升级注意（Breaking Changes）
- 验证方法

**AI 看版**（`.claude/memory/context/`）：
- frontmatter：date / type / module / tags / git_commits
- 技术决策（为什么选方案 A）
- 引入的新模式（新增了什么类/函数/约定）
- 已知边界情况
- 下次改动注意
- 关联文件列表

## 高风险操作清单

以下操作执行前必须确认：
- 删除或重命名公开 API / 函数签名（检查所有调用方）
- 修改数据库 schema 或文件格式（需要迁移方案）
- 修改全局配置或初始化逻辑（影响范围最广）
- 修改构建脚本 / CI 配置（先在分支验证）

## 研究循环模式（autoresearch，可选）

> 适用于可量化目标的自动优化：ML 实验、性能调优、覆盖率提升。
> 哲学：一个指标 + 一个约束 + 一个循环。人定方向，Agent 自主迭代。

### 三文件架构

| 文件 | 角色 | 可修改？ |
|------|------|---------|
| `program.md` | 实验方向 + 规则（人类控制） | ✅ 人工调整 |
| `src/experiment.py` | 模型/算法/参数（Agent 沙箱） | ✅ Agent 唯一可改文件 |
| `src/evaluate.py` | 评估逻辑（冻结基准） | ❌ 禁止修改 |

### 自主循环流程

```
Phase 0: 前置检查（git 干净度）
  ↓
Phase 1: Review（读 git log + 历史结果）
  ↓
Phase 2: Ideate（基于历史选择下一实验）
  ↓
Phase 3: Modify（一个原子改动）
  ↓
Phase 4: Commit（先提交再验证）
  ↓
Phase 5: Verify（运行评估命令提取数字）
  ↓
Phase 6: Decide（指标改善 → keep；退步 → git revert）
  ↓
Phase 7: Log（results.tsv 记录）
  ↓
Phase 8: Repeat（或停止：target_reached / budget_exhausted / plateau）
```

### 启动条件

1. `program.md` 已填写目标、评估命令、成功标准
2. `src/evaluate.py` 存在且可运行
3. 有 baseline 数值（第一次运行采集）
4. Git 工作区干净

### 停止条件

- target_reached：指标达到目标值
- budget_exhausted：超过最大迭代次数
- plateau：连续 15 轮改善 < 3%

### 安全约束

- 研究循环模式仅限 `work_mode: research` 时启用
- 循环内不碰 `.claude/`、`CLAUDE.md`、`program.md`
- 连续 3 次崩溃 → 暂停报告用户
