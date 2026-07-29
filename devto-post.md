# 我们开源了一套让 LLM 真正“学会思考”的方法论

> **Agentic Method** —— 不是更多的 prompt，而是一套让模型输出更可观测、可证伪、可进化的工作流。
>
> GitHub: https://github.com/Ghost-Silver/Agentic-Method

---

## 一个越来越明显的问题

现在的 LLM，尤其是中档模型，**指令遵循能力已经很强了**。你让它按格式输出、按步骤执行、调用工具，它基本都能做到。

但一到复杂任务——比如审查一个多文件代码改动、设计一组对照实验、或者推理一个系统 bug 的根因——模型就开始出现两种典型失败：

1. **幻觉**：自信地给出没有依据的结论。
2. **事后合理化**：先跳到一个答案，再编造一个看似合理的推理过程（fake CoT）。

这些不是模型“不够聪明”，而是模型的**解码空间太大**，没有足够的外部约束把它锚定在“正确思考”的轨道上。

---

## 我们的思路：用方法论约束解码空间

我们开源的 **Agentic Method**，本质上不是一套“提示词合集”，而是一套**元工作流（meta-workflow）**。它通过四个机制，把模型的思考过程外化、结构化、可审计：

### 1. 严格 DSL 锚定

用类似 `(CTX)`、`(H)`、`(PREDICTION)`、`(OBSERVATION)`、`(VERDICT)` 的标签，强制模型在每个关键节点声明：

- 当前上下文是什么？
- 假设是什么？
- 可证伪的预测是什么？
- 实际观测到了什么？
- 最终裁决是什么？

这能把模型的输出从“自由作文”变成“结构化科研记录”，显著降低幻觉。

### 2. 强制深层推理

每个关键结论必须附带：

- 证据等级（F0-F4）
- 置信度 `(CONF: <level>, <证据统计>)`
- 至少一个竞争假设 `(BRANCH)`
- 明确的证伪条件 `(FALSIFICATION)`

模型不能再停留在表面回答。

### 3. 子 Agent 交叉审查

通过 `FORM_REVIEWER`、`HYPOTHESIS_VALIDATOR`、`COUNTEREXAMPLE_REVIEWER` 等角色，让不同 Agent 互相挑错。循环论证、隐藏假设、事后合理化会被显式标记出来。

### 4. 引入科研方法

二分、消融、对照、反事实推理——这些方法不是作为“建议”写在文档里，而是作为**不可跳过的步骤**嵌入 prompt。

---

## 30 个核心 prompt，覆盖高风险任务

仓库里包含了 30 个已经脱敏、可直接复用的核心 prompt：

- `experimental-design-prompt.md`：设计可验证的实验
- `logical-inference-prompt.md`：严格逻辑推理与证明审查
- `code-review-prompt.md`：系统性代码审查
- `debug-prompt.md`：因果排查与修复
- `performance-optimization-prompt.md`：性能优化决策
- `prompt-evolution-prompt.md`：**让 prompt 自己进化自己**
- `subagent-protocol.md`：18 个子 Agent 角色的协作协议
- ……以及更多

所有 prompt 都遵循同一套 DSL，可以按需加载、组合、演化。

---

## Prompt 自动进化（PEL）

最有意思的部分可能是 **Prompt Evolution Loop（PEL）**。

它的思路很简单：对同一个种子 prompt，自动生成多个变异版本，用同一组真实任务并行评测，然后保留适应度最高的变体。

我们已经在示例报告中展示了一次真实的 PEL 运行结果：

- `CONSTRAINT_ADD` 算子修复了一个 P0 级协议一致性缺陷；
- `ANTI_PATTERN_BLOCK` 算子因为与既有规则矛盾而被废弃；
- `EXAMPLE_INJECT` 算子需要与清单化调用点结合才有效。

这些结论本身，就是 prompt 工程从“玄学”走向“可实验科学”的证据。

---

## 推荐配置

这套方法论是为了高风险任务设计的，会消耗更多 token 和上下文。但我们认为值得。

- **主 Agent / 编排层**：推荐 200B+、200K+ 上下文的强模型；
- **子 Agent / 审查层**：可以用更便宜的中等模型；
- **运行方式**：先读 `main.md`，再按需加载对应 prompt。

---

## 适用场景

- 复杂代码审查与架构决策
- Bug 根因排查
- 性能优化实验设计
- 科研论证与技术调研
- 任何“说错一句话代价很高”的任务

---

## 开源，MIT 协议

我们希望这套方法能被更多人验证、改进、应用到不同领域。

如果你：

- 成功把它用到了软件工程或科研之外的领域；
- 用 PEL 进化出了更好的 prompt 变体；
- 发现了某个 prompt 的漏洞；

欢迎在 GitHub 上开 Issue 或 PR。社区会一起积累更多领域的 adapter 和最佳实践。

---

## 下一步

1. 打开仓库：https://github.com/Ghost-Silver/Agentic-Method
2. 从 `core/master-prompt.md` 开始读
3. 选一个你正在头疼的复杂任务，试试 `experimental-design-prompt.md` 或 `debug-prompt.md`
4. 如果有效，回来点个 ⭐，或者分享你的使用案例

---

**这不是又一个 prompt 仓库。这是一套让 LLM 学会像科研人员一样思考的工作流。**

https://github.com/Ghost-Silver/Agentic-Method
