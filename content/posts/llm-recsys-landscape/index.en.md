---
title: "LLMs Meet Recommender Systems: A Map of 41 Papers (2022–2025)"
date: 2026-02-26
summary: "A categorized reading report on 41 papers at the intersection of recommender systems and LLMs, spanning Semantic ID generative retrieval, two-tower cold start, ranking scaling, and diffusion models."
label: "Literature Review"
tags: ["Generative Recommendation", "LLM", "Semantic ID", "Cold Start", "Diffusion"]
math: true
mermaid: false
translationKey: "llm-recsys-landscape"
---

**Date: February 24, 2026**
**Total documents: 44 (including duplicates)**

---

## 1. Overview

This collection contains 41 papers from 2022–2025 at the intersection of recommender systems and large language models, covering the full technical evolution from classic two-tower retrieval to end-to-end generative recommendation. Sources include leading industry teams — Google DeepMind, ByteDance (Douyin), Kuaishou, Alibaba, Meta, Xiaohongshu, TikTok, Pinterest, Tencent — as well as academic institutions such as Princeton, UIUC, and USTC.

Technically, the papers revolve around the following core questions:
1. **How can the generative paradigm reshape retrieval and ranking in recommender systems?** (Semantic ID + Generative Retrieval)
2. **How can the world knowledge and semantic understanding of LLMs be brought into recommendation?** (LLM-based Recommendation)
3. **How can cold-start and long-tail problems be solved under the constraints of a two-tower architecture?** (Cold Start / Two-Tower Enhancement)
4. **How can recommendation models exhibit scaling laws?** (Large User Model / Ranking Scaling)
5. **How can multimodal information improve recommendation understanding?** (VLM / Multimodal Embedding)
6. **How can generative models such as diffusion and flows model uncertainty and distributional representations in recommendation?** (Diffusion Modeling)

---

## 2. Detailed Taxonomy

---

### Category 1: Semantic IDs and Generative Retrieval

> **Core idea**: Encode items as sequences of discrete semantic IDs using methods such as RQ-VAE, turning recommendation into an autoregressive sequence generation task and thereby breaking away from the traditional multi-stage retrieve-and-rank cascade.

**This category contains 10 papers — the largest and most complete direction in the collection.**

#### 1.1 Foundational Work

| # | Paper | Institution | Venue/Year | Key Contribution |
|---|------|------|-----------|----------|
| 1 | **TIGER: Recommender Systems with Generative Retrieval** | Google DeepMind | NeurIPS 2023 | Introduces the concept of the Semantic ID: items are encoded via RQ-VAE into tuples of discrete semantic codewords, and a Transformer seq-to-seq model is trained to autoregressively predict the Semantic ID of the next item. Significantly outperforms SOTA two-tower retrieval on multiple datasets and generalizes better to items with zero interactions. **The seminal work of this direction.** |
| 2 | **Language Models as Semantic Indexers (LMIndexer)** | UIUC / Amazon | ICML 2024 | Proposes a self-supervised framework for learning semantic IDs: a generative language model produces hierarchical discrete ID representations through progressive training and contrastive learning, with a document reconstruction objective to address the lack of semantic supervision. Validated on recommendation, product search, and document retrieval. |
| 3 | **BETTER GENERALIZATION WITH SEMANTIC IDS** | Google DeepMind / YouTube | 2024 | Studies replacing random IDs with Semantic IDs in industrial ranking models. Proposes a SentencePiece-based tokenization that applies sub-piece hashing to Semantic ID sequences; on YouTube's ranking model, it improves generalization to new and long-tail items without sacrificing overall quality. |

#### 1.2 Industrial End-to-End Systems

| # | Paper | Institution | Year | Key Contribution |
|---|------|------|------|----------|
| 4 | **OneRec: Unifying Retrieve and Rank with Generative Recommender** | Kuaishou | 2024 | **The first end-to-end generative model to significantly outperform a traditional cascaded recommender in a real-world setting.** Uses an Encoder-Decoder + MoE architecture, proposes session-wise generation (instead of item-by-item generation), and incorporates DPO preference alignment. Deployed at Kuaishou. |
| 5 | **OneRec Technical Report** | Kuaishou | 2025 | The full technical report for OneRec. Highlights: a 10x increase in compute FLOPs and the discovery of scaling laws for recommendation; RL shows great potential within the framework; training MFU of 23.7% and inference MFU of 28.8%; OPEX only 10.6% of the traditional pipeline. Handles 25% of QPS on Kuaishou / Kuaishou Lite, improving App Stay Time by 0.54% / 1.24%. |
| 6 | **OneRec-V2 Technical Report** | Kuaishou | 2025 | Targets two bottlenecks of V1: (1) in the Encoder-Decoder, 97.66% of compute is spent on encoding rather than generation; (2) reward-model-based RL is inefficient and prone to reward hacking. Proposes a **Lazy Decoder-Only architecture** (94% less total compute, 90% fewer training resources); scales successfully to 8B parameters; introduces preference alignment based on real user feedback (Duration-Aware Reward Shaping + Adaptive Ratio Clipping). App Stay Time improves by a further 0.467% / 0.741%. |
| 7 | **PLUM: Adapting Pre-trained LLMs for Industrial-scale Generative Recommendations** | Google DeepMind / YouTube | 2025 | Adapts pre-trained LLMs for industrial-scale generative recommendation: Item Tokenization (Semantic ID) → Continued Pre-training → Task-specific Fine-tuning. Significantly outperforms the production model built on large embedding tables in YouTube's large-scale video recommendation and already serves billions of users. **The first large-scale deployment of LLM + Semantic ID at YouTube.** |

