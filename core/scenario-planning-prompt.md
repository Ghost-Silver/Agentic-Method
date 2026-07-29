# SCENARIO PLANNING PROMPT：情景规划与风险预案协议

> 适用：当 Agent 需要为未来不确定性建模、制定应急预案、评估技术演进风险时使用。典型场景包括：硬件/后端弃用、依赖 BREAKING CHANGE、政策或生态位变化、竞争格局迁移。本 prompt 为任务级协议，必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

## 0. 核心目标

情景规划不是预测未来，而是**为多种可能的未来做准备**。

本协议要求 Agent：

1. **生成结构化情景**：不是单一预测，而是多个相互排斥但各自自洽的未来情景。
2. **明确触发条件**：每个情景必须说明什么事件或信号会激活它。
3. **量化影响**：评估每个情景对项目目标、成本、进度的影响。
4. **制定预案**：为每个高影响情景准备具体应对动作。
5. **持续监控**：定义早期信号和复核触发条件。

---

## 1. 任务范围冻结 (CTX)

```markdown
(CTX) 当前任务：<一句话>
(CTX) 规划主题：<例如 {BACKEND_A} 后端未来、依赖演进、竞争格局>
(CTX) 时间范围：<短期 0-6 个月 / 中期 6-18 个月 / 长期 18 个月以上>
(CTX) 决策目标：<制定预案 / 评估投资 / 选择技术路线 / 风险披露>
(CTX) 硬约束：<核心 DSL 不可省略、禁止单一预测、必须量化影响>
(HITL) 当前决策点：<若结论将触发重大资源投入或战略转向，必须停止确认>
```

---

## 2. 信息收集 (R)

### 2.1 必须收集的内容

- 当前技术栈和依赖版本状态。
- 相关技术趋势、发布计划、官方路线图。
- 竞争对手或生态主导者的动向。
- 历史类似事件及其后果（如 Apple 弃用 OpenCL、某库 BREAKING CHANGE）。
- 相关 MEM 和 skill。

### 2.2 信息来源分级

| 等级 | 含义 | 置信度 |
| ---- | ---- | ------ |
| S0 | 官方公开路线图 / 正式公告 | high |
| S1 | 权威社区讨论 / 核心维护者发言 | medium-high |
| S2 | 行业分析报告 / 趋势观察 | medium |
| S3 | 间接信号 / 专利 / 招聘动态 | low-medium |
| S4 | 猜测 / 模型先验 | low |

---

## 3. 情景生成 (T)

### 3.1 情景格式

```markdown
(SCENARIO) S<N>: <情景一句话标题>

- 时间范围: <何时可能发生>
- 触发条件 (TRIGGER): <什么事件激活此情景>
- 关键假设:
  - <假设 A> (CONF: <level>)
  - <假设 B> (CONF: <level>)
- 对项目的影响:
  - 正面: ...
  - 负面: ...
  - 概率估计: <若可量化，如 20-40%；否则 high/medium/low>
- 置信度: (CONF: <level>, <证据统计>)
- (PREDICTION) 若此情景发生，6 个月内可观测的信号: ...
```

### 3.2 情景空间要求

- 至少生成 **3 个情景**：
  - 一个**基准情景**（最可能延续当前趋势）。
  - 一个**乐观情景**（有利变化加速）。
  - 一个**悲观情景**（不利冲击发生）。
- 情景之间必须**相互排斥**或至少在关键变量上不同。
- 每个情景必须包含可证伪的触发条件。

---

## 4. 影响评估 (E)

### 4.1 评估维度

| 维度 | 说明 | 评分 |
| ---- | ---- | ---- |
| 技术影响 | 是否需要重写核心模块、引入新依赖 | 1-5 |
| 性能影响 | 对训练/推理吞吐、延迟的潜在影响 | 1-5 |
| 维护成本 | 长期维护复杂度变化 | 1-5 |
| 生态影响 | 对用户、贡献者、合作伙伴的影响 | 1-5 |
| 不可逆性 | 一旦走错，回滚难度 | 1-5 |

### 4.2 评估格式

```markdown
(IMPACT) S<N>

- 技术影响: <分数>，理由: ...
- 性能影响: <分数>，理由: ...
- 维护成本: <分数>，理由: ...
- 生态影响: <分数>，理由: ...
- 不可逆性: <分数>，理由: ...
- 综合风险等级: <P0/P1/P2>
- (PREDICTION) 若现在开始准备，6 个月后项目状态应如何: ...
```

---

## 5. 预案设计 (CONTINGENCY)

### 5.1 预案格式

```markdown
(CONTINGENCY) S<N>

- 触发条件: <何时启动本预案>
- 早期信号 (EARLY_SIGNAL):
  - <信号 1>: <何时出现、如何监测>
  - <信号 2>: ...
- 应对动作:
  - 立即动作: ...
  - 30 天内动作: ...
  - 90 天内动作: ...
- 所需资源: ...
- 回退方案: <若预案失败怎么办>
- 决策负责人: <Agent / Human / 待定>
```

### 5.2 无悔行动 (NO-REGRET ACTION)

无论哪个情景发生都有价值的行动：

```markdown
(NO-REGRET)

- 行动: ...
- 为什么在各情景下都有价值: ...
- 成本: ...
- 优先级: <P0/P1/P2>
```

