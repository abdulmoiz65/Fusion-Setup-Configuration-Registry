# Sales CPQ integration route withdrawal from 26D

## Decision and scope

On 2026-10-15, the requester directed removal of the dedicated Sales CPQ
integration skill and its routing references from a branch based on the latest
`26.10.main`. Commit `a3ac34af480b81c92945be8667a492ba648ca55e` removes the
package, the Integrations task-list entry, and the Opportunities handoff. The
change is limited to `pillars/cx/sales/`; CPQ-specific Adaptive Search guidance
is retained. This records the requested release scope, without asserting a
product defect or reviewer approval.

The withdrawn skill identity is
`cx.sales.integrations.manage-oracle-cx-sales-to-oracle-cpq-cloud-integration`,
for **Manage Oracle CX Sales to Oracle CPQ Cloud Integration**, catalog task
`ORA_ZCA_OSC_CPQ_INTEGRATION` under Sales / Integrations
(`ORA_ZCA_INTEGRATIONS`). Its manifest, resources, rule registry, scripts, and
package tests are removed. No shared or core service is removed.

This decision supersedes only the statements that retain the Sales route and
its package in the earlier [CPQ-side removal
record](../../../configure-price-quote/quoting/references/26d-integration-skill-removal.md).
That record remains provenance and handoff guidance for its two withdrawn
CPQ-side skills. Historical identifiers in either record are not execution
dependencies.

## Catalog and replacement behavior

Keep the Oracle setup-task catalog identity and flags: a catalog entry describes
the task independently of whether FSCR ships an execution skill. It does not
authorize an API call or import. No catalog or generator change is required.

Under the current Run Book task-context policy, a newly generated plan for this
exact catalog task has no pillar skill binding and routes to
[Manual Tasks](../../../../../shared/common/manual-tasks/SKILL.md). That skill
provides manual guidance only. It does not open Fusion, call APIs, create an
import, or configure an integration. The Sales owner must use task-specific
instructions for the application's current release, or obtain guidance from
the Fusion administrator when those instructions are unavailable. Involve the
CPQ owner for CPQ-side prerequisites and administration.

## Existing projects and handoff

Before resuming a project plan or Run Book that names the withdrawn skill,
stop before invoking that binding. Using the project's existing state and
artifact workflow, record the unavailable route as a blocker with failure class
`catalog_or_metadata_mismatch`, the exact task and old binding, and the Sales
owner handoff as the next action. Do not mark the integration complete or
substitute a browser, REST, loader, or another integration route.

Replan future execution bindings explicitly through the existing project
workflow. Retain the catalog task identity and dependent tasks, select the
manual handoff, and preserve the prior plan as evidence. Replanning does not
perform the task or grant permission for a live change. Any independently
supported procedure must meet its own workflow, access, environment, preview,
and approval requirements before execution.

The Sales owner assesses the intended configuration and coordinates unresolved
CPQ prerequisites with the CPQ owner. Record the target environment, approved
change reference, implementer, changed integration identifiers, validation
outcome, and sanitized supporting evidence through the project's normal
workflow. Resume dependent tasks only after their existing validation and
evidence gates pass; success on one application side does not establish
completion on the other.

The source withdrawal does not disable, delete, or change an integration already
configured in Fusion or CPQ. No automatic data migration or deletion is needed.
Preserve existing project artifacts, approvals, external job identifiers, and
verification evidence. For any submitted or uncertain operation, reconcile its
status through the supported original workflow before replanning; do not
resubmit it through the withdrawn route.

## Recovery and review

If release owners later approve reinstatement, recover the package from the
first parent of removal commit `a3ac34af480b81c92945be8667a492ba648ca55e`
(`3e3029501be3668b0a585ffb4a06efff2cd2dd0d`) and review its required parent
links and task routing together. Revalidate against the target branch's current
catalogs, execution contracts, and tests, and obtain a fresh merge audit.
Reinstating source does not authorize live application execution.

Required merge reviewers are the responsible CX Sales Pillar Development Lead
or SME and an FSCR A-Team/core reviewer, with functional/automation and QA
review of the withdrawn coverage and handoff as applicable. Record approvals
in the merge request. Before merge, attach an MR-scope audit matching its
current source and target snapshots; this note is not merge authorization.
