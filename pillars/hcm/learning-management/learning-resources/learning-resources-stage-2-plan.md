# Learning Resources Skill — Stage 2 Plan and Structure Options

## Recommendation

Use a nested task skill for each of the three tasks.

The recommended structure is:

```text
pillars/hcm/learning-management/learning-resources/
├── SKILL.md
├── manage-instructors/
│   └── SKILL.md
├── manage-classrooms/
│   └── SKILL.md
└── manage-training-suppliers/
    └── SKILL.md
```

This structure is the best fit because each resource has its own registered REST object, creation contract, dependencies, validations, error paths, and user-review workflow.

## Option 1: Flat Task Metadata

Flat mode creates one functional-area skill and a small Markdown metadata file for each task:

```text
learning-resources/
├── SKILL.md
├── manage-instructors.md
├── manage-classrooms.md
└── manage-training-suppliers.md
```

The parent `SKILL.md` owns almost all functional behavior. Each task file primarily records catalog identity, task code, REST import mode, business object, and routing information.

### Benefits

- Small number of files.
- Low maintenance overhead.
- Good for simple tasks that need only catalog identity and generic Data Loader routing.
- Easy to keep all shared behavior in one functional-area skill.

### Limitations for Learning Resources

- The three workflows have different required fields and validations.
- Classroom creation has two mutually exclusive location paths and address-country rules.
- Instructor creation depends on HCM person and assignment data and must prevent duplicate instructor records.
- Training supplier creation has its own contact resolution and supplier relationship behavior.
- Task-specific tests, scripts, and Oracle guidance would all accumulate in the parent skill.
- The parent skill would become large and harder to route, test, and maintain.

Flat metadata is therefore not recommended for this case.

## Option 2: Nested Task Skills

Nested mode creates a complete child skill for every setup task. Each child has its own full manifest and can own task-specific workflows, references, resources, scripts, and tests.

### Benefits

- Clear separation of the three resource workflows.
- Direct mapping from Jira story to repository skill:
  - `OLC-120235` → Manage Training Suppliers
  - `OLC-120236` → Manage Classrooms
  - `OLC-120237` → Manage Instructors
- Direct mapping from each task to its registered REST business object.
- Each task can define its own intake questions, validation table, preview/approval step, error handling, and dependencies.
- Task-specific `ora-resource/` guidance and tests can be added without enlarging the parent skill.
- Future changes to one resource are less likely to affect the other two.
- The functional-area parent remains a clean router and shared-policy owner.

### Costs

- More files and manifests.
- Shared rules must be centralized or referenced carefully to avoid duplication.
- Validation must cover the parent plus all three child skills.

These costs are justified because all three tasks are substantial and independently executable.

## Option 3: Hybrid Structure

Hybrid mode mixes flat task metadata and nested task skills. For example, Classrooms and Instructors could be nested while Training Suppliers remains flat.

### Benefits

- Useful when one or two tasks are complex and the others only need simple routing metadata.
- Reduces file count compared with making every task nested.

### Limitations for Learning Resources

- Training Suppliers is not merely metadata: it has a dedicated REST object, required and recommended fields, contact-person resolution, set filtering, flexfields, related materials, and downstream relationships.
- A flat Training Suppliers file would put its functional behavior back into the parent while the other two tasks are self-contained.
- Reviewers and future maintainers would need to remember why equivalent resource tasks use different representations.
- Jira-to-skill traceability would be inconsistent.

Hybrid is therefore possible but not beneficial here.

## Why Nested Skills Are Best for This Case

All three tasks share a high-level pattern—interpret input, resolve dependent records, validate, show a review table, obtain approval, and execute through Data Loader REST—but their concrete rules differ materially.

### Manage Training Suppliers

- REST object: `learningTrainingSuppliers`
- Required creation input: supplier name.
- Recommended inputs: description and contact.
- Conditional inputs: enterprise set and configured flexfields.
- Needs unique person resolution for the optional contact.

### Manage Classrooms

- REST object: `learningClassrooms`
- Required inputs: name, description, and one location method.
- Existing-location and ad-hoc-address paths are mutually exclusive.
- Country-specific address rules apply.
- Seating capacity must be a whole number.
- Depends on HCM Locations, shared address services, and optional person contact data.

### Manage Instructors

- REST object: `learningInstructors`
- Required input: an existing HCM person.
- Must confirm the intended person using person number, department, location, or assignment context.
- Must prevent a person from being created as a second instructor.
- Worker assignment status affects instructor status.
- Depends on the HCM Person Record capability.

These differences deserve separate child workflows and tests.

## Proposed Implementation Plan

1. Apply the confirmed source precedence: use the latest FDD for functional requirements and use Jira for scope and traceability.
2. Generate the functional-area skill and three nested child skills with `pillar-skill-gen`.
3. Configure REST mode and registered business objects:
   - Manage Instructors → `learningInstructors`
   - Manage Classrooms → `learningClassrooms`
   - Manage Training Suppliers → `learningTrainingSuppliers`
4. Keep shared prerequisites and cross-resource sequencing in the parent skill.
5. Put resource-specific intake, validation, preview, approval, execution, and error handling in each child skill.
6. Add source-grounded Oracle guidance with `fusionapps-resource-authoring` where required.
7. Add contract and behavior tests for each child skill.
8. Validate manifests, links, dry-run output, tests, and `git diff --check`.

## Review Gate

The source-precedence decision is approved: the latest FDD governs functional behavior when Jira is less detailed or not textually identical. The remaining stage-two review decision is approval of the recommended three nested task skills.
