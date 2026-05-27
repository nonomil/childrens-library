# RTK + Reasonix + Caveman — AI Agent 缓存优化三件套

> 来源: 小红书笔记 + DDGS 搜索  
> 日期: 2026-05-27

---

## 三者简介

| 项目 | 类型 | 核心功能 | GitHub |
|------|------|---------|--------|
| **RTK** | CLI 代理 | 过滤命令输出噪音，减少输入 token（60-90%） | [rtk-ai/rtk](https://github.com/rtk-ai/rtk) |
| **Reasonix** | AI Coding Agent | 利用 DeepSeek prefix caching，99.82% 缓存命中率 | [esengine/deepseek-reasonix](https://github.com/esengine/deepseek-reasonix) |
| **Caveman** | Agent Skill | 用"穴居人"风格压缩输出，减少 65-75% 输出 token | JuliusBrussee/caveman |

---

## 组合效果

```
输入侧: RTK 过滤噪音 → 减少 60-90% 输入 token
        ↓
推理侧: Reasonix 缓存前缀 → 99.82% 缓存命中率
        ↓
输出侧: Caveman 压缩表达 → 减少 65-75% 输出 token
```

**最终结果**: 每次 Agent 请求花费从 ¥0.001 降到 ¥0.00001，月成本从 ¥300 降到 ¥3。

---

## 详细说明

### 1. RTK (Rust Token Killer)

- **原理**: 拦截 Shell 命令输出，过滤掉无关信息（如 git status 中的空白、重复路径）
- **效果**: 平均减少 89% 噪音，3 倍长会话
- **安装**: `cargo install rtk` 或直接用预编译二进制
- **License**: MIT

### 2. Reasonix

- **原理**: 利用 DeepSeek 的 byte-stable prefix caching，相同前缀的推理结果直接复用
- **效果**: 99.82% 缓存命中率（实测单文件场景）
- **关键**: 专为 DeepSeek 设计，其他模型不一定有效
- **注意**: 1 天前才发布，非常新的项目

### 3. Caveman

- **原理**: 系统提示词约束 AI 用极简语言（"穴居人风格"）回复
- **效果**: 减少 65-75% 输出 token
- **代价**: 牺牲部分可读性，适合内部工具/日志场景
- **模式**: lite / full / ultra（压缩程度递增）

---

## 使用建议

| 场景 | 推荐组合 |
|------|---------|
| **个人开发** | RTK + Caveman（省钱为主） |
| **团队项目** | RTK + Reasonix + Caveman（省钱+提速） |
| **生产环境** | 谨慎使用 Caveman（可读性风险） |

---

## 参考链接

- RTK: https://github.com/rtk-ai/rtk
- Reasonix: https://github.com/esengine/deepseek-reasonix
- Caveman: https://github.com/JuliusBrussee/caveman

---

*调研完成于 2026-05-27*
