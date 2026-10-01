# BioKG data

- `graph/`: complete Neo4j database dump and manifest.
- `base/`: canonical node and relationship CSVs plus build reports.
- `claims/`: Claim memberships, relations, and summary counts.
- `normalization/`: concept normalization map and measured-gene universe.

Normal operation treats these files as read-only. Mutable build and database
state belongs under the projection's ignored `_work/` directory.

