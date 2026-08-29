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
        "problem_terms": ("mismatch", "does not cover", "different scenario", "错位", "不匹配", "不覆盖", "实际路径"),
        "solution_terms": ("containment root", "discovery root", "symlink", "realpath", "链接"),
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
        "problem_terms": ("demonstrated", "reproduc", "orphan", "已证明", "已证实", "孤儿"),
        "solution_terms": ("owned launcher", "production", "fixture"),
        "decision_terms": ("comment",),
        "severity": "P1",
        "reach_terms": ("reasonable failure", "recovery", "category 2", "类别 2", "②"),
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
        "problem_terms": ("demonstrated", "stale", "preview"),
        "solution_terms": ("retry", "refresh", "cache"),
        "decision_terms": ("comment",),
        "severity": "P2",
        "reach_terms": ("normal user", "正常用户", "category 1", "类别 1", "①"),
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
        "problem_terms": ("demonstrated", "rotation", "credential", "已证明", "已证实", "轮换", "凭据"),
        "solution_terms": ("rolling", "legacy_token", "compatibility"),
        "decision_terms": ("comment",),
        "severity": "P1",
        "reach_terms": ("normal user", "正常用户", "normal deployment", "category 1", "类别 1", "正常部署", "①"),
        "forbid_approve": True,
    },
}


DESIGN_CASES = (
    "review-value-mismatch",
    "review-production-composition",
    "review-severity-calibration",
    "status-only-close-non-trigger",
)
HOLDOUT_CASES = ("review-live-compatibility-holdout",)
