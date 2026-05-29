# claude-workflow-init.md — 项目初始化配置

> 本文档在项目首次使用时执行一次，结果写入 `claude-workflow-config.md` 的“项目常量”区块。
> 后续开发流程通过读取常量使用这些配置，无需重复询问。

---

## 触发条件

满足以下任一条件时，AI 自动触发本流程：

- 用户说"初始化项目" / "整理目录" / "配置 worktree"
- 检测到根目录存在 `.git/` 但 `claude-workflow-config.md` 中无“项目常量”区块
- 用户显式要求"运行 init 流程"

---

## 推荐主流程（安全默认值）

### Step 1：复制模板并保持目录结构

把模板仓库整体复制到目标项目后，先只做最小确认，不做目录重组。

必须保留的共享入口：

| 文件 | 角色 |
|------|------|
| `CLAUDE.md` | 项目级行为入口 |
| `AGENTS.md` | Codex 侧说明 |
| `.claude/settings.json` | 共享配置主入口 |
| `.claude/settings.local.example.json` | 本机覆写示例 |
| `.claude/workflows/` | 工作流文档 |
| `.claude/scripts/` | Hook 脚本 |

初始化时，若目标项目缺少运行期文档骨架，还要一并补齐以下目录和文件：

| 路径 | 最小要求 |
|------|----------|
| `docs/plan/` | 保留 `PLAN.md` 总计划入口，继续承载任务状态 |
| `docs/修订记录/` | 新建 `目录索引.md`，写明“这里只记录具体问题为什么这样改，不承担 changelog 职责” |
| `docs/修订记录/模板/` | 预置 `0000-模板-轻量模式.md`，只存模板，不存真实记录 |
| `docs/修订记录/<任务主题>/` | 首次写真实记录时再创建，目录名直接表明任务主题 |

对 `docs/修订记录/目录索引.md` 的初始化要求：
- 建立 Markdown 表格表头：`编号 | 日期 | 模块/问题范围 | 核心结论 | 文件`
- 建立“禁止重试方案速查”区块
- 保持“先读索引，再按需深读任务目录下记录文件”的使用方式

### Step 2：校验配置边界

先检查 JSON 语法，再检查职责边界。

```bash
python -m json.tool .claude/settings.json
python -m json.tool .claude/settings.local.example.json
```

校验要求：
- `.claude/settings.json` 承载共享的 permissions、hooks、`extraKnownMarketplaces`、`enabledPlugins`
- `.claude/settings.local.example.json` 只提供本机覆写示例
- `.claude/settings.local.json` 只放本机专属覆写，不放模板共享真相
- 不把当前机器的绝对路径写进共享配置

### Step 3：验证 hooks 与插件

先确认核心 Hook 脚本可读、可运行，再确认插件路径和回退链路。

```bash
python .claude/scripts/auto_checkpoint_commit.py --dry-run
python .claude/scripts/gate_guard.py
```

校验要求：
- 官方 Cartographer 插件可用时，优先产出或刷新 `docs/CODEBASE_MAP.md`
- 插件不可用或未启用时，自动回退到 `largebase-structured-scan extract`
- `docs/CODEBASE_MAP.md` 是运行期产物，不要求模板仓库预置

### Step 4：写入项目常量

将当前项目选择写入 `claude-workflow-config.md` 的“项目常量”区块。

优先确认的常量：
- `BRANCH_MODE`
- `WORKTREE_BASE`
- `MAIN_BRANCH`
- `PROJECT_ROOT`
- `INIT_DATE`

### Step 5：完成验收

初始化完成前，做一次轻量验收。

```bash
git status --short
git diff --name-only HEAD
```

验收要求：
- 没有把旧的说明路径和任务日志路径带进新模板
- 没有把目录重组、归档、bare repo 转换混进默认初始化流程
- 复制后可以直接继续工作流，不需要先做危险清理
- `docs/修订记录/` 骨架已就位，且没有把 `docs/changes/` 和“局部决策账本”职责混写

## 可选附录

### A. Bare Repo 转换

仅当项目确实需要裸仓库模式时，再参考单独的迁移说明执行。不要把 bare repo 转换当成模板初始化的默认步骤。

### B. 目录重组与归档

如果历史项目里确实存在需要归档的旧目录，先确认范围，再单独处理。新模板复制场景默认不做目录移动。

### C. 危险清理

`rm -rf`、`Remove-Item -Recurse`、`git clean -f` 这类操作只在明确批准后、并且作为独立任务执行，不出现在默认 init 主流程中。

---

## 注意事项

- 本流程只执行一次；常量写入后，后续流程直接读取，不再询问
- 用户可随时手动编辑 `claude-workflow-config.md` 中的“项目常量”和“用户偏好”区块
- 校验配置或补本机覆写前，尽量先确认 `git status` 干净，避免把历史改动混进模板初始化
