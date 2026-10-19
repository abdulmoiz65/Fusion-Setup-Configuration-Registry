# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Initiating Events: Submit | Selected | A new attestation row is created and no explicit selection is supplied for Submit | Yes | |
| Initiating Events: Resubmit | Selected | A new attestation row is created and no explicit selection is supplied for Resubmit | Yes | |

## Complete Business Summary Default Reporting

The Complete Business Summary must show each default actually applied after validation and lookup resolution. Present the applied default in the Defaults Applied section using its business label and business display value. Do not list a default that was not applied, and do not expose technical fields, identifiers, codes, or rule names.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAS_DEFAULT_EVENTS | step | 20 | apply_default | applied_or_not_needed->TAS_VALIDATE_LOVS;cannot_apply->RETURN_ISSUES | TAS_VALIDATE_FIELDS | stop | A new attestation row is prepared |
