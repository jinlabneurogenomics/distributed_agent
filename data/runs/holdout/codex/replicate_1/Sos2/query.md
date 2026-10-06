Done. I wrote the forecast artifacts:

- [trace.md]([local file: trace.md:1]) with the biology bundle, count-table, Parquet profile, and same-experiment comparator evidence behind the call.
- [answer.txt]([local file: answer.txt:1]) with exactly the requested TSV:

```tsv
target_name	predicted_n_degs
Sos2	0
```

I also parsed `answer.txt` as TSV and verified it has the single `Sos2` row with a non-negative integer prediction.