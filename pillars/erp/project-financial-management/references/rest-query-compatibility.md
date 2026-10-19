# REST Request Preflight and Query Compatibility

Apply this preflight before every REST request selected by a Project Financial
Management workflow, including reference lookups, metadata, pagination and
verification. It supplies request-construction checks only; the active workflow
still owns route selection, target/identity/privilege checks, artifacts, approval,
execution and retry gates. A reference example never authorizes a live request.

## Determine the Effective Framework Version

1. Read the selected core client's skill, routed instructions and implementation,
   plus the active workflow's request/header policy. Determine the effective
   `REST-Framework-Version` before constructing the query. The resource release
   segment (`11.13.18.05` or `latest`) is not the REST framework version.
2. Use the owning core client or workflow's version selection. Do not independently
   pin a numeric version in a pillar instruction, script or copied command. If the
   core client accepts headers without choosing a version, obtain the explicit
   version from the active workflow and pass that same value to the client. An
   omitted header is not evidence that expanded query syntax is supported.
3. If the workflow deliberately relies on a server default, require existing,
   target-specific `defaultFrameworkVersion`/`allowedFrameworkVersions` evidence
   from its declared discovery step before using that default. Do not make an
   exploratory request, select a different client or initiate authentication to
   fill this gap. Missing or contradictory version/header evidence blocks the
   affected request until the workflow or core owner resolves it.
4. Retain the selected client/workflow reference, effective framework version,
   header source and query form in the workflow's existing redacted preflight
   evidence. Check the actual outgoing header policy against that evidence before
   execution and keep it consistent across pages.

Current core references to inspect (read these again when selecting a route):

| Selected route | Version authority and required action |
|---|---|
| `core.fusion-api.rest-api-client` standard Fusion CLI | `core/fusion-api/rest-api-client/references/fusion-rest-api.md` and `scripts/rest_client_common.py`: repeated query/header arguments are passed through; no framework header is selected automatically. Supply the active workflow's resolved version, including on lookup GETs. |
| `core.data-loader`, `core.data-loader.task-rest`, `core.data-loader.fscr-task-rest` | Their manifests/instructions own the header policy; the loader implementation exposes `REST_FRAMEWORK_VERSION` in `core/data-loader/scripts/data_loader_metadata.py`. Derive the version from that selected workflow, rather than copying its current value into this pillar. |
| `core.runbook` | Its manifest and `core/runbook/scripts/runbook_http.py` own the request header policy. Use that policy when the workflow selects this client. |
| FSM, ESS or other service-specific core adapter | Inspect its own protocol and query contract first. An ESS scheduler path's `/v1` is not an ADF framework version. Record non-ADF applicability when established by that contract; do not apply ADF `q` grammar or add an ADF header by analogy. A workflow-required header that the selected adapter cannot send is a core blocker. |

The generic CLI's absent default is an unresolved preflight input when the
workflow has not selected a version; the pillar wrapper now blocks that case.
There is also a conditional core conflict: `core.runbook` and `core.data-loader`
require a framework header on every Fusion REST request, while
`core/fusion-api/ess-job-submitter/scripts/ess_job_submitter.py`'s `request_json`
does not send one or accept a framework-header option. If either universal
policy governs the selected ESS step, block that step for core-owner resolution
before submission or status retrieval. Do not inject a pillar header or switch
adapters to bypass the conflict. The standalone ESS contract must be assessed
on its own applicability rather than assigned an ADF version from its URL.

## Construct and Check Query Parameters

- ADF framework version 1 uses query-by-example syntax; version 2 and later use
  expanded expressions. Compound `q` examples in this pillar use the latter:
  `q=Name='<name>' and ClassificationCode='<code>'`. Execute them only when the
  resolved version supports that grammar. If it does not, stop the request for a
  compatible, evidenced workflow contract; do not drop a predicate or change the
  selected framework version to make an example run.
- Preserve every filter, Boolean grouping, null/date test, exact/LIKE matching
  rule and fallback/classification precedence. Do not broaden a query to hide a
  syntax problem. Single equality examples still require the version preflight.
- Treat each parameter according to its own grammar. A finder such as
  `finder=PrimaryKey;BookTypeCode=<code>` or
  `finder=AssignmentFinder;DeterminantValue=<id>,ReferenceGroupName=PJF_RATES`
  keeps its semicolon and bind separators. Semicolons inside quoted names,
  descriptions or other literal values are data. Never globally replace them;
  `fields`, `expand`, finder bindings and `q` are separate contracts.
- Escape literal values for the selected framework's query language first,
  preserving intentional LIKE wildcards and handling literal wildcard/escape
  characters according to that version. Then pass separate `--query key=value`
  arguments to the core CLI for URL encoding. Do not interpolate untrusted text
  into shell commands, split literals on semicolons, or encode a value twice.
- When a core CLI needs an explicit header, use
  `--header "REST-Framework-Version=${workflow_rest_framework_version:?resolve from the selected core workflow}"`.
  This variable is a resolved, non-secret workflow value, not a pillar default.
  Omit this extra argument only when the selected adapter already supplies the
  same header or the workflow has evidenced its deliberate server-default policy.

On a mismatch, stop before authentication/transport and record the blocker and
next action through the existing workflow diagnostics. Do not downgrade a
malformed request to a no-match or successful validation. Existing task-specific
policies for unavailable reference validation still govern whether the remaining
offline work may continue with a disclosed unresolved reference.

## REST Usage Inventory

All task manifests and `ora-resource/ora_reference_lookups.md` files link to this
preflight. REST use is delegated to core services:

| Task area | Usage and pillar scripts/references |
|---|---|
| Project Foundation: project types, roles, statuses, work types | Governed reference/baseline reads and task export/loader handoffs. Status/work-type helpers evaluate evidence locally; they do not send requests. |
| Project Foundation: rate schedules and planning/billing RBS | Reference and capability GETs; approved loader route for changes. RBS package builder is offline. |
| Project Foundation: project templates | REST operation contract in `manage-project-templates/references/project-template-rest-contract.md`; payload validator builds lookup specifications locally, with execution delegated to the selected core workflow. |
| Project Control: project plan types | Reference GETs and approved loader handoff. `prepare_import.py`, `import_preview.py` and `validate_import.py` prepare/validate locally. |
| Project Organizations: unit options, unit organizations, hierarchies/classifications, accounting business function | Governed lookups and export/loader routes. Reference-set, HDL and hierarchy validators consume evidence or construct single-equality URLs locally. |
| Project Organizations: organization classifications | `resolve_project_organization_baseline.py` is the pillar GET wrapper around the core CLI. Its `--rest-framework-version` must come from the selected workflow; it has no numeric default. Other classification helpers are local. |
| Project Organizations: maintain organizations process | `run_maintain_project_organizations.py` delegates the fixed ESS submission/status route to `core.fusion-api.ess-job-submitter`; it does not use ADF collection filters. |

## Oracle Syntax References

- [Set the REST Framework Version (Project Management 26C)](https://docs.oracle.com/en/cloud/saas/project-management/26c/fapap/Setting_the_REST_Framework_Version.html)

Use current available Oracle documentation and the selected target's evidenced
contract when they differ from these references. Documentation lookup does not
authorize a Fusion discovery call.
