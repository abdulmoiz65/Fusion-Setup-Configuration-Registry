# Input Intake

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Approved COA design plus complete same-task FSM export | Business identifiers, requested definitions, populated CSV files, and ASM_SETUP_CSV_METADATA.xml | Value sets |
| Template-only FSM export | File-shape supplement only after the complete export | Value sets |
| Previously exported complete FSM ZIP | Place the unchanged ZIP under project/{project_id}/exports/financials/financial-reporting-structures/manage-chart-of-accounts-value-sets/baselines/ and provide its path | Value sets |
| Approved COA segment design | COA identity; every requested SegmentCode, segment name, business classification, and value length; explicit ValueSetCode when the SegmentCode_VS candidate must not be used | One value-set candidate per requested COA segment |

## Body Field Rules

| Situation | What Happens |
|---|---|
| COA creation supplies segment definitions | Treat every requested segment as a value-set preflight candidate. Derive SegmentCode_VS only as a lookup candidate when ValueSetCode is omitted; do not treat the candidate as an existing value set until lookup verifies it. |
| COA segment has no explicit ValueSetCode | Retain the derived SegmentCode_VS candidate, its requested MaximumLength, and its business classification for validation and lookup. |
| A compatible value set is absent | Continue with the validated candidate's creation readiness. Do not ask for a separate value-set creation confirmation; the COA request already authorizes dependency preparation. |
| COA segment set is incomplete | Stop before value-set package generation; collect the missing SegmentCode, name, classification, or length for all requested segments. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAVS.COLLECT | step | 1 | collect_input | valid->COAVS.VALIDATE | none | stop | Always |
