# Available Functional Areas

Use this reference to retrieve available Fusion functional areas. Call BOSS
`setupEntities` with `functionalAreas=FUNCTIONALAREA` and all other entity
selectors set to `null`. Print the first 25 rows by default with Functional
Area Name, Functional Area Shortname (Code), and Product.

```bash
python3 core/fusion-api/fsm-rest-client/scripts/available-setup-entities.py --entity functional-area
```

Fetch every page and write a project CSV only on an explicit all-areas request:

```bash
python3 core/fusion-api/fsm-rest-client/scripts/available-setup-entities.py --entity functional-area \
  --all --project-id fdos-initial-setup
```
