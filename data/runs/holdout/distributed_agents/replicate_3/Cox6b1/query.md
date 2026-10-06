Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

I predicted `Cox6b1` as `0` DEGs. The reasoning trace grounds that call in the focal-cell training counts for complex-IV and adjacent OXPHOS perturbations: `Cox4i1`, `Cox6a1`, `Cox7b`, `Cox8a`, `Cox11`, `Coa8`, and `Lrpprc` were all zero in `151 TH Prkcd Grin2c Glut`, while `Cox5a` and `Ndufa4` only reached one self-target DEG.

Verification passed: `answer.txt` contains exactly one fenced `tsv` block, exactly one row, `Cox6b1` in manifest order, and a non-negative integer prediction.