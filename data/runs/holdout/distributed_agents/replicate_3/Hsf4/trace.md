# Hsf4 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The held-out target list for this run is exactly one perturbation:

```text
Hsf4
```

The requested value is the number of measured mouse genes with `pvals_adj < 0.05`
in `151 TH Prkcd Grin2c Glut` nuclei after an acute P16-to-P37/P44 AAV-CRISPR
loss-of-function perturbation. I treated `151 TH Prkcd Grin2c Glut` as the Allen
thalamic glutamatergic class described by the dataset portrait; `TH` is thalamus,
not tyrosine hydroxylase. `Hsf4` is held out, so its own DEG count and expression
signature were not used from the differential-expression parquet.

## Sources used

- Input manifest:
  `[local file: 108_Hsf4.csv]`.
- Training endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Same-experiment semantic layer: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for `Hsf1`,
  `Hspa8`, `Hspa5`, `Dnajb6`, `Foxe3`, `Maf`, and `Pax6` target contexts and
  for the heat-shock/proteostasis candidate topology.
- External literature through NCBI PubMed:
  - Shi et al. 2009, BMC Molecular Biology, doi:10.1186/1471-2199-10-10,
    PMID:19224648.
  - Christians and Benjamin 2006, Handbook of Experimental Pharmacology,
    doi:10.1007/3-540-29717-0_6, PMID:16610358.
  - Nakai 2009, BMB Reports, doi:10.5483/bmbrep.2009.42.10.631,
    PMID:19874706.
  - Anand et al. 2018, Human Mutation, doi:10.1002/humu.23395,
    PMID:29314435.
  - Morishita et al. 2021, Nature, doi:10.1038/s41586-021-03439-w,
    PMID:33854238.
  - Cui et al. 2016, International Journal of Biochemistry & Cell Biology,
    doi:10.1016/j.biocel.2016.08.022, PMID:27586257.

## Computational checks

The training endpoint table contained 1,674 non-held-out perturbations in the
focal cell class. It is highly zero-inflated: 1,205 targets, or 72.0%, had
`n_degs = 0`; 276 had one DEG; 90 had 2-10 DEGs; and 42 had more than 100 DEGs.
`Hsf1` was the only `Hsf*` target in the training-count table, with `n_degs = 6`.
`Hsf2` was not a training perturbation, and `Hsf4` was absent by design.

I then scanned the parquet only for the focal group and for a hand-curated set
of heat-shock, chaperone, stress-transcription-factor, proteasome, and
developmental-eye transcription-factor perturbations. The operation was:

```python
scanner = ds.dataset(de_path, format="parquet").scanner(
    columns=[
        "names", "scores", "logfoldchanges", "pvals", "pvals_adj",
        "group_name", "gene_target", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
    ) & ds.field("gene_target").isin(targets),
)
```

Exact focal-cell `pvals_adj < 0.05` counts for the mechanistic neighborhood were:

| training perturbation | focal `n_degs` | focal FDR<0.05 expression evidence |
| --- | ---: | --- |
| `Hsf1` | 6 | `Hsph1`, `Hsp90aa1`, `Rsrp1`, `Hsp90ab1`, `Mat2a`, `Ahsa2`, all down |
| `Hspa8` | 9 | Up-regulated `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1`, `Cct6a`; down-regulated `Fras1`, `Unc79`, `Leng8`, `Apba2` |
| `Hspa5` | 5 | `Erc1` down; `Hsp90b1`, `Nfe2l1`, `Pdia4`, `Derl3` up |
| `Hsp90ab1` | 1 | only `Hsp90ab1` itself |
| `Dnajb4` | 0 | no FDR<0.05 row |
| `Dnajb6` | 0 | no FDR<0.05 row |
| `Dnajc13` | 1 | only `Dnajc13` itself |
| `Dnajc5` | 1 | only `Dnajc5` itself |
| `Atf6` | 0 | no FDR<0.05 row |
| `Vcp` | 2 | `Rasgef1b` up, `Nsmf` down |
| `Nfe2l1` | 0 | no FDR<0.05 row; five rows, including `Nfe2l1` and `Ubc`, stopped at FDR 0.06198 |
| `Nfe2l2` | 0 | no FDR<0.05 row |
| `Mafg` | 1 | only `Lamp2` |
| `Foxe3` | 0 | no FDR<0.05 row |
| `Maf`, `Mafa`, `Mafb` | 0, 0, 0 | no FDR<0.05 rows in this thalamic group |
| `Pax2`, `Pax3`, `Pax4`, `Pax6`, `Pax7`, `Pax8` | all 0 | no FDR<0.05 rows in this thalamic group |
| `Psmb4`, `Psmc1` | 742, 430 | broad proteasome-damage stress signatures; retained as high-effect counterexamples rather than Hsf4 analogs |

The `Cry1` and `Cry2` rows in the screen are cryptochrome circadian genes, not
lens crystallins, so I did not treat them as crystallin-pathway perturbations.
Actual HSF4 lens outputs such as `Cryaa`, `Cryab`, `Crygs`, `Bfsp1`, and
`Bfsp2` were present as measured genes in the parquet, but not as training
perturbations.

## Hsf4-specific reasoning

