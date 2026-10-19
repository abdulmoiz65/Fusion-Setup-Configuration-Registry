# Workstations Design Enforcement

## Source Evidence

| Source | Verified Fact | Source Anchor |
|---|---|---|
| Workstation design and technical specification | A Workstation belongs to exactly one existing Work Center. `WorkstationCode` is unique within the organization. | [Workstation - Design & Technical Specification](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=8555976642), Workstation relationship and Create Workstation attributes |
| Workstation design and technical specification | A Workstation can have zero or more equipment-resource-instance associations after creation. Any associated equipment resource instance belongs to the parent Work Center. | [Workstation - Design & Technical Specification](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=8555976642), Equipment Resource Instance Association |
| FDD - 24C Manage Workstation (marked Draft) | A Workstation must belong to a manufacturing-plant organization; its Work Center must be valid and in that same organization. An equipment association must be active equipment, in the same organization, and not already associated with another Workstation. | [FDD - 24C Manage Workstation](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=8819715515), WIS-WS-020 through WIS-WS-024 |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| WORKSTATIONS.DESIGN.MANUFACTURING_ORGANIZATION | Every Workstation creation request | Blocker | | `OrganizationCode` does not identify a manufacturing-plant organization. | Supply an organization that is flagged as a manufacturing plant. Current FSM guidance does not define an automatic lookup; do not guess or select an organization by position. | Yes |
| WORKSTATIONS.DESIGN.PARENT_WORK_CENTER | Every Workstation creation request | Blocker | | `WorkCenterCode` does not identify one existing Work Center in the same manufacturing organization, or the requested Workstation would have more than one parent Work Center. | Supply one existing parent Work Center in the selected organization. Current FSM guidance does not define an automatic lookup; do not guess or select a Work Center by position. | Yes |
| WORKSTATIONS.DESIGN.CODE_UNIQUE_IN_ORGANIZATION | Every Workstation creation request | Blocker | | The requested `WorkstationCode` is already used in the target organization. | Use a different code or treat the request as an update after obtaining the approved FSM update contract. | Yes |
| WORKSTATIONS.DESIGN.EQUIPMENT_OPTIONAL_AND_ALIGNED | An equipment-resource-instance association is requested | Blocker | | The equipment-resource instance is not active equipment, does not belong to the Workstation's manufacturing organization and parent Work Center, or is already associated with another Workstation. | Omit the equipment row or select an active equipment-resource instance in the same organization and parent Work Center that is not associated with another Workstation. | Yes |

## Known Design-Check Boundary

The source establishes the business checks above but does not specify a current FSM read-only lookup, package-order rule, or error response for the checks. The validator must stop and report the unresolved check rather than invent a lookup or select a record.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WORKSTATIONS.DESIGN_CREATE_CONTRACT | decision | 20 | design_enforcement | pass->WORKSTATIONS.DONE;failure->WORKSTATIONS.RETURN_ISSUES;incomplete->WORKSTATIONS.RETURN_ISSUES | WORKSTATIONS.FSM_PREPARE | stop | When source-backed Workstation creation checks can be evaluated. |
