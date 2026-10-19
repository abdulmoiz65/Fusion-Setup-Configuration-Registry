# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Read scope | Environment and optional LookupType or meaning | Stop only when the environment or requested type is ambiguous | Resolve exactly one configured environment and an exact task-scoped type when named | Read request | resolve_hierarchy_lookup_target |
| Create | Environment, LookupType, LookupCode, Meaning, authoritative hierarchy type evidence | Stop before preview | Collect the missing value and obtain hierarchy evidence from its owning setup | Create PARTY_HIERARCHY_TYPE code | resolve_hierarchy_lookup_target |
| Update, enable, or disable | Environment, LookupType, LookupCode, named changed fields | Stop before preview | Retrieve the exact current code and collect only named changes | Update request | resolve_hierarchy_lookup_target |
| Delete | Environment, LookupType, LookupCode | Stop before preview | Retrieve the exact current code and prove it is a permitted custom code | Delete request | resolve_hierarchy_lookup_target |
| Import | Validated immutable ZIP, exact task code, target environment, exact `ASM_SETUP_CSV_METADATA.xml` member, metadata task identity, immutable hash, Task Hook validation envelope, and separate approval | Stop before Core Data Loader upload or initiation | Preserve the ZIP, require metadata task identity `HZ_MANAGE_HIERARCHY_LOOKUPS`, and complete Core Data Loader Task Hook validation and approval for the exact archive | Import request |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| HZ_TREE_STATUS create, enable, disable, date, tag, or delete is requested | Blocked | Explain that the System lookup and seeded status codes are protected | resolve_hierarchy_lookup_target |
| HZ_TREE_STATUS meaning or translation change is requested | Conditionally eligible | Continue only when current Oracle rules and exact metadata permit the named field | resolve_hierarchy_lookup_target |
| PARTY_HIERARCHY_TYPE code is seeded | Blocked | Select a permitted custom code or use the owning hierarchy task | resolve_hierarchy_lookup_target |
| Authoritative hierarchy type evidence is absent for a PARTY_HIERARCHY_TYPE create | Blocked | Verify the hierarchy type in its owning task before preview; do not infer or call an undocumented endpoint |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| LookupCode | Require 30 or fewer characters, uppercase alphabetic characters, no spaces, a stable identifier, no ORA prefix, and no exact duplicate | Create | resolve_hierarchy_lookup_target |
| Meaning | Require a nonempty user-facing value of 80 or fewer characters | Create |  |
| Description | Accept at most 240 characters and only when current describe metadata permits it | Create or update |  |
| EnabledFlag | Accept Y or N only | Create or enabled-state update |  |
| Effective dates | Reject an end date earlier than the start date; otherwise require the current REST-supported format | Dates are supplied |  |
| Upsert mode | Reject true; create must omit Upsert-Mode or set it to false | Create |  |
| Identity fields | Reject changes to lookup type, lookup code identity, module, category, or seeded-code identity | Update | resolve_hierarchy_lookup_target |
| FSM archive marker | Require a ZIP member whose exact case-sensitive basename is `ASM_SETUP_CSV_METADATA.xml`; reject absent, duplicate, unreadable, encrypted, unsafe-path, or ambiguous metadata | Import |  |
| FSM task identity | Parse the metadata without rewriting the ZIP and require exactly one task identity equal to `HZ_MANAGE_HIERARCHY_LOOKUPS`; outer and inner request TaskCode values must match it | Import |  |
| Data Loader handoff | Require a current Task Hook validation envelope bound to the exact approved environment, task code, ZIP path, and SHA-256; reject locally reconstructed or preflight-only envelopes | Import |  |
| Import execution owner | Require `core.data-loader`, a current Task Hook validation envelope bound to the exact archive SHA-256, and separate explicit approval; reject every task-local endpoint, adapter, routing-field, or retry selection | Import |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HL.VALIDATE | step | 1 | validate_input | valid->HL.DEFAULT_SCOPE;invalid->HL.RETURN_ISSUES | none | stop | Before lookup resolution, validation, export, or import routing. |
