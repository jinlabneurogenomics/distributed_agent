Created the required run-local outputs:

- [trace.md](./trace.md) with the target-specific evidence and rationale for `Thbd`
- [answer.txt](./answer.txt) with the exact fenced `tsv` answer

The final point prediction is:

```tsv
target_name	predicted_n_degs
Thbd	0
```

I also mechanically validated that `answer.txt`:

- contains only a single fenced `tsv` block
- has the exact header `target_name	predicted_n_degs`
- has exactly one row
- preserves the requested manifest order
- contains `Thbd` exactly once and no extra targets
- uses a non-negative integer prediction