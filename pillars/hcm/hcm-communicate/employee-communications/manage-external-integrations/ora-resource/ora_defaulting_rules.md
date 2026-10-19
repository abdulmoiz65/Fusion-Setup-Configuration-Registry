# Manage External Integrations Defaulting Rules

Do not default a desired state, environment, or writable setting value. The only defaults below apply to the read-only status GET.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| REST resource version | latest | The status GET is built | Yes, when the routed REST workflow supplies a supported version | |
| Integration selection | Microsoft Teams and Slack | A current-status request does not name one integration | Yes | |
