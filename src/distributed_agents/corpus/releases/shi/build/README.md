# Shi build commands

Run these commands from the release directory to rebuild and validate the
derived artifacts:

```bash
python build/build_ledgers.py
python skills/findings-ledger-skill/scripts/generate_ledger_calibration.py
python skills/findings-bm25-skill/scripts/findings_bm25.py build --overwrite
python skills/findings-bm25-skill/scripts/findings_bm25.py verify
python -m distributed_agents.build.reference_normalization \
  --release-root . \
  --output artifacts/contracts/publication_reference_mapping.json
python build/materialize_claim_overlay.py
PYTHONPATH=projections python -m biokg.build.reconcile_sourceguard_base
python -m distributed_agents.corpus doctor --release shi
```

Update the artifact hashes, byte sizes, and record counts in `release.json`
after rebuilding tracked outputs.
