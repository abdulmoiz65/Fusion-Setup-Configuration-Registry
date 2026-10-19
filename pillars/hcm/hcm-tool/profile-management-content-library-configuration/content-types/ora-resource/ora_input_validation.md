# Content Types Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Supplied configuration | Direct values, blank requirements template, or readable existing file; supplied objects, identifiers, properties and relationships | Return the blank template or identify the required object/row correction | Capture supplied values from local intake without purpose or downstream discovery | Every request | |
| Content Types ownership signal | Supplied type, property or relationship fields, or explicit task/object input | Clarify the supplied object before selection | Ordinary language is accepted; task names are optional | Every proposal request | |
| Proposed content definition | Supplied type name, properties and relationships with source references and mappings | Retain unresolved required fields as blockers | Confirm uncertain mappings and keep all supplied rows together | A new definition is requested | |
| Current-state evidence | Authenticated structured target context; fresh complete current-task export and fingerprint; integrity-validated seed manifest | Block exact-match classification, not the preliminary proposal | Resolve target without screenshots or attestations; record release only from trusted metadata | Exact duplicate checking or configuration readiness is requested | find_complete_content_type_evidence |
| Create-only FSM package | Approved proposal and provider-row fingerprints; authenticated target; fresh complete current-state ZIP; seed manifest; reviewed same-task baseline; exact rows for all three CSV members; package SHA-256; sanitized readiness receipt | Block package and Data Loader preview | Prepare the package through the parent create-only FSM contract | Create or import is requested | verify_content_type_fsm_import_contract |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Supplied Content Type objects or explicit task scope identify the owner | Validated | Check supplied required fields and existing dependencies | |
| Two or more materially different owners or patterns are equally supported | Ambiguous | Ask one concise question about the supplied object or mapping and stop | |
| The request concerns rating models, profile types, profile sections, employee profiles, or another task | Unsupported | Route to the owning skill without preparing Content Types configuration | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Supplied-object routing | Select from the supplied object and fields without purpose or downstream discovery | Every request | |
| Mapping ledger | Record source, evidence, confidence and confirmation for each technical mapping; never infer optional values | Every proposal | |
| Source mapping | Preserve local source values, confirm uncertain mappings, and leave optional omissions unchanged | Direct or file input | |
| Environment and release evidence | Resolve the live target from authenticated context; never request screenshots, copied URLs, exact replies, or attestations; never ask for or infer the quarterly release | Fusion-touching phase | |
| Exactness | Check exact `ContextName` in fresh customer evidence first and seed evidence second; treat names or labels alone as insufficient; compare every applicable supported property and relationship | Existing content is evaluated | find_complete_content_type_evidence |
| Scope boundary | Reject transactional profile changes, downstream profile design, update, merge, delete, or end-date operations | Every request | |
| Provider row completeness | Require every exact header field; source-backed ViewInstanceName and GroupingKey; approved property pairs; property ContextName consistent with the containing parent; relationship ContextName and ContextName1 consistent with portable endpoints; supplied relationship DateFrom; blank ModuleId and generated identifiers. Leave DateTo omitted when absent and allow equal start/end dates. | Create-only package or import | verify_content_type_fsm_import_contract |
| Approval separation | Proposal and package confirmation cannot approve upload; the current core.data-loader immutable preview uses Core's authoritative approval policy: valid same-request auto-approval for the identified load or later contextual approval | Create-only import | verify_content_type_fsm_import_contract |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CT.CAPTURE_CONFIGURATION | decision | 1 | validate_input | valid->CT.CHECK_DEPENDENCIES;ambiguous->CT.RETURN_QUESTION;unsupported->CT.RETURN_UNSUPPORTED;invalid->CT.RETURN_BLOCKED | none | stop | Every Content Types request with supplied objects or fields |
| CT.VALIDATE_FSM_IMPORT | decision | 11 | validate_input | valid->CT.ENFORCE_FSM_IMPORT;invalid->CT.RETURN_IMPORT_BLOCKED;changed->CT.RETURN_IMPORT_BLOCKED | CT.CHECK_DEPENDENCIES | stop | A create-only Content Types package is presented to Task Hook for core.data-loader preview |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
- [Content Types](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/content-types.html)
- [Content Type Properties](https://docs.oracle.com/en/cloud/saas/human-resources/faucf/content-type-properties.html)
