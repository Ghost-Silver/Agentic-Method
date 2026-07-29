# DEBUG PROMPT：{PROJECT_NAME} Bug 排查与修复协议

> 适用：任何程序异常、测试结果不符、运行时错误、数值异常、性能衰退、{BACKEND_A}/CPU 结果不一致等场景。

---

## 1. 阶段一：问题冻结 (R)

### 1.1 (CTX) 复述模板

```markdown
(CTX) Bug 现象：<用户描述 + 你观察到的具体输出>
(CTX) 期望行为：
(CTX) 实际行为：
(CTX) 触发条件：<输入 / 参数 / 环境 / 复现步骤>
(CTX) 已知约束：<来自项目 memory 的硬约束>
```

### 1.2 证据收集清单 (R)

必须按顺序检查并记录：

1. **最小复现路径**：构造或确认最小可复现命令 / 测试用例 / 脚本。
2. **版本与差异**：`git status`、`git log --oneline -5`、与上一次正常版本的 diff。
3. **日志与输出**：完整错误日志、堆栈、警告、assert 失败信息。
4. **相关代码**：从入口到异常点的调用链、关键变量、状态机。
5. **隐藏假设审查**：
   - 时序：异步执行是否完成？{BACKEND_A}/{BACKEND_B} buffer 是否已 flush？
   - 同步：GPU→CPU 拷贝前是否等待 command buffer？
   - 内存：对象生命周期、深拷贝 vs 浅拷贝、悬垂指针。
   - 数值：精度、累加顺序、NaN/Inf、除零。
   - 语义：函数契约、返回值约定、异常处理路径。

---

## 2. 阶段二：假设生成与实验设计 (T)

### 2.1 假设树 (Hypothesis Tree)

```markdown
(BRANCH) 分支 H1：{BACKEND_A} backward 同步缺失导致梯度未写回 (CONF: medium, F1×1, F3×1)
(H1.1) CrossEntropyNode::backward 缺少 flush
(H1.2) GradAccumulator 读取 {BACKEND_A} buffer 前未 wait
(BRANCH) 分支 H2：Storage/Tensor 拷贝语义与异步 GPU 写入冲突 (CONF: medium, F1×2, F3×1)
(H2.1) 节点保存前向输入副本时深拷贝触发过早
(H2.2) Tensor 拷贝构造初始化顺序导致未定义行为
(BRANCH) 分支 H3：通用路径或数据问题 (CONF: low, F4×1)
(H3.1) 数据集加载错误
(H3.2) 学习率设置不当
(MERGE) 汇总：H1 与 H2 均与 {BACKEND_A} 异步相关；H3 目前无证据支持。
```

### 2.1.1 子 Agent 假设扩展（可选但推荐）

生成初始假设树后，调用 **HYPOTHESIS_EXPANDER** 角色：

```markdown
(SUB) [YYYY-MM-DD HH:MM:SS] HYPOTHESIS_EXPANDER | 扩展假设空间
输入: 当前假设 H1, H2, H3 及其证据
约束: 新假设必须与已有假设竞争，不能是 trivial 变体；必须提供证伪方式

(SUB-OUTPUT) [YYYY-MM-DD HH:MM:SS]

- H4: <被忽略但合理的假设>（支持/反对/证伪）
- H5: <看起来荒谬但历史上发生过的假设>（支持/反对/证伪）

(SUB-VERDICT) [YYYY-MM-DD HH:MM:SS]

- 采纳: ...
- 拒绝: ...
- 是否改变假设优先级: 是/否
```

每个假设必须满足：

- **可证伪**：存在至少一个实验能在合理代价内推翻它。
- **可解释**：能解释全部或大部分观察到的现象。
- **可度量**：有明确的判断标准（pass/fail、数值阈值、diff 大小）。
- **带置信度**：每个假设后必须标注 `(CONF: <level>, <证据统计>)`。

### 2.2 实验模块 (EXP) 设计

对每个高优先级假设，设计如下实验：

