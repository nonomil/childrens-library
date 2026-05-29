# claude-workflow-parallel｜多功能并行开发流程

> 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束
> 触发条件：任务数 ≥ 2 且可解耦
> 入口：从 `claude.md` 场景路由跳转至此
> 注意：并行开发通常也是复杂模式，先完成 `claude-workflow-complex.md` Phase 1-4.5 再进入此文档
> **路径常量**：本文档中所有 worktree 路径使用 `[WORKTREE_BASE]` 占位符，实际值读取 `claude-workflow-config.md` 中的 `WORKTREE_BASE` 常量（默认：`worktrees`）
> **分支模式**：根据 `BRANCH_MODE` 常量调整行为（`temporary` = 临时分支模式，`bare` = Bare Repo 模式）
> **并行策略**：根据 `parallel_strategy` 偏好选择 `patch / stack / worktree / isolated`（见 Phase 0）
> **控制面模式**：根据 `collaboration_mode` 选择 `normal / advanced`（见 Phase 0）

---

## Phase 0：并行策略与控制面模式选择

> 在进入 Phase 1 之前，先确定“怎么隔离执行”和“控制面要启多重”。

### 0.1 读取偏好

读取 `.claude/preferences.json` 的两个字段：

- `parallel_strategy`（默认 `auto`）
- `collaboration_mode`（默认 `normal`）

### 0.2 控制面模式判断

| 值 | 语义 | 必填契约 |
|---|---|---|
| `normal`（默认） | 最小控制面，适合 1 个主会话 + 1~2 个子任务或低冲突并行 | `PLAN.md`、`tasks/`、`.meta.yaml`、`allowed_paths`；大文档再补 `section_anchor` 或 `doc_targets(path + section_anchor)` |
| `advanced` | 强治理控制面，只在确实出现并发写冲突或合并顺序风险时启用 | 在 `normal` 基础上强制 `lane_key`、`file_leases`、`approval_target` |

若配置仍为 `normal`，但当前任务满足下列任一条件，应在本任务内升级为 `advanced`，并把升级原因写入 `PLAN.md` 决策日志：

| # | 升级条件 |
|---|---|
| 1 | 活跃并行任务数 `>= 3` |
| 2 | 同一个文件或文档被 2 个及以上活跃任务同时声明 |
| 3 | 同一个文件的不同 section 需要并行推进 |
| 4 | 文档与代码联动，且 review / merge 顺序已经变成关键路径 |

`route_key`、`shared_files_owner`、外部治理层接入仍可在 `advanced` 下补充，但它们属于扩展元数据，不再是最小硬门票。

### 0.3 策略判断（`auto` 模式）

按以下顺序机械判断，命中即停：

| # | 条件 | 策略 |
|---|------|------|
| 1 | 用户显式指定策略 | 用户指定值 |
| 2 | 需要独立工具链 / 服务 / 容器 / 远端环境 | **L4**（isolated） |
| 3 | 需要独立编译 / 运行 / 测试，但仍在同仓库内完成 | **L3**（worktree） |
| 4 | 共享接口、共享文件 owner、或需要分支级顺序集成 | **L2**（stack） |
| 5 | 文件集合不重叠，且可由 coordinator 统一应用 patch | **L1**（patch） |
| 6 | 条件不确定（L1/L2 临界） | **L2**（宁可多协调） |

**兼容别名**：
- `lightweight` 视为 `patch`
- `peers-mcp` 视为 `stack`
- `always-worktree` 视为 `worktree`

### 0.4 输出策略选择

```
并行策略选择：
  控制面模式：[normal/advanced]
  策略：[patch/stack/worktree/isolated]
  原因：[命中条件 #N]
  任务：[task-1: 文件列表], [task-2: 文件列表]
  重叠文件：[无 / 有（owner: task-N）]
  需要独立运行：[是/否]
```

用户确认后进入对应流程。

---

## 控制面前置契约

进入任何并行策略前，必须先建立控制面。默认按 `normal` 执行，只有命中升级条件或用户显式要求时才启用 `advanced`。

推荐由 coordinator 用脚本维护控制面，而不是手工同步状态：

```bash
python scripts/taskctl.py sync
python scripts/taskctl.py start --task T001
python scripts/taskctl.py submit --task T001
python scripts/taskctl.py approve --task T001
python scripts/taskctl.py enqueue --task T001
python scripts/taskctl.py merge --task T001
```

