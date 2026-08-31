# Astro Skills

[English](README.md) | 中文

![Every token should change behavior.](assets/astro-skills-hero.png)

## 每一个 token，都得起作用。

这套 skills 不教 Agent 走更长的流程，只在它容易做错决定的地方拉一把：动手之前先问清楚，修 bug 之前先找到证据，收到 review 之后先判断对不对，结束任务之前把该收的尾收干净。

## 我为什么做这套 skills

我最早用的是 [Superpowers](https://github.com/obra/superpowers)。它让我第一次看到，一套设计严密的工作流，确实能让 Agent 把代码写得更靠谱。但用久了，我也越来越觉得它太重。哪怕只改几行代码，也可能要从 spec、plan 一路走完整套开发流程。

后来我看到 Matt Pocock 的 [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)。内容短得惊人，效果却很好。它没有试图包办整个流程，只抓住了最要紧的一件事：在真正需要用户拿主意的地方，别让模型自己猜。

这件事改变了我对 skill 的理解。Skill 不是越长越好，也不是流程越完整越好。真正有用的 skill，应该找到模型最容易犯错的那个点，用尽可能少的指令把行为纠正过来。

后来我就按这个标准重写自己常用的 skills：每一个都要解决真实、反复出现的问题；每一句话都要对模型有用；能删的继续删，直到再删就会影响效果。

## 这些 skills 有什么用

| Skill | 什么时候用 | 你会得到什么 |
| --- | --- | --- |
| [`goal-writer`](skills/goal-writer/) | 你有一个有野心或需要长期推进的任务，但终点还很模糊。 | 一份最小执行契约，写清可观察结果、接受判据，以及当前任务真正需要的边界。 |
| [`shape`](skills/shape/) | decision tree 中还有影响结果的分支没有解决，而 Agent 自己猜会改变方案。 | 一份你确实参与决定并同意的方案；每次只解决一个关键分支。 |
| [`craft-skill`](skills/craft-skill/) | 你想创建或改进一个可复用的 Agent skill，也想知道它的指令是否值得占用上下文。 | 一份符合目标平台的 skill：用 Call 找对任务，用 Steer 把行动带到真正完成，再让每个 token、每次评测和每行代码通过 Earn。 |
| [`parallel-research`](skills/parallel-research/) | 一个重要问题需要广泛、最新且可信的证据。 | 更快得到覆盖充分、证据更扎实的答案：并行调查不同证据方向，再由主 Agent 交叉核验关键结论与冲突。 |
| [`learn-anything`](skills/learn-anything/) | 你想真正学会或练习一个主题，而不只是听一遍解释。 | 根据你的水平实时调整的辅导，通过主动回忆、应用和复述，建立真正能用的理解。 |
| [`eli5`](skills/eli5/) | 你想用视觉方式给一个完全不了解主题的人讲明白。 | 一张简单、好看、只有一个清楚想法的视觉解释：大图、少字。 |
| [`tdd`](skills/tdd/) | 你要新增或改变生产行为，需要快速而可信的反馈。 | 以小步、可验证的方式交付：先看到符合预期的 RED，再完成最小 GREEN，然后安全重构。 |
| [`debug`](skills/debug/) | bug 或性能退化需要调查，不能靠一个听起来合理的猜测。 | 一个可重复的故障信号、一条能排除其他可能的证据链，以及经过原始场景验证的根因。 |
| [`simplify-audit`](skills/simplify-audit/) | 一个已有代码库里堆着没人证明过还需要的复杂度。 | 一份关于什么真的可以消失的审计：每条删减都有需求链和净减少作为依据，还没证明闭合的线索单独列出，不包装成结论。 |
| [`review-feedback`](skills/review-feedback/) | code review 意见可能引发代码改动，需要先判断再行动。 | 对每条意见做出有证据的决定：在真正负责问题的层次修复、简化、暂缓，或明确拒绝。 |
| [`pr-review`](skills/pr-review/) | 你要审查一个 PR 或梳理 review 队列。 | 一份先证明问题与范围、再核对生产 ownership、完整 diff 和真实可达 P0–P3 finding 的审查结果。 |
| [`wrap-up`](skills/wrap-up/) | 工作即将结束，你要的是确实完成，而不只是一段总结。 | 一个真正收好的工作现场：承诺的结果经过验证，本次会话留下的问题得到处理，最终状态如实报告。 |

`shape` 最能代表这套思路。它真正重要的只有 decision tree：凡是会把方案带向不同方向的选择，都应该拿出来和用户逐项确认，而不是让模型悄悄替用户做决定。如果要选的是界面、布局或其他视觉方案，就用最接近目标产品的可用呈现方式忠实地并排展示；界面优先使用渲染后的 HTML。能看，就别只靠说。

## Evals

`evals/` 目前为 `tdd`、`debug`、`review-feedback` 和 `pr-review` 提供可执行的配对对照。
fixture 代替真实工作，共用 runner 保留每个 arm 的产物，grader 记录预先声明的检查项。
评测覆盖什么会明确写出，不暗示每个 skill 都已经接入自动评测。详见
[共用评测装置](evals/README.md) 和其中各 skill 的评测记录。

## 安装

### GitHub CLI

使用 v2.90.0 或更高版本的 [GitHub CLI](https://cli.github.com/manual/gh_skill_install)，为 Codex 安装全部 skills：

```bash
gh skill install Astro-Han/skills --all --agent codex --scope user
```

也可以只装一个：

```bash
gh skill install Astro-Han/skills shape --agent codex --scope user
```

如果使用其他 Agent，请替换 `codex`；如果只想在当前仓库中安装，请改用 `--scope project`。

### Skills CLI

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

- `learn-anything` 和 `wrap-up` 是我从自己的工作流里做出来的原创 skills。这里的 `eli5` 改写自 Thariq Shihipar 的 [`eli5`](https://github.com/anthropics/claude-plugins-community/tree/main/eli5)：保留“大图、少字”，使用当前最合适的视觉工具，没有可用工具时再回退到 HTML。
- `craft-skill` 借鉴了 [OpenAI 的 `skill-creator`](https://github.com/openai/skills/tree/main/skills/.system/skill-creator)、[Anthropic 的 `skill-creator`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)、Matt Pocock 的 [`writing-great-skills`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills) 和 Superpowers 的 [`writing-skills`](https://github.com/obra/superpowers-skills/tree/main/skills/meta/writing-skills)。它没有叠加四套流程，而是围绕三个约束重新构建：为正确的任务 Call skill，用 Steer 把 Agent 带到真正完成，并让每个 token Earn 自己的位置。
- `shape` 借鉴了 Matt Pocock 的 [`grilling`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)。遇到视觉选择时直接展示方案，这一点来自 Superpowers 的 [`brainstorming`](https://github.com/obra/superpowers/tree/main/skills/brainstorming)。
- `tdd` 借鉴了 Matt Pocock 的 [`tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)。
- `debug` 参考了 Matt Pocock 的 [`diagnosing-bugs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs)、Superpowers 的 [`systematic-debugging`](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) 和 Waza 的 [`hunt`](https://github.com/tw93/Waza/tree/main/skills/hunt)。我有意删掉了其中不少流程，只留下最小的证据链。
- `simplify-audit` 基于 [M4n5ter 的 `simplify-audit`](https://github.com/M4n5ter/skills/tree/main/simplify-audit) 重写，改成默认怀疑的姿态、不对称举证，并把三层报告按「还缺什么才能删掉」命名——什么都不缺、缺一个事实、缺一个决定——只差一个仓库内查不到的事实的高信号线索不再被直接丢掉。其中两个猎场——成熟依赖已经提供却手搓的基础设施、防御性拷贝与重复的生命周期状态——来自 DeepSeek 的 [`dsh-find-simplifications`](https://github.com/deepseek-ai/deepseek-harness/tree/master/.agents/skills/dsh-find-simplifications)。
- `review-feedback` 最初参考了 Superpowers 的 [`receiving-code-review`](https://github.com/obra/superpowers/tree/main/skills/receiving-code-review)，后来围绕证据、职责、改动范围和系统成本重新写过，现在已经很不一样了。

这些外部项目仍然是各自 skills 的权威来源。这里放的是我自己的改写版本，没有直接复制外部 skill。Astro Skills 以英文 `SKILL.md` 为准。

## 许可

MIT