#### 1.3 Semantic ID Improvements and Variants

| # | Paper | Institution | Year | Key Contribution |
|---|------|------|------|----------|
| 8 | **TermID (GRLM): LLM-Based Generative Recommendation via Structured Term Identifiers** | Kuaishou | 2025 | Proposes **Term IDs** as a replacement for conventional Semantic IDs: semantically rich, normalized textual keywords serve as item identifiers, avoiding the semantic gap between SIDs and the LLM's native vocabulary. The framework comprises Context-aware Term Generation, Integrative Instruction Fine-tuning, and Elastic Identifier Grounding. |
| 9 | **OneSug: Unified End-to-End Generative Framework for E-commerce Query Suggestion** | Kuaishou | 2025 | Applies the end-to-end generative paradigm to e-commerce search query suggestion. Includes prefix2query representation enhancement, an Encoder-Decoder generative model, and reward-weighted ranking. Fully deployed in Kuaishou e-commerce: CTR +2.01%, Orders +2.04%, Revenue +1.69%. |

#### 1.4 Supporting Reference in This Category

| # | Paper | Notes |
|---|------|------|
| 10 | **Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?** | Tsinghua LeapLab, 2025. Strictly speaking not a recommender systems paper, but a critical analysis of RLVR (Reinforcement Learning with Verifiable Rewards). Finds that current RLVR does not truly elicit reasoning ability beyond the base model, and that distillation works better. **Useful for understanding the design and limitations of the RL module in the OneRec series.** |

---

### Category 2: Cold Start and Two-Tower Architecture Enhancement

> **Core question**: While preserving the deployment efficiency of two-tower + ANN retrieval, how can retrieval quality be improved for cold start (new users / new items / sparse users)?

**This category contains 14 papers (including 8 in the two-tower improvement subfolder) — the second-largest direction in the collection.**

#### 2.1 Two-Tower Architecture Improvements

| # | Paper | Institution | Key Contribution |
|---|------|------|----------|
| 1 | **DAT: A Dual Augmented Two-tower Model for Online Large-scale Recommendation** | Meituan, 2021 | Proposes the Adaptive-Mimic Mechanism (AMM), which learns a customized augmented vector for each query and item to mitigate the lack of information interaction between the two towers; a Category Alignment Loss (CAL) aligns item representations across imbalanced categories. |
| 2 | **CL-EPIDTN: Contrastive Learning-Enhanced Personalized Interaction Dual Tower Network** | PLoS One, 2025 | Integrates a multi-layer Transformer to capture dynamic user preferences; introduces a dual-path personalized enhancement mechanism to strengthen user-item feature dependencies; uses contrastive learning to improve representations of long-tail items and low-activity users. |
| 3 | **HIT Model: A Hierarchical Interaction-Enhanced Two-Tower Model for Pre-Ranking Systems** | Tencent, CIKM 2025 | Proposes a **hierarchical interaction-enhanced two-tower model**: a generator pre-produces global vectors containing coarse-grained user-ad interactions, and a multi-head representer projects them into multiple subspaces to capture fine-grained interests. On Tencent's advertising platform: GMV +1.66%, ROI +1.55%. |
| 4 | **Tricolore: Multi-Behavior User Profiling for Enhanced Candidate Generation** | Renmin Univ / WeChat, IEEE TKDE | A multi-behavior user profiling framework: leverages multiple types of user feedback (view / click / favorite / purchase) to produce multi-vector representations, uses a behavior-level multi-view fusion module to dynamically enhance learning, and applies a popularity-balanced strategy to trade off accuracy and diversity. Significant gains for cold-start users. |

#### 2.2 Dedicated Cold-Start Solutions

