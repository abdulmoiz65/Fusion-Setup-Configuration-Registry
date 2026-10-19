# Input Intake

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Approved COA design plus complete same-task FSM export | Business identifiers, requested definitions, populated CSV files, and ASM_SETUP_CSV_METADATA.xml | Structure instances |
| Template-only FSM export | File-shape supplement only after the complete export | Structure instances |
| Previously exported complete FSM ZIP | Place the unchanged ZIP under project/{project_id}/exports/financials/financial-reporting-structures/manage-chart-of-accounts-structure-instances/baselines/ and provide its path | Structure instances |
| Approved COA structure with verified segment value sets | Existing structure identity and, for every inherited or overridden segment, verified ValueSetCode and metadata | Structure instances |

## Body Field Rules

| Situation | What Happens |
|---|---|
| Instance creation or override is requested | Require a verified structure identity and verified inherited or override value-set metadata before collecting instance package rows. |
| An override ValueSetCode is omitted | Use the referenced structure value set only after its metadata has been verified; do not infer a new value-set code. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAINS.COLLECT | step | 1 | collect_input | valid->COAINS.VALIDATE | none | stop | Always |
