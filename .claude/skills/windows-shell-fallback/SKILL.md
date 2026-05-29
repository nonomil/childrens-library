---
name: windows-shell-fallback
description: Windows 环境下 shell 命令失败的排查与回退指南。覆盖 Python 不可用、rg 失败、GBK 编码错误、文件被占用等常见问题。
layer: ondemand
tags: [windows, shell, fallback, troubleshooting]
domain: platform
---

# Windows Shell 失败回退指南

## 核心原则

- 先保任务连续，不先保某个命令
- 同一路径失败两次，就切换路线，不要机械重试
- `python` 路线失效后，Node 和 PowerShell 足够覆盖大多数任务

## 速查表

| 现象 | 常见原因 | 立即回退 |
|------|---------|---------|
| `~/.codex/superpowers/...` 无法启动 | Windows 不能直接执行该入口 | `node C:/Users/Administrator/.codex/superpowers/.codex/superpowers-codex ...` |
| `rg` 报 `ResourceUnavailable` | `rg.exe` 在当前环境不可启动 | `Get-ChildItem` + `Select-String` |
| `python` 不存在 | PATH 中没有 Python | 切 Node / PowerShell |
| `py` 报 `No installed Python found` | 启动器存在但未绑定解释器 | 切 Node / PowerShell |
| 绝对路径 `python.exe` 拒绝访问 | 沙箱或工作目录阻止 | 不再尝试 Python |
| `Skill not found` | 技能名写错或不存在 | 重新看 bootstrap 列表，用精确技能名 |
| 读取 `.jsonl` 失败 | 文件被另一个进程占用 | 用 Node 读取或 `.NET FileShare.ReadWrite` |
| `UnicodeDecodeError` / `gbk` | 默认编码错误 | 改用 Node 或显式 UTF-8 读取 |

## 替代方案

### 用 Node 读取 UTF-8 文本

```powershell
node -e "const fs=require('fs'); console.log(fs.readFileSync('C:/path/file.md','utf8').slice(0,1000));"
```

### 用 PowerShell 搜索文件

```powershell
Get-ChildItem -LiteralPath <path> -Recurse -File | Select-String -Pattern '<pattern>'
```

### 用 Node 读取 JSONL

```powershell
@'
const fs = require('fs');
const lines = fs.readFileSync('C:/path/file.jsonl', 'utf8').trim().split(/\r?\n/);
for (const line of lines.slice(0, 5)) { console.log(JSON.parse(line).type); }
'@ | node -
```

### 用 .NET 共享读取被占用文件

```powershell
$fs = [System.IO.File]::Open($path, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
$reader = New-Object System.IO.StreamReader($fs, [System.Text.UTF8Encoding]::new($false))
try { $reader.ReadToEnd() } finally { $reader.Dispose(); $fs.Dispose() }
```

## 红旗

- 同一个失败命令连续重试两次以上
- 已看到 `No installed Python found` 还继续走 Python 路线
- `Skill not found` 后不看 bootstrap 列表，直接猜名字
