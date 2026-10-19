# Defaulting Rules

Apply the developer-requested create defaults below when the user omits a value, and materialize them in the CSV. These are task authoring policy, not a claim about task-UI or FSM importer defaults. Other defaults require source confirmation; the candidate transfer default remains unverified. Explicit codes, meanings, translations, or ordinary-language values take precedence after resolution.

Retain REFERENCE_UNRESOLVED warnings from earlier checks. Missing membership
authority is not permission to replace a supplied value with a default, invent
a language/context code, or skip a remaining supported lookup.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Omitted base/child group | Preserve current values/rows | Update; only for omitted groups, never explicit changes | No | find_work_type |
| StartDateActive (From Date) | Current calendar date in the user's timezone at preparation | Create when omitted | No |  |
| EndDateActive (To Date) | Blank | Create | No |  |
| Set assignments | Omit when not supplied; no implicit set and no required-set question | Create | No |  |
| TpAmtTypeCode (Transfer Price Amount Type) | Candidate COST_TRANSFER; unverified UI default | Create when omitted and a source-confirmed project default exists; otherwise request explicit intent | No | resolve_work_type_transfer_type |
| BillableCapitalizableFlag (Billable) | N | Create when omitted; developer-requested authoring default | No | resolve_work_type_boolean |
| UtilizableFlag (Utilizable) | Y | Create when omitted; developer-requested authoring default | No | resolve_work_type_boolean |
| Translation source language | Target base language only when confirmed | Create translation | No | resolve_work_type_children |

## Create Default Application

For a create, apply each omitted field's default independently, including when the entire base group is omitted. Preserve explicit values; an explicit invalid value or clear request is not omission and must follow validation. Updates and end-dates never receive these create defaults.

Capture the current calendar date once per preparation in the user's timezone from the active session context; serialize StartDateActive using the validated target FSM date format. Record the timezone, captured date, original omission and each applied value in task-rule evidence. If the timezone or date representation is unavailable, return the existing missing-input/failure outcome rather than guessing. Keep the captured date in the frozen preview and approved payload; do not recompute it during submission or resume of that preview. A new preparation captures the current date again and requires the normal fresh preview/approval.

Pass the defaulted flags through resolve_work_type_boolean and validate the completed date range before preview. An explicit EndDateActive earlier than the defaulted StartDateActive is invalid; do not alter either date to make it pass. These defaults do not supply the transfer classification or set assignments, or waive other checks.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WTYPE.APPLY_DEFAULTS | step | 2 | apply_default | applied->WTYPE.FIND_WORK_TYPE;warning->WTYPE.FIND_WORK_TYPE;failure->WTYPE.RETURN_ISSUES | WTYPE.VALIDATE_INPUT | stop | Valid input with any retained nonblocking warnings |

## Source Evidence and Default Boundaries

Reviewed on 2026-10-08 against the latest published Oracle Project Management documentation, release 26D.

| Rule | Evidence | Status and use |
|---|---|---|
| Omitted group preservation and no implicit set | Local task design policy, reviewed through scenarios WT-02 and WT-03 in ../../../noship/tests/project-foundation/manage-work-types/golden-scenarios.md | Preserve baseline only for omitted groups; explicit changes retain precedence. No claim that the importer preserves omitted rows automatically |
| Optional EndDateActive | [PJF_WORK_TYPES_B, 26D](https://docs.oracle.com/en/cloud/saas/project-management/26d/oedpp/pjfworktypesb-25294.html), END_DATE_ACTIVE is nullable | Supports an omitted end date; target FSM representation must still be checked |
| Candidate COST_TRANSFER default | [Work Types for Billing, 26D](https://docs.oracle.com/en/cloud/saas/project-management/26d/oapfm/work-types-for-billing.html), Cross-Charge Classification | Supports cost/revenue business classifications and default cost-based treatment of project costs. It does not prove the task UI or CSV importer defaults TpAmtTypeCode to COST_TRANSFER |
| Create Billable=N, Utilizable=Y and StartDateActive=current date | Explicit developer request, 2026-10-08 | Confirmed task authoring policy for omitted create values; materialize in CSV and validate representation. No claim of Oracle UI/importer defaults |
| Translation source language | [PJF_WORK_TYPES_TL, 26D](https://docs.oracle.com/en/cloud/saas/project-management/26d/oedpp/pjfworktypestl-25298.html), SOURCE_LANG | Identifies original-content language; no blanket default or equality with Language is evidenced. Retain confirmed intent and baseline relationships |

Unverified default evidence is a source gap, not proof that a candidate is invalid. When a required create value remains missing after the documented defaults, use the existing missing-input outcome; do not fabricate it, apply the unverified transfer default, or require a waiver. An update preserving that field needs no default. Public documentation review is authoring evidence and adds no runtime acquisition route.
