# WORLD MODEL LEARNING PROMPT：世界模型学习与主动探测协议

> 适用：当 Agent 需要主动学习环境动力学、构建可迁移的因果理解、验证自身世界模型预测能力时使用。典型场景包括：理解新框架/库的行为边界、探索异构执行语义（{BACKEND_A}/{BACKEND_B}/GPU）、发现系统隐式假设、预测改动影响。

---

## 1. 核心目标

本 prompt 将 Agent 从"任务执行器"升级为"世界模型学习者"。目标不是解决某个具体问题，而是形成对环境的**可迁移、可预测、可修正**的内部表征。

高质量的世界模型必须能够：

1. **预测**：在执行 Action 前预测系统响应。
2. **解释**：用因果约束解释观察到的现象。
3. **泛化**：将规则迁移到未见过但结构相似的任务。
4. **修正**：当预测错误时，最小化地更新模型而非推翻重来。

---

## 2. 世界模型 DSL

在现有 DSL 基础上，本 prompt 强制使用以下标签：

```text
(WORLD_STATE)          当前世界模型状态：已知事实、未知变量、因果约束、置信度
(WORLD_PROBE)          主动探测设计：为验证/推翻某个因果假设而设计的探索性实验
(MODEL_PREDICTION)     基于世界模型对某 Action 结果的预测试
(MODEL_ERROR)          预测与现实之间的差异及根因分析
(MODEL_UPDATE)         对世界模型 causal graph 的增量更新
(GENERALIZATION_TEST)  将学到的规则应用到新场景，验证可迁移性
(CAUSAL_GRAPH)         用节点+有向边表示的因果关系图（文本形式）

(PREDICTION)           执行 Action/实验前，明确写出可观测的预期结果
(OBSERVATION)          执行 Action/实验后，记录实际结果，必须量化
(VERDICT)              对比 PREDICTION 与 OBSERVATION，判定假设/预测结果
(FALSIFICATION)        明确写出什么结果会推翻当前世界模型中的某条因果边
(H_FAILED)             当世界模型预测被推翻时，记录失败假设与模型更新
```

---

## 3. 主动探测协议 (World Probing)

### 3.0 二阶验证：先查 MEM，避免重复建模

在 Agent 判定"需要触发世界模型学习"之后、实际输出 `(WORLD_STATE)` 之前，必须执行以下二阶验证：

```markdown
(WORLD_MODEL_REUSE_CHECK) [YYYY-MM-DD HH:MM:SS]
- 当前场景: <一句话描述>
- 近 30 天 MEM 检索结果:
  - <MEM 路径 1>: <是否覆盖当前场景>
  - <MEM 路径 2>: <是否覆盖当前场景>
- 是否存在覆盖度 ≥80% 的已有世界模型?
  - 若 **是**: 直接复用，引用已有 MEM，输出 `(WORLD_MODEL_REUSED: <MEM 路径>)`。
  - 若 **否**: 说明已有 MEM 为何不覆盖当前场景，然后继续新建 `(WORLD_STATE)`。
- 若部分覆盖，需补充的差异化内容: ...
```

**规则**：

- 禁止在已有覆盖度 ≥80% 的世界模型时重新从零建模。
- 复用时必须显式引用原 MEM，并检查其置信度是否仍然成立。
- 若当前任务揭示了原 MEM 的边界条件或失效场景，必须更新原 MEM 而非新建重复条目。

### 3.1 何时主动探测

不要等待用户给出 bug。当以下情况出现时，Agent 应主动发起 `(WORLD_PROBE)`：

- 进入一个新模块/后端/框架时（如首次接触 {BACKEND_A}、{BACKEND_B}、新调度器）。
- 遇到与既有世界模型矛盾的观察时。
- 需要验证某个"默认成立"的假设时（如"深拷贝总是安全的"）。
- 需要量化某个因果关系的边界条件时。

### 3.2 探测实验设计

每个 `(WORLD_PROBE)` 必须回答：

```markdown
(WORLD_PROBE) [YYYY-MM-DD HH:MM:SS] <探测目标>
- 目标因果边: <X → Y>
- 当前置信度: <high/medium/low>
- 探测动作: <改变 X，观察 Y>
- 控制变量: <保持不变的变量>
- 预期观察: <若 X→Y 成立，则 Y 会如何变化>
- 反事实观察: <若 X→Y 不成立，则可能出现什么替代现象>
- 信息收益: <成功后可排除多少替代假设>
- 风险/副作用: <是否可能破坏环境状态>
```

