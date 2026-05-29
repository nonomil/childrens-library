# claude-workflow-config.md — 项目配置与偏好契约

> 本文档承载模板复制后仍需长期保留的配置真相源：共享配置边界、项目常量、用户偏好。
> 所有 workflow 默认只读 `claude-workflow-constants.md`；只有涉及初始化、并行协作、偏好分流时才按需加载本文档。

---

## 1. 配置边界

### 1.1 共享 / 本地 / 运行产物

| 位置 | 角色 | 是否提交 git |
|------|------|-------------|
| `.claude/settings.json` | 项目共享配置主入口 | 是 |
| `.claude/settings.local.json` | 本机专属覆写 | 否 |
| `.claude/state/.gate-approved` | 当前任务门禁放行凭据 | 否 |
| `docs/CODEBASE_MAP.md` | Cartographer / extract 运行期产物 | 按项目策略决定 |
| `docs/scan/` | largebase 扫描产物 | 按项目策略决定 |
| `.claude/backups/` | 自动 checkpoint 备份 | 否 |

### 1.2 共享配置规则

- `.claude/settings.json` 承载共享的 permissions、hooks、`extraKnownMarketplaces`、`enabledPlugins`
- `.claude/settings.local.json` 只放本机覆写，不作为模板共享真相源
- 共享配置禁止写当前机器的绝对路径；优先相对项目根目录或 Claude Code 官方支持的项目级写法
- 模板迁移时，默认路径是：复制仓库即可得到共享配置；个人只额外维护未提交的 `settings.local.json`

### 1.3 Cartographer 双轨契约

- 主路径：官方 Cartographer 插件已启用时，使用插件生成或刷新 `docs/CODEBASE_MAP.md`
- 回退路径：插件不可用、未启用或执行失败时，回退到 `largebase-structured-scan extract`
- 统一输出：无论插件还是回退链路，最终都以 `docs/CODEBASE_MAP.md` 为统一消费入口
- 重要：仅把插件目录 vendored 到仓库不会自动识别，必须通过 `.claude/settings.json` 的 `extraKnownMarketplaces` 与 `enabledPlugins` 显式启用

---

## 2. 项目常量（init 写入）

> 由 `claude-workflow-init.md` 在项目首次使用时补齐；后续 workflow 直接读取，不重复询问。

| 常量 | 默认值 | 说明 |
|------|--------|------|
| `BRANCH_MODE` | `temporary` | 分支管理模式：`temporary` / `bare` |
| `WORKTREE_BASE` | `worktrees` | worktree 目录前缀，可选：`worktrees` / `.worktree` / `.` |
| `MAIN_BRANCH` | `master` | 主分支名，可选：`master` / `main` |
| `PROJECT_ROOT` | _(运行时自动检测)_ | 项目根目录绝对路径 |
| `INIT_DATE` | _(未初始化)_ | 初始化日期 |

**引用方式：**

```bash
# 创建 worktree 时，路径使用 WORKTREE_BASE
git worktree add [PROJECT_ROOT]/[WORKTREE_BASE]/feat-xxx -b feat/xxx

# 合并时，目标分支使用 MAIN_BRANCH
git switch [MAIN_BRANCH]
git merge --no-ff feat/xxx
```

---

## 3. 用户偏好（preferences.json）

> 配置文件：`.claude/preferences.json`。文件不存在或字段缺失时使用默认值，不阻断流程。

### 3.1 读取规则

1. 每个任务开始时读取一次，任务内冻结，不响应中途修改
2. 字段缺失时使用默认值；值非法时使用默认值并输出警告
3. 用户说“初始化偏好”或“设置偏好”时，进入交互式引导生成

### 3.2 `profile`（模式预设，覆盖全局）

| 值 | 效果 |
|----|------|
| `standard`（默认） | 正常工作流，各字段独立控制 |
| `minimal` | 关闭工作流和自动化，CC 退化为纯对话助手 |

`minimal` 等效于：
- `git_strategy=skip`
- `codex_invocation=skip`
- `review_strategy=cc_only`
- 跳过 workflow 子文档、Stop Hook 自动提交和 Changelog 生成

### 3.3 `git_strategy`（Git 提交策略）

| 值 | 行为 | 影响点 |
|----|------|--------|
| `auto_commit` | Stop Hook 自动提交（默认） | `auto_checkpoint_commit.py` |
| `ask` | 收尾时询问用户是否提交 | CLAUDE.md Step 4 |
| `skip` | 不自动提交，用户自行管理 | Stop Hook 直接退出 |

