---
paths:
  - "**/*.cpp"
  - "**/*.cc"
  - "**/*.h"
  - "**/*.hpp"
---

# 代码风格（C++）

> 依据：Google C++ Style Guide + C++ Core Guidelines (C++17)。

## 标准版本

- 默认 C++17；有明确需求时升至 C++20
- 禁止已废弃特性：`auto_ptr`、`register`、C-style cast、`std::bind`（优先 lambda）

## 命名

| 场景 | 规则 | 示例 |
|------|------|------|
| 变量 / 函数参数 | `snake_case` | `file_path`, `max_size` |
| 函数 | `PascalCase` | `LoadImage()`, `MergeFiles()` |
| 类 / 结构体 / 枚举 | `PascalCase` | `ImageMerger`, `BatchConfig` |
| 常量 / 枚举值 | `kCamelCase`（Google 风格） | `kMaxBatchSize`, `kDefaultTimeout` |
| 私有成员变量 | 末尾下划线 | `file_path_`, `cache_size_` |
| 命名空间 | `snake_case` | `namespace image_merger` |
| 模板参数 | `PascalCase` | `typename T`, `typename KeyType` |
| 宏（必须用时） | `ALL_CAPS_WITH_PREFIX` | `PROJECT_VERSION` |

## 文件组织

- 头文件扩展名统一用 `.h`，实现文件用 `.cpp`
- 每个头文件必须有 `#pragma once`（优先于 include guard）
- 头文件只声明接口，实现放 `.cpp`（模板和 `constexpr` 除外）
- 导入顺序（每组空一行）：
  1. 对应头文件（`foo.cpp` 先 `#include "foo.h"`）
  2. C 标准库（`<cstdint>`, `<cstring>`）
  3. C++ 标准库（`<vector>`, `<string>`）
  4. 第三方库
  5. 本项目头文件（用引号）

## 内存管理

- 禁止裸 `new` / `delete`，统一用智能指针
- 独占所有权用 `std::unique_ptr`，共享所有权用 `std::shared_ptr`
- 工厂函数用 `std::make_unique` / `std::make_shared`，不直接 `new`
- RAII：资源在构造函数获取，在析构函数释放，不依赖手动 cleanup
- 禁止返回局部变量的指针或引用

```cpp
// 正确
auto merger = std::make_unique<ImageMerger>(config);

// 错误
ImageMerger* merger = new ImageMerger(config);
```

## 类设计

- 单参数构造器加 `explicit`，防止隐式转换
- 明确声明五大函数（copy/move 构造、copy/move 赋值、析构）或用 `= default` / `= delete`
- 优先组合而非继承；继承只用于"is-a"关系
- 所有继承声明为 `public`；需要私有继承时改用成员组合
- 虚析构函数：有虚函数的基类必须声明虚析构函数

## 类型与转换

- 用 `static_cast` / `dynamic_cast` / `const_cast`，禁止 C-style cast `(int)x`
- 跨平台 / 序列化场景用固定宽度类型：`int32_t`, `uint64_t`
- 浮点数比较用 epsilon，禁止直接 `==`
- 优先用 `std::string` 而非 `char*`；需要 C 接口时再 `.c_str()`

## 现代 C++ 惯用法

- 范围 for 代替下标循环（需要索引时用 `enumerate` 等辅助或显式索引）
- `auto` 减少冗余类型声明，但公开 API 签名要写明确类型
- 移动语义：大对象传参用 `const T&` 或 `T&&`，不值传递
- `constexpr` 优先于 `#define` 宏常量
- 结构化绑定（C++17）：`auto [key, val] = *it;`
- `std::optional<T>` 表示可能为空的返回值，不用 `nullptr` 或哨兵值

## 错误处理

- 可恢复错误用返回值：`std::optional<T>`（C++17）或错误码
- 不可恢复错误用异常，配合 RAII 保证资源安全释放
- 禁止空 `catch(...)` 块（吞掉异常）
- 断言用 `assert()` 标注前置条件，配明确注释

## 并发

- 共享可变数据必须用 `std::mutex` 或原子类型保护
- 用 `std::lock_guard` / `std::unique_lock` 管理锁，禁止手动 `unlock()`
- 禁止在持锁期间调用外部回调（死锁风险）
- 优先无锁设计：immutable 数据、thread-local 存储、消息队列

## 格式（clang-format 管辖）

- 缩进 2 空格（Google 风格），禁止 tab
- 行长度上限 100 字符
- 大括号同行：`if (cond) {`，不换行
- 函数实现之间空一行
