Done.

Created both required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I mechanically validated that `answer.txt`:

- is a single fenced `tsv` block
- has exactly `target_name` and `predicted_n_degs`
- contains exactly the one requested target
- preserves requested-target order
- has no duplicate or extra targets
- uses a non-negative integer prediction

Final prediction:

```tsv
target_name	predicted_n_degs
Chrnb4	0
```