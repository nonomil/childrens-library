# Skills 路由表

> 本文件定义 Skills 的分层加载策略。目标：默认加载 ≤6 个常驻 Skills，按需激活领域和专项 Skills。

## 常驻层（Always-On，≤6 个）

所有项目自动加载，不依赖项目类型：

| Skill | 用途 | 触发信号 |
|-------|------|---------|
| commit | 提交/检查点/历史/回退 | "提交"/"commit"/"保存"/"回退"/"历史" |
| memory | 跨会话记忆检索 | "之前"/"上次"/"历史经验"/"记得" |
| plan-checklist | 讨论结论→可执行计划 | "沉淀结论"/"写计划"/"checklist" |
| review | 代码审核 | "review"/"审查"/"审核" |
| changelog | 变更日志生成 | "changelog"/"变更日志" |
| smoke-test | Codex 连通性验证 | "测试连通"/"smoke test"/"Codex 可用？" |

> **模式切换**：用户说"子代理执行"/"subagent 执行"/"委托子代理" → 自动将 preferences.json 的 subagent_execution 切换为 "on"，并确认切换。用户说"内联执行" → 切回 "off"。

## 领域层（Domain，按 project_lang 激活）

### Python 项目
| Skill | 触发信号 |
|-------|---------|
| test | "运行测试"/"跑测试"/"pytest" |

### C++ 项目
| Skill | 触发信号 |
|-------|---------|
| cpp-build | "编译"/"build"/"CMake" |
| cpp-unit-test | "gtest"/"单元测试" |

### UI 项目
| Skill | 触发信号 |
|-------|---------|
| ui-ux-design-guide | "UI 设计"/"配色"/"字体" |
| industrial-ui-design | "工业 UI"/"Qt 界面" |
| ui-screenshot-audit | "截图审查"/"UI 审计" |

## 按需层（On-Demand，关键词触发）

| Skill | 触发信号 |
|-------|---------|
| doc-gen | "生成文档"/"写报告"/"解释报告"/"整理资料包"/"share bundle"/"打包给其他 AI" |
| doc-sync | "同步文档"/"文档更新" |
| doc-ref | "参考 XX 文档"/"查 API"/"SDK 文档" |
| dl-experiment-report | "实验报告"/"训练报告"/"DL 报告"/"--report" |
| orchestrate | "全流程"/"编排"/"流水线" |
| pipeline-init | "初始化流水线"/"pipeline" |
| largebase-structured-scan | "扫描代码库"/"影响分析" |
| graphify | "创建知识图谱"/"生成知识图谱"/"graphify"/"代码图谱"/"知识图谱" |
| codex-toolkit | "导出 Codex"/"部署到 Codex" |
| algorithm-spec-review | "算法审查"/"规格审查" |
| plan | "生成计划"/"拆任务"/"pipeline 计划" |
| execute | "执行任务"/"Codex 执行"/"pipeline 执行" |
| career.skill | "职业规划"/"职业 Skill"/"帮我拆 Skill" |
| windows-shell-fallback | "shell 失败"/"命令报错"/"Python 不可用" |
| reviewer-cpp-expert | "C++ 专家审查"/"内存安全审查"/"RAII 审查"/"MISRA 审查" |
| reviewer-senior-engineer | "架构审查"/"SOLID 审查"/"设计模式审查"/"Tech Lead 审查" |
| reviewer-vision-expert | "机器视觉审查"/"图像处理审查"/"OpenCV 审查"/"数值精度审查" |
| reviewer-security-expert | "安全审查"/"OWASP 审查"/"注入审查"/"认证审查" |
| reviewer-performance-engineer | "性能审查"/"延迟审查"/"SIMD 审查"/"并发审查" |
| reviewer-embedded-expert | "嵌入式审查"/"实时审查"/"看门狗审查"/"WCET 审查" |
| reviewer-qa-engineer | "QA 审查"/"覆盖率审查"/"边界测试审查"/"fuzz 审查" |
| adversarial | "对抗式开发"/"adversarial"/"battle 模式"/"红蓝对抗"/"AI 对战" |
| direction-reviewer | "方向审查"/"检查方向"/"drift check"/"方向漂移" |
| debate | "debate"/"需求讨论"/"辩证讨论"/"对抗式需求" — `debate_strategy=on_demand` 时复杂任务自动触发 |
| conductor | Plan 定稿后执行阶段自动触发 — `claude-workflow-complex.md` Phase 6 跳转 |

## Superpowers 门控（复杂度路由）

Superpowers 技能（`使用超能力`、`编写技能`、`子代理驱动开发`、`并行代理分发` 等）**不默认激活**，按任务复杂度按需触发：

### 复杂度判断（机械套用）

| 等级 | 条件（满足全部） | Superpowers 策略 |
|------|----------------|-----------------|
| **简单** | 文件 ≤2、改动 ≤50 行、需求明确、单模块 | **不激活** — 直接用项目 Skills 完成 |
| **中等** | 文件 3-5、或跨模块、或需要设计决策 | **选择性激活** — 只激活相关的 1-2 个 |
| **复杂** | 文件 >5、或多步骤编排、或架构级变更 | **按需激活** — 根据具体需求选择 |

### 激活映射

| Superpowers Skill | 触发条件（不是每次都激活） |
|-------------------|------------------------|
| `使用超能力` | 复杂度 ≥中等 且 需要查找不熟悉的技能 |
| `编写技能` | 用户说"创建/编辑 Skill" |
| `子代理驱动开发` | 有实施计划需要分步执行 |
| `并行代理分发` | ≥2 个独立任务可并行 |
| `编写计划` / `all-plan` | 用户说"规划"/需求不明确需讨论 |
| `执行计划` | 有书面计划需执行 |
| `请求代码审查` | 用户说"请求 review"/提交 PR 前 |
| `接收代码审查` | 收到 review 反馈需处理 |
| `测试驱动开发` | 用户说"TDD"/先写测试 |
| `系统化调试` | bug 需要系统排查 |
| `文档驱动验证` | 有规范文档需要验证 |
| `头脑风暴` | 创造性任务/设计新功能 |
| `完成前验证` | 准备声称完成前 |
| `完成开发分支` | 实施完成需决定集成方式 |
| `使用Git工作树` | 需要隔离的功能开发 |

### 简单任务示例（不激活 Superpowers）

- 改 typo / 加注释 / 改配置
- 回答关于代码的问题
- 单文件小修改（<50 行）
- 查看文件/搜索代码

---

## 路由决策规则

1. **匹配优先级**：常驻层 > 领域层 > 按需层 > Superpowers（最低，需复杂度达标）
2. **复杂度优先判断**：收到请求后先判断复杂度等级，再决定是否激活 Superpowers
3. **领域自动判断**：读取 `.claude/preferences.json` 的 `project_lang` 字段
4. **未命中时**：搜索 skills/ 目录下所有 SKILL.md 的 description 字段
5. **多个匹配**：列出匹配的 Skills 及其区别，让用户选择
