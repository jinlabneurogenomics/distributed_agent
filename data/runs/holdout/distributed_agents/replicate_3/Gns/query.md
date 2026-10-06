Done: I created both required deliverables in the run directory.

- [trace.md]([local file: trace.md]) documents the same-experiment analogs, Distributed Agents corpus evidence, external `Gns`/MPS IIID biology, counterexamples, and why the final call is `0`.
- [answer.txt]([local file: answer.txt]) contains exactly the requested fenced TSV:

```tsv
target_name	predicted_n_degs
Gns	0
```

I also validated that `answer.txt` matches the requested shape exactly: one fenced `tsv` block, the two required columns, one row for `Gns`, a non-negative integer prediction, no duplicate or extra targets, and no prose outside the block.