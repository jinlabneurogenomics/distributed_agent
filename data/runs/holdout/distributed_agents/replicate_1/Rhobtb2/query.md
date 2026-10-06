Created the two required outputs in the run directory:

- [trace.md](./trace.md)
- [answer.txt](./answer.txt)

I predicted `Rhobtb2` as `0` DEGs in `151 TH Prkcd Grin2c Glut`, based on:

- The focal training distribution being zero-inflated: median `0`, 1,205/1,674 training perturbations at `0`, and the 90th percentile only `2`.
- Focused Parquet checks showing the nearest visible BTB/KCTD/KLHL adaptor perturbations are focal-null or tiny:
  `Btbd9=0`, `Kctd1=2`, `Kctd8=0`, `Kctd16=0`, `Klhl7=0`, `Klhl20=0`.
- Focused small-GTPase/Rho-neighborhood checks showing the same:
  `Cdc42=1`, `Rac1=0`, `Rala=0`, `Rapgef2=0`, `Rapgef4=0`, `Arhgap18=0`, `Arhgap32=0`, `Arhgef9=1`.
- The July 260713 sourceguard PerturbAI corpus indicating those visible BTB and Rho/Rac/Cdc42/Ral perturbations did not form a broad shared survivor-state nuclear RNA program.
- External `RHOBTB2` literature supporting neuronal relevance but making BTB-domain missense stabilization and fly overexpression stronger models than acute P16 mosaic CRISPR loss of function.

I validated `answer.txt` mechanically against the requested-target CSV:

- single fenced `tsv` block
- exact header
- `1` data row for `1` requested target
- target order preserved
- no duplicate targets
- integer non-negative prediction