Done. I created both required outputs in the run directory:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

I predicted `Psmc5` as a broad nonzero 26S proteasome perturbation and set the point estimate to `560` DEGs, anchored on the two direct structural-proteasome training hits in `151 TH Prkcd Grin2c Glut`: `Psmc1` with `430` DEGs and `Psmb4` with `742` DEGs.

I also validated that `answer.txt` contains exactly one `tsv` fenced block, exactly the requested target in order, no duplicate rows, and a single non-negative integer prediction.