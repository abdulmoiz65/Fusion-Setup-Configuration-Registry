---
skill_id: "core.getting-started.onboarding"
name: "FSCR Onboarding"
description: "Introduces users to FSCR and guides onboarding, public OAuth client (Mobile Application) setup, fusionEnv.properties configuration, and any login or authentication questions or issues, including Fusion environment trust enrollment, PKCE, and access tokens. Provides guidance and troubleshooting; hands authentication execution to the OAuth skill."
layer: "core"
pillar: "Core"
type: "advisory"
execution_mode: "advisory"
owner_team: "Central platform team"
version: "0.3.0"
inputs:
  - "getting_started_question"
  - "selected_service_and_client_type_if_known"
  - "redacted_configuration_or_error_if_available"
outputs:
  - "getting_started_guidance"
  - "configuration_guidance"
  - "authentication_guidance_and_diagnosis"
  - "next_action_or_source_gap"
depends_on: []
uses_core:
  - "core.auth.fusion-oauth-authentication"
persists_project_state: false
applicability:
  industries: ["All"]
  countries: ["All"]
  fusion_releases: ["Current Oracle Fusion Cloud release"]
side_effects: []
required_privileges: []
---

# FSCR Onboarding

## Purpose and ownership

Guide users through an introduction to FSCR, initial setup, and authentication
readiness. Answer login and authentication questions and help diagnose issues at
any stage of their FSCR journey. Owner: Central platform team.

Use this skill for “Introduce me to FSCR”, “How do I get started?”, “Help me create
the public client / Mobile Application”, “How do I configure fusionEnv.properties?”,
“How does environment enrollment work?”, “How do I authenticate?”, and any login,
token, or authentication question or issue. Guidance alone does not require a
successful login or a new implementation project.

## Guidance workflow

1. Identify the immediate goal and what the user has already completed. Start new
   users with the introduction below; resume experienced users at the relevant
   setup step or failing authentication stage. Ask only for missing information.
2. Introduce FSCR as the Oracle Fusion Setup and Configuration Skills Registry for
   implementation guidance and reusable technical workflows. Explain the router's
   orchestration, core services, shared cross-pillar guidance, and pillar-specific
   skills. Use [README](../../../README.md) for the repository overview. Explain
   that `project/{project_id}` preserves implementation state across sessions.
3. Use [IAM client application setup](references/iam-client-application-setup.md)
   as the guided setup journey, with the relevant screenshot displayed and explained
   at each step: select the Fusion Identity Domain; create a **Mobile Application**;
   optionally restrict access and assign users/groups; configure Authorization code
   and the callback; add resource scopes; activate; obtain the OAuth Client ID;
   and populate `core/auth/fusionEnv.properties`. Use the
   [26D Word source](assets/oauth-setup-fscr-26d.docx) when source detail is needed.
   Do not merely send a document link or dump all diagrams without explanation.
4. Use [property guidance](references/fusion-environment-configuration.md) to map
   each value to its source and explain what it must match. Cover the Fusion HTTPS
   base URL, local environment name, OAuth Client ID, exact registered callback,
   and selected service scopes. Distinguish Application ID from OAuth Client ID.
   Use placeholders; never copy a screenshot's environment values into configuration.
5. Explain authentication using [PKCE login flow](references/pkce-login-flow.md)
   and the current [OAuth skill](../../auth/fusion-oauth-authentication/SKILL.md).
   Show the flow diagram and distinguish three stages:
   - First-time enrollment collects the Fusion URL, environment name, and OAuth
     Client ID, discovers the trusted issuer through the declared Fusion redirect
     flow, and writes the private `~/.fusionaim/oauth-trust.json` policy. Explain
     why trust is separate from caller-selectable properties, how the values must
     match, and how an existing or additional environment is handled. Use the
     auth skill's exact welcome prompt when handing off actual enrollment.
   - PKCE login generates a verifier/challenge, opens browser sign-in, validates
     the callback state, and exchanges the authorization code for an access token
     without a public-client secret.
   - The private profile cache supports subsequent authorized Fusion REST calls;
     scopes, Fusion roles, and data access still control access. Explain renewal
     according to the current implementation, not assumed refresh-token support.
6. For an issue, follow the diagnosis workflow below. For a request to execute
   enrollment or login, hand off to the OAuth skill with the selected environment,
   service, and known prerequisites; do not leave an action request at explanation.
7. Finish each relevant stage with the next concrete step and any unresolved gap.
   Keep the journey progressive and skip completed stages. Do not claim setup,
   authentication, or REST access succeeded without execution evidence.

## Login and authentication diagnosis

Use this skill for all login/authentication guidance, including issues encountered
after onboarding. Identify the failing stage from a redacted error: IAM application
activation or user assignment, property configuration, trust enrollment, browser
sign-in, callback, code exchange, token storage/reuse, or Fusion REST authorization.
Consult the troubleshooting tables in the configuration and PKCE references and
the current OAuth skill before explaining a cause or next action.

Check only the context relevant to the failure: selected environment and service,
public/PKCE versus an existing confidential client, exact callback registration,
required scope, or trust mismatch. Distinguish a confirmed mismatch from a
hypothesis. Explain the specific correction and hand execution to the responsible
workflow. A repeated 403 may require role or data-access diagnosis rather than
another login. Do not disable PKCE, broaden scopes, replace trust, or repeat a live
operation as a generic workaround.

Use redacted errors and synthetic examples. Do not dump the properties file or
request passwords, client secrets, authorization codes, verifiers, or token
contents. Guide users through browser sign-in or the auth skill's private input
mechanisms when execution requires sensitive input.

## Routes and execution boundary

| User intent | Next skill |
| --- | --- |
| FSCR overview, onboarding, IAM setup guidance, or any login/authentication question or issue | Continue this skill's guided journey and diagnosis |
| Start or resume an implementation | [Implementation Router](../../../router/implementation-router/SKILL.md) |
| Log in, enroll trust, obtain or refresh a token | [Fusion OAuth Authentication](../../auth/fusion-oauth-authentication/SKILL.md), when selected by the active workflow |
| Create implementation users or assign their roles | Route through the Implementation Router to [Implementation Users](../implementation-users/SKILL.md) |

This advisory skill has no live external-operation step. It does not navigate the
Identity Domain, register applications, enroll trust, launch login, refresh tokens,
or test REST endpoints. Hand execution to the selected workflow and honor its
preflight and approval gates; do not substitute a browser or direct REST call.
IAM application creation is a user/admin-performed prerequisite here. The user
needs the appropriate Identity Domain application administration permissions to
perform it; no such privilege is needed to receive guidance.

## Persistence

Ordinary Q&A produces a conversational answer and changes no project state or
configuration. If the user requests a durable checklist or troubleshooting report,
route that artifact work through the implementation workflow and its project
workspace services. Use the selected project, or initialize
`draft_impl_project_<date>` from `project/_template` when required and offer to
rename it. Record the run and token usage in the prescribed project log:
`project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md`.
Persist only redacted findings, artifact references, and next actions.
