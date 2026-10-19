# Operation-Scoped Environment and Compatibility Contract

## Purpose

Bind live read-only evidence to the authenticated FDOS Fusion context without
using screenshots, URLs or user attestations to establish identity/access, or requiring a quarterly
release.

## Select the Actual Operation First

Missing quarterly metadata is not a global readiness failure. Require only
the prerequisites of the selected operation; do not require creation evidence
to collect the export that will establish that evidence.

| Operation | Required preflight | Release handling |
|---|---|---|
| Local requirements template, intake or preliminary review | Safe local inputs and project paths | No target, login, release or capability receipt required |
| FSM data export or FSM template/spec export | shared.setup-export.task-level-export owns authentication, exact TaskCode, CSV support, privileges, payload approval, polling and artifacts | Quarterly release may remain unknown; no Talent Catalog REST probe or seed overlay is a prerequisite |
| Registered Content Item REST evidence | Authenticated target plus the declared bounded REST capability check below | Release labels do not gate a structurally valid registered read; read success does not certify creation |
| Local FSM package and Core Data Loader import | Task-specific fresh complete evidence, same-target baseline, exact provider schema, dependencies, immutable fingerprints, Task Hook and its approval workflow | No release prerequisite or allowlist; validate the actual task/provider contract |
| Instance Qualifier containing evidence | Separately owned Profile Types workflow | Do not probe Talent Catalog or retry the unsupported standalone qualifier task |

FSM-only tasks, including Educational Establishments, have no dependency on
the Content Items REST adapter. Use their already declared export and Core
Data Loader workflows, not a newly invented REST check. Preserve the owning
workflow's actual sanitized diagnostics and receipts; do not manufacture a
CATALOG_REST capability receipt for an FSM operation. Authentication, task
privilege, unsupported CSV flags and data-handling failures still stop the
affected external operation.

## Structured REST Evidence

A registered Content Item REST preflight result contains only sanitized fields:

| Field | Contract |
|---|---|
| status | verified |
| target_environment | Exact alias resolved from authenticated FDOS configuration |
| environment_fingerprint | SHA-256 over the sanitized alias and capability selection |
| authenticated_context_source | Existing repository Fusion authentication context |
| operation | read-only-capability-check |
| selected_api_version | Registry-declared API namespace that passed the capability check |
| selected_resource | Registry-declared relative REST resource path |
| fusion_release | Present only when trusted authenticated metadata explicitly provides the quarterly release |
| release_status | verified or unknown |
| checked_at | UTC timestamp |
| capability_fingerprint | SHA-256 over the complete verified capability receipt |

A blocked result contains only `status: blocked`, a classified
`failure_class`, and a sanitized actionable `message`. It must not fabricate
target, API, release, timestamp, or fingerprint fields that were not verified.

This blocked result is a diagnostic, not a capability receipt. The existing
`schemas/fusion-environment-capability.schema.json` accepts verified receipts
only. Never validate a blocked diagnostic as a verified receipt, pass it to a
consumer requiring capability evidence, or invent fields to make it pass.
Persist it through the project's diagnostic workflow, adding the prescribed
stage, recommended action and artifact references to that diagnostic envelope.
No capability-schema extension or alternate execution route is implied.

Do not persist a base URL, token, token-cache content, client secret, password,
private key, raw response, or credential diagnostics.

## REST Target Resolution

Resolve the target from the authenticated repository Fusion configuration and
prove authentication through the declared bounded GET. An optional expert
expected-environment value may be used only as a mismatch assertion; it is not
the source of environment identity.

Never accept a screenshot, address-bar image, copied URL, hostname, exact reply,
or user attestation as authenticated identity/access evidence. The narrowly scoped
new-set classification confirmation in [the new-set contract](new-catalog-set-contract.md)
is permitted only for non-production classification, not identity, privileges or
data-handling permission. If authenticated context is missing
or cannot be verified, return blocked instead of asking for visual evidence.

## API Capability Selection

Use only ordered candidates declared in the task-local provider registry. For
each candidate, issue one bounded GET with the registry-declared query and the
adapter's existing timeout and output bounds. Select the first candidate
returning the documented response shape. Stop immediately on authentication,
authorization, or target binding failure. Do not invent or probe an undeclared
API version or resource.

A successful API capability check proves resource availability only. It does
not prove a quarterly Fusion release or a create/import provider lifecycle.

## Release Metadata Is Informational

No Content Library task or operation requires a quarterly or technical release
label, release match, allowlist, release attestation, or release-specific catalog
regeneration. This includes availability, exact checks, local templates, FSM
exports/imports, all nine catalog-backed contexts, the optional test batch, and
the explicitly selected verified GOAL fallback. Do not ask the user to supply
or prove a release. Use unknown where an existing receipt requires a value.

Keep observed source metadata as-is. A technical value such as 11.13.26.10.0
does not need conversion to 26C. User-supplied or conflicting labels are not
authenticated evidence, but neither is an operation blocker. The optional
quarterly-only field in a REST capability receipt may simply be omitted with
release_status unknown; it is never required for provider selection.

Validate compatibility from the actual task identity, provider, required ZIP
members, headers, fields, keys, complete fresh same-target evidence, and declared
readback contract. Preserve baseline metadata unchanged. A schema version or API
namespace is a real interface contract, not a Fusion release eligibility gate.
Actual provider/schema mismatches, unsupported fields or lifecycle, duplicates,
missing dependencies, auth/privilege failures and immutable approvals still stop
the affected action. Source release labels in registries describe prior evidence,
not a runtime allowlist or certification of every deployed version.

For Content Types and legacy Content Items, use the packaged seed catalogs
after checking manifest kind, source provenance, hashes, columns, row counts and
exact keys. Do not compare their source release with the target. Keep each
match's source customer or seeded; never relabel a packaged row as observed on
the target. Report availability as the fresh customer export plus the packaged
seed baseline, with their coverage stated separately. A missing customer layer
or incomplete export remains an evidence gap, not a release gap. A header-only
unfiltered same-target export plus validated seeds supports the declared overlay
comparison; neither seeds nor a header-only export proves independent readback.

Removing release gates does not expand provider scope, enable Instance Qualifier
standalone execution, repair the GOAL FSM defect, or authorize an external call.
Changing an already fingerprinted artifact still invalidates its exact approval.

## Failure and Retry

Classify failures as input validation, auth/authz, transport/environment,
Fusion API, catalog mismatch, or artifact persistence. Refresh an expired token
once through the existing core authentication path. Retry only a known
recoverable read-only transport failure within the existing bounded policy.
Never retry or substitute a mutation.