| # | Paper | Institution | Key Contribution |
|---|------|------|----------|
| 5 | **GAR: Generative Adversarial Framework for Cold-Start Item Recommendation** | Beihang/Tencent/Alibaba, SIGIR 2022 | Uses a GAN framework to resolve the seesaw problem in cold start (improving cold-item recommendation hurts warm items, and vice versa): the generator produces "fake" warm embeddings from content features, while the discriminator (the recommender) learns to both distinguish and rank, so that cold and warm item recommendation no longer interfere with each other. |
| 6 | **LLMTreeRec: Unleashing the Power of LLMs for Cold-Start Recommendations** | CityU HK / Huawei Noah's Ark, COLING 2025 | Uses LLMs to tackle system cold start: all items are organized into a tree, and the LLM retrieves efficiently by searching along the tree, greatly reducing token consumption. With zero training data, it approaches the performance of conventional deep recommendation models. Deployed in Huawei's industrial system. |
| 7 | **MotiR: Motivation-aware Retrieval for Long-Tail Recommendation** | Fudan/Taobao, ACL 2025 Industry Track | Uses an LLM to generate "purchase motivations" as semantic abstractions of an item's intrinsic attributes; fused with conventional features, they let the two-tower model capture semantic similarity among long-tail items. A gating network adaptively adjusts the weights: long-tail items lean on semantics, while popular items retain collaborative filtering signals. CTR and CVR both improve by 4%+ in Taobao's 88VIP scenario. |
| 8 | **Next-User Retrieval: Enhancing Cold-Start Recommendations via Generative Next-User Modeling** | ByteDance, 2025 | Inverts the problem: rather than predicting "which item to recommend to a user," it predicts "who the item's next potential user is." A Transformer models the sequence of users who have interacted with an item and generatively predicts the next likely user. Online on Douyin: DAU +0.0142%, posting volume +0.1144%. |

#### 2.3 Survey / Research Document

| # | Paper | Notes |
|---|------|------|
| 9 | **Cold-Start Retrieval Enhancement Under a Strict Two-Tower Retrieval Architecture (2024–2026): Practical Methods and Recipes** | A systematic survey report focused on cold-start improvements under the constraint of "not breaking pure two-tower serving." It summarizes three practical directions: (1) content / multi-source information enhancement + multi-task unified representations (representative: OmniSearchSage); (2) multi-interest / multi-vector retrieval (representative: Pinterest multi-embedding); (3) training-side sampling and contrastive learning (representative: Mixed Negative Sampling). **A highly practical technical roadmap.** |

#### 2.4 Technical Foundations in This Category

| # | Paper | Notes |
|---|------|------|
| 10 | **RQ-VAE: Autoregressive Image Generation using Residual Quantization** | POSTECH/Kakao Brain, CVPR 2022. Proposes the Residual Quantized VAE, which uses residual quantization to precisely compress image features into stacked sequences of discrete codes. **The core technical foundation of Semantic IDs in generative recommenders such as TIGER and OneRec.** |
| 11 | **Indexing Shared Content in Information Retrieval Systems** | Yahoo/Google/IBM. A classic IR paper on index optimization for duplicated/shared content. Uses a tree-structured document representation to reduce index size and query time. |
| 12 | **ReAct: Synergizing Reasoning and Acting in Language Models** | Princeton/Google Brain, ICLR 2023. Proposes the ReAct framework, in which an LLM interleaves reasoning traces and actions. Strong results on HotpotQA and WebShop. **A methodological reference for applying LLM agents in recommender systems.** |
| 13 | **RankMixer: Scaling Up Ranking Models in Industrial Recommenders** | ByteDance, 2025 | Proposes a hardware-aware, unified, scalable feature-interaction architecture: multi-head token mixing replaces quadratic attention, per-token FFNs preserve feature-subspace modeling, and Sparse-MoE scales the model to a billion parameters. MFU rises from 4.5% to 45%, and parameters scale by two orders of magnitude with unchanged inference latency. Online on Douyin: active days +0.3%, usage duration +1.08%. **Although filed under cold start, it is really more about ranking-model scaling.** |

---

### Category 3: I2U Retrieval (Creator-Side Recommendation)

> **Core idea**: Starting from the item's perspective, find the most suitable users for each piece of content, improving the creator experience and the platform's content ecosystem.

| # | Paper | Institution | Key Contribution |
|---|------|------|----------|
| 1 | **DualRec: Creator-Side Recommender System** | Kuaishou, WWW 2025 | Proposes DualRec, a creator-side recommender system that answers "how to find the most suitable users for each item." Conventional user-side algorithms (retrieval/ranking) can be adapted into creator-side versions with simple modifications. Addresses the user availability problem (users have limited attention). Deployed at Kuaishou (100M+ users, 10M+ creators), significantly improving the creator experience. |
| 2 | **Next-User Retrieval** | ByteDance, 2025 | (Same as paper 8 in Section 2.2.) Uses a generative approach to predict an item's next potential user. Complementary to DualRec: DualRec leans toward an engineering solution, while Next-User Retrieval leans toward generative modeling. |

