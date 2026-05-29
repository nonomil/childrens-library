# 工作流文档指南

本目录包含 Claude Code + Codex MCP 协作的工作流文档。所有工作流默认只读取 `claude-workflow-constants.md` 的最小核心约束；配置、治理和工具生态改为按需加载。

---

## 📚 工作流文档列表

### 1. `claude-workflow-constants.md`
**用途**：所有 workflow 默认常驻的最小核心约束

**包含**：
- Codex 调用核心约束（插件 + MCP）
- 文件操作边界与删除禁令
- Git 安全约束
- 角色边界（CC vs Codex）
- 工作流路由优先级
- 确认词与门禁

### 2. `claude-workflow-config.md`
**用途**：项目常量、共享/本地配置边界、用户偏好

### 3. `claude-workflow-governance.md`
**用途**：验证完成门禁、lessons、context 健康、Prompt 模板与沉淀规则

### 4. `claude-workflow-ecosystem.md`
**用途**：Cartographer、Skills、Hooks、安全工具等可选增强

---

### 5. `claude-workflow-cpp-build.md`
**触发条件**：用户说"编译/build/构建/CMake/MSBuild"
**工作流**：C++ 项目编译（CMake / MSBuild 二选一）
**详见**：`.claude/workflows/claude-workflow-cpp-build.md`

---

### 6. `claude-workflow-cpp-test.md`
**触发条件**：用户说"运行测试/跑单测/gtest/单元测试"
**工作流**：C++ 单元测试（GTest + CTest）
**详见**：`.claude/workflows/claude-workflow-cpp-test.md`

---

### 7. `claude-workflow-adversarial.md`
**触发条件**：用户说"对抗式开发/adversarial/battle 模式/红蓝对抗/AI 对战"，或 `adversarial_strategy=always`

**流程**：
- 计划阶段红蓝对抗
- 执行阶段独立复核
- 问题分级与收敛

**关键特点**：把 Codex 产出放进更强对抗式审查，不走顺从型 review

---

### 8. `claude-workflow-complex.md`
**触发条件**：任意一条不满足简单模式标准
- 涉及文件 > 3 个
- 预估 diff > 200 行
- 需求有歧义
- 跨多个模块

**流程阶段**：
- Phase 0：扫描路由判断
- Phase 1：CC 生成 Plan 文档
- Phase 2：CC 调用 Codex 工程审查 Plan
- Phase 3：交叉 Review
- Phase 4：CC 调用 Codex 生成开发计划
- Phase 5：（可选）Opus 审查
- Phase 6：执行代码

**关键特点**：多阶段审查，确保高质量交付

---

### 9. `claude-workflow-debate.md`
**触发条件**：复杂任务且 `debate_strategy=on_demand/always`，或用户显式要求“debate/需求讨论/辩证讨论”

**流程**：
- 目标与边界澄清
- 分歧点对撞
- must / should 承诺冻结
- 将共识移交复杂流程生成正式 Plan

**关键特点**：先把需求争议讲透，再进入 Plan 与实施阶段

---

### 10. `claude-workflow-conductor.md`
**触发条件**：`claude-workflow-complex.md` Phase 6，用户明确说“开始开发”

**流程**：
- 读取控制面与当前任务
- `taskctl preflight/proceed`
- 单任务增量执行
- review / queue / merge 收口

**关键特点**：以 task 为单位推进，控制上下文膨胀和多任务漂移

---

### 11. `claude-workflow-debug.md`
**触发条件**：用户描述 bug / 错误 / 测试失败

**流程**：
- 问题复现与诊断
- 根因分析
- 修复方案设计
- 实施与验证

**关键特点**：快速定位问题，系统化调试

---

### 12. `claude-workflow-multi-review.md`
**触发条件**：用户说"多专家评审/多视角审查/并行审查/3 路 review"

**流程**：
- 先做评审视角头脑风暴
- 将 reviewer 任务登记到控制面
- 多路 reviewer 并行产出独立 `review.md`
- Coordinator 汇总、仲裁并决定后续走向

**关键特点**：比“直接开多个子代理”更可控，适合高风险评审

---

### 13. `claude-workflow-research.md`
**触发条件**：用户说"调研/对比/选型/搜索/研究"

**流程**：
- 需求理解
- 信息收集
- 对比分析
- 建议输出

**关键特点**：深度研究，提供多个方案对比

---

### 14. `claude-workflow-parallel.md`
**触发条件**：任务数 ≥ 2 且可解耦

