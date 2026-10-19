---
skill_id: "shared.extensibility.vblens-express-mode"
name: "VBLens Express Mode"
description: "Manages the full Oracle Fusion Express Mode lifecycle: discover supported customization, assess and explain behavior, create or update Business Rules, Advanced Expressions, layouts and verified Page Properties, validate, document, import, export, build, explicitly deploy, answer deployed-runtime questions, and commit reviewed Extension changes."
layer: "shared"
pillar: "Common"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "Shared extensibility enablement team with core platform review"
version: "0.3.0"
inputs:
  - "project_id"
  - "business_requirement"
  - "extension_workspace"
  - "express_mode_target"
  - "fusion_environment_context"
  - "source_or_import_package"
  - "execution_options"
  - "approval_state"
outputs:
  - "exploration_report"
  - "capability_summary"
  - "feasibility_report"
  - "effective_behavior_explanation"
  - "runtime_evidence_manifest"
  - "rest_schema_evidence"
  - "field_contract_evidence"
  - "change_proposal"
  - "extension_change"
  - "validation_result"
  - "functional_documentation"
  - "implementation_record"
  - "import_or_export_assessment"
  - "vx_build_result"
  - "deployment_result"
  - "deployment_urls"
  - "commit_result"
  - "diagnostics"
  - "token_usage_record"
depends_on:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
uses_core:
  - "core.auth.fusion-oauth-authentication"
  - "core.fusion-api.rest-api-client"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
persists_project_state: true
state_updates:
  - "skill_path"
  - "requirements"
  - "design_decisions"
  - "configuration_blueprints"
  - "exports"
  - "baselines"
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/shared/extensibility/vblens-express-mode/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/shared/extensibility/vblens-express-mode/current/reports/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects:
  - "Makes approved read-only Fusion REST requests through the core REST client."
  - "Downloads fixed-origin Oracle App UI bundles without Fusion credentials."
  - "Writes evidence, proposals, reports, documents, and diagnostics to the project workspace."
  - "May create or update approved customer-owned Express Mode Extension artifacts."
  - "May replace generated build output and create a VX archive in the Extension workspace."
  - "Uploads one approved VX archive to Fusion and creates no business data."
  - "May create one reviewed Git commit after explicit COMMIT approval."
required_privileges:
  - "Fusion privileges to read App UI metadata, setup values, and selected REST descriptions"
  - "Fusion privileges to upload a Visual Builder Extension archive"
  - "Local read and write access to the selected Extension and project workspaces"
---

# VBLens Express Mode

## Purpose

This skill takes care of the full Oracle Fusion Express Mode lifecycle. It
turns a business requirement into an evidence-backed customization, explains
existing behavior, creates or updates supported Extension artifacts, validates
and documents the result, handles import and export assessment, builds and
deploys a reviewed VX archive, answers deployed-source questions, and commits
approved source changes.

Its writable scope includes Business Rules, nested rules, validation messages,
Advanced Expressions, rule-set layouts, containers and sections, and Page
Properties whose exact overlay contract is proven. It also discovers Flexfield,
lookup, language, and setup dependencies.

The method is cross-pillar. Page paths, field contracts, and setup values must
always come from the selected Fusion family, page, release, and environment.
The bundled examples are strongest for HCM and never replace target-page
evidence for ERP, SCM, Procurement, CX, or another family.

## Operating contract

1. Resolve the implementation project and Git repository. Run
   `scripts/repository_preflight.js` before repository mutation and preserve
   unrelated user work.
2. Inspect Oracle-delivered evidence and customer Extension evidence. Treat
   Oracle source and downloaded bundles as read-only.
3. Complete the Explore route before Assess, Create, or Update. For a
   field-based change, require matching page, Dynamic Form, Business Rules,
   REST-schema, and environment provenance evidence. Never propose code,
   formulas, accessors, or destination files from partial evidence.
4. Classify the exact artifact and operation with
   `references/express-mode-capability-contracts.json`. Source visibility alone
   is not write permission.
5. Maintain an evidence ledger for material claims. Unsupported conclusions
   require affirmative negative evidence for the exact page, operation, and
   release.
6. Keep Business Rules accessor shape, internal page-state shape, REST-schema
   shape, and observed-runtime shape separate.
7. Present the proposed behavior and test cases in business language. Require
   approval before changing Extension source.
8. Change only the minimum customer-owned Extension files. Never modify an
   Oracle-delivered artifact.
9. Validate the exact change and scenarios before Build, Deploy, or Commit.
10. Use only pinned build dependencies already present in the Extension
   workspace. Never install packages.
