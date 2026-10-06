Done.

Created both required files in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Nf2	0
```

I verified that `answer.txt`:

- contains only a single fenced `tsv` block
- has the exact required header
- includes the requested `Nf2` target exactly once
- preserves the requested-target order
- uses a non-negative integer prediction
- contains no extra prose outside the fenced block