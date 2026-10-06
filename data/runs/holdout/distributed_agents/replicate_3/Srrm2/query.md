Done: I created both required outputs in the run directory.

- [trace.md]([local file: trace.md]) contains the target-specific reasoning for `Srrm2`, with the focal training counts, same-experiment corpus evidence, SRRM2/SON literature, local GO/Reactome/CORUM/STRING annotation evidence, and explicit caveats.
- [answer.txt]([local file: answer.txt]) contains exactly the requested fenced TSV:

```tsv
target_name	predicted_n_degs
Srrm2	8
```

I also validated that `answer.txt` has the single `tsv` fence, the correct header, one `Srrm2` row, and no extra prose.