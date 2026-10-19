# Learning security decision support

Sources supplied by the user, read 2026-09-22:

- `Oracle_Learning_Security_Decision_Support.xlsx`: Read Me rows 2–7,
  Decision Questions rows 2–21, Mapping rows 2–56 (columns A–G).
- `Decision support for Oracle Learning security.docx`: introductory questions
  and the operating-model comparison table (centralized, geographic and
  business-function distribution).

These are source-grounded design prompts, not an entitlement list or authority
to assign roles. Read only the relevant question/mapping groups. Potential
answers are examples, not closed enums; mixed operating models are valid.
Blank mapping cells mean unknown/not applicable to assess, not no privilege
needed, all data access or permission to invent a role code.

## Three independent decisions

Capture **who**, **which actions**, and **which scope**. Functional roles,
duties and privileges determine actions. HCM person security/data roles define
people/record scope; hierarchy or area of responsibility must be established,
not assumed. CAPs define specialist catalog segments, while learner visibility
and access groups address a different access question. A CAP is not person
security and profile enablement is not a security grant.

This separation agrees with [Oracle's Learning catalog access guidance](https://docs.oracle.com/en/cloud/saas/talent-management/falct/how-the-oracle-learning-catalog-works.html).
Use current [Securing HCM and Security Reference links from Learning setup](https://docs.oracle.com/en/cloud/saas/talent-management/famlc/set-up-oracle-learning.html)
when validating the selected release. Resolve exact role/duty/privilege codes
and inheritance using the separately selected security workflow; display names
from the workbook must not be serialized as guessed codes.

## Focused discovery and handoffs

| Mapping source rows | Questions / proposed design | Boundary and validation |
| --- | --- | --- |
| 2–14: catalog | Who manages all items, only self-paced/events/courses/paths, or a defined segment? Who only views? Who maintains CAPs or may deactivate/delete? | Workbook differentiates All Items management from segmented catalog management and CAP maintenance. Route segment design to the existing CAP child; verify action privileges independently. Never grant all-items access to solve a missing contributor assignment. |
| 15–26: assignments, audiences and assignment profiles | Who assigns/views for everyone, a defined population, their team or themselves? Who can perform mass actions, delete or withdraw completed assignments? | Separate action duties/privileges from HCM person security, data roles, hierarchy and AOR. Audience definitions and assignment profiles do not grant person access. Mass/delete/withdraw permissions need explicit scope and impact review. |
| 27–30: delivery resources | Who manages classrooms, instructors and suppliers; which resources and events may an instructor handle? | Workbook suggests Manage Training Resources and Learning Instructor starting points. Verify their current duties, data policies and actual event/offering assignment. Do not assume supplier scope equals person scope. |
| 31–35: learner/manager | Which own required/voluntary learning and certificate actions are needed? Which team assignments should managers see, including hidden-assignment settings? | Keep self-service actions distinct from manager hierarchy and object visibility. Workbook calls Line Manager a job role in some rows and abstract role elsewhere; verify type/code, never infer it. |
| 36–39: communities | Who administers, owns, joins or views communities? Which populations and private/secret membership rules apply? | Blank functional mappings need evidence. Membership, visibility and person scope require separate decisions; no automatic full access. |
| 40–48: AI agents | Who builds/configures, invokes or monitors agents? Which external backends, collaboration channels, schedules and Learning actions are used? | Builder/admin duties are not runtime end-user access. Workbook names duty/permission-group starting points including Learning and Development Agents, ORA_WLF_LEARNING_COMMON and agent administration. Verify each exact release-specific code/group and underlying HCM action/data security; extension placement does not grant them. |
| 49–52: integrations and alerts | Who configures content/calendar/virtual providers or alerts; who receives/views messages? | Functional blanks remain unresolved. Route to External Providers or Learning Configurations after the relevant owner confirms supported security; recipients do not become configuration administrators. |
| 53–56: reporting | Who creates/administers versus views reports, for all people, a defined population or a team? | Separate report/catalog permission from HCM data scope and report execution identity. A blank report-creation mapping is not permission to assign a broad Learning role. |

Decision Questions rows 2–21 cover these groups plus operating model. Reuse
known answers; ask only unresolved applicable questions. For example: “Should
regional specialists manage only their catalog segment, only their region's
learners, or both?” They are two independent scopes, not one security switch.

## Operating-model recommendations

The DOCX comparison suggests centralized catalog ownership for shared content,
with segment-specific administration where needed. Distributed geographic or
business-function models may combine central/shared catalog management with
regional/function CAPs. Assignment administration may similarly be centralized
or limited to governed populations, with line managers retaining team scope.
These are design choices to confirm, not defaults to apply to every tenant.

Read Me recommends treating delivered roles as references and using governed
custom-role design for production. Attribute that recommendation to this
workbook/customer policy; do not claim Oracle universally prohibits delivered
production roles. Apply least privilege, segregation of duties, customer
standards and the supported current-release design.

## Output and acceptance

Produce one decision row per persona/capability/scope: synthetic persona label,
business action, functional starting point, exact-code verification status,
person/record scope, catalog segment, visibility, configuration dependencies,
owner, source coordinates and unresolved questions. Never copy a real-user
roster into the skill or project records.

Route person-security design to HCM Security Profile and role-to-profile
association to HCM Data Role; use the existing
[CAP child](../../learning-catalog/manage-catalog-administration-profiles/SKILL.md) only for
catalog ownership. Broader design uses
[Security Role Guidance](../../../../../shared/best-practices/security-role-guidance/SKILL.md).
If a specific executable security workflow is absent, preserve the decision
handoff and name the missing contract. Do not assign a broader delivered role
as a shortcut or use direct REST, a loader or the browser as a fallback.

Require positive and negative tests with synthetic personas: permitted action
on an in-scope item/person; denied action or out-of-scope item/person; read
versus manage; regional/functional isolation; manager hierarchy/hidden records;
learner visibility; and agent actions honoring the same underlying security.
A successful role assignment alone is not proof of correct least-privilege
behavior. Role grants are outside this skill and need their own exact target,
payload, approval and readback workflow.
