# Docs Index: full-project-scan

> Generated at: 2026-04-02T19:29
> Scope: .claude/workflows, .claude/rules, .claude/scripts, .claude/skills, docs
> 文档数: 98

## 文档列表

| 文档 | 字数 | 含代码块 | 含表格 | 摘要 |
|------|------|----------|--------|------|
| `code-style-cpp.md` | 2K | ✓ | ✓ | paths: - "**/*.cpp" - "**/*.cc" - "**/*.h" - "**/*.hpp" |
| `code-style.md` | 2K | ✓ | ✓ | paths: - "**/*.py" - "**/*.pyi" |
| `project.md` | 763 |  | ✓ | Python 3.10+ / Pillow / tkinter / SQLite |
| `security-cpp.md` | 1K | ✓ |  | paths: - "**/*.cpp" - "**/*.cc" - "**/*.h" - "**/*.hpp" |
| `security.md` | 1K | ✓ |  | paths: - "**/*.py" |
| `testing-cpp.md` | 3K | ✓ | ✓ | paths: - "tests/**/*.cpp" - "tests/**/*.cc" - "test_*.cpp" |
| `testing.md` | 2K | ✓ |  | paths: - "tests/**/*.py" - "test_*.py" - "*_test.py" |
| `workflows.md` | 1K | ✓ |  | > 无 paths 限制，所有文件类型均加载。 |
| `README.md` | 4K | ✓ | ✓ | 本目录包含 Claude Code + Codex MCP 协作中使用的自动化脚本。所有脚本通过 Hook 机制触发。 |
| `README.md` | 2K | ✓ | ✓ | 本目录包含 Claude Code + Codex 协作流水线中使用的自定义技能。 |
| `README.md` | 2K | ✓ |  | 本目录包含 Claude Code + Codex MCP 协作的工作流文档。所有工作流遵循 `claude-workf... |
| `claude-workflow-complex.md` | 8K | ✓ | ✓ | > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 触发条件：任... |
| `claude-workflow-constants.md` | 16K | ✓ | ✓ | 此文档是所有工作流的"单一真相"来源。所有其他文档应引用此文档，而非复制规则。 |
| `claude-workflow-cpp-build.md` | 2K | ✓ | ✓ | 用户说"编译" / "build" / "构建" / "CMake" / "MSBuild"，且涉及 C++ 项目。 |
| `claude-workflow-cpp-test.md` | 2K | ✓ | ✓ | 用户说"运行测试" / "跑单测" / "gtest" / "单元测试" / "test"，且涉及 C++ 项目。 |
| `claude-workflow-debug.md` | 6K | ✓ | ✓ | > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 触发条件：用... |
| `claude-workflow-init.md` | 4K | ✓ | ✓ | > 本文档在项目首次使用时执行一次，结果写入 `claude-workflow-constants.md` 的"项目配置... |
| `claude-workflow-largebase.md` | 8K | ✓ | ✓ | > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 适用：源码文... |
| `claude-workflow-parallel.md` | 9K | ✓ | ✓ | > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 触发条件：任... |
| `claude-workflow-research.md` | 5K | ✓ | ✓ | > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 触发条件：用... |
| `claude-workflow-review.md` | 4K | ✓ | ✓ | > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 触发条件：用... |
| `CODEBASE_MAP.md` | 11K | ✓ | ✓ | last_mapped: 2026-04-02T11:26:03Z total_files: 304 total_tok... |
| `IMPROVEMENTS-2026-02-26.md` | 6K | ✓ | ✓ | 本次改进涉及全局硬约束统一、工作流流程对齐、大型代码库扫描升级三个方向。 |
| `skill.md` | 1K |  | ✓ | name: "git" description: "在 git 仓库中完成代码修改、开始复杂任务前、需要查看历史或回退时... |
| `changelog-draft.md` | 6K |  |  | - 2026-02-28 11:55 [7c3498f] checkpoint: 11:53 - 2026-02-28 ... |
| `plan-2025-02-28-cartographer-phase1.md` | 1K |  |  | 将 Cartographer 作为 largebase-structured-scan skill 的前置架构地图提供者... |
| `plan-2026-02-26-image-merger-requirements.md` | 847 | ✓ |  | > 日期：2026-02-26 > 状态：已确认 ✅ |
| `plan-2026-02-26-image-merger-v2-requirements.md` | 2K | ✓ | ✓ | > 日期：2026-02-26 > 状态：已确认 ✅ > 分支：feat/image-merger-v2 > 基于：im... |
| `plan-2026-02-27-merge-reference-docs.md` | 3K | ✓ |  | **日期**：2026-02-27 **任务**：从 `AI开发-PLan-Program-Debug-Claude和C... |
| `plan-2026-02-27-refactor-claude-structure-requirements.md` | 1K |  | ✓ | **日期**：2026-02-27 **任务**：验证和优化 `.claude/` 目录结构，确保文档引用关系正确，添加... |
| `plan-2026-02-27-refactor-claude-structure.md` | 2K | ✓ | ✓ | **日期**：2026-02-27 **状态**：待用户确认 **复杂度**：复杂开发（涉及 5+ 文件，跨模块） |
| `plan-2026-02-28-largebase-token-optimization.md` | 11K | ✓ | ✓ | > 日期：2026-02-28 > 主题：对比当前 largebase-structured-scan 与 GitNex... |
| `plan-2026-03-03-workflow-refactor.md` | 2K |  |  | > **生成日期**：2026-03-03 > **依据参考**：23.1 审查报告、23.2 审查报告及全量核查补充 ... |
| `plan-2026-03-09-thread-registry-requirements.md` | 809 |  | ✓ | **日期**：2026-03-09 **任务**：为项目新增多线程协作注册表规范，并提供 3 个 YAML 示例文件 |
| `plan-2026-04-02-hook-scripts-optimization.md` | 1K |  | ✓ | > 创建时间: 2026-04-02 > 状态: 需求讨论 |
| `walkthrough.md` | 2K | ✓ | ✓ | > 审查时间：2026-03-01 · 覆盖文件：CLAUDE.md, AGENTS.md, README.md, co... |
| `skill.md` | 1K | ✓ | ✓ | name: "init" description: "分析项目结构，生成项目和模块的 CLAUDE.md 文档" use... |
| `01-architecture.md` | 2K | ✓ | ✓ | memory-system/ ├── scripts/                  # 核心实现（索引、搜索、状态... |
| `02-dataflow.md` | 2K |  | ✓ | ｜ 结构 ｜ 字段 ｜ 类型 ｜ 用途 ｜ 位置 ｜ ｜------｜------｜------｜------｜----... |
| `03-api-surface.md` | 2K | ✓ | ✓ | ｜ 名称 ｜ 签名/形态 ｜ 文件:行号 ｜ 调用方 ｜ ｜------｜-----------｜----------｜... |
| `04-reference-constraints.md` | 1K |  | ✓ | ｜ 文档A ｜ 文档B ｜ 冲突点 ｜ 建议采用 ｜ 理由 ｜ ｜------｜------｜-------｜-----... |
| `05-impact-matrix.md` | 1K |  | ✓ | ｜ 修改点 ｜ 直接影响 ｜ 间接影响 ｜ 回归验证点 ｜ 风险等级 ｜ ｜-------｜---------｜----... |
| `06-exec-brief.md` | 913 |  | ✓ | - 代码结构集中在 `scripts/memory.py`，属于“单文件多职责”形态。 - 参数与 schema 文档化... |
| `CLAUDE.preview.md` | 258 |  |  | <!-- largebase-scan:auto-summary:start --> |
| `01-architecture.md` | 8K |  | ✓ | ｜ L1 ｜ L2 ｜ ?? ｜ ??? ｜ ???? ｜ ｜ --- ｜ --- ｜ --- ｜ ---: ｜ ---... |
| `02-dataflow.md` | 3K |  | ✓ | ｜ ??? ｜ ?????? ｜ ?? ｜ ?? ｜ ｜ --- ｜ --- ｜ --- ｜ --- ｜ ｜ `scan... |
| `03-api-surface.md` | 24K | ✓ | ✓ | ｜ API ｜ ?? ｜ ?? ｜ ｜ --- ｜ --- ｜ --- ｜ ｜ `parse_gitignore` ｜ ... |
| `04-reference-constraints.md` | 2K |  | ✓ | ｜ ??A ｜ ??B ｜ ???? ｜ ???? ｜ ?? ｜ ???? ｜ ｜ --- ｜ --- ｜ --- ｜ ... |
| `05-impact-matrix.md` | 1K |  | ✓ | ｜ ??? ｜ ???? ｜ ???? ｜ ??? ｜ ???? ｜ ｜ --- ｜ --- ｜ --- ｜ --- ｜... |
| `06-exec-brief.md` | 1K |  | ✓ | ｜ ?? ｜ ??? ｜ ?? ｜ ???? ｜ ｜ ---: ｜ --- ｜ --- ｜ --- ｜ ｜ 1 ｜ ??... |
| `01-architecture.md` | 2K |  | ✓ | ｜ L1 ｜ L2 ｜ 类型 ｜ 文件/目录数量 ｜ 职责 ｜ ｜ --- ｜ --- ｜ --- ｜ ---: ｜ -... |
| `02-dataflow.md` | 2K |  | ✓ | ｜ 数据结构 ｜ 定义位置 ｜ 结构形态 ｜ 生产者 ｜ 消费者 ｜ 关键约束 ｜ ｜ --- ｜ --- ｜ --- ... |
| `05-impact-matrix.md` | 1K |  | ✓ | ｜ 修改点 ｜ 直接影响 ｜ 间接影响 ｜ 验证点 ｜ ｜ --- ｜ --- ｜ --- ｜ --- ｜ ｜ `mer... |
| `06-exec-brief.md` | 1K |  | ✓ | ｜ 排名 ｜ 风险项 ｜ 触发条件 ｜ 影响范围 ｜ 建议控制 ｜ ｜ ---: ｜ --- ｜ --- ｜ --- ｜... |
| `01-architecture.md` | 3K | ✓ | ✓ | > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE... |
| `02-dataflow.md` | 3K | ✓ | ✓ | > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE... |
| `03-api-surface.md` | 2K | ✓ | ✓ | > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE... |
| `04-reference-constraints.md` | 2K |  | ✓ | > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE... |
| `05-impact-matrix.md` | 1K | ✓ | ✓ | > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE... |
| `06-exec-brief.md` | 1K |  | ✓ | > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE... |
| `CODEBASE_MAP.md` | 2K |  | ✓ | > Generated at: 2026-03-01T23:12 > Scope: .claude/skills/lar... |
| `docs-index.md` | 3K | ✓ | ✓ | > Generated at: 2026-03-01T23:12 > Scope: .claude/skills/lar... |
| `CODEBASE_MAP.md` | 244 |  | ✓ | > Generated at: 2026-03-01T23:12 > Scope: F:\KLD_WORK\产品方案\翘... |
| `docs-index.md` | 3K | ✓ | ✓ | > Generated at: 2026-03-01T23:12 > Scope: F:\KLD_WORK\产品方案\翘... |
| `CODEBASE_MAP.md` | 2K |  | ✓ | > Generated at: 2026-03-01T23:19 > Scope: .claude/skills/lar... |
| `docs-index.md` | 3K | ✓ | ✓ | > Generated at: 2026-03-01T23:19 > Scope: .claude/skills/lar... |
| `CODEBASE_MAP.md` | 188 |  | ✓ | > Generated at: 2026-03-01T23:19 > Scope: .claude/workflows |
| `docs-index.md` | 11K | ✓ | ✓ | > Generated at: 2026-03-01T23:19 > Scope: .claude/workflows ... |
| `parallel-impact-scope-template.md` | 790 |  | ✓ | Usage notes: - Each task can only edit files inside its allo... |
| `largebase-structured-scan 重构指导手册.md` | 16K | ✓ | ✓ | > 版本：v2.0 > 目标：修复现有设计的四个核心缺陷，不推翻重来 > 执行者：Claude Code（自动执行，无需... |
| `扫描报告文档规范 v1.0.md` | 10K | ✓ | ✓ | > 适用范围：largebase-structured-scan 所有输出文档（01 ~ 06） > 执行者：生成报告的... |
| `code-style-cpp.md` | 2K | ✓ | ✓ | paths: - "**/*.cpp" - "**/*.cc" - "**/*.h" - "**/*.hpp" |
| `code-style-python.md` | 2K | ✓ | ✓ | paths: - "**/*.py" - "**/*.pyi" |
| `security-cpp.md` | 1K | ✓ |  | paths: - "**/*.cpp" - "**/*.cc" - "**/*.h" - "**/*.hpp" |
| `security-python.md` | 1K | ✓ |  | paths: - "**/*.py" |
| `testing-cpp.md` | 3K | ✓ | ✓ | paths: - "tests/**/*.cpp" - "tests/**/*.cc" - "test_*.cpp" |
| `testing-python.md` | 2K | ✓ |  | paths: - "tests/**/*.py" - "test_*.py" - "*_test.py" |
| `workflows.md` | 1K | ✓ |  | > 无 paths 限制，所有文件类型均加载。 |
| `编码规范.md` | 3K | ✓ |  | 好，我来调研一下业界主流的 AI 编码工作流规范实践。好，信息够了。下面是完整的调研结论。 |
| `AI Agent 记忆系统改造模板-v2.md` | 8K | ✓ | ✓ | > 适用于：Claude Code / 任何基于 LLM 的 Coding Agent 项目 > 参考来源：智谱 AI ... |
| `AI Agent 记忆系统改造模板.md` | 8K | ✓ | ✓ | > 适用于：Claude Code / 任何基于 LLM 的 Coding Agent 项目 > 参考来源：智谱 AI ... |
| `Memory Skill — CC 原生记忆管理.txt` | 2K | ✓ | ✓ | > 无需外部 API / MCP 服务器。CC 直接用 Read/Write/Grep 管理记忆文件。 > 触发后按下方... |
| `complex.md — Phase 4 Prompt 替换内容.md` | 1K | ✓ |  | - Plan 文档（已定稿）：[PLAN_DIR]YYYY-MM-DD-[FEATURE_NAME].md |
| `constants.md — Codex Prompt 模板替换内容.md` | 1K | ✓ |  | > **Context 注入原则（借鉴 Trellis 按需加载机制）** > > Codex Session 启动时，... |
| `constants.md — 路径 A 替换内容（Codex 调用规范第一节）.md` | 1K | ✓ |  | **适用环境**：CLI 终端 / VS Code 扩展 / Desktop App（装后需重启 Claude Code... |
| `Claude流程优化意见.md` | 3K | ✓ | ✓ | 我来分析这套 Claude Code + Codex MCP 协作工作流，找出潜在问题和优化空间。先搜索一下当前 AI ... |
| `simpread-Claude Code 源码泄露事件全解析：一场意外背后的技术狂欢与冷思考.md` | 12K | ✓ |  | > 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp... |
| `simpread-看了 ClaudeCode 源码，我发现我的软件跟他非常像.md` | 4K | ✓ |  | > 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp... |
| `vibecoding经验总结--两个开源项目clawcode-FBM.md` | 6K | ✓ | ✓ | > 来源：Claude Code 源码泄露（claw-code）+ AuroraFairy 开发者复盘 + FBM / ... |
| `防止AI误删文件-三层防护方案.md` | 6K | ✓ |  | > 适用场景：Claude Code + Codex MCP 协作开发，或任何通过 AI Agent 执行 shell ... |
| `code_style.md` | 389 |  |  | - 函数/变量：snake_case - 类：PascalCase - 常量：UPPER_SNAKE_CASE |
| `code_style_cpp.md` | 1K |  |  | - 默认使用 C++17，有明确需求时可升至 C++20 - 禁止使用已废弃特性（`auto_ptr`、`registe... |
| `project_template.md` | 682 |  | ✓ | Python 3.10+ / Pillow / tkinter / SQLite |
| `security.md` | 363 |  |  | - 所有输入路径必须存在且可读：`Path.is_file()` / `Path.is_dir()` - 文件类型校验在... |
| `security_cpp.md` | 692 |  |  | - 禁止裸 `new`/`delete`，用智能指针 - 数组访问用 `.at()` 代替 `[]`（需要边界检查时） ... |
| `testing.md` | 364 | ✓ |  | python -m pytest tests/ -v |
| `testing_cpp.md` | 864 | ✓ | ✓ | - 默认使用 Google Test（gtest） - Mock 使用 Google Mock（gmock，gtest ... |
| `项目规则说明.md` | 4K | ✓ | ✓ | 业界的主流做法和你现在的结构对比 AGENTS.md 已经成为一个开放标准，被超过 6 万个开源项目使用，定位是"给 A... |

## code-style-cpp.md

路径: `.claude/rules/code-style-cpp.md`
> paths: - "**/*.cpp" - "**/*.cc" - "**/*.h" - "**/*.hpp"

### 标题大纲

- 代码风格（C++） (L9)
  - 标准版本 (L13)
  - 命名 (L18)
  - 文件组织 (L31)
  - 内存管理 (L43)
  - 类设计 (L59)
  - 类型与转换 (L67)
  - 现代 C++ 惯用法 (L74)
  - 错误处理 (L83)
  - 并发 (L90)
  - 格式（clang-format 管辖） (L97)

### 代码块

- `cpp` (L51)
  ```// 正确```

