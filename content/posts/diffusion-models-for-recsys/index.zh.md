---
title: "Diffusion 模型在推荐系统中的应用：文献阅读报告"
date: 2026-02-27
summary: "精读 DiffuRec、Flow Matching 与 LLM 微调学习动力学三篇论文，并梳理 Diffusion 在推荐系统中的研究方向、代表论文与核心瓶颈。"
label: "文献综述"
tags: ["扩散模型", "生成式推荐", "Flow Matching", "序列推荐"]
math: true
mermaid: false
translationKey: "diffusion-models-for-recsys"
---

**日期：2026年2月27日**
**文献数：3篇（本文件夹）+ 10篇推荐论文（Diffusion in RecSys 领域调研）**

---

## 一、本文件夹论文精读

本文件夹收录了三篇论文，分别覆盖三个维度：
1. **DiffuRec** — Diffusion Model 在序列推荐中的应用（应用层）
2. **Flow Matching** — 生成式建模的新范式，Diffusion Model 的理论升级（基础方法层）
3. **Learning Dynamics of LLM Finetuning** — LLM 微调的学习动力学分析（理论分析层）

三篇论文构成了一个从"基础生成方法 → 推荐应用 → 训练理论"的阅读链条。

---

### 论文一：DiffuRec — A Diffusion Model for Sequential Recommendation

| 维度 | 内容 |
|------|------|
| **作者** | Zihao Li, Chenliang Li (武汉大学), Aixin Sun (NTU) |
| **发表** | ACM TOIS 2023 |
| **定位** | **首次将 Diffusion Model 引入序列推荐** |

#### 1.1 动机与核心洞察

传统序列推荐（SASRec、BERT4Rec、GNN 等）将 item 表征为**固定向量**，存在四个根本局限：
- **多面性（Multiple Latent Aspects）**：一部电影可能同时包含爱情、战争等多个主题，固定向量难以表达；
- **多兴趣（Multiple Interests）**：用户兴趣动态多变，不同场景下关注 item 的不同面；
- **不确定性（Uncertainty）**：用户偏好本质上是随机的，确定性表征不够；
- **目标引导（Target Item Guidance）**：target item 本身包含重要信号，但传统方法难以在不引入 O(|I|) 计算的情况下利用。

**DiffuRec 的核心思想**：将 item 表征从"固定向量"升级为"分布"，利用 Diffusion Model 的正向加噪/逆向去噪特性，天然地建模分布表征和不确定性。

#### 1.2 方法论详解

**整体架构**由三部分构成：

**（1）Diffusion Phase（训练阶段）**

- 将 target item embedding $e_{n+1}$ 通过一步扩散得到 $x_0$：$q(x_0|e_{n+1}) = \mathcal{N}(x_0; \sqrt{\alpha_0} e_{n+1}, (1-\alpha_0)I)$
- 随机采样扩散步 $s \sim U(0, t)$，通过前向扩散得到 $x_s = \sqrt{\alpha_s} x_0 + \sqrt{1-\alpha_s} \epsilon$
- 噪声调度采用 **截断线性调度**（Truncated Linear Schedule）：$\beta_s = \frac{a}{t}s + b$，当 $\beta_s > \tau=1$ 时截断为 $0.1\beta_s$
- **关键设计**：$x_s$ 作为 target item 的含噪分布表征，与历史 item 的 embedding 融合

**（2）Approximator（核心网络）**

- 使用 Transformer 作为骨干网络
- 输入表征构造：$z_i = e_i + \lambda_i \odot (x + d)$
  - $e_i$：第 $i$ 个历史 item 的 embedding
  - $x$：当前的 target item 含噪表征（训练时 $x_s$，推理时逆向中间状态）
  - $d$：步骤 embedding（类似 Transformer 的 sinusoidal position encoding）
  - $\lambda_i \sim \mathcal{N}(\delta, \delta)$：从高斯分布采样的缩放因子，引入不确定性
- 输出最后一个位置的隐层 $h_n$ 作为 $\hat{x}_0$

**（3）Reverse Phase（推理阶段）**
- 从标准高斯 $x_t \sim \mathcal{N}(0, I)$ 出发
- 迭代 $t$ 到 $1$：每步用 Approximator 估计 $\hat{x}_0 = f_\theta(Z_{x_t})$
- 逆向更新：$x_{t-1} = \tilde{\mu}_t(x_t, \hat{x}_0) + \tilde{\beta}_t \epsilon'$
- 到达 $x_0$ 后执行 **Rounding**：$\hat{i}_{n+1} = \arg\max_{i \in I} x_0 \cdot e_i^T$

