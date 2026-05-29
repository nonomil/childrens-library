---
name: cpp-build
description: C++ 项目编译，支持 CMake 和 MSBuild 两种方式。编译前检测项目结构，编译后输出报告。
---

# C++ 编译技能

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

## 约束

- 不删除源文件
- 不修改 .sln / CMakeLists.txt（除非用户明确要求）
- 编译产物输出到 `build/` 目录
