Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

Final prediction:

```tsv
target_name	predicted_n_degs
Six1	0
```

I validated that `answer.txt` is exactly one `tsv` fenced block, has the required header, contains the one requested target in manifest order with no duplicates or extras, and uses a non-negative integer prediction.