### `normal`（默认）

1. 在 `docs/plan/PLAN.md` 新增任务索引行
2. 在 `docs/plan/tasks/` 创建任务目录
3. 在 `.meta.yaml` 中至少声明：
   - `mode`
   - `allowed_paths`
   - `branch_or_workspace`
   - `depends_on`
4. 普通文档修订可只依赖 `allowed_paths`
5. 若目标是 `> 200` 行的大文档或活文档，再补：
   - 顶层 `section_anchor`
   - 或 `doc_targets` 中的 `path + section_anchor`
6. 大文档任务一次只允许改一个 section，不允许整页重写
7. `.claude/state/MANIFEST.yaml` 只记录当前会话缓存，不作为总真相源；进入 `doing` 后建议把 `current_focus.task_id` 指向当前任务

### `advanced`

在 `normal` 基础上，`.meta.yaml` 额外强制声明：

- `lane_key`
- `file_leases`
- `approval_target`

其中：
- `lane_key` 用于限制“同一写入泳道只能有一个活跃执行者”
- `file_leases` 用于声明当前任务持有的显式写租约，推荐使用结构化 YAML：`path + section_anchor + lease_owner + lease_state`
- `approval_target` 用于显式声明 gate / review / merge 由谁放行
- `route_key`、`shared_files_owner` 可按需补充，用于外部入口映射或补充 owner 注释，但默认不是最小阻断字段

### Coordinator 放行条件

#### `normal`

Coordinator 只有在下面条件全部满足时，才能让任务进入 `doing`：

1. `allowed_paths` 已声明
2. 文档任务若修改大文档，已声明 `section_anchor`，或在 `doc_targets` 中写明 `path + section_anchor`
3. 大文档任务一次只改一个 section，不得整页重写
4. 和所有活跃任务做过重叠检查；若命中升级条件则不能继续停留在 `normal`
5. 任务状态已从 `todo` 更新为 `doing`

#### `advanced`

在 `normal` 基础上，额外要求：

1. `lane_key` 已声明
2. `approval_target` 已声明
3. 若存在同文档 / 同文件的并行 section 写入，`file_leases` 已声明
4. `.claude/state/MANIFEST.yaml` 的 `current_focus.task_id` 已指向当前任务

统一生命周期：

```text
todo -> doing -> in_review -> approved -> queued -> merged
```

补充规则：
- review 退回：`in_review -> doing`
- 发现阻塞：任意状态 -> `blocked`
- 只有 coordinator 能推进 `approved -> queued -> merged`
- `queued` 之后的真实 merge 顺序以 `docs/plan/MERGE_QUEUE.yaml` 为准

---

## 策略 A：Patch（L1，共享工作区 + coordinator 应用）

> 适用：文档、配置、脚本、小范围代码，不需要独立运行，且文件集合完全不重叠。

### 核心原则

- **共享工作区**：不创建 `worktree`
- **Patch 优先**：Agent 优先提交 patch/diff，由 coordinator 统一应用
- **文件边界先声明**：每个任务必须先声明 `allowed_paths`
- **命中升级条件即切 advanced**：一旦同一文件/文档被多个活跃任务声明、同一文件不同 section 需要并行、文档+代码联动且顺序关键、或活跃任务数达到 `3+`，立即升级到 `advanced`
- **大文档先收窄再改**：`README.md`、`CLAUDE.md`、HTML 指南页这类文件，优先用 `doc_targets + section_anchor` 缩小写入范围

### 操作要求

- Agent Prompt 必须声明仅允许改动的文件列表
- 文档任务还应声明 `section_anchor`，并遵守 `claude-workflow-governance.md` 的“文档安全编辑协议”
- coordinator 负责最终 `git add / commit`
- 如果两个任务都需要改 `PLAN.md`，只能 append，不得重写整个文件
- patch 应用后立即验证 `git diff --stat`
- 如果 `allowed_paths` 与活跃任务重叠，或同一文档需要并行改不同 section，任务不得继续停留在 `normal`

---

## 策略 B：Stack（L2，同仓库短分支 / stacked diffs）

> 适用：不需要独立运行，但任务间存在共享接口、共享文件 owner 或需要按依赖顺序集成。

### 核心原则

