# DEG-count prediction trace

## Question and endpoint

The run asks for one held-out perturbation, `Pdhx`, and a point prediction for
the number of genes that would satisfy `pvals_adj < 0.05` in `151 TH Prkcd
Grin2c Glut` cells after sparse postnatal AAV-CRISPR loss of function.

I treated the focal training CSV as a directly observed count of that endpoint
for non-held-out perturbations. I treated the Parquet rows for the same focal
class as the direct per-gene Wilcoxon evidence from which those counts are
derived. `Pdhx` was completely held out, so no `Pdhx` knockout signature was
available; the prediction is therefore a transfer from same-experiment
perturbations of PDH-complex and nearby mitochondrial-carbon genes, interpreted
with external knowledge of the PDH complex.

## Sources

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact focal-cell
  training endpoint for 1,674 non-held-out perturbations.
- `training_de_all_cell_groups.parquet`: exact focal differential-expression
  rows, inspected for biologically relevant PDH/TCA analog perturbations.
- Held-out manifest `b0268.csv`: confirmed that this run requests only `Pdhx`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`
  Findings and Evidence records for `Dlat`, `Dld`, `Dlst`, `Ogdh`, and
  `Pdha1`, used only as bounded mechanistic summaries over the same experiment.
- External mechanism references:
  - Reactome, "PDH complex synthesizes acetyl-CoA from PYR", stable identifier
    `R-HSA-9861559`, reviewed 2024.
  - Ganetzky, McCormick, and Falk 2021, *GeneReviews*, "Primary Pyruvate
    Dehydrogenase Complex Deficiency Overview", NCBI Bookshelf NBK571223.
  - Patel, Nemeria, Furey, and Jordan 2014, *J. Biol. Chem.*,
    DOI `10.1074/jbc.R114.563148`, PMID `24798336`.
  - Hiromasa et al. 2003, *J. Biol. Chem.*, DOI
    `10.1074/jbc.M308172200`, PMID `14638692`.
  - Brautigam et al. 2006, *Structure*, DOI
    `10.1016/j.str.2006.01.001`, PMID `16442803`.
  - Brown, Head, and Brown 2002, *Human Genetics*, DOI
    `10.1007/s00439-001-0665-3`, PMID `11935326`; and Brown et al. 2006,
    *Developmental Medicine & Child Neurology*, DOI
    `10.1017/S0012162206001617`, PMID `16904023`.

## Quantitative calibration

The training endpoint is highly zero-inflated in this cell group: 1,205 of
1,674 perturbations had `n_degs = 0`, 276 had `n_degs = 1`, the median was 0,
the 90th percentile was 2, and the 95th percentile was 18. Large responses were
rare, so a held-out target needed a close same-experiment analog or a strong
external reason to escape the zero or singleton regime.

I then streamed the focal-cell Parquet row groups for represented PDC and
nearby carbon-metabolism genes and counted rows with `pvals_adj < 0.05`.
The central analog counts in `151 TH Prkcd Grin2c Glut` were:

| training perturbation | relationship to Pdhx/PDH | observed `n_degs` |
| --- | --- | ---: |
| `Dlat` | PDH E2 core component that associates with E3BP | 1 |
| `Pdha1` | PDH E1-alpha catalytic subunit | 1 |
| `Dld` | E3 enzyme used by PDH and other 2-oxoacid dehydrogenases | 0 |
| `Mpc1` | mitochondrial pyruvate import | 0 |
| `Dlst` | E2 component of the alpha-ketoglutarate dehydrogenase complex | 0 |
| `Ogdh` | E1 component of the alpha-ketoglutarate dehydrogenase complex | 0 |
| `Bckdhb` | branched-chain alpha-ketoacid dehydrogenase E1 beta | 0 |
| `Aco2` | TCA aconitase | 0 |
| `Sdha` | succinate dehydrogenase complex | 1 |
| `Idh3a` | mitochondrial NAD-IDH alpha | 1 |
| `Mdh2` | mitochondrial malate dehydrogenase | 1 |

The `Dlat` and `Pdha1` singleton counts were self-transcript rows, not shared
downstream PDH-program rows:

| perturbation | significant focal row at FDR 0.05 | log2 FC |
| --- | --- | ---: |
| `Dlat` | `Dlat` | -0.673 |
| `Pdha1` | `Pdha1` | -1.039 |

`Dld`, `Dlst`, `Ogdh`, `Mpc1`, `Bckdhb`, and `Suclg1` had no FDR 0.05 focal
rows. PDH/TCA perturbations also failed to induce canonical stress or pyruvate
handling transcripts in the focal class: `Atf4`, `Ddit3`, `Asns`, `Trib3`,
`Ppp1r15a`, `Hspa5`, `Xbp1`, `Hspd1`, `Hspe1`, `Sqstm1`, `Map1lc3b`, `Pdk1`,
`Pdk4`, `Ldha`, and `Slc16a1` all had `pvals_adj = 1.0` across the inspected
PDH/TCA analogs except subthreshold `Mdh1` rows. The same-experiment corpus
made the same point at a looser FDR 0.10 level: `Dlat` had only a borderline
`Jarid2`-down downstream signal in this class, and represented same-complex or
nearby metabolic perturbations did not phenocopy it; `Pdha1` had visible
self-transcript reduction in several groups without a coherent downstream PDH
or mitochondrial ISR module.

## Causal transfer to Pdhx

`Pdhx` encodes the mammalian PDH E3-binding protein. Reactome and Patel et al.
place E1, DLAT/E2, DLD/E3, and PDHX/E3BP in the mitochondrial pyruvate
dehydrogenase complex that converts pyruvate to acetyl-CoA. Hiromasa et al.
showed that E3BP substitutes into the mammalian E2/E3BP 60-mer core rather
than adding as a separate scaffold, and Brautigam et al. showed structurally
that E3BP recruits the E3 homodimer to the human PDC. Brown et al. established
that inherited PDHX defects cause primary PDH-complex deficiency, usually with
residual PDC activity and often a milder course than classical `PDHA1`
deficiency.

The intervention-to-endpoint chain I used was therefore:

`Pdhx` CRISPR loss -> reduced E3BP in the PDH core and weaker E3 recruitment ->
impaired but not necessarily abolished PDH flux -> possible pyruvate/lactate,
acetyl-CoA, redox, or stress changes in recovered neurons -> Wilcoxon DEG count
3 to 4 weeks after P16 mosaic perturbation.

That chain makes `Dlat` and `Pdha1` legitimate same-limiting-function analogs,
because each impairs the same PDC that `Pdhx` helps assemble. It does not make
`Mdh1` or unrelated high-yield perturbations good positive analogs, even when
they are mitochondrial or have more DEGs, because their focal signatures were
different and not specific to the E3BP recruitment step. The key
candidate-specific break is that PDHX loss removes the E3-binding component
rather than the E1 or E2 active site. Residual PDC activity in PDHX disease and
the lack of any broad same-experiment response after `Dlat`, `Pdha1`, or `Dld`
argue that this partial, mosaic perturbation should land below the threshold
for a robust nuclear stress or metabolic transcriptional program in recovered
thalamic Prkcd/Grin2c glutamatergic nuclei.

## Target-specific prediction

### Pdhx

The best endpoint-bearing in-dataset analogs were `Dlat` with 1 DEG and
`Pdha1` with 1 DEG; in both cases the sole FDR 0.05 row was the perturbed
transcript itself. `Dld` was a counterexample in the same enzymatic reaction:
although it is the E3 enzyme recruited by E3BP, its focal signature had 0 DEGs.
`Mpc1`, `Dlst`, `Ogdh`, `Aco2`, and `Bckdhb` showed that perturbing pyruvate
entry, alpha-ketoglutarate dehydrogenase, and related mitochondrial carbon
enzymes did not produce a shared focal stress signature in this assay.

Externally, `Pdhx` is unquestionably a PDH-complex gene, but it is the E3
recruitment/scaffold subunit, not the E1 or E2 catalytic subunit. The acute
postmitotic CRISPR experiment measured a sparse survivor-conditioned nuclear
RNA endpoint; it did not measure pyruvate flux, lactate, ATP, acetyl-CoA,
lipoylation, or PDC assembly. A biochemical effect could therefore be present
with no genes crossing FDR. Because the two closest held-in PDC catalytic
perturbations were self-only, because the shared E3 perturbation was null, and
because no canonical PDH-stress module appeared in the Parquet rows, I predict
that `Pdhx` will also be transcriptionally buffered at FDR 0.05.

Point prediction: **0 DEGs**.

## Limits

This is an extrapolation from neighboring PDC perturbations, not a direct
`Pdhx` measurement. The endpoint includes possible self-transcript loss, and
the training singleton counts for `Dlat`, `Pdha1`, `Idh3a`, and `Mdh2` were
self rows; I did not assume that `Pdhx` self RNA would be significant because
target-mRNA reduction is variable in this CRISPR/nuclear-RNA assay. The same
experiment shows that severe mitochondrial biochemistry can be missed by the
snRNA-seq DEG endpoint in recovered neurons, so the zero prediction means no
measured gene is expected to pass BH FDR 0.05, not that PDHX is dispensable or
that PDH flux is unchanged.