`Hsf1` is the only direct heat-shock factor analog in the training set. It is a
real positive control for HSF-family transcription in the focal thalamic class:
the six corrected `151 TH Prkcd Grin2c Glut` genes were the expected
HSP90/HSP110/co-chaperone output (`Hsph1`, `Hsp90aa1`, `Hsp90ab1`, `Ahsa2`) plus
`Rsrp1` and `Mat2a`. The Distributed Agents Hsf1 report summarizes the same experiment as
a restricted, direct chaperone-output decrease rather than a broad UPR,
autophagy, proteasome, apoptosis, or mitochondrial stress response.

That Hsf1 result is an upper-bound analogy for Hsf4, not a direct transfer.
Hsf4 is a heat-shock-factor family transcription factor, but mammalian knockout
work places its reproducible requirement in the ocular lens: Hsf4 knockout mice
develop cataracts with down-regulation of `Crygs`, `Bfsp1`, and `Bfsp2`
(Shi et al. 2009); review of HSF knockout mice described Hsf4-null animals as
giving the consistent lens-formation phenotype among the HSF family
(Christians and Benjamin 2006); and a cataract-gene review lists HSF4 together
with FOXE3, MAF, and PITX3 as lens transcription factors whose human variants
cause developmental ocular disease (Anand et al. 2018). More recent lens work
puts HSF4 upstream of lens fiber-cell organelle breakdown by PLAAT phospholipases
(Morishita et al. 2021) and upstream of lens epithelial lysosomal homeostasis
through alpha B-crystallin and ATP6V1A (Cui et al. 2016). None of these primary
programs is an obvious basal requirement of recovered postmitotic thalamic
glutamatergic neurons.

The dataset-local lens-factor checks point the same way. `Foxe3`, a close
cataract/developmental-ocular comparator from Anand et al. 2018, had
`n_degs = 0` in the focal group; the Distributed Agents Foxe3 report found 0 downstream
FDR<0.10 genes in every recovered neuronal cell group and explicitly noted that
canonical lens epithelial, crystallin, and growth-factor targets were absent in
neurons. Large-MAF lens/neurodevelopment factors were also unhelpful for Hsf4:
`Maf`, `Mafa`, and `Mafb` were all 0 in the focal class, and the Maf corpus
report emphasizes small, cell-context-specific Pvalb effects rather than a
shared eye-lineage program. `Pax6` and the represented Pax-family perturbations
were likewise all 0 in `151 TH Prkcd Grin2c Glut`; the Pax6 report describes
acute P16 Pax6 loss as transcriptionally silent across recovered NeuN+ classes.
These are imperfect same-lineage analogies, but they are much closer to Hsf4's
dominant mouse loss-of-function biology than core proteasome subunit loss.

The broader proteostasis neighborhood argues against assigning a small nonzero
count simply because Hsf4 contains a heat-shock-factor DNA-binding domain.
`Hspa8` and `Hspa5` produced small positive focal responses, but their signatures
were cytosolic Hsc70 counterinduction and ER BiP/ERAD induction respectively;
`Hsp90ab1`, `Dnajc13`, and `Dnajc5` were self-only; and `Dnajb4`, `Dnajb6`,
`Atf6`, `Nfe2l1`, and `Nfe2l2` were 0 in this exact cell group. The Distributed Agents
candidate topology links these nodes in a single proteostasis report component,
but the target-context records stress that single chaperone, DNAJ/HSP40, HSF1,
and ER-chaperone perturbations do not collapse onto one generic heat-shock or
UPR transcriptomic state in this juvenile neuronal assay. `Psmb4` and `Psmc1`
show that severe core proteasome damage was easy to detect in the same focal
group, yet Hsf4 is not a core proteasome subunit or a general neuronal
proteotoxic-load generator.

Taken together, the prediction is that acute sparse Hsf4 editing will look more
like the flat lens-development transcription factors and most distal chaperone
nodes than like Hsf1 or Hspa8. I therefore predict no gene crossing BH FDR 0.05
in `151 TH Prkcd Grin2c Glut`.

## Predicted count

| target | predicted_n_degs |
| --- | ---: |
| `Hsf4` | 0 |

## Limits and extrapolation

- Hsf4 itself has no same-experiment corpus report or training signature because
  it was held out; the prediction is necessarily an extrapolation from Hsf1,
  chaperone/stress comparators, and lens-development transcription factors.
- `Hsf1` is the only measured HSF paralog. `Hsf2` was absent from the training
  target set, so HSF-family redundancy or antagonism could not be mapped
  directly.
- The lens comparators are same-tissue-program priors, not same-complex partners
  of HSF4 in thalamic neurons. Their flat focal responses support contextual
  mismatch but do not prove that Hsf4 protein is absent or functionless in every
  neuronal subtype.
- The assay reads survivor-conditioned nuclear RNA 3-4 weeks after sparse
  AAV-CRISPR. It would miss DNA indels, HSF4 protein binding, a transient early
  response, local synaptic effects, or a response in eye, olfactory epithelium,
  glia, vascular cells, olfactory bulb, or hindbrain.
- Target-transcript knockdown is not available for held-out Hsf4 and, in this
  platform, target mRNA reduction is not a reliable quantitative proxy for
  editing. I did not use self-RNA strength to promote or demote any comparator.
