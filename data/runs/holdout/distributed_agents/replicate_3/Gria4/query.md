Done. I wrote both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The manifest contained a single held-out target, `Gria4`. I predicted:

```tsv
target_name	predicted_n_degs
Gria4	0
```

I also validated that `answer.txt` is only one fenced `tsv` block, has the required header, contains exactly the requested target once, and preserves the manifest order.