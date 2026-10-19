# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Establish XML mapping evidence | Use the validated OMIntegration XML to identify the source and target, their availability and permissions, and any direct assignment evidence |
| 2 | Confirm candidate metadata | Use the permitted describe lookup when source discovery, target discovery, child-target discovery, or compatibility confirmation is required; do this before returning missing-input rows for standard fields |
| 3 | Classify the mapping outcome | Distinguish an existing mapping from source-and-target availability without assignment evidence, a mapping gap, or a metadata or compatibility blocker |
| 4 | Produce tab-by-tab implementation instructions | For Entities, Sources, and Services, identify exact verify rows or exact add/edit rows without representing field availability as an assignment |
| 5 | Verify applicable prerequisites | Confirm grouping, feature, duration or pricing, and fulfillment evidence when applicable |
| 6 | Present the result inline | Return the assessment and ordered Entities, Sources, and Services instructions directly in chat; do not create a human-readable Markdown plan artifact |
| 7 | Enforce the read-only boundary | Return an assessment and UI change plan only; do not change Service Mapping configuration or XML |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every mapping assessment with a missing requested target | Blocker | resolve_subscription_target_metadata | The validated XML does not establish the requested writable target and no current describe of that exact entity or documented child branch has been inspected | Resolve documented metadata for the user-selected target before the final missing-target conclusion. Do not hardcode an entity, redirect the target, or imply an Algorithm can replace missing Service Mapping evidence | Yes |
| A standard target property is confirmed by describe but is absent from the corresponding OMIntegration entity | Blocker | resolve_described_field_exposure | The result declares the target unavailable, proposes Algorithm access, or proposes an alias without exact describe Type, compatible entity type or conversion contract, provider view-object mapping, and explicit Services flags | Return an Entities/Sources/Services exposure plan for one Service Mapping extension attribute on the selected entity. It is an alias to the described standard property, not a native custom field or an assignment. Revalidate the complete contract in a new OMIntegration export before an Algorithm draft uses it | Yes |
| A custom indicator behavior is requested | Blocker | resolve_subscription_target_metadata | The design infers a source EFF, target alias, provider mapping, or permissions from the business wording | Return a mapping-information request and validate every supplied value before recommending an Algorithm. | Yes |
| A conditional primary/fallback rule is requested | Blocker | resolve_order_mapping_source_metadata / resolve_subscription_target_metadata | The primary or fallback source, its type, the primary-absence test, target overwrite behavior, or repeated-source selection is inferred or unspecified after current describe has been inspected for unresolved standard entities | Run documented describe for unresolved standard source and target entities first, then return one missing-input row for each contract still unresolved. Require deterministic `ZERO_OR_ONE` selection or an explicit selection rule; do not default to first, sum, or any arbitrary source row. | Yes |
| An alias type differs from the described property type | Blocker | resolve_described_field_exposure | The design assumes implicit conversion | Require an evidenced conversion contract with valid, blank, and invalid-value behavior and a conversion owner. | Yes |
| A Subscription Management child target is requested | Blocker | resolve_subscription_child_resource_metadata | The assessment uses a child field or URI without traversing the exact documented root-to-child branch and inspecting the selected root descriptor | Record the documentation branch, documented child collection path, parent identifiers, nested descriptor schema path, and candidate evidence. Do not derive a child describe URI or select a same-named branch below another root | Yes |
| A requested outcome spans two context entities and relies on an interface-table correlation | Blocker |  | The XML does not evidence the interface entity, its source and target identifiers, or the provider joins to both entities | Return the missing correlation evidence; do not infer a bridge, cardinality, SDO traversal, direct assignment, or Service Mapping UI change | Yes |
| The target entity exposes a direct source correlation key | Decision |  | The assessment uses the direct key to bypass the XML-evidenced interface-table lineage | Establish the interface-table bridge first. Record the direct key only as corroborating evidence or an additional safe match check, and state cardinality and null behavior | Yes |
| The XML exposes the requested source and writable target but no direct assignment | Decision |  | The result is presented as an existing mapping, or a provider/source row is presented as a cross-entity assignment | Return source-and-target availability without assignment evidence. Mark already-correct Entities, Sources, and Services rows as no_change and recommend an Algorithm assessment only when the business requirement needs value population | Yes |
| A Custom EFF is requested as source or target | Blocker |  | The Entities, Sources, or Services tab lacks the EFF entity/attribute, owner-key join, compatible type, provider view-object attribute, source non-writable exposure, or target write capability | Return exact missing or inconsistent tab rows and an inline mapping-information request for every unresolved placeholder. Validate supplied responses against updated XML or permitted describe evidence before claiming availability or handing off an approval-ready Algorithm draft | Yes |
| A Custom EFF crosses context entities | Blocker |  | The assessment uses a legacy direct relation rather than an evidenced EFF-to-owner-to-OSSTransactions-to-target chain | Establish the complete interface-table lineage and state the source EFF owner, bridge keys, target entity, and duplicate behavior | Yes |
| A Service Mapping assessment is returned | Blocker |  | The result omits an Entities, Sources, or Services tab conclusion, is not presented in chat, or proposes a revised XML artifact | Return exact tab-by-tab verify or add/edit instructions in chat. A complete mapping-gap plan may be used by the companion task for a provisional draft, but must be marked unapplied and unvalidated; do not create a Service Mapping artifact or a human-readable Markdown plan | Yes |
| Source discovery or compatibility confirmation is required | Blocker | resolve_order_mapping_source_metadata | The candidate is absent, ambiguous, non-queryable when queryability is required, type-incompatible, outside the documented entity context, or no documented describe route is available | Run the documented current-release describe path before requesting clarification for a standard field; recommend only a confirmed candidate and record remaining ambiguity explicitly | Yes |
| A recommendation affects subscription grouping | Blocker |  | The intended grouping result is not evidenced | Identify the affected grouping attributes and intended outcome before returning the assessment | Yes |
| A recommendation affects duration, rate plan, or pricing context | Blocker |  | UOM compatibility evidence is missing or incompatible | Obtain compatible configuration evidence before returning the assessment | Yes |
| Every Service Mapping request | Blocker |  | The request would create, edit, import, publish, deploy, or return revised Service Mapping XML | Keep the result to a read-only assessment and prerequisites | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_order_mapping_source_metadata | Source discovery or compatibility confirmation is required | Confirmed entity, attribute name, type, queryability, metadata evidence status, and candidate confidence | ora_reference_lookups.md |
| resolve_subscription_target_metadata | Target discovery or direct-correlation confirmation is required for any requested Subscription Management entity | Selected entity and documented branch, candidate target identity, type, read/write evidence, business-meaning match confidence, and required OMIntegration revalidation | ora_reference_lookups.md |
| resolve_described_field_exposure | A described standard property must be surfaced through the corresponding Service Mapping entity | Canonical property, Type, selected entity and alias, entity type, conversion outcome, provider mapping, explicit Services flags, and revalidation requirement | ora_reference_lookups.md |
| resolve_subscription_child_resource_metadata | A requested target or correlation is a Subscription Management child object | Documentation branch, documented child collection path, parent identifiers, nested schema path, child field metadata, and descendant identity | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OMSUBMAP.ENFORCE.DESIGN | decision | 4 | design_enforcement | pass->OMSUBMAP.ADVISORY.GATE;blocked->OMSUBMAP.RETURN.ISSUES | OMSUBMAP.RESOLVE.DEPENDENCIES | stop | Dependency readiness is satisfied |

## Sources

- User-approved FOM-to-OSS operating model: the Service Mapping task is read-only and returns an assessment.
- User-approved FOM-to-OSS operating model: describe metadata must support every mapping recommendation.
- User-approved FOM-to-OSS provisional rule: an exact but unapplied three-tab plan may be handed to the companion task only as the basis for a clearly labelled provisional draft.
