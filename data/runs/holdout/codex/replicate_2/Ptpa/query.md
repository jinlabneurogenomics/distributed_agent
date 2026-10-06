Done. I wrote the direct forecast artifacts:

- [trace.md]([local file: trace.md]) with the Ptpa biology, same-class PTP/Src training-count evidence, corpus boundaries, and focal-class profile checks that determined the forecast.
- [answer.txt]([local file: answer.txt]) containing exactly:

```tsv
target_name	predicted_n_degs
Ptpa	0
```

I also mechanically validated `answer.txt`: 2 tab-separated rows, exact header `target_name	predicted_n_degs`, target `Ptpa`, and a non-negative integer prediction.