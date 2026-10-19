# Reference Lookups

## Supplied CSV pass-through import

Resolve only the exact object routing and transport metadata:

1. Obtain the exact Import Management object code from explicit user context or
   the optional authoritative mapping CSV. If neither supplies it, ask for the
   CX Business Object code. Never derive it by inspecting data columns or rows.
2. Query `importExportObjectMetadata` with the exact code and require one exact
   row with `ImportSupport=Y`.
3. Query `objectMetadata/{ObjectCode}?fields=UcmAccount&onlyData=true` and use
   the returned UCM account for upload.
4. Resolve the exact job-level `ImportMode` from explicit user intent or an
   already reviewed workflow artifact: `create` -> `CREATE_ONLY`; `update`,
   `create and update`, or `create-or-update` -> `CREATE_RECORD`; and `delete` ->
   `DELETE_RECORD`. Never derive the mode from supplied CSV content and never
   rely on Oracle's default.

Do not query, validate, or require active values for any field contained in—or
absent from—a supplied data CSV. This includes `PartyUsageCode`, `LinkType`,
parent identities, source-system references, lookups, and product identities.
Job-level `ImportMode` is not a CSV field check. Do not ask the user to waive
such checks.

An explicit supplied `Hierarchy` or `HierarchyNode` delete uses this same
pass-through route. Do not query row identities or require a pre-delete match.
Record-level lookups are optional verification performed only when the user
separately supplies the necessary identities.

If the user reports changed login, role, or privilege access, force one fresh OAuth login
and repeat only the exact read-only Import Management finder once.
Do not treat CRM metadata access as proof of UCM upload authorization.

## Generation or explicit data validation

Only for generation or an explicit data-validation request, resolve profile,
field, parent, lookup, identity, operation, volume, and verification contracts
from `references/object-profiles.json`, `references/column-contracts.json`, and
`references/field-contracts.json`. Preserve the distinctions between Account
and Organization, Contact and Person, and display names versus exact object
codes when selecting the import object.

For a generated or explicitly validated Linked Party file, resolve LinkType
through a `fusion-runtime` `--target-values-json` contract. Resolve the
Organization item through `/hubOrganizations/{PartyNumber}/child/LinkedParty`;
use PartyNumber, not `PartyId`, as that collection key. For hierarchy work, an
active lookup is necessary but not sufficient evidence of configuration, and
the Manage Hierarchies search selector is also insufficient. Require direct
evidence of the tree structure definition.

For generated or explicitly validated Hierarchy and Hierarchy Member files, use
`TreeStructureCode + TreeCode` as the Hierarchy identity. Use that tree identity
plus either `PartyNumber` or `PartyOrigSystem + PartyOrigSysRef` for a Hierarchy
Member update. For member deletion, additionally require the exact parent
identity and `AsOfDate` so one member-parent edge in one effective version is
selected. Delete rows are identifier-only. Before a live hierarchy delete, retain
current target-specific evidence that the exact object accepts `DELETE_RECORD`;
generic Import Management delete guidance is not object-specific proof.

For a generated or explicitly validated Additional Identifier delete, resolve
the selected parent party first, then query its `AdditionalIdentifier` child by
the exact `PartyIdentifierId`. Require exactly one pre-delete match and retain
the parent identity and identifier ID in the immutable preview. Do not
substitute `PartyNumber`, identifier type/value, or a source-system pair as the
delete identity. After successful processing, repeat the same lookup and
require zero exact matches.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TCA.METADATA | decision | 4 | reference_lookup | resolved->TCA.DESIGN_GATE;missing->TCA.RETURN_ISSUES;failure->TCA.RETURN_ISSUES | TCA.DEPENDENCIES | stop | Resolve only object import support and UCM routing for supplied CSVs. |
