# Reference Lookups

Source basis: Oracle Fusion Cloud Sales, Sales Lead Lookups, and Oracle
Applications Common Standard Lookups REST endpoints.

## Documented Standard Candidate Baseline

| Lookup Type | Documented Area | Product Description |
|---|---|---|
| MKL_ACCESS_LEVEL | Lead | Access level |
| MKL_LEAD_ACCEPTED_FLAG | Lead | Lead accepted flag |
| MKL_LEAD_ASGNT_STATUS_CODE | Lead | Assignment mode or assignment status; one exact type despite two page entries |
| MKL_ASGN_JOB_TYPE | Lead | Assignment job type |
| MKL_FUSE_DASHBOARD_DISPLAY | Lead | Dashboard display |
| MKL_LEAD_SCHEDULE_STATUS | Lead | Schedule status |
| MKL_LEAD_SCHEDULE_MODE | Lead | Schedule mode |
| MKL_WAIT_LAG_UNITS | Lead | Wait or lag units |
| MKL_SCH_OPERATORS | Lead | Schedule operators |
| ORA_MKL_LEAD_REASSIGN_STATE | Lead | Reassignment state |
| MKL_DEAL_APPROVAL_STATUS | Lead | Deal approval status |
| MKL_LEAD_REGISTERED | Lead | Lead registration status |
| MKL_LEAD_SRCH_GROUP | Lead | Search group |
| MKL_LEAD_STATUS | Lead | Lead status |
| MKL_RETIRE_REASON_CD | Lead | Retire reason |
| MKL_YES_NO_REVERSE | Lead | Reverse yes or no |
| MKL_SPD_ACTION_TYPE | Lead | Sales prospecting action type |
| ORA_ZCA_AI_WHO_THRESHOLD_MODES | Lead | AI update threshold modes |
| ORA_MKL_DEAL_ACCESS_LEVEL | Deal Registration | Access level |
| ORA_MKL_DEAL_ASSIGN_MODE | Deal Registration | Assignment mode |
| ORA_MKL_DEAL_REJECT_REASON | Deal Registration | Rejection reason |
| ORA_MKL_DEAL_RETURN_REASON | Deal Registration | Return reason |
| ORA_MKL_DEAL_SRCH_RECORD_SET | Deal Registration | Search record set |
| ORA_MKL_DEAL_WRKSPC_RECORD_SET | Deal Registration | Workspace record set |
| ORA_MKL_DEAL_REG_STATUS | Deal Registration | Registration status |
| ORA_MKL_DEALREG_DEAL_TYPE | Deal Registration | Deal type |

## Explicit Set-Enabled Exclusions

| Lookup Type | Disposition |
|---|---|
| MKL_LEAD_BUDGET_STATUS_SETID | Route to Manage Set Enabled Lookups |
| MKL_LEAD_RANK_SETID | Route to Manage Set Enabled Lookups |
| MKL_LEAD_REASSIGN_REASON_SETID | Route to Manage Set Enabled Lookups |
| MKL_REJECT_REASON_SETID | Route to Manage Set Enabled Lookups |
| MKL_RETIRE_REASON_CD_SETID | Route to Manage Set Enabled Lookups |
| MKL_DEAL_TYPE_SETID | Route to Manage Set Enabled Lookups |
| MKL_LEAD_CHANNEL_SETID | Route to Manage Set Enabled Lookups |
| MKL_LEAD_TIMELINE_SETID | Route to Manage Set Enabled Lookups |

## Live Lookups

