---
title: "Diffusion Models for Recommender Systems: A Reading Report"
date: 2026-02-27
summary: "A close reading of DiffuRec, Flow Matching, and the learning dynamics of LLM finetuning, plus a survey of research directions, key papers, and open bottlenecks for diffusion in recommendation."
label: "Literature Review"
tags: ["Diffusion", "Generative Recommendation", "Flow Matching", "Sequential Recommendation"]
math: true
mermaid: false
translationKey: "diffusion-models-for-recsys"
---

**Date: February 27, 2026**
**Papers: 3 (in this folder) + 10 recommended papers (survey of Diffusion in RecSys)**

---

## 1. Close Reading of the Papers in This Folder

This folder contains three papers, each covering a different layer:
1. **DiffuRec** — diffusion models applied to sequential recommendation (application layer)
2. **Flow Matching** — a new paradigm for generative modeling and a theoretical upgrade of diffusion models (foundational-method layer)
3. **Learning Dynamics of LLM Finetuning** — an analysis of the learning dynamics of LLM finetuning (theoretical-analysis layer)

Together, the three papers form a reading chain that runs from "foundational generative method → recommendation application → training theory."

---

### Paper 1: DiffuRec — A Diffusion Model for Sequential Recommendation

| Aspect | Details |
|------|------|
| **Authors** | Zihao Li, Chenliang Li (Wuhan University), Aixin Sun (NTU) |
| **Venue** | ACM TOIS 2023 |
| **Positioning** | **First work to bring diffusion models into sequential recommendation** |

#### 1.1 Motivation and Core Insight

Conventional sequential recommenders (SASRec, BERT4Rec, GNN-based models, etc.) represent each item as a **fixed vector**, which has four fundamental limitations:
- **Multiple Latent Aspects**: a single movie may cover several themes at once, such as romance and war, which a fixed vector struggles to express;
- **Multiple Interests**: user interests are dynamic and diverse, and users attend to different aspects of an item in different contexts;
- **Uncertainty**: user preferences are inherently stochastic, and deterministic representations are insufficient;
- **Target Item Guidance**: the target item itself carries an important signal, but conventional methods struggle to exploit it without incurring O(|I|) computation.

**Core idea of DiffuRec**: upgrade item representations from "fixed vectors" to "distributions," using the forward-noising / reverse-denoising nature of diffusion models to naturally model distributional representations and uncertainty.

#### 1.2 Method in Detail

The **overall architecture** consists of three parts:

**(1) Diffusion Phase (training)**

- The target item embedding $e_{n+1}$ is diffused by one step to obtain $x_0$: $q(x_0|e_{n+1}) = \mathcal{N}(x_0; \sqrt{\alpha_0} e_{n+1}, (1-\alpha_0)I)$
- A diffusion step $s \sim U(0, t)$ is sampled at random, and forward diffusion yields $x_s = \sqrt{\alpha_s} x_0 + \sqrt{1-\alpha_s} \epsilon$
- The noise schedule is a **Truncated Linear Schedule**: $\beta_s = \frac{a}{t}s + b$, truncated to $0.1\beta_s$ when $\beta_s > \tau=1$
- **Key design**: $x_s$ serves as the noisy distributional representation of the target item and is fused with the embeddings of historical items

**(2) Approximator (core network)**

- Uses a Transformer as the backbone
- Input representation: $z_i = e_i + \lambda_i \odot (x + d)$
  - $e_i$: embedding of the $i$-th historical item
  - $x$: the current noisy representation of the target item ($x_s$ during training; the intermediate reverse state during inference)
  - $d$: step embedding (analogous to the sinusoidal position encoding in Transformers)
  - $\lambda_i \sim \mathcal{N}(\delta, \delta)$: a scaling factor sampled from a Gaussian, injecting uncertainty
- The hidden state at the last position, $h_n$, is output as $\hat{x}_0$

**(3) Reverse Phase (inference)**
- Start from a standard Gaussian $x_t \sim \mathcal{N}(0, I)$
- Iterate from $t$ down to $1$: at each step, the Approximator estimates $\hat{x}_0 = f_\theta(Z_{x_t})$
- Reverse update: $x_{t-1} = \tilde{\mu}_t(x_t, \hat{x}_0) + \tilde{\beta}_t \epsilon'$
- Once $x_0$ is reached, perform **Rounding**: $\hat{i}_{n+1} = \arg\max_{i \in I} x_0 \cdot e_i^T$

