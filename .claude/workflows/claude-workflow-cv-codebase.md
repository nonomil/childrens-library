# claude-workflow-cv-codebase｜机器视觉 C++/Python 代码库工作流

> 本文档中的所有规则遵循 `claude-workflow-constants.md` 中的全局约束
> 适用：C++ + Python 混合机器视觉项目，含相机驱动、算法核心、pybind11 绑定层、Python 推理/调度
> 目标：三阶段工具链（Cartographer → code-review-graph → Graphify）落地，覆盖接手期、日常开发、深度分析
> 核心约束：pybind11 跨语言调用链无法被静态 AST 追踪，必须由 Cartographer 语义分析覆盖
> 推荐技能：`largebase-structured-scan`（见 `.claude/skills/largebase-structured-scan/SKILL.md`）

---

## 0. 前置：项目特征识别

进入本流程前，先确认项目符合以下特征（满足 ≥ 2 条即适用）：

| 特征 | 识别方式 |
|------|---------|
| C++ 负责底层采集/算法 | 存在 `.cpp/.h` 且含 `cv::`、`pcl::`、`cuda` 关键词 |
| Python 负责上层推理/调度 | 存在 `.py` 且含 `import torch`、`onnxruntime`、`tensorrt` |
| 存在跨语言绑定层 | 存在 `pybind11`、`PYBIND11_MODULE`、`Cython`、`.pyi` stub |
| 包含算法论文/设计文档 | `docs/` 下有 PDF 或含算法描述的 Markdown |
| 含 CUDA/TensorRT 加速 | 存在 `.cu` 文件或 `trt.Builder`、`<<<` 调用 |

**C++ + pybind11 的核心盲区**（贯穿全流程）：

`PYBIND11_MODULE` 是动态注册宏，静态 AST 无法追踪 Python 侧 `import your_module` 最终调用了哪个 C++ 函数。code-review-graph 和 Graphify 的跨语言调用链均不可信，**跨语言边界的调用关系必须由 Cartographer 子代理语义分析覆盖**，不可用图谱节点替代。

---

## 1. 触发与跳过

满足任意一条即进入本流程：

- 首次接手该机器视觉项目（`docs/CODEBASE_MAP.md` 不存在或 > 7 天）
- 需要理解 C++ 与 Python 的职责边界或 pybind11 接口列表
- 涉及 pipeline 流向变更（采集 → 预处理 → 推理 → 后处理）
- 更换推理后端（如 ONNX → TensorRT，或升级模型版本）
- 跨模块重构（≥ 3 个模块）
- 用户关键词：重构、迁移、pybind、pipeline、跨语言、接口变更、算法替换

满足任意一条可跳过：

- 仅改动单个 `.py` 脚本且不涉及 binding 层，diff 预估 < 80 行
- 用户明确要求“不要扫描，直接改”
- 当前会话已有 ≤ 7 天内的 `docs/CODEBASE_MAP.md` + `scan.db`

---

## 2. 三阶段工具链

### 工具定位总览

| 工具 | 阶段 | 触发时机 | 产出 | 跨语言追踪 |
|------|------|---------|------|-----------|
| Cartographer | 接手期（一次性） | 首次接手 / Map 过期 | `CODEBASE_MAP.md` | ✅ 语义分析，可追踪 pybind11 |
| code-review-graph | 日常开发（持续） | 安装后常驻 MCP | SQLite 图 + MCP 服务 | ⚠️ 单语言内可信，跨语言不可信 |
| Graphify | 深度分析（按需） | 重构前 / 架构评审 / 耦合异常 | `GRAPH_REPORT.md` + `graph.html` | ⚠️ 同上 |

### 阶段 1：接手期 — Cartographer

**目标**：生成面向人类的架构综述，重点覆盖跨语言边界。

**执行命令**（Claude Code 环境）：

```bash
/plugin marketplace add kingbootoshi/cartographer
/plugin install cartographer@kingbootoshi-cartographer
```

触发后，追加以下 prompt 引导子代理聚焦机器视觉关键维度：

