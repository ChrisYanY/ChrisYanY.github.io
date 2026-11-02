---
title: "Seeding Creation"
date: 2026-11-01
summary: "Getting users to create is the same kind of growth problem as seeding and closing a sale in commerce. Almost everything commerce has learned carries over: seeding makes people want to create, closing helps them finish, and when creators start seeding other creators, the ecosystem turns on its own."
label: "Thoughts"
tags: ["Creator Ecosystem", "Creation", "Recommender Systems", "Growth", "Thoughts"]
math: false
mermaid: false
translationKey: "creation-seeding"
ai_assisted: true
ai_note: "The views come from the author's own discussion with an AI; the write-up is AI-assisted."
---

Working on creator ecosystems, I say "inspire creation" almost every day. Say it often enough and you notice how vague it is. What makes a piece of content "inspiring"? What actually happens between a user watching a video and making one of their own?

A few mornings ago it occurred to me: this is just *zhongcao*.

*Zhongcao* (种草, literally "planting grass") is the Chinese commerce term for seeding desire: content plants a little want in someone's mind, and over time it grows into a purchase. Its partner is *bacao* (拔草, "pulling the grass"): the moment that want is acted on and the purchase is made.

With creation, what gets planted isn't a product. It's a thought: "I want to make one too."

The more I followed that thought, the less it felt like a metaphor.

## The same kind of growth problem

Here is my view: **getting users to create is the same kind of growth problem as seeding and closing a sale in commerce.**

Both try to do the same thing. A user is scrolling, and the platform wants them, in the middle of scrolling, to take a **more costly action**. Commerce wants them to spend money on something; creation wants them to spend time making something. And in both cases, what drives that action is mostly what they see while scrolling.

Put the two side by side and the structure is almost identical:

| | Commerce | User creation |
|---|---|---|
| Target action | Purchase | Publish a creation |
| Cost of the action | Money | Time, skill, and the nerve to post it |
| Content that drives it | Recommendation posts, creator videos, ads | Other people's creations, templates, music |
| Product initiatives that drive it | Sales events, product launches, flash sales, brand challenges | Trends, challenges, seasonal topics, creation campaigns, creator incentives |
| Intent signals | Search, add-to-cart, save | Saving a song, opening a template, opening the camera, saving a draft |
| Closing infrastructure | Cart, coupons, one-tap checkout | Templates, one tap into the editor, drafts |
| Measurement difficulty | Attribution is noisy; true incrementality is what matters | The same problem |
| Tradeoff with consumption | More ads degrade the experience | Users who go off to create scroll a little less |
| What it means for the ecosystem | More sellers, richer supply | More creators, richer content |

One thing in this table is worth calling out: **growth on both sides walks on two legs, content and initiatives.** Content does the everyday, continuous seeding. Initiatives create concentrated moments that give users a reason to act *now*. Commerce has Singles' Day; creation has trends and challenges.

If this is the same problem, then the funnels, playbooks and measurement methods commerce has validated over the years, along with the mistakes it has made, are all worth borrowing.

This class of problem has more members than these two: following someone, paying for a subscription, sending a gift in a live stream are all "moving from consuming to acting". Commerce just happens to have studied it most thoroughly, and creation happens to be what I work on every day.

## One funnel: seeding, closing, and self-sustaining

Chinese platforms have turned seeding into a fine-grained craft. Ocean Engine's O-5A model splits users into five layers: Aware, Appeal, Ask, Act and Advocate.[^o5a] What I find most notable is how the third layer, Ask, is defined: not by how much someone has watched, but by **proactive, high-intent actions** such as searching and adding to cart.

The insight behind it is simple: **seeing is not wanting, and wanting is not doing.** There is a hurdle between every pair of layers.

Mapped to creation:

| Stage | Commerce | Creation | Belongs to |
|---|---|---|---|
| Aware | Comes across a product | Comes across something they could imitate | Seeding |
| Appeal | Watches again, is moved | Thinks "I want to try this" | Seeding |
| Ask | Searches, adds to cart | Saved a song, opened a template, saved a draft, but hasn't posted | The boundary between seeding and closing |
| Act | Buys | Publishes | Closing |
| Advocate | Buys again, recommends to friends | Keeps creating, and gets others to create too | Self-sustaining |

I use Ask, the moment a user is already tempted, as the dividing line. **Seeding** brings people to that moment and answers "seed whom, with what?". **Closing** takes them from tempted to published and answers "how do we follow up on that want?". **Self-sustaining** is the last layer: creators seeding more people in turn.

Looking at this table, my strongest impression is that in creation, most of the effort goes into the first two layers: getting users to see more inspiring content. Yet a large number of users are already stuck at the third. They saved a song, opened a template, maybe even shot half of something, and then nothing. In commerce, users with something sitting in their cart are the most valuable users there are. In creation, this group is rarely singled out.

## Seeding: making people want to create

