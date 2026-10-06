Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md]) with the dataset checks, complex III analog counts, focal-cell expression-profile evidence, Distributed Agents corpus evidence, external UQCC2 biology, and the explicit uncertainty around `0` vs `1`.
- [answer.txt]([local file: answer.txt]) containing exactly one fenced `tsv` block.

The final point prediction is:

```tsv
target_name	predicted_n_degs
Uqcc2	1
```

I also verified that `answer.txt` matches the required fenced-TSV shape exactly and that both output files are ASCII-only.