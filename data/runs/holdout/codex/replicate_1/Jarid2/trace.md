# Jarid2 151 TH Prkcd Grin2c Glut DEG-count forecast

## Target and endpoint

- Target: `Jarid2`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- I used the declared one-row `Jarid2` manifest, the Jarid2 canonical biology bundle, the focal training count table, and 151-filtered rows from the declared training DE parquet. The Parquet/profile rows and packaged Findings are same-experiment views, so agreement between them was treated as interpretation of one Perturb-seq experiment rather than replication.

## Evidence used

### Jarid2 biology bundle

- Exact target reach is not limiting: `Jarid2` is measured in the focal non-targeting nuclei, with 19,761/23,679 nuclei expressing it, 83.45% expressing, mean raw UMI 2.118, mean CP10K 1.337, and pseudobulk CPM 132.75 in `151 TH Prkcd Grin2c Glut`.
- Functional-stock adjudication calls the P16 disruptive edit likely to reach only a partial or leading-edge Jarid2 deficit by P37-P44. The rationale is that the edit stops new JARID2 synthesis, most thalamic proteins are probably renewed within 21-28 days, and JARID2/PRC2.2 chromatin occupancy is renewable; however, pre-existing H3K27me3-marked locus states can persist and MTF2-linked PRC2 recruitment can preserve part of the function.
- The strongest matched biology is developmental: mouse germline disruption causes embryonic lethality with incompletely penetrant neural-tube defects, and conditional retinal-progenitor loss alters temporal identity and H3K27me3. No post-P16 thalamic-neuron timing measurement for JARID2 protein, PRC2.2 residence, or chromatin-state clearance was found.

Interpretation: the target is present and there is a plausible route to a transcriptional response, but it should be weaker and more delayed than complete acute loss of a core RNA-processing or chromatin-maintenance factor.

### Focal training counts

The declared `151 TH Prkcd Grin2c Glut` count table contains 1,674 training perturbations:

| count class | perturbations |
| --- | ---: |
| `n_degs = 0` | 1,205 |
| `n_degs > 0` | 469 |
| `n_degs >= 10` | 106 |
| `n_degs >= 50` | 59 |
| `n_degs >= 100` | 43 |

Jarid2 is therefore in a very sparse response regime, even for a high-yield cell class.

Closest counted genes were not exact PRC2-core matches: `Eed`, `Ezh1`, `Ezh2`, `Suz12`, `Aebp2`, `Mtf2`, `Phf1`, and `Phf19` were absent from this training count table. The observed focal counts for chromatin regulators that were present were highly heterogeneous:

| comparator | `n_degs` | role in the forecast |
| --- | ---: | --- |
| `Kdm6b` | 0 | H3K27me3-opposing enzyme; boundary that Polycomb/H3K27 relevance alone was insufficient |
| `Dnmt3a` | 0 | chromatin/DNA-methylation boundary |
| `Smarca4` | 0 | same-family core chromatin boundary with no detectable 151 response |
| `Smarca2` | 1 | same-family chromatin boundary with minimal 151 response |
| `Mga` | 2 | ncPRC1.6-associated Polycomb-adjacent boundary |
| `Mecp2` | 16 | low but nonzero chromatin/neurodevelopmental response |
| `Setdb1` | 22 | low-tens chromatin response |
| `Kmt2a` | 24 | low-tens histone-methylation response |
| `Arid1a` | 22 | accessory mSWI/SNF response |
| `Arid2` | 56 | PBAF-specific mSWI/SNF response |
| `Chd4` | 100 | stronger NuRD chromatin-remodeler response |
| `Setd1a` | 368 | high H3K4-methyltransferase-complex response |
| `Brd4` | 311 | broad chromatin/transcription response |
| `Yy1` | 720 | broad, pleiotropic transcriptional/chromatin response |

The broad high-count examples show that postmitotic thalamic neurons can give large chromatin-factor signatures, but the PRC-adjacent and accessory examples put more probability in the 0-60 range than in the hundreds for Jarid2.

### Same-experiment Findings and profile comparisons

Packaged Findings for training genes supported the count-table heterogeneity rather than a generic chromatin module. For example, `Arid1a` converged with a restricted cBAF-axis module while related `Smarca2`, `Smarca4`, `Smarcc1`, `Smarcd1`, and `Arid2` did not broadly phenocopy it; `Arid2` itself produced a separate 151-restricted PBAF-like response; and `Brd4` had a broad posterior-enriched response. Those Findings are useful for mechanism labels but are derived from the same experiment as the counts.

I also compared 151 profiles for 16 chromatin or transcription-regulatory training perturbations (`Setd1a`, `Chd4`, `Kmt2a`, `Mga`, `Dnmt3a`, `Kdm6b`, `Smarca4`, `Smarca2`, `Setdb1`, `Mecp2`, `Arid1a`, `Arid2`, `Chd8`, `Brd4`, `Yy1`, `Ctcf`) using the declared training parquet and Wilcoxon scores. The diagnostic found all 16 profiles and showed weak cohesion:

- across all 120 selected pairs, median positive-tail overlap was 0.030 and median negative-tail overlap was 0.035;
- among focal nodes, observed DEG counts exactly matched the count table: `Setd1a` 368, `Chd4` 100, `Kmt2a` 24, `Mga` 2, and `Dnmt3a` 0;
- pairwise similarities between the moderate focal nodes and high pleiotropic peers were shallow or inconsistent, so I did not use `Setd1a`, `Brd4`, or `Yy1` as direct quantitative stand-ins.

## Synthesis

I predict a real but small-to-moderate 151 signature. Jarid2 has broad in-assay expression and a PRC2.2 recruitment function that should begin to turn over in the 21-28 day window, which argues against simply using the screen-wide zero median. The developmental nature of the strongest neural Jarid2 evidence, persistence of already-installed chromatin states, and partial MTF2/PRC2.1 buffering argue against the hundred-gene chromatin outliers. With no exact PRC2-core training comparator and with Polycomb-adjacent `Mga`/`Kdm6b` lying at 2 and 0, the most defensible point is near the low-tens chromatin responders (`Arid1a`, `Setdb1`, `Kmt2a`) rather than the larger `Chd4`/`Setd1a`/`Brd4` responses.

Point forecast: `Jarid2` will have **24** BH-significant DEGs in `151 TH Prkcd Grin2c Glut`.
