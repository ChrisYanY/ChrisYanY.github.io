---
title: "Reduce the Decision: Where LLMs Belong in Recommender Systems"
date: 2026-10-16
summary: "LLMs adapt fast but compute slowly; classic models compute fast but adapt slowly. The way to make LLMs land in recommender systems is to reduce the dimensionality of the decisions they make."
label: "Thoughts"
tags: ["LLM", "Recommender Systems", "Thoughts"]
math: false
mermaid: false
translationKey: "decision-dimensionality"
ai_assisted: true
ai_note: "The views come from the author's own discussion with an AI; the write-up is AI-assisted."
---

In the previous two posts, I argued first that [LLMs replace the *person*, not the probability model](/posts/llm-takeover-recsys/), and then that if we let an LLM iterate on a recommender system by itself, [what it lacks isn't intelligence but runway](/posts/llm-runway/).

This post started from something I ran into recently. I've been trying out a kind of model built specifically for judgments, one that outputs calibrated probabilities directly,[^jev] and using it to label content: is this user-generated, is this AI-generated. It does remarkably well.

That reminded me of a technique used at the blending and re-ranking stage: adding contextual bandits that change the mix of candidates based on what the user is actually interested in. These methods have worked very well in the past. Meanwhile, classic recommender systems have never been great at adjusting to real-time interest; the adjustments tend to feel either forced or clumsy.

So if LLMs are this good at content understanding and labeling, could they label and adjust the mix of candidates according to real-time interest? Wouldn't that reduce the dimensionality of the decision and improve system metrics at the same time?

Answering that takes two steps. Everyone in the industry is talking about "LLM-native" recommendation. What actually counts as LLM-native? And in a feed, where can it really land?

## Looking like an LLM is not being LLM-native

Many generative recommenders today, such as Kuaishou's OneRec and the earlier TIGER, cut each item into a short sequence of discrete semantic IDs, generate the next item's IDs autoregressively with a Transformer, and add MoE layers and reinforcement-learning alignment on top.[^onerec] From architecture to training recipe, they look a lot like LLMs.

But their "vocabulary" is learned from scratch out of content and behavior embeddings. There is no language in it, and no world knowledge. They borrow the form of an LLM, not its knowledge. I'd rather call these models LLM-style.

To me, the essence of LLM-native is this: **the foundation is the semantic understanding and world knowledge that come from language pretraining, with behavioral data aligned into the same space.** The first supplies a prior, letting the system understand content and people without spending traffic. The second supplies calibration, filling in collaborative patterns that aren't in language at all, such as "people who like A also like B." Google's PLUM, which continues training a pretrained language model with semantic IDs, is heading in this direction.[^plum]

Whether the funnel still ends in a ranker is an implementation choice; it doesn't change whether the system is LLM-native. In fact, when today's generative models reach production, most of them are still just one retrieval source, with a ranker after them as usual.[^snap]

Four questions tell you whether a system is really LLM-native:

- If a product manager edits one sentence, does the system's behavior change?
- Can a brand-new item, with zero interactions, reach the right people?
- Can the system explain in one sentence why it recommended something?
- If a user says "show me less of this lately," does the system understand?

Today's cascades can do none of these. These four things are exactly the new value LLMs can bring to recommendation.

## Three bills

The moment you try to put LLM-native recommendation into a feed, three bills come due: latency, scale, and real-time intent.

**Latency can be worked around.** What really slows things down is an LLM generating word by word on the request's critical path. The workarounds all move it off that path: compute content understanding and user profiles asynchronously before the request arrives; for anything that must be online, have the LLM run a single forward pass and return a judgment instead of generating text; failing that, distill its semantic space into a small model that can run online.

**Scale depends on what you amortize the cost over.** A rough estimate using the public price of a model built specifically for judgments,[^jev] assuming one billion users:

| Where the cost lands | Assumption | Cost per day |
|---|---|---|
| Once per user per day | One 2,000-token profile per user | about $84 thousand |
| Every candidate in every request | 50 requests per user per day, 500 candidates each, 500 tokens per candidate | about $525 million |

That's a difference of more than six thousand times, and this is a judgment model that only charges for input; with an LLM that generates text, the second row would cost far more. Amortized over users and items, the numbers work. Amortized over every candidate, they never will.

**Real-time intent is the real problem.** Within a single session of scrolling, a user's intent changes every few seconds: swipe past three videos, then watch one all the way through. A profile computed in advance is stale by definition, and calling an LLM on every swipe puts you back on the second row of that table.

## Two kinds of "fast"

Thinking this through gave me a clearer sense of the difference between LLMs and classic models: **LLMs are more flexible and more real-time, but imprecise. Classic models are more dogmatic, more scalable and more precise, but slow to react.**

"Real-time" and "slow to react" here are really two different kinds of speed.

| | LLM | Classic model |
|---|---|---|
| Compute speed: how long one judgment takes | Slow, hundreds of milliseconds to seconds | Fast, milliseconds |
| Adaptation speed: how quickly it adjusts to something new | Fast; one sentence or one new signal can change its judgment | Slow; it needs data to accumulate and a retrain |

**LLMs adapt fast but compute slowly. Classic models compute fast but adapt slowly.**

A user just searched for "camping gear," or just watched a breaking-news clip, and a new interest appears. A classic model has to wait for data to accumulate; an LLM gets it at a glance. But ask it to give hundreds of candidates a precise score between every two swipes, and it can't keep up.

There's an irony here. That model built for judgments named itself a "System One" model, after Kahneman's fast thinking.[^kahneman] But in a recommender system, the real System 1 is the classic ranker: fast, statistical, running on memory. The LLM is more like System 2: slow, able to reason, and knowledgeable about the world.

## Reduce the decision

So where can an LLM actually land in a feed? After a lot of thought, I found only one place where the numbers work.

The classic system ranks everything first and splits the results into three or four semantic groups of candidates, each already fully ranked. When the user shows a new interest, the LLM uses that real-time intent to choose among and adjust these groups, much like a value model or a bandit fine-tuning the blend.

Why do the numbers work this way? Because the decision the LLM has to make has **lower dimensionality**:

- Instead of scoring hundreds of candidates, it picks one of three or four groups, or assigns them weights.
- Instead of one call per candidate, it's one call per screen refresh, or only when interest shifts.
- Its input is just a summary of the last few actions plus a semantic description of each group.
- It doesn't need to know whether you like something 75% or 83%, only which group you'd rather see right now.
- The latency can be hidden: while the user watches the current video for ten-odd seconds, compute the next screen in advance.

At the same price, one billion users each making 20 such decisions a day comes to about $840 thousand a day. Not cheap, but entirely affordable, and triggering only on interest shifts, or switching to a small in-house model, would cut it by another order of magnitude.

An analogy: **the classic model cooks, the LLM orders.** How good each dish is has to be calculated precisely; which dishes come first tonight depends on your mood right now. That used to be the job of human operators. Now the LLM does it in real time, in every session. It's the real-time version of "LLMs replace the person."

It also pairs naturally with bandits: the LLM supplies a prior for each group, and the bandit corrects the posterior quickly from real-time feedback.[^bandit] The LLM provides understanding; the bandit provides speed.

This is also why I think it's more promising than what came before. The bottleneck of contextual bandits has always been how the context is represented. Context features used to be mostly hand-designed, which is exactly why adjusting to real-time interest so often felt forced or clumsy. LLM labeling fills that gap, and the work can be split: content labels are computed once per item; the user's current intent is summarized only when their interest shifts; and how the two match is left to the bandit to learn from real-time feedback. What the LLM produces is the bandit's context, not a real-time score for every candidate.

Of course, this is still just an idea, and a few questions have to be answered.

**Where exactly does the LLM beat a bandit?** Classic sequence models already adjust within a session. The LLM's edge will only show up in semantic jumps, in new interests that never appeared in the history, and in feedback users give in language. How much traffic falls into these cases decides whether this layer is worth building.

**The groups have to be meaningful.** Each group needs a semantic label for the LLM to reason about; the groups need to be genuinely different for there to be a real choice; and the LLM needs a "go fetch a new group" action, so that when a new interest isn't in any group, it can trigger a fresh retrieval.

**Don't chase every passing interest.** Pushing a whole category hard after one video is an easy way to fall back into a low-quality local optimum. A long-term profile should serve as the prior and limit how far each adjustment can go.

## Layer by cost

Generalize this idea, and the ideal shape of LLM-native recommendation is layered by how often each part is computed:

- **System layer, weekly or quarterly:** the LLM works like an engineer and operator, reading experiments, proposing changes, assembling modules, and translating policies written in natural language into rewards. Humans set the values and the runway.
- **Content layer, once per item:** the LLM understands each item and produces semantic labels and quality judgments. Computed once, reused by every later impression of that item.
- **User layer, per user every hour or day, asynchronously:** the LLM understands each person and writes a "user memo": stable interests, emerging interests, what to explore, what to avoid. Computed once, reused by every later request from that user.
- **Request layer, every request, in milliseconds:** classic models handle retrieval and precise scoring; the LLM steps in only at the few decision points that have been reduced in dimension.

In one line: **the LLM supplies the prior; the classic models supply the posterior.** The LLM's hypotheses become exploration traffic, and what the classic models measure flows back to correct the LLM.

## The boundary will move

The boundaries between these layers are, at bottom, a cost curve.

Every order of magnitude that inference gets cheaper, the boundary moves down a level: the user layer goes from daily refreshes to per-session, then per-request; the part of the request layer owned by classic models keeps narrowing. Single-pass judgment models maturing, and small models that run on phones getting stronger, push the line down too.

If one day the LLM cost of a request falls below the value that request brings, and precision and calibration are solved, "full replacement" may simply happen. That's why I've said I stay open to full replacement. The ideal shape isn't a fixed architecture diagram; it's the output of a cost function.

Today, though, the answer is clear:

> Classic models are good at getting a calculation right. LLMs are good at deciding which calculation to do right now.

The first post said LLMs replace the person; the second said what they lack is runway. This one says: to make them truly land in recommender systems, reduce the dimensionality of the decisions they make.

---

[^onerec]: Jiaxin Deng et al. *OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment.* arXiv:2502.18965, 2025; Shashank Rajput et al. *Recommender Systems with Generative Retrieval.* NeurIPS 2023.
[^plum]: Google. *PLUM: Adapting Pre-trained Language Models for Industrial-scale Generative Recommendations.* 2025.
[^snap]: GRP Team, Snap Inc. *GRP v0.1 Technical Report.* arXiv:2609.36688, 2026.
[^jev]: Estimated at TypeSafe Jev's public pricing of $0.042 per million input tokens, with output free. Diogo Almeida. *Introducing System One Models & Jev.* TypeSafe AI Blog, 2026-09-15.
[^kahneman]: Daniel Kahneman. *Thinking, Fast and Slow.* 2011.
[^bandit]: Lihong Li, Wei Chu, John Langford, Robert E. Schapire. *A Contextual-Bandit Approach to Personalized News Article Recommendation.* WWW 2010.
