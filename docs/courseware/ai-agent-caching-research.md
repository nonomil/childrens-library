# AI Agent 缓存命中率优化方案

> 目标：将缓存命中率提升至 99%，大幅降低 Token 消耗成本  
> 来源：基于小红书笔记 "怎么才能省token" 的调研方案  
> 日期：2026-05-27

---

## 核心思路

**"三层缓存 + 语义匹配"**——将重复/相似的 Agent 请求拦截在缓存层，避免重复调用 LLM。

| 层级 | 名称 | 作用 | 命中率 |
|------|------|------|--------|
| **L1** | **Exact Match**（精确匹配） | 完全相同的 Prompt → 直接返回缓存 | ~60% |
| **L2** | **Semantic Cache**（语义缓存） | 相似语义的 Prompt → 复用结果 | ~35% |
| **L3** | **Reasoning Cache**（推理缓存） | 相同推理路径 → 跳过推理直接出结果 | ~4% |
| **兜底** | LLM 调用 | 真正需要新推理的请求 | ~1% |

**总命中率：99%**

---

## 架构设计

```
┌─────────────────────────────────────────────────────┐
│                    User Request                      │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  L1: Exact Match Cache                              │
│  - Hash(prompt) → 查 Redis/Memory                   │
│  - 命中：直接返回结果                                 │
│  - 未命中 → 下一层                                   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  L2: Semantic Cache                                  │
│  - Embedding(prompt) → 向量检索(FAISS/Pinecone)    │
│  - 相似度 > 阈值(如0.92) → 返回缓存结果               │
│  - 未命中 → 下一层                                   │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  L3: Reasoning Cache                                 │
│  - 提取推理路径 signature                           │
│  - 相同推理模式 → 复用推理结果                        │
│  - 未命中 → 调用 LLM                                │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│  LLM API Call                                       │
│  - DeepSeek / OpenAI / Anthropic                   │
│  - 返回结果                                         │
│  - 写入三层缓存                                      │
└─────────────────────────────────────────────────────┘
```

---

## 关键技术点

### 1. L1: Exact Match（精确匹配）

```python
import hashlib
import json
from functools import lru_cache

class ExactCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        
    def _hash(self, prompt: str, model: str, params: dict) -> str:
        """生成唯一缓存键"""
        key_data = json.dumps({"prompt": prompt, "model": model, "params": params}, sort_keys=True)
        return hashlib.sha256(key_data.encode()).hexdigest()[:16]
    
    def get(self, prompt, model, params):
        key = self._hash(prompt, model, params)
        return self.redis.get(f"exact:{key}")
    
    def set(self, prompt, model, params, result):
        key = self._hash(prompt, model, params)
        self.redis.setex(f"exact:{key}", 3600, result)  # TTL 1小时
```

**优化点**：
- Prompt 标准化（去除多余空格、统一换行符）
- 参数排序后生成 Hash
- TTL 根据业务场景调整（高频请求可延长）

---

### 2. L2: Semantic Cache（语义缓存）

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SemanticCache:
    def __init__(self, model_name='all-MiniLM-L6-v2', threshold=0.92):
        self.encoder = SentenceTransformer(model_name)
        self.threshold = threshold
        self.dimension = self.encoder.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dimension)  # 内积 = cosine similarity
        self.prompts = []  # 存储原始prompt，用于反向查找
        self.results = {}  # prompt_hash -> result
        
    def encode(self, text: str) -> np.ndarray:
        return self.encoder.encode([text], normalize_embeddings=True)
    
    def get(self, prompt: str):
        if len(self.prompts) == 0:
            return None
            
        query_vec = self.encode(prompt)
        scores, indices = self.index.search(query_vec, k=1)
        
        if scores[0][0] > self.threshold:
            matched_prompt = self.prompts[indices[0][0]]
            return self.results.get(matched_prompt)
        return None
    
    def set(self, prompt: str, result: str):
        vec = self.encode(prompt)
        self.index.add(vec)
        self.prompts.append(prompt)
        self.results[prompt] = result
