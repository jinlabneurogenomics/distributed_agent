Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted:

```tsv
target_name	predicted_n_degs
Avpr2	0
```

I validated that `answer.txt` is a single fenced `tsv` block, has the exact required header, contains exactly the one requested target in manifest order, has no duplicate targets or extra rows, and uses a non-negative integer point prediction.