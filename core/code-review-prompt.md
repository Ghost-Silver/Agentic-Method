# CODE REVIEW PROMPT：全局代码审查协议

> 适用：当 Agent 需要对 {PROJECT_NAME} 项目的代码库、模块、PR、commit 或特定改动进行系统性审查时使用。本 prompt 为任务级协议，必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

## 0. 核心目标

全局代码审查不是寻找"风格问题"，而是识别并量化以下五类风险：

1. **正确性风险**：算法实现、边界条件、并发/同步、资源生命周期、数值精度、自动微分正确性。
2. **性能风险**：调度优先级、同步点分布、内存分配、kernel fusion 机会、batching 效率。
3. **可维护性风险**：接口契约清晰度、依赖方向、重复代码、命名一致性、注释与文档。
4. **安全/稳定性风险**：越界访问、未初始化内存、异常安全、资源泄漏、未定义行为。
5. **测试/可验证性风险**：单元测试覆盖、对照实验、断言强度、可复现性。

审查输出必须同时服务于两个目的：

- **人类工程师**：可执行的改进清单，附带置信度和证据。
- **未来模型训练**：完整的假设-验证轨迹，包含失败假设与反事实思考。

---

## 1. 审查范围冻结 (CTX)

收到审查任务后，首条响应必须输出：

```markdown
(CTX) 当前任务：<一句话>
(CTX) 审查对象：<文件/模块/PR/commit 范围>
(CTX) 审查目标：<bug 发现 / 性能评估 / 架构合规 / 安全审计 / 全面审查>
(CTX) 审查基线：<对比的版本/分支/设计文档>
(CTX) 硬约束：<{BACKEND_A} 同步、LTO、调度优先级 {BACKEND_A}→{CPU_ACCEL_A}→{CPU_ACCEL_B}→BASIC、ABI 稳定性等>
(HITL) 当前决策点：<是否有需要立即人类确认的范围或目标>
```

**范围冻结要求**：

- 明确列出纳入审查的文件路径或 diff 范围。
- 明确列出**不纳入**审查的部分，避免无限扩展。
- 若审查对象过大，必须将其拆分为多个子审查任务，并用 `(PUSH)` / `(POP)` 管理上下文。

---

## 2. 信息收集 (R)

### 2.1 必须读取的信息

- 待审查代码本身（函数、类、模块）。
- 相关单元测试与集成测试。
- 相关设计文档、ADR、skill、MEM。
- 若审查 PR/commit：
  - `git diff` / `git show`
  - `git log --oneline -n 10`
  - PR 描述与相关 issue。
- 项目工程约束：
  - `{BUILD_SCRIPT}` 编译选项（LTO、优化级别）
  - `master-prompt.md` 中的硬约束
  - `project_memory.md` 中的项目级规则

### 2.2 证据分级

所有观察必须标注证据等级：

- **F0**：直接代码语义（如函数读取未初始化变量）
- **F1**：静态分析或类型系统结论（如函数签名不匹配）
- **F2**：文档/注释声明（需交叉验证）
- **F3**：间接推断（如性能采样显示某函数占比高）
- **F4**：模型先验/常见模式（仅作启发）

### 2.3 R 阶段输出格式

```markdown
## [YYYY-MM-DD HH:MM:SS] R | <审查对象>

- 来源：<文件路径 / 命令 / URL>
- 关键证据：<引用代码块或输出片段>
- (HEURISTIC) 直觉/猜测: <若本次阅读触发非线性直觉，原样记录>
```

---

## 3. 假设生成 (T)

### 3.1 必须生成的假设空间

禁止单一归因。至少生成 **2 个竞争性假设**，且必须包含：

- 一个"存在缺陷"假设（如某处同步缺失）。
- 一个"无明显缺陷但存在隐忧"假设（如边界条件未测试）。
- 一个"通用/非特定"假设（如测试覆盖不足、文档滞后）。

### 3.2 假设格式

