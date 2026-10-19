# Sales Orchestration Overview

## Purpose

Use this reference for source-backed explanations of what Sales Orchestration
is, how it helps sellers, the agent-assisted capabilities it provides, and its
trust and security model. Use the nested task skills for task-specific setup,
security, API, and live-read questions.

## What Sales Orchestration Is

Sales Orchestration is an agentic seller experience built into Oracle Sales.
It uses intelligent agents to automate routine work and streamline seller
workflows while sellers engage customers and progress opportunities.

It is not merely a configuration model of Sales Motions, Sales Plays, and Data
Capture Rules. Those setup objects provide strategy, approved collateral, and
data-extraction context; the seller experience applies that context to the
active opportunity and its customer engagements.

## Definition Response Guidance

When a user asks a broad definition question such as "What is Sales
Orchestration?", explain all of the following in plain language:

1. It is an AI-agent-based selling experience in Oracle Sales, rather than a
   standalone integration or a static workflow checklist.
2. It helps sellers work opportunities by bringing customer-engagement context,
   sales strategy, and approved product knowledge into their daily workflow.
3. It reduces administrative work—such as reviewing communications and manually
   recording opportunity details—so sellers can spend more time with customers.
4. It supports deal progression through interaction summaries, prioritized
   next-best actions, suggested opportunity updates, drafted emails and talking
   points, product/deal answers, collateral, and suggested new contacts.
5. Sellers retain control: they review drafts and suggested updates; the
   documented experience does not send emails or add products without a human
   in the loop.
6. Recommendations and drafts during a sale are grounded in the sales
   application and uploaded documents. Internet information is limited to the
   initial Sales Motion setup.

Mention Sales Motions, Sales Plays, and Data Capture only as supporting
configuration context after giving the definition and business value. Do not
present them as the complete product definition.

## How It Helps

Sales Orchestration helps sellers create communications tailored to customer
needs and product strategies. By reducing routine work and manual data entry,
it gives sellers more time for customer engagement, improves productivity, and
helps opportunities progress more quickly.

The documented agent-assisted capabilities include:

- summarizing customer interactions so sellers do not need to review every
  email thread and note;
- recommending next-best actions aimed at completing configured sales-strategy
  objectives;
- capturing opportunity information from interactions and suggesting updates
  to fields and attributes;
- capturing and summarizing supported web-conference transcripts;
- drafting emails and talking points;
- answering product and deal questions and surfacing relevant collateral; and
- recommending contacts to add to an opportunity.

## Human Oversight and Source Boundaries

- Sellers can review drafted emails and suggested opportunity updates.
- The documented experience does not send an email or add a product to an
  opportunity without a person in the loop.
- Because Sales Orchestration is embedded in the sales application, it follows
  the application's existing setup and security.
- Only initial Sales Motion setup may use internet information. During a sale,
  recommendations and drafts use information from the sales application and
  uploaded documents.

Do not generalize these statements into an approval for unattended changes or
an external API operation. A conceptual answer is guidance only.

## Task Routing

- Route Sales Motion strategy, objectives, and high-value activities to
  `cx.sales.sales-orchestration.sales-motions`.
- Route Sales Plays, content bundles or packets, collateral, and Content
  Intelligence to `cx.sales.sales-orchestration.sales-plays-and-content`.
- Route Data Capture Rules and captured attributes to
  `cx.sales.sales-orchestration.data-capture-rules`.
- Route general prerequisite readiness to
  `cx.sales.sales-orchestration.pre-requisites`.

## Source

- Oracle Fusion Cloud Sales, *Overview of Sales Orchestration*:
  https://docs.oracle.com/en/cloud/saas/sales/gsaso/overview.html
- Source accessed: 2026-08-24.
- The Oracle page is published under the `latest` documentation path. Recheck
  the page when answering release-sensitive questions.
