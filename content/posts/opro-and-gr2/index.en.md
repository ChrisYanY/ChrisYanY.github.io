---
title: "OPRO & GR2: LLMs as Optimizers and Generative Reasoning Re-rankers"
date: 2026-07-10
summary: "A close reading of OPRO, which uses meta-prompts to let LLMs iteratively optimize prompts, and GR2, which builds a recommendation re-ranker via semantic-ID mid-training, reasoning data generation, and DAPO RL."
label: "Paper Notes"
tags: ["LLM", "Prompt Optimization", "Generative Recommendation", "Re-ranking", "Reinforcement Learning"]
math: false
mermaid: true
translationKey: "opro-and-gr2"
---

> **Date**: 2026-07
> **Paper 1**: Large Language Models as Optimizers (OPRO) — Google DeepMind, ICLR 2024
> **Paper 2**: GR2: Generative Reasoning Re-ranker — Meta AI, arXiv 2602.07774, Jan 2026

---

## Paper 1: OPRO — Large Language Models as Optimizers

### 1.1 Core Idea

OPRO proposes a new paradigm: **using the LLM itself as the optimizer**. Classical optimization requires a formal objective function and gradient computation, yet many real-world tasks (especially prompt optimization in NLP) are hard to specify precisely in mathematical form. OPRO's key insight is that an LLM can understand an optimization problem from a natural-language description and progressively approach the optimum by iteratively generating solutions.

```mermaid
graph LR
    subgraph Traditional["Classical Optimization"]
        T1["Formal objective f(x)"] --> T2["Gradient df/dx"]
        T2 --> T3["Parameter update x -= lr * df/dx"]
        T3 --> T4["Convergence"]
    end

    subgraph OPRO["OPRO Optimization"]
        O1["Objective described in natural language"] --> O2["LLM reads past solutions + scores"]
        O2 --> O3["LLM generates new candidate solutions"]
        O3 --> O4["Scorer evaluates"]
        O4 -->|"Append to trajectory"| O2
    end

    style Traditional fill:#ffcdd2,stroke:#c62828
    style OPRO fill:#c8e6c9,stroke:#2e7d32
```

### 1.2 Method: Meta-Prompting

The core mechanism of OPRO is the **meta-prompt**, which contains two key components:

1. **Problem Description**: the optimization objective described in natural language
2. **Optimization Trajectory**: previously generated solutions and their scores, sorted in ascending order of score

```mermaid
graph TB
    subgraph MP["Meta-Prompt Structure"]
        DESC["Problem description (natural language)"]
        HIST["Past solutions & scores (ascending)<br/>Solution 1: score=60<br/>Solution 2: score=72<br/>Solution 3: score=85"]
        INST["Please generate a better solution"]
        DESC --> HIST --> INST
    end

    MP --> OPT["Optimizer LLM"]
    OPT --> NEW["New candidate solutions (multiple)"]
    NEW --> SCORER["Scorer evaluates"]
    SCORER -->|"(solution, score) appended to trajectory"| HIST

    style MP fill:#e1f5fe,stroke:#0288d1
    style OPT fill:#f3e5f5,stroke:#9c27b0
    style SCORER fill:#fff3e0,stroke:#ef6c00
```

In each iteration:
- The LLM (called the **Optimizer LLM**) reads the meta-prompt
- It generates new candidate solutions
- A **Scorer** (which can be another LLM or a program) evaluates the quality of each candidate
- The new (solution, score) pairs are appended to the optimization trajectory
- Repeat until convergence or the budget is exhausted

### 1.3 Key Design Details

```mermaid
graph TB
    subgraph Design["Four Key Design Choices"]
        D1["Ascending order<br/>Best solutions sit closest to the generation point<br/>Exploits LLM recency bias"]
        D2["Multiple samples per step<br/>8 candidates per iteration<br/>Increases exploration diversity"]
        D3["Sliding window<br/>Keep only the top-20 recent solutions<br/>Avoids overly long prompts"]
        D4["Temperature control<br/>Relatively high temperature T=1.0<br/>Encourages exploration"]
    end

    style Design fill:#fff9c4,stroke:#f9a825
```

### 1.4 Application 1: Classical Optimization Problems