```text
请在生成 CODEBASE_MAP.md 时，重点描述以下内容：
1. C++ 与 Python 的职责边界（哪些逻辑在 C++，哪些在 Python）
2. pybind11 / Cython 绑定层暴露的接口列表（函数名、参数类型、所在文件）
3. 图像处理主 pipeline 的完整数据流：
   - 数据从哪里进入（相机 SDK / 文件 / 网络）
   - 经过哪些处理节点（预处理 / 推理 / 后处理）
   - 最终输出什么（检测框 / 分割掩码 / 关键点 / 控制信号）
4. 推理后端位置（TensorRT / ONNXRuntime / LibTorch）及模型文件对应关系
5. CUDA / GPU 加速代码的位置和调用路径
6. 历史设计注释中的 "why"（为什么用 TensorRT 而不是直接 ONNX 等决策）
```

**产物检查**（生成后必查）：

```markdown
- [ ] CODEBASE_MAP.md 包含 pybind11 接口列表（至少列出函数名和所在 .cpp 文件）
- [ ] 包含 pipeline 数据流描述（从采集到输出的完整路径）
- [ ] 包含推理后端说明（模型文件 ↔ 代码对应关系）
- [ ] Generated at 时间戳已记录
```

**回退策略**：Cartographer 不可用时，执行 `largebase-structured-scan extract` 生成本地 `CODEBASE_MAP.md`（零 AI Token），但跨语言调用链部分需人工补充。

---

### 阶段 2：日常开发 — code-review-graph（常驻 MCP）

**目标**：为 Claude 提供持续的代码结构查询底座，改一个文件 2 秒内完成增量更新。

**安装**：

```bash
pip install code-review-graph
code-review-graph install
code-review-graph build
code-review-graph watch
```

**`.code-review-graphignore` 配置**（必须添加，排除非业务文件）：

```text
build/
cmake-build-*/
third_party/
vendor/
*.pb
*_pb2.py
*_pb2_grpc.py
models/
weights/
*.onnx
*.engine
*.trt
*.pt
*.pth
__pycache__/
.venv/
node_modules/
```

**机器视觉场景的核心用法**：

```text
"修改 preprocess/image_normalize.cpp 的 NormalizeImage() 函数，
 会影响哪些 Python 推理脚本？"
→ code-review-graph 返回 blast radius，Claude 只读相关文件，不扫全库
```

**已知局限**（必须了解）：

- C++ / Python 单语言内调用链：可信
- 跨 pybind11 边界的调用链：**不可信**，需查阅 Cartographer 产出的 `CODEBASE_MAP.md`
- flow detection 对 C++ 框架模式识别有限，复杂 pipeline 流向仍以 `CODEBASE_MAP.md` 为准

---

### 阶段 3：深度分析 — Graphify（按需）

**触发时机**（满足任意一条）：

- 重构前需要识别耦合热点
- 新人接手，需要可视化模块社区结构
- 架构评审，需要展示模块依赖关系
- 发现某个模块改动影响范围异常大，怀疑耦合问题

**执行命令**（分模块扫，不要全量）：

```bash
python .claude/scripts/graphify_codebase_scan.py \
  --scope src/capture src/preprocess src/inference python/pipeline docs/papers \
  --generate-viewer
```

输出自动到 `docs/代码库-知识图谱/{项目名}-LLM图谱/`，无需手动指定 `--output-dir`。

**为什么不全量扫**：机器视觉项目历史代码多，全量扫出的 `GRAPH_REPORT.md` 极易超过 100KB，超出 LLM 上下文。按 pipeline 层级分模块扫，社区结构会自然对齐业务分层。

**论文和设计文档的价值**（机器视觉特有）：

把算法论文 PDF（YOLO、ViT、SAM 等）和设计文档一起放入 `docs/papers/`，Graphify 的 LLM 语义提取会将代码节点与论文概念关联。效果：当 AI 被问到”为什么这里用这个 anchor size”时，能追溯到论文中的实验依据。

**产物读取顺序**：

```bash
cat docs/代码库-知识图谱/{项目名}-LLM图谱/scan-summary.json
```

然后：

- 读 `docs/代码库-知识图谱/{项目名}-LLM图谱/GRAPH_REPORT.md` 找 god nodes 和 surprising connections
- 双击 `docs/代码库-知识图谱/{项目名}-LLM图谱/打开图谱查看器.bat` 在浏览器看社区分布

**预期社区结构**（健康的机器视觉项目应呈现）：

