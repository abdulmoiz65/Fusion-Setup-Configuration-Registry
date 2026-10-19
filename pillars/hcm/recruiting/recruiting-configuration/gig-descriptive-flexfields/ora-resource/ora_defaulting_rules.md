# Gig Descriptive Flexfields Defaulting Rules

For copy, update, and disable, ask only for Segment Name when missing, then validate a fresh exact-task export for this request; if unavailable or empty, use the qualified Global fallback proposal instead of stopping; label older evidence UNVERIFIED. For new create, use a validated matching package or export fresh when absent. Follow the required-values table, confirmation, optional-values table, confirmation sequence in ../SKILL.md.

Preserve supplied values and authoritative current values. Optional settings may use only a supported UI default disclosed in the pre-submission Optional Edit Segment fields section; identities, storage, sequence, contexts, value sets, and approvals have no inferred default.

Data type, display control, and storage suggestions follow the name-based rules in `../SKILL.md`; they require confirmation and are not fixed defaults. Never apply Character/TEXT_BOX/ATTRIBUTE_CHAR1 to every name, or reuse the fallback template's Number/ATTRIBUTE_NUMBER1/10/Number values for every new segment.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Existing segment property | Preserve the authoritative current value | PlanUpdate omits the property | No | verify_gig_dff_current_definition |
| Optional Create Segment setting | Compatible supported UI default, disclosed before execution | PlanCreate omits the optional setting | No | |
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
| Segment default rule | None | The requester explicitly chooses no initial default | No | |
| Context | No default | Every context-sensitive request | No | verify_gig_context_identity |
| Storage column | No default | PlanCreate | No | verify_gig_dff_current_definition |
| Sequence | No default | PlanCreate | No | verify_gig_dff_current_definition |
| Value-set identifier or Module | No default | Value-set selection or creation | No | verify_gig_value_set_compatibility |
