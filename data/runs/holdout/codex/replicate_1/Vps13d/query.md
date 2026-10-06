Done. I wrote the direct forecast artifacts:

- [trace.md]([local file: trace.md:1]) with the biology, training-count, corpus, and Parquet/profile evidence used for the call.
- [answer.txt]([local file: answer.txt:1]) with only:

```tsv
target_name	predicted_n_degs
Vps13d	3
```

I also validated that `answer.txt` has exactly the requested two TSV rows and that the prediction is a non-negative integer.