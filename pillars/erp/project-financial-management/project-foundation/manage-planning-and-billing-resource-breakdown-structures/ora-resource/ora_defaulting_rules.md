# Defaulting Rules

UI defaults and FSM import behavior are different. The minimal UI save created Resource Class format, root and four class elements, while the sparse FSM imports left format and element members empty. Reproducing the observed UI outcome therefore requires those rows in the prepared package. The values below are test-target observations, not universal constants or customer inputs.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| RBS type | PLANNING | Every new custom planning RBS | No |  |
| Version number | 1 | New RBS in the observed UI/import cases | No; this is the tested profile |  |
| To Date | Blank | Omitted in the observed UI/import cases | Nonblank To Date behavior was not tested |  |
| Description | Blank | Customer omits it | Yes |  |
| Job Set | Blank | No Job Set supplied and no Job resource component requested | Yes |  |
| Resource Class format and tree | Explicit Resource Class format plus root and four class elements | Every new RBS even when no extra format or resource is requested | No; the UI creates these defaults |  |
| Additional format | None | Customer selects no additional format | Yes |  |
| Specific planning resource | None | Customer supplies no resource row | Yes |  |
| CentrallyControlFlag | Y | Project-level resource changes unchecked, as in tested saves | No different state was tested |  |
| UseForAllocFlag, UseForCmtCtrlFlag, UseForIcBillingFlag, AutoAddResFlag | N | Tested UI controls left unchecked | No different state was tested |  |
| LaborDisabledFlag, EquipmentDisabledFlag, MaterialDisabledFlag | N | Tested Resource Class controls left enabled | No different state was tested |  |
| Version StatusCode, CurrentReportingFlag | FROZEN, Y | New RBS in observed target | No different state was tested |  |
| Named Person class and curve | Labor, Prorated Even | Actual Named Person row; fields left at UI selections | No override behavior was tested |  |
| Project Nonlabor Resource class and curve | Equipment, Back Loaded | Actual Nonlabor row; fields left at UI selections | No override behavior was tested |  |
| Job class and curve | Labor, Prorated Even | Actual Job row; fields left at UI selections | No override behavior was tested |  |
| Job: Expenditure Category class and curve | Labor, Prorated Even | Actual Job-category row; fields left at UI selections | No override behavior was tested |  |
| Named Person Alias | Selected person label | Actual Named Person row with Resource Name blank | A supplied alias was not tested |  |
| Synthesized Job parent Alias | Selected Job label | Job: Expenditure Category row without a separately entered Job parent | No different parent alias was tested |  |
| Organization, Expenditure Type, Expenditure Category class and curve | No UI preselection | Actual row in one of these formats | Customer must select both; only tested pairs are established |  |

## FSM Create Projection

This table is the observed package shape, not a standalone payload template. The task-owned offline batch serializer builds the guarded seven-member ZIP after source-backed references have been resolved; it does not perform lookups or imports. Core Data Loader owns upload/approval. Preserve the task export's headers, metadata and translation rows; a three-column import does not reproduce UI defaults.

| Package Member | Required New-Create Content | Observed Behavior |
|---|---|---|
| ORA_PJF_RBS_HEADER.csv | One header per requested RBS; Name, OrgName, StartDateActive and supported flags/context | Customer Name and Project Unit name survived import |
| ORA_PJF_RBS_VERSION.csv | One version per header; matching Name, StartDateActive, optional resolved SetCode | Job Set name is not itself the CSV SetCode |
| ORA_PJF_RBS_HEADER_TRANSLATION.csv | Required target-template language rows for each header | Two languages appeared in the tested target; do not universalize that count |
| ORA_PJF_RBS_VERSION_TRANSLATION.csv | Required target-template language rows for each version | Description and identity survived when supplied |
| ORA_PJF_RBS_FORMAT.csv | Resource Class format for every RBS, then each requested extra path and its ancestors | Sparse imported members stayed empty; Fusion did not synthesize format 323 |
| ORA_PJF_RBS_ELEMENT.csv | Root plus four class elements per RBS, then requested resources and required ancestors | Sparse imported members stayed empty; Fusion did not synthesize five default elements |
| ASM_SETUP_CSV_METADATA.xml | Complete task export metadata for the same seven-member package | Required to classify the ZIP as a task setup-data package |

## Default Resource Class Tree

These are the five elements observed after a minimal UI create and after explicitly supplied FSM import. The preparer must verify target-supported IDs and flags from a fresh complete target package rather than transplant opaque IDs from another pod.

| Outline | Alias | ResourceClassCode | Observed ResourceClassId | Observed ResourceTypeId | Spread Curve Name3 | Tree Role |
|---|---|---|---|---|---|---|
| 0 | Requested RBS Name |  |  | -1 |  | Root; nonleaf; Alias must be rewritten to the new Name |
| 1 | Labor | PEOPLE | 1 | 13 | Prorated Even | Default class child |
| 2 | Equipment | EQUIPMENT | 2 | 13 | Back Loaded | Default class child |
| 3 | Material Items | MATERIAL_ITEMS | 3 | 13 | S Curve | Default class child |
| 4 | Financial Resources | FINANCIAL_ELEMENTS | 4 | 13 | Prorated Even | Default class child |

