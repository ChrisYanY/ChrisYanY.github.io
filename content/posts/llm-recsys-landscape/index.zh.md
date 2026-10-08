---
title: "推荐系统 × 大模型：41 篇论文的分类阅读报告"
date: 2026-02-26
summary: "分类梳理 2022–2025 年推荐与大模型交叉领域的 41 篇论文，涵盖语义 ID 生成式检索、双塔冷启动、排序 Scaling 与扩散模型。"
label: "文献综述"
tags: ["生成式推荐", "大语言模型", "语义 ID", "冷启动", "扩散模型"]
math: true
mermaid: false
translationKey: "llm-recsys-landscape"
ai_assisted: true
---

**日期：2026年2月24日**
**文献总数：44篇（含重复收录）**

---

## 一、总览

本文件夹收录了 2022-2025 年间推荐系统与大语言模型交叉领域的 41 篇论文，涵盖了从传统双塔召回到端到端生成式推荐的完整技术演进路线。论文来源覆盖 Google DeepMind、ByteDance（抖音）、Kuaishou（快手）、Alibaba、Meta、Xiaohongshu（小红书）、TikTok、Pinterest、Tencent 等业界一线团队，以及 Princeton、UIUC、USTC 等学术机构。

从技术脉络看，这批文献围绕以下核心问题展开：
1. **如何用生成式范式重构推荐系统的召回与排序？**（Semantic ID + Generative Retrieval）
2. **如何将 LLM 的世界知识和语义理解能力引入推荐？**（LLM-based Recommendation）
3. **如何在双塔架构约束下解决冷启动与长尾问题？**（Cold Start / Two-Tower Enhancement）
4. **如何实现推荐模型的 Scaling Law？**（Large User Model / Ranking Scaling）
5. **如何利用多模态信息增强推荐理解？**（VLM / Multimodal Embedding）
6. **如何用 Diffusion/Flow 等生成模型建模推荐中的不确定性与分布表征？**（Diffusion Modeling）

---

## 二、分类详述

---

### 第一大类：Semantic IDs 与生成式检索（Generative Retrieval）

> **核心思想**：用 RQ-VAE 等方法将 item 编码为离散语义 ID 序列，将推荐转化为自回归序列生成任务，从而打破传统 retrieve-and-rank 的多阶段级联架构。

**本类共 10 篇，是本文件夹中数量最多、体系最完整的一个方向。**

#### 1.1 奠基性工作

| # | 论文 | 机构 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|----------|
| 1 | **TIGER: Recommender Systems with Generative Retrieval** | Google DeepMind | NeurIPS 2023 | 提出 Semantic ID（语义 ID）概念：用 RQ-VAE 将 item 编码为离散语义码字元组，训练 Transformer seq-to-seq 模型自回归预测下一个 item 的 Semantic ID。在多个数据集上显著超越 SOTA 双塔检索，并对零交互 item 表现出更好的泛化能力。**本方向的开山之作。** |
| 2 | **Language Models as Semantic Indexers (LMIndexer)** | UIUC / Amazon | ICML 2024 | 提出自监督框架学习语义 ID：利用生成式语言模型通过渐进训练和对比学习生成层次化的离散 ID 表示，用文档重建目标解决语义监督不足问题。在推荐、商品搜索、文档检索三类任务上验证有效性。 |
| 3 | **BETTER GENERALIZATION WITH SEMANTIC IDS** | Google DeepMind / YouTube | 2024 | 研究 Semantic ID 在工业级排序模型中替代随机 ID 的效果。提出 SentencePiece 分词方法对 Semantic ID 序列进行 sub-piece 哈希，在 YouTube 排序模型上验证了对新物品和长尾物品的泛化提升，且不牺牲整体质量。 |

#### 1.2 工业级端到端系统

