---
name: doc-ref
description: 本地 SDK/API 文档库检索。当任务涉及外部库 API、框架用法、SDK 接口时触发。先查本地索引 docs/api/，未命中则联网抓取官方文档并缓存。触发信号：用户说"参考 [库名] 文档"、任务涉及不熟悉的第三方 API、需要查阅特定版本的 SDK 用法。
layer: ondemand
tags: [doc, reference, api]
domain: docs
---

# doc-ref：本地文档库检索

## 概述

替代 Context7 的本地文档检索方案。按需抓取官方文档，缓存到本地，离线可用。支持私有 SDK 和内部 API 文档。

---

## 触发条件

- 任务涉及外部 API/SDK/框架，需要查阅具体版本用法
- 用户说"参考 [库名] 文档" / "索引 [SDK] 文档" / "更新 [库名] 索引"
- CC 在上下文检查门禁中发现"已有模式"信息缺失

---

## 工作流程

### Step 1：查本地索引

```
读取 docs/api/index.md
搜索匹配库名 + 版本的条目
```

### Step 2：命中 → 注入上下文

```
读取 docs/api/[sdk-name]/ 下的相关文档片段
将片段注入 Codex Prompt 的 Context 区
```

### Step 3：未命中 → 抓取 + 缓存

```
1. 触发 research workflow 联网搜索官方文档
2. 抓取项目用到的 API 部分（不全量下载）
3. 保存到 docs/api/[sdk-name-version]/
4. 更新 docs/api/index.md 索引
5. 将文档片段注入当前上下文
```

### Step 4：调用 Codex

```
在 Codex Prompt 的 Context 区自动附带相关文档片段：
  [sdk-name v版本]：[本任务需要的 API]
  本地路径：docs/api/[sdk-name-version]/[topic].md
```

---

## 更新策略

**手动触发**：用户说"更新 [库名] 文档索引到最新版本"时执行

更新流程：
1. 读取 `docs/api/index.md` 中该库的当前版本
2. 联网搜索最新版本文档
3. 对比差异，只更新变化部分
4. 更新 `index.md` 中的版本号和索引时间

---

## 本地文档库结构

```
docs/api/
├── README.md                 # 目录说明
├── index.md                  # 索引：库名 | 版本 | 索引时间 | 本地路径
├── [sdk-name-version]/       # 各 SDK 文档
│   ├── README.md             # 该 SDK 文档说明
│   └── [topic].md            # 按主题拆分的文档片段
```

---

## 索引格式（index.md）

```markdown
# API 文档库索引

| 库名 | 版本 | 索引时间 | 本地路径 | 备注 |
|------|------|---------|---------|------|
| FastAPI | 0.110 | 2026-04-03 | fastapi-0.110/ | 路由 + 依赖注入 |
| Pillow | 10.2 | 2026-04-03 | pillow-10.2/ | Image + ImageOps |
```

---

## 与 Context7 的区别

| | Context7 | doc-ref |
|--|---------|---------|
| 联网 | 每次实时拉取 | 首次抓取，后续缓存 |
| 离线 | 不可用 | 可用 |
| 私有 SDK | 不支持 | 支持 |
| 更新 | 自动 | 手动触发 |
| 存储 | 无本地缓存 | 本地 docs/api/ |
