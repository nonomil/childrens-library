---
paths:
  - "**/*.py"
  - "**/*.pyi"
---

# 代码风格（Python）

> 依据：PEP 8 + Google Python Style Guide。格式问题交给 Black/Ruff 自动处理，本文件只记录 linter 无法自动修复的结构性规范。

## 命名

| 场景 | 规则 | 示例 |
|------|------|------|
| 函数 / 变量 | `snake_case` | `load_image`, `file_path` |
| 类 | `PascalCase` | `ImageMerger`, `BatchProcessor` |
| 常量（模块级） | `UPPER_SNAKE_CASE` | `MAX_BATCH_SIZE` |
| 私有成员 | 单下划线前缀 | `_cache`, `_validate()` |
| 名称与关键字冲突 | 末尾加单下划线 | `type_`, `class_` |
| 标准库别名 | 只用公认缩写 | `import numpy as np`, `import pandas as pd` |

## 类型标注

- 所有公开函数必须标注参数类型和返回类型，包括 `-> None`
- 路径参数统一用 `Union[Path, str]`，函数体内立即转 `Path`
- 可选参数用 `Optional[T]`（或 `T | None`，Python 3.10+）
- 容器类型用具体泛型：`list[str]`，不用裸 `list`
- 类型仅用于静态检查的导入放在 `if TYPE_CHECKING:` 块内

```python
# 正确
def merge(paths: list[Union[Path, str]], output: Union[Path, str]) -> Path:
    ...

# 错误——缺返回类型，路径类型不明确
def merge(paths, output):
    ...
```

## 导入顺序（isort 标准）

1. `__future__` 导入
2. 标准库
3. 第三方库
4. 本地模块

每组之间空一行，每组内按字母排序。不使用通配符导入（`from x import *`）。

## 文件路径

- 统一用 `pathlib.Path`，禁止 `os.path`
- 不拼接字符串构造路径，用 `/` 操作符：`base_dir / "output" / filename`
- 传给需要字符串的第三方库时才 `str(path)`

## 函数设计

- 单个函数不超过 50 行；超过则拆分
- 参数超过 4 个时改用 dataclass 或 TypedDict 封装
- 默认参数不使用可变对象（`[]`、`{}`），用 `None` 代替
- lambda 只用于单行表达式；超过 60 字符改写为具名函数

## 类设计

- 优先用组合而非继承
- 单参数构造器加 `@classmethod` 工厂方法替代多态构造
- 数据类优先用 `@dataclass`，避免手写 `__init__` + `__repr__` + `__eq__`
- 属性访问控制用 `@property`，不用 `get_x()` / `set_x()` 方法

## 注释与文档

- 公开函数 / 类必须有 docstring，格式遵循 Google Style：
  ```python
  def fetch(table: str, keys: list[str]) -> dict[str, Any]:
      """从数据库获取指定行。

      Args:
          table: 目标表名。
          keys: 行键列表。

      Returns:
          键到行数据的映射字典。

      Raises:
          ConnectionError: 数据库连接失败时。
      """
  ```
- 行内注释解释"为什么"，不解释"是什么"
- 不保留注释掉的死代码，直接删除

## 错误处理

- 捕获具体异常，绝不裸 `except:` 或 `except Exception:` 后静默吞掉
- 捕获后必须：log 错误 **或** re-raise **或** 返回明确错误值，三选一
- `try` 块只包裹可能抛出的最小代码范围
- 资源对象（文件、连接、图像）用 `with` 语句管理，不手动 `close()`

```python
# 正确
try:
    img = Image.open(path)
except FileNotFoundError:
    logger.error("文件不存在: %s", path)
    raise
except UnidentifiedImageError:
    logger.warning("无法识别的图片格式: %s", path)
    return None

# 错误——吞掉异常
try:
    img = Image.open(path)
except Exception:
    pass
```

## 性能与内存

- 大集合遍历用生成器，不一次性构建列表
- 批量处理分批加载，单批处理完后显式释放大对象引用
- 字符串拼接用 `"".join(parts)`，不在循环里用 `+=`
