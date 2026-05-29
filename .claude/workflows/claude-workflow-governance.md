# claude-workflow-governance.md — 运行治理与 Prompt 资产

> 本文档承载所有 workflow 不必默认常驻、但在验证收口、记忆沉淀、上下文治理和 Prompt 复用时必须遵守的共享规则。

---

## 1. 验证完成门禁（全 workflow 通用）

每个任务标记完成前，必须满足：

- 运行测试或实际调用，证明功能可用
- 质量自检清单全部通过：
  - 问题真是存在吗？是真实问题还是想象的？
  - 有没有更简单的方式？
  - 这会破坏现有功能或向后兼容吗？
  - Staff Engineer 会批准这个最终方案吗？
- 对非简单修复，主动思考“有没有更优雅的写法”；若有则重构

---

## 2. Self-Improvement 全局规则

### 2.1 文件路径

- 固定路径：`.claude/memory/lessons/`
- 首次使用时自动创建

### 2.2 记录格式

```markdown
- [YYYY-MM-DD] [场景/bug-id] → 错误根因 → 下次防范方式
```

### 2.3 写入时机

| 触发事件 | 写入内容 |
|----------|----------|
| 用户纠正 AI 错误 | 错误 pattern + 防范规则 |
| Bug 修复完成 | 根因 + 预防措施 |
| 任务执行中发现可复用经验 | 经验 pattern |
| Review 超过 3 轮仍未通过 | 记录任务粒度判断失误及原因 |
| 简单模式升级为复杂模式 | 记录误判原因 |

### 2.4 读取时机

| 触发事件 | 读取目的 |
|----------|----------|
| 任何新任务开始 | 规避历史错误 |
| 每个 Codex Session 开始 | 注入相关约束到 Prompt |

---

## 3. Context 健康检查门禁

每个 Phase 切换前估算 context 占用，按以下阈值处理：

| Context 占用 | 处理方式 |
|--------------|----------|
| ≤50% | 正常继续 |
| >50% | 在 Phase 交界处执行 `/compact` |
| >70% | 强制 `/compact`，并把关键状态写入 `docs/plan/handoff-*.md` |
| >85% | 必须开新 Session，通过 handoff 文档传递状态 |

估算方式：
- 已读取文件数 × 约 `15k tokens/文件`
- 对话历史行数 × 约 `0.5k tokens/行`

handoff 文档必须包含：
- 当前 Phase
- 已完成步骤
- 未完成步骤
- 关键决策和约束
- 待解决阻塞项

生命周期：
- 新 Session 启动时，读取最新的 `docs/plan/handoff-*.md`
- 任务完成后，将已用 handoff 文档移动到 `docs/archive/`

### P4 增强：上下文根除策略（Conductor 模式下优先）

> 设计灵感：BinkRon Conductor 通过 progress.md 做结构化交接，"根本不让上下文长到需要续命的程度"。

**优先级**：当使用 `claude-workflow-conductor.md` 执行任务时，此策略优先于上方压缩策略。

**原则**：每个 task 用新 session，通过 progress.md 做结构化交接，不继承整个对话历史。

**实施路径**：
1. Conductor 每完成一个 task，生成/更新 progress.md（已完成列表 + 关键决策 + 变更摘要）
2. 下一个 task 启动时，只读取：progress.md + 该 task 的 steps.md + 相关源文件
3. 不读取整个对话历史
4. 本节上方的 Context 压缩策略降级为"兜底保险"（非 Conductor 模式仍生效）

**交接协议**（详见 `claude-workflow-conductor.md` Phase 2）：

```
必读：progress.md + steps.md + Plan 相关部分
按需：相关源文件 + 测试文件
不读：整个对话历史 + 前序 task 详细执行过程 + 不相关文件
```

---

## 4. Codex 调用前上下文检查门禁

调用 Codex 生成代码前，CC 必须确认以下 4 项已注入 Context：

1. 技术栈版本
2. 相关文件路径
3. 现有实现模式
4. 约束边界

缺失时，优先从以下来源补齐：
- `scan.db`
- `doc-ref` skill
- `docs/CODEBASE_MAP.md`

---

## 5. SCAN_SUMMARY 刷新规则

- 写入位置：`claude.md` 中 `<!-- SCAN_SUMMARY_START -->` 与 `<!-- SCAN_SUMMARY_END -->` 之间
- 触发刷新：重大架构变更 / 核心模块新增或删除 / 距上次扫描超过 7 天
- 刷新命令：

```bash
python .claude/skills/largebase-structured-scan/scan.py export-to-claude-md \
  --db [latest_scan_db] \
  --claude-md claude.md
```

- 责任人：触发 largebase 扫描的一方在交付前必须刷新并核对摘要时效

---

## 6. Prompt 沉淀规则

1. 成功的 Codex Prompt 模板保存到 `.claude/memory/prompts/`
2. 命名格式：`[场景]-prompt.md`
3. 每个模板至少包含：场景说明 + 输入占位符 + 约束清单 + 输出格式要求
4. 同类任务优先复用已有模板，不重复从零写 Prompt
5. 模板经 3 次以上验证有效，标记为 `[STABLE]`
6. 失败 Prompt 的原因写入 `.claude/memory/lessons/`