---

### Category 4: LLM Foundation Models and Embeddings

> **Core question**: How can the semantic understanding of LLMs be used to build high-quality general-purpose embedding models that serve the representation layer of recommender systems?

#### 4.1 LLM Backbones for Recommendation

| # | Paper | Institution | Key Contribution |
|---|------|------|----------|
| 1 | **HLLM: Enhancing Sequential Recommendations via Hierarchical Large Language Models** | ByteDance, 2024 | Proposes a two-level LLM architecture: an Item LLM extracts content features from text descriptions → a User LLM models the user's interest sequence to predict future behavior. Validates the value of LLM pre-trained weights (world knowledge) for recommendation, as well as the necessity of fine-tuning and scaling. The largest configuration uses two 7B models and achieves SOTA on PixelRec and Amazon Reviews. |
| 2 | **LUM: Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm** | Alibaba, 2025 | Proposes the Large User Model: a three-step paradigm that closes the gaps between E2E-GR methods and traditional DLRMs in features, architecture, and practice. Performance keeps improving up to 7B parameters (scaling law), validated in Alibaba's industrial applications. |
| 3 | **NoteLLM: A Retrievable Large Language Model for Note Recommendation** | USTC / Xiaohongshu, WWW 2024 | Uses an LLM for I2I note recommendation: a Note Compression Prompt compresses each note into a single special token, and contrastive learning trains embeddings of related notes; instruction tuning is used simultaneously to auto-generate tags/categories. Deployed at Xiaohongshu. |
| 4 | **MiniOneRec: An Open-Source Framework for Scaling Generative Recommendation** | USTC / NUS, 2025 | **The first fully open-source generative recommendation framework.** End-to-end workflow: RQ-VAE builds Semantic IDs → SFT → recommendation-oriented RL. Validates scaling laws with Qwen 0.5B–7B. Proposes full-pipeline SID alignment and hybrid-reward RL. Open-sourced on GitHub and HuggingFace. |

#### 4.2 General-Purpose Embedding Models

| # | Paper | Institution | Key Contribution |
|---|------|------|----------|
| 5 | **Gemini Embedding: Generalizable Embeddings from Gemini** | Google, 2025 | A SOTA general-purpose embedding model built on the Gemini LLM. Comprehensively surpasses prior work on MMTEB (100+ tasks, 250+ languages). A single unified model achieves SOTA across multilingual, English, and code. |
| 6 | **Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models** | Alibaba Tongyi Lab, 2025 | A family of embedding and reranking models (0.6B/4B/8B) built on the Qwen3 LLM. Multi-stage training (large-scale unsupervised pre-training + high-quality supervised fine-tuning) plus a model-merging strategy. SOTA on MTEB multilingual, code retrieval, and cross-lingual retrieval. Open-sourced under Apache 2.0. |

---

### Category 5: Multimodal VLMs (Vision-Language Models)

> **Core question**: How can vision-language models be turned into strong multimodal embedding models that support image, text, and video understanding in recommender systems?

| # | Paper | Institution | Key Contribution |
|---|------|------|----------|
| 1 | **VLM2Vec: Training Vision-Language Models for Massive Multimodal Embedding Tasks** | U of Waterloo / Salesforce, 2024 | Proposes MMEB (Massive Multimodal Embedding Benchmark, 36 datasets) and the VLM2Vec contrastive training framework, which converts any VLM into an embedding model that accepts arbitrary image-text combinations plus task instructions. Based on models such as Phi-3.5-V, LoRA fine-tuning alone yields 10–20% gains. **Reveals that "VLMs are themselves powerful hidden embedding models."** |
| 2 | **VLM2Vec-V2: Advancing Multimodal Embedding for Videos, Images, and Visual Documents** | Salesforce / UCSB / Waterloo, 2025 | V2 extends to video and document modalities. Proposes the MMEB-V2 benchmark (adding five task types: video retrieval, temporal grounding, video classification, video QA, and document retrieval). Handles text / image / video / document inputs in a unified way, with strong performance across all modalities. |

---

### Category 6: LLM Variants and Architectural Innovation

> **Core question**: How can the architectural evolution of LLMs themselves empower recommender systems?