| # | 论文 | 机构 | 年份 | 核心贡献 |
|---|------|------|------|----------|
| 4 | **OneRec: Unifying Retrieve and Rank with Generative Recommender** | Kuaishou | 2024 | **首个在真实场景中显著超越传统级联推荐系统的端到端生成式模型。** 采用 Encoder-Decoder + MoE 架构，提出 session-wise generation（替代逐条生成），结合 DPO 偏好对齐。已部署于快手。 |
| 5 | **OneRec Technical Report** | Kuaishou | 2025 | OneRec 的完整技术报告。亮点：计算 FLOPs 提升 10x 并发现推荐领域的 Scaling Law；RL 技术在该框架下展现巨大潜力；训练 MFU 达 23.7%，推理 MFU 达 28.8%；OPEX 仅为传统管线的 10.6%。已在快手/快手极速版处理 25% QPS，App Stay Time 提升 0.54%/1.24%。 |
| 6 | **OneRec-V2 Technical Report** | Kuaishou | 2025 | 针对 V1 的两大瓶颈：(1) Encoder-Decoder 中 97.66% 算力消耗在编码而非生成；(2) 基于 Reward Model 的 RL 效率低且易 reward hacking。提出 **Lazy Decoder-Only 架构**（总算力减少 94%，训练资源减少 90%）；成功扩展到 8B 参数；引入基于真实用户反馈的偏好对齐（Duration-Aware Reward Shaping + Adaptive Ratio Clipping）。App Stay Time 再提升 0.467%/0.741%。 |
| 7 | **PLUM: Adapting Pre-trained LLMs for Industrial-scale Generative Recommendations** | Google DeepMind / YouTube | 2025 | 将预训练 LLM 适配为工业级生成式推荐：Item Tokenization（Semantic ID）→ Continued Pre-training → Task-specific Fine-tuning。在 YouTube 大规模视频推荐中显著超越基于大 Embedding Table 的生产模型，已服务数十亿用户。**LLM + Semantic ID 在 YouTube 的首次大规模落地。** |

#### 1.3 Semantic ID 改进与变体

| # | 论文 | 机构 | 年份 | 核心贡献 |
|---|------|------|------|----------|
| 8 | **TermID (GRLM): LLM-Based Generative Recommendation via Structured Term Identifiers** | Kuaishou | 2025 | 提出 **Term ID** 替代传统 Semantic ID：用语义丰富的标准化文本关键词作为 item 标识符，避免 SID 与 LLM 原生词汇表之间的语义鸿沟。框架包含 Context-aware Term Generation、Integrative Instruction Fine-tuning、Elastic Identifier Grounding。 |
| 9 | **OneSug: Unified End-to-End Generative Framework for E-commerce Query Suggestion** | Kuaishou | 2025 | 将端到端生成式范式应用于电商搜索 query suggestion。包含 prefix2query 表征增强、Encoder-Decoder 生成模型、reward-weighted ranking。已在快手电商全量部署，CTR +2.01%，Order +2.04%，Revenue +1.69%。 |

#### 1.4 本类中的辅助参考论文

| # | 论文 | 说明 |
|---|------|------|
| 10 | **Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?** | 清华 LeapLab，2025。严格来说不属于推荐系统，而是对 RLVR（Reinforcement Learning with Verifiable Rewards）的批判性分析。发现当前 RLVR 并未真正激发超越 base model 的推理能力，distillation 效果更好。**对理解 OneRec 系列中 RL 模块的设计和局限性有参考价值。** |

---

### 第二大类：冷启动与双塔架构增强

> **核心问题**：在保持双塔 + ANN 检索的部署效率前提下，如何提升冷启动（新用户/新物品/稀疏用户）的召回质量？

**本类共 14 篇（含双塔改进子目录 8 篇），是本文件夹的第二大方向。**

#### 2.1 双塔架构改进

| # | 论文 | 机构 | 核心贡献 |
|---|------|------|----------|
| 1 | **DAT: A Dual Augmented Two-tower Model for Online Large-scale Recommendation** | Meituan, 2021 | 提出 Adaptive-Mimic Mechanism（AMM）为每个 query 和 item 定制增强向量，缓解双塔信息交互不足；Category Alignment Loss（CAL）对齐不均匀类别的 item 表示。 |
| 2 | **CL-EPIDTN: Contrastive Learning-Enhanced Personalized Interaction Dual Tower Network** | PLoS One, 2025 | 集成多层 Transformer 捕捉动态用户偏好；引入双路径个性化增强机制强化 user-item 特征依赖；对比学习增强长尾 item 和低活跃用户的表示学习。 |
| 3 | **HIT Model: A Hierarchical Interaction-Enhanced Two-Tower Model for Pre-Ranking Systems** | Tencent, CIKM 2025 | 提出 **层次化交互增强双塔模型**：通过 generator 预生成含粗粒度 user-ad 交互的全局向量，multi-head representer 投射到多个子空间捕获细粒度兴趣。在腾讯广告平台 GMV +1.66%，ROI +1.55%。 |
| 4 | **Tricolore: Multi-Behavior User Profiling for Enhanced Candidate Generation** | Renmin Univ / WeChat, IEEE TKDE | 多行为用户画像框架：利用多种用户反馈（浏览/点击/收藏/购买）生成多向量表示，行为级多视角融合模块动态增强学习，popularity-balanced 策略平衡准确性与多样性。对冷启动用户有显著提升。 |

