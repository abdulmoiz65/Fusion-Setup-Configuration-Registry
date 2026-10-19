# Adapter-free feasibility trial

Date: 2026-10-09. No external writes; no Benefits or Core Data Loader changes.

## Verified

- Listing uses the existing shared Fusion REST client (see SKILL.md).
- The unchanged parent `scripts/eligibility.py import` accepts `--task-name
  "Opportunity Marketplace Eligibility Profiles"`, `--operation-label
  "Opportunity Marketplace Eligibility Plan Copy import"`, and `--import-prefix
  OM_TRIAL_`. With the existing child task context, its local preview binds
  ORA_IRC_MP_ELIGIBILITY_PROFILE and the active Run Book correctly.
- The parent `excel_to_plan_copy_package.build_eligibility_import_package`
  function assembles existing validated XML directly; its package validator
  passes and APS/PRTP/ORA_OPP_MARKET_PLACE remain intact. No module globals
  or source files were patched.

## Trial limits and remaining requirements

The test reused import-9 XML and archive, whose Test Profile4 already exists.
Do not submit that package again or treat this trial as an approval request.
It does not establish fresh workbook conversion or a complete replacement
execution route. The parent workbook converter still rejects Specific
assignment/APS. A declarative XML preparation procedure would need explicit
field mappings, exact lookup resolution, cross-tab dependency validation,
source-to-XML checks and tests before becoming the creation route. Do not
convert a falsified ANE workbook and silently patch its package afterward.

The parent importer does not provide the child's enterprise-wide name
preflight. Preserve the all-usage paginated check immediately before any
future authorized creation, as well as local duplicate checks and Fusion's
final validation. Validate usage, Participant and Specific assignment before
preview. Verify monitoring recovery and usage-scoped evaluation independently.

Existing adapter-dependent commands remain unavailable when their executable
is absent. These findings are feasibility evidence, not authorization to bypass
that gap with direct REST writes. A full migration must update the operation
routes and replace adapter-dependent tests with behavioral coverage.
