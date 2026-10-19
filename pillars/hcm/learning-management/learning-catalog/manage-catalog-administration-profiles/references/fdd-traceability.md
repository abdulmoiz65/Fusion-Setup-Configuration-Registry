# Visible FDD coverage and evidence limits

Read live acceptance from the selected project's submission and readback records;
historical create results do not establish current readiness or processing completion.
Independent multi-create orchestration, mixed change planning, bounded processing,
metadata-gated child inspection and UTF-8/text-PDF intake now have executable
helpers and offline tests. Multi-create is separate root loads, not atomic
multi-row or parent/child import. Basic name/description/visibility updates have
separate evidence-gated loader and shared REST contracts. Child, lifecycle and
reconcile mutations remain unavailable. Universal-format input and full FDD
acceptance are not claimed. See automation-helpers.md and operation-contract-evidence.md.
Authority: OLC-116676 FDD Confluence page21981495777 v4, updated2026-09-17,
reviewed from the saved project source on2026-09-18; Oracle-authored CAP article
summary provided by the user. The article is functional context, not a deployed
REST contract; customer comments/roadmap are excluded. See the project matrix
for87 stable criteria:53 general/safety,8 broader-scope,26 illustrative examples.

| FDD requirement | Local implementation / evidence | Remaining acceptance |
|---|---|---|
| Requirement1.0 business intent -> attributed proposal | cap_proposal draft/normalize/presentation; test_proposal and varied test_fdd_scenarios | Agent interpretation/reader quality needs fresh prompt tests; no arbitrary document parser claimed |
| R1 multiple formats | Bounded UTF-8 text/Markdown/CSV and installed pdftotext text-PDF extraction with provenance; strict local contributor CSV bytes parser | Office/XLSX/image/OCR/presentation extraction remains unavailable without a supported tested reader |
| R2 completeness and generated fields | Names/descriptions proposed only when missing; stable source classification; unknown fields/counts explicit | Actual people resolution/grants not implied |
| R3 rephrase, R4 add/edit/remove | Immutable revision/diff, stable rows, cleared approval; proposal removal only | Ambiguous removal clarified by agent; live deletion unavailable |
| R5/R6 and A/B boundaries/partial drafts | Unknown groups rejected; named groups generate partial proposal and request missing facts | Prompt behavior needs independent evaluation |
| R7 exact approval and required named executor | Shared-loader create and evidence-gated sparse update; separate shared REST name/description/visibility update; artifact/approval tamper tests. Lifecycle and child writes refused; no fabricated service | Manage Administrator Profile Values is not a CAP CRUD route; route-specific readiness and exact approval remain required |
| R8 next steps/reply | Helper next_step/reply_example plus skill response contract | All conversational outcomes need clean forward tests |
| R9 baseline and existing rows | Shared root reads, bounded pagination, root candidate comparison | Fresh access baseline required; effective contributor/business suitability cannot be inferred from roots |
| R10 default/custom reuse or activation | Candidate/default-flag/inactive review and difference reporting | No auto reuse with unverified management scope; activation mapping/approval unavailable |
| R11 exact supplied names | Preserved legal names/descriptions; explicit length errors | Quoted names may require supported query-literal contract for exact REST query |
| C empty contributors | Agreed conditional policy; no fixed person requirement or guessed broad/creator-only access | Actual target behavior and disclosure required before creation |
| D contributor files/counts | Readability/syntax/duplicates/leading zeros/alias resolution counts; test_contributors | Parser's local CSV is not Fusion attachment contract; people API/file lifecycle/processing unavailable |
| Five simulations | Varied synthetic group/count/revision/baseline cases, never literal required deployments | No mandatory replay of FDD countries/counts |
| Execution/readback for each attempt | Exact-approved shared-loader creates and separate basic updates have executable validation/readback; shared-boundary negative tests retained | Evaluate live create/batch/update receipts per target and run; effective contributors and full FDD business execution remain unverified |
| Earlier lifecycle/defaults/certificates/reconcile | Retained task detail, explicit unavailable operations and tests | Per-operation contracts and live acceptance pending |

Conflicts/gaps retained:
- Contributor-free statements differ; agreed policy permits it only after actual
  access semantics are verified/disclosed, not by accepting either assertion.
- “Manage Administrator Profile Values” is not permission to invent an endpoint.
- Missing catalog-administration-profile-skill-requirements.md attachment and
  OLC-12345 acceptance placeholder remain evidence gaps. Proceed with visible
  requirements, never claim unseen coverage or repeatedly retry forbidden access.
- Historical APEX root-only exclusion and later saved contributorCriteria template
  differ; compare actual current deployment before prescribing a registration change.
- Current-release Oracle documentation and deployment must be refreshed during
  an authorized external evidence step; this local implementation makes no new
  external verification claim.

Sources:
- [FDD](https://confluence.oraclecorp.com/confluence/display/VS/OLC-116676+FDD+%5BP1%5D+Learning+Catalog+Administration+Profile+Setup+Skill)
- [Oracle functional article](https://community.oracle.com/customerconnect/discussion/954807/catalog-administration-profiles)
- [Oracle functional documentation](https://docs.oracle.com/en/cloud/saas/talent-management/fatul/catalog-administration-profiles.html)
- [Runtime contract](runtime-contract.md) and [business behavior](business-behavior.md).
