# Reference Lookups

## Live Lookups

| Resolver | Runs When | Required evidence | Safe execution and outcome |
|---|---|---|---|
| `resolve_order_mapping_source_metadata` | The validated XML does not establish a requested Order Management source, including a conditional-rule primary or fallback source | Current official documentation identifies the exact current-release entity-level `describe` route | Use the declared REST client for a read-only describe request before returning missing-input rows. Capture only the candidate identity, type, capability, and description. If no single compatible candidate is found, return a mapping-information request. |
| `resolve_subscription_target_metadata` | The XML does not establish any requested Subscription Management target entity, attribute, child target, or correlation | Current official documentation identifies the exact current-release entity-level `describe` route or the exact root-to-child branch for a child target | Resolve the entity from the user's selected target, then use the declared REST client for a read-only describe request before returning a target blocker. Do not hardcode an entity, choose a different target, or stop at XML absence. Treat every result as a candidate until the mapping export proves entity exposure, provider mapping, and service permission. |
| `resolve_described_field_exposure` | A described target candidate is absent from the mapping | Canonical property identity, type, capability, and existing mapping context | Return an unapplied Entities/Sources/Services plan using only the evidenced values. Require a conversion contract for type differences. |
| `resolve_subscription_child_resource_metadata` | The target is a documented child resource | Exact official documentation branch and parent descriptor schema path | Traverse the documented branch first. Do not synthesize a child describe URI from a record GET path. |
| `resolve_interface_transaction_metadata` | XML lineage needs candidate confirmation | Current official documentation identifies the exact current-release entity-level `describe` route | Confirm candidate interface identifiers only; require XML joins before using them as a correlation bridge. |

## Lookup Execution Rules

For workflow-authorized GET-only metadata probes, run the
task-local `scripts/fusion_rest_curl_probe.py`. It delegates OAuth and HTTP
execution to `core.fusion-api.rest-api-client`, keeps OAuth tokens out of
stdout and command arguments, accepts only `/crmRestApi/.../describe` paths,
and rejects response-output paths inside the repository workspace. Write raw
responses outside tracked project workspaces.

| Situation | What Happens |
|---|---|
| The XML establishes the required source, target, permissions, and assignment | Do not call REST; return the XML-based assessment. |
| A requested target detail is absent from XML but the target entity is known | Resolve that exact entity or documented child branch with describe before concluding the target is unavailable, requesting target selection, or asking for the target field name. |
| A required standard source detail is absent from XML | Run the documented source describe route before returning a mapping-information request. Return a source metadata prerequisite only when no documented route exists, the route cannot be called, or describe yields no single compatible candidate. |
| A primary/fallback rule references standard source or target business meanings but XML lacks exact aliases | Run source and target describe for every unresolved standard entity first; then classify candidates, mapping gaps, ambiguity, or remaining user inputs. |
| The requested source is a fulfillment-line EFF or another custom context | Do not infer an EFF context, owner key, attribute, polymorphic type, provider mapping, or URL. Request those details and use only a current documented describe route when available. |
| Describe returns a candidate | Record property identity, type, required capability, and relationship confidence. It does not create an alias, Service Mapping row, assignment, or algorithm input. |
| Describe does not return one compatible candidate | Return a metadata blocker and the exact missing input; do not guess. |
| A mapping alias type differs from a described type | Return `incompatible` unless a validated conversion contract defines values, blank handling, invalid-value handling, and conversion owner. |
| Any operation other than the permitted describe read is requested | Refuse it as out of scope. |
| The user says not to use cached data | Run a new describe for each unresolved requested entity, use a new raw-response path outside the repository, and force a fresh authentication flow when authentication is required. Do not reuse previous describe responses or project assessment artifacts as evidence. |

## Sources

- User-approved operating model: inspect supplied Service Mapping XML before requesting metadata.
- User-approved operating model: use only documented, current-release, read-only REST describe metadata when XML evidence is insufficient.
