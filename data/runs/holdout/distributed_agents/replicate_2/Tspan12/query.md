Done. I created both required files:

- [trace.md]([local file: trace.md]): target-specific reasoning for `Tspan12`, including the focal training counts, filtered parquet checks, same-experiment Distributed Agents corpus evidence, and external Norrin/FZD4/LRP5/TSPAN12 citations.
- [answer.txt]([local file: answer.txt]): the strict single fenced `tsv` block.

I also validated that `answer.txt` is exactly one TSV code block, preserves the manifest order, includes only `Tspan12`, and uses a non-negative integer prediction:

```tsv
target_name	predicted_n_degs
Tspan12	0
```