| # | Paper | Institution | Key Contribution |
|---|------|------|----------|
| 1 | **CALM: Continuous Autoregressive Language Models** | Tencent WeChat AI, 2025 | Moves from discrete next-token prediction to **continuous next-vector prediction**: a high-fidelity autoencoder compresses K tokens into one continuous vector (>99.9% reconstruction accuracy), reducing the number of generation steps by a factor of K. Develops a complete likelihood-free framework (training / evaluation / controllable sampling). **Suggestive for continuous representations of Semantic IDs in recommender systems.** |
| 2 | **AgenticTagger: Structured Item Representation for Recommendation with LLM Agents** | Google DeepMind / UCSD, 2025 | Uses an LLM agent framework to produce structured item representations for recommender systems (ordered coarse-to-fine sequences of textual descriptors). Two stages: (1) vocabulary construction (an architect LLM iteratively refines while annotator LLMs validate in parallel); (2) vocabulary assignment. Improves generative retrieval, term-based retrieval, ranking, and critique-based recommendation. |
| 3 | **COEF-VQ: Cost-Efficient Video Quality Understanding through a Cascaded Multimodal LLM Framework** | TikTok, 2024 | An industrial video quality understanding solution: an MLLM fusing visual / text / audio signals + a cascaded framework (a lightweight model pre-screens, the MLLM makes fine-grained judgments), greatly reducing GPU consumption. Deployed on TikTok's video management platform. **Directly relevant to the content understanding module of recommender systems.** |

---

### Category 7: Classic Fine-Ranking Model Optimization and Scaling

> **Core question**: Can recommendation ranking models exhibit scaling laws the way LLMs do?

| # | Paper | Institution | Key Contribution |
|---|------|------|----------|
| 1 | **Wukong: Towards a Scaling Law for Large-Scale Recommendation** | Meta AI, ICML 2024 | A network architecture based on Stacked Factorization Machines plus a synergistic upscaling strategy. Captures feature interactions of arbitrary order through taller and wider layers. Consistently outperforms SOTA on 6 public datasets, and validates scaling laws across two orders of magnitude (beyond 100 GFLOP/example) on Meta's internal large-scale dataset. **A milestone for scaling laws in recommendation.** |
| 2 | **RankMixer** | ByteDance, 2025 | (See paper 13 in the cold-start category.) A hardware-aware, unified, scalable ranking architecture; MFU from 4.5% to 45%; a 1B dense-parameter model is deployed on full traffic. |

---

### Category 8: Watch Time Prediction

> **Core question**: In short-video scenarios, how can user watch time be predicted accurately while handling distributional imbalance?

| # | Paper | Institution | Key Contribution |
|---|------|------|----------|
| 1 | **CREAD: Classification-Restoration Framework with Error Adaptive Discretization for Watch Time Prediction** | Kuaishou, AAAI 2024 | Reformulates watch time prediction as multi-class classification. Core innovation: Error-Adaptive Discretization (EAD), which theoretically analyzes how discretization affects learning error and restoration error and achieves an optimal balance between the two. Fully launched in the Kuaishou app, increasing watch time by 0.29%. |
| 2 | **EGMN: Multi-Granularity Distribution Modeling for Video Watch Time Prediction via Exponential-Gaussian Mixture Network** | Xiaohongshu, RecSys 2025 | Models watch time from a distributional perspective: identifies skewness at the coarse level (concentration of quick skips) and diversity at the fine level (varied interaction patterns). Proposes an Exponential-Gaussian Mixture distributional assumption, parameterized by the EGMN network. Outperforms SOTA on Xiaohongshu's short-video scenario. Open-sourced. |

---

### Category 9: Interest Modeling

| # | Paper | Institution | Key Contribution |
|---|------|------|----------|
| 1 | **Trinity: Syncretizing Multi-/Long-tail/Long-term Interests All in One** | ByteDance, 2025 | A unified framework that addresses "interest forgetting" across multi-interest, long-tail, and long-term interests simultaneously. Builds a real-time clustering system that maps items into enumerable clusters and computes statistical interest histograms; identifies under-delivered topics and stays stable when trending topics emerge. Deployed in Douyin's retrieval stage, significantly improving user experience and retention. |

---

### Category 10: Diffusion Modeling (Diffusion Models and Generative Modeling)

> **Core question**: How can continuous generative models such as diffusion models and flow matching be used to model distributional representations, uncertainty, and preference dynamics in recommendation?

**This category contains 3 papers (in this collection) + 10 recommended papers, covering foundational methods, recommendation applications, and training theory.**

#### 10.1 Papers in This Collection

