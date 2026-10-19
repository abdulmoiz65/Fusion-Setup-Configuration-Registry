# Design Enforcement

Enforce the whole-task FSM and descriptive-flexfield deployment boundaries.
Do not perform deployment or direct flexfield changes from this resource.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Fix task and scope | Use only the exact customer account relationship DFF task and complete unfiltered non-template package scope |
| 2 | Bind export route | Export directly through shared.setup-export.task-level-export after task-level preview approval; do not require deployment evidence or a pre-existing ZIP/hash |
| 3 | Bind import route | Route exclusively through core.data-loader and let it own adapter, endpoint, payload, submission, status, and retry-policy selection |
| 4 | Preserve import bytes | Import only the unchanged exact-task ZIP with its approved SHA-256 |
| 5 | Separate deployment result | After import, verify target deployment and functional behavior before complete-success reporting |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every run | Error |  | Task name or code differs from Manage Customer Account Relationship Descriptive Flexfields and HZ_CUSTOMER_ACCOUNT_RELATIONSHIP_DESCRIPTIVE_FLEXFIELDS | Restore the catalog-backed task identity | Yes |
| Export | Error |  | Template, export criteria, filter, partial selection, or nonshared executor is requested | Use complete, unfiltered, non-template shared FSM export | Yes |
| Export | Error |  | Core Data Loader, approved-loader-payload, executionRoute=data-loader, deployment evidence, or a pre-existing ZIP/hash is required before export | Restore the direct shared task-level export route and request only operation-specific preview approval | Yes |
| Import | Error |  | ZIP bytes, hash, task metadata, target, or Task Hook validation envelope differs from the approved preview | Restart Core Data Loader validation and obtain fresh approval | Yes |
| Import | Error |  | This pillar skill selects or invokes an adapter, endpoint, routing field, payload builder, upload method, initiation method, status implementation, or retry policy | Hand the immutable task context to core.data-loader and let it choose and execute the registered import route | Yes |
| Direct DFF change | Error |  | Request creates, edits, deletes, deploys, or inspects individual flexfield metadata through REST or task-local code | Refuse and direct the user to the supported FSM whole-task or manual Fusion lifecycle | No |
| Successful import | Error |  | Complete migration is claimed without target status and functional-test evidence | Return import_succeeded_deployment_pending until verification passes | Yes |
| Manual deployment required | Error |  | Descriptive flexfield is published without required sandbox deployment and testing | Validate and deploy to sandbox, test, then publish using the Fusion UI lifecycle | Yes |
| Deployment behavior | Error |  | Extensible-flexfield background queue behavior is asserted for this descriptive-flexfield task | Remove the unsupported EFF behavior and use DFF deployment rules | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CARDFF.DESIGN_GATE | decision | 4 | design_enforcement | pass->CARDFF.VALIDATED;fail->CARDFF.ERROR | CARDFF.DEPENDENCY_READINESS | stop | Before operation-specific preview, adapter release, or complete-success reporting |
