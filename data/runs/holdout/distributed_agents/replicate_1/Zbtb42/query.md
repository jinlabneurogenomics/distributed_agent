Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

Final prediction:

```tsv
target_name	predicted_n_degs
Zbtb42	0
```

I validated that `answer.txt` is a single fenced `tsv` block, has exactly the required header, contains one non-negative integer row, preserves the requested-target order, has no duplicate or extra targets, and is referentially identical to the requested manifest target list.