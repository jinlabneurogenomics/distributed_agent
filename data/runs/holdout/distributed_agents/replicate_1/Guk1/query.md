Created the requested outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The final point prediction is:

```tsv
target_name	predicted_n_degs
Guk1	0
```

I based the zero call on the focal training-count distribution plus raw focal parquet checks for the closest available purine/nucleotide analogs:

- `Adk`: `n_degs = 0`, focal min adjusted P `0.202556`
- `Nt5c2`: `n_degs = 0`, focal min adjusted P `1.0`
- `Slc25a36`: `n_degs = 0`, all focal adjusted P values `1.0`
- `Slc25a4`: `n_degs = 1`, but the lone call was the `Slc25a4` self transcript, not a downstream nucleotide-stress program
- `Lyrm4`: `n_degs = 0`, focal min adjusted P `0.650782`, with only an isolated `Gmpr` off-focal hit in the same-experiment corpus

I also verified that `answer.txt` is exactly one fenced `tsv` block, has the required header, preserves the single requested target `Guk1`, contains one non-negative integer prediction, and has no duplicate or extra rows.