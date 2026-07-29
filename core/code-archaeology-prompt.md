# CODE ARCHAEOLOGY PROMPT：代码考古与遗留系统理解协议

> 适用：当 Agent 需要理解缺乏文档、作者已离开、历史沿革复杂的代码模块时使用。目标不是立即修改，而是建立对代码的**可信历史模型**和**演化因果图**。本 prompt 为任务级协议，必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

## 0. 核心目标

代码考古不是读代码，而是**通过代码、提交历史、测试、注释和运行时行为，逆向工程代码为何变成今天这样**。

本协议要求 Agent：

1. **识别考古对象**：明确哪些代码是遗留的、无主的、难以理解或频繁出问题的。
2. **重建历史假设**：对每一段奇怪代码，生成"它为什么存在"的竞争性假设。
3. **用证据约束假设**：通过 git blame、commit message、测试用例、issue 验证假设。
4. **标记知识债务**：明确哪些部分仍不可解释，需要人类补充。
5. **输出可迁移理解**：将学到的模式沉淀为 `(MEM)`，帮助未来开发者避免重复踩坑。

---

## 1. 任务范围冻结 (CTX)

```markdown
(CTX) 当前任务：<一句话>
(CTX) 考古对象：<文件/模块/类/函数>
(CTX) 考古目标：<理解行为 / 定位历史 bug / 评估重构风险 / 补全文档>
(CTX) 时间范围：<代码引入至今 / 特定时间段>
(CTX) 硬约束：<核心 DSL 不可省略、禁止编造历史、必须区分推测与事实>
(HITL) 当前决策点：<若建议删除或重写遗留代码，必须停止确认>
```

---

## 2. 信息收集 (R)

### 2.1 必须收集的内容

- 当前代码完整阅读。
- `git log --follow`、`git blame`、`git log -p -- <file>`。
- 相关 commit message、PR、issue、ADR。
- 相关测试（包括被跳过的、被标记为 TODO 的）。
- 相关 MEM 和 skill。
- 运行时行为（若可行）：打印、日志、调试输出。

### 2.2 证据分级（考古专用）

| 等级 | 含义 | 示例 |
| ---- | ---- | ---- |
| A0 | 代码直接语义 | 函数当前实现 |
| A1 | commit message / PR 描述 | "修复 {BACKEND_A} 异步读取 bug" |
| A2 | 测试用例意图 | 某测试验证了特定边界条件 |
| A3 | issue / 讨论推断 | 用户报告的问题模式 |
| A4 | 推测 / 模型先验 | "看起来像是 workaround" |

---

## 3. 历史假设生成 (T)

### 3.1 假设格式

```markdown
(ARTIFACT) A<N>: <代码片段或设计决策>

- 当前形态: <代码是什么样的>
- 奇怪之处: <为什么看起来不自然>
- (BRANCH) H1: <假设 1：它为何存在> (CONF: <level>, <证据统计>)
- (BRANCH) H2: <假设 2： competing 解释> (CONF: <level>, <证据统计>)
- (BRANCH) H3: <通用假设：历史债务 / 临时 workaround> (CONF: <level>, <证据统计>)
- (FALSIFICATION) 什么证据会推翻 H1: ...
- (PREDICTION) 若 H1 成立，git history 中应出现: ...
```

### 3.2 假设空间要求

- 每个"奇怪"代码片段至少生成 2 个竞争性历史假设。
- 必须包含一个"这是临时 workaround 但未被清理"假设。
- 必须包含一个"这是为了兼容旧行为"假设。

---

## 4. 证据链构建 (E)

### 4.1 证据链格式

```markdown
(EVIDENCE_CHAIN) A<N> / H<x>

- 直接证据:
  - <A0/A1/A2 证据>
- 间接证据:
  - <A3/A4 证据>
- 矛盾证据:
  - <任何与 H<x> 冲突的证据>
- (PREDICTION) 若 H<x> 成立，进一步检查应发现: ...
- (FALSIFICATION) 若发现以下情况，则 H<x> 被推翻: ...
```

### 4.2 常用验证命令

```bash
# 查看文件历史
git log --follow --oneline -- <file>

# 查看特定行最后修改者
git blame -L <start>,<end> <file>

# 查看某次提交完整改动
git show <commit>

# 查看某段代码何时引入
git log -S '<code_snippet>' -- <file>

# 查看相关 issue/PR
git log --grep='<keyword>' --oneline
```

---

## 5. 观察更新 (OU)

```markdown
(OU) [YYYY-MM-DD HH:MM:SS] A<N> 历史验证结果

- (OBSERVATION) 实际证据: <git log / commit message / test / issue>
- 与预测差异: ...
- (VERDICT) 假设裁决:
  - H1: 被支持 / 被推翻 / 待验证
  - H2: 被支持 / 被推翻 / 待验证
- 若被推翻:
  - (H_FAILED) 原假设: ...
  - (H_FAILED) 原预测: ...
  - (H_FAILED) 实际证据: ...
  - (H_FAILED) 更新后假设: ...
```

---

## 6. 遗留代码风险评估

### 6.1 风险维度

