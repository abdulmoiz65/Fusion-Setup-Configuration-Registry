# Connector Authentication Configuration

This reference defines the non-secret connector setup inputs required when the
selected connector OpenAPI contract does not document their values. It documents the
runtime contract; it is not a credential store and must not contain tenant
values, tokens, private keys, client secrets, or `authenticationDetails`.

## Supported properties

An approved local, gitignored properties source may provide only these keys:

```properties
authType=OAuth2
grantType=<connector-supported-grant-type>
hostUrl=https://<connector-service-host>
accessTokenUrl=https://<identity-domain-host>/oauth2/v1/token
scopes=<oauth-scope>
```

The same five fields may be supplied directly by the user as a structured
`connector_setup` object. Do not infer values from the Risk Cloud environment
authentication properties file; that file authenticates the BOSS client and is
not the connector configuration.

## Resolution and validation

Resolve values in this order:

1. Explicit values supplied by the user.
2. Values from an approved local, gitignored properties source.
3. Ask the user for any missing required values.

Reject unknown keys, blank values, malformed properties, and non-HTTPS
`hostUrl` or `accessTokenUrl` values. Keep the resolved configuration in memory
for the current run and include only these non-secret fields in the
approval-bound connector payload.

## Missing-Value Prompt Protocol

Treat a value as unavailable when it is blank, absent, enclosed in angle
brackets, or uses an example or dummy host such as `<identity-domain-host>` or
`https://...`. Do not treat `authType=OAuth2` as a complete configuration by
itself.

When one or more required values are unavailable, ask the user for only the
affected values in one JSON object. Preserve all valid resolved values and put
the user's returned values into the in-memory `connector_setup` output before
the next workflow step. Never write the returned values to this reference file.

- If `hostUrl` is unavailable or dummy, ask the user for the actual HTTPS connector
  service base URL.
- If `accessTokenUrl` is unavailable or dummy, ask the user for the actual
  HTTPS OAuth token URL.
- If `authType` is `OAuth2` and `scopes` is unavailable or blank, ask the user
  for the actual OAuth scopes.
- If `grantType` is unavailable, ask the user for the connector-supported grant
  type.

Use this response shape, omitting already-resolved fields:

```json
{
  "grantType": "<connector-supported grant type>",
  "hostUrl": "https://<connector-service-host>",
  "accessTokenUrl": "https://<identity-domain-host>/oauth2/v1/token",
  "scopes": "<OAuth scopes>"
}
```

Do not request or accept client secrets, bearer tokens, refresh tokens, private
keys, or `authenticationDetails` in this response.

Credentials and authentication details are completed through the Risk Cloud
UI after connector registration. Never read or persist client secrets, bearer
tokens, refresh tokens, private keys, or `authenticationDetails` from this
configuration source.
