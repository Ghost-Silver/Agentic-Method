# 大模型推理能力差距分析 Prompt

> 目标：系统评估当前项目距离能够稳定、高效地推理一个数十亿参数级别的大语言模型还缺少哪些关键能力，并给出分阶段补齐路径。
> 本 prompt 要求输出可被挑战、可被验证的结论，而不是泛泛而谈的功能清单。

---

## 0. 问题冻结 (CTX)

```markdown
(CTX) 任务：评估 {PROJECT_NAME} 支持大模型推理的能力差距
(CTX) 模型定义：数十亿参数规模的 Transformer-based 语言模型（例如 {MODEL_FAMILY_A}、{MODEL_FAMILY_B} 或同类架构）
(CTX) 推理定义：在目标运行环境（{BACKEND_A}/CPU/GPU）下完成一次前向传播（prefill + decode），输出 logits 或下一个 token
(CTX) 成功标准：
  - 能加载模型权重并完成一次完整前向推理
  - 数值结果与参考实现（如 PyTorch/Transformers）误差在可接受范围（如 <1e-3）
  - 模型能在目标消费级设备内存预算内运行（允许量化/分页/卸载）
(CTX) 硬约束：
  - 必须基于 {PROJECT_NAME} 当前真实代码状态，不能假设未来会实现的特性
  - 每个关键结论必须标注证据等级 F0-F4 与置信度 CONF
  - 每个差距必须给出验证实验或反事实推演
```

---

## 1. 信息收集 (R)

请先收集以下信息（若信息不足，请明确标注为假设并要求后续验证）：

1. **{PROJECT_NAME} 当前算子覆盖**：列出 {PROJECT_NAME} 已实现的核心算子（MatMul/Linear、Softmax、LayerNorm、RMSNorm、RoPE、{OP_EXAMPLE}/SiLU、Attention 等）。
2. **{PROJECT_NAME} 当前内存管理**：Storage/Tensor 的内存分配、device 迁移、临时 buffer 生命周期管理。
3. **{PROJECT_NAME} 当前图执行能力**：是否有计算图/图捕获？是否支持算子融合？是否有静态/动态 shape 支持？
4. **{PROJECT_NAME} 当前并行与调度**：ThreadPool、{BACKEND_A} command buffer 批处理、CPU {CPU_ACCEL_B}/{CPU_ACCEL_A}、多设备协同。
5. **{PROJECT_NAME} 当前模型加载与序列化**：支持哪些权重格式（safetensors/bin/npz/自定义）？是否有模型转换工具？
6. **{PROJECT_NAME} 当前量化与优化**：是否支持 FP16/BF16/INT8/INT4？是否有 kernel 融合、内存池、KV cache 优化？
7. **参考模型需求**：{MODEL_FAMILY_A}、{MODEL_FAMILY_B} 等模型的层数、hidden size、head 数、vocab size、激活函数、位置编码方式。

---

## 2. 差距分析维度 (T)

请从以下维度生成差距清单。每个维度至少给出 **1 个关键差距** 和 **1 个可验证的预测**：

| 维度 | 关键问题 | 当前状态假设 | 大模型要求 | 差距等级 |
|------|----------|--------------|------------|----------|
| 算子覆盖 | 是否缺少 Transformer 推理必需的算子？ | | | Blocker / Critical / Nice-to-have |
| 内存管理 | 模型权重+KV cache+激活值是否会 OOM？ | | | Blocker / Critical / Nice-to-have |
| 计算图/融合 | 是否有算子融合、图优化来降低 memory bandwidth？ | | | Blocker / Critical / Nice-to-have |
| 位置编码 | 是否支持 RoPE / ALiBi / 其他大模型使用的位置编码？ | | | Blocker / Critical / Nice-to-have |
| 量化与压缩 | 是否支持让大模型在消费级设备上跑起来的量化方案？ | | | Blocker / Critical / Nice-to-have |
| 模型加载 | 是否能从 safetensors/bin 加载真实权重？ | | | Blocker / Critical / Nice-to-have |
| 数值精度 | 当前实现是否与参考实现误差可控？ | | | Blocker / Critical / Nice-to-have |
| 并行/异步 | {BACKEND_A}/CPU 是否能高效并行处理大模型的计算图？ | | | Blocker / Critical / Nice-to-have |
| 错误处理/边界 | 大模型推理中的 shape 变化、溢出、NaN 是否有健全处理？ | | | Blocker / Critical / Nice-to-have |

每个差距必须包含：

```markdown
(GAP) G<N>: <差距一句话描述>
- 维度：
- 差距等级：Blocker / Critical / Nice-to-have
- 证据等级：(F0-F4)
- 置信度：(CONF: <level>, <证据统计>)
- 当前状态：<{PROJECT_NAME} 已有什么>
- 大模型要求：<需要什么>
- (PREDICTION) 若补齐该差距，应观测到什么可量化改进：
- (FALSIFICATION) 什么结果会证明这个差距不存在或被高估：
- (EXP) 建议的最小验证实验：
```

---

## 3. 竞争性假设 (BRANCH)

请生成至少 **2 个竞争性假设**：

```markdown
(BRANCH) H1: {PROJECT_NAME} 当前最大短板是算子覆盖，补齐 Attention/RoPE/RMSNorm 后即可跑通大模型。
(BRANCH) H2: {PROJECT_NAME} 当前最大短板是内存管理与量化，即使算子齐全，大模型也会在 {BACKEND_A}/CPU 上 OOM。
(BRANCH) H3: {PROJECT_NAME} 当前最大短板是图执行与算子融合，没有融合会导致 memory bandwidth 瓶颈，推理速度不可接受。
```

对每个假设，给出：
- 支持证据
- 反对证据
- 关键区分实验（即验证哪个假设更成立的实验）

---

## 4. 分阶段路径 (M)

请给出两条路径：

### 4.1 最小可行路径（MVP）

目标：在限定时间内让一个大模型在 {PROJECT_NAME} 上“能跑起来”，不追求速度。

输出格式：

```markdown
(MVP) 阶段 1（第 1-N 天）：...
(MVP) 阶段 2（第 N+1-M 天）：...
(MVP) 阶段 3（第 M+1-K 天）：...
```

每个阶段必须包含：任务、验收标准、风险、所需 HITL 决策点。

### 4.2 生产级路径

目标：让大模型在 {PROJECT_NAME} 上高效、稳定、可部署。

输出格式同上，但需包含量化、KV cache 优化、算子融合、错误处理等。

---

## 5. 输出要求

1. 先输出 `(CTX)` 复述，确认理解任务。
2. 按维度输出 `(GAP)` 清单，按 Blocker / Critical / Nice-to-have 排序。
3. 输出 `(BRANCH)` 竞争性假设与区分实验。
4. 输出 `(MVP)` 和 `(M)` 生产级路径。
5. 每个关键结论必须带 `(CONF)` 和证据等级。
6. 若信息不足，输出 `(HYPOTHESIS_UNVERIFIED)` 并停止，不得编造。
7. 最后输出 `(DATA_QUALITY)` 自评与置信度最低的 3 项结论。