---

## code-style.md

路径: `.claude/rules/code-style.md`
> paths: - "**/*.py" - "**/*.pyi"

### 标题大纲

- 代码风格（Python） (L7)
  - 命名 (L11)
  - 类型标注 (L22)
- 正确 (L31)
- 错误——缺返回类型，路径类型不明确 (L35)
  - 导入顺序（isort 标准） (L40)
  - 文件路径 (L49)
  - 函数设计 (L55)
  - 类设计 (L62)
  - 注释与文档 (L69)
  - 错误处理 (L90)
- 正确 (L98)
- 错误——吞掉异常 (L108)
  - 性能与内存 (L115)

### 代码块

- `python` (L30)
  ```# 正确```
- `python` (L72)
  ```  def fetch(table: str, keys: list[str]) -> dict[str, Any]:```
- `python` (L97)
  ```# 正确```

---

## project.md

路径: `.claude/rules/project.md`
> Python 3.10+ / Pillow / tkinter / SQLite

### 标题大纲

- 项目架构（image-merger） (L1)
  - 技术栈 (L3)
  - 入口点 (L6)
  - 核心模块 (L10)
  - 架构约束 (L19)
  - 图片处理规范（Pillow 专属） (L23)
  - 批量处理策略（项目专属） (L29)
  - 安全约束（项目专属） (L33)
  - 关键测试场景 (L36)
  - 输出验证 (L43)

---

## security-cpp.md

路径: `.claude/rules/security-cpp.md`
> paths: - "**/*.cpp" - "**/*.cc" - "**/*.h" - "**/*.hpp"

### 标题大纲

- 安全规范（C++） (L9)
  - 内存安全 (L13)
  - 输入验证 (L30)
  - 路径与命令安全 (L42)
  - 并发安全 (L48)
  - 编译期安全加固 (L54)
- Debug / CI 构建额外开启 (L66)
  - Secrets 与数据安全 (L75)
  - 静态分析 (L81)

### 代码块

- `cpp` (L35)
  ```  auto resolved = std::filesystem::canonical(user_path);```
- `cmake` (L58)
  ```target_compile_options(${TARGET} PRIVATE```

---

## security.md

路径: `.claude/rules/security.md`
> paths: - "**/*.py"

### 标题大纲

- 安全规范（Python） (L6)
  - 输入验证 (L10)
  - 路径安全 (L17)
  - 代码执行安全 (L28)
  - Secrets 管理 (L40)
  - 依赖安全 (L46)
  - 资源安全 (L52)
  - 日志安全 (L59)

### 代码块

- `python` (L21)
  ```  resolved = Path(user_input).resolve()```
- `python` (L32)
  ```  # 正确```

---

## testing-cpp.md

路径: `.claude/rules/testing-cpp.md`
> paths: - "tests/**/*.cpp" - "tests/**/*.cc" - "test_*.cpp"

### 标题大纲

- 测试规范（C++） (L8)
  - 运行命令 (L12)
- 构建并运行全量测试（CMake） (L15)
- 只跑某个测试二进制 (L18)
- 只跑某个 test suite (L21)
- 只跑某个测试用例 (L24)
- Windows (MSVC) (L27)
  - 命名规范 (L32)
  - 测试结构（AAA 模式） (L41)
  - Fixtures (L58)
  - 断言选择 (L78)
  - Mock 策略 (L89)
  - 参数化测试 (L109)
  - 覆盖率要求 (L125)
  - 测试原则 (L137)
  - 具体业务场景见各项目 project.md (L144)

### 代码块

- `bash` (L14)
  ```# 构建并运行全量测试（CMake）```
- `cpp` (L43)
  ```TEST_F(MergerTest, TwoImages_ReturnsCorrectWidth) {```
- `cpp` (L64)
  ```class MergerTest : public ::testing::Test {```
- `cpp` (L93)
  ```  class IFileSystem {```
- `cpp` (L113)
  ```class UnsupportedFormatTest : public ::testing::TestWithParam<std::string> {};```
- `cmake` (L130)
  ```  if(ENABLE_COVERAGE)```

---

## testing.md

路径: `.claude/rules/testing.md`
> paths: - "tests/**/*.py" - "test_*.py" - "*_test.py"

### 标题大纲

- 测试规范（Python） (L8)
  - 运行命令 (L12)
- 全量测试 + 覆盖率报告 (L15)
- 只跑某个模块 (L18)
- 只跑某个测试函数 (L21)
- 失败后立即停止 (L24)
  - 文件与函数命名 (L28)
  - 测试结构（AAA 模式） (L37)
  - Fixtures (L55)
  - Mock 策略 (L71)
  - 覆盖率要求 (L80)
  - 测试原则 (L89)
  - 具体业务场景见各项目 project.md (L110)

### 代码块

- `bash` (L14)
  ```# 全量测试 + 覆盖率报告```
- `python` (L41)
  ```def test_merge_two_images_returns_correct_width(tmp_path):```
- `python` (L62)
  ```@pytest.fixture```
- `python` (L76)
  ```  mock_open.assert_called_once_with(expected_path, "rb")```
- `bash` (L85)
  ```  python -m pytest --cov=src --cov-fail-under=80```
- `python` (L94)
  ```  def test_open_nonexistent_file_raises_file_not_found(tmp_path):```
- `python` (L100)
  ```  @pytest.mark.parametrize("fmt", [".txt", ".pdf", ".exe", ".zip"])```

---

## workflows.md

路径: `.claude/rules/workflows.md`
> > 无 paths 限制，所有文件类型均加载。

### 标题大纲

- 工作流规范 (L1)
  - 核心开发循环 (L5)
  - 开始新任务前 (L15)
  - 实现阶段 (L22)
  - Code Review 检查项 (L29)
  - Debug 工作流 (L53)
  - 子任务分发（Claude Code 多 Agent） (L61)
  - 提交规范（Conventional Commits） (L72)
  - 高风险操作清单 (L95)

### 代码块

- `text` (L9)
  ```理解需求 → 阅读相关代码 → 制定方案 → 小步实现 → 运行测试 → Code Review → 提交```
- `text` (L74)
  ```<type>(<scope>): <summary>```
- `text` (L84)
  ```feat(merger): 支持 TIFF 格式输入```

---

## README.md

路径: `.claude/scripts/README.md`
> 本目录包含 Claude Code + Codex MCP 协作中使用的自动化脚本。所有脚本通过 Hook 机制触发。

### 标题大纲

- 脚本文件指南 (L1)
  - 📜 脚本文件列表 (L7)
    - 1. `auto_checkpoint_commit.py` (L9)
    - 2. `append_changelog_draft.py` (L53)
  - [Unreleased] (L102)
    - Added (L104)
    - Fixed (L107)
    - Changed (L110)
    - 3. `pre_merge_scope_guard.py` (L116)
  - 🔧 脚本管理 (L167)
    - 添加新脚本 (L169)
    - 修改现有脚本 (L175)
    - 测试脚本 (L181)
- 预览模式 (L183)
- 验证 JSON 配置 (L186)
- 检查脚本语法 (L189)
  - 📋 Hook 配置最佳实践 (L195)
    - 1. 使用相对路径 (L197)
    - 2. 设置合理的超时 (L204)
    - 3. 使用异步执行（不阻塞主流程） (L211)
    - 4. 多平台支持 (L218)
  - 🚀 常见操作 (L229)
    - 手动执行脚本 (L231)
- 检查点提交 (L233)
- CHANGELOG 更新 (L236)
- 合并前检查 (L239)
    - 调试脚本 (L243)
- 预览模式 (L245)
- 详细输出 (L248)
- 强制执行 (L251)
  ... 共 32 个标题

### 代码块

- `json` (L20)
  ```{```
- `bash` (L46)
  ```python auto_checkpoint_commit.py --dry-run  # 预览将执行的操作```
- `json` (L64)
  ```{```
- `text` (L90)
  ```feat: 新功能描述```
- `markdown` (L101)
  ```## [Unreleased]```
- `json` (L127)
  ```{```
- `bash` (L152)
  ```python pre_merge_scope_guard.py --base main              # 指定基础分支```
- `markdown` (L159)
  ```| 任务 ID | 文件 | 影响范围 | 风险 |```

---

## README.md

路径: `.claude/skills/README.md`
> 本目录包含 Claude Code + Codex 协作流水线中使用的自定义技能。

### 标题大纲

- 技能文件指南 (L1)
  - Claude Code 侧技能（`.claude/skills/`） (L9)
    - 流水线核心 (L11)
    - 工具类 (L22)
  - Codex 侧技能（`.codex/skills/`） (L36)
    - 流水线执行 (L38)
    - 通用工具 (L45)
    - 专业领域 (L54)
  - 流水线调用路径 (L65)
  - 流水线状态协议 (L91)
  - 技能管理 (L101)
    - 添加新技能 (L103)
    - 文件命名约定 (L108)
  - 相关文档 (L114)

### 代码块

- `text` (L70)
  ```/codex:review --background        # 审查```
- `javascript` (L79)
  ```mcp__codex__codex({ model: "gpt-5.4", sandbox: "danger-full-access",```
- `bash` (L85)
  ```codex exec -m gpt-5.4 "..."```

---

## README.md

路径: `.claude/workflows/README.md`
> 本目录包含 Claude Code + Codex MCP 协作的工作流文档。所有工作流遵循 `claude-workflow-constants.md` 中的全局约束。

### 标题大纲

- 工作流文档指南 (L1)
  - 📚 工作流文档列表 (L7)
    - 1. `claude-workflow-constants.md` (L9)
    - 2. `claude-workflow-cpp-build.md` (L27)
    - 3. `claude-workflow-cpp-test.md` (L34)
    - 4. `claude-workflow-complex.md` (L41)
    - 3. `claude-workflow-debug.md` (L61)
    - 4. `claude-workflow-research.md` (L74)
    - 5. `claude-workflow-parallel.md` (L87)
    - 6. `claude-workflow-largebase.md` (L100)
  - 🔄 工作流路由优先级 (L117)
  - 📋 简单模式标准 (L132)
  - 🚀 快速开始 (L145)
    - 对于新任务 (L147)
    - 对于 Bug 修复 (L154)
    - 对于大型库修改 (L159)
  - 📖 引用方式 (L167)
  - 🔗 相关文档 (L179)

### 代码块

- `markdown` (L171)
  ```> 参见 `workflows/claude-workflow-constants.md` 中的"Codex 调用规范（双路径）"```

---

## claude-workflow-complex.md

路径: `.claude/workflows/claude-workflow-complex.md`
> > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 触发条件：任意一条不满足简单模式标准（文件>3 / diff>200行 / 需求有歧义 / 跨模块） > 入口：从 `claude.md` 场景路由跳转至此

### 标题大纲

- claude-workflow-complex｜复杂开发流程 (L1)
  - ⛔ 强制门禁：用户确认需求后，必须按顺序执行，不得跳过，不得在 Phase 6 前调用 Codex 写代码 (L9)
  - Phase 0：扫描路由判断（可选） (L52)
    - 0Pre. 搜索历史记忆（必做） (L54)
    - 0A. 是否进入大型代码库流程 (L62)
    - 0B. 未命中 largebase 时执行轻量扫描 (L75)
    - 0C. Phase 0 跳过条件 (L102)
  - Plan 文档标准结构 (L110)
- [FEATURE_NAME] Plan 方案 (L115)
  - 流程进度 (L120)
  - 需求理解 (L128)
  - 技术方案 (L131)
    - 方案选择 (L132)
    - 选定方案详述 (L135)
    - 涉及文件 (L138)
  - Worktree 并行计划 (L144)
  - 风险点 (L150)
  - 待确认问题 (L155)
  - 验收标准 (L159)
  - 已知权衡（CC vs Codex 分歧） (L163)
  - Phase 2：Codex 工程审查 Plan Prompt (L170)
  - Context (L173)
  - Task (L176)
  - Acceptance (L186)
  - Phase 4：生成 Step-by-Step 开发计划 Prompt (L193)
  - Context (L196)
  - Task (L199)
    - 任务 N：[任务名] (L216)
  - Constraints (L224)
  - Phase 4.5：解耦审查清单 (L233)
  ... 共 45 个标题

### 代码块

- `text` (L11)
  ```Phase 0  （可选）扫描路由判断（largebase / 轻量扫描）```
- `text` (L57)
  ```Grep({ pattern: "[当前任务核心关键词]", path: ".claude/memory/" })```
- `text` (L77)
  ```mcp__codex__codex({```
- `markdown` (L114)
  ```# [FEATURE_NAME] Plan 方案```
- `text` (L172)
  ```## Context```
- `text` (L195)
  ```## Context```
- `markdown` (L235)
  ```## 解耦确认清单```
- `bash` (L266)
  ```git diff --stat   # 单次任务 diff 应 ≤ 200 行```

---

## claude-workflow-constants.md

路径: `.claude/workflows/claude-workflow-constants.md`
> 此文档是所有工作流的"单一真相"来源。所有其他文档应引用此文档，而非复制规则。

### 标题大纲

- workflow-constants.md — 全局硬约束与常量 (L1)
  - Codex 调用规范（双路径，不可变） (L7)
    - 路径 A：codex-plugin-cc（插件，推荐） (L12)
      - AI 可直接调用的命令（无限制） (L18)
      - AI 调用 review 的方案：直调底层脚本 (L26)