```markdown
(BRANCH) H<N>: <假设一句话> (CONF: <level>, <证据统计>)

- 支持证据: <F0/F1 列表>
- 反对证据: <若有则列出，禁止隐藏>
- (FALSIFICATION) 推翻本假设的可观测结果: <数值或明确模式>
- (PREDICTION) 若本假设正确，(EXP-<编号>) 的预期结果: <数值或明确模式>
- (EXP) 验证本假设的实验: <编号与一句话描述>
- 预期信息收益: <高/中/低>
```

### 3.3 与代码审查的结合

针对代码审查，常见假设类型包括：

- H_correctness：某处实现与设计意图不一致。
- H_performance：某处调度或同步选择不是最优。
- H_maintainability：某处接口设计会增加未来维护成本。
- H_test_gap：某处行为缺乏自动化验证。
- H_security：某处存在越界/泄漏/UB 风险。

---

## 4. 验证实验 (E)

### 4.1 三类验证手段

| 类型         | 适用场景                       | 示例                                                      |
| ------------ | ------------------------------ | --------------------------------------------------------- |
| **静态验证** | 代码路径、依赖、类型、生命周期 | 函数调用图分析、边界条件检查、异常路径追踪                |
| **动态验证** | 运行时行为、性能、数值正确性   | 运行单元测试、构造边界输入、性能采样                      |
| **交叉验证** | 与基线/规范/历史对比           | CPU vs {BACKEND_A} 输出对比、与既有 MEM 对比、与历史 bug 模式对比 |

### 4.2 实验模板

```markdown
(EXP-<编号>) <实验一句话描述>

- 目标: <验证/推翻哪个假设>
- 验证假设: H<x>
- 审查维度: <正确性/性能/可维护性/安全/测试>
- 控制变量: <保持不变的代码/输入/环境>
- 改变变量: <仅一个>
- (PREDICTION) 若 H<x> 成立，预期可观测结果: <具体模式或数值>
- (PREDICTION) 若 H<x> 不成立，预期可观测结果: <具体模式或数值>
- (FALSIFICATION) 什么结果会推翻 H<x>: <具体模式或数值>
- 验证方法: <静态/动态/交叉>
- 优先级: <P0/P1/P2>
```

### 4.3 代码审查特有验证

- **编译验证**：修改后是否能通过 `-O3 -flto=thin` 编译。
- **测试验证**：相关单元测试是否通过。
- **对照验证**：与未修改版本在关键指标上是否一致或改进。
- **边界输入验证**：构造空 tensor、单元素 tensor、极大/极小值输入。
- **后端一致性验证**：CPU ({CPU_ACCEL_A}/{CPU_ACCEL_B}/BASIC) 与 {BACKEND_A} 输出差异是否可接受。

---

## 5. 观察更新 (OU)

每个实验执行后必须输出：

```markdown
(OU) [YYYY-MM-DD HH:MM:SS] EXP-<编号> 结果

- (OBSERVATION) 实际观察: <原始输出/数据/现象>
- 与预测差异: <量化差异，禁止模糊描述>
- (VERDICT) 假设裁决:
  - H<x>: 被支持 / 被推翻 / 待进一步验证
- 若 H<x> 被推翻:
  - (H_FAILED) 原假设: <H<x> 原始描述>
  - (H_FAILED) 原预测: <原始 PREDICTION>
  - (H_FAILED) 实际观测: <实际结果>
  - (H_FAILED) 推翻原因: <为什么原假设不能解释观测>
  - (H_FAILED) 更新后假设: <H<x'> 新描述>
```

---

## 6. 审查报告 (M)

### 6.1 报告结构

全局代码审查报告必须写入 `{MEMORY_DIR}/reports/YYYY-MM-DD/code-review-<title>.md`：

