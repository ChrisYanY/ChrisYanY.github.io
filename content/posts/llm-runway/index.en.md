---
title: "What LLMs Lack Isn't Intelligence. It's Runway."
date: 2026-10-13
summary: "Letting an LLM iterate on a recommender system by itself is not limited by how smart it is, but by whether it gets a non-greedy reward and a runway that tolerates negative results."
label: "Thoughts"
tags: ["LLM", "Recommender Systems", "Thoughts"]
math: false
mermaid: false
series: "llm-recsys"
part: 2
translationKey: "llm-runway"
ai_assisted: true
ai_note: "The views come from the author's own discussion with an AI; the write-up is AI-assisted."
---

At the end of the [previous post](/posts/llm-takeover-recsys/), I argued that LLMs replace the *person*, not the probability model, and that in the recommender system I have in mind, an LLM would autonomously organize the classic model modules.

Following that idea leads to a few natural questions. If we really let an LLM decide when to call a ranking model and how to assemble the pieces of a model architecture, does this path have a higher ceiling? If we give it enough experiment traffic and let it ship one change a week, can it make the system better on its own?

This post is where I ended up after chasing those questions. By the end, the answer had little to do with whether the LLM is smart enough.

## A higher ceiling, but the bottleneck isn't the model

Start with the ceiling. A system that can freely choose and combine modules searches a space that is a superset of any fixed architecture. In principle, its ceiling is no lower than any single fixed design.

But a high ceiling doesn't mean you can reach it.

If the LLM orchestrates models in real time on every request, we're back to the cost problem from the previous post: the numbers don't add up. The realistic form is offline, with the LLM playing the role of the engineer and researcher. It proposes a change, runs an experiment, reads the result, and decides what to do next.

Then the bottleneck is no longer the LLM's ability to come up with proposals. It's evaluation. Whether a change is good can only be answered by experiments.

## What happens with one change a week

Suppose we give an LLM some experiment traffic and let it ship one change a week and read the results. It sounds great, but it runs into a few very practical problems.

**A week only shows you the short term.** A one-week A/B test mostly shows short-term metrics. Long-term retention, which is what a recommender system really cares about, often takes months to show up, and users slowly adapt to changes, so a short-term win can shrink or even reverse. Google studied exactly this and found that decisions based only on short-term metrics systematically drift away from what is better for both users and the business.[^longterm]

**False positives accumulate.** One change a week is fifty-some tests a year. If you judge only by statistical significance, a few of them will be noise that happened to look significant. If the system automatically ships these "winners," over time it fills up with changes that do nothing, or quietly hurt.[^kohavi]

**Traffic costs something, and experiments interfere with each other.** Experiment traffic is itself a cost. Experiments running at the same time also share the same content pool and creator supply, and they contaminate each other.

So the hardest part isn't getting the LLM to propose good ideas. It's **building an experimentation framework that needs no human in the loop and can still be trusted**.

Look one level deeper, and that framework is essentially a greedy algorithm: every week, take the step that looks best right now. And greedy is not the same as globally optimal.

## Who brings new paradigms?

That raises the next question. Humans also iterate weekly inside frameworks like this. Why can humans bring paradigm-level change while LLMs can't?

My first intuition was that humans have new ideas and LLMs don't. That intuition doesn't hold up.

A study with more than a hundred NLP researchers found that LLM-generated research ideas were judged, in blind review, to be **more novel** than those of human experts, if slightly less feasible.[^si] Looking back at recommender systems' paradigm shifts, from Wide & Deep and YouTube's deep candidate generation to DIN, SASRec, TIGER and HSTU,[^paradigms] many of the key ideas already existed in other fields: attention and Transformers came from NLP, generative retrieval from information retrieval, scaling laws from large language models. Carrying an idea from one field to another is exactly what LLMs are good at.

What humans really have in addition is not ideas but three things: persisting through a run of negative results; building new modules from scratch for a new direction; and placing a bet, then being accountable for it.

There's an even more basic fact to admit: **humans don't reliably make the right call either.** We remember the people who bet right. The people who bet on the wrong direction at the same time, spent years on it and quietly gave up, we don't remember. Overall, the hit rate of human bets under high uncertainty is not high. Our sense that "humans get it right" is largely survivorship bias.

## Nintendo: lateral thinking with withered technology

When it comes to knowledge transfer, the company I admire most is Nintendo. Its design philosophy comes from a phrase of Gunpei Yokoi's: "lateral thinking with withered technology."[^yokoi] Don't chase the newest technology; take technology that is mature, cheap and well understood, and use it somewhere nobody else thought of.

Almost every Nintendo breakthrough came this way. The story goes that Yokoi saw a bored businessman on the bullet train fiddling with an LCD calculator, and that became the Game & Watch. The Game Boy had a monochrome screen while its rivals had backlit colour screens, but it was cheap, tough and easy on batteries, and it won. The accelerometers in the Wii remote were cheap parts that were already everywhere, and the console was clearly weaker than its competitors. The Switch shipped with a mobile chip that was two years old.

I find this remarkable. And it isn't just Nintendo: most breakthroughs at the company level come from here. The economist Brian Arthur argues that new technologies are almost always new combinations of existing ones.[^arthur] Multi-touch, capacitive screens, mobile chips: none of the iPhone's parts were invented by Apple.

But look closely at Nintendo, and the technology is not the hard part. Carrying mature technology somewhere new is, as I said above, exactly what LLMs can do too. The hard part is two other things.

**First, it rejected the whole industry's reward.** For years the games industry's reward was horsepower, graphics, specs, with everyone pushing greedily along the same metric. By choosing weaker technology, Nintendo deliberately stepped out of that race and optimized a different objective: who would play, and how it would feel. The Wii brought grandparents and kids into the living room, not with a better graphics card, but by changing the reward. And choosing which reward to pursue is itself a value judgment.