- 普通 review (L33)
- 对抗性 review (L36)
      - 用户手动可用的命令（供参考，AI 不调） (L47)
    - 路径 B：MCP（通用） (L56)
    - 必填参数（两路径共用，MANDATORY） (L82)
  - 文件操作边界与删除禁令（不可变） (L100)
    - 风险原则 (L102)
    - CC 调用前（强制注入 Constraints） (L107)
    - CC 验收时（强制检查） (L118)
    - Hook 强制拦截（本机） (L129)
  - Codex 推理强度规则（不可变） (L150)
  - Superpowers 调用规范（Windows，不可变） (L168)
    - 固定命令（绝对路径） (L174)
    - Skill 选择规则（仅 Codex MCP 场景） (L191)
  - Git 安全约束（不可变） (L213)
    - 禁止操作（未获用户明确批准） (L215)
    - 必须操作（强制门禁） (L223)
- 如果有未提交改动，询问用户： (L228)
- A) 提交当前改动 (L229)
- B) 暂存到 stash（需用户确认） (L230)
- C) 放弃改动（需用户确认） (L231)
- 输出变更摘要，等用户确认后再合并 (L237)
    - SCAN_SUMMARY 刷新规则（claude.md） (L251)
  - 角色边界（不可变） (L265)
    - CC（Claude Code）职责 (L267)
  ... 共 76 个标题

### 代码块

- `text` (L20)
  ```/codex:rescue <任务描述>     ← AI 可调，适合执行任务 + 顺带修复```
- `bash` (L32)
  ```# 普通 review```
- `text` (L49)
  ```/codex:review --background```
- `javascript` (L61)
  ```mcp__codex__codex({```
- `javascript` (L73)
  ```mcp__codex__codex-reply({```
- `text` (L111)
  ```Scope: Only modify files under [当前 worktree 绝对路径]```
- `bash` (L120)
  ```git diff --name-only HEAD```
- `bash` (L139)
  ```echo '{"command":"rm -rf C:/test"}' | python C:/Users/Administrator/.claude/hook```

---

## claude-workflow-cpp-build.md

路径: `.claude/workflows/claude-workflow-cpp-build.md`
> 用户说"编译" / "build" / "构建" / "CMake" / "MSBuild"，且涉及 C++ 项目。

### 标题大纲

- claude-workflow-cpp-build.md — C++ 编译工作流 (L1)
  - 触发条件 (L3)
  - 前置检测 (L7)
  - Phase 0：编译方式选择 (L12)
  - Phase 1：编译前检查 (L28)
  - Phase 2：执行编译 (L38)
    - CMake 路径 (L40)
- 1. 配置（首次或 CMakeLists.txt 变更后） (L43)
- 2. 编译 (L46)
- 3. 清理重编（用户要求时） (L49)
    - MSBuild 路径 (L54)
- 1. 编译 (L57)
- 2. 清理重编 (L60)
  - Phase 3：编译结果检查 (L65)
  - Phase 4：编译后可选操作 (L80)
  - 输出格式 (L87)
  - 编译报告 (L90)
    - 警告列表（如有） (L103)
    - 输出产物 (L106)
  - 验证完成门禁 (L111)

### 代码块

- `text` (L30)
  ```□ 确认编译方式（CMake / MSBuild）```
- `bash` (L42)
  ```# 1. 配置（首次或 CMakeLists.txt 变更后）```
- `bash` (L56)
  ```# 1. 编译```
- `text` (L67)
  ```□ 编译是否成功（exit code = 0）```
- `text` (L89)
  ```## 编译报告```

---

## claude-workflow-cpp-test.md

路径: `.claude/workflows/claude-workflow-cpp-test.md`
> 用户说"运行测试" / "跑单测" / "gtest" / "单元测试" / "test"，且涉及 C++ 项目。

### 标题大纲

- claude-workflow-cpp-test.md — C++ 单元测试工作流 (L1)
  - 触发条件 (L3)
  - 前置检测 (L7)
  - Phase 0：任务难度评估 (L13)
  - Phase 1：测试范围确定 (L32)
  - Phase 2：执行测试 (L43)
    - 方式 A：通过 CTest (L45)
- 配置（如需要） (L48)
- 运行全部测试 (L51)
- 运行指定测试 (L54)
    - 方式 B：直接运行 GTest 可执行文件 (L58)
- 运行全部 (L61)
- 运行指定测试 (L64)
- 运行并显示详细输出 (L67)
    - 方式 C：已有二进制，无需编译 (L71)
- 直接运行已有的测试可执行文件 (L74)
  - Phase 3：结果分析 (L78)
  - 测试报告 (L83)
    - 失败测试详情 (L94)
    - 结论 (L99)
  - Phase 4：失败处理 (L103)
  - Phase 5：结果审查 (L116)
  - Phase 6：报告输出 (L127)
- C++ 单元测试报告 (L132)
  - 执行摘要 (L134)
  - 测试结果 (L140)
  - 失败分析（如有） (L143)
  - 审查结论 (L146)
  - 建议 (L149)
  - 验证完成门禁 (L154)

### 代码块

- `text` (L17)
  ```满足全部 → 轻量模式（直接测）：```
- `bash` (L47)
  ```# 配置（如需要）```
- `bash` (L60)
  ```# 运行全部```
- `bash` (L73)
  ```# 直接运行已有的测试可执行文件```
- `text` (L82)
  ```## 测试报告```
- `text` (L119)
  ```□ 所有测试通过？如有失败，是否已知 issue？```
- `markdown` (L131)
  ```# C++ 单元测试报告```

---

## claude-workflow-debug.md

路径: `.claude/workflows/claude-workflow-debug.md`
> > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 触发条件：用户描述 bug / 错误信息 / 测试失败 / 意外行为 > 入口：从 `claude.md` 场景路由跳转至此 > 详细参考：`AI开发-PLan-Program-Debug-Claude和Codex协作/06-AI调试阶段-复杂问题分析模板.md`

### 标题大纲

- claude-workflow-debug｜Debug 流程 (L1)
  - 核心原则 (L10)
  - 流程分层（Lite / Full） (L19)
  - Debug 流程（Lite 5阶段） (L36)
    - Phase 0：症状收集 + Bug 卡片（CC） (L40)
  - Bug 卡片 (L45)
    - Phase 1：快速排查（≤5 分钟） (L70)
    - Phase 2：Codex 扫描代码库定位根因 (L92)
    - Phase 3：CC 制定修复方案 + 交叉验证 + 用户确认 (L139)
    - Phase 4：Codex 执行修复 + Review (L181)
- 写能复现 bug 的测试，运行确认失败 (L186)
- 预期：FAIL (L188)
    - Phase 5：根因文档记录与复盘 (L231)
- Bug 记录：[bug-id] (L238)
  - 现象 (L242)
  - 根本原因 (L245)
  - 分析过程 (L248)
  - 修复方案 (L253)
  - 预防措施 (L258)
  - Bug修复: [一句话描述] (L276)
  - 止损规则 (L291)
  - 补充：完整调试扩展（参考 reference/07） (L300)
    - 1. Phase 3 扩展：CC Plan Mode 架构分析（完整版） (L305)
    - 2. Phase 4 扩展：交叉验证对比表 + 决策规则 (L339)
    - 3. Phase 6 补充：回归验证（Lite 版缺失） (L366)
- 1. 运行受影响模块的测试 (L371)
- 2. 手动验证关键路径 (L374)
- - [手动验证步骤1] (L375)
- - [手动验证步骤2] (L376)
    - 4. Phase 7 扩展：根因文档"经验教训"部分 (L386)
  ... 共 32 个标题

### 代码块

- `markdown` (L44)
  ```## Bug 卡片```
- `bash` (L74)
  ```git log --oneline -10                        # 是否最近提交引入？```
- `text` (L96)
  ```mcp__codex__codex({```
- `text` (L129)
  ```根因：[文件:行号] [一句话描述]```
- `text` (L143)
  ```根因：[文件:行号] [一句话描述]```
- `text` (L164)
  ```[CC Plan Mode]```
- `bash` (L185)
  ```# 写能复现 bug 的测试，运行确认失败```
- `text` (L193)
  ```mcp__codex__codex-reply({```

---

## claude-workflow-init.md

路径: `.claude/workflows/claude-workflow-init.md`
> > 本文档在项目首次使用时执行一次，结果写入 `claude-workflow-constants.md` 的"项目配置"区块。 > 后续开发流程通过读取常量使用这些配置，无需重复询问。

### 标题大纲

- claude-workflow-init.md — 项目初始化配置 (L1)
  - 触发条件 (L8)
  - Step 1：扫描根目录 (L18)
  - Step 2：归档整理（可选） (L41)
- ... (L63)
  - Step 3：分支管理模式选择 (L73)
  - Step 4：Worktree 目录偏好 (L99)
    - 若选模式一（临时分支）： (L103)
    - 若选模式二（Bare Repo）： (L117)
  - Step 5：主分支名确认 (L140)
  - Step 6：Bare Repo 初始化（仅模式二执行） (L163)
