# claude-workflow-cpp-test.md — C++ 单元测试工作流

## 触发条件

用户说"运行测试" / "跑单测" / "gtest" / "单元测试" / "test"，且涉及 C++ 项目。

## 前置检测

1. 检查是否有可执行文件（编译产物）
2. 如果没有 → 提示用户先编译，或自动调用 `claude-workflow-cpp-build.md`
3. 检查是否使用 GTest 框架（grep `gtest` / `TEST()` 宏）

## Phase 0：任务难度评估

**CC 自主判断，决定测试范围**：

```
满足全部 → 轻量模式（直接测）：
  ✓ 仅改单个函数/方法
  ✓ 改动 ≤ 50 行
  ✓ 无跨模块依赖
  ✓ 现有测试已覆盖该区域

任意不满足 → 完整模式（走全部 Phase）：
  → 跨模块 / 核心算法 / API 变更 / 新功能
  → 改动 > 50 行
  → 现有测试覆盖不确定
```

判断后告知用户结果和将走的流程。

## Phase 1：测试范围确定

**轻量模式**：
- 只运行受影响模块的测试
- 输出简要结果

**完整模式**：
- 运行全量测试
- 生成详细报告
- 包含覆盖率分析（如可获取）

## Phase 2：执行测试

### 方式 A：通过 CTest

```bash
# 配置（如需要）
cmake --build build --config Release

# 运行全部测试
cd build && ctest --output-on-failure --output-junit test_report.xml

# 运行指定测试
cd build && ctest -R <test_name> --output-on-failure
```

### 方式 B：直接运行 GTest 可执行文件

```bash
# 运行全部
./build/bin/Release/test_runner --gtest_output=xml:test_report.xml

# 运行指定测试
./build/bin/Release/test_runner --gtest_filter=TestSuite.TestName --gtest_output=xml:test_report.xml

# 运行并显示详细输出
./build/bin/Release/test_runner --gtest_print_time=1 --gtest_output=xml:test_report.xml
```

### 方式 C：已有二进制，无需编译

```bash
# 直接运行已有的测试可执行文件
<path/to/test_executable> --gtest_output=xml:test_report.xml
```

## Phase 3：结果分析

解析 XML 报告或命令行输出：

```text
## 测试报告

| 项目 | 结果 |
|------|------|
| 总测试数 | X |
| 通过 | X |
| 失败 | X |
| 跳过 | X |
| 耗时 | Xs |
| 通过率 | XX% |

### 失败测试详情
| 测试名 | 文件:行 | 失败原因 |
|--------|---------|---------|
| TestSuite.TestName | src/test.cpp:42 | Expected 5 but got 3 |

### 结论
PASS / FAIL / PARTIAL
```

## Phase 4：失败处理

1. 分析失败原因（断言错误 / 编译问题 / 环境问题）
2. 修复测试或代码
3. 重新运行失败的测试
4. 最多 3 轮修复
5. 超过 3 轮 → 标记 `blocked`，通知用户介入

**修复策略**：
- 断言错误 → 修复代码逻辑或更新测试预期
- 编译问题 → 跳转到 `claude-workflow-cpp-build.md`
- 环境问题 → 提示用户检查依赖

## Phase 5：结果审查

**自动审查清单**：
```
□ 所有测试通过？如有失败，是否已知 issue？
□ 新增测试是否覆盖了关键路径？
□ 测试耗时是否合理（无超时）？
□ 是否有被跳过的测试（DISABLED_）？原因是什么？
□ 通过率是否达标（项目标准，默认 100%）？
```

## Phase 6：报告输出

写入 `pipeline/test_report.md`（如 pipeline 存在）或 `docs/test_report.md`：

```markdown
# C++ 单元测试报告

## 执行摘要
- 日期：YYYY-MM-DD
- 测试框架：Google Test
- 通过率：XX%
- 结论：PASS / FAIL / PARTIAL

## 测试结果
[Phase 3 的表格]

## 失败分析（如有）
[Phase 4 的修复记录]

## 审查结论
[Phase 5 的审查结果]

## 建议
- [优化建议 1]
- [优化建议 2]
```

## 验证完成门禁

参见 `claude-workflow-governance.md` 中的"验证完成门禁（全 workflow 通用）"。
