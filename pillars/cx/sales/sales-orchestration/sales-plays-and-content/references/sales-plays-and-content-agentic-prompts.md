# Sales Plays and Content Agentic Authoring Prompt Examples

## Purpose

Use these examples when a user asks what they can enter in the Fusion Sales
Plays and Content UI's embedded agentic authoring experience. The prompts below
ask the product agent to propose a Sales Play definition and supporting
collateral for the user to review.

These are UI prompt examples only. They do not authorize the FSCR skill to
create, update, activate, publish, archive, copy, or otherwise modify a Sales
Play or content record through BOSS, REST, Data Loader, or another integration.

## Prompt Emission Rules

- Use business context supplied by the user when it is available.
- When context is missing, choose realistic synthetic values for the industry,
  customer segment, geography, product, selling scenario, and supporting
  collateral.
- Emit every prompt as standalone, copy-ready text. Never emit a prompt that
  requires the user to replace a placeholder, blank, generic stand-in, or
  bracketed value.
- Keep synthetic scenarios free of real customer names, tenant details, and
  confidential configuration.
- Put each emitted prompt in its own fenced text block. Any explanation that
  values are synthetic belongs outside the prompt.
- Even when the user requests a reusable template, return one or more fully
  populated examples and offer to generate another concrete scenario instead
  of emitting placeholders.

## Content Source Boundary

The approved source establishes agentic prompt authoring for a Sales Play and
the supporting collateral the agent recommends. It does not establish a
separate agentic prompt flow for creating a `CONTENT_BUNDLE` record. Cover
content requests by naming concrete collateral in a Sales Play prompt. For a
request specifically asking for a content-bundle authoring prompt, return
`SOURCE_GAP` until an approved Oracle source establishes that UI behavior; do
not present a Sales Play prompt as content-bundle creation.

## Sample Sales Play Prompts

1. Create a sales play to upsell an AI-powered cybersecurity monitoring module
   to existing North American technology customers with more than 1,000
   employees that already use the core security platform. Focus on chief
   information security officers and security operations leaders. Recommend a
   solution brief, threat-detection demonstration, security architecture guide,
   ROI calculator, implementation plan, and enterprise customer success story
   as supporting collateral.
2. Create a sales play to sell energy-efficient automated packaging equipment
   to large food and beverage manufacturers in Germany. Focus on production
   executives, plant managers, engineering leaders, and procurement teams.
   Recommend technical specifications, an energy-savings assessment,
   total-cost-of-ownership calculator, regulatory compliance brief, factory
   reference story, and installation-readiness checklist as supporting
   collateral.
3. Create a sales play to sell net-new edge-computing hardware to
   telecommunications operators in Southeast Asia that are expanding 5G
   coverage. Focus on network modernization, low-latency processing, deployment
   scale, resilience, and operating cost. Recommend a reference architecture,
   benchmark report, deployment guide, product comparison, commercial proposal
   template, and telecom customer case study as supporting collateral.
4. Create a sales play to sell a cloud financial management solution to
   mid-sized wholesale distribution companies in India with annual revenue
   between INR 500 crore and INR 2,000 crore. Focus on finance transformation,
   faster period close, procurement control, inventory visibility, and
   regulatory reporting. Recommend an executive presentation, process-maturity
   assessment, solution demonstration, value calculator, implementation
   roadmap, and distribution-industry customer story as supporting collateral.
5. Create a sales play to cross-sell workforce planning and employee experience
   capabilities to United Kingdom retail customers already using cloud human
   capital management. Focus on HR leaders, workforce planning teams, finance
   executives, and store operations leaders. Recommend an adoption assessment,
   workforce-planning demonstration, business-value brief, integration guide,
   phased rollout plan, and retail customer success story as supporting
   collateral.

## Source

- Oracle Fusion Cloud Sales, *Create a Sales Play*:
  https://docs.oracle.com/en/cloud/saas/sales/gsaso/create-a-sales-play.html
- Source accessed: 2026-08-10.