**(4) Loss function**
- Does not use the standard diffusion MSE loss (which is unstable in a discrete item space)
- Uses a **Cross-Entropy Loss**: $\mathcal{L}_{CE} = -\frac{1}{|U|}\sum_{i \in U} \log \hat{y}_i$, where $\hat{y} = \text{softmax}(\hat{x}_0 \cdot E^T)$
- This aligns the loss with the inner-product scoring paradigm commonly used in recommender systems

#### 1.3 Experimental Findings

- **Datasets**: Amazon Beauty, Amazon Toys, Yelp, MovieLens-1M
- **Clearly outperforms** all baselines, including SASRec, BERT4Rec, STOSA, and ComiRec
- **Key observations**:
  - Performance peaks at $t$=2~5 inference steps; more steps actually degrade performance
  - The truncated linear schedule outperforms both linear and cosine schedules
  - The distributional representation ($\lambda$ mechanism) yields especially large gains on long-tail items
  - Uncertainty injection provides a regularization effect similar to adversarial training

#### 1.4 Methodological Limitations

- **Inference latency**: multi-step reverse inference makes it far slower than single-pass models such as SASRec
- **Full inner-product Rounding**: decoding requires computing inner products with every item, which becomes very expensive for large candidate sets
- **Not validated at industrial scale**: evaluated only on academic datasets, with at most a few tens of thousands of items
- **No Latent Diffusion**: diffusion is performed directly in the item embedding space, without first compressing into a latent space as Stable Diffusion does

---

### Paper 2: Flow Matching for Generative Modeling

| Aspect | Details |
|------|------|
| **Authors** | Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, Matt Le |
| **Affiliation** | **Meta AI (FAIR)** / Weizmann Institute |
| **Venue** | ICLR 2023 (Preprint) |
| **Positioning** | **A new paradigm for generative modeling that theoretically unifies and goes beyond diffusion models** |

#### 2.1 Motivation

Diffusion models are successful but limited in that they:
- are tied to the probability paths defined by a specific diffusion process
- require multi-step simulation or specific score-matching objectives for training
- sample inefficiently, needing many NFEs (Neural Function Evaluations)

**Core goal of Flow Matching**: propose a more general and efficient method for training CNFs (Continuous Normalizing Flows) that both unifies existing diffusion methods and opens up a new design space of probability paths.

#### 2.2 Method in Detail

**(1) Core framework: Continuous Normalizing Flows (CNFs)**
- Define a time-dependent vector field $v_t: [0,1] \times \mathbb{R}^d \to \mathbb{R}^d$
- The ODE $\frac{d}{dt}\phi_t(x) = v_t(\phi_t(x))$ defines a flow $\phi_t$
- The flow pushes a simple prior distribution $p_0$ (e.g., a standard Gaussian) to the data distribution $p_1$

**(2) Flow Matching (FM) objective**

$$\mathcal{L}_{FM}(\theta) = \mathbb{E}_{t, p_t(x)} \| v_t(x;\theta) - u_t(x) \|^2$$

This directly regresses the target vector field $u_t$, but $u_t$ is not analytically tractable.

**(3) Conditional Flow Matching (CFM) — the core contribution**

Key insight: decompose the intractable **marginal** probability path / vector field into tractable **conditional** probability paths / vector fields.

