# Pex13 prediction trace

## Question and endpoint

I interpreted the task as a point prediction for the held-out perturbation `Pex13` in `151 TH Prkcd Grin2c Glut` neurons.  The endpoint is the total number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after CRISPR loss of function, including the target transcript itself if it passes FDR.  The requested target was absent as a `gene_target` from the supplied differential-expression parquet and absent from the focal training-count CSV, so all evidence below comes from non-held-out perturbations and outside knowledge of PEX13.

Two ambiguities mattered.

- The same-experiment Distributed Agents corpus often summarizes "downstream" signatures at `FDR < 0.10`, excluding the perturbed transcript.  I used those summaries to understand biology, then checked the raw parquet at the task's exact `FDR < 0.05` threshold and counted the self-transcript when present.
- Weak or absent target-RNA reduction is not failed editing in this AAV-CRISPR assay.  I therefore used self rows only for the arithmetic endpoint, not as evidence that a perturbation worked or failed.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, the direct training endpoint for the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`, queried for exact focal rows and sentinel genes for the relevant peroxisome perturbations.
- `[local file: 175_Pex13.csv]`, which contains the single held-out target `Pex13`.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`, especially target-centered reports for `Pex14`, `Pex1`, `Abcd3`, `Acbd5`, `Agps`, `Far1`, and `Hsd17b4`.
- External gene-function evidence from PubMed and NCBI Gene:
  - Krause et al. 2013, Human Molecular Genetics, DOI 10.1093/hmg/ddt238: PEX13 homooligomerization is needed for PTS1 matrix-protein import, and PEX13 interacts with PEX14 at the peroxisomal membrane.
  - Dias et al. 2017, Journal of Biological Chemistry, DOI 10.1074/jbc.M117.805044: PEX5 enters the PEX docking/translocation module and interacts with PEX14 during peroxisomal matrix-protein import.
  - Mueller et al. 2010, Disease Models and Mechanisms, DOI 10.1242/dmm.004622: brain-restricted Pex13 deficiency in mice causes developmental cerebellar defects, reactive gliosis, oxidative stress, and early postnatal lethality.
  - Lee et al. 2016, EMBO Reports, DOI 10.15252/embr.201642443: PEX13 has a selective autophagy/mitophagy function separable from PEX14 and PEX19 in cultured cells.
  - Borgia et al. 2022, Orphanet Journal of Rare Diseases, DOI 10.1186/s13023-022-02415-5: biallelic human PEX13 variants cause Zellweger-spectrum disease and can disturb the PEX13/PEX14 translocation module.
  - NCBI Gene, Mus musculus `Pex13`, accessed 2026-09-23, as a database check that Pex13 encodes peroxisomal biogenesis factor 13.

## Computation over the supplied data

I first loaded the held-out manifest and found exactly one requested target, `Pex13`.

I then scanned the focal training-count CSV for peroxisome targets.  The directly represented analogs had very small focal counts:

| training perturbation | focal `n_degs`, FDR 0.05 |
|---|---:|
| `Pex14` | 1 |
| `Pex1` | 0 |
| `Abcd3` | 0 |
| `Acbd5` | 0 |
| `Hsd17b4` | 0 |
| `Agps` | 1 |
| `Far1` | 2 |

I queried the parquet for `151 TH Prkcd Grin2c Glut` rows for these genes and inspected both significant rows and expected peroxisome/stress sentinels.  The key exact focal observations were:

| perturbation | matched perturbed nuclei | exact focal evidence |
|---|---:|---|
| `Pex14` | 187 | one FDR 0.05 row, and it was `Pex14` itself, logFC -0.907, `pvals_adj = 3.74e-7`; the best downstream row was `Hspa4l`, `pvals_adj = 0.382` |
| `Pex1` | 110 | 0 FDR rows; `Pex1` self logFC -0.346, `pvals_adj = 1.0` |
| `Abcd3` | 163 | 0 FDR rows; `Abcd3` self logFC -0.409, `pvals_adj = 1.0` |
| `Acbd5` | 160 | 0 FDR rows; best downstream `Tpd52l1`, `pvals_adj = 0.456`; `Acbd5` self `pvals_adj = 1.0` |
| `Hsd17b4` | 140 | 0 FDR rows; every focal row had `pvals_adj = 1.0`, including `Hsd17b4` itself |
| `Agps` | 151 | one FDR 0.05 downstream row, `Dhcr24` up with logFC 0.660 and `pvals_adj = 0.00192`; `Cyp51` and `Lmtk3` were only FDR 0.10-level; `Agps` self was not significant |
| `Far1` | 152 | two FDR 0.05 rows: `Far1` self, logFC -0.438, `pvals_adj = 0.00313`, and `Tial1` up, `pvals_adj = 0.0243` |