- **共享仓库，不共享提交边界**：每个任务走短分支、stacked diff 或 virtual branch
- **共享文件唯一 owner**：非 owner 不得修改共享接口文件
- **协调方式不绑定工具**：可使用普通 Git 分支、Graphite、GitButler，`claude-peers-mcp` 只是可选增强
- **先 review，后入队**：每个 stack 节点先过 review，再进入 merge 顺序

### 操作要求

- 每个任务都必须有独立 `branch_or_workspace`
- `.meta.yaml` 必须记录 `depends_on`
- 共享接口调整后，必须更新下游任务 `handoff.md`
- 若任务升级为需要独立 build/run/test，转到 `worktree`
- 只有 review 通过后，任务才能从 `approved` 进入 `queued`

---

## 策略 C：Worktree（L3，独立运行隔离）

> 适用：需要独立编译、运行、测试，或构建产物、依赖环境会污染主工作区。

### 核心原则

- **运行隔离真实有收益**：不是所有并行都默认升到 `worktree`
- **文件边界即任务边界**：共享文件必须声明 owner
- **合并顺序显式化**：先合无共享文件任务，后合共享文件 owner

---

## 策略 D：Isolated（L4，独立 clone / 容器 / devcontainer）

> 适用：工具链冲突、数据库副本、服务编排、CI 级验证、远端运行器等重型场景。

### 核心原则

- **环境隔离优先于 Git 便利性**
- **不与主工作区共享运行态**
- **结果回流前必须先过独立 review 和验收**

---

## Worktree 详细流程（L3）

> 以下为原有 worktree 并行流程，不做改动。

- **解耦是前提**：未通过解耦审查，不得创建 worktree 开始并行
- **Codex 长上下文优势**：每个 worktree 的 Codex Session 独立，互不干扰
- **文件边界即任务边界**：两个任务不得同时修改同一文件
- **文件影响范围表必须产出**：进入 Phase 2 前，必须有一张表列明每个任务允许改动的路径、共享文件及 owner
- **共享文件唯一 owner**：有共享文件时必须指定唯一 owner，非 owner 任务不得修改该文件
- **合并顺序**：先合并无共享文件任务，最后合并共享文件 owner 任务

---

## 并行开发流程（3阶段）

> ⚡ 每个 Phase 切换前执行 Context 健康检查（见 `constants.md`「Context 健康检查门禁」）

### Phase 1：解耦确认（来自 complex 流程 Phase 4.5）

必须满足以下全部条件才能开始并行：

```markdown
## 解耦确认清单
- [ ] 每个任务的修改文件列表互不重叠（或重叠部分已明确声明 owner 并排定串行顺序）
- [ ] 任务依赖关系形成 DAG（无循环依赖）
- [ ] 每个任务有独立的 *-steps.md 文件
- [ ] 并行批次已确定（哪些可同时跑，哪些必须串行）
- [ ] 已产出文件影响范围表（含共享文件 owner 指定）
- [ ] 用户已确认"开始开发"
```

文件影响范围表（必须产出）：

- 模板：`docs/templates/parallel-impact-scope-template.md`
- 产物：`docs/development/[feature]-impact-scope.md`
- 复制命令（Windows PowerShell）：
```powershell
Copy-Item docs/templates/parallel-impact-scope-template.md docs/development/[feature]-impact-scope.md
```

让 Opus/CC 在拆任务时同步产出，在 prompt 里加：
```text
同时输出文件影响范围表，列格式固定为：
任务 | worktree | 允许改动路径 | 共享文件（无则填"-"）| owner（无共享文件则填"-"）。
若存在共享文件，必须指定唯一 owner，并声明非 owner 禁止修改。
```

并行执行计划表（来自 Plan 文档）：

| 批次 | 任务 | Worktree | 依赖 |
|------|------|----------|------|
| 批次1（并行） | task-1, task-2 | [WORKTREE_BASE]/task-1, [WORKTREE_BASE]/task-2 | 无 |
| 批次2（串行） | task-3 | [WORKTREE_BASE]/task-3 | 批次1完成 |

---

### Phase 2：创建 Worktree + 分配任务

先执行仓库状态门禁（必须）：

```bash
cd [DEV_DIR]
git status --short
```

若存在未提交改动：
- 停止创建 worktree，先向用户汇报改动列表
- 让用户选择：提交 / 暂存（仅用户明确同意）/ 放弃（高风险，需明确确认）

仅在仓库状态可继续时，执行：

