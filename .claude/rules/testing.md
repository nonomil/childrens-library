---
paths:
  - "tests/**/*.py"
  - "test_*.py"
  - "*_test.py"
---

# 测试规范（Python）

> 框架：pytest。覆盖率工具：pytest-cov。

## 运行命令

```bash
# 全量测试 + 覆盖率报告
python -m pytest tests/ -v --cov=src --cov-report=term-missing

# 只跑某个模块
python -m pytest tests/test_merger.py -v

# 只跑某个测试函数
python -m pytest tests/test_merger.py::test_merge_two_images_returns_correct_size -v

# 失败后立即停止
python -m pytest tests/ -x
```

## 文件与函数命名

- 测试文件：`test_<模块名>.py`，放在 `tests/` 目录，镜像 `src/` 结构
- 测试函数：`test_<场景>_<预期结果>`，例如：
  - `test_merge_empty_list_raises_value_error`
  - `test_scan_directory_returns_sorted_files`
  - `test_open_unsupported_format_returns_none`
- 每个测试函数只测一个行为，测试体通常不超过 20 行

## 测试结构（AAA 模式）

每个测试遵循 Arrange → Act → Assert 三段式，段间空一行：

```python
def test_merge_two_images_returns_correct_width(tmp_path):
    # Arrange
    img_a = create_test_image(tmp_path / "a.png", width=100, height=200)
    img_b = create_test_image(tmp_path / "b.png", width=150, height=200)

    # Act
    result = merge_horizontal([img_a, img_b])

    # Assert
    assert result.width == 250
    assert result.height == 200
```

## Fixtures

- 共享的测试数据 / 资源用 `@pytest.fixture` 管理，不在测试函数里手动 setup/teardown
- 临时文件用 pytest 内置的 `tmp_path` fixture，不手动创建和删除
- 作用域按需选择：`scope="function"`（默认）/ `"module"` / `"session"`
- 昂贵的资源（数据库连接、大文件）用 `scope="session"` 避免重复初始化

```python
@pytest.fixture
def sample_image(tmp_path) -> Path:
    """创建 100x100 的测试用 PNG 文件。"""
    path = tmp_path / "sample.png"
    Image.new("RGB", (100, 100), color=(128, 0, 0)).save(path)
    return path
```

## Mock 策略

- 只 mock 外部依赖（文件系统 IO、网络、时钟、数据库），不 mock 被测单元内部逻辑
- 用 `unittest.mock.patch` 或 `pytest-mock` 的 `mocker` fixture
- mock 后验证调用次数和参数，不只验证返回值：
  ```python
  mock_open.assert_called_once_with(expected_path, "rb")
  ```

## 覆盖率要求

- 新增代码的行覆盖率不低于 **80%**
- 核心业务逻辑（merger、file_manager 等）不低于 **90%**
- 覆盖率检查集成到 CI，低于阈值时构建失败：
  ```bash
  python -m pytest --cov=src --cov-fail-under=80
  ```

## 测试原则

- 每个测试独立，不依赖其他测试的执行顺序或共享状态
- 覆盖四类场景：正常路径、边界值、异常/错误路径、空输入
- 异常测试用 `pytest.raises()`，不用 `try/except`：
  ```python
  def test_open_nonexistent_file_raises_file_not_found(tmp_path):
      with pytest.raises(FileNotFoundError, match="no_such_file.png"):
          load_image(tmp_path / "no_such_file.png")
  ```
- 参数化测试用 `@pytest.mark.parametrize` 减少重复：
  ```python
  @pytest.mark.parametrize("fmt", [".txt", ".pdf", ".exe", ".zip"])
  def test_unsupported_format_raises_error(tmp_path, fmt):
      path = tmp_path / f"file{fmt}"
      path.touch()
      with pytest.raises(ValueError, match="不支持的文件格式"):
          load_image(path)
  ```
- 测试函数不包含业务逻辑；如果需要辅助计算，提取为测试辅助函数

## 具体业务场景见各项目 project.md
