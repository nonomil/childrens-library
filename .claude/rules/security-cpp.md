---
paths:
  - "**/*.cpp"
  - "**/*.cc"
  - "**/*.h"
  - "**/*.hpp"
---

# 安全规范（C++）

> 依据：C++ Core Guidelines 安全 profile + CERT C++ + CWE Top 25。

## 内存安全

- 禁止裸 `new` / `delete`，统一用智能指针（见 code-style-cpp.md）
- 数组访问需要边界检查时用 `.at()`，不用 `[]`
- 禁止使用不安全 C 函数：

  | 禁止 | 替代 |
  |------|------|
  | `gets()` | `fgets()` 或 `std::getline()` |
  | `sprintf()` | `snprintf()` 或 `std::format()`（C++20） |
  | `strcpy()` / `strcat()` | `strncpy()` / `strncat()` 或 `std::string` |
  | `scanf("%s")` | 指定宽度 `scanf("%255s")` 或用流 |

- 禁止 `reinterpret_cast` 用于非 POD 类型
- 禁止读取未初始化变量（开启 `-Wall -Wuninitialized`）
- 缓冲区写入前检查目标大小

## 输入验证

- 所有外部输入（文件路径、网络数据、用户参数）必须验证长度和格式
- 整数输入检查溢出：用 `std::numeric_limits` 边界校验或 checked arithmetic
- 文件路径用 `std::filesystem::canonical()` 规范化，防止目录穿越：
  ```cpp
  auto resolved = std::filesystem::canonical(user_path);
  if (!IsUnderAllowedRoot(resolved)) {
      throw std::invalid_argument("路径越界: " + resolved.string());
  }
  ```

## 路径与命令安全

- 禁止拼接用户输入构造 shell 命令（`system()`、`popen()`）
- 必须执行外部命令时用参数数组（`execv` 系列或 `CreateProcess`），不用字符串拼接
- 输出路径不能指向系统目录（`/etc`、`/proc`、`C:\Windows` 等）

## 并发安全

- 共享可变数据必须用 `std::mutex` 或原子类型保护（见 code-style-cpp.md）
- 数据竞争检测：开发阶段用 `-fsanitize=thread`（ThreadSanitizer）
- 死锁预防：多锁按固定顺序获取，或用 `std::scoped_lock` 同时获取

## 编译期安全加固

开发和 CI 构建必须启用：

```cmake
target_compile_options(${TARGET} PRIVATE
  -Wall -Wextra -Wpedantic
  -Wformat=2          # 格式字符串漏洞
  -Wnull-dereference
  -Wstack-protector
)

# Debug / CI 构建额外开启
target_compile_options(${TARGET} PRIVATE
  -fsanitize=address,undefined   # ASan + UBSan
)
target_link_options(${TARGET} PRIVATE
  -fsanitize=address,undefined
)
```

## Secrets 与数据安全

- 禁止以明文存储密码、密钥等敏感数据
- 内存中的敏感数据用完后显式清零（`std::fill` 或 `SecureZeroMemory`）；不依赖析构函数，编译器可能优化掉普通赋零
- 禁止联网上传文件（除非有明确业务需求且经过审查）

## 静态分析

- CI 中集成至少一个静态分析工具：`clang-tidy`（推荐）或 `cppcheck`
- 关键规则集：`clang-analyzer-security.*`、`cert-*`、`bugprone-*`
