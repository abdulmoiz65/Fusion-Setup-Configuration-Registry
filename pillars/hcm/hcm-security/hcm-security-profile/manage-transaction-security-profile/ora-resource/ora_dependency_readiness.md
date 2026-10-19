# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Transaction security profile | Create or select the transaction security profile using the Manage Transaction Security Profiles task |
| 2 | Data role | Assign the transaction security profile to a data role |
| 3 | User assignment | Assign the data role to the intended users |
| 4 | Transaction security enablement | Enable transaction security in Manage Enterprise HCM Information |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| transaction_security_profile_assignment | Data role has the selected transaction security profile | Yes | Claiming that users are restricted to selected transaction types | Verify | Oracle public documentation | TBD | The profile identifies the transaction categories that a data role can manage | Assign the profile to each applicable data role | Assigned transaction security profile |
| transaction_security_role_assignment | Intended users have the applicable data role | Yes | Claiming that users are restricted to selected transaction types | Verify | Oracle public documentation | TBD | Data-role users manage only transactions permitted by the assigned profile and person security | Assign each applicable data role to the intended users | Assigned users |
| transaction_security_enabled | Transaction security is enabled | Yes | Claiming that users are restricted to selected transaction types | Verify | Oracle public documentation | TBD | Access restrictions are not applied while transaction security is disabled | Enable transaction security in Manage Enterprise HCM Information | Transaction security enabled status |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| readiness missing | Profile, role assignment, user assignment, or enablement is not verified | No |
| ready for access restriction | All documented dependency checks are verified | No |