| # | Paper | Institution | Venue/Year | Key Contribution |
|---|------|------|-----------|----------|
| 1 | **DiffuRec: A Diffusion Model for Sequential Recommendation** | Wuhan University / NTU | TOIS 2023 | **The first to bring diffusion models into sequential recommendation.** Upgrades item representations from fixed vectors to distributions: in the forward process, the target item embedding is noised into a Gaussian distribution, and a Transformer Approximator reconstructs the target item. Training uses a cross-entropy loss (instead of the standard MSE); at inference, multi-step reverse denoising is followed by Rounding (a full inner-product search) to map back to discrete items. A random scaling factor $\lambda_i \sim \mathcal{N}(\delta, \delta)$ introduces uncertainty, yielding notable gains on long-tail items. Substantially outperforms SASRec/BERT4Rec on four datasets. Limitations: high multi-step inference latency; validated only on academic datasets. |
| 2 | **Flow Matching for Generative Modeling** | **Meta AI (FAIR)** / Weizmann Institute | ICLR 2023 | **A new paradigm for generative modeling that unifies and surpasses diffusion models.** Proposes Conditional Flow Matching (CFM): by decomposing into conditional probability paths and conditional vector fields, it enables simulation-free training of CNFs with gradients equivalent to the FM objective (Theorem 2). The core innovation is the **Optimal Transport (OT) path**: a linear mean plus linear standard deviation yields straight-line trajectories, reducing sampling NFE by 40%+ and achieving SOTA NLL/FID across the board on ImageNet. Implication for RecSys: it can replace the DDPM in DiffuRec to greatly improve inference efficiency. |
| 3 | **Learning Dynamics of LLM Finetuning** | UBC / Amii | **ICLR 2025** | A unified analysis of the learning dynamics of SFT/DPO: $\Delta \log \pi_t(x_o) = -\eta \cdot A_t \cdot K_t \cdot G_t$. The most important finding is the **Squeezing Effect**: when a negative gradient is applied to a softmax (e.g., on $y^-$ in DPO), probability mass is "squeezed" onto the argmax token. The sharper the distribution, the stronger the squeezing; and the less likely $y^-$ is, the stronger the squeezing. This explains why off-policy DPO trained for too long causes the probabilities of all outputs to drop and text to degenerate. Proposes an "extend" strategy (also training on $y^-$ during SFT) to mitigate squeezing, significantly improving win-rate. **Directly relevant to understanding DPO preference alignment in the OneRec series.** |

#### 10.2 Recommended Papers in the Field (Diffusion in RecSys Survey)

> The following 10 papers are important works on diffusion models in recommender systems, grouped by direction. Industry papers and top-venue publications are prioritized.

**A. Collaborative Filtering**

| # | Paper | Institution | Venue/Year | Key Contribution | Why Read It |
|---|------|------|-----------|----------|----------|
| 4 | **DiffRec: Recommender Systems with Generalized Diffusion Models** | NUS | WSDM 2023 | **The first to apply diffusion to collaborative filtering.** Takes user-item interaction vectors as input and recovers corrupted interaction signals via forward noising + reverse denoising. Proposes L-DiffRec (Latent Diffusion, diffusing in a VAE latent space for dimensionality reduction) and T-DiffRec (Temporal Diffusion, handling temporal information). | A pioneering work in this direction, complementary to DiffuRec's "generate the item embedding" approach. Highly cited. |

**B. Sequential Recommendation**

| # | Paper | Institution | Venue/Year | Key Contribution | Why Read It |
|---|------|------|-----------|----------|----------|
| 5 | **DreamRec: Generate What You Prefer — Towards Controllable Recommendation via Diffusion Models** | Zhejiang University / Microsoft | SIGIR 2023 | Proposes replacing the "discriminative paradigm" with a "generative paradigm": rather than using contrastive learning to distinguish positives from negatives, it uses diffusion to directly **generate** the oracle embedding of the target item from the history sequence. No negative sampling is required, and it is the first to apply **Classifier-Free Guidance (CFG)** in recommendation for controllable recommendation. | Explicitly frames the discriminative vs. generative paradigm debate in recommendation; first application of CFG in recommendation; conceptually influential. |
| 6 | **CDDRec: Conditional Denoising Diffusion for Sequential Recommendation** | Microsoft Research | CIKM 2023 | Conditional denoising diffusion for sequential recommendation: the user's history sequence is encoded as a conditioning signal that guides item embedding generation in the reverse process. Introduces cross-attention to fuse the condition with the diffusion state. | A direct improvement on DiffuRec (explicit conditional generation instead of implicit conditioning). Microsoft Research background. |

**C. Data Augmentation**

| # | Paper | Institution | Venue/Year | Key Contribution | Why Read It |
|---|------|------|-----------|----------|----------|
| 7 | **Diff4Rec: Diffusion Recommender Model** | Beihang / **Alibaba** | SIGIR 2023 | Generates synthetic user embeddings via forward-reverse diffusion in the user representation space to augment training data. Combined with curriculum learning (low-noise synthetic data first, then gradually increasing noise). | **Alibaba industrial background.** "Diffusion for data augmentation" is more pragmatic than direct prediction and more likely to land in industry. |
| 8 | **DiffASR: Diffusion Augmentation for Sequential Recommendation** | Rutgers / **Amazon** | CIKM 2023 | Applies diffusion-denoising to users' historical interaction sequences to generate augmented sequences. **Plug-and-play**: integrates seamlessly into the training pipeline of any sequential recommender (SASRec, BERT4Rec, etc.). | **Amazon industrial background.** No changes to the downstream model architecture are needed, so it adapts well to industry. |