```markdown
# 代码审查报告：<标题>

## 1. 审查摘要

- 审查对象：
- 审查目标：
- 关键发现数量：
- 风险等级分布：P0 <数量> / P1 <数量> / P2 <数量>
- 推荐行动：

## 2. 关键发现（按风险等级排序）

### [P0] <问题标题>

- 位置：<文件路径:行号范围>
- 问题描述：
- 证据等级：<F0/F1/F2/F3>
- 置信度：(CONF: <level>, <证据统计>)
- 验证实验：<EXP 引用>
- 修复建议：
- HITL 建议：<是否需要人类确认>

### [P1] ...

## 3. 假设与验证轨迹

- H1: ... → VERDICT: ...
- H2: ... → VERDICT: ...
- (HYPOTHESIS_UNVERIFIED): ...

## 4. 性能/正确性/安全专题分析（若适用）

## 5. 可维护性与工程规范检查

## 6. 测试覆盖评估

## 7. 对抗思考 (ADV)

- 有没有可能遗漏了更严重的隐藏问题？
- 当前建议是否过度乐观或过度悲观？
- 如果核心假设错误，最快如何发现？

## 8. 推荐行动清单

| 优先级 | 行动 | 负责人      | 验证方式 |
| ------ | ---- | ----------- | -------- |
| P0     | ...  | Agent/Human | ...      |

## 9. 附件

- diff 摘要
- 测试输出
- 性能采样结果
```

### 6.2 风险等级定义

- **P0**：可能导致崩溃、数据损坏、安全漏洞、严重性能衰退或训练 correctness 错误。必须立即修复并触发 HITL。
- **P1**：可能导致维护困难、边缘 case 错误、性能次优。建议修复。
- **P2**：代码风格、轻微可读性问题、可未来改进的低风险项。

---

## 7. DSL 标签要求

### 7.1 核心标签（不可省略）

`(CTX)` / `(HITL)` / `(R)` / `(T)` / `(E)` / `(M)` / `(CONF)` / `(AUDIT)` / `(ADV)` / `(HEURISTIC)`

### 7.2 扩展标签（强烈建议）

- `(EXP)` / `(PREDICTION)` / `(OBSERVATION)` / `(VERDICT)` / `(FALSIFICATION)` / `(H_FAILED)`：假设验证闭环。
- `(CFC)`：反事实检查，验证"如果这部分代码不存在，问题是否仍会出现"。
- `(BRANCH)` / `(MERGE)`：多假设并行与汇总。
- `(SUB)`：调用子 Agent 进行专项审查。
- `(SYNC)`：涉及 {BACKEND_A}/{BACKEND_B}/GPU 异步时必须使用。

---

## 8. 子 Agent 调用

### 8.1 强制调用（MUST）

| 场景            | 子 Agent 角色    | 输入                 | 输出                    |
| --------------- | ---------------- | -------------------- | ----------------------- |
| ADV 阶段        | ADVERSARIAL_PAIR | 当前审查结论与证据   | 拥护/攻击观点与综合裁决 |
| 生成最终 MEM 前 | MEM_DEDUPLICATOR | 新发现与近 30 天 MEM | 重复度评分与合并建议    |

### 8.2 建议调用（SHOULD）

**硬约束**：建议调用的每个子 Agent 角色必须在 `subagent-protocol.md` 第 2 章中有明确定义；未定义角色不得出现在调用建议中。当前已注册角色清单：ADVERSARIAL_PAIR、CONFUSION_HUNTER、HYPOTHESIS_EXPANDER、EXPERIMENT_AUDITOR、MEM_DEDUPLICATOR、PROMPT_REVIEWER、FORM_REVIEWER、WORLD_MODEL_AUDITOR、HYPOTHESIS_VALIDATOR、EXPERIMENT_DESIGN_REVIEWER、PROOF_REVIEWER、COUNTEREXAMPLE_REVIEWER、SCENARIO_DIVERGENCE_REVIEWER、IMPACT_REVIEWER、SOURCE_RELIABILITY_REVIEWER、LANDSCAPE_REVIEWER、LEGACY_RISK_REVIEWER、TASK_AUDITOR。

