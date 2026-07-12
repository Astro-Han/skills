<h1>Astro Skills <sub><a href="README.md">English</a></sub></h1>

![Every token should change behavior.](assets/astro-skills-hero.png)

## 每一个 token，都得起作用。

这套 skills 不教 Agent 走更长的流程，只在它容易做错决定的地方拉一把：动手之前先问清楚，修 bug 之前先找到证据，收到 review 之后先判断对不对，结束任务之前把该收的尾收干净。

## 我为什么做这套 skills

我最早用的是 [Superpowers](https://github.com/obra/superpowers)。它让我第一次看到，一套设计严密的工作流，确实能让 Agent 把代码写得更靠谱。但用久了，我也越来越觉得它太重。哪怕只改几行代码，也可能要从 spec、plan 一路走完整套开发流程。

后来我看到 Matt Pocock 的 [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)。内容短得惊人，效果却很好。它没有试图包办整个流程，只抓住了最要紧的一件事：在真正需要用户拿主意的地方，别让模型自己猜。

这件事改变了我对 skill 的理解。Skill 不是越长越好，也不是流程越完整越好。真正有用的 skill，应该找到模型最容易犯错的那个点，用尽可能少的指令把行为纠正过来。

后来我就按这个标准重写自己常用的 skills：每一个都要解决真实、反复出现的问题；每一句话都要对模型有用；能删的继续删，直到再删就会影响效果。

## 这些 skills 有什么用

| Skill | Agent 常犯的问题 | 用了之后 |
| --- | --- | --- |
| [`goal-writer`](skills/goal-writer/) | 长任务只有一个模糊目标，做到哪算完成、遇到什么该停，都说不清。 | 把目标写成一份有边界的执行契约，明确验证证据、完成条件和需要用户介入的关口。 |
| [`shape`](skills/shape/) | 关键选择还没聊清楚，就急着开始实现。 | 把方案拆成一棵 design tree，每次只和你确认一个真正影响结果的分支。 |
| [`debug`](skills/debug/) | 看到一个像是原因的地方，马上动手修。 | 先稳定复现，再用能排除其他可能的证据确认根因。 |
| [`tdd`](skills/tdd/) | 代码写完才补测试，测试只能证明代码现在能跑。 | 先看到符合预期的 RED，再写出最小的 GREEN，最后在测试保护下重构。 |
| [`review-feedback`](skills/review-feedback/) | 把 review 意见当成命令，别人说什么就改什么。 | 先验证意见是否成立，再决定该改、暂缓、删掉，还是应该反驳。 |
| [`parallel-research`](skills/parallel-research/) | 几个研究者重复搜索同一个方向，增加的只是信心，不是证据。 | 每个人负责一个独立的证据方向，最后由主 Agent 核对冲突和关键结论。 |
| [`wrap-up`](skills/wrap-up/) | 总结写完了，自己留下的进程、临时文件或未提交改动却没人管。 | 先核对结果和现场，处理完本次会话留下的问题，再报告最终状态。 |
| [`learn-anything`](skills/learn-anything/) | 把“听懂了”误当成“学会了”。 | 让学习者自己回忆、应用和复述，直到这份理解真的能拿来用。 |

`shape` 最能代表这套思路。它真正重要的只有 design tree：凡是会把方案带向不同方向的选择，都应该拿出来和用户逐项确认，而不是让模型悄悄替用户做决定。如果要选的是界面、布局或其他视觉方案，就直接做成 HTML 给人看。能看，就别只靠说。

## 安装

安装全部 skills：

```bash
npx skills add Astro-Han/skills
```

也可以只装一个：

```bash
npx skills add Astro-Han/skills --skill shape
```

支持哪些 Agent、还有哪些参数，可以查看 [Skills CLI 文档](https://skills.sh/docs)。

## 我的取舍标准

- 只解决 Agent 真实、反复出现的问题。
- 找到最小但足够的指令，把错误行为纠正过来。
- 看证据和实际结果，不追求流程上的完整感。
- 条件允许时，尽量拿较弱的模型来试。如果换成弱模型就没效果，那很可能只是基础模型够强，不是 skill 写得好。

模型的上下文很宝贵。如果删掉一句话，并不会让它把事情做得更差，那这句话就没有必要留下。

## 来源与致谢

- `learn-anything` 和 `wrap-up` 是我从自己的工作流里做出来的原创 skills。
- `shape` 借鉴了 Matt Pocock 的 [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)。遇到视觉选择时直接展示方案，这一点来自 Superpowers 的 [`brainstorming`](https://github.com/obra/superpowers/tree/main/skills/brainstorming)。
- `tdd` 借鉴了 Matt Pocock 的 [`tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)。
- `debug` 参考了 Matt Pocock 的 [`diagnosing-bugs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs)、Superpowers 的 [`systematic-debugging`](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) 和 Waza 的 [`hunt`](https://github.com/tw93/Waza/tree/main/skills/hunt)。我有意删掉了其中不少流程，只留下最小的证据链。
- `review-feedback` 最初参考了 Superpowers 的 [`receiving-code-review`](https://github.com/obra/superpowers/tree/main/skills/receiving-code-review)，后来围绕证据、职责、改动范围和系统成本重新写过，现在已经很不一样了。

这些外部项目仍然是各自 skills 的权威来源。这里放的是我自己的改写版本，没有直接复制外部 skill。Astro Skills 以英文 `SKILL.md` 为准。

## 许可

MIT