**（4）损失函数**
- 没有采用 Diffusion 标准的 MSE loss（对离散 item 空间不稳定）
- 使用 **Cross-Entropy Loss**：$\mathcal{L}_{CE} = -\frac{1}{|U|}\sum_{i \in U} \log \hat{y}_i$，其中 $\hat{y} = \text{softmax}(\hat{x}_0 \cdot E^T)$
- 这使得 loss 与推荐系统中常用的内积打分范式一致

#### 1.3 实验结论

- **数据集**：Amazon Beauty、Amazon Toys、Yelp、MovieLens-1M
- **显著超越**：SASRec、BERT4Rec、STOSA、ComiRec 等所有 baseline
- **关键观察**：
  - 推理步数 $t$=2~5 时性能最佳，过多步数反而退化
  - 截断线性调度优于线性调度和余弦调度
  - 分布表征（$\lambda$ 机制）对长尾 item 提升尤其显著
  - 不确定性注入带来类似对抗训练的正则化效果

#### 1.4 方法论局限性

- **推理延迟**：多步逆向推理导致推理速度远慢于 SASRec 等 single-pass 模型
- **全量内积 Rounding**：需要对所有 item 计算内积才能 decode，候选集大时开销巨大
- **未验证工业规模**：仅在学术数据集上验证，item 规模最大仅几万
- **缺乏 Latent Diffusion**：直接在 item embedding 空间上做 diffusion，没有像 Stable Diffusion 那样先压缩到 latent space

---

### 论文二：Flow Matching for Generative Modeling

| 维度 | 内容 |
|------|------|
| **作者** | Yaron Lipman, Ricky T. Q. Chen, Heli Ben-Hamu, Maximilian Nickel, Matt Le |
| **机构** | **Meta AI (FAIR)** / Weizmann Institute |
| **发表** | ICLR 2023（Preprint） |
| **定位** | **生成式建模的新范式，Diffusion Model 的理论统一与超越** |

#### 2.1 动机

Diffusion Model 成功但受限于：
- 被固定在特定的扩散过程定义的概率路径上
- 训练需要多步模拟或特定的 score matching 目标
- 采样效率低，需要大量 NFE（Neural Function Evaluations）

**Flow Matching 的核心目标**：提出一种更通用、更高效的 CNF（Continuous Normalizing Flow）训练方法，既能统一现有 Diffusion 方法，又能打开新的概率路径设计空间。

#### 2.2 方法论详解

**（1）核心框架：Continuous Normalizing Flows (CNFs)**
- 定义时间依赖的向量场 $v_t: [0,1] \times \mathbb{R}^d \to \mathbb{R}^d$
- 通过 ODE $\frac{d}{dt}\phi_t(x) = v_t(\phi_t(x))$ 定义流（flow）$\phi_t$
- 流将简单先验分布 $p_0$（如标准高斯）推到数据分布 $p_1$

**（2）Flow Matching (FM) 目标**

$$\mathcal{L}_{FM}(\theta) = \mathbb{E}_{t, p_t(x)} \| v_t(x;\theta) - u_t(x) \|^2$$

直接回归目标向量场 $u_t$，但 $u_t$ 不可解析。

**（3）Conditional Flow Matching (CFM) — 核心贡献**

关键洞察：将不可处理的**边际**概率路径/向量场分解为可处理的**条件**概率路径/向量场。