---

<!-- BEGIN:doc-edit-protocol -->
## 7. 文档安全编辑协议

适用范围：
- `.md` / `.mdx` / `.html` / `.htm` / `.rst` / `.txt`
- `README.md`、`CLAUDE.md`、`AGENTS.md`
- `.claude/workflows/`、`docs/` 下的长文档

规则：
1. 改前必须重新读取目标文件最新内容，不允许基于旧上下文连续重试 patch
2. 对于大文档（建议阈值：`> 200` 行），只允许按 section 小块补丁，不做整页重写
3. 文档任务若目标文档 `>200` 行，应声明 `section_anchor`，或在 `doc_targets` 中写 `path + section_anchor`
4. 若文档存在 `BEGIN/END` 标记或稳定标题，优先围绕这些锚点编辑
5. patch 失败一次后，先重读文件，再重新生成补丁；禁止对同一旧上下文重复套补丁
6. `Read` 文档后应刷新 `.claude/state/MANIFEST.yaml` 内的 freshness snapshot；若 snapshot 与当前文件哈希不一致，后续写入必须先重新读取
7. 命中 `<!-- BEGIN GENERATED:... -->` / `<!-- END GENERATED:... -->` 的生成区块时，不直接手改产物，优先回到生成源或专用流程
8. 同一文档被多个活跃任务声明时：
   - `normal`：默认串行，不并发写
   - `advanced`：每个任务都必须补 `file_leases`，并让 `.claude/state/MANIFEST.yaml` 的 `current_focus.task_id` 指向当前任务
9. 若命中 `<!-- BEGIN GENERATED:... -->` / `<!-- END GENERATED:... -->`，视为 generated block：
   - 默认禁止直接改落地文档
   - 应改上游生成源，或切到对应生成链路后再更新
10. freshness 快照由 Hook 自动维护：
   - `Read` 后把 `content_hash` 记入 `.claude/state/MANIFEST.yaml` 的 `doc_freshness`
   - `Edit / Write / MultiEdit` 前若发现快照已过期，强制先重读文件

建议给 Codex 的约束语句：

```text
若目标是 >200 行的 Markdown/HTML 文档，只允许基于 section_anchor 或 BEGIN/END 标记做小块补丁。
若补丁失败，先重新读取目标文件，不允许基于旧上下文连续重试。
```
<!-- END:doc-edit-protocol -->

---

## 8. 输出与排版约束

### 8.1 结构化输出

Codex 输出必须包含：
- 结构化数据（JSON / 表格）
- 文件路径 + 行号引用
- 验证点 / 测试用例
- 信息缺口标注

禁止：
- 纯散文输出
- 无法追溯的结论
- 模糊的“可能 / 也许”

### 8.2 表格排版

- Markdown 表格统一使用左对齐或居中对齐
- 保持同一文档内对齐风格一致
- 优先表格，不堆砌大段文字

---

## 9. Codex Prompt 模板（通用）

> Context 注入原则：优先读取当前 `*-steps.md` 的 frontmatter `context:`，只加载显式声明的规范文件；禁止全量加载 `.claude/rules/`。

```text
## Context
- 技术栈：[语言/框架/版本]
- 规范文件（仅加载 steps.md frontmatter 中声明的）：
  [path1]：[一句话说明为何本任务需要它]
  [path2]：[一句话说明为何本任务需要它]
- 任务文件：[路径]：[用途]
- 参考：[风格/模式参考文件路径]

## Task
[清晰、单一、可验证的任务]
步骤：1. [步骤] 2. [步骤] 3. [步骤]

## Constraints
- API：不得修改 [签名]
- 范围：仅限 [当前 worktree 绝对路径] 下文件
- 依赖：不引入新依赖
- 风格：遵循 [参考]
- 禁止：不得修改、移动、删除范围外文件
- 禁止命令：rm -rf / del / rd /s / Remove-Item -Recurse / git clean -f / git reset --hard
- 推理强度说明（以参数层 reasoning 为准，此处仅作可读性说明）：
  - 审查/调试/规划（reasoning: high）：需要深度推理，先分析再结论
  - 直接编码/小改（reasoning: low）：直接执行，无需深度推理；只输出实现与结果

## Acceptance
- [ ] 测试通过（pytest / npm test）
- [ ] [项目特定验收标准]

## Output Format
1. 改动文件列表（路径 + 改动行数）
2. 验收自检结果（逐条打勾）
3. 遗留问题（若有）
```

---

## 版本历史

- 2026-03-01：从 constants 拆出 Self-Improvement 与验证门禁
- 2026-04-07：补齐 `docs/CODEBASE_MAP.md`、`scan.db`、Prompt 资产沉淀等治理契约
- 2026-04-07：新增文档安全编辑协议，约束大文档只做 section 级补丁，并与 `current_focus.task_id` / `file_leases` 联动