```markdown
### EXP-<编号>：<假设一句话>

- 目的：验证 / 推翻 H<x>
- 方法：<二分 / 消融 / 反事实 / 对照 / 单元测试 / 中间变量输出>
- 单一变量：<明确列出>
- 对照组：<基线>
- 实验组：<改动>
- 判断标准：<什么结果支持假设，什么结果推翻>
- 风险与回滚：<如何恢复>
- 预期信息收益：<若成功可排除多少搜索空间>
```

### 2.3 方法选择指南

| 现象                    | 首选方法                     | 次选方法     |
| ----------------------- | ---------------------------- | ------------ |
| 输出完全错误            | 对照实验 (CPU gold standard) | 中间变量输出 |
| 输出部分错误 / 梯度异常 | 中间变量输出 + 二分          | 消融实验     |
| 随机 / 时好时坏         | 时序同步检查 (SYNC)          | 反事实 (CFC) |
| 性能衰退                | 采样 + 阶段拆解              | 消融实验     |
| 回归（之前正常）        | `git bisect` / 二分          | 版本 diff    |
| 数值精度差异            | 对照实验 + 精度分析          | 反事实       |

---

## 3. 阶段三：受控实验执行 (E)

### 3.1 执行纪律

1. **每次只改一个变量**（CFC）。
2. **先写测试，再改代码**：单元测试优先覆盖异常路径。
3. **显式同步点 (SYNC)**：任何 {BACKEND_A}/{BACKEND_B}/GPU 相关读取前必须 flush/wait。
4. **保留原始状态**：修改前先记录 git 状态，便于回滚。
5. **实时记录**：每步操作后立即写入 R/T/E/M 日志。

### 3.2 中间变量输出规范

当需要定位错误传播路径时，必须：

- 选择**最小集合**的中间变量，避免日志爆炸。
- 同时输出 CPU 与 {BACKEND_A}（或改动前后）版本，便于 diff。
- 使用 L2 / L∞ / 相对误差等量化差异。
- 输出后立即移除或禁用调试代码，禁止把临时输出残留到提交中。

---

## 4. 阶段四：归因与修复 (M)

### 4.1 反事实归因 (CFC)

修复前必须回答：

```markdown
(CFC) 若撤回本次修复，Bug 是否复现？
(CFC) 是否只修改了单一变量？
(CFC) 该变量是否必然导致该现象？
(CFC) 是否存在其他共变因素？
```

### 4.2 修复实施

1. **最小化改动**：仅修改必要代码，禁止顺带重构。
2. **单元测试**：新增或更新测试用例，必须 fail before fix / pass after fix。
3. **集成验证**：运行完整相关测试套件。
4. **对照验证**：如果涉及 {BACKEND_A}/GPU，必须与 CPU 结果对照；如果涉及性能，必须与基线对照。

### 4.3 对抗思考 (ADV)

```markdown
(ADV) 是否存在更简洁的修复？
(ADV) 是否存在更根本的修复（架构/接口层面）？
(ADV) 同类问题是否在其他 Node / Kernel / Scheduler 中存在？
(ADV) 本次修复是否可能引入新的时序 / 内存 / 精度问题？
```

#### 4.3.1 子 Agent 对抗对（强制）

完成上述 ADV 后，必须调用 **ADVERSARIAL_PAIR**：

```markdown
(SUB) [YYYY-MM-DD HH:MM:SS] ADVERSARIAL_PAIR | 修复方案对抗审查
输入: 当前修复方案、已执行实验结果、已生成的 (ADV) 内容
约束: 攻击者必须找到至少一个能推翻当前结论的致命假设；拥护者必须真诚辩护最强点

(SUB-OUTPUT) [YYYY-MM-DD HH:MM:SS]
(ADV-PRO) 拥护者辩护:

- <最强点 1>
- <最强点 2>

(ADV-CON) 攻击者反驳:

- <致命缺陷 1>
- <致命缺陷 2>
- 若当前方案错误，最不起眼的初始假设是：...

(SUB-VERDICT) [YYYY-MM-DD HH:MM:SS]

- 采纳: ...
- 拒绝: ...及理由
- 是否更新修复方案: 是/否
```

---

## 5. 阶段五：报告与沉淀

