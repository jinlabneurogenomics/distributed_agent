# Question

Predict the held-out value of `n_degs` for `Ednrb` in `151 TH Prkcd Grin2c Glut` cells. Here `n_degs` is the count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the acute AAV-PHP.eB CRISPR loss-of-function Perturb-seq comparison of recovered perturbed nuclei against matched controls. I treated the endpoint as the assay-specific focal-cell DEG count, not as developmental essentiality, a viability score, target-RNA knockdown, or the strength of endothelin biology in non-neuronal cells.

`Ednrb` is absent as a perturbation from the training count CSV and from the supplied DE parquet by construction, so its own focal signature is absent. The output CSV of requested targets contains one gene, `Ednrb`.

# Sources

- Direct endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Direct DE signatures: `training differential-expression dataset`
- Requested targets: `single-target request for Ednrb`
- Run-local bindings, dataset portrait, compact coverage, and measurement registry in `codex_runtime/pipeline/`
- Internal same-experiment interpretation layer: PerturbAI July corpus release `perturbai-july-260713-sourceguard-1773-v1`; I used its Ednra Claim/story summaries, its bounded Ednra Evidence records, and its BioKG projection only to verify same-experiment endothelin comparators.
- Independent literature from NCBI PubMed:
  - Davenport et al. 2016, Pharmacological Reviews, endothelin pharmacology review, DOI `10.1124/pr.115.011833`, PMID `26956245`.
  - Shin, Russell and Tilghman 1997, PNAS, molecular Ednrb alleles and piebald/enteric-neuron phenotypes, DOI `10.1073/pnas.94.24.13105`, PMID `9371807`.
  - Gadea et al. 2009, Journal of Neuroscience, endothelin regulation of oligodendrocyte progenitor migration/differentiation, DOI `10.1523/JNEUROSCI.0822-09.2009`, PMID `19675238`.
  - Swire et al. 2019, eLife, EDNRB and PKC-epsilon mediated regulation of adaptive CNS myelination in oligodendrocytes, DOI `10.7554/eLife.49493`, PMID `31657718`.
  - Michinaga et al. 2021, Neurochemistry International, ETB receptor regulation of astrocytic sonic hedgehog after traumatic brain injury, DOI `10.1016/j.neuint.2021.105042`, PMID `33838160`.
  - Chen et al. 2017, Scientific Reports, ET1-ETBR signaling in basolateral amygdala pyramidal neurons, DOI `10.1038/s41598-017-02583-6`, PMID `28539637`.

# Dataset calibration

The focal training table contains 1,674 visible perturbations. `n_degs` is zero for 1,205 of them, one for 276, and positive for 469; the median is zero, the 75th percentile is one, the 90th percentile is two, the 95th percentile is 18, and the maximum is 2,677. Thus a zero prediction is the empirical default unless a target has a close measured analog or pathway evidence supporting a broad recovered-cell transcriptional response.

For target-specific analogs, I queried the DE parquet with a focal-cell filter and a bounded list of endothelin, GPCR, and proximal signaling perturbations, then counted FDR-significant rows and inspected the smallest adjusted p-values:

```python
tab = ds.dataset(parquet, format="parquet").to_table(
    columns=["names", "gene_target", "scores", "logfoldchanges",
             "pvals_adj", "n_pert_matched", "n_ctrl_matched"],
    filter=(pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
           & pc.field("gene_target").isin(selected_targets),
)
```

`Ednra`, the only visible endothelin receptor perturbation, had 130 recovered perturbed nuclei, 23,679 matched controls, zero genes at `pvals_adj < 0.05`, and a minimum `pvals_adj` of 1.0 in the focal group. The internal PerturbAI July corpus independently summarizes the same experiment as a buffered `Ednra` response: 19 of 20 measured neuronal groups had no downstream genes even at FDR<0.10, and the only remaining group had a single `Dhtkd1` hit. The corpus Ednra report also notes that literature-obvious proximal endothelin comparators were represented only for `Calm1`, `Calm2`, `Calm3`, `Dlx6`, `Mapk1`, `Plcb1`, and `Prkca`; ligand targets, `Ednrb`, `Gnaq`, `Gna11`, `Gna12`, `Gna13`, `Ece1`, `Ece2`, `Arrb1`, `Arrb2`, `Rock1`, and `Rock2` were not visible training perturbations.

# Ednrb reasoning

