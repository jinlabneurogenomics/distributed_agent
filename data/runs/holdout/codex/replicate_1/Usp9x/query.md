Done. I wrote the direct forecast artifacts:

- [trace.md]([local file: trace.md]) with the biology, comparator training evidence, Parquet/profile checks, and synthesis.
- [answer.txt]([local file: answer.txt]) as the required two-line TSV:

```tsv
target_name	predicted_n_degs
Usp9x	6
```

I also verified `answer.txt` parses exactly as `[['target_name', 'predicted_n_degs'], ['Usp9x', '6']]`.