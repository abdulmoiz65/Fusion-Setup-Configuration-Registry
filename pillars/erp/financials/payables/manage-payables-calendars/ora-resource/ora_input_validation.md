# Input Validation

<!-- fscr-supported-operations: create, update -->
<!-- fscr-create-fields: AP_OTHER_PERIOD_TYPE::CalendarName, AP_OTHER_PERIOD_TYPE::CalendarType, AP_OTHER_PERIOD_TYPE::Description, AP_OTHER_PERIOD_TYPE::AttributeCategory, AP_OTHER_PERIOD_TYPE::Attribute1, AP_OTHER_PERIOD_TYPE::Attribute2, AP_OTHER_PERIOD_TYPE::Attribute3, AP_OTHER_PERIOD_TYPE::Attribute4, AP_OTHER_PERIOD_TYPE::Attribute5, AP_OTHER_PERIOD_TYPE::Attribute6, AP_OTHER_PERIOD_TYPE::Attribute7, AP_OTHER_PERIOD_TYPE::Attribute8, AP_OTHER_PERIOD_TYPE::Attribute9, AP_OTHER_PERIOD_TYPE::Attribute10, AP_OTHER_PERIOD_TYPE::Attribute11, AP_OTHER_PERIOD_TYPE::Attribute12, AP_OTHER_PERIOD_TYPE::Attribute13, AP_OTHER_PERIOD_TYPE::Attribute14, AP_OTHER_PERIOD_TYPE::Attribute15, AP_OTHER_PERIOD_TYPE::EffectiveFrom, AP_OTHER_PERIOD_TYPE::EffectiveTo, AP_OTHER_PERIOD_TYPE::PeriodFrequency, AP_OTHER_PERIOD_TYPE::PeriodNameFormat, AP_OTHER_PERIOD_TYPE::PeriodsPerYear, AP_OTHER_PERIOD_TYPE::StartDate, AP_OTHER_PERIOD_PERIOD::AP_OTHER_PERIOD_TYPE.CalendarName, AP_OTHER_PERIOD_PERIOD::AP_OTHER_PERIOD_TYPE.CalendarType, AP_OTHER_PERIOD_PERIOD::ApplicationId, AP_OTHER_PERIOD_PERIOD::CalendarName, AP_OTHER_PERIOD_PERIOD::CalendarType, AP_OTHER_PERIOD_PERIOD::Description, AP_OTHER_PERIOD_PERIOD::AttributeCategory, AP_OTHER_PERIOD_PERIOD::Attribute1, AP_OTHER_PERIOD_PERIOD::Attribute2, AP_OTHER_PERIOD_PERIOD::Attribute3, AP_OTHER_PERIOD_PERIOD::Attribute4, AP_OTHER_PERIOD_PERIOD::Attribute5, AP_OTHER_PERIOD_PERIOD::Attribute6, AP_OTHER_PERIOD_PERIOD::Attribute7, AP_OTHER_PERIOD_PERIOD::Attribute8, AP_OTHER_PERIOD_PERIOD::Attribute9, AP_OTHER_PERIOD_PERIOD::Attribute10, AP_OTHER_PERIOD_PERIOD::Attribute11, AP_OTHER_PERIOD_PERIOD::Attribute12, AP_OTHER_PERIOD_PERIOD::Attribute13, AP_OTHER_PERIOD_PERIOD::Attribute14, AP_OTHER_PERIOD_PERIOD::Attribute15, AP_OTHER_PERIOD_PERIOD::DueDate, AP_OTHER_PERIOD_PERIOD::EndDate, AP_OTHER_PERIOD_PERIOD::EnteredPeriodName, AP_OTHER_PERIOD_PERIOD::PeriodName, AP_OTHER_PERIOD_PERIOD::PeriodNum, AP_OTHER_PERIOD_PERIOD::PeriodYear, AP_OTHER_PERIOD_PERIOD::StartDate -->
<!-- fscr-update-fields: AP_OTHER_PERIOD_TYPE::Description, AP_OTHER_PERIOD_TYPE::AttributeCategory, AP_OTHER_PERIOD_TYPE::Attribute1, AP_OTHER_PERIOD_TYPE::Attribute2, AP_OTHER_PERIOD_TYPE::Attribute3, AP_OTHER_PERIOD_TYPE::Attribute4, AP_OTHER_PERIOD_TYPE::Attribute5, AP_OTHER_PERIOD_TYPE::Attribute6, AP_OTHER_PERIOD_TYPE::Attribute7, AP_OTHER_PERIOD_TYPE::Attribute8, AP_OTHER_PERIOD_TYPE::Attribute9, AP_OTHER_PERIOD_TYPE::Attribute10, AP_OTHER_PERIOD_TYPE::Attribute11, AP_OTHER_PERIOD_TYPE::Attribute12, AP_OTHER_PERIOD_TYPE::Attribute13, AP_OTHER_PERIOD_TYPE::Attribute14, AP_OTHER_PERIOD_TYPE::Attribute15, AP_OTHER_PERIOD_TYPE::EffectiveTo, AP_OTHER_PERIOD_PERIOD::AP_OTHER_PERIOD_TYPE.CalendarName, AP_OTHER_PERIOD_PERIOD::AP_OTHER_PERIOD_TYPE.CalendarType, AP_OTHER_PERIOD_PERIOD::Description, AP_OTHER_PERIOD_PERIOD::AttributeCategory, AP_OTHER_PERIOD_PERIOD::Attribute1, AP_OTHER_PERIOD_PERIOD::Attribute2, AP_OTHER_PERIOD_PERIOD::Attribute3, AP_OTHER_PERIOD_PERIOD::Attribute4, AP_OTHER_PERIOD_PERIOD::Attribute5, AP_OTHER_PERIOD_PERIOD::Attribute6, AP_OTHER_PERIOD_PERIOD::Attribute7, AP_OTHER_PERIOD_PERIOD::Attribute8, AP_OTHER_PERIOD_PERIOD::Attribute9, AP_OTHER_PERIOD_PERIOD::Attribute10, AP_OTHER_PERIOD_PERIOD::Attribute11, AP_OTHER_PERIOD_PERIOD::Attribute12, AP_OTHER_PERIOD_PERIOD::Attribute13, AP_OTHER_PERIOD_PERIOD::Attribute14, AP_OTHER_PERIOD_PERIOD::Attribute15, AP_OTHER_PERIOD_PERIOD::DueDate, AP_OTHER_PERIOD_PERIOD::EndDate, AP_OTHER_PERIOD_PERIOD::PeriodNum, AP_OTHER_PERIOD_PERIOD::StartDate -->

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Exact FSM package contract | AP_OTHER_PERIOD_TYPE.csv, AP_OTHER_PERIOD_PERIOD.csv, ASM_SETUP_CSV_METADATA.xml, and task identity AP_MANAGE_PAYABLES_CALENDARS | Block preview | Use the exact same-task template and current-data export package | Always | |
| Parent calendar identity | AP_OTHER_PERIOD_TYPE CalendarName and CalendarType | Block preview | Supply the parent identity using the exact package headers | When a calendar candidate is requested | |
| Child period parent linkage | AP_OTHER_PERIOD_PERIOD AP_OTHER_PERIOD_TYPE.CalendarName and AP_OTHER_PERIOD_TYPE.CalendarType matching one supplied parent calendar identity, with that parent header row included in the same FSM archive | Block preview | Add the matching parent header row and correct the child-to-parent key values before candidate preparation | When a period candidate is requested | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Package members, header order, node paths, or parent-child keys differ from the exact template | Blocked | Do not build a candidate; restore exact same-task package fidelity | |
| A child period lacks the parent calendar identity or differs from its parent row | Blocked | Correct the parent-child linkage before preview | |
| Package structure and supplied identities pass the documented checks | Supported create/update boundary | Permit only the explicitly supported create fields and bounded update fields; keep every other default, value constraint, and update field unresolved | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Entity and header fidelity | Preserve the exact ordered headers for AP_OTHER_PERIOD_TYPE and AP_OTHER_PERIOD_PERIOD from the same-task template; reject renamed, reordered, added, or omitted fields | Always | |
| CSV row width | Require every nonempty row to contain its entity's exact header count and serialize trailing blank cells explicitly | Always | |
| Date serialization | Parse `YYYY/MM/DD` when retained from a fresh export, then serialize every nonblank candidate date as `YYYY-MM-DD` | Before candidate import | |
| Parent-child hierarchy | Preserve the metadata hierarchy and require each AP_OTHER_PERIOD_PERIOD parent-key pair to be explicitly serialized and match its AP_OTHER_PERIOD_TYPE parent identity | When a child row is supplied | |
| Audit fields | Do not accept CreatedBy, CreationDate, LastUpdatedBy, LastUpdateDate, or LastUpdateLogin as requester-authored create values | When those package columns are present | |
| Supported create fields | Permit the documented task field contract, including AttributeCategory and Attribute1 through Attribute15 on both calendar and period rows | Before candidate preparation | |
| Period DueDate | Require DueDate for PAYMENT TERMS calendar periods; permit a blank DueDate for GENERAL calendar periods. Validate every supplied DueDate as on or after EndDate | Before candidate preparation | |
| Bounded parent update fields | Permit AP_OTHER_PERIOD_TYPE.Description, EffectiveTo, AttributeCategory, and Attribute1 through Attribute15 for an exact existing CalendarName and CalendarType target when all other target values and unspecified rows are preserved; EffectiveTo must be on or after the retained EffectiveFrom | Before candidate preparation | |
| Bounded period update fields | Permit AP_OTHER_PERIOD_PERIOD.Description, StartDate, EndDate, PeriodNum, DueDate, AttributeCategory, and Attribute1 through Attribute15 for an exact existing CalendarName, CalendarType, and PeriodName target when all other target values and unspecified rows are preserved. AP_OTHER_PERIOD_TYPE.CalendarName and AP_OTHER_PERIOD_TYPE.CalendarType are required immutable parent-reference context, not mutable child business fields; enforce EndDate >= StartDate, DueDate >= EndDate when DueDate is supplied, require DueDate for PAYMENT TERMS calendars, prevent overlap with retained ranges, and keep (PeriodYear, PeriodNum) unique | Before candidate preparation | |
| Unproven field behavior | Do not infer defaults, value constraints, direct-write endpoints, or update support for any other package attribute | Before candidate preparation | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CALENDAR.VALIDATE_INPUT | step | 10 | validate_input | valid->CALENDAR.ENFORCE_DESIGN;invalid->CALENDAR.INPUT_BLOCKED | none | stop | Always |
