# Dalrd3 n_degs forecast

## Target and endpoint

- Target: `Dalrd3`
- Population: `151 TH Prkcd Grin2c Glut`
- Endpoint to predict: measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- Direct training source: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Profile source used for selected analog checks: `training_de_all_cell_groups.parquet`

## Evidence used

The canonical `Dalrd3` biology bundle reports exact in-assay expression in this
cell group: 20,282 of 23,679 non-target nuclei expressed `Dalrd3`
(`85.65395498120698%`), with mean raw UMI `2.2757717809029097` and pseudobulk
CPM `142.63068767691584`. This supports reach in the requested thalamic
glutamatergic population, but the bundle explicitly treats expression as
context reach rather than a measure of edit efficiency.

The same bundle places DALRD3 in a narrow cytoplasmic tRNA-modification role:
DALRD3 targets selected arginine tRNAs to METTL2 for m3C32 modification.
Editing should stop new DALRD3 production while leaving residual targeting
protein and already modified tRNAs to decay. Generic brain-protein and
mammalian tRNA turnover proxies make substantial depletion by the 21-28 day
harvest plausible, but no mouse postnatal neural loss time course was found.
The functional-stock conclusion was therefore `likely_substantially_depleted`
with partial evidence completeness rather than a directly timed neuronal
phenotype.

The requested training count table is highly zero-inflated in `151 TH Prkcd
Grin2c Glut`: 1,205 of 1,674 visible perturbations had `n_degs = 0`, the median
was 0, the 75th percentile was 1, and only 106 had at least 10 DEGs. That
background made large values require a close observed high-yield analogue, not
just broad neurological relevance.

Training perturbations closest to the Dalrd3 operation split sharply:

| training target | direct `n_degs` |
| --- | ---: |
| Alkbh8 | 0 |
| Cdkal1 | 0 |
| Nsun2 | 0 |
| Trmt1 | 0 |
| Bdp1 | 8 |
| Polr3b | 8 |
| Eef2 | 9 |
| Nop56 | 25 |
| Elp2 | 150 |
| Elp1 | 645 |

Parquet checks on the exact `151 TH Prkcd Grin2c Glut` rows reproduced the
small or absent FDR<0.05 surfaces for the RNA/tRNA comparators (`Alkbh8` 0,
`Trmt1` 0, `Bdp1` 8, `Polr3b` 8) and the large Elongator branch (`Elp1` 645,
`Elp2` 150).

The packaged same-experiment corpus explains why I did not average Dalrd3 up to
the Elongator scale. Elp1 and Elp2 converge on a strong thalamic
ATF4/amino-acid stress program, but represented non-Elongator tRNA-modification
enzymes such as Alkbh8, Nsun2, Cdkal1, and Trmt1 are largely buffered or flat at
the basal neuronal mRNA level. Likewise, Polr3b is a sparse Pol III-associated
response and Bdp1 is a compact synthetase/CHOP response rather than a broad
Elongator phenocopy.

## Synthesis

The upward evidence is that `Dalrd3` is expressed in most nuclei in the focal
population and its installed tRNA modification should be at least partly
depleted over the screen window. The downward evidence is stronger for this
exact scalar: the direct operation is a selective METTL2 targeting step on two
arginine-tRNA substrates, DALRD3 knockout in human cells did not lower those
tRNAs' steady-state abundance, the bundle has no postnatal mouse neuronal
timing or phenotype, and the closest measured non-Elongator tRNA modifiers were
zero in the same thalamic class.

I therefore placed `Dalrd3` just above a hard null to reflect possible
detectable amino-acid/tRNA-pressure transcripts, but below the Bdp1/Polr3b/Eef2
8-9 DEG scale because there was no evidence for a general tRNA-production or
translation-elongation failure.

Point prediction: `1`
