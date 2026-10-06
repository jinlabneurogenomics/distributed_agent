Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The prediction is:

```tsv
target_name	predicted_n_degs
Satb1	0
```

I calibrated `Satb1` against the focal training distribution and relevant in-dataset analogs: `Satb2`, `Bcl11a`, `Bcl11b`, `Tbr1`, and `Foxp2` were all focal zeros, while nearby neuronal TF counterexamples such as `Sox5`, `Zbtb18`, `Cux2`, `Ski`, and `Mef2c` only reached 1-5 DEGs. I used `Chd4`, `Smarcc2`, and `Ctcf` as broader chromatin-regulator counterexamples showing that the focal group can produce large responses, but they looked mechanistically less appropriate than the quiet SATB/developmental-TF class.

I also validated [answer.txt]([local file: answer.txt]) for the strict format: exactly one fenced `tsv` block, one row, `Satb1` in manifest order, no duplicate targets, and an integer `predicted_n_degs`.