- 1. 备份当前 .git 目录 (L168)
- 2. 转换为 bare repo (L171)
- 3. 创建 .git 文件指向 .bare (L174)
- 4. 配置 fetch (L177)
- 编辑 .bare/config，确保有：fetch = +refs/heads/*:refs/remotes/origin/* (L178)
- 5. 创建主分支 worktree (L180)
- 6. 移动原项目代码到主分支 worktree (L183)
- 7. 提交整理 (L186)
- 8. 清理备份（注意：此操作可能会被系统 Hook 拦截，若被拦请手动确认清理） (L191)
  - Step 7：写入常量 (L207)
  - 项目配置（init 生成，可手动修改） (L212)
  - 注意事项 (L232)

### 代码块

- `bash` (L22)
  ```ls -la [PROJECT_ROOT]```
- `text` (L45)
  ```检测到以下文件建议归档到 archives/ 目录：```
- `bash` (L59)
  ```mkdir -p [PROJECT_ROOT]/archives```
- `text` (L77)
  ```选择 Git 分支管理模式：```
- `text` (L105)
  ```新建功能分支 worktree 时，目录放在哪里？```
- `text` (L119)
  ```当前目录结构将变为 Bare Repo 风格：```
- `bash` (L144)
  ```git symbolic-ref --short HEAD```
- `text` (L150)
  ```当前主分支为 master，是否重命名为 main？```

---

## claude-workflow-largebase.md

路径: `.claude/workflows/claude-workflow-largebase.md`
> > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 适用：源码文件多、跨模块改动、多份参考文档并存、需要先产出"可消费的数据文档"再规划实施。 > 目标：让 Codex 先生成结构化扫描包，Claude/CC 再基于扫描包写 Plan，避免盲目搜索。 > 核心：三层结构（JSON 存储 + SQLite 查询 + Markdown 展示），参...

### 标题大纲

- claude-workflow-largebase｜大型代码库与多参考文档流程（结构化数据版） (L1)
  - 1. 触发与跳过 (L12)
  - 2. 标准交付物（扫描包） (L36)
  - 3. 扫描模式选择 (L59)
  - 4. 执行流程（强制顺序） (L70)
    - Step 0：可选增强 — Cartographer / 本地 Extract (L72)
    - Step 1: 强制 API 成本提示（触发条件满足时必须执行） (L88)
    - Step 2: 定义扫描范围与初始化（CC 执行） (L138)
  - Scan Preflight (L157)
    - Step 3: 代码结构扫描（Codex） (L175)
    - Phase C：数据与 API 扫描（Codex，按模式选） (L201)
    - Phase D：参考文档融合（Codex） (L213)
    - Phase E：影响矩阵与执行摘要（Codex + CC） (L221)
  - 5. Codex Prompt 模板（可直接复制） (L237)
    - 5.1 全量扫描模板（M4） (L242)
  - Context (L245)
  - Output Contract (L266)
  - Constraints (L272)
    - 5.2 多参考文档融合模板（独立调用） (L278)
  - Context (L281)
  - Task (L288)
  - Output Rules (L295)
  - 6. 输出质量门禁（CC 必查） (L303)
  - 7. memory-system 参考示例（精简） (L336)
  - 8. 反模式 (L356)
  - 9. 与 Skill 的衔接 (L368)

### 代码块

- `markdown` (L100)
  ```⚠️ 大规模扫描即将开始，Token 消耗预警 ⚠️```
- `markdown` (L156)
  ```## Scan Preflight```
- `text` (L230)
  ```   扫描已完成，所有产物已生成。```
- `text` (L244)
  ```## Context```
- `text` (L280)
  ```## Context```

---

## claude-workflow-parallel.md

路径: `.claude/workflows/claude-workflow-parallel.md`
> > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 触发条件：任务数 ≥ 2 且可解耦，需要多个 worktree 同时开发 > 入口：从 `claude.md` 场景路由跳转至此 > 注意：并行开发通常也是复杂模式，先完成 `claude-workflow-complex.md` Phase 1-4.5 再进入此文档 > **路径常量**：...

### 标题大纲

- claude-workflow-parallel｜多功能并行开发流程 (L1)
  - 核心原则 (L12)
  - 并行开发流程（3阶段） (L23)
    - Phase 1：解耦确认（来自 complex 流程 Phase 4.5） (L27)
  - 解耦确认清单 (L32)
    - Phase 2：创建 Worktree + 分配任务 (L66)
    - 若 BRANCH_MODE = temporary（临时分支模式） (L83)
- 按批次创建（批次1示例） (L88)
    - 若 BRANCH_MODE = bare（Bare Repo 模式） (L95)
- 按批次创建（批次1示例） (L102)
- 直接在根目录下创建分支文件夹 (L103)
- worktree-task-1 的 Codex Session (L127)
    - Phase 3：监控 + 合并 (L163)
- 若 BRANCH_MODE = temporary: (L170)
- 若 BRANCH_MODE = bare: (L174)
- 按依赖顺序合并 (L218)
- 运行测试确认无回归 (L220)
- 运行测试确认无回归 (L224)
- 清理 worktree（根据 BRANCH_MODE 选择路径） (L226)
  - 若 BRANCH_MODE = temporary: (L228)
  - 若 BRANCH_MODE = bare: (L232)
  - Session 管理（防止降智） (L247)
- 每个 worktree 保存各自的 threadId (L250)
- threadId-task-1 = "xxx-1" (L251)
- threadId-task-2 = "xxx-2" (L252)
- 单个 Session 执行超过 3 个任务 → 开新 Session，重新提供 context (L254)
- 发现明显低质量输出 → 立即重启 Session (L255)
  - 止损规则 (L260)
  - 补充：完整发布流程扩展（参考 reference/06） (L268)
    - Phase 0：读取 Plan 文档 (L275)
  ... 共 46 个标题

### 代码块

- `markdown` (L31)
  ```## 解耦确认清单```
- `powershell` (L46)
  ```Copy-Item docs/templates/parallel-impact-scope-template.md docs/development/[fea```
- `text` (L51)
  ```同时输出文件影响范围表，列格式固定为：```
- `bash` (L70)
  ```cd [DEV_DIR]```
- `bash` (L85)
  ```cd [DEV_DIR]```
- `bash` (L99)
  ```cd [PROJECT_ROOT]   # 注意：不是 [DEV_DIR]，而是项目根目录```
- `text` (L126)
  ```# worktree-task-1 的 Codex Session```
- `bash` (L169)
  ```# 若 BRANCH_MODE = temporary:```

---

## claude-workflow-research.md

路径: `.claude/workflows/claude-workflow-research.md`
> > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 触发条件：用户说"调研/对比/选型/搜索/研究/怎么实现/有哪些方案" > 入口：从 `claude.md` 场景路由跳转至此 > 详细参考：`AI开发-PLan-Program-Debug-Claude和Codex协作/03-AI资料调研搜索阶段模板.md`

### 标题大纲

- claude-workflow-research｜研究调研流程 (L1)
  - 核心原则 (L10)
  - 调研深度分层（快速 / 标准 / 深度） (L19)
    - 快速（默认） (L21)
    - 标准 (L25)
    - 深度（强制切换） (L29)
  - 研究流程（4阶段） (L41)
    - Phase 0：问题定义（CC） (L43)
  - 研究卡片 (L48)
    - Phase 1：CC 快速搜索（WebSearch） (L68)
    - Phase 2：Codex 深度读取文档 (L85)
    - Phase 3：CC 整合 + 交叉验证 + 输出结论 (L122)
  - 方案对比 (L129)
  - 推荐方案 (L140)
    - Phase 4：输出调研报告（可选） (L164)
- 调研报告：[topic] (L169)
  - 背景 (L174)
  - 方案对比 (L177)
  - 推荐方案详述 (L180)
  - 参考来源 (L183)
  - 研究完成后的衔接 (L199)
  - 止损规则 (L207)
  - 补充：深度调研扩展（参考 reference/04） (L215)
    - 1. 10 轮迭代搜索跟踪表 (L219)
    - 2. Google Deep Research 模式（生成搜索方向） (L238)
    - 3. 多工具并行搜索 (L259)
    - 4. Opus 多源文档整合（结构化报告） (L275)
    - 5. 结论验证实验 (L298)
- 根据 BRANCH_MODE 选择路径 (L303)
- 或 (L305)
  ... 共 32 个标题

### 代码块

- `markdown` (L47)
  ```## 研究卡片```
- `text` (L72)
  ```WebSearch: "[技术关键词] best practices [当前年份]"```
- `text` (L89)
  ```mcp__codex__codex({```
- `markdown` (L128)
  ```## 方案对比```
- `markdown` (L168)
  ```# 调研报告：[topic]```
- `bash` (L188)
  ```git add docs/research/YYYY-MM-DD-[topic].md```
- `text` (L245)
  ```主题：[RESEARCH_TOPIC]　目标：[RESEARCH_GOAL]```
- `bash` (L302)
  ```# 根据 BRANCH_MODE 选择路径```

---

## claude-workflow-review.md

路径: `.claude/workflows/claude-workflow-review.md`
> > 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束 > 触发条件：用户说"review/审查/检查代码质量/走 review 流程" > 入口：从 `CLAUDE.md` 场景路由跳转至此

### 标题大纲

- claude-workflow-review｜Code Review 流程 (L1)
  - 核心原则（强制，全场景适用） (L9)
  - 场景路由 (L21)
  - Scene 1 — Spec/Plan Review（计划阶段，代码生成前） (L38)
    - 步骤 (L43)
  - Scene 2 — Code Review（代码生成后，P0-P3 分级） (L80)
    - 问题分级定义 (L85)
    - 步骤 (L94)
    - Review 止损阈值 (L144)
  - Scene 3 — PR Review（合并前） (L154)
    - 步骤 (L158)
  - 与 complex.md 的关系 (L182)
  - Self-Improvement 联动 (L194)

### 代码块

- `text` (L23)
  ```当前处于哪个阶段？```
- `text` (L45)
  ```Step 1  定位 plan 文档```
- `text` (L96)
  ```Step 1  确定改动范围（Preflight）```
- `text` (L160)
  ```Step 1  展示变更摘要（必须先展示，再进行任何操作）```

---

## CODEBASE_MAP.md

路径: `docs/CODEBASE_MAP.md`
> last_mapped: 2026-04-02T11:26:03Z total_files: 304 total_tokens: 634340

### 标题大纲

- Codebase Map (L7)
  - System Overview (L12)
  - Directory Structure (L92)
  - Module Guide (L149)
    - .claude/workflows/ — 工作流引擎 (L151)
    - .claude/rules/ — 按需加载规则 (L168)
    - .claude/scripts/ — Hook 脚本 (L188)
    - .claude/skills/ — 技能库 (L203)
    - .claude/fbm/ — FBM 记忆系统 (L219)
    - image-merger/ — 演示应用 (L226)
    - .codex/ — Codex 侧技能 (L243)
    - .coordination/ — 多线程协调 (L248)
  - Data Flow (L253)
    - 主路由流程 (L255)
    - 扫描流水线 (L275)
  - Conventions (L297)
  - Gotchas (L305)
  - Navigation Guide (L314)

### 代码块

- `mermaid` (L16)
  ```graph TB```
- `text` (L94)
  ```.```
- `mermaid` (L257)
  ```sequenceDiagram```
- `mermaid` (L277)
  ```sequenceDiagram```

---

## IMPROVEMENTS-2026-02-26.md

路径: `docs/IMPROVEMENTS-2026-02-26.md`
> 本次改进涉及全局硬约束统一、工作流流程对齐、大型代码库扫描升级三个方向。

### 标题大纲

- 文档改进总结 — 2026-02-26 (L1)
  - 改进范围 (L3)
  - 第一阶段：全局硬约束统一 (L9)
    - 创建 workflow-constants.md (L11)
    - 更新 claude.md (L25)
  - 第二阶段：工作流流程对齐 (L38)
    - Phase 0 分流规则（.claude/workflows/claude-workflow-complex.md） (L40)
    - Debug 流程分层（.claude/workflows/claude-workflow-debug.md） (L49)
    - Research 流程分层（.claude/workflows/claude-workflow-research.md） (L58)
    - Parallel 流程门禁（.claude/workflows/claude-workflow-parallel.md） (L67)
  - 第三阶段：大型代码库扫描升级 (L77)
    - 新增 Skill：largebase-structured-scan (L79)
    - 核心改进 (L99)
    - 扫描模式（4 档） (L112)
    - 标准交付物（7 + 2） (L121)
    - 更新 .claude/workflows/claude-workflow-largebase.md (L136)
    - 与路由表衔接 (L144)
  - 质量检查清单 (L160)
    - ✅ 已完成的检查项 (L162)
    - 待验证的项目 (L176)
  - 使用指南 (L186)
    - 对于系统架构师（决策） (L188)
    - 对于开发者（实施） (L194)
    - 对于大型代码库扫描 (L202)
- 1. 初始化 (L207)
- 2. 调用 Codex（参考对应的 Prompt 模板） (L213)
- 输出 scan-data.json 到 docs/scan/2026-02-26-add-cache-layer/ (L214)
- 3. 加载到数据库 (L216)
- 4. 查询（可选） (L221)
- 5. 基于 06-exec-brief.md 路由到后续工作流 (L227)
  ... 共 37 个标题

### 代码块

- `text` (L82)
  ```.claude/skills/largebase-structured-scan/```
- `text` (L147)
  ```大型代码库 | 源码文件 > 20 / 跨 3+ 模块 / 多参考文档 / 重构迁移 | .claude/workflows/claude-workflow-l```
- `bash` (L206)
  ```# 1. 初始化```

---

## skill.md

路径: `docs/auto-save/skill.md`
> name: "git" description: "在 git 仓库中完成代码修改、开始复杂任务前、需要查看历史或回退时调用" user-invocable: true

### 标题大纲

- Git 版本管理 (L7)
  - 子命令 (L11)
    - /git save - 提交完成的修改 (L13)
    - /git checkpoint - 保存临时状态 (L34)
    - /git history [文件/关键词] - 查看历史 (L41)
    - /git restore <hash> [file] - 还原版本 (L49)
    - /git status - 查看当前状态 (L57)
  - 智能判断（无参数时） (L63)
  - 注意事项 (L74)

---

## changelog-draft.md

路径: `docs/changelog-draft.md`
> - 2026-02-28 11:55 [7c3498f] checkpoint: 11:53 - 2026-02-28 11:56 [7c3498f] checkpoint: 11:53 - 2026-02-28 11:57 [7c3498f] checkpoint: 11:53 - 2026-02-28 11:58 [4f6445d] fix: restore SKILL.md content ...

### 标题大纲

- Changelog Draft (L1)

---

## plan-2025-02-28-cartographer-phase1.md

路径: `docs/plan/plan-2025-02-28-cartographer-phase1.md`
> 将 Cartographer 作为 largebase-structured-scan skill 的前置架构地图提供者，实现"优先消费 CODEBASE_MAP.md，缺失则回退现有扫描流"的并存增强策略。

### 标题大纲

- Phase 1: Cartographer 接入计划 (L1)
  - 需求概述 (L3)
  - 关键定义（本期新增） (L6)
    - CODEBASE_MAP 可用性判定 (L8)
    - 回退规则（强制） (L14)
  - 改动范围 (L21)
    - 文件清单 (L23)
    - 不改动（保持现状） (L28)
  - 具体改动点 (L33)
    - 1. SKILL.md (L35)
    - 2. claude-workflow-largebase.md (L40)
    - 3. output-contract.md (L44)
  - 验收标准 (L48)
  - 可执行验收（命令级） (L54)
  - 复杂度判断 (L60)
  - 执行人 (L65)

---

## plan-2026-02-26-image-merger-requirements.md

路径: `docs/plan/plan-2026-02-26-image-merger-requirements.md`
> > 日期：2026-02-26 > 状态：已确认 ✅

### 标题大纲

- 需求初稿：Python 图像左右拼接项目 (L1)
  - 需求理解 (L8)
  - 歧义点列表 (L14)
  - 复杂度判断 (L27)
  - 待确认问题 (L40)
  - 确认方案 (L48)

### 代码块

- `text` (L29)
  ```涉及文件：≤ 3 个（main.py + merger.py + tests）```

---

## plan-2026-02-26-image-merger-v2-requirements.md

路径: `docs/plan/plan-2026-02-26-image-merger-v2-requirements.md`
> > 日期：2026-02-26 > 状态：已确认 ✅ > 分支：feat/image-merger-v2 > 基于：image-merger v1（CLI 单次拼接）

### 标题大纲

- 需求文档：Image Merger v2 — GUI 批量双文件夹拼接工具 (L1)
  - 需求理解 (L10)
  - 功能模块拆解 (L20)
    - 模块 A：文件夹扫描与图像重命名 (L22)
    - 模块 B：批量拼接引擎 (L27)
    - 模块 C：GUI 界面（tkinter） (L33)
    - 模块 D：单元测试 (L42)
  - 文件结构 (L50)
  - 并行开发任务拆解（适合 Worktree 并行） (L68)
  - 接口约定（Task-1 与 Task-2 的边界） (L82)
- file_manager.py 对外暴露 (L85)
- batch_merger.py 对外暴露 (L95)
  - 约束 (L109)
  - 验收标准 (L118)
  - 歧义点（待确认） (L128)

### 代码块

- `text` (L52)
  ```image-merger/```
- `python` (L84)
  ```# file_manager.py 对外暴露```

---

## plan-2026-02-27-merge-reference-docs.md

路径: `docs/plan/plan-2026-02-27-merge-reference-docs.md`
> **日期**：2026-02-27 **任务**：从 `AI开发-PLan-Program-Debug-Claude和Codex协作/` 目录中选择合适的文件，合入 `.claude` 目录，并进行适当的重命名和组织。

### 标题大纲

- 需求文档：合并参考文档到 .claude 目录 (L1)
  - 需求理解 (L8)
    - 源目录分析 (L10)
      - 1. 概览和快速开始（3个文件） (L13)
      - 2. 工作流阶段模板（6个文件） (L18)
      - 3. 特殊工作流（3个文件） (L26)
      - 4. 补充文档（2个文件） (L31)
  - 与现有 .claude 结构的对比 (L37)
    - 现有 .claude 目录结构 (L39)
    - 潜在重叠和冲突 (L66)
  - 歧义点和待确认问题 (L73)
    - 1. 合并策略 (L75)
    - 2. 文件重命名规则 (L79)
    - 3. 目录组织 (L86)
    - 4. 内容去重 (L93)
    - 5. 优先级 (L99)
  - 复杂度判断 (L108)
    - 评估标准 (L110)
    - 判断结果 (L118)
  - 建议的执行流程 (L129)
    - 阶段 1：需求澄清（当前） (L131)
    - 阶段 2：内容分析 (L137)
    - 阶段 3：实施 (L143)
    - 阶段 4：验证 (L149)
  - 待用户确认的决策 (L157)

### 代码块

- `text` (L40)
  ```.claude/```
- `text` (L111)
  ```涉及文件数：14 个源文件 + 现有 .claude 结构 = 高```

---

## plan-2026-02-27-refactor-claude-structure-requirements.md

路径: `docs/plan/plan-2026-02-27-refactor-claude-structure-requirements.md`
> **日期**：2026-02-27 **任务**：验证和优化 `.claude/` 目录结构，确保文档引用关系正确，添加结构说明文档

### 标题大纲

- 需求初稿：重构 .claude 目录结构与验证引用关系 (L1)
  - 需求理解 (L8)
    - 需求 1：验证引用关系 (L12)
    - 需求 2：可选的结构优化 (L16)
    - 需求 3：添加结构说明文档 (L20)
    - 需求 4：未完成 (L24)
  - 歧义点与待确认问题 (L29)
    - 歧义 1：引用验证的范围 (L31)
    - 歧义 2：是否必须移动 constants 文件 (L42)
    - 歧义 3：README 文档的详细程度 (L52)
    - 歧义 4：未完成的需求 (L63)
  - 复杂度判断 (L70)
  - 建议的后续步骤 (L90)
  - 当前状态 (L110)

---

## plan-2026-02-27-refactor-claude-structure.md

路径: `docs/plan/plan-2026-02-27-refactor-claude-structure.md`
> **日期**：2026-02-27 **状态**：待用户确认 **复杂度**：复杂开发（涉及 5+ 文件，跨模块）

### 标题大纲

- Plan：重构 .claude 目录结构与验证工作流执行 (L1)
  - 需求确认 (L9)
  - 当前状态分析 (L19)
    - 文件结构 (L21)
    - 引用关系（需要更新） (L38)
  - 执行计划 (L47)
    - Task 1：移动 claude-workflow-constants.md (L49)
    - Task 2：更新所有引用 (L66)
    - Task 3：创建 .claude/README.md (L83)
    - Task 4：验证工作流执行 (L101)
    - Task 5：分析其他优化点 (L110)
  - 风险评估 (L120)
  - 验收标准 (L130)
  - 后续步骤 (L141)

### 代码块

- `text` (L22)
  ```.claude/```

---

## plan-2026-02-28-largebase-token-optimization.md

路径: `docs/plan/plan-2026-02-28-largebase-token-optimization.md`
> > 日期：2026-02-28 > 主题：对比当前 largebase-structured-scan 与 GitNexus 方案，探讨 Token 优化策略 > 状态：Phase 0 已就绪，待大型代码库验证

### 标题大纲

- 大型代码库扫描 Token 优化方案讨论 (L1)
  - 0. 审查结论与最简优化策略（2026-02-28 补充） (L9)
    - 0.1 审查发现 (L11)
    - 0.2 最简策略：双会话手动 API 切换（零代码改动） (L22)
    - 0.3 验证计划（先验证，再决定是否优化） (L53)
      - Step 1：测量输入规模（零成本） (L58)
      - Step 2：用当前 API (yunyi) 做一次完整扫描 (L64)
      - Step 3：用便宜 API (aliyun) 做同样扫描 (L69)
      - Step 4：对比判断 (L74)
      - Step 5：根据数据决策 (L82)
  - 1. 核心问题陈述 (L89)
    - 1.1 当前方案的 Token 消耗痛点 (L91)
    - 1.2 GitNexus 的核心洞察 (L110)
  - 2. 方案对比分析 (L134)
    - 2.1 两种哲学的对比 (L136)
      - 方案 A：当前 AI-First 方案 (L138)
- 核心理念：AI 理解代码并生成摘要 (L141)
      - 方案 B：GitNexus 本地解析方案 (L163)
- 核心理念：本地工具提取结构，AI 只做查询和推理 (L166)
    - 2.2 适用场景对比 (L193)
  - 3. 可能的优化路径 (L206)
    - 3.1 渐进式改进（保持现有架构） (L208)
      - 改进 1：引入真正的增量机制（保持现有输出合同） (L212)
- 新增 incremental_scan.py（伪代码） (L215)
      - 改进 2：模式优选与分层触发（合同内） (L248)
- 先做模式路由，再做对应深度扫描 (L251)
      - 改进 3：扫描结果缓存与复用 (L273)
- 新增 scan_cache.py（伪代码） (L276)
    - 3.2 与现有 workflow/skill 的兼容约束（必须） (L297)
    - 3.3 激进重构（引入本地解析） (L305)
  ... 共 46 个标题

### 代码块

- `text` (L26)
  ```Session 1（低成本扫描）```
- `bash` (L59)
  ```python scan.py measure --scope <大型代码库路径> --output docs/scan/measure-baseline.jso```
- `text` (L95)
  ```Cartographer Map 预检（可复用）```
- `python` (L140)
  ```# 核心理念：AI 理解代码并生成摘要```
- `python` (L165)
  ```# 核心理念：本地工具提取结构，AI 只做查询和推理```
- `python` (L214)
  ```# 新增 incremental_scan.py（伪代码）```
- `yaml` (L250)
  ```# 先做模式路由，再做对应深度扫描```
- `python` (L275)
  ```# 新增 scan_cache.py（伪代码）```

---

## plan-2026-03-03-workflow-refactor.md

路径: `docs/plan/plan-2026-03-03-workflow-refactor.md`
> > **生成日期**：2026-03-03 > **依据参考**：23.1 审查报告、23.2 审查报告及全量核查补充 > **涉及文件**：`CLAUDE.md`, `constants.md`, `complex.md`, `debug.md`, `research.md`, `parallel.md`, `init.md`, `README.md`

### 标题大纲

- 工作流文档体系综合修改计划 (L1)
  - 🔴 P0 — 立即修复（功能级 Bug） (L9)
  - 🔴 P1 — 立即修复（规则矛盾与执行死角） (L15)
  - 🟡 P2 — 本周修复（流程结构与一致性梳理） (L23)
  - 🟢 P3 — 有空再做（阅读体验及规范收口） (L39)

---

## plan-2026-03-09-thread-registry-requirements.md

路径: `docs/plan/plan-2026-03-09-thread-registry-requirements.md`
> **日期**：2026-03-09 **任务**：为项目新增多线程协作注册表规范，并提供 3 个 YAML 示例文件

### 标题大纲

- 需求初稿：多线程协作注册表最小落地版 (L1)
  - 需求理解 (L8)
  - 方案边界 (L16)
  - 歧义与处理 (L25)
  - 复杂度判断 (L32)
  - 历史教训 (L45)
  - 当前状态 (L51)

---

## plan-2026-04-02-hook-scripts-optimization.md

路径: `docs/plan/plan-2026-04-02-hook-scripts-optimization.md`
> > 创建时间: 2026-04-02 > 状态: 需求讨论

### 标题大纲

- Hook 脚本基座优化 (L1)
  - 需求理解 (L6)
  - 现状问题 (L10)
  - 优化目标 (L21)
    - 1. 结构化日志（全部脚本） (L23)
    - 2. 配置中心化 (L28)
    - 3. 错误恢复 (L33)
    - 4. git_safety_check 增强 (L38)
  - 涉及文件 (L43)
  - 约束 (L54)
  - 实施顺序 (L61)

---

## walkthrough.md

路径: `docs/plan/walkthrough.md`
> > 审查时间：2026-03-01 · 覆盖文件：CLAUDE.md, AGENTS.md, README.md, complex.md, debug.md, constants.md, largebase.md, parallel.md, research.md

### 标题大纲

- 全面审查报告：CLAUDE.md / AGENTS.md / Workflows (L1)
  - 🔴 高优先级：会导致卡住的问题 (L7)
    - 1. CLAUDE.md — SCAN_SUMMARY 区块已失效 (L9)
    - 2. debug.md / research.md — 外部文档引用不可达 (L24)
    - 3. parallel.md — 模板文件假设不成立 (L40)
  - 🟡 中优先级：逻辑隐患 (L52)
    - 4. CLAUDE.md — AGENTS.md 文件名不一致 (L54)
    - 5. complex.md — Phase 5 Opus 审查是"可选"但无明确跳过条件 (L65)
    - 6. constants.md — SCAN_SUMMARY 标记位置未记录 (L83)
  - 🟢 低优先级：信息过时 (L91)
    - 7. CLAUDE.md — Codebase Overview 描述已过时 (L93)
  - 修复优先级汇总 (L103)

### 代码块

- `text` (L11)
  ```<!-- SCAN_SUMMARY_START -->```
- `text` (L27)
  ```AI开发-PLan-Program-Debug-Claude和Codex协作/06-AI调试阶段-复杂问题分析模板.md```
- `powershell` (L42)
  ```Copy-Item docs/templates/parallel-impact-scope-template.md docs/development/[fea```
- `text` (L57)
  ```完整工作流规范见 `claude.md`（Claude Code 对话时遵循）```
- `text` (L67)
  ```Phase 5  （可选）Opus 审查开发计划```
- `text` (L74)
  ```Phase 5（可选，满足以下任一条可跳过）：```
- `text` (L95)
  ```scan.py（843行）```

---

## skill.md

路径: `docs/project-init/skill.md`
> name: "init" description: "分析项目结构，生成项目和模块的 CLAUDE.md 文档" user-invocable: true

### 标题大纲

- 项目初始化 (L7)
  - 执行步骤 (L11)
    - 1. 检查现有文档 (L13)
    - 2. 分析项目结构 (L18)
- 查看目录结构 (L20)
- 或 Windows (L22)
    - 3. 识别模块 (L32)
    - 4. 分析关键文件 (L38)
    - 5. 生成项目 CLAUDE.md (L45)
  - 项目概览 (L49)
  - 技术栈 (L52)
  - 目录结构 (L57)
  - 模块说明 (L62)
  - 开发注意事项 (L67)
  - 当前任务 (L70)
  - 最近修改 (L73)
    - 6. 生成模块 CLAUDE.md（可选） (L77)
  - 模块职责 (L81)
  - 关键文件 (L84)
  - 依赖关系 (L89)
  - 核心逻辑 (L93)
  - 注意事项 (L96)
  - 最近修改 (L99)
    - 7. 确认结果 (L103)
  - 判断是否需要模块 CLAUDE.md (L108)
  - 注意事项 (L116)

### 代码块

- `bash` (L19)
  ```# 查看目录结构```
- `markdown` (L48)
  ```## 项目概览```
- `text` (L60)
  ``````
- `markdown` (L80)
  ```## 模块职责```

---

## 01-architecture.md

路径: `docs/scan/2026-02-26-memory-system-scan/01-architecture.md`
> memory-system/ ├── scripts/                  # 核心实现（索引、搜索、状态、写入、清理） │   ├── memory.py             # 单文件 CLI 与核心逻辑 │   └── requirements.txt      # 运行依赖 ├── references/               # 参数与 schema 参考 │  ...

### 标题大纲

- 01 Architecture (L1)
  - 目录职责图（2层） (L3)
  - 模块清单 (L15)
  - 入口点清单 (L23)
  - 与“分块/检索重构”直接相关文件 (L34)
  - 信息缺口 (L42)

### 代码块

- `text` (L5)
  ```memory-system/```

---

## 02-dataflow.md

路径: `docs/scan/2026-02-26-memory-system-scan/02-dataflow.md`
> | 结构 | 字段 | 类型 | 用途 | 位置 | |------|------|------|------|------| | `meta` | `key`, `value` | `TEXT`, `TEXT` | 记录模型名与向量维度 | `scripts/memory.py:100` | | `files` | `path`, `hash`, `mtime`, `size` | `TEXT`...

### 标题大纲

- 02 Dataflow (L1)
  - 核心数据结构 / Schema (L3)
  - 主流程数据流 (L14)
  - 存储层清单 (L23)
  - 配置常量映射 (L31)
  - 潜在影响点 (L43)
  - 信息缺口 (L51)

---

## 03-api-surface.md

路径: `docs/scan/2026-02-26-memory-system-scan/03-api-surface.md`
> | 名称 | 签名/形态 | 文件:行号 | 调用方 | |------|-----------|----------|-------| | `init_db` | `(db_path: str) -> sqlite3.Connection` | `scripts/memory.py:95` | `cmd_index`, `cmd_search`, `cmd_status`, `cmd_add` ...

### 标题大纲

- 03 API Surface (L1)
  - 公共函数/命令签名表 (L3)
  - 调用关系图（公共接口） (L19)
  - CLI 参数表面 (L41)
  - 接口变更影响矩阵 (L51)
  - 外部依赖清单 (L59)
  - 信息缺口 (L67)

### 代码块

- `text` (L21)
  ```main```

---

## 04-reference-constraints.md

路径: `docs/scan/2026-02-26-memory-system-scan/04-reference-constraints.md`
> | 文档A | 文档B | 冲突点 | 建议采用 | 理由 | |------|------|-------|---------|------| | `SKILL.md` | `scripts/memory.py` | 安装提示：`pip install -r ...` vs 错误提示 `pip3 install sentence-transformers` | `SKILL.md` 作为主入口，...

### 标题大纲

- 04 Reference Constraints (L1)
  - 文档冲突检测 (L3)
  - 需求相关约束汇总 (L10)
  - 实现必须遵守的规范 (L19)
  - 文档需要同步更新的位置 (L26)
  - 信息缺口 (L33)

---

## 05-impact-matrix.md

路径: `docs/scan/2026-02-26-memory-system-scan/05-impact-matrix.md`
> | 修改点 | 直接影响 | 间接影响 | 回归验证点 | 风险等级 | |-------|---------|---------|-----------|---------| | `chunk_markdown` (`scripts/memory.py:173`) | `chunks` 切块边界变化 | 相同查询返回段落可能变化 | 重建索引后对比 Top-K 结果稳定性 | 高 | | `in...

### 标题大纲

- 05 Impact Matrix (L1)
  - 可安全先改（低耦合） (L14)
  - 信息缺口 (L21)

---

## 06-exec-brief.md

路径: `docs/scan/2026-02-26-memory-system-scan/06-exec-brief.md`
> - 代码结构集中在 `scripts/memory.py`，属于“单文件多职责”形态。 - 参数与 schema 文档化质量较好（`references/config.md`），可作为变更基线。 - 高风险区域聚焦在分块、混合评分、FTS tokenizer 回退路径。

### 标题大纲

- 06 Exec Brief (L1)
  - 扫描结论摘要 (L3)
  - 最高风险改动点（Top 3） (L9)
  - 建议拆分任务数 (L15)
  - 推荐任务拆分 (L23)
  - 建议流程路由 (L31)
  - 下一步执行前置条件 (L36)
  - 信息缺口 (L42)

---

## CLAUDE.preview.md

路径: `docs/scan/2026-02-28-cartographer-phase1-verify/CLAUDE.preview.md`
> <!-- largebase-scan:auto-summary:start -->

### 标题大纲

  - 项目架构速查（auto-generated by largebase-scan） (L2)

---

## 01-architecture.md

路径: `docs/scan/2026-02-28-claude-system-scan/01-architecture.md`
> | L1 | L2 | ?? | ??? | ???? | | --- | --- | --- | ---: | --- | | `README.md` | `-` | ?? | 1 | `.claude`??? | | `plugins` | `-` | ?? | 7 | ??????????? | | `plugins` | `cartographer` | ??? | 7 | ???????...

### 标题大纲

- 01 Architecture (L1)
  - ??????2?? (L3)
  - ???????/????/??? (L58)
  - ??????????/????3?? (L79)
  - ???? (L96)

---

## 02-dataflow.md

路径: `docs/scan/2026-02-28-claude-system-scan/02-dataflow.md`
> | ??? | ?????? | ?? | ?? | | --- | --- | --- | --- | | `scan_meta` | `key`<br>`value` | `TEXT PRIMARY KEY`<br>`TEXT NOT NULL` | 扫描元数据 | | `modules` | `id`<br>`path`<br>`name`<br>`responsibility`<br>`e...

### 标题大纲

- 02 Dataflow (L1)
  - ?????????/??/??? (L3)
  - ????????????? (L18)
  - ???????? (L30)
  - ???? (L41)

---

## 03-api-surface.md

路径: `docs/scan/2026-02-28-claude-system-scan/03-api-surface.md`
> | API | ?? | ?? | | --- | --- | --- | | `parse_gitignore` | `parse_gitignore(root)` | `.claude/plugins/cartographer/plugins/cartographer/skills/cartographer/scripts/scan-codebase.py:118` | | `matches_...

### 标题大纲

- 03 API Surface (L1)
  - ??API???????:??? (L3)
  - ???????????? (L84)
  - ???? (L217)
  - ???? (L228)

### 代码块

- `mermaid` (L86)
  ```graph TD```

---

## 04-reference-constraints.md

路径: `docs/scan/2026-02-28-claude-system-scan/04-reference-constraints.md`
> | ??A | ??B | ???? | ???? | ?? | ???? | | --- | --- | --- | --- | --- | --- | | `.claude/workflows/claude-workflow-constants.md:130` | `superpowers bootstrap ??` | skill ?????? | constants ????????? s...

### 标题大纲

- 04 Reference Constraints (L1)
  - ?????? (L3)
  - ?????? (L11)
  - ???????? (L25)
  - ???????? (L35)
  - ???? (L45)

---

## 05-impact-matrix.md

路径: `docs/scan/2026-02-28-claude-system-scan/05-impact-matrix.md`
> | ??? | ???? | ???? | ??? | ???? | | --- | --- | --- | --- | --- | | ?? scan.py cmd_load ???? | ?? scan-data.json ?????? | scan.db ????????? | ???????? load ? query all | high | | ?? scan.py SQLite ??...

### 标题大纲

- 05 Impact Matrix (L1)
  - ??????? (L3)
  - ??????? (L18)
  - ???? (L26)

---

## 06-exec-brief.md

路径: `docs/scan/2026-02-28-claude-system-scan/06-exec-brief.md`
> | ?? | ??? | ?? | ???? | | ---: | --- | --- | --- | | 1 | ?? scan.py cmd_load ???? | high | ?? scan-data.json ?????? / scan.db ????????? | | 2 | ?? scan.py SQLite ??? | high | load/query SQL ?? / M2/M...

### 标题大纲

- 06 Exec Brief (L1)
  - ?? TopN (L3)
  - ??????? (L14)
  - ?????complex/parallel/debug? (L25)
  - ???? (L34)

---

## 01-architecture.md

路径: `docs/scan/2026-02-28-image-merger-docs-scan/01-architecture.md`
> | L1 | L2 | 类型 | 文件/目录数量 | 职责 | | --- | --- | --- | ---: | --- | | `image-merger` | `src` | 源码目录 | 5 模块 | 图像拼接核心能力、批处理编排、CLI/GUI 入口 | | `image-merger` | `tests` | 测试目录 | 3 模块 | 核心几何逻辑、批处理行为、文件管理行为验证 |...

### 标题大纲

- 01 Architecture (L1)
  - 目录职责表（2层） (L3)
  - 模块清单（职责 / 导出符号 / 依赖） (L13)
  - 入口点清单（CLI + GUI） (L26)

---

## 02-dataflow.md

路径: `docs/scan/2026-02-28-image-merger-docs-scan/02-dataflow.md`
> | 数据结构 | 定义位置 | 结构形态 | 生产者 | 消费者 | 关键约束 | | --- | --- | --- | --- | --- | --- | | `Image` 对象（`PIL.Image.Image`） | `image-merger/src/merger.py` | RGB 图像实例（含 `width`/`height`） | `_load_image`, `merge_im...

### 标题大纲

- 02 Dataflow (L1)
  - 核心数据结构 (L3)
  - 数据流（CLI 流） (L11)
  - 数据流（GUI 流） (L21)
  - 数据流（批处理流） (L34)
  - 存储层（输出格式 / 命名规则） (L47)

---

## 05-impact-matrix.md

路径: `docs/scan/2026-02-28-image-merger-docs-scan/05-impact-matrix.md`
> | 修改点 | 直接影响 | 间接影响 | 验证点 | | --- | --- | --- | --- | | `merger._load_image` 的 `convert("RGB")` 策略变更 | 输出图像色彩模式变化 | CLI 与批处理输出颜色/透明通道行为变化 | `image-merger/tests/test_merger.py::test_merge_single_pixel_...

### 标题大纲

- 05 Impact Matrix (L1)
  - 修改影响矩阵（重点：`merger.py` / `batch_merger.py` / `file_manager.py`） (L3)

---

## 06-exec-brief.md

路径: `docs/scan/2026-02-28-image-merger-docs-scan/06-exec-brief.md`
> | 排名 | 风险项 | 触发条件 | 影响范围 | 建议控制 | | ---: | --- | --- | --- | --- | | 1 | 源文件重命名冲突/中断 | `rename_in_place=True` 且目录内已有目标编号文件 | `batch_merger.py`、`file_manager.py`、GUI 重命名流程 | 先临时名再落盘（已实现），补充冲突回归测试 | | 2...

### 标题大纲

- 06 Exec Brief (L1)
  - 风险 TopN (L3)
  - 建议拆分任务数 (L13)
  - 推荐路由 (L19)

---

## 01-architecture.md

路径: `docs/scan/2026-03-01-full-codebase-scan/01-architecture.md`
> > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE_MAP.md

### 标题大纲

- 01-architecture.md - 架构文档 (L1)
  - 1. 目录职责 (L7)
  - 2. 模块清单 (L17)
    - 2.1 AI 工作流配置 (`.claude/`) (L19)
    - 2.2 技能模块 (`.claude/skills/`) (L30)
    - 2.3 钩子脚本 (`.claude/scripts/`) (L40)
    - 2.4 图片合并应用 (`image-merger/src/`) (L48)
  - 3. 入口点清单 (L58)
  - 4. 依赖关系 (L67)

### 代码块

- `text` (L69)
  ```CLAUDE.md (路由层)```

---

## 02-dataflow.md

路径: `docs/scan/2026-03-01-full-codebase-scan/02-dataflow.md`
> > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE_MAP.md

### 标题大纲

- 02-dataflow.md - 数据流文档 (L1)
  - 1. 核心数据结构 (L7)
    - 1.1 扫描数据结构 (largebase-structured-scan) (L9)
    - 1.2 图片合并数据结构 (image-merger) (L25)
  - 2. 数据流 (L34)
    - 2.1 AI 工作流数据流 (L36)
    - 2.2 图片合并数据流 (L57)
  - 3. 存储层 (L80)
    - 3.1 SQLite 数据库 (scan.db) (L82)
    - 3.2 文件存储 (L91)
  - 4. 数据转换 (L99)
    - 4.1 扫描流程转换 (L101)
    - 4.2 图片处理转换 (L115)
  - 5. 关键约束 (L129)

### 代码块

- `text` (L38)
  ```用户请求```
- `text` (L59)
  ```输入文件夹```
- `text` (L103)
  ```CODEBASE_MAP.md (Markdown)```
- `text` (L117)
  ```图片文件 (二进制)```

---

## 03-api-surface.md

路径: `docs/scan/2026-03-01-full-codebase-scan/03-api-surface.md`
> > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE_MAP.md

### 标题大纲

- 03-api-surface.md - API 接口文档 (L1)
  - 1. 公共 API 签名清单 (L7)
    - 1.1 图片合并 API (image-merger/src/) (L9)
    - 1.2 扫描脚本 API (largebase-structured-scan/scan.py) (L19)
  - 2. 调用关系图 (L28)
    - 2.1 图片合并调用关系 (L30)
    - 2.2 工作流调用关系 (L46)
  - 3. 兼容策略 (L59)
  - 4. 调用者清单 (L68)
  - 5. API 变更风险 (L79)

### 代码块

- `text` (L32)
  ```main.py:main()```
- `text` (L48)
  ```CLAUDE.md```

---

## 04-reference-constraints.md

路径: `docs/scan/2026-03-01-full-codebase-scan/04-reference-constraints.md`
> > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE_MAP.md, CLAUDE.md

### 标题大纲

- 04-reference-constraints.md - 参考约束文档 (L1)
  - 1. 文档冲突矩阵 (L7)
  - 2. 约束汇总 (L16)
    - 2.1 强制约束（不可违反） (L18)
    - 2.2 推荐约束 (L28)
    - 2.3 流程约束 (L36)
  - 3. 实现必须遵守清单 (L44)
  - 4. 文档待同步更新位置 (L55)
  - 5. 关键依赖规则 (L65)

---

## 05-impact-matrix.md

路径: `docs/scan/2026-03-01-full-codebase-scan/05-impact-matrix.md`
> > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE_MAP.md

### 标题大纲

- 05-impact-matrix.md - 影响矩阵 (L1)
  - 1. 影响矩阵 (L7)
  - 2. 模块依赖影响 (L18)
    - 2.1 image-merger 模块 (L20)
    - 2.2 扫描模块 (L35)
  - 3. 变更场景分析 (L50)
    - 3.1 修改 merge_images() 签名 (L52)
    - 3.2 修改扫描流程 (L61)
    - 3.3 修改全局约束 (L70)
  - 4. 回归测试清单 (L78)
  - 5. 风险 Top 3 (L86)

### 代码块

- `text` (L22)
  ```merger.py (核心)```
- `text` (L37)
  ```scan.py (核心)```

---

## 06-exec-brief.md

路径: `docs/scan/2026-03-01-full-codebase-scan/06-exec-brief.md`
> > 生成时间: 2026-03-01 > 扫描模式: M4 (全量深度扫描) > 数据来源: docs/CODEBASE_MAP.md

### 标题大纲

- 06-exec-brief.md - 执行摘要 (L1)
  - 1. 扫描统计 (L7)
  - 2. 风险 Top N (L19)
  - 3. 建议拆分任务数 (L28)
  - 4. 推荐路由 (L37)
  - 5. 关键发现 (L48)
    - 5.1 架构亮点 (L50)
    - 5.2 改进建议 (L56)
  - 6. 信息缺口 (L64)
  - 7. 下一步建议 (L71)

---

## CODEBASE_MAP.md

路径: `docs/scan/2026-03-01-test-mixed/CODEBASE_MAP.md`
> > Generated at: 2026-03-01T23:12 > Scope: .claude/skills/largebase-structured-scan

### 标题大纲

- Codebase Map: test-mixed (L1)
  - 模块概览 (L6)
  - .claude (L12)
    - 公开函数 (L18)
    - 依赖 (L42)

---

## docs-index.md

路径: `docs/scan/2026-03-01-test-mixed/docs-index.md`
> > Generated at: 2026-03-01T23:12 > Scope: .claude/skills/largebase-structured-scan > 文档数: 3

### 标题大纲

- Docs Index: test-mixed (L1)
  - 文档列表 (L7)
  - ANALYSIS.md (L15)
    - 标题大纲 (L20)
    - 代码块 (L46)
  - README.md (L61)
    - 标题大纲 (L66)
    - 代码块 (L85)
  - SKILL.md (L100)
    - 标题大纲 (L105)
    - 代码块 (L125)

### 代码块

- `text` (L49)
  ```- `text` (L32)```
- `text` (L51)
  ```- `text` (L71)```
- `text` (L53)
  ```- `bash` (L98)```
- `text` (L55)
  ```- `text` (L155)```
- `text` (L57)
  ``````
- `text` (L88)
  ```- `mermaid` (L59)```
- `text` (L90)
  ```- `mermaid` (L86)```
- `text` (L92)
  ```- `mermaid` (L115)```

---

## CODEBASE_MAP.md

路径: `docs/scan/2026-03-01-warpage-docs/CODEBASE_MAP.md`
> > Generated at: 2026-03-01T23:12 > Scope: F:\KLD_WORK\产品方案\翘曲度与应力\算法验证\玻璃翘曲度计算软件\椭圆拟合_上下表面圆斑分离\docs\玻璃表面平整度计算

### 标题大纲

- Codebase Map: warpage-docs (L1)
  - 模块概览 (L6)

---

## docs-index.md

路径: `docs/scan/2026-03-01-warpage-docs/docs-index.md`
> > Generated at: 2026-03-01T23:12 > Scope: F:\KLD_WORK\产品方案\翘曲度与应力\算法验证\玻璃翘曲度计算软件\椭圆拟合_上下表面圆斑分离\docs\玻璃表面平整度计算 > 文档数: 3

### 标题大纲

- Docs Index: warpage-docs (L1)
  - 文档列表 (L7)
  - 实际光学系统参数分析--精度与近似判定.md (L15)
    - 标题大纲 (L20)
    - 代码块 (L54)
  - 工程近似方案分析--三层实施策略.md (L63)
    - 标题大纲 (L68)
    - 代码块 (L92)
  - 文档1--椭圆变形法与质心偏移法混合：绝对曲率测量完整方案-V1.3.md (L103)
    - 标题大纲 (L108)
    - 代码块 (L142)

### 代码块

- `text` (L57)
  ```- `text` (L673)```
- `text` (L59)
  ``````
- `text` (L95)
  ```- `text` (L212)```
- `text` (L97)
  ```- `text` (L232)```
- `text` (L99)
  ``````
- `text` (L145)
  ```- `mermaid` (L131)```
- `text` (L147)
  ```- `mermaid` (L267)```
- `text` (L149)
  ```- `mermaid` (L887)```

---

## CODEBASE_MAP.md

路径: `docs/scan/test-merge/part-a/CODEBASE_MAP.md`
> > Generated at: 2026-03-01T23:19 > Scope: .claude/skills/largebase-structured-scan

### 标题大纲

- Codebase Map: part-a (L1)
  - 模块概览 (L6)
  - .claude (L12)
    - 公开函数 (L18)
    - 依赖 (L42)

---

## docs-index.md

路径: `docs/scan/test-merge/part-a/docs-index.md`
> > Generated at: 2026-03-01T23:19 > Scope: .claude/skills/largebase-structured-scan > 文档数: 3

### 标题大纲

- Docs Index: part-a (L1)
  - 文档列表 (L7)
  - ANALYSIS.md (L15)
    - 标题大纲 (L20)
    - 代码块 (L46)
  - README.md (L61)
    - 标题大纲 (L66)
    - 代码块 (L85)
  - SKILL.md (L100)
    - 标题大纲 (L105)
    - 代码块 (L126)

### 代码块

- `text` (L49)
  ```- `text` (L32)```
- `text` (L51)
  ```- `text` (L71)```
- `text` (L53)
  ```- `bash` (L98)```
- `text` (L55)
  ```- `text` (L155)```
- `text` (L57)
  ``````
- `text` (L88)
  ```- `mermaid` (L59)```
- `text` (L90)
  ```- `mermaid` (L86)```
- `text` (L92)
  ```- `mermaid` (L115)```

---

## CODEBASE_MAP.md

路径: `docs/scan/test-merge/part-b/CODEBASE_MAP.md`
> > Generated at: 2026-03-01T23:19 > Scope: .claude/workflows

### 标题大纲

- Codebase Map: part-b (L1)
  - 模块概览 (L6)

---

## docs-index.md

路径: `docs/scan/test-merge/part-b/docs-index.md`
> > Generated at: 2026-03-01T23:19 > Scope: .claude/workflows > 文档数: 8

### 标题大纲

- Docs Index: part-b (L1)
  - 文档列表 (L7)
  - README.md (L20)
    - 标题大纲 (L25)
    - 代码块 (L44)
  - claude-workflow-complex.md (L51)
    - 标题大纲 (L56)
    - 代码块 (L90)
  - claude-workflow-constants.md (L111)
    - 标题大纲 (L116)
    - 代码块 (L150)
  - claude-workflow-debug.md (L171)
    - 标题大纲 (L176)
    - 代码块 (L210)
  - claude-workflow-init.md (L231)
    - 标题大纲 (L236)
    - 代码块 (L262)
  - claude-workflow-largebase.md (L283)
    - 标题大纲 (L288)
    - 代码块 (L317)
  - claude-workflow-parallel.md (L332)
    - 标题大纲 (L337)
    - 代码块 (L371)
  - claude-workflow-research.md (L392)
    - 标题大纲 (L397)
    - 代码块 (L431)

### 代码块

- `text` (L47)
  ``````
- `text` (L93)
  ```- `text` (L64)```
- `text` (L95)
  ```- `markdown` (L101)```
- `text` (L97)
  ```- `text` (L159)```
- `text` (L99)
  ```- `text` (L182)```
- `text` (L101)
  ```- `markdown` (L211)```
- `text` (L103)
  ```- `bash` (L242)```
- `text` (L105)
  ```- `text` (L251)```

---

## parallel-impact-scope-template.md

路径: `docs/templates/parallel-impact-scope-template.md`
> Usage notes: - Each task can only edit files inside its allowed paths. - If shared files exist, assign exactly one owner. Non-owner tasks must not edit shared files. - Merge order: tasks without share...

### 标题大纲

- Parallel Impact Scope Template (L1)
  - Pre-merge checklist (L13)

---

## largebase-structured-scan 重构指导手册.md

路径: `docs/代码库扫描/largebase-structured-scan 重构指导手册.md`
> > 版本：v2.0 > 目标：修复现有设计的四个核心缺陷，不推翻重来 > 执行者：Claude Code（自动执行，无需人工确认中间步骤）

### 标题大纲

- largebase-structured-scan 重构指导手册 (L1)
  - 一、问题清单（必须修复） (L9)
  - 二、架构改进总览 (L22)
    - 改进前 (L24)
    - 改进后 (L36)
  - 三、各模块改造规格 (L50)
    - 模块 A：`_extract_python()` 重写 (L54)
- 函数类型 (L63)
- 类信息 (L70)
- 导入 (L75)
- 入口检测 (L80)
- 新增：模块级变量（常量） (L83)
- 用 ast.walk 替代 ast.iter_child_nodes (L122)
- 给节点附加 parent 引用的方法（ast 没有内置） (L130)
    - 模块 B：`_extract_js_ts()` 重写 (L138)
- 优先：tree-sitter（精确） (L145)
- 箭头函数：export const fn = (...) => (L203)
- TypeScript interface (L208)
- TypeScript type alias (L213)
    - 模块 C：`cmd_load()` 真正的 Schema 校验 (L249)
    - 模块 D：`cmd_query()` 增加高价值查询子命令 (L345)
      - `impact` — 影响分析查询 (L351)
- 输入：--query impact --filter "file_manager" (L353)
- 查询：谁调用了 file_manager 的函数，以及影响矩阵 (L354)
- 再查影响矩阵 (L360)
      - `callers` — 调用链查询 (L367)
- 输入：--query callers --filter "merge_images" (L369)
- 查询：谁调用了这个函数 (L370)
      - `risks` — 高风险点汇总（无需 --filter） (L377)
- 输入：--query risks (L379)
  ... 共 70 个标题

### 代码块

- `text` (L26)
  ```extract（ast.iter_child_nodes 顶层）```
- `text` (L38)
  ```extract（tree-sitter 深度提取 + SHA256 增量）```
- `python` (L62)
  ```# 函数类型```
- `python` (L89)
  ```{```
- `python` (L121)
  ```# 用 ast.walk 替代 ast.iter_child_nodes```
- `python` (L144)
  ```# 优先：tree-sitter（精确）```
- `text` (L157)
  ```函数类型：```
- `scheme` (L179)
  ```; 函数声明```

---

## 扫描报告文档规范 v1.0.md

路径: `docs/代码库扫描/扫描报告文档规范 v1.0.md`
> > 适用范围：largebase-structured-scan 所有输出文档（01 ~ 06） > 执行者：生成报告的 AI（Codex / Claude） > 强制级别：⚠️ 标记的规则不得违反，💡 标记的规则为建议

### 标题大纲

- 扫描报告文档规范 v1.0 (L1)
  - 一、核心原则 (L9)
  - 二、文档结构模板 (L19)
- [文档编号] 文档标题 (L24)
  - 目录 (L28)
  - 概览图 (L31)
  - [主体章节 × N] (L34)
  - 附录 (L37)
  - 三、图表规范 (L43)
    - 3.1 图表选型规则 (L45)
    - 3.2 Mermaid 规范 (L63)
    - 3.3 SVG 规范 (L108)
  - 四、公式规范 (L163)
  - 五、代码块规范 (L198)
  - 六、各报告文档内容规范 (L223)
    - 01-architecture.md — 架构文档 (L225)
  - 概览图          ← 分层架构图（SVG） (L243)
  - 模块依赖        ← Mermaid 依赖图 + 每个模块一句话说明 (L244)
  - 目录结构        ← SVG 文件树 (L245)
  - 入口点          ← 列表：文件路径 → 触发方式 → 初始化顺序 (L246)
  - 关键约束        ← 不超过 5 条，影响整体结构的设计决策 (L247)
    - 02-dataflow.md — 数据流文档 (L252)
  - 数据流全景      ← Mermaid graph LR（端到端） (L271)
  - 核心数据结构    ← classDiagram + 字段说明表格 (L272)
  - 处理管道        ← 每个处理阶段：输入格式 → 变换 → 输出格式 (L273)
  - 存储层          ← 数据持久化位置和格式 (L274)
  - 异常数据路径    ← 错误数据如何被捕获和处理（flowchart） (L275)
    - 03-api-surface.md — API 文档 (L280)
  - API 总览        ← SVG 分类卡片 (L298)
  - 公开接口列表    ← 表格：函数名 | 签名 | 说明 | 所在文件 (L299)
  ... 共 56 个标题

### 代码块

- `text` (L23)
  ```# [文档编号] 文档标题```
- `text` (L67)
  ```- 节点 ID 只用英文字母、数字、下划线，不用中文做 ID```
- `text` (L78)
  ```- classDiagram 中字段类型写在冒号后：+String name```
- `markdown` (L86)
- `text` (L105)
- `text` (L112)
  ```- SVG 源码中不含空白行（每行之间无空行）```
- `xml` (L124)
  ```<svg viewBox="..." xmlns="http://www.w3.org/2000/svg">```
- `xml` (L136)
  ```<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">```

---

## code-style-cpp.md

路径: `docs/编程规范/code-style-cpp.md`
> paths: - "**/*.cpp" - "**/*.cc" - "**/*.h" - "**/*.hpp"

### 标题大纲

- 代码风格（C++） (L9)
  - 标准版本 (L13)
  - 命名 (L18)
  - 文件组织 (L31)
  - 内存管理 (L43)
  - 类设计 (L59)
  - 类型与转换 (L67)
  - 现代 C++ 惯用法 (L74)
  - 错误处理 (L83)
  - 并发 (L90)
  - 格式（clang-format 管辖） (L97)

### 代码块

- `cpp` (L51)
  ```// 正确```

---

## code-style-python.md

路径: `docs/编程规范/code-style-python.md`
> paths: - "**/*.py" - "**/*.pyi"

### 标题大纲

- 代码风格（Python） (L7)
  - 命名 (L11)
  - 类型标注 (L22)
- 正确 (L31)
- 错误——缺返回类型，路径类型不明确 (L35)
  - 导入顺序（isort 标准） (L40)
  - 文件路径 (L49)
  - 函数设计 (L55)
  - 类设计 (L62)
  - 注释与文档 (L69)
  - 错误处理 (L90)
- 正确 (L98)
- 错误——吞掉异常 (L108)
  - 性能与内存 (L115)

### 代码块

- `python` (L30)
  ```# 正确```
- `python` (L72)
  ```  def fetch(table: str, keys: list[str]) -> dict[str, Any]:```
- `python` (L97)
  ```# 正确```

---

## security-cpp.md

路径: `docs/编程规范/security-cpp.md`
> paths: - "**/*.cpp" - "**/*.cc" - "**/*.h" - "**/*.hpp"

### 标题大纲

- 安全规范（C++） (L9)
  - 内存安全 (L13)
  - 输入验证 (L30)
  - 路径与命令安全 (L42)
  - 并发安全 (L48)
  - 编译期安全加固 (L54)
- Debug / CI 构建额外开启 (L66)
  - Secrets 与数据安全 (L75)
  - 静态分析 (L81)

### 代码块

- `cpp` (L35)
  ```  auto resolved = std::filesystem::canonical(user_path);```
- `cmake` (L58)
  ```target_compile_options(${TARGET} PRIVATE```

---

## security-python.md

路径: `docs/编程规范/security-python.md`
> paths: - "**/*.py"