**D. Cross-Domain / Knowledge-Enhanced Recommendation**

| # | Paper | Institution | Venue/Year | Key Contribution | Why Read It |
|---|------|------|-----------|----------|----------|
| 9 | **DCDR: Diffusion Cross-domain Recommendation** | Renmin University / **Tencent** | AAAI 2024 | The first to use diffusion for cross-domain recommendation: diffusion transforms source-domain user embeddings into target-domain user embeddings, avoiding the information loss of direct domain mapping. Designs a timestamp-based Diffusion Guidance mechanism. | **Tencent industrial background.** Cross-domain recommendation is a core industry need, and the denoising nature of diffusion naturally suits inter-domain transformation. |
| 10 | **DiffKG: Knowledge Graph Enhanced Diffusion for Recommendation** | USTC | AAAI 2024 | Injects knowledge graph information into a diffusion recommendation framework: the forward process adds noise selectively according to KG structure (preserving KG neighbor information), and the reverse process uses KG-aware attention to guide denoising. | At the intersection of KG and diffusion; helpful for interpretability and cold start. |

**E. Preference Dynamics Modeling**

| # | Paper | Institution | Venue/Year | Key Contribution | Why Read It |
|---|------|------|-----------|----------|----------|
| 11 | **PDRec: Preference Dynamics for Recommendation via Diffusion Models** | Multiple institutions | NeurIPS 2024 | Uses score-based diffusion (SDE perspective) to model the **dynamic evolution** of user preferences: user preference is treated as a time-varying distribution whose trajectory is modeled, enabling sampling of user preference at any future time point. | Understands the role of diffusion in recommendation from a temporal-dynamics perspective; theoretically strong; NeurIPS. |

**F. Flow Matching in Industry**

| # | Paper | Institution | Venue/Year | Key Contribution | Why Read It |
|---|------|------|-----------|----------|----------|
| 12 | **RecFlow: An Industrial Full Flow Recommendation Dataset** | **Kuaishou** | 2024 | Releases Kuaishou's full-pipeline recommendation dataset (retrieval → impression) and methodologically explores **applying Flow Matching across the full recommendation pipeline**, modeling multi-stage filtering as a continuous normalizing flow. | **Kuaishou industrial practice.** A direct attempt to apply Flow Matching (included in this collection) to recommendation. |

**G. Survey**

| # | Paper | Notes |
|---|------|------|
| 13 | **A Survey on Diffusion Models for Recommender Systems** | arXiv 2024 survey. Systematically categorizes existing work into: (1) data engineering and augmentation; (2) representation enhancement; (3) direct recommendation. Summarizes open problems: inference efficiency, adaptation to discrete spaces, controllability, and evaluation. **The best entry point for building a global view.** |

#### 10.3 Suggested Reading Path

```
1. Survey → build a global picture
2. DiffRec (WSDM'23) → pioneering work in collaborative filtering
3. DiffuRec (TOIS'23) → pioneering work in sequential recommendation (in this collection)
4. DreamRec (SIGIR'23) → understand the "generative vs. discriminative" paradigm debate
5. Flow Matching (ICLR'23) → the theoretical upgrade of diffusion (in this collection)
6. CDDRec / DiffASR → two practical routes: conditional generation & data augmentation
7. Diff4Rec / DCDR → industrial (Alibaba / Tencent) practice
8. Learning Dynamics (ICLR'25) → understand DPO/SFT training dynamics (in this collection)
```

---

## 3. Cross-Category Technical Relationship Map

```
                    ┌──────────────────────────────────────────┐
                    │        LLM Foundation Models             │
                    │  (Gemini Emb / Qwen3 Emb / CALM)        │
                    └──────────┬───────────────┬───────────────┘
                               │               │
                    ┌──────────▼──────┐  ┌─────▼───────────────┐
                    │  Multimodal VLM │  │  LLM-based RecSys   │
                    │ (VLM2Vec v1/v2) │  │ (HLLM / LUM /       │
                    │ (COEF-VQ)       │  │  NoteLLM / MotiR)    │
                    └─────────────────┘  └─────┬───────────────┘
                                               │
          ┌────────────────────────────────────┼────────────────────────┐
          │                                    │                        │
┌─────────▼──────────┐            ┌────────────▼──────────┐   ┌────────▼──────────┐
│ Semantic ID + GR   │            │  Two-Tower Enhancement│   │  Ranking Scaling   │
│ (TIGER → PLUM →    │            │  (DAT/HIT/CL-EPIDTN   │   │  (Wukong /         │
│  OneRec → V2)      │            │   GAR/MotiR/Tricolore) │   │   RankMixer)       │
│ (TermID/LMIndexer) │            │  + Cold Start          │   │                    │
│ (MiniOneRec)       │            │  (LLMTreeRec/          │   │                    │
│ (AgenticTagger)    │            │   Next-User Retrieval)  │   │                    │
└────────┬───────────┘            └────────────────────────┘   └────────────────────┘
         │                                    │
         │   ┌───────────────────────┐        │
         ├──►│ Diffusion Modeling    │◄───────┘
         │   │ (DiffuRec/DreamRec/  │
         │   │  Flow Matching/      │
         │   │  Diff4Rec/DCDR)      │
         │   └───────────────────────┘
         │                                    │
         │         ┌─────────────────┐        │
         └────────►│ I2U / Creator   │◄───────┘
                    │ (DualRec /      │
                    │  Next-User Ret.)│
                    └─────────────────┘
```