| 社区 | 典型内容 |
|------|---------|
| 采集层 | 相机 SDK 封装、帧缓冲、时间戳同步 |
| 预处理层 | resize/normalize/crop、色彩空间转换 |
| 推理层 | 模型加载、前向推理、TensorRT engine 管理 |
| 后处理层 | NMS、关键点解码、坐标变换 |
| Python 接口层 | pybind11 binding、pipeline 调度脚本 |

若实际社区与上述分层严重不符（如预处理和推理混为一个社区），说明存在层间耦合，需优先重构。

---

## 3. 扫描包输出（结合 largebase-structured-scan）

**扫描包目录**：`docs/scan/YYYY-MM-DD-cv-[topic]/`

在标准 `00-06` 扫描包基础上，机器视觉项目必须额外输出：

### 必须补充的 CV 专项内容

**`01-architecture.md` 必须包含**：

```markdown
## C++/Python 分层职责表
| 层级 | 语言 | 目录 | 职责 |
|------|------|------|------|
| 采集层 | C++ | src/capture/ | 相机驱动、帧缓冲 |
| 算法核心 | C++ | src/preprocess/ src/inference/ | 图像处理、推理 |
| 绑定层 | C++/Python | src/bindings/ | pybind11 模块定义 |
| 调度层 | Python | python/pipeline/ | 业务流程编排 |
| 推理接口 | Python | python/inference/ | 模型管理、后处理 |

## pybind11 暴露接口清单
| 函数名 | 所在 .cpp 文件 | 参数类型 | Python 调用方式 |
|--------|--------------|---------|----------------|
| ... | ... | ... | ... |
```

**`02-dataflow.md` 必须包含**：

```markdown
## 图像处理主 Pipeline
输入源（相机/文件/网络）
  → [C++] 采集与解码（src/capture/）
  → [C++] 预处理（resize/normalize，src/preprocess/）
  → [pybind11 边界]
  → [Python] 推理调度（python/pipeline/）
  → [Python] 模型前向（python/inference/，TRT/ONNX）
  → [Python] 后处理（NMS/decode，python/postprocess/）
  → 输出（检测框/掩码/控制信号）

## 推理后端对应关系
| 模型文件 | 后端 | 加载代码 | 备注 |
|---------|------|---------|------|
| models/det.engine | TensorRT | python/inference/trt_runner.py | 需 TRT 8.x |
| models/seg.onnx | ONNXRuntime | python/inference/ort_runner.py | CPU fallback |
```

**`05-impact-matrix.md` 机器视觉专项规则**：

```markdown
| 修改点 | 直接影响 | 间接影响 | pybind11 边界 | 验证点 |
|--------|---------|---------|--------------|-------|
| NormalizeImage() 参数变更 | preprocess 模块 | Python pipeline 调用方 | ✅ 穿越边界 | binding 函数签名 + Python 调用测试 |
```

---

## 4. 执行流程（强制顺序）

### Step 0：工具链状态检查

```bash
python .claude/scripts/cartographer_smoke.py --project-dir .
code-review-graph status
graphify --version
```

根据检查结果：

| 状态 | 行动 |
|------|------|
| `CODEBASE_MAP.md` 存在且 ≤ 7 天 | 跳过阶段 1，直接进入 Step 1 |
| `CODEBASE_MAP.md` 不存在或已过期 | 先执行阶段 1（Cartographer） |
| `code-review-graph` 未安装 | 执行阶段 2 安装步骤 |
| `graphify` 未安装 | 仅在触发阶段 3 时安装 |

### Step 1：Cartographer 建立架构基线（首次接手必做）

详见阶段 1。产出检查通过后，将 `CODEBASE_MAP.md` 加入后续扫描的 `--refs` 参数。

### Step 2：API 成本提示（触发条件同 `claude-workflow-largebase.md` §4 Step 1）

机器视觉项目的额外触发条件：

| 指标 | 阈值 |
|------|------|
| `.cpp/.h` 文件数 | > 200 |
| CUDA 文件（`.cu`）数 | > 20 |
| 论文 PDF 数 | > 10 |

### Step 3：largebase-structured-scan 扫描

