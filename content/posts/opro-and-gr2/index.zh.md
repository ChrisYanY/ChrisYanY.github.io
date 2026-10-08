---
title: "OPRO 与 GR2 精读：LLM 作为优化器与生成式推理重排"
date: 2026-07-10
summary: "精读 OPRO 与 GR2：前者以元提示让 LLM 迭代优化 prompt，后者通过语义 ID 中训练、推理数据生成与 DAPO 强化学习构建推荐重排器。"
label: "论文精读"
tags: ["大语言模型", "提示词优化", "生成式推荐", "重排", "强化学习"]
math: false
mermaid: true
translationKey: "opro-and-gr2"
---

> **日期**: 2026-07
> **Paper 1**: Large Language Models as Optimizers (OPRO) — Google DeepMind, ICLR 2024
> **Paper 2**: GR2: Generative Reasoning Re-ranker — Meta AI, arXiv 2602.07774, Jan 2026

---

## Paper 1: OPRO — Large Language Models as Optimizers

### 1.1 核心思想

OPRO 提出了一个全新的范式：**用 LLM 本身作为优化器**。传统优化问题需要形式化的目标函数和梯度计算，但很多现实任务（尤其是 NLP prompt 优化）难以用数学形式精确定义。OPRO 的核心洞察是：LLM 可以通过自然语言描述来理解优化问题，并通过迭代生成解来逐步逼近最优解。

```mermaid
graph LR
    subgraph Traditional["传统优化"]
        T1["形式化目标函数 f(x)"] --> T2["梯度计算 df/dx"]
        T2 --> T3["参数更新 x -= lr * df/dx"]
        T3 --> T4["收敛"]
    end

    subgraph OPRO["OPRO 优化"]
        O1["自然语言描述目标"] --> O2["LLM 阅读历史解 + 分数"]
        O2 --> O3["LLM 生成新候选解"]
        O3 --> O4["Scorer 评分"]
        O4 -->|"加入轨迹"| O2
    end

    style Traditional fill:#ffcdd2,stroke:#c62828
    style OPRO fill:#c8e6c9,stroke:#2e7d32
```

### 1.2 方法：元提示 (Meta-Prompting)

OPRO 的核心机制是**元提示 (meta-prompt)**，包含两个关键部分：

1. **问题描述 (Problem Description)**: 用自然语言描述优化目标
2. **优化轨迹 (Optimization Trajectory)**: 之前生成的解及其对应的评分，按分数升序排列

```mermaid
graph TB
    subgraph MP["Meta-Prompt 结构"]
        DESC["问题描述（自然语言）"]
        HIST["历史解 & 分数（升序排列）<br/>解1: score=60<br/>解2: score=72<br/>解3: score=85"]
        INST["请生成一个更好的解"]
        DESC --> HIST --> INST
    end

    MP --> OPT["Optimizer LLM"]
    OPT --> NEW["新候选解（多个）"]
    NEW --> SCORER["Scorer 评分"]
    SCORER -->|"(解, 分数) 加入轨迹"| HIST

    style MP fill:#e1f5fe,stroke:#0288d1
    style OPT fill:#f3e5f5,stroke:#9c27b0
    style SCORER fill:#fff3e0,stroke:#ef6c00
```

每轮迭代中：
- LLM（称为 **Optimizer LLM**）阅读 meta-prompt
- 生成新的候选解
- 用 **Scorer**（可以是另一个 LLM 或程序）评估候选解的质量
- 将新的 (解, 分数) 对加入优化轨迹
- 重复直到收敛或达到预算

### 1.3 关键设计细节

```mermaid
graph TB
    subgraph Design["四个关键设计"]
        D1["升序排列<br/>最优解离生成位置最近<br/>利用 LLM recency bias"]
        D2["每步多采样<br/>每轮生成 8 个候选<br/>增加探索多样性"]
        D3["滑动窗口<br/>只保留最近 top-20 个解<br/>避免 prompt 过长"]
        D4["温度控制<br/>较高温度 T=1.0<br/>鼓励探索"]
    end

    style Design fill:#fff9c4,stroke:#f9a825
```

### 1.4 应用一：经典优化问题

作为概念验证，OPRO 在线性回归和旅行商问题 (TSP) 上进行了测试：