11. Obtain explicit approval immediately before the exact Fusion upload. Send
    one upload request, never retry or poll, and return URLs without opening
    them.
12. Require a later message beginning with `COMMIT` before creating one scoped
    Git commit. Do not push.
13. Store durable work under `project/{project_id}` and use only the standard
    FSCR token-usage log.

Read [end-to-end-assessment-workflow.md](references/end-to-end-assessment-workflow.md)
for any non-trivial discovery, assessment, authoring, validation, or delivery
request.

## Route the request

| User goal | Route | Read or run |
| --- | --- | --- |
| Investigate a page before selecting a solution | **Explore** | `investigate_express_evidence.js`, runtime graph, Business Rules extractor, REST describe |
| Show everything an Express Mode page supports | **Capability Discovery** | `inspect_express_capabilities.js`, capability contracts, capability template |
| Decide whether a policy is feasible | **Assess** | behavior contracts, field evidence, feasibility template |
| Explain current rules or effective page behavior | **Explain** | effective configuration and cached or repository evidence |
| Add Business Rules, defaults, validations, layouts, sections, or Page Properties | **Create** | authoring guide, destination resolver, change proposal |
| Change an existing customer rule or property | **Update** | effective configuration, destination and validation contracts |
| Answer from deployed App UI source | **Runtime Evidence** | runtime cache builder and answering guide |
| Verify fields, children, types, or setup values | **REST and Setup Evidence** | service evidence and setup resolver through the central REST client |
| Check Extension source and scenarios | **Validate and Test** | Extension validator and verification template |
| Package a reviewed Extension | **Build** | VX build contract and builder |
| Upload once and generate test URLs | **Deploy** | deployment workflow and direct binary uploader |
| Produce business and engineering handoffs | **Document** | functional and implementation templates |
| Plan a portable rule package | **Export** | import/export contract |
| Review an incoming package | **Import** | import/export contract and import assessment |
| Commit reviewed source | **Commit** | repository lifecycle and explicit `COMMIT` gate |

Use the smallest set of routes that completes the request, but never omit
Explore before a field-based Assess, Create, or Update. A full delivery can
flow through Explore, Discovery, Assess, Create or Update, Validate, Build,
Deploy, Document, and Commit.

## Project workspace

Resolve `project/{project_id}` before a durable run. When implementation work
has no project, route creation through
`core.project-mgmt.project-workspace-initializer` with a skill-derived ID. Do
not derive the ID from free-form prompt wording or require the user to supply
one. Use the resolved technical target:

- Redwood page: `vblens-express-mode-<application>-<flow>-<page>`;
- dynamic layout: `vblens-express-mode-<owner>-<layout>`;
- target not yet resolved: `vblens-express-mode-<date>`.

For example, the Promote target resolves to
`vblens-express-mode-employment-change-update-promote`. Use:

```text
project/{project_id}/artifacts/shared/extensibility/vblens-express-mode/current/
```

Store proposals and reports under `reports/`, documents under `documents/`,
portability work under `exports/` or `imports/`, and sanitized failures under
`diagnostics/`. Register durable artifacts and write a run record.

Store immutable runtime and REST evidence in the shared local cache at
`project/.vblens-cache/`. The cache keys entries by environment and deployed
version. App-info still proves the current environment and deployed version
before each runtime lookup. Never reuse a partial entry, an unmatched
environment or version, or an entry without a valid `COMPLETE` marker.

## Explore

Run `scripts/investigate_express_evidence.js` before selecting a technical
solution. It calls Fusion app-info first, builds or reuses the shared cache,
walks the exact page and fragment graph, proves the Dynamic Form binding, reads
Business Rules and data descriptions, inventories the customer Extension, and
calls one REST describe only after the service and resource are resolved from
page evidence.

When the request supplies a business concept but no verified field path, the
investigator returns `selection_required` with a compact field index. This is a
successful discovery continuation, not a failed or blocked Explore. Search the
index by the user's terminology, read the exact matching layout, data
description, and Business Rules source, select the field semantically, and
rerun with `--field`. Do not try to resolve every unrelated runtime-graph
warning. An unresolved item blocks only when it intersects the selected
field's evidence closure.

After one exact field is selected, the investigator derives one REST describe
target from the deployed dynamic-layout service binding and service catalog
when the match is unambiguous. Supply explicit `--rest-*` options only when
automatic resolution reports no match or multiple matches. Generated `build/`,
`dist/`, and `webApps/` content is never treated as editable Extension source.

For a field-based rule, all of these gates must pass:

