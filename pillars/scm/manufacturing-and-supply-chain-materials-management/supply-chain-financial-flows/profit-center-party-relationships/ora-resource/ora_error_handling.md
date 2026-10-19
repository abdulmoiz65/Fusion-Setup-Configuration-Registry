# PCBU diagnostics and handoff gate

Operation scope: historical parent-only restrictions below apply to parent-create/header-update. For buyer-create/buyer-edit/buyer-delete or seller-create/seller-edit/seller-delete, evaluate the respective profile sections and their transport gate instead; shared identity, environment and artifact rules still apply.


For parent operations this resource validates one parent-only create or header-update artifact; completing these rules does not submit it. This resource does not author payloads, REST writes or runbook processing. The generated task declares core.data-loader as the import route; that route's live validation, immutable-artifact review and approval workflow must be followed separately. Data Loader automatic read-only-field filtering is explicitly deferred, not verified.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Authoring contract incomplete | Stop before planning or execution; report the owning file and unresolved canonical fields |
| Header create reports an existing PCBU | Report the returned duplicate/existing-record message and stop. Do not switch to update, alter the BU, change keys, or retry creation automatically |
| Header-only create scope | Evaluate header inputs and supplied header LOV selections only. Do not create child rows or require child ParentIdentifier propagation for this test. For a parent-only request, populated child rows require separate buyer intent and the buyer dependency gate |
| Multiple LOV candidates | Return the full candidate list with useful names/codes and request a choice before continuing; this is input clarification, not approval to submit an import |
| Registration/schema disagreement | Compare the final artifact to live target metadata through core.data-loader and stop on disagreement. For minimal header creation enforce the input file's writable-field restriction; omit the generated PCRelationshipId and do not depend on backend read-only filtering or child linkage |
| Unavailable source during a later run | Report access failure without declaring source missing. This review read source successfully outside the sandbox; do not run view setup, refresh or recovery merely to bypass source access |
| FOS_CRCT_BILL_TO_LOC_RECS or FOS_CRCT_SUPP_SITE_RECS | Parent revalidation detected invalid child bill-to or supplier-site records; inspect the relevant child and reference resolver. Source: ProfitCenterBuHeaderEOImpl.java validateBillToLocAndThrowEx:1657 and validateSuppSiteAndThrowEx:1666. Do not retry unchanged input |
| Live request previously failed or outcome unknown | Do not retry; disclose sanitized status and reconcile previous effects through the approved workflow |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Shape, identity or required contract unresolved | Resolve the specific input contract; do not invent values |
| Approval blocker | No approved import artifact/environment or authoring-only request | Stop; later invoke the declared Data Loader workflow when requested |
| Transport/environment | Source unavailable or deployed metadata not established | Restore source access and verify release-specific behavior |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Rule validation handoff | Task code/name, reached rule, outcomes, unresolved fields, source limitations and zero Fusion side effects |
| Header-only Data Loader preflight | The calling Data Loader workflow must validate the exact registered business object, live headers/operation, target environment and prepared header-only artifact before approval. Do not invent surrogate IDs. Do not supply read-only fields and assume automatic filtering. Preserve filtering as a disclosed deferred check; stop on schema disagreement or preparation failure |
| Header-only submission approval | Present the resolved BU, optional selections, exact target environment and validated immutable artifact using core.data-loader's approval workflow. No live creation is authorized by completing these resource rules. Accepted submission is not proof of a successfully created header |
| Import preparation | A ready scoped rule plan is permission to evaluate rules, not evidence that an import file passed. Require the selected environment, live metadata validation, resolved lookup evidence, and exact immutable header-create artifact to pass before approval. Buyer requests follow the operation-specific extension and transport gate; other unsupported-field updates remain unsupported; never present templates or synthetic fixtures as validated live test data |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Registry exists but readiness incomplete | Do not override readiness or execute an import |
| APEX export contains MERGE_DELETE or HCM seed-data paths | Do not infer delete support or correct seed ownership from exporter defaults; verify through the uptake workflow before seeding |
| Deferred foreign keys or user keys | Do not add mappings, trust cross-environment IDs or claim reference validation is unnecessary |

## Uptake and remaining verification

The developer-provided Data Loader - Uptake Instructions for seeding Business Objects.pdf requires registration in a DIT environment, Update Attributes, completion in View Update Processes, then testing before seed extraction/merge. It does not specify ExcludeInPayload filtering, surrogate creation or parent-ID propagation. Do not execute its SQL, metadata updates or seeding commands under an authoring request.

The FSCR client handles schema validation and DAT preparation; this review has not established the backend adapter's empty-ExcludeInPayload behavior. Required evidence is a supported adapter contract or sanitized generated metadata and a verified PCBU mapping example. For new-parent plus child creation, explicitly establish generated surrogate and ParentIdentifier/ParentId semantics; do not equate those two field names or invent a parent ID. Buyer planning follows the extension below; buyer execution remains gated on the child transport contract. Other unsupported-field or filtering-dependent requests must stop. The minimal header-create experiment excludes those cases and still requires live Data Loader validation before approval; no direct REST or import fallback.

