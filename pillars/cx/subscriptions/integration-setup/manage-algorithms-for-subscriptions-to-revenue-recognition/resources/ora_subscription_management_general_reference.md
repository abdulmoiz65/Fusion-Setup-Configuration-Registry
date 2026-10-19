# Subscription Management Context for RMCS Algorithms

Subscriptions-to-Revenue-Recognition requests must retain their document, line or satisfaction-event meaning. Do not reuse Receivables interface behavior because the skills share a primary/companion structure.

Read the [source catalogue](../ora-resource/ora_reference_lookups.md#source-catalogue) for the Subscription Management guide, the Revenue Management guide's integration context and physical table evidence. The unrelated 25D readiness article is not a source for this workflow. Public physical-column documentation does not by itself establish algorithm aliases, access, Groovy helpers or deployment support.

Use the current user-supplied algorithm and Service Mapping source for runtime structure. The authoring attachments established structural examples only; they are not bundled templates or substitutes for current inputs. User-provided business examples do not become default customer fields or values.

## Resource routing

| Question | Read |
|---|---|
| Is this the correct active input and action? | [Algorithm XML guidance](ora_algorithm_xml_guidance.md) |
| Who owns source discovery and how does the companion return? | [Use-case resolution](ora_use_case_resolution.md) |
| Where may this value be written? | [RMCS data model](ora_rmcs_data_model_reference.md) |
| How should selected source values and existing code be handled? | [Groovy and functions](ora_groovy_function_guidance.md) |
| What must the final proposal/configuration handoff show? | [Final traceability and configuration handoff](ora_use_case_resolution.md#final-traceability-and-configuration-handoff) |
| Which behavior and evidence should a later review expect? | [Documented acceptance cases](ora_use_case_resolution.md#documented-acceptance-cases) |

The active assisted workflow supports evidence review, Groovy proposals and explicitly approved local Algorithm_BO.xml preparation. It does not select a Fusion import, publication or execution route.

## Remaining RMCS evidence

Use this index for RMCS-specific handoff guidance and remaining gaps. Ask for missing guidance only when the corresponding decision is needed. This index does not make every item a prerequisite for unrelated local analysis. Current supplied files and recorded implementer choices are authoring evidence; they do not establish publication or successful Fusion execution.

| Area | Evidence and owning guidance |
|---|---|
| Custom-source alias naming | The accepted RMCS handoff for ordinary unexposed source attributes is `<sourceAttributeName>_Custom` on the selected Service Mapping object/entity, mapped in Sources to the exact selected VO attribute and exposed in Services with the required access. Do not use this for function-backed ProductAssociations/BillLines or protected RMCS outputs. The companion's [`_Custom` exposure guidance](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md#custom-source-exposure-for-ordinary-service-mapping-attributes) owns source decisions and exposure evidence |
| General runtime helpers and conversions | RMCS-specific runtime documentation or current supported capability evidence for helper name/signature, accepted input and result types, null behavior and date/number conversion. Existing examples do not prove general helper support; the [Groovy guide](ora_groovy_function_guidance.md) owns the supplied date/timestamp policy and capability gate |
| Line-extension FlexContext | Confirmation of the deployed context resolving the prose/example conflict for a new line-extension insert. The [line FlexContext gate](ora_rmcs_data_model_reference.md#line-flexcontext-confirmation) owns the decision; do not borrow an AR context |
| Missing subline step and new row identities | The primary can create the missing subline step locally by cloning the unambiguous highest-version line step, adding the `RmcsDocSublines` data set and generating new UUID-shaped row identities after explicit approval. Follow [missing subline step](ora_algorithm_xml_guidance.md#missing-subline-step). Stop only when the source line step is missing, duplicated or structurally ambiguous, or when validation/comparison fails |
| Export and manual handoff instructions | RMCS implementer instructions are captured in [Algorithm export/import handoff](ora_algorithm_xml_guidance.md#implementer-algorithm-export-and-import-handoff) and [Service Mapping handoff](../../manage-service-mappings-for-subscriptions-to-revenue-recognition/resources/ora_service_mapping_guidance.md#implementer-service-mapping-handoff). They explain how the implementer supplies current files and later performs manual UI import/configuration. They do not authorize Codex import, publish or runtime verification |

Record each applicable gap, its evidence reference and safe next action in the primary's final handoff. Public documentation and example exports may support a stated detail; neither authorizes a Fusion action under this local authoring workflow.