- exact deployed page source and page attributes;
- an `oj-dyn-form` bound to the selected dynamic layout;
- exact Business Rules, data-description, field-operation, and import evidence;
- exact REST resource and attribute evidence;
- matching environment and deployed-version provenance.

The Explore output always sets `proposalAllowed` to `false` and
`implementationSuggestion` to `null`. A successful exploration routes to a
separate Assess step. The central REST client starts the existing
`core.auth.fusion-oauth-authentication` flow when authentication is needed. If
authentication fails, classify the failure as auth or authz and repeat the
exploration only after the login issue is resolved. Do not substitute examples,
tests, chat statements, or a similar page for any missing gate.

## Capability Discovery and Assess

Run `scripts/inspect_express_capabilities.js` against the exact page or layout.
Use `assets/templates/capability-summary.md` for supported business choices.

For a requested behavior, run
`scripts/resolve_solution_contract.js --intent <intent> --json`, inspect the
exact target evidence, and record conclusions in the evidence ledger. Use
`assets/templates/feasibility-report.md` for the internal assessment. Classify
each item as supported, supported with setup dependency, unsupported, unresolved,
or outside Express Mode.

Assess must consume a successful exploration report. It must not derive a
calculation, percentage scale, accessor, endpoint, or destination path while a
required exploration gate remains incomplete.

Read these references when relevant:

- [business-rules-authoring.md](references/business-rules-authoring.md) for fields, accessors, defaults, validations, and Advanced Expressions;
- [discovery-and-flexfields.md](references/discovery-and-flexfields.md) for services, LOVs, DFFs, EFFs, languages, and lookup values;
- [field-evidence-and-shape-contracts.md](references/field-evidence-and-shape-contracts.md) for evidence-domain separation;
- [setup-mapping-and-defaulting.md](references/setup-mapping-and-defaulting.md) for setup-driven mappings and overwrite policy;
- [source-intelligence-map.md](references/source-intelligence-map.md) before using a stored example or exception.

## Explain

Read all active Oracle and Extension rules, imported Advanced Expressions,
Page Properties, and layout artifacts contributing to the target. Apply
[effective-configuration.md](references/effective-configuration.md) to resolve
order, status, conditions, actions, messages, and source layer. Explain the
effective behavior in business language and identify conflicts, inactive rules,
and unresolved expressions.

## Create and Update

Create and Update cover:

- simple, nested, If/Else, and Switch Business Rules;
- defaulting and validation-message rules;
- Advanced Expressions and their imports;
- rule-set layouts, field order, containers, and sections;
- evidence-backed Page Properties and conditional Page Property rules;
- Guided Journey properties when the page proves the property contract.

Resolve the exact customer destination with
`scripts/resolve_business_rule_destination.js`. Create a missing minimum
overlay only when one exact Oracle counterpart is proven. Use a simple inline
expression when it remains clear; select an Advanced Expression when helper
values, branches, loops, mapping, or shape normalization are required.

The durable `assets/templates/change-proposal.md` must retain exact files,
complete code, identifiers, imports, evidence, source hashes, setup values,
test cases, and deployment targets. Recheck those facts immediately before
editing. Preserve unrelated ordering and content.

Create and Update are blocked unless the approved proposal cites a successful
exploration report for the same environment, route, deployed version, fields,
and REST resource.

## Runtime, REST, and Setup Evidence

Use `scripts/investigate_express_evidence.js` as the normal entry point. It uses
`scripts/fetch_runtime_evidence.js` to build or reuse the immutable shared
cache after app-info resolves the current deployed version. A user may supply a
relative Redwood route such as
`/fscmUI/redwood/employment-change/update/promote`; pass it as `--target-route`
so the Fusion host is resolved only from `core/auth/fusionEnv.properties`.
App-info uses the central REST client. Oracle CDN bundle requests remain
anonymous and fixed-origin. Read the manifest before cached modules and follow
[runtime-question-answering.md](references/runtime-question-answering.md).

Oracle CDN transport is proxy-aware by default. It honors `HTTPS_PROXY` or
`ALL_PROXY` and `NO_PROXY`, then evaluates the macOS system PAC through
CFNetwork for the exact Oracle CDN URL when no environment proxy applies.
`--cdn-proxy` remains an optional anonymous HTTP proxy override; callers do not
need to pass `--cdn-proxy auto`. Resolution fails closed for credentials,
unsupported proxy types, non-Oracle targets, or invalid PAC output. The proxy
applies only to approved Oracle CDN bundle requests; it never receives Fusion
REST credentials or OAuth traffic.

