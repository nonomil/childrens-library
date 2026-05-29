---
name: ui-screenshot-audit
description: 本地 Web 应用的截图审查，集成 Playwright MCP 自动化采集，生成带证据的 Markdown 报告
layer: ondemand
tags: [ui, screenshot, audit, playwright]
domain: ui
---

# UI 截图审查

面向 Web/React/Next.js 本地项目的截图审查技能，把"页面能跑"升级成"页面有证据地被审过"。

## 采集方式（按优先级选择）

| 方式 | 前置条件 | 适用场景 |
|------|---------|---------|
| **Playwright MCP** | `claude mcp add playwright npx @playwright/mcp@latest` | 有 MCP 客户端，需自动化 |
| **Playwright CLI** | `npm install -D @playwright/test` | 有 Node 环境，无 MCP |
| **手动截图** | 无 | 以上都不可用时的兜底 |

> 优先使用 Playwright MCP。它通过 accessibility tree 快照（2-5KB）而非截图（500KB-2MB）理解页面，速度快 10-100x。

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

## Playwright MCP 采集流程

### 0. 安装与检查

```bash
# 首次安装（一条命令）
claude mcp add playwright npx @playwright/mcp@latest

# 安全配置（生产环境推荐）
# --isolated: 隔离浏览器上下文
# --allowed-origins: 限制访问域名
# --headless: 无头模式（CI 必须）
# --save-trace: 保存 Playwright trace 用于调试
# --output-dir: 指定截图/trace 输出目录
```

### 1. 确认运行实例

- 优先避免干扰用户正在使用的开发实例
- 如果默认端口被占用，选择独立端口
- 报告里必须写清楚审查实例地址和启动方式

### 2. 先修数据，再截图

- 确认 fixture 没有乱码或脏数据
- Windows 下中文可疑时先做 UTF-8 回读
- 优先用 API 种子测试数据（比 UI 操作快 50x）：
  ```
  await request.post('/api/test/seed', { data: { scenario: 'audit' } });
  ```

### 3. Accessibility Tree 分析（Playwright MCP 核心）

在截图前，先用 `browser_snapshot` 获取页面结构：

```
# MCP 工具调用示例
browser_navigate → browser_snapshot → 分析页面结构
```

Accessibility tree 输出示例：
```
- button "Submit": clickable, visible, ref="abc123"
- textbox "Email": editable, value="", ref="def456"
- link "Forgot password?": clickable, visible, ref="ghi789"
```

**分析检查项**：
- 交互元素是否都有可读标签（name）
- 角色是否正确（button/link/textbox）
- 是否有元素 visible=false 但应该是可见的
- Tab 顺序是否合理

### 4. 采集截图（多视口）

使用 `browser_take_screenshot` 按视口逐一采集：

**必覆盖视口**：
| 视口 | 尺寸 | 说明 |
|------|------|------|
| Desktop | 1920×1080 | 主桌面 |
| Tablet | 768×1024 | iPad 竖屏 |
| Mobile | 375×812 | iPhone 尺寸 |

**必覆盖页面状态**：
- 首页或入口页
- 一个弹层/设置态
- 一个移动端视口
- 一个流程初始态
- 一个流程完成态
- 一个错误/空数据态

截图同时写 `capture_manifest.json`，记录：文件名、URL、视口尺寸、状态说明、元素 ref。

### 5. 交互流程验证

用 Playwright MCP 工具模拟关键流程：

```
browser_navigate → browser_snapshot → browser_click → browser_fill_form → browser_snapshot → browser_take_screenshot
```

**断言要点**（用 web-first assertions）：
- 元素可见性：`toBeVisible()`
- 文本内容：`toHaveText()`
- URL 跳转：`toHaveURL()`
- 表单状态：`toBeEnabled()` / `toBeDisabled()`

> 不要用 `waitForTimeout()`，用 web-first assertions 自动重试。

### 6. Trace 证据收集

```bash
# 启动时加 --save-trace，审查完成后保存 trace 文件
npx @playwright/mcp@latest --save-trace --output-dir docs/analysis/img/<report>.assets/
```

Trace 文件包含：每一步的 DOM 快照、网络请求、控制台输出。后续可用 `npx playwright show-trace trace.zip` 回放。

## 手动兜底流程

当 Playwright 不可用时，回退到手动采集：

1. 确认运行实例 → 修数据 → 手动截图（至少覆盖 5 个页面状态）
2. 截图命名规范：`{viewport}-{page}-{state}.png`
3. 手动写 `capture_manifest.json`

## 采集验证证据

至少跑一组与页面相关的测试。报告中写命令、通过数、是否有警告。

## 输出审查报告

### 报告结构

```
# UI 审查报告：{项目名}

## 环境
- 审查实例地址：
- 采集方式：Playwright MCP / CLI / 手动
- 视口覆盖：Desktop / Tablet / Mobile
- 浏览器：Chrome / Firefox / WebKit

## Accessibility Tree 分析
- 发现的可访问性问题
- 交互元素标签缺失
- Tab 顺序异常

## 截图分析
### {页面名} — Desktop
[截图] | [分析]
### {页面名} — Mobile
[截图] | [分析]

## 测试结果
- 命令：
- 通过/失败/警告：

## P1/P2 优化建议
| 优先级 | 问题 | 建议 | 影响范围 |
|--------|------|------|---------|

## 下一步迭代
```

### 报告重点

不只看"好不好看"，还要看：
- 入口可发现性
- CTA 是否可理解
- 反馈是否及时
- 流程收口是否完整
- Accessibility tree 中的角色/标签是否正确
- 多视口下布局是否合理（不只是缩小版）

## Playwright 最佳实践速查

| 场景 | 推荐 |
|------|------|
| 定位元素 | `getByRole()` > `getByTestId()` > CSS selector |
| 断言 | `toBeVisible()` / `toHaveText()`（自动重试） |
| 测试数据 | API seeding > UI 操作（50x 速度差） |
| 调试 | `--save-trace` + `npx playwright show-trace` |
| CI | `--headless --no-sandbox --isolated` |
| 第三方依赖 | `page.route()` mock，不直接测试 |
| Trace 查看 | `npx playwright show-trace trace.zip` |
| 失败重试 | `trace: 'on-first-retry'` 只在失败时抓 trace |