| 问题 | 结果 | 评价 |
|------|------|------|
| **线性回归** | LLM 从零逼近最优解 (w=2, b=3) | 可行，但不如梯度下降精确 |
| **TSP (10 节点)** | 路径长度误差 < 1% | 节点数增加后性能下降 |

### 1.5 应用二：Prompt 优化（核心贡献）

这是 OPRO 最重要的应用。任务是自动搜索最优的指令 prompt，使目标 LLM（Scorer LLM）在下游任务上表现最好。

```mermaid
graph TB
    subgraph Pipeline["Prompt 优化流程"]
        TASK["下游任务<br/>(GSM8K / BBH)"]
        TRAIN["训练集子采样<br/>(3.5% of GSM8K)"]
        META["构建 Meta-Prompt<br/>(任务描述 + 历史 prompt + 分数)"]
        GEN["Optimizer LLM 生成<br/>8 个候选 prompt"]
        EVAL["Scorer LLM 在训练集上评估<br/>每个 prompt 的准确率"]
        SELECT["选择最优 prompt"]
        TEST["在完整测试集上评估"]

        TASK --> TRAIN --> META --> GEN --> EVAL
        EVAL -->|"迭代"| META
        EVAL --> SELECT --> TEST
    end

    style Pipeline fill:#e8f5e9,stroke:#388e3c
```

**实验结果**:

```mermaid
graph LR
    subgraph GSM8K["GSM8K 数学推理"]
        G1["人工基线<br/>'Let's think step by step'<br/>71.8%"]
        G2["OPRO 最优<br/>'Take a deep breath and<br/>work on this problem<br/>step-by-step'<br/>80.2%"]
        G1 -->|"+8.4%"| G2
    end

    subgraph BBH["BBH (23 个任务)"]
        B1["空 prompt 基线"]
        B2["OPRO 优化后"]
        B1 -->|"最高 +50%"| B2
    end

    style GSM8K fill:#e1f5fe,stroke:#0288d1
    style BBH fill:#f3e5f5,stroke:#9c27b0
```

**关键发现**:
1. 不同 Scorer LLM 偏好不同的 prompt — 对 PaLM 2-L 最优的 prompt 对 GPT 不一定最优
2. 优化后的 prompt 可能在语义上出人意料（如包含情感鼓励的词汇）
3. 搜索过程展现了清晰的学习曲线：分数随迭代次数稳步上升

### 1.6 局限性

- 计算成本高：每轮需要多次 LLM 推理
- 对离散的结构化优化问题（如大规模 TSP）效果有限
- Prompt 优化高度依赖具体的 Scorer LLM
- 缺乏收敛保证

### 1.7 启示

OPRO 开辟了 "LLM-as-optimizer" 的新方向，表明 LLM 可以在**不依赖梯度**的情况下进行迭代优化。这对那些目标函数难以形式化、但可以用自然语言描述的问题特别有价值。

---

## Paper 2: GR2 — Generative Reasoning Re-ranker

### 2.1 核心思想

GR2 是 Meta AI 提出的端到端 LLM 推荐系统 re-ranking 框架。它的核心创新是**三阶段训练流水线**，将语义 item 表示、推理能力和强化学习结合，专门为 re-ranking 任务设计。

```mermaid
graph TB
    subgraph Problems["解决的三个关键问题"]
        P1["1. Re-ranking 被忽视<br/>现有工作聚焦检索和排序<br/>re-ranking 阶段缺少关注"]
        P2["2. 推理能力未充分利用<br/>LLM 多用 zero-shot / SFT<br/>RL + 高质量推理数据未被用"]
        P3["3. ID 可扩展性<br/>非语义 ID 导致<br/>海量 vocabulary 问题"]
    end

    style Problems fill:#ffcdd2,stroke:#c62828
```

### 2.2 三阶段训练流水线