### 标题大纲

- 安全规范（Python） (L6)
  - 输入验证 (L10)
  - 路径安全 (L17)
  - 代码执行安全 (L28)
  - Secrets 管理 (L40)
  - 依赖安全 (L46)
  - 资源安全 (L52)
  - 日志安全 (L59)

### 代码块

- `python` (L21)
  ```  resolved = Path(user_input).resolve()```
- `python` (L32)
  ```  # 正确```

---

## testing-cpp.md

路径: `docs/编程规范/testing-cpp.md`
> paths: - "tests/**/*.cpp" - "tests/**/*.cc" - "test_*.cpp"

### 标题大纲

- 测试规范（C++） (L8)
  - 运行命令 (L12)
- 构建并运行全量测试（CMake） (L15)
- 只跑某个测试二进制 (L18)
- 只跑某个 test suite (L21)
- 只跑某个测试用例 (L24)
- Windows (MSVC) (L27)
  - 命名规范 (L32)
  - 测试结构（AAA 模式） (L41)
  - Fixtures (L58)
  - 断言选择 (L78)
  - Mock 策略 (L89)
  - 参数化测试 (L109)
  - 覆盖率要求 (L125)
  - 测试原则 (L137)
  - 具体业务场景见各项目 project.md (L144)

### 代码块

