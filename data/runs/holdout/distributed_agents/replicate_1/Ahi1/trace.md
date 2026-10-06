# Prediction trace

## Question and endpoint

I interpreted the task as a scalar holdout prediction for one perturbation,
`Ahi1`.  The endpoint is:

`n_degs = count(names with pvals_adj < 0.05 after Ahi1 CRISPR perturbation in 151 TH Prkcd Grin2c Glut)`

The count is the PerturbAI Wilcoxon/BH count among recovered, NeuN+,
class-assigned nuclei.  It is not a direct estimate of editing rate, cilium
assembly, protein localization, viability, or total RNA.  I treated the
training-count CSV as the direct endpoint for non-held-out targets, and used
the differential-expression Parquet to inspect the focal-cell signatures behind
candidate analogs.  `Ahi1` itself was held out and was absent from both inputs.

## Sources used

- Declared input endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared input DE table:
  `training differential-expression dataset`
- Requested-target manifest:
  `single-target request for Ahi1`
- Run-local dataset portrait, measurement registry, task bindings, compact
  coverage, and capability manifest under `codex_runtime/pipeline`.
- Internal same-experiment semantic layer: the PerturbAI July 260713 Sourceguard
  1773 v1 Findings/Evidence/Reference corpus.  This was used as packaged
  interpretation of the same experiment, not as independent replication.
- PubMed literature:
  Hsiao et al. 2009, Human Molecular Genetics, DOI 10.1093/hmg/ddp335,
  PMID 19625297; Tuz et al. 2013, Journal of Biological Chemistry,
  DOI 10.1074/jbc.M112.420786, PMID 23532844; Munoz-Estrada and Ferland 2019,
  Journal of Cell Science, DOI 10.1242/jcs.230680, PMID 31391239; Hsiao et al.
  2021, Journal of Neuroscience, DOI 10.1523/JNEUROSCI.2993-20.2021,
  PMID 33741721; Gana, Serpieri and Valente 2022,
  American Journal of Medical Genetics Part C, DOI 10.1002/ajmg.c.31963,
  PMID 35238134; Dowdle et al. 2011, American Journal of Human Genetics,
  DOI 10.1016/j.ajhg.2011.06.003, PMID 21763481; Garcia-Gonzalo et al. 2011,
  Nature Genetics, DOI 10.1038/ng.891, PMID 21725307.
- Reactome mouse IFT-B complex curation, R-MMU-5617824, as cited by the
  internal Ift88 report.

## Quantitative calibration

The requested manifest contains exactly:

```text
target_name
Ahi1
```

