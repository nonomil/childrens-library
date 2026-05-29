---
name: screenshot-report
description: AI 截图 + 裁切 + 报告生成技能。截全屏→AI查看→定位目标区域→裁切→审查验证→生成带截图的 Markdown 报告。
version: 1.0.0
triggers:
  - "截图报告"
  - "截图测试"
  - "screenshot report"
  - "生成带截图的测试报告"
  - "截图并生成报告"
---

# Screenshot Report Skill

## 概述

让 AI 自主完成"截图 → 定位 → 裁切 → 审查 → 报告"全流程。适用于测试报告、UI 审查、流程文档等需要截图证据的场景。

## 前置依赖

| 依赖 | 用途 | 检查命令 |
|------|------|---------|
| Python 3.10+ | 截图脚本运行 | `python --version` |
| Pillow (PIL) | ImageGrab 截图 + Image 裁切 | `python -c "from PIL import ImageGrab; print('OK')"` |
| mss（可选） | 备选截图库，多显示器支持 | `pip show mss` |
| VSCode CLI | 打开目标文件到编辑器 | `code --goto file:line` |

## 核心流程（5 步循环）

```
Step 1: 准备 — 用 code --goto 打开目标文件到 VSCode 编辑器
Step 2: 截全屏 — PIL ImageGrab.grab() 捕获整个屏幕
Step 3: 查看 — 用 Read 工具查看截图（AI 视觉能力），定位目标区域坐标
Step 4: 裁切 — Image.crop((left, top, right, bottom)) 提取目标区域
Step 5: 审查 — Read 查看裁切后的图，验证是否匹配目标；不匹配则回到 Step 1
```

## 关键参数

### VSCode 编辑器区域（典型值）

| 参数 | 值 | 说明 |
|------|-----|------|
| 侧边栏宽度 | ~320px | 文件浏览器占位 |
| 编辑器左边界 | ~320px | 裁切时 left 至少 320 |
| 编辑器右边界 | 1920px | 全屏宽度 |
| 工具栏高度 | ~30px | 顶部标题栏 |

### 裁切模板

```python
# 编辑器内容区域（不含侧边栏）
region = (320, top_y, 1920, bottom_y)

# 终端输出区域（底部）
region = (0, terminal_top, 1920, 1080)
```

### 坐标定位技巧

1. **先截全屏**：`ImageGrab.grab()` → 1920x1080
2. **Read 查看**：AI 视觉定位目标内容的大致位置
3. **估算坐标**：基于 VSCode 布局（侧边栏 ~320px，顶部 ~30px）
4. **裁切验证**：crop → Read → 确认内容正确
5. **微调**：如果裁切不精确，调整 ±50px 重试

## 截图辅助脚本

```python
# screenshot_helper.py — 放在报告目录下
from PIL import ImageGrab, Image
import os

class ScreenshotHelper:
    def __init__(self, output_dir="./images"):
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

    def capture(self, name, region=None):
        """截全屏或指定区域"""
        filepath = os.path.join(self.output_dir, f"{name}.png")
        img = ImageGrab.grab(bbox=region)
        img.save(filepath)
        return filepath

    def crop(self, source_name, region, output_name=None):
        """从已有截图裁切目标区域"""
        if output_name is None:
            output_name = f"{source_name}-cropped"
        src = os.path.join(self.output_dir, f"{source_name}.png")
        dst = os.path.join(self.output_dir, f"{output_name}.png")
        Image.open(src).crop(region).save(dst)
        return dst

    def view(self, name):
        """返回绝对路径，供 Read 工具查看"""
        return os.path.abspath(os.path.join(self.output_dir, f"{name}.png"))
```

## 报告模板

```markdown
# [报告标题]

> 测试日期：YYYY-MM-DD
> 测试方法：全屏截图 → AI 查看定位 → 区域裁切 → 审查验证

## 测试概览
| 测试项 | 描述 | 结果 |
|--------|------|------|
| T1 | ... | ✅/❌ |

## T1: [测试名称]

**目的**：...

**截图 — [描述]**：

![T1: 描述](images/T1-cropped.png)

图中可见...

## 截图审查记录
| 截图 | 目标 | 是否匹配 | 审查结论 |
|------|------|---------|---------|

## 截图索引（含在线预览链接）
| 序号 | 文件 | 在线预览 |
|------|------|---------|
```

## 使用示例

```
用户：截图测试对抗式工作流集成

AI 执行流程：
1. 对每个测试项（T1-T6）：
   a. code --goto target_file:line → 打开目标内容到编辑器
   b. sleep 2 → 等待编辑器加载
   c. ImageGrab.grab() → 截全屏
   d. Read 查看截图 → 定位目标区域坐标
   e. Image.crop(region) → 裁切
   f. Read 查看裁切图 → 验证内容匹配
   g. 不匹配 → 调整坐标或重新打开文件
2. 汇总所有截图，生成 Markdown 报告
3. 报告中用相对路径引用 images/ 下的截图
4. 同时提供 CDN 在线预览链接
```

## 注意事项

1. **用户操作干扰**：截图期间用户不应操作电脑（鼠标移动、窗口切换会导致截图内容变化）
2. **窗口焦点**：`code --goto` 可能被其他窗口遮挡，需要确认 VSCode 在前台
3. **多显示器**：`ImageGrab.grab()` 默认截主显示器，如需截其他显示器用 mss 库
4. **编码问题**：Windows 终端输出中文可能乱码，截图是更可靠的验证方式
5. **图片大小**：裁切后的图片应 >100x100，过小说明裁切区域有误

## 版本历史

- 2026-04-10：v1.0 初版，基于对抗式工作流测试实践总结
