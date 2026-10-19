# Work Skills Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate workbook structure | Confirm the Work Skills and configured Work Skill Conditions data are present before evaluating design rules |
| 2 | Validate qualification model | Confirm each work skill represents a meaningful qualification difference and does not over-fragment the routing pool |
| 3 | Validate condition design | Confirm condition sources are reliable and all configured conditions are assessed with AND logic |
| 4 | Validate level and routing eligibility | Confirm required and preferred levels are used correctly and every required skill and level is met |
| 5 | Validate routing operations | Confirm active assignment, teamwork sharing, group/capacity effects, and advanced routing or optimization testing are addressed |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A Work Skill is created or changed | Error |  | The skill does not represent a meaningful qualification difference, or excessive granularity would unnecessarily shrink the eligible routing pool | Define skills for real qualifications such as technology, certification, security, or service capability; avoid encoding every job combination as a separate skill | Yes, before preview |
| Work-skill conditions are configured | Error |  | A condition derives from an unreliable activity attribute, or the activity data needed to evaluate it is not consistently populated | Derive skill requirements only from reliable activity attributes, such as Activity Type, customer classification, certification, or location/security need | Yes, before preview |
| Multiple work-skill conditions apply | Error |  | The design assumes OR behavior or has not accounted for all conditions being required | Design condition sets knowing that multiple conditions use AND logic; verify the resulting eligible-resource pool | Yes, before preview |
| Required or preferable skill levels are configured | Error |  | Required levels are used as preferences, preferable levels are below required levels, or level 0 is used for a mandatory qualification | Use required levels as routing eligibility thresholds and preferable levels to rank already eligible resources. Use level 0 only for genuinely optional skills; keep preferable levels at least as high as required levels | Yes, before preview |
| An Activity Type requires multiple skills | Error |  | The design has not verified that a resource must meet every required skill and level | Validate routing against the complete requirement set; a resource must meet every required skill and level to be eligible | Yes, before preview |
| Skills are enabled for routing or assigned during onboarding | Error |  | Active skills are not intended for routing evaluation, or resources can be created without the skills needed for their work | Keep a skill active only when conditions and routing should evaluate it; assign and maintain skills during onboarding and expose the read-only activity Work Skill field for dispatcher visibility | Yes, before preview |
| Teamwork skill sharing is configured | Error |  | The sharing mode does not match the actual qualification rule, or inactive/non-working members are assumed to contribute | Select sharing deliberately: Maximal for any qualified member, Minimal for all-member requirements, No Sharing for independent holders, and Summary only for additive capability; account for daily availability | Yes, before preview |
| Work-skill groups are used | Error |  | Group-level precedence or capacity effects are unknown | Use groups for common bundles; individual assignments override group levels and the highest applicable group level wins. For capacity, remember any member skill contributes capacity and any group skill consumes it | Yes, before preview |
| Skills support certifications, crews, vehicles, or advanced capacity design | Error |  | The model has not been tested against actual routing and optimization behavior | Validate the end-to-end eligibility and optimization outcome before rollout; use the Metadata API for large or repeatable multi-environment configuration | Yes, before preview |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| WS.QUALIFICATION_MODEL | decision | 2 | design_enforcement | passed->WS.CONDITION_SOURCE;blocked->RETURN_ISSUES | WS.WORKBOOK_STRUCTURE | stop | A Work Skill is created or changed |
| WS.CONDITION_SOURCE | decision | 3 | design_enforcement | passed->WS.CONDITION_LOGIC;blocked->RETURN_ISSUES | WS.QUALIFICATION_MODEL | stop | Work-skill conditions are configured |
| WS.CONDITION_LOGIC | decision | 4 | design_enforcement | passed->WS.REQUIRED_AND_PREFERRED_LEVELS;blocked->RETURN_ISSUES | WS.CONDITION_SOURCE | stop | Multiple work-skill conditions apply |
| WS.REQUIRED_AND_PREFERRED_LEVELS | decision | 5 | design_enforcement | passed->WS.ROUTING_ELIGIBILITY;blocked->RETURN_ISSUES | WS.CONDITION_LOGIC | stop | Required or preferable skill levels are configured |
| WS.ROUTING_ELIGIBILITY | decision | 6 | design_enforcement | passed->WS.ACTIVE_AND_ASSIGNED;blocked->RETURN_ISSUES | WS.REQUIRED_AND_PREFERRED_LEVELS | stop | An Activity Type requires multiple skills |
| WS.ACTIVE_AND_ASSIGNED | decision | 7 | design_enforcement | passed->WS.TEAMWORK_SHARING;blocked->RETURN_ISSUES | WS.ROUTING_ELIGIBILITY | stop | Skills are enabled for routing or assigned during onboarding |
| WS.TEAMWORK_SHARING | decision | 8 | design_enforcement | passed->WS.GROUPS_AND_CAPACITY;blocked->RETURN_ISSUES | WS.ACTIVE_AND_ASSIGNED | stop | Teamwork skill sharing is configured |
| WS.GROUPS_AND_CAPACITY | decision | 9 | design_enforcement | passed->WS.ADVANCED_VALIDATION;blocked->RETURN_ISSUES | WS.TEAMWORK_SHARING | stop | Work-skill groups are used |
| WS.ADVANCED_VALIDATION | decision | 10 | design_enforcement | passed->RETURN_READY_FOR_PREVIEW;blocked->RETURN_ISSUES | WS.GROUPS_AND_CAPACITY | stop | Skills support certifications, crews, vehicles, or advanced capacity design |
