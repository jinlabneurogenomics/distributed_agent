Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Rab28	0
```

I mechanically verified:

- `trace.md` and `answer.txt` both exist.
- `answer.txt` contains a single fenced `tsv` block and no outside prose.
- The header is exactly `target_name	predicted_n_degs`.
- There is exactly one data row.
- The sole target is exactly the requested `Rab28`, in requested order.
- There are no duplicate targets or extra targets.
- `predicted_n_degs` is a non-negative integer.