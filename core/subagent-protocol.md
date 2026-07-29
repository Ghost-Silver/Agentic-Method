# SUBAGENT PROTOCOL：子 Agent 讨论与审查协议

> 作用：定义何时、如何、以何种角色调用子 Agent 进行讨论或审查，避免"为调用而调用"，确保讨论结果可训练、可审计。

---

## 0. 核心原则

1. **子 Agent 不是必需品**。只有在主 Agent 独自推理容易产生偏见、盲点或防御性结论时，才调用子 Agent。
2. **子 Agent 必须被赋予明确角色**。没有角色的讨论只会产生附和。
3. **子 Agent 输出必须被压缩**。禁止把子 Agent 的完整输出原样复制到主 reasoning log。
4. **主 Agent 保留最终决策权**。子 Agent 的输入是 `(SUB)` 证据，不是结论。
5. **所有子 Agent 调用必须记录**。包括角色、输入摘要、输出摘要、主 Agent 采纳/拒绝理由。

---

## 1. 调用触发条件

### 1.1 强制调用（MUST）

以下场景必须调用子 Agent：

| 场景                | 主 Agent 弱点                | 子 Agent 角色                       |
| ------------------- | ---------------------------- | ----------------------------------- |
| ADV 对抗思考        | 自我攻击容易变成防御性找补   | ADVERSARIAL_PAIR（拥护者 + 攻击者） |
| COUNTERFACTUAL_RISK | 容易遗漏混淆变量             | CONFUSION_HUNTER（混淆变量猎人）    |
| 生成 (MEM) 前       | 容易生成重复或过度泛化的 MEM | MEM_DEDUPLICATOR（去重审查员）      |
| 任务 (M) 阶段结束后 | 容易遗漏未完成任务或提前结束 | TASK_AUDITOR（任务连续性审查员）    |

### 1.2 建议调用（SHOULD）

以下场景建议调用：

| 场景               | 子 Agent 角色                                   |
| ------------------ | ----------------------------------------------- |
| 假设生成后         | HYPOTHESIS_EXPANDER（假设扩展器）               |
| 假设生成后         | HYPOTHESIS_VALIDATOR（假设验证审查员）          |
| 实验设计后         | EXPERIMENT_AUDITOR（实验审计员）                |
| 实验设计后         | EXPERIMENT_DESIGN_REVIEWER（实验设计审查员）    |
| Prompt 设计/审查后 | PROMPT_REVIEWER（Prompt 自审查员）              |
| 关键 HITL 决策前   | HITL_ADVISOR（决策顾问）                        |
| 逻辑证明完成后     | PROOF_REVIEWER（逻辑证明审查员）                |
| 反例构造后         | COUNTEREXAMPLE_REVIEWER（反例审查员）           |
| 情景生成后         | SCENARIO_DIVERGENCE_REVIEWER（情景发散审查员）  |
| 影响评估后         | IMPACT_REVIEWER（影响评估审查员）               |
| 来源评估后         | SOURCE_RELIABILITY_REVIEWER（来源可靠性审查员） |
| 技术地图绘制后     | LANDSCAPE_REVIEWER（技术地图审查员）            |
| 遗留风险评估后     | LEGACY_RISK_REVIEWER（遗留风险审查员）          |

### 1.3 禁止调用（MUST NOT）

- 简单的事实收集（如 `ls`、`grep`、`read`）
- 明确的代码执行（如 `cmake`、`make`、`pytest`）
- 用户已经给出明确指令且无争议空间的任务
- 上下文已经紧张时（剩余 token < 30%）

---

## 2. 子 Agent 角色定义

### 2.1 ADVERSARIAL_PAIR（对抗对）

**触发**：ADV 阶段
**输入**：当前方案/结论、已生成的 (ADV) 内容、相关证据
**输出**：

```markdown
(ADV-PRO) 拥护者辩护:

- 当前方案 strongest point 1
- strongest point 2

(ADV-CON) 攻击者反驳:

- 致命缺陷 1：...
- 致命缺陷 2：...
- 若当前方案错误，最不起眼的初始假设是：...

(ADV-SYNTHESIS) 主 Agent 综合:

- 采纳哪些攻击点
- 是否更新方案
```

