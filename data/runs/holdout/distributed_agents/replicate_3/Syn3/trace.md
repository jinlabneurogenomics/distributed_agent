# Syn3 DEG-count prediction trace

## Question understood

I interpreted the task as a point prediction of the held-out endpoint
`n_degs` for each requested perturbation in `151 TH Prkcd Grin2c Glut`
cells, where `n_degs` is the count of measured genes with BH-adjusted Wilcoxon
`pvals_adj < 0.05` in perturbed nuclei versus matched controls. `Syn3` is held
out, so its focal-cell differential-expression signature and its observed
focal-cell DEG count were absent from the supplied parquet and count CSV.

The manifest for this run contains one requested target, in this order:

```tsv
target_name
Syn3
```

I resolved the main ambiguity as follows: because a single self-depleted target
transcript can count as one DEG in this endpoint, a prediction of 0 versus 1
should depend on whether the closest measured paralogs show only self hits and
whether the held-out target is likely to produce a detectable self hit in this
focal population. I therefore treated zero as "no measured gene, including
Syn3 itself, is expected to pass FDR 0.05".

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene DE statistics for
  non-held-out perturbations. I filtered this to
  `group_name == "151 TH Prkcd Grin2c Glut"` and a biologically chosen set of
  synapsin, synaptic-vesicle, SNARE/active-zone, postsynaptic, and NMDAR
  comparator perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the observed focal
  `n_degs` values for 1,674 non-held-out training perturbations.
