# Approval-Bound Reference Value Suggestions

Read this reference when a user-supplied Questionnaire reference value does not resolve exactly and the selected task declares that value suggestion-capable.

## Safety boundary

Suggestions help the user select an exact value already present in the current target. They never create a value, weaken an exact identity check, or authorize DAT generation or a live import.

Use this sequence:

1. Run the task's existing exact resolver first.
2. Enter suggestion handling only when that resolver returns zero exact matches. Multiple exact matches remain ambiguous and are not ranked away.
3. Retrieve the complete documented candidate catalog through `core.fusion-api.rest-api-client`. Apply subscriber, parent, active-state, capability, effective-date, and authorization restrictions before ranking.
4. Rank at most three exact returned candidates. For ranking only, trim outer whitespace, collapse repeated whitespace, compare case-insensitively, and treat spaces, hyphens, and underscores as token separators. Typographic similarity may order candidates but cannot validate one.
5. Mark one candidate as probable only when it is uniquely best supported by the supplied value and business context. Otherwise present the shortlist without selecting a value.
6. Require explicit approval of the complete exact target value or compatible value set. Never modify the business specification or DAT while approval is pending.
7. Bind approval to the target environment, task, portable parent business key, original input, selected exact value, catalog timestamp, source-request fingerprint, and exact ordered candidate-set fingerprint.
8. Immediately before a new immutable DAT preview, rerun the original exact resolver and every compatibility check for the approved value. Changed input, target, parent key, candidate set, catalog, or failed exact recheck invalidates approval.

Candidate retrieval failure, incomplete pagination, an empty authorized catalog, or no eligible candidates is `MISSING` or `FAILED`; do not invent a fallback.

## Suggestion-capable values

| Value family | Required candidate restriction |
|---|---|
| Subscriber name | Exact values returned by `questionnaireSubscribersLOV` |
| Question category | Same subscriber and `ContainQuestions='Y'` |
| Questionnaire category | Same subscriber and `ContainQuestionnaires='Y'` |
| Question type and response type | Exact compatible pair; permitted question type; template capability when applicable |
| Status | Exact target lookup code and meaning for the applicable object |
| Calculation rule | Exact target calculation-rule code and meaning |
| Rating model and level | Exact model; levels restricted to that approved model |
| Installed language | Fully installed target languages only |
| Reusable question | Same-subscriber active exact QuestionCode and version combinations |
| Questionnaire template | Same-subscriber exact template codes from the LOV, followed by authoritative full-template verification |
| Questionnaire | Same-subscriber exact questionnaire code and version combinations for user selection only |
| Controlling question and answer | Same-subscriber active question/version, then answers beneath that exact parent |
| Placement response override | Compatible with the referenced question and permitted by template capabilities |
| Recruiting organization, location, job family, or job function | Authorized, active/effective candidates with the complete business key; display name alone is insufficient when the target exposes additional key context |

Use a suggestion family only when the task's `ora_reference_lookups.md` declares both the exact resolver and a documented way to retrieve its bounded candidate set. An exact-only endpoint does not become a fuzzy-search endpoint.

## Exact-only evidence

Never use similarity to resolve Data Loader registrations, generated IDs, owner person numbers, create/update identity and duplicate checks, AnswerCode uniqueness, version or sequence keys, current lifecycle or in-use state, downstream usage, hierarchy child identity, or returned item/child links. These remain exact evidence gates.

Suggestion approval is distinct from Data Loader approval. It permits only replacement of the named raw input with the approved canonical target value for a new validation and immutable preview.
