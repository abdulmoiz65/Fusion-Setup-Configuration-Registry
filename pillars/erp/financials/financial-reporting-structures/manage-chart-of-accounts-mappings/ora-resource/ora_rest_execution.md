# Execution Contract

This task does not authorize hand-authored direct REST writes. Use the existing shared FDOS export, validation, authentication, FSM client, and import paths. Use the supported FSM task-CSV import contract for mapping headers, segment rules, rollup rules, and account rules; do not treat it as a public direct GL mapping REST endpoint.

## Runtime Sources

| Source | Purpose |
|---|---|
| shared.setup-export.task-level-export | Retrieve same-task setup evidence where supported |
| shared.validation.setup-data-validator | Validate supported setup data and generated artifacts |
| chartOfAccountsLOV | Read-only source and target COA lookup before any export using the documented collection and item paths |
| valueSets and child values | Read-only value-set definition and referenced-value lookup after segment-to-value-set resolution |
| shared.validation.reference-data-validator | Validate charts, segments, values, and hierarchies |
| shared.setup-import.task-level-import | Execute an approved FSM task-CSV import, including export-derived account-rule rows |
| Existing FDOS authentication skills | Supply environment-bound authentication without persisting secrets |
| Core FSM REST client | Shared execution primitive only; no task-local REST contract is invented |
| Same-task FSM CSV export | Establish the current task CSV contract; ORA_GL_AFF_MAP_RULE.csv and ASM_SETUP_CSV_METADATA.xml are required evidence for account-rule import |

## Execution Contract

| Situation | What Happens |
|---|---|
| Read-only discovery | Resolve and compare the current mapping before artifact generation |
| Source or target COA lookup | Use only GET /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV and GET /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV/{StructureInstanceId}; no write path is authorized |
| Value-set lookup | Use GET /fscmRestApi/resources/11.13.18.05/valueSets for an exact ValueSetCode, then follow the returned item link for GET child/values. No value-set write path is authorized by this skill. |
| Header absent | Preview the export-derived FSM task-CSV create action and require explicit approval |
| Header differs | Show field-level and rule-level differences; require update or distinct-name direction |
| Standard segment or single-source rollup import | Use the export-derived FSM task-CSV route after readiness passes unless the user explicitly selects FBDI |
| Multiple-source segment or rollup import | Use the current FBDI route; no public REST endpoint or export-derived FSM multiple-source CSV contract is confirmed |
| Account rule | Do not route through the FBDI workbook. Preview the export-derived FSM task-CSV action with ORA_GL_AFF_MAP_RULE.csv and matching metadata. |
| Update | Reread the mapping immediately before execution and stop on concurrent changes |
| Replace | Require separate explicit approval and complete-replacement proof |
| Delete | Require explicit target confirmation, impact disclosure, and approval |

## Endpoint

| Action | Method | Path |
|---|---|---|
| Resolve source or target COA | GET | /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV |
| Read resolved COA detail | GET | /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV/{StructureInstanceId} |
| Resolve value-set definition | GET | /fscmRestApi/resources/11.13.18.05/valueSets?q=ValueSetCode='{ValueSetCode}' |
| Read value-set values | GET | {returned value-set item link}/child/values |
| Read existing mapping | Supported read-only lookup or export | Manage Chart of Accounts Mappings; no public GL COA Mapping REST endpoint is confirmed |
| Upload FSM task-CSV package | POST through shared import workflow | /fscmRestApi/resources/11.13.18.05/setupTaskCSVImports |
| Upload segment and rollup rules | Shared import workflow | Manage Chart of Accounts Mappings, Actions, Upload Rules |
| Import segment and rollup rules | Shared import workflow | Manage Chart of Accounts Mappings, Actions, Import Rules |
| Import account rules | Shared FSM task-CSV import workflow | ORA_GL_AFF_MAP_RULE.csv in an export-derived setup-task CSV package |
| Review implemented rules | Read-only report | Chart of Accounts Mapping Rules Report |

## Preview Pattern

| Step | Requirement |
|---|---|
| 1 | Show environment, mapping, source and target charts, resolved SecurityFlag, resolved import mode, accounting date, whether each was user-supplied or defaulted, action, and execution route |
| 2 | Show existing-object comparison and concurrent-update baseline |
| 3 | Show rule counts by segment, single-source rollup, multiple-source rollup, and account rule |
| 4 | Show overlap results and the account-rule precedence outcome |
| 5 | Show selected-import-contract evidence, files, mode, unresolved values, and readiness decision; show ORA_GL_AFF_MAP_RULE.csv metadata when account rules are present |
| 5a | Show why FSM or FBDI was selected; disclose FSM availability when an explicit FBDI choice is honored |
| 6 | Show side effects, especially Replace omissions and any create, update, or delete |

## Live Pattern

| Step | Requirement |
|---|---|
| 1 | Obtain explicit approval for the exact environment, mapping, action, mode, and artifact fingerprint |
| 2 | Refresh current mapping evidence and invalidate approval when it changed |
| 3 | Execute once through the supported shared import workflow |
| 4 | Persist request or process identifiers, status, logs, artifact references, and errors without secrets |
| 5 | Verify through the Chart of Accounts Mapping Rules Report or equivalent read-only review |
| 6 | Do not retry a live mutation without idempotency evidence or fresh approval |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| COAMAP.PREVIEW | step | 10 | preview_gate | pass->COAMAP.APPROVAL | COAMAP.BULK | stop | Readiness passes |
| COAMAP.APPROVAL | decision | 11 | approval_gate | approved->COAMAP.EXECUTE;declined->COAMAP.STOPPED | COAMAP.PREVIEW | stop | A live mutation is requested |
| COAMAP.EXECUTE | step | 12 | execution_gate | success->COAMAP.VERIFY;failed->COAMAP.ERROR | COAMAP.APPROVAL | stop | Exact action is approved |
