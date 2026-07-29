# LOGICAL INFERENCE PROMPT：纯逻辑推理与形式化分析协议

> 适用：当 Agent 需要脱离具体代码执行，对算法正确性、不变量、边界条件、并发模型、类型系统性质或抽象命题进行严格推理时使用。本 prompt 为任务级协议，必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

## 0. 核心目标

纯逻辑推理任务的目标是产出**可被挑战的命题**和**可验证的论证**，而不是"看起来合理"的叙述。

本协议要求 Agent：

1. **显式声明命题**：将隐含假设写成 `(CLAIM)`，使其可被反驳。
2. **构造证明或反例**：每个非平凡命题必须通过证明 `(PROOF)` 或反例 `(COUNTEREXAMPLE)` 验证。
3. **追踪不变量**：识别系统在任何状态下都必须满足的性质 `(INVARIANT)`。
4. **管理抽象层级**：用 `(LEMMA)` 组织复杂论证，避免跳跃式推理。
5. **承认不确定性**：无法证明时显式标记 `(UNPROVEN)` 并说明所需额外条件。

---

## 1. 任务范围冻结 (CTX)

```markdown
(CTX) 当前任务：<一句话>
(CTX) 推理对象：<算法/抽象/命题/模型>
(CTX) 推理目标：<证明正确性 / 寻找反例 / 识别不变量 / 分析边界条件>
(CTX) 形式化程度：<严格证明 / 半形式化论证 / 概念一致性检查>
(CTX) 硬约束：<核心 DSL 不可省略、禁止无证据的"显然">
(HITL) 当前决策点：<若结论将固化为项目约束或接口契约，必须停止确认>
```

---

## 2. 信息收集 (R)

### 2.1 必须收集的内容

- 相关代码、伪代码或算法描述。
- 形式化规范（若存在）：类型签名、前置/后置条件、不变式。
- 相关论文、书籍、协议文档。
- 历史 bug 或反例（证明某些边界条件确实会触发）。
- 相关 MEM 和 skill。

### 2.2 证据分级

| 等级 | 含义 | 示例 |
| ---- | ---- | ---- |
| F0 | 代码/规范直接语义 | 函数前置条件要求 `n > 0` |
| F1 | 数学/逻辑直接推导 | 由归纳假设可得 P(k+1) |
| F2 | 权威来源声明 | 论文定理、官方文档 |
| F3 | 间接推断 | 由测试模式推测的边界行为 |
| F4 | 模型先验 | 常见模式、直觉 |

---

## 3. 命题生成 (T)

### 3.1 命题格式

```markdown
(CLAIM) C<N>: <命题一句话>

- 类型: <正确性 / 安全性 / 活性 / 不变量 / 边界条件>
- 形式化表述: <若可写，用数学或伪代码表达>
- 置信度: (CONF: <level>, <证据统计>)
- (FALSIFICATION) 推翻本命题的反例应满足: <条件>
- (PREDICTION) 若本命题成立，应能证明: <子结论>
```

### 3.2 命题空间要求

- 至少生成 **2 个竞争性命题**：一个"成立"，一个"在特定条件下不成立"。
- 必须包含至少一个关于**边界条件**或**极端输入**的命题。
- 必须包含至少一个关于**不变量**的命题。

---

## 4. 证明与反例 (E)

### 4.1 证明格式

```markdown
(PROOF) C<N>

- 方法: <归纳法 / 反证法 / 构造法 / 不变量追踪 / 模型检测>
- 基础步骤: ...
- 归纳/推导步骤: ...
- 关键引理: (LEMMA) ...
- 结论: C<N> 成立 / 在 <条件> 下成立
```

### 4.2 反例格式

```markdown
(COUNTEREXAMPLE) C<N>

- 反例构造: <具体输入/状态/序列>
- 违反的命题: <C<N> 的哪一部分被违反>
- 触发条件: <在什么边界下出现>
- 推论: <命题应弱化为什么形式>
```

### 4.3 无法证明时的处理

```markdown
(UNPROVEN) C<N>

- 已尝试的方法: ...
- 阻碍: <缺少什么条件或信息>
- 弱化的命题 C<N'>: ...
- 验证 C<N'> 所需的最小额外条件: ...
```

---

## 5. 不变量分析 (INVARIANT)

### 5.1 不变量格式

```markdown
(INVARIANT) I<N>: <不变量描述>

- 作用域: <函数/模块/系统/生命周期>
- 初始化保证: <何时成立>
- 保持性证明: <每次操作后仍成立的理由>
- 被违反的后果: <若失效会出现什么问题>
```

### 5.2 不变量与 {PROJECT_NAME}

常见需要分析的不变量：