| Rule ID | Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|---|
| SLL.LOOKUP | find_standard_lookup_candidates | After validation and dependency readiness | Operation, exact LookupType and LookupCode when supplied, 26-code documented baseline, and unique export type codes for Inventory/Review | GET /fscmRestApi/resources/11.13.18.05/standardLookups/{LookupType}; GET child/lookupCodes with pagination; exact GET child/lookupCodes/{LookupCode}; GET child/translations only when requested | Type: LookupType, Meaning, Description, ModuleId, CustomizationLevel, RestAccessSecured, links; code: LookupCode, Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, CreatedBy, CreationDate, LastUpdatedBy, LastUpdateDate, links; translations for Review or Meaning-change impact | Inventory de-duplicates documented plus export-only standard types and excludes Set ID types. Review requires exact type and optional exact code. AddCode requires one exact parent and zero exact code matches. UpdateCode/DisableCode require one exact item. RemoveCode additionally requires positive customer-created evidence; missing evidence is not inferred from absence of a seed marker. Never fuzzy-match or require export membership for mutation | Candidate source class, export membership for reconciliation, type status, complete code inventory, exact code cardinality, current-state fingerprint, canonical item link, customer-created evidence status, translations when requested, mutation method selection, attempted/resolved/not_found/error counts, timestamp | Healthy exact 404 is not_found; AddCode may proceed on zero code matches under one exact live parent. Many blocks. 401/403/systemic transport/pagination/shape failure blocks. Export omission never blocks Apps Common CRUD. RemoveCode without positive customer-created evidence routes blocked |

## Reconciliation Rules

| Situation | What Happens |
|---|---|
| Documented type resolves live and appears in export | Classify documented-and-exported |
| Documented type resolves live but is omitted from export | Classify documented-live-only; allow Inventory, Review, and eligible Apps Common code CRUD |
| Export-only type resolves at standardLookups | Classify export-only and require explicit environment-only review before mutation |
| Candidate exact GET returns healthy 404 | Classify unavailable; retain it in completion evidence |
| Candidate has auth/transport/pagination/shape failure | Classify lookup_error and fail inventory completion |
| Export contains only one type | Continue full union; never return it as complete inventory |
| Same exact LookupType appears twice in documentation | De-duplicate by exact code and retain descriptions |
| Set ID type is requested | Return unsupported_task_scope and route to Manage Set Enabled Lookups |
| AddCode finds exact code | Return resolved and block duplicate |
| AddCode finds no exact code under one live parent | Return not_found and allow POST preview |
| UpdateCode or DisableCode finds one exact code | Return resolved and allow PATCH preview after remaining gates |
| RemoveCode finds one exact code but custom evidence is absent/ambiguous | Return resolved with delete_safety_blocked and offer DisableCode |
| RemoveCode positively resolves a customer-created code | Return resolved and allow DELETE preview after impact/approval gates |

## Lookup Rules

- Follow pagination to `hasMore=false` for types, codes, and translations.
- Prefer Fusion-returned item links when they differ from constructed paths.
- Use exact code absence and existence only from live Apps Common reads; export
  omission is never absence or mutation authority.
- Use `CreatedBy` and other returned ownership/customization evidence only when
  it positively establishes customer creation. Do not infer deletability from
  `LastUpdatedBy`, export presence, or lack of a known seed marker.
- Re-read the parent and code immediately before execution and compare the
  complete expected-state fingerprint.
- Treat translation reads as impact evidence only; this task never writes the
  translations child.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SLL.LOOKUP | step | 3 | reference_lookup | resolved->SLL.ROUTE;not_found->SLL.ROUTE;many->SLL.RETURN_ISSUES;failure->SLL.RETURN_ISSUES;unsupported_task_scope->SLL.RETURN_ISSUES | SLL.DEPENDENCIES | stop | Resolve complete Inventory candidate union or one exact requested standard lookup type/code and obtain duplicate, current-state, translation, ownership, and deterministic CRUD evidence through Apps Common reads |
| SLL.ROUTE | decision | 4 | evaluate_result | proceed->SLL.DESIGN;blocked->SLL.RETURN_ISSUES | SLL.LOOKUP | stop | Proceed for complete Inventory/Review, AddCode with one parent and zero code matches, UpdateCode/DisableCode with one exact current code, safe RemoveCode with positive custom evidence, or valid BulkSet rows; block unsupported scope, duplicate, ambiguous/missing target, unsafe delete, translation/type mutation, or systemic read failure |
