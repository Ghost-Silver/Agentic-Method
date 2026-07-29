# REFLECTION PROMPT：{PROJECT_NAME} 反思与记录协议

> 适用：任务结束后的复盘、skill 更新、方法论提炼、错误模式归档、会话日志整理。

---

## 1. 阶段一：事实回放 (R)

### 1.1 (CTX) 复述模板

```markdown
(CTX) 反思对象：<任务 / Bug / 实验 / 设计>
(CTX) 时间范围：<开始 - 结束>
(CTX) 参与 Agent / 子 Agent：<列表>
(CTX) 原始目标：
(CTX) 最终结果：
```

### 1.2 证据回放

1. 读取本次任务的 R/T/E/M 日志。
2. 读取最终报告 / ADR / Bug 报告 / 实验报告。
3. 读取相关 git diff 与测试输出。
4. 收集关键时间戳与决策点。
5. 检索近 30 天内主题相似的 reasoning log 与 MEM，为后续去重与一致性审查做准备。

---

## 2. 阶段二：结构化复盘 (T)

### 2.1 五维复盘框架

```markdown
### 1. 结果复盘

- 目标达成度：
- 关键指标：
- 剩余问题：
- 整体置信度：(CONF: <level>, <证据统计>)

### 2. 过程复盘

- 哪些 (R/T/E/M) 步骤信息收益最高？
- 哪些步骤是弯路？为什么？
- 是否有更好的实验设计？

### 3. 方法复盘

- 哪些方法论有效？（二分、消融、反事实、对照、单元测试、中间变量）
- 哪些方法论被误用或遗漏？
- 隐藏假设审查是否充分？

### 4. 认知复盘

- 最初假设是什么？哪些被推翻？
- 模型是否存在幻觉或过度归因？
- 反事实归因是否足够谨慎？

### 5. 工程复盘

- 代码改动是否最小化？
- 测试覆盖是否充分？
- 文档 / skill 是否及时更新？
```

### 2.2 反事实分析 (CFC)

```markdown
(CFC) 若最初选择另一个假设，会少走多少弯路？
(CFC) 若更早引入某个实验，是否能更快定位？
(CFC) 若某个中间决策被撤回，最终结果是否不同？
```

### 2.3 竞争性解释合并 (BRANCH / MERGE)

```markdown
(BRANCH) 解释 A：任务成功主要归因于实验设计严谨 (CONF: medium, F1×1, F3×1)
(BRANCH) 解释 B：任务成功主要归因于问题本身较为简单 (CONF: low, F4×1)
(MERGE) 综合：解释 A 有更多证据支持，但不能完全排除解释 B；建议未来遇到更复杂问题时复用当前方法以验证。
```

---

## 3. 阶段三：沉淀与更新 (E)

### 3.1 Skill / Prompt / MEM 更新规则

根据 `main.md` 要求：

1. 每个 skill 条目后注明更新日期。
2. 每个 prompt 条目后注明更新日期。
3. 每个 MEM 文件必须经过去重审查。
4. 在 `main.md` 目录部分新增或更新对应条目说明。
5. 只沉淀可复用的经验、方法、坑，不沉淀一次性细节。
6. 新增/更新 skill 或 prompt 后，必须在 (M) 阶段输出 `(AUDIT) 已更新 main.md 目录：<文件名> 更新日期 YYYY-MM-DD`。

#### 3.1.1 子 Agent MEM 去重审查（强制）

生成新 MEM 前，必须调用 **MEM_DEDUPLICATOR**：

```markdown
(SUB) [YYYY-MM-DD HH:MM:SS] MEM_DEDUPLICATOR | 审查新 MEM 是否重复
输入: 新 MEM 的 Rule/When/Because；memories/YYYY-MM-DD/ 下近 30 天条目列表
约束: 重复度 >80% 时必须建议合并；必须给出最相似的已有 MEM

(SUB-OUTPUT) [YYYY-MM-DD HH:MM:SS]
(SUB-MEM-DEDUP)

- 重复度评分: 0-100
- 最相似的已有 MEM: <路径>
- 建议: 新建 / 合并到已有 / 更新已有
- 理由: ...

(SUB-VERDICT) [YYYY-MM-DD HH:MM:SS]

- 采纳: ...
- 若建议合并/更新，具体修改计划: ...
```

#### 3.1.2 日志层去重审查（强制）

整理本次 reasoning log 或会话日志前，必须检查是否存在主题高度重复的历史日志：

```markdown
(TRAJECTORY_DEDUP) [YYYY-MM-DD HH:MM:SS]

- 近 30 天相似日志: <路径列表>
- 本次新增洞察: <与历史日志相比，本次新增了哪些认知>
- 若新增洞察为空或高度重复，建议: 合并到历史日志 Related Logs / 不新建文件
- 若必须新建，差异点说明: ...
```

**禁止**：无新增洞察却新建独立日志。

#### 3.1.3 跨任务一致性审查（强制）

生成新 MEM 前，必须检查本次结论与已有 MEM 是否冲突：

```markdown
(CROSS_TASK_CONSISTENCY) [YYYY-MM-DD HH:MM:SS]

- 本次核心结论: ...
- 冲突的已有 MEM: <路径>
- 冲突性质: 真正矛盾 / 边界条件不同 / 无冲突
- 处理方案: 更新已有 MEM 的 When/Failure cases / 新建边界说明 MEM / 无需处理
```

**示例**：若已有 MEM 认为"{BACKEND_A} 同步越多越好"，本次发现"过度同步降低性能"，必须解释边界条件（小模型 vs 大模型）。

### 3.2 沉淀内容模板

