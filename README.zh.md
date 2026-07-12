# Astro Skills

[English](README.md)

## 每一个 token，都应该改变模型的行为。

这是一组帮助编码 Agent 做出更好判断的小型 skills：动手前确认，修复前举证，接受意见前验证，停下来前真正闭环。

## 我为什么做这些 skills

我最初使用的是 [Superpowers](https://github.com/obra/superpowers)。它让我看到，结构化工作流确实能显著改善 Agent 编码。但在日常使用中，我也觉得它完整的 spec → plan → development 流程太重了。有时只改几行代码，也要走完整套流程。

后来我看到了 Matt Pocock 的 [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)。它短得出人意料，却恰好改变了对话中最关键的行为。那一刻我真正意识到：skill 的价值不在于说了多少，而在于能否用很少的指令，稳定改变一个重要行为。

Astro Skills 就从这个标准长出来。只有真正值得占用模型上下文的约束才会留下：对应一个反复出现的问题，带来一个可观察的行为变化，然后一直删到不能再删。

## 这些 skills 解决什么问题

| Skill | 没有它时 | 使用它后 |
| --- | --- | --- |
| [`shape`](skills/shape/) | 关键设计分歧还没有浮出水面，Agent 就开始实现。 | Agent 沿着 design tree，每次与你确认一个真正影响结果的分支。 |
| [`debug`](skills/debug/) | Agent 找到第一个看似合理的原因就开始修补。 | 它先建立可重复的信号，再用有区分力的证据确认根因。 |
| [`tdd`](skills/tdd/) | 实现写完才补测试，测试很难证明设计过程。 | Agent 亲眼看到符合预期的 RED，只写出最小 GREEN，再安全重构。 |
| [`review-feedback`](skills/review-feedback/) | Review 意见被直接当成指令执行。 | 每条意见先验证，再在正确的职责归属处修复、推迟、简化或拒绝。 |
| [`wrap-up`](skills/wrap-up/) | 会话写完总结，却留下自己制造的未完成现场。 | Agent 验证结果、清理本次工作足迹，并报告真实的最终状态。 |
| [`learn-anything`](skills/learn-anything/) | 清楚的解释让人产生“已经学会”的错觉。 | 主动回忆、应用和 teach-back 帮助学习者建立真正能用的理解。 |

`shape` 最能体现这套设计。它的核心是 **design tree**：只要一个分支会实质改变结果，Agent 就应该和用户逐项讨论，而不是默默替用户选择。如果这真的是一个视觉决策，它会把方案做成 HTML，因为让人直接看到，永远比用文字描述更清楚。

## 安装

安装全部 skills：

```bash
npx skills add Astro-Han/skills
```

或只安装一个：

```bash
npx skills add Astro-Han/skills --skill shape
```

支持的 Agent 和其他参数见 [Skills CLI 文档](https://skills.sh/docs)。

## 唯一的标准

- 从 Agent 真实、反复出现的问题出发。
- 找到能够改变这个行为的最小指令。
- 保留证据和可观察结果，删掉流程仪式。
- 条件允许时，用较弱模型验证要求较高的 skill。如果 skill 只有依靠强基础模型才有效，它本身就还没有证明多少价值。

每一行都在争夺有限的上下文。如果删掉一句话不会让 Agent 把事情做得更差，这句话就不该留在 skill 里。

## 来源与致谢

- `learn-anything` 和 `wrap-up` 完全来自我自己的工作流，是原创 skills。
- `shape` 借鉴了 Matt Pocock 的 [`grill-me`](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me)；其中视觉决策的规则，也延续了 Superpowers [`brainstorming`](https://github.com/obra/superpowers/tree/main/skills/brainstorming) 工作流里的一个思路。
- `tdd` 借鉴了 Matt Pocock 的 [`tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)。
- `debug` 借鉴了 Matt Pocock 的 [`diagnosing-bugs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs)、Superpowers 的 [`systematic-debugging`](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging)，以及 Waza 的 [`hunt`](https://github.com/tw93/Waza/tree/main/skills/hunt)，但刻意将这些方法简化为一个更小的、由证据驱动的核心流程。
- `review-feedback` 最初借鉴了 Superpowers 的 [`receiving-code-review`](https://github.com/obra/superpowers/tree/main/skills/receiving-code-review)，后来围绕证据、职责归属、范围和系统成本进行了大幅重写，目前已经有明显差异。

上述项目仍是其各自 skills 的权威来源。本仓库收录的是我自己的改写版本，不是对外部 skill 的直接复制。英文 `SKILL.md` 是 Astro Skills 的权威指令版本。

## 许可

MIT
