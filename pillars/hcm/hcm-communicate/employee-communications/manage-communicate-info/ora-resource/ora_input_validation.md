# Manage Communicate Info Input Validation

This executable validation scope covers Campaign Management numbering only.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Campaign number generation | Campaign Number Generation Method; Campaign Number Starting Value when explicitly supplied | Stop when the generation method is missing or a supplied starting value is invalid | Supply Automatic, Manual, ORA_CAMP_GEN_METHOD_AUTO, or ORA_CAMP_GEN_METHOD_MANUAL; validate any supplied starting value | Reviewing or changing Campaign Management numbering | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Campaign Number Generation Method is supplied and valid | Ready | Continue to campaign-number dependency readiness | |
| Campaign Number Generation Method is missing or unsupported | Blocked | Supply Automatic or Manual | |
| Campaign Number Starting Value is supplied and valid | Ready | Preserve the supplied value in the reviewed configuration | |
| Campaign Number Starting Value is supplied and invalid | Blocked | Supply a positive whole number matching ^[1-9][0-9]*$ or omit it from the requested change | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Campaign Number Generation Method | Map Automatic or ORA_CAMP_GEN_METHOD_AUTO to ORA_CAMP_GEN_METHOD_AUTO; map Manual or ORA_CAMP_GEN_METHOD_MANUAL to ORA_CAMP_GEN_METHOD_MANUAL; reject any other value | A generation method is reviewed or changed | |
| Campaign Number Starting Value format | Accept only a positive whole number matching ^[1-9][0-9]*$; reject blank, zero, negative, signed, decimal, whitespace-containing, and non-numeric values before import preparation | A starting value is explicitly supplied | |
| Unrequested starting-value change | Preserve the current Campaign Number Starting Value when the request changes only the generation method | Only the generation method is requested to change | |

## Post-Action Validation

| Action | Source-Backed Check | If Evidence Is Missing or Fails | Next Action |
|---|---|---|---|
| FSM CSV import initiation | Fusion returns an accepted initiation response for the approved immutable archive | Do not claim that the setting is verified | Stop without retrying and perform a fresh task-level CSV export when verification is requested |
| Task-level CSV readback | ORA_HCO_CAMP_NUM_AUTO_GEN_FLAG equals the requested backing value and ORA_HCO_CAMP_NUM_INIT_VALUE equals the reviewed value | Report the mismatch and do not resubmit automatically | Review the readback values and prepare a new immutable preview only if another change is required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MCI.VALIDATE_INPUT | decision | 1 | validate_input | valid->MCI.CHECK_DEPENDENCIES;invalid->MCI.HANDLE_ERROR | none | stop | Campaign-number generation values are reviewed |
| MCI.EVALUATE_RESULT | decision | 7 | evaluate_result | verified->MCI.RETURN_SUCCESS;issues->MCI.HANDLE_ERROR | MCI.EXECUTION_GATE | stop | A supported FSM import result or task-level CSV readback is evaluated |

## Open TBD Items

| TBD Item | Owner | Blocker | Next Action |
|---|---|---|---|
| Campaign Number Starting Value precision | HCM Communicate ADF owner | The exact ADF precision is absent; no undocumented maximum is enforced by this workflow | Provide the source-backed precision if a maximum-length rule is required |
