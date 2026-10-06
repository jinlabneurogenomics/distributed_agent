# DEG-count prediction trace

## Question and endpoint

The requested prediction is the integer number of genes with `pvals_adj < 0.05`
in `151 TH Prkcd Grin2c Glut` cells after a held-out `Gbf1` perturbation. The
held-out target itself has no rows in the training count table or in
`training_de_all_cell_groups.parquet`, so I treated the training file as direct
endpoint measurements only for non-held-out analog perturbations. I did not
interpret the absent held-out rows as a zero.

The readout is a survivor-conditioned snRNA-seq DEG count from P16-to-P37/44
acute mosaic AAV CRISPR loss of function in NeuN-positive postmitotic neurons.
It is a response-breadth endpoint, not a direct assay of editing efficiency,
viability, Golgi traffic, or organelle morphology.

## Sources used

- Declared focal training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Gbf1`.
- Internal same-experiment corpus: PerturbAI July 260713 sourceguard 1773 v1
  ledgers and bounded reports, used only as packaged interpretation of the
  same Perturb-seq experiment, not as independent replication.
- External literature from PubMed:
  Zhao et al. 2006, J Cell Sci, DOI 10.1242/jcs.03173, PMID 16926190;
  Jackson 2014, Cell Logist, DOI 10.4161/21592780.2014.943616, PMID 25610717;
  Takashima et al. 2011, Cell Struct Funct, DOI 10.1247/csf.11035, PMID
  22185782; Pocognoni et al. 2018, Am J Physiol Cell Physiol, DOI
  10.1152/ajpcell.00221.2017, PMID 29443553; Zou et al. 2021, Microsc
  Microanal, DOI 10.1017/S1431927620024885, PMID 33478608.

## Dataset checks and computations

The requested manifest contained one unique target, `Gbf1`. The focal training
count table contained 1,674 unique non-held-out perturbations, had median 0 and
mean 14.1 DEGs, and was highly zero-inflated: 469/1,674 perturbations had a
nonzero focal DEG count. `Gbf1` was not in that CSV, and a PyArrow filtered
scan of the training Parquet found 0 rows with `gene_target == "Gbf1"`.

I then filtered the count table for the direct ER-Golgi/COPI neighborhood of
GBF1 and for nearby counterexample pathways. Training targets on the exact
GBF1-ARF axis were sparse: no `Arf*` target and no ARFGEF paralog were present
as focal training perturbations. The represented early secretory comparators
were:

| comparator | focal `n_degs` | why it was used |
|---|---:|---|
| `Copa` | 0 | alpha-COP, a core COPI subunit downstream of GBF1/ARF activation |
| `Copg1` | 1 | gamma1-COP, the other assayed core COPI subunit |
| `Sec23a` | 0 | COPII coat component for ER export, upstream of COPI-mediated ERGIC/Golgi maturation |
| `Sar1b` | 0 | COPII initiation GTPase |
| `Cog4` | 0 | conserved oligomeric Golgi tethering complex |
| `Cog5` | 0 | conserved oligomeric Golgi tethering complex |
| `Stx5a` | 0 | Golgi/ER traffic SNARE target represented in training |
| `Stx16` | 1 | TGN-endosomal SNARE; one self-transcript hit only in the focal table |
| `Rab18` | 0 | ER/lipid-droplet Rab adjacent to organelle traffic rather than a COPI member |
| `Rab27a` | 0 | secretory Rab counterexample |
| `Rab3gap1` | 0 | vesicle Rab regulator counterexample |
| `Rab3gap2` | 0 | vesicle Rab regulator counterexample |
| `Rab7` | 501 | late-endosomal/lysosomal positive counterexample, not a COPI phenocopy |
| `Sec63` | 11 | ER translocon/UPR positive counterexample, not a COPI phenocopy |

For the closest analogs I queried the Parquet for
`group_name == "151 TH Prkcd Grin2c Glut"` and those `gene_target` values, then
examined the smallest adjusted p-values. The count-table zeros were supported
by flat focal signatures rather than many near-threshold hits: `Copa` had 75
perturbed nuclei and best adjusted p=0.364; `Cog4` had 80 and all adjusted
p-values equal to 1; `Cog5` had 169 and best adjusted p=0.377; `Sar1b` had 112
and best adjusted p=0.108 for its own transcript; `Sec23a` had 307 and best
adjusted p=0.874 for its own transcript; `Stx5a` had 113 and all adjusted
p-values equal to 1. `Copg1` had 234 focal nuclei and exactly one focal
FDR<0.05 gene, `Copg1` itself (logFC -0.668, adjusted p=9.24e-17), with no
secondary gene approaching significance.

## Gbf1-specific reasoning

GBF1 is the cis-Golgi/ERGIC Sec7 guanine-nucleotide exchange factor that
activates ARFs for early secretory COPI recruitment. Zhao et al. showed that
GBF1 localizes dynamically to cis-Golgi and peripheral vesicular tubular
clusters and that blocking GBF1 dissociates COPI from these membranes. Jackson
separates the secretory ARF-GEFs by site: GBF1 first activates ARF1 at the
cis-Golgi, whereas BIG1/BIG2 act later at the trans-Golgi/TGN for AP-1/GGA
coats. Pocognoni et al. further showed that GBF1 Golgi targeting is required
for ARF activation, COPI recruitment, secretion, and cell viability in a
replacement assay. Those data make COPI components, rather than late endosomal
Rabs, the most direct training analogs.

The causal transfer chain for `Gbf1` is:

`Gbf1` indel perturbation -> reduced GBF1 protein/activity at the cis-Golgi and
ERGIC -> weaker local ARF activation and impaired COPI-dependent retrograde or
Golgi trafficking -> potential ER/Golgi lipid or client stress in exposed,
surviving neurons -> FDR-detectable nuclear RNA response in recovered
`151 TH Prkcd Grin2c Glut` nuclei.

The same limiting function was directly challenged by `Copa` and `Copg1`
perturbations in the training set. Both impair COPI, which should be downstream
of GBF1 in the same direction if partial early secretory failure were enough to
create a broad stress transcriptome. Instead `Copa` had 0 focal DEGs, and the
same-experiment PerturbAI corpus classified `Copa` as strict whole-surface
buffered/null: 21 recovered NeuN+ cell groups had no downstream genes even at
FDR<0.10. The corpus also reported that `Copg1` did not recover canonical
COPI-failure outputs: the only represented same-coatomer comparator, `Copa`,
was flat, and prespecified ER-stress/UPR/ISR and STING/type-I-IFN panels were
absent. In the focal count endpoint `Copg1` contributed only one DEG, its own
transcript, which is not evidence for a propagated GBF1/COPI state.

The ER-Golgi counterexamples did not argue for a hidden strong `Gbf1`
signature. `Sec23a` and `Sar1b`, representing COPII export into the same early
secretory route, were both zero in 151 TH Prkcd Grin2c Glut; the internal
corpus explicitly summarized `Sec23a` as producing no adjusted downstream
response in any measured neuronal group and as failing to induce the
UPR/ERAD marker program. `Cog4`, `Cog5`, and `Stx5a` were also focal zeros.
`Sec63` and `Rab7` show that the assay can see ER-client and lysosomal stress
when they are transcriptionally engaged in this cell group, but they act
through different limiting functions. In this dataset `Rab7` produced a large
late-endosomal/lysosomal, sterol, UPR/ISR, autophagy, and proteasome recovery
program; that is a downstream catabolic stress state, not a demonstrated
phenocopy of cis-Golgi ARF-GEF loss. `Sec63` produced only 11 focal DEGs at
the stricter q<0.05 endpoint and works at ER translocation rather than COPI
coat recruitment.

The external evidence that GBF1 depletion can affect organelles and lipid
handling was treated as a weak positive prior, not as an endpoint override.
Takashima et al. found increased lipid droplets after siRNA depletion of GBF1,
Arf4/Arf5, beta-COP, and ArfGAP1-3 in cultured cells, tying GBF1 to the same
COPI-dependent Golgi-to-ER/lipid homeostasis axis. Zou et al. found that loss
of GBF1 activity in mouse oocytes altered Golgi, ER, and mitochondrial
dynamics and increased the ER-stress marker GRP78. Those studies used stronger
non-neuronal cultured or oocyte perturbations and phenotypic organelle assays;
they do not establish that sparse P16 neuronal `Gbf1` CRISPR will create a
large survivor nuclear DEG burden when the assayed COPI subunits were flat.

Balancing these pieces, the most defensible prediction is no gene crossing the
FDR<0.05 threshold. A tiny one-gene self-transcript event like `Copg1` is
possible, but the held-out endpoint should be an integer count and the closest
coatomer analog `Copa` had zero. I therefore assign:

| target_name | predicted_n_degs |
|---|---:|
| `Gbf1` | 0 |

## Limits

- The training set lacks direct `Arf1`, `Arf4`, `Arf5`, `Arfgap1-3`,
  `Arfgef1`, and `Arfgef2` perturbations, so the strongest comparison is to
  COPI coat subunits rather than to an ARF or ARFGEF paralog.
- DNA indels and GBF1 protein loss were not measured. As instructed, I did not
  use weak self-transcript depletion in analogs to infer failed editing.
- The prediction transfers from surviving `Copa` and `Copg1` CRISPR neurons.
  Complete GBF1 inhibition or loss could be more severe and could deplete cells
  before snRNA recovery; such earlier selection would not necessarily produce
  a large survivor-conditioned DEG count.
- External GBF1 studies often use cell lines, oocytes, siRNA, antibodies, or
  pharmacological brefeldin-A/Golgicide-style inhibition. Those are mechanistic
  priors for the early secretory pathway, not direct calibrators of this P16
  sparse neuronal CRISPR DEG-count endpoint.