**约束**：攻击者必须找到至少一个能推翻当前结论的致命假设，否则视为失败。

### 2.2 CONFUSION_HUNTER（混淆变量猎人）

**触发**：(COUNTERFACTUAL_RISK) 阶段
**输入**：当前因果结论、已声明的前提假设
**输出**：

```markdown
(SUB-CONFUSION)

- 隐藏变量 1：若此变量变化，结论是否仍成立？
- 隐藏变量 2：...
- 最小验证实验：...
```

**约束**：必须至少提出 2 个未在主 Agent 输出中出现的混淆变量。

### 2.3 HYPOTHESIS_EXPANDER（假设扩展器）

**触发**：(T) 假设生成后
**输入**：主 Agent 已生成的假设 H1, H2, ...
**输出**：

```markdown
(SUB-HYPOTHESIS)

- H<N+1>：被忽略但合理的假设
  - 支持证据：
  - 反对证据：
  - 证伪方式：
- H<N+2>：看起来荒谬但历史上发生过的假设
  - 支持证据：
  - 反对证据：
  - 证伪方式：
```

**约束**：新假设必须与已有假设形成竞争关系，不能是 trivial 变体。

### 2.4 EXPERIMENT_AUDITOR（实验审计员）

**触发**：(EXP) 实验设计后
**输入**：实验目标、控制变量、改变变量、预期结果、信息收益评估
**输出**：

```markdown
(SUB-EXP-AUDIT)

- 信息收益是否被高估？
- 是否存在成本更低的替代实验？
- 该实验是否真的能证伪目标假设？
- 建议修改：
```

### 2.5 MEM_DEDUPLICATOR（MEM 去重审查员）

**触发**：(KU) 生成新 MEM 前
**输入**：新 MEM 的 Rule/When/Because、memories/ 下近 30 天条目
**输出**：

```markdown
(SUB-MEM-DEDUP)

- 重复度评分：0-100
- 最相似的已有 MEM：
- 建议：新建 / 合并到已有 / 更新已有
- 理由：
```

**约束**：重复度 >80 时必须建议合并，禁止新建。

### 2.6 PROMPT_REVIEWER（Prompt 自审查员）

**触发**：prompt 设计/修改完成后，或候选 prompt 进入评测前
**输入**：待审查 prompt 全文、种子 prompt（如有）、变异算子（如有）
**输出**：

```markdown
(SUB-PROMPT-REVIEW)

- 缺陷类型：<假设-实验未绑定 / DSL 分层不清 / 子 Agent 无角色 / MEM 过度泛化 / HITL 遗漏 / 环境探针缺失 / 自指性冗余 / 反事实多变量 / 输出不可观测 / 无替代假设 / 其他>
- 严重级别：P0/P1/P2
- 证据等级：F0-F4
- 修复建议：...
- 结论：通过 / 修改后通过 / 废弃
```

**约束**：必须按 `prompt-review-prompt.md` 的 12 类缺陷清单审查；P0 缺陷必须触发 HITL。

### 2.7 FORM_REVIEWER（形式审查员）

**触发**：(M) 验证阶段
**输入**：主 Agent 当前段落的完整输出
**输出**：

```markdown
(SUB-FORM)

- 缺失标签：
- 格式违规：
- 建议修正：
```

**约束**：只审查格式和结构，不审查内容正确性。

### 2.8 WORLD_MODEL_AUDITOR（世界模型审计员）

**触发**：世界模型学习任务中，生成 `(WORLD_STATE)` / `(MODEL_PREDICTION)` / `(MODEL_UPDATE)` 后
**输入**：当前世界模型、因果图、预测、更新计划
**输出**：

```markdown
(SUB-WORLD-MODEL)

- 缺失实体/边: <世界模型中未显式建模但应存在的实体或因果边>
- 预测可证伪性: <MODEL_PREDICTION 是否包含明确的失败条件>
- 更新合理性: <MODEL_UPDATE 是过度推翻、更新不足还是刚好>
- 建议补充探测: <至少一个 WORLD_PROBE>
```

