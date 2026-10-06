Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted:

```tsv
target_name	predicted_n_degs
Mpdz	0
```

I also mechanically validated the final table:

- `answer.txt` contains exactly one fenced `tsv` block and no prose outside it.
- Header is exactly `target_name	predicted_n_degs`.
- Row count matches the requested-target manifest: 1 row.
- Target order matches the manifest: `Mpdz`.
- Targets are unique.
- `predicted_n_degs` is a non-negative integer.