Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md:1]) with the dataset calibration, Gpr162 analog comparisons, same-experiment corpus context, PubMed-supported biology, and limitations.
- [answer.txt]([local file: answer.txt:1]) with the required single fenced TSV block.

I validated that `answer.txt` parses as fenced TSV, preserves the manifest order, contains exactly `Gpr162` once, and gives a non-negative integer prediction:

```tsv
target_name	predicted_n_degs
Gpr162	1
```