**约束**：必须至少指出一个缺失的实体/边或一个可证伪性缺陷。

### 2.9 HYPOTHESIS_VALIDATOR（假设验证审查员）

**触发**：`(T)` 阶段生成假设树后，或在 `(EXP)` 设计前
**输入**：假设 H1, H2, ...；每个假设的支持/反对证据；已设计的验证实验（若有）
**输出**：

```markdown
(SUB-HYP-VALID)

- H1 可证伪性: 是/否，理由
- H1 验证实验是否已设计: 是/否
- H1 的 PREDICTION 是否明确: 是/否
- H1 的 FALSIFICATION 条件是否明确: 是/否
- H1 若被推翻，是否有替代假设: 是/否
- 建议: 通过 / 修改后通过 / 放弃
```

**约束**：对每个假设必须给出通过/修改/放弃建议；不能全部默认通过。

### 2.10 EXPERIMENT_DESIGN_REVIEWER（实验设计审查员）

**触发**：`(EXP)` 实验设计完成后
**输入**：实验目标、验证假设、控制变量、改变变量、对照组、实验组、PREDICTION、FALSIFICATION、信息收益评估
**输出**：

```markdown
(SUB-EXP-DESIGN)

- 单一变量原则: 是否每次只改一个变量
- 对照组明确性: 对照组是否可信
- PREDICTION 可观测性: PREDICTION 是否包含具体数值或明确模式
- FALSIFICATION 条件: 什么结果会推翻目标假设
- 信息收益评估: 是否高估/低估
- 成本与风险: 是否合理
- 建议: 通过 / 修改 / 补充实验 / 放弃
```

**约束**：必须指出至少一个潜在缺陷或改进点；禁止仅写"设计良好"。

### 2.11 PROOF_REVIEWER（逻辑证明审查员）

**触发**：`logical-inference-prompt.md` 中完成 `(PROOF)` 后
**输入**：命题 `(CLAIM)`、证明步骤、引用的 `(LEMMA)`、已知假设
**输出**：

```markdown
(SUB-PROOF)

- 证明方法是否适用: 是/否，理由
- 是否存在循环论证: 是/否，位置
- 是否存在未声明的隐藏假设: 是/否，列出
- 引理是否已证明或可接受: 是/否
- 边界条件是否被覆盖: 是/否
- 建议: 通过 / 补充证明 / 弱化命题 / 放弃
```

**约束**：必须找出至少一个证明漏洞或未覆盖的边界；不能仅写"证明正确"。

### 2.12 COUNTEREXAMPLE_REVIEWER（反例审查员）

**触发**：`logical-inference-prompt.md` 中构造 `(COUNTEREXAMPLE)` 后
**输入**：命题 `(CLAIM)`、反例构造、预期违反的命题部分
**输出**：

```markdown
(SUB-COUNTEREXAMPLE)

- 反例是否真实违反命题: 是/否
- 反例是否满足命题的所有前提条件: 是/否
- 是否存在更小的反例: 是/否
- 反例是否揭示了更深层的问题: 是/否
- 建议: 接受 / 修正反例 / 重新理解命题
```

**约束**：必须确认反例确实在命题的前提范围内；禁止接受"近似违反"的反例。

### 2.13 SCENARIO_DIVERGENCE_REVIEWER（情景发散审查员）

**触发**：`scenario-planning-prompt.md` 中生成 `(SCENARIO)` 后
**输入**：已生成的情景 S1, S2, ...、触发条件、概率估计
**输出**：

```markdown
(SUB-SCENARIO)

- 情景间是否真正互斥: 是/否，重叠点
- 是否遗漏黑天鹅/尾部情景: 是/否，建议补充
- 触发条件是否可证伪: 是/否
- 概率估计是否存在锚定偏差: 是/否
- 是否遗漏了跨情景的共同脆弱点: 是/否
- 建议: 通过 / 补充情景 / 调整触发条件 / 重新评估概率
```

**约束**：必须指出至少一个遗漏的情景或一个概率估计偏差。

