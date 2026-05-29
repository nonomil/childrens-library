---
name: memory-system
description: "本地记忆系统（实验性可选增强）。将 Markdown 文件索引到 SQLite 实现跨会话语义搜索。仅在记忆文件 >50 或 Grep 搜索效果不佳时启用。零外部依赖，纯 SQLite FTS5。"
layer: always
tags: [memory, sqlite, search]
domain: memory
---

> ⚠️ **实验性功能** — 本技能为可选增强，非必需。
> - **启用条件**：`.claude/memory/` 下文件 >50 个，或 Grep 关键词搜索效果不佳
> - **依赖**：零外部依赖（纯 Python + SQLite）
> - **默认**：所有工作流使用 `memory` skill（Grep 搜索），不调用本技能
> - **与 memory skill 关系**：本技能是 memory skill 的搜索引擎增强，不替代它


# Memory System

脚本路径: `.claude/skills/memory-system/scripts/memory.py`

## 自动行为

### 当用户说"搜索记忆"或"在记忆中查找 X"

```bash
python scripts/memory.py search "用户的查询" \
  --db ./memory/memory.sqlite --json --top 6
```

读取 JSON 结果后，用搜索到的上下文回答用户问题。如果数据库不存在，先执行索引。

### 当用户说"记住这个"或"添加到记忆"

将内容写入 `memory/` 目录的 .md 文件：

```bash
python scripts/memory.py add "内容" \
  --file 合适的文件名.md --dir ./memory --db ./memory/memory.sqlite
```

### 当用户说"索引记忆"或"更新记忆索引"

```bash
python scripts/memory.py index \
  --dir ./memory --db ./memory/memory.sqlite
```

### 当用户说"记忆状态"或"memory status"

```bash
python scripts/memory.py status \
  --db ./memory/memory.sqlite -v
```

### 当用户说"清理记忆"

```bash
python scripts/memory.py cleanup \
  --days 90 --dir ./memory --force
```

## 首次使用

如果运行脚本报 `ModuleNotFoundError`，安装依赖：

```bash
pip install -r scripts/requirements.txt
```

## 注意事项

- `./memory/` 和 `--db` 路径相对于项目工作目录
- 索引是增量的（SHA256 哈希比对），重复运行不会重新处理未变化的文件
- 搜索只查 SQLite，不读源文件
- `--json` 输出适合程序解析，不加则人类可读

## 配置参考

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `CHUNK_MAX_CHARS` | 1600 | 分块最大字符数（~400 tokens） |
| `CHUNK_OVERLAP_CHARS` | 320 | 分块重叠字符数（~80 tokens） |
| `DEFAULT_TOP_K` | 6 | 默认返回结果数 |
| `DEFAULT_MIN_SCORE` | -20.0 | BM25 最小分数阈值（越低越宽松） |
| `TOKENIZER` | trigram | FTS5 分词器（支持中文子串匹配） |
