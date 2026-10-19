# Talent Notifications Defaulting Rules

Request intent is never defaulted to implementation. Notification target,
product scope, candidate selection, provider identity, and enabled state are
never defaulted. Defaults apply only to deterministic trace fields on the
applicable request path.

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | request_mode | No implementation default | Request intent does not explicitly authorize configuration or another change | Never; classify a pure question as guidance_only, a blank-template request as blank_template, and supplied values with ambiguous change intent as draft_questionnaire | |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | draft_questionnaire_status | UNVALIDATED DRAFT - no Fusion lookup or implementation has been performed | draft_questionnaire is selected | No; this is a required disclosure, not a business value | |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | missing_draft_value | No default | A draft omits target, enabled state, or context | Never; list an open question and do not invent a value | |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | input_method | direct_conversation | The user supplies direct conversational rows and no file is present | No | |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | source_reference | direct-conversation | input_method is direct_conversation | No | |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | alerts_composer_handoff_status | not_requested | No Alerts Composer requirement is explicit | No | |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | authenticated_environment | No default | Active FDOS Fusion authentication context is missing or malformed | Never; require login or environment-configuration correction and do not accept a user-derived host | |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | quarterly_release | No default | Trusted authenticated-context and validated same-environment FSM metadata do not explicitly supply it | Never; omit the value and its source and continue without asking the user | |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | quarterly_release_source | No default | quarterly_release is absent | Never; record only the source of an explicit trusted quarterly-release value | |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | notification_target | No default | Identity, label, or business intent is missing | Never; request the missing business-facing value | resolve_talent_notification_targets |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | product_scope | No default | Exported ProductCode is missing, conflicting, ambiguous, or non-HRT | Never; use only the exact ProductCode in the fresh export and do not infer from prefixes, labels, descriptions, intent, or tab names | resolve_talent_notification_targets |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | notification_enabled | No default | State is missing or ambiguous | Never; request an accepted explicit enabled value | |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | mapping_confirmation | No default | A unique case/whitespace-only correction exists | Never; require explicit clarification | resolve_talent_notification_targets |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | candidate_selection | No default | One or more semantic candidates exist | Never; require explicit selection, rejection, or refinement | resolve_talent_notification_targets |
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | provider_identifier | No default | Target is confirmed | Never; derive only through provider-key resolution | resolve_talent_notification_targets |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| HRT_MANAGE_TALENT_NOTIFICATIONS | Talent Notifications | TPN.APPLY_TRACE_DEFAULTS | step | 6 | apply_default | applied->TPN.ENFORCE_DESIGN;not_needed->TPN.ENFORCE_DESIGN | TPN.RESOLVE_TARGETS | stop | On the implementation path, apply trace-only defaults after eligible target and provider-key resolution; never default request intent to implementation, the authenticated environment, quarterly release, target, product scope, enabled state, or confirmation |
