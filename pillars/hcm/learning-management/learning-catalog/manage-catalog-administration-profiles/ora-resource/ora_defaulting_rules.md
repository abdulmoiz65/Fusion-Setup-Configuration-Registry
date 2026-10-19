# CAP proposal defaults, not Fusion server defaults

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CAP-P-DEFAULT | step | 30 | apply_default | passed->CAP-P-DESIGN | CAP-PROPOSAL | stop | Offline proposal output only |

## Default Rules

| Rule ID | When | Default | Override Allowed | Source |
|---|---|---|---|---|
| CAP-NAME | Name not supplied, known content group | cap_proposal proposes content group followed by Catalog; mark assistant-proposed and require review; reject generated text exceeding250 characters without truncation | Yes; supplied name preserved exactly | FDD Validation B and approved full-FDD WP1 |
| CAP-DESCRIPTION | Description not supplied, known content group | cap_proposal generates Catalog administration for followed by content group; mark assistant-proposed and review | Yes; supplied description preserved exactly | Approved full-FDD WP1 and visible FDD naming/description rules |
| CAP-UNKNOWN | Ownership, visibility, contributors or resolved count unknown | Keep unknown/missing; never use zero people or infer Everyone/creator-only semantics | Replace only from attributed input/evidence | FDD partial-draft rule and DEC-029 |
| CAP-EXISTING | Existing/default candidate found | Suggest reuse/activation only with visible differences and unresolved access checks; never automatically create/delete | User may select a distinct new name and review | FDD baseline rule and Oracle article |
| CAP-SERVER | Preparing a root create with omitted optional inputs | Use source-backed omission contracts corroborated by target evidence; inherited HCM dates remain server-controlled, not synthesized DAT fields; verify exposed defaults after creation | No invented values or default-date assertions | references/create-source-contract.md and retained create validator |
