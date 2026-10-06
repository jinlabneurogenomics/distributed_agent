# Held-out target

## Question and interpretation

The requested held-out perturbation list contains one mouse target:

```text
Prokr2
```

I interpreted the endpoint as the exact assay endpoint used in the supplied training file: the number of measured genes with `pvals_adj < 0.05` after a Scanpy Wilcoxon test in `151 TH Prkcd Grin2c Glut` nuclei. `Prokr2` itself was completely held out as a perturbation target, so I did not use a Prokr2 DEG count or Prokr2 knockout signature. I used the non-held-out perturbations to calibrate whether comparable receptor and G-protein perturbations ever give a broad signature in this focal cell type.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: observed `n_degs` for the 1,674 non-held-out perturbations in `151 TH Prkcd Grin2c Glut`.
- `[local file: training_de_all_cell_groups.parquet]`: per-gene log2 fold changes and adjusted p-values for the same perturbations; I queried only the focal cell group and mechanistically relevant candidate targets/features.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`: queried `target_context(Prokr2)`. The corpus had no Claims, Findings, or explicit same-experiment references for `Prokr2`, so it did not supply Prokr2-specific internal neighbors.
- Distributed Agents runtime profile comparison MCP: compared a hand-selected cohort of Prokr2-relevant GPCR/G-protein/Fgfr1/Zbtb20 perturbations on focal-cell log-fold-change vectors.
- Public PubMed literature on PROKR2 biology:
  - Prosser, Bradley, and Caldwell 2007, "Olfactory bulb hypoplasia in Prokr2 null mice stems from defective neuronal progenitor migration and differentiation", DOI `10.1111/j.1460-9568.2007.05958.x`, PMID `18052978`.
  - Prosser et al. 2007, "Prokineticin receptor 2 (Prokr2) is essential for the regulation of circadian behavior by the suprachiasmatic nuclei", DOI `10.1073/pnas.0606884104`, PMID `17202262`.
  - Monnier et al. 2008, "PROKR2 missense mutations associated with Kallmann syndrome impair receptor signalling activity", DOI `10.1093/hmg/ddn318`, PMID `18826963`.
  - Sarfati, Dode, and Young 2010, "Kallmann syndrome caused by mutations in the PROK2 and PROKR2 genes", DOI `10.1159/000312698`, PMID `20389090`.
  - Qu et al. 2016, "Loss of ZBTB20 impairs circadian output and leads to unimodal behavioral rhythms", DOI `10.7554/eLife.17171`, PMID `27657167`.
  - Mohsen et al. 2017, "Sexually dimorphic distribution of Prokr2 neurons revealed by the Prokr2-Cre mouse model", DOI `10.1007/s00429-017-1456-5`, PMID `28616754`.
  - Zhao et al. 2018, "Prokineticins and their G protein-coupled receptors in health and disease", DOI `10.1016/bs.pmbts.2018.09.006`, PMID `30711026`.
  - Wen et al. 2019, "The PROK2/PROKR2 signaling pathway is required for the migration of most olfactory bulb interneurons", DOI `10.1002/cne.24719`, PMID `31132148`.
  - Yin et al. 2022, "Activation of amygdala prokineticin receptor 2 neurons drives the anorexigenic activity of the neuropeptide PK2", DOI `10.1016/j.jbc.2022.102814`, PMID `36539034`.

## Computation over the training data

The focal training endpoint was zero-heavy:

- `1,205 / 1,674` perturbations had `0` DEGs.
- The median was `0`; the 75th percentile was `1`; the 90th percentile was `2`.
- Very broad responses were rare and came from core cellular regulators such as `Uba5` (`2677`), `Tpr` (`1768`), `Sin3a` (`1433`), spliceosome/proteasome/nuclear transport genes, and chromatin factors.

I then queried the focal-cell rows of the parquet for Prokr2-relevant analogs and counted significant genes by target:

```python
f = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
)
sig = (sub.pvals_adj < 0.05).sum()
```

I also queried `names in {"Prokr2", "Prok1", "Prok2"}` across all 1,674 focal signatures. As measured genes, all three prokineticin-axis features had `pvals_adj = 1.0` in every non-held-out perturbation. Their scores were near zero despite occasional very large log-fold changes, the pattern expected from extremely sparse zero-inflated features rather than a stable focal-cell program. That argues against `Prokr2` itself becoming a reliable self-DEG in the held-out knockout.

The in-dataset perturbations I treated as mechanistic analogs or counterexamples were:

| training perturbation(s) | observed `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` | relevance to `Prokr2` |
| --- | ---: | --- | --- |
| `Gnao1` | 1 | The only significant feature was `Gnao1` itself (`logFC = -0.591`, `p_adj = 9.42e-7`). No other genes passed FDR. | Heterotrimeric G-protein alpha subunit. A proximal GPCR-signaling comparator showed only on-target RNA depletion, not a downstream state. |
| `Gnas`, `Gnb5` | 0, 0 | Neither had any FDR-significant feature. | Other proximal GPCR transduction components. Their null results make a large generic GPCR second-messenger response unlikely in this focal population. |
| Gq- or neuropeptide-linked GPCRs: `Htr2a`, `Htr2c`, `Chrm3`, `Grm5`, `Kiss1r`, `Tacr3`, `Avpr1a`, `Avpr1b`, `Crhr1`, `Ntsr1` | all 0 | The directly queried receptors had no significant features: for example `Kiss1r` had a minimum adjusted p-value of `0.759`, `Htr2a` had `0.890`, and `Htr2c`, `Chrm3`, `Grm5`, `Tacr3`, and `Ntsr1` bottomed out at `1.0` within their own signatures. | PROKR2 is a GPCR that can trigger calcium and other G-protein pathways. These are the closest available receptor-level counterexamples to a Prokr2 receptor knockout in postnatal neurons. |
| Gi/o-like neuropeptide or transmitter GPCRs: `Npy1r`, `Npy2r`, `Npy5r`, `Oprd1`, `Oprk1`, `Oprl1`, `Oprm1`, `Galr1`, `Cnr1` | all 0 except `Cnr1 = 1` | `Cnr1` had one significant feature, `Srcap`; the opioid, galanin, and NPY receptors had zero. | These broaden the receptor counterexample set beyond Gq-biased receptors; most assayed neuronal GPCR knockouts were transcriptionally silent. |
| `Gabbr1`, `Gabbr2`, `Gpr158` | 1, 1, 1 | `Gabbr1` and `Gpr158` each had the target transcript as the only clear significant feature (`Gabbr1 logFC = -0.602`, `p_adj = 1.54e-17`; `Gpr158 logFC = -0.991`, `p_adj = 3.39e-26`). | These show that the dataset can count a receptor perturbation as `1` when the receptor RNA itself is reliably knocked down, but they do not show a downstream receptor program. The measured `Prokr2` row did not look similarly detectable in this focal cell group. |
| `Plcb1`, `Prkca`, `Prkcg`, `Prkaca`, `Adcy1`, `Adcy3`, `Adcy5`, `Pde1c`, `Pde4b`, `Pde4d` | all 0 except `Prkaca = 1`, `Prkcg = 1` | No PLC/PKC/cAMP-pathway member produced more than a singleton response. | PROKR2 signaling can converge on calcium, cAMP, ERK, and related kinase pathways; these intracellular comparators were still essentially null. |
| Kallmann/PROKR2-associated developmental comparators `Fgfr1`, `Fgf1`, `Fgf12`, `Fgf13`, `Fgfr2`, `Fgfr3`, `Zbtb20` | `Fgfr1 = 0`, `Fgf1 = 0`, `Fgf12 = 0`, `Fgf13 = 2`, `Fgfr2 = 0`, `Fgfr3 = 0`, `Zbtb20 = 0` | `Fgfr1` and `Zbtb20` had no significant features; `Fgf13` had only two. | `FGFR1/FGF` signaling and `PROK2/PROKR2` are both implicated in olfactory/GnRH development, and `Zbtb20` regulates `Prokr2` in SCN circadian-output neurons. Their null focal signatures argue that this dataset is not capturing a developmental Kallmann-like program in this cell class. |
| Distal second-messenger genes `Calm1`, `Braf`, `Ntrk2` | 14, 4, 3 | These gave small but nonzero counts. | They are broad neuronal signaling hubs rather than Prokr2-specific receptor analogs; I used them as an upper-bound reminder that a signaling perturbation can occasionally make a few DEGs, but they were weaker analogs than the directly assayed GPCRs. |

The Distributed Agents profile comparison on `Gnao1`, `Gnas`, `Gnb5`, `Kiss1r`, `Tacr3`, `Htr2a`, `Htr2c`, `Chrm3`, `Grm5`, `Fgfr1`, `Zbtb20`, `Gpr158`, `Gabbr1`, and `Cnr1` classified 10 of 14 supplied profiles as having no significant features and 4 as having only 1 to 9. No pair shared a significant up- or down-regulated feature in the projected inspection table, reinforcing that this receptor/G-protein candidate set did not form a common downstream transcriptional module.

## Prokr2-specific biological reasoning

`Prokr2` encodes prokineticin receptor 2, a GPCR for the small secreted ligands PROK1 and PROK2. PROK2/PROKR2 signaling is biologically real and important: Prokr2-null mice have olfactory bulb hypoplasia and defective migration of olfactory bulb interneuron precursors (Prosser, Bradley, and Caldwell 2007; Wen et al. 2019), Prok2/Prokr2 loss causes Kallmann-like GnRH and olfactory phenotypes (Sarfati, Dode, and Young 2010; Zhao et al. 2018), and Prokr2 also contributes to SCN circadian output and amygdala control of feeding (Prosser et al. 2007; Yin et al. 2022). Disease-associated PROKR2 mutations impair receptor calcium/G-protein signaling in vitro (Monnier et al. 2008). `Zbtb20` can regulate `Prokr2` in SCN output neurons (Qu et al. 2016).

Those mechanisms do not map cleanly onto this readout. The strongest Prokr2 phenotypes are developmental, and the Perturb-seq perturbation was acute AAV CRISPR starting at P16 with nuclei harvested at P37-P44. The olfactory bulb, a major Prokr2-dependent structure, was not part of the profiled tissue. Adult Prokr2 expression is distributed in specialized hypothalamic, amygdalar, SCN, and other nuclei (Mohsen et al. 2017; Yin et al. 2022), whereas this held-out endpoint is one thalamic/glutamatergic Allen group. In the focal data, neither the `Prokr2` transcript nor its ligands behaved like reliably expressed/modulated features.

The direct in-dataset receptor evidence was even more conservative. Almost every assayed neuropeptide or G-protein-coupled receptor nearest to a plausible Prokr2 mechanism had 0 DEGs. The rare 1-DEG receptor cases were dominated by self-knockdown of the receptor transcript (`Gabbr1`, `Gpr158`) or a singleton off-target-looking feature (`Cnr1`). Since measured `Prokr2` was fully nonsignificant as a feature across all focal training signatures, I did not expect even a robust self-DEG for Prokr2.

## Prediction

Final point prediction:

```text
Prokr2 -> 0 DEGs
```

This is driven mainly by within-dataset evidence: receptor, G-protein, PLC/PKA/PKC, `Fgfr1`, and `Zbtb20` perturbations were null or singleton in `151 TH Prkcd Grin2c Glut`. External gene-function knowledge was used to choose those comparisons and to down-weight germline/embryonic olfactory and GnRH phenotypes that should not be recapitulated by sparse postnatal CRISPR in a thalamic glutamatergic group.

## Limits and uncertainty

- There was no exact in-dataset `Prokr1`, `Prok1`, `Prok2`, `Mrap2`, or `Anos1` perturbation, so the prediction has no same-ligand or same-receptor-family positive control.
- PROKR2 is pleiotropic. A true Prokr2-expressing SCN, amygdala, terminal-nerve, or olfactory-lineage population could respond strongly; the prediction is specifically for `151 TH Prkcd Grin2c Glut` in this postnatal whole-brain-minus-olfactory-bulb/hindbrain screen.
- A zero point estimate means I do not expect any gene to pass BH FDR 0.05 at the available power. It does not imply Prokr2 is biologically unimportant or that editing failed.
- Singleton DEG counts in receptor knockouts show that target self-knockdown alone can produce `n_degs = 1` when the transcript is expressed enough. If a small Prokr2-positive subset exists inside the focal group, the true count could be 1, but the focal measured-feature evidence made 0 more likely.
