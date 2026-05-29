# 需求初稿：批量注入 village-reporter.js 引用

> 创建时间：2026-05-29
> 状态：待确认

---

## 任务概述

在 `Prj/childrens-library/courseware/` 目录下的所有 HTML 文件中批量注入 `village-reporter.js` 脚本引用。

## 具体要求

1. **目标目录**：`Prj/childrens-library/courseware/`（不包括 `shared/` 子目录）
2. **目标文件**：所有 `.html` 文件
3. **注入位置**：`</head>` 标签之前
4. **注入内容**：`<script src="shared/village-reporter.js"></script>`
5. **跳过条件**：文件已包含 "village-reporter" 字符串

## 当前状态

- 目标 HTML 文件数量：110 个
- 已包含 village-reporter 的文件：0 个

## 技术方案

使用 Python 脚本批量处理：
- 遍历目录下所有 `.html` 文件（排除子目录）
- 检查文件是否已包含 "village-reporter"
- 若未包含，在 `</head>` 前插入 script 标签
- 保持 UTF-8 编码

## 复杂度评估

- 文件数量：110 个（>3，不满足简单标准）
- 单文件 diff：1 行（极小）
- 逻辑复杂度：极低（单一重复操作）
- 模块范围：单模块内
- 风险等级：低（仅添加 script 引用，不修改逻辑）

## 待确认事项

1. 是否需要备份原文件？
2. 处理完成后是否需要验证插入结果？
3. 是否需要生成处理报告？

---

**用户确认后开始执行**