**根据 BRANCH_MODE 选择创建方式：**

### 若 BRANCH_MODE = temporary（临时分支模式）

```bash
cd [DEV_DIR]

# 按批次创建（批次1示例）
git worktree add [WORKTREE_BASE]/task-1 -b feat/[feature]-task-1
git worktree add [WORKTREE_BASE]/task-2 -b feat/[feature]-task-2

git worktree list   # 验证
```

### 若 BRANCH_MODE = bare（Bare Repo 模式）

在 Bare Repo 模式下，worktree 直接创建在项目根目录下（平铺结构）：

```bash
cd [PROJECT_ROOT]   # 注意：不是 [DEV_DIR]，而是项目根目录

# 按批次创建（批次1示例）
# 直接在根目录下创建分支文件夹
git worktree add task-1 -b feat/[feature]-task-1
git worktree add task-2 -b feat/[feature]-task-2

git worktree list   # 验证
```

**目录结构对比：**

| 模式 | 创建的 worktree 路径 |
|------|---------------------|
| temporary | `[PROJECT_ROOT]/worktrees/task-1/` |
| bare | `[PROJECT_ROOT]/task-1/` |

每个 worktree 独立启动 Codex Session：

**Session cwd 根据 BRANCH_MODE 设置：**

| BRANCH_MODE | Codex Session cwd |
|-------------|-------------------|
| temporary | `[DEV_DIR]/[WORKTREE_BASE]/task-1` |
| bare | `[PROJECT_ROOT]/task-1` |

```
# worktree-task-1 的 Codex Session
mcp__codex__codex({
  model: "gpt-5.4",
  sandbox: "danger-full-access",
  "approval-policy": "on-failure",
  cwd: "[根据 BRANCH_MODE 选择上方对应路径]",
  prompt: "
    ## Context
    - 技术栈：[语言/框架/版本]
    - Steps 文档：docs/development/[feature]-task-1-steps.md
    - 本 worktree 负责的任务：[task-1 描述]
    - 不得修改的文件：[task-2 负责的文件列表]

    ## Task
    按 steps 文档逐任务执行，每个任务完成后 git commit，然后继续下一个。

    ## Constraints
    - 范围：仅限 steps 文档中指定的文件
    - 不引入新依赖
    - 每次 commit 前确认 diff ≤ 200 行

    ## Acceptance
    - [ ] 所有任务完成并提交
    - [ ] pytest / npm test 全部通过
  "
})
// 保存 threadId-task-1
```

**每个 worktree 内部的 TDD 执行循环遵循 `AI开发-PLan-Program-Debug-Claude和Codex协作/05-ClaudeCode+Codex+Git Worktree-功能分支开发流程模板.md` Phase 3，包括：**
- 步骤 3.1：CC Plan Mode 搜索现有代码，回答 Linus 三问
- 步骤 3.4.5：每个任务完成后必须执行多轮 Review（CC 轮次1 + Codex 轮次2），连续 2 轮无新问题才可提交
- Diff 上限：每次 commit 前 `git diff --stat` 确认 ≤ 200 行

---

### Phase 3：监控 + 合并

**CC 监控各 worktree 进度：**

根据 `BRANCH_MODE` 选择正确的路径：

```bash
# 若 BRANCH_MODE = temporary:
git -C [DEV_DIR]/[WORKTREE_BASE]/task-1 log --oneline -5
git -C [DEV_DIR]/[WORKTREE_BASE]/task-2 log --oneline -5

# 若 BRANCH_MODE = bare:
git -C [PROJECT_ROOT]/task-1 log --oneline -5
git -C [PROJECT_ROOT]/task-2 log --oneline -5
```

**批次1完成后，串行执行批次2：**
- 确认批次1所有 worktree 测试通过
- 创建批次2的 worktree
- 批次2的 Codex Session 可以读取批次1的产出

**合并顺序（由 CC 决定）：**

在执行任何 `git merge --no-ff` 之前，必须先输出并等待用户回复"确认合并"：

```
即将合并 [BRANCH_NAME] → main，变更摘要：

变更文件（N 个）：[列表]
Commit 列表（N 条）：[列表]
CI 状态：✅ 通过 / ❌ 未通过 / ⏳ 未验证

请回复"确认合并"后执行。
```

合并前范围门禁（每个任务分支都要执行）：