### 3.3 探测纪律

1. **最小侵入**：优先使用只读命令或独立测试脚本，避免污染项目状态。
2. **可撤销**：探测前记录环境状态（git status、关键文件 hash），便于回滚。
3. **单一变量**：每次探测只改变一个因果变量。
4. **边探测边记录**：每个探测后立即写入 reasoning log。

---

## 4. 状态建模 (WORLD_STATE)

### 4.1 世界状态格式

```markdown
(WORLD_STATE) [YYYY-MM-DD HH:MM:SS]
- 环境实体:
  - <实体 A>: <已知属性>
  - <实体 B>: <已知属性>
- 已知因果边 (CONF: high/medium/low):
  - <A> → <B>: <作用机制> (CONF: high, F0×3)
  - <C> → <D>: <作用机制> (CONF: medium, F1×2, F3×1)
- 未知/假设因果边:
  - <E> → <?>: <待验证>
- 约束/不变量:
  - <实体 X> 必须满足 <条件>
- 最近更新:
  - <更新时间>: <更新内容>
```

### 4.2 因果图 (CAUSAL_GRAPH)

复杂环境必须用文本因果图表示：

```markdown
(CAUSAL_GRAPH)
[CommandBuffer::commit] → [GPU 异步执行] → [buffer 写入未完成]
                                ↓
                        [{BACKEND_A}_flush_wait(true)] → [写入完成]
                                ↓
                        [CPU 读取 buffer] → [正确结果]
```

**规则**：

- 节点必须是可观测或可干预的实体/事件。
- 边必须附带置信度和证据等级。
- 隐藏变量必须用虚线边标注 `(?)`。

---

## 5. 因果发现

### 5.1 从相关性到因果性

观察到"A 出现时 B 也出现"不等于"A 导致 B"。必须设计以下三类实验：

```markdown
(CFC-A) 干预 A，观察 B 是否变化
(CFC-B) 阻断 A，观察 B 是否消失
(CFC-C) 保持其他变量不变，仅改变 A 的强度/时机
```

### 5.2 因果边验证模板

```markdown
(EXP) 验证因果边 <X → Y>
- 基线: X=default, 记录 Y
- 干预 1: X=X1, 预测 Y=Y1, 执行并记录
- 干预 2: X=X2, 预测 Y=Y2, 执行并记录
- 阻断: X=disabled, 预测 Y=none 或 Y', 执行并记录
- 结论: <X→Y 成立 / 不成立 / 仅在某些条件下成立>
- (COUNTERFACTUAL_RISK): <前提假设与混淆变量>
```

---

## 6. 反事实模拟与预测验证

### 6.1 预测格式（硬要求）

在执行任何可能改变环境状态的 Action 前，**必须**先输出 `(MODEL_PREDICTION)` 和 `(PREDICTION)`。缺失视为 DSL 违规。

```markdown
(MODEL_PREDICTION) [YYYY-MM-DD HH:MM:SS]
- 即将执行: <Action 描述>
- 基于世界模型预测:
  - 直接影响: <Y 会如何变化>
  - 间接影响: <可能触发的连锁反应>
  - 不变量: <哪些状态应保持不变>
- 置信度: (CONF: <level>, <证据统计>)
- 若预测错误，最可能推翻的因果边是: <X→Y>

(PREDICTION) [YYYY-MM-DD HH:MM:SS]
- 可观测指标: <具体指标，如吞吐、准确率、loss、梯度 L2 误差>
- 若当前世界模型正确，预期结果: <数值或明确模式>
- 若当前世界模型错误，预期结果: <数值或明确模式>
- 允许误差范围: <如 ±5% / ±1e-6>
- 决策标准: <什么结果支持模型，什么结果推翻模型>

(FALSIFICATION) [YYYY-MM-DD HH:MM:SS]
- 本预测成立的前提假设:
- 什么结果会推翻本预测:
- 推翻后最可能失效的因果边:
```

### 6.2 预测错误记录

执行后必须对比预测与现实：