I loaded the 1,674 visible training targets for `151 TH Prkcd Grin2c Glut` and
counted the focal endpoint distribution.  It is sparse: 1,205/1,674 training
perturbations have `n_degs = 0`; the median is 0, the mean is 14.05, 132 targets
have at least 5 DEGs, and 106 targets have at least 10 DEGs.  Large responses in
this class are carried by targets such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`,
`Zbtb7a`, and proteasome/splicing/transcription factors, not by cilium genes.

I then selected the training perturbations most informative for AHI1 from
external and corpus biology and queried the Parquet only for those perturbations
in the exact held-out cell group.  The operation was:

```python
f = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(ciliary_analogs)
)
```

The focal-cell results were:

| training target | relationship to Ahi1 | 151 TH Prkcd Grin2c Glut count and local signature |
| --- | --- | --- |
| `Cep290` | Joubert/transition-zone comparator; AHI1 and CEP290 mutations both cause Joubert syndrome and retinal degeneration | 0 DEGs; 99 perturbed nuclei vs 23,679 controls; minimum adjusted p = 0.650 |
| `Rpgrip1l` | Joubert/NPHP transition-zone comparator | 0 DEGs; 137 perturbed vs 23,679 controls; minimum adjusted p = 0.184 |
| `Cplane1` | CPLANE/JBTS17 ciliary assembly and PCP/Hedgehog comparator | 0 DEGs; 179 perturbed vs 23,679 controls; minimum adjusted p = 1.000 |
| `B9d1` | B9/MKS transition-zone gate component; a positive counterexample elsewhere in the corpus | 0 DEGs; 180 perturbed vs 23,679 controls; minimum adjusted p = 1.000 |
| `Ift88` | IFT-B component, ciliogenesis/Hedgehog counterexample | 0 DEGs; 143 perturbed vs 23,679 controls; minimum adjusted p = 1.000 |
| `Ift43` | IFT-A component | 0 DEGs; 328 perturbed vs 23,679 controls; minimum adjusted p = 0.847 |
| `Ift81` | IFT-B component | 0 DEGs; 152 perturbed vs 23,679 controls; minimum adjusted p = 0.391 |
| `Kif3b` | anterograde ciliary kinesin-2 motor | 0 DEGs; 156 perturbed vs 23,679 controls; minimum adjusted p = 1.000 |
| `Dync2h1` | retrograde IFT dynein-2 motor | 0 DEGs; 98 perturbed vs 23,679 controls; minimum adjusted p = 0.348 |
| `Dync2i1` | dynein-2 IFT subunit | 0 DEGs; 229 perturbed vs 23,679 controls; minimum adjusted p = 1.000 |
| `Bbs5` | BBSome ciliary cargo-trafficking component | 0 DEGs; 121 perturbed vs 23,679 controls; minimum adjusted p = 0.220 |
| `Arl3` | ciliary small GTPase, less directly tied to AHI1 than ARL13B or RAB8A | 1 DEG, which was `Arl3` itself; 228 perturbed vs 23,679 controls |

For the closest Joubert/structural-cilium analogs I also counted DEGs across
all measured classes: `Cep290` had 0 total BH < 0.05 genes in 20 groups,
`Rpgrip1l` had 0 in 21 groups, `Cplane1` had only 1 in 22 groups, and `Ift88`
had only 1 in 21 groups.  `B9d1` was the main cilium-adjacent counterexample,
with 9 BH < 0.05 genes outside the focal class in `308 CB GABA`; the internal
July corpus likewise summarized that B9d1 response as CB-GABA restricted and
not as a pan-neuronal ciliary-loss program.  The same corpus summarized
`Cplane1` and `Rpgrip1l` as transcriptionally flat across the sampled acute
postnatal neuronal scope and `Cep290` as lacking a ciliary-gate, neuronal
ciliary-GPCR, or Hedgehog RNA program.

## Target-specific reasoning

### Ahi1

`Ahi1` encodes jouberin, a ciliary basal-body/transition-zone protein mutated in
Joubert syndrome.  External data make it a real neuronal cilium gene rather
than a superficial family match: Hsiao et al. showed that Ahi1 loss impairs
ciliogenesis and Rab8a localization; Tuz et al. showed that Joubert missense
mutations alter ciliary localization and binding to NPHP1/HAP1; Munoz-Estrada
and Ferland found that Ahi1 deletion reduces ARL13B ciliary recruitment and
Hedgehog signaling in mouse embryonic fibroblasts; and Hsiao et al. showed in
mouse neurons that Ahi1 loss reduces ciliary localization of MCHR1 and its
cAMP/ERK response without reducing total or surface MCHR1.  Gana et al. review
AHI1, CEP290, and RPGRIP1L as Joubert genes with related ciliary disease
biology.

Those mechanisms point to ciliary trafficking, ciliary compartment gating, and
ligand-dependent signaling as the direct molecular consequences of losing AHI1.
They do not require a broad steady-state nuclear RNA response in mature
thalamic neurons three to four weeks after a sparse P16 CRISPR perturbation.
The transfer chain is therefore:

`Ahi1 CRISPR -> impaired transition-zone/basal-body cargo localization -> altered ciliary GPCR/Hedgehog or vesicle-trafficking output in neurons -> possible secondary transcription only if the affected receptor pathway is active and synchronous in recovered 151 TH Prkcd Grin2c Glut nuclei -> BH DEG count`

The weakest link is the last step.  The matched training perturbations already
removed several genes from the same ciliary chain, including transition-zone or
Joubert genes (`Cep290`, `Rpgrip1l`, `Cplane1`, `B9d1`), core IFT machinery
(`Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Dync2h1`, `Dync2i1`), and a BBSome
trafficking component (`Bbs5`), and every one was a focal-cell zero.  The
strongest counterexample, `B9d1`, shows that a ciliary-gate target can produce
some RNA output in this experiment, but its output was confined to cerebellar
GABAergic neurons and did not phenocopy the AHI1-relevant Joubert comparators in
the requested thalamic group.

I therefore predict `Ahi1` will follow the local Joubert/ciliary null pattern
rather than the rare CB-GABA `B9d1` exception or the unrelated high-burden
splicing/proteostasis targets.  The appropriate point estimate is exactly zero
FDR-significant genes.

## Limits and uncertainty

- The prediction is supported by directly observed DEG counts for mechanistic
  analogs, but it is still an extrapolation from related perturbations because
  `Ahi1` itself was completely held out.
- `Ahi1` can have organelle-localization and GPCR-signaling phenotypes that
  snRNA-seq would miss unless they create coordinated nuclear RNA changes.
- Several very close components were absent from the training perturbation
  universe or from this manual analog set, including direct AHI1-linked
  `Rab8a`, `Arl13b`, `Nphp1`, and multiple MKS/Tectonic/CPLANE components.
- The focal cilium analogs include some low recovered-nucleus contrasts
  (`Cep290`, `Dync2h1`, `Bbs5`), so a small one- or two-gene effect could be
  missed.  The all-zero pattern across many related perturbations makes a broad
  effect unlikely, but not biologically impossible.
- The same-experiment corpus, the training-count CSV, and the Parquet all come
  from the same PerturbAI experiment; agreement among them is consistency, not
  independent replication.
