# CPQ integration skill removal from 26D

## Decision and scope

On 2026-10-15, the requester directed removal of the CPQ-side integration
backports introduced into `26.10.main` by reviews 1977 and 1698. This record
documents that release-scope decision; it does not assert a product defect or
owner approval. The implementation is prepared on `om_sales_skill_removal`.

| Withdrawn skill | Introducing review | Replacement in 26D |
| --- | --- | --- |
| `cx.configure-price-quote.quoting.quoting-to-oracle-order-management-integration` | 1977, merge `42478619f` | CPQ-owner handoff for Order Management integration administration |
| `cx.configure-price-quote.quoting.oracle-sales-to-quoting-integration` | 1698, merge `13cf56fdb` | CPQ-owner handoff for Generic Integration and CRM Fusion Integration administration |

The removal withdraws these repository execution routes from 26D. It does not
delete or disable an integration already configured in Fusion or CPQ, change
credentials, or submit a live application operation. Other release branches
are outside this change.

## Dependency and release impact

- Remove both task packages, including the Sales agent configuration and the
  Order Management resources, rule registry, and package-local tests.
- Remove both links from Quoting and clear its required setup-task list so
  planning does not require execution of a withdrawn skill.
- Retain the Fusion Sales-side task
  `cx.sales.integrations.manage-oracle-cx-sales-to-oracle-cpq-cloud-integration`.
  Remove its dependency and conditional route to the withdrawn CPQ-side Sales
  task; retain its explicit prohibition on CPQ administrative mutations.
- Keep the existing custom task catalog identities. Catalog entries describe
  setup tasks independently of whether a task skill ships in this release;
  their presence does not authorize execution or supply a replacement route.
  No generated catalog or generator changes are needed for this skill removal.
- Retain the Quoting functional-area skill and the Fusion Sales-side task's
  scripts, resources, and tests. No shared/core execution service is removed.

## Existing projects and handoff

For a project plan or Run Book that references either withdrawn skill, stop
before invoking it. Record the unavailable 26D route and the CPQ-owner handoff
as a blocker or manual task using the project's normal state and artifact
workflow. Do not silently mark the CPQ work complete or substitute browser,
REST, loader, or another integration route.

The CPQ owner must assess and perform any necessary administration through an
independently supported and approved procedure. Resume dependent work only
after the project's existing validation and evidence gates pass. The retained
Fusion Sales-side task can perform its own declared Sales configuration work;
its success does not imply CPQ-side completion.

Existing project artifacts and deployed configuration need no automatic data
migration or deletion. Preserve prior evidence and external job identifiers.
Only future execution bindings to the withdrawn skills need explicit replanning.

## Recovery

If release owners later approve reinstatement, restore both packages together
with the appropriate parent links, required setup tasks, and Sales handoff.
Use the original introducing reviews as provenance. Do not restore unrelated
local configuration files. Review the restored routes against the target
release's current catalogs and execution contracts, run the relevant tests,
and obtain a fresh merge audit before release. Reinstatement of source does
not authorize live application execution.

## Validation and approval

Validate both deleted packages, the absence of executable inbound references,
the retained Sales-side tests, its offline metadata preview, and
`git diff --check`. The historical identifiers in this record are provenance,
not executable dependencies.

Required merge reviewers are the responsible CX Pillar Development Lead or SME
and an FSCR A-Team/core reviewer. Functional/automation and QA reviewers must
assess the affected coverage and handoff as required by repository governance.
Approval is pending and must be recorded in the merge request; this record and
the automated audit do not grant it. Run the canonical auditor in MR scope
after creating the MR and attach a report matching its source and target SHAs.