```mermaid
graph TB
    subgraph S1["阶段 1: Tokenized Mid-Training"]
        ID["非语义 Item ID"] --> RQVAE["RQ-VAE Tokenizer"]
        RQVAE --> SID["语义 ID (SID)<br/>>=99% 唯一性"]
        SID --> MIX["SID + 自然语言<br/>交错混合序列"]
        MIX --> MIDTRAIN["LLM Mid-Training<br/>(Qwen3-8B)<br/>Next-token Prediction"]
    end

    subgraph S2["阶段 2: Reasoning Data Generation"]
        PROMPT["Re-ranking Prompt<br/>(5 条设计原则)"] --> TEACHER["Teacher LLM<br/>(Qwen3-32B)"]
        TEACHER --> TRACE["推理轨迹 + 排序结果"]
        TRACE --> FILTER["Rejection Sampling<br/>预测 == ground truth?"]
        FILTER -->|"Yes"| KEEP["保留高质量样本"]
        FILTER -->|"No"| TEACHER
    end

    subgraph S3["阶段 3: Reasoning Enablement"]
        KEEP2["高质量推理轨迹"] --> SFT["SFT 微调<br/>解耦推理损失 + 排序损失<br/>lambda_r < lambda_o"]
        SFT --> RL["RL (DAPO)<br/>排序奖励 + 条件格式奖励"]
        RL --> FINAL["最终 Re-ranker"]
    end

    S1 --> S2
    S2 --> S3

    style S1 fill:#e1f5fe,stroke:#0288d1
    style S2 fill:#fff3e0,stroke:#ef6c00
    style S3 fill:#e8f5e9,stroke:#388e3c
```

### 2.3 阶段 1: Tokenized Mid-Training

#### 2.3.1 语义 ID (SID) 生成

使用 **RQ-VAE** (Residual-Quantized Variational Autoencoder) 将 item 的文本特征编码为离散 token 序列：

```
Tokenizer(x) = (z_1, z_2, ..., z_K),   z_k in {1, ..., C_k}
```

其中 C_k 是第 k 层 codebook 的大小。核心是用 item 的标题、类目等文本特征的 dense embedding 进行残差量化。

```mermaid
graph LR
    subgraph RQVAE["RQ-VAE Tokenizer"]
        TEXT["Item 文本特征<br/>(标题, 类目, ...)"]
        ENC["Encoder<br/>f_enc(x)"]
        H["Dense Embedding h"]
        Q1["Codebook 1<br/>粗粒度语义<br/>(如产品类型)"]
        R1["残差 r1 = h - e1"]
        Q2["Codebook 2<br/>中粒度语义"]
        R2["残差 r2 = r1 - e2"]
        QK["Codebook K<br/>细粒度语义"]

        TEXT --> ENC --> H --> Q1
        Q1 --> R1 --> Q2
        Q2 --> R2 --> QK
    end

    QK --> SID2["SID: (z1, z2, ..., zK)<br/>离散 token 序列"]

    style RQVAE fill:#f3e5f5,stroke:#9c27b0
```

#### 2.3.2 Codebook 均衡利用的五种技术

RQ-VAE 训练的关键挑战是 **codebook collapse**（只有少数 code 被使用）。GR2 采用五种互补技术：

```mermaid
graph TB
    subgraph Essential["必需技术"]
        EMA["EMA 更新<br/>唯一性 31% -> 97.5%<br/>(+66.2%)"]
        RLL["Random Last Level<br/>唯一性 54% -> 83%<br/>(+28.7%)"]
    end

    subgraph Optional["可选/负面技术"]
        DIV["Diversity Loss<br/>+0.6%（边际）"]
        DCR["Dead Code Reset<br/>-4.0%（略负）"]
        CTR["Contrastive Loss<br/>唯一性 -13.2%<br/>但推荐性能最好!"]
    end

    subgraph Key["关键发现"]
        K1[">=99% 唯一性 =<br/>EMA + Random Last Level"]
        K2["高唯一性 != 好推荐<br/>Contrastive Loss 降低唯一性<br/>但一致提升下游指标"]
    end

    Essential --> Key
    Optional --> Key

    style Essential fill:#c8e6c9,stroke:#2e7d32
    style Optional fill:#fff9c4,stroke:#f9a825
    style Key fill:#e1f5fe,stroke:#0288d1
```

| 技术 | 对唯一性的影响 | 对推荐性能的影响 | 重要性 |
|------|---------------|-----------------|--------|
| **EMA 更新** | +66.2% | 正面 | 必需 |
| **Random Last Level** | +28.7% | 正面 | 必需 |
| **Diversity Loss** | +0.6% | 边际 | 可选 |
| **Dead Code Reset** | -4.0% | 轻微负面 | 可选 |
| **Contrastive Loss** | -13.2% | **最佳推荐性能** | 复杂 trade-off |