- 张量维度一致性：操作前后 shape 的约束。
- 设备一致性：同一操作内张量是否在同一设备。
- 梯度累积：未 zero_grad 前梯度是否正确累加。
- 异步执行：读取 buffer 前 command buffer 是否已完成。
- 内存所有权：shared_ptr 引用计数是否避免悬空。

---

## 6. 观察更新 (OU)

```markdown
(OU) [YYYY-MM-DD HH:MM:SS] C<N> 验证结果

- (OBSERVATION) 实际推导结果: <证明成立 / 找到反例 / 无法证明>
- 与预测差异: <若反例与预期不同>
- (VERDICT) 命题裁决:
  - C<N>: 成立 / 在 <条件> 下成立 / 被推翻 / 待进一步验证
- 若被推翻:
  - (H_FAILED) 原命题: <C<N> 原始描述>
  - (H_FAILED) 原预测: <原始 PREDICTION>
  - (H_FAILED) 实际反例: <具体反例>
  - (H_FAILED) 推翻原因: ...
  - (H_FAILED) 更新后命题: <C<N'> 描述>
```

---

## 7. 总结与报告 (M)

### 7.1 报告结构

逻辑推理报告写入 `{MEMORY_DIR}/reports/YYYY-MM-DD/logical-inference-<title>.md`：

```markdown
# 逻辑推理报告：<标题>

## 1. 问题陈述

## 2. 定义与符号

## 3. 命题列表

## 4. 证明与反例

## 5. 不变量分析

## 6. 边界条件总结

## 7. 未证明命题与开放问题

## 8. 对抗思考 (ADV)

## 9. 可迁移结论
```

### 7.2 可迁移结论

若发现通用规则，沉淀为 `(MEM)`：

```markdown
(MEM) <规则标题>
**发现日期**: YYYY-MM-DD
**来源任务**: <任务标识>

Rule: ...
When: ...
Because: ...
Verification: ...
Failure cases: ...
Future scenarios: ...
```

---

## 8. DSL 标签要求

### 8.1 核心标签（不可省略）

`(CTX)` / `(HITL)` / `(R)` / `(T)` / `(E)` / `(M)` / `(CONF)` / `(AUDIT)` / `(ADV)` / `(HEURISTIC)`

### 8.2 本任务专用标签

```text
(CLAIM)           命题声明
(PROOF)           证明
(COUNTEREXAMPLE)  反例
(INVARIANT)       不变量
(LEMMA)           引理
(UNPROVEN)        无法证明的命题
(PREDICTION)      证明前的预期
(OBSERVATION)     推导后的实际结果
(VERDICT)         命题裁决
(FALSIFICATION)   证伪条件
(H_FAILED)        命题被推翻
```

---

## 9. 子 Agent 调用

### 9.1 强制调用（MUST）

| 场景 | 角色 | 作用 |
| ---- | ---- | ---- |
| ADV 阶段 | ADVERSARIAL_PAIR | 寻找证明中的隐藏假设和逻辑漏洞 |
| 复杂证明 | PROOF_REVIEWER | 检查证明步骤是否跳跃、是否循环论证 |

### 9.2 建议调用（SHOULD）

| 场景 | 角色 | 作用 |
| ---- | ---- | ---- |
| 反例构造后 | COUNTEREXAMPLE_REVIEWER | 确认反例确实违反命题，而非误解命题 |
| 生成 MEM 前 | MEM_DEDUPLICATOR | 检查与已有 MEM 的重复度 |

---

## 10. HITL 触发条件

1. 结论将固化为项目约束、接口契约或规范文档。
2. 证明涉及安全关键性质（如内存安全、并发正确性）。
3. 发现与既有实现矛盾的命题。
4. 需要人类提供缺失的规范或权威来源。

---

## 11. 正反面示例

### 11.1 命题

**Bad**：

```markdown
(CLAIM) 这个函数应该能处理所有输入。
```

**Good**：

```markdown
(CLAIM) C1: 对于任意非空张量 x，ReLUBackward(x, grad) 的输出 shape 与 x 相同。
- 类型: 正确性 / 不变量
- 形式化表述: ∀x, shape(x) ≠ ∅ → shape(ReLUBackward(x, grad)) = shape(x)
- 置信度: (CONF: high, F0×3)
- (FALSIFICATION) 反例: 存在 x 使得输出 shape 与 x 不同
```

### 11.2 证明

**Bad**：

```markdown
(PROOF) 显然，因为 ReLU 是 element-wise 操作。
```

**Good**：

```markdown
(PROOF) C1
- 方法: 构造法
- ReLUBackward 对 x 的每个元素独立应用: out_i = grad_i if x_i > 0 else 0
- 因此输出元素数量与 x 相同，shape 不变
- (LEMMA) element-wise 操作保持 shape: 已在 <引用> 中证明
```