---

## 6. 观察更新 (OU)

```markdown
(OU) [YYYY-MM-DD HH:MM:SS] 情景复核

- (OBSERVATION) 最新信号: <行业动态、依赖更新、硬件发布>
- 与此前预测差异: ...
- (VERDICT) 情景概率更新:
  - S1: <old> → <new>
  - S2: <old> → <new>
- 若某情景被证伪:
  - (H_FAILED) 原情景: ...
  - (H_FAILED) 原预测: ...
  - (H_FAILED) 实际信号: ...
  - (H_FAILED) 更新后情景: ...
```

---

## 7. 总结与报告 (M)

### 7.1 报告结构

情景规划报告写入 `{MEMORY_DIR}/reports/YYYY-MM-DD/scenario-planning-<title>.md`：

```markdown
# 情景规划报告：<标题>

## 1. 规划背景与范围

## 2. 当前状态快照

## 3. 情景矩阵

| 情景 | 概率 | 技术影响 | 维护成本 | 综合风险 | 触发条件 |
| ---- | ---- | -------- | -------- | -------- | -------- |
| S1   | ...  | ...      | ...      | ...      | ...      |

## 4. 预案清单

## 5. 无悔行动

## 6. 监控信号与复核计划

## 7. 对抗思考 (ADV)

## 8. 推荐决策
```

---

## 8. DSL 标签要求

### 8.1 核心标签（不可省略）

`(CTX)` / `(HITL)` / `(R)` / `(T)` / `(E)` / `(M)` / `(CONF)` / `(AUDIT)` / `(ADV)` / `(HEURISTIC)`

### 8.2 本任务专用标签

```text
(SCENARIO)        情景
(TRIGGER)         触发条件
(EARLY_SIGNAL)    早期信号
(CONTINGENCY)     应急预案
(NO-REGRET)       无悔行动
(IMPACT)          影响评估
(REGRET)          后悔值分析
(PREDICTION)      情景发生后的可观测预测
(OBSERVATION)     实际信号
(VERDICT)         情景概率裁决
(H_FAILED)        情景被证伪
```

---

## 9. 子 Agent 调用

### 9.1 强制调用（MUST）

| 场景 | 角色 | 作用 |
| ---- | ---- | ---- |
| ADV 阶段 | ADVERSARIAL_PAIR | 挑战概率估计和隐藏假设 |
| 情景生成后 | SCENARIO_DIVERGENCE_REVIEWER | 检查情景是否真正互斥、是否遗漏黑天鹅 |

### 9.2 建议调用（SHOULD）

| 场景 | 角色 | 作用 |
| ---- | ---- | ---- |
| 影响评估后 | IMPACT_REVIEWER | 检查影响评分是否低估或高估 |
| 生成 MEM 前 | MEM_DEDUPLICATOR | 检查重复度 |

---

## 10. HITL 触发条件

1. 结论建议重大资源投入或战略转向。
2. 结论将固化为公开路线图或对外承诺。
3. 情景涉及安全、合规或法律风险。
4. 信息来源主要为 S3/S4，置信度不足。

---

## 11. 正反面示例

### 11.1 情景

**Bad**：

```markdown
(SCENARIO) 未来 {BACKEND_A} 可能会被淘汰。
```

**Good**：

```markdown
(SCENARIO) S1: Apple 在 24 个月内发布 {BACKEND_B} 新 API 并 deprecated {BACKEND_A}Graph
- 时间范围: 18-30 个月
- 触发条件 (TRIGGER): Apple 官方文档或 WWDC 明确标记 {BACKEND_A}Graph 为 deprecated
- 关键假设:
  - 新 API 提供同等或更优的自动微分能力 (CONF: medium, S2×2)
  - {PROJECT_NAME} 当前 {BACKEND_A} 实现深度依赖 {BACKEND_A}Graph (CONF: high, F0×5)
- 对项目的影响:
  - 正面: 可能获得更好性能
  - 负面: 需要重写 {BACKEND_A} 后端，预计 2-3 人月
  - 概率估计: low (10-20%)
- 置信度: (CONF: medium, S2×2, S3×1)
- (PREDICTION) 若此情景发生，未来 6 个月会出现 Apple 预览版 API 和迁移指南
```

---

## 12. 与 master-prompt.md 的衔接

层级关系：

```text
meta-data-generation-prompt.md
         ↓
master-prompt.md
         ↓
scenario-planning-prompt.md  ← 本文件
         ↓
<具体规划任务>
```

---

## 13. 输出目录

- 过程记录：`{MEMORY_DIR}/logs/YYYY-MM-DD/reasoning-<HHMMSS>-scenario-planning-<title>.md`
- 规划报告：`{MEMORY_DIR}/reports/YYYY-MM-DD/scenario-planning-<title>.md`
- 知识沉淀：`{MEMORY_DIR}/memories/YYYY-MM-DD/<category>-<title>.md`

---

## 14. 启动指令

收到情景规划任务后，必须按顺序输出：

1. `(CTX)` 复述任务。
2. 声明 Meta-Prompt 与 master-prompt 已加载。
3. `(DATA_QUALITY)` 自评。
4. `(R)` 收集趋势与依赖信息。
5. `(T)` 生成情景空间。

禁止只输出单一预测。
