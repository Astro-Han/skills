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
    "protect-committed-boundary": {
        "fixture": "transferlog",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- D1 (F3): `transferlog.api.commit` can append a non-positive transfer to the "
            "external ledger. Add an amount guard in that function.\n"
            "- D2 (F3): `transferlog.importer.commit_row` can do the same. Add another guard "
            "before constructing the transfer.\n"
            "- D3 (F2): `Ledger.count()` crashes when empty because `len([])` raises. Return "
            "zero early."
        ),
        "comments": ("D1", "D2", "D3"),
        "production_paths": ("transferlog/api.py", "transferlog/importer.py",
                             "transferlog/model.py", "transferlog/ledger.py"),
        "root_all": ("transfer",),
        "root_any": ("invariant", "owner", "amount", "不变量", "所有者"),
        "false_terms": ("len", "empty"),
        "expected_severity": "P1",
        "owner_files": ("transferlog/model.py",),
        "forbidden_files": ("transferlog/api.py", "transferlog/importer.py"),
        "owner_required": {"transferlog/model.py": ("__post_init__", "amount")},
        "owner_forbidden": {},
        "false_forbidden": {"transferlog/ledger.py": ("if not self.entries",)},
        "acceptance": "accept_review_feedback_committed_boundary.py",
        "root_label": "Transfer owns intrinsic amount validity",
        "false_label": "len accepts an empty list",
    },
    "preserve-live-compatibility": {
        "fixture": "credrotate",
        "prompt": (
            "Use the review-feedback skill at "
            "`.agents/skills/review-feedback-eval/SKILL.md`. We received the review below. "
            "Please address all of it and make the needed changes.\n\n"
            "- K1 (F1): `credrotate.api.rotate` changes `token` without copying the old value "
            "to `legacy_token`. Add both assignments there.\n"
            "- K2 (F1): `credrotate.importer.rotate_row` needs the same two assignments for "
            "rolling-version readers.\n"
            "- K3 (F2): `Credential.active()` raises ValueError for an empty token because "
            "`bool(\"\")` is invalid. Return false early."
        ),
        "comments": ("K1", "K2", "K3"),
        "production_paths": ("credrotate/api.py", "credrotate/importer.py", "credrotate/model.py"),
        "root_all": ("rotate",),
        "root_any": ("compatibility", "owner", "rolling", "兼容", "所有者"),
        "false_terms": ("bool", "empty"),
        "expected_severity": "P2",
        "owner_files": ("credrotate/model.py", "credrotate/api.py", "credrotate/importer.py"),
        "forbidden_files": (),
        "owner_required": {"credrotate/model.py": ("def rotate", "legacy_token"),
                           "credrotate/api.py": (".rotate",),
                           "credrotate/importer.py": (".rotate",)},
        "owner_forbidden": {"credrotate/api.py": (".token =", "legacy_token"),
                            "credrotate/importer.py": (".token =", "legacy_token")},
        "false_forbidden": {"credrotate/model.py": ("if not self.token",)},
        "acceptance": "accept_review_feedback_live_compatibility.py",
        "root_label": "Credential.rotate owns the live compatibility update",
        "false_label": "bool accepts an empty string",
    },
    "rebase-cumulative-diff": {
        "fixture": "mediathread",
        "seed_patch": "mediathread-pr.patch",
        "prompt": (
            "Use the review-feedback skill at "
            "'.agents/skills/review-feedback-eval/SKILL.md'. This is the second review "
            "round for the current PR. The repository root commit is the pre-PR base; "
            "all later commits are the cumulative PR diff, including changes made for "
            "earlier review suggestions. The original PR goal was only to render "
            "current-session 'media://' attachment images, preserve text rendering, and "
            "keep copied-session messages and replay ledger consistent. It did not change "
            "blob export semantics or add remote-image support. Re-evaluate the whole diff, "
            "address the review below, and leave the PR ready to merge.\n\n"
            "- A1 (P1): 'clone_session' rewrites attachment IDs in 'messages' but not in "
            "'ledger', so replay in a copied session still reads the source artifact. "
            "Rewrite both authorities.\n"
            "- A2 (P2): 'ImageLoader' permanently caches a failed read as 'None', so a "
            "transient failure can never recover. Failed reads must be retryable while "
            "successful duplicate reads remain deduplicated.\n"
            "- A3 (P1): The earlier review added a 2 MB preview policy to 'export_blob', "
            "but the policy is only a function. Keep that global transport change and "
            "expand it into a 'BlobPolicy' class so every future blob flow can share it.\n"
            "- A4 (P2): Keep 'ImageSourceRegistry' and register 'https://' now so remote "
            "images can be supported later without another refactor.\n"
            "- A5 (P2): 'render(\"\")' crashes because the Markdown image regex cannot "
            "match an empty string. Add an empty-string special case."
        ),
        "comments": ("A1", "A2", "A3", "A4", "A5"),
        "production_paths": (
            "mediathread/copying.py",
            "mediathread/loader.py",
            "mediathread/policy.py",
            "mediathread/preview.py",
            "mediathread/registry.py",
            "mediathread/transport.py",
        ),
        "acceptance": "accept_review_feedback_scope_rebase.py",
        "kind": "scope_rebase",
    },
    "synthesize-digest-flows": {
        "fixture": "digestflow",
        "prompt": (
            "Use the review-feedback skill at "
            "'.agents/skills/review-feedback-eval/SKILL.md'. We received a large review "
            "of the scheduled digest change below. Please address the feedback and make "
            "the necessary changes.\n\n"
            "- D8 (P1): Migrated tasks inherit the snapshot permission, including `bypass`. "
            "Force `ask` in `migrate_legacy`.\n"
            "- D3 (P2): `report_rows` filters history by the current random task ID, so "
            "deleting and recreating the task hides older reports. Keep a list of old task IDs.\n"
            "- D11 (P2): Bridge v1 silently drops a requested date-range intent. Fall back "
            "to the default range when the bridge is old.\n"
            "- D1 (P1): Released version-1 snapshots use `model_connection`, but migration "
            "rejects every schema except version 2. Add a version-1 branch.\n"
            "- D6 (P2): A running Session with a partial Artifact is shown as a completed "
            "report. Add a state check in `report_rows`.\n"
            "- D4 (P1): Migration appends report Sessions before checking whether the target "
            "can execute; a failed migration leaks interactive projections. Delete the new "
            "Sessions on failure.\n"
            "- D9 (P2): Edited Session revisions are counted as separate activity. Deduplicate "
            "inside `activity_total`.\n"
            "- D2 (P1): `create_task` resolves the connection from `selected_host` but stores "
            "`default_host`, producing an impossible cross-host binding. Copy the selected host.\n"
            "- D12 (P2): `active_conversations` returns only a number, removing the list and "
            "open action. Return the canonical active Session rows instead.\n"
            "- D7 (P2): Retrying migration appends another digest task. Check existing task "
            "titles before appending.\n"
            "- D5 (P1): A persisted active task without a connection raises forever during "
            "recovery. Resolve the only ready connection, otherwise pause it.\n"
            "- D10 (P2): Successful migration never retires the legacy snapshot. Add a "
            "separate tombstone registry so startup can ignore it next time."
        ),
        "comments": tuple("D{}".format(index) for index in range(1, 13)),
        "production_paths": (
            "digestflow/migration.py",
            "digestflow/execution.py",
            "digestflow/projection.py",
            "digestflow/models.py",
        ),
        "production_prefix": "digestflow/",
        "authority_terms": ("retired", "preset", "permission", "authority", "权威"),
        "entropy_forbidden": {
            "digestflow/migration.py": ("tombstone",),
            "digestflow/projection.py": ("old_task_ids", "legacy_task_ids"),
            "digestflow/execution.py": ("default_range", "default_date_range"),
        },
        "acceptance_checks": (
            ("migration flow", "accept_review_feedback_causal_migration.py"),
            ("execution flow and unmentioned sibling", "accept_review_feedback_causal_execution.py"),
            ("projection flow", "accept_review_feedback_causal_projection.py"),
        ),
        "kind": "causal_synthesis",
        "cohort": "design",
    },
    "synthesize-shipment-flows": {
        "fixture": "shipmentflow",
        "prompt": (
            "Use the review-feedback skill at "
            "'.agents/skills/review-feedback-eval/SKILL.md'. Please address this review "
            "of recipient identity and label export.\n\n"
            "- H5 (P1): `export_recipient` drops `legacy_route`, so deployed label scanners "
            "cannot route old-format records. Preserve it in the exported record.\n"
            "- H2 (P2): `add_invitation` compares raw email strings, so a case variant can "
            "invite the same recipient twice. Lowercase locally before the loop.\n"
            "- H7 (P2): `len([])` raises on an empty recipient list. Add an empty-list guard "
            "to `add_invitation`.\n"
            "- H4 (P2): Email and display-name cleanup are both normalization. Replace both "
            "helpers with one shared `normalize_text` that lowercases every value.\n"
            "- H1 (P2): `create_recipient` stores mixed-case email even though email is a "
            "case-insensitive identity. Lowercase it before constructing the object.\n"
            "- H8 (P2): Some locales capitalize family names differently. Expand this change "
            "with a locale-aware name-policy registry.\n"
            "- H3 (P2): `clean_display_name` lowercases user-selected capitalization. Preserve "
            "the case while trimming surrounding whitespace.\n"
            "- H6 (P2): `legacy_route` duplicates the new recipient ID. Delete the field and "
            "make scanners migrate immediately."
        ),
        "comments": tuple("H{}".format(index) for index in range(1, 9)),
        "production_paths": (
            "shipmentflow/identity.py",
            "shipmentflow/compat.py",
            "shipmentflow/models.py",
        ),
        "production_prefix": "shipmentflow/",
        "false_comment": "H7",
        "deferred_comment": "H8",
        "authority_terms": ("email", "display", "legacy_route", "scanner", "authority", "权威"),
        "entropy_forbidden": {
            "shipmentflow/identity.py": ("normalize_text",),
        },
        "acceptance_checks": (
            ("identity, presentation, and compatibility", "accept_review_feedback_causal_holdout.py"),
        ),
        "kind": "causal_synthesis",
        "cohort": "holdout",
    },
    "synthesize-subscription-flows": {
        "fixture": "subscriptionflow",
        "prompt": (
            "Use the review-feedback skill at "
            "'.agents/skills/review-feedback-eval/SKILL.md'. Please address this review "
            "of subscription lifecycle, activity, and renewal compatibility.\n\n"
            "- U6 (P1): `export_subscription` omits `legacy_channel`, so deployed renewal "
            "workers lose their route. Preserve it in the record.\n"
            "- U2 (P2): `cancel_from_row` changes state without history. Append `cancelled` "
            "in that importer function.\n"
            "- U8 (P2): Add a global state-alias registry now so future billing states can "
            "be migrated without another refactor.\n"
            "- U4 (P2): `active_rows` shows superseded active revisions. Pass a list of old "
            "session IDs from every caller and filter them locally.\n"
            "- U1 (P2): `pause` changes state without history. Append `paused` in the API.\n"
            "- U9 (P2): `len([])` raises when there are no sessions. Add empty-list guards "
            "to both activity functions.\n"
            "- U7 (P2): `legacy_channel` duplicates the subscription ID. Delete it and make "
            "renewal workers upgrade immediately.\n"
            "- U3 (P2): `Subscription.transition` recurses forever for a same-state request. "
            "Add a same-state early return.\n"
            "- U5 (P2): `active_total` counts old revisions separately. Deduplicate inside "
            "that function."
        ),
        "comments": tuple("U{}".format(index) for index in range(1, 10)),
        "production_paths": (
            "subscriptionflow/actions.py",
            "subscriptionflow/compat.py",
            "subscriptionflow/models.py",
            "subscriptionflow/projection.py",
        ),
        "production_prefix": "subscriptionflow/",
        "false_comment": "U9",
        "deferred_comment": "U8",
        "authority_terms": (
            "transition", "history", "root_id", "revision", "legacy_channel",
            "authority", "owner", "权威", "所有者",
        ),
        "entropy_forbidden": {
            "subscriptionflow/actions.py": ("history.append",),
            "subscriptionflow/models.py": ("alias_registry", "state_aliases"),
            "subscriptionflow/projection.py": ("old_session_ids",),
        },
        "acceptance_checks": (
            ("lifecycle, latest projection, and renewal compatibility",
             "accept_review_feedback_subscription_holdout.py"),
        ),
        "kind": "causal_synthesis",
        "cohort": "fresh_holdout",
    },
    "synthesize-policy-flows": {
        "fixture": "policyflow",
        "prompt": (
            "Use the review-feedback skill at "
            "'.agents/skills/review-feedback-eval/SKILL.md'. Please address this review "
            "of delivery destinations and export compatibility.\n\n"
            "- P4 (P2): Email and bucket destinations are both identifiers. Replace their "
            "helpers with one `normalize_identifier` that lowercases both.\n"
            "- P1 (P2): `create_email_delivery` stores mixed-case email. Lowercase locally "
            "before constructing the delivery.\n"
            "- P7 (P1): `export_delivery` drops `legacy_route`, which deployed dispatch "
            "scanners still read. Preserve it.\n"
            "- P5 (P2): `clean_label` lowercases user-selected capitalization. Preserve case "
            "while trimming whitespace.\n"
            "- P9 (P2): `len([])` raises for an empty delivery list. Add an empty-list guard "
            "to `find_email_delivery`.\n"
            "- P2 (P2): `find_email_delivery` compares raw email case. Lowercase in that "
            "caller before searching.\n"
            "- P8 (P2): `legacy_route` duplicates destination identity. Delete it and require "
            "all scanners to migrate now.\n"
            "- P3 (P2): Bucket keys that differ only by case should be merged. Keep the "
            "current lowercase behavior and add duplicate rejection.\n"
            "- P10 (P2): Add a locale-aware label-policy registry for future capitalization "
            "rules.\n"
            "- P6 (P2): Replace email, bucket, and label helpers with one `normalize_text` "
            "so every string follows the same policy."
        ),
        "comments": tuple("P{}".format(index) for index in range(1, 11)),
        "production_paths": (
            "policyflow/compat.py",
            "policyflow/intake.py",
            "policyflow/models.py",
            "policyflow/normalization.py",
        ),
        "production_prefix": "policyflow/",
        "false_comment": "P9",
        "deferred_comment": "P10",
        "authority_terms": (
            "email", "bucket", "label", "legacy_route", "scanner", "contract",
            "authority", "owner", "权威", "所有者",
        ),
        "entropy_forbidden": {
            "policyflow/normalization.py": ("normalize_identifier", "normalize_text"),
        },
        "acceptance_checks": (
            ("separate identity, external-key, presentation, and compatibility policies",
             "accept_review_feedback_policy_holdout.py"),
        ),
        "kind": "causal_synthesis",
        "cohort": "fresh_holdout",
    },
}


CAUSAL_SYNTHESIS_DESIGN_CASES = ("synthesize-digest-flows",)
CAUSAL_SYNTHESIS_HOLDOUT_CASES = (
    "synthesize-shipment-flows",
    "synthesize-subscription-flows",
    "synthesize-policy-flows",
)
