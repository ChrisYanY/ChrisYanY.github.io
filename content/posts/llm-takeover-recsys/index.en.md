---
title: "LLMs Taking Over RecSys? Maybe We're Running in the Wrong Direction"
date: 2026-10-09
summary: "An LLM is more like a knowledgeable person than a precision machine. Rather than letting it take over recommender systems, let it and classic models each do what they do best."
label: "Thoughts"
tags: ["LLM", "Recommender Systems", "Essay"]
math: false
mermaid: false
translationKey: "llm-takeover-recsys"
ai_assisted: true
ai_note: "The views are my own; the write-up was AI-assisted."
pinned: true
---

There is a growing tendency in academia to pursue LLMs that fully take over recommender systems. In my view, that is a dead end, or at the very least not the right road, and we shouldn't be sprinting down it.

LLMs combined with classic computational models are the right approach. Different model architectures are naturally suited to different jobs. When people do math, they still reach for pen and paper, or a calculator, once the arithmetic gets hard. The same logic applies here.

Why do I think so? Because an LLM is more like a person than a precision machine. Once you see that, it becomes clear where it belongs in a recommender system.

## For the first time, it "understands" content

What a piece of content is about used to be something only human reviewers could tell you. Classic recommender systems never truly knew it; they simply worked around the problem. Collaborative filtering and sequence modeling don't need to understand the content at all. They only need to observe "people who liked A also liked what?" The price is that you need traffic first. Until enough people have seen a new piece of content, it is close to a blank to the system.

Anyone who has worked on recommendations has seen the consequences of not understanding content: the system easily falls into a local optimum. Whatever topics have good engagement soak up all the traffic, and "personalization" ends up looking the same for everyone. Platforms fill up with memes, borderline sexual content, and pet videos: content low in information but great on the metrics.

It's not that nobody wants to break out. On one hand, metric pressure keeps platforms from exploring enough. On the other, when you don't understand the content, every bit of exploration has to be paid for with real traffic, and that is expensive. So balancing traffic has largely been left to operations teams and manual intervention, or to hand-designed diversity metrics that only partially help.

LLMs are the first thing that can tell you what a piece of content is and what it's about, with no traffic and without first trying it on users. For the first time, a system can know, before spending any traffic, whether a piece of content is worth trying and whom to try it on. Classic systems can't do this, or do it poorly. It is the most distinctive thing LLMs bring to recommender systems.

## Knowledgeable, but imprecise

An LLM is like a knowledgeable salesperson in a store. Tell them what style you like, and they immediately know which racks to check, even for new arrivals that went on the shelf this morning and that no one has bought yet.

But they can't answer a different question: exactly how much do you like this shirt? Is it 75%, 77%, or 83%?

Say there are ten videos you like to some degree: 0.8, 0.75, 0.9, and so on. In everyday life, it hardly matters which one you watch first.

In a large-scale recommender system, though, getting the order wrong often costs 0.1% or 0.2% in time spent, sessions, or long-term retention. These are differences a person would shrug off, but multiplied by hundreds of millions of impressions a day and accumulated over time, the losses add up to something serious. In ads it's even more direct: this probability determines how much a single impression is charged. An early Facebook paper on ad click prediction makes the point that even a small improvement in prediction accuracy translates into real business gains.[^fb]

Fitting that level of precision takes careful modeling, massive traffic, and a large number of features that "memorize" specific users and specific items. LLMs can't handle this kind of precise computation. It's a job for a precision machine, not for a person.

Interestingly, an LLM's strength and its weakness come from the same place. It can understand content without seeing any data because, like a person, it generalizes from semantics and common sense. The flip side of generalization is that it doesn't memorize precise statistics. Google's 2016 Wide & Deep paper split what a recommender needs into two halves: memorization and generalization.[^wd] Through that lens, LLMs have pushed generalization further than ever, but the memorization half still belongs to classic models.

In *Thinking, Fast and Slow*, Kahneman describes how human intuition is fast and often right, yet error-prone the moment it has to estimate probabilities precisely.[^kahneman] LLMs inherit exactly this profile. One team has recently started building "System One" models designed to output calibrated probabilities, the name taken from Kahneman's "fast thinking,"[^jev] a sign that people recognize this gap. Maybe models like that will change the picture someday, but today, the gap between LLMs and classic recommender systems on precise scoring is still large.

## The math doesn't work either

There's an even more basic problem: cost.

Every time a user refreshes, the system has to pick the best few out of hundreds of candidates. If an LLM scored every one of them, the inference cost would quite likely exceed the revenue that refresh brings in. At the scale of real-world traffic, letting an LLM take over ranking entirely is not realistic for now.

Understanding a piece of content, by contrast, only has to happen once, and the result is reused by every impression that follows. Put the LLM in the "understand the content" seat and the math works; put it in the "score every request" seat and it doesn't.

## So LLMs replace the person

If an LLM is more like a person, the question becomes: which parts of a recommender system were people doing in the first place?

Deciding what a piece of content is about and whether it's compliant: that was reviewers. Choosing features, trading off objectives, deciding what the next experiment should test: that was engineers. Deciding which new content to support, how to balance traffic, how to pull the system out of a local optimum: that was operations. These jobs call for understanding, judgment, and common sense, not probabilities accurate to two decimal places.

The parts that need precise probabilities were never done by people in the first place. They were done by probabilistic models.

So the recommender system I have in mind is one where LLMs and classic models work together. LLMs handle understanding and judgment; classic models handle precise computation. Going further, the LLM can coordinate and orchestrate those classic model modules on its own, using them to cover its weaknesses. That is also where LLMs themselves are heading: when facing precise computation, the best move is never to brute-force it, but to learn to call a calculator, to call tools.[^toolformer] The idea of using an LLM as an optimizer, letting it call an evaluator and iterate, has already appeared in public research as well.[^opro] As I said at the start, a person doing hard math reaches for pen, paper, and a calculator; a knowledgeable person should likewise make good use of the precision instruments at hand.

People won't disappear entirely. The final system may still need a very small amount of human intervention, but it will need very few people, and they will work on very high-level questions: What style should this recommender have? Roughly what share should each kind of traffic get? Should it lean more "grassroots" or more "elite"? These are choices about direction, and they belong to people.

That is the future of recommender systems.

Put simply: LLMs replace the *person*, not the probability model.

---

[^fb]: Xinran He et al. *Practical Lessons from Predicting Clicks on Ads at Facebook.* ADKDD 2014.
[^wd]: Heng-Tze Cheng et al. *Wide & Deep Learning for Recommender Systems.* DLRS 2016. arXiv:1606.07792.
[^kahneman]: Daniel Kahneman. *Thinking, Fast and Slow.* 2011.
[^jev]: Diogo Almeida. *Introducing System One Models & Jev.* TypeSafe AI Blog, 2026-09-15. https://typesafe.ai/blog/introducing-system-one-models-and-jev
[^toolformer]: Timo Schick et al. *Toolformer: Language Models Can Teach Themselves to Use Tools.* NeurIPS 2023. arXiv:2302.04761.
[^opro]: Chengrun Yang et al. *Large Language Models as Optimizers.* ICLR 2024. arXiv:2309.03409. See also my [reading notes](/posts/opro-and-gr2/) on this site.