---

## 12. 与 master-prompt.md 的衔接

层级关系：

```text
meta-data-generation-prompt.md
         ↓
master-prompt.md
         ↓
logical-inference-prompt.md  ← 本文件
         ↓
<具体推理任务>
```

启动顺序：

1. `meta-data-generation-prompt.md`
2. `master-prompt.md`
3. `logical-inference-prompt.md`

---

## 13. 输出目录

- 过程记录：`{MEMORY_DIR}/logs/YYYY-MM-DD/reasoning-<HHMMSS>-logical-inference-<title>.md`
- 推理报告：`{MEMORY_DIR}/reports/YYYY-MM-DD/logical-inference-<title>.md`
- 知识沉淀：`{MEMORY_DIR}/memories/YYYY-MM-DD/<category>-<title>.md`

---

## 14. 启动指令

收到逻辑推理任务后，必须按顺序输出：

1. `(CTX)` 复述任务。
2. 声明 Meta-Prompt 与 master-prompt 已加载。
3. `(DATA_QUALITY)` 自评。
4. `(R)` 收集定义与规范。
5. `(T)` 生成命题空间。

6. 当任务涉及第 15 章的 few-shot 证明模式示例时，可在 `(ADV)` 或 `(E)` 阶段按需调用 `PROOF_REVIEWER` 审查证明步骤是否跳跃、是否循环论证，或调用 `COUNTEREXAMPLE_REVIEWER` 确认反例确实违反命题而非误解命题。

禁止跳过命题声明直接给出结论。

---

## 15. 证明模式 few-shot 示例库

> 以下 9 个示例全部来自 `{MEMORY_DIR}/data/YYYY-MM-DD/proof-patterns/` 中的真实模式。Agent 在逻辑推理任务中可将其作为 few-shot 模板引用，但不得替代对当前任务的 `(R)` 信息收集与 `(T)` 命题生成。

### 15.1 结构归纳法（Structural Induction）

- **模式名称与适用前提**：对良基归纳类型 `T` 证明 `forall x:T, P x`；性质 `P` 必须覆盖 `T` 的所有构造子。
- **具体问题**：证明自然数加法右单位元 `forall n:nat, n + 0 = n`（`SF-zh/lf-current/Induction.v`，`Theorem plus_n_O`）。

```markdown
(CLAIM) C1: 对任意自然数 n，n + 0 = n。
- 类型: 正确性 / 全称量化
- 形式化表述: ∀n:nat, n + 0 = n
- 置信度: (CONF: high, F0×2 + F1×2)
- (PREDICTION) 若 C1 成立，可进一步证明加法交换律（需 plus_n_Sm 作为辅助引理）。
- (FALSIFICATION) 推翻 C1 的反例应满足：存在 n 使得 n + 0 ≠ n。

(PROOF) C1
- 方法: 对 n 做结构归纳法。
- 基础步骤: n = 0。由 plus 定义，0 + 0 = 0，成立。
- 归纳步骤: 设 n = S n'，归纳假设 IH：n' + 0 = n'。
  1. 左边: S n' + 0 = S (n' + 0)（plus 的 S 分支定义）。
  2. 由 IH 重写 n' + 0 = n'，左边化为 S n'，与右边相同。
- 关键引理:
  - (LEMMA) plus 定义：0 + m = m；S n + m = S (n + m)。
- 结论: C1 成立。

(INVARIANT) I1: 在证明 P(S n') 时，持有 P(n') 作为归纳假设。
- 作用域: 当前 S n' 分支。
- 初始化保证: 由 `induction n` 策略自动引入。
- 保持性: 仅使用子项 n' 上的 IH，保持良基性。
- 被违反的后果: 若错误地把 P(n) 本身当假设用于证明 P(S n)，会导致循环论证。

(COUNTEREXAMPLE) C2: 错误命题“∀n:nat, n + 1 = n”不成立。
- 反例构造: n = 0，则 0 + 1 = 1 ≠ 0。
- 违反的命题: C2 的等式。
- 触发条件: 把加法单位元从 0 误写为 1。
- 推论: 自然数加法的右单位元只能是 0。
```

- **适用场景标签**：`(CLAIM)` `(PROOF)` `(INVARIANT)` `(LEMMA)` `(COUNTEREXAMPLE)` `(FALSIFICATION)` `(PREDICTION)` `(CONF)`

### 15.2 反证法（Proof by Contradiction）

- **模式名称与适用前提**：目标是否定命题、不等式或“不可能性”；假设该命题成立后能与已知事实导出矛盾。
- **具体问题**：证明 1 不是偶数 `~ even 1`（`SF-zh/lf-current/IndProp.v`，`Theorem one_not_even`）。