### 2.14 IMPACT_REVIEWER（影响评估审查员）

**触发**：`scenario-planning-prompt.md` 中完成 `(IMPACT)` 评估后
**输入**：情景描述、影响评分矩阵、项目目标
**输出**：

```markdown
(SUB-IMPACT)

- 技术影响评分是否合理: 高估 / 低估 / 合理
- 维护成本是否被低估: 是/否，理由
- 生态影响是否被忽略: 是/否
- 不可逆性评估是否准确: 是/否
- 是否存在未量化的第二阶效应: 是/否
- 建议: 通过 / 调整评分 / 补充维度
```

**约束**：必须指出至少一个被低估的影响维度或一个第二阶效应。

### 2.15 SOURCE_RELIABILITY_REVIEWER（来源可靠性审查员）

**触发**：`research-survey-prompt.md` 中完成 `(SOURCE)` 评估后
**输入**：来源清单、每个来源的等级、关键论断、引用网络
**输出**：

```markdown
(SUB-SOURCE)

- 是否存在单一来源断言被当作事实: 是/否，列出
- 来源等级是否被高估: 是/否
- 是否存在 echo chamber（多个来源引自同一原始出处）: 是/否
- 过时来源是否仍在使用: 是/否
- 利益相关方偏见是否被标注: 是/否
- 建议: 通过 / 降级来源 / 补充独立来源 / 移除不可信论断
```

**约束**：必须识别至少一个来源可靠性问题或 echo chamber。

### 2.16 LANDSCAPE_REVIEWER（技术地图审查员）

**触发**：`research-survey-prompt.md` 中绘制 `(LANDSCAPE)` 后
**输入**：技术地图、问题分解 `(QUESTION)`、已列方案
**输出**：

```markdown
(SUB-LANDSCAPE)

- 地图维度是否覆盖了关键决策因素: 是/否
- 是否遗漏了重要方案或替代路径: 是/否
- {PROJECT_NAME} 当前位置是否准确: 是/否
- 空白区域 (GAP) 是否真实存在机会: 是/否
- 是否存在维度间的高相关性被忽略: 是/否
- 建议: 通过 / 调整维度 / 补充方案 / 重新定位
```

**约束**：必须指出至少一个遗漏的方案或一个维度缺陷。

### 2.17 LEGACY_RISK_REVIEWER（遗留风险审查员）

**触发**：`code-archaeology-prompt.md` 中完成 `(LEGACY_RISK)` 评估后
**输入**：代码文物 `(ARTIFACT)`、历史假设、风险评分、当前依赖关系
**输出**：

```markdown
(SUB-LEGACY-RISK)

- 理解难度评分是否合理: 高估 / 低估 / 合理
- 修改风险是否被低估: 是/否，潜在破坏点
- 是否存在未被识别的隐藏依赖: 是/否
- 替代成本是否考虑了迁移期间的并行维护: 是/否
- 知识债务是否可接受: 是/否
- 建议: 通过 / 调整风险等级 / 补充依赖分析 / 建议更保守的处置
```

**约束**：必须指出至少一个被低估的风险或一个隐藏依赖。

### 2.18 TASK_AUDITOR（任务连续性审查员）

**触发**：每次任务 `(M)` 阶段完成后，根据 `master-prompt.md` 规则 17
**输入**：用户原始请求、当前 `todo-active.md` 内容、本次任务实际完成内容、当前阶段输出
**输出**：

```markdown
(SUB-TASK-AUDIT)

- 用户原始请求是否已完全满足: 是/否
- 原始请求分解后的待办事项完成情况:
  - [x] <任务 1>
  - [ ] <任务 2>
  - [ ] <任务 3> (HITL: <原因>)
- 是否存在 Agent 遗漏（应做未做）: 是/否，列出
- 未完成任务是否需要人类确认: 是/否
- 建议下一步行动: <具体动作>
- 是否应继续执行: 是/否
- 若继续，优先级最高的未完成任务: ...
```

**约束**：