- `229_Syn3.csv`: the requested-target manifest.
- Distributed Agents same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`: I queried target contexts for
  `Syn1`, `Syn2`, `Syp`, `Sv2a`, and `Grin1`. The release had no target-specific
  `Syn3` finding, but it did contain curated same-experiment findings that
  `Syn1`/`Syn2`, `Syp`, `Sv2a`, `Cplx1/Cplx2`, `Stx1b`, `Unc13`, `Bsn`, and
  `Pclo` were mostly flat or self-only in this acute postnatal snRNA-seq
  setting.
- Distributed Agents runtime profile tools: I computed an explicit signed-profile
  comparison over `Syn1`, `Syn2`, `Syp`, `Sv2a`, `Cplx1`, `Cplx2`, `Stxbp1`,
  `Unc13a`, `Unc13b`, `Unc13c`, `Bsn`, `Pclo`, `Vamp1`, `Stx1b`, `Dlg4`, and
  `Grin1` in the focal cell group.
- PubMed literature:
  - Kao et al. 1998, DOI 10.1073/pnas.95.8.4667, PMID 9539796: cloning of
    `SYN3` as a third neuron-specific synapsin/synaptic-vesicle gene.
  - Hosaka and Sudhof 1999, DOI 10.1074/jbc.274.24.16747, PMID 10358015:
    synapsin C-domains can homo- and heterodimerize, with `Syn3` protein
    stability affected in `Syn1`/`Syn2` double knockouts.
  - Feng et al. 2002, DOI 10.1523/JNEUROSCI.22-11-04372.2002,
    PMID 12040043: `Syn3` knockout changes synaptic-vesicle trafficking and
    release in cultured neurons, and delays axon outgrowth.
  - Gitler et al. 2004, DOI 10.1523/JNEUROSCI.3795-04.2004,
    PMID 15601943: pan-synapsin loss changes reserve-pool vesicles and
    transmission, illustrating that synapsin loss has presynaptic physiological
    consequences even when basal morphology is grossly preserved.
  - Porton et al. 2011, DOI 10.1016/j.semcdb.2011.07.007, PMID 21827867:
    review of the roles of `Syn3`, including its differences from `Syn1` and
    `Syn2` and links to development and dopaminergic transmission.
  - Faustini et al. 2022, DOI 10.3390/cells11233902, PMID 36497160:
    evidence that Synapsin III regulates dopaminergic-neuron development
    upstream of BDNF/CDK5-dependent dendrite development.

## Computational calibration

The focal training CSV contained 1,674 perturbations. Its `n_degs` distribution
was zero-heavy:

```text
min=0, q25=0, median=0, q75=1, q90=2, q95=18, q99=436.48, max=2677
```

Only 469 of 1,674 perturbations had any focal DEG. Thus 0 or 1 DEG is the
expected range for weak structural or synaptic targets; hundreds of DEGs are a
distinct response class dominated by nuclear, proteostasis, receptor, or
trafficking hits.

I then inspected the training counts for the measured synapsins and nearby
presynaptic-vesicle genes:

| comparator | focal `n_degs` | reason for comparison and expression-pattern evidence |
|---|---:|---|
| `Syn1` | 1 | Closest first-degree synapsin paralog. In the focal parquet, the one FDR hit was only `Syn1` itself, down with logFC -0.834 and adjusted p = 1.59e-24. `Syn3` was not FDR-regulated in the `Syn1` perturbation. |
| `Syn2` | 0 | Closest first-degree synapsin paralog. Its own transcript moved downward in the focal profile but did not pass FDR, logFC -0.497 and adjusted p = 0.425, and no downstream gene passed FDR. |
| `Syp` | 1 | Abundant synaptic-vesicle membrane protein; the lone focal hit was self-depletion of `Syp`, logFC -1.776 and adjusted p = 7.95e-66. The Distributed Agents corpus also called the broader `Syp` surface downstream-absent/self-only rather than a vesicle-mRNA compensation program. |
| `Sv2a` | 1 | Ubiquitous vesicle glycoprotein with direct presynaptic release biology; the lone focal hit was self-depletion of `Sv2a`, logFC -1.048 and adjusted p = 1.86e-38. |
| `Cplx1` | 1 | SNARE-fusion regulator and very close vesicle-release comparator; the lone focal hit was self-depletion of `Cplx1`, logFC -0.863 and adjusted p = 4.29e-24. |
| `Cplx2` | 0 | Paralogous SNARE regulator; no significant focal features. |
| `Stxbp1` | 1 | Munc18-1 vesicle-fusion factor and the presynaptic exception in the same-experiment corpus in some other cell groups; in this focal group it also had only a self hit, logFC -0.663 and adjusted p = 9.38e-19. |
| `Stx1b` | 0 | Plasma-membrane SNARE; no significant focal features. |
| `Unc13a`, `Unc13b`, `Unc13c` | 0, 0, 0 | Active-zone vesicle priming genes; none produced any FDR-significant focal gene. |
| `Bsn`, `Pclo` | 0, 0 | Active-zone scaffold genes; neither produced any FDR-significant focal gene. |
| `Vamp1` | 1 | Vesicle SNARE paralog; the lone focal hit was self-depletion of `Vamp1`. |
| `Dlg4` | 1 | Postsynaptic scaffold counterexample; it too was self-only in the focal group. |
| `Grin1` | 89 | Positive control/counterexample. This obligate NMDA-receptor subunit generated a real mixed synaptic, ion-channel, growth/plasticity, and stress response in `151 TH Prkcd Grin2c Glut`, showing that the focal class and assay can report a synaptic perturbation when loss feeds into a sustained calcium-to-nucleus state. |

For a signed-profile check independent of the final count table, I compared the
focal log2-fold-change profiles of those 16 perturbations over the shared
17,259 measured features using `logfoldchanges` and `pvals_adj < 0.05`.
Eight of the 16 selected profiles had no significant feature at all, seven had
1 to 9 significant features, and only `Grin1` had at least 50. `Syn1` had one
negative significant feature; `Syn2` had none. `Syp`, `Sv2a`, `Cplx1`,
`Stxbp1`, and `Vamp1` likewise each had one negative significant feature, while
`Unc13a/b/c`, `Bsn`, `Pclo`, `Cplx2`, and `Stx1b` had none. The significant
feature intersections among the near-null synapsin/vesicle profiles were empty,
so the subthreshold whole-profile correlations among them are best read as
shared assay-floor behavior, not as a coherent multi-gene program.

`Syn3` itself is present as a measured feature in the focal parquet for all
1,674 non-held-out perturbations, but it did not move with FDR support under
the immediate paralog and vesicle comparators. For example, its adjusted
p-value was 1.0 after `Syn1`, `Syn2`, `Syp`, `Sv2a`, `Cplx1`, and `Grin1`
perturbation. That makes `Syn3` measurable in principle but gives no evidence
for compensatory regulation by the assayed synapsin or vesicle perturbations.

## Target-specific prediction

### Syn3

`Syn3` encodes Synapsin III, a neuron-specific synapsin family member on
synaptic vesicles. Literature places it in the same broad presynaptic reserve
pool, vesicle-trafficking, and release biology as `Syn1` and `Syn2`; the
synapsins can multimerize through conserved C-domains (Hosaka and Sudhof 1999),
and `Syn3` knockout perturbs synaptic-vesicle trafficking/release and axon
outgrowth in neuronal preparations (Feng et al. 2002). At the same time,
`Syn3` is not simply an interchangeable copy of `Syn1` or `Syn2`: it has a
stronger developmental/dopaminergic emphasis than the older synapsins
(Porton et al. 2011; Faustini et al. 2022).

Those literature distinctions argue against treating `Syn1` or `Syn2` as exact
phenocopies of `Syn3`, but they do not argue for a broad acute nuclear RNA
response in postmitotic P37-P44 glutamatergic TH/Prkcd/Grin2c neurons. The
decisive same-assay evidence is that both measured synapsin paralogs were at
the floor of the focal endpoint: `Syn1` had only a self-transcript hit and
`Syn2` had zero DEGs. The same pattern extended to the other closest
presynaptic-vesicle and active-zone genes in the training set. `Syp`, `Sv2a`,
`Cplx1`, `Stxbp1`, and `Vamp1` scored as self-only, while `Cplx2`, `Stx1b`,
`Unc13a/b/c`, `Bsn`, and `Pclo` were fully zero. These are mechanistically
appropriate because their primary functions, like Synapsin III, are
presynaptic vesicle organization, priming, or exocytosis rather than direct
transcriptional control.

The main counterexample was `Grin1`: a synaptic receptor gene can produce 89
DEGs in this exact focal population. I treated `Grin1` as a boundary rather
than as a direct analog, because an obligate NMDA-receptor subunit changes
calcium signaling to the nucleus, whereas a partial mosaic `Syn3` loss is more
likely to alter vesicle reserve-pool physiology or dopaminergic release at the
protein/electrophysiological level. The corpus findings for `Syp`, `Sv2a`,
`Syn1`, and `Syn2` made the same broader point in the full experiment: acute
single-gene perturbation of most represented vesicle-cycle genes was buffered
or self-only in snRNA-seq, with broad steady-state nuclear programs being the
exception rather than the rule.

Prediction: `Syn3` should behave like the quiet synapsin/vesicle group, not
like `Grin1`. I predict no focal genes will pass FDR 0.05, including the target
transcript itself, so `predicted_n_degs = 0`.

## Limits

- `Syn3` was completely held out; there is no same-experiment `Syn3` signature,
  no `Syn3` guide efficiency measurement, and no direct `Syn3` protein or DNA
  indel measurement in the provided data.
- A prediction of 0 rather than 1 hinges partly on whether the guide pool will
  make the `Syn3` transcript cross the FDR threshold. The closest assayed
  genes show both outcomes: self-only for `Syn1`, `Syp`, `Sv2a`, `Cplx1`,
  `Stxbp1`, and `Vamp1`, but zero for `Syn2`, `Cplx2`, and `Stx1b`.
- The public `Syn3` literature includes developmental and dopaminergic
  functions. Those functions could be more relevant in a TH-labeled class than
  in an arbitrary glutamatergic class, but many of the cited effects come from
  germline knockout, knockdown, culture, or disease-model settings rather than
  sparse P16 AAV CRISPR in recovered adult neuronal nuclei.
- The predicted endpoint is assay-power-dependent. A real presynaptic
  electrophysiological phenotype could exist with zero FDR-significant nuclear
  RNA genes under this snRNA-seq readout.
