# Subscription to RMCS Service Mapping Reference Lookups

## Scope and authority

This resource owns lookup mechanics and the preserved physical-documentation ledger. The current user enhancement contract authorizes assisted authoring checkpoints using the request's current supplied files and recorded decisions as local evidence. It does not authorize Fusion writes or equate those inputs to published state. The former incomplete live workflow is retained under Unsupported live contracts, outside the assisted graph. The authoring prompt and explicit authority clarification are sources for this route; sample attachments are not bundled.

## Source catalogue

| Source ID | Documentation | Use and release boundary |
|---|---|---|
| G1 | [Using Subscription Management](https://docs.oracle.com/en/cloud/saas/subscription-management/fasum/using-subscription-management.pdf) | Supplied unversioned guide; integration discussion, printed pages 27-28. Not a Service Mapping configuration specification. |
| G2 | [Using Revenue Management, 26B](https://docs.oracle.com/en/cloud/saas/financials/26b/fafrm/using-revenue-management.pdf) | Supplied guide; only Guidelines for Integrating Revenue Management with Subscription Management, printed page 94. |
| G2C | [Using Revenue Management, 26C](https://docs.oracle.com/en/cloud/saas/financials/26c/fafrm/using-revenue-management.pdf) | Newer verified edition of the same integration section; not authority for unrelated Financials setup. |
| SH | [OSS_RMCS_DOC_T](https://docs.oracle.com/en/cloud/saas/sales/oedms/ossrmcsdoct-26506.html) | Supplied source header definition; current unversioned OEDMS destination. |
| SL | [OSS_RMCS_DOC_LINES_T](https://docs.oracle.com/en/cloud/saas/sales/oedms/ossrmcsdoclinest-21926.html) | Supplied source line definition; current unversioned OEDMS destination. |
| SS | [OSS_RMCS_DOC_SUB_LINES_T](https://docs.oracle.com/en/cloud/saas/sales/oedms/ossrmcsdocsublinest-11773.html) | Supplied source subline definition; current unversioned OEDMS destination. |
| TH25D | [VRM_SOURCE_DOCUMENTS, 25D](https://docs.oracle.com/en/cloud/saas/financials/25d/oedmf/vrmsourcedocuments-26721.html) | Supplied target header baseline. |
| TH26B | [VRM_SOURCE_DOCUMENTS, 26B](https://docs.oracle.com/en/cloud/saas/financials/26b/oedmf/vrmsourcedocuments-26541.html) | Newer verified header edition; not a claim that no later edition exists. |
| TL25D | [VRM_SOURCE_DOC_LINES, 25D](https://docs.oracle.com/en/cloud/saas/financials/25d/oedmf/vrmsourcedoclines-30660.html#Details) | Supplied target line baseline. |
| TL26C | [VRM_SOURCE_DOC_LINES, 26C](https://docs.oracle.com/en/cloud/saas/financials/26c/oedmf/vrmsourcedoclines-31165.html) | Newer verified line edition; release-specific fields must be checked against the deployment. |
| TS26A | [VRM_SOURCE_DOC_SUB_LINES, 26A](https://docs.oracle.com/en/cloud/saas/financials/26a/oedmf/vrmsourcedocsublines-19061.html) | Supplied target subline baseline. |
| TS26C | [VRM_SOURCE_DOC_SUB_LINES, 26C](https://docs.oracle.com/en/cloud/saas/financials/26c/oedmf/vrmsourcedocsublines-19621.html) | Newer verified subline edition. |

Only this source set and its verified newer editions inform Oracle behavior here. AR mappings, Groovy examples, earlier Confluence attachments and unrelated readiness features are not technical authority for this package.

## Physical object identities

This is a layer comparison, not a deployed mapping or a SQL join specification. The physical target names below correct the shorthand names supplied in the request.

| Layer | Source physical object and identity | Target physical object and identity | Important distinction | Sources |
|---|---|---|---|---|
| Header | OSS_RMCS_DOC_T; DOCUMENT_ID NUMBER(18) primary key; DOC_ID_INT_1 identifies the subscription | VRM_SOURCE_DOCUMENTS; DOCUMENT_ID NUMBER(18) primary key; separate DOC_ID_INT_1-5 and DOC_ID_CHAR_1-5 source keys | An OSS document key, subscription key and VRM document key are not established as interchangeable | SH; TH25D; TH26B |
| Line | OSS_RMCS_DOC_LINES_T; DOCUMENT_LINE_ID NUMBER(18) primary key; DOC_ID_INT_2 described as parent document foreign key; DOC_LINE_ID_CHAR_1 revenue-line identity | VRM_SOURCE_DOC_LINES; system-generated DOCUMENT_LINE_ID NUMBER(18); DOCUMENT_ID parent foreign key | DOC_ID_INT_2 differs from DOC_LINE_ID_INT_2; physical linkage does not establish mapper aliases or cardinality | SL; TL25D; TL26C |
| Subline | OSS_RMCS_DOC_SUB_LINES_T; DOCUMENT_SUB_LINE_ID NUMBER(18) primary key; mandatory DOCUMENT_LINE_ID NUMBER(18) | VRM_SOURCE_DOC_SUB_LINES; system-generated DOCUMENT_SUB_LINE_ID NUMBER(18); DOCUMENT_LINE_ID and DOCUMENT_ID foreign keys | Target has separate header, line and subline source-key groups; resolve the deployed association contract | SS; TS26A; TS26C |

## Source column evidence

| Layer or group | Verified metadata | Interpretation boundary | Source |
|---|---|---|---|
| Header text | DOCUMENT_NUMBER VARCHAR2(300); CURRENCY_CODE VARCHAR2(15); CUST_PO_NUMBER VARCHAR2(50); CURR_CONVERSION_RATE_TYPE VARCHAR2(30) | Validate the actual selected column, not a similarly named runtime field | SH |
| Header conversion | DOCUMENT_DATE and CURR_CONVERSION_RATE_DATE DATE; CURR_CONVERSION_RATE NUMBER | Conversion-date conditionality is distinct from physical nullability | SH |
| Header identifiers | ORG_ID, LEGAL_ENTITY_ID and bill-to identifiers NUMBER(18) | Numeric equality is not proof of correct business identity | SH |
| Line labels and units | DOC_LINE_ID_CHAR_1 and LINE_NUM VARCHAR2(30); UOM_CODE and CHARGE_UOM VARCHAR2(200) | LINE_NUM denotes product number; source string capacity does not prove target semantic compatibility | SL |
| Line source attributes | SRC_ATTRIBUTE_CHAR1-5 VARCHAR2(150): charge name, price type, periodicity, external-asset key, product PUID | These slots already have documented meanings; not an unused-slot list | SL |
| Line RMCS attributes | RMCS_ATTRIBUTE1-3: charge name, charge type, balance-register number; RMCS_ATTRIBUTE_NUMBER1-3: allowance, actual usage, top-up usage; RMCS_ATTRIBUTE_DATE1-2: bill-period boundaries | Character fields are VARCHAR2(150), numeric fields NUMBER, dates DATE; not a promise of mapper exposure | SL |
| Line additional metadata | SRC_ATTRIBUTE_CHAR13 is individually documented; SRC_ATTRIBUTE_NUMBER1-4 are NUMBER; RMCS_ATTRIBUTE_CATEGORY VARCHAR2(30) | Do not extrapolate an uninterrupted source range or invent a context literal; numeric type takes precedence over the inconsistent character comment | SL |
| Subline satisfaction | SATISFACTION_MEASUREMENT_DATE DATE; SATISFACTION_EVENT_QUANTITY and SATISFACTION_EVENT_PERCENT NUMBER | Percentage applies to the percentage-satisfied model; no numeric bounds are supplied here | SS |
| Subline classification | DOC_SUB_LINE_TYPE VARCHAR2(30); PROCESSED_FLAG VARCHAR2(1) | Length is not an enumeration; accepted runtime values remain TBD | SS |

## Target column evidence

| Layer or group | Verified metadata | Interpretation boundary | Sources |
|---|---|---|---|
| Header stored requirements | DOCUMENT_ID and APPLICATION_ID NUMBER(18); DOCUMENT_NUMBER VARCHAR2(300); DOCUMENT_TYPE VARCHAR2(30); DOCUMENT_DATE DATE; DOCUMENT_CREATION_DATE and DOCUMENT_UPDATE_DATE TIMESTAMP are required stored fields | Database requirements are not the Service Mapping request schema or a requirement to supply generated values | TH25D; TH26B |
| Header and line generic source attributes | SRC_ATTRIBUTE_CHAR1-60 VARCHAR2(150); SRC_ATTRIBUTE_NUMBER1-20 NUMBER; SRC_ATTRIBUTE_DATE1-10 DATE | Extensible groups at these layers; corresponding source slots and deployed use must still be verified | TH26B; TL26C |
| Line fields | UOM_CODE VARCHAR2(200); QUANTITY and UNIT_SELLING_PRICE NUMBER; DOCUMENT_DATE DATE | Required stored fields; runtime names, accepted formats and population responsibility remain unverified | TL25D; TL26C |
| Line lookup and revision | SATISFACTION_MEASUREMENT_MODEL VARCHAR2(30) references ORA_VRM_SATIS_MEAS_MODEL; VERSION_NUMBER NUMBER(9); VERSION_FLAG VARCHAR2(1) | Lookup values are not enumerated by this page; revision fields are not mapping-definition versions | TL26C |
| Line release difference | INITIAL_PERF_EVENT_DATE DATE is present in reviewed 26C, absent from reviewed 25D | Do not assume availability in an older deployed release | TL25D; TL26C |
| Subline satisfaction and period fields | SATISFACTION_MEASUREMENT_DATE DATE; SATISFACTION_EVENT_QUANTITY and SATISFACTION_EVENT_PERCENT NUMBER; PERIOD_ACTION_CODE VARCHAR2(30); PERIOD_ACTION_EVENT_DATE DATE; PREV_DOCUMENT_SUB_LINE_ID NUMBER(18) | Satisfaction columns exist in both reviewed editions; their deployed binding is a separate unresolved question | TS26A; TS26C |
| Subline generic source attributes | SRC_ATTRIBUTE_CHAR1-60, SRC_ATTRIBUTE_NUMBER1-20 and SRC_ATTRIBUTE_DATE1-10 are marked Oracle internal use only | Not arbitrary customer extension slots | TS26A; TS26C |
| Subline descriptive flexfields | ATTRIBUTE1-20; ATTRIBUTE_DATE1-5; ATTRIBUTE_NUMBER1-5 are described as descriptive flexfields | Distinct from internal SRC groups; this does not establish Subscription mapper support | TS26A; TS26C |

## Mapping evidence still required

| Contract component | Required evidence | Current status |
|---|---|---|
| Mapping identity and operation | Exact deployed service mapping, release, version, supported requested operation and privileges | TBD: task-specific configuration documentation and authoritative acquisition |
| Entity exposure | Runtime entities, attributes, source bindings, contexts, associations and cardinalities. For a new ordinary source attribute, the proposed Service Mapping alias follows `<sourceAttributeName>_Custom` on the selected object/entity unless that accepted alias already ends in `_Custom` | Existing source XML or refreshed source XML proves exposure; proposed `_Custom` rows remain prerequisites or named assumptions until refreshed evidence is supplied |
| Field correspondence | For each change, source entity/attribute, transformation, target entity/attribute, population responsibility and business meaning. A proposed `_Custom` alias must map to the exact selected VO attribute, for example `LegalEntityName_Custom` to `PricingSubscriptions.LegalEntityName` | Same-name or same-index fields do not prove an existing mapping; the `_Custom` handoff is proposed configuration, not deployed proof |
| Extension compatibility | Supported extension mechanism, current slot usage, context, types and downstream consumer expectations | TBD: a documented database column may not be exposed to this mapper |
| Change lifecycle | Supported edit, validation, save/publish, rollback and verification behavior | Manual implementer navigation is documented in the mapping guide; no Codex executor, publication proof or runtime verification is established |

## Local Lookups

The user explicitly authorizes current supplied XML and recorded choices as local authoring evidence, not proof of Fusion publication. Keep acquisition and match mechanics here; source candidate interpretation and decisions remain in the [mapping guide](../resources/ora_service_mapping_guidance.md).

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_rmcs_service_mapping_contract | Every checkpoint | Current raw `Algorithm_BO.xml` and mapping XML plus shared preflight evidence | Apply the [primary preflight](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_algorithm_xml_guidance.md#input-preflight) to the exact pair or reuse the same-request fingerprint-matched result; no stale export fallback | Validated context/consumer and selected-version evidence, input fingerprints and active XML inventory | Stop for missing/wrong/ambiguous inputs; do not relabel another integration |
| resolve_rmcs_mapping_bindings | analysis or handoff | Current XML inventory, action scope, source questions, accepted decisions and any existing environment-matched describe evidence | Trace active source declarations/provider/access and selected function-backed providers; apply the [source-resolution record](../resources/ora_service_mapping_guidance.md#source-resolution-record), candidate rules and `_Custom` exposure handoff for ordinary unexposed sources | Evidence-backed candidates, binding/type/queryability facts, accepted decisions, proposed object/entity alias, exact VO attribute, Services read/write handoff and missing evidence, kept distinct from publication | Ambiguity, no candidate and missing exposure remain distinct outcomes; request only the missing metadata through the declared optional route, or return a named assumption/prerequisite when accepted by the implementer |
| verify_rmcs_mapping_handoff | handoff only | Current source-resolution records, decisions, prerequisites and companion outcome; primary-supplied operation/proposal rows only when available | Match the [companion handoff](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#companion-handoff-template) and available source-owned [final handoff fields](../../manage-algorithms-for-subscriptions-to-revenue-recognition/resources/ora_use_case_resolution.md#final-traceability-and-configuration-handoff) to request identity and fingerprints; compare proposal/version only if supplied | Completed source-owned findings, evidence/status, remaining implementer actions and unchanged continuation identity; primary-owned fields remain pending or N/A when no output operation has been proposed | Return incomplete source-owned handoff or stale evidence; never require or invent primary Groovy, approval or target decisions before analysis returns |

## Live Lookups

Only these optional describe GETs are declared. Select one or more by a recorded missing metadata question; sufficient current evidence takes the no_lookup path. A handoff-only checkpoint never acquires new metadata. Paths are the user-provided RMCS discovery contract, not evidence of successful execution.

Before DESCRIBE_METADATA: finish current-input preflight and local analysis; identify the exact unresolved question; verify the project, environment, authenticated identity, describe privilege and scoped endpoint/query; present that exact GET scope; satisfy any routed read approval; validate redacted audit destinations. Missing prerequisites return an issue without a call.

Use [core.fusion-api.rest-api-client](../../../../../../core/fusion-api/rest-api-client/SKILL.md) and load its standard Fusion REST instructions before a call. Pass partialDescription as a query parameter through that client, not as a hand-built alternate client. The core owns authentication and its single allowed cached-auth refresh. Do not inspect or persist credentials. Record only permitted redacted metadata/provenance and request status through the selected project route.

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| describe_rmcs_subscription_attributes | analysis with a missing subscription metadata question and completed live prerequisites | Verified environment, source object and requested attribute/meaning | GET /crmRestApi/resources/11.13.18.05/subscriptions/describe | Relevant returned attribute names, labels, types, scalar/complex shape and queryability when present | Exact then supported semantic candidates under PricingSubscriptions; interpret with canonical candidate rules | Describe evidence/provenance, candidate facts and missing metadata | Return no-match, ambiguity or acquisition failure separately; never auto-accept |
| describe_rmcs_product_attributes | analysis with a missing product metadata question and completed live prerequisites | Verified environment, source object and requested attribute/meaning | GET /crmRestApi/resources/11.13.18.05/subscriptionProducts/describe | Relevant returned attribute names, labels, types, scalar/complex shape and queryability when present | Exact then supported semantic candidates under PricingProducts | Describe evidence/provenance, candidate facts and missing metadata | Return no-match, ambiguity or acquisition failure separately; never auto-accept |
| describe_rmcs_charge_attributes | analysis with a missing charge metadata question and completed live prerequisites | Verified environment, source object and requested attribute/meaning | GET /crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=charges | Relevant charges attributes, type/shape and queryability when present | Match the charges description only; retain provider and owning object | Describe evidence/provenance, candidate facts and missing metadata | Do not substitute product metadata when the charges description is absent |
| describe_rmcs_covered_level_attributes | analysis with a missing function-provider metadata question and completed live prerequisites | Verified environment and requested ProductAssociations provider attribute | GET /crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=coveredLevels | Relevant coveredLevels attributes, type/shape and queryability when present | Match coveredLevels for algorithm-provider analysis, not mapping entity creation | Candidate VO/provider evidence for primary function analysis | Return unresolved provider metadata; never invent a Service Mapping entity |
| describe_rmcs_bill_line_attributes | analysis with a missing function-provider metadata question and completed live prerequisites | Verified environment and requested BillLines provider attribute | GET /crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=billLines | Relevant billLines attributes, type/shape and queryability when present | Match billLines for algorithm-provider analysis, not mapping entity creation | Candidate VO/provider evidence for primary function analysis | Return unresolved provider metadata; never invent a Service Mapping entity |

No HeaderSalesCredits or ProductSalesCredits describe endpoint is established. Their current XML/provider evidence may be reviewed; an unresolved metadata question needs a documented endpoint or appropriate supplied evidence, not an invented URI.

## Lookup execution rules

| Situation | What Happens |
|---|---|
| RESOLVE_EVIDENCE reached | Evaluate applicable Local Lookups only. Use no_lookup when current evidence answers the question; use needs_describe only for an analysis-phase unresolved question with a selected supported lookup. |
| DESCRIBE_METADATA reached | Apply only selected Live Lookups after every live prerequisite passes; do not run the entire endpoint list. Return obtained evidence or a classified failure. |
| Returned metadata lacks a requested field | Missing queryability/type/shape is unresolved, not false, true or a guessed scalar type. The candidate guide owns compatibility decisions. |
| Describe endpoint unavailable or rejected | Follow the [mapping failure outcomes](../resources/ora_service_mapping_guidance.md#outcomes-and-continuation); never substitute browser, general business-data GET or a mutation. |
| A source question is resolved | Record evidence separately from source acceptance and publication. Only the primary runbook can decide continuation into Groovy. |

## Unsupported live contracts

These blocking gaps are retained outside the assisted checkpoint graph. They must not become hidden prerequisites for otherwise supported local analysis, or be marked complete by a current-file check.

| Future capability | Missing contract | Required completion evidence |
|---|---|---|
| Mapping create/update/save/publish | Codex executor, privileges, payload/operation, preview, approval, verification and recovery remain unsupported. The companion may give manual sandbox steps only | Refreshed View Source XML for exposure evidence and separate publication evidence before claiming deployed state |
| Persisted publication-state acquisition | TBD: authoritative environment read and exact deployed revision correlation | Supported read contract and deployed evidence |
| Subscription integration configuration/status lookup | TBD: environment setup and linked lifecycle acquisition | Separate supported lookup contract |
| Integration execution and result verification | TBD: operation, polling, outcome correlation and recovery | Separate approved implementation workflow |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RMCSSM.RESOLVE_EVIDENCE | decision | 20 | evaluate_result | no_lookup->RMCSSM.CHECK_DEPENDENCIES;needs_describe->RMCSSM.DESCRIBE_METADATA;unresolved->RMCSSM.REPORT_ISSUES | RMCSSM.VALIDATE_INPUT | stop | Evaluate applicable local evidence; choose a live branch only for the documented analysis-phase missing metadata question. |
| RMCSSM.DESCRIBE_METADATA | step | 25 | reference_lookup | resolved->RMCSSM.CHECK_DEPENDENCIES;unresolved->RMCSSM.REPORT_ISSUES | RMCSSM.RESOLVE_EVIDENCE | stop | Execute only the selected describe GET contract after all live prerequisites; never a general GET or write. |
