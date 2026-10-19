# Self-Paced Learning Design Enforcement

These gates apply to each operation and row after validation, dependency
classification, lookups, and defaults. Passing them still does not authorize a
write.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Route readiness | Confirm exact Data Loader registration, template, components, and operation or one named Direct REST exception |
| 2 | Content integrity | Confirm content intent, source, type, processing state, and required references agree |
| 3 | Identity and freshness | Resolve one exact target or duplicate check, follow returned links, and freeze a fresh fingerprint |
| 4 | Reference readiness | Confirm only the owner, language, lookup, profile, questionnaire, list, and DFF dependencies this row uses |
| 5 | Lifecycle and history safety | Apply the FDD state transition, assignment, transcript, prerequisite, and where-used rules |
| 6 | Row isolation | Exclude invalid rows and stop subsequent writes after an uncertain row outcome |
| 7 | Approval | Show exact effects and omission choices and require approval for the immutable fingerprint |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Parent deep insert with content | Blocker | resolve_self_paced_loader_registration | The artifact sends status or autoCommit, or the readback does not derive content status ORA_ACTIVE and autoCommit Y | Omit both fields and verify their server-derived values | Yes |
| Standalone child create exception | Blocker | resolve_self_paced_lookup_value | Current child Describe requires status or autoCommit and the exception payload omits or misstates them | Correct the exception payload using the current child contract | Yes |
| Create or add content | Blocker | resolve_self_paced_lookup_value | Content type, source, URL, binary metadata, provider, language, scoring, questionnaire, or completion configuration is missing or inconsistent | Correct the content definition before preview | Yes |
| Activate | Blocker | resolve_self_paced_identity | Data Loader update support is unresolved; or the Direct REST exception lacks Effective-Of RangeMode=UPDATE; or readback is not Active with DraftExists N and PublishedExists Y; or content changed | Use the supported loader update or exact activation exception and reconcile parent plus content | Yes |
| Publish content | Blocker | resolve_self_paced_identity | Required item metadata or content is missing, unsupported, failed, or still processing, or the request treats publish as UI activation | Keep the item in draft until readiness is verified and keep publishing distinct from activation | Yes |
| Private publish | Blocker | resolve_self_paced_catalog_profile | No exact active compatible catalog profile or audience evidence is available | Resolve the profile and audience before a separate publish preview | Yes |
| Replace content | Blocker | resolve_self_paced_identity | Active or completed assignments and the replacement's learner impact are unknown or not disclosed | Read usage and preserve completion/history semantics before approval | Yes |
| Reprocess | Blocker | resolve_self_paced_identity | The content type or current processing state is ineligible, or exact action parameters are unresolved | Correct eligibility and use only the documented returned-item action | Yes |
| Lifecycle transition | Blocker | resolve_self_paced_lookup_value | The target status or reason is not an exact enabled target value or the FDD disallows the transition from current state | Select an eligible state and required reason | Yes |
| Delete content | Blocker | resolve_self_paced_identity | The parent is not in the FDD-permitted inactive state, or assignment and completion effects are unresolved | Inactivate first when eligible and preserve required history | Yes |
| Delete parent | Blocker | resolve_self_paced_identity | Assignments, transcripts, prerequisites, communities, topics, other where-used relationships, or completion-preservation behavior remain unresolved | Use a safe lifecycle action or obtain an authoritative deletion contract | No |
| Owner supplied | Blocker | resolve_self_paced_owner | Owner identity is missing, ambiguous, inactive, inaccessible, or incompatible with the writable field | Supply one exact current person identifier | Yes |
| Language supplied | Blocker | resolve_self_paced_language | Language is missing, ambiguous, inactive, uninstalled, or cannot be serialized as the target schema expects | Select one exact active installed language | Yes |
| Questionnaire supplied | Blocker | resolve_self_paced_questionnaire | Questionnaire is missing, ambiguous, inactive, or incompatible by subscriber, purpose, or version | Select one compatible active questionnaire | Yes |
| Extensible attributes supplied | Blocker | resolve_self_paced_dff | Context differs from WLF_LEARNING_ITEM or a segment is not current, writable, or value-valid on the target | Refresh target metadata and correct the segments | Yes |
| Filtered list selected | Blocker | resolve_self_paced_hcm_list | List identity, active state, subscriber, object, name, or scope is missing or incompatible | Supply one exact active compatible list | Yes |
| Filtered-list association write | Blocker | | The association is not exposed by the confirmed learningSelfPacedItems schema | Do not execute without an authoritative write contract | No |
| Demo preview | Blocker | | Count is outside 1 through 10, generated provenance is absent, or Article plus URL intent is not compatible and reachable | Correct the candidate set before approval | Yes |
| Demo Objective or Ideal Learner | Blocker | | Preview does not plainly state that these values are non-persistable through this REST contract, or approval does not accept omission | Add explicit omission disclosure and obtain exact acceptance | Yes |
| Any mutation | Blocker | resolve_self_paced_identity | Current fingerprint differs from the approved fingerprint or the opaque returned link is unavailable | Re-read, rebuild the delta and preview, and obtain new approval | Yes |
| Multi-row mutation | Blocker | | A row lacks independent validation, evidence, fingerprint, approval state, or planned result handling | Complete or exclude the row before aggregate approval | Yes |
| Mutation route | Blocker | resolve_self_paced_loader_registration | A create or update bypasses core.data-loader, a Direct REST mutation is not a named exception, unsupported-operation evidence is absent, or the request relies on user-facing upsert, a manufactured item hash, an undocumented field, or inferred concurrency protection | Use Data Loader BC REST or the exact approved exception; otherwise stop | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_self_paced_loader_registration | Any create or update mutation | Exact registration, template, components, selected operation support, and metadata fingerprint | ora_reference_lookups.md |
| resolve_self_paced_identity | Existing-item operation, collision check, lifecycle or usage decision, content processing, and mutation freshness | Exact identity, returned links, current state, usage, processing state, and fingerprint | ora_reference_lookups.md |
| resolve_self_paced_owner | Owner is supplied | Exact active accessible person and writable identifier evidence | ora_reference_lookups.md |
| resolve_self_paced_language | Language is supplied | Exact installed active code, label, and serialization evidence | ora_reference_lookups.md |
| resolve_self_paced_lookup_value | A lookup-backed field or lifecycle transition is used | Lookup type, exact enabled code, meaning, validity, and transition evidence | ora_reference_lookups.md |
| resolve_self_paced_catalog_profile | Private publish or demo default profile is used | Exact active usable profile, default flag when applicable, processing state, and audience evidence | ora_reference_lookups.md |
| resolve_self_paced_questionnaire | Content references a questionnaire | Exact active compatible identity, subscriber, purpose, and version | ora_reference_lookups.md |
| resolve_self_paced_hcm_list | A filtered list is selected | Exact active compatible list identity and scope evidence | ora_reference_lookups.md |
| resolve_self_paced_dff | DFF values are supplied | WLF_LEARNING_ITEM context and exact current writable segment definitions | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SPL.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->SPL.AUTHORIZE_EXECUTION;blocked->SPL.HANDLE_ERROR | SPL.APPLY_DEFAULTS | stop | Inputs, dependencies, references, and defaults are ready for a final design gate |
