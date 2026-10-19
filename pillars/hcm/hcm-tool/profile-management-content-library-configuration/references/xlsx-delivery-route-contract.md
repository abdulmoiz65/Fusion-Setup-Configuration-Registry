# XLSX Business-Object Prefix and Delivery Route Contract

## Purpose

Detect an ambiguous Data Loader XLSX business-object or worksheet prefix before
creating the technical workbook. This contract does not apply to the governed
blank setup-intake workbook.

Current GROW-8154 V1 does not select technical HDL/HSDL/DAT preparation.
The detection helper and legacy decision table below preserve historical
regression coverage, not a current V1 fallback route. For V1, select only an
exact supported FSM contract after its gates; otherwise return the provider
blocker. Blank configuration intake remains available without Fusion access.

## Detection

Use exact technical business-object and section discriminators resolved from
the workflow-declared Data Loader metadata source. Before writing an XLSX:

1. Truncate each section discriminator to the existing 30-character Data
   Loader worksheet limit.
2. Compare the generated prefixes case-insensitively.
3. Treat a duplicate generated prefix as a collision.
4. Treat a requested root prefix that resolves to more than one registered
   top-level business object as a collision.
5. Return blocked when the metadata source is absent or ambiguous; never invent
   a discriminator.

The existing Core Data Loader validation remains a second fail-closed gate.

## Historical Technical Route Decision (Not V1 Authorization)

| Condition | Result |
|---|---|
| No collision and no explicit DAT request | Technical XLSX is eligible for later generation |
| Collision and the exact requested operation has a task-local valid FSM route | Select FSM and do not create XLSX |
| Collision and no valid FSM route | Block before file creation and require an explicit request to prepare DAT |
| Explicit DAT request | Select DAT preparation; this is a format request only |

A generic continuation, proposal confirmation, assumption review, or package
approval is not an explicit DAT request. DAT preparation does not approve
upload or import. Never fall back to DAT or HDL after a failed or uncertain FSM
mutation.