#### 2.2 冷启动专项解决方案

| # | 论文 | 机构 | 核心贡献 |
|---|------|------|----------|
| 5 | **GAR: Generative Adversarial Framework for Cold-Start Item Recommendation** | Beihang/Tencent/Alibaba, SIGIR 2022 | 用 GAN 框架解决冷启动的 seesaw 问题（改善冷 item 推荐会损害热 item，反之亦然）：生成器从 content 特征生成"假"warm embedding，判别器（推荐模型）同时学习区分和排序，使冷热 item 推荐互不干扰。 |
| 6 | **LLMTreeRec: Unleashing the Power of LLMs for Cold-Start Recommendations** | CityU HK / Huawei Noah's Ark, COLING 2025 | 用 LLM 解决系统冷启动：将所有 item 组织为树结构，LLM 沿树搜索高效检索，大幅降低 token 消耗。在零训练数据下达到接近传统深度推荐模型的性能。已部署于华为工业系统。 |
| 7 | **MotiR: Motivation-aware Retrieval for Long-Tail Recommendation** | Fudan/Taobao, ACL 2025 Industry Track | 利用 LLM 生成"购买动机"作为 item 内在属性的语义抽象，与传统特征融合后使双塔模型能捕获长尾 item 的语义相似性。门控网络自适应调节权重：长尾 item 侧重语义，热门 item 保留协同过滤信号。淘宝 88VIP 场景 CTR/CVR 均提升 4%+。 |
| 8 | **Next-User Retrieval: Enhancing Cold-Start Recommendations via Generative Next-User Modeling** | ByteDance, 2025 | 反向思维：不预测"给用户推什么 item"，而是预测"item 的下一个潜在用户是谁"。用 Transformer 建模 item 的已交互用户序列，生成式预测下一个可能交互的用户。抖音上线 DAU +0.0142%，发布量 +0.1144%。 |

#### 2.3 综述/调研文档

| # | 论文 | 说明 |
|---|------|------|
| 9 | **坚持双塔检索架构下的冷启动召回增强（2024-2026）可落地方法与配方** | 系统性调研报告，聚焦"不破坏纯双塔 serving"约束下的冷启动改进。总结三大可落地方向：(1) 内容/多源信息增强 + 多任务统一表征（代表：OmniSearchSage）；(2) 多兴趣/多向量检索（代表：Pinterest multi-embedding）；(3) 训练侧采样与对比学习（代表：Mixed Negative Sampling）。**极具实践参考价值的技术路线图。** |

#### 2.4 本类中的技术基础论文

| # | 论文 | 说明 |
|---|------|------|
| 10 | **RQ-VAE: Autoregressive Image Generation using Residual Quantization** | POSTECH/Kakao Brain, CVPR 2022。提出 Residual Quantized VAE，用残差量化将图像特征精确压缩为堆叠离散码序列。**TIGER/OneRec 等生成式推荐中 Semantic ID 的核心技术基础。** |
| 11 | **Indexing Shared Content in Information Retrieval Systems** | Yahoo/Google/IBM。经典 IR 论文，研究重复/共享内容的索引优化。树状文档表示模型，减少索引大小和查询时间。 |
| 12 | **ReAct: Synergizing Reasoning and Acting in Language Models** | Princeton/Google Brain, ICLR 2023。提出 ReAct 框架让 LLM 交替生成推理链和动作。HotpotQA 和 WebShop 上效果显著。**作为 LLM Agent 在推荐系统中应用的方法论参考。** |
| 13 | **RankMixer: Scaling Up Ranking Models in Industrial Recommenders** | ByteDance, 2025 | 提出硬件感知的统一可扩展特征交互架构：用 multi-head token mixing 替代二次注意力，Per-token FFN 维持特征子空间建模，Sparse-MoE 扩展到十亿参数。MFU 从 4.5% 提升到 45%，参数量扩展两个数量级且推理延迟不变。抖音上线 active days +0.3%，usage duration +1.08%。**虽放在冷启动目录下，实际更偏排序模型 scaling。** |

---

### 第三大类：I2U 类召回（创作者侧推荐）

> **核心思想**：从 item 视角出发，为每个内容找到最合适的用户，提升创作者体验和平台内容生态。