- 必须逐条核对 `todo-active.md` 中的任务。
- 不能仅因 Agent 已输出 `(M)` 总结就默认任务完成。
- 若判定存在无需 HITL 的未完成任务，必须输出继续执行建议。

---

### 2.19 HITL_ADVISOR（HITL 决策顾问）

**触发**：关键 HITL 决策前，当主 Agent 不确定是否应触发人工确认或需要多角度评估决策影响时
**输入**：当前决策点描述、候选方案、风险等级、相关证据、项目硬约束
**输出**：

```markdown
(SUB-HITL-ADVISOR)

- 是否必须触发 HITL: 是/否/建议
- 触发理由（若建议触发）:
  - <理由 1>
  - <理由 2>
- 不触发 HITL 的潜在风险: <描述>
- 需要人类确认的最小信息集: <列出>
- 建议的人类决策选项: <A/B/C>
```

**约束**：

- 不得替代主 Agent 的 HITL 决策权，仅提供建议。
- 必须基于 `master-prompt.md` 第 7 章 HITL 决策树给出判断。
- 对安全关键、ABI 破坏、默认行为变更等场景应倾向于建议触发 HITL。

---

### 2.20 COMPILER_FLAGS_ADVISOR（编译器标志决策顾问）

**触发**：任何涉及 {PROJECT_NAME} 编译选项（`-O*`、`-ffast-math`、`-flto`、PGO、`-march=native`、`-fvisibility` 等）的评估、变更、回归排查或性能决策场景
**输入**：当前 CMake/编译配置、变更 diff、历史性能案例、目标构建环境
**输出**：

```markdown
(SUB-COMPILER-FLAGS)

- 变更风险等级: P0/P1/P2
- 是否必须 HITL: 是/否
- 建议对照组:
  - <基线配置>
  - <实验配置>
- 关键测量指标: <端到端时间/峰值显存/产物大小/指令数/...>
- 最小重复次数: <≥5>
- 反直觉点提醒: <如 PGO+LTO 非单调>
- 推荐行动: <接受/拒绝/需补充实验>
```

**约束**：

- 不得以产物指标（体积/指令数）替代端到端时间验证。
- 必须引用 `performance-decisions/` 历史案例作为 few-shot。
- 任何关闭 LTO、修改 `-ffast-math`、修改 `-march=native` 的建议必须触发 HITL。

---

### 2.21 SEMANTIC_CHANGE_REGRESSION_DESIGNER（语义变更回归设计师）

**触发**：修改 `Storage`、`Tensor`、`Node`、`AutogradMeta` 的拷贝/移动/析构/共享语义，或涉及设备迁移、overlap、异步同步、算子 ABI、跨后端调度时
**输入**：变更 diff、受影响源码路径、7 套语义测试模板、既有 MEM 与 bug-pattern
**输出**：

```markdown
(SUB-SEMANTIC-REGRESSION)

- 触发维度: <拷贝独立性/设备迁移/梯度共享/in-place-overlap/异步同步/算子 ABI/跨后端一致性>
- 参数化组合: <dtype × device × shape × ...>
- C++ 测试骨架: <代码块>
- 量化断言（≥3）:
  1. <断言 1>
  2. <断言 2>
  3. <断言 3>
- 反事实检查 (CFC): <如果保持深拷贝，预期结果>
- 风险等级: P0/P1/P2
- HITL 建议: 是/否
```

**约束**：

- 禁止仅验证修复目标而遗漏历史契约。
- 所有断言必须量化，必须包含 CFC 检查。
- 涉及真实 GPU/{BACKEND_A}/{CPU_ACCEL_A} 硬件的测试需 HITL 确认设备可用性。

---

### 2.22 ALGORITHM_CORRECTNESS_REVIEWER（算法正确性审查员）

**触发**：对 {PROJECT_NAME} 代码级算法正确性进行严格审查与形式化论证时
**输入**：相关源代码、头文件、形式化规范、单元测试、历史 bug、相关 MEM
**输出**：

