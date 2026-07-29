# RESEARCH SURVEY PROMPT：研究调研与技术趋势分析协议

> 适用：当 Agent 需要调研新技术、竞品实现、学术论文、开源项目或行业趋势，并产出可行动的知识地图时使用。本 prompt 为任务级协议，必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

## 0. 核心目标

研究调研不是信息搬运，而是**将外部信息转化为可验证、可迁移的项目决策输入**。

本协议要求 Agent：

1. **明确调研问题**：不是"了解一下 X"，而是"X 是否适用于 {PROJECT_NAME} 的 Y 场景"。
2. **分级信息来源**：区分官方文档、论文、社区讨论、模型先验。
3. **绘制技术地图**：定位各方案在问题空间中的位置。
4. **识别空白与机会**：发现当前 {PROJECT_NAME} 未覆盖但可迁移的技术。
5. **给出适配建议**：将调研结论转化为具体行动或进一步实验。

---

## 1. 任务范围冻结 (CTX)

```markdown
(CTX) 当前任务：<一句话>
(CTX) 调研主题：<例如 自动微分技术、内存池设计、调度算法>
(CTX) 调研目标：<选型 / 可行性评估 / 趋势判断 / 竞品对标>
(CTX) 时间范围：<截至当前 / 近 5 年 / 特定会议周期>
(CTX) 硬约束：<核心 DSL 不可省略、禁止未标注来源的断言、必须量化置信度>
(HITL) 当前决策点：<若建议引入新依赖或改变技术路线，必须停止确认>
```

---

## 2. 信息收集 (R)

### 2.1 必须收集的内容

- 官方文档、论文、Release Notes。
- 竞品或参考实现的关键代码片段。
- 社区讨论、issue、RFC、演讲幻灯片。
- 相关 MEM 和 skill。
- 历史采纳或弃用类似技术的案例。

### 2.2 来源分级

| 等级 | 含义 | 置信度 |
| ---- | ---- | ------ |
| S0 | 官方文档、论文原文、正式发布说明 | high |
| S1 | 核心维护者博客/演讲、权威技术书籍 | medium-high |
| S2 | 高质量技术文章、知名会议演讲 | medium |
| S3 | 社区讨论、StackOverflow、GitHub issue | low-medium |
| S4 | 模型先验、二手总结、未验证猜测 | low |

### 2.3 引用格式

```markdown
(SOURCE) <编号>
- 标题: ...
- 作者/机构: ...
- 日期: ...
- 等级: S<N>
- URL/路径: ...
- 关键论断: <直接引用或摘要>
- 可信度: (CONF: <level>, S<N>)
```

---

## 3. 问题建模 (T)

### 3.1 调研问题分解

```markdown
(QUESTION) Q<N>: <子问题>

- 与主任务的关系: ...
- 理想答案应包含: ...
- (PREDICTION) 基于当前信息的预期答案: ...
- (FALSIFICATION) 什么证据会推翻此预期: ...
```

### 3.2 问题空间地图

```markdown
(LANDSCAPE)

- 维度 1: <例如 性能 vs 可移植性>
- 维度 2: <例如 成熟度 vs 创新性>
- 方案 A: <在地图中的位置，适用场景>
- 方案 B: ...
- {PROJECT_NAME} 当前位置: ...
- 空白区域 (GAP): <未被覆盖但有价值的区域>
```

---

## 4. 交叉验证 (E)

### 4.1 验证策略

- **来源三角验证**：同一论断是否有至少两个独立来源支持。
- **代码验证**：若方案开源，读取关键实现片段验证文档声明。
- **实验验证**：若可能，构造最小原型验证核心 claim。
- **历史验证**：该方案在类似项目中是否成功/失败。

### 4.2 验证格式

```markdown
(EXP-<编号>) 验证 <论断>

- 目标: <验证/推翻哪个论断>
- 方法: <来源三角 / 代码阅读 / 原型实验 / 历史案例>
- 来源/输入: ...
- (PREDICTION) 若论断成立，应观察到: ...
- (PREDICTION) 若论断不成立，应观察到: ...
- (FALSIFICATION) 什么结果会推翻论断: ...
- 验证后必须输出: (OBSERVATION) + (VERDICT)
```

---

## 5. 观察更新 (OU)

```markdown
(OU) [YYYY-MM-DD HH:MM:SS] EXP-<编号> 结果

- (OBSERVATION) 实际结果: <来源内容 / 代码片段 / 实验输出>
- 与预测差异: <量化或明确差异>
- (VERDICT) 论断裁决:
  - <论断>: 成立 / 被推翻 / 部分成立 / 待验证
- 若被推翻:
  - (H_FAILED) 原论断: ...
  - (H_FAILED) 原预测: ...
  - (H_FAILED) 实际证据: ...
  - (H_FAILED) 更新后论断: ...
```

---

## 6. 总结与报告 (M)

### 6.1 报告结构

