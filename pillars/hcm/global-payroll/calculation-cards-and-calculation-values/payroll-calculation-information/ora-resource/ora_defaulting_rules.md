# Wage Basis Rules Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Common Create start propagation | Reuse the user's explicit request-wide Create start | Component has no explicit component-specific start; establish during intake before date-sensitive discovery | No | |
| Included/Excluded encoding | Included=P; Excluded=N | User explicitly supplied inclusion for each component | No | |
| Create effective end | Explain No end date (open-ended); omit EffectiveEndDate from Create DAT and expect 4712-12-31 in full-year REST readback | Create with no requested finite end; never replace a supplied finite end | No | |
| Effective dates in DAT | Render each selected full-year business date as YYYY/MM/DD; normalized internal/readback dates remain YYYY-MM-DD | Native TaxabilityRule only; preserve each component's selected start | No | |
| Unused context slots | Empty, preserving slot order | Current reference metadata proves that slot inactive | No | find_wbr_reference_level |
| Correction dates | Retain both actual physical dates of the explicitly resolved existing version | Correct; an as-of selection identifies the version but does not replace either date | No | read_wbr_history |
| Whole-history Delete identity dates | Retain the verified selected version's actual dates; if no version was selected, use the latest version in the completely verified history solely as a native identity anchor | Explicit whole-history Delete with no unresolved date-limited intent; never require a user-supplied deletion date | No | read_wbr_history |
| Update/Correct future-change control | SET PURGE_FUTURE_CHANGES N | Supported inclusion-only Update or Correct | No | |

No invented default for environment, LDG, component, classification, effective start,
active context, inclusion, all-secondaries selection, or destructive intent.
Do not default a missing secondary to none when eligible choices remain.
Physical dates, IDs and stored context codes come from current reads, not
historical fixtures. Do not globally impose this BO's date format on other BOs.

Common-start propagation reuses an explicit business instruction; it is not a
fallback to today or the as-of lookup date. A component-specific start wins.
For example, 01-Feb-2026 is normalized to 2026-02-01 and serialized as
2026/02/01. Neither formatting nor all-secondary expansion changes that date.
Do not ask the user for the open-ended sentinel, author it as an extra Create
column, or imply that later End Date is supported. A requested finite end is
pending under the design boundary and must not be discarded.

History-derived dates require full-year physical verification under the
reference contract. The Delete anchor is a serialization convention, not a
version selection for destruction: all versions of the selected logical rule
are removed. Neither this convention nor Correction date retention defaults
the operation, target, desired inclusion or whole-history intent.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WBR.APPLY_DEFAULTS | step | 5 | apply_default | applied->WBR.VALIDATE_NATIVE_CONTRACT;blocked->WBR.HANDLE_ERROR | WBR.CHECK_PREPARATION | stop | Apply only documented conditional values after business-readiness checks; read/reconciliation changes no values |
