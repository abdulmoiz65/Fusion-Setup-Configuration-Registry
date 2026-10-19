# Value Set Value Design Enforcement

## Mandatory Gates

| Gate | Block When | Fix |
|---|---|---|
| FBDI-only mutation | A Value Sets POST/PATCH, FSM import, or manual per-row write is planned | Route all requested rows through one values-only FBDI package and `core/data-loader` |
| Value-set existence | Parent GET doesn't return exactly one case-sensitive ValueSetCode match | Correct the code or resolve catalog/access ambiguity before package work |
| Maximum length | Resolved parent MaximumLength is missing, nonnumeric, or outside 1-150 | Resolve the metadata mismatch; never guess or default it |
| Image fidelity | Required image cells are unreadable or ambiguous | Ask for exact cells or a CSV/ZIP |
| Summary-value qualifiers | SummaryFlag is Y and either AllowPostingFlag or AllowBudgetingFlag is Y on the same row | Reject the complete batch and require both Allow Posting and Allow Budgeting to be N |
| Complete batch | Any row fails static or FBDI-shape validation | Correct all rows before generation |
| Package structure | Row width isn't 101 or ZIP member set differs | Regenerate by following `ora_fbdi_processing.md` |
| Values-only scope | Hierarchy rows/member are present | Remove them and use the hierarchy task separately |
| Execution intent | File was only attached without create/update/import instruction | Return preview only |
| Data Loader route | `core.data-loader` can't complete its gates or return an execution result | Stop and report the blocking component; don't bypass the route |
| Data Loader result | Data Loader reports an incomplete, timed-out, failed, or uncertain outcome | Report the returned outcome and primary request ID when present; don't launch supplemental status or verification calls and don't retry automatically |

## Rule Ownership

| Rules | Markdown Authority | Timing |
|---|---|---|
| MVS.002-MVS.006 and MVS.010-MVS.023 | `ora_input_validation.md` and `ora_fbdi_processing.md` | Before package generation |
| ZIP safety | `ora_bulk_intake.md` and `ora_fbdi_processing.md` | During intake and generation |

## Boundaries

- Don't mutate the parent Value Sets resource or use child Values REST.
- Don't query values to determine whether requested rows already exist.
- Don't query values to classify Natural Account usage.
- Don't invoke FSM import/export or task-level setup export anywhere in this task.
- Don't bypass `core.data-loader`.
- Don't submit an unverified or changed-after-preview ZIP.
- Don't launch separate status, process-tree, child-job, LOG, OUT, or post-handoff Values REST requests.
- Don't claim created, updated, unchanged, or rejected row counts unless Data Loader returns them.
- Don't claim rollback for rows already imported.