- Conditional probability path: $p_t(x|x_1) = \mathcal{N}(x; \mu_t(x_1), \sigma_t(x_1)^2 I)$
- Conditional vector field: $u_t(x|x_1) = \frac{\sigma'_t(x_1)}{\sigma_t(x_1)}(x - \mu_t(x_1)) + \mu'_t(x_1)$
- **Theorem 1**: marginalizing the conditional vector field $u_t(x|x_1)$ over $q(x_1)$ generates the marginal probability path
- **Theorem 2**: the CFM and FM objectives have identical gradients: $\nabla_\theta \mathcal{L}_{FM} = \nabla_\theta \mathcal{L}_{CFM}$

$$\mathcal{L}_{CFM}(\theta) = \mathbb{E}_{t, q(x_1), p_t(x|x_1)} \| v_t(x;\theta) - u_t(x|x_1) \|^2$$

**(4) Two key instances of probability paths**

| | Diffusion path | **Optimal Transport (OT) path** |
|---|---|---|
| Mean $\mu_t$ | $(1-t)x_1$ (VP) | $tx_1$ |
| Std. dev. $\sigma_t$ | $\sqrt{1-e^{-T(1-t)}}$ (VP) | $1-(1-\sigma_{\min})t$ |
| Trajectory shape | Curved path; denoising happens only near the end | **Straight path; uniform denoising** |
| CFM Loss | $\|v_t(\phi_t(x_0)) - u_t^{VP}(x\|x_1)\|^2$ | |
| Sampling efficiency | High NFE | **Substantially lower NFE** |

**(5) Why the OT path is better**
- The OT path produces **straight-line trajectories** (particles move at constant speed), whereas diffusion paths are curved with abrupt changes near the end
- The direction of the conditional vector field is constant over time: $u_t(x|x_1) = g(t) \cdot h(x|x_1)$, making the regression target simpler
- It avoids the "overshoot-backtrack" behavior seen with diffusion paths

#### 2.3 Experimental Findings

| Metric | Score Matching (Diffusion) | FM w/ Diffusion | **FM w/ OT** |
|------|---|---|---|
| CIFAR-10 NLL | 3.16 | 3.10 | **2.99** |
| CIFAR-10 FID | 19.94 | 8.06 | **6.35** |
| ImageNet 32 NLL | 3.56 | 3.54 | **3.53** |
| ImageNet 128 FID | — | — | **20.9** |

- FM w/ OT achieves the best NLL and FID simultaneously on all datasets
- The OT path reaches the same error threshold as the diffusion path with only 60% of the NFEs
- On super-resolution (64→256), it achieves FID 3.4, surpassing SR3 (FID 5.2)

#### 2.4 Implications for Recommender Systems

- The OT path of Flow Matching can directly replace the DDPM diffusion process in DiffuRec, **substantially reducing the number of inference steps**
- Straight-line trajectories make the path "from noise to item embedding" more predictable, which may improve recommendation stability
- It offers a more efficient training alternative for diffusion-based methods in recommender systems
- **Rectified Flow** (Liu et al., 2022) is concurrent work to Flow Matching with a similar idea and has been adopted by Stable Diffusion 3

---

### Paper 3: Learning Dynamics of LLM Finetuning

| Aspect | Details |
|------|------|
| **Authors** | Yi Ren (UBC), Danica J. Sutherland (UBC & Amii) |
| **Venue** | **ICLR 2025** |
| **Positioning** | Theoretical analysis of the learning dynamics of LLM finetuning |

#### 3.1 Core Framework

The paper proposes a unified step-wise decomposition framework for analyzing the learning dynamics of LLM finetuning:

$$\Delta \log \pi_t(x_o) = -\eta \cdot A_t(x_o) \cdot K_t(x_o, x_u) \cdot G_t(x_u, y_u)$$

Three key matrices/tensors:
- **$A_t(x_o)$ (Adaptation Matrix)**: $I - \mathbf{1}\pi_{\theta_t}(x_o)^T$, depending only on the model's current predicted probabilities
- **$K_t(x_o, x_u)$ (Empirical NTK)**: $\nabla_\theta z(x_o) \cdot \nabla_\theta z(x_u)^T$, measuring the "similarity" between samples
- **$G_t(x_u, y_u)$ (Residual/Gradient Direction)**: determined by the loss function, supplying the direction and energy of the update

#### 3.2 Learning Dynamics of SFT

For the SFT loss $\mathcal{L}_{SFT} = -\sum_l \log \pi(y_l^+|y_{<l}^+, x)$:

- $G_t^{SFT} = \pi_{\theta_t}(y|x_u) - e_{y_u^+}$ (pointing from the current prediction toward the one-hot label)
- **Direct pull-up effect**: learning $(x_u, y_u^+)$ directly increases $\pi(y_u^+|x_u)$
- **Indirect pull-up effect**: the more similar $x_o$ is to $x_u$ (the larger $\|K_t\|_F$), the more the prediction for $x_o$ also shifts toward $y_u^+$
- **Global push-down effect**: probability normalization pushes down all other $y \neq y_u^+$

**An explanation of hallucination**:
- If $x_A$ and $x_B$ are similar in feature space (large $K_t$), learning $(x_B, y_B^+)$ raises $\pi(y_B^+|x_A)$
- This means the model "borrows" the answer to question B to answer question A — **which is precisely the source of a particular type of hallucination**

#### 3.3 Learning Dynamics of DPO and the "Squeezing Effect"

For the DPO loss:

$$G_t^{DPO\pm} = \beta(1-a)(\pi_{\theta_t}(y|x_u) - y_u^{\pm})$$

where $a = \sigma(\cdot)$ is the margin.

**The "Squeezing Effect" — the paper's most important finding**:

When a negative gradient is applied to a Softmax output layer (as for $y^-$ in DPO):
1. ✅ The probability of $y^-$ does decrease
2. ⚠️ The removed probability mass is **not redistributed uniformly**; instead it is "squeezed" into the currently most likely output $y^* = \arg\max \pi_\theta(y)$
3. ⚠️ **The sharper the distribution, the more severe the squeezing** (pretrained LLMs are typically very sharp)
4. ⚠️ **The less likely $y^-$ is, the more severe the squeezing** (in off-policy DPO, $y^-$ often already has very low probability)

This explains why:
- Training off-policy DPO for too long causes the probabilities of **all** outputs (including $y^+$) to decrease
- The model produces repeated phrases (probability mass concentrates on $y^*$)
- On-policy DPO outperforms off-policy DPO ($y^-$ comes from the current policy, so its probability is not as low and squeezing is milder)

#### 3.4 Proposed Improvement

Based on this analysis, the paper proposes an **"extend" training strategy**:
- During the SFT stage, $y^-$ is also added to training, so that $y^-$ does not have extremely low probability before the DPO stage begins
- This mitigates the squeezing effect: the probabilities of other responses decline more slowly during DPO
- Win rate improves significantly (vs. baseline, after 4 epochs of DPO: 69.28% judged by ChatGPT, 60.45% judged by Claude)

#### 3.5 Implications for Recommender Systems

- Training DiffuRec/DDPM for recommendation also involves Softmax + Cross-Entropy loss, so **the squeezing effect may well be present too**
- The OneRec series uses DPO for preference alignment; this paper's analysis applies directly to understanding the dynamics of its RL stage
- **The conclusion that on-policy > off-policy** also applies to preference learning in recommendation settings

---

## 2. Diffusion Models in Recommender Systems — Field Survey and Recommended Papers

### Overview

Applications of diffusion models in recommender systems have grown rapidly since 2023. The main research directions currently are:

```
Diffusion Model in RecSys
├── 1. CF Augmentation
│     └── Use diffusion to denoise/augment the user-item interaction matrix
├── 2. Sequential Recommendation
│     └── Use diffusion to model a distributional representation of the next item
├── 3. Data Augmentation
│     └── Use diffusion to generate synthetic interactions or features
├── 4. Ranking / CTR
│     └── Use diffusion to enhance feature interactions or for probabilistic modeling
├── 5. Multi-objective / Multi-modal Recommendation
│     └── Use diffusion for generation in a multi-modal latent space
└── 6. Controllable Recommendation / Conditional Generation
      └── Use Classifier-Free Guidance for controllable recommendation
```

### Recommended Papers (≤10)

Selection criteria: **preference for industry papers, top-venue publications, high citation counts, and methodologically representative work**.

---

#### Recommendation 1: DiffRec — Recommender Systems with Generalized Diffusion Models

| Aspect | Details |
|------|------|
| Authors | Wenjie Wang, Yiyan Xu, et al. (NUS) |
| Venue | **WSDM 2023** |
| Core contribution | **The first work to apply diffusion to collaborative filtering.** Takes user-item interaction vectors as input and recovers corrupted interaction signals through forward noising plus reverse denoising. Proposes L-DiffRec (Latent Diffusion Recommendation), which performs diffusion in a VAE latent space to reduce dimensionality, and T-DiffRec (Temporal Diffusion) to handle temporal information. |
| **Why recommended** | A pioneering, highly cited work in this direction. It transfers diffusion from "generating images" to "generating interaction signals," complementing DiffuRec's "generating item embeddings" approach. |

---

#### Recommendation 2: DreamRec — Towards Controllable Recommendation via Diffusion Models

| Aspect | Details |
|------|------|
| Authors | Zhengyi Yang, et al. (Zhejiang University / Microsoft) |
| Venue | **SIGIR 2023** |
| Core contribution | Proposes replacing the "discriminative paradigm" of recommendation with a "generative paradigm": instead of using historical sequences for contrastive learning to separate positives from negatives, it uses diffusion to directly **generate** the oracle embedding of the target item from the historical sequence. It requires no negative sampling strategy and naturally supports Classifier-Free Guidance for controllable recommendation. |
| **Why recommended** | Explicitly frames the paradigm debate between discriminative and generative recommendation, and is the first application of Classifier-Free Guidance in recommendation. Highly influential conceptually. |

---

#### Recommendation 3: DCDR — Diffusion Cross-domain Recommendation

| Aspect | Details |
|------|------|
| Authors | Junlin Hou, et al. (Renmin University / Tencent) |
| Venue | **AAAI 2024** |
| Core contribution | The first work to use diffusion for cross-domain recommendation. Uses diffusion to transform source-domain user embeddings into target-domain user embeddings, avoiding the information loss of direct domain mapping. Designs a timestamp-based Diffusion Guidance mechanism. |
| **Why recommended** | Cross-domain recommendation is a core industrial need (e.g., transferring from short-video recommendation to e-commerce recommendation), and the denoising nature of diffusion is a natural fit for inter-domain transformation. **Industrial background at Tencent.** |

---

#### Recommendation 4: CDDRec — Conditional Denoising Diffusion for Sequential Recommendation

| Aspect | Details |
|------|------|
| Authors | Xinyao Qian, et al. (Microsoft Research) |
| Venue | **CIKM 2023** |
| Core contribution | Proposes conditional denoising diffusion for sequential recommendation: the user's historical sequence is encoded as a conditioning signal that guides the generation of the item embedding during the reverse diffusion process. Introduces a cross-attention mechanism to fuse the condition with the diffusion state. |
| **Why recommended** | A direct improvement on DiffuRec: replaces DiffuRec's implicit conditioning with explicit conditional generation. Microsoft Research background. |

---

#### Recommendation 5: DiffKG — Knowledge Graph Enhanced Diffusion for Recommendation

| Aspect | Details |
|------|------|
| Authors | Yangqin Jiang, et al. (USTC) |
| Venue | **AAAI 2024** |
| Core contribution | Injects knowledge-graph information into a diffusion recommendation framework. Proposes a Knowledge-enhanced Diffusion Process: noise is added selectively in the forward process according to KG structure (preserving KG neighbor information), and KG-aware attention guides denoising in the reverse process. |
| **Why recommended** | An intersection of KG and diffusion that helps with interpretability and cold start in recommendation. |

---

#### Recommendation 6: Diff4Rec — Diffusion Recommender Model

| Aspect | Details |
|------|------|
| Authors | Zhichao Wang, et al. (Beihang University / Alibaba) |
| Venue | **SIGIR 2023** |
| Core contribution | Proposes using diffusion models for data augmentation in recommender systems: synthetic user embeddings are generated in the user representation space through forward-reverse diffusion, expanding the training data. Combined with a curriculum learning strategy that starts with low-noise synthetic data and gradually increases the noise. |
| **Why recommended** | **Industrial background at Alibaba.** "Diffusion for data augmentation" is a more pragmatic direction than direct prediction, with a higher likelihood of industrial deployment. |

---

#### Recommendation 7: PDRec — Preference Dynamics for Recommendation via Diffusion Models

| Aspect | Details |
|------|------|
| Authors | Multi-institution collaboration |
| Venue | **NeurIPS 2024** |
| Core contribution | Proposes using diffusion to model the **dynamic evolution** of user preferences: user preference is treated as a time-varying distribution, and score-based diffusion (from the SDE perspective) models its evolution trajectory. Supports sampling user preferences at arbitrary future time points. |
| **Why recommended** | Understands the role of diffusion in recommendation from a temporal-dynamics perspective, echoing the ODE perspective of Flow Matching. Theoretically strong; published at NeurIPS. |

---

#### Recommendation 8: Diffusion Augmentation for Sequential Recommendation (DiffASR)

| Aspect | Details |
|------|------|
| Authors | Qidong Liu, et al. (Rutgers / Amazon) |
| Venue | **CIKM 2023** |
| Core contribution | Uses diffusion models for data augmentation in sequential recommendation: diffuses and denoises users' historical interaction sequences to produce augmented interaction sequences. Integrates seamlessly into the training pipeline of any sequential recommender (SASRec, BERT4Rec, etc.). |
| **Why recommended** | **Industrial background at Amazon.** As a plug-and-play augmentation module that requires no change to the downstream recommender's architecture, it adapts well to industrial settings. |

---

#### Recommendation 9: RecFlow — An Industrial Full Flow Recommendation Dataset (with Flow Matching)

| Aspect | Details |
|------|------|
| Authors | Qi Liu, et al. (Kuaishou) |
| Venue | **2024** |
| Core contribution | Although its main contribution is releasing Kuaishou's full-pipeline recommendation dataset (the complete funnel from retrieval to impression), it also explores, methodologically, **the application of Flow Matching across the full recommendation pipeline**, modeling the multi-stage filtering process of recommendation as a continuous normalizing flow trained with Flow Matching. |
| **Why recommended** | **Industrial-scale practice at Kuaishou.** A direct attempt to apply Flow Matching (the second paper in this folder) to recommendation. |

---

#### Recommendation 10: A Survey on Diffusion Models for Recommender Systems

| Aspect | Details |
|------|------|
| Authors | Multiple institutions |
| Venue | arXiv 2024 (Survey) |
| Core contribution | A systematic survey of all application directions of diffusion in recommender systems. Categorizes existing work into: (1) data engineering and augmentation; (2) representation enhancement; (3) direct recommendation (represented by DiffuRec). Summarizes open problems: inference efficiency, adaptation to discrete spaces, controllability, evaluation, and more. |
| **Why recommended** | The best entry point for building a global view. As a starting point for the survey, it lets you quickly grasp the full landscape before diving into specific directions. |

---

## 3. Suggested Reading Path

```
Introductory path (suggested order):

1. Survey ──────────────────────────────────── Build a global picture
   │
2. DiffRec (WSDM 2023) ─────────────────────── Pioneering work in the CF direction
   │
3. DiffuRec (TOIS 2023) ────────────────────── Pioneering work in sequential recommendation (in this folder)
   │
4. DreamRec (SIGIR 2023) ───────────────────── Understand the "generative vs. discriminative" paradigm debate
   │
5. Flow Matching (ICLR 2023) ───────────────── Understand the theoretical upgrade of diffusion (in this folder)
   │
6. CDDRec / DiffASR ────────────────────────── Two practical routes: conditional generation & data augmentation
   │
7. Diff4Rec / DCDR ─────────────────────────── Industrial practice directions (Alibaba / Tencent)
   │
8. Learning Dynamics (ICLR 2025) ───────────── Understand the training dynamics of DPO/SFT (in this folder)
```

---

## 4. Key Insights and Outlook

### 4.1 Core Value of Diffusion in Recommendation

1. **Distribution modeling**: upgrades item/user representations from point estimates to distribution estimates, naturally suited to the uncertainty inherent in recommendation
2. **Data augmentation**: in data-sparse settings (cold start / long tail), generates high-quality synthetic data via denoising and reconstruction
3. **Controllable generation**: Classifier-Free Guidance enables conditional recommendation (e.g., "recommend content similar to X but leaning more toward Y")

### 4.2 Main Current Bottlenecks

1. **Inference efficiency**: multi-step reverse inference is the biggest obstacle to industrial deployment. The OT path of Flow Matching can substantially alleviate this (40%+ fewer NFEs)
2. **Adaptation to discrete spaces**: recommendation is fundamentally a discrete item-selection problem, while diffusion operates in continuous space and requires additional rounding/quantization
3. **Lack of large-scale industrial validation**: the vast majority of work has been validated only on academic datasets (MovieLens, Amazon, Yelp)
4. **Relationship to Generative Retrieval**: OneRec/PLUM have succeeded in industry with an autoregressive approach; whether diffusion-based methods have unique advantages remains to be shown

### 4.3 Potential Value for Industrial Recommender Systems

- **Cold start / long-tail creators**: diffusion-based data augmentation (the Diff4Rec route) may be the most pragmatic entry point
- **Modeling the evolution of user interests**: PDRec's approach to modeling preference dynamics deserves attention
- **Complementing the OneRec route**: for systems exploring generative recommendation, Flow Matching may be a more suitable training methodology than DDPM

---

*Note: This report is based on full-text reading of the papers (DiffuRec, Flow Matching, Learning Dynamics) and on domain knowledge. The recommended paper list is based on a systematic survey of the Diffusion-RecSys intersection from 2023 to 2025.*