#### 2.3.3 Mid-Training 策略

借鉴 OneRec-Think 的 item alignment 思路：**在单个序列中交错 SID token 和自然语言 token**，通过 next-token prediction 让 LLM 对齐推荐知识与语言知识。

```mermaid
graph LR
    subgraph Sequence["Mid-Training 混合序列示例"]
        S1["[SID_BEGIN]"]
        S2["s_a_57"]
        S3["[SID_END]"]
        S4[", title:"]
        S5["Argan Oil Shampoo"]
        S6[", categories:"]
        S7["Beauty > Hair Care"]

        S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7
    end

    subgraph Objective["训练目标"]
        NTP["Next-Token Prediction<br/>同时学习 SID token<br/>和自然语言 token"]
    end

    Sequence --> NTP

    style Sequence fill:#fff3e0,stroke:#ef6c00
    style Objective fill:#e8f5e9,stroke:#388e3c
```

### 2.4 阶段 2: 推理数据生成

#### 2.4.1 Chat 格式训练数据

训练样本采用三角色 chat 格式：

```mermaid
graph TB
    subgraph Chat["Chat 格式训练样本"]
        SYS["System Message<br/>角色: 电商推荐专家<br/>任务: 从 10 个候选中 re-rank"]
        USER["User Message<br/>购买历史 (SID + 标题 + 类目)<br/>+ 10 个候选 item (SID + 元数据)"]
        ASST["Assistant Message<br/>JSON 输出:<br/>- explanation: 三步推理轨迹<br/>- recommendations: 排序列表"]

        SYS --> USER --> ASST
    end

    style SYS fill:#ffcdd2,stroke:#c62828
    style USER fill:#e1f5fe,stroke:#0288d1
    style ASST fill:#c8e6c9,stroke:#2e7d32
```

#### 2.4.2 两种推理轨迹生成策略

```mermaid
graph TB
    subgraph Targeted["Targeted Sampling（目标采样）"]
        T1["输入: 用户历史 + 候选集<br/>+ 正确答案"]
        T2["Teacher LLM 生成<br/>解释为什么答案正确"]
        T3["优点: 总能产出合理解释<br/>缺点: 可能事后合理化"]
        T1 --> T2 --> T3
    end

    subgraph Rejection["Rejection Sampling（拒绝采样）"]
        R1["输入: 用户历史 + 候选集<br/>（不给正确答案）"]
        R2["Teacher LLM 自主预测"]
        R3{"预测 == 真实标签?"}
        R4["保留推理轨迹"]
        R5["丢弃, 重新采样"]

        R1 --> R2 --> R3
        R3 -->|"Yes"| R4
        R3 -->|"No"| R5 --> R2
    end

    subgraph Verdict["实验结论"]
        V1["Rejection Sampling 更好<br/>推理更真实, 不含事后合理化<br/>RL 阶段受益更大"]
    end

    Targeted --> Verdict
    Rejection --> Verdict

    style Targeted fill:#fff3e0,stroke:#ef6c00
    style Rejection fill:#e8f5e9,stroke:#388e3c
    style Verdict fill:#e1f5fe,stroke:#0288d1
```

#### 2.4.3 五条 Prompt 设计原则

```mermaid
graph TB
    subgraph Principles["Prompt 设计五原则"]
        P1["P1: 角色与任务定义<br/>建立电商推荐专家 persona<br/>明确 re-ranking 目标"]
        P2["P2: 协作上下文展示<br/>同时呈现历史 + 候选集<br/>支持全局比较（非逐个评估）"]
        P3["P3: 领域知识引导 (KP)<br/>提示序列购买模式<br/>洗发水 -> 护发素 -> 造型产品"]
        P4["P4: 关键约束<br/>强制引用 SID<br/>确保推理可追溯可验证"]
        P5["P5: 结构化多步推理<br/>三步: 模式识别 -> 类目匹配<br/>-> 候选匹配"]
    end

    style Principles fill:#f3e5f5,stroke:#9c27b0
```

### 2.5 阶段 3: 推理能力激活

#### 2.5.1 SFT 阶段

用生成的推理轨迹微调 student LLM（Qwen3-8B）。损失函数**解耦推理和排序**：