```markdown
(CLAIM) C1: ~ even 1。
- 类型: 否定命题 / 不可能性
- 形式化表述: even 1 → False
- 置信度: (CONF: high, F0×2 + F1×1)
- (PREDICTION) 若 C1 成立，可从构造子不交性导出 1 = S (S n') 的矛盾。
- (FALSIFICATION) 若 even 的归纳定义允许 1 由某个构造子直接生成，则 C1 不成立。

(PROOF) C1
- 方法: 反证法（Reductio ad absurdum）。
- 基础步骤:
  1. 假设 H : even 1。
  2. 对 H 反演（inversion）。唯一可能构造子是 ev_SS n' E'，要求 1 = S (S n')。
  3. 由构造子不交性（O ≠ S n）得 1 = S (S n') 不可能，导出 False。
  4. 用 `exfalso` / `discriminate` 关闭分支。
- 关键引理:
  - (LEMMA) 构造子不交性：O ≠ S n。
  - (LEMMA) 归纳命题 ev_SS 的形式：forall n, even n -> even (S (S n))。
- 结论: ~ even 1 成立。

(INVARIANT) I1: 反证过程中假设集合必须保持一致；一旦出现 False，当前分支即被关闭。
- 作用域: 当前子证明。
- 初始化保证: 由 `intros H` 引入临时假设。
- 保持性: 每次推理必须保持“若所有假设为真则产生矛盾”。
- 被违反的后果: 若未真正导出矛盾就关闭分支，会接受假命题。

(COUNTEREXAMPLE) C2: 试图用反证法证明正存在命题“∃n, even n”而不给出具体 n，在构造主义 Coq 中不可行。
- 反例构造: 仅有 ~~(∃n, even n) 的证据，没有 n=0 或 n=2 等计算见证。
- 违反的命题: “反证法可以证明所有命题”。
- 触发条件: 目标是 ∃ 或正等式，且逻辑框架不允许排中律。
- 推论: 反证法在构造主义中主要用于否定命题；正命题优先构造性证明。
```

- **适用场景标签**：`(CLAIM)` `(PROOF)` `(INVARIANT)` `(LEMMA)` `(COUNTEREXAMPLE)` `(FALSIFICATION)` `(PREDICTION)` `(CONF)`

### 15.3 循环不变量（Loop Invariant in Hoare Logic）

- **模式名称与适用前提**：命令式 `WHILE` 循环的部分正确性；需找到满足“初始化成立、循环保持、退出蕴含后置条件”的断言 `I`。
- **具体问题**：验证慢减法程序 `WHILE ~(X=0) DO Y := Y-1; X := X-1 END`，前置 `X = m ∧ Y = n`，后置 `Y = n - m`（假设 m ≤ n）（`SF-zh/plf-current/Hoare2.v`）。

```markdown
(CLAIM) C1: 在初始 X=m、Y=n（m ≤ n）的前提下，上述 WHILE 循环终止后 Y = n - m。
- 类型: 正确性 / 不变量
- 形式化表述: {{X=m ∧ Y=n}} WHILE ~(X=0) DO Y:=Y-1; X:=X-1 END {{Y=n-m}}
- 置信度: (CONF: high, F0×3 + F2×1)
- (PREDICTION) 若 C1 成立，循环不变量应能同时绑定 X、Y 与初始参数 m、n。
- (FALSIFICATION) 若循环不终止，或不变量退出时不能推出 Y=n-m，则 C1 失效。

(PROOF) C1
- 方法: 霍尔逻辑循环规则 + 后果规则 + 赋值规则。
- 基础步骤（初始化）: 取 I := Y - X = n - m。初始 X=m、Y=n 时显然成立。
- 保持步骤:
  1. 假设当前状态满足 I ∧ ~(X=0)，即 Y - X = n - m 且 X ≠ 0。
  2. 执行 Y := Y-1; X := X-1 后，新状态为 (Y-1) - (X-1) = Y - X = n - m，I 仍成立。
- 终止步骤: 退出时 I ∧ X=0，故 Y - 0 = n - m，即 Y = n - m，蕴含后置条件。
- 关键引理:
  - (LEMMA) hoare_while: {{I ∧ b}} c {{I}} ⊢ {{I}} WHILE b DO c END {{I ∧ ~b}}。
  - (LEMMA) 赋值规则与整数算术：(Y-1) - (X-1) = Y - X。
- 结论: 循环满足部分正确性规范。

(INVARIANT) I1: Y - X = n - m。
- 作用域: 整个 WHILE 循环生命周期。
- 初始化保证: 由前置条件 X=m、Y=n 直接得到。
- 保持性: 每次迭代将 X、Y 同时减 1，差值不变。
- 被违反的后果: 若 I 不保持，循环退出后无法保证 Y = n - m。

(COUNTEREXAMPLE) C2: 取过弱不变量 I := True。
- 反例构造: 循环退出时仅知 True ∧ X=0，无法推出 Y = n - m。
- 违反的命题: “True 是不变量”本身可证，但不能蕴含后置条件。
- 触发条件: 不变量过弱，未捕获 X 与 Y 的代数关系。
- 推论: 不变量必须与循环变量和后置条件同时相关。
```