I think seeding breaks down into six pieces of work:

| Work | How commerce does it | How creation can do it |
|---|---|---|
| Find content that seeds | Reviews, roundups, tutorials | Replicable creations, tutorials, timely and fresh formats |
| Seed the right people | Audience targeting | Target by creation propensity, creative niche and interests |
| Pick the right seed sources | KOL / KOC pyramid, weighted to the middle tier | Let "people like me" do the seeding, not the biggest accounts |
| Product initiatives | Sales events, launches, brand challenges | Trends, challenges, seasonal topics, delivered to the right people |
| Lower the barrier | Free samples | Templates, the same song, one tap into the editor |
| Social proof | Sales counts, reviews | "10,000 people made this", "someone you follow made this" |

**Find content that seeds.** Content that makes people want to create is often not the same content that makes people want to keep scrolling. Tutorials, fresh formats and creations ordinary people can reproduce are not necessarily the most "watchable", but they are the most likely to get someone started. Timeliness matters too: a format that is just emerging inspires far more than one that has been done to death.

**Seed the right people.** The worst way to seed is to sprinkle it everywhere. The same piece of content does very different things when shown to someone who already creates in that niche versus someone who only watches.

**Pick the right seed sources.** Brand seeding works as a pyramid: top KOLs create buzz, while mid-tier creators and many ordinary users (KOCs) drive conversion. An early large-scale experiment at Facebook found that while a single strong tie is more influential, most new information actually spreads through the sheer number of weak ties.[^bakshy] This is even more true for creation. When a creator with a million followers makes something, ordinary viewers think "that's their thing". When someone like them makes it, they think "I could do that."

**Product initiatives.** Commerce concentrates its bursts in sales events; creation uses trends and challenges to give people a reason to create now. The recommender's job here is to deliver the initiative to the right people: a beauty creator won't care about a basketball challenge, and an initiative pushed to the wrong people is just noise, however hot it is. Trend stage matters as well: early on, show it to people who like to try new things; later, show it to people who need something to copy.

**Lower the barrier.** Free samples are one of the oldest tools in marketing. Research found that the value of sampling is not only that people who would have bought anyway buy sooner; more importantly, it creates **expansion**: people who would never have tried the product try it once.[^sampling] Creation's free samples are templates, the same song, pre-cut beats. Their biggest value is not serving existing creators, but bringing in people who have never made anything. And once someone is tempted, take them straight into the editor. Every extra page in between loses another group of people.

**Social proof.** A well-known experiment with an artificial music market found that letting people see others' choices significantly changed their own.[^salganik] At the moment a user is hesitating, telling them how many people, or which of their friends, have already made one often works better than showing them ten more example videos.

**How do you know the seed took?** RED and Douyin often measure seeding by "search after viewing": did the user go search for the thing after seeing the content? Creation can have a counterpart, "create after viewing": did they save the song, open the template, start creating? But these attribution numbers are easy to overestimate. One study compared approaches directly and found that observational attribution methods often fail to recover the true ad effects measured in randomized experiments.[^gordon] To know whether seeding really works, you ultimately need A/B tests.

## Closing: helping them finish

After seeding comes closing. In commerce, closing is a whole set of infrastructure: carts, coupons, one-tap checkout, price-drop alerts. Platforms put enormous effort into making sure people who are already tempted can pay without friction.

In creation, closing means helping someone who is already tempted, or has already started, finish the piece. Almost no one works on this seriously today. I think it breaks down into five pieces of work:

| Work | How commerce does it | How creation can do it |
|---|---|---|
| Identify the tempted | People who added to cart, saved, searched | People who saved a song, opened a template, saved a draft |
| Repeated same-interest exposure | Retargeting | Keep showing content from the same interest across sessions |
| Broad to narrow over the lifecycle | From category to specific model | From direction, to concrete references, to detailed techniques |
| Advance, don't imitate | Show what drives the purchase, not just what gets clicked | Show what moves them a step forward, not just what they'd watch |
| Reduce friction, remind at the right time | Cart reminders, price-drop alerts | After a draft sits for a few days, bring them back with related content |

**Identify the tempted.** Closing starts with finding these people. It can go one step finer: group them by the creation entry point they used most recently. People who came in through a music page, through a template, or by opening the camera themselves need different kinds of help.

**Repeated same-interest exposure.** Once a user shows intent, it is worth continuing to show them content from the same interest over their next few sessions. But commerce has hit a pitfall here: research found that repeatedly showing people the **same** product they had shown interest in was, on average, less effective than generic ads.[^retarget] So the point of repeated exposure is "the same interest, different content", and frequency should be restrained. Seeing the same creation opportunity two or three times a day feels like seeding; seeing it ten times feels like nagging.

**Broad to narrow over the lifecycle.** To me this is the most interesting part of closing. Someone needs completely different things at different stages of creating, so the scope of recommendations should narrow as they go. Take someone who wants to film themselves making pour-over coffee at home:

