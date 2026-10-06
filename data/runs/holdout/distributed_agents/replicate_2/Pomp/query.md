Done. I wrote both required outputs in the run directory:

- [trace.md]([local file: trace.md]) with the POMP-specific reasoning, internal Distributed Agents corpus evidence, same-experiment `Psmb4`/`Psmc1` analogs, weak proteostasis counterexamples, PubMed citations, and the limits of the extrapolation.
- [answer.txt]([local file: answer.txt]) with the strict fenced TSV.

The final point prediction is:

```tsv
target_name	predicted_n_degs
Pomp	560
```

I also validated that `answer.txt` contains only a single `tsv` fenced block, has exactly one row for the manifest target, preserves the requested order, and uses a non-negative integer.