- **适用场景标签**：`(CLAIM)` `(PROOF)` `(INVARIANT)` `(LEMMA)` `(COUNTEREXAMPLE)` `(FALSIFICATION)` `(PREDICTION)` `(CONF)`

### 15.4 并查集正确性（Union-Find Equivalence）

- **模式名称与适用前提**：动态维护等价关系；关系必须自反、对称、传递；无删除操作。
- **具体问题**：洛谷 P3367 模板并查集：`find(x)=find(y)` 当且仅当 `x` 与 `y` 属于所有 `union(a,b)` 操作生成的等价闭包（`{MEMORY_DIR}/刷题日志/并查集.org`）。

```markdown
(CLAIM) C1: 在任意操作序列之后，find(x) = find(y) 当且仅当 R*(x, y)，其中 R* 是所有 union(a,b) 引入的对称传递闭包。
- 类型: 正确性 / 不变量
- 形式化表述: find(x)=find(y) ↔ R*(x,y)
- 置信度: (CONF: high, F0×2 + F1×2)
- (PREDICTION) 若 C1 成立，P3367 的同集查询、P1892 的团伙计数均正确。
- (FALSIFICATION) 若父指针成环、union 未链接根、或关系不传递，则 C1 失效。

(PROOF) C1
- 方法: 对操作序列长度归纳 + 森林结构归纳。
- 基础步骤: 初始 parent[i]=i，每棵树只有一个节点。R* 只含自环，find(i)=i，命题成立。
- 归纳步骤:
  1. union(x,y): 找到根 rx、ry。若 rx=ry 不改变；否则 parent[ry]=rx。新森林把两棵树的等价类取并，与 R* 增加 (x,y) 后的闭包一致。
  2. find(x): 沿父链走到根 r，路径压缩把链上节点父指针改为 r，但每个节点仍与根同属一个等价类，find 返回值不变。
- 关键引理:
  - (LEMMA) 父指针森林无环：parent 始终指向根，故沿父链严格接近根。
  - (LEMMA) find 返回其所在树当前根，且根满足 parent[r]=r。
  - (LEMMA) union 的对称链接保证 R* 的自反、对称、传递性。
- 结论: 并查集维护的等价类与操作序列生成的等价闭包一致。

(INVARIANT) I1: 对所有 x，反复取 parent 必在有限步内到达根 r 且 parent[r]=r。
- 作用域: 并查集数据结构全生命周期。
- 初始化保证: 初始 parent[i]=i。
- 保持性: union 链接根、find 压缩路径，均不引入环。
- 被违反的后果: 若出现环，find 可能无限递归或返回错误代表元。

(COUNTEREXAMPLE) C2: 错误的 union 实现直接写 parent[y] = x（x 不一定是根）。
- 反例构造: 设 parent[x]=z≠x，parent[y]=y。执行 parent[y]=x 后，y 的代表元变为 x，而 x 的代表元是 z，导致 y 与 x 被误判为不同类。
- 违反的命题: C1 的双向等价。
- 触发条件: union 未先调用 find 获取根。
- 推论: union 必须链接两个根节点。
```

- **适用场景标签**：`(CLAIM)` `(PROOF)` `(INVARIANT)` `(LEMMA)` `(COUNTEREXAMPLE)` `(FALSIFICATION)` `(PREDICTION)` `(CONF)`

### 15.5 图遍历可达性（Reflexive-Transitive Closure）

- **模式名称与适用前提**：有限有向图；边关系可判定；仅需判断源点可达集合。
- **具体问题**：BFS/DFS 从源点 s 出发，终止后 `visited` 是否等于 `R*(s)` 可达集（`SF-zh/lf-current/Rel.v`，`clos_refl_trans`）。

