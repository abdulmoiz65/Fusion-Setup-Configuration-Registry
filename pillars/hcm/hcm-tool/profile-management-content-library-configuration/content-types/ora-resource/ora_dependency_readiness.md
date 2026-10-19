# Content Types Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Supplied configuration | Preserve local intake and confirmed mappings; identify missing required values without comparable-configuration discovery |
| 2 | Fresh customer layer plus seeded catalog | For exact claims, bind one fresh complete task export to the authenticated target and validate the matching packaged seed catalog |
| 3 | Scope ownership | Confirm the request is limited to Content Types and owned relationships |
| 4 | Create-only FSM provider | Require the approved local package receipt and mandatory core.data-loader handoff |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| supplied_configuration_capture | Supplied Content Types configuration | Yes | A review proposal is requested | Verify | Local normalized user input and confirmed source-to-field mappings | capture_content_type_supplied_configuration | All supplied type, property and relationship rows must survive normalization | Identify exact missing rows or mappings; leave optionals omitted | proposal_scope; proposed_values; assumption_ledger; exclusions |
| complete_content_type_evidence | Fresh customer layer plus seeded Content Types evidence | Yes | Exact duplicate review, or configuration readiness is requested | Verify | Workflow-approved complete same-target task export plus the checked-in catalog with validated schema and fingerprints | find_complete_content_type_evidence | The task export can omit Oracle-seeded definitions, while a seed catalog alone cannot reveal customer overrides | Check the fresh export first, overlay the validated seed catalog second, and fail closed on incomplete or mismatched evidence | evidence_path; target_identity; customer_evidence_fingerprint; seed_manifest_fingerprint; fusion_release; completeness_status |
| scope_ownership | Content Types ownership | Yes | Every request | Satisfied | Normalized supplied-object routing record | | Nearby profile and rating-model work belongs elsewhere | Split or reroute out-of-scope work | owned_scope; routed_scope |
| create_import_provider | Approved Content Types create-only FSM provider | Yes | Create or import is requested | Verify | Approved proposal and provider-row fingerprints, fresh unfiltered customer layer, integrity-validated seed manifest fingerprint, reviewed same-task baseline, exact provider rows, and immutable package receipt | verify_content_type_fsm_import_contract | The local builder owns package preparation and core.data-loader owns Task Hook, preview, approval, upload, and initiation | Resolve every package gate; never substitute direct REST, HDL, HSDL, an internal service, or the seed catalog as a payload | package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; seed_manifest_fingerprint; data_loader_route |
| unsupported_mutation | Unsupported Content Types mutation | Yes | Update, merge, delete, end-date, replace, or direct write is requested | Blocked | Create-only FSM contract | | Existing keys are duplicate locks and never become update operations | Change the request to create-only or route it to a future approved contract | blocker_reference |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The fresh customer layer, matching seed catalog, and scope ownership are established for review, or every create-only FSM gate is ready | Lookup yes; create only through core.data-loader |
| Proposal-ready | Supplied object ownership and mappings are unambiguous but technical or exact evidence is incomplete | Preliminary review-only proposal; no exact or create claim |
| Needs evidence | The task export is absent, stale, filtered, or not target-bound, or the integrity-validated seed catalog is unavailable | No |
| Blocked | Evidence is incomplete, the package contract fails, or an unsupported mutation/provider is requested | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CT.CHECK_DEPENDENCIES | decision | 2 | resolve_dependency | ready->CT.CHECK_EXACT_EXISTING;proposal_only->CT.ENFORCE_DESIGN;import_ready->CT.VALIDATE_FSM_IMPORT;evidence_unavailable->CT.RETURN_BLOCKED;unsupported_mutation->CT.RETURN_UNSUPPORTED;blocked->CT.RETURN_BLOCKED | CT.CAPTURE_CONFIGURATION | stop | A supplied-configuration Content Types proposal, exact review, or create-only import request is being resolved |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [HCM Tool FSCR taxonomy](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-tool-fscr-taxonomy/)
- [HCM Common Foundation Skill Baseline](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-common-foundation-skill-baseline/)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
