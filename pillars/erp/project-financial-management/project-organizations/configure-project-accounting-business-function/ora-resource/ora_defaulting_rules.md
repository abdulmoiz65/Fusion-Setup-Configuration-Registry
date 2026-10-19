# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| `ProjEffectiveStartDate`, `ProjEffectiveEndDate`, `ExpEffectiveStartDate`, `ExpEffectiveEndDate` | Empty value | Final package assembly, after all baseline merges and defaults and before package validation, preview, or import | Yes; discard every user-supplied value |  |
| Omitted option group | Preserve current target group | Update omits group | Yes | find_current_bu_options |
| Expenditure hierarchy | Owning hierarchy triple | Explicitly select shared hierarchy: UI `SameAsProjTaskOrg=false` means "Use different details" is unchecked; do not infer polarity from the attribute name | Yes, in working request after resolving owning references; disclose original and resulting expenditure values; no implicit target overwrite | resolve_project_org_hierarchies |
| Business-unit financial context | Existing primary ledger, legal entity, currency, and calendar | Implementation-row creation or calendar/period, costing/conversion, or cross-charge change; otherwise preserve the omitted group without a separate lookup | Yes | resolve_bu_financial_context |
| Relationship omission | Preserve current selected project units | project_units omitted | Yes | resolve_project_unit_relationships |
| Feature-hidden fields | Preserve runtime values | Target feature hides surface | Yes | verify_bu_feature_status |
| Overtime allowed | `N` | Initial setup row | No; value is limited to `Y` or `N` | resolve_costing_references |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BUFUNC.NORMALIZE_EXPORT_ONLY_EFFECTIVE_DATES | step | 16 | apply_default | normalized->BUFUNC.EXECUTION_GATE | BUFUNC.ENFORCE_DESIGN | stop | Final package sanitization before package validation, preview, or import |
| BUFUNC.APPLY_DEFAULTS | step | 3 | apply_default | applied->BUFUNC.FIND_BUSINESS_UNIT;failure->BUFUNC.RETURN_ISSUES | BUFUNC.VALIDATE_INPUT | stop | Valid business-function input |

## UI Behavior Boundaries

In the simplified non-None hierarchy page, unchecking Use different details for project expenditure organization copies the owning tree, version and starting organization into expenditure details and disables separate entry. Checking it enables separate entry without itself clearing or choosing values. While shared details remain selected, changes to owning details synchronize their expenditure counterparts, including a cleared value.

The copy replaces prior explicit expenditure values in the working UI state. Resolve the complete requested hierarchy before FSCR preview; do not mimic intermediate empty selections. Omitted groups preserve current target values. For example, owning Tree A/V1/Org A with expenditure Tree B/V2/Org B and explicit shared details yields expenditure Tree A/V1/Org A in working input, with both triples disclosed. Normalization does not authorize an existing-data write.

Shared details copy the display tree name, version name and start organization into working input. Technical codes still come only from the matching fndTrees REST response, unchanged; the expenditure resolver may reuse the verified response for the identical tree name. This default never derives, normalizes, uppercases or constructs a tree code or tree structure code from a name, and it never obtains a code from a version name.
