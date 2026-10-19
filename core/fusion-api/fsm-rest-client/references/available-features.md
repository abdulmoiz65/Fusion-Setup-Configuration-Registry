# Available Features

Use this reference when a user asks for available Fusion features.

Use `available-setup-entities.py --entity feature`. By default it returns 25
rows with Feature Name, Feature Shortname (Code), and Product.

Run from the FSCR repository root:

```bash
python3 core/fusion-api/fsm-rest-client/scripts/available-setup-entities.py
```

Only when the user explicitly asks for every feature, require a project ID and
write a CSV artifact:

```bash
python3 core/fusion-api/fsm-rest-client/scripts/available-setup-entities.py \
  --all --project-id fdos-initial-setup
```

The script uses `boss_scope` and `.fusionaim_boss_token.json`. It is read-only
against Fusion; `--all` writes only the local CSV artifact.
