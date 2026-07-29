<div align="center">

# Agentic Method · 智能体方法论

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Prompts](https://img.shields.io/badge/Prompts-30%20core-green)](./core)
[![Examples](https://img.shields.io/badge/Examples-12-orange)](./examples)
[![Methodology](https://img.shields.io/badge/Methodology-OHEOU--KU-purple)]()

**一套严谨、证据驱动的自主智能体方法论。**  
**由 CTorch Agent 验证。**

<p align="center">
  <b>观察 → 假设 → 实验 → 观测更新 → 知识更新</b><br/>
  <b>Observation → Hypothesis → Experiment → Observation Update → Knowledge Update</b>
</p>

[English Version](./README.en.md)

</div>

---

## 这是什么？

`Agentic Method` 是一组元提示词（meta-prompts）与子智能体协议，面向高风险的工程、研究与决策任务。它不是轻量级的聊天提示词库，而是一套工作流系统，强制智能体：

1. **冻结上下文**后再行动。
2. 生成**竞争性假设**，而非单一答案。
3. 在实验前做出**可证伪的量化预测**。
4. 报告**观测与裁决**，而非仅有结论。
5. **归档失败**并诚实更新世界模型。
6. 通过受控的并行评测**进化自身提示词**。

## 设计原理

当前的中低端模型已经具备足够强的**指令遵循能力**，其真正落后于高端模型的地方是**零样本推理能力**。然而，即使是高端模型，在面对大型代码开发或复杂科研问题时，也难免产生逻辑谬误与模型幻觉。

`Agentic Method` 通过以下机制解决这一问题：

- **严格 DSL 锚定**：用 `(CTX)`、`(H)`、`(EXP)`、`(PREDICTION)`、`(OBSERVATION)`、`(VERDICT)` 等标签将模型的解码空间约束到特定任务区域，显著降低幻觉。
- **强制深层推理**：每个关键结论必须附带置信度 `(CONF)` 与证据等级，模型不能停留在表面回答。
- **子 Agent 交叉审查**：通过 `FORM_REVIEWER`、`HYPOTHESIS_VALIDATOR`、`COUNTEREXAMPLE_REVIEWER` 等角色识别循环论证、隐藏假设与事后合理化。
- **引入科研方法**：反事实推理、二分实验、消融实验、对照实验、思想实验等方法被显式嵌入工作流，强制模型进行高阶思考。

本质上，我们不是让模型“更聪明”，而是让模型的思考过程**更可观测、可证伪、可审计**。

## 模型要求与成本策略

### 推荐配置

为完整运行本协议中的复杂任务（尤其是涉及多文件代码审查、架构决策、长链条因果推理），推荐使用：

- **参数量**：200B+
- **上下文窗口**：200K+
- **能力**：强指令遵循、长上下文稳定、支持工具调用（用于子 Agent）

### 降低成本的关键策略

本协议会消耗大量 token 与上下文，但这种消耗对任务质量的提升是显著的。最佳实践是**按需加载 + 模型路由**：

- **主 Agent / 编排层**：使用最强模型，负责任务分解、假设生成、最终裁决。
- **子 Agent / 审查层**：使用更便宜的模型，负责格式审查、假设验证、反例构造等子任务。
- **按需加载**：不要让 Agent 一次性加载全部 prompt。让它先读取 `main.md`，再根据当前任务类型加载对应的核心 prompt。
- **定时进化**：在每天空闲时间运行 `prompt-evolution-prompt.md` 对已有 prompt 进行 PEL 迭代。

在良好 prompt 的加持下，中等模型在特定子任务上可以接近甚至媲美更高级模型。

## 推荐工作流

```
Step 1: Agent 读取 main.md，理解全局协议与可用 prompt 目录
        ↓
Step 2: 用户告诉 Agent 当前环境（项目类型、偏好、硬约束、目标）
        ↓
Step 3: Agent 自动选择并填充适配后的 prompt
        ↓
Step 4: 运行任务，必要时调用子 Agent
        ↓
Step 5: 任务结束后，Agent 整理资料、归纳经验、生成 MEM
        ↓
Step 6: 在空闲时间运行 PEL，迭代优化 prompt（建议至少 2 轮）
```

## 适用领域

`Agentic Method` 最初为**软件开发**和**科研推理**场景设计，特别适用于：

- 代码审查与重构
- 复杂 Bug 排查
- 性能优化与实验设计
- 架构决策与技术调研
- 论文/研究报告的因果论证

对于其他领域，欢迎参考 `ADAPTATION_GUIDE.md` 进行适配，也欢迎贡献你的适配案例。

## 项目缘起

`Agentic Method` 最初是为 **CTorch Agent** 设计的一套内部工作流，用于在 CTorch 深度学习框架的代码审查、Bug 排查、性能优化和架构决策中约束 Agent 的推理过程。经过多轮实战验证后，我们将其中与项目无关的通用方法论抽象出来，脱敏并开源。

CTorch Agent 仍然是 Agentic Method 的一个**参考实现**：它在系统编程、HPC 后端、自动微分等高风险场景中证明了这套方法论的价值。如果你在类似的工程领域工作，可以直接参考 `examples/mems/` 和 `examples/reports/` 中的脱敏案例。

## 仓库结构

```
agentic-method/
├── core/                        # 30 个通用协议提示词
│   ├── master-prompt.md         # 总控协议
│   ├── meta-data-generation-prompt.md
│   ├── prompt-evolution-prompt.md
│   ├── experimental-design-prompt.md
│   ├── logical-inference-prompt.md
│   ├── subagent-protocol.md
│   ├── prompt-review-prompt.md
│   ├── reflection-prompt.md
│   ├── code-review-prompt.md
│   ├── cpp-code-review-prompt.md
│   ├── debug-prompt.md
│   ├── performance-optimization-prompt.md
│   ├── algorithm-correctness-prompt.md
│   ├── semantic-regression-test-prompt.md
│   ├── semantic-change-regression-prompt.md
│   ├── world-model-learning-prompt.md
│   └── ... 等 30 个核心 prompt
├── main.md                      # 自动生成的 prompt 目录索引
├── examples/                    # 12 个示例（适配案例 + MEM + 报告）
│   ├── software-engineering-review-example.md
│   ├── research-survey-example.md
│   ├── large-model-inference-gap-example.md
│   ├── mems/                    # 6 个脱敏后的可迁移知识示例
│   │   ├── counterfactual-single-variable-principle.md
│   │   ├── semantic-change-full-regression.md
│   │   ├── prompt-evolution-failures.md
│   │   ├── operator-addition-abi-checklist.md
│   │   ├── backend-dtype-constraint.md
│   │   └── inplace-memory-overlap.md
│   └── reports/                 # 3 个脱敏后的复盘/进化报告示例
│       ├── prompt-evolution-daily-report-example.md
│       ├── new-prompts-reflection-example.md
│       └── large-model-inference-gap-analysis.md
├── .github/                     # Issue / PR 模板
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── ADAPTATION_GUIDE.md          # 如何适配到你的项目
├── CONTRIBUTING.md              # 贡献指南
├── .gitignore
└── LICENSE                      # MIT
```

完整 prompt 列表请见 [`main.md`](./main.md)。

## 快速开始

1. 阅读 `core/master-prompt.md`，理解 DSL 标签与全局规则。
2. 根据任务类型选择核心 prompt（例如 `experimental-design-prompt.md`）。
3. 参考 `ADAPTATION_GUIDE.md` 将其适配到你的项目。
4. 跑一个小型试点任务，检查输出是否遵循 DSL。
5. 使用 `prompt-evolution-prompt.md` 持续变异和优化提示词。

## 自动化与持续进化

`prompt-evolution-prompt.md` 不应该是手动运行的奢侈品。为了真正发挥 PEL 的价值，强烈建议将其**自动化**：

- **GitHub Actions**：通过 `schedule` 事件每天/每周自动触发 PEL 工作流，自动评测变异、生成日报、提交 Draft PR。
- **自托管 cron**：在本地服务器或工作站上设置定时任务，利用空闲 GPU/CPU 运行进化实验。
- **低代码平台**：使用 n8n、Make、Zapier 等工具编排“读取 main.md → 选择种子 prompt → 调用 LLM 生成变异 → 并行评测 → 写入报告”的流程。
- **Agent 框架**：使用 LangChain、LangGraph、AutoGen 等框架实现可复用的 PEL Runner，支持多模型路由、结果持久化、人类审批节点。

自动化目标不是取代人类判断，而是把“哪些 prompt 变体值得看”的筛选工作交给机器，让人类把决策精力放在“是否集成到 core”这一最终环节。

## 测试环境

本协议已在 **TRAE CN** 等集成开发环境中实测，效果良好。

## 贡献指南

项目处于起步阶段，prompt 类型和泛化能力仍有很大扩展空间。我们将持续提供更多领域的**样例适配**和**社区 prompt**，也欢迎你贡献自己的实践：

- 成功将 `Agentic Method` 应用到新的领域（如硬件设计、生物医药、法律研究、游戏开发等）；
- 提交针对特定任务或领域的 adapter prompt；
- 分享使用 PEL 自动进化出的优质 prompt 变体；
- 提供真实任务的成功/失败案例；
- 有任何建议、批评或改进想法。

请在 Issue 中描述你的使用场景，或在 Pull Request 中提交新的 `examples/<domain>-adapter.md` 和 `core/<task>-prompt.md`。在社区的帮助下，我们可以积累越来越多、越来越丰富的 prompt 与最佳实践。

## 许可证

[MIT License](./LICENSE)

---

<div align="center">

**这是开源的力量，祝各位使用愉快！**

</div>
