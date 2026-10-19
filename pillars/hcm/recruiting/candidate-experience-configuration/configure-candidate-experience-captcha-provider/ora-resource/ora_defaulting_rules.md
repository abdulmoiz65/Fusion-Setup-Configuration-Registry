# Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Provider Code | HCAPTCHA | The supported hCAPTCHA provider is selected for every requested record. | No | |
| Provider ID | 2 | The supported hCAPTCHA provider is selected for every requested record. | No | |
| Configuration Status | Draft | The initial supported outcome is prepared or imported for every requested record. | No | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAPTCHA.APPLY_DEFAULTS | step | 30 | apply_default | defaulted->CAPTCHA.ENFORCE_DESIGN | CAPTCHA.CHECK_DEPENDENCIES | stop | Every requested record and its dependencies are ready. |