### 3.4 `codex_invocation`（Codex 调用策略）

| 值 | 行为 | 影响点 |
|----|------|--------|
| `cc_auto_decides` | CC 按复杂度判断是否调 Codex（默认） | CLAUDE.md Step 2 |
| `always` | 所有代码改动都调 Codex | CLAUDE.md Step 2 |
| `ask` | 每次涉及代码改动时询问用户 | CLAUDE.md 门禁 |
| `skip` | 不使用 Codex，CC 自己处理所有代码 | 各 workflow 旁路 fallback |

`skip` 模式下的 fallback：
- debug：CC 自行定位和修复
- research：CC 用 WebSearch / Grep 替代 Codex 深读
- parallel：使用 CC 多会话 / 子代理替代 Codex session
- largebase：CC 用 Grep / Glob + 本地 extract 替代 Codex 辅助扫描

### 3.5 `parallel_strategy`（执行隔离方式）

| 值 | 行为 | 影响点 |
|----|------|--------|
| `auto`（默认） | CC 自动选择 `patch / stack / worktree / isolated` | `claude-workflow-parallel.md` |
| `patch` | 强制 L1：同工作区，以 patch / coordinator 应用为主 | 并行策略 A |
| `stack` | 强制 L2：短分支 / stacked diffs / virtual branches | 并行策略 B |
| `worktree` | 强制 L3：worktree 隔离（需要独立 build/run/test） | 并行策略 C |
| `isolated` | 强制 L4：独立 clone / 容器 / devcontainer / runner | 并行策略 D |

`auto` 判断顺序：

| # | 条件 | 策略 |
|---|------|------|
| 1 | 用户显式指定策略 | 用户指定值 |
| 2 | 需要独立工具链 / 服务 / 容器 / CI 环境 | `isolated` |
| 3 | 需要独立编译 / 运行 / 测试，但仍在同仓库内完成 | `worktree` |
| 4 | 存在共享接口、共享文件 owner、或需要按依赖顺序集成 | `stack` |
| 5 | 改动文件不重叠，且可由 coordinator 统一应用 patch | `patch` |
| 6 | 条件不确定 | `stack` |

兼容别名：
- `lightweight` → `patch`
- `peers-mcp` → `stack`
- `always-worktree` → `worktree`

### 3.6 `collaboration_mode`（协作控制面复杂度）

| 值 | 行为 | 影响点 |
|----|------|--------|
| `normal`（默认） | 最小控制面：`PLAN.md` + `tasks/` + `.meta.yaml` + `allowed_paths`；文档大文件再补 `section_anchor` 或 `doc_targets(path + section_anchor)` | `claude-workflow-parallel.md` |
| `advanced` | 在 `normal` 基础上强制 `lane_key / file_leases / approval_target` | `claude-workflow-parallel.md` |

任务内自动升级到 `advanced` 的条件：
- 活跃并行任务数 `>= 3`
- 同一个文件或文档被 2 个及以上活跃任务同时声明
- 同一个文件需要按不同 section 并行推进
- 文档与代码联动，且 review / merge 顺序已经变成关键路径

### 3.7 并行协作控制面（总真相源）

| 位置 | 角色 |
|------|------|
| `docs/plan/PLAN.md` | 全局任务索引、依赖、merge 顺序 |
| `docs/plan/tasks/*/.meta.yaml` | 单任务结构化状态 |
| `docs/plan/MERGE_QUEUE.yaml` | merge queue 真相源，决定真实合并顺序 |
| `.claude/state/MANIFEST.yaml` | 当前会话缓存，不是全局真相源 |

规则：
- `PLAN.md` 只保留索引和状态，不存长篇执行细节
- 每个任务的详细步骤写入 `docs/plan/tasks/`
- 推荐通过 `python scripts/taskctl.py ...` 维护状态机、queue 与 `MANIFEST.yaml`
- `normal` 模式最小必填契约：`mode`、`allowed_paths`、`branch_or_workspace`、`depends_on`
- 文档任务若目标文档 `> 200` 行，必须声明 `section_anchor`，或在 `doc_targets` 中写明 `path + section_anchor`
- `advanced` 模式额外必填：`lane_key`、`approval_target`
- 同文档 / 同文件的并行 section 写入，再额外补 `file_leases`
- `route_key`、`shared_files_owner` 仍可作为扩展元数据保留，但不再属于最小硬门票
- 当前会话进入 `doing` 前，建议把 `.claude/state/MANIFEST.yaml` 的 `current_focus.task_id` 指向当前任务；文档冲突 Hook 会依赖它判断当前写入者，并在 `Read` 文档时刷新 freshness snapshot