```

**优化点**：
- 使用 FAISS 实现高效的向量检索（百万级毫秒级）
- Embedding 模型选择轻量级的（all-MiniLM-L6-v2，仅 80MB）
- 阈值可调（0.92 适合大多数场景，高精确度场景可调至 0.95+）
- 定期清理低频缓存，控制内存

---

### 3. L3: Reasoning Cache（推理缓存）

```python
class ReasoningCache:
    """
    缓存推理路径，而非最终结果。
    适用于：多步骤推理、Agent 工具调用链
    """
    
    def __init__(self):
        self.reasoning_index = {}  # reasoning_signature -> result
        
    def extract_signature(self, reasoning_steps: list) -> str:
        """
        提取推理路径的签名
        示例：['search_web', 'extract_content', 'summarize']
        """
        return "->".join(reasoning_steps)
    
    def get(self, reasoning_steps: list):
        sig = self.extract_signature(reasoning_steps)
        return self.reasoning_index.get(sig)
    
    def set(self, reasoning_steps: list, result: str):
        sig = self.extract_signature(reasoning_steps)
        self.reasoning_index[sig] = result
```

**适用场景**：
- Agent 执行固定流程（如：搜索 → 提取 → 总结）
- 工具调用顺序固定的任务
- 推理链可抽象为模板的场景

---

## 成本测算

假设场景：每天 10,000 次 Agent 请求

| 指标 | 无缓存 | 有缓存（99%命中率） |
|------|--------|-------------------|
| LLM 调用次数 | 10,000 | 100 |
| 单次成本（DeepSeek V3） | ¥0.001 | ¥0.001 |
| 日成本 | ¥10.00 | ¥0.10 |
| **月成本** | **¥300** | **¥3** |
| **年成本** | **¥3,650** | **¥36.5** |

**节省：99.9%**（从 ¥3,650 降至 ¥36.5）

---

## 实施方案

### 方案 A：轻量级（适合个人/小团队）

**技术栈**：Python + Redis + FAISS

```bash
pip install redis sentence-transformers faiss-cpu
```

```python
# 核心代码
class AgentCache:
    def __init__(self):
        self.exact = ExactCache(redis_client)
        self.semantic = SemanticCache()
        self.reasoning = ReasoningCache()
    
    def query(self, prompt, model="deepseek-chat"):
        # L1: Exact Match
        if result := self.exact.get(prompt, model, {}):
            return {"result": result, "cache": "L1-exact"}
        
        # L2: Semantic Cache
        if result := self.semantic.get(prompt):
            return {"result": result, "cache": "L2-semantic"}
        
        # L3: Reasoning Cache (for agent flows)
        # ...
        
        # Fallback: LLM
        result = call_llm(prompt, model)
        
        # Write to caches
        self.exact.set(prompt, model, {}, result)
        self.semantic.set(prompt, result)
        
        return {"result": result, "cache": "LLM"}
```

**部署**：单机 Docker，内存占用 < 2GB

---

### 方案 B：企业级（适合高并发）

**技术栈**：
- L1: Redis Cluster
- L2: Pinecone / Milvus（向量数据库）
- L3: 自定义推理缓存服务
- 代理层：Nginx / Envoy（缓存拦截）

```yaml
# docker-compose.yml
version: '3'
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  faiss:
    image: faiss:latest
    volumes:
      - ./index:/data
  
  agent-cache:
    build: .
    environment:
      - REDIS_URL=redis://redis:6379
      - FAISS_HOST=faiss:50051
    ports:
      - "8080:8080"
```

---

## 注意事项

1. **缓存失效**：LLM 模型更新后，缓存需清空或重新验证
2. **隐私安全**：缓存中不要存储敏感信息（PII、密码等）
3. **TTL 策略**：根据业务场景设置合理的过期时间
4. **监控指标**：缓存命中率、平均延迟、内存占用
5. **冷热分离**：高频缓存放内存，低频放磁盘/冷存储

---

## 参考资源

- FAISS: https://github.com/facebookresearch/faiss
- Sentence-Transformers: https://www.sbert.net/
- Redis: https://redis.io/
- DeepSeek 定价: https://platform.deepseek.com/

---

*调研完成于 2026-05-27*
