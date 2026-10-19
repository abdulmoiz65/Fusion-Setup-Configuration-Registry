# Sales Motion Agentic Authoring Prompt Examples

## Purpose

Use these examples when a user asks what they can enter in the Fusion Sales
Motion UI's embedded agentic authoring experience. The prompts ask the product
agent to propose a Sales Motion definition for the user to review.

These are UI prompt examples only. They do not authorize the FSCR skill to
create, update, activate, archive, or otherwise modify a Sales Motion through
BOSS, REST, Data Loader, or another integration.

## Prompt Emission Rules

- Use business context supplied by the user when it is available.
- When context is missing, choose realistic synthetic values for the industry,
  customer segment, geography, product, business outcome, stakeholders, risks,
  and sales-cycle conditions.
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

## Sample Prompts

1. Create a sales motion for acquiring North American manufacturing companies
   with annual revenue above USD 1 billion for a cloud-based financial
   management and procurement solution. Establish a streamlined pathway from
   initial qualification through procurement, contracting, and solution
   delivery. Emphasize rapid opportunity qualification, executive sponsorship,
   business-case development, security and compliance review, technical
   validation, implementation readiness, and measurable completion criteria.
   Ask follow-up questions if important information is missing.
2. Create a sales motion for growing revenue from existing customers currently
   using an on-premise human capital management solution by moving them to cloud
   HCM with payroll, workforce planning, and employee experience capabilities.
   Include objectives for assessing current usage, identifying operational
   gaps, engaging HR and finance executives, demonstrating incremental value,
   validating budget, addressing migration risks, and agreeing on an adoption
   roadmap. Generate high-value activities and observable completion criteria
   for every objective.
3. Create a sales motion for selling a patient scheduling and engagement
   platform to mid-sized healthcare providers in the United States. Focus on
   establishing trust, agreeing on business goals, uncovering scheduling and
   patient-access challenges, understanding budget availability, identifying
   clinical and administrative stakeholders, and documenting the customer's
   decision and approval process. Generate measurable objectives, recommended
   high-value activities, and evidence-based completion criteria.
4. Create a sales motion for renewing a customer-service software subscription
   for a national retail company whose product usage has declined and whose
   contract expires in 120 days. Include objectives for assessing adoption,
   identifying unresolved service issues, quantifying realized value,
   rebuilding executive alignment, creating a customer recovery plan,
   presenting the renewal business case, and confirming renewal scope, budget,
   and signature date. Define clear evidence required to complete each
   objective.
5. Create a sales motion for selling a cloud analytics platform to state
   government agencies in India. Address stakeholder mapping, business
   requirements, budget approval, public procurement procedures, tender
   requirements, data security, regulatory compliance, technical evaluation,
   proof of concept, contracting, and phased implementation planning. Generate
   practical high-value activities and objective completion criteria based on
   observable customer evidence.
6. Create a sales motion for selling energy-efficient cooling systems to large
   data-center operators in Southeast Asia. Cover site assessment, capacity and
   energy requirements, solution design, regulatory considerations,
   total-cost-of-ownership analysis, technical validation, executive and
   facilities-management approval, commercial negotiation, delivery planning,
   installation, testing, training, and post-sale support. Identify the
   relevant decision-makers and define measurable completion criteria for every
   objective.

## Source

- Oracle Fusion Cloud Sales, *Create a Sales Motion*:
  https://docs.oracle.com/en/cloud/saas/sales/gsaso/create-a-sales-motion.html
- Source accessed: 2026-08-10.
