---
name: ui-screenshot-audit
description: 本地 Web 应用的截图审查，生成带证据的 Markdown 报告
layer: ondemand
tags: [ui, screenshot, audit]
---

# UI 截图审查

面向 Web/React/Next.js 本地项目的截图审查技能，把"页面能跑"升级成"页面有证据地被审过"。

## 何时使用

- 需要重新截图并输出前端界面审查报告
- 需要验证 localhost 页面在桌面端和移动端的表现
- 需要沿关键流程抓取多个状态（首页、弹层、表单完成态等）
- 需要把截图、按钮状态、页面文案、测试结果一起固化到本地文档

## 必交付物

- `docs/analysis/<date>-<topic>.md`
- `docs/analysis/img/<report>.assets/*.png`
- `docs/analysis/img/<report>.assets/capture_manifest.json`
- 至少一条自动化验证记录

## 推荐流程

### 1. 确认运行实例

- 优先避免干扰用户正在使用的开发实例
- 如果默认端口被占用，选择独立端口
- 报告里必须写清楚审查实例地址和启动方式

### 2. 先修数据，再截图

- 确认 fixture 没有乱码或脏数据
- Windows 下中文可疑时先做 UTF-8 回读

### 3. 采集截图

最少覆盖：
- 首页或入口页
- 一个弹层/设置态
- 一个移动端视口
- 一个流程初始态
- 一个流程完成态

截图同时写 `capture_manifest.json`，记录文件名、URL、视口尺寸、状态说明。

### 4. 采集验证证据

至少跑一组与页面相关的测试。报告中写命令、通过数、是否有警告。

### 5. 输出审查报告

- 范围、环境、测试结果
- 截图按页面/流程分析
- P1/P2 优化建议和下一步迭代

## 报告重点

不只看"好不好看"，还要看：
- 入口可发现性
- CTA 是否可理解
- 反馈是否及时
- 流程收口是否完整
