# Legislative Data Group Security Profile Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EnabledFlag | true (Y) | A new profile does not explicitly supply the flag | Yes |  |
| ViewAllFlag | false | Always; the describe metadata marks it non-updateable | No |  |
| Name | Derive a compact meaningful name from the validated configuration: start with LDGSP; infer the geographic scope from the validated LegislativeDataGroupName values; when all selected LDGs clearly indicate one region, append that region once; otherwise append each distinct inferred country scope in configured order; do not concatenate full LDG names; remove every character other than ASCII letters and digits; truncate the result to a maximum of 119 characters | Creating a new profile when Name is not supplied | Yes |  |

The derived Name is intentionally stricter than the source schema's allowance of
at most 240 characters: it must contain only ASCII letters and digits and must
be fewer than 120 characters. Preserve a user-supplied Name exactly as supplied,
including when it is 120 through 240 characters; do not normalize or truncate it.
If a country or regional scope cannot reasonably be inferred from the LDG names,
or derivation produces an empty or non-meaningful name, stop and request a
user-supplied Name; do not substitute full LDG names, punctuation, spaces, or an
opaque identifier.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LDGSP.DEFAULT | step | 6 | apply_default | applied->LDGSP.READINESS;not_needed->LDGSP.READINESS | LDGSP.RESOLVE_LDG | stop | Valid lookup results are available |
