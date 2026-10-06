Created the required outputs in the run directory:

- [trace.md](./trace.md): target-specific reasoning for `Gli3`, including focal-cell training analogs, same-experiment corpus evidence, PubMed-cited Hedgehog/Gli biology, causal transfer logic, and limitations.
- [answer.txt](./answer.txt): the required single fenced `tsv` block.

I predicted:

```tsv
target_name	predicted_n_degs
Gli3	0
```

I also mechanically validated that `answer.txt` has:

- exactly one fenced `tsv` block;
- header `target_name	predicted_n_degs`;
- exactly one data row;
- the requested target order from `the single-target request`;
- no duplicate or extra targets;
- a non-negative integer prediction.