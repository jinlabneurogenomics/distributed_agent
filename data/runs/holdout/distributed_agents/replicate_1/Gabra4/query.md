Created the requested run-local outputs:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Gabra4` at `2` DEGs, based on the near-floor focal counts of represented GABA-A receptor subunits and the closer thalamic alpha4-beta2-delta relationship to `Gabrb2` and `Gabrd`, which had only 4 and 2 FDR<0.05 calls in `151 TH Prkcd Grin2c Glut`.

Verification passed: `answer.txt` is exactly one fenced `tsv` block, has the required header, contains one non-duplicate row, preserves the requested manifest order, uses exact target spelling, and has a nonnegative integer prediction.