```markdown
(CLAIM) C1: 对有限有向图，BFS/DFS 终止后 visited = { v | R*(s, v) }。
- 类型: 正确性 / 不变量
- 形式化表述: visited = { v | clos_refl_trans R s v }
- 置信度: (CONF: high, F0×2 + F1×2 + F2×1)
- (PREDICTION) 若 C1 成立，可判断 s 是否能到达 t，也可作为无权最短路径 BFS 的基础。
- (FALSIFICATION) 若图无限、未维护 visited、或需要带权最短路径，则 C1 或其推论失效。

(PROOF) C1
- 方法: 不变量法 + 自反传递闭包归纳。
- 定义不变量 I:
  - s ∈ visited；
  - 对任意边 u→v，若 u ∈ visited 且 u 已被处理，则 v ∈ visited。
- 基础步骤: 初始化 visited={s}，queue/stack=[s]；由 rt_refl 知 s ∈ R*(s)。
- 保持步骤: 取出 u 并考察邻居 v；若 v 未访问则加入。此时 R*(s,u) 成立（由 I），R(u,v) 成立，由 rt_trans 得 R*(s,v)。
- 完备性: 算法只加入 R* 可达节点，故 visited ⊆ R*(s)。
- 完全性: 对任意 R*(s,v)，按闭包构造长度归纳：rt_refl 已处理；rt_step 由前驱 u 被访问而加入 v；rt_trans 由归纳假设可得。
- 关键引理:
  - (LEMMA) rt_trans 保证可达性可沿路径拼接。
  - (LEMMA) 有限图中 visited 单调递增，故算法终止。
- 结论: 终止时二者相等。

(INVARIANT) I1: visited 包含 s，且对已处理顶点的出边封闭。
- 作用域: BFS/DFS 主循环。
- 初始化保证: visited := {s}，queue/stack := [s]。
- 保持性: 每次弹出 u 并加入其未访问邻居 v 后，封闭性保持。
- 被违反的后果: 若未标记已访问，有向环会导致非终止或重复计数。

(COUNTEREXAMPLE) C2: 有向图 A→B→C→A 且未维护 visited。
- 反例构造: DFS 从 A 出发访问 B、C，又回到 A，因未标记 A 已访问而无限递归。
- 违反的命题: 算法终止性。
- 触发条件: 存在环且 visited 集合缺失或更新滞后。
- 推论: 可达性遍历必须维护 visited。
```

- **适用场景标签**：`(CLAIM)` `(PROOF)` `(INVARIANT)` `(LEMMA)` `(COUNTEREXAMPLE)` `(FALSIFICATION)` `(PREDICTION)` `(CONF)`

### 15.6 类型系统安全性（Progress + Preservation）

- **模式名称与适用前提**：形式化类型系统 + 小步操作语义 + 值的定义；需证明“良类型闭项不会 stuck”。
- **具体问题**：STLC 的 Progress 定理 `empty |- t : T -> value t ∨ ∃t', t --> t'`（`SF-zh/plf-current/StlcProp.v`）。

```markdown
(CLAIM) C1: 若空上下文下项 t 具有类型 T，则 t 是值，或存在 t' 使得 t 单步归约到 t'。
- 类型: 正确性 / 活性
- 形式化表述: ∀t T, empty |- t ∈ T -> value t ∨ ∃t', t --> t'
- 置信度: (CONF: high, F0×2 + F1×2 + F2×1)
- (PREDICTION) 若 C1 成立，闭合规约项不会卡住。
- (FALSIFICATION) 若类型规则给会卡住的项类型，或变量在空上下文中被定型，则 C1 失效。

(PROOF) C1
- 方法: 对定型推导 `empty |- t ∈ T` 做结构归纳。
- 直接情形:
  - T_Tru、T_Fls、T_Abs: 直接是值。
  - T_Var: 空上下文不可能，用反演排除。
- 归纳步骤:
  - T_App: t = t1 t2。分别对 t1、t2 用 IH。
    - t1 可步进 → ST_App1；
    - t1 是值，对 t2 用 IH；
    - 两者都是值 → t1 必为 λ（典范形式），用 ST_AppAbs。
  - T_Test: 对条件子项用 IH；若为布尔值则选分支。
- 关键引理:
  - (LEMMA) canonical_forms_fun: 类型为 Arrow T11 T12 的闭值必是 λ 抽象。
  - (LEMMA) canonical_forms_bool: 类型为 Bool 的闭值必是 tru 或 fls。
- 结论: Progress 成立。

(INVARIANT) I1: 良类型闭项在每一步归约前要么已是值，要么可继续归约。
- 作用域: 整个归约序列。
- 初始化保证: 由 Progress 提供。
- 保持性: 需 Preservation 定理配合（下一步仍良类型）。
- 被违反的后果: 若出现卡住项且仍被定型，则运行时类型错误。

(COUNTEREXAMPLE) C2: 若类型系统允许 `scc true : Nat`。
- 反例构造: `scc true` 可按规则步进到卡住状态，但该状态无归约规则且不是值。
- 违反的命题: Preservation（步进后类型不变且不会 stuck）。
- 触发条件: 类型规则过于宽松，给会卡住的项赋予类型。
- 推论: 类型安全要求类型规则与归约规则精确匹配。
```