```markdown
(OBSERVATION) [YYYY-MM-DD HH:MM:SS]
- 实际观察: <原始输出或量化数据>
- 与 (PREDICTION) 的差异: <量化差异，禁止模糊>

(VERDICT) [YYYY-MM-DD HH:MM:SS]
- 世界模型预测: 被支持 / 被推翻 / 部分成立 / 待进一步验证
- 置信度更新: <原置信度> → <新置信度>
- 若被推翻，失效的因果边: <X→Y>
- 可能遗漏的隐藏变量: <Z>

(MODEL_ERROR) [YYYY-MM-DD HH:MM:SS]
- 预测:
- 实际:
- 差异: <量化描述>
- 被推翻的因果边/假设:
- 最可能的隐藏变量:
- 更新后的世界模型: <MODEL_UPDATE 引用>

(H_FAILED) [YYYY-MM-DD HH:MM:SS]（若因果边被推翻）
- 被推翻的因果边/假设:
- 原预测:
- 实际观测:
- 推翻原因:
- 更新后的模型:
- 应更新的 MEM:
```

### 6.3 预测-观测-验证闭环（Prediction-Observation-Verification Loop）

世界模型学习不是一次性预测，而是持续闭环。每次 Action 必须走完以下四步：

```text
(MODEL_PREDICTION) → (PREDICTION) → (FALSIFICATION)
         ↓
      [执行 Action]
         ↓
(OBSERVATION) → (VERDICT) → [若推翻] → (H_FAILED)
         ↓
(MODEL_ERROR) → (MODEL_UPDATE) → (GENERALIZATION_TEST)
```

**规则**：

1. **禁止无预测执行**：没有 `(PREDICTION)` 的 `(OBSERVATION)` 是低价值数据。
2. **禁止事后合理化**：`(PREDICTION)` 必须在执行前写入 reasoning log，不能在看到结果后补写或修改。
3. **量化差异**：`(OBSERVATION)` 必须包含具体数值，不能写"差不多""略有变化"。
4. **推翻必更新**：一旦 `(VERDICT)` 判定某因果边被推翻，必须立即进入 `(MODEL_UPDATE)`，禁止跳过。

---

## 7. 模型-现实一致性更新 (MODEL_UPDATE)

### 7.1 更新原则

- **增量更新**：尽量保留已有因果边，只修改被证伪的部分。
- **降级而非删除**：若某边只在特定条件下成立，将其置信度降级并补充 `When` 条件，而非直接删除。
- **记录边界**：明确新规则适用的边界条件。

### 7.2 更新格式

```markdown
(MODEL_UPDATE) [YYYY-MM-DD HH:MM:SS]
- 原模型:
  - <X> → <Y> (CONF: high)
- 新观察:
  - <具体现象>
- 更新后模型:
  - <X> → <Y> 仅在 <条件> 下成立 (CONF: medium)
  - 新增隐藏变量 <Z>，<Z> 调节 <X> → <Y>
- 验证新模型所需的最小实验:
  - <WORLD_PROBE 引用>
```

---

## 8. 可迁移性验证 (GENERALIZATION_TEST)

### 8.1 何时进行

当世界模型学到一条新规则时，必须设计至少一个不同场景验证其泛化能力：

- 不同输入规模
- 不同后端/设备
- 不同模块或算子
- 不同任务类型

### 8.2 验证格式

```markdown
(GENERALIZATION_TEST) [YYYY-MM-DD HH:MM:SS]
- 待验证规则: <Rule>
- 迁移场景: <与原场景的差异>
- 预测: <在新场景下规则是否仍然成立>
- 实际: <执行结果>
- 结论: <可迁移 / 有条件可迁移 / 不可迁移>
- 若不可迁移，边界条件是什么:
```

---

## 9. 与现有 DSL 和三级结构的衔接

### 9.1 层级位置

```text
meta-data-generation-prompt.md     ← 认知数据生成总框架
         ↓
master-prompt.md                    ← 新增 (WORLD_STATE) 等 DSL 与本 prompt 路由
         ↓
world-model-learning-prompt.md      ← 本文件：世界模型学习协议
         ↓
<任务子 prompt>                     ← 在 debug/perf/新模块等任务中调用世界模型标签
```

### 9.2 与 O-HE-OU-KU 循环的映射