| # | 论文 | 机构 | 核心贡献 |
|---|------|------|----------|
| 1 | **DualRec: Creator-Side Recommender System** | Kuaishou, WWW 2025 | 提出创作者侧推荐系统 DualRec：回答"如何为每个 item 找到最合适的用户"。传统 user-side 算法（检索/排序）可以简单修改适配为 creator-side 版本。解决了 user availability 问题（用户注意力有限）。已部署于快手（1亿+用户，1000万+创作者），显著提升创作者体验。 |
| 2 | **Next-User Retrieval** | ByteDance, 2025 | （同上 2.2 节第 8 篇）用生成式方法预测 item 的下一个潜在用户。与 DualRec 形成互补：DualRec 偏工程方案，Next-User Retrieval 偏生成式建模方案。 |

---

### 第四大类：LLM 基础模型与 Embedding

> **核心问题**：如何利用 LLM 的语义理解能力构建高质量的通用 Embedding 模型，服务于推荐系统的表征层？

#### 4.1 LLM Backbone 用于推荐

| # | 论文 | 机构 | 核心贡献 |
|---|------|------|----------|
| 1 | **HLLM: Enhancing Sequential Recommendations via Hierarchical Large Language Models** | ByteDance, 2024 | 提出两层 LLM 架构：Item LLM 从文本描述提取内容特征 → User LLM 建模用户兴趣序列预测未来行为。验证了 LLM 预训练权重（世界知识）对推荐的价值，以及 fine-tuning 和 scaling 的必要性。最大配置双 7B 参数，在 PixelRec 和 Amazon Reviews 上 SOTA。 |
| 2 | **LUM: Unlocking Scaling Law in Industrial Recommendation Systems with a Three-step Paradigm** | Alibaba, 2025 | 提出 Large User Model（大用户模型）：三步范式解决 E2E-GR 方法与传统 DLRM 在特征/架构/实践上的差距。扩展到 7B 参数仍保持性能提升（Scaling Law），已在阿里巴巴工业应用中验证。 |
| 3 | **NoteLLM: A Retrievable Large Language Model for Note Recommendation** | USTC / Xiaohongshu, WWW 2024 | 利用 LLM 进行 I2I 笔记推荐：Note Compression Prompt 将笔记压缩为单个特殊 token，对比学习训练相关笔记的 embedding；同时用 instruction tuning 实现自动生成标签/分类。已部署于小红书。 |
| 4 | **MiniOneRec: An Open-Source Framework for Scaling Generative Recommendation** | USTC / NUS, 2025 | **首个完全开源的生成式推荐框架**。端到端工作流：RQ-VAE 构建 Semantic ID → SFT → 推荐导向 RL。基于 Qwen 0.5B-7B 验证 Scaling Law。提出全流程 SID 对齐和混合奖励 RL。开源于 GitHub 和 HuggingFace。 |

#### 4.2 通用 Embedding 模型

| # | 论文 | 机构 | 核心贡献 |
|---|------|------|----------|
| 5 | **Gemini Embedding: Generalizable Embeddings from Gemini** | Google, 2025 | 基于 Gemini LLM 构建的 SOTA 通用 Embedding 模型。在 MMTEB（100+ 任务、250+ 语言）上全面超越前作。统一模型在多语言、英语、代码三个维度均达到 SOTA。 |
| 6 | **Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models** | Alibaba Tongyi Lab, 2025 | 基于 Qwen3 LLM 的 Embedding 和 Reranking 系列模型（0.6B/4B/8B）。多阶段训练（大规模无监督预训练 + 高质量监督 fine-tuning）+ 模型合并策略。在 MTEB 多语言/代码检索/跨语言检索上 SOTA。Apache 2.0 开源。 |

---

### 第五大类：多模态 VLM（视觉语言模型）

> **核心问题**：如何将视觉-语言模型转化为强大的多模态 Embedding 模型，支撑推荐系统中的图文视频理解？

| # | 论文 | 机构 | 核心贡献 |
|---|------|------|----------|
| 1 | **VLM2Vec: Training Vision-Language Models for Massive Multimodal Embedding Tasks** | U of Waterloo / Salesforce, 2024 | 提出 MMEB（大规模多模态 Embedding Benchmark，36 数据集）和 VLM2Vec 对比训练框架：将任意 VLM 转化为 Embedding 模型，支持任意图文组合 + 任务指令输入。基于 Phi-3.5-V 等模型，LoRA 微调即可提升 10-20%。**揭示"VLM 本身就是强大的隐藏 Embedding 模型"。** |
| 2 | **VLM2Vec-V2: Advancing Multimodal Embedding for Videos, Images, and Visual Documents** | Salesforce / UCSB / Waterloo, 2025 | V2 版本扩展到视频和文档模态。提出 MMEB-V2 benchmark（新增视频检索、时序定位、视频分类、视频 QA、文档检索 5 类任务）。统一处理文本/图像/视频/文档输入，在所有模态上均达到强性能。 |

