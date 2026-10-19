---
skill_id: "hcm.benefits-configuration.benefits-alerts"
name: "Benefits Alerts"
description: "Enable or disable only the 14 approved Benefits alerts through Alert Foundation; excludes alert creation, deletion, copying, delivery, and template changes."
layer: "pillar"
pillar: "HCM"
type: "orchestration"
execution_mode: "hybrid"
owner_team: "HCM Benefits Configuration pillar team"
version: "0.2.0"
inputs: ["implementation_objective", "project_context", "target_environment", "operation", "alert_codes"]
outputs: ["validated_business_intent", "execution_preview", "execution_result", "verification_result"]
depends_on: ["hcm.hcm-tool.alert-foundation"]
uses_core: []
persists_project_state: false
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact accounting is available"
  required_fields: ["activity_start_time", "skill_id", "task", "trigger", "artifacts_written", "files_read", "estimated_input_tokens", "estimated_output_tokens", "estimated_total_tokens", "estimation_method", "notes"]
side_effects:
  - "Delegates read-only alert resolution to Alert Foundation."
  - "May enable or disable an allowlisted existing alert only through Alert Foundation after its exact preview is approved."
required_privileges:
  - "Target-environment access to inspect and update the selected alerts, validated by Alert Foundation."
---

# Benefits Alerts

## Scope

Use this consumer skill only to enable or disable existing Benefits alerts.
The exact allowlist in [the intake guard](scripts/benefits_alert_scope.py) is:

- BEN_BILL_CHARGES
- BEN_BILL_PAYMENT
- BEN_PENDING_ACTIONS_NOTIFICATION
- BEN_SELF_REPORTED_LIFE_EVENT_APPROVED
- BEN_COURT_ORDER_DEPENDENT_CREATED
- BEN_REPORT_LIFE_EVENT
- BEN_COURT_ORDER_DEPENDENT_ENDDATED
- BEN_DOCUMENT_APPROVAL
- BEN_OPEN_NOTIFICATION
- BEN_OPEN_REMINDER
- BEN_SELF_REPORTED_LIFE_EVENT_REJECTED
- BEN_SELF_REPORTED_LIFE_EVENT_INFO_REQD
- BEN_SELF_REPORTED_LIFE_EVENT_SUBMIT
- BEN_ELECTIONS_SUMMARY

A BEN_ prefix alone is insufficient. Reject any other code, wildcard, unknown
field, or operation. Do not silently filter an invalid mixed selection.
For an explicit request for all Benefits alerts, expand to exactly this list and
show the complete selection before approval. Otherwise ask for missing codes
or the desired enable/disable operation; never infer a toggle from current state.
Different desired states require separate validated selections.

## Provider workflow

Before external access or approval, run the read-only
[provider compatibility check](scripts/check_provider_compatibility.py):

```sh
python3 pillars/hcm/benefits-configuration/benefits-alerts/scripts/check_provider_compatibility.py
```

A nonzero result blocks execution. This checks transport call shape only, not
provider readiness or authorization. Do not modify Alert Foundation, monkey-patch
its runtime, or bypass its executor to work around a failure. Report a provider
compatibility blocker before asking for mutation approval. A successful check
still requires every provider gate below, including contract-version consistency.

1. Read [Alert Foundation](../../hcm-tool/alert-foundation/SKILL.md) and its
   [consumer contract](../../hcm-tool/alert-foundation/references/provider-contract.md).
   It owns current contract version, routing, metadata, identity resolution,
   immutable previews, approval, execution, verification, and redacted evidence.
   Do not copy its REST schema, call endpoints directly, or select another
   transport. Inconsistent provider versions or unsupported contracts are
   blockers, not permission to guess a version.
2. Establish the existing implementation project and exact target environment
   through the active workflow. Run the local intake guard before provider
   reads with JSON containing only operation and alert_codes:

   ```sh
   python3 pillars/hcm/benefits-configuration/benefits-alerts/scripts/benefits_alert_scope.py --input-stdin
   ```

   Example input: `{"operation":"enable","alert_codes":["BEN_OPEN_REMINDER"]}`.
   This helper performs no I/O beyond stdin/stdout, no Fusion calls, and grants
   no approval. Its output is business intent, not a complete provider request
   or REST payload.
3. Invoke the provider with consumer_skill_id
   hcm.benefits-configuration.benefits-alerts, project identity, objective,
   target environment, and each validated alert intent. Enable maps to provider
   update with desired enabled true; disable maps to disable with enabled false.
   Sequential existing-item processing only; never use batch-create.
4. Ask the provider to resolve each exact code to exactly one existing alert,
   obtain fresh state and canonical identity, and complete its existing-item
   gates. Missing or ambiguous alerts block the selection; do not create them.
   Preserve current name, test mode, access level, and every other setting.
   Where the provider requires these values in its logical request, obtain
   them from its read evidence rather than defaulting or requesting changes.
5. Validate the entire selection before its first write. An alert already in
   the requested state is unchanged and needs no mutation. For each remaining
   alert, inspect the provider-owned immutable preview: it must refer to the
   exact resolved allowlisted parent and change only EnabledFlag. Reject any
   child operation, extra changed field, mismatched code, or environment change.
   This is a restriction on the provider preview, not consumer payload building.
6. Present current and desired state, environment, and provider verification
   plan. Obtain the provider's individual approval for each exact mutation;
   generic prior consent or this skill's creation does not authorize writes.
   Enabling permits future configured alert processing; it does not itself
   authorize invoking notification delivery.
7. Delegate one submission and independent read-back to the provider. Require
   the same exact alert code and desired enablement in verified evidence.
   Preserve provider statuses and artifact references. Report each selected
   code as verified enabled/disabled, unchanged, failed, unverified, or not
   attempted. Never equate an accepted response with verified completion.

## Failure and recovery

- Invalid input: block before any provider call; identify the offending field
  without reflecting arbitrary payloads. The guard exits 1 on invalid input
  and 0 on valid business intent. Duplicate codes and empty selections fail.
- Missing metadata, identity, or provider readiness: return a blocker; no
  fallback to HDL, Data Loader, browser, or direct REST execution.
- Authentication, access, transport, or API failures: preserve the provider's
  failure class and redacted recommended action. Its bounded read retry and
  single permitted token-refresh policy remain authoritative.
- Stale state or preview changes: stop and obtain a fresh provider preview and
  approval. Do not expand the approved selection or change another setting.
- Failed or uncertain writes/read-back: stop before the next write, retain
  verified successes, and reconcile through provider reads. Do not retry a
  write or roll it back automatically. Recovery needs fresh approval.
- Timeout: report the last known result as unverified, not success. This is
  synchronous provider verification, not a background load to poll indefinitely.
- Artifact persistence or approval failure: stop before execution. The provider
  owns durable project evidence; do not duplicate its run records or store
  credentials, tokens, or customer records in this skill.

## Verification and ownership

Run [offline scope tests](tests/test_benefits_alert_scope.py). They verify the
local allowlist and business-intent boundary only; live provider authorization,
preview integrity, and read-back must still pass at runtime. No shared provider
code is modified by this consumer.

Reviewers: Benefits Pillar Lead/SME and FSCR A-Team/core reviewer. Keep catalog
identity unchanged; this consumer does not introduce a new FSM task code.