```
L_SFT = -lambda_r * sum(log P(r_i | P, r_<i))
        -lambda_o * sum(log P(o_j | P, tau, o_<j))

其中 lambda_r < lambda_o（排序权重 > 推理权重）
只对 assistant message 计算损失
```

#### 2.5.2 RL 阶段 (DAPO)

```mermaid
graph TB
    subgraph Reward["奖励函数设计"]
        subgraph RankR["排序奖励 R_rank"]
            RR["R_rank = (r_D - r_o) / |D|<br/>r_D = 原始排名<br/>r_o = 重排后排名<br/>目标 item 排名提升越多, 奖励越高"]
        end

        subgraph FmtR["格式奖励 R_fmt"]
            FR["R_fmt = Omega(o)<br/>检查输出是否可解析<br/>(推理轨迹 + 排序列表)"]
        end

        subgraph CondR["条件格式奖励（防 Reward Hacking）"]
            CR["R = R_rank + alpha * R_fmt<br/>当 R_rank > 0 或 target 已排第一<br/><br/>R = R_rank<br/>否则（不奖励原地不动）"]
        end

        RankR --> CondR
        FmtR --> CondR
    end

    subgraph Hacking["Reward Hacking 现象"]
        H1["问题: LLM 学会保持原始排序不变"]
        H2["原因: 不改变排序 -> R_rank=0<br/>但格式正确 -> 拿到 R_fmt"]
        H3["解法: 条件格式奖励<br/>只有做出改善才给格式分"]
        H1 --> H2 --> H3
    end

    CondR --> Hacking

    style RankR fill:#c8e6c9,stroke:#2e7d32
    style FmtR fill:#e1f5fe,stroke:#0288d1
    style CondR fill:#fff3e0,stroke:#ef6c00
    style Hacking fill:#ffcdd2,stroke:#c62828
```

**DAPO 算法特性** (基于 GRPO 改进):

| 特性 | 说明 |
|------|------|
| Clip-Higher 策略 | 解耦上下裁剪范围 (epsilon_low, epsilon_high) |
| 过滤无效 prompt | 准确率为 0 或 1 的 prompt 不产生梯度, 过滤掉 |
| 过采样 | 过采样低优势样本, 提升样本效率 |
| Token 级优化 | 每个 token 独立计算 importance ratio |

### 2.6 实验结果

#### 2.6.1 数据集

| 数据集 | 用户数 | Item 数 | 平均序列长度 |
|--------|--------|---------|-------------|
| Amazon Beauty | 22,363 | 12,101 | 8.87 |
| Amazon Sports | 35,598 | 18,357 | 8.32 |

#### 2.6.2 Mid-Training 性能 vs OneRec-Think

```mermaid
graph LR
    subgraph Comparison["Amazon Beauty: Mid-Training 对比"]
        subgraph ORT["OneRec-Think (ORT)"]
            OB["Base<br/>R@5=0.0460<br/>NDCG@5=0.0314"]
            OIA["Base+IA<br/>R@5=0.0532<br/>NDCG@5=0.0342"]
        end

        subgraph GR2M["GR2 (Ours)"]
            GT["Tokenization<br/>R@5=0.0491<br/>NDCG@5=0.0328"]
            GS["Single-task MT<br/>R@5=0.0564<br/>NDCG@5=0.0406"]
            GM["Multi-task MT<br/>R@10=0.0774<br/>NDCG@5=0.0396"]
        end
    end

    OB -->|"GR2 tokenization<br/>R@5 +6.7%"| GT
    OIA -->|"GR2 MT single<br/>NDCG@5 +18.7%"| GS

    style ORT fill:#ffcdd2,stroke:#c62828
    style GR2M fill:#c8e6c9,stroke:#2e7d32
```

#### 2.6.3 Re-ranking 性能（Amazon Beauty）

