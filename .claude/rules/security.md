---
paths:
  - "**/*.py"
---

# 安全规范（Python）

> 依据：OWASP Python 安全指南 + Bandit 规则集。

## 输入验证

- 所有外部输入（文件路径、用户参数、环境变量）在使用前必须验证
- 路径存在性校验：`Path.is_file()` / `Path.is_dir()`；失败时抛出明确异常，不静默跳过
- 文件类型校验：在项目允许列表内做扩展名 + MIME 类型双重校验，不只检查扩展名
- 整数 / 数值输入检查范围边界，防止意外的大数导致资源耗尽

## 路径安全

- 禁止拼接用户输入构造路径：用 `Path(user_input).resolve()` 防止目录穿越
- 校验 resolve 后的路径在允许的根目录内：
  ```python
  resolved = Path(user_input).resolve()
  if not resolved.is_relative_to(ALLOWED_ROOT):
      raise ValueError(f"路径越界: {resolved}")
  ```
- 输出路径不能指向系统目录（`/etc`、`/sys`、`C:\Windows` 等）

## 代码执行安全

- 禁止 `eval()` / `exec()` 执行动态代码
- 禁止 `subprocess` 使用 `shell=True`；必须执行外部命令时用参数列表形式：
  ```python
  # 正确
  subprocess.run(["convert", str(input_path), str(output_path)], check=True)
  # 错误
  subprocess.run(f"convert {input_path} {output_path}", shell=True)
  ```
- 禁止 `pickle.loads()` 处理不可信来源数据（可用 `json` 替代）

## Secrets 管理

- 禁止在代码中硬编码密钥、密码、token（包括测试代码）
- 从环境变量或专用 secrets 管理工具读取，不从配置文件读取明文
- 日志中禁止输出敏感字段；如需调试，用占位符替代实际值

## 依赖安全

- 固定依赖版本（`requirements.txt` 锁定到 patch 版本）
- CI 中集成 `pip-audit` 或 `safety` 扫描已知漏洞
- 不引入仅用于开发的库到生产依赖

## 资源安全

- 文件句柄、网络连接、数据库连接用 `with` 语句管理，确保释放
- 大文件分块读取，不一次 `read()` 全部内容
- 用户上传的图片等文件处理完后显式释放：`image.close()` 或 `with Image.open() as img:`
- 不联网上传任何用户文件或处理结果（除非有明确业务需求且经过审查）

## 日志安全

- 不在日志中记录：密码、token、完整信用卡号、身份证号
- 记录足够的操作上下文用于审计，但避免过度记录用户私有数据
- 生产环境日志级别设为 `WARNING` 以上，不留 `DEBUG` 日志
