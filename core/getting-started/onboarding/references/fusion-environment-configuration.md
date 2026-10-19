# Fusion environment configuration guidance

## Source guide and diagrams

Use the bundled [26D OAuth setup guide](../assets/oauth-setup-fscr-26d.docx)
and [illustrated setup steps](iam-client-application-setup.md) for IAM prerequisites
and property configuration questions. The illustrated reference indexes the source
sections and all eight extracted screenshots from the 26D document.
Show and explain the relevant diagram as part of the answer. If the
interface cannot display images, link the figure and describe its controls.

The guide is source material for advisory help, not authorization to act on the
user's Identity Domain. Follow the current OAuth skill for execution. Never copy
sample tenant values into a user's configuration. For source provenance and the boundary between IAM setup guidance and the current
auth implementation, read the illustrated reference's source notes.

## Property mapping

Repository sources: [OAuth skill](../../../auth/fusion-oauth-authentication/SKILL.md)
and [auth implementation](../../../auth/fusion-oauth-authentication/scripts/fusion_auth.py).
Read these again when behavior may have changed. The table describes FSCR's local
contract; it does not establish a tenant's IAM registration values.

| Property | Meaning and source | Check to explain |
| --- | --- | --- |
| `environment` | Local environment name selected for trust enrollment | Must match the selected entry in the private trust policy. |
| `restBaseUrl` | Selected Fusion application's base URL | Use the Fusion application, not the Identity Domain console or OAuth endpoint; it must match the enrolled Fusion origin. |
| `clientId` | Client ID of the application registered for the selected Identity Domain | Must match the enrolled client ID; do not substitute an application display name. |
| `redirectUrl` | Callback registered in the guide: `http://127.0.0.1:8765/oauth/callback` | Match the registered URI exactly. If the user selects a different supported callback, update both registration and local configuration. |
| `scope` | Exact scope registered and authorized for standard Fusion REST | Copy the approved scope; never derive it from the environment label. |
| `ai_scope` | Exact Fusion AI scope selected in Add resources | Used by the [workflow agent invoker](../../../fusion-ai/workflow-agent-invoker/SKILL.md); it is not a `fusion_login.py --service ai` option. |
| `km_scope`, `rmc_scope`, `cpq_scope` | Optional Knowledge Management, Risk, and CPQ scopes listed in the guide | Configure only when the corresponding REST client/workflow is selected. They are not login CLI service names. |
| `enableProxy` | Optional proxy setting listed in the source configuration block | The example is not proof that a selected client implements this property; inspect that client before recommending changes. It does not fix IAM grants. |
| `pkce` | FSCR client mode; `true` by default | Match the registered client type. Only an explicitly configured confidential application uses `false`. |
| `boss_scope` | Exact approved BOSS service scope | Required when selecting `boss`; uses `restBaseUrl`. |
| `fusion_common_scope` | Exact approved Fusion Common service scope | Required when selecting `fusion-common`; no fallback to `scope` or `boss_scope`. |
| `fs_restBaseUrl`, `fs_scope` | Field Service target and approved scope | Required for `field-service`; do not fill these with another service's values. |
| `cdp_restBaseUrl`, `cdp_scope` | CDP target and approved scope | Required for `cdp`; do not fill these with another service's values. |

The guide prepares Fusion, BOSS, Fusion Common, and Fusion AI scopes for the broader
FSCR journey. An individual login needs the properties required by its selected
service; optional product scopes are added only as needed.
Do not suggest putting `authorizeUrl` or `tokenUrl` into the properties file.
The current auth implementation derives these from the issuer and endpoint paths
in `~/.fusionaim/oauth-trust.json`. Conflicting legacy endpoint properties are
rejected. Trust enrollment is a separate operation owned by the OAuth workflow.

Plaintext `clientSecret` properties are not used for authentication. For an existing
confidential client, refer to the OAuth skill's platform-specific private storage
and migration workflow; never request the secret in chat or insert it in a command,
skill asset, tracked properties file, or project artifact. Do not disable PKCE as a
generic workaround for a failed login.

## Guided diagnosis

Use the user's redacted error and the mapping above to narrow the next check.
Do not run login or network probes to diagnose an advisory question.

| Symptom | Guidance and next check |
| --- | --- |
| Missing/blank property | Identify the selected service and its required base URL/scope; explain the value's source. |
| Client or environment not enrolled, or mismatched origin | Compare the selected environment, client, and Fusion origin with the intended enrollment. Hand trust creation/correction to the OAuth skill; do not bypass pins or replace trust silently. |
| Redirect mismatch | Compare scheme, host, port, path, and trailing slash with the registered callback and active flow. |
| Login denied with Enforce grants as authorization enabled | Ask the Identity Domain administrator to check that the intended FSCR user or group is assigned under the application's Users or Groups tab; this assignment does not grant Fusion roles. |
| Invalid client or client authentication failure | Verify the selected client and public/confidential mode; consult the auth skill for private secret storage if confidential. Do not ask to see the secret. |
| Invalid/missing scope | Confirm the exact registered scope for the selected service; do not guess or broaden grants. |
| API 401 or 403 | Treat as an auth/authz finding requiring the responsible workflow. A token alone does not prove Fusion roles or data access. Do not prescribe repeated retries or role grants without diagnosis. |
| Missing guide, unreadable diagram, or ambiguous IAM step | Report the missing source and request the specific document/section; stop the dependent IAM guidance rather than inventing settings. |

Return the affected property or prerequisite, its source, the mismatch if known,
and one concrete next action. Label an unverified cause as a hypothesis. For a
durable downstream diagnostic, use the repository failure classes (for example,
`input validation` or `auth/authz`), with stage, redacted message, and recommended
action under the selected project workflow.
