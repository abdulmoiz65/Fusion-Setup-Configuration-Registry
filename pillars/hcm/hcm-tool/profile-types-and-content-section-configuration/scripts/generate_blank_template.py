#!/usr/bin/env python3
"""Create a deterministic Profile Types configuration or export questionnaire."""
import argparse
from pathlib import Path

SEEDED_PROFILE_TYPES = (
    (1, "PERSON"),
    (2, "JOB"),
    (3, "POSITION"),
    (4, "ORGANIZATION"),
    (5, "TEMPLATE"),
    (10, "REQUISITION"),
    (11, "PREREQUISITE"),
    (12, "GUIDE"),
)
SEEDED_PROFILE_TYPE_OPTIONS = ", ".join(
    f"{type_id} {type_key}" for type_id, type_key in SEEDED_PROFILE_TYPES
)

CONFIGURATION_TEMPLATE = f"""# Profile Types and Content Section Configuration Intake

Use this blank template to collect requirements. It does not validate or submit configuration.
Profiles V2 displays only the seeded types listed below. UI visibility does not confirm that every operation is supported.

## Profile Type

| Field | Value |
|---|---|
| Seeded Profiles V2 Type ({SEEDED_PROFILE_TYPE_OPTIONS}) | |
| Requested Operation | |
| Source ProfileTypeCode (if supplied; not the seeded type key) | |
| Source ProfileUsageCode (if supplied; not the seeded type key) | |
| Name | |
| Description | |
| Active | |
| Autocreate Person Profiles (Person only) | |

## Content Sections

| Section Name | Predefined Template (Person only) | Person Section Source (required for non-Person) | Active | Default | Approval Required | Display Order | DFF Context |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Section Properties and Subscribers

| Section | Property | Label | Field Type | Value Set or Lookup | Display (Summary, Detail, Hide) | Default Value | Subscriber |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Ratings, Access, and Dependencies

| Topic | Requirement or Reference |
|---|---|
| Talent ratings | |
| Rating model | |
| Role access | |
| Item catalog or value set | |
| Flexfield | |
| Synchronization | |
| Missing Person section prerequisite | Leave pending; the skill requests scope approval after the exact lookup |
"""

EXPORT_TEMPLATE = f"""# Profile Types and Content Section Instance Export Request

Use this blank template to request an export of current setup data from an authorized Fusion instance.
Completing this template does not validate, approve, submit, or retry an export.
Do not enter passwords, OAuth tokens, client secrets, cookies, token-cache content, or customer configuration rows.

## Request Summary

| Field | Value |
|---|---|
| Project ID | |
| Business Purpose (review, backup, comparison, migration preparation) | |
| Source Fusion Environment Name or Configured Alias | |
| Requested Scope (Profile Types, Content Subscribers, Both) | |
| Coverage (Full task, Filtered) | |
| Keep Returned ZIP Unchanged (recommended: Yes) | Yes |
| Include ZIP File Listing (Yes, No) | Yes |
| Include SHA-256 (Yes, No) | Yes |
| Extract ZIP Under Project Workspace (Yes, No; default: No) | No |

## Scope Details

| Field | Value |
|---|---|
| Profile Types Task | HRT_MANAGE_PROFILE_TYPES |
| Content Subscribers Task | HRT_MANAGE_CONTENT_SUBSCRIBERS |
| Requested Seeded Profiles V2 Type ({SEEDED_PROFILE_TYPE_OPTIONS}; only for a filtered Profile Types request) | |
| Business Description of Any Other Filter | |
| Reason Full-Task Export Is Not Appropriate | |

Do not enter BusinessObjectCode, AttributeSet, AttributeName, or AttributeValue unless an implementation specialist supplies current source-instance evidence. The skill must confirm any technical export criteria before execution and must not derive them from the seeded type ID or key.

## Output and Timing Preferences

| Field | Value |
|---|---|
| Output Directory (optional; must remain under project/{{project_id}}/exports) | |
| Preferred File Label (optional; no overwrite) | |
| Wait Seconds (optional; default: 300) | |
| Poll Interval Seconds (optional; default: 15) | |

## Readiness Notes

| Check | Response or Notes |
|---|---|
| Source environment is the intended instance | |
| User can authenticate through the configured FDOS login flow | |
| Export Import Functional Setups User role is available | |
| Task-specific export privilege is available | |
| Filter evidence is available, if Filtered was selected | |

## Execution Approval

| Field | Value |
|---|---|
| Status | Pending |
| Note | Approval is requested separately after the exact export plan is shown. Do not enter approval here. |
"""

TEMPLATES = {
    "configuration": CONFIGURATION_TEMPLATE,
    "export": EXPORT_TEMPLATE,
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=tuple(TEMPLATES),
        default="configuration",
        help="Template to generate (default: configuration).",
    )
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(TEMPLATES[args.mode], encoding="utf-8")

if __name__ == "__main__":
    main()