- `bash` (L14)
  ```# 构建并运行全量测试（CMake）```
- `cpp` (L43)
  ```TEST_F(MergerTest, TwoImages_ReturnsCorrectWidth) {```
- `cpp` (L64)
  ```class MergerTest : public ::testing::Test {```
- `cpp` (L93)
  ```  class IFileSystem {```
- `cpp` (L113)
  ```class UnsupportedFormatTest : public ::testing::TestWithParam<std::string> {};```
- `cmake` (L130)
  ```  if(ENABLE_COVERAGE)```

---

## testing-python.md

路径: `docs/编程规范/testing-python.md`
> paths: - "tests/**/*.py" - "test_*.py" - "*_test.py"

### 标题大纲

- 测试规范（Python） (L8)
  - 运行命令 (L12)
- 全量测试 + 覆盖率报告 (L15)
- 只跑某个模块 (L18)
- 只跑某个测试函数 (L21)
- 失败后立即停止 (L24)
  - 文件与函数命名 (L28)
  - 测试结构（AAA 模式） (L37)
  - Fixtures (L55)
  - Mock 策略 (L71)
  - 覆盖率要求 (L80)
  - 测试原则 (L89)
  - 具体业务场景见各项目 project.md (L110)

### 代码块

- `bash` (L14)
  ```# 全量测试 + 覆盖率报告```
