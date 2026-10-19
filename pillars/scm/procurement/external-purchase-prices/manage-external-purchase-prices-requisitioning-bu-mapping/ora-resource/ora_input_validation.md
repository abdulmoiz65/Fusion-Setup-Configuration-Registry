# External Purchase Prices Requisitioning BU Mapping Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request intent | Explicit record retrieval or requested parent/child mutations | Clarify before selecting a route | Pure reads use user-supplied lookup keys and the direct REST read workflow; mutations use the reviewed loader input. A missing loader file/action is not a reason to infer POST | Before any lookup or mutation preparation |  |
| Mapping source | SourceOrganization | Block before lookup or Data Loader preparation | Supply the source organization from the read request or reviewed mutation input; do not invent it | Parent identity is required |  |
| Procurement identity | ProcurementBUName or ProcurementBUId | Block before lookup or Data Loader preparation | Supply an exact name or ID; numeric IDs remain optional when the name is supplied | Parent identity is required |  |
| Child identity | RequisitioningBUName or RequisitioningBUId, with RequistioningBUMappingId when supplied for an existing child | Block only the affected child operation | Supply the exact child name or ID and parent identity through the registered loader linkage | A child operation is present |  |
| Optional loader fields | MappingId, RequisitioningBUGroupId, StatusCode, Status, AgreementUpdateStatusCode, AgreementUpdateStatus | Continue | Do not make optional status fields mandatory; preserve supplied values subject to the selected operation's live loader schema | Mutation input only; no loader metadata is required for pure GET |  |
| Operation | Parent and child operations from the reviewed Data Loader input | Block ambiguous mutation intent | Let core.data-loader resolve the registered operation and representation; do not infer POST from blank action on an existing target | Before mutation preparation |  |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Input shape and required alternatives are valid | Continue | Reference resolution owns lookup mechanics; design enforcement owns active-mapping policy |  |
| Required key is absent or contradictory operations target one row | Block | Correct the exact input; do not silently omit or transform a requested operation |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Source organization | Reject blank-after-trim SourceOrganization or a value longer than 700 characters; preserve case and supplied business value | SourceOrganization is supplied or required |  |
| Optional numeric identifiers | Do not require IDs when supported names are supplied. For mutation input validate supplied types using live loader metadata; for read queries require all supplied keys to agree with the returned identity under the lookup contract, without consulting Data Loader | Parent or child keys are supplied |  |
| Activation value | Accept the live loader's boolean representation, preserving explicit false; reject unrecognized supplied values rather than treating them as blank | ActivationFlag is supplied for a mutation |  |
| Parent-child representation | Use registered parent/child sections and key metadata selected by core.data-loader; do not require a child MappingId or invent ParentIdentifier. A REST nested-body example is not a loader linkage contract | Child records are supplied |  |
| Status attributes | Do not require AgreementUpdateStatus or any optional status attribute; read-only/writeability handling belongs to the selected live loader contract | Mutation input only; pure reads return observed values without defaulting or requiring status input |  |

## Golden Scenarios

| Scenario | Supplied Input | Expected Result |
|---|---|---|
| parent-name-only | SourceOrganization=FIXTURE_SOURCE_ALPHA; ProcurementBUName=Fixture Procurement Alpha | Accept key shape without numeric IDs; resolve and validate before preview |
| child-name-only | RequisitioningBUName=Fixture BU Alpha with registered parent linkage | Accept key shape without child MappingId or RequisitioningBUId |
| blank-source | SourceOrganization contains only whitespace | Block input validation |
| missing-procurement-key | Neither ProcurementBUName nor ProcurementBUId supplied for parent identity | Block input validation |
| optional-status-absent | AgreementUpdateStatus and AgreementUpdateStatusCode omitted | Do not fail a mandatory-status check |
| child-action-missing | Child mutation requested but its action cannot be resolved from reviewed input | Block ambiguous intent; do not guess a child POST |
| read-natural-keys | Explicit GET with SourceOrganization and ProcurementBUName; no workbook or action column | Validate read keys and use direct core REST; mutation schema/defaults/approval are not applicable |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPBU.VALIDATE_INPUT | step | 10 | validate_input | valid->EPPBU.RESOLVE_REFERENCES;invalid->EPPBU.HANDLE_ERROR | none | stop | Before any lookup or Data Loader preparation; input contract only, not business policy |
