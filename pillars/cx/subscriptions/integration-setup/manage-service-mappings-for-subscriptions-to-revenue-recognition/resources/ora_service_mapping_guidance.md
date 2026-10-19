# RMCS Service Mapping Source Guidance

## Ownership and entry

This is the canonical owner for source discovery, source XML interpretation, view-object bindings, attribute types, service access, and mapping/publication prerequisites. The [Algorithms primary](../../manage-algorithms-for-subscriptions-to-revenue-recognition/SKILL.md) owns algorithm identity, version and action selection, Groovy, output behavior, and approved local Algorithm_BO.xml artifacts.

Apply the primary's [input preflight](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_algorithm_xml_guidance.md#input-preflight) before this analysis. Both the current Service Mapping source and Algorithm_BO.xml must be attached. The Service Mapping attachment can have any file name when it contains the current source XML; validate it by content and exact RMCS context, not by file name. That single preflight owns the exact RMCS context, algorithm-name, highest-version and active-state gates; do not substitute a previous sample, a describe response, or another integration's export. Samples are evidence for understanding, not files to package with the skill.

When invoked by the primary, preserve its continuation context and return the [companion handoff](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#companion-handoff-template). The primary resumes automatically at the saved stage. For a direct mapping invocation, return the requested mapping analysis to the implementer; do not invent a suspended primary run. Route subsequent algorithm work to the primary only when it is part of the requested outcome.

## Resolve the functional source

Start with the business rule, header/line/subline target, intended functional owner, source meaning, and required row scope. Resolve a field by business meaning and verified ownership, not by a same-name match on the first object found. Create a [source-resolution record](#source-resolution-record) for every business source used by new Groovy, including sources used in conditions, calculations and output values.

1. Parse current XML with namespace awareness and without external entity or DTD resolution. XML comments do not establish active entities, attributes, provider bindings or service access.
2. Inventory the active context entities, provider mappings, consumer/service identity, and per-entity/per-attribute access. Preserve exact casing and explicitly record missing or duplicate matches.
3. Trace each proposed ordinary source through its entity declaration, attribute type, provider view-object attribute, query/join, and consumer read access. Describe metadata alone does not expose a field in the algorithm's Service Mapping source. If the requested value is absent from active mapping evidence, decide whether it is an ordinary Service Mapping source that needs the [_Custom exposure handoff](#custom-source-exposure-for-ordinary-service-mapping-attributes) or a function-backed provider value that belongs to the primary's function analysis.
4. Check the selected algorithm action separately for its dataset alias, variable path, filter and cardinality. Entity existence is not proof that an alias is available in every step; a provider join is not proof of One or ZeroOrOne cardinality.
5. Apply [candidate validation](#candidate-shape-queryability-and-type-compatibility) and the per-source decision contract below. Present functional-owner, relationship and row-scope alternatives without silently choosing an easier-cardinality source. Preserve an accepted optional owner.
6. Return source-resolution records, rejected alternatives, search coverage and prerequisites. Do not draft Groovy or choose an arbitrary aggregation for multiple matching rows.

The current request's supplied files and user choices are authoritative evidence for local analysis under the canonical input contract. They do not prove Fusion publication or deployed state. Record their provenance and freshness separately from any environment-matched or publication evidence. Do not make live environment verification a global prerequisite for supported analysis or local artifact work using already exposed current sources. A proposed unexposed source remains a Service Mapping prerequisite until refreshed source evidence proves it; the primary may use it only as a clearly labelled conditional assumption after the implementer explicitly asks to proceed on that named assumption.

### Discovery scope and search coverage

| Requirement state | Search decision | Evidence to retain |
|---|---|---|
| Exact owning object and source attribute supplied | Inspect that exact source in current active XML and its applicable provider/action evidence first; do not ask the implementer to select it again | Exact-name decision, current evidence, missing exposure or conflicts |
| Object supplied but attribute unclear | Inspect the named object's active attributes, then relevant environment-matched metadata; do not widen to another object silently | Searched object, exact and semantic candidates, type/operation fit and rejection reasons |
| Attribute or business outcome supplied without an object | Scan active sources, use Subscription business context and general Subscription documentation to identify relevant families, then examine evidence for each plausible functional owner | Families considered and searched, fit reasoning, candidates and rejected alternatives; never default to Subscription or another alias |
| Existing evidence resolves the metadata question | Reuse sufficient current, environment-matched evidence under the input/authority gate | Evidence provenance and why another describe is unnecessary |
| A specific metadata gap remains | Select only the [declared optional describe lookup](../ora-resource/ora_reference_lookups.md#live-lookups) after its gates pass | Exact unresolved question and scoped source family; no broad mandatory GET or automatic endpoint expansion |

Use business context to explain fit, not to prove an attribute exists. Identify explicitly stated objects before considering copied or denormalized fields from another family. If ownership is unclear, return the alternatives for a primary-led decision. A named-source search does not authorize changing the source object; a materially different alternative is a new recommendation requiring acceptance.

## Source-resolution record

This section is the canonical per-source decision schema. The primary and the final output handoff reference these records rather than copying a second schema. Record decisions independently from exposure, publication and runtime-authority evidence.

| Field | Required content |
|---|---|
| source_record_id | Stable reference used by the primary's proposed operations and final handoff |
| business_meaning_and_use | Functional meaning and how the source supports the condition, calculation or output requirement |
| owning_object_and_exact_attribute | Selected business object and exact case-sensitive attribute or unresolved candidates |
| source_origin | Implementer exact source, current-export candidate, describe candidate, or specifically named recommended default |
| alias_and_provider | Current action alias, mapping entity/attribute when applicable, provider kind, and exact VO/REST field; keep unresolved names explicit |
| datatype_and_shape | Observed scalar/object/collection shape, source type, proposed mapping type and compatibility conclusion |
| action_scope_and_cardinality | Selected version/action/record level and dataset/current-row cardinality evidence supplied by the primary; metadata shape is not action cardinality |
| queryability_and_operation | Relevant queryability evidence, intended read/filter/join/provider operation and whether its prerequisites are satisfied, inapplicable or unresolved |
| evidence_and_authority | Current supplied-file fingerprint/location or scoped metadata evidence, provenance and freshness; distinguish authoritative local analysis evidence from any environment/publication claim |
| exposure_access_and_publication | Separate current/proposed/missing status for source exposure, provider binding, applicable access and publication evidence |
| search_coverage_and_alternatives | Examined families, candidate fit, functional-owner reasoning, rejected alternatives and reasons |
| decision_and_reference | Exact source supplied, recommendation pending, explicitly accepted, explicitly declined, or accepted for review only; record the relevant user instruction/acceptance reference |
| assumptions_and_prerequisites | Specifically named assumptions, unresolved evidence and exact next actions; no unnamed defaults |

Apply these decision rules:

- An exact source already supplied by the implementer is a source choice. Record it without asking again; still validate its current applicability, type and exposure. A contradiction or missing fact is a correction/prerequisite question, not permission to select another source.
- Every newly recommended source needs explicit acceptance, including a sole semantic match or one exposed field that merely appears to fit. Distinguish "the attribute exists" from "the implementer chose it for this requirement."
- A recommended default must identify one actual candidate, its evidence and why its functional owner/type fit. Record acceptance of that named candidate; generic "go with assumptions" cannot select a source.
- An accepted source can remain unexposed or publication-unverified. Do not use acceptance to change those evidence states. Hold dependent drafting/artifact readiness for a proposed unexposed source under the primary's gates; lack of live publication verification alone does not invalidate an already exposed current-file source for supported local analysis.
- A changed object, attribute, provider, type, scope or material source requirement reopens the affected decision and downstream proposal. Preserve prior decisions and the reason for change; do not re-ask unchanged, already accepted choices.

## Candidate shape, queryability and type compatibility

Read the actual metadata structure before extracting candidate names. Preserve the exact field name, relevant label, datatype and provenance; do not treat nested object metadata or a list of child objects as a scalar source attribute.

| Metadata or operation | Required validation |
|---|---|
| Scalar field | Verify the exact field, observed type and support for the intended mapping/provider operation |
| Object field | Resolve a supported scalar child and its exact provider path from evidence; do not serialize the object or invent a dotted attribute path |
| Collection field | Preserve collection shape, resolve the intended member scalar where supported, and return the iteration/selection/aggregation decision to the primary; never choose the first item |
| Filter, query or join attribute | Check queryability and the supported predicate/join contract when that operation requires it; absent metadata is unresolved, not implicit true |
| Read-only value access | Check exposure and read/provider support appropriate to that operation; do not reject an otherwise supported value solely because filtering is not queryable |
| String or character type | Confirm compatibility with the proposed mapping/provider type and any verified length limits; do not convert a display code or identifier to number from its name |
| Integer, long, decimal or other numeric type | Preserve the proven numeric type and available precision/scale/range evidence; do not silently narrow, round or invent conversion rules |
| Date or timestamp type | Preserve the distinction and pass it to primary runtime/target guidance; do not invent formatting, timezone or conversion helpers |
| Boolean or coded flag | Distinguish actual Boolean metadata from string-coded values and verify the operation's accepted representation; do not assume Y/N, true/false or a character conversion globally |
| Unknown or conflicting type | Return the conflicting evidence and request the missing compatible-type/provider contract; physical table metadata is not a substitute runtime type system |

An Id suffix is not numeric-type evidence. Map only types supported by the selected RMCS source/provider operation; exact matching type evidence can support compatibility, but a different representation needs its own conversion contract. Queryability, datatype, mapping exposure and selected-action cardinality are separate checks. Primary [runtime guidance](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_groovy_function_guidance.md) owns approved Groovy handling and [target guidance](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_rmcs_data_model_reference.md) owns target-family and conversion decisions.

The following are recognizable source/provider patterns, not a replacement for the attached export:

| Context entity | Provider view object | Relationship to verify in the current source |
|---|---|---|
| Subscription | PricingSubscriptions | SubscriptionId input selection |
| Products | PricingProducts | SubscriptionId joins Subscription.SubscriptionId |
| Charges | PricingCharges | SubscriptionProductId joins Products.SubscriptionProductId; ProductAssociationId may map to CoveredLevelId |
| HeaderSalesCredits | PricingSalesCreditsHdr | SubscriptionId joins Subscription.SubscriptionId |
| ProductSalesCredits | PricingSalesCreditsPrd | SubscriptionProductId joins Products.SubscriptionProductId |

Do not assume business or custom fields are exposed merely because these entities exist. For an unexposed source field, return its verified owning object and describe type, the required entity/provider/access additions as an unexecuted prerequisite, and the effect on the primary action's available data. If the exact object or attribute cannot be confirmed, derive named candidates from the current mapping, Subscription context and allowed describe metadata, then request implementer selection; proceed only with explicitly accepted, named assumptions. A customer-specific field name in an example is not a seeded contract.

### Custom-source exposure for ordinary Service Mapping attributes

Use the accepted RMCS Service Mapping handoff contract for ordinary source attributes that are needed by Groovy but are not exposed in the current Service Mapping source. Recommend a new context-entity attribute named `<sourceAttributeName>_Custom` on the selected related object/entity. If the selected Service Mapping alias or implementer-supplied variable already ends with `_Custom`, do not append the suffix again.

Resolve the selected object and exact underlying view-object attribute before recommending the alias. In the provider/source layer, map the new context-entity attribute to the exact VO attribute, preserving its case and type. Example: expose `LegalEntityName_Custom` on the `Subscription` entity, map it in Sources to `LegalEntityName` on the Subscription view object/provider (`PricingSubscriptions` in the known pattern), then reference the Service Mapping alias only after the implementer accepts or supplies refreshed source evidence.

When the source is a Subscription or Product DFF, flex or custom value, preserve the datatype from current mapping evidence, describe metadata or the implementer's explicitly accepted named assumption. Recommend a string `_Custom` attribute for string values, a compatible numeric `_Custom` attribute for numeric values and a date-compatible `_Custom` attribute for date values. Return the alias, owning object, exact VO attribute and datatype to the Algorithms primary so it can choose the matching RMCS target family. This companion does not select or increment target DFF/flex slots.

In Services, instruct the implementer to add the attribute under the same related object section and enable the required access for algorithm use. For this RMCS handoff, state read access is required for Groovy source consumption and include write access when the implementer is configuring the new Service Mapping attribute according to the supplied setup instruction. Record the access as proposed until the refreshed source proves it.

This contract is only for ordinary Service Mapping source inputs. Do not apply `_Custom` to function-backed ProductAssociations/BillLines provider values, to protected output entities RmcsDoc/RmcsDocLines/RmcsDocSublines, or to RMCSInterface insert target attributes. Do not edit the supplied Service Mapping text file, claim the configuration was created, or claim publication. Return the configuration steps and require refreshed View Source XML before treating the new source exposure as established; if the primary proceeds on a named assumption, keep the Groovy/XML result conditional and runtime readiness pending.

## Protected output schema and runtime access

Do not add, remove, rename or modify attribute definitions, types, provider mappings or service access for RmcsDoc, RmcsDocLines or RmcsDocSublines. These are protected output entities. A proposed new target column is an algorithm output-routing question, not permission to extend these entities. Return the confirmed target exposure to the primary's [Groovy guidance](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_groovy_function_guidance.md).

Distinguish schema changes from changing the value of an existing writable output attribute through the selected algorithm action. For the latter, verify the exact output entity/attribute and both entity-level and attribute-level write access; a declaration alone does not authorize a direct assignment.

| Output entity | Binding details to preserve | Checks that affect primary processing |
|---|---|---|
| RmcsDoc | RmcsDocVO; DocumentId identifies a document | Verify each requested attribute's type and write access |
| RmcsDocLines | RmcsDocLinesVO; DocumentLineId identifies a document line | ExtractionStatus can be exposed with write=false; never treat all line attributes as writable. Report every active `SrcAttributeChar*`, `SrcAttributeNumber*` and `SrcAttributeDate*` attribute exposed on RmcsDocLines as line DFF/flex occupancy evidence for the primary; this is not permission to direct-assign it |
| RmcsDocSublines | Exact spelling has a lowercase l in Sublines; RmcsDocSubLinesVO uses different casing | DocLineId may map to VO DocumentLineId and join RmcsDocLines.DocumentLineId; preserve the current export's actual binding |

SkipFlag and ReferenceId can be declared, readable and writable output/control attributes without provider VO attribute mappings. Do not apply the source-input provider requirement to these runtime output/control attributes. Verify their declaration, type, access and selected-action availability. SkipFlag is a string in the supplied RMCS pattern; do not turn it into a Boolean. The primary owns skip values, target scope, direct-write syntax, and the prohibition on subline inserts.

For a line DFF/flex target, the companion does not choose the replacement slot. It returns the current RmcsDocLines `SrcAttribute*` occupancy, type and read/write access to the primary. The primary decides whether an implementer-supplied exact slot may be modified or whether a new assumption-backed slot must be selected and written through `RMCSInterface.insert`.

For ordinary source inputs, all three layers remain necessary: entity attribute definition, provider mapping, and consumer read access. If one is missing, return source exposure as a prerequisite rather than claiming the source is available. When recommending a new ordinary source attribute, apply the `_Custom` exposure handoff above and identify the intended entity alias, VO attribute and service access. Do not add provider mappings to output controls merely to make those layers look uniform.

Physical table names, column names and lengths are maintained in the [source catalogue](../ora-resource/ora_reference_lookups.md#source-catalogue) and the primary's [data-model reference](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_rmcs_data_model_reference.md). Database column existence does not prove runtime alias, write permission, source translation or Service Mapping extensibility. The scoped assisted rules do not establish Fusion mutation, setup-verification or downstream-result contracts; those remain separate and blocked rather than prerequisites for unrelated supported analysis.

## Function-backed source objects

ProductAssociations and BillLines can be supplied by algorithm functions rather than active Service Mapping entities. Commented-out XML definitions are not exposure. Do not create custom Service Mapping entities for these objects merely to support the algorithm's existing function datasets. When a requirement names one of their attributes, verify the exact provider field, type, shape and selected action dataset through current algorithm evidence and supported describe metadata where needed; return those facts to the primary instead of treating the missing Service Mapping entity as a required mapping edit.

Send function binding, selected dataset, variable-path changes, filters and cardinality decisions to the primary's [Groovy function guidance](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_groovy_function_guidance.md). Inspect the current algorithm before calling a function unwired: a BillLines dataset may already invoke filterBillLinesbyChargeId. A direct VO/function attribute may not require a Service Mapping custom attribute, but its actual availability, datatype, functional ownership and action cardinality still require evidence. Covered-level and bill-line describe results support that analysis; they do not convert either object into an active mapping entity.

## Implementer Service Mapping handoff

When the implementer needs to provide the current Service Mapping source, give these RMCS-specific input steps:

1. Navigate to Subscriptions > Subscription Configuration > Dynamic Matrix Configuration > Manage Service Mappings.
2. Select the `Subscription RMCS Integrations` row.
3. From Actions, use View Source XML.
4. Copy the source XML into a text file and attach it to the request. The file name can vary; the content must pass the `RMCSInterface` context validation.

When Groovy or an Algorithm_BO.xml artifact depends on a Service Mapping assumption, include the Service Mapping configuration handoff with the response:

1. List every assumption used in Groovy, including source object, Service Mapping alias, exact VO attribute, datatype if known, and whether the source is existing, proposed or accepted only as an assumption.
2. Tell the implementer to enter a Sandbox and add Manage Service Mapping as a tool if it is not already available.
3. Navigate to Subscriptions > Subscription Configuration > Dynamic Matrix Configuration > Manage Service Mappings > Subscription RMCS Integrations.
4. In Entities, add the attribute row on the selected related object. Any newly added ordinary source attribute must end with `_Custom`.
5. In Sources, select that entity attribute and map it to the exact view-object attribute, for example `LegalEntityName_Custom` to `PricingSubscriptions.LegalEntityName`.
6. In Services, add the row under the same object/attribute section and enable the required read/write options for the new mapping attribute according to the customer's configuration policy.
7. For DFF/flex/custom sources, include the selected datatype in the handoff so the primary can match it to the proper character, number or date target family.
8. After configuration, the implementer can publish the Sandbox and runtime-test with the approved Algorithm change. The skill does not publish or verify runtime behavior; require refreshed View Source XML before claiming the mapping exposure is present.

## Optional describe lookup route

Use the [canonical live-lookups contract](../ora-resource/ora_reference_lookups.md#live-lookups) for all describe paths, request/response mechanics, client routing, preflight, authority, environment, privilege, audit and retry gates. Do not duplicate endpoint tables or invent a second acquisition route here. Select it only for a specific unresolved metadata question after the discovery decision above; sufficient current environment-matched evidence avoids an unnecessary call.

No HeaderSalesCredits or ProductSalesCredits describe path is established. Return a missing-route prerequisite when valid existing evidence is insufficient; do not infer a route from the VO name. Function-backed source metadata remains distinct from Service Mapping entity exposure.

## Failure and review-only assumption outcomes

Return the observed outcome and exact corrective question to the primary. Do not collapse a completed search into a connection failure or turn a chosen source into proof of exposure.

| Observation | Companion result and corrective action for the primary |
|---|---|
| Successful search with no viable source | Record the searched scope and rejection reasons; request the owning object/exact attribute or a revised requirement, not a transport retry |
| Multiple plausible sources or unresolved functional owner | Return named alternatives and evidence with needs_decision; require selection instead of choosing the first/easier source |
| Sole newly recommended source | Return the named candidate with needs_decision until explicitly accepted, even if its metadata match is strong |
| Selected source missing required mapping/provider/access evidence, or proposed new exposure not yet established | Preserve its source choice but return prerequisite_pending with the exact configuration/evidence gap, including the `_Custom` entity/source/service handoff when it is an ordinary unexposed source. Describe existence does not resolve it. Keep publication unverified separately unless a publication claim or applicable prerequisite requires proof. If the implementer explicitly accepts a named assumption, mark it conditional rather than confirmed |
| Describe connection, authentication, privilege, transport or endpoint failure | Record the failed metadata scope and available sanitized status/classification; let the primary ask whether to remedy and repeat the same authorized lookup or review specifically named unconfirmed assumptions |
| Metadata shape/type/operation incompatibility | Return the incompatible fact and required scalar/provider/type evidence; do not invent coercion, queryability or a replacement source |
| Missing current input/freshness or requested live-operation identity evidence | Return the prerequisite for the affected input or live lookup under its canonical gate; do not confuse this with missing deployed-state proof for otherwise supported local analysis |

If the primary offers a review-only assumption path, require explicitly named assumptions and record the implementer's acceptance in the source-resolution record. This allows review of recommendations or a conditional primary proposal only: it never supplies an unnamed source or bypasses input validation, authority/freshness, actual source/access/publication evidence, context confirmation, or Groovy/XML approval. Keep runtime readiness and confirmed-exposure status gated until refreshed evidence is supplied. A failure does not authorize another endpoint, browser, direct client or authentication route; retry mechanics remain with the canonical lookup owner.

## Outcomes and continuation

Use the canonical [companion handoff template](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#companion-handoff-template), not a second competing return schema. Reference the source-resolution records and return the saved continuation context. Contribute source configuration facts to the primary-owned [final traceability and configuration handoff](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#final-traceability-and-configuration-handoff): exact alias/type, VO attribute, joins, access, existing/proposed state, publication prerequisites and remaining implementer actions. The primary supplies algorithm/output facts and owns the one complete handoff shown in chat and aligned with the approved proposal and conditional local artifact. Use the implementer handoff steps above where applicable; do not invent additional RMCS UI/export steps.

- Confirmed: return the accepted source decision and separately verified exposure/access/target facts. The primary resumes its saved stage and decides Groovy/direct-write/insert behavior under its own rules.
- Decision required: return the competing functional sources or row scopes and one concrete choice needed. Do not mark either alternative confirmed before the implementer decides.
- Prerequisite required: return missing source exposure, describe authority, target access or publication evidence needed for the specific proposed source or deployment claim. The primary can continue unaffected local analysis and may produce a conditional proposal only after explicit acceptance of the named assumption, but it cannot present the dependent branch as runtime-ready.
- Rejected: return failed identity/context/input validation without trying to repair or relabel an unrelated attachment.

This companion performs no Service Mapping XML rewrite, import, publication or other Fusion write. A needed change is a prerequisite for separately authorized work in a workflow that declares the required operation. After such work, require refreshed current-source evidence before treating newly proposed exposure as established for local analysis, and publication evidence before claiming publication. Planning or naming a change establishes neither. Keep these evidence states separate so deployment verification does not block unrelated supported local work.

Classify failures as input validation, catalog mismatch, auth/authz, transport/environment, Fusion API, artifact persistence, or approval blocker as applicable. Retain the exact failed stage, sanitized reason, environment, evidence references and next action. Do not loop back to the same unresolved primary request without new evidence or a new implementer decision. Document acceptance scenarios and expected evidence through the primary's final handoff/checklist owner; do not execute them while authoring skills.
