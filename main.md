# Agentic Method 主索引

本文件是 Agent 的入口索引。Agent 应首先读取本文件，了解当前可用的 prompt 目录，
然后根据任务类型加载对应的核心 prompt。

## 使用方式

1. 读取 `core/master-prompt.md`，理解 DSL 标签与全局规则。
2. 根据任务类型，从下方目录中选择合适的 prompt。
3. 参考 `ADAPTATION_GUIDE.md` 将其适配到你的项目。
4. 使用过程中产生的新知识，请沉淀到 `{MEMORY_DIR}/memories/YYYY-MM-DD/`。

## Prompt 目录

### [core/algorithm-correctness-prompt.md](core/algorithm-correctness-prompt.md) - ALGORITHM CORRECTNESS PROMPT：代码级算法正确性审查协议

适用：当 Agent 需要对 {PROJECT_NAME} 代码级算法正确性进行严格审查与形式化论证时使用。本 prompt 聚焦**具体代码实现**中的算法正确性，而非脱离代码的纯抽象逻辑推理。必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

### [core/api-design-prompt.md](core/api-design-prompt.md) - API DESIGN PROMPT：{PROJECT_NAME} 公共 API 与接口设计协议

适用：新增公共 C++ API、ABI 稳定性设计、序列化格式、错误码与异常策略、运算符重载、后端抽象接口。

---

### [core/architecture-prompt.md](core/architecture-prompt.md) - ARCHITECTURE PROMPT：{PROJECT_NAME} 架构设计与重构协议

适用：模块划分、接口设计、调度策略、内存模型、异构执行模型、重构等影响系统结构的决策。

---

### [core/code-archaeology-prompt.md](core/code-archaeology-prompt.md) - CODE ARCHAEOLOGY PROMPT：代码考古与遗留系统理解协议

适用：当 Agent 需要理解缺乏文档、作者已离开、历史沿革复杂的代码模块时使用。目标不是立即修改，而是建立对代码的**可信历史模型**和**演化因果图**。本 prompt 为任务级协议，必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

### [core/code-review-prompt.md](core/code-review-prompt.md) - CODE REVIEW PROMPT：全局代码审查协议

适用：当 Agent 需要对 {PROJECT_NAME} 项目的代码库、模块、PR、commit 或特定改动进行系统性审查时使用。本 prompt 为任务级协议，必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

### [core/compiler-flags-prompt.md](core/compiler-flags-prompt.md) - COMPILER FLAGS PROMPT：{PROJECT_NAME} 编译器标志决策与验证协议

作用：任务级协议 prompt，叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上使用。

---

### [core/cpp-code-review-prompt.md](core/cpp-code-review-prompt.md) - CPP_CODE_REVIEWER：通用 C++ 系统编程代码审查协议

适用：当代码审查对象涉及 C++ 系统编程风险时使用，包括内存安全、并发同步、ABI/链接/API 设计、测试覆盖、语义回归、性能与后端调度等主题。本 prompt 为任务级协议，叠加在 `master-prompt.md` 与 `code-review-prompt.md` 之上执行；若与 {PROJECT_NAME} 深度学习框架专项规则冲突，以 `code-review-prompt.md` 中的 {PROJECT_NAME} 专项规则为准。

---

### [core/debug-prompt.md](core/debug-prompt.md) - DEBUG PROMPT：{PROJECT_NAME} Bug 排查与修复协议

适用：任何程序异常、测试结果不符、运行时错误、数值异常、性能衰退、{BACKEND_A}/CPU 结果不一致等场景。

---

### [core/decision-analysis-prompt.md](core/decision-analysis-prompt.md) - DECISION ANALYSIS PROMPT：{PROJECT_NAME} 多方案决策分析协议

适用：A/B/C 方案选型、是否引入新后端/新依赖、是否重构、技术债优先级排序、资源分配决策。

---

### [core/experimental-design-prompt.md](core/experimental-design-prompt.md) - EXPERIMENT DESIGN PROMPT：严谨实验设计协议

适用：任何需要建立因果结论、验证假设、量化影响或排除混淆变量的场景。本 prompt 是 {PROJECT_NAME} 项目通用实验设计方法论，叠加在 `master-prompt.md` 之上执行，并为 `debug-prompt.md`、`performance-optimization-prompt.md`、`world-model-learning-prompt.md` 提供实验设计基线。当各子 prompt 在本基线之上增加领域专用约束（如性能实验的统计纪律、{BACKEND_A} 同步要求）时，以该子 prompt 为准；当子 prompt 的实验规则低于本基线（如缺失 PREDICTION/FALSIFICATION）时，以本协议为准。最终冲突由 `master-prompt.md` 裁决。

