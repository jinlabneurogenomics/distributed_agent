Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The requested manifest had a single held-out target, `Epb41l1`. I anchored the call on the same-experiment ankyrin/spectrin/adducin and AMPAR/PSD neighborhoods, checked their exact focal DEG counts and significant genes, treated `Grin1` as a detectable but mechanistically too-distant NMDAR-core boundary, and predicted:

```tsv
target_name	predicted_n_degs
Epb41l1	0
```

I also validated that `answer.txt` is exactly one fenced `tsv` block, preserves the manifest target order, has no duplicate targets, and contains a non-negative integer prediction.