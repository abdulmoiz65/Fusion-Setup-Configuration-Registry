# Request Feedback for Goals Profile Option

Use this route only when Requested Feedback Template source evidence explicitly
includes the `ORA_HRG_REQUEST_FEEDBACK_ENABLED` profile option.

## Route

Use `core.fusion-api.apps-common.profile-options`, not FSM export/import, for
this profile option:

1. Read the profile definition and SITE value through the documented
   `profileOptions` and `siteProfileOptionValues` resources.
2. Validate `SiteLevelEnabled`, current SITE value, and the requested new
   value. Use `SiteLevelUpdatable` when returned; an explicit false value
   blocks a change. If omitted, inspect the declared profile provider's
   supported definition/SITE reads and update contract. A SITE-enabled exact
   profile with a readable existing SITE value and a declared SITE PATCH
   contract may proceed to preview without this optional response field.
   Retain applicable same-target successful PATCH/readback evidence when
   available, but do not require historical execution for first-time setup.
   Record updatability as not returned, not proven true. This is a scoped
   consumer rule for this profile, not a change to the shared provider.
   A GET does not prove write privilege: use available current authorization
   evidence and preserve any explicit denial. If already at the requested
   value, report verified no-change rather than sending a PATCH.
3. Present the exact target environment, endpoint, current value, proposed
   value, and validation result.
4. Obtain fresh explicit approval immediately before a SITE-level POST or PATCH.

The default Requested Feedback for Goals value from approved source evidence is
carried unchanged into the preview. Do not infer a value, use an FSM archive as
a substitute for the direct profile route, or apply this route to another
profile option without explicit source scope.

If the exact definition or SITE resource cannot be resolved after the declared
reads, or authorization is denied, stop the dependent action with that observed
failure. An omitted updatability field alone is not a customer-input blocker.
Do not fall back to generic import/export
unless the consultant explicitly requests an FSM migration artifact.
