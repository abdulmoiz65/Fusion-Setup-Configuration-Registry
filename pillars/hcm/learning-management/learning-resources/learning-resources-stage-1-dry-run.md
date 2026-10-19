# Learning Resources Skill — Stage 1 Dry Run

## Result

The local `pillar-skill-gen` dry run passed catalog validation and did not write any skill files.

It found this scope:

- Pillar: `HCM`
- Offering: `Learning Management` (`LEARNING_MANAGEMENT`)
- Functional area: `Learning Resources` (`ORA_LEARNING_RESOURCES`)
- Tasks: `Manage Instructors`, `Manage Classrooms`, and `Manage Training Suppliers`
- Registered REST objects: `learningInstructors`, `learningClassrooms`, and `learningTrainingSuppliers`

The dry run proposed:

- Skill ID: `hcm.learning-management.learning-resources`
- Folder: `pillars/hcm/learning-management/learning-resources`
- Default representation: one functional-area `SKILL.md` plus three task metadata Markdown files

## Resolved Decision

The user selected the current local taxonomy. The implementation will therefore use:

- Skill ID: `hcm.learning-management.learning-resources`
- Parent skill ID: `hcm.learning-management`
- Folder: `pillars/hcm/learning-management/learning-resources`

## Clarifications Needed

### 1. Task structure — resolved by stage-two recommendation

Choose whether the three tasks should be:

- Flat task metadata files (the dry-run default), or
- Nested task skills (recommended for the detailed, task-specific workflows in the FDD), or
- A hybrid structure.

### 2. FDD and Jira synchronization — observed, then resolved

The FDD contains detailed field rules, dependencies, validations, and workflow requirements. The three Jira child stories currently contain only their titles as descriptions and no acceptance criteria:

- `OLC-120235`: Manage Training Suppliers
- `OLC-120236`: Manage Classrooms
- `OLC-120237`: Manage Instructors

The sources were not identical in the first pass. The user subsequently confirmed that the FDD is the latest authoritative functional source. Jira remains required for task scope and traceability, but exact textual parity is no longer an implementation blocker.

### 3. Source access — resolved

Both the Confluence FDD and authenticated Jira pages were read successfully.

## Sources Checked

- Local FSCR git branch: `csardar_learning_resources_skill`
- Local effective setup-task taxonomy under `knowledge/setup-task-catalog/effective/`
- Local `pillar-skill-gen` implementation and `--dry-run`
- Local HCM dependency graph
- Data Loader Business Object Registration page
- Confluence FDD: `OLC-116674 FDD [P1] Learning Resources Skill`

## No Changes Made

No functional-area skill, task metadata file, nested task skill, taxonomy file, or REST registration was created or changed in stage one.
