# Country Security Profile Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EnabledFlag | true | A new profile does not explicitly supply the flag | Yes | |
| ViewAllFlag | false | Always; the describe metadata marks it non-updateable | No | |
| Name | Derive a meaningful name from the validated configuration: CountrySecurityProfile followed by the validated CountryName values in their configured order; remove every character other than ASCII letters and digits; truncate the result to a maximum of 119 characters | Creating a new profile when Name is not supplied | Yes | |

The derived Name is intentionally stricter than the source schema's allowance of
at most 240 characters: it must contain only ASCII letters and digits and must
be fewer than 120 characters. Preserve a user-supplied Name exactly as supplied,
including when it is 120 through 240 characters; do not normalize or truncate it.
If derivation produces an empty or non-meaningful name, stop and request a
user-supplied Name; do not substitute punctuation, spaces, or an opaque identifier.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.DEFAULT | step | 6 | apply_default | applied->CSP.LAYOUT;not_needed->CSP.LAYOUT | CSP.RESOLVE_COUNTRY | stop | Valid task inputs and country lookup results are available |