- `python` (L41)
  ```def test_merge_two_images_returns_correct_width(tmp_path):```
- `python` (L62)
  ```@pytest.fixture```
- `python` (L76)
  ```  mock_open.assert_called_once_with(expected_path, "rb")```
- `bash` (L85)
  ```  python -m pytest --cov=src --cov-fail-under=80```
- `python` (L94)
  ```  def test_open_nonexistent_file_raises_file_not_found(tmp_path):```
- `python` (L100)
  ```  @pytest.mark.parametrize("fmt", [".txt", ".pdf", ".exe", ".zip"])```

---

## workflows.md

路径: `docs/编程规范/workflows.md`
> > 无 paths 限制，所有文件类型均加载。

### 标题大纲

- 工作流规范 (L1)
  - 核心开发循环 (L5)
  - 开始新任务前 (L15)
  - 实现阶段 (L22)
  - Code Review 检查项 (L29)
  - Debug 工作流 (L53)
  - 子任务分发（Claude Code 多 Agent） (L61)
  - 提交规范（Conventional Commits） (L72)
  - 高风险操作清单 (L95)

### 代码块

- `text` (L9)
  ```理解需求 → 阅读相关代码 → 制定方案 → 小步实现 → 运行测试 → Code Review → 提交```
- `text` (L74)
  ```<type>(<scope>): <summary>```
- `text` (L84)
  ```feat(merger): 支持 TIFF 格式输入```

---

## 编码规范.md

路径: `docs/编程规范/编码规范.md`
> 好，我来调研一下业界主流的 AI 编码工作流规范实践。好，信息够了。下面是完整的调研结论。

### 标题大纲

  - 调研结论 (L5)
    - 一、你的核心问题：`.claude/instructions/` 这个结构本身就不是业界标准 (L7)
    - 二、分 `python/` 和 `cpp/` 子文件夹：可以但没必要 (L15)
- Python 代码规范 (L25)
- C++ 代码规范 (L36)
    - 三、内容质量问题：你的文件确实偏薄 (L44)
    - 四、建议的目录结构调整 (L56)
    - 五、下一步建议 (L78)
  - 目录结构 (L103)
  - 关键改进点 (L124)

### 代码块

- `yaml` (L19)
  ```---```
- `yaml` (L29)
  ```---```
- `text` (L58)
  ```~/.claude/```
- `text` (L90)
  ```.claude/rules/```
- `text` (L107)
  ```~/.claude/```

---

## AI Agent 记忆系统改造模板-v2.md

路径: `docs/记忆与优化/AI Agent 记忆系统改造模板-v2.md`
> > 适用于：Claude Code / 任何基于 LLM 的 Coding Agent 项目 > 参考来源：智谱 AI 记忆机制文档 + FBM 实战经验 + Vibecoding 复盘

### 标题大纲

- AI Agent 记忆系统改造模板 v2 (L1)
  - 一、三层记忆架构 (L7)
  - 二、目录结构规范 (L49)
- CC 内置记忆不进 git（CC 自动管理路径） (L75)
- 项目记忆全部进 git，无需排除 (L76)
  - 三、CLAUDE.md 主文件模板 (L83)
- [项目名称] — Agent 主记忆 (L86)
  - 项目概述 (L88)
  - 导入规则（按需加载） (L93)
  - 快速命令参考 (L102)
  - 记忆管理触发规则 (L109)
  - 四、指令型记忆文件模板 (L129)
    - `project.md` — 项目架构 (L131)
- 项目架构指令 (L134)
  - 模块职责边界 (L136)
  - 禁止行为 (L142)
    - `code-style.md` — 编码规范 (L148)
- 编码规范指令 (L151)
  - TypeScript (L154)
  - 文件大小 (L159)
  - 命名约定 (L163)
  - 不允许的写法 (L168)
    - `testing.md` — 测试约定 (L174)
- 测试指令 (L177)
  - 命令 (L179)
  - 约定 (L184)
    - `security.md` — 安全红线 (L192)
- 安全指令（最高优先级，不可绕过） (L195)
  - 绝对禁止 (L197)
  - 敏感操作前必须确认 (L203)
  ... 共 64 个标题

### 代码块

- `text` (L11)
  ```Layer 1 · CC 内置记忆（个人层）```
- `text` (L51)
  ```.```
- `text` (L74)
  ```# CC 内置记忆不进 git（CC 自动管理路径）```
- `markdown` (L85)
  ```# [项目名称] — Agent 主记忆```
- `markdown` (L133)
  ```# 项目架构指令```
- `markdown` (L150)
  ```# 编码规范指令```
- `markdown` (L176)
  ```# 测试指令```
- `markdown` (L194)
  ```# 安全指令（最高优先级，不可绕过）```

---

## AI Agent 记忆系统改造模板.md

路径: `docs/记忆与优化/AI Agent 记忆系统改造模板.md`
> > 适用于：Claude Code / 任何基于 LLM 的 Coding Agent 项目 > 参考来源：智谱 AI 记忆机制文档 + FBM 实战经验 + Vibecoding 复盘

### 标题大纲

- AI Agent 记忆系统改造模板 (L1)
  - 一、目录结构规范 (L7)
  - 二、CLAUDE.md 主文件模板 (L42)
- [项目名称] — Agent 主记忆 (L47)
  - 项目概述 (L49)
  - 导入规则（按需加载） (L55)
  - 学习型记忆（AI 积累） (L63)
  - 快速命令参考 (L67)
  - 本次会话规则 (L75)
  - 三、指令型记忆文件模板 (L83)
    - 3.1 `project.md` — 项目架构 (L85)
- 项目架构指令 (L88)
  - 模块职责边界 (L90)
  - 禁止行为 (L96)
  - 关键依赖约束 (L101)
    - 3.2 `code-style.md` — 编码规范 (L107)
- 编码规范指令 (L112)
  - TypeScript (L114)
  - 文件大小 (L120)
  - 命名约定 (L124)
  - 不允许的写法 (L130)
    - 3.3 `testing.md` — 测试约定 (L136)
- 测试指令 (L139)
  - 命令 (L141)
  - 约定 (L146)
  - 断言风格 (L152)
    - 3.4 `security.md` — 安全红线 (L157)
- 安全指令（最高优先级，不可绕过） (L160)
  - 绝对禁止 (L162)
  - 敏感操作前必须确认 (L168)
  ... 共 74 个标题

### 代码块

- `text` (L11)
  ```.```
- `text` (L35)
  ```.claude/learning/local.md```
- `markdown` (L46)
  ```# [项目名称] — Agent 主记忆```
- `markdown` (L87)
  ```# 项目架构指令```
- `markdown` (L111)
  ```# 编码规范指令```
- `markdown` (L138)
  ```# 测试指令```
- `markdown` (L159)
  ```# 安全指令（最高优先级，不可绕过）```
