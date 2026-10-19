# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| The supplied XML is malformed or its root contextName is not OMIntegration | Stop before any XML-dependent assessment and request a valid OMIntegration Service Mapping XML |
| The XML exposes the requested source and target but has no direct assignment evidence | Return source-and-target availability without assignment evidence and state whether an Algorithm assessment is needed; do not claim an existing mapping |
| A Custom EFF is requested but its entity, owner-key join, provider attribute mapping, type, or service exposure is incomplete | Return a mapping prerequisite with the exact missing Entities, Sources, or Services row and an inline mapping-information request for each unresolved placeholder. When the technical plan is complete but a post-change export is unavailable, ask the explicit validation-skip question; only an explicit yes permits a skipped-validation provisional handoff. Do not represent the EFF as available or use Algorithm logic as a substitute |
| A Custom EFF provider attribute mapping is blank, truncated, ambiguous, or unexplained | Treat the source as unconfirmed and request the provider metadata or corrected mapping; do not infer the provider attribute from the context attribute name |
| A Custom EFF proposal uses a direct target-to-source relation instead of the EFF-to-owner-to-OSSTransactions-to-target chain | Return the missing interface-table lineage and do not recommend an Algorithm draft |
| A requested candidate has no documented describe path or the response is unavailable | Return the missing documented path or metadata prerequisite; do not infer a replacement |
| A requested target is absent and no documented metadata route has been checked | Stop the final missing-target conclusion. First request the exact current-release documented entity-level describe route, then use it only through the approved read-only client. |
| A standard property exists in the selected target entity's describe but no matching mapping attribute is present | Return a describe-backed extension-attribute mapping gap. Give exact Entities, Sources, and Services rows needed to expose one alias on that entity; do not conclude the target cannot be controlled or invent an Algorithm field. |
| A custom-indicator request lacks source EFF or target details | Return a mapping-information request for each unknown technical value. Do not return an implementation-ready plan or Algorithm draft. |
| An assessment omits an unresolved custom source or target detail | Correct it by adding the literal placeholder and required evidence to the mapping-information request; do not fill it from an example. |
| The selected target alias type differs from the describe Type | Return `incompatible` unless documented configuration evidence provides a conversion contract, including blank and invalid-value handling, and a conversion owner. Do not infer conversion from a similar alias. |
| The selected target alias is present but its Services entry omits read or write | Return a permission prerequisite. Require explicit per-attribute flags for the Algorithm direction; do not infer them from the enclosing entity. |
| A requested Subscription Management child object has not been traced through the supplied root documentation tree | Return the missing branch segment, selected root, documented child page, or parent identifier. Do not select a sibling or infer a child collection path. |
| A child GET path is used to invent a child describe path | Stop the lookup. Inspect the verified root describe response at its documented nested child schema path, or require an explicit documented or returned kind=describe route. |
| A describe response has no compatible candidate, multiple candidates, a non-queryable candidate when queryability is required, or a type mismatch | Return the ambiguity and request clarified business meaning or confirmed source metadata |
| A documented metadata candidate has a different name from the XML context attribute | Return the candidate confidence and request assignment evidence when the relationship remains unproven |
| Required grouping, feature, duration or pricing, or orchestration evidence is absent | Return the missing evidence and stop the assessment |
| The request includes a Fusion mutation or revised Service Mapping artifact | Refuse the request as out of scope |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input-context blocker | The XML is missing, malformed, or not OMIntegration | Request valid source XML |
| Mapping gap | The XML lacks the required readable source or writable target | Request the missing Service Mapping exposure and return exact tab-by-tab changes directly in chat when evidenced. State that a complete plan is not an applied mapping and is only eligible for the companion task's provisional-draft path |
| Metadata blocker | The describe path or response cannot yield one confirmed compatible candidate | Request documented metadata or clarified mapping meaning |
| Target-metadata prerequisite | The requested target is absent from OMIntegration and the exact entity's documented metadata contract is not checked or cannot establish a compatible candidate | Report the documented candidate, if any, and require revalidation of its entity, provider row, and writable service permission in OMIntegration |
| Describe-backed exposure gap | A standard target property is described but its selected-entity alias, type compatibility, source mapping, or explicit Services permissions are incomplete | Return exact unapplied Entities, Sources, and Services steps. Once all rows are specified, ask the explicit validation-skip question only if post-change export validation is unavailable; an affirmative response permits only the provisional Algorithm path |
| Type-compatibility blocker | The describe Type and Service Mapping attribute type differ without an evidenced conversion contract | Request a directly compatible type or the conversion contract; do not propose a Boolean Algorithm expression against arbitrary text |
| Child-metadata prerequisite | The requested target is a child resource but its exact documentation branch, parent identifiers, or nested root-descriptor schema path is missing | Return the child branch prerequisite and stop before a field or URI recommendation |
| Dependency blocker | Required implementation evidence is absent or incompatible | Request the specific evidence |
| Scope blocker | The request would modify Fusion or Service Mapping XML | Return the read-only assessment boundary |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| XML context blocker | The observed root contextName and required OMIntegration value without disclosing unrelated XML content |
| Mapping assessment | Source and target evidence, permissions, direct-assignment result, mapping_status, algorithm_recommendation, and whether any three-tab plan is unapplied and unvalidated. Present the ordered tab instructions directly in chat without creating a human-readable Markdown plan |
| Metadata blocker | Source entity, requested business meaning, candidate count, relationship confidence, and compatibility outcome without persisting response payloads |
| Dependency blocker | Missing evidence category and the one safe next action |
| Scope blocker | That no configuration or artifact change was performed |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| XML context is not OMIntegration | Do not treat it as FOM-to-OSS input or reuse its attributes |
| Metadata is unavailable or ambiguous | Do not invent an attribute, URI, alias, transformation, or Algorithm input |
| Source and target names are similar or have matching types | Do not present similarity as an XML assignment or an existing mapping |
| A Custom EFF is partially represented | Do not infer the omitted entity, source mapping, provider attribute, service permission, owner-key join, or cross-entity lineage |
| A describe-backed standard target field is partially exposed | Do not infer the alias type, conversion, provider view-object attribute, or Services permission from a similar field or an entity-level flag |
| A remote operation is requested | Do not use POST, PUT, PATCH, DELETE, action invocation, direct database access, or a general GET resource request |
| A revised Service Mapping artifact is requested | Do not create, edit, package, import, publish, or deploy it |
| A human-readable Service Mapping plan file is requested or implied | Do not create a Markdown plan artifact; present the structured Entities, Sources, and Services steps in chat |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OMSUBMAP.ADVISORY.GATE | decision | 5 | execution_gate | assessment-ready->OMSUBMAP.RETURN.ASSESSMENT;out-of-scope->OMSUBMAP.RETURN.ISSUES | OMSUBMAP.ENFORCE.DESIGN | stop | The design is valid and the requested outcome is a read-only assessment |
| OMSUBMAP.RETURN.ASSESSMENT | terminal | 6 | terminal | none | OMSUBMAP.ADVISORY.GATE | stop | A validated service_mapping_assessment is ready for return |
| OMSUBMAP.RETURN.ISSUES | terminal | 7 | terminal | none | none | stop | Any blocking validation, lookup, dependency, design, or scope outcome occurs |

## Sources

- User-approved FOM-to-OSS operating model: the Service Mapping task is read-only and describe is its only permitted remote operation.
- User-approved FOM-to-OSS provisional rule: a mapping-gap UI plan is advisory only and never makes the mapping available or applied.
