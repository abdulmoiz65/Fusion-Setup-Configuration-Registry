# Assign Balancing Segment Values to Legal Entities Input Validation

## Lifecycle Position

| Topic | Contract |
|---|---|
| Purpose | Add or update balancing-segment-value assignments for an existing legal entity in one existing ledger accounting-configuration scope |
| Starts after | The ledger, legal entity, chart of accounts, balancing value set, and eligible balancing values exist and the legal entity is already present in the scoped accounting configuration |
| Ends before | Review and Submit, ledger activation, period opening, journal processing, and deletion or reassignment of values used by posted accounting |
| Supported baseline | Validate and preview the smallest supported task CSV delta; derive technical fields from current authoritative evidence before the first import attempt |

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Target context | Environment, Fusion release, task code, and exact primary-ledger name or ID | Stop before authoring | Resolve exactly one PRIMARY ledger and retain its canonical LedgerId before requesting a task export; never use the first available ledger | Always | resolve_primary_ledger_scope_for_export |
| Legal entity | Exact LegalEntityIdentifier or exact legal-entity name resolvable to one scoped parent row | Block the requested rows | Ask for one exact identifier or name | Always | resolve_legal_entity_parent_row |
| Balancing value set | Optional FlexValueSetCode for cross-checking; otherwise derive it from the exact selected ledger's balancing-segment metadata | Block only if the ledger value set cannot be derived exactly | Use the current scoped ledger alias, then validate the derived code through read-only Value Sets metadata | Always | derive_scoped_balancing_value_set |
| Balancing values | One or more nonblank FlexSegmentValue values | Block invalid rows and show their input positions | Ask for every exact value | Always | verify_balancing_value_exact |
| Effective dates | Optional StartDate and EndDate per assignment | Preserve blank when omitted | Accept ISO `YYYY-MM-DD`; serialize only after the current export contract establishes the physical CSV format | User supplies a date | derive_assignment_row_contract |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Raw text | Preserve raw values; whitespace-only is missing; do not fuzzy-match, change case, or silently normalize business keys | Every text input |  |
| Exact task and scope | Require task code GL_ASSIGN_BALANCING_SEGMENT_VALUES_TO_LEGAL_ENTITIES and one exact PRIMARY ledger resolved to its canonical LedgerId; use that ID to submit a new populated task CSV export first. A current template export is permitted only after the populated attempt has a classified eligible carrier failure | Always | resolve_primary_ledger_scope_for_export |
| Legal-entity identity | Require exactly one confirmed `LEGAL_ENTITY` parent; identifier and name must agree when both are supplied | Always | resolve_legal_entity_parent_row |
| Value-set identity | Derive BalSegValueSetCode from the exact scoped ledger alias; if the user supplies FlexValueSetCode require equality; then require one exact REST match and retain ValueSetId, MaximumLength, ValidationType, and ValueDataType | Always | derive_scoped_balancing_value_set |
| Segment-value length | Require character length not to exceed the exact current MaximumLength; do not hardcode a portable maximum | Each requested value | resolve_value_set_exact |
| Segment-value eligibility | Require one exact value in the resolved value set that is enabled and effective for the proposed dates | Each requested value | verify_balancing_value_exact |
| Date syntax | Accept a real ISO calendar date in `YYYY-MM-DD`; reject invalid text, impossible dates, timestamps, and locale-dependent strings | A date is supplied | derive_assignment_row_contract |
| Date order | EndDate must be on or after StartDate | Both dates are supplied |  |
| Duplicate input rows | Report duplicate semantic keys; do not silently collapse them | Batch contains duplicate keys |  |
| Unknown fields | Reject fields absent from the current exported header or reviewed same-release same-role contract | User supplies additional attributes | derive_assignment_row_contract |
| CSV physical serialization | Parse every changed CSV member from the final ZIP and require the exact export-derived header, one physical header record, intended physical data records, and the expected field count for every record; literal escape text is data, not a row boundary | Before preview and import | derive_assignment_row_contract |

## Population Classification

| Class | Policy |
|---|---|
| Required user input | Exact target scope, legal entity, and one or more values are never guessed |
| Optional user input | StartDate and EndDate remain blank when omitted; never default to current date |
| Resolver derived | Canonical ledger name and LedgerId, legal-entity identifier, balancing ValueSetCode, value-set metadata, and exact value eligibility require exact current receipts |
| Carrier derived | Actual child header, field order, date serialization, and manifest graph come from the new ledger-scoped populated export or, after a classified eligible carrier failure, a current same-task template export |
| Current-state derived | Parent technical fields and current legal-entity/direct-ledger assignment rows come from the populated export or separately validated current read-only Fusion evidence during fallback; a template or prior-run package never proves current ownership |
| Intentional blank | Omitted dates and optional translation value remain blank only when the current same-role contract permits it |
| Service owned | Audit, request, process, and generated metadata are not fabricated or copied from unrelated rows |

## Source Basis

| Source | Use |
|---|---|
| Oracle Fusion Cloud Financials, Assign Legal Entities and Balancing Segments | Task order, assignment purpose, and optional assignment start date |
| Oracle Fusion Cloud Applications Common, Value Sets REST resources | Read-only exact value-set and child-value validation fields |
| Oracle Fusion Cloud Applications Common, Setup Task CSV Exports REST resource | Ledger-scoped task export through `SetupTaskCSVExportCriteria` before package authoring |
| Shared task-level template export route | Current same-task physical carrier through setupTaskCSVTemplateExports after a classified eligible populated-export carrier failure |
| Current task catalog and developer-provided same-task FSM export structure | Task support flags, physical members, headers, data types, and parent-child graph |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ABSV.VALIDATE | decision | 10 | validate_input | valid->ABSV.DEPENDENCIES;invalid->ABSV.RETURN_ISSUES | none | stop | Always |
