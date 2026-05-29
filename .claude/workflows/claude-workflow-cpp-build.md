# claude-workflow-cpp-build.md — C++ 编译工作流

## 触发条件

用户说"编译" / "build" / "构建" / "CMake" / "MSBuild"，且涉及 C++ 项目。

## 前置检测

1. 检查项目根目录是否存在 `CMakeLists.txt` 或 `.sln` / `.vcxproj` 文件
2. 如果都不是 C++ 项目 → 提示用户确认，避免误触发

## Phase 0：编译方式选择

**必须问用户选择编译方式（二选一）**：

| 方式 | 命令 | 适用场景 |
|------|------|---------|
| **A) CMake** | `cmake -G "Visual Studio 17 2022" -B build && cmake --build build --config Release` | 跨平台项目、有 CMakeLists.txt |
| **B) MSBuild** | `msbuild <project>.sln /p:Configuration=Release /p:Platform=x64` | 纯 Windows 项目、已有 .sln 文件 |

**自动推荐逻辑**：
- 存在 `CMakeLists.txt` → 推荐 CMake
- 仅存在 `.sln` → 推荐 MSBuild
- 两者都有 → 推荐用户选择

选择后记录到当前会话上下文，后续编译默认使用该方式。

## Phase 1：编译前检查

```
□ 确认编译方式（CMake / MSBuild）
□ 检查依赖是否就位（vcpkg / conan / 系统库）
□ 检查是否有未保存的改动（git status）
□ 确认编译配置（Debug / Release）
□ 确认目标平台（x86 / x64 / ARM64）
```

## Phase 2：执行编译

### CMake 路径

```bash
# 1. 配置（首次或 CMakeLists.txt 变更后）
cmake -G "Visual Studio 17 2022" -A x64 -B build

# 2. 编译
cmake --build build --config Release --parallel

# 3. 清理重编（用户要求时）
cmake --build build --target clean
cmake --build build --config Release
```

### MSBuild 路径

```bash
# 1. 编译
msbuild <project>.sln /p:Configuration=Release /p:Platform=x64 /m

# 2. 清理重编
msbuild <project>.sln /t:Clean /p:Configuration=Release
msbuild <project>.sln /p:Configuration=Release /p:Platform=x64 /m
```

## Phase 3：编译结果检查

```
□ 编译是否成功（exit code = 0）
□ 警告数量和级别（/W4 或 /Wall）
□ 输出产物位置（.exe / .dll / .lib / .a）
□ 输出文件大小是否合理
```

**编译失败时**：
1. 分析错误信息，定位根因
2. 修复后重新编译
3. 最多重试 3 轮
4. 超过 3 轮 → 通知用户人工介入

## Phase 4：编译后可选操作

向用户确认：
- **运行单元测试？** → 跳转到 `claude-workflow-cpp-test.md`
- **查看编译警告？** → 输出警告详情
- **生成编译报告？** → 输出编译摘要

## 输出格式

```text
## 编译报告

| 项目 | 结果 |
|------|------|
| 编译方式 | CMake / MSBuild |
| 配置 | Release / Debug |
| 平台 | x64 |
| 结果 | ✅ 成功 / ❌ 失败 |
| 警告数 | X |
| 错误数 | X |
| 耗时 | Xs |
| 输出路径 | build/bin/... |

### 警告列表（如有）
- [文件:行] 警告内容

### 输出产物
- build/bin/Release/app.exe (XX MB)
- build/bin/Release/lib.dll (XX MB)
```

## 验证完成门禁

参见 `claude-workflow-governance.md` 中的"验证完成门禁（全 workflow 通用）"。
