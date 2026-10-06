Done. I created both requested outputs in the run directory:

- [trace.md]([local file: trace.md]) with the Rab28-specific evidence chain, including focal training-count calibration, ciliary/Rab/endolysosomal within-dataset analogs, Distributed Agents corpus evidence, Rab28 PubMed citations, and limitations.
- [answer.txt]([local file: answer.txt]) with exactly the required fenced TSV:

```tsv
target_name	predicted_n_degs
Rab28	0
```

I also validated that `answer.txt` has the exact header, preserves the one requested manifest target, has no duplicate rows, and contains a non-negative integer prediction.