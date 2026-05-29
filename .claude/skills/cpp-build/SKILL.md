---
name: cpp-build
description: C++ 项目编译，支持 CMake 和 MSBuild 两种方式。编译前检测项目结构，编译后输出报告。
layer: domain
tags: [cpp, build, cmake]
domain: cpp
---

# C++ 编译技能

## ⛔ MANDATORY GATES (read before proceeding)

> 执行前必须 echo-back 本块。未输出 = 未开始。

| # | 门禁点 | 位置 | 通过条件 |
|---|--------|------|----------|
| G1 | 编译通过才继续 | 编译后 | 退出码 = 0，无 error |
| G2 | 输出编译报告 | 末尾 | 报告含：警告数、错误数、耗时 |

## 适用场景

- C++ 项目需要编译
- 用户说"编译" / "build" / "构建"
- 单元测试前需要先编译

不适用：非 C++ 项目。

## 编译方式

### 方式 A：CMake

适用：跨平台项目、存在 `CMakeLists.txt`

```bash
# 配置
cmake -G "Visual Studio 17 2022" -A x64 -B build

# 编译
cmake --build build --config Release --parallel

# 清理重编
cmake --build build --target clean
cmake --build build --config Release
```

### 方式 B：MSBuild

适用：纯 Windows 项目、存在 `.sln` 文件

```bash
# 编译
msbuild <project>.sln /p:Configuration=Release /p:Platform=x64 /m

# 清理重编
msbuild <project>.sln /t:Clean /p:Configuration=Release
msbuild <project>.sln /p:Configuration=Release /p:Platform=x64 /m
```

## 选择逻辑

1. 存在 `CMakeLists.txt` → 推荐 CMake
2. 仅存在 `.sln` → 推荐 MSBuild
3. 两者都有 → **问用户选择**
4. 都没有 → 提示"未检测到 C++ 项目文件"

## 执行流程

1. **检测项目结构**：确认编译方式
2. **问用户确认**：编译方式 + 配置（Debug/Release）+ 平台（x86/x64）
3. **执行编译**
4. **检查结果**：exit code + 警告数 + 错误数
5. **输出报告**：
   ```
   编译方式: CMake / MSBuild
   配置: Release / Debug
   结果: ✅ 成功 / ❌ 失败
   警告: X 个
   错误: X 个
   耗时: Xs
   产物: [输出文件列表]
   ```

## 失败处理

- 最多重试 3 轮
- 每轮分析错误、修复、重编译
- 超过 3 轮 → 通知用户介入

## 常见编译错误速查表

| 错误类型 | 典型信息 | 常见原因 | 快速修复 |
|---------|---------|---------|---------|
| 头文件未找到 | `fatal error: No such file` | include 路径未配置 | 检查 CMake `target_include_directories` |
| 未定义引用 | `undefined reference to` | 链接顺序或缺少源文件 | 检查 `target_link_libraries` 和源文件列表 |
| 重复定义 | `multiple definition of` | 头文件中定义了非 inline 函数 | 加 `inline` 或移到 .cpp |
| 模板实例化失败 | `template instantiation error` | 缺少特化或 SFINAE 错误 | 检查模板参数约束 |
| CMake 未找到包 | `Could not findXXX` | 未安装或路径不对 | 设置 `XXX_ROOT` 或安装依赖 |
| 编译器版本不兼容 | `不支持某个 C++ 特性` | CMakeLists.txt 中标准设置过低 | `set(CMAKE_CXX_STANDARD 17)` |
| 预编译头问题 | `PCH warning/error` | 预编译头与当前配置不匹配 | 清理 build 目录重编译 |
| 链接器错误 LNK2001 | `unresolved external symbol` | Windows 专有：lib 文件路径或 32/64 位不匹配 | 检查 lib 路径和架构一致性 |
| UTF-8 BOM 问题 | `非 ASCII 字符错误` | 源文件含 BOM 或中文注释 | `/utf-8` 编译选项或转 UTF-8 无 BOM |
| 内存对齐 | `alignas` 或 packing 错误 | 跨平台结构体大小不一致 | 显式 `#pragma pack` 或 `alignas` |

## 3 次停止规则

遇到编译错误时：
1. **第 1 次**：分析错误信息，尝试修复
2. **第 2 次**：检查 CMake 配置和依赖，换一种修复方案
3. **第 3 次**：**停止**，向用户报告完整错误日志和已尝试的修复，请求指导

不要盲目重试。3 次失败意味着需要更多信息或人工决策。

## 约束

- 不删除源文件
- 不修改 .sln / CMakeLists.txt（除非用户明确要求）
- 编译产物输出到 `build/` 目录
