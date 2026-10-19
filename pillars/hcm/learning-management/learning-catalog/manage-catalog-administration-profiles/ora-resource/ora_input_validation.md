# CAP input and operation selection

Authority: approved full-FDD plan D0–D3, visible FDD rules1–11/A–D and the local proposal contract. Examples are not fixed configurations. Future write contracts remain in the task metadata and references/runtime-contract.md; their current executable behavior is refusal, not incomplete execution.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAP-SELECT | decision | 10 | validate_input | draft->CAP-PROPOSAL;read->CAP-R-VALIDATE;inspect->CAP-CHECK-VALIDATE;profile->CAP-I-VALIDATE;prepare->CAP-CREATE-VALIDATE;update_prepare->CAP-UPDATE-VALIDATE;batch_update->CAP-BATCH-INPUT;write->CAP-WRITE-BLOCK | none | stop | Dedicated create/loader-update or shared-REST basic-attribute batch preparation; raw mutations still select refusal |
| CAP-BATCH-INPUT | step | 350 | validate_input | passed->CAP-BATCH-OBSERVE | CAP-SELECT | stop | cap_batch_update: exact number, confirmed target and explicit name/description/visibility replacement; no caller URL or other mutation |
| CAP-I-VALIDATE | step | 260 | validate_input | passed->CAP-I-PREREQ | CAP-SELECT | stop | inspect-profile: exact-number only, confirmed target and read headers, no child selector or payload |
| CAP-PROPOSAL | step | 20 | validate_input | passed->CAP-P-DEFAULT | CAP-SELECT | stop | Offline proposal or contributor intake only; no external source reader |
| CAP-R-VALIDATE | step | 100 | validate_input | passed->CAP-R-PREREQ | CAP-SELECT | stop | Exact lookup or unfiltered listing only |
| CAP-CHECK-VALIDATE | step | 160 | validate_input | passed->CAP-CHECK-PREREQ | CAP-SELECT | stop | Read-only write-contract inspection; no data payload or caller endpoint |
| CAP-CREATE-VALIDATE | step | 220 | validate_input | passed->CAP-CREATE-EVIDENCE | CAP-SELECT | stop | cap_create_handoff validates one root DAT POST, intended fields, current evidence integrity and target/project/task identity; no approval or submission |
| CAP-UPDATE-VALIDATE | step | 300 | validate_input | passed->CAP-UPDATE-EVIDENCE | CAP-SELECT | stop | Sparse root PATCH preparation: immutable identity, name/description/visibility allowlist and explicit baseline/diff; no-op stops without a load |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Proposal ownership and provenance | cap_proposal.draft requires known content groups and source references. Missing ownership/visibility/contributors remains explicit. Preserve exact supplied text; propose descriptions. Reject unknown payload fields and duplicate exact draft names. | draft/revise |  |
| Proposal limits | name<=250, description<=4000; no silent trim/truncation. Local proposal is not deployed schema evidence or write approval. | draft/revise |  |
| Local contributor input | cap_contributors.parse_csv accepts UTF-8 one-column personNumber/email CSV under its explicit local format only. Reject malformed input, retain leading zeros, count duplicates and invalid rows. Syntax is not person resolution or a Fusion attachment format. | draft/revise |  |
| Read shape | cap_workflow.validate_read_request requires confirmed HTTPS origin, exact environment identity, GET, root/describe allowlist, framework9 and optional supported Accept-Language. No body, custom auth/header, children or as-of date. | retrieve/list |  |
| Exact selector | One nonempty text name<=250 or number<=2000 local safety bound, additionally honor advertised maxLength; displaySize30 is not maxLength. Optional expected ID text; reject unverified query literals; finder rejects comma/colon/equals. | retrieve/inspect-profile |  |
| List input | Explicit list mode; no name/number/expected ID. Default100 rows/page,20 pages,2000 rows,120 seconds, metadata60 seconds. Limits stop honestly; no fabricated total on partial results. | list |  |
| Contract inspection input | mode contract; only confirmed environment/host pair and read-header allowlist; reject selectors, body, arbitrary paths and approval fields. cap_workflow uses the existing shared GET CLI for fixed metadata only. | inspect-write-contract |  |
