# Candidate Security Profiles Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EnabledFlag | N | An eligible create omits EnabledFlag; do not prompt, apply to updates, or overwrite an explicit value | No | |
| Unselected security dimensions | N for each unselected SecureBy flag; no detail rows when no criteria are selected; retain the required detail CSV header | An eligible create omits the corresponding dimension; selected dimensions still require resolved values; never replace existing update criteria | No | |
| ViewAllFlag | N | An eligible create omits ViewAllFlag; never apply this default to an update or overwrite an explicit value | No | |
| Profile description | No default | Description is omitted | No | |
| Dimension flag selected by supplied criteria | Y for the corresponding supported dimension when criteria are supplied and the flag is omitted, on creates and updates | Allow activation from exported N to Y. An explicit N conflicting with supplied criteria is rejected; without supplied criteria preserve omitted flags | No | |
| Omitted update fields and criteria | Preserve omitted exported settings and all existing criterion rows; no update defaults | Existing-profile updates; includes Name, Description, EnabledFlag, ViewAllFlag, and every SecureBy flag. Apply only requested EnabledFlag and supported SecureBy flag changes or criterion-derived activation; other setting changes remain unsupported | No | find_candidate_security_profile_by_name |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CSP.APPLY_DEFAULTS | step | 35 | apply_default | applied->CSP.CHECK_VIEW_ALL;not_applicable->CSP.CHECK_VIEW_ALL | CSP.VALIDATE_INPUTS | stop | After classification and field validation; preserve omitted update data and apply only applicable create defaults |
