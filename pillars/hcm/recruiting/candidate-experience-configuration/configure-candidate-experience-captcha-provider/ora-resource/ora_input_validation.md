# Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Configuration records | One or more ordered records, each with configurationName and configurationCode | Stop before dependency readiness. | Provide a non-empty Name and Code within their verified maximum lengths for every requested record. | A Draft preview or controlled multi-provider import is requested. | |
| Provider selection | provider for every requested record | Stop before dependency readiness. | Provide the supported hCAPTCHA provider for every requested record. | A Draft preview or controlled multi-provider import is requested. | |
| Export request | Explicit task-level export request | Stop before export routing. | Explicitly request the task-level export. | A task-level export is requested. | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A post-import reconciliation is requested and a fresh task export is supplied. | The evidence must identify the requested Code and Name exactly, plus Provider ID and Draft status, for every requested record. | Continue to reconciliation evaluation. | |
| A post-import reconciliation is requested without a fresh task export. | Invalid. | Stop and provide the fresh post-import task export. | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| configurationName | Reject an empty value, a value longer than 240 characters, or a value duplicated within the requested batch. Retain each accepted value unchanged for fresh-target collision review. | configurationName is supplied for any requested record. | |
| configurationCode | Reject an empty value, a value longer than 200 characters, or a value duplicated within the requested batch. Retain each accepted value unchanged for fresh-target collision review. | configurationCode is supplied for any requested record. | |
| configurationDescription | Accept an omitted or blank value. Reject a value longer than 1000 characters. | configurationDescription is supplied for any requested record. | |
| provider | Reject a value other than hCAPTCHA. | provider is supplied for any requested record. | |
| Requested status | Reject an Active status request. Draft is derived for every requested record in the supported initial outcome. | A status is supplied or inferred for the initial outcome. | |
| Sensitive or environment input | Stop before configuration preview or import-artifact generation and redact any Site Key, Secret Key, token, tenant-specific URL, customer configuration value, Fusion credential, session data, or environment identifier. | A configuration preview or import input includes a prohibited value. | |
| User-requested task-level export | Allow the routed task-level export without a second protected-data confirmation or approval. Do not apply configuration-input validation to the export request. A theoretical risk, stale blocker, or unrelated workspace file is not an export-input validation failure. | An export is explicitly requested. | |
| Batch shape | Reject an empty batch, a duplicate configurationCode or configurationName, or a record that fails any required field rule. Do not omit an invalid record and submit the remaining subset. Preserve the caller-supplied record order in the CSV. | A provider-header CSV is prepared. | |
| Character and message behavior | Other than the documented per-record maximum lengths and batch-local configurationCode and configurationName uniqueness, do not apply an additional character, whitespace, Unicode, or message-text rule. Fresh-target Code and Name collision checks are enforced by the Minimal-Delta Import Contract. | Always | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAPTCHA.VALIDATE_INPUT | step | 10 | validate_input | valid->CAPTCHA.CHECK_DEPENDENCIES;export_requested->CAPTCHA.GATE_EXPORT;invalid->CAPTCHA.HANDLE_INPUT_ERROR | none | stop | A task-level export, non-secret Draft preview, or controlled multi-provider import is requested. A potential but unobserved export value is not invalid input. |
| CAPTCHA.RECONCILE_EXPORT | step | 60 | evaluate_result | reconciled->CAPTCHA.DONE_RECONCILED;mismatch->CAPTCHA.HANDLE_RECONCILIATION_ERROR | CAPTCHA.ENFORCE_DESIGN | stop | A fresh post-import task export is supplied to reconcile every requested provider record. |