```bash
python .claude/skills/largebase-structured-scan/scan.py scan \
  --mode M2 \
  --scope src python docs/papers \
  --topic cv-pipeline \
  --refs docs/CODEBASE_MAP.md

python .claude/skills/largebase-structured-scan/scan.py extract \
  --scope src python docs/papers \
  --topic cv-pipeline
```

**CV 专项约束**：

- `--scope` 必须显式列出 `src`（C++ 源码）和 `python`（Python 源码）
- 禁止把 `models/`、`weights/` 纳入 scope
- 论文 PDF 目录（如 `docs/papers/`）可以纳入 scope，Graphify 会处理，largebase-scan 会跳过 PDF

### Step 4：按需触发 Graphify 深度分析

详见阶段 3。

### Step 5：结果路由

| 扫描结论 | 路由 |
|---------|------|
| 单模块改动，影响链清晰 | `claude-workflow-complex.md`（跳过其 Phase 0） |
| 多模块并行任务 | `claude-workflow-parallel.md` |
| 跨语言 bug，调用链不清晰 | `claude-workflow-debug.md` + 手动补充 pybind11 调用链 |
| 大规模重构（如替换推理后端） | `claude-workflow-parallel.md` + Graphify 社区分析前置 |

---

## 5. 反模式

| 错误做法 | 后果 | 正确做法 |
|---------|------|---------|
| 用 Graphify 图谱替代 Cartographer 分析跨语言调用链 | pybind11 边界节点不可信，产出错误的影响范围 | 跨语言调用链只信 `CODEBASE_MAP.md` |
| 全量扫描整个仓库（含 `models/`、`build/`） | `GRAPH_REPORT.md` 超过 100KB，超出上下文 | 分模块扫，排除 build 产物和模型权重 |
| 首次接手跳过 Cartographer 直接用 code-review-graph | 拿到图节点但不理解 pipeline 语义，改错地方 | 必须先有 `CODEBASE_MAP.md` 建立心智模型 |
| 论文 PDF 不投入 Graphify | 代码节点缺少算法背景，AI 无法解释设计决策 | 把算法论文和设计文档一起投入 `docs/papers/` |
| 改了 pybind11 binding 函数签名后只跑 Python 测试 | C++ 侧编译通过但 Python 运行时崩溃 | binding 变更必须同时验证 C++ 侧和 Python 调用方 |
| code-review-graph 未配置 ignore 文件 | 扫入 `.onnx`、`.engine` 等二进制，图结构混乱 | 首次安装后立即配置 `.code-review-graphignore` |

---

## 6. 工具链维护规则

**`CODEBASE_MAP.md` 刷新时机**：

| 触发事件 | 刷新方式 |
|---------|---------|
| pybind11 接口新增或变更 | 重新运行 Cartographer |
| pipeline 主流程变更（新增/删除处理节点） | 重新运行 Cartographer |
| 超过 30 天未刷新 | 重新运行 Cartographer |
| 推理后端替换 | 重新运行 Cartographer + Graphify |

**code-review-graph 增量更新**：

```bash
code-review-graph status
```

应看到近期更新时间以及 `Watch: active` 或 git hook 路径。

**Graphify 重建时机**：

仅在以下情况重建：重构前、架构评审前、新人 onboarding。日常开发不需要重建，code-review-graph 已覆盖增量需求。

---

## 7. 与 largebase-structured-scan Skill 的衔接

本工作流是 `largebase-structured-scan` 的领域特化版本，不替代通用流程，而是在以下节点注入 CV 专项规则：

| largebase-scan 节点 | CV 专项补充 |
|--------------------|-----------|
| Step 0：Cartographer 检测 | 检查 `CODEBASE_MAP.md` 是否包含 pybind11 接口列表 |
| Step 1.5：本地 extract | scope 必须同时包含 `src`（C++）和 `python` 两个目录 |
| `01-architecture.md` 生成 | 必须补充 C++/Python 分层职责表和 pybind11 接口清单 |
| `02-dataflow.md` 生成 | 必须补充图像处理主 pipeline 数据流和推理后端对应关系 |
| `05-impact-matrix.md` 生成 | 跨语言改动必须标注“pybind11 边界穿越”风险 |
| Step 6：路由 | 跨语言 bug 路由到 `claude-workflow-debug.md` + 手动补充调用链 |