---

### [core/future-roadmap-prompt.md](core/future-roadmap-prompt.md) - FUTURE ROADMAP PROMPT：{PROJECT_NAME} 技术路线与未来规划协议

适用：制定季度/年度技术路线、评估技术债、规划优化路径、决定功能优先级、设计里程碑。

---

### [core/large-model-inference-gap-prompt.md](core/large-model-inference-gap-prompt.md) - 大模型推理能力差距分析 Prompt

目标：系统评估当前项目距离能够稳定、高效地推理一个数十亿参数级别的大语言模型还缺少哪些关键能力，并给出分阶段补齐路径。

---

### [core/logical-inference-prompt.md](core/logical-inference-prompt.md) - LOGICAL INFERENCE PROMPT：纯逻辑推理与形式化分析协议

适用：当 Agent 需要脱离具体代码执行，对算法正确性、不变量、边界条件、并发模型、类型系统性质或抽象命题进行严格推理时使用。本 prompt 为任务级协议，必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

### [core/master-prompt.md](core/master-prompt.md) - MASTER PROMPT：{PROJECT_NAME} 高级工程任务执行总控协议

作用：本 prompt 为总控协议。收到具体任务后，必须根据任务类型加载对应子 prompt，并严格执行其中的 DSL、流程与格式要求。

---

### [core/meta-cognition-prompt.md](core/meta-cognition-prompt.md) - META-COGNITION PROMPT：{PROJECT_NAME} 逻辑推理与元认知方法论强化协议

适用：需要强化 Agent 自身推理质量、审查推理漏洞、设计复杂推理链、避免模型幻觉与过度归因。

---

### [core/meta-data-generation-prompt.md](core/meta-data-generation-prompt.md) - META-DATA-GENERATION PROMPT：Agent 认知轨迹数据生成优化协议

适用：所有 Agent 任务。本 prompt 为最高层 Meta-Prompt，优化目标从"让 Agent 像优秀工程师一样工作"升级为"让 Agent 的工作过程变成未来模型可以学习的高质量认知轨迹数据"。

---

### [core/new-module-prompt.md](core/new-module-prompt.md) - NEW MODULE PROMPT：{PROJECT_NAME} 新模块 / 新算子开发协议

适用：新增算子、Node、Kernel、层、工具类、测试框架、CLI 等任何新增代码模块。

---

### [core/performance-optimization-prompt.md](core/performance-optimization-prompt.md) - PERFORMANCE OPTIMIZATION PROMPT：{PROJECT_NAME} 性能优化决策与消融实验设计协议

作用：任务级协议 prompt，叠加在 `master-prompt.md` 之上使用。

---

### [core/performance-test-prompt.md](core/performance-test-prompt.md) - PERFORMANCE TEST PROMPT：{PROJECT_NAME} 性能测试与优化协议

适用：性能回归排查、性能优化、吞吐/延迟基准测试、瓶颈分析、kernel 调度优化等。

---

### [core/prompt-evolution-prompt.md](core/prompt-evolution-prompt.md) - PROMPT EVOLUTION PROMPT：提示词自动进化与并行评测协议

适用：当需要持续改进 `skills/prompts/` 中的任务级 prompt、子 Agent 角色定义或元规则时使用。本协议定义 `PROMPT_EVOLUTION_ENGINEER` 角色，负责从现有 prompt、MEM 和任务历史中自动变异、测试、选择并沉淀更优 prompt。

---

### [core/prompt-review-prompt.md](core/prompt-review-prompt.md) - PROMPT_REVIEWER Protocol: Prompt Self-Defect Review

(CTX) 本 prompt 为任务级协议，设计为叠加在 `master-prompt.md` 之上使用。当主 Agent 需要生成、修订或审计任何任务级 prompt（含 `skills/prompts/*.md` 与临时子 prompt）时，必须调用 `PROMPT_REVIEWER` 子 Agent，依据本协议审查 prompt 是否存在 12 类常见设计缺陷。

---

### [core/reflection-prompt.md](core/reflection-prompt.md) - REFLECTION PROMPT：{PROJECT_NAME} 反思与记录协议

