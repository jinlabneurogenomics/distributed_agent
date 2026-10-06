Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md]) with the Zbtb24-specific evidence trail, same-experiment analogs/counterexamples, PubMed-supported biology, and limits.
- [answer.txt]([local file: answer.txt]) with exactly the fenced TSV answer.

I also validated that `answer.txt` is a single `tsv` code fence, preserves the manifest order, contains exactly one non-duplicate row for `Zbtb24`, and has a non-negative integer prediction:

```tsv
target_name	predicted_n_degs
Zbtb24	0
```