# Subscription Maintenance Readiness Reference

## Use

Read this reference when a Service Mapping request depends on preventive maintenance behavior for subscriptions, including coverage-template association, covered levels, downstream Maintenance Cloud processing, or transfer readiness.

## Source

- [Sell and Manage Preventive Maintenance Plans for Subscriptions](https://docs.oracle.com/en/cloud/saas/readiness/sales/24b/ssma-24b/24B-subscription-wn-f31902.htm)

## Key Guidance

- The 24B readiness feature associates a maintenance program template to a coverage product so a maintenance program can be created for the coverage product covered levels.
- After a subscription is active, the documented downstream sequence is:
  1. Send Maintenance Program and Covered Assets to Oracle Maintenance.
  2. Import Maintenance Programs.
  3. Retrieve Instantiated Maintenance Program.
- The instantiated maintenance program is visible in Subscriptions after the three scheduled processes complete.
- The readiness note says no additional feature-enablement steps are required.

## Boundaries

This reference does not define Service Mapping source aliases, algorithm mutation routes, ESS request parameters, polling contracts, or Maintenance import execution paths. Treat those items as separate environment-specific workflow contracts.
