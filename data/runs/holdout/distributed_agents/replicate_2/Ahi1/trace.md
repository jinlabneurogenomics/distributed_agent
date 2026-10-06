# Ahi1 held-out DEG-count prediction

## Question and interpretation

The requested output is a point prediction for the held-out endpoint
`n_degs`: the number of measured genes with BH-adjusted Wilcoxon
`pvals_adj < 0.05` after each held-out knockout in `151 TH Prkcd Grin2c
Glut` neurons.

The manifest for this run contains one target:

| target_name |
|---|
| Ahi1 |

I treated `151 TH Prkcd Grin2c Glut` as the Allen thalamic glutamatergic
cell group described in the task, not as a tyrosine-hydroxylase label. I also
treated zero as a valid endpoint value: it means no measured nuclear RNA
feature is predicted to pass FDR 0.05 in the focal cell group, not that AHI1 is
dispensable or unedited.

I verified the training-count file has 1,674 non-held-out perturbations and no
`Ahi1` row. A direct parquet scan for `gene_target == "Ahi1"` also returned 0
rows, so the Ahi1 signature itself was not used.

## Sources

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 008_Ahi1.csv]`
- Same-experiment Distributed Agents corpus:
  `perturbai-july-260713-sourceguard-1773-v1`
- Run-local Distributed Agents profile comparison over focal-cell log-fold-change
  vectors for represented ciliary genes.
- External literature via PubMed:
  - Dixon-Salazar et al. 2004, DOI `10.1086/425985`, PMID `15467982`
  - Eley et al. 2008, DOI `10.1038/ki.2008.377`, PMID `18633336`
  - Lancaster et al. 2009, DOI `10.1038/nm.2010`, PMID `19718039`
  - Lancaster et al. 2011, DOI `10.1038/nm.2380`, PMID `21623382`
  - Lancaster, Schroth and Gleeson 2011, DOI `10.1038/ncb2259`, PMID
    `21602792`
  - Romani et al. 2014, DOI `10.1016/j.diff.2014.02.005`, PMID `24613594`
  - Nguyen et al. 2017, DOI `10.1136/jmedgenet-2016-104200`, PMID `28442542`

## Computations over the training data

1. I read the focal `n_degs` CSV and summarized the empirical count scale.
   Among 1,674 training perturbations in `151 TH Prkcd Grin2c Glut`, 1,205
   were exact zeros, 363 had 1-9 DEGs, 63 had 10-99, and 43 had at least 100.
   The median was 0, the 75th percentile was 1, and the 95th percentile was
   18. This establishes that small integer counts, especially 0, are common in
   this endpoint.

2. I pulled the exact focal-cell DE rows for a ciliary/Joubert comparator set
   from the parquet with a pyarrow filter on cell group and target:

```python
dataset.to_table(
    columns=[
        "gene_target", "names", "logfoldchanges", "pvals_adj",
        "scores", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
    ) & ds.field("gene_target").isin(targets),
)
```

   This was used only for non-held-out training perturbations.

3. I compared the full signed focal-cell log-fold-change vectors for a
   ciliary cohort with the run-local Distributed Agents profile tooling. The cohort
   was `Cep290`, `Rpgrip1l`, `Cplane1`, `B9d1`, `Ift43`, `Ift81`, `Ift88`,
   `Kif3b`, `Ttc21b`, `Bbs5`, `Lztfl1`, `Arl3`, and `Ttc8`. The comparison
   confirmed that 11 of 13 had no significant features at FDR 0.05 in the
   focal cell group; `Arl3` and `Ttc8` had exactly one negative significant
   feature each, their own target transcript. Full-profile Pearson
   correlations among core ciliary candidates were moderately high, roughly
   0.63 to 0.70 for the closest pairs I inspected, but the leading absolute
   log-fold-change features had adjusted p-values of 1.0 and no recurrent
   FDR-supported module. I therefore used the comparison as evidence for a
   shared near-null RNA state, not as evidence for a hidden positive program.

4. I inspected the profile-comparison eligible-neighbor lists. The closest
   whole-profile neighbors of `Cep290`, for example `Tfg`, `Marchf6`, `Nek1`,
   `Phf6`, and `Kif2a`, were not treated as Ahi1 analogs unless they had
   ciliary mechanism support. Those similarities are across weak,
   nonsignificant vectors; the curated same-experiment Cep290, Rpgrip1l,
   Cplane1, Ift88, and Bbs5 reports explicitly warn against over-interpreting
   such near-null full-surface neighbors as mechanism.

## Biological analogs for Ahi1

`Ahi1` encodes Jouberin, a ciliary/basal-body/centrosomal protein mutated in
Joubert syndrome. AHI1 was identified as a Joubert syndrome gene by
Dixon-Salazar et al. 2004, and Eley et al. 2008 showed that Jouberin localizes
to primary cilia/basal bodies and interacts with nephrocystin-1, placing it in
the NPHP/Joubert transition-zone neighborhood. Lancaster, Schroth and Gleeson
2011 showed that Jouberin can regulate canonical Wnt signaling at primary
cilia, Lancaster et al. 2011 showed reduced Wnt reporter activity in an
`Ahi1` mutant mouse cerebellar-midline model, and Romani et al. 2014 tied
Jouberin to cilium-associated neural differentiation in mouse embryonic stem
cells. Nguyen et al. 2017 further supports AHI1 as a ciliary-base protein in
retinal ciliopathy.

That external biology made the following training perturbations the relevant
comparators in this focal endpoint:

| training target | focal `n_degs` | focal expression-pattern evidence | reason for use |
|---|---:|---|---|
| `Cep290` | 0 | minimum focal adjusted p-value 0.650; no FDR 0.05 genes | Joubert/transition-zone neighbor; the Distributed Agents same-experiment corpus says Cep290 had no robust nuclear DE program in assayed postmitotic neurons and that ciliary GPCR, BBSome/IFT, and Hedgehog programs were absent or nearly absent after Cep290 and its tested pathway neighbors. |
| `Rpgrip1l` | 0 | minimum focal adjusted p-value 0.184; no FDR 0.05 genes | Transition-zone/NPHP/Joubert neighbor; corpus reports acute postnatal `Rpgrip1l` CRISPR was flat across recovered neuronal groups and most ciliogenesis/Hedgehog comparators were flat or singleton-only. |
| `Cplane1` | 0 | every focal adjusted p-value was 1.0; no FDR 0.05 genes | Joubert/CPLANE ciliary-assembly comparator; corpus reports no downstream DE in measured neuronal groups and no Hedgehog, IFT, or PCP mRNA response. |
| `B9d1` | 0 | every focal adjusted p-value was 1.0; no FDR 0.05 genes | MKS transition-zone comparator and counterexample: it had a compact signal in a different cerebellar GABA group in the same experiment, but not in this thalamic glutamate endpoint. |
| `Ift88` | 0 | every focal adjusted p-value was 1.0; no focal FDR 0.05 genes | Core IFT-B and ciliogenesis comparator; corpus reports IFT/BBS/transition-zone perturbations converge mainly by transcriptional buffering rather than by a shared IFT knockout transcriptome. |
| `Ift81` | 0 | minimum focal adjusted p-value 0.391; no FDR 0.05 genes | Core IFT-B comparator, near-null in the focal cell group. |
| `Ift43` | 0 | minimum focal adjusted p-value 0.847; no FDR 0.05 genes | IFT-A comparator, near-null in the focal cell group. |
| `Kif3b` | 0 | every focal adjusted p-value was 1.0; no FDR 0.05 genes | Kinesin-2 anterograde ciliary transport comparator, near-null in the focal cell group. |
| `Ttc21b` | 0 | minimum focal adjusted p-value 0.459; no FDR 0.05 genes | Retrograde IFT-A ciliary trafficking comparator, near-null in the focal cell group. |
| `Bbs5` | 0 | minimum focal adjusted p-value 0.220; no FDR 0.05 genes | BBSome ciliary-cargo trafficking comparator; BBSome membership produced only sparse, non-overlapping neuronal RNA effects in the same-experiment corpus. |
| `Lztfl1` | 0 | minimum focal adjusted p-value 0.195; no FDR 0.05 genes | BBSome regulator and ciliary trafficking comparator, near-null in the focal cell group. |
| `Ttc8` | 1 | the only focal FDR 0.05 hit was `Ttc8` itself | BBSome/BBS8 comparator; its single significant focal hit looks like on-target transcript loss rather than a downstream ciliary program. |
| `Arl3` | 1 | the only focal FDR 0.05 hit was `Arl3` itself | ARL ciliary lipidated-protein trafficking comparator; the observed focal response again did not extend past the target transcript. |
| `Alms1`, `Dync2h1`, `Rab3gap2`, `Nek1` | all 0 | all had zero focal FDR 0.05 genes | Broader ciliary/basal-body/ciliary-trafficking neighbors available in the training set; these reinforced the same near-null calibration. |

## Ahi1-specific prediction

The evidence pushing `Ahi1` away from a generic zero is real: AHI1/Jouberin is
a disease ciliary protein, it localizes at the primary cilium and basal body,
and loss can alter Wnt signaling and neural development in embryonic
cerebellum and differentiation systems. If this experiment had measured
embryonic progenitors, cerebellar morphogenesis, cilium morphology, ciliary
receptor localization, or retinal/kidney phenotypes, those facts would make a
positive effect plausible.

The requested endpoint is narrower: acute mosaic CRISPR at P16, 3-4 week
postmitotic NeuN+ survivor nuclei, thalamic glutamatergic group 151, and a
basal nuclear RNA count after BH correction. In exactly that focal endpoint,
the directly measured transition-zone and Joubert-like perturbations
`Cep290`, `Rpgrip1l`, `Cplane1`, and `B9d1` were all zero; the IFT and
BBSome/ciliary-trafficking perturbations were zero or self-transcript
singletons; and the same-experiment corpus summarizes the represented ciliary
perturbations as largely buffered at the basal nuclear RNA level rather than a
coherent shared ciliary transcriptional module. Ahi1 therefore looks more like
the `Cep290`/`Rpgrip1l`/`Cplane1` near-null class than like the strong
spliceosome, proteasome, or transcription-factor outliers in this cell group.

My point prediction for `Ahi1` is therefore:

| target_name | predicted_n_degs |
|---|---:|
| Ahi1 | 0 |

## Limits

- The Ahi1 perturbation was completely held out, so no Ahi1 expression
  signature, target-transcript trend, or cell recovery measurement was used.
- The strongest Ahi1 biology is developmental and ciliary-subcellular. The
  assay does not image cilia, localize ciliary proteins, measure cAMP/Wnt/Shh
  activity directly, assay retinal or kidney lineages, or sample embryonic
  neural progenitors.
- Many canonical immediate AHI1 neighbors, including `Nphp1`, `Tmem67`,
  `Cc2d2a`, `Tctn` genes, and several core BBS genes, were not present as
  training perturbations in this focal count file.
- Zero for `Cep290`, `Rpgrip1l`, and `Cplane1` in this endpoint is strong
  calibration for basal postnatal neuronal nuclear RNA, but it does not prove
  that ciliary architecture was intact after perturbation.
- The run-local full-vector similarities were computed over many
  nonsignificant rows; I used them only to check for gross hidden convergence
  and did not convert them into quantitative weights.
- A nonzero singleton for Ahi1, analogous to `Arl3` or `Ttc8`, is possible if
  the Ahi1 transcript itself crosses FDR. I assigned 0 rather than 1 because
  the closer transition-zone and Joubert comparators in this exact focal group
  were completely FDR-flat.
