Done. I created:

- [trace.md]([local file: trace.md])
- [answer.txt]([local file: answer.txt])

The held-out manifest only contained `Ccr5`, and the final point prediction is `0` DEGs. I based that on the same-assay focal-cell counts and DE signatures for the closest available chemokine and downstream inflammatory/signaling comparators: `Ccr2`, `Cxcr4`, `Rac1`, `Nfkb1`, `Rel`, `Mapk1`, `Pik3r1`, `Pik3cb`, IFN/STAT nodes, and TLR/cytokine receptors are flat in `151 TH Prkcd Grin2c Glut`, with only a `Stat1` self-hit among the core STAT analogs.

I also validated that `answer.txt` is exactly a single fenced `tsv` block with the required header and one `Ccr5	0` row, and that `trace.md` is present and ASCII-clean.