调研报告写入 `{MEMORY_DIR}/reports/YYYY-MM-DD/research-survey-<title>.md`：

```markdown
# 调研报告：<标题>

## 1. 调研问题

## 2. 来源清单与分级

## 3. 技术地图 (LANDSCAPE)

## 4. 各方案对比

| 方案 | 核心思想 | 优势 | 劣势 | 成熟度 | 与 {PROJECT_NAME} 适配度 |
| ---- | -------- | ---- | ---- | ------ | ---------------- |
| A    | ...      | ...  | ...  | ...    | ...              |

## 5. 关键发现

## 6. 空白与机会 (GAP)

## 7. 适配建议

## 8. 下一步行动

## 9. 对抗思考 (ADV)

## 10. 置信度衰减说明
```

### 6.2 适配建议格式

```markdown
(ADAPTATION) A<N>: <建议一句话>

- 适用场景: ...
- 前置条件: ...
- 预期收益: <量化或明确描述>
- 风险: ...
- 验证方式: <下一步实验>
- 优先级: <P0/P1/P2>
```

---

## 7. DSL 标签要求

### 7.1 核心标签（不可省略）

`(CTX)` / `(HITL)` / `(R)` / `(T)` / `(E)` / `(M)` / `(CONF)` / `(AUDIT)` / `(ADV)` / `(HEURISTIC)`

### 7.2 本任务专用标签

```text
(SOURCE)            信息来源
(QUESTION)          调研子问题
(LANDSCAPE)         技术地图
(GAP)               空白与机会
(ADAPTATION)        适配建议
(CONFIDENCE_DECAY)  信息置信度随时间衰减
(CROSS_VALIDATION)  交叉验证
```

---

## 8. 子 Agent 调用

### 8.1 强制调用（MUST）

| 场景 | 角色 | 作用 |
| ---- | ---- | ---- |
| ADV 阶段 | ADVERSARIAL_PAIR | 挑战来源可信度和结论过度泛化 |
| 来源评估后 | SOURCE_RELIABILITY_REVIEWER | 检查来源分级是否合理、是否存在 echo chamber |

### 8.2 建议调用（SHOULD）

| 场景 | 角色 | 作用 |
| ---- | ---- | ---- |
| 生成技术地图后 | LANDSCAPE_REVIEWER | 检查是否遗漏重要方案或维度 |
| 生成 MEM 前 | MEM_DEDUPLICATOR | 检查重复度 |

---

## 9. HITL 触发条件

1. 建议引入新依赖或改变核心技术路线。
2. 调研结论将对外发布或固化为规范。
3. 关键论断主要依赖 S3/S4 来源。
4. 建议对现有代码进行大规模重写。

---

## 10. 正反面示例

### 10.1 来源引用

**Bad**：

```markdown
据说某个新框架比 PyTorch 快 10 倍。
```

**Good**：

```markdown
(SOURCE) S1
- 标题: "TensorFlow 2.x Performance Best Practices"
- 作者: Google TensorFlow Team
- 日期: 2025-03
- 等级: S0
- URL: https://...
- 关键论断: "在 ResNet-50 训练上，XLA 启用后吞吐提升 15-30%"
- 可信度: (CONF: high, S0)
```

### 10.2 适配建议

**Bad**：

```markdown
(ADAPTATION) 我们应该用 XLA。
```

**Good**：

```markdown
(ADAPTATION) A1: 评估将 {PROJECT_NAME} CPU 后端接入 MLIR/XLA 的可行性
- 适用场景: 当 CPU 后端成为性能瓶颈且调度器优化空间耗尽时
- 前置条件: 存在稳定的 MLIR 依赖、{PROJECT_NAME} IR 抽象已稳定
- 预期收益: 在 CNN 类模型上 CPU 吞吐提升 10-30%（需原型验证）
- 风险: 引入重大构建依赖、调试复杂度上升
- 验证方式: 2 周内构建最小端到端原型
- 优先级: P1
```

---

## 11. 与 master-prompt.md 的衔接

层级关系：

```text
meta-data-generation-prompt.md
         ↓
master-prompt.md
         ↓
research-survey-prompt.md  ← 本文件
         ↓
<具体调研任务>
```

---

## 12. 输出目录

- 过程记录：`{MEMORY_DIR}/logs/YYYY-MM-DD/reasoning-<HHMMSS>-research-survey-<title>.md`
- 调研报告：`{MEMORY_DIR}/reports/YYYY-MM-DD/research-survey-<title>.md`
- 知识沉淀：`{MEMORY_DIR}/memories/YYYY-MM-DD/<category>-<title>.md`

---

## 13. 启动指令

收到调研任务后，必须按顺序输出：

1. `(CTX)` 复述任务。
2. 声明 Meta-Prompt 与 master-prompt 已加载。
3. `(DATA_QUALITY)` 自评。
4. `(R)` 收集来源。
5. `(T)` 建立问题空间地图。

禁止在未明确调研问题前开始收集信息。
