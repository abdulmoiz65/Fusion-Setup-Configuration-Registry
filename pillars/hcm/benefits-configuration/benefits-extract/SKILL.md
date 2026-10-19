---
skill_id: "hcm.benefits-configuration.benefits-extract"
name: "Benefits Extract"
description: "Prepares, approves, submits, and monitors supported Benefits Extract ESS processes through the shared ESS Job Submitter."
layer: "pillar"
pillar: "HCM"
type: "import"
execution_mode: "hybrid"
owner_team: "HCM Benefits Configuration pillar team"
version: "0.5.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "fusion_environment_context"
  - "effective_date"
  - "carrier_id"
  - "extract_type"
  - "transmit"
  - "ess_execution_options"
  - "execution_approval"
outputs:
  - "ess_request_id"
  - "ess_status"
  - "ess_response"
  - "diagnostics"
  - "audit_summary"
  - "implementation_gap"
depends_on:
  - "core.fusion-api.ess-job-submitter"
  - "core.fusion-api.rest-api-client"
uses_core:
  - "core.fusion-api.ess-job-submitter"
  - "core.fusion-api.rest-api-client"
persists_project_state: true
state_updates:
  - "validation_results"
  - "reports"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "other"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-extract/current/"
    versioning_policy: "append-only"
  - artifact_type: "report"
    default_location: "project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-extract/current/"
    versioning_policy: "append-only"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields: ["activity_start_time", "skill_id", "task", "trigger", "artifacts_written", "files_read", "estimated_input_tokens", "estimated_output_tokens", "estimated_total_tokens", "estimation_method", "notes"]
side_effects:
  - "After explicit approval, submits one confirmed Benefits Extract ESS request through core.fusion-api.ess-job-submitter."
  - "Polls the submitted or explicitly supplied ESS request until terminal status or the approved timeout."
required_privileges:
  - "Fusion privileges to submit and monitor the confirmed Benefits Extract scheduled process."
---

# Benefits Extract

## Purpose

Use this skill only to run or track the `Extract Benefits Data` scheduled
process.

This skill owns the Benefits-specific selection of the scheduled job, its exact
Oracle package and job definition, and the ordered business-parameter mapping.
It delegates authentication, Scheduler REST submission, request-ID capture,
polling, terminal-state evaluation, and response redaction exclusively to
`core.fusion-api.ess-job-submitter`. Do not create or use a Benefits-specific
ESS REST client or submitter.

## Fixed Scheduler Contract

The consuming skill—not the user—always supplies this exact Scheduler job
identity. Reject an override for any of these values.

| Field | Fixed value |
|---|---|
| Scheduled process | `Extract Benefits Data` |
| Job definition ID | `JobDefinition://oracle/apps/ess/hcm/benefits/processes/BENEXTPROC` |
| Application | `EarHcmEss` |
| Product | `BEN` |

Do not take user input for `jobDefinitionId`, application, or product. Do not
substitute a similarly named scheduled process.

The product-owned mapping for `Extract Benefits Data` is fixed as follows. Keep
these parameters in this order in `requestParameters`; do not renumber them.

| User input | Scheduler parameter | Type | Payload value |
|---|---|---|---|
| Effective Date | `submit.argument2` | `STRING` | Parsed then formatted as `YYYY-MM-DD` |
| Carrier ID | `submit.argument1` | `STRING` | Supplied Carrier ID |
| Extract Type | `submit.argument4` | `STRING` | Resolved `BEN_EXT_TYP` LookupCode |
| Transmit | `submit.argument5` | `STRING` | Resolved `BEN_YES_NO` LookupCode |

Accept a valid user-supplied Effective Date only when it can be parsed without
ambiguity; serialize it as a `STRING` in `YYYY-MM-DD` format before building
the payload. Reject an invalid or ambiguous date instead of sending the
original representation.

The exact payload is limited to these four ordered parameters; do not add,
remove, renumber, or override them:

```json
{
  "jobDefinitionId": "JobDefinition://oracle/apps/ess/hcm/benefits/processes/BENEXTPROC",
  "application": "EarHcmEss",
  "product": "BEN",
  "requestParameters": [
    {"name": "submit.argument1", "paramType": "STRING", "value": "<carrier_id>"},
    {"name": "submit.argument2", "paramType": "STRING", "value": "<effective_date_yyyy-mm-dd>"},
    {"name": "submit.argument4", "paramType": "STRING", "value": "<extract_type_lookup_code>"},
    {"name": "submit.argument5", "paramType": "STRING", "value": "<transmit_lookup_code>"}
  ]
}
```

## Lookup-code Resolution

Before creating a submission payload, resolve the user-facing Extract Type and
Transmit values through `core.fusion-api.rest-api-client`. These are read-only
lookups; this skill must not call Fusion REST directly or implement its own
OAuth handling.

