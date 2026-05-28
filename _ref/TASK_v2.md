# 任务：基于飞书调研报告生成 HTML 绘本课件

## ⚠️ 核心要求
不要直接写代码！先读文档、调研项目、分析方案，再动手。

## 第一步：读飞书调研报告（必做）
读 `_ref/feishu_doc_full.txt`，重点理解：
- 四个视觉变体：太空冒险(Space)、森林动物(Forest)、海洋世界(Ocean)、童话城堡(Fairy)
- TEMPLATE_CONFIG 架构：CONFIG区放主题配置，REUSABLE区放通用引擎
- 组件生命周期契约：init→mount→unmount→resize→update
- 组件库：text-block, image-display, audio-player, interactive-canvas, choice-button, branch-story

## 第二步：调研开源项目（必做）
1. 搜索并阅读 PBS-KIDS/HTML5-Storybook 的架构（注意：仅学习，代码有版权限制）
2. 搜索 Ink/inkjs 分支叙事引擎的用法
3. 搜索 Turn.js 翻页引擎的集成方式
4. 搜索 Edge-TTS 生成音频的方法

## 第三步：分析现有课件（必做）
读 `_ref/sample_courseware.html`，理解：
- 现有课件的代码结构
- Turn.js + GSAP + Canvas 的使用方式
- Steve/Alex/Bob 角色的引入方式

## 第四步：选择模板策略
根据故事类型选择不同模板：
- 绘本故事 → 森林动物/海洋世界主题
- 古诗讲解 → 童话城堡主题
- 教案活动 → 太空冒险主题
- 英语故事 → 海洋世界主题

## 第五步：创建通用模板引擎
1. 创建一个 TEMPLATE_CONFIG 系统
2. 每个主题有独立的颜色方案和装饰元素
3. 保持代码复用，只改配置

## 第六步：生成 HTML 课件
1. 先做一个测试文件验证
2. 确认无误后批量生成 50 个
3. 每个文件必须是完整独立的 HTML

## 第七步：更新首页 + Git 推送
1. 更新 docs/index.md
2. git add + commit + push
