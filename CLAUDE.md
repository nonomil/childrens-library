# Claude Code 工程协作规范

> 本文件是路由索引，仅包含门禁规则和路由表。详细规范按需从子文档加载。

---

## ⛔ 强制门禁：任何行动前必须先讨论需求

> 核心规则已提取到 `.claude/rules/gate.md`（自动加载，不可跳过）。以下仅保留路由和偏好配置。

**收到新任务时按顺序执行，不得跳过：**

1. **读取偏好** → Read `.claude/preferences.json`
   - `profile=minimal` → 跳过下方所有步骤，直接响应用户请求
   - `profile=standard`（默认）→ 继续
2. **读取需求** → 自动初始化 `docs/plan/` 目录，先写轻量草稿（3-5 行要点），确认后在 `docs/plan/PLAN.md` 总表追加任务行 + 创建任务目录 `docs/plan/tasks/Txxx-主题/`
3. **与用户讨论**：复述需求、列歧义、判断复杂度
3.5. **信心检查**：≥95% 继续；60-95% 再问 1 个问题；<60% 给引导模板
4. **复杂度判断**：文件 ≤3、diff ≤200行、需求明确、单模块内 → 简单模式；否则复杂模式
5. **读取历史教训**：Grep 搜索 `.claude/memory/lessons/`
6. **停止** — 用户说"确认"/"开始"之前，不得写代码
7. **确认后**：写入 `.claude/state/.gate-approved`，进入对应模式

---

## 修改前必读（修订记录机制）

1. 读取 `docs/修订记录/目录索引.md`
2. 先检查"禁止重试方案速查"区块
3. 如有相关修订记录 AI 摘要，先读该摘要
4. 或执行 `git log --oneline -20` 确认近期修改

---

## 场景路由表

| 场景 | 触发条件 | 读取文档 |
|------|---------|---------|
| Debug | 描述 bug/错误/测试失败 | `claude-workflow-debug.md` |
| Code Review | 说"review/审查/检查代码质量" | `claude-workflow-review.md` |
| 研究调研 | 说"调研/对比/选型/搜索/研究" | `claude-workflow-research.md` |
| 大型代码库 | 代码文件 >20 / 跨 3+模块 | `claude-workflow-largebase.md` |
| 复杂开发 | 不满足简单标准 | `claude-workflow-complex.md` |
| 简单开发 | 满足全部简单标准 | 无需读文档 |
| **韧性执行** | **任何涉及代码改动的任务（自动加载）** | **`.claude/rules/resilient-workflow.md`** |

> 所有子文档位于 `.claude/workflows/`

---

## 简单模式流程

1. **需求讨论**（门禁）→ 复述需求、列歧义、确认改动文件
2. **实现** → CC 直接编写代码（或子代理执行，按 `subagent_execution` 偏好）
3. **Review + 验证** → CC 自查（≤100行）或调用 Codex 审查（>100行）
4. **提交与收尾** → 检查 git 状态 → 汇报 → 提交（按 `git_strategy` 偏好）
5. **Changelog 双轨** → `docs/changes/` 人看 + `.claude/memory/context/` AI 看

---

## 核心原则

- **CC 是主力**（规划、搜索、决策、编写代码），Codex 是辅助工具（审查、对抗审查、任务救援）
- 单次任务 diff ≤200行（硬约束），合并冲突必须停下报告
- **方向漂移防控**：工件驱动 > 对话信号驱动
- **任务完成必须检查 git status**
- 用户纠正 → 立即写入 `.claude/memory/lessons/`

---

## Codex 集成（可选辅助工具）

> Codex 是 OpenAI 的代码 agent，作为 CC 的辅助工具使用。两种接入方式按需选择。

### 方式 1：Codex MCP（工具调用）

```bash
claude mcp add codex -s user -- codex mcp-server
claude mcp list  # 验证安装
```

使用：在 CC 对话中直接调用 `mcp__codex__codex`，将任务委托给 Codex 执行。

### 方式 2：Codex 插件（命令式）

```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```

| 命令 | 用途 | 场景 |
|------|------|------|
| `/codex:review` | 标准代码审查（只读） | 改完代码后提交前的"第二双眼睛" |
| `/codex:adversarial-review` | 对抗性审查（主动挑刺） | 高风险操作（认证/数据迁移/支付） |
| `/codex:rescue` | 任务救援（接手卡住的任务） | CC 卡住推不动时，把接力棒交给 Codex |

### Trellis（可选项目管理）

> Trellis 是 PLAN.md + tasks/ 的替代方案，更轻量。如果项目已有 docs/plan/ 结构，不需要安装 Trellis。

```bash
npm install -g @mindfoldhq/trellis@latest
trellis init --claude-code --codex -u yourname
```

### autoresearch（可选研究循环）

> 适用于可量化目标的自动优化。需要在项目根目录有 `program.md`（已提供模板）。

启动方式：
```bash
claude "按照 program.md 的指令运行 autoresearch 循环，
       每轮修改实验文件，运行评估，
       如果指标提升则 git commit，否则 git revert，
       持续运行直到收敛或我叫停"
```

---

## 项目特定信息

### Codebase Overview

**项目**: 印刷标签缺陷检测（PLDD 框架复现与研究）
**论文**: "Printed label defect detection using twice gradient matching based on improved cosine similarity measure" (ESWA 2022)
**Stack**: Python 3.10+, OpenCV, NumPy, Pillow
**入口点**: `CLAUDE.md`（路由）→ `.claude/workflows/`（执行流程）

**核心模块**:
- `src/`：PLDD 算法实现（LDCE + 二次梯度匹配）
- `tests/`：pytest 测试
- `scripts/`：实验脚本
- `Ref/`：参考论文

**关键约束**: diff ≤200行 | 两轮独立 Review

### 工作模式

默认 `research`（研究模式）：调研搜索、概念学习、方案对比、知识整理。
通过 preferences.json 切换。

---

## 子文档索引

| 需要什么 | 读取文档 |
|---------|---------|
| Codex 调用参数 / 文件边界 | `claude-workflow-constants.md` |
| 用户偏好 / 项目常量 | `claude-workflow-config.md` |
| 验证完成门禁 / lessons | `claude-workflow-governance.md` |
| Skills / Hooks | `claude-workflow-ecosystem.md` |

---

## Development Environment
- OS: Windows 10.0.19044
- Shell: Git Bash
- Path format: Windows (use forward slashes in Git Bash)
- File system: Case-insensitive
- Line endings: CRLF (configure Git autocrlf)
