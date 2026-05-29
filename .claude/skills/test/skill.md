---
name: test
description: Use when 需要围绕当前任务的 acceptance、handoff 和 review 证据运行测试，并在通过后把任务推进到待评审状态。
layer: domain
tags: [test, pytest, taskctl]
domain: testing
---

# 任务测试技能

当前 Codex 主流程里的测试，不再是独立的旧 pipeline 阶段文件，而是围绕任务目录中的 `acceptance.md`、`handoff.md`、`review.md` 和本地验证命令完成。测试的目标是拿到足够证据支撑 `submit`，而不是只给一句“跑过了”。

## 触发方式

- 实现阶段已完成，需要补任务级验证证据
- 用户要求“跑测试”“补回归”“确认可提交 review”
- 评审前需要把失败原因、修复结果和残余风险写回任务目录

## 先看什么

1. 目标任务目录下的 `acceptance.md`
2. 目标任务目录下的 `handoff.md`
3. 目标任务目录下的 `review.md`
4. `AGENTS.md`
5. `python scripts/taskctl.py submit -h`

## 推荐测试节奏

### 1. 先按任务契约收敛范围

优先确认：

- `acceptance.md` 要求的命令和通过标准
- `handoff.md` 已记录的已知风险、未完成项、环境约束
- 是否需要把关键失败原因补充到 `review.md`

### 2. 跑最小可复现验证

默认先从快速 pytest 开始：

```bash
python -m pytest --tb=short -q
```

如果失败，再拉长日志定位：

```bash
python -m pytest --tb=long -v
python -m pytest --tb=short -q --lf
```

如果任务要求的不是 pytest，以 `acceptance.md` 中记录的命令为准。

### 3. 回写测试证据

- 在 `handoff.md` 记录本次执行的命令、结果、失败原因和修复结论
- 需要让 reviewer 直接看到风险时，把摘要同步到 `review.md`
- 若新增验证边界或例外说明，也要补回 `acceptance.md`

### 4. 通过后推进到待评审

验证完成且证据充分后，再提交：

```bash
python scripts/taskctl.py submit --task T001
```

`submit` 表示“已准备进入 review”，不是“已经批准合并”。

## 输出至少要包含

- 实际执行过的命令
- 通过 / 失败结果
- 失败时的原因与修复动作
- 剩余风险或未覆盖场景

## 不要这样做

- 不要再把旧 `pipeline` 状态文件当测试结果账本
- 不要把项目私有示例路径硬编码进技能模板
- 不要只口头说“测试通过”，不写回 `handoff.md`
- 不要绕过 `submit`，直接宣称任务已经进入评审