| 场景         | 子 Agent 角色                                               | 审查重点                                                                                                        |
| ------------ | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 安全敏感代码 | CONFUSION_HUNTER + 已知安全模式（越界、泄漏、UB、异常安全） | 先识别混淆变量，再按 `system-programming-patterns/pattern-06-uninitialized-pointer-resource-leak.md` 等清单检查 |
| 性能敏感代码 | EXPERIMENT_AUDITOR + EXPERIMENT_DESIGN_REVIEWER             | 调度、同步、内存、kernel fusion；实验必须满足单一变量与可观测性                                                 |
| 架构耦合复杂 | LANDSCAPE_REVIEWER + IMPACT_REVIEWER                        | 接口契约、依赖方向、可扩展性                                                                                    |
| 假设生成后   | HYPOTHESIS_VALIDATOR                                        | 假设可证伪性、PREDICTION/FALSIFICATION 明确性                                                                   |
| 实验设计后   | EXPERIMENT_DESIGN_REVIEWER                                  | 单一变量、对照组、可观测性                                                                                      |

### 8.3 子 Agent 输出压缩

所有子 Agent 输出必须压缩到 300 tokens 以内，保留关键论点、代码位置、致命缺陷和导致结论改变的输入。

---

## 9. HITL 触发条件

以下情况必须停止审查并请求人类确认：

1. 建议删除、重命名或修改公共接口/ABI。
2. 建议绕过、禁用或弱化现有测试。
3. 发现潜在安全漏洞、数据竞争或未定义行为。
4. 审查结论与既有工程约束（如调度优先级、LTO、{BACKEND_A} 同步规则）冲突。
5. 建议大规模重构或架构调整。
6. 审查对象涉及尚未发布的敏感代码或第三方私有实现。

### 9.1 HITL_REJECTED 记录

若人类否决审查建议，必须按 `master-prompt.md` 要求记录完整 `(HITL_REJECTED)` 轨迹。

---

## 10. {PROJECT_NAME} 特定审查清单

### 10.1 异构后端审查

- [ ] {BACKEND_A}/{BACKEND_B}/GPU 读取 buffer 前是否调用 `{BACKEND_A}_flush_wait(true)`。
- [ ] {BACKEND_A} kernel 是否包裹在 `@autoreleasepool` 中。
- [ ] 调度器是否优先选择 {BACKEND_A} → {CPU_ACCEL_A} → {CPU_ACCEL_B} → BASIC，避免 BASIC。
- [ ] 数值精度：{BACKEND_A} 与 CPU 输出差异是否在允许范围内。
- [ ] 自动微分节点是否正确处理 buffer modified 标记。

### 10.2 性能审查

- [ ] 编译是否启用 LTO。
- [ ] 热点函数是否优先使用 {CPU_ACCEL_B}/{CPU_ACCEL_A} 而非 BASIC。
- [ ] 是否存在不必要的同步点或 buffer 分配。
- [ ] 是否存在 kernel fusion 或 command buffer batching 机会。

### 10.3 可维护性审查

- [ ] 新接口是否最小化、是否破坏现有 ABI；若修改 `include/` 下公共头文件，必须对照 `system-programming-patterns/pattern-02-abi-break-public-header.md`。
- [ ] 错误处理是否使用 `{PROJECT_NAME}Error::throwException()` 而非 silent fallback。
- [ ] 是否避免深拷贝旧 buffer，优先使用移动语义或浅拷贝；若修改 `Storage`/`Tensor`/`Node` 拷贝/移动/析构语义，必须对照 `bug-patterns/pattern-01-semantic-side-effect-in-copy-fix.md`。
- [ ] 单元测试是否覆盖异步路径和边界条件；若涉及 {BACKEND_A}/{BACKEND_B} 异步读写，必须对照 `bug-patterns/pattern-04-async-backend-missing-sync.md`。

### 10.4 历史 bug 模式触发条件

以下代码气味出现时，必须按对应历史 bug 模式输出结构化审查发现，禁止仅做文字描述：

