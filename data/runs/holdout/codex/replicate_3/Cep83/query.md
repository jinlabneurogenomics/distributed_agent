Done. I wrote the direct forecast artifacts:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

`answer.txt` is formatted as the requested two-column TSV and predicts:

```tsv
target_name	predicted_n_degs
Cep83	0
```

I also verified the TSV shape: exactly two tab-separated columns, exactly the `Cep83` row, and a non-negative integer prediction.