```mermaid
graph TB
    subgraph Rerank["Re-ranking 对比（Amazon Beauty）"]
        PRE["Pre-rank (MTL)<br/>R@1=0.2892  R@5=0.7227<br/>NDCG@5=0.5101"]

        subgraph SFTGroup["SFT 阶段"]
            SFTRK["SFT-rejection-KP<br/>R@1=0.2784  R@5=0.7091<br/>NDCG@5=0.4970<br/>（性能反而下降!）"]
        end

        subgraph RLGroup["SFT + RL 阶段"]
            RLRK["RL-rejection-KP (BEST)<br/>R@1=0.2977  R@5=0.7460<br/>NDCG@5=0.5234"]
            RLTK["RL-targeted-KP<br/>R@1=0.2898  R@5=0.7221<br/>NDCG@5=0.5101"]
        end
    end

    PRE -->|"SFT 单独用<br/>反而下降"| SFTRK
    SFTRK -->|"RL 挽救并提升"| RLRK
    PRE -->|"vs Pre-rank<br/>R@5 +2.4%<br/>NDCG@5 +1.3%"| RLRK

    style PRE fill:#fff9c4,stroke:#f9a825
    style SFTGroup fill:#ffcdd2,stroke:#c62828
    style RLGroup fill:#c8e6c9,stroke:#2e7d32
```

#### 2.6.4 关键发现

```mermaid
graph TB
    subgraph Findings["四个关键发现"]
        F1["1. RL > SFT<br/>SFT 单独用时 re-ranking<br/>性能可能反而下降<br/>RL 是必要的"]
        F2["2. Rejection > Targeted<br/>Rejection sampling 的<br/>推理轨迹质量更高<br/>（无事后合理化）"]
        F3["3. KP 很重要<br/>领域知识引导 (Knowledge Priming)<br/>显著提升性能"]
        F4["4. RL-rejection-KP 最佳<br/>超越 SOTA OneRec-Think<br/>R@5 +2.4%, NDCG@5 +1.3%"]
    end

    style Findings fill:#e1f5fe,stroke:#0288d1
```

### 2.7 启示

1. **Re-ranking 是 LLM 推荐系统中被忽视但重要的环节** — 不同于检索/排序，re-ranking 需要对候选集进行精细比较
2. **推理能力对 re-ranking 至关重要** — 但仅靠 SFT 不够，需要 RL 来真正优化排序目标
3. **SID 的唯一性和语义性存在 trade-off** — contrastive loss 降低唯一性但提升推荐质量
4. **Reward 设计需要防范 hacking** — 条件格式奖励是一个有效的防御手段

---

## 两篇论文的对比与联系

```mermaid
graph TB
    subgraph OPRO_Sum["OPRO"]
        O1["范式: LLM-as-Optimizer"]
        O2["方法: Meta-Prompt 迭代搜索"]
        O3["应用: Prompt 优化"]
        O4["推理: 隐式<br/>（从历史解中学习模式）"]
        O5["优化: 无 RL<br/>纯搜索"]
    end

    subgraph GR2_Sum["GR2"]
        G1["范式: LLM-as-Reranker"]
        G2["方法: 三阶段训练流水线"]
        G3["应用: 推荐系统 Re-ranking"]
        G4["推理: 显式<br/>（CoT 推理轨迹）"]
        G5["优化: DAPO RL<br/>自定义排序奖励"]
    end

    subgraph Common["共同主题"]
        C1["LLM 推理能力是核心资产"]
        C2["迭代改进<br/>OPRO: 元提示迭代<br/>GR2: SFT -> RL 逐步提升"]
        C3["自然语言作为接口<br/>非传统数学形式"]
        C4["质量筛选很重要<br/>OPRO: top-k 解<br/>GR2: rejection sampling"]
    end

    OPRO_Sum --> Common
    GR2_Sum --> Common

    style OPRO_Sum fill:#e1f5fe,stroke:#0288d1
    style GR2_Sum fill:#c8e6c9,stroke:#2e7d32
    style Common fill:#f3e5f5,stroke:#9c27b0
```

| 维度 | OPRO | GR2 |
|------|------|-----|
| **核心范式** | LLM 作为通用优化器 | LLM 作为推荐 re-ranker |
| **优化对象** | Prompt / 数学问题的解 | 候选 item 的排序 |
| **搜索方法** | 元提示迭代搜索 | 三阶段训练 (mid-training - SFT - RL) |
| **LLM 角色** | 优化器 + 评分器 | 推理器 + 排序器 |
| **推理方式** | 隐式（从历史中学习） | 显式（CoT 推理轨迹） |
| **RL 使用** | 无 | DAPO + 自定义排序奖励 |
| **规模** | 学术验证 (GSM8K, BBH) | 工业级 (Amazon, 面向大规模部署) |
| **共同点** | 都利用 LLM 推理能力解决传统方法难以处理的优化/排序问题 |