The REST adapter delegates cached-token checks and interactive login to the
existing `core.auth.fusion-oauth-authentication` flow through the central REST
client. When authentication is needed, complete that login before continuing
the same exploration.

Use `scripts/fetch_service_evidence.js` for one selected REST resource describe.
Use `scripts/resolve_setup_value.js` for active or installed languages and
standard or common lookup codes. Both use `core.fusion-api.rest-api-client` via
`scripts/fscr_rest_client.js`; normal JSON POST calls must use the same path.

This skill does not use browser automation. Missing observed runtime
shape remains unresolved and does not erase coherent static evidence.

## Validate and Test

Run `scripts/validate_extension_changes.js` against the intended integration
base and pass an evidence manifest when the Oracle counterpart exists only in
cache. Validate JSON, JavaScript, imports, identifiers, messages, artifact
ownership, Page Properties, layouts, containers, path safety, conflicts, and
secret leakage.

Test applicable positive, negative, null, unchanged, boundary, setup-missing,
duplicate-match, and overwrite cases. Run available repository tests and
`git diff --check`. Record `assets/templates/verification-report.md`. Block
Build, Deploy, and Commit on unresolved findings.

## Build and Deploy

Read [local-vx-build-and-deploy.md](references/local-vx-build-and-deploy.md).
Build with `scripts/build_vx.js`, an expected reviewed HEAD, a clean-worktree
requirement, and dependencies already present. Report the archive identity,
snapshot selector, hash, size, entry count, source commit, and warnings.

Deployment is a mutating external operation. Immediately before upload,
present the environment and host from `fusionEnv.properties`, fixed endpoint,
immutable archive identity, and every target route. Require exact approval,
then run `scripts/deploy_express_mode.js --token-cache <local-cache>
--confirm-deploy`.

The direct `scripts/upload_vx.js` path is the sole transport exception because
the central client accepts JSON, not raw archives. It accepts only the fixed VX
endpoint, streams one archive, sanitizes the response, and never retries. URL
generation preserves route queries and fragments while replacing only the
snapshot selector.

## Document, Export, and Import

Use `assets/templates/functional-documentation.md` for business users and
`assets/templates/implementation-record.md` for engineering handoff.

Follow [import-export.md](references/import-export.md). Export verifies the
selected rules, dependencies, compatibility, mappings, and checksums, then
returns a portable plan and manifest design. Import treats content as untrusted,
compares target compatibility, and produces
`assets/templates/import-assessment.md` before routing approved integration
through Create or Update.

## Commit

Require a later message beginning with `COMMIT`. Recheck the reviewed source,
validation result, build state, deployment state when relevant, and working-tree
hashes. Stage only approved Extension source files, exclude generated output,
caches, credentials, and unrelated changes, and create one commit. Do not push.

## Boundaries

- Read environment identity and OAuth settings from
  `core/auth/fusionEnv.properties`.
- Route normal authenticated Fusion REST calls through the central REST client.
- Never send Fusion credentials to the Oracle static CDN.
- Never execute downloaded or imported JavaScript during inspection.
- Never install dependencies, skills, hooks, or browser components.
- Do not add custom telemetry or a second token-usage path.
- Do not use browser automation or interactive page control.
- Do not modify Advanced Mode-only pages, fragments, action chains, services,
  backends, or dependencies.
- Do not retry or poll a VX upload.
- Do not push Git branches.

## Preflight checks

Before network, project-write, source mutation, build, upload, or Git effects,
confirm safe paths, project identity, repository state, exact page and layout,
environment identity, privilege and token-cache state, artifact size limits,
successful exploration status, evidence sufficiency, source hashes, validation status, installed pinned build
tools, and the required approval gate. Fail closed on ambiguity.

## Failure handling

Classify failures as `input_validation`, `catalog_or_metadata_mismatch`,
`auth_expired_or_invalid`, `authorization_or_privilege`,
`transport_or_environment`, `fusion_api_error`, `process_timeout`,
`process_failed`, `artifact_persistence`, or `approval_blocker`.

Read-only Fusion calls may refresh a rejected cached token once through the
central client. Never retry a live mutation without an idempotency contract and
fresh approval; the VX upload is always one-shot. Preserve partial evidence and
record sanitized diagnostics under the project workspace.

## Verification contract

Report checks as Passed, Failed, Not run, or Not applicable. Cover manifest and
contract validity, cache hashes, safe paths, target resolution, behavior
scenarios, Extension validation, build source binding, archive identity, upload
request count, response redaction, URL preservation, documentation or package
integrity, Git scope, and `git diff --check` as applicable.