`Ednrb` encodes endothelin receptor type B, a seven-transmembrane GPCR for endothelins rather than a transcription factor or core chromatin/RNA-processing factor. The biological prior from endothelin genetics is strong in developmental and non-neuronal contexts: Ednrb is required in neural-crest derived melanocyte and enteric-neuron development in piebald/Hirschsprung models, astrocyte-derived endothelin affects OPC migration and differentiation, EDNRB signaling can regulate oligodendrocyte myelination, and ETB receptors regulate astrocyte/BBB responses after traumatic injury. Those stages do not line up well with this assay's acute postnatal mosaic LOF in NeuN-enriched recovered thalamic glutamatergic nuclei.

The most relevant in-dataset perturbations were:

| training perturbation | focal `n_degs` | expression-pattern evidence | interpretation for `Ednrb` |
| --- | ---: | --- | --- |
| `Ednra` | 0 | closest visible endothelin receptor; zero focal DEGs, minimum focal `pvals_adj=1.0`; internal corpus says the Ednra surface was buffered across neuronal groups | Same family and ligand system but not an obligate EDNRB partner. Its flat response says endothelin GPCR perturbation was not broadly visible in this postnatal neuronal DE assay. |
| `Plcb1` | 0 | canonical endothelin downstream effector listed in the Ednra corpus report; zero focal DEGs | Proximal Gq/PLC signaling did not generate a focal thalamic response on its own. |
| `Prkca` | 0 | canonical endothelin downstream effector; zero focal DEGs | PKC signaling membership was not sufficient for a detectable response. |
| `Mapk1` | 0 | canonical MAPK-pathway comparator; zero focal DEGs | ERK/MAPK propagation downstream of a receptor was not a strong analog here. |
| `Calm1`, `Calm2`, `Calm3` | 14, 0, 1 | calcium/calmodulin comparators from the Ednra corpus; one paralog had a small 14-DEG response, the others were zero or singleton | These are broad calcium sensors, not EDNRB-specific dependencies; at most they support a weak low-count receptor-cascade prior. |
| `Dlx6` | 0 | developmental endothelin target in craniofacial neural crest; zero focal DEGs | The neural-crest transcriptional endpoint of endothelin signaling did not transfer into P16 postmitotic thalamic neurons. |
| `Agtr1a`, `Agtr2`, `Avpr1a`, `Avpr1b`, `S1pr2` | 0, 0, 0, 0, 0 | peptide/lipid GPCR receptor perturbations in the same focal group were all flat | GPCR receptor perturbations are commonly buffered or context-mismatched in the recovered thalamic cell group. |

The causal chain I used was: acute AAV CRISPR loss of `Ednrb` in sparse postmitotic cells -> partial loss of EDNRB receptor function in any edited NeuN-positive focal neurons -> propagation through G-protein/PKC/MAPK or calcium pathways only if endogenous endothelin tone and receptor expression are present -> recovered thalamic glutamatergic nuclei at P37-P44 -> Wilcoxon DEG count. External EDNRB phenotypes mostly break this chain at the exposure/context step: they are neural crest, oligodendrocyte, astrocyte, vascular, injury, or myelination phenomena, while this experiment deliberately under-samples non-neuronal cells and tests a non-injured neuronal endpoint. Chen et al. did report ET1-ETBR modulation of amygdala pyramidal-neuron excitability, so EDNRB can act in glutamatergic neurons, but that is a regional electrophysiological effect rather than evidence for a broad thalamic nuclear-RNA DEG response after receptor loss.

The measured analogs and the context prior therefore agree. I predict `Ednrb` will behave like `Ednra` and the many buffered GPCR perturbations, with no gene crossing FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

# Limits

This is an extrapolation from `Ednra` and pathway relatives because the held-out `Ednrb` expression signature is absent. I did not observe baseline Ednrb RNA or protein in the focal thalamic class from the supplied inputs, and partial AAV CRISPR could miss a low-abundance receptor effect. The GPCR comparisons are mechanistic but imperfect: EDNRB differs from EDNRA in ligand preference, cellular localization, and glial/oligodendrocyte biology, while calmodulins and MAPK genes are shared signaling nodes rather than endothelin-specific obligate complex members. The point prediction is therefore high confidence only for the assay-specific zero/nonzero decision; it should not be read as saying EDNRB is biologically inert in brain, development, vascular cells, glia, or injury models.