| User input | GET resource | Match and payload mapping |
|---|---|---|
| Extract Type | `/fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=BEN_EXT_TYP&onlyData=true&fields=Meaning,LookupCode&limit=25&offset=0` | Require exactly one returned `Meaning` equal to the supplied Extract Type; map its returned `LookupCode` to `submit.argument4`. |
| Transmit | `/fscmRestApi/resources/11.13.18.05/commonLookupsLOV?finder=LookupTypeFinder;LookupType=BEN_YES_NO&onlyData=true&fields=Meaning,LookupCode&limit=25&offset=0` | Require exactly one returned `Meaning` equal to the supplied Transmit value; map its returned `LookupCode` to `submit.argument5`. |

Use the shared REST client with the relative resource path and repeated query
arguments: `finder=LookupTypeFinder;LookupType=<lookup type>`,
`onlyData=true`, `fields=Meaning,LookupCode`, `limit=25`, and `offset=0`.
Retain the resolved Meaning and LookupCode in the redacted preflight artifact.
Do not send a user-facing Meaning directly to either Scheduler argument.

Stop with `catalog_or_metadata_mismatch` if the lookup call fails, returns zero
matches, returns multiple matches, omits `LookupCode`, or its result cannot be
matched exactly. Do not choose a code, use a stale lookup result, or submit a
partial payload.

For every submission, the consuming skill must retain an immutable mapping
that includes:

1. scheduled-job name `Extract Benefits Data`;
2. the fixed job definition ID, application `EarHcmEss`, and product `BEN`;
3. each business input, its Scheduler parameter name, `STRING` type, resolved
   payload value, and ordinal position; and
4. the resolved `requestParameters` list in that confirmed ordinal order.

The mapping belongs here, in the Benefits Extract consuming skill and its
project artifact. The shared submitter receives the resulting exact payload;
it does not infer Benefits business defaults or parameter mappings.

## Preflight and Approval

Before a new request, require an initialized project workspace with active Run
Book control, target-environment identity, resolved Effective Date, Carrier ID,
Extract Type, and Transmit values, and privileges to submit and monitor
`Extract Benefits Data`.

Validate that every supplied business value maps once to a confirmed Scheduler
parameter. Resolve Extract Type and Transmit to their verified LookupCodes
before building the payload, and serialize Effective Date as `YYYY-MM-DD`.
Reject unknown, omitted required, duplicate, out-of-order, or unresolved
parameters. Build one immutable payload with the fixed Scheduler contract and
review it with the environment, job name, application, product, ordered
parameters, poll interval, timeout, and artifact destination.

Obtain explicit approval immediately before submission. Approval for setup,
another extract, a prior request, or a plan does not approve a new ESS POST.
Any change to the environment, job contract, parameter values, or polling
options invalidates the review.

## Submission and Terminal-status Tracking

After the gate and approval pass, create an `approved_submission` envelope
conforming to `schemas/ess-delegation-contract.schema.json` and invoke
`core.fusion-api.ess-job-submitter` once with the exact product-owned payload,
approved wait time, poll interval, and a unique project-local output path. Do
not use `--submit-only`: every new invocation must poll the returned request to
a terminal status or the approved timeout.

The returned `execution_result.requestId` is the submitted request ID. Return
it immediately and persist it with the selected job name, confirmed contract,
parameter mapping, target environment, and polling settings. Return and persist
the final `execution_result.status` plus the core submitter's diagnostics and
raw/redacted ESS response fields. Do not replace or hide the ESS response with
a Benefits-only success/failure summary.

For an explicit request-status inquiry, invoke the core submitter with only
`--request-id <requestId>` and polling settings. Never turn tracking into a
new submission.

## Failure Handling

- An invalid/ambiguous Effective Date or failed/ambiguous lookup-code resolution
  is an `input_validation` or `catalog_or_metadata_mismatch` failure. Record it
  and stop before approval or submission.
- Surface terminal unsuccessful status as returned by the core submitter,
  including ESS state, process phase, cause, error/warning message, ECID, and
  diagnostics. Preserve the submitted request ID and full redacted response.
- Surface a timeout with the request ID, last response/status, elapsed wait,
  and the read-only request-tracking path. Do not submit again automatically.
- Do not retry a POST after transport uncertainty, timeout, or terminal
  failure. A new submission requires a fresh immutable review and approval.
- The shared core skill alone may refresh a cached token and retry an
  authentication 401/403 once. This skill must not add authentication, REST,
  or polling loops.

Persist redacted execution artifacts under
`project/{project_id}/artifacts/pillars/hcm/benefits-configuration/benefits-extract/current/`
and append the skill run and token-usage records as configured. Never persist
credentials, token-cache contents, authorization headers, or an unredacted
ESS response.
