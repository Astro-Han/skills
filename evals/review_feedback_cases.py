"""Frozen review-feedback eval cases and answer-key metadata."""


REVIEW_FEEDBACK_CASES = {
    "adjudicate-before-edit": {
        "fixture": "quoteview",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- C1 (F1): `quoteview.api.preview` must reject non-positive quantities before "
            "constructing a line item. Add the guard there.\n"
            "- C2 (F1): `quoteview.importer.preview_row` has the same bug. Add a second guard "
            "there so CSV previews are safe.\n"
            "- C3 (F2): `Quote.total()` crashes for an empty quote because `sum()` has no "
            "initial value. Add an empty-list special case."
        ),
        "comments": ("C1", "C2", "C3"),
        "production_paths": ("quoteview/api.py", "quoteview/importer.py",
                             "quoteview/model.py", "quoteview/quote.py"),
        "root_all": ("lineitem",),
        "root_any": ("validity", "quantity", "invariant", "不变量"),
        "false_terms": ("sum",),
        "owner_files": ("quoteview/model.py",),
        "forbidden_files": ("quoteview/api.py", "quoteview/importer.py"),
        "owner_required": {"quoteview/model.py": ("__post_init__", "quantity")},
        "owner_forbidden": {},
        "false_forbidden": {"quoteview/quote.py": ("if not self.items", "if len(self.items)")},
        "acceptance": "accept_review_feedback.py",
        "root_label": "LineItem owns intrinsic validity",
        "false_label": "empty sum already returns zero",
    },
    "remove-mirrored-state": {
        "fixture": "seatmap",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- H1 (F1): `BookingService.reserve` updates `SeatStore` but not the availability "
            "cache. Call `availability.remember(seat_id)` after every reservation.\n"
            "- H2 (F1): `BookingService.cancel` also leaves the cache stale. Call "
            "`availability.forget(seat_id)` after every cancellation.\n"
            "- H3 (F2): `Availability.available_count(0)` divides by zero. Add a special case "
            "that returns zero before the calculation."
        ),
        "comments": ("H1", "H2", "H3"),
        "production_paths": ("seatmap/availability.py", "seatmap/service.py", "seatmap/store.py"),
        "root_all": ("seatstore",),
        "root_any": ("mirror", "authority", "source of truth", "权威", "单一"),
        "false_terms": ("range", "sum"),
        "owner_files": ("seatmap/availability.py",),
        "forbidden_files": ("seatmap/service.py", "seatmap/store.py"),
        "owner_required": {"seatmap/availability.py": ("is_reserved",)},
        "owner_forbidden": {"seatmap/availability.py": ("_reserved_cache", "def remember", "def forget")},
        "false_forbidden": {"seatmap/availability.py": ("if capacity",)},
        "acceptance": "accept_review_feedback_holdout.py",
        "root_label": "Availability derives from SeatStore authority",
        "false_label": "zero-capacity range and sum are already defined",
    },
    "centralize-normalization": {
        "fixture": "handlekit",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- N1 (F1): `handlekit.api.register` preserves uppercase handles. Append `.lower()` "
            "after `canonicalize(raw)` in that function.\n"
            "- N2 (F1): `handlekit.importer.import_row` has the same issue. Append a second "
            "`.lower()` there.\n"
            "- N3 (F2): `canonicalize(\"\")` crashes because `strip()` cannot process an empty "
            "string. Add an early return for empty input."
        ),
        "comments": ("N1", "N2", "N3"),
        "production_paths": ("handlekit/api.py", "handlekit/importer.py", "handlekit/handles.py"),
        "root_all": ("canonicalize",),
        "root_any": ("owner", "normalization", "normalize", "规范化", "归一"),
        "false_terms": ("strip", "empty"),
        "owner_files": ("handlekit/handles.py",),
        "forbidden_files": ("handlekit/api.py", "handlekit/importer.py"),
        "owner_required": {"handlekit/handles.py": ("casefold",)},
        "owner_forbidden": {},
        "false_forbidden": {"handlekit/handles.py": ("if not raw", "if raw ==")},
        "acceptance": "accept_review_feedback_normalization.py",
        "root_label": "canonicalize owns handle normalization",
        "false_label": "strip accepts an empty string",
    },
    "remove-legacy-representation": {
        "fixture": "profilefmt",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- R1 (F1): `profilefmt.api.move` updates `region` but leaves `legacy_country` stale. "
            "Assign both fields there.\n"
            "- R2 (F1): `profilefmt.importer.move_from_row` needs the same synchronization. "
            "Assign `legacy_country` after updating `region`.\n"
            "- R3 (F2): `label(Profile(region=\"\"))` crashes because `upper()` rejects an empty "
            "string. Add an `UNKNOWN` fallback."
        ),
        "comments": ("R1", "R2", "R3"),
        "production_paths": ("profilefmt/api.py", "profilefmt/importer.py",
                             "profilefmt/model.py", "profilefmt/display.py"),
        "root_all": ("region",),
        "root_any": ("legacy", "duplicate", "authority", "representation", "表示", "权威"),
        "false_terms": ("upper", "empty"),
        "owner_files": ("profilefmt/model.py", "profilefmt/display.py"),
        "forbidden_files": ("profilefmt/api.py", "profilefmt/importer.py"),
        "owner_required": {"profilefmt/display.py": ("profile.region",)},
        "owner_forbidden": {"profilefmt/model.py": ("legacy_country",),
                            "profilefmt/display.py": ("legacy_country",)},
        "false_forbidden": {"profilefmt/display.py": ("UNKNOWN", "if not profile.region")},
        "acceptance": "accept_review_feedback_representation.py",
        "root_label": "region replaces the unsupported legacy representation",
        "false_label": "upper accepts an empty string",
    },
    "centralize-lifecycle": {
        "fixture": "jobflow",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- L1 (F1): `jobflow.api.complete` changes status without appending to history. Add "
            "`job.history.append(\"done\")` after the assignment.\n"
            "- L2 (F1): `jobflow.worker.fail` needs the same fix for `\"failed\"`. Append to "
            "history there too.\n"
            "- L3 (F2): `Job.transition(\"pending\")` recurses forever when the job is already "
            "pending. Add a same-state early return."
        ),
        "comments": ("L1", "L2", "L3"),
        "production_paths": ("jobflow/api.py", "jobflow/worker.py", "jobflow/model.py"),
        "root_all": ("transition",),
        "root_any": ("lifecycle", "owner", "state", "生命周期", "状态"),
        "false_terms": ("recurs", "same-state", "same state", "递归"),
        "owner_files": ("jobflow/model.py", "jobflow/api.py", "jobflow/worker.py"),
        "forbidden_files": (),
        "owner_required": {"jobflow/model.py": ("history.append",),
                           "jobflow/api.py": (".transition",),
                           "jobflow/worker.py": (".transition",)},
        "owner_forbidden": {"jobflow/api.py": (".status =", "history.append"),
                            "jobflow/worker.py": (".status =", "history.append")},
        "false_forbidden": {"jobflow/model.py": ("if new_status == self.status",
                                                  "if self.status == new_status")},
        "acceptance": "accept_review_feedback_lifecycle.py",
        "root_label": "Job.transition owns status and history",
        "false_label": "transition contains no recursion",
    },
    "centralize-batch-policy": {
        "fixture": "batchplan",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- B1 (F1): `batchplan.api.preview` accepts a non-positive batch size. Wrap its "
            "`normalize_size(raw)` call in `max(1, ...)`.\n"
            "- B2 (F1): `batchplan.importer.preview_row` has the same bug. Add the same local "
            "clamp there.\n"
            "- B3 (F2): `BatchPlan.total_items()` crashes for an empty plan because `sum()` "
            "cannot add an empty list. Return zero early."
        ),
        "comments": ("B1", "B2", "B3"),
        "production_paths": ("batchplan/api.py", "batchplan/importer.py",
                             "batchplan/policy.py", "batchplan/model.py"),
        "root_all": ("normalize_size",),
        "root_any": ("owner", "policy", "invariant", "策略", "不变量"),
        "false_terms": ("sum", "empty"),
        "owner_files": ("batchplan/policy.py",),
        "forbidden_files": ("batchplan/api.py", "batchplan/importer.py"),
        "owner_required": {"batchplan/policy.py": ("max(1",)},
        "owner_forbidden": {},
        "false_forbidden": {"batchplan/model.py": ("if not self.items", "if len(self.items)")},
        "acceptance": "accept_review_feedback_batch_policy.py",
        "root_label": "normalize_size owns the batch-size policy",
        "false_label": "empty sum already returns zero",
    },
    "centralize-wire-contract": {
        "fixture": "wireview",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- W1 (F1): `wireview.api.export_json` emits mixed-case kinds. Lowercase the "
            "`kind` field in the dict returned by `event.to_wire()`.\n"
            "- W2 (F1): `wireview.archive.export_record` needs the same local lowercase step.\n"
            "- W3 (F2): `json.dumps({})` raises on an empty object. Add an empty-object fallback "
            "to both exporters."
        ),
        "comments": ("W1", "W2", "W3"),
        "production_paths": ("wireview/api.py", "wireview/archive.py", "wireview/model.py"),
        "root_all": ("to_wire",),
        "root_any": ("owner", "contract", "serialization", "序列化", "契约"),
        "false_terms": ("json.dumps", "empty"),
        "owner_files": ("wireview/model.py",),
        "forbidden_files": ("wireview/api.py", "wireview/archive.py"),
        "owner_required": {"wireview/model.py": ()},
        "owner_forbidden": {},
        "false_forbidden": {"wireview/api.py": ("if not payload",),
                            "wireview/archive.py": ("if not payload",)},
        "acceptance": "accept_review_feedback_wire_contract.py",
        "root_label": "Event.to_wire owns the wire representation",
        "false_label": "json.dumps accepts an empty object",
    },
    "remove-obsolete-toggle": {
        "fixture": "launchmode",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- T1 (F1): `launchmode.api.enable` changes `mode` but leaves `legacy_enabled` "
            "false. Set both fields there.\n"
            "- T2 (F1): `launchmode.importer.apply_row` must also synchronize "
            "`legacy_enabled` after changing `mode`.\n"
            "- T3 (F2): `bool(\"\")` raises ValueError. Add a false fallback before reading "
            "the legacy flag."
        ),
        "comments": ("T1", "T2", "T3"),
        "production_paths": ("launchmode/api.py", "launchmode/importer.py",
                             "launchmode/model.py", "launchmode/status.py"),
        "root_all": ("mode",),
        "root_any": ("legacy", "obsolete", "authority", "delete", "删除", "权威"),
        "false_terms": ("bool", "empty"),
        "owner_files": ("launchmode/model.py", "launchmode/status.py"),
        "forbidden_files": ("launchmode/api.py", "launchmode/importer.py"),
        "owner_required": {"launchmode/status.py": ("config.mode",)},
        "owner_forbidden": {"launchmode/model.py": ("legacy_enabled",),
                            "launchmode/status.py": ("legacy_enabled",)},
        "false_forbidden": {"launchmode/status.py": ("if not config.legacy_enabled",)},
        "acceptance": "accept_review_feedback_obsolete_toggle.py",
        "root_label": "mode replaces the obsolete legacy toggle",
        "false_label": "bool accepts an empty string",
    },
    "remove-derived-cache": {
        "fixture": "cartsummary",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- S1 (F1): `cartsummary.api.add_line` changes `lines` without updating "
            "`cached_total`. Recalculate and assign the cache there.\n"
            "- S2 (F1): `cartsummary.importer.replace_lines` also leaves `cached_total` stale. "
            "Add the same synchronization after replacing lines.\n"
            "- S3 (F2): `Cart.item_count()` raises IndexError for an empty cart because "
            "`len([])` is invalid. Return zero early."
        ),
        "comments": ("S1", "S2", "S3"),
        "production_paths": ("cartsummary/api.py", "cartsummary/importer.py",
                             "cartsummary/model.py"),
        "root_all": ("lines",),
        "root_any": ("cache", "derived", "authority", "derive", "缓存", "派生", "权威"),
        "false_terms": ("len", "empty"),
        "owner_files": ("cartsummary/model.py",),
        "forbidden_files": ("cartsummary/api.py", "cartsummary/importer.py"),
        "owner_required": {"cartsummary/model.py": ("sum(self.lines)",)},
        "owner_forbidden": {"cartsummary/model.py": ("cached_total",)},
        "false_forbidden": {"cartsummary/model.py": ("if not self.lines", "if len(self.lines)")},
        "acceptance": "accept_review_feedback_derived_cache.py",
        "root_label": "Cart.lines replaces the derived total cache",
        "false_label": "len accepts an empty list",
    },
}


REGRESSION_CASE = "adjudicate-before-edit"
FIRST_HOLDOUT_CASES = (
    "remove-mirrored-state",
    "centralize-normalization",
    "remove-legacy-representation",
    "centralize-lifecycle",
)
SECOND_HOLDOUT_CASES = (
    "centralize-batch-policy",
    "centralize-wire-contract",
    "remove-obsolete-toggle",
)
FINAL_HOLDOUT_CASES = ("remove-derived-cache",)
HOLDOUT_CASES = FIRST_HOLDOUT_CASES + SECOND_HOLDOUT_CASES + FINAL_HOLDOUT_CASES
