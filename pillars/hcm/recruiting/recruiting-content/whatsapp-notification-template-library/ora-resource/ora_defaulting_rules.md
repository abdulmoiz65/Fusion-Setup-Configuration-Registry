# WhatsApp Notification Template Library Defaulting Rules

Apply the fixed system values to every base-template creation and classify the proposed Meta category for natural-language requests. Do not collect or accept the fixed system values as user inputs. Translation payload mappings do not include them.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| wabaTemplateCategory | Authentication when the requested message authenticates or verifies a recipient; Marketing when it promotes a job, performs talent-pool outreach, or runs a campaign; Utility for every other expected transactional update, including application receipt, interview confirmation, schedule change, or a requested status update | A natural-language base-template proposal is being derived | No — classify from the stated purpose; a user correction changes the requirement and restarts validation |  |
| productContext | HCM_RECRUITING | Every base-template creation; the field is not collected from the user | No — always use the fixed system default |  |
| recruitingSource | ORA_FSM_UI | Every base-template creation; the field is not collected from the user | No — always use the fixed system default |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When | Rule Selection |
|---|---|---|---|---|---|---|---|---|
| WATL.DEFAULT.NL_META_CATEGORY | decision | 27 | apply_default | defaulted->WATL.LOOKUP.NL_CATEGORY | WATL.LOOKUP.AVAILABLE_NL_NAME | stop | Classify the natural-language proposal as Authentication for authentication, Marketing for promotional outreach or campaigns, and Utility for every other expected transactional message | all |
| WATL.DEFAULT.PRODUCT_CONTEXT | decision | 100 | apply_default | defaulted->WATL.DEFAULT.RECRUITING_SOURCE | WATL.LOOKUP.CREATE_TOKENS | stop | Set productContext to HCM_RECRUITING for every base-template create or Draft update; do not collect it as user input | all |
| WATL.DEFAULT.RECRUITING_SOURCE | decision | 101 | apply_default | defaulted->WATL.ENFORCE.CONVERSATION_STARTER | WATL.DEFAULT.PRODUCT_CONTEXT | stop | Set recruitingSource to ORA_FSM_UI for every base-template create or Draft update; do not collect it as user input | all |
