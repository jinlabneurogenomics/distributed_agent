Created both requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The requested held-out manifest contains one target, `Gria4`, and `answer.txt` contains exactly one fenced `tsv` block with that target in manifest order:

```tsv
target_name	predicted_n_degs
Gria4	0
```

I mechanically validated that:

- `trace.md` exists and is non-empty.
- `answer.txt` exists.
- `answer.txt` is exactly one fenced `tsv` block.
- The header is exactly `target_name	predicted_n_degs`.
- The answer has exactly one data row.
- The row target list exactly matches the requested-target CSV in order.
- There are no duplicate targets.
- `predicted_n_degs` is a non-negative integer.

The prediction is anchored on the declared training endpoint and exact focal-cell DE rows: `Gria1`, `Gria2`, and `Gria3` all had `0` focal DEGs; the AMPAR-adjacent `Cacng2`/`Cacng3` perturbations were also `0`; most PSD and nearby signaling perturbations were 0 to 2, often self-only; and `Grin1 = 89` was treated as a thalamic NMDAR counterexample rather than transferred to `Gria4`.