---

## 4. Key Findings and Trends

### 4.1 Generative recommendation is moving from experiments to large-scale deployment
- The **OneRec series** (Kuaishou) and **PLUM** (YouTube) mark the validation of end-to-end generative recommendation on platforms with hundreds of millions of users.
- OneRec-V2's Lazy Decoder-Only architecture and 8B-parameter scale show that generative recommendation is catching up with the LLM scaling trajectory.

### 4.2 Semantic IDs are the key bridge between LLMs and recommender systems
- From TIGER (2023) to PLUM/OneRec (2025), Semantic IDs have evolved from an academic concept into an industry standard.
- TermID explores a return to natural-language tokens, consistent with the direction of AgenticTagger.

### 4.3 The two-tower architecture is still viable, but requires systematic enhancement
- Work such as HIT/DAT/Tricolore shows that the two-tower architecture can keep improving through enhanced interaction, multi-behavior modeling, and contrastive learning.
- MotiR shows how LLM-generated semantic features can be fused with a conventional two-tower model — an excellent example of "LLMs empowering traditional architectures."

### 4.4 Scaling laws are emerging in recommendation
- Wukong (Meta) was the first to validate scaling laws in recommendation.
- OneRec, PLUM, LUM, and RankMixer further confirm that both generative and traditional ranking models can keep improving as parameter counts grow.

### 4.5 Multimodality and the creator side are emerging directions
- The VLM2Vec series points to a new paradigm of "using VLMs as general-purpose multimodal embedders."
- DualRec / Next-User Retrieval open a new track for optimizing recommendation from the creator's perspective.

### 4.6 Diffusion / Flow Matching bring a new paradigm of distributional modeling to recommendation
- DiffuRec was the first to upgrade item representations from "point estimates" to "distribution estimates," which naturally fits uncertainty and multi-interest modeling in recommendation.
- The OT path of Flow Matching (Meta FAIR) can improve diffusion inference efficiency by 40%+, addressing the core bottleneck for industrial deployment.
- "Diffusion for data augmentation" (Diff4Rec / DiffASR) is a more pragmatic route to industrial deployment than direct prediction.
- The squeezing effect (Learning Dynamics) is directly relevant to understanding the behavior of DPO preference alignment in systems such as OneRec and PLUM.

---

## 5. Suggested Reading Order

**If you are a recommender systems engineer, the following reading order is suggested:**

1. **Getting started with generative recommendation**: TIGER → OneRec (KDD paper) → OneRec Technical Report → OneRec-V2
2. **Understanding Semantic IDs in industrial deployment**: PLUM → BETTER GENERALIZATION WITH SEMANTIC IDS → LMIndexer → TermID
3. **Two-tower cold-start solutions (production-ready)**: the strict two-tower survey report → DAT → HIT → MotiR → Next-User Retrieval
4. **LLM + recommender systems**: HLLM → LUM → NoteLLM → LLMTreeRec → AgenticTagger
5. **Scaling and efficiency**: Wukong → RankMixer → CALM → MiniOneRec
6. **Embedding / multimodal foundations**: Gemini Embedding → Qwen3 Embedding → VLM2Vec → VLM2Vec-V2
7. **Watch time modeling**: CREAD → EGMN
8. **Interest modeling**: Trinity
9. **Diffusion Modeling**: Survey → DiffRec → DiffuRec → DreamRec → Flow Matching → Diff4Rec/DiffASR → Learning Dynamics

---

*Note: This report is based on each paper's abstract, introduction, and core methodology sections. Some papers appear in multiple folders (e.g., TIGER and Next-User Retrieval), reflecting cross-category technical connections. The 10 recommended papers in the Diffusion Modeling category are based on a survey of the field from 2023–2025, prioritizing representative works with industrial backgrounds (Alibaba / Tencent / Amazon / Kuaishou / Microsoft) and top-venue publications.*
