# Cep164 n_degs prediction trace

## Target and endpoint

- Target perturbation: `Cep164`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with Wilcoxon BH-adjusted `p < 0.05`
- Prediction: `0`

## Biology used

The canonical biology bundle marks `Cep164` as a distal-appendage/basal-body
component that supports ciliary docking and IFT recruitment or stabilization.
It is an installed structure at the P16 edit age, so a disruptive edit should
stop new supply before old distal-appendage/ciliary material has cleared. The
functional-stock adjudication nevertheless calls substantial depletion by the
P37-P44 harvest likely: post-ciliogenesis Cep164 loss in mouse photoreceptors
caused IFT loss and sensory-cilium deterioration on a 2-4 week clock. This is
positive evidence for reachability but only partial endpoint evidence because
the timing comes from high-flux photoreceptor cilia, not ordinary thalamic
primary cilia.

Exact in-assay reach was moderate rather than absent: in non-target nuclei from
`151 TH Prkcd Grin2c Glut`, `Cep164` was detected in 12,103 of 23,679 nuclei
with mean CP10K 0.487 and pseudobulk CPM 48.53. I treated this as sufficient
for editing to reach many recovered cells, while still allowing attenuation
from mosaic CRISPR, slower turnover of thalamic neuronal cilia, and
survivor-conditioned nuclear RNA sampling.

## Training measurements used

The focal count table contains 1,674 training perturbations for this same
thalamic class and is strongly zero-inflated: 1,205 are zero, the median is
zero, the 75th percentile is 1, and only 106 targets have at least 10 DEGs.
Thus the base rate already favors a null or near-null point unless the
biological analogs give a clear upward pull.

I used typed gene-analog nomination against that exact training universe rather
than selecting by symbol prefix. The strongest measured candidates were the
human one-to-one ortholog projections of curated CORUM complexes containing
CEP164, plus the nearest transition-fiber physical interactor:

| comparator | typed relation to Cep164 | `n_degs` |
| --- | --- | ---: |
| `Dzip1` | CEP164-DZIP1 CORUM complex; STRING physical interaction; ciliary transition fiber | 0 |
| `Sclt1` | CORUM distal-appendage complex; STRING physical interaction; ciliary transition fiber | 0 |
| `Cep290` | CORUM distal-appendage complex; ciliary transition zone / assembly | 0 |
| `Nin` | STRING physical interaction; ciliary transition fiber | 0 |

The next broad cilium/IFT/transition-zone comparators also stayed essentially
silent in the declared endpoint. Among the first 20 ciliary candidates
(`Dzip1`, `Sclt1`, `Cep290`, `Nin`, `Ift81`, `Ift88`, `Arl3`, `B9d1`,
`Ift43`, `Rpgrip1l`, `Bbs5`, `Ttc8`, `Cplane1`, `Rpgr`, `Kif3b`, `Iqcb1`,
`Alms1`, `Ttc21b`, `Dync2i1`, `Dync2h1`), 18 had `n_degs = 0` and the only
nonzero values were `Arl3 = 1` and `Ttc8 = 1`; the mean was 0.1 and the median
was 0. This outweighed later high-count broad-fallback genes such as `Ctnnb1`
or `Huwe1`, whose links were generic centrosome/cilium/protein-binding
annotations rather than specific distal-appendage comparators.

I also checked the declared expression Parquet for those same 20 candidates in
`151 TH Prkcd Grin2c Glut`. All 20 profiles were available. The profile
comparison reported 18 nodes with no significant features and 2 nodes with
1-9 significant features, matching the count table. A 20-node cohort diagnostic
over all 190 pairwise comparisons showed no recurrent positive significant
program overlap and only one negative significant-overlap row with coefficient
0, so the ciliary cohort did not hide a shared FDR-supported program beneath
the scalar counts.

## Synthesis

Cep164 is biologically active enough that a response is plausible, but its best
task-matched analogs indicate that perturbing ciliary distal-appendage and IFT
machinery usually produces zero detected DEGs in this thalamic population over
the assay window. The biology bundle's uncertainties all point toward further
attenuation relative to the severe photoreceptor literature phenotype:
ordinary thalamic primary cilia have lower renewal demand, the edit is mosaic,
and the assay observes recovered nuclei. I therefore placed Cep164 at the mode
of the closest measured ciliary cohort and predicted no FDR-significant genes.
