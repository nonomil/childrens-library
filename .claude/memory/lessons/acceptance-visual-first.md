---
name: dl_acceptance_visual_first
description: 训练、推理、实验任务在执行前必须先与用户对齐验收标准，且验收不能只看数值，必须检查最终图像效果
type: feedback
---
训练、推理、阈值扫描、消融实验等任务，执行前必须先和用户讨论并对齐验收标准；验收时不能只看日志、统计值或中间 mask，必须把最终图像效果作为硬门槛。

**Why:** 本次 T013 中，数值指标看起来在改善，但最终 `annotated_v2` / `comparison_v2` 仍与 T010 参考图差距很大，说明“只看指标不看最终图像”会导致误判通过。

**How to apply:** 以后在 training / inference / experiment 场景下，先与用户确认目标、通过条件、固定样例图和非目标，再执行；结果验收必须同时检查统计指标与最终图像效果，若两者冲突，以最终图像效果未达标为未通过或 PARTIAL。