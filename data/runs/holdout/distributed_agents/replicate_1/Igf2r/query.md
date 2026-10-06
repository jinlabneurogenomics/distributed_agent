Created the required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Igf2r	0
```

I validated that `answer.txt` contains only a single fenced `tsv` block, has exactly the required `target_name	predicted_n_degs` header, contains the one requested target `Igf2r` exactly once in manifest order, and uses a non-negative integer prediction.