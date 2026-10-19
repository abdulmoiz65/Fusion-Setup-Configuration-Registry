# Data Capture Rules Overview

## Purpose

Use this reference for source-backed conceptual and business-value questions
about Data Capture and Data Capture Rules. Use the task's BOSS reference for
record metadata and read API behavior, and its security reference for access
requirements.

## What Data Capture Is

Data Capture automates updates to application information by interpreting
free-form sources such as emails, call notes, and meeting summaries. A Data
Capture Rule identifies the fields or attributes relevant to a business
context and provides AI instructions for extracting and mapping information.

## How It Helps

For Sales Orchestration, Data Capture enables the Deal Advisor to suggest
updates to opportunity attributes from customer interactions. This reduces
manual data entry and helps keep opportunity information aligned with what was
learned during seller-customer engagement.

The public setup guidance describes this high-level flow:

1. Open **Data Capture Rules** from Sales Administration.
2. Start **Create Data Capture**.
3. Describe the data to capture or select attributes to explore.
4. Specify the opportunity attributes that the rule should update.

## Attribute Guidance

Oracle lists these as typical opportunity attributes for effective deal
capture, not as a mandatory set:

- Close Date
- Win Probability
- Expected Revenue
- Opportunity Type
- Status
- Comments

Budget Amount, Forecast Category, and Decision Level are additional examples
that can provide more context and forecasting insight.

## Release-Specific Boundary

The public page specifically states that in release 26B only opportunity
attributes can be enabled and that the agent cannot extract Dynamic Choice List
values, dependent-list values, or child-object data. Treat this as a 26B
statement. Revalidate it against documentation and API metadata for any later
target release; do not silently apply it to 26C or beyond.

Do not infer record fields, REST payloads, statuses, or validation behavior from
the setup examples. Use the target-release BOSS contract or return
`SOURCE_GAP`.

## Source

- Oracle Fusion Cloud Sales, *Before You Start*, Data Capture section:
  https://docs.oracle.com/en/cloud/saas/sales/gsaso/befoer-you-start.html#Data-Capture
- Source accessed: 2026-08-10.
- The Oracle page is published under the `latest` documentation path. Recheck
  the page when answering release-sensitive questions.