---

### 第六大类：LLM 变体与架构创新

> **核心问题**：LLM 自身的架构演进如何赋能推荐系统？

| # | 论文 | 机构 | 核心贡献 |
|---|------|------|----------|
| 1 | **CALM: Continuous Autoregressive Language Models** | Tencent WeChat AI, 2025 | 从离散 next-token prediction 转向 **连续 next-vector prediction**：用高保真 autoencoder 将 K 个 token 压缩为一个连续向量（>99.9% 重建精度），生成步骤减少 K 倍。开发了完整的无似然框架（训练/评估/可控采样）。**对推荐系统中 Semantic ID 的连续化表示有启发意义。** |
| 2 | **AgenticTagger: Structured Item Representation for Recommendation with LLM Agents** | Google DeepMind / UCSD, 2025 | 用 LLM Agent 框架为推荐系统生成结构化 item 表示（有序的粗到细文本描述符序列）。两阶段：(1) 词汇构建（architect LLM 迭代优化 + annotator LLM 并行验证）；(2) 词汇分配。在生成式检索、term-based 检索、排序、critique-based 推荐等多场景提升。 |
| 3 | **COEF-VQ: Cost-Efficient Video Quality Understanding through a Cascaded Multimodal LLM Framework** | TikTok, 2024 | 工业级视频质量理解方案：融合视觉/文本/音频的 MLLM + 级联框架（轻量模型预筛 + MLLM 精细判断），大幅降低 GPU 消耗。已部署于 TikTok 视频管理平台。**对推荐系统中的内容理解模块有直接参考价值。** |

---

### 第七大类：传统精排模型优化与 Scaling

> **核心问题**：推荐排序模型能否像 LLM 一样展现 Scaling Law？

| # | 论文 | 机构 | 核心贡献 |
|---|------|------|----------|
| 1 | **Wukong: Towards a Scaling Law for Large-Scale Recommendation** | Meta AI, ICML 2024 | 基于堆叠分解机（Stacked Factorization Machines）的网络架构 + 协同扩展策略。通过更高更宽的层捕获任意阶特征交互。在 6 个公开数据集上一致超越 SOTA；在 Meta 内部大规模数据集上验证了跨两个数量级（超 100 GFLOP/example）的 Scaling Law。**推荐领域 Scaling Law 的里程碑工作。** |
| 2 | **RankMixer** | ByteDance, 2025 | （见冷启动类第 13 篇）硬件感知的统一可扩展排序架构，MFU 从 4.5% 到 45%，1B Dense 参数已全流量部署。 |

---

### 第八大类：时长建模优化（Watch Time Prediction）

> **核心问题**：短视频场景下如何准确预测用户观看时长，解决分布不平衡问题？

| # | 论文 | 机构 | 核心贡献 |
|---|------|------|----------|
| 1 | **CREAD: Classification-Restoration Framework with Error Adaptive Discretization for Watch Time Prediction** | Kuaishou, AAAI 2024 | 将观看时长预测转化为多分类问题。核心创新：Error-Adaptive Discretization（EAD）技术，理论分析离散化对学习误差和恢复误差的影响，实现两者最优平衡。快手 App 全量上线，观看时长提升 0.29%。 |
| 2 | **EGMN: Multi-Granularity Distribution Modeling for Video Watch Time Prediction via Exponential-Gaussian Mixture Network** | Xiaohongshu, RecSys 2025 | 从分布角度建模观看时长：发现粗粒度上的 skewness（快速跳过集中）和细粒度上的 diversity（多样交互模式）。提出 Exponential-Gaussian Mixture 分布假设，EGMN 网络参数化该分布。在小红书短视频场景验证优于 SOTA。已开源。 |

---

### 第九大类：兴趣建模（Interest Modeling）

| # | 论文 | 机构 | 核心贡献 |
|---|------|------|----------|
| 1 | **Trinity: Syncretizing Multi-/Long-tail/Long-term Interests All in One** | ByteDance, 2025 | 统一框架同时解决多兴趣/长尾兴趣/长期兴趣的"兴趣遗忘"问题。构建实时聚类系统将 item 投射到可枚举的 cluster，计算统计兴趣直方图；识别欠分发主题并在热点涌现时保持稳定。已部署于抖音召回阶段，显著提升用户体验和留存。 |