## Resource Serialization

These are conversions observed in the UI/export and the successful FSM import/readback. Project Unit, Set, Job, Named Person and Organization mappings are confirmed. Named Person support requires its resolved PersonNumber to have consistent date/enterprise context in the complete current target export. Project Unit and Organization reads supply CSV context, not an FSCR eligibility verdict. For nonlabor, expenditure type and category, the tested imports retained name fields; no separate pre-import lookup was established. Fusion import validation and later readback decide whether copied names are valid in the target.

The tested element CSV does not use Org ID or Person ID. The Organization row carries its name plus copied classification, enterprise and effective-date context; Named Person carries both its display/list-name Alias and PersonNumber. Job carries both an Alias and JobCode with SetCode. Effective dates are copied as import context, not compared with the RBS From Date.

| Customer Value | Observed FSM Element or Version Field | Conversion Rule |
|---|---|---|
| Job Set name | Version SetCode; Job-element SetCode | Resolve exact SetName to one canonical SetCode; do not copy the label into SetCode |
| Job display label | JobCode and Alias | Resolve within the selected Job Set to one JobCode; a standalone Job uses its supplied resource name as Alias, while the generated Job: Expenditure Category parent uses the selected Job label |
| Named Person Display Name or fallback List Name | PersonNumber and Alias | Resolve one public worker; the customer need not supply PersonNumber, and the matched name is retained as Alias |
| Project Nonlabor Resource name | NlrName | Copy the supplied name; target eligibility is not prevalidated by a documented lookup |
| Organization name | Alias, Name5, ClassificationCode1, Organization EffectiveStartDate4/EffectiveEndDate4, Name4 and enterprise EffectiveStartDate5/EffectiveEndDate5 | Select one Organization using PA_EXPENDITURE_ORG, PA_PROJECT_ORG, DEPARTMENT, FUN_BUSINESS_UNIT precedence; copy its name/classification/dates and the unique current-export enterprise context; do not use OrganizationId or perform an FSCR eligibility check |
| Expenditure Type name | ExpenditureTypeName | Copy the supplied name; target eligibility is not prevalidated by a documented lookup |
| Expenditure Category name | ExpenditureCategoryName | Copy the supplied name; target eligibility is not prevalidated by a documented lookup |
| Resource Class label | ResourceClassCode and ResourceClassId | The tested Labor and Equipment choices serialized as PEOPLE/1 and EQUIPMENT/2; other mappings are unproven |
| Spread Curve label | Name3 | Tested values remained Prorated Even and Back Loaded; the default class tree also used S Curve |
| Job: Expenditure Category combination | Parent Job element and category child element | Child repeats JobCode and SetCode, carries ExpenditureCategoryName, and has a synthesized nonleaf Job parent |
| Optional resource alias | Alias | Preview actual value; custom typed names did not survive every observed UI save path |

## Alias Observations

| Observed Save Path | Saved Alias Behavior | Limit |
|---|---|---|
| Direct Job row with a typed Name | Typed Name persisted as the Job element Alias | Proved for the directly saved Job case only |
| Named Person row with blank Name | Fusion filled Name and Alias from the selected person label | Proved for the tested synthetic worker |
| Job: Expenditure Category child with a typed Name | Typed child Alias persisted; generated Job parent Alias used the selected Job label | Proved for this child combination only |
| Nonlabor, Organization and Expenditure Type rows after format switches | Saved Alias used the selected reference label, not the typed custom Name | Do not promise this behavior for a direct-save path |
| Expenditure Category row after the same switches | Typed resource Alias persisted | Do not generalize this result to other formats |

## Bulk and Readback Rules

| Situation | Required Preparation or Verification |
|---|---|
| Multiple new RBSs or resource rows | Validate every row first, then build one consolidated seven-member ZIP and make one loader submission; never one import per row |
| A selected format has no resource row | Include the format and required format ancestors only; keep the specific-resource element count unchanged |
| A Job: Expenditure Category row is selected | Include Job and Job: Expenditure Category formats plus the observed generated Job parent and category child; do not generalize this element synthesis to other descendants |
| An untested descendant or actual Organization: Inventory Item row is requested | Stop for new UI/import evidence; a format-only Inventory Item choice is the only tested case |
| A cloned template root Alias names a source fixture | Rewrite it to the requested new RBS Name before preview; do not leak the fixture alias into the import |
| Fusion reorders top-level elements after import | Compare logical resource identities and parent paths first; report OutlineNumber and OrderNumber differences separately instead of calling a present resource missing |
| Post-import confirmation requested | Obtain a fresh complete same-task export after terminal loader success; compare all approved header, format and element values |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RBS.APPLY_DEFAULTS | step | 2 | apply_default | applied->RBS.ROUTE_OPERATION;failure->RBS.RETURN_ISSUES | RBS.VALIDATE_INPUT | stop | Valid create input; add explicit UI-equivalent default requirements before package preview |
