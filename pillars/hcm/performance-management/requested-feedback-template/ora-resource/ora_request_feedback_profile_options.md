# Mandatory Request Feedback Profile Options

Use this route for every Requested Feedback Template Run Book. It is a
functional-area baseline and does not depend on the consultant source naming
the profiles.

## Required SITE values

| Profile option | Required configured value | Purpose |
|---|---|---|
| `HRA_REQUEST_FEEDBACK_ENABLED` | `Y` | Enables Request Feedback |
| `ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED` | `Y` | Enables Redwood Request Feedback |

The configured REST value is the literal `Y`. A user interface may render that
value as **Yes**; do not send `Yes` in the profile-option payload.

## Run Book mapping rule

Use the effective-catalog setup task:

- task name: `Manage Administrator Profile Values`
- task code: `FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`
- offering: `Performance Management`
- functional area: `Performance Management Common`
- route: `core.fusion-api.apps-common.profile-options`

Read both exact profile definitions and SITE values before mapping when the
routed target is available.

- If both values are verified as `Y`, record verified no-change and omit the
  profile task.
- If either value is non-`Y`, absent, or not yet verifiable, add exactly one
  profile task as the first Run Book task. Unknown state is a verification gate,
  not evidence of compliance.
- Put both profile codes, current values or `unknown`, desired value `Y`, and
  evidence references in the task notes. Do not create duplicate setup-task
  rows for the two profiles.

The leading task must complete with both profiles verified as `Y` before a
dependent Questionnaire or Feedback Templates mutation proceeds.

## Read, preview, and write route

Use `core.fusion-api.apps-common.profile-options`, not FSM export/import:

1. Read each exact definition through `profileOptions` and its SITE record
   through `siteProfileOptionValues`.
2. Validate the exact profile code, `SiteLevelEnabled`, current SITE value,
   required value `Y`, and available write authorization. An explicit false
   `SiteLevelUpdatable` blocks the profile write. If that field is omitted, use
   the scoped provider contract and record updatability as not returned, not as
   proven true.
3. Re-read immediately before preview. If the current value is already `Y`,
   record verified no-change and send no write.
4. For an existing non-`Y` SITE record, preview a PATCH to the exact `SITE`
   child with `{"ProfileOptionValue":"Y"}`. For a confirmed absent SITE record,
   preview the provider-supported SITE POST with the same desired value.
5. Present the target environment, exact endpoint, method, current value,
   payload, and validation result. Obtain fresh explicit approval for each exact
   write immediately before dispatch.
6. Dispatch once, never retry automatically, and read back the exact SITE value.
   Mark the prerequisite complete only after both values are verified as `Y`.

If identity, SITE state, authorization, or write capability cannot be resolved,
classify and persist the observed failure and stop the dependent external step.
Do not infer success, fall back to generic import/export, or silently continue
to a dependent mutation.

## Scope boundary

`ORA_HRG_REQUEST_FEEDBACK_ENABLED` is a separate Request Feedback for Goals
profile. Continue to use `ora_request_feedback_goals_profile_option.md` only
when that goal-specific profile is explicitly in scope; it does not satisfy or
replace either mandatory profile above.