<!-- BEGIN:doc-edit-contract -->
### 3.7.1 文档并行编辑附加契约

当任务涉及高频 `.md/.html` 活文档，或单文档长度 `> 200` 行时，不再只声明 whole-file `allowed_paths`，而是追加以下字段：

```yaml
doc_targets:
  - path: "docs/project-overview.md"
    section_anchor: "project-structure-tree"
file_leases:
  - path: "docs/project-overview.md"
    section_anchor: "project-structure-tree"
    lease_owner: "T001"
    lease_state: "active"
```

字段语义：
- `doc_targets`：任务允许修改的文档片段集合；当文档 `> 200` 行时，至少声明 `path + section_anchor`
- `section_anchor`：文档内稳定锚点，对应 `<!-- BEGIN:... -->` / `<!-- END:... -->`
- `file_leases`：当多个活跃任务共享同一文档时，用于声明 section 级租约；advanced 下每个任务都必须声明
- `lease_state`：推荐值 `active / released`

freshness 规则：
- 文档被 `Read` 后，Hook 会把当前 `content_hash` 写入 `.claude/state/MANIFEST.yaml` 的 `doc_freshness`
- 真正执行 `Edit / Write / MultiEdit` 前必须再次比对；若文件已变化，先重读，不得继续套旧 patch

兼容策略：
- 简单任务或非活文档仍可只用 `allowed_paths`
- 一旦文档 `> 200` 行，Hook 会要求 `section_anchor` 或 `doc_targets.path + section_anchor`，并阻断整页重写
- 一个任务一次只允许改一个 section；命中多个锚点时必须拆成多个任务
- 一旦同一文档出现 2 个及以上活跃任务，或同一文件需要并行推进不同 section，必须升级 `advanced` 并补齐 `file_leases`
- 涉及 generated block 时，必须改上游生成源，不得直接改文档落地产物
<!-- END:doc-edit-contract -->

### 3.8 `review_strategy`（代码审查策略）

| 值 | 行为 | 影响点 |
|----|------|--------|
| `auto_gate` | diff ≤100 行 CC 自查，>100 行触发 Codex 深审（默认） | CLAUDE.md Step 3 |
| `cc_only` | 始终由 CC 审查，不调 Codex | CLAUDE.md Step 3 |
| `codex_required` | 所有审查都必须经 Codex | CLAUDE.md Step 3 |

### 3.9 `expert_review_strategy`（多专家评审升级策略）

| 值 | 行为 | 影响点 |
|----|------|--------|
| `manual`（默认） | 仅当用户明确要求“多专家评审 / 多视角审查 / 并行审查”时触发 | `claude-workflow-multi-review.md` |
| `auto_on_high_risk` | 命中高风险文件、多材料联审或普通 review 分歧明显时自动升级 | `claude-workflow-multi-review.md` |
| `always` | 一旦进入 review，优先先走多专家评审 | `claude-workflow-multi-review.md` |

推荐解释：

- `manual`：最轻，适合作为模板默认值
- `auto_on_high_risk`：适合工程化要求高、误判成本高的项目
- `always`：只适合审计型或高合规项目，不建议默认开启

---

## 4. 推荐读取关系

- 初始化 / 迁移模板：读取本文档 + `claude-workflow-init.md`
- 并行开发：读取本文档 + `claude-workflow-parallel.md`
- 多专家评审：读取本文档 + `claude-workflow-multi-review.md`
- 只做普通开发：优先读取 `claude-workflow-constants.md`，无需默认加载本文档全部内容

---

## 版本历史

- 2026-02-28：从 constants 拆出项目常量区块
- 2026-04-07：明确 `.claude/settings.json` 为共享入口，`.claude/settings.local.json` 为本机覆写
- 2026-04-07：明确 `parallel_strategy` 负责执行隔离，`collaboration_mode` 负责控制面复杂度
- 2026-04-07：补充文档任务契约：`doc_targets`、`section_anchor`、`file_leases` 与 `current_focus.task_id`
- 2026-04-08：新增 `expert_review_strategy`，用于控制多专家评审的触发方式
