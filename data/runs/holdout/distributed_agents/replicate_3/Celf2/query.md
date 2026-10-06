Done. I created the required deliverables in the run directory:

- [trace.md]([local file: trace.md]) documents the Celf2-specific reasoning, the within-dataset RNA-processing analogs/counterexamples, Distributed Agents corpus/runtime use, PubMed citations, and the evidence limits.
- [answer.txt]([local file: answer.txt]) contains exactly the required single fenced TSV block.

I also validated that `answer.txt` preserves the manifest order, includes `Celf2` exactly once, and uses a non-negative integer prediction:

```tsv
target_name	predicted_n_degs
Celf2	12
```