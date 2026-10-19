# Algorithm Dependency Readiness

## Required Dependencies

| Dependency | Required state | If not ready |
|---|---|---|
| Mandatory preflight | Completed before every advisory, mapping, Groovy, validation, source-resolution, target-resolution, or use-case request | Stop and request corrected current exports before any source or target reasoning |
| Algorithm_BO.xml | Supplied as a current attachment or explicit file input in the same request and identifies the Subscription Management and Account Receivables Integration algorithm | Request both current XML exports; do not use chat cache, prior project artifacts, remembered paths, or default assumptions |
| Service Mapping source XML | Supplied as a current attachment or explicit file input in the same request; any filename is accepted, but it must contain `contextName="ARInterface"` | Request both current XML exports; do not use chat cache, prior project artifacts, remembered paths, or default assumptions |
| Editable version | All versions are read and the absolute highest `VersionNum` has `ActiveFlag` `Y` | Inform the implementer that the highest version is not in In Progress state; do not proceed with advisory, Groovy, or XML editing |
| Input type classification | The request is classified as Type 1, 2, 3, 4, or 5 from `references/ora_use_case_resolution.md` | Follow the required source and target resolution path before drafting |
| Existing action | The target `StepActionSetup` and its current Groovy state are identified | Ask whether existing Groovy is replaced or new logic is added above it, and whether formatting is wanted |
| Companion result | The Service Mapping companion has returned confirmed aliases, alternatives, assumptions, and publication prerequisites when mapping is involved | Route to the companion and wait for its result |
| Describe runtime path | When the companion cannot complete a required describe because of runtime environment connection, authentication, privilege, transport, or endpoint failure, the implementer has chosen whether to fix the connection and rerun describe or proceed only with named unconfirmed assumptions for review | Stop; do not substitute assumptions until the implementer chooses that path |
| Source-resolution record | Every Groovy source is an accepted existing attribute, exact implementer-provided source, or explicitly accepted named describe candidate | Do not draft Groovy; return to the companion for discovery and an implementer decision |
| Groovy approval | The implementer explicitly approves the reviewable Groovy | Do not create a local import artifact |
| Service Mapping configuration handoff | The companion has supplied the final configuration handoff after local approved XML creation | Persist the handoff before final implementation handoff |
| Final source-target table | The final handoff includes source object, source attribute, Service Mapping alias, target RA column, insert name, context, flex context, transaction scope, and confirmed-or-assumed status | Add the table before handoff |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ALG_AR_CHECK_DEPENDENCIES | step | 3 | resolve_dependency | ready->ALG_AR_APPLY_DEFAULT;blocked->ALG_AR_BLOCKED | ALG_AR_ROUTE_SERVICE_MAPPING | stop | Input validation and any required companion mapping review are complete |