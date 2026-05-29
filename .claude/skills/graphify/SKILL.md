---
name: graphify
description: Use when 需要为当前项目创建知识图谱、生成代码图谱、运行 graphify、建立可查询的代码关系图，或用户明确说"创建知识图谱""生成知识图谱""graphify""代码图谱""知识图谱"。
layer: ondemand
tags: [graphify, graph, scan, knowledge]
domain: tooling
---

# graphify

## ⛔ MANDATORY GATES (read before proceeding)

> 执行前必须 echo-back 本块。未输出 = 未开始。

| # | 门禁点 | 位置 | 通过条件 |
|---|--------|------|----------|
| G1 | 输出目录符合规范 | 执行前 | docs/代码库-知识图谱/{项目名}-LLM图谱/ |
| G2 | 产物完整性 | 执行后 | graph.json + GRAPH_REPORT.md 均存在 |

## 目标

为当前项目生成可查询的本地图谱产物，优先服务 Codex/Claude 后续的架构理解与关系追问。

## 统一输出目录规范

**所有知识图谱工具的输出，统一放在仓库根目录 `docs/代码库-知识图谱/` 下，按项目名+图谱类型扁平存放**：

```
docs/代码库-知识图谱/
├── {项目名}-LLM图谱/            ← graphify（语义级，LLM 推断关系）
├── {项目名}-AST图谱/            ← code-review-graph（结构级，AST 解析）
├── {项目名}-模块架构和数据流/    ← cartographer（架构扫描）
```

示例：
```
docs/代码库-知识图谱/
├── 检测软件工程-LLM图谱/
├── 检测软件工程-AST图谱/
├── 检测软件工程-模块架构和数据流/
├── ClaudeCode_Codex_Cowork_Example-LLM图谱/
└── ...
```

项目名规则：
- 扫描根目录 → 用根目录文件夹名（如 `ClaudeCode_Codex_Cowork_Example`）
- 扫描 `prj/xxx` → 用 `xxx`（如 `检测软件工程`）

工具代码位于 `.claude/tools/`：
- `.claude/tools/graphify-viewer/` — 浏览器可视化工具
- `.claude/tools/code-review-graph-viewer/` — code-review-graph 浏览器 viewer

## 默认入口

```bash
# 扫描根目录项目
python .claude/scripts/graphify_codebase_scan.py \
  --scope .agents .claude .codex scripts \
  --generate-viewer

# 扫描 prj 下的子项目
python .claude/scripts/graphify_codebase_scan.py \
  --project-dir prj/检测软件工程 \
  --scope core utils gui \
  --generate-viewer
```

输出自动计算，无需手动指定 `--output-dir`。

## 执行步骤

1. 先确认用户要的是"创建知识图谱/代码图谱"，而不是完整 `CODEBASE_MAP.md` 架构文档。
2. 运行项目包装脚本，**加 `--generate-viewer`**：
   ```bash
   python .claude/scripts/graphify_codebase_scan.py \
     --scope .agents .claude .codex scripts \
     --generate-viewer
   ```
3. 脚本自动完成：graphify 扫描 → 生成 viewer_data.js → 启动浏览器
4. 读取 `docs/代码库-知识图谱/{项目名}/LLM图谱/scan-summary.json`，向用户汇报统计。
5. 读取 `docs/代码库-知识图谱/{项目名}/LLM图谱/GRAPH_REPORT.md`，提取关键发现。
6. **扫描完成后告知用户**：
   ```
   ✅ 知识图谱已生成！

   📂 扫描结果：docs/代码库-知识图谱/{项目名}/LLM图谱/
   📊 统计：{node_count} 节点 / {edge_count} 边 / {community_count} 社区
   🌐 浏览器已自动打开（或手动双击：docs/代码库-知识图谱/{项目名}/LLM图谱/打开图谱查看器.bat）
   ```

## 产物

输出到 `docs/代码库-知识图谱/{项目名}/LLM图谱/`：
- `GRAPH_REPORT.md` — 分析报告
- `graph.json` — 图谱数据
- `graph.html` — graphify 内置可视化
- `scan-summary.json` — 扫描摘要
- `打开图谱查看器.bat` — 用户手动打开浏览器入口

工具侧：
- `.claude/tools/graphify-viewer/viewer_data.js`（自动生成）

## 与其他工具的边界

| 工具 | 层级 | 输出位置 | 用途 |
|------|------|---------|------|
| graphify | LLM 语义级 | `docs/代码库-知识图谱/{项目名}-LLM图谱/` | 跨文件推断关系，社区检测 |
| code-review-graph | AST 结构级 | `docs/代码库-知识图谱/{项目名}-AST图谱/` | 精确调用链，测试覆盖 |
| cartographer | 人类可读文档 | `docs/代码库-知识图谱/{项目名}-模块架构和数据流/` | 架构综述，onboarding |

- 用户说"创建知识图谱" → `graphify`
- 用户说"生成 CODEBASE_MAP.md / 架构地图" → `cartographer`
- 用户说"查调用链 / 依赖关系 / 测试覆盖" → `code-review-graph`
