# Work Skills Workbook Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Work Skills section | Work Skills worksheet with ID or Label, Name, Status, Sharing of the skill in teamwork, qualification-difference/business-purpose, routing/optimization validation evidence, and notes/source-reference columns | Block preview | Provide a completed Work Skills worksheet with the listed columns; the three evidence fields are mandatory for an active skill | Always |  |
| Work Skill Groups section | Work Skill Groups worksheet with group label, English Name, Active, and business-purpose/capacity rationale | Block preview | Provide a complete group row; optional capabilities remain false unless explicitly selected | A group is configured |  |
| Work Skill Group Members section | Work Skill Group Members worksheet with group label, Work Skill Label, and Ratio | Block preview | Provide at least one unique member per group; each member must be in the workbook or already exist in the target | A group is configured |  |
| Work Skill Conditions section | Work Skill Conditions entries with Model Code/Skill, Required, Preferred, Skills Condition, operator, and condition value | Block this runner | A separate operation must map the source API's Work Skill Conditions `POST`/`PUT` payload and condition internal IDs; this runner must not ignore or infer them | Work-skill conditions are configured |  |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Work Skills sheet is present and readable | Continue to design enforcement | Always |  |
| Work Skill Label, English Name, Active, and Sharing are supplied | Build only the API-supported Work Skill payload (`name`, `active`, `sharing`, `translations`) | Always |  |
| Work Skill Group Label, English Name, Active, and business purpose/capacity rationale are supplied | Build the group payload (`active`, `assignToResource`, `addToCapacityCategory`, `translations`, `workSkills`) | A group is configured |  |
| Group member labels are unique and their ratios are whole, non-negative numbers | Put Work Skills before Work Skill Groups and block unknown target members before preview | A group is configured |  |
| Assign to Resource and Add to Capacity Category are blank | Set both group capabilities to `false` | A group is configured |  |
| Active Work Skills include qualification purpose, routing/optimization validation evidence, and onboarding/dispatcher notes | Execute the qualification, routing eligibility, active assignment, teamwork-sharing, and advanced-validation design gates before any metadata GET | A Work Skill is created or changed |  |
| Required and Preferred levels are supplied with each configured condition | Send the record to design enforcement for required-versus-preferred and optional-level checks | Required or preferable skill levels are configured |  |
| Condition attribute, operator, and value are supplied | Send the record to design enforcement for condition-source and AND-logic checks | Work-skill conditions are configured |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| WS.WORKBOOK_STRUCTURE | step | 1 | validate_input | valid->WS.QUALIFICATION_MODEL;invalid->RETURN_ISSUES | none | stop | Always |