```markdown
## <经验标题>

**更新日期**：YYYY-MM-DD

**场景**：
**现象**：
**根因**：
**方法**：
**修复 / 方案**：
**验证**：
**教训**：
```

### 3.3 会话日志整理

将本次会话的 R/T/E/M 日志整理为 `{MEMORY_DIR}/sessions/YYYY-MM-DD/session-<id>.md`，其中 `<id>` 可使用本次会话标识或首次记录时间 `HHMMSS`。包含：

1. 关键 prompt 列表。
2. 核心修改与验证结果。
3. 性能数据（若有）。
4. 方法与逻辑总结。
5. 下一步建议。
6. 本次新增/更新的 skill 或 prompt 清单，以及 `main.md` 更新记录。

**注意**：项目根目录下若存在历史 `session-prompt-log.md`，可继续保留作为索引引用，但新的会话主副本必须写入 `skills/sessions/YYYY-MM-DD/`。

---

## 4. 阶段四：输出与确认 (M)

### 4.0 预测能力审计 (PREDICTION_AUDIT)

复盘时必须检查本次任务是否包含高质量预测-验证循环：

```markdown
(PREDICTION_AUDIT)

- 本次任务中 (MODEL_PREDICTION) 数量: <N>
- 被 (MODEL_ERROR) 验证的数量: <N>
- 预测准确率: <正确 / 部分正确 / 错误 / 未做预测>
- 错误预测是否导致 (MODEL_UPDATE):
- 若未做预测，原因:
  - [ ] 任务性质不适合预测（如纯信息收集）
  - [ ] 遗漏了应有的预测机会
- 改进建议: <下次应在哪些节点插入预测>
```

**规则**：对于需要理解环境动力学的任务，长期缺乏 (MODEL_PREDICTION) 的复盘视为不完整。

### 4.1 复盘报告

写入 `{MEMORY_DIR}/reports/YYYY-MM-DD/reflection-<YYYYMMDD>-<title>.md`：

```markdown
# 复盘报告：<标题>

## 1. 任务概述

## 2. 关键时间线

## 3. 结果与指标

## 4. 五维复盘

## 5. 反事实分析 (CFC)

## 6. 竞争性解释合并 (BRANCH / MERGE)

## 7. Skill 更新清单

## 8. 对抗思考 (ADV)

## 9. 后续行动项

- 行动项：
- 优先级：
- 置信度：(CONF: <level>, <证据统计>)
```

### 4.2 对抗思考 (ADV)

```markdown
(ADV) 本次复盘是否遗漏了重要失败信号？
(ADV) 提炼的方法论是否过度泛化？
(ADV) 是否有其他项目/模块能从本次经验受益？
(ADV) 本次记录是否足够让未来 Agent 复现推理过程？
```

#### 4.2.1 子 Agent 形式审查（强制）

最终输出前，调用 **FORM_REVIEWER**：

```markdown
(SUB) [YYYY-MM-DD HH:MM:SS] FORM_REVIEWER | 审查复盘报告格式
输入: 当前复盘报告与 reasoning log 的完整输出
约束: 只审查格式和结构，不审查内容正确性

(SUB-OUTPUT) [YYYY-MM-DD HH:MM:SS]
(SUB-FORM)

- 缺失标签: <例如：缺少 (CONF)、缺少 (CFC)>
- 格式违规: <例如：Delta 描述法枚举了物理位置>
- 建议修正: ...

(SUB-VERDICT) [YYYY-MM-DD HH:MM:SS]

- 采纳: ...
- 拒绝: ...
```

### 4.3 预测准确率趋势审查 (PREDICTION_TREND_REVIEW)

复盘时必须检查 Agent 的预测能力是否出现系统性退化：

```markdown
(PREDICTION_TREND_REVIEW) [YYYY-MM-DD HH:MM:SS]

- 任务类型: <debug / perf / world-model / 新模块 / ...>
- 近 N 次同类任务的 (MODEL_PREDICTION) 数量: <N>
- 近 N 次同类任务的预测准确率趋势:
  - 第 1 次: <正确/部分正确/错误>
  - 第 2 次: <正确/部分正确/错误>
  - ...
- 是否出现连续下降? <是/否>
- 若连续 ≥2 次错误或部分正确，标记: (PREDICTION_DRIFT_ALERT)
- 可能原因:
  - [ ] 世界模型过时（环境已变化但模型未更新）
  - [ ] 过度泛化（把特定场景规则用到了不适用场景）
  - [ ] 隐藏变量未建模
  - [ ] 预测本身过于模糊，无法证伪
- 建议动作:
  - 触发 `(WORLD_PROBE)` 重新校准世界模型
  - 触发 `(HITL)` 请求人类审核当前世界模型
  - 更新/废弃相关 MEM
```

**HITL 升级规则**：

- 同类任务连续 2 次预测错误 → 在复盘中自动标记 `(PREDICTION_DRIFT_ALERT)`。
- 同类任务连续 3 次预测错误 → 必须触发 `(HITL)`，请求人类审核世界模型和相关 MEM。
- 涉及安全关键场景（如 {BACKEND_A} 同步、内存管理）的预测错误 → 即使只有 1 次，也必须 HITL 审核。

---

## 5. (HITL) 决策门

1. 更新 `main.md` 或项目级 skill 前必须确认。
2. 归档失败或敏感实验数据前必须确认。
3. 将复盘结论固化为工程规范前必须确认。
4. 复盘发现重大认知偏差或归因错误且需要修正历史结论时必须确认。

### 5.1 HITL_REJECTED 记录

若人类否决了复盘结论、skill 更新、归因解释或历史结论修正，必须立即记录 `(HITL_REJECTED)`：

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