**流程**：
- 任务解耦
- 影响范围分析
- 并行执行
- 合并验证

**关键特点**：多任务并行，提高效率

---

### 15. `claude-workflow-largebase.md`
**触发条件**：
- 递归代码文件 > 20
- 目录层级深且跨 3+ 模块
- Markdown 与参考文档较多
- 命中"重构迁移、影响分析"关键词

**流程**：
- 结构化扫描（产出 00-06 扫描包）
- 架构分析
- 数据流分析
- 影响矩阵生成

**关键特点**：大型库专用，系统化分析

---

### 16. `claude-workflow-cv-codebase.md`
**触发条件**：
- C++ + Python 混合代码库
- 命中 `pybind11 / Cython / pipeline / TensorRT / ONNX / 跨语言` 等关键词
- 涉及推理后端替换、跨层重构、机器视觉主链路改动

**流程**：
- Cartographer 建立跨语言架构基线
- code-review-graph 承担日常增量查询
- Graphify 按需做深度社区分析
- 结构化扫描产出 CV 专项扫描包

**关键特点**：专门解决 C++/Python 混合项目中的跨语言边界分析问题

---

## 🔄 工作流路由优先级

**从高到低**：
1. **Debug** — 用户描述 bug / 错误 / 测试失败
2. **对抗式协作** — 用户说"对抗式开发/adversarial/battle 模式/红蓝对抗/AI 对战"
3. **多专家评审** — 用户说"多专家评审/多视角审查/并行审查/3 路 review"
4. **Debate 需求讨论** — 用户显式说"debate/需求讨论/辩证讨论"，或复杂任务命中 `debate_strategy`
5. **Code Review** — 用户说"review/审查/检查代码质量"
6. **C++ Build** — 用户说"编译/build/CMake"且涉及 C++
7. **C++ Test** — 用户说"运行测试/gtest"且涉及 C++
8. **CV 混合代码库** — C++ + Python 混合 / pybind11 / pipeline / 推理后端替换
9. **研究调研** — 用户说"调研/对比/选型/搜索/研究"
10. **大型代码库** — 递归代码文件 > 20 / 跨 3+ 模块 / 用户显式要求先扫描
11. **并行开发** — 任务数 ≥ 2 且可解耦
12. **复杂开发** — 任意简单标准不满足
13. **简单开发** — 满足全部 5 条简单标准

**规则**：优先级高的流程优先匹配，一旦匹配不再检查低优先级

**自我改进闭环**：所有工作流共享 `.claude/memory/lessons/`，详见 `claude-workflow-governance.md` 中的「Self-Improvement 全局规则」

---

## 📋 简单模式标准

满足以下全部 5 条 → 简单模式（直接执行）：
- ✓ 涉及文件 ≤ 3 个
- ✓ 预估 diff ≤ 200 行
- ✓ 需求明确，无歧义
- ✓ 单模块内，不跨模块
- ✓ 不触及高风险文件（schema/公共API/auth/CI/CD/核心配置）

任意 1 条不满足 → 按路由表选择工作流

---

## 🚀 快速开始

### 对于新任务
1. 用户提出需求
2. CC 复述需求、列出歧义
3. 等待用户确认
4. 判断复杂度，选择对应工作流
5. 按工作流执行

### 对于 Bug 修复
1. 用户描述 bug
2. 直接跳转 `claude-workflow-debug.md`
3. 系统化调试

### 对于大型库修改
1. 用户提出需求
2. 检查是否命中大型库条件
3. 如是，跳转 `claude-workflow-largebase.md`
4. 执行结构化扫描

---

## 📖 引用方式

所有工作流文档应这样引用 constants 文件：

```markdown
> 参见 `workflows/claude-workflow-constants.md` 中的「Codex 调用核心约束」
```

而不是复制规则。

---

## 🔗 相关文档

- `../claude.md` — Claude Code 工作流规范（包含场景路由表）
- `../README.md` — .claude 目录完整指南
- `../MIGRATION-GUIDE.md` — 迁移指南
- `claude-workflow-constants.md` — 全局核心约束（默认常驻）
- `claude-workflow-config.md` — 项目常量与偏好
- `claude-workflow-governance.md` — 验证、lessons、Prompt 治理
- `claude-workflow-ecosystem.md` — 工具生态与可选增强
- `claude-workflow-multi-review.md` — 多专家并行评审（review 高级版）