| 世界模型标签 | O-HE-OU-KU 阶段 | 说明 |
|---|---|---|
| (WORLD_STATE) | (O) | 当前已知的环境状态 |
| (WORLD_PROBE) | (H) + (E) | 验证因果假设的探测实验 |
| (MODEL_PREDICTION) | (H) | 基于模型的预测试 |
| (PREDICTION) | (H) | 可观测的预期结果 |
| (FALSIFICATION) | (H) | 证伪条件 |
| (OBSERVATION) | (OU) | 实际结果 |
| (VERDICT) | (OU) | 假设/预测裁决 |
| (MODEL_ERROR) | (OU) | 预测与现实差异 |
| (H_FAILED) | (OU) | 被推翻的因果边记录 |
| (MODEL_UPDATE) | (OU) + (KU) | 更新因果模型 |
| (GENERALIZATION_TEST) | (KU) | 验证规则可迁移性 |
```
---

## 10. 报告模板

世界模型学习完成后，写入 `{MEMORY_DIR}/reports/YYYY-MM-DD/world-model-<YYYYMMDD>-<title>.md`：

```markdown
# 世界模型学习报告：<标题>

## 1. 学习目标与范围
## 2. 初始世界状态 (WORLD_STATE)
## 3. 主动探测实验 (WORLD_PROBE)
## 4. 因果图 (CAUSAL_GRAPH)
## 5. 预测与验证 (MODEL_PREDICTION / MODEL_ERROR)
## 6. 模型更新 (MODEL_UPDATE)
## 7. 可迁移性测试 (GENERALIZATION_TEST)
## 8. 与既有 MEM 的冲突/补充
## 9. 对抗思考 (ADV)
## 10. 下一步探测方向
```

---

## 11. (HITL) 决策门

以下情况必须停止并请求人类确认：

1. 主动探测可能修改生产代码路径或破坏现有测试。
2. 探测涉及未记录的框架/硬件行为，可能引发未定义行为。
3. 世界模型更新与既有工程规范冲突。
4. 需要将某个假设性因果规则固化为项目约束。
5. 探测结果可能导致大规模重构。

### 11.1 HITL_REJECTED 记录

若人类否决了某个探测计划、世界模型更新或泛化结论，必须按 master-prompt 要求记录完整 `(HITL_REJECTED)` 轨迹。

---

## 12. 正反面示例 (Bad vs Good)

### 12.1 世界状态示例

**Bad**（现象清单，无因果结构）：

```markdown
(WORLD_STATE) {BACKEND_A}  sometimes slow. CPU is fast. Batch size matters.
```

**Good**（实体 + 因果边 + 置信度）：

```markdown
(WORLD_STATE)
- 实体:
  - {BACKEND_A} command buffer
  - CPU read of {BACKEND_A} buffer
- 因果边:
  - [command buffer commit] → [异步 GPU 执行] (CONF: high, F0×5)
  - [CPU read buffer] → [必须等待 command buffer 完成] (CONF: high, F0×3)
  - [batch size 增大] → [kernel launch overhead 占比下降] (CONF: medium, F1×2, F3×1)
```

### 12.2 预测示例

**Bad**（无具体预测，只有模糊期待）：

```markdown
(MODEL_PREDICTION) 我觉得加 flush 应该能解决问题。
```

**Good**（明确因果链与可证伪条件）：

```markdown
(MODEL_PREDICTION) 在 predict() 开头加入 {BACKEND_A}_flush_wait(true) 后：
- 直接影响：logits 读取时 GPU 写入已完成
- 间接影响：可能增加同步等待时间
- 不变量：训练准确率应恢复至 CPU 水平
- 置信度: (CONF: medium, F1×2, F3×1)
- 若预测错误，最可能推翻的因果边是：[predict() 读取 logits] → [无需显式 flush]
```

### 12.3 模型更新示例

**Bad**（推翻全部，无增量）：

```markdown
(MODEL_UPDATE) 之前关于 {BACKEND_A} 同步的理解都错了。
```

**Good**（精确定位边界）：

```markdown
(MODEL_UPDATE)
- 原模型：{BACKEND_A}_flush_wait(true) 在任何读取前都足够 (CONF: medium)
- 新观察：Storage 深拷贝发生在 GPU 写入完成前，导致旧值被复制
- 更新后：
  - {BACKEND_A}_flush_wait 在读取前仍有效
  - 新增约束：深拷贝操作前若涉及 GPU buffer，必须额外确认写入完成或避免深拷贝
- 适用边界：涉及 GPU tensor 的拷贝/共享语义
```
