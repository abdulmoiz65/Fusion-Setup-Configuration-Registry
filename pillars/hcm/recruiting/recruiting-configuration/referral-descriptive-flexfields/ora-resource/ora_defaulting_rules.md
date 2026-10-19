# Referral Descriptive Flexfields Defaulting Rules

For copy, update, and disable, ask only for Segment Name when missing, then validate a fresh exact-task export for this request; if unavailable or empty, use the qualified Global fallback proposal instead of stopping; label older evidence UNVERIFIED. For new create, use a validated matching package or export fresh when absent. Follow the required-values table, confirmation, optional-values table, confirmation sequence in ../SKILL.md.

For new segments, non-asterisk UI settings are optional. Omitted optional settings use the supported Create Segment UI defaults and are disclosed in the preview. Required asterisk-marked fields must be explicitly confirmed. Omitted existing values are preserved.

Data type, display control, and storage suggestions follow the name-based rules in `../SKILL.md`; they are proposals requiring confirmation, not fixed defaults. Never apply Character/TEXT_BOX/ATTRIBUTE_CHAR1 to every segment name.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Existing segment property | Preserve the latest authoritative existing value | PlanUpdate omits the property | No | |
| Optional UI setting | Compatible value from the supported Create Segment UI | PlanCreate omits a non-asterisk UI setting | No; disclose it in the preview | |
| Description | Blank | PlanCreate or copy | No | |
| Enabled | Yes | PlanCreate or copy | No | |
| Range Type | None | PlanCreate or copy | No | |
| Required | No | PlanCreate or copy | No | |
| Default Type | None | PlanCreate or copy | No | |
| Definition Help Text | Blank | PlanCreate or copy | No | |
| Instruction Help Text | Blank | PlanCreate or copy | No | |
| Display Size | Blank (UI default) | PlanCreate or copy | No | |
| Display Height | Blank (UI default) | PlanCreate or copy | No | |
| Read-only | No | PlanCreate or copy | No | |
| Segment default rule | None | PlanCreate or PlanUpdate explicitly selects no default | No | |
| Proposed explicit default | The one approved correctly typed constant, parameter, or supported SQL default | The requester elects to define a default | No | |
| Storage column | No default | Every request | No | |
| Sequence | No default | Every request | No | |
| Internal value-set identifier | No default | Segment uses an LOV or value set | No | |
| Historical-contract current state | No default; unavailable checks remain `UNVERIFIED` | New Global PlanCreate uses the failed/header-only export fallback | No; require explicit requester confirmation of column, sequence, and displayed value-set code/name | |