The targeted sentinel check showed no compensatory PEX import or stress module in the closest focal contrasts.  In the `Pex14` focal contrast, for example, `Pex13`, `Pex5`, `Pex6`, `Pex16`, `Pex19`, `Pex26`, `Abcd3`, `Acbd5`, `Agps`, `Hsd17b4`, `Hspa5`, `Atf4`, `Ddit3`, `Dhcr24`, `Sqle`, `Insig1`, and `Tial1` all had `pvals_adj = 1.0` except for subthreshold `Dhcr24` with `pvals_adj = 0.517`.  In the `Pex1` focal contrast, `Dhcr24` had nominal `p = 0.00329` but still `pvals_adj = 1.0`, and the PEX/import/stress genes were flat.

## Target-specific reasoning

### `Pex13`

`Pex13` is a peroxisomal membrane peroxin in the matrix-protein import machinery.  It is mechanistically closest to the PEX docking/translocation module rather than to the downstream lipid enzymes: PEX13 self-associates and functions with PEX14 in PTS1 import, while PEX5 delivers cargo into that PEX14-containing docking/translocation assembly (Krause et al. 2013; Dias et al. 2017).  Human PEX13 variants cause Zellweger-spectrum disorders and can compromise the PEX13/PEX14 module (Borgia et al. 2022), so if the acute neuronal screen had shown a PEX14-like downstream stress response, `Pex13` would be a natural candidate to share it.

The dataset did not show such a response.  The most direct non-held-out PEX import analog, `Pex14`, had no downstream FDR 0.05 or FDR 0.10 gene in the focal cell group; its focal count of 1 came entirely from the `Pex14` self-transcript.  `Pex1`, an AAA peroxin that recycles the ubiquitinated PEX5 receptor rather than forming the docking pore, was also focal-zero.  Across the same-experiment corpus, `Pex1` produced only two singleton downstream FDR 0.10 events in other classes, and `Pex14` was downstream-flat across all 23 measured neuronal classes.  The corpus' higher-order peroxisome claim grouped `Abcd3`, `Acbd5`, `Agps`, `Far1`, `Hsd17b4`, `Pex1`, and `Pex14` and concluded that represented peroxisome-linked perturbations do not converge on a shared acute neuronal transcriptomic module.

The lipid-pathway comparators are informative counterexamples, not positive analogs.  `Agps` gave a tiny `151 TH Prkcd Grin2c Glut` sterol response through `Dhcr24` at FDR 0.05 and `Cyp51`/`Lmtk3` at FDR 0.10, and `Far1` had a self-plus-`Tial1` focal signature.  Distributed Agents explicitly interpreted both as node-specific ether-lipid/sterol events not reproduced by `Pex1`, `Pex14`, `Hsd17b4`, `Abcd3`, or `Acbd5`.  Since `Pex13` is an import/docking peroxin, the better analogy is the flat `Pex14`/`Pex1` side, not the `Agps` or `Far1` sterol branch.

External biology leaves open a unique `Pex13` effect: brain Pex13 deficiency in mice is damaging in developmental conditional models, and PEX13 has been implicated in mitophagy in cultured cells, unlike PEX14 (Mueller et al. 2010; Lee et al. 2016).  I did not upweight that to a broad DEG prediction because those studies assay embryonic/broad brain deletion, glial inflammation, cell culture autophagy, ROS, organelle localization, and lipid metabolism.  The training PEX and peroxisome perturbations show that, in the P16 sparse NeuN-positive postmitotic assay, even severe peroxisome-linked biology often fails to become a nuclear RNA program within recovered thalamic neurons over 3-4 weeks.

The remaining arithmetic question is whether the `Pex13` transcript itself will pass FDR, as `Pex14` and `Far1` did.  This is the least mechanistic part of the endpoint.  `Pex14` is evidence for a possible self-only count of one; `Pex1`, `Abcd3`, `Hsd17b4`, `Acbd5`, and `Agps` show that a visible self row is not guaranteed even for related peroxisomal genes.  Because the downstream prediction is zero and the self-transcript behavior of a held-out target is idiosyncratic in this CRISPR/snRNA design, I made the conservative point prediction:

`Pex13 -> 0`

## Limits and extrapolation

- `Pex13` itself has no same-experiment perturbation signature in the supplied inputs or in the Distributed Agents training corpus, so the prediction is an extrapolation from `Pex14`, `Pex1`, and broader peroxisome-pathway genes.
- The call is stronger for "no broad downstream program" than for "no self-transcript DEG".  A hidden `Pex13` self row passing FDR would turn the correct count from 0 to 1 without changing the biological interpretation.
- `Pex5`, `Pex6`, `Pex26`, `Pex3`, `Pex19`, `Pex2`, `Pex10`, and `Pex12` were not represented as focal training perturbations, so the closest docking/recycling/RING comparators are incomplete.
- The assay did not measure PEX13 protein, peroxisomal import, PEX5 ubiquitination, catalase localization, plasmalogens, very-long-chain fatty acids, mitophagy flux, ROS, or lipidomics.
- Brain-wide or germline Pex13 knockout phenotypes involve development, cerebellar lamination, glial activation, and organismal illness; those are imperfect analogs for sparse acute P16 editing in recovered NeuN-positive thalamic neurons.
