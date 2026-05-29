---
name: memory-system
description: "本地记忆系统，将 Markdown 文件索引到 SQLite 实现跨会话语义搜索。支持增量索引、混合搜索（向量+全文）、记忆添加和清理。"
---

# Memory System

脚本路径: `scripts/memory.py`

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
| `EMBEDDING_DIM` | 384 | 向量维度（all-MiniLM-L6-v2） |
| `VECTOR_WEIGHT` | 0.7 | 混合搜索中向量搜索权重 |
| `TEXT_WEIGHT` | 0.3 | 混合搜索中全文搜索权重 |
| `DEFAULT_TOP_K` | 6 | 默认返回结果数 |
| `DEFAULT_MIN_SCORE` | 0.35 | 最小分数阈值 |
