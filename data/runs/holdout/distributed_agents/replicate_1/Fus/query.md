Created both requested outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Fus` as a nonzero, intermediate RNA-binding-protein response in `151 TH Prkcd Grin2c Glut`, closest to the visible `Tardbp` / `Matr3` / `Hnrnpc` tier and below `Hnrnpu` or the core-spliceosome perturbations:

```tsv
target_name	predicted_n_degs
Fus	180
```

I also mechanically checked that `answer.txt` is exactly one fenced `tsv` block, has the required two columns, contains exactly one row, preserves the requested `Fus` order and spelling, has no duplicate targets, and uses a non-negative integer prediction.