---

### 第十大类：Diffusion Modeling（扩散模型与生成式建模）

> **核心问题**：如何用 Diffusion Model / Flow Matching 等连续生成模型建模推荐中的分布表征、不确定性和偏好动态？

**本类共 3 篇（本文件夹收录）+ 10 篇推荐论文，覆盖基础方法、推荐应用和训练理论三个层面。**

#### 10.1 本文件夹收录论文

| # | 论文 | 机构 | 会议/年份 | 核心贡献 |
|---|------|------|-----------|----------|
| 1 | **DiffuRec: A Diffusion Model for Sequential Recommendation** | 武汉大学 / NTU | TOIS 2023 | **首次将 Diffusion Model 引入序列推荐。** 将 item 表征从固定向量升级为分布，在前向过程中将 target item embedding 加噪为高斯分布，利用 Transformer Approximator 重建 target item。训练使用 Cross-Entropy Loss（替代标准 MSE），推理时多步逆向去噪后通过 Rounding（全量内积）映射回离散 item。$\lambda_i \sim \mathcal{N}(\delta, \delta)$ 的随机缩放因子引入不确定性，对长尾 item 提升显著。四个数据集上大幅超越 SASRec/BERT4Rec。局限：多步推理延迟大，仅在学术数据集验证。 |
| 2 | **Flow Matching for Generative Modeling** | **Meta AI (FAIR)** / Weizmann Institute | ICLR 2023 | **生成式建模的新范式，统一并超越 Diffusion Model。** 提出 Conditional Flow Matching (CFM)：通过条件概率路径和条件向量场的分解，实现 CNF 的 simulation-free 训练，且与 FM 目标梯度等价（定理 2）。核心创新是 **Optimal Transport (OT) 路径**：线性均值+线性标准差产生直线轨迹，采样 NFE 降低 40%+，NLL/FID 在 ImageNet 上全面 SOTA。对 RecSys 启示：可替代 DiffuRec 中的 DDPM 大幅提升推理效率。 |
| 3 | **Learning Dynamics of LLM Finetuning** | UBC / Amii | **ICLR 2025** | 统一分析 SFT/DPO 的学习动力学：$\Delta \log \pi_t(x_o) = -\eta \cdot A_t \cdot K_t \cdot G_t$。最重要发现是 **"挤压效应"（Squeezing Effect）**：对 Softmax 施加负梯度（如 DPO 的 $y^-$）时，概率质量被"挤压"到 argmax token。越尖锐的分布挤压越严重，$y^-$ 越不可能挤压越严重。这解释了 off-policy DPO 训练过久导致所有输出概率下降、文本退化的现象。提出"extend"策略（SFT 阶段也训练 $y^-$）缓解挤压效应，win-rate 显著提升。**对 OneRec 系列中 DPO 偏好对齐的理解有直接参考价值。** |

#### 10.2 领域推荐论文（Diffusion in RecSys 调研）

> 以下 10 篇为 Diffusion Model 在推荐系统中的重要论文，按方向分类。优先工业界论文和顶会发表。

**A. 协同过滤方向**

| # | 论文 | 机构 | 会议/年份 | 核心贡献 | 推荐理由 |
|---|------|------|-----------|----------|----------|
| 4 | **DiffRec: Recommender Systems with Generalized Diffusion Models** | NUS | WSDM 2023 | **首个将 Diffusion 应用于协同过滤。** 将 user-item 交互向量作为输入，前向加噪+逆向去噪恢复被腐蚀的交互信号。提出 L-DiffRec（Latent Diffusion，在 VAE latent space 做扩散降维）和 T-DiffRec（Temporal Diffusion，处理时序信息）。 | 方向开创性工作，与 DiffuRec 的"生成 item embedding"思路互补。引用量高。 |

**B. 序列推荐方向**