| 维度 | 说明 | 评分 |
| ---- | ---- | ---- |
| 理解难度 | 新开发者理解所需时间 | 1-5 |
| 修改风险 | 改动时引入 bug 的概率 | 1-5 |
| 知识债务 | 多少历史原因未被记录 | 1-5 |
| 活跃依赖 | 是否仍在关键路径上 | 1-5 |
| 替代成本 | 替换为清晰实现的成本 | 1-5 |

### 6.2 风险格式

```markdown
(LEGACY_RISK) A<N>

- 理解难度: <分数>，理由: ...
- 修改风险: <分数>，理由: ...
- 知识债务: <分数>，理由: ...
- 活跃依赖: <分数>，理由: ...
- 替代成本: <分数>，理由: ...
- 综合风险: <P0/P1/P2>
- 建议处置: <保留并补文档 / 逐步重构 / 重写 / 隔离>
```

---

## 7. 总结与报告 (M)

### 7.1 报告结构

代码考古报告写入 `{MEMORY_DIR}/reports/YYYY-MM-DD/code-archaeology-<title>.md`：

```markdown
# 代码考古报告：<标题>

## 1. 考古对象与目标

## 2. 代码现状摘要

## 3. 历史时间线

## 4. 关键谜团与假设验证

## 5. 遗留风险矩阵

## 6. 推荐处置方案

## 7. 需要人类补充的知识债务

## 8. 对抗思考 (ADV)

## 9. 可迁移教训 (MEM)
```

### 7.2 知识债务格式

```markdown
(KNOWLEDGE_DEBT)

- 无法解释的现象: ...
- 已尝试的验证: ...
- 需要人类补充的信息: ...
- 若无法补充，建议的保守处置: ...
```

---

## 8. DSL 标签要求

### 8.1 核心标签（不可省略）

`(CTX)` / `(HITL)` / `(R)` / `(T)` / `(E)` / `(M)` / `(CONF)` / `(AUDIT)` / `(ADV)` / `(HEURISTIC)`

### 8.2 本任务专用标签

```text
(ARTIFACT)          代码文物 / 奇怪代码片段
(EVIDENCE_CHAIN)    证据链
(LEGACY_RISK)       遗留风险
(KNOWLEDGE_DEBT)    知识债务
(HISTORICAL_CAUSE)  历史成因
```

---

## 9. 子 Agent 调用

### 9.1 强制调用（MUST）

| 场景 | 角色 | 作用 |
| ---- | ---- | ---- |
| ADV 阶段 | ADVERSARIAL_PAIR | 挑战历史假设，防止事后合理化 |
| 历史假设生成后 | HYPOTHESIS_VALIDATOR | 检查假设是否可证伪、是否有替代假设 |

### 9.2 建议调用（SHOULD）

| 场景 | 角色 | 作用 |
| ---- | ---- | ---- |
| 风险评估后 | LEGACY_RISK_REVIEWER | 检查风险评分是否低估 |
| 生成 MEM 前 | MEM_DEDUPLICATOR | 检查重复度 |

---

## 10. HITL 触发条件

1. 建议删除、重写或迁移遗留代码。
2. 遗留代码涉及安全关键路径。
3. 历史原因无法通过现有证据重建，需要原始作者输入。
4. 处置方案与既有工程约束冲突。

---

## 11. 正反面示例

### 11.1 历史假设

**Bad**：

```markdown
(ARTIFACT) 这段代码看起来是为了兼容旧版本。
```

**Good**：

```markdown
(ARTIFACT) A1: Storage 深拷贝构造函数中显式调用 {BACKEND_A}_flush_wait(true)
- 当前形态: 拷贝构造函数在复制 buffer 前调用全局 flush
- 奇怪之处: 拷贝构造函数通常不应关心设备同步细节
- (BRANCH) H1: 这是为了修复某次 {BACKEND_A} 异步写入未完成的 bug (CONF: medium, A3×1)
- (BRANCH) H2: 这是防御性编程，实际可能不需要 (CONF: low, A4×1)
- (FALSIFICATION) 若 H1 成立，git history 中应存在相关 bug fix commit
- (PREDICTION) 若 H1 成立，commit message 或 PR 中会出现 "async" "copy" "race" 等关键词
```

---

## 12. 与 master-prompt.md 的衔接

层级关系：

```text
meta-data-generation-prompt.md
         ↓
master-prompt.md
         ↓
code-archaeology-prompt.md  ← 本文件
         ↓
<具体考古任务>
```

---

## 13. 输出目录

- 过程记录：`{MEMORY_DIR}/logs/YYYY-MM-DD/reasoning-<HHMMSS>-code-archaeology-<title>.md`
- 考古报告：`{MEMORY_DIR}/reports/YYYY-MM-DD/code-archaeology-<title>.md`
- 知识沉淀：`{MEMORY_DIR}/memories/YYYY-MM-DD/<category>-<title>.md`

---

## 14. 启动指令

收到代码考古任务后，必须按顺序输出：

1. `(CTX)` 复述任务。
2. 声明 Meta-Prompt 与 master-prompt 已加载。
3. `(DATA_QUALITY)` 自评。
4. `(R)` 收集代码与 git 历史。
5. `(T)` 生成历史假设空间。

禁止在仅阅读当前代码后就给出"这段代码应该被重写"的结论。
