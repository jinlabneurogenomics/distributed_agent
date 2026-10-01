# Shi holdout Claim artifacts

| File | Role |
|---|---|
| `neighborhoods.jsonl` | Overlapping discovery neighborhoods |
| `proposals.jsonl` | Neighborhood-local Claim proposals |
| `proposal_dispositions.jsonl` | Outcome for every proposal |
| `claims.jsonl` | Final normalized Claim nodes |
| `contributions.jsonl` | Typed Finding-to-Claim contributions |
| `finding_dispositions.jsonl` | Claim coverage state for every Finding |
| `build.json` | Build configuration, counts, and artifact hashes |

Every final Claim has at least two Findings from at least two targets and at
least one `ANCHORS` contribution.

Validate the release after changing these files:

```bash
python -m distributed_agents.corpus doctor --release shi_holdout
```