| # | 论文 | 机构 | 会议/年份 | 核心贡献 | 推荐理由 |
|---|------|------|-----------|----------|----------|
| 5 | **DreamRec: Generate What You Prefer — Towards Controllable Recommendation via Diffusion Models** | 浙江大学 / Microsoft | SIGIR 2023 | 提出"生成式范式"取代"判别式范式"：不用对比学习区分正负样本，而是直接用 Diffusion 从历史序列**生成** target item 的 oracle embedding。无需负采样，首次在推荐中应用 **Classifier-Free Guidance (CFG)** 做可控推荐。 | 明确提出判别式 vs 生成式推荐的范式之争，CFG 在推荐中首次应用，概念影响力大。 |
| 6 | **CDDRec: Conditional Denoising Diffusion for Sequential Recommendation** | Microsoft Research | CIKM 2023 | 条件去噪扩散做序列推荐：将 user 历史序列编码为条件信号，在逆向过程中作为 condition 引导 item embedding 生成。引入交叉注意力机制融合条件和 diffusion 状态。 | 对 DiffuRec 的直接改进（显式条件生成替代隐式条件）。Microsoft Research 背景。 |

**C. 数据增强方向**

| # | 论文 | 机构 | 会议/年份 | 核心贡献 | 推荐理由 |
|---|------|------|-----------|----------|----------|
| 7 | **Diff4Rec: Diffusion Recommender Model** | 北航 / **阿里巴巴** | SIGIR 2023 | 在 user representation space 中通过前向-逆向扩散生成合成 user embedding 扩充训练数据。结合 curriculum learning（先低噪声合成数据，再逐步增大噪声）。 | **阿里巴巴工业背景**。"Diffusion 做数据增强"比直接做预测更务实，工业落地可能性更高。 |
| 8 | **DiffASR: Diffusion Augmentation for Sequential Recommendation** | Rutgers / **Amazon** | CIKM 2023 | 对 user 历史交互序列进行扩散-去噪，生成增强后的交互序列。**即插即用**：可无缝集成到任何序列推荐模型（SASRec、BERT4Rec 等）的训练管线中。 | **Amazon 工业背景**。不需改变下游模型架构，工业适配性好。 |

**D. 跨域推荐 / 知识增强方向**

| # | 论文 | 机构 | 会议/年份 | 核心贡献 | 推荐理由 |
|---|------|------|-----------|----------|----------|
| 9 | **DCDR: Diffusion Cross-domain Recommendation** | 人大 / **腾讯** | AAAI 2024 | 首个将 Diffusion 用于跨域推荐：通过 Diffusion 将源域 user embedding 转化为目标域 user embedding，避免直接域映射的信息损失。设计了基于时间戳的 Diffusion Guidance 机制。 | **腾讯工业背景**。跨域推荐是工业界刚需，Diffusion 的去噪特性天然适合域间转化。 |
| 10 | **DiffKG: Knowledge Graph Enhanced Diffusion for Recommendation** | USTC | AAAI 2024 | 将知识图谱信息注入 Diffusion 推荐框架：前向过程根据 KG 结构选择性加噪（保留 KG 邻居信息），逆向过程用 KG-aware attention 引导去噪。 | KG + Diffusion 交叉方向，对可解释性和冷启动有帮助。 |

**E. 偏好动力学建模**

| # | 论文 | 机构 | 会议/年份 | 核心贡献 | 推荐理由 |
|---|------|------|-----------|----------|----------|
| 11 | **PDRec: Preference Dynamics for Recommendation via Diffusion Models** | 多机构 | NeurIPS 2024 | 用 Score-based Diffusion（SDE 视角）建模用户偏好的**动态演化**：将 user preference 看作随时间变化的分布，建模其演化轨迹，支持在任意未来时间点采样 user preference。 | 从时间动力学角度理解 Diffusion 在推荐中的角色，理论性强，NeurIPS 顶会。 |

**F. 工业界 Flow Matching 实践**

| # | 论文 | 机构 | 会议/年份 | 核心贡献 | 推荐理由 |
|---|------|------|-----------|----------|----------|
| 12 | **RecFlow: An Industrial Full Flow Recommendation Dataset** | **快手** | 2024 | 发布快手全链路推荐数据集（召回→展示），在方法论上探索了 **Flow Matching 在推荐全链路中的应用**：将多阶段筛选建模为连续正规化流。 | **快手工业级实践**。Flow Matching（本文件夹收录）在推荐中的直接应用尝试。 |

**G. 综述**

| # | 论文 | 说明 |
|---|------|------|
| 13 | **A Survey on Diffusion Models for Recommender Systems** | arXiv 2024 综述。系统分类现有工作为：(1) 数据工程与增强；(2) 表征增强；(3) 直接推荐。总结开放问题：推理效率、离散空间适配、可控性、evaluation。**建立全局视野的最佳入口。** |

#### 10.3 建议阅读路径