```bash
python .claude/scripts/verify_parallel_scope.py \
  --table docs/development/[feature]-impact-scope.md \
  --task task-1 \
  --base main
```
注：若仓库默认主分支不是 `main`（如 `master`/`develop`），请替换 `--base` 参数。

规则：
- 返回非 0（失败）时，禁止执行 merge
- 必须先修复范围越界或 owner 冲突，再次校验
- 通过后再执行“确认合并”流程
- 若 `queue_guard.py` 判定当前来源分支不是 merge queue 队首，也禁止继续 merge

```bash
cd [DEV_DIR]
git switch main
git pull --ff-only

# 按依赖顺序合并
git merge --no-ff feat/[feature]-task-1 -m "feat: merge task-1"
# 运行测试确认无回归
pytest / npm test

git merge --no-ff feat/[feature]-task-2 -m "feat: merge task-2"
# 运行测试确认无回归

# 清理 worktree（根据 BRANCH_MODE 选择路径）

## 若 BRANCH_MODE = temporary:
git worktree remove [WORKTREE_BASE]/task-1
git worktree remove [WORKTREE_BASE]/task-2

## 若 BRANCH_MODE = bare:
git worktree remove task-1
git worktree remove task-2

git branch -d feat/[feature]-task-1 feat/[feature]-task-2
```

**冲突处理：**
- 出现冲突 → 立即停止自动合并，CC 先汇报冲突文件与原因（解耦不充分？）
- 冲突必须人工处理，不允许 Codex 自动批量解冲突后直接提交
- 解决冲突后重新运行全量测试与关键 E2E
- 冲突频繁 → 回到解耦审查，重新拆分任务

---

## Session 管理（防止降智）

```
# 每个 worktree 保存各自的 threadId
# threadId-task-1 = "xxx-1"
# threadId-task-2 = "xxx-2"

# 单个 Session 执行超过 3 个任务 → 开新 Session，重新提供 context
# 发现明显低质量输出 → 立即重启 Session
```

---

## 止损规则

- 并行中发现文件冲突 → 停止，回到解耦审查重新拆分
- 某个 worktree Codex 连续失败 3 次 → CC 接管该 worktree，手动处理
- 合并冲突超过 3 处 → 停止合并，分析根因，考虑串行化

---

## 补充：完整发布流程扩展（参考 reference/06）

> 以下阶段补充并行开发完成合并后的完整发布流程，与上方 Phase 1-3 衔接。
> 占位符说明见 reference/06 前置信息表。

---

### Phase 0：读取 Plan 文档

```bash
cat [PLAN_FILE]
```

进入并行开发前必须确认：

- [ ] 所有任务数量和顺序
- [ ] 每个任务涉及的文件路径
- [ ] 测试命令和预期结果
- [ ] 任务间的依赖关系

---

### Phase 1 补充：未提交改动的完整处理

现有 Phase 2 已包含门禁检查，此处补充完整的三选项流程和风险说明：

| 选项 | 命令 | 风险 | 前提 |
|------|------|------|------|
| A 提交 | `git add -A && git commit -m "chore: save wip before [BRANCH_NAME]"` | 低 | 改动是完整功能 |
| B 暂存 | `git stash -u -m "wip: before [BRANCH_NAME]"` | 中（`-u` 会收走未跟踪文件） | 用户明确同意 |
| C 放弃 | `git checkout -- .` | **高（不可恢复）** | 用户明确确认 |

处理后验证：`git status --short` 预期无输出。

---

### Phase 4：版本号更新 + CHANGELOG

所有并行任务合并到 main 后，统一更新版本号。

| 文件类型 | 更新方式 |
|----------|----------|
| `package.json` | `npm version minor --no-git-tag-version` |
| `version.json` | 手动编辑：新功能 minor+1，修复 patch+1，破坏性 major+1 |
| `CMakeLists.txt` | 修改 `PROJECT_VERSION_MAJOR/MINOR/PATCH` |

更新 CHANGELOG.md：

```markdown
## [新版本号] - YYYY-MM-DD

### Added
- [功能1简述]

### Fixed
- [修复1简述]
```

```bash
git add [VERSION_FILE] CHANGELOG.md
git commit -m "chore: bump version to [新版本号]"
```

---

### Phase 5：Release Notes + 推送分支

**5.1 生成 Release 说明**

创建 `docs/releases/[新版本号].md`，包含：概述、新功能、修复、技术变更、已知问题、提交记录。