## Backend source trace evidence

Read-only search on 2026-09-15 used the indexed FUSIONAPPS_PT.V2MIBSCPSILVER_LINUX.X64 series and the developer-selected kbhinde_kishan0203 view. Indexed ExcludeInPayload searches and a ParentIdentifier search scoped to dataLoader returned no matches. A path search located hcm/components/hcmCoreSetup/common/dataLoader. One bounded symlink-following source fallback in that component searched Java/XML for ExcludeInPayload, ParentIdentifier and SurrogateIdColumnName. Matches for the last term occurred in classic metadata and external-interface classes, but did not establish the requested REST adapter behavior. A further bounded check for ADF_REST, REST_ADAPTER, RestAdapter, MetadataOverride, metadata_override and EXCLUDE_IN_PAYLOAD found no matches there.

This is a scoped negative result, not proof of absence from Fusion or from another branch/repository. No backend filtering or parent-ID propagation behavior is asserted. Do not change APEX settings on this evidence. The required next source is the implementation/branch that consumes ADF_REST registration metadata, specifically ExcludeInPayload and ParentId, or an authoritative adapter contract with equivalent behavior. Classic InterfaceDataSource surrogate handling is not a verified substitute.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCBU.CHECK_HANDOFF | step | 60 | execution_gate | success->PCBU.RETURN_RULE_RESULTS;failure->PCBU.RETURN_ISSUES | PCBU.CHECK_DESIGN | stop | Return rule results only; this node never submits Data Loader work |
| PCBU.RETURN_ISSUES | terminal | 70 | terminal | none | none | stop | Any failed rule; return issues without mutation |
| PCBU.RETURN_RULE_RESULTS | terminal | 80 | terminal | none | PCBU.CHECK_HANDOFF | stop | Return validated rule results only; never claim import success |

## Header update diagnostics

Header update must not convert a duplicate-create error into PATCH automatically. It requires a separate explicit update request and newly validated source. Missing existing parent, multiple parents, supplier ambiguity, invalid legal-entity supplier, null clearing requests, unsupported headers, POST fallback, and identity mismatch stop before approval. Existing child relationships may cause parent revalidation errors; surface Fusion's error and do not modify or delete children to force the header update.

Before approval show the selected BU, old and new values for each requested field, exact environment and immutable artifact. Report no change without uploading when all requested values are already selected. Never claim a live update passed from registry readiness or local fixtures. A failed or indeterminate PATCH/load must not be repeated automatically. Use the shared Data Loader status workflow when requested, and distinguish accepted initiation from a successfully loaded update.

## Buyer errors and verification

| Situation | What Should Happen |
|---|---|
| Buyer transport evidence missing | Report buyer planning complete but execution blocked by unverified deployed child registration/linkage/operation contract. Keep parent operations available; never substitute direct REST batch |
| FA_SHARED_ITEM_NULL on buyer create | Inspect ProcurementBUId and PayablesInvoicingBUId; REST row create requires both. Do not invent defaults |
| FOS_FOSTP_NO_DEL_OF_ICBP_11 | Buyer deletion is blocked by trade relationships. Report the dependency; do not delete relationships to force success |
| Invalid bill-to BU | Recheck procurement service-provider BU and parent's primary ledger together; backend validates both |
| Partial failure or unknown outcome | Reconcile parent site, payables child and customer rows through the routed workflow before any retry. Do not assume Redwood batch semantics provide Data Loader atomicity |

Before buyer approval, show operation, PCBU, target environment, current and requested BU/site/address values, removed rows, profile-delete cascade impact and the immutable validated artifact. After successful process completion, reread payables identity, header party site and customer rows; verify requested changes and retained fields. For delete, verify buyer absence and customer-row outcome while parent and seller remain present as applicable. Record source-only, schema-validated and live-tested coverage separately. No live buyer CRUD test was performed in this authoring change.

## Seller errors and verification

| Situation | What Should Happen |
|---|---|
| Missing supplier or buyer-detail row on create | Report prerequisite; Redwood requires a parent supplier and at least one buyer-detail row. Do not add dependencies or placeholder rows |
| FOS_FOSTP_NO_DEL_OF_ICSP_11 | Report seller delete dependency failure; do not remove trade relationships or supplier rows to force deletion |
| Insert-only change requested | Explain affected field and prepare a replacement proposal; no silent delete/add or retry of PATCH |
| Set derivation mismatch | Stop and retain actual assignment/set result; investigate deployed behavior instead of forcing the displayed set ID |
| Partial or unknown process outcome | Read back assignment and supplier rows before proposing retry; do not assume batch atomicity |

Before approval show environment, PCBU, operation, receivables BU and set context, supplier-row before/after values, explicit row removals/replacements and profile-delete cascade impact. Require the Data Loader immutable-artifact workflow. After success verify assignment identity, IntercompanyReceivablesBUId, ICReceivablesCustomerAddrSetid and every affected SupplierAssociation row, plus preservation of parent and buyer data. Source coverage, generated metadata validation and live CRUD tests are separate results. No live seller operation was performed during this authoring change.
