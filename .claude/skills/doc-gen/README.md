# doc-gen 技能使用指南

> 统一文档生成入口。用户说"写文档/解释报告/整理资料包"即可触发，内部自动路由到六种文档模式。explain 含 share-bundle 子分支。

## 快速开始

**触发方式**：对话中出现以下任一信号，自动激活 doc-gen skill：

| 触发词 | 示例 |
|--------|------|
| 写文档 | "帮我写一份架构说明文档" |
| 生成文档 | "生成测试报告" |
| 整理成文档 | "把这些调研整理成文档" |
| 写成报告 | "把测试结果写成报告" |
| 写总结 | "给这次改动写总结" |
| 产出 ADR | "为这个技术选型产出一份 ADR" |
| 写 README | "给这个模块写个 README" |
| 解释报告 | "把这个测试报告解释一下" |
| 整理资料包 | "把这条主线整理成给其他 AI 的资料包" |
| share bundle | "生成一份 share bundle 资料包" |
| 打包给其他 AI | "把主线打包给其他 AI 继续分析" |

**不触发**（纯问答，不走模板）：

| 说法 | 为什么不触发 |
|------|------------|
| "解释一下这段代码" | 没有文档产物意图 |
| "这个函数什么意思" | 纯问答 |
| "加个注释" | 单行操作，其他 skill 职责 |

## 内部路由：六种模式

触发后，skill 根据上下文自动判断模式，不需要用户指定：

```
用户说"写文档"
  |
  +-- 有 largebase 扫描包？ ------> scan
  +-- 数据驱动（测试/审查结果）？ -> report
  +-- 方案对比/设计决策？ -------> design
  +-- 明确说 ADR？ --------------> adr
  +-- 变更总结？ ----------------> change
  +-- 资料包/打包给其他 AI？ ----> explain:share-bundle
  +-- 解释 + 文档意图？ ---------> explain（默认）
```

### 模式速查

| 模式 | 一句话定位 | 典型输入 |
|------|-----------|---------|
| **scan** | 代码库结构化扫描（largebase 专用） | 扫描包 01-06 |
| **report** | 数据驱动的测试/审查/分析报告 | 测试结果、运行数据 |
| **design** | 设计文档，方案对比有结论 | 新功能设计、技术选型 |
| **adr** | 架构决策记录 | "为什么选这个方案" |
| **change** | 变更总结，before/after 对比 | diff 总结、版本回顾 |
| **explain** | 解释型文档，假设读者无前置知识 | 架构说明、流程文档 |
| **explain:share-bundle** | 多 AI 交接资料包 | 主线资料打包给其他 AI |

## 用户可以显式指定模式

如果自动路由判断不准，可以在请求中加上模式名：

- "用 design 模式写一份方案文档"
- "生成一份 explain:share-bundle 资料包 README"
- "用 explain 模式整理说明文档"

## 协作 Skill 自动路由

| 协作 Skill | 自动使用的模式 |
|-----------|---------------|
| `largebase-structured-scan` | scan |
| `report` | report |
| `review` | report |
| `plan` / `plan-checklist` | design |
| `changelog` | change |

## 文件结构

```
doc-gen/
  SKILL.md                  # 主控：门禁 + 路由 + 核心原则 + 模式模板
  README.md                 # 本文件：使用指南
  references/
    mode-templates.md       # 旧版模板参考（已被 SKILL.md 自包含模式模板取代，保留作历史对照）
  largebase-structured-scan/    # scan 模式专用规范
    references/doc-format-spec.md
```

## 维护入口

| 想改什么 | 改哪个文件 |
|---------|-----------|
| 触发词（外部入口） | `.claude/rules/skills-router.md` |
| 模式路由逻辑 | `SKILL.md` > 模式识别与触发 节 |
| 某个模式的模板/规则 | `SKILL.md` > 对应 Mode: xxx 节 |
| share-bundle 子分支 | `SKILL.md` > share-bundle 子分支 节 |
| scan 模式专用规范 | `largebase-structured-scan/references/doc-format-spec.md` |

## 真实样例（share-bundle）

- `Docs/深度学习方案/AI-share-EfficientAD-2026-04-27/README.md`
- `Docs/深度学习方案/AI-share-AutoLabeling-SAM-YOLO-2026-04-27/README.md`

这两份 README 是当前 `explain:share-bundle` 的真实参考样例，优先复用其目录分层与 handoff 写法。
