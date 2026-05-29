---
name: cpp-unit-test
description: C++ 单元测试（Google Test），支持直接运行已有测试可执行文件、CTest 运行、编译后运行。自动生成测试报告。
---

# C++ 单元测试技能

## 适用场景

- C++ 项目需要运行单元测试
- 用户说"运行测试" / "跑单测" / "gtest"
- 编译完成后需要验证

不适用：非 C++ 项目、非单元测试（如集成测试、性能测试）。

## 运行方式

### 方式 A：直接运行已有测试可执行文件（无需编译）

```bash
<path/to/test_executable> --gtest_output=xml:test_report.xml

# 指定测试
<path/to/test_executable> --gtest_filter=TestSuite.TestName --gtest_output=xml:test_report.xml
```

### 方式 B：通过 CTest

```bash
cd build && ctest --output-on-failure --output-junit test_report.xml

# 指定测试
cd build && ctest -R <test_name> --output-on-failure
```

### 方式 C：编译后运行

先调用 `cpp-build` 技能编译，再运行测试。

## 任务难度评估

CC 自主判断：

| 判断标准 | 轻量模式 | 完整模式 |
|---------|---------|---------|
| 改动范围 | 单函数/方法 | 跨模块/核心算法 |
| 改动行数 | ≤ 50 行 | > 50 行 |
| 覆盖情况 | 现有测试已覆盖 | 覆盖不确定 |
| 执行方式 | 只跑受影响测试 | 全量测试 + 覆盖率 |

## 执行流程

1. **检测测试可执行文件**：是否存在已编译的测试
2. **评估任务难度**：轻量模式 vs 完整模式
3. **运行测试**：选择 A/B/C 方式
4. **解析结果**：从 XML 或命令行输出提取通过/失败/跳过
5. **失败处理**：分析原因 → 修复 → 重跑（最多 3 轮）
6. **输出报告**：

```
总测试数: X
通过: X
失败: X
跳过: X
通过率: XX%
耗时: Xs
结论: PASS / FAIL / PARTIAL
```

## 报告输出

写入 `pipeline/test_report.md`（pipeline 存在时）或 `docs/test_report.md`。

## 约束

- 不修改测试源文件（除非修复失败测试时用户确认）
- 不删除编译产物
- 测试超时：单测试默认 60s，可配置
