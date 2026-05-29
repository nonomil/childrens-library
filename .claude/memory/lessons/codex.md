# Codex 调用教训

> 从 SPC_Floor 项目继承的通用教训。

- 调用方式优先级：脚本 > MCP > CLI
- 首次调用前检测可用性
- 重试导致上下文膨胀，不自动重试

## [2026-05-29] beecode.cc 503 恢复

**失败类型**: DEPENDENCY
**症状**: Codex MCP 调用返回 503 Service Unavailable (beecode.cc/responses)
**根因**: beecode.cc 后端临时过载，主页 200 但 /responses 端点 503
**修复**: 等待约2分钟后自动恢复，curl 验证端点返回 401（需认证=端点存在）
**教训**: beecode.cc 503 是临时性的，先 curl 验证端点状态，恢复后重试即可。降级方案：CC 自查完成审查
**相关文件**: `.codex/config.toml` (model_provider=cliproxyapi, base_url=https://beecode.cc)
