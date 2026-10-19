# Educational Establishments Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Supplied configuration | Direct values, blank requirements template, or readable existing file; supplied institution identifiers and fields | Return the blank template or identify the required row correction | Capture supplied local intake without purpose or downstream discovery | Every request | |
| Educational Establishments ownership signal | Supplied establishment reference values or exact task/object input | Clarify the supplied object before selection | Accept ordinary language without requiring Fusion task names | Every proposal request | |
| Approved establishment values | Supplied SchoolCode, Name and applicable optional fields, with source references and mapping review status | Retain unresolved required values as blockers | Preserve supplied values; never derive them from employee records or comparable setups | A proposal is requested | |
| Current-state evidence | Authenticated structured target context; complete current Educational Establishments evidence; fingerprint and freshness | Block exact-match classification, not the preliminary proposal | Obtain a fresh workflow-approved complete task export without screenshots, copied URLs, exact replies, or attestations | Exact duplicate checking or configuration readiness is requested | find_complete_educational_establishment_evidence |
| Create-only FSM package | Approved proposal, source-authority, and provider-row fingerprints; exact task and target; complete fresh current-state ZIP; reviewed same-task baseline; exact HRT_SCHOOL rows; package path/SHA-256; sanitized readiness receipt | Block package and Data Loader preview | Prepare the package through the parent create-only FSM contract | Create or import is requested | verify_educational_establishment_fsm_import_contract |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Supplied establishment reference values or an explicit task scope identify the owner | Validated | Check supplied required fields and existing references | |
| Two or more materially different owners or patterns are equally supported | Ambiguous | Ask one concise question about the supplied object or mapping and stop | |
| The request changes education content types, degrees, fields of study, profile sections, or employee education records | Unsupported | Route to the owning skill | |
| Proposal or package confirmation is presented as Data Loader submission approval | Invalid | Stop; only approval of the current immutable core.data-loader preview can authorize upload | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supplied-object routing | Select from supplied objects and fields without purpose or downstream discovery | Every request | |
| Mapping ledger | Record source, evidence, confidence and confirmation for each mapping; never infer optional values | Every proposal | |
| Source mapping | Preserve local source values, confirm uncertain mappings, and leave optional omissions unchanged | Direct or file input | |
| Environment and release evidence | Resolve the live target from authenticated context; never request screenshots, copied URLs, exact replies, or attestations; never ask for or infer the quarterly release | Fusion-touching phase | |
| Duplicate identity | Compare all applicable source-supported values; a name-only match does not establish full equality | Existing establishments are evaluated | find_complete_educational_establishment_evidence |
| Scope boundary | Reject employee education transactions, neighboring tasks, update, merge, delete, end-date, and direct-write routes outside the create-only FSM contract | Every request | |
| Provider row completeness | Require every exact header field; EstablishmentVO; GroupingKey equal to SchoolCode; explicit geography pairs; blank generated identifiers | Create-only package or import | verify_educational_establishment_fsm_import_contract |
| Migration-view requiredness | Require supplied SchoolCode, Name and Description for the supported EstablishmentVO package. Location and geography are optional; leave omitted values empty. Supplied geography identifiers must form complete country/state pairs. Never derive Description or Location from Name. | Supported create-only FSM package | verify_educational_establishment_fsm_import_contract |
| Approval separation | Proposal and package confirmation cannot approve upload; the current core.data-loader immutable preview uses Core's authoritative approval policy: valid same-request auto-approval for the identified load or later contextual approval | Create-only import | verify_educational_establishment_fsm_import_contract |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EE.CAPTURE_CONFIGURATION | decision | 1 | validate_input | valid->EE.CHECK_DEPENDENCIES;ambiguous->EE.RETURN_QUESTION;unsupported->EE.RETURN_UNSUPPORTED;invalid->EE.RETURN_BLOCKED | none | stop | Every Educational Establishments request, with supplied configuration values or explicit task scope |
| EE.VALIDATE_FSM_IMPORT | decision | 11 | validate_input | valid->EE.ENFORCE_FSM_IMPORT;invalid->EE.RETURN_IMPORT_BLOCKED;changed->EE.RETURN_IMPORT_BLOCKED | EE.CHECK_DEPENDENCIES | stop | A create-only Educational Establishments package is presented to Task Hook for core.data-loader preview |

## Sources

- Source: `educationEstablishmentService/view/EstablishmentVO.xml`, UserKey and ViewAttribute declarations, plus `model/entity/EstablishmentEO.xml` and `EstablishmentTranslationEO.xml`. The migration VO declares Description `IsNotNull=true`; Location has no `IsNotNull`. This source contract does not establish deployed release or target privileges.

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
- [Using Enhanced Talent Profiles](https://docs.oracle.com/en/cloud/saas/talent-management/fauep/using-enhanced-talent-profiles.pdf)
