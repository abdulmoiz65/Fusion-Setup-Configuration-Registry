# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Procurement offering | Opt in to Procurement and applicable offerings before implementing Procurement setup. |
| 2 | Implementation access | Assign a configured implementation role based on Application Implementation Consultant before performing implementation setup. |
| 3 | Line-type access | Grant the supplied Manage Purchasing Line Type privilege before using the UI or REST resource. |
| 4 | Flexfield setup | Deploy the required descriptive-flexfield context and segments before supplying DFF values. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PLT.PROCUREMENT_OPT_IN | Procurement offering is opted in | Yes | Any implementation activity | Verify | Oracle Procurement implementation documentation | | The task belongs to the Procurement offering | Confirm the offering is opted in before setup work | Offering readiness |
| PLT.IMPLEMENTATION_ROLE | Configured implementation role is assigned | Yes | Any implementation activity | Verify | Oracle Procurement implementation documentation | | Oracle requires a configured role based on Application Implementation Consultant to start an implementation | Obtain the required implementation access before proceeding | Access readiness |
| PLT.LINE_TYPE_PRIVILEGE | Manage Purchasing Line Type privilege is available | Yes | UI or REST create or update | Verify | Supplied UI and REST acceptance criteria | | The supplied acceptance criteria identify the privilege as the access gate for the page and REST service | Obtain the privilege before attempting the operation | Authorization readiness |
| PLT.DFF_CONTEXT | DFF context and segments are deployed | Conditional | DFF is supplied | Verify | Data Loader business-object execution result | | The Data Loader business object identifies DFF attributes and validates server acceptance; client-side validation must not retrieve them | Supply the parent `LineTypeCode` linkage. The converter derives a deployed global context from the DFF header and omits its display value from technical `__FLEX_Context`; let the Data Loader resolve remaining context and segments. | Data Loader validation result |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| MISSING | Required offering, role, privilege, or DFF context evidence is absent | No |
| READY | Required dependency evidence is present | No |
| TBD | Supplied deployment evidence does not establish the DFF context and values before the Data Loader validates them | No |