- `markdown` (L181)
  ```# 工作流指令```

---

## Memory Skill — CC 原生记忆管理.txt

路径: `docs/记忆与优化/Memory Skill — CC 原生记忆管理.txt`
> > 无需外部 API / MCP 服务器。CC 直接用 Read/Write/Grep 管理记忆文件。 > 触发后按下方协议操作 `.claude/memory/` 目录。

### 标题大纲

- Memory Skill — CC 原生记忆管理 (L1)
  - 触发条件（自动激活） (L8)
  - 存储结构 (L19)
  - 操作协议 (L36)
    - 写记忆 (L38)
- [标题] (L46)
  - 内容 (L53)
  - 适用场景 (L56)
  - 注意事项 (L59)
    - 读记忆（新会话 context 加载） (L68)
    - 搜记忆 (L79)
- 按关键词搜索 (L84)
- 按类型搜索 (L87)
- 按日期范围 (L90)
    - 清理 / 归档 (L97)
  - 与现有系统联动 (L107)
  - 不做什么（边界） (L117)

### 代码块

- `text` (L21)
  ```.claude/memory/```
- `markdown` (L42)
  ```文件命名：YYYY-MM-DD-[2-4个关键词].md```
- `text` (L64)
  ```- [YYYY-MM-DD] [类型] [标题] → [文件路径] | 关键词: [词1, 词2]```
- `bash` (L83)
  ```# 按关键词搜索```

---

## complex.md — Phase 4 Prompt 替换内容.md

路径: `docs/记忆与优化/complex.md — Phase 4 Prompt 替换内容.md`
> - Plan 文档（已定稿）：[PLAN_DIR]YYYY-MM-DD-[FEATURE_NAME].md

### 标题大纲

  - Phase 4：生成 Step-by-Step 开发计划 Prompt (L1)
  - Context (L4)
  - Task (L7)
    - 任务 N：[任务名] (L34)
  - Constraints (L42)

### 代码块

- `text` (L3)
  ```## Context```

---

## constants.md — Codex Prompt 模板替换内容.md

路径: `docs/记忆与优化/constants.md — Codex Prompt 模板替换内容.md`
> > **Context 注入原则（借鉴 Trellis 按需加载机制）** > > Codex Session 启动时，CC 按以下优先级决定注入哪些规范文件： > 1. 读取当前 `*-steps.md` 的 frontmatter `context:` 字段 → **只加载声明的文件** > 2. 若无 frontmatter → 默认加载 `.claude/instructions/proj...

### 标题大纲

  - Codex Prompt 模板（通用） (L1)
  - Context (L16)
  - Task (L24)
  - Constraints (L28)
  - Acceptance (L39)
  - Output Format (L43)

### 代码块

- `text` (L15)
  ```## Context```

---

## constants.md — 路径 A 替换内容（Codex 调用规范第一节）.md

路径: `docs/记忆与优化/constants.md — 路径 A 替换内容（Codex 调用规范第一节）.md`
> **适用环境**：CLI 终端 / VS Code 扩展 / Desktop App（装后需重启 Claude Code）

### 标题大纲

    - 路径 A：codex-plugin-cc（插件，推荐） (L1)
      - AI 可直接调用的命令（无限制） (L9)
      - AI 调用 review 的方案：直调底层脚本 (L17)
- 普通 review (L25)
- 对抗性 review (L28)
      - 用户手动可用的命令（供参考，AI 不调） (L39)

### 代码块

- `text` (L11)
  ```/codex:rescue <任务描述>     ← AI 可调，适合执行任务 + 顺带修复```
- `bash` (L24)
  ```# 普通 review```
- `text` (L41)
  ```/codex:review --background```

---

## Claude流程优化意见.md

路径: `docs/记忆与优化/记忆与优化/Claude流程优化意见.md`
> 我来分析这套 Claude Code + Codex MCP 协作工作流，找出潜在问题和优化空间。先搜索一下当前 AI 辅助开发工作流的最佳实践。好，信息够了，来做系统分析。

### 标题大纲

  - 工作流分析报告 (L5)
    - 一、核心缺陷（需要修复） (L11)
    - 二、设计冗余（可以精简） (L40)
    - 三、遗漏的新能力（可以利用） (L60)
    - 优先级总结 (L87)

### 代码块

- `text` (L18)
  ```每个 Phase 切换前：```

---

## simpread-Claude Code 源码泄露事件全解析：一场意外背后的技术狂欢与冷思考.md

路径: `docs/记忆与优化/记忆与优化/simpread-Claude Code 源码泄露事件全解析：一场意外背后的技术狂欢与冷思考.md`
> > 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/iTJsusJ3hyTplLuzGLj61w)

### 标题大纲

    - 那个疯狂的凌晨 (L20)
    - 项目有多火？ (L26)
    - 为什么有两个版本？ (L32)
    - Anthropic 的反应 (L43)
    - 不是你想的那种 "源码" (L54)
    - 泄露代码里都有啥？ (L69)
    - 技术亮点分析 (L104)
    - 什么是 "Clean Room" 重写？ (L125)
    - Claw Code 的实际内容 (L140)
    - 技术实现浅析 (L166)
    - Rust 重写计划（这才是重头戏） (L209)
    - 1. 学习 AI Agent 架构设计（适合开发者） (L261)
    - 2. 理解 AI 编程助手的工作原理（适合所有人） (L285)
    - 3. 评估和选择 AI 编程工具（适合正在选型的人） (L318)
    - 4. 动手党专属：自己编译 Rust 版本（进阶） (L353)
- 克隆仓库 (L369)
- 编译（Release模式大概需要几分钟） (L373)
- 运行 (L376)
- 交互式REPL (L385)
- 指定模型 (L388)
- 查看状态 (L391)
- 切换权限模式 (L394)
    - 5. 不要做的事情（重要！） (L408)
    - AI 编程助手正在变成基础设施 (L440)
    - 开源 vs 闭源的博弈 (L457)
    - 技术民主化的双刃剑 (L477)

### 代码块

- `text` (L172)
  ```def _score(tokens: set[str], module: PortingModule) -> int:```
- `text` (L187)
  ```def execute(self, prompt: str) -> str:```
- `text` (L197)
  ```def submit_message(self, prompt: str, ...):```
- `text` (L237)
  ```cd rust/```
- `text` (L368)
  ```# 克隆仓库```
- `text` (L384)
  ```# 交互式REPL```

---

## simpread-看了 ClaudeCode 源码，我发现我的软件跟他非常像.md

路径: `docs/记忆与优化/记忆与优化/simpread-看了 ClaudeCode 源码，我发现我的软件跟他非常像.md`
> > 本文由 [简悦 SimpRead](http://ksria.com/simpread/) 转码， 原文地址 [mp.weixin.qq.com](https://mp.weixin.qq.com/s/4-LPI7jNR8cuNkmJCmNsUA)

### 代码块

- `text` (L87)
  ```FBM（记忆管理系统）：```

---

## vibecoding经验总结--两个开源项目clawcode-FBM.md

路径: `docs/记忆与优化/记忆与优化/vibecoding经验总结--两个开源项目clawcode-FBM.md`
> > 来源：Claude Code 源码泄露（claw-code）+ AuroraFairy 开发者复盘 + FBM / FairyAction 两个开源项目实测

### 标题大纲

- Vibecoding 经验总结 (L1)
  - 一、AI Agent 的本质认知：它不是魔法，是胶水 (L6)
  - 二、记忆系统：上下文管理是最大的工程难题 (L22)
    - 2.1 真实踩坑复盘（来自 AuroraFairy 开发者） (L24)
    - 2.2 可直接集成：FBM（Fairy Bionic Memory） (L35)
  - 三、工具系统：FairyAction —— 让 AI 真正能操控浏览器 (L118)
    - 3.1 这是什么 (L120)
    - 3.2 接口设计亮点（对 vibecoding 很有启发） (L128)
    - 3.3 如何在你的项目中集成 (L142)
- 编译 (L145)
- 配置（.env 或 config.json） (L149)
  - 四、系统架构：模块化是一等公民 (L179)
  - 五、权限与安全：AI 执行操作需要边界 (L197)
  - 六、会话管理：持久化是生产力保障 (L212)
  - 七、常见陷阱清单 (L225)
  - 八、推荐实践：一套 Vibecoding SOP (L239)
  - 九、两个项目的快速参考 (L266)

### 代码块

- `text` (L42)
  ```FBM Core```
- `text` (L52)
  ```memories/```
- `typescript` (L64)
  ```import { FBM, OpenAILLMAdapter, OpenAIEmbeddingAdapter } from '@fairy/bionic-mem```
- `typescript` (L92)
  ```const fbm = new FBM(```
- `typescript` (L101)
  ```import type { LLMAdapter } from '@fairy/bionic-memory'```
- `json` (L132)
  ```// 请求（写入 stdin）```
- `bash` (L144)
  ```# 编译```
- `javascript` (L156)
  ```const { spawn } = require('child_process')```

---

## 防止AI误删文件-三层防护方案.md

路径: `docs/防止AI误删文件-三层防护方案.md`
> > 适用场景：Claude Code + Codex MCP 协作开发，或任何通过 AI Agent 执行 shell 命令的场景。

### 标题大纲

- 防止 AI Agent 误删文件：三层防护方案 (L1)
  - 背景：为什么会发生误删？ (L7)
  - 解决思路：不改权限，加三层防护 (L22)
  - 第一层：Prompt 约束 (L34)
  - Context (L48)
  - Task (L52)
  - Constraints (L55)
  - Acceptance (L62)
  - 第二层：PreToolUse Hook 硬拦截 (L71)
    - 2.1 创建拦截脚本 (L75)
    - 2.2 注册 Hook (L184)
    - 2.3 验证 Hook 生效 (L226)
- 应返回 decision=block (L229)
- 应返回 decision=approve (L232)
  - 第三层：CC 验收门禁 (L245)
  - AGENTS.md 兜底配置 (L261)
  - 文件操作硬限制 (L266)
  - 常见问题 (L277)
  - 快速检查清单 (L297)

### 代码块

- `text` (L24)
  ```第一层：Prompt 约束    → 告诉 Codex "不许删"```
- `text` (L38)
  ```Scope: Only modify files under [当前项目绝对路径]```
- `text` (L47)
  ```## Context```
- `python` (L79)
  ```import json```
- `json` (L188)
  ```{```
- `bash` (L228)
  ```# 应返回 decision=block```
- `json` (L238)
  ```{"decision": "block", "reason": "危险命令已拦截，请人工确认后再执行：rm -rf D:/test"}```
- `bash` (L249)
  ```git diff --name-only HEAD```

---

## code_style.md

路径: `docs/项目规则/code_style.md`
> - 函数/变量：snake_case - 类：PascalCase - 常量：UPPER_SNAKE_CASE

### 标题大纲

- 代码风格（Python 通用） (L1)
  - 命名 (L3)
  - 导入顺序 (L8)
  - 类型标注 (L13)
  - 文件路径 (L18)
  - 错误处理 (L22)
  - 大批量处理 (L27)

---

## code_style_cpp.md

路径: `docs/项目规则/code_style_cpp.md`
> - 默认使用 C++17，有明确需求时可升至 C++20 - 禁止使用已废弃特性（`auto_ptr`、`register`、C-style cast 等）

### 标题大纲

- 代码风格（C++ 通用） (L1)
  - 标准版本 (L3)
  - 命名 (L7)
  - 文件组织 (L14)
  - 导入顺序 (L20)
  - 内存管理 (L26)
  - 类型与转换 (L31)
  - 错误处理 (L36)
  - 现代 C++ 优先 (L41)

---

## project_template.md

路径: `docs/项目规则/project_template.md`
> Python 3.10+ / Pillow / tkinter / SQLite

### 标题大纲

- 项目架构（image-merger） (L1)
  - 技术栈 (L3)
  - 入口点 (L6)
  - 核心模块 (L10)
  - 架构约束 (L19)
  - 图片处理规范（Pillow 专属） (L24)
  - 关键测试场景 (L30)
  - 输出验证 (L37)

---

## security.md

路径: `docs/项目规则/security.md`
> - 所有输入路径必须存在且可读：`Path.is_file()` / `Path.is_dir()` - 文件类型校验在允许列表内（具体列表见各项目 project.md）

### 标题大纲

- 安全规范（通用） (L1)
  - 输入验证 (L3)
  - 路径安全 (L7)
  - 资源安全 (L12)
  - 禁止项 (L16)

---

## security_cpp.md

路径: `docs/项目规则/security_cpp.md`
> - 禁止裸 `new`/`delete`，用智能指针 - 数组访问用 `.at()` 代替 `[]`（需要边界检查时） - 禁止使用 `gets()`、`sprintf()`、`strcpy()` 等不安全 C 函数 - 替代：`fgets()`、`snprintf()`、`strncpy()` 或 `std::string`

### 标题大纲

- 安全规范（C++ 通用） (L1)
  - 内存安全 (L3)
  - 输入验证 (L9)
  - 路径安全 (L14)
  - 并发安全 (L19)
  - 禁止项 (L24)

---

## testing.md

路径: `docs/项目规则/testing.md`
> python -m pytest tests/ -v

### 标题大纲

- 测试规范（Python 通用） (L1)
  - 测试命令 (L3)
  - 测试结构 (L8)
  - 测试原则 (L14)
  - 验证方式 (L20)

### 代码块

- `bash` (L4)
  ```python -m pytest tests/ -v```

---

## testing_cpp.md

路径: `docs/项目规则/testing_cpp.md`
> - 默认使用 Google Test（gtest） - Mock 使用 Google Mock（gmock，gtest 内置）

### 标题大纲

- 测试规范（C++ 通用） (L1)
  - 测试框架 (L3)
  - 测试命令 (L7)
- CMake 项目 (L9)
- 单个测试二进制 (L12)
  - 测试结构 (L16)
  - 测试原则 (L23)
  - 断言选择 (L29)
  - Mock 使用 (L37)
  - 具体业务场景的测试用例见各项目 project.md (L41)

### 代码块

- `bash` (L8)
  ```# CMake 项目```

---

## 项目规则说明.md

路径: `docs/项目规则/项目规则说明.md`
> 业界的主流做法和你现在的结构对比 AGENTS.md 已经成为一个开放标准，被超过 6 万个开源项目使用，定位是"给 AI agent 的 README"——把构建步骤、测试命令、代码约定这些放在一个可预期的位置。 Agents 主流的层级结构是：全局（~/.claude/）放个人偏好，项目根目录放项目规范，子目录可以有局部 override。 Aruniyer 你现在的 .claude/inst...

### 标题大纲

  - 命名 (L31)
  - 导入顺序 (L36)
  - 类型标注 (L41)
  - 文件路径 (L46)
  - 输入验证 (L50)
  - 路径安全 (L54)
  - 资源安全 (L59)
  - 测试命令 (L62)
  - 测试结构 (L67)
  - 测试原则 (L73)
  - 技术栈 (L78)
  - 入口点 (L81)
  - 核心模块 (L85)
  - 标准版本 (L97)
  - 命名 (L101)
  - 内存安全 (L108)
  - 输入验证 (L114)
  - 测试框架 (L118)
  - 测试命令 (L122)
- CMake 项目 (L124)
- 单个测试二进制 (L127)
  - 测试结构 (L131)

### 代码块

- `bash` (L63)
  ```python -m pytest tests/ -v```
- `bash` (L123)
  ```# CMake 项目```

---
