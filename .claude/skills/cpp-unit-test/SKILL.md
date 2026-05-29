---
name: cpp-unit-test
description: C++ 单元测试（Google Test），支持直接运行已有测试可执行文件、CTest 运行、编译后运行。自动生成测试报告。
layer: domain
tags: [cpp, test, gtest]
domain: cpp
---

# C++ 单元测试技能

## ⛔ MANDATORY GATES (read before proceeding)

> 执行前必须 echo-back 本块。未输出 = 未开始。

| # | 门禁点 | 位置 | 通过条件 |
|---|--------|------|----------|
| G1 | 测试全部通过 | 运行后 | 退出码 = 0，无 FAIL |
| G2 | 生成测试报告 | 末尾 | 报告含：通过/失败/跳过数 |

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

写入 `docs/plan/tasks/<task>/review.md`（有任务目录时）或 `docs/test_report.md`。

## Sanitizer 支持

编译时启用 sanitizer 可检测运行时内存错误：

| Sanitizer | CMake 选项 | 检测内容 |
|-----------|-----------|---------|
| ASAN (Address) | `-fsanitize=address` | 越界、use-after-free、双重 free |
| TSAN (Thread) | `-fsanitize=thread` | 数据竞争、死锁 |
| UBSAN (Undefined) | `-fsanitize=undefined` | 未定义行为（溢出、空指针等） |

**推荐 CMake 配置**：
```cmake
option(ENABLE_ASAN "Enable Address Sanitizer" OFF)
if(ENABLE_ASAN)
    target_compile_options(${TARGET} PRIVATE -fsanitize=address -fno-omit-frame-pointer)
    target_link_options(${TARGET} PRIVATE -fsanitize=address)
endif()
```

**使用**：`cmake -DENABLE_ASAN=ON .. && cmake --build . && ctest`

## 覆盖率测量

```bash
# gcov (GCC)
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="--coverage" ..
cmake --build .
ctest
gcov *.cpp.gcno

# llvm-cov (Clang)
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="-fprofile-instr-generate -fcoverage-mapping" ..
cmake --build .
ctest
llvm-profdata merge default.profraw -o test.profdata
llvm-cov show ./test_binary -instr-profile=test.profdata
```

**CI 门控**：覆盖率低于阈值（如 80%）时构建失败。

## CI 集成要点

- GitHub Actions: 使用 `actions/setup-cmake` + `ctest --output-junit report.xml`
- 失败时上传 test log 作为 artifact
- 覆盖率报告上传到 Codecov/Coveralls
- sanitizer 构建与普通构建分开运行（性能差异大）

## 约束

- 不修改测试源文件（除非修复失败测试时用户确认）
- 不删除编译产物
- 测试超时：单测试默认 60s，可配置
