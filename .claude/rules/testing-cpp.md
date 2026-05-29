---
paths:
  - "tests/**/*.cpp"
  - "tests/**/*.cc"
  - "test_*.cpp"
---

# 测试规范（C++）

> 框架：Google Test（gtest）+ Google Mock（gmock）。覆盖率：gcov / llvm-cov。

## 运行命令

```bash
# 构建并运行全量测试（CMake）
cmake --build build && cd build && ctest -V

# 只跑某个测试二进制
./build/tests/test_merger --gtest_filter="*"

# 只跑某个 test suite
./build/tests/test_merger --gtest_filter="MergerTest.*"

# 只跑某个测试用例
./build/tests/test_merger --gtest_filter="MergerTest.TwoImages_ReturnsCorrectWidth"

# Windows (MSVC)
cmake --build build --config Release
cd build && ctest -V -C Release
```

## 命名规范

- 文件名：`test_<模块名>.cpp`
- Test Suite：`<被测类名>Test`，例如 `MergerTest`、`FileManagerTest`
- 测试用例：`<场景>_<预期结果>`，例如：
  - `TwoImages_ReturnsCorrectWidth`
  - `EmptyDirectory_ReturnsEmptyList`
  - `UnsupportedFormat_ThrowsInvalidArgument`

## 测试结构（AAA 模式）

```cpp
TEST_F(MergerTest, TwoImages_ReturnsCorrectWidth) {
    // Arrange
    auto img_a = CreateTestImage(100, 200);
    auto img_b = CreateTestImage(150, 200);

    // Act
    auto result = merger_.MergeHorizontal({img_a, img_b});

    // Assert
    EXPECT_EQ(result.width(), 250);
    EXPECT_EQ(result.height(), 200);
}
```

## Fixtures

- 共享资源用 `TEST_F` + fixture 类管理，不在测试函数里手动 setup/teardown
- 复杂初始化放 `SetUp()`，复杂清理放 `TearDown()`
- 跨多个 suite 复用的资源用 `SetUpTestSuite()` / `TearDownTestSuite()`（suite 级别）

```cpp
class MergerTest : public ::testing::Test {
 protected:
  void SetUp() override {
    config_.output_dir = temp_dir_.path();
    merger_ = std::make_unique<ImageMerger>(config_);
  }

  TempDirectory temp_dir_;
  MergerConfig config_;
  std::unique_ptr<ImageMerger> merger_;
};
```

## 断言选择

| 场景 | 用法 |
|------|------|
| 后续逻辑依赖此结果 | `ASSERT_*`（失败立即终止当前测试） |
| 收集所有失败信息 | `EXPECT_*`（失败继续执行，推荐默认） |
| 浮点数比较 | `EXPECT_NEAR(a, b, 1e-6)` |
| 异常 | `EXPECT_THROW(expr, ExceptionType)` |
| 无异常 | `EXPECT_NO_THROW(expr)` |
| 字符串包含 | `EXPECT_THAT(s, ::testing::HasSubstr("foo"))` |

## Mock 策略

- 只 mock 外部依赖（IO、网络、时钟、数据库）；不 mock 被测单元内部实现
- 用纯虚接口隔离依赖，通过构造函数注入 mock：
  ```cpp
  class IFileSystem {
   public:
    virtual ~IFileSystem() = default;
    virtual bool Exists(const std::filesystem::path& p) const = 0;
    virtual std::vector<uint8_t> Read(const std::filesystem::path& p) const = 0;
  };

  class MockFileSystem : public IFileSystem {
   public:
    MOCK_METHOD(bool, Exists, (const std::filesystem::path&), (const, override));
    MOCK_METHOD(std::vector<uint8_t>, Read, (const std::filesystem::path&), (const, override));
  };
  ```
- 用 `EXPECT_CALL` 验证调用次数和参数，不只验证返回值

## 参数化测试

减少重复用 `INSTANTIATE_TEST_SUITE_P`：

```cpp
class UnsupportedFormatTest : public ::testing::TestWithParam<std::string> {};

TEST_P(UnsupportedFormatTest, Throws_InvalidArgument) {
    EXPECT_THROW(LoadImage("file" + GetParam()), std::invalid_argument);
}

INSTANTIATE_TEST_SUITE_P(
    Formats, UnsupportedFormatTest,
    ::testing::Values(".txt", ".pdf", ".exe", ".zip"));
```

## 覆盖率要求

- 新增代码行覆盖率不低于 **80%**
- 核心业务逻辑不低于 **90%**
- CMake 中集成覆盖率：
  ```cmake
  if(ENABLE_COVERAGE)
    target_compile_options(${TARGET} PRIVATE --coverage)
    target_link_options(${TARGET} PRIVATE --coverage)
  endif()
  ```

## 测试原则

- 每个测试独立，不依赖全局状态或其他测试的执行顺序
- 覆盖四类场景：正常路径、边界值、异常/错误路径、空输入
- 测试代码与生产代码同等对待：可读性、命名、不重复
- 禁止在测试里用 `sleep()` 等待异步结果；改用条件变量或 mock 时钟

## 具体业务场景见各项目 project.md
