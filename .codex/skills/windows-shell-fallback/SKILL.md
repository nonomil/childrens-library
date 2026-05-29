---
name: windows-shell-fallback
description: Windows 环境启动时加载。提供 shell 命令优先级、路径自适应、编码规范，预防 ResourceUnavailable / GBK 乱码 / python 缺失等常见问题。Codex 启动、执行任何 shell 命令、遇到路径或编码问题时自动适用。
---

# Windows Shell 预防指南

> 目标：**预防**问题，不是等问题出现再回退。Codex 在 Windows 上执行任何 shell 命令前，按本指南选择正确的执行路径。

---

## 启动自检（每次会话第一个命令）

```powershell
# 步骤 1：获取 home 目录（不硬编码用户名）
node -e "console.log(require('os').homedir())"

# 步骤 2：用 node 执行 superpowers bootstrap
node <步骤1输出>/.codex/superpowers/.codex/superpowers-codex bootstrap

# 步骤 3：检查全局 AGENTS.md 是否需要修复
node -e "const f=require('os').homedir()+'/.codex/AGENTS.md'; const c=require('fs').readFileSync(f,'utf8'); if(c.includes('~/.codex/superpowers')){const n=c.replace(/~\/\.codex\/superpowers\/\.codex\/superpowers-codex bootstrap/g,'node '+require('os').homedir().replace(/\\/g,'/')+'/.codex/superpowers/.codex/superpowers-codex bootstrap'); require('fs').writeFileSync(f,n,'utf8'); console.log('[FIXED] AGENTS.md bootstrap path updated');} else {console.log('[OK] AGENTS.md already correct');}"
```

---

## Shell 命令优先级（Windows）

按此顺序选择执行工具，**不要跳级尝试**：

| 优先级 | 工具 | 适用场景 | 何时跳过 |
|--------|------|---------|---------|
| 1 | `node -e` | 文件读取、JSON 解析、文本处理、路径操作 | — |
| 2 | PowerShell 原生 | 目录遍历、文件搜索、进程管理 | 需要跨平台时 |
| 3 | `python` | 仅当任务明确需要 Python 生态（如 Pillow、pytest） | PATH 中无 python |

**禁止**：
- 直接执行 `~/.codex/...`（Windows 不展开 `~`）
- 用 `Get-Content`/`Set-Content` 不带 `-Encoding UTF8`（默认 GBK 会乱码）
- `python` 失败后继续尝试 `python3`、`py`（浪费轮次）
- `rg` 失败后重试（直接换 `Get-ChildItem` + `Select-String`）

---

## 常用操作的正确写法

### 读取文本文件

```powershell
# 正确：node + utf8
node -e "console.log(require('fs').readFileSync('C:/path/file.md','utf8').slice(0,2000))"

# 正确：PowerShell + UTF8
Get-Content -LiteralPath 'C:\path\file.md' -Encoding UTF8

# 错误：PowerShell 默认编码（GBK）
Get-Content 'C:\path\file.md'   # ← 中文会乱码
```

### 搜索文件内容

```powershell
# 正确：PowerShell 原生（rg 不可用时）
Get-ChildItem -LiteralPath 'C:\path' -Recurse -File | Select-String -Pattern 'keyword'

# 正确：node
node -e "const{execSync}=require('child_process'); console.log(execSync('findstr /s /i keyword C:\\path\\*.md',{encoding:'utf8'}))"
```

### 读取被占用的文件（jsonl 等）

```powershell
# 正确：Node 流式读取
node -e "const rl=require('readline').createInterface({input:require('fs').createReadStream('C:/path/file.jsonl',{encoding:'utf8'})}); rl.on('line',l=>{console.log(JSON.parse(l).type)}); setTimeout(()=>rl.close(),3000)"

# 正确：.NET 共享读取
$fs = [System.IO.File]::Open($path, 'Open', 'Read', 'ReadWrite)
$reader = New-Object System.IO.StreamReader($fs, [System.Text.UTF8Encoding]::new($false))
try { $reader.ReadToEnd() } finally { $reader.Dispose(); $fs.Dispose() }
```

### Superpowers 技能调用

```powershell
# 正确：node + 动态 home 路径
node "$((node -e \"console.log(require('os').homedir())\" ))/.codex/superpowers/.codex/superpowers-codex use-skill superpowers:using-superpowers"

# 错误：直接路径
~/.codex/superpowers/.codex/superpowers-codex use-skill ...   # ← Windows 无法执行
```

---

## 路径规范

| 写法 | 可用性 | 说明 |
|------|--------|------|
| `C:/Users/XXX/...` | 每台机器不同 | 禁止硬编码用户名 |
| `~/.codex/...` | Linux/Mac | Windows PowerShell 不展开 |
| `$HOME/.codex/...` | bash | PowerShell 不识别 |
| `node -e "require('os').homedir()"` | 全平台 | **推荐**：动态获取 |
| `%USERPROFILE%\.codex\...` | cmd.exe | PowerShell 中也可用 `$env:USERPROFILE` |

**推荐模式**：所有涉及 home 目录的命令，统一用 `node -e "require('os').homedir()"` 获取，拼接到路径中。

---

## 红旗（出现即停）

- 同一个失败命令重试 2 次以上
- `python` 失败后还尝试 `python3`、`py`、`python.exe`
- `ResourceUnavailable` 后不切换工具继续尝试
- 使用 `Get-Content` 不带 `-Encoding UTF8`
- 路径中包含 `~`（在 PowerShell 中无效）