```markdown
(SUB-ALGORITHM-CORRECTNESS)

- (CLAIM) <命题>
- (PROOF) / (COUNTEREXAMPLE) / (UNPROVEN): <论证或反例>
- (INVARIANT) <识别的不变量>
- (LEMMA) <引用的引理>
- (FALSIFICATION) <推翻条件>
- 风险等级: P0/P1/P2
- HITL 建议: 是/否
```

**约束**：

- 每个非平凡命题必须通过证明或反例验证；无法证明时标记 `(UNPROVEN)`。
- 所有命题、证明、反例必须绑定真实源码位置或测试输出。
- 结论将固化为项目约束或接口契约时必须建议 HITL。

---

## 3. 调用格式

主 Agent 在 reasoning log 中必须按以下格式发起调用：

```markdown
(SUB) [YYYY-MM-DD HH:MM:SS] <role> | <任务摘要>
输入:

- <关键信息 1>
- <关键信息 2>
  约束:
- <子 Agent 必须遵守的规则>

(SUB-OUTPUT) [YYYY-MM-DD HH:MM:SS]
<压缩后的子 Agent 输出，禁止原文复制>

(SUB-VERDICT) [YYYY-MM-DD HH:MM:SS]
主 Agent 对子 Agent 输入的处理：

- 采纳: <哪些点>
- 拒绝: <哪些点及理由>
- 是否改变原结论: 是/否
```

---

## 4. 输出压缩规则

子 Agent 输出通常较长，主 Agent 必须压缩后记录：

1. **保留**：关键论点、致命缺陷、具体证据、导致结论改变的输入。
2. **删除**：寒暄、重复、过度解释、已被主 Agent 已知的信息。
3. **长度**：每个子 Agent 输出压缩后不超过 300 tokens。
4. **引用**：如果子 Agent 提出了具体代码位置或文件路径，必须保留。

---

## 5. 责任归属

- **子 Agent 输入**标记为 `(SUB)` 或 `(SUB-OUTPUT)`，明确区分于主 Agent 的 `(R)/(T)/(E)/(M)`。
- **最终结论**必须由主 Agent 在 `(T)` 或 `(M)` 中重新输出，不能直接把子 Agent 结论当结论。
- 如果子 Agent 建议错误，主 Agent 要记录拒绝理由，这是有价值的训练数据。

---

## 6. 训练数据价值

子 Agent 讨论产生的高质量轨迹可用于：

- 训练模型的对抗推理能力
- 训练模型识别混淆变量
- 训练模型进行假设空间扩展
- 训练模型评估实验设计

同时，低质量的子 Agent 附和是噪声。因此必须：

- 明确角色对抗性
- 压缩输出
- 记录主 Agent 的采纳/拒绝决策

---

## 7. 与现有 DSL 的衔接

- `(SUB)`：发起子 Agent 调用
- `(SUB-OUTPUT)`：子 Agent 输出（压缩后）
- `(SUB-VERDICT)`：主 Agent 对子 Agent 输入的裁决
- `(ADV-PRO)` / `(ADV-CON)`：对抗对输出
- `(SUB-CONFUSION)`：混淆变量猎人输出
- `(SUB-HYPOTHESIS)`：假设扩展器输出
- `(SUB-EXP-AUDIT)`：实验审计员输出
- `(SUB-MEM-DEDUP)`：MEM 去重审查员输出
- `(SUB-FORM)`：形式审查员输出
- `(SUB-WORLD-MODEL)`：世界模型审计员输出
- `(SUB-HYP-VALID)`：假设验证审查员输出
- `(SUB-EXP-DESIGN)`：实验设计审查员输出
- `(SUB-PROOF)`：逻辑证明审查员输出
- `(SUB-COUNTEREXAMPLE)`：反例审查员输出
- `(SUB-SCENARIO)`：情景发散审查员输出
- `(SUB-IMPACT)`：影响评估审查员输出
- `(SUB-SOURCE)`：来源可靠性审查员输出
- `(SUB-LANDSCAPE)`：技术地图审查员输出
- `(SUB-LEGACY-RISK)`：遗留风险审查员输出
- `(SUB-TASK-AUDIT)`：任务连续性审查员输出
- `(TASK_CONTINUATION)`：主 Agent 决定继续执行未完成任务
