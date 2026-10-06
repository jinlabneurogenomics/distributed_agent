# Grm3 DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and scope

The run requested one held-out perturbation, `Grm3`, from
`101_Grm3.csv`. I interpreted the prediction as the integer number of measured
genes with `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` cell
group after sparse P16 AAV-CRISPR loss of `Grm3`, including the `Grm3`
self-transcript if it crossed the same DE threshold. I treated self-transcript
DE only as a possible contributor to this exact count, not as evidence for
stronger or weaker DNA editing.

`Grm3` was absent from both supplied training inputs, as intended. `Grm2`, the
closest group-II metabotropic glutamate receptor paralog, was also absent as a
training perturbation, so the prediction necessarily transfers from other
metabotropic glutamate receptors, Gi/o-coupled receptor pathway nodes, cAMP
nodes, and counterexamples in the same dataset.

## Sources used

- Raw differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Training focal-cell DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested manifest:
  `[local file: 101_Grm3.csv]`
- Distributed Agents same-experiment PerturbAI atlas corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, especially the curated
  `Grm1`, `Grm5`, `Grm7`, `Grm8`, and `Gnao1` target contexts.
- PubMed-indexed external literature for mGluR3 and group-II mGluR signaling:
  Sheffler et al., 2011, DOI `10.1021/cn200008d`, PMID `22860167`;
  Tamaru et al., 2001, DOI `10.1016/s0306-4522(01)00305-0`,
  PMID `11591452`; Lea et al., 2001, DOI `10.1152/jn.2001.85.3.1097`,
  PMID `11247980`; Jin et al., 2018, DOI `10.1093/cercor/bhx005`,
  PMID `28108498`.

## Computational evidence from the training data

The training count file contained 1,674 perturbations in the focal class.
`n_degs` was highly zero-inflated: median `0`, 75th percentile `1`, 90th
percentile `2`, 95th percentile `18`, with only 28.0% of training targets
nonzero. This makes a zero or singleton call the calibrated default for weak
single-receptor perturbations, but not for every excitatory receptor, since
`Grin1` had 89 focal-cell DEGs.

I filtered the parquet to the focal `group_name` and a curated set of candidate
analogs, then counted FDR-significant rows and inspected the top adjusted
p-values:

```python
flt = (
    ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & ds.field("gene_target").isin(targets)
df = ds.dataset(parquet, format="parquet").scanner(
    columns=[
        "names", "gene_target", "logfoldchanges",
        "pvals", "pvals_adj", "scores",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=flt,
).to_table().to_pandas()
```

Key focal-cell analog counts:

| training perturbation | focal `n_degs` | expression-pattern evidence |
| --- | ---: | --- |
| `Grm1` | 1 | The only FDR gene was `Grm1` itself, log2FC `-0.438`, q `4.28e-05`. |
| `Grm5` | 0 | No FDR genes; the best focal adjusted p-value was 1.0. |
| `Grm6` | 0 | No FDR genes; `Grm6` is retina-specialized and appears uninformative in this cell class. |
| `Grm7` | 1 | The only FDR gene was `Grm7` itself, log2FC `-0.364`, q `7.07e-04`. |
| `Grm8` | 0 | No FDR genes; the best focal adjusted p-value was 1.0. |
| `Homer2` | 0 | No focal DEGs for this postsynaptic mGluR scaffold. |
| `Plcb1` | 0 | No focal DEGs for this group-I mGluR/GPCR effector. |
| `Gnao1` | 1 | The only FDR gene in the focal class was `Gnao1` itself, log2FC `-0.591`, q `9.42e-07`. |
| `Gnas`, `Gnb5` | 0, 0 | No focal FDR genes in sampled G-protein nodes. |
| `Adcy1`, `Adcy3`, `Adcy5` | 0, 0, 0 | No focal FDR genes in the sampled adenylyl-cyclase nodes. |
| `Gabbr1`, `Gabbr2` | 1, 1 | The only focal FDR genes were the respective self-transcripts. |
| `Grin1` | 89 | Positive counterexample: an ionotropic glutamate receptor perturbation can produce a sizable 151 TH response. |
| `Grin2a`, `Grin2b`, `Grin2d`, `Grin3a` | 1, 2, 0, 0 | NMDA-family perturbations ranged from self-only/sparse to null except for `Grin1`. |

I also ran a signed-profile comparison over 17,259 focal measured genes for the
mGluR/cAMP/GABA-B candidate set. The exact full-profile correlations were not
decisive because almost-flat perturbations share many tiny same-direction
shifts. The FDR-level part was decisive: none of the represented mGluR,
`Homer2`, `Plcb1`, `Gnao1`, `Gnas`, `Adcy1`, `Adcy3`, `Adcy5`, `Gnb5`,
`Gabbr1`, or `Gabbr2` profiles shared a significant downstream gene in this
focal class, and top-200 tail overlaps between the receptor profiles were only
small nominal overlaps, not a recurrent FDR module.

