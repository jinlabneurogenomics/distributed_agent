Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md]) contains the Nme7-specific reasoning, same-experiment ciliary/Hedgehog analogs and Wnt counterexamples, Distributed Agents corpus evidence, PubMed/UniProt/GO sources, and explicit caveats.
- [answer.txt]([local file: answer.txt]) contains exactly one fenced `tsv` block with the requested row:

```tsv
target_name	predicted_n_degs
Nme7	0
```

I also validated that `answer.txt` exactly matches the required fenced TSV format and that both output files are ASCII.