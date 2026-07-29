# Example：大模型推理能力差距分析适配

> 本示例展示如何将 `agentic-method` 适配到“评估一个框架/引擎距离支持大模型推理还差什么”的战略规划任务。

---

## 0. 问题冻结 (CTX)

```markdown
(CTX) 任务：评估 {FRAMEWORK_NAME} 支持 {MODEL_SIZE} 参数模型推理的能力差距
(CTX) 模型定义：{ARCHITECTURE}-based 语言模型，约 {MODEL_SIZE} 参数
(CTX) 推理定义：在 {TARGET_ENV} 上完成一次前向传播，输出 logits 或下一个 token
(CTX) 成功标准：
  - 能加载模型权重并完成完整前向推理
  - 数值结果与参考实现误差在 {ERROR_THRESHOLD} 内
  - 能在 {MEMORY_BUDGET} 内存预算内运行（允许量化/分页/卸载）
(CTX) 硬约束：
  - 必须基于 {FRAMEWORK_NAME} 当前真实代码状态
  - 每个关键结论必须标注证据等级 F0-F4 与置信度 CONF
  - 每个差距必须给出验证实验或反事实推演
```

---

## 1. 信息收集 (R)

1. {FRAMEWORK_NAME} 当前算子覆盖：MatMul/Linear、Softmax、LayerNorm/RMSNorm、RoPE、激活函数、Attention 等。
2. 内存管理：分配器、device 迁移、临时 buffer 生命周期。
3. 计算图能力：图捕获、算子融合、静态/动态 shape。
4. 并行与调度：线程池、异步后端批处理、CPU 向量化、多设备协同。
5. 模型加载：支持的权重格式、转换工具。
6. 量化与优化：FP16/BF16/INT8/INT4、kernel 融合、KV cache。
7. 参考模型需求：层数、hidden size、head 数、vocab size、位置编码方式。

---

## 2. 差距分析维度 (T)

| 维度 | 差距等级 |
|------|----------|
| 算子覆盖 | Blocker / Critical / Nice-to-have |
| 内存管理 | Blocker / Critical / Nice-to-have |
| 计算图/融合 | Blocker / Critical / Nice-to-have |
| 位置编码 | Blocker / Critical / Nice-to-have |
| 量化与压缩 | Blocker / Critical / Nice-to-have |
| 模型加载 | Blocker / Critical / Nice-to-have |
| 数值精度 | Blocker / Critical / Nice-to-have |
| 并行/异步 | Blocker / Critical / Nice-to-have |
| 错误处理/边界 | Blocker / Critical / Nice-to-have |

每个差距必须包含：`(GAP)`、证据等级、置信度、当前状态、3B 要求、`(PREDICTION)`、`(FALSIFICATION)`、`(EXP)`。

---

## 3. 竞争性假设 (BRANCH)

```markdown
(BRANCH) H1: 最大短板是算子覆盖。
(BRANCH) H2: 最大短板是内存管理与量化。
(BRANCH) H3: 最大短板是图执行与算子融合。
```

---

## 4. 分阶段路径 (M)

### 4.1 最小可行路径（MVP）

目标：在 {TIME_BUDGET} 内让模型“能跑起来”，不追求速度。

```markdown
(MVP) 阶段 1：...
(MVP) 阶段 2：...
(MVP) 阶段 3：...
```

### 4.2 生产级路径

目标：高效、稳定、可部署。

```markdown
(M) 阶段 1：...
(M) 阶段 2：...
(M) 阶段 3：...
```

---

## 5. 输出要求

1. `(CTX)` 复述。
2. 按维度输出 `(GAP)` 清单，按 Blocker/Critical/Nice-to-have 排序。
3. `(BRANCH)` 竞争性假设与区分实验。
4. `(MVP)` 和 `(M)` 路径。
5. 每个关键结论带 `(CONF)` 和证据等级。
6. 若信息不足，输出 `(HYPOTHESIS_UNVERIFIED)` 并停止。
7. 最后输出 `(DATA_QUALITY)` 自评与置信度最低的 3 项结论。
