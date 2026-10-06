Done. I wrote:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

`answer.txt` contains exactly:

```tsv
target_name	predicted_n_degs
Fnip1	1
```

I also generated bounded profile evidence under `./evidence/` for the 12 selected FLCN/FNIP-adjacent, mTOR/AMPK, and Hsp90/chaperone training perturbations, and validated that the final answer TSV is two rows with the expected header and a non-negative integer prediction.