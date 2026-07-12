# Astro Skills

这是我日常使用的一组 Agent Skills，用来让编码 Agent 更认真地推理、依据证据行动，并把工作真正收尾。

它不是提示词合集，也不追求覆盖所有工作流。每个 skill 都来自一个仅靠普通提示仍会反复出现的问题：尚未确认关键决策就开始实现、没有证明根因就修补症状、先写实现再补测试、不经验证地服从 review 意见，或在会话结束时留下未处理的现场。

这些 skills 刻意保持精简，只保留经过反复使用证明有价值的行为约束。复杂 skill 会尽量用较弱模型验证，让效果来自 skill 本身，而不只是基础模型能力。

## Skills

| Skill | 解决的问题 |
| --- | --- |
| [`learn-anything`](skills/learn-anything/) | 通过自适应教学和主动回忆建立可用、持久的理解。 |
| [`shape`](skills/shape/) | 实现前逐项确认真正属于用户的关键决策。 |
| [`debug`](skills/debug/) | 复现故障、隔离根因，并回到原始场景验证。 |
| [`tdd`](skills/tdd/) | 通过可靠的红—绿—重构循环改变生产行为。 |
| [`review-feedback`](skills/review-feedback/) | 在接受或拒绝 review 意见前先用证据验证。 |
| [`wrap-up`](skills/wrap-up/) | 结束会话时清理本次工作留下的未完成事项。 |

## 安装

安装全部 skills：

```bash
npx skills add Astro-Han/skills
```

安装单个 skill：

```bash
npx skills add Astro-Han/skills --skill debug
```

支持的 Agent 与其他参数见 [Skills CLI 文档](https://skills.sh/docs)。

## 设计原则

- 从 Agent 真实、反复出现的失败出发。
- 明确 skill 应该触发和不该触发的场景。
- 只添加模型无法稳定自行推断的指令。
- 用证据和可观察结果替代流程仪式。
- 条件允许时，用较弱模型验证要求较高的 skill。
- 外部 skill 保留在原始来源，不复制进本仓库。

英文 `SKILL.md` 是 Agent 指令的权威版本。

## 许可

MIT
