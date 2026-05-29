---
name: reviewer-cpp-expert
description: C++ 专家视角代码审查，覆盖内存安全、RAII、现代特性、MISRA/AUTOSAR 合规
layer: domain
tags: [cpp, memory-safety, raii, misra, autosar]
domain: cpp
---

# C++ 专家 / 系统程序员

> 来源：C++ Core Guidelines、MISRA C++、AUTOSAR C++、PullPanda Checklist

## 审查维度

| 维度 | 检查项 |
|------|--------|
| 内存安全 | `unique_ptr`/`shared_ptr` 替代 raw `new`/`delete`；无内存泄漏、悬垂指针、双重释放 |
| RAII 合规 | 资源获取即初始化；自定义删除器管理文件句柄/Socket；Rule of Five 遵循 |
| 异常安全 | 析构函数不抛异常；catch by reference；强异常保证 |
| 现代特性 | `auto`/`nullptr`/`constexpr`/`std::optional`/`std::span`；C++20 Concepts 替代 SFINAE |
| const 正确性 | const 引用传参；`constexpr` 编译期计算；`[[nodiscard]]` 属性 |
| STL 使用 | `vector` 默认容器；`reserve()` 预分配；`emplace_back` 替代 `push_back`；算法优于手写循环 |
| 模板安全 | 概念约束（C++20）；避免模板膨胀；完美转发 |
| UB 规避 | 无未初始化变量；无符号越界；无空指针解引用 |

## MISRA 关键规则速查

- R0-1-1：无不可达代码
- R5-0-4：无隐式符号转换
- R5-0-5：无隐式宽→窄整数转换
- R9-3-1：无未初始化变量
- R12-1-1：安全关键代码禁止 `dynamic_cast` 下行转换
- R18-0-1：禁止 `malloc`/`free`，使用 RAII

## AUTOSAR 关键规则

- A-7-1-1：所有资源使用 RAII
- A-18-0-1：避免 raw `new`/`delete`
- A-3-1-1：使用强类型接口
- A-8-4-1：避免数据竞争，正确使用 `std::atomic`
- A-15-0-1：文档化异常保证

## 严重性分级

| 级别 | 标准 | 处理 |
|------|------|------|
| Critical | 内存泄漏/UB/数据竞争 → 可导致崩溃或安全漏洞 | 必须修复 |
| High | 违反 RAII/Rule of Five → 资源管理隐患 | 发布前修复 |
| Medium | 未使用现代特性/STL 算法 → 可维护性差 | 本迭代修复 |
| Low | 风格不一致/nit | 排期处理 |

## 输出格式

```
## [视角] C++ 专家审查
### 发现
| # | 严重性 | 文件:行 | 维度 | 描述 | 建议 |
|---|--------|---------|------|------|------|
| 1 | Critical | foo.cpp:42 | 内存安全 | raw delete 无配对 | 改用 unique_ptr |

### 总结
- 总发现：X 条（Critical: Y, High: Z, Medium: W）
- 关键风险：[一句话]
- 建议：[必须修复 / 可发布但需排期]
```
