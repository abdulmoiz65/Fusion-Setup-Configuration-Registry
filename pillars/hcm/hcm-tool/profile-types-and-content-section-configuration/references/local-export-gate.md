# Skill-local export gate

Use `scripts/export_profile_setup.py` for every new export initiated by this
skill. It delegates once to the existing shared task-level orchestration script;
it does not implement Fusion transport or change core/shared services.

First complete the skill's scope, catalog, privilege and native-template reuse
checks. Reuse an existing valid empty template for ZIP preparation. Missing
metadata never authorizes a data export. Build this local request object:

```json
{
  "environment": "TEST",
  "restBaseUrl": "https://example.test",
  "task_code": "HRT_MANAGE_PROFILE_TYPES",
  "mode": "template",
  "criteria": [],
  "project_id": "example-project",
  "output_dir": "/repository/project/example-project/exports/hcm-tool/profile-types-and-content-section-configuration/profile-types"
}
```

Allowed modes are `template` and `data`. The only tasks are Profile Types and
Content Subscribers; use the corresponding task directory for the destination.
The example above requests an empty template. For an explicitly requested
current-state snapshot, set `mode` to `data` and obtain approval for that exact
request. The wrapper must pass `--data` to the shared adapter; omission defaults
to template-only and does not retrieve current values. Template mode explicitly
passes `--template-only`. Changing modes invalidates the earlier approval.
Filters must be live-confirmed, explicitly reviewed and normalized with exact
TaskCode. Template mode rejects filters. The source configuration comes from
core/auth/fusionEnv.properties through the core authentication service.

Run `python3 scripts/export_profile_setup.py --request request.json` for a local
plan; this performs no authentication or Fusion call. Present the complete
request to the user, obtain explicit export approval, then create approval JSON
with `approved: true`, a unique `approval_ref` identifying that actual user
approval, and `request` containing the exact reviewed object. Never manufacture
approval or reuse a reference for another operation. Run:

```text
python3 scripts/export_profile_setup.py --request request.json \
  --approval approval.json --execute --token-cache auto
```

The guard records an exclusive attempt reservation in the selected project's
state/runs directory before invoking the adapter. A timeout, exception, unknown
result or process failure does not release that reservation. Do not delete it
or choose a new approval reference to bypass it. Reconcile the returned
ProcessId using the shared GET-only polling route; a new creation requires
fresh explicit retry approval after checking for an existing process. If no
ProcessId was returned, report uncertain submission and stop for reconciliation.
Polling must never re-enter the creation wrapper. The wrapper is not a universal
security boundary against independent callers of shared services.

The selected `export_setup_task_csv.py` orchestration path calls creation once
without catching and replaying it. Do not substitute the shared standalone
creation CLI or generic FSM creation CLI, whose authentication recovery can
repeat creation. Recheck this contract after changes to shared dependencies;
report an unsupported route to its owner rather than patching shared code.

The adapter owns the bounded 300-second wait, 10-second polling, download and
normal result report. Nonzero results remain nonzero. Attempt journals retain
only a request digest, status and returned ProcessIds, never raw logs or tokens.
Approval for this export never authorizes a later import or Jira mutation.
