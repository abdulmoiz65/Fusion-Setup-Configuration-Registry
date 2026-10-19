# Recruiting Agencies Defaulting Rules

## Purpose

Defines the only source-backed default and the Update preservation behavior.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| StatusCode | ORA_ACTIVE | Create is requested and Status is omitted | No | |

## Defaulting Behavior

| Situation | What Happens |
|---|---|
| Create omits Status | Populate StatusCode with ORA_ACTIVE before CSV generation and show it in the preview |
| Create supplies Status | Preserve the supplied target-valid value; do not replace it |
| Update omits Status | Preserve StatusCode from the exact exported row; do not apply the Create default |
| Any other omitted field | Do not invent a default; preserve Update values and validate Create requirements |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RA.APPLY_STATUS_DEFAULT | step | 20 | apply_default | applied->RA.RESOLVE_REFERENCES;preserved->RA.RESOLVE_REFERENCES;blocked->RA.HANDLE_ISSUES | RA.VALIDATE_REQUEST | stop | Create |
