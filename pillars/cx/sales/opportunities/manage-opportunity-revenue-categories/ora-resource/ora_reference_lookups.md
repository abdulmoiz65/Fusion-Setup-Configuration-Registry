# Manage Opportunity Revenue Categories Reference Lookups

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Use the Common Features Standard Lookups resource to resolve the parent lookup
type and one exact code. Opportunity revenue category is standard lookup
MOO_REVN_CATEGORY and is distinct from set-enabled MOO_SETID_REVN_CATEGORY.
These lookup nodes are read-only. Pass their validated identity and current
state to package readiness. Apps Common is GET-only for this task. An immutable
FSM package hands off to core.data-loader, which owns its Task Hook preview,
later standalone approval, upload, initiation, and accepted result.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
| --- | --- | --- | --- | --- | --- | --- | --- |
| verify_revenue_category_lookup_type | Revenue-category input validation and defaulting succeed | LookupType fixed to MOO_REVN_CATEGORY | GET /fscmRestApi/resources/11.13.18.05/standardLookups/MOO_REVN_CATEGORY with fields=LookupType,Meaning,Description,ModuleId,CustomizationLevel,RestAccessSecured and self/canonical links | LookupType, Meaning, Description, ModuleId, CustomizationLevel, RestAccessSecured, self/canonical links | Match exactly one parent whose LookupType is MOO_REVN_CATEGORY and preserve its returned current business metadata and links; task ownership comes from the exact catalog mapping, not REST presence alone | Verified parent lookup type, ParentMeaning, ParentDescription, ModuleId, CustomizationLevel, RestAccessSecured, ParentItemLink, ParentStateFingerprint, and catalog task-scope evidence | Stop as catalog mismatch, auth/authz, transport, or Fusion API failure; never create or substitute another lookup type or synthesize parent business metadata |
| find_revenue_category_lookup_code | The parent resolves and RequestMode is SingleLookup | LookupCode and fixed LookupType MOO_REVN_CATEGORY | GET /fscmRestApi/resources/11.13.18.05/standardLookups/MOO_REVN_CATEGORY/child/lookupCodes/{LookupCode}; percent-encode LookupCode as exactly one path segment and request exact fields and self/canonical links | LookupCode, Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, Tag, LastUpdatedBy, self/canonical links | Match zero or one exact case-sensitive LookupCode under MOO_REVN_CATEGORY; preserve the returned item link for existing-code evidence | Existing or absent lookup-code state, seed-data indicator, current-state fingerprint, lookup timestamp, and returned child item link | Return not_found only for a healthy exact 404; stop on mismatch, ambiguity, 401/403, transport failure, malformed data, or any other lookup failure |
| verify_revenue_category_fsm_package | Package Export; SingleLookup Create, Update, or Disable; or Package Import after parent and route-aware code resolution | For Export: exact target/release/task identity and a fresh completed MOO_MANAGE_REVENUE_CATEGORIES baseline ZIP. For mutation or Import: that baseline plus a separate final ZIP, exact TaskName/TaskCode, ASM_SETUP_CSV_METADATA.xml, metadata-derived members and headers, exact parent-child closure, reviewed child state locks/impact, preservation evidence, PackagePath/PackageSha256, persisted TaskContextPath, and positive TaskSequence resolved to the exact skill path, TaskCode, TaskName, offering, and functional area | Local read-only ZIP, XML, CSV, persisted Data Loader task context, SHA-256, and fresh Apps Common GET validation; no Fusion mutation | Export receipt, exact task identity and task-context receipt, ASM/member/header fingerprints, parent/child counts and state, per-row before/after/impact, closure/preservation receipts, PackagePath, reopened PackageSha256 | Export validates the complete unmodified full-task baseline. Mutation/Import requires exactly one current MOO_REVN_CATEGORY parent carrier row when changed children exist, exact child linkage, reviewed row scope/state/impact, preserved unrelated content, and reopened SHA-256; require persisted Data Loader task context for every mutation or import handoff | For Export: validated baseline receipt. For mutation or Import: FsmPackageReady, exact task identity, persisted Data Loader task context, package/closure/state/per-row/preservation evidence, PackagePath, and PackageSha256 | Stop on wrong target/release/task, inconsistent persisted Data Loader task context, ASM/member/header/parent/child/state/impact/preservation/path/hash mismatch; never hand-author or synthesize task context or parent business metadata, repair, partially submit, or require Data Loader approval before handoff |

## Lookup Execution Rules

| Situation | What Happens |
| --- | --- |
| The fixed MOO_REVN_CATEGORY parent lookup type does not resolve exactly | Stop as a catalog mismatch or Fusion API failure; do not create a lookup type or substitute MOO_SETID_REVN_CATEGORY |
| A revenue-category lookup returns one exact MOO_REVN_CATEGORY code | Preserve the returned child item link and current state for design validation and preview |
| No exact code is found | Continue only as a Create candidate; Update, Disable, and Read remain blocked by design validation |
| RequestMode is Package | Skip the single-code lookup as not_applicable; full-task Export has no code scope, while Package Import validates every changed row through package readiness |
| LookupCode is inserted into the child item request path | Percent-encode it as exactly one path segment; never concatenate an unescaped value into the URL |
| Fusion returns 401 or 403 | Stop as authentication or privilege failure; do not try common, generic, or set-enabled lookup resources as substitutes |
| A mutation is requested through the reference lookup | Refuse; pass only validated identity and current state to package readiness. No direct REST write is supported |
| A changed child-code CSV is paired with a header-only or mismatched parent CSV | Fail package readiness; Fusion treats the child as orphaned and may report completed with warnings while processing zero setup objects |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.REVENUE_CATEGORY.VERIFY_TYPE | step | 3 | reference_lookup | resolved->OPP.REVENUE_CATEGORY.LOOKUP_CODE;missing->OPP.REVENUE_CATEGORY.RETURN_FAILED;failed->OPP.REVENUE_CATEGORY.RETURN_FAILED | OPP.REVENUE_CATEGORY.DEFAULT | stop | Before checking any MOO_REVN_CATEGORY lookup code |
| OPP.REVENUE_CATEGORY.LOOKUP_CODE | step | 4 | reference_lookup | resolved->OPP.REVENUE_CATEGORY.VERIFY_PACKAGE;not_found->OPP.REVENUE_CATEGORY.VERIFY_PACKAGE;not_applicable->OPP.REVENUE_CATEGORY.VERIFY_PACKAGE;failed->OPP.REVENUE_CATEGORY.RETURN_FAILED | OPP.REVENUE_CATEGORY.VERIFY_TYPE | stop | Resolve SingleLookup state; Package Export or Import continues as not_applicable to package readiness |