Finally, I checked how the `Grm3` transcript behaved as a measured gene across
the 1,674 non-held-out focal perturbations. Its adjusted p-values were all
large, with a minimum q of `0.97`; that does not speak to `Grm3` editing, but
it does suggest the `Grm3` RNA row is not a high-power thalamic readout likely
to add a one-gene self hit by itself.

## Same-experiment corpus evidence

The Distributed Agents corpus had no `Grm3` context, consistent with holdout or missing
coverage. Its mGluR findings are nevertheless the right internal summaries of
the analog space:

- `Grm8:F002` reports that `Grm1`, `Grm5`, `Grm6`, `Grm7`, and `Grm8` were
  FDR-flat at the downstream level and that represented mGluR paralogs did not
  expose a hidden basal mGluR transcriptional module.
- `Grm5:F003` reports shared basal buffering across measured mGluR, PLC/IP3,
  PKC/CaMK, and postsynaptic scaffold perturbations, including `Homer2`,
  `Itpr1`, `Plcb1`, `Prkca`, `Dlg4`, and `Shank2`.
- `Grm7:F003` and `Grm7:F004` reject convergence between `Grm7`, `Grm8`,
  `Grm1`, `Grm5`, `Grm6`, and broader Gi/o-to-adenylyl-cyclase comparators
  including `Gabbr1`, `Gabbr2`, `Gnao1`, `Gnb5`, `Rgs6`, `Adcy1`, `Adcy3`,
  and `Adcy5`.
- `Grm1:F003` makes the same point for the group-I/Homer/IP3R/PKC neighborhood:
  expected pathway or scaffold relatives are basal RNA nulls or isolated
  singletons rather than a common mGluR-like program.
- `Gnao1:F003` shows that represented Gi/o and cAMP relatives did not
  phenocopy the narrow `Gnao1` response, bounding the prediction away from a
  generic chronic GPCR/cAMP transcriptome.

## Target-specific biological rationale

`Grm3` encodes mGluR3, one of the two group-II metabotropic glutamate
receptors. Group-II mGluRs, including mGluR2 and mGluR3, are class-C GPCRs that
couple through Gi/o and negatively regulate adenylyl cyclase rather than
forming ion channels (Sheffler et al. 2011; Lea et al. 2001). mGluR3 can be
present in neuronal pre- and postsynaptic compartments as well as glia in mouse
CNS (Tamaru et al. 2001), and primate cortical data further support a
postsynaptic mGluR3 route to cAMP/K-channel control that differs from the more
presynaptic mGluR2 pattern (Jin et al. 2018). Thus the best external prior is
not a broad transcription-factor, proteostasis, or developmental-state
perturbation; it is a receptor-mediated Gi/o/cAMP synaptic modulator.

Within the training data, that prior maps to an almost entirely silent basal
snRNA-seq neighborhood. `Grm1` and `Grm7` only counted their own knocked-down
transcripts in the focal endpoint, while `Grm5`, `Grm6`, `Grm8`, `Homer2`,
`Plcb1`, `Gnas`, `Gnb5`, and `Adcy1/3/5` were all zero. The closest directly
tested inhibitory class-C receptor analogy, GABA-B, also gave self-only
singletons for `Gabbr1` and `Gabbr2`. By contrast, `Grin1` produced a genuine
89-gene focal signature, so the null prediction is not because glutamatergic
receptors are assumed invisible in general; it is specific to metabotropic
receptors and proximal second-messenger perturbations in this chronic basal
assay.

For `Grm3`, I therefore predict no stable downstream DE genes in 151 TH Prkcd
Grin2c Glut. I also do not add a self-transcript singleton: `Grm3` is likely a
weaker focal-class RNA readout than `Grm1`, `Grm7`, `Gabbr1`, or `Gabbr2`, and
the dataset-local mGluR rates make a zero-count result more likely than a
self-only one.

Predicted `n_degs`: `0`.

## Limits and extrapolation

- The closest paralog, `Grm2`, was not a training perturbation, and `Grm3`
  itself was absent from the same-experiment corpus, so the prediction is an
  extrapolation from group-I, group-III, GABA-B, and cAMP-neighbor tests rather
  than a direct group-II comparison.
- The focal readout is a basal nuclear RNA endpoint 3 to 4 weeks after sparse
  postmitotic editing. It can miss evoked Ca2+/cAMP fluxes, synaptic release
  changes, receptor trafficking, and transient immediate-early responses.
- `Grm3` has glial roles, but the experiment is NeuN-enriched and largely
  under-samples glia, so a real astrocytic mGluR3 phenotype would not rescue a
  neuronal DEG count here.
- Distinguishing `0` from `1` is mostly about whether the self `Grm3`
  transcript crosses FDR; average CRISPR target-RNA reduction in this platform
  is modest and self rows are an imperfect, stochastic contributor to the
  requested count.
