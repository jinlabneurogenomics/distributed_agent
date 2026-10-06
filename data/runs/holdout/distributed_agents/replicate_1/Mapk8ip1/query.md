Created both required files in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final prediction is:

```tsv
target_name	predicted_n_degs
Mapk8ip1	0
```

I also mechanically validated `answer.txt`: it is a single fenced `tsv` block, has the exact two required columns, contains exactly the one requested target in manifest order, has no duplicate or extra targets, and the prediction is a non-negative integer.