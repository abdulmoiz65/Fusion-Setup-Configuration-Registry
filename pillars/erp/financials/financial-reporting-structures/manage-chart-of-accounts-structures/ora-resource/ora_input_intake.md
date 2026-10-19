# Input Intake

## Accepted Input Formats

| Input Format | What Must Be Provided | Applies To |
|---|---|---|
| Approved COA design plus complete same-task FSM export | Business identifiers, requested definitions, populated CSV files, and ASM_SETUP_CSV_METADATA.xml | Structures |
| Template-only FSM export | File-shape supplement only after the complete export | Structures |
| Previously exported complete FSM ZIP | Place the unchanged ZIP under project/{project_id}/exports/financials/financial-reporting-structures/manage-chart-of-accounts-structures/baselines/ and provide its path | Structures |
| Vague create request | COA name, confirmation or revision of the proposed Company, Cost Center, Account, and Intercompany baseline, and any additional user-designed segments | Structures |
| Configuration-only request | Explicit COA Name or StructureCode identifying the chart of accounts that owns the configuration | Structures |
| Approved COA design with verified value-set references | COA identity, requested segments, and one verified ValueSetCode with compatible metadata for every segment | Structures |

## Body Field Rules

| Situation | What Happens |
|---|---|
| User asks to create or add a chart of accounts without structural details | Present Company as Primary Balancing, Cost Center as Cost Center, Account as Natural Account, and Intercompany as Intercompany as the basic proposed segment set. Ask for the COA name, confirmation or revision of this set, and any additional segments. Do not create artifacts or start setup activity until the user responds. |
| User supplies some COA configuration but does not identify a chart of accounts | Ask which COA the configuration belongs to. Do not derive COA Name or StructureCode from segment names, value-set codes, configuration values, files, environment context, or a previously discussed COA. |
| User confirms the basic segment set | Use only the confirmed baseline plus additional segments explicitly supplied by the user. Do not infer, invent, reserve, or append other segments. |
| User supplies a segment without a ValueSetCode | Derive SegmentCode_VS only as a read-only lookup candidate. An absent match is not a user-clarification or separate creation-approval request; do not populate DefaultValueSetCode or create a structure package until compatible value-set evidence is available. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COASTR.COLLECT | step | 1 | collect_input | valid->COASTR.VALIDATE | none | stop | Always |