- **适用场景标签**：`(CLAIM)` `(PROOF)` `(INVARIANT)` `(LEMMA)` `(COUNTEREXAMPLE)` `(FALSIFICATION)` `(PREDICTION)` `(CONF)`

### 15.7 二元运算结合律（Associativity of a Binary Operation）

- **模式名称与适用前提**：纯函数式二元运算递归定义在第一个参数上，且存在单位元。
- **具体问题**：证明列表拼接结合律 `forall A (l m n : list A), l ++ (m ++ n) = (l ++ m) ++ n`（`SF-zh/lf-current/Poly.v`，`Theorem app_assoc`）。

```markdown
(CLAIM) C1: 对任意类型 A 和列表 l、m、n，有 l ++ (m ++ n) = (l ++ m) ++ n。
- 类型: 正确性 / 代数性质
- 形式化表述: ∀A (l m n : list A), l ++ (m ++ n) = (l ++ m) ++ n
- 置信度: (CONF: high, F0×2 + F1×2)
- (PREDICTION) 若 C1 成立，fold/reduce 的重结合优化合法。
- (FALSIFICATION) 若存在 l、m、n 使等式不成立，则 C1 被推翻。

(PROOF) C1
- 方法: 对 l 做结构归纳。
- 基础步骤: l = []。
  - 左边: [] ++ (m ++ n) = m ++ n。
  - 右边: ([] ++ m) ++ n = m ++ n。
  - 两边相等。
- 归纳步骤: l = a :: l'，归纳假设 IH：l' ++ (m ++ n) = (l' ++ m) ++ n。
  - 左边: (a :: l') ++ (m ++ n) = a :: (l' ++ (m ++ n)) = a :: ((l' ++ m) ++ n)（由 IH）。
  - 右边: ((a :: l') ++ m) ++ n = (a :: (l' ++ m)) ++ n = a :: ((l' ++ m) ++ n)。
  - 两边相等。
- 关键引理:
  - (LEMMA) app 的定义：[] ++ ys = ys；(x::xs) ++ ys = x :: (xs ++ ys)。
  - (LEMMA) 构造子单射/等式保持：a :: xs = a :: ys → xs = ys（ implicitly by reflexivity ）。
- 结论: C1 成立。

(INVARIANT) I1: P(l) := ∀m n, l ++ (m ++ n) = (l ++ m) ++ n。
- 作用域: 对 l 的归纳证明。
- 初始化保证: P([]) 由单位元 nil 直接验证。
- 保持性: 若 P(l') 成立，app 的递归定义使 P(a::l') 成立。
- 被违反的后果: 若 app 在递归分支中不是把操作下推到子列表，则 IH 无法直接应用。

(COUNTEREXAMPLE) C2: 自然数减法不满足结合律。
- 反例构造: 5 - (3 - 1) = 3，而 (5 - 3) - 1 = 1。
- 违反的命题: “所有递归定义的二元运算都结合”。
- 触发条件: 运算没有单位元或递归分支破坏同态结构。
- 推论: 结合律必须逐运算验证，不可机械套用。
```

- **适用场景标签**：`(CLAIM)` `(PROOF)` `(INVARIANT)` `(LEMMA)` `(COUNTEREXAMPLE)` `(FALSIFICATION)` `(PREDICTION)` `(CONF)`

### 15.8 对归纳命题的反演（Inversion on Inductive Evidence）

- **模式名称与适用前提**：上下文中存在形如 `P t` 的假设，`P` 为归纳谓词；需要由证据结构推出参数形状或更小证据。
- **具体问题**：证明 `forall n, even (S (S n)) -> even n`（`SF-zh/lf-current/IndProp.v`，`Theorem evSS_ev`）。