### 5.1 Bug 报告模板

写入 `{MEMORY_DIR}/reports/YYYY-MM-DD/debug-<YYYYMMDD>-<short-title>.md`：

```markdown
# Bug 报告：<标题>

## 1. 现象

## 2. 复现步骤

## 3. 根因分析（含假设树）

## 4. 实验记录（EXP-1 ... EXP-N）

## 5. 修复内容（文件、函数、行号）

## 6. 验证结果（测试输出、对照数据）

## 7. 对抗思考 (ADV)

## 8. 教训与后续行动

## 9. 状态：CLOSED / PENDING
```

### 5.2 更新 Skill

若修复过程中发现可复用经验，按 `main.md` 要求更新对应 skill 文件，并注明日期。

---

## 6. 正反面示例 (Bad vs Good)

### 6.1 假设生成示例

**Bad**（单一归因、无证据）：

```markdown
(T) 根因：{BACKEND_A} 有 bug，导致准确率只有 9.87%。
```

**Good**（多分支、可证伪、带置信度）：

```markdown
(BRANCH) H1：{BACKEND_A} backward 同步缺失 (CONF: medium, F1×1, F3×1)
(BRANCH) H2：Storage 深拷贝与异步写入冲突 (CONF: medium, F1×2, F3×1)
(BRANCH) H3：通用数据/参数问题 (CONF: low, F4×1)
(MERGE) H1 与 H2 均指向 {BACKEND_A} 异步路径；优先验证 H1。
```

### 6.2 反事实归因示例

**Bad**（多变量同时改变）：

```markdown
(CFC) 我把设备换成 CPU、batch size 改为 1、学习率调大后准确率正常了，所以是 {BACKEND_A} bug。
```

**Good**（单一变量、明确对照）：

```markdown
(CFC) 仅切换 device=cpu，其余参数不变；若准确率恢复，则问题与 {BACKEND_A} 路径相关。
(CFC) 仅添加 {BACKEND_A}_flush_wait(true) 一处，其余不变；若准确率恢复，则归因于该同步点。
```

### 6.3 修复验证示例

**Bad**（修复后只跑通一次）：

```markdown
(M) 已修复，测试通过。
```

**Good**（可复现、可撤销、多维度验证）：

```markdown
(M) 修复前复现：test_{DATASET_NAME} 准确率 9.87% (CONF: high, F0×3)
(M) 修复后验证：test_{DATASET_NAME} 准确率 99.31% (CONF: high, F0×3)
(CFC) 撤回修复后复现：准确率回到 9.87% (CONF: high, F0×3)
(CTRL) CPU 对照：准确率 99.29%，{BACKEND_A} 99.31%，误差 < 0.1% (CONF: high, F0×2)
```

## 7. (HITL) 决策门

以下情况必须停止并请求人类确认：

1. 需要修改公共接口、ABI、序列化格式。
2. 需要删除已有功能或测试。
3. 修复方案会显著降低性能（>5%）或改变默认行为。
4. 根因涉及设计缺陷，需要架构级改动。
5. 无法构造稳定复现，需要用户协助提供环境或数据。
6. 置信度为 low 的假设需要作为修复依据时。

### 7.1 HITL_REJECTED 记录

若人类否决了 Agent 提出的修复方案、根因假设或实验计划，必须立即记录 `(HITL_REJECTED)`：

```markdown
(HITL_REJECTED) [YYYY-MM-DD HH:MM:SS]

- 被否决方案: <Agent 原本提议>
- 人类理由: <逐条记录>
- Agent 隐藏假设: <未显式声明的假设>
- 表层优点: <为什么看起来合理>
- 深层缺陷: <为什么被否决>
- 替代方向: <人类建议>
- 假设更新: H<x>: <old> → <new>
- 应生成的 MEM: <标题>
```

- 写入当前 reasoning log。
- 若可迁移，额外生成 `{MEMORY_DIR}/memories/YYYY-MM-DD/hitl-rejected-<title>.md`。
- (M) 阶段输出：`(AUDIT) 已记录 HITL_REJECTED：<描述>`。