| Stage | What they are doing | Scope | What to show |
|---|---|---|---|
| Has an idea | Wants to make a coffee video | Broad: coffee, lifestyle vlogs | Coffee videos in many styles, to help them find a direction |
| Starts filming | Saved a draft, shot a few clips | Medium: the same format | Other single-take pour-over videos, commonly used music |
| Polishing | Editing, choosing music, color grading | Narrow: the same technique | Transition tutorials, the best videos using the same song, color references |
| After publishing | The video is out | Back to broad | Fresh inspiration, starting the next round |

This mirrors commerce too: show categories while someone is browsing, specific models once they know what they want, and reviews and comparisons just before they buy.

**Advance, don't imitate.** Behind broad-to-narrow is a change in what the recommender is trying to do. Normally a recommender asks "what will they probably watch next?", which imitates their past behavior. For someone in the middle of creating, the better question is "what can I show them that moves this piece one step forward?". The first may show them things they'd drift off-topic into; the second shows them things that send them back to the draft to keep going.

**Reduce friction, remind at the right time.** Cart reminders work because they remind users of something they themselves wanted. Creation is the same: when a draft has been sitting for a few days, rather than a generic "come create something!", show them a great piece related to their draft and let it bring them back naturally. An unwanted reminder is spam; a reminder about what they are working on is help.

**How do you know the deal closed?** Closing is measured by draft completion rate and time from start to publish. Completion rate matters more: most drafts don't fail because they are slow, they fail because they are abandoned.

## Self-sustaining: creators seeding creators

Back to the last layer of the funnel: Advocate. In commerce, advocacy is repeat purchase and word of mouth. In creation, it is someone who keeps creating, and whose work gets more people to create.

In my post on [the creator flywheel](/posts/creator-flywheel/), I drew a loop: consumers become creators, creators produce content, and content flows back to consumers. The part of that loop most easily overlooked is the "inspire" path: **creation itself seeds creation.**

Whether an ecosystem can turn on its own depends largely on this path. If every new creator has to be inspired by the platform, the ecosystem will always need the platform to push it. Only when a creator's work reliably reaches people who are similar to them and on the fence, and gets them to start too, does the ecosystem begin to sustain itself. So distributing creators' work should also be treated as seeding: show it not only to people who will watch it, but to people who will create because of it.

The other half of self-sustaining is the creation equivalent of a repeat purchase: when a newcomer posts for the first time, do they quickly get likes, comments and follows? A good first experience is what leads to a second.

| | Commerce | Creation |
|---|---|---|
| Repeat purchase | Satisfied with the first purchase, so buys again | Gets feedback on the first post, so posts again |
| Word of mouth | Buyers recommend it to friends | Their creation gets similar people to create too |

## Where it differs from commerce

Calling them the same kind of problem doesn't mean they are identical. There are at least three differences.

First, **the goal diverges from consumption value.** In commerce, products that sell well are often also things users like to look at. In creation, that's not the case: content that makes people want to create and content that makes people want to keep scrolling are often not the same. Distribute purely on consumption value, and the content most likely to inspire creation gets buried. So creation needs its own objective; you can't expect consumption-side recommendation to take care of it along the way.

Second, **there is a tradeoff between creating and consuming.** When users go off to make a video, they scroll a little less. In the long run, more creators mean more good content, and the trade is very likely worth it; but it should be seen clearly and chosen deliberately, not ignored.

Third, **too much seeding makes content homogeneous.** The more of a product you sell, the better. But when the same song or the same template is copied by a million people, the platform is left with only one voice. Imitation is how many people take their first step, and that is fine; but the end point of seeding should be more people starting to express themselves, not more people repeating the same thing.

## Finally

Commerce seeds desire, and the end point is a purchase.

Seeding creation, the end point is one more creator.

[^o5a]: Ocean Engine (ByteDance), O-5A audience asset model.
[^bakshy]: Eytan Bakshy, Itamar Rosenn, Cameron Marlow, Lada Adamic. *The Role of Social Networks in Information Diffusion.* WWW 2012. arXiv:1201.4145.
[^sampling]: Kapil Bawa, Robert Shoemaker. *The Effects of Free Sample Promotions on Incremental Brand Sales.* Marketing Science, 2004.
[^salganik]: Matthew Salganik, Peter Dodds, Duncan Watts. *Experimental Study of Inequality and Unpredictability in an Artificial Cultural Market.* Science, 2006.
[^gordon]: Brett Gordon, Florian Zettelmeyer, Neha Bhargava, Dan Chapsky. *A Comparison of Approaches to Advertising Measurement: Evidence from Big Field Experiments at Facebook.* Marketing Science, 2019.
[^retarget]: Anja Lambrecht, Catherine Tucker. *When Does Retargeting Work? Information Specificity in Online Advertising.* Journal of Marketing Research, 2013.