| 代码气味                                                              | 必须对照的模式                                                      | 输出模板来源        |
| --------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------- |
| 修改 `Storage`/`Tensor`/`Node`/`AutogradMeta` 拷贝/移动/析构/共享语义 | `bug-patterns/pattern-01-semantic-side-effect-in-copy-fix.md`       | 模式 1 审查输出模板 |
| 修改 `include/` 下类布局、枚举、虚函数、函数签名                      | `system-programming-patterns/pattern-02-abi-break-public-header.md` | 模式 3 审查输出模板 |
| {BACKEND_A}/{BACKEND_B}/GPU 异步 kernel 返回后直接读取 buffer                       | `bug-patterns/pattern-04-async-backend-missing-sync.md`             | 模式 2 审查输出模板 |
| 同一次 PR 同时修改 allocator、deleter、sync 中的两个以上              | `bug-patterns/pattern-01-semantic-side-effect-in-copy-fix.md`       | 模式 1 CFC 段       |
| 深拷贝 `make_shared<Tensor>(...)` 改为共享指针                        | `bug-patterns/pattern-01-semantic-side-effect-in-copy-fix.md`       | 模式 1 危险信号     |

触发以上任一气味时，输出必须包含：位置、证据等级、PREDICTION、FALSIFICATION、验证实验、CFC、HITL 建议。

---

## 11. 正反面示例 (Bad vs Good)

### 11.1 发现问题

**Bad**：

```markdown
(M) 这段代码看起来有问题，可能会变慢。
```

**Good**：

```markdown
(M) [P1] MatMulNode::backward 中每次反向都分配新 {BACKEND_A} buffer

- 位置: src/AutoGrad/Nodes/MatMulNode.cpp:142-158
- 证据: F1（代码语义），每次调用创建 newBufferWithLength
- (PREDICTION) 若使用 buffer pool，backward 阶段耗时降低 10-20%
- (EXP-1) 使用 test_{DATASET_NAME}_perf --device {BACKEND_A} --batch 128 对比当前与 buffer pool 版本
- (VERDICT) 待执行
- 置信度: (CONF: medium, F1×2, F3×1)
```

### 11.2 结论表述

**Bad**：

```markdown
(ADV) 我觉得这个实现应该没问题。
```

**Good**：

```markdown
(ADV-BACKWARD) 反向推演

- 假设"当前实现正确"是错误的。
- 最不起眼的初始假设：开发者默认输入 tensor 总是非空。
- 失效场景：空 batch 或零维 tensor 时可能导致未定义行为。
- 最小验证实验：构造空 tensor 输入运行单元测试。
```

---

## 12. 与 master-prompt.md 的衔接

### 12.1 层级关系

```text
meta-data-generation-prompt.md
         ↓
master-prompt.md
         ↓
code-review-prompt.md  ← 本文件
         ↓
<具体审查任务>
```

### 12.2 加载顺序

首轮必须按以下顺序加载：

1. `meta-data-generation-prompt.md`
2. `master-prompt.md`
3. `code-review-prompt.md`
4. 子 prompt（如审查涉及性能优化则再加载 `performance-test-prompt.md`）

---

## 13. 输出目录结构

- 过程记录：`{MEMORY_DIR}/logs/YYYY-MM-DD/reasoning-<HHMMSS>-code-review-<title>.md`
- 审查报告：`{MEMORY_DIR}/reports/YYYY-MM-DD/code-review-<title>.md`
- 可迁移知识：`{MEMORY_DIR}/memories/YYYY-MM-DD/<category>-<title>.md`
- 会话日志：`{MEMORY_DIR}/sessions/YYYY-MM-DD/session-<id>.md`

---

## 14. 启动指令 (Activation)

收到代码审查任务后，必须按以下顺序输出：

1. `(CTX)` 复述审查对象、目标、基线、硬约束。
2. 声明 Meta-Prompt 与 master-prompt 已加载。
3. `(DATA_QUALITY)` 自评初始状态。
4. `(R)` 收集信息，进入 O-HE-OU-KU 循环。

禁止在未完成上述步骤前直接输出审查结论。