适用：任务结束后的复盘、skill 更新、方法论提炼、错误模式归档、会话日志整理。

---

### [core/research-survey-prompt.md](core/research-survey-prompt.md) - RESEARCH SURVEY PROMPT：研究调研与技术趋势分析协议

适用：当 Agent 需要调研新技术、竞品实现、学术论文、开源项目或行业趋势，并产出可行动的知识地图时使用。本 prompt 为任务级协议，必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

### [core/scenario-planning-prompt.md](core/scenario-planning-prompt.md) - SCENARIO PLANNING PROMPT：情景规划与风险预案协议

适用：当 Agent 需要为未来不确定性建模、制定应急预案、评估技术演进风险时使用。典型场景包括：硬件/后端弃用、依赖 BREAKING CHANGE、政策或生态位变化、竞争格局迁移。本 prompt 为任务级协议，必须叠加在 `master-prompt.md` 与 `meta-data-generation-prompt.md` 之上执行。

---

### [core/semantic-change-regression-prompt.md](core/semantic-change-regression-prompt.md) - SEMANTIC CHANGE REGRESSION PROMPT：核心数据结构语义变更后的完整回归协议

作用：本 prompt 为任务级协议，必须叠加在 `master-prompt.md`、`meta-data-generation-prompt.md` 与 `semantic-regression-test-prompt.md` 之上执行。当 {PROJECT_NAME}（或任何具有相似三段式结构的自动微分框架）的 `Storage`、`Tensor`、`Node`、`AutogradMeta` 发生拷贝/移动/析构/共享语义变更时，由本 prompt 定义的 **`SEMANTIC_CHANGE_REGRESSION_DESIGNER`** 负责设计、执行并输出一份**完整语义回归报告**，而非仅验证原始修复目标是否达成。

---

### [core/semantic-regression-test-prompt.md](core/semantic-regression-test-prompt.md) - SEMANTIC REGRESSION TEST DESIGNER PROMPT：核心数据结构语义变更后自动生成回归测试

作用：本 prompt 为任务级协议，需叠加在 `master-prompt.md` 之上使用。当 {PROJECT_NAME}（或任何具有相似三段式结构的自动微分框架）的 `Tensor`、`Storage`、`AutogradMeta`、`Node` 等核心数据结构发生拷贝/移动/析构/共享语义、设备迁移、算子 ABI、in-place/overlap 或异步同步语义变更时，由本 prompt 定义的 **`SEMANTIC_REGRESSION_TEST_DESIGNER`** 子 Agent 负责设计并输出一套参数化、可执行的语义回归测试方案。

---

### [core/subagent-experiment-prompt.md](core/subagent-experiment-prompt.md) - SUBAGENT EXPERIMENT PROMPT：为子 Agent 设计实验协议

适用：当任务过大或需要并行探索时，将工作拆分为多个子 Agent，每个子 Agent 执行受控实验，并汇总结果。

---

### [core/subagent-protocol.md](core/subagent-protocol.md) - SUBAGENT PROTOCOL：子 Agent 讨论与审查协议

作用：定义何时、如何、以何种角色调用子 Agent 进行讨论或审查，避免"为调用而调用"，确保讨论结果可训练、可审计。

---

### [core/technical-writing-prompt.md](core/technical-writing-prompt.md) - TECHNICAL WRITING PROMPT：{PROJECT_NAME} 技术文档与提案写作协议

适用：撰写 ADR、设计提案、README、迁移指南、API 文档、会议纪要、复盘报告、博客/对外技术文章。

---

### [core/world-model-learning-prompt.md](core/world-model-learning-prompt.md) - WORLD MODEL LEARNING PROMPT：世界模型学习与主动探测协议

适用：当 Agent 需要主动学习环境动力学、构建可迁移的因果理解、验证自身世界模型预测能力时使用。典型场景包括：理解新框架/库的行为边界、探索异构执行语义（{BACKEND_A}/{BACKEND_B}/GPU）、发现系统隐式假设、预测改动影响。

---

## 用户自定义区域

请在下方维护你自己的 skill、memory 和 report 目录：

### Skills 文档

- 在此处添加项目特定的经验与方法论。

### Memories 文档

- 在此处添加可迁移的知识沉淀。

### Reports / Logs

- 在此处添加实验报告与推理日志。
