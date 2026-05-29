# Codex Hooks 运行时说明

本目录承接 hooks 的统一运行时与后续场景 pack，目标是把 `docs/Hooks钩子功能说明/` 里的案例脚本沉淀成可组合、可验证、可灰度启用的能力层。

---

## 目录结构

```text
.codex/hooks/
├── README.md
├── runtime/
│   ├── __init__.py
│   ├── audit_log.py
│   ├── contracts.py
│   ├── dispatcher.py
│   ├── platform_adapter.py
│   ├── runner.py
│   └── state_store.py
├── packs/
│   ├── __init__.py
│   ├── common.py
│   ├── context/
│   ├── git/
│   ├── notify/
│   ├── quality/
│   ├── resilience/
│   ├── security/
│   └── validate/
└── tests/
    ├── fixtures/
    ├── test_compatibility.py
    ├── test_dispatcher.py
    └── test_packs.py
```

---

## 当前运行时能力

- 统一事件与动作契约
- 统一平台探测与兼容判断
- 统一共享状态存储
- 统一审计日志写入
- 统一调度器与 dry-run / simulate 入口
- 统一 pack runner 与 hooks.json 挂载方式

后续 pack 会在此基础上继续补：

- `quality`
- `security`
- `context`
- `git`
- `notify`
- `validate`
- `resilience`

---

## 共享状态约定

默认状态目录：

```text
.codex/hooks/state/
```

关键键位：

- `runtime.dispatch_total`
- `runtime.last_event`
- `runtime.last_output`
- `sessions.<session_id>.last_event`

说明：

- 所有文本文件都必须显式使用 UTF-8
- 审计日志写入 `.codex/hooks/state/audit.log.jsonl`
- 不允许各 pack 自己再发明平级状态文件名

---

## 调度器用法

### 1. 作为模块使用

```python
from pathlib import Path

from runtime.contracts import HookEvent, HookPlatform, HookRequest, HookResult
from runtime.dispatcher import DispatchRule, HookRuntimeDispatcher


def sample_rule(request: HookRequest) -> HookResult:
    return HookResult.context("示例上下文")


dispatcher = HookRuntimeDispatcher(project_dir=Path("."))
dispatcher.register_rule(
    DispatchRule(
        name="sample",
        events=(HookEvent.STOP,),
        handler=sample_rule,
    )
)
outcome = dispatcher.dispatch(
    HookRequest(
        event_name=HookEvent.STOP,
        platform=HookPlatform.CODEX,
        payload={"last_assistant_message": "hello"},
    )
)
print(outcome.to_payload())
```

### 2. 作为命令行模拟器使用

```bash
python .codex/hooks/runtime/dispatcher.py \
  --event Stop \
  --platform codex \
  --payload-file hook-payload.json \
  --dry-run
```

说明：

- `--payload-file` 可选；不传时默认从标准输入读取 JSON
- `--dry-run` 会把原本可能 `block / deny / allow` 的结果降级成说明文本，方便先观察再上门禁

### 3. 作为 pack runner 使用

```bash
python .codex/hooks/runtime/runner.py \
  --pack resilience \
  --event Stop \
  --platform codex \
  --mode warn \
  --payload-file hook-payload.json
```

说明：

- `--pack` 当前支持 `context`、`git`、`notify`、`quality`、`resilience`、`security`、`validate`
- `--mode` 支持 `observe`、`warn`、`enforce`
- runner 会自动挂载运行时基础守卫，再追加指定 pack 的规则
- `resilience` 除了限流恢复和 Stop 续跑，还会在 Windows 下处理 `rg ResourceUnavailable`、`py` 启动失败、`gbk` 解码错误，以及 `~/.codex/...` 的前置防呆
- `git` pack 的自动切分支、自动提交属于高副作用动作，只有在 `enforce` 且显式开启 `git_auto_branch` / `git_auto_commit`（或对应环境变量）时才会真正执行

---

## 平台策略

- Codex：先稳定 `Stop`、`PostToolUse` 和命令式验证
- Claude：保留完整事件矩阵与扩展能力
- Windows：避免 `~`、`/tmp`、系统默认编码和类 Unix shell 假设

---

## 测试

```bash
python .codex/hooks/tests/test_dispatcher.py
python .codex/hooks/tests/test_packs.py
python .codex/hooks/tests/test_compatibility.py
```

测试覆盖：

- 调度顺序与终止语义
- dry-run 行为
- `PermissionRequest` 自动放行输出
- 状态存储与审计日志落盘
- pack 规则行为、fixture 和平台兼容判断
