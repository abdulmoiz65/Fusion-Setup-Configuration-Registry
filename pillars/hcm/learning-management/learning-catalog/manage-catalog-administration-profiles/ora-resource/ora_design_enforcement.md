# CAP business design and revision isolation

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAP-BATCH-DESIGN | step | 370 | design_enforcement | passed->CAP-BATCH-READY | CAP-BATCH-OBSERVE | stop | Attributed update privilege assessment, no known denial, one sparse part and immutable target/key/date/baseline binding; no-op stops; not Data Loader readiness |
| CAP-P-DESIGN | step | 40 | design_enforcement | passed->CAP-P-DONE | CAP-P-DEFAULT | stop | Review normalized draft and revision diff |
| CAP-UPDATE-DESIGN | step | 320 | design_enforcement | passed->CAP-UPDATE-ARTIFACT | CAP-UPDATE-EVIDENCE | stop | Sparse supplied fields only; protect identity and seeded visibility; disclose last-writer-wins and pending processing; no lifecycle or child edits |

## Design Rules

| Rule ID | Condition | Enforcement | Required Lookup |
|---|---|---|---|
| CAP-REVISION | A proposal changes | cap_proposal.revise preserves prior object, stable unchanged row IDs, explicit before/after and previous digest; clears approval and write eligibility. Row removal is proposal removal, not Fusion deletion. |  |
| CAP-ACCESS | Any business proposal | Keep catalog-manager visibility, contributors, functional privileges, central override and learner access distinct. No role assignment. Everyone is not contributor management access or learner enrollment. |  |
| CAP-DEFAULT | Delivered system default considered | Never delete it. Do not copy its special broad access behavior to empty custom CAPs. No activation or deactivation execution is currently enabled. |  |
| CAP-APPROVAL | User accepts a draft | Proposal agreement is not write approval. Loader create/update requires its dedicated handoff and exact ZIP approval without duplication. Separately selected basic-attribute batch requires cap_batch_update preparation and immediate exact target/payload/preview-hash approval; approvals cannot transfer between routes. |  |
| CAP-PRIVACY | Contributor intake or raw REST data | Keep real rosters and raw person data ephemeral or in approved protected storage; no tracked/project persistence. Record sanitized references/hashes/counts only. |  |
| CAP-EXAMPLES | FDD simulation or attachment gap | Generalize visible rules; no hardcoded organizations, profile/person counts or required replay. Missing attachment is an evidence gap, not an invented contract or blanket draft blocker. |  |