As a proof of concept, OPRO was tested on linear regression and the traveling salesman problem (TSP):

| Problem | Result | Evaluation |
|------|------|------|
| **Linear regression** | The LLM approaches the optimum (w=2, b=3) from scratch | Feasible, but less precise than gradient descent |
| **TSP (10 nodes)** | Tour-length error < 1% | Performance degrades as the number of nodes grows |

### 1.5 Application 2: Prompt Optimization (Core Contribution)

This is OPRO's most important application. The task is to automatically search for the optimal instruction prompt that maximizes the target LLM's (the Scorer LLM's) performance on a downstream task.

```mermaid
graph TB
    subgraph Pipeline["Prompt Optimization Pipeline"]
        TASK["Downstream task<br/>(GSM8K / BBH)"]
        TRAIN["Subsample training set<br/>(3.5% of GSM8K)"]
        META["Build meta-prompt<br/>(task description + past prompts + scores)"]
        GEN["Optimizer LLM generates<br/>8 candidate prompts"]
        EVAL["Scorer LLM evaluates the accuracy<br/>of each prompt on the training set"]
        SELECT["Select the best prompt"]
        TEST["Evaluate on the full test set"]

        TASK --> TRAIN --> META --> GEN --> EVAL
        EVAL -->|"Iterate"| META
        EVAL --> SELECT --> TEST
    end

    style Pipeline fill:#e8f5e9,stroke:#388e3c
```

**Experimental results**:

```mermaid
graph LR
    subgraph GSM8K["GSM8K Math Reasoning"]
        G1["Human baseline<br/>'Let's think step by step'<br/>71.8%"]
        G2["Best OPRO prompt<br/>'Take a deep breath and<br/>work on this problem<br/>step-by-step'<br/>80.2%"]
        G1 -->|"+8.4%"| G2
    end

    subgraph BBH["BBH (23 tasks)"]
        B1["Empty-prompt baseline"]
        B2["After OPRO optimization"]
        B1 -->|"Up to +50%"| B2
    end

    style GSM8K fill:#e1f5fe,stroke:#0288d1
    style BBH fill:#f3e5f5,stroke:#9c27b0
```

**Key findings**:
1. Different Scorer LLMs prefer different prompts — the best prompt for PaLM 2-L is not necessarily the best for GPT
2. Optimized prompts can be semantically surprising (e.g., containing emotionally encouraging phrasing)
3. The search process exhibits a clear learning curve: scores rise steadily with the number of iterations

### 1.6 Limitations

- High compute cost: each iteration requires many LLM inference calls
- Limited effectiveness on discrete, structured optimization problems (e.g., large-scale TSP)
- Prompt optimization depends heavily on the specific Scorer LLM
- No convergence guarantees

### 1.7 Takeaways

OPRO opens up the new direction of "LLM-as-optimizer," showing that LLMs can perform iterative optimization **without relying on gradients**. This is particularly valuable for problems whose objectives are hard to formalize but can be described in natural language.

---

## Paper 2: GR2 — Generative Reasoning Re-ranker

### 2.1 Core Idea

GR2 is an end-to-end LLM-based re-ranking framework for recommender systems proposed by Meta AI. Its core innovation is a **three-stage training pipeline** that combines semantic item representations, reasoning capability, and reinforcement learning, designed specifically for the re-ranking task.

```mermaid
graph TB
    subgraph Problems["Three Key Problems Addressed"]
        P1["1. Re-ranking is overlooked<br/>Existing work focuses on retrieval and ranking<br/>The re-ranking stage gets little attention"]
        P2["2. Reasoning is underutilized<br/>LLMs are mostly used zero-shot / with SFT<br/>RL + high-quality reasoning data go unused"]
        P3["3. ID scalability<br/>Non-semantic IDs lead to<br/>a massive vocabulary problem"]
    end

    style Problems fill:#ffcdd2,stroke:#c62828
```

### 2.2 Three-Stage Training Pipeline

```mermaid
graph TB
    subgraph S1["Stage 1: Tokenized Mid-Training"]
        ID["Non-semantic item ID"] --> RQVAE["RQ-VAE Tokenizer"]
        RQVAE --> SID["Semantic ID (SID)<br/>>=99% uniqueness"]
        SID --> MIX["SID + natural language<br/>interleaved sequences"]
        MIX --> MIDTRAIN["LLM Mid-Training<br/>(Qwen3-8B)<br/>Next-token Prediction"]
    end

    subgraph S2["Stage 2: Reasoning Data Generation"]
        PROMPT["Re-ranking Prompt<br/>(5 design principles)"] --> TEACHER["Teacher LLM<br/>(Qwen3-32B)"]
        TEACHER --> TRACE["Reasoning trace + ranking"]
        TRACE --> FILTER["Rejection Sampling<br/>prediction == ground truth?"]
        FILTER -->|"Yes"| KEEP["Keep high-quality samples"]
        FILTER -->|"No"| TEACHER
    end

    subgraph S3["Stage 3: Reasoning Enablement"]
        KEEP2["High-quality reasoning traces"] --> SFT["SFT fine-tuning<br/>Decoupled reasoning loss + ranking loss<br/>lambda_r < lambda_o"]
        SFT --> RL["RL (DAPO)<br/>Ranking reward + conditional format reward"]
        RL --> FINAL["Final Re-ranker"]
    end

    S1 --> S2
    S2 --> S3

    style S1 fill:#e1f5fe,stroke:#0288d1
    style S2 fill:#fff3e0,stroke:#ef6c00
    style S3 fill:#e8f5e9,stroke:#388e3c
```

### 2.3 Stage 1: Tokenized Mid-Training

#### 2.3.1 Semantic ID (SID) Generation

**RQ-VAE** (Residual-Quantized Variational Autoencoder) is used to encode an item's text features into a sequence of discrete tokens:

```
Tokenizer(x) = (z_1, z_2, ..., z_K),   z_k in {1, ..., C_k}
```

where C_k is the size of the k-th codebook. The core idea is to apply residual quantization to a dense embedding of the item's text features, such as its title and category.

```mermaid
graph LR
    subgraph RQVAE["RQ-VAE Tokenizer"]
        TEXT["Item text features<br/>(title, category, ...)"]
        ENC["Encoder<br/>f_enc(x)"]
        H["Dense Embedding h"]
        Q1["Codebook 1<br/>Coarse-grained semantics<br/>(e.g., product type)"]
        R1["Residual r1 = h - e1"]
        Q2["Codebook 2<br/>Mid-grained semantics"]
        R2["Residual r2 = r1 - e2"]
        QK["Codebook K<br/>Fine-grained semantics"]

        TEXT --> ENC --> H --> Q1
        Q1 --> R1 --> Q2
        Q2 --> R2 --> QK
    end

    QK --> SID2["SID: (z1, z2, ..., zK)<br/>Discrete token sequence"]

    style RQVAE fill:#f3e5f5,stroke:#9c27b0
```

#### 2.3.2 Five Techniques for Balanced Codebook Utilization

The key challenge in training an RQ-VAE is **codebook collapse** (only a few codes get used). GR2 employs five complementary techniques:

```mermaid
graph TB
    subgraph Essential["Essential Techniques"]
        EMA["EMA updates<br/>Uniqueness 31% -> 97.5%<br/>(+66.2%)"]
        RLL["Random Last Level<br/>Uniqueness 54% -> 83%<br/>(+28.7%)"]
    end

    subgraph Optional["Optional / Negative Techniques"]
        DIV["Diversity Loss<br/>+0.6% (marginal)"]
        DCR["Dead Code Reset<br/>-4.0% (slightly negative)"]
        CTR["Contrastive Loss<br/>Uniqueness -13.2%<br/>but best recommendation performance!"]
    end

    subgraph Key["Key Findings"]
        K1[">=99% uniqueness =<br/>EMA + Random Last Level"]
        K2["High uniqueness != good recommendations<br/>Contrastive Loss lowers uniqueness<br/>but consistently improves downstream metrics"]
    end

    Essential --> Key
    Optional --> Key

    style Essential fill:#c8e6c9,stroke:#2e7d32
    style Optional fill:#fff9c4,stroke:#f9a825
    style Key fill:#e1f5fe,stroke:#0288d1
```

| Technique | Effect on uniqueness | Effect on recommendation performance | Importance |
|------|---------------|-----------------|--------|
| **EMA updates** | +66.2% | Positive | Essential |
| **Random Last Level** | +28.7% | Positive | Essential |
| **Diversity Loss** | +0.6% | Marginal | Optional |
| **Dead Code Reset** | -4.0% | Slightly negative | Optional |
| **Contrastive Loss** | -13.2% | **Best recommendation performance** | Complex trade-off |

#### 2.3.3 Mid-Training Strategy

Following the item-alignment idea from OneRec-Think: **interleave SID tokens and natural-language tokens within a single sequence**, and use next-token prediction to align the LLM's recommendation knowledge with its linguistic knowledge.

```mermaid
graph LR
    subgraph Sequence["Example Mid-Training Mixed Sequence"]
        S1["[SID_BEGIN]"]
        S2["s_a_57"]
        S3["[SID_END]"]
        S4[", title:"]
        S5["Argan Oil Shampoo"]
        S6[", categories:"]
        S7["Beauty > Hair Care"]

        S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7
    end

    subgraph Objective["Training Objective"]
        NTP["Next-Token Prediction<br/>Jointly learns SID tokens<br/>and natural-language tokens"]
    end

    Sequence --> NTP

    style Sequence fill:#fff3e0,stroke:#ef6c00
    style Objective fill:#e8f5e9,stroke:#388e3c
```

### 2.4 Stage 2: Reasoning Data Generation

#### 2.4.1 Chat-Format Training Data

Training samples use a three-role chat format:

```mermaid
graph TB
    subgraph Chat["Chat-Format Training Sample"]
        SYS["System Message<br/>Role: e-commerce recommendation expert<br/>Task: re-rank 10 candidates"]
        USER["User Message<br/>Purchase history (SID + title + category)<br/>+ 10 candidate items (SID + metadata)"]
        ASST["Assistant Message<br/>JSON output:<br/>- explanation: three-step reasoning trace<br/>- recommendations: ranked list"]

        SYS --> USER --> ASST
    end

    style SYS fill:#ffcdd2,stroke:#c62828
    style USER fill:#e1f5fe,stroke:#0288d1
    style ASST fill:#c8e6c9,stroke:#2e7d32
```

#### 2.4.2 Two Strategies for Generating Reasoning Traces

```mermaid
graph TB
    subgraph Targeted["Targeted Sampling"]
        T1["Input: user history + candidate set<br/>+ correct answer"]
        T2["Teacher LLM generates<br/>an explanation of why the answer is correct"]
        T3["Pro: always yields a plausible explanation<br/>Con: may be post-hoc rationalization"]
        T1 --> T2 --> T3
    end

    subgraph Rejection["Rejection Sampling"]
        R1["Input: user history + candidate set<br/>(correct answer withheld)"]
        R2["Teacher LLM predicts on its own"]
        R3{"Prediction == ground-truth label?"}
        R4["Keep the reasoning trace"]
        R5["Discard and resample"]

        R1 --> R2 --> R3
        R3 -->|"Yes"| R4
        R3 -->|"No"| R5 --> R2
    end

    subgraph Verdict["Experimental Conclusion"]
        V1["Rejection Sampling is better<br/>More faithful reasoning, no post-hoc rationalization<br/>Benefits more in the RL stage"]
    end

    Targeted --> Verdict
    Rejection --> Verdict

    style Targeted fill:#fff3e0,stroke:#ef6c00
    style Rejection fill:#e8f5e9,stroke:#388e3c
    style Verdict fill:#e1f5fe,stroke:#0288d1
```

#### 2.4.3 Five Prompt Design Principles

```mermaid
graph TB
    subgraph Principles["Five Prompt Design Principles"]
        P1["P1: Role and task definition<br/>Establish an e-commerce recommendation expert persona<br/>Make the re-ranking objective explicit"]
        P2["P2: Collaborative context presentation<br/>Show history + candidate set together<br/>Enable global comparison (not item-by-item scoring)"]
        P3["P3: Domain knowledge priming (KP)<br/>Hint at sequential purchase patterns<br/>shampoo -> conditioner -> styling products"]
        P4["P4: Key constraints<br/>Require citing SIDs<br/>Keep reasoning traceable and verifiable"]
        P5["P5: Structured multi-step reasoning<br/>Three steps: pattern recognition -> category matching<br/>-> candidate matching"]
    end

    style Principles fill:#f3e5f5,stroke:#9c27b0
```

### 2.5 Stage 3: Reasoning Enablement

#### 2.5.1 SFT Stage

The student LLM (Qwen3-8B) is fine-tuned on the generated reasoning traces. The loss function **decouples reasoning from ranking**:

```
L_SFT = -lambda_r * sum(log P(r_i | P, r_<i))
        -lambda_o * sum(log P(o_j | P, tau, o_<j))

where lambda_r < lambda_o (ranking weight > reasoning weight)
loss is computed only on the assistant message
```

#### 2.5.2 RL Stage (DAPO)

```mermaid
graph TB
    subgraph Reward["Reward Function Design"]
        subgraph RankR["Ranking Reward R_rank"]
            RR["R_rank = (r_D - r_o) / |D|<br/>r_D = original rank<br/>r_o = rank after re-ranking<br/>The more the target item moves up, the higher the reward"]
        end

        subgraph FmtR["Format Reward R_fmt"]
            FR["R_fmt = Omega(o)<br/>Checks whether the output is parseable<br/>(reasoning trace + ranked list)"]
        end

        subgraph CondR["Conditional Format Reward (Anti Reward Hacking)"]
            CR["R = R_rank + alpha * R_fmt<br/>if R_rank > 0 or the target is already ranked first<br/><br/>R = R_rank<br/>otherwise (no reward for staying put)"]
        end

        RankR --> CondR
        FmtR --> CondR
    end

    subgraph Hacking["Reward Hacking Phenomenon"]
        H1["Problem: the LLM learns to keep the original ranking unchanged"]
        H2["Cause: unchanged ranking -> R_rank=0<br/>but correct format -> earns R_fmt"]
        H3["Fix: conditional format reward<br/>Format reward only when the ranking improves"]
        H1 --> H2 --> H3
    end

    CondR --> Hacking

    style RankR fill:#c8e6c9,stroke:#2e7d32
    style FmtR fill:#e1f5fe,stroke:#0288d1
    style CondR fill:#fff3e0,stroke:#ef6c00
    style Hacking fill:#ffcdd2,stroke:#c62828
```

**DAPO algorithm features** (an improvement over GRPO):

| Feature | Description |
|------|------|
| Clip-Higher strategy | Decouples the lower and upper clipping ranges (epsilon_low, epsilon_high) |
| Filtering uninformative prompts | Prompts with accuracy 0 or 1 produce no gradient and are filtered out |
| Oversampling | Oversamples low-advantage samples to improve sample efficiency |
| Token-level optimization | Importance ratio is computed independently for each token |

### 2.6 Experimental Results

#### 2.6.1 Datasets

| Dataset | #Users | #Items | Avg. sequence length |
|--------|--------|---------|-------------|
| Amazon Beauty | 22,363 | 12,101 | 8.87 |
| Amazon Sports | 35,598 | 18,357 | 8.32 |

#### 2.6.2 Mid-Training Performance vs. OneRec-Think

```mermaid
graph LR
    subgraph Comparison["Amazon Beauty: Mid-Training Comparison"]
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

#### 2.6.3 Re-ranking Performance (Amazon Beauty)

```mermaid
graph TB
    subgraph Rerank["Re-ranking Comparison (Amazon Beauty)"]
        PRE["Pre-rank (MTL)<br/>R@1=0.2892  R@5=0.7227<br/>NDCG@5=0.5101"]

        subgraph SFTGroup["SFT Stage"]
            SFTRK["SFT-rejection-KP<br/>R@1=0.2784  R@5=0.7091<br/>NDCG@5=0.4970<br/>(performance actually drops!)"]
        end

        subgraph RLGroup["SFT + RL Stage"]
            RLRK["RL-rejection-KP (BEST)<br/>R@1=0.2977  R@5=0.7460<br/>NDCG@5=0.5234"]
            RLTK["RL-targeted-KP<br/>R@1=0.2898  R@5=0.7221<br/>NDCG@5=0.5101"]
        end
    end

    PRE -->|"SFT alone<br/>actually drops"| SFTRK
    SFTRK -->|"RL recovers and improves"| RLRK
    PRE -->|"vs Pre-rank<br/>R@5 +2.4%<br/>NDCG@5 +1.3%"| RLRK

    style PRE fill:#fff9c4,stroke:#f9a825
    style SFTGroup fill:#ffcdd2,stroke:#c62828
    style RLGroup fill:#c8e6c9,stroke:#2e7d32
```

#### 2.6.4 Key Findings

```mermaid
graph TB
    subgraph Findings["Four Key Findings"]
        F1["1. RL > SFT<br/>With SFT alone, re-ranking<br/>performance may actually drop<br/>RL is necessary"]
        F2["2. Rejection > Targeted<br/>Rejection sampling yields<br/>higher-quality reasoning traces<br/>(no post-hoc rationalization)"]
        F3["3. KP matters<br/>Domain knowledge guidance (Knowledge Priming)<br/>significantly improves performance"]
        F4["4. RL-rejection-KP is best<br/>Outperforms SOTA OneRec-Think<br/>R@5 +2.4%, NDCG@5 +1.3%"]
    end

    style Findings fill:#e1f5fe,stroke:#0288d1
```

### 2.7 Takeaways

1. **Re-ranking is an overlooked yet important stage in LLM-based recommender systems** — unlike retrieval/ranking, re-ranking requires fine-grained comparison across the candidate set
2. **Reasoning is crucial for re-ranking** — but SFT alone is insufficient; RL is needed to truly optimize the ranking objective
3. **There is a trade-off between SID uniqueness and semantics** — contrastive loss lowers uniqueness but improves recommendation quality
4. **Reward design must guard against hacking** — the conditional format reward is an effective defense

---

## Comparison and Connections Between the Two Papers

```mermaid
graph TB
    subgraph OPRO_Sum["OPRO"]
        O1["Paradigm: LLM-as-Optimizer"]
        O2["Method: iterative meta-prompt search"]
        O3["Application: prompt optimization"]
        O4["Reasoning: implicit<br/>(learns patterns from past solutions)"]
        O5["Optimization: no RL<br/>pure search"]
    end

    subgraph GR2_Sum["GR2"]
        G1["Paradigm: LLM-as-Reranker"]
        G2["Method: three-stage training pipeline"]
        G3["Application: recommender re-ranking"]
        G4["Reasoning: explicit<br/>(CoT reasoning traces)"]
        G5["Optimization: DAPO RL<br/>custom ranking reward"]
    end

    subgraph Common["Common Themes"]
        C1["LLM reasoning is the core asset"]
        C2["Iterative improvement<br/>OPRO: meta-prompt iterations<br/>GR2: SFT -> RL progressive gains"]
        C3["Natural language as the interface<br/>instead of classical mathematical formulations"]
        C4["Quality filtering matters<br/>OPRO: top-k solutions<br/>GR2: rejection sampling"]
    end

    OPRO_Sum --> Common
    GR2_Sum --> Common

    style OPRO_Sum fill:#e1f5fe,stroke:#0288d1
    style GR2_Sum fill:#c8e6c9,stroke:#2e7d32
    style Common fill:#f3e5f5,stroke:#9c27b0
```

| Dimension | OPRO | GR2 |
|------|------|-----|
| **Core paradigm** | LLM as a general-purpose optimizer | LLM as a recommendation re-ranker |
| **What is optimized** | Prompts / solutions to math problems | Ordering of candidate items |
| **Search method** | Iterative meta-prompt search | Three-stage training (mid-training - SFT - RL) |
| **Role of the LLM** | Optimizer + scorer | Reasoner + ranker |
| **Reasoning style** | Implicit (learns from history) | Explicit (CoT reasoning traces) |
| **Use of RL** | None | DAPO + custom ranking reward |
| **Scale** | Academic validation (GSM8K, BBH) | Industrial-scale (Amazon, targeting large-scale deployment) |
| **Common ground** | Both leverage LLM reasoning to tackle optimization/ranking problems that are hard for traditional methods |