```bash
git add docs/releases/[新版本号].md
git commit -m "docs: add release notes for [新版本号]"
```

**5.2 push-branch.bat（Windows 代理检测）**

在 `[DEV_DIR]` 下创建 `push-branch.bat`，核心逻辑：
- 检测当前分支（禁止在 main 上执行）
- 探测 `127.0.0.1:1080` 代理是否可用
- 代理可用 → `git -c http.proxy=... push`；不可用 → `git -c http.version=HTTP/1.1 push`

```bash
git add push-branch.bat && git commit -m "chore: add push-branch.bat"
```

**5.3 推送**

```bash
push-branch.bat   # 或 git push origin [BRANCH_NAME]
```

---

### Phase 6：CI 验证

| 构建类型 | 验证方式 |
|----------|----------|
| Android APK | 远端 CI：push 自动触发或手动 `gh run list` / `gh run watch [run_id]` 监控 |
| CMake exe | 本地：`cmake -B build` → `cmake --build build --config Debug` → `ctest -C Debug --output-on-failure` → Release 构建 |
| npm/web | 本地：`node scripts/sync-web.js` 或 `npm run build`，验证输出文件 |

失败处理：查看日志 → worktree 中修复 → push → 重新触发。

---

### Phase 7：合并到 main + 验证

```bash
cd [PROJECT_ROOT]
git switch main
git pull --ff-only origin main
git merge --no-ff [BRANCH_NAME] -m "feat: merge [BRANCH_NAME] - [功能简述]"
```

合并后运行全量测试（npm test / ctest）确认无回归。冲突处理：`git status` → 解决 → `git add && git merge --continue`。

---

### Phase 8：更新 main 版本号 + CHANGELOG

```bash
cat [VERSION_FILE]   # 确认版本号（功能分支已更新则通常无需重复）
```

更新 CHANGELOG 追加 Merged 记录：

```markdown
## [版本号] - YYYY-MM-DD

### Merged
- feat: merge [BRANCH_NAME] - [功能简述]
```

```bash
git add CHANGELOG.md && git commit -m "chore: update CHANGELOG for [版本号]"
```

---

### Phase 9：推送 main + 等待 CI

```bash
push.bat --mode auto --yes --no-pause   # 或 git push origin main
```

等待验证：
- CI APK 构建 → `gh run list --limit 5`
- GitHub Pages（如有）
- Release 页面：确认 APK 文件 + Release 说明均已发布

---

### Phase 10：总结报告 + Plan 文档勾选 + worktree 清理

**10.1 计划文档打勾**

打开 `[PLAN_FILE]`，将完成的 `[ ]` 改为 `[x]`。

**10.2 生成总结报告**

创建 `docs/development/YYYY-MM-DD-[BRANCH_NAME]-summary.md`，包含：

- 完成情况表（任务 / 状态 / 备注）
- 详细修改点（文件、函数、测试用例数）
- 遇到的问题及解决方案
- 生成的文件清单
- 构建结果（APK / exe / Pages）
- 后续建议

**10.3 清理 worktree**

```bash
cd [DEV_DIR]   # temporary 模式
# 或 cd [PROJECT_ROOT]   # bare 模式

# 根据 BRANCH_MODE 选择路径
git worktree remove [WORKTREE_BASE]/[BRANCH_NAME]   # temporary
git worktree remove [BRANCH_NAME]                   # bare

git branch -d [BRANCH_NAME]   # 可选
```

**10.4 自我改进联动（必做）**

必须将并行开发中遇到的文件冲突、依赖遗漏、解耦不足等经验写入 `.claude/memory/lessons/`。

> 参见 `claude-workflow-governance.md` 中的「Self-Improvement 全局规则」

---

### 合并确认清单模板

在执行任何 `git merge --no-ff` 之前，AI 必须先输出以下内容并等待用户回复"确认合并"：

```
即将合并 [BRANCH_NAME] → main，变更摘要：

变更文件（N 个）：
  M  src/xxx.js
  A  docs/releases/x.x.x.md
  ...

Commit 列表（N 条）：
  abc1234 feat: 功能描述1
  def5678 feat: 功能描述2
  ...

CI 状态：✅ 通过 / ❌ 未通过 / ⏳ 未验证

请回复"确认合并"后执行，或说明需要调整的内容。
```
