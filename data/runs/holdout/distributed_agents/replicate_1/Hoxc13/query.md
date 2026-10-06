Created both required outputs in the working run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

The prediction is:

```tsv
target_name	predicted_n_degs
Hoxc13	0
```

I based the zero call on the supplied focal training counts and direct Parquet queries: all represented Hox-family perturbations in `151 TH Prkcd Grin2c Glut` had `n_degs = 0`, the Pbx/Meis and retinoic-acid comparators were also focal zeros, and the Dlx3/Hoxc13/Foxn1 hair-follicle program was absent from the postnatal neuronal DE surface. External Hoxc13 literature supported treating the known Hoxc13 biology as hair/nail/keratinized-ectoderm specific rather than as a thalamic juvenile neuronal maintenance program.

I also mechanically validated `answer.txt`: it is a single fenced `tsv` block, has the exact required header, contains exactly one row, preserves the requested target order, has no duplicate or extra targets, and uses a non-negative integer prediction.