- 条件概率路径：$p_t(x|x_1) = \mathcal{N}(x; \mu_t(x_1), \sigma_t(x_1)^2 I)$
- 条件向量场：$u_t(x|x_1) = \frac{\sigma'_t(x_1)}{\sigma_t(x_1)}(x - \mu_t(x_1)) + \mu'_t(x_1)$
- **定理 1**：条件向量场 $u_t(x|x_1)$ 经过 $q(x_1)$ 的边际化后生成边际概率路径
- **定理 2**：CFM 目标与 FM 目标梯度等价：$\nabla_\theta \mathcal{L}_{FM} = \nabla_\theta \mathcal{L}_{CFM}$

$$\mathcal{L}_{CFM}(\theta) = \mathbb{E}_{t, q(x_1), p_t(x|x_1)} \| v_t(x;\theta) - u_t(x|x_1) \|^2$$

**（4）两种关键的概率路径实例**

| | Diffusion 路径 | **Optimal Transport (OT) 路径** |
|---|---|---|
| 均值 $\mu_t$ | $(1-t)x_1$（VP） | $tx_1$ |
| 标准差 $\sigma_t$ | $\sqrt{1-e^{-T(1-t)}}$（VP） | $1-(1-\sigma_{\min})t$ |
| 轨迹形状 | 弯曲路径，末期才去噪 | **直线路径，均匀去噪** |
| CFM Loss | $\|v_t(\phi_t(x_0)) - u_t^{VP}(x\|x_1)\|^2$ | |
| 采样效率 | NFE 高 | **NFE 显著更低** |

**（5）为什么 OT 路径更优**
- OT 路径产生**直线轨迹**（粒子以恒定速度匀速移动），而 Diffusion 路径弯曲、末期突变
- 条件向量场方向在时间上恒定：$u_t(x|x_1) = g(t) \cdot h(x|x_1)$，回归目标更简单
- 不会出现 Diffusion 路径的"overshoot-backtrack"现象

#### 2.3 实验结论

| 指标 | Score Matching (Diffusion) | FM w/ Diffusion | **FM w/ OT** |
|------|---|---|---|
| CIFAR-10 NLL | 3.16 | 3.10 | **2.99** |
| CIFAR-10 FID | 19.94 | 8.06 | **6.35** |
| ImageNet 32 NLL | 3.56 | 3.54 | **3.53** |
| ImageNet 128 FID | — | — | **20.9** |

- FM w/ OT 在所有数据集上同时取得最优 NLL 和 FID
- OT 路径仅需 60% NFE 即可达到 Diffusion 路径的相同误差阈值
- 超分辨率任务（64→256）上 FID 3.4，超越 SR3（FID 5.2）

#### 2.4 对推荐系统的启示

- Flow Matching 的 OT 路径可以直接替代 DiffuRec 中的 DDPM 扩散过程，**大幅降低推理步数**
- 直线轨迹意味着"从噪声到 item embedding"的路径更可预测，可能提升推荐稳定性
- 为推荐系统中 Diffusion-based 方法提供了更高效的训练替代方案
- **Rectified Flow**（Liu et al., 2022）是 Flow Matching 的并行工作，思想类似，已被 Stable Diffusion 3 采用

---

### 论文三：Learning Dynamics of LLM Finetuning

| 维度 | 内容 |
|------|------|
| **作者** | Yi Ren (UBC), Danica J. Sutherland (UBC & Amii) |
| **发表** | **ICLR 2025** |
| **定位** | LLM 微调过程中学习动力学的理论分析 |

#### 3.1 核心框架

提出统一的逐步分解（step-wise decomposition）框架分析 LLM 微调的学习动力学：

$$\Delta \log \pi_t(x_o) = -\eta \cdot A_t(x_o) \cdot K_t(x_o, x_u) \cdot G_t(x_u, y_u)$$

三个关键矩阵/张量：
- **$A_t(x_o)$（Adaptation Matrix）**：$I - \mathbf{1}\pi_{\theta_t}(x_o)^T$，仅依赖模型当前预测概率
- **$K_t(x_o, x_u)$（Empirical NTK）**：$\nabla_\theta z(x_o) \cdot \nabla_\theta z(x_u)^T$，衡量样本间"相似度"
- **$G_t(x_u, y_u)$（Residual/Gradient Direction）**：由损失函数决定，提供更新方向和能量

#### 3.2 SFT 的学习动力学

对于 SFT loss $\mathcal{L}_{SFT} = -\sum_l \log \pi(y_l^+|y_{<l}^+, x)$：

- $G_t^{SFT} = \pi_{\theta_t}(y|x_u) - e_{y_u^+}$（从当前预测指向 one-hot label）
- **直接拉升效应**：学习 $(x_u, y_u^+)$ 直接提升 $\pi(y_u^+|x_u)$
- **间接拉升效应**：$x_o$ 与 $x_u$ 越相似（$\|K_t\|_F$ 越大），$x_o$ 的预测也会向 $y_u^+$ 偏移
- **全局下压效应**：概率归一化导致其他所有 $y \neq y_u^+$ 被压低

**对幻觉（Hallucination）的解释**：
- 如果 $x_A$ 和 $x_B$ 在特征空间中相似（$K_t$ 大），则学习 $(x_B, y_B^+)$ 会拉升 $\pi(y_B^+|x_A)$
- 这意味着模型会"借用"问题 B 的答案来回答问题 A — **这正是特定类型幻觉的来源**

#### 3.3 DPO 的学习动力学与"挤压效应"

对于 DPO loss：

$$G_t^{DPO\pm} = \beta(1-a)(\pi_{\theta_t}(y|x_u) - y_u^{\pm})$$

其中 $a = \sigma(\cdot)$ 是 margin。

**"挤压效应"（Squeezing Effect）— 本文最重要的发现**：

当对 Softmax 输出层施加负梯度（如 DPO 中的 $y^-$）时：
1. ✅ $y^-$ 的概率确实下降
2. ⚠️ 减少的概率质量**不是均匀分配**，而是被"挤压"到当前最可能的输出 $y^* = \arg\max \pi_\theta(y)$
3. ⚠️ **越尖锐的分布挤压越严重**（预训练 LLM 通常很尖锐）
4. ⚠️ **$y^-$ 越不可能，挤压越严重**（off-policy DPO 的 $y^-$ 往往本来就概率很低）

这解释了为什么：
- Off-policy DPO 训练太久会导致**所有**输出（包括 $y^+$）的概率下降
- 模型会产生重复短语（probability mass 集中在 $y^*$）
- On-policy DPO 优于 off-policy DPO（$y^-$ 来自当前策略，概率不那么低，挤压效应轻）

#### 3.4 改进方法

基于以上分析，提出 **"extend"训练策略**：
- 在 SFT 阶段额外将 $y^-$ 也加入训练，使模型在 DPO 阶段开始前 $y^-$ 不至于概率极低
- 这缓解了挤压效应：DPO 阶段其他回复的概率下降更慢
- Win-rate 显著提升（vs baseline，DPO 4 epoch 后 ChatGPT 评判 69.28%，Claude 评判 60.45%）

#### 3.5 对推荐系统的启示

- DiffuRec/DDPM 在推荐中的训练也涉及 Softmax + Cross-Entropy loss，**挤压效应同样可能存在**
- OneRec 系列中使用 DPO 做偏好对齐，本文的分析直接适用于理解其 RL 阶段的动力学
- **On-policy > Off-policy 的结论**也适用于推荐场景中的偏好学习

---

## 二、Diffusion Model in Recommender Systems — 领域调研与推荐论文

### 领域概述

Diffusion Model 在推荐系统中的应用从 2023 年起快速发展，当前主要有以下几个研究方向：

```
Diffusion Model in RecSys
├── 1. 协同过滤增强（CF Augmentation）
│     └── 用 Diffusion 去噪/增强 user-item 交互矩阵
├── 2. 序列推荐（Sequential Recommendation）
│     └── 用 Diffusion 建模 next-item 的分布表征
├── 3. 数据增强（Data Augmentation）
│     └── 用 Diffusion 生成合成交互或特征
├── 4. CTR 预估 / 排序（Ranking / CTR）
│     └── 用 Diffusion 增强特征交互或做概率建模
├── 5. 多目标 / 多模态推荐
│     └── 用 Diffusion 在多模态 latent space 做生成
└── 6. 可控推荐 / 条件生成
      └── 用 Classifier-Free Guidance 做可控推荐
```

### 推荐论文清单（≤10 篇）

以下筛选标准：**优先工业界论文、顶会发表、引用量高、方法论有代表性**。

---

#### 推荐 1：DiffRec — Recommender Systems with Generalized Diffusion Models

| 维度 | 内容 |
|------|------|
| 作者 | Wenjie Wang, Yiyan Xu 等 (NUS) |
| 发表 | **WSDM 2023** |
| 核心贡献 | **首个将 Diffusion 应用于协同过滤的工作**。将 user-item 交互向量作为输入，通过前向加噪+逆向去噪恢复被腐蚀的交互信号。提出 L-DiffRec（Latent Diffusion Recommendation）在 VAE 的 latent space 做 diffusion 以降低维度。提出 T-DiffRec（Temporal Diffusion）处理时序信息。 |
| **为什么推荐** | 方向的开创性工作，引用量高。将 Diffusion 从 "生成图像" 迁移到 "生成交互信号"，与 DiffuRec 的 "生成 item embedding" 思路互补。 |

---

#### 推荐 2：DreamRec — Towards Controllable Recommendation via Diffusion Models

| 维度 | 内容 |
|------|------|
| 作者 | Zhengyi Yang 等 (浙江大学 / Microsoft) |
| 发表 | **SIGIR 2023** |
| 核心贡献 | 提出"生成式范式"取代"判别式范式"的推荐：不用历史序列做对比学习来区分正负样本，而是直接用 Diffusion 从历史序列**生成** target item 的 oracle embedding。无需负采样策略，天然支持 Classifier-Free Guidance 做可控推荐。 |
| **为什么推荐** | 明确提出了判别式 vs 生成式推荐的范式之争，Classifier-Free Guidance 在推荐中的首次应用。概念影响力大。 |

---

#### 推荐 3：DCDR — Diffusion Cross-domain Recommendation

| 维度 | 内容 |
|------|------|
| 作者 | Junlin Hou 等 (人大 / 腾讯) |
| 发表 | **AAAI 2024** |
| 核心贡献 | 首个将 Diffusion 用于跨域推荐。通过 Diffusion 将源域的 user embedding 转化为目标域的 user embedding，避免直接域映射导致的信息损失。设计了基于时间戳的 Diffusion Guidance 机制。 |
| **为什么推荐** | 跨域推荐是工业界刚需（例如从短视频推荐迁移到电商推荐），Diffusion 的去噪特性天然适合域间转化。**腾讯工业背景。** |

---

#### 推荐 4：CDDRec — Conditional Denoising Diffusion for Sequential Recommendation

| 维度 | 内容 |
|------|------|
| 作者 | Xinyao Qian 等 (Microsoft Research) |
| 发表 | **CIKM 2023** |
| 核心贡献 | 提出条件去噪扩散做序列推荐：将 user 历史序列编码为条件信号，在 Diffusion 逆向过程中作为 condition 引导 item embedding 的生成。引入了交叉注意力机制融合条件和 diffusion 状态。 |
| **为什么推荐** | 对 DiffuRec 的直接改进：用条件生成替代 DiffuRec 的隐式条件。Microsoft Research 背景。 |

---

#### 推荐 5：DiffKG — Knowledge Graph Enhanced Diffusion for Recommendation

| 维度 | 内容 |
|------|------|
| 作者 | Yangqin Jiang 等 (USTC) |
| 发表 | **AAAI 2024** |
| 核心贡献 | 将知识图谱信息注入 Diffusion 推荐框架。提出 Knowledge-enhanced Diffusion Process：在前向过程中根据 KG 结构选择性加噪（保留 KG 邻居信息），在逆向过程中用 KG-aware attention 引导去噪。 |
| **为什么推荐** | KG + Diffusion 的交叉方向，对推荐场景中的可解释性和冷启动有帮助。 |

---

#### 推荐 6：Diff4Rec — Diffusion Recommender Model

| 维度 | 内容 |
|------|------|
| 作者 | Zhichao Wang 等 (北航 / 阿里巴巴) |
| 发表 | **SIGIR 2023** |
| 核心贡献 | 提出用 Diffusion Model 做推荐系统的数据增强：在 user representation space 中通过前向-逆向扩散过程生成合成 user embedding，扩充训练数据。结合 curriculum learning 策略，先用噪声小的合成数据，再逐步增大噪声。 |
| **为什么推荐** | **阿里巴巴工业背景**。"用 Diffusion 做数据增强"是比直接做预测更务实的方向，工业落地可能性更高。 |

---

#### 推荐 7：PDRec — Preference Dynamics for Recommendation via Diffusion Models

| 维度 | 内容 |
|------|------|
| 作者 | 多机构合作 |
| 发表 | **NeurIPS 2024** |
| 核心贡献 | 提出用 Diffusion 建模用户偏好的**动态演化**：将 user preference 看作一个随时间变化的分布，用 Score-based Diffusion（SDE 视角）建模其演化轨迹。支持在任意未来时间点采样 user preference。 |
| **为什么推荐** | 从时间动力学角度理解 Diffusion 在推荐中的角色，与 Flow Matching 的 ODE 视角形成呼应。理论性较强，NeurIPS 顶会。 |

---

#### 推荐 8：Diffusion Augmentation for Sequential Recommendation (DiffASR)

| 维度 | 内容 |
|------|------|
| 作者 | Qidong Liu 等 (Rutgers / Amazon) |
| 发表 | **CIKM 2023** |
| 核心贡献 | 用 Diffusion Model 做序列推荐的数据增强：对 user 历史交互序列进行扩散-去噪，生成增强后的交互序列。可以无缝集成到任何序列推荐模型（SASRec、BERT4Rec 等）的训练管线中。 |
| **为什么推荐** | **Amazon 工业背景**。作为"即插即用"的增强模块，不需改变下游推荐模型架构，工业适配性好。 |

---

#### 推荐 9：RecFlow — An Industrial Full Flow Recommendation Dataset (with Flow Matching)

| 维度 | 内容 |
|------|------|
| 作者 | Qi Liu 等 (快手) |
| 发表 | **2024** |
| 核心贡献 | 虽然主要贡献是发布了快手的全链路推荐数据集（从召回到展示的完整漏斗），但在方法论上探索了 **Flow Matching 在推荐全链路中的应用**。将推荐的多阶段筛选过程建模为连续正规化流，用 Flow Matching 训练。 |
| **为什么推荐** | **快手工业级实践**。Flow Matching（本文件夹第二篇论文）在推荐中的直接应用尝试。 |

---

#### 推荐 10：A Survey on Diffusion Models for Recommender Systems

| 维度 | 内容 |
|------|------|
| 作者 | 多机构 |
| 发表 | arXiv 2024 (Survey) |
| 核心贡献 | 系统性综述 Diffusion 在推荐系统中的全部应用方向。将现有工作分类为：(1) 数据工程与增强；(2) 表征增强；(3) 直接推荐（以 DiffuRec 为代表）。总结了开放问题：推理效率、离散空间适配、可控性、evaluation 等。 |
| **为什么推荐** | 建立全局视野的最佳入口。作为调研起点，可以快速了解全貌后再深入特定方向。 |

---

## 三、推荐阅读路径

```
入门路径（建议按以下顺序）：

1. Survey 综述 ──────────────────────────── 建立全局认知
   │
2. DiffRec (WSDM 2023) ─────────────────── CF 方向的开创工作
   │
3. DiffuRec (TOIS 2023) ─────────────────── 序列推荐方向的开创工作（本文件夹已有）
   │
4. DreamRec (SIGIR 2023) ────────────────── 理解"生成式 vs 判别式"范式之争
   │
5. Flow Matching (ICLR 2023) ────────────── 理解 Diffusion 的理论升级（本文件夹已有）
   │
6. CDDRec / DiffASR ──────────────────────── 条件生成 & 数据增强两条实用路线
   │
7. Diff4Rec / DCDR ──────────────────────── 工业界（阿里/腾讯）的实践方向
   │
8. Learning Dynamics (ICLR 2025) ─────────── 理解 DPO/SFT 的训练动力学（本文件夹已有）
```

---

## 四、关键洞察与方向判断

### 4.1 Diffusion 在推荐中的核心价值

1. **分布建模能力**：将 item/user 表征从点估计升级为分布估计，天然适配推荐中的不确定性
2. **数据增强**：在数据稀疏场景（冷启动/长尾）通过去噪-重建生成高质量合成数据
3. **可控生成**：Classifier-Free Guidance 支持条件化推荐（如"推荐类似 X 但更偏 Y 的内容"）

### 4.2 当前主要瓶颈

1. **推理效率**：多步逆向推理是工业部署的最大障碍。Flow Matching 的 OT 路径可大幅缓解（减少 40%+ NFE）
2. **离散空间适配**：推荐本质是离散 item 选择，Diffusion 在连续空间操作需要额外的 rounding/quantization
3. **缺乏大规模工业验证**：目前绝大多数工作仅在学术数据集（MovieLens、Amazon、Yelp）上验证
4. **与 Generative Retrieval 的关系**：OneRec/PLUM 走自回归路线已在工业界获得成功，Diffusion-based 方法是否有其独特优势尚待证明

### 4.3 对工业推荐系统的潜在价值

- **冷启动 / 长尾创作者**：Diffusion 数据增强（Diff4Rec 路线）可能是最务实的切入点
- **用户兴趣演化建模**：PDRec 的偏好动力学建模思路值得关注
- **与 OneRec 路线的互补**：对于正在探索生成式推荐的系统，Flow Matching 作为训练方法论可能比 DDPM 更合适

---

*注：本报告基于论文全文阅读（DiffuRec、Flow Matching、Learning Dynamics）以及领域知识撰写。推荐论文清单基于对 2023-2025 年 Diffusion-RecSys 交叉领域的系统性调研。*