```
1. Survey 综述 → 建立全局认知
2. DiffRec (WSDM'23) → 协同过滤方向开创工作
3. DiffuRec (TOIS'23) → 序列推荐方向开创工作（本文件夹）
4. DreamRec (SIGIR'23) → 理解"生成式 vs 判别式"范式之争
5. Flow Matching (ICLR'23) → Diffusion 的理论升级（本文件夹）
6. CDDRec / DiffASR → 条件生成 & 数据增强两条实用路线
7. Diff4Rec / DCDR → 工业界（阿里/腾讯）实践方向
8. Learning Dynamics (ICLR'25) → 理解 DPO/SFT 训练动力学（本文件夹）
```

---

## 三、跨类别技术关联图

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
│ Semantic ID + GR   │            │  双塔 增强            │   │  Ranking Scaling   │
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

## 四、关键发现与趋势总结

### 4.1 生成式推荐正在从实验走向大规模部署
- **OneRec 系列**（Kuaishou）和 **PLUM**（YouTube）标志着端到端生成式推荐已在亿级用户平台完成验证。
- OneRec-V2 的 Lazy Decoder-Only 架构和 8B 参数规模表明生成式推荐正在追赶 LLM 的 scaling 路线。

### 4.2 Semantic ID 是连接 LLM 与推荐系统的关键桥梁
- 从 TIGER（2023）到 PLUM/OneRec（2025），Semantic ID 从学术概念发展为工业标配。
- TermID 探索了回归自然语言 token 的可能性，与 AgenticTagger 的方向一致。

### 4.3 双塔架构仍有生命力，但需要系统性增强
- HIT/DAT/Tricolore 等工作表明双塔架构通过增强交互、多行为建模、对比学习仍可持续改进。
- MotiR 展示了 LLM 生成的语义特征如何与传统双塔融合，是"LLM 赋能传统架构"的优秀范例。

### 4.4 Scaling Law 在推荐领域开始显现
- Wukong（Meta）首次在推荐领域验证了 Scaling Law。
- OneRec、PLUM、LUM、RankMixer 进一步证实：无论是生成式还是传统排序模型，都可通过扩大参数规模持续提升。

### 4.5 多模态和创作者侧是新兴方向
- VLM2Vec 系列指向"用 VLM 做通用多模态 Embedding"的新范式。
- DualRec/Next-User Retrieval 开辟了从创作者视角优化推荐的新赛道。

### 4.6 Diffusion/Flow Matching 为推荐带来分布建模新范式
- DiffuRec 首次将 item 表征从"点估计"升级为"分布估计"，天然适配推荐中的不确定性和多兴趣建模。
- Flow Matching（Meta FAIR）的 OT 路径可将 Diffusion 推理效率提升 40%+，解决工业部署的核心瓶颈。
- "Diffusion 做数据增强"（Diff4Rec/DiffASR）是比直接做预测更务实的工业落地路线。
- 挤压效应（Learning Dynamics）对理解 OneRec/PLUM 等系统中 DPO 偏好对齐的行为有直接参考价值。

---

## 五、建议阅读顺序

**如果你是推荐系统研发工程师，建议按以下顺序阅读：**

1. **入门理解生成式推荐**: TIGER → OneRec (KDD paper) → OneRec Technical Report → OneRec-V2
2. **理解 Semantic ID 的工业落地**: PLUM → BETTER GENERALIZATION WITH SEMANTIC IDS → LMIndexer → TermID
3. **双塔冷启动方案（实际落地）**: 坚持双塔调研报告 → DAT → HIT → MotiR → Next-User Retrieval
4. **LLM + 推荐系统**: HLLM → LUM → NoteLLM → LLMTreeRec → AgenticTagger
5. **Scaling 与效率**: Wukong → RankMixer → CALM → MiniOneRec
6. **Embedding/多模态基础**: Gemini Embedding → Qwen3 Embedding → VLM2Vec → VLM2Vec-V2
7. **时长建模**: CREAD → EGMN
8. **兴趣建模**: Trinity
9. **Diffusion Modeling**: Survey 综述 → DiffRec → DiffuRec → DreamRec → Flow Matching → Diff4Rec/DiffASR → Learning Dynamics

---

*注：本报告基于各论文的摘要、引言及核心方法章节撰写。部分论文在多个目录中重复收录（如 TIGER 和 Next-User Retrieval），反映了跨类别的技术关联性。Diffusion Modeling 类的 10 篇推荐论文基于 2023-2025 年领域调研，优先选取工业背景（阿里/腾讯/Amazon/快手/Microsoft）和顶会发表的代表性工作。*