**Second, it had a runway.** Nintendo bet wrong plenty of times. The Virtual Boy was close to Yokoi's own Waterloo, and he left Nintendo not long after. Lateral thinking with withered technology is not a formula that guarantees success; we remember the Game Boy and easily forget the Virtual Boy, which is survivorship bias again. The Wii U was a commercial failure too, but the idea of merging the home console and the handheld wasn't abandoned, and five years later it became the Switch. An idea held through years of negative results before it finally worked: that's a runway.

## The difference is the reward

So where is the real difference between humans and LLMs? Nintendo already hints at it: I think the root is the reward.

An LLM is rewarded for two things in training: in pretraining, predicting the most likely next word in its corpus; in alignment, satisfying the rater in front of it. The first pulls its default position toward consensus. The second makes it inclined to please: push back, and it tends to change its answer.[^syco] While discussing this post with an AI, I pushed back twice, and twice it changed its answer. Both times I was right. But what if I'd been wrong?

Put together, an LLM optimizes for "looks right now and satisfies the person in front of me," not "turns out to be right."

A human's reward is different. Humans face real outcomes that arrive much later, stakes that land on themselves, and their own convictions. But humans have plenty of bad rewards too: half-year performance cycles, weekly metrics, organizational politics. Under short-term rewards, a room full of very smart people will make locally optimal choices just the same, and when they can't deliver, they get busy assigning blame.

So humans don't naturally reason from first principles either. Most people, most of the time, are chasing the reward in front of them and following consensus.

Truly sticking to first principles takes two things. The first is **axioms**. In recommender systems, "what is a user's long-term value," "how much information does this signal actually carry," "compute is cost" are not derived; they're worn in by long contact with real data and failed experiments. An LLM can derive, but its axioms are secondhand. The second is **persistence**: holding on to your own conclusion through months of negative results while everyone around you says it won't work. Today's LLMs have no persistent self across sessions, pay no price for a wrong bet, and are trained to give way.

In the end:

> A paradigm shift is, at its core, going against the reward in front of you to chase a farther reward you believe in. Humans occasionally manage it. LLMs are trained not to.

## Give the LLM a runway

So the problem is not "LLMs can't." It's that we haven't given them that environment. If we really want an LLM to make non-greedy decisions in a recommender system, what has to change is the reward it lives under:

- a fixed long-term objective, such as long-term retention, that short-term metrics cannot override;
- persistent memory of the hypotheses it proposed, the bets it placed, and how they turned out;
- an explicit budget for negative results, allowing it to be negative in one direction for weeks or even months without being shut down;
- evaluation on long horizons, not weekly.

Look closely and this list is exactly what organizations give their senior people: a mandate, and a runway.

You could also build it as two tiers. The fast tier keeps iterating greedily every week, run by classic automated pipelines, and collects every short-term win available. The slow tier belongs to the LLM: it holds a few long-term bets, with its own runway and memory, and reviews results quarterly.

In other words, **the hardest part of building the experimentation framework is designing the reward.** If the framework only offers a weekly A/B reward, even the smartest LLM will just reach local optima faster and more thoroughly. When a measure becomes a target, it ceases to be a good measure; the old saying holds for LLMs too, maybe more so, because they optimize more thoroughly than people do.

## What stays with humans

Looking back at the differences between humans and LLMs, they fall into two groups.

One group is capability gaps: context that was never written down, like who tried what three years ago and why it failed, and the ability to keep learning from a small number of one's own long-delayed outcomes. These will shrink as memory and continual learning improve.

The other group isn't about capability: who is accountable for the outcome, and value choices such as whether a recommender should be more grassroots or more elite. These questions have no right answer. They go to humans not because humans choose better, but because humans can be held accountable and have the legitimacy to make such choices.

So my view is this: LLMs will replace people's execution, and even most of their judgment; but accountability and value choices will stay with humans.

The previous post said LLMs replace the person. This one adds: what they lack isn't intelligence, but a reward that isn't greedy, and a runway that lets them be wrong.

And whether to give them that runway is itself a human decision.

---

[^longterm]: Henning Hohnhold, Deirdre O'Brien, Diane Tang. *Focusing on the Long-term: It's Good for Users and Business.* KDD 2015.
[^kohavi]: Ron Kohavi, Diane Tang, Ya Xu. *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing.* Cambridge University Press, 2020.
[^si]: Chenglei Si, Diyi Yang, Tatsunori Hashimoto. *Can LLMs Generate Novel Research Ideas? A Large-Scale Human Study with 100+ NLP Researchers.* ICLR 2025. arXiv:2409.04109.
[^paradigms]: Cheng et al. *Wide & Deep Learning for Recommender Systems*, 2016; Covington et al. *Deep Neural Networks for YouTube Recommendations*, RecSys 2016; Zhou et al. *Deep Interest Network for Click-Through Rate Prediction*, KDD 2018; Kang & McAuley. *Self-Attentive Sequential Recommendation*, ICDM 2018; Rajput et al. *Recommender Systems with Generative Retrieval*, NeurIPS 2023; Zhai et al. *Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations*, ICML 2024.
[^yokoi]: Gunpei Yokoi, Takefumi Makino. *Yokoi Gunpei Game-kan* (横井軍平ゲーム館). ASCII, 1997.
[^arthur]: W. Brian Arthur. *The Nature of Technology: What It Is and How It Evolves.* Free Press, 2009.
[^syco]: Mrinank Sharma et al. *Towards Understanding Sycophancy in Language Models.* ICLR 2024. arXiv:2310.13548.
