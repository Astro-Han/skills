"""Predeclared PR-review evaluation cases and report-level answer keys."""


PR_REVIEW_CASES = {
    "review-value-mismatch": {
        "fixture": "prreview-mismatch",
        "prompt": (
            "Review the pull request represented by PR_SNAPSHOT.md and PATCH.diff. "
            "Decide whether to Approve, Comment, Wait, or require human confirmation. "
            "Do not modify files or contact anyone."
        ),
        "should_trigger": True,
        "pr_url": "https://example.test/pulls/84",
        "issue_url": "https://example.test/issues/79",
        "head": "84ca11ab",
        "diff_terms": ("42 additions", "9 deletions"),
        "diff_counts": (42, 9),
        "split_counts": (14, 5, 24, 2),
        "problem_terms": ("mismatch", "does not cover", "different scenario", "错位", "不匹配", "不覆盖", "实际路径"),
        "solution_terms": ("containment root", "discovery root", "symlink", "realpath", "链接"),
        "required_term_groups": (
            ("outside the configured discovery root", "cross-root", "outside-root", "root 外", "跨 root", "外部 target"),
            ("inside the configured discovery root", "inside-root", "root 内", "内部 target"),
        ),
        "decision_terms": ("comment", "wait"),
        "forbid_approve": True,
    },
    "review-production-composition": {
        "fixture": "prreview-composition",
        "prompt": (
            "Review the pull request represented by PR_SNAPSHOT.md, PATCH.diff, and "
            "PRODUCTION_COMPOSITION.md. Recommend the next review action. Do not modify "
            "files or contact anyone."
        ),
        "should_trigger": True,
        "pr_url": "https://example.test/pulls/112",
        "issue_url": "https://example.test/issues/109",
        "head": "1120cafe",
        "diff_terms": ("31 additions", "6 deletions"),
        "diff_counts": (31, 6),
        "split_counts": (15, 6, 16, 0),
        "problem_terms": ("demonstrated", "reproduc", "orphan", "已证明", "已证实", "孤儿"),
        "solution_terms": ("owned launcher", "production", "fixture"),
        "required_term_groups": (
            ("launch_owned", "owned launcher"),
            ("detached fixture", "helper directly", "fixture bypass", "directly calling", "rather than calling", "直接调用", "只覆盖", "未覆盖真实"),
        ),
        "decision_terms": ("comment",),
        "severity": "P1",
        "reach_terms": ("reasonable failure", "recovery", "category 2", "类别 2", "第 2 类", "②", "故障", "恢复"),
        "forbid_approve": True,
    },
    "review-severity-calibration": {
        "fixture": "prreview-severity",
        "prompt": (
            "Review the pull request represented by PR_SNAPSHOT.md and PATCH.diff. "
            "Pay particular attention to the existing reviewer's severity claim and "
            "recommend the next action. Do not modify files or contact anyone."
        ),
        "should_trigger": True,
        "pr_url": "https://example.test/pulls/203",
        "issue_url": "https://example.test/issues/198",
        "head": "203decaf",
        "diff_terms": ("18 additions", "4 deletions"),
        "diff_counts": (18, 4),
        "split_counts": (5, 2, 13, 2),
        "problem_terms": ("demonstrated", "stale", "preview"),
        "solution_terms": ("retry", "refresh", "cache"),
        "decision_terms": ("comment", "approve"),
        "severity": "P2",
        "reach_terms": ("normal user", "正常用户", "category 1", "类别 1", "第 1 类", "①"),
        "forbid_p1": True,
    },
    "status-only-close-non-trigger": {
        "fixture": "prreview-status",
        "prompt": (
            "From PR_SNAPSHOT.md, report only the exact head SHA and current CI results. "
            "Do not review the change, inspect the patch, or recommend an action."
        ),
        "should_trigger": False,
        "head": "77bada55",
        "status_pairs": (("unit", "success"), ("package", "pending")),
    },
    "feedback-summary-close-non-trigger": {
        "fixture": "prreview-feedback-summary",
        "prompt": (
            "Summarize only the three existing reviewer comments in PR_SNAPSHOT.md for "
            "my stand-up. Do not perform a new review, inspect correctness, assign severity, "
            "or recommend an action."
        ),
        "should_trigger": False,
        "head": "512cab00",
        "status_pairs": (("aria", "null"), ("ben", "命名"), ("chen", "截图")),
        "require_head": False,
    },
    "review-process-race-minimum": {
        "fixture": "prreview-process-race",
        "prompt": (
            "Review the pull request represented by PR_SNAPSHOT.md and PATCH.diff. "
            "Recommend the next review action. Do not modify files or contact anyone."
        ),
        "should_trigger": True,
        "pr_url": "https://example.test/pulls/401",
        "issue_url": "https://example.test/issues/397",
        "head": "401a11ce",
        "diff_terms": ("27 additions", "3 deletions"),
        "diff_counts": (27, 3),
        "split_counts": (12, 3, 15, 0),
        "problem_terms": ("demonstrated", "race", "orphan", "reproduced"),
        "solution_terms": ("ownedhostsupervisor", "lease", "process"),
        "required_term_groups": (
            ("process-level test", "subprocess regression", "real process", "跨进程", "真实 launcher/worker"),
            ("necessary", "required", "必要"),
            ("single owner", "one owner", "no new authority", "单一 owner", "唯一 owner", "现有生命周期 owner", "没有引入并行 owner"),
        ),
        "decision_terms": ("approve",),
        "required_recommendation": "approve",
    },
    "review-parallel-authority-ux": {
        "fixture": "prreview-parallel-authority",
        "prompt": (
            "Review the pull request represented by PR_SNAPSHOT.md and PATCH.diff. "
            "Recommend the next review action. Do not modify files or contact anyone."
        ),
        "should_trigger": True,
        "pr_url": "https://example.test/pulls/420",
        "issue_url": "https://example.test/issues/418",
        "head": "420f00d1",
        "diff_terms": ("96 additions", "11 deletions"),
        "diff_counts": (96, 11),
        "split_counts": (70, 8, 26, 3),
        "problem_terms": ("demonstrated", "stalled", "send"),
        "solution_terms": ("host queue", "runtime loop", "ui loop", "authority"),
        "required_term_groups": (
            ("parallel authority", "second authority", "duplicate authority", "并行 authority", "第二 authority", "双重 authority", "第二个恢复循环", "两个恢复 authority", "host queue authority 重叠"),
            ("non-atomic", "not atomic", "stop then send", "stop→send", "非原子", "原子边界"),
            ("queue", "queued content"),
            ("manual acceptance", "human confirmation", "ux confirmation"),
        ),
        "decision_terms": ("human confirmation required",),
        "required_recommendation": "human confirmation required",
        "severity": "P1",
        "reach_terms": ("reasonable failure", "recovery", "category 2", "类别 2", "第 2 类", "②", "故障", "恢复"),
        "forbid_approve": True,
    },
    "review-low-value-test-matrix": {
        "fixture": "prreview-test-matrix",
        "prompt": (
            "Review the pull request represented by PR_SNAPSHOT.md and PATCH.diff. "
            "Recommend the next review action. Do not modify files or contact anyone."
        ),
        "should_trigger": True,
        "pr_url": "https://example.test/pulls/433",
        "issue_url": "https://example.test/issues/430",
        "head": "4337e570",
        "diff_terms": ("196 additions", "5 deletions"),
        "diff_counts": (196, 5),
        "split_counts": (12, 5, 184, 0),
        "problem_terms": ("demonstrated", "mixed-case", "canonical"),
        "solution_terms": ("canonicalizer", "matrix", "boundary"),
        "required_term_groups": (
            ("low-value matrix", "redundant matrix", "test matrix", "低价值", "冗余矩阵", "测试矩阵"),
            ("three", "3"),
            ("remove", "delete", "collapse", "移除", "删除", "精简", "收缩"),
        ),
        "decision_terms": ("comment",),
        "severity": "P3",
        "forbid_approve": True,
    },
    "review-unverified-value": {
        "fixture": "prreview-unverified-value",
        "prompt": (
            "Review the pull request represented by PR_SNAPSHOT.md and PATCH.diff. "
            "Recommend the next review action. Do not modify files or contact anyone."
        ),
        "should_trigger": True,
        "pr_url": "https://example.test/pulls/451",
        "issue_url": "https://example.test/issues/448",
        "head": "4510beef",
        "diff_terms": ("37 additions", "2 deletions"),
        "diff_counts": (37, 2),
        "split_counts": (21, 2, 16, 0),
        "problem_terms": ("plausible but unverified", "unverified", "no reproduction"),
        "solution_terms": ("fallback", "resolver", "test"),
        "required_term_groups": (
            ("no user report", "no reproduction", "no observed failure", "user report", "没有用户报告", "无用户报告", "没有复现", "缺少独立"),
            ("test does not prove", "test proves neither", "test does not independently", "new test", "测试不能证明", "测试并不能", "不能证明修复", "自证式测试"),
        ),
        "decision_terms": ("comment", "wait"),
        "forbid_approve": True,
    },
    "review-contrived-security": {
        "fixture": "prreview-contrived-security",
        "prompt": (
            "Review the pull request represented by PR_SNAPSHOT.md and PATCH.diff. "
            "Pay particular attention to the existing P1 security claim and recommend "
            "the next action. Do not modify files or contact anyone."
        ),
        "should_trigger": True,
        "pr_url": "https://example.test/pulls/470",
        "issue_url": "https://example.test/issues/468",
        "head": "4705afe0",
        "diff_terms": ("9 additions", "8 deletions"),
        "diff_counts": (9, 8),
        "split_counts": (5, 5, 4, 3),
        "problem_terms": ("contrived", "unsupported", "disproved", "unverified"),
        "solution_terms": ("debug", "symlink", "log"),
        "required_term_groups": (
            ("category 4", "contrived path", "第 4 类", "类别 4", "④", "构造路径"),
        ),
        "decision_terms": ("comment", "wait"),
        "forbid_p1": True,
        "forbid_approve": True,
    },
    "review-live-compatibility-holdout": {
        "fixture": "prreview-compatibility",
        "prompt": (
            "Review the pull request represented by PR_SNAPSHOT.md and PATCH.diff. "
            "Recommend the next review action. Do not modify files or contact anyone."
        ),
        "should_trigger": True,
        "pr_url": "https://example.test/pulls/318",
        "issue_url": "https://example.test/issues/315",
        "head": "318feed0",
        "diff_terms": ("24 additions", "37 deletions"),
        "diff_counts": (24, 37),
        "split_counts": (14, 30, 10, 7),
        "problem_terms": ("demonstrated", "rotation", "credential", "已证明", "已证实", "轮换", "凭据"),
        "solution_terms": ("rolling", "legacy_token", "compatibility"),
        "required_term_groups": (
            ("preserve", "retain", "keep", "保留", "不能删除"),
            ("obligation", "contract", "rolling-upgrade window", "义务", "契约", "滚动升级窗口"),
        ),
        "decision_terms": ("comment",),
        "severity": "P1",
        "reach_terms": ("normal user", "正常用户", "normal deployment", "category 1", "类别 1", "第 1 类", "正常部署", "①"),
        "forbid_approve": True,
    },
    "review-durable-ledger-holdout": {
        "fixture": "prreview-durable-ledger",
        "prompt": (
            "Review the pull request represented by PR_SNAPSHOT.md and PATCH.diff. "
            "Recommend the next review action. Do not modify files or contact anyone."
        ),
        "should_trigger": True,
        "pr_url": "https://example.test/pulls/489",
        "issue_url": "https://example.test/issues/486",
        "head": "4891ed90",
        "diff_terms": ("18 additions", "46 deletions"),
        "diff_counts": (18, 46),
        "split_counts": (12, 39, 6, 7),
        "problem_terms": ("demonstrated", "duplicate", "restart", "replay"),
        "solution_terms": ("ledger", "in-memory", "durable", "authority"),
        "required_term_groups": (
            ("persisted ledger", "durable ledger", "durable authority", "持久化 ledger", "持久化 authority", "持久 authority"),
            ("in-memory", "memory-only", "内存", "进程内"),
            ("restart", "recovery", "replay", "重启", "恢复", "重放"),
            ("preserve", "retain", "restore", "保留", "恢复"),
        ),
        "decision_terms": ("comment",),
        "severity": "P1",
        "reach_terms": ("recovery", "category 2", "类别 2", "第 2 类", "②", "恢复"),
        "forbid_approve": True,
    },
}


DESIGN_CASES = (
    "review-value-mismatch",
    "review-production-composition",
    "review-severity-calibration",
    "review-process-race-minimum",
    "review-parallel-authority-ux",
    "review-low-value-test-matrix",
    "review-unverified-value",
    "review-contrived-security",
    "status-only-close-non-trigger",
    "feedback-summary-close-non-trigger",
)
HOLDOUT_CASES = (
    "review-live-compatibility-holdout",
    "review-durable-ledger-holdout",
)
