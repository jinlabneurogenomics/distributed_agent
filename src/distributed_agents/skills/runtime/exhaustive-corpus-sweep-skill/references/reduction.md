# Reduction protocol

Reduction begins only after deterministic reconciliation passes.

1. Read `sweep_audit.json` and `merged_candidates.jsonl`.
2. Preserve the originating `unit_id` and `slice_id` for every emitted record.
3. Deduplicate only records that assert the same task-relevant relationship;
   retain all supporting and contradicting provenance when merging them.
4. Apply cross-unit comparison, ordering, and scientific synthesis only in the
   root agent. Reader-local order and slice membership carry no significance.
5. Do not use graph proximity, number of mentions, number of slices, or reader
   confidence as a biological ranking score.
6. Report exact planned, covered, emitted, and rejected counts. If the audit is
   not passing, label the work incomplete and do not claim an exhaustive sweep.

