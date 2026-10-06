Done. I wrote the direct forecast artifacts:

- [trace.md]([local file: trace.md:1]) with the biology, typed analog, focal count-table, and Parquet-row evidence that led to the number.
- [answer.txt]([local file: answer.txt:1]) containing only:

```tsv
target_name	predicted_n_degs
Nlgn1	1
```

I also mechanically validated that `answer.txt` has exactly the requested two-column TSV shape and a non-negative integer prediction.