```markdown
(CLAIM) C1: 若 even (S (S n)) 成立，则 even n 成立。
- 类型: 正确性 / 证据分析
- 形式化表述: ∀n, even (S (S n)) → even n
- 置信度: (CONF: high, F0×2 + F1×1)
- (PREDICTION) 若 C1 成立，可由偶数证据的构造子形状直接得到更小的偶数证据。
- (FALSIFICATION) 若 even 允许非归纳构造的方式生成 S (S n)，则 C1 失效。

(PROOF) C1
- 方法: 对证据 H : even (S (S n)) 做反演（inversion）。
- 基础步骤:
  - even 的构造子有 ev_0（生成 0）和 ev_SS k E（生成 S (S k)）。
  - H 的证据不可能由 ev_0 生成，因为 0 ≠ S (S n)。
  - 故 H 必由 ev_SS k E 生成，且 S (S n) = S (S k)，E : even k。
  - 由构造子单射性得 n = k，因此 E 即为 even n 的证据。
- 关键引理:
  - (LEMMA) 构造子不交性：0 ≠ S (S n)。
  - (LEMMA) 构造子单射性：S (S n) = S (S k) → n = k。
  - (LEMMA) ev_SS 的类型：∀k, even k → even (S (S k))。
- 结论: even n 成立。

(INVARIANT) I1: 归纳命题的证据结构必须与项的构造子形状一一对应。
- 作用域: 对 H 进行反演的子证明。
- 初始化保证: H 已存在于上下文中。
- 保持性: 反演只拆分出与 S (S n) 形状兼容的分支。
- 被违反的后果: 若对 n 而非对 H 做 destruct，无法直接获得 even n 的子证据。

(COUNTEREXAMPLE) C2: 直接对 n 做 `destruct n` 证明 evSS_ev。
- 反例构造: n = S n' 分支下，目标仍是 even (S (S (S n'))) → even (S n')，没有给出 even (S n') 的证据。
- 违反的命题: “对参数 destruct 总能解决归纳谓词相关目标”。
- 触发条件: 需要的约束隐藏在证据而非参数中。
- 推论: 对归纳谓词应优先反演其证据，而非仅对参数分类。
```

- **适用场景标签**：`(CLAIM)` `(PROOF)` `(INVARIANT)` `(LEMMA)` `(COUNTEREXAMPLE)` `(FALSIFICATION)` `(PREDICTION)` `(CONF)`

### 15.9 穷举分类讨论（Exhaustive Case Analysis）

- **模式名称与适用前提**：类型 `T` 的构造子有限且无递归；目标是 `forall x:T, P x`。
- **具体问题**：证明 `forall b:bool, orb b (negb b) = true`（`SF-zh/lf-current/Basics.v`，布尔函数真值表）。

```markdown
(CLAIM) C1: 对任意布尔值 b，b 与它的取反做或运算结果为 true。
- 类型: 正确性 / 穷举验证
- 形式化表述: ∀b:bool, orb b (negb b) = true
- 置信度: (CONF: high, F0×2 + F1×1)
- (PREDICTION) 若 C1 成立，两个分支的化简结果都应为 true。
- (FALSIFICATION) 若 bool 有第三个构造子或某分支结果不为 true，则 C1 失效。

(PROOF) C1
- 方法: 对 b 穷举分类讨论（destruct b）。
- 分支 1: b = true。negb true = false，orb true false = true。
- 分支 2: b = false。negb false = true，orb false true = true。
- 关键引理:
  - (LEMMA) negb 的定义：negb true = false；negb false = true。
  - (LEMMA) orb 的定义：orb true _ = true；orb false b = b。
- 结论: C1 成立。

(INVARIANT) I1: 每个构造子恰好对应一个子目标，所有可能取值都被覆盖。
- 作用域: destruct b 生成的子目标集合。
- 初始化保证: Coq 根据 Inductive bool 自动生成 true、false 两个分支。
- 保持性: 每个分支独立证明，不跨分支依赖。
- 被违反的后果: 若手动 match 遗漏分支，会产生非穷举模式匹配或错误命题。

(COUNTEREXAMPLE) C2: 用一次 `destruct n` 证明 `∀n:nat, n = 0 ∨ n ≠ 0`。
- 反例构造: n = S n' 分支下，目标化为 S n' = 0 ∨ S n' ≠ 0；仅由 destruct 无法自动得到 S n' ≠ 0，需要额外证明（反证法/构造子不交性）。
- 违反的命题: “穷举分类讨论可单独解决无限类型的全称命题”。
- 触发条件: 类型递归无限，destruct 一次只展开一层。
- 推论: 对 nat、list 等无限类型，需要结构归纳而非单纯 destruct。
```

- **适用场景标签**：`(CLAIM)` `(PROOF)` `(INVARIANT)` `(LEMMA)` `(COUNTEREXAMPLE)` `(FALSIFICATION)` `(PREDICTION)` `(CONF)`

### 15.10 示例库使用说明

- 引用示例时，必须显式说明当前任务与示例的差异点（类型、语义、边界条件）。
- 若示例中的 `(FALSIFICATION)` 条件在当前任务中成立，则禁止直接套用该模式，应改用 `(UNPROVEN)` 标记并请求 `(HITL)`。
- 每个 few-shot 示例都已内建可被挑战的 `(CLAIM)` / `(COUNTEREXAMPLE)`；Agent 在复用前应先用 `PROOF_REVIEWER` 检查证明步骤，或用 `COUNTEREXAMPLE_REVIEWER` 确认反例确实违反命题。
