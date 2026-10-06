Done: I wrote the direct SDHB forecast artifacts.

- [trace.md]([local file: trace.md:1]) records the biology and training-measurement reasoning that led to a **1 DEG** point forecast.
- [answer.txt]([local file: answer.txt:1]) contains only:

```tsv
target_name	predicted_n_degs
Sdhb	1
```

I also validated that `answer.txt` has exactly two rows, the expected TSV header, the exact manifest target `Sdhb`, and a non-negative integer prediction.