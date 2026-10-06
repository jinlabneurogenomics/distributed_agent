# DEG-count prediction for held-out Ano3

## Question and ambiguity handling

The held-out manifest for this run contains one requested perturbation:

```text
Ano3
```

I interpreted the requested scalar as the exact `n_degs` endpoint used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured
genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` in the Wilcoxon
comparison of a perturbation against matched non-targeting controls. The
training counts include the targeted transcript itself when it passes FDR, so
I treated single-gene, self-only events such as `Kcnma1 = 1` as valid examples
of the endpoint. I did not treat self-target RNA loss as an editing-efficiency
score, because the experiment's nuclear target mRNA change is not a reliable
proxy for functional indel burden.

## Sources used

- Training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression profiles:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest:
  `[local file: 011_Ano3.csv]`.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. The corpus had no
  `Ano3`-specific Finding or Claim, but it contained interpreted
  same-experiment Findings for the training comparators below.
- Distributed Agents runtime profile comparison over a run-local 151-class comparator
  panel, used to check FDR-level overlap among channel and calcium signatures.
- PubMed-indexed external literature on ANO3/TMEM16C function and disease.

## Computation on the training data

The training count table has 1,674 non-held-out targets in the focal cell group:

- 1,205/1,674 targets have `n_degs = 0`.
- 363 have 1-9 DEGs.
- 63 have 10-99 DEGs.
- 43 have at least 100 DEGs.
- The median is 0, the 75th percentile is 1, and the 95th percentile is 18.

I avoided loading the full 616,253,184-row parquet at once. I used the parquet
row-group metadata to find row groups whose `group_name` range included
`151 TH Prkcd Grin2c Glut`, read only `names`, `gene_target`,
`logfoldchanges`, `scores`, and `pvals_adj` from those row groups, filtered to
the focal cell group, and then retained the biologically selected candidate
genes. For each candidate I counted rows with `pvals_adj < 0.05`, checked that
the count matched the training CSV, and inspected the significant genes.

Exact focal counts for the main analogs and counterexamples were:

| training perturbation | focal `n_degs` | observed 151-class expression pattern |
|---|---:|---|
| `Kcnt1` | 0 | no FDR 0.05 genes |
| `Kcnt2` | 0 | no FDR 0.05 genes |
| `Kcnn2` | 0 | no FDR 0.05 genes |
| `Kcnn3` | 0 | no FDR 0.05 genes |
| `Kcnma1` | 1 | `Kcnma1` self-transcript only |
| `Kcnq2` | 1 | `Kcnq2` self-transcript only |
| `Kcnq3` | 1 | `Kcnq3` self-transcript only |
| `Cacna1g` | 12 | Cav3.1-specific thalamic program, including `Cacna1g` down, `Ptprn` up, `Stmn4`/`Cpne7`/`Jun` down |
| `Atp2b1` | 22 | PMCA1 activity-like program, including `Atp2b1` down, `Fos`, `Nr4a1`, `Vgf`, `Ptprn`, and `Chml` up |
| `Ppp3r1` | 9 | calcineurin-regulatory signature with `Pcsk1n`, `Ptprs`, `Atp2a2`, `Coro6`, and `Septin4` |
| `Ppp3ca` | 4 | sparse calcineurin-catalytic response, mostly not shared with `Ppp3r1` |
| `Calm1` | 14 | small thalamic calmodulin-locus response with `Rasgrp2`, `Peg3`, `Aifm3`, `Tuba1b`, `Resp18` |
| `Calm2` | 0 | no FDR 0.05 genes |
| `Calm3` | 1 | `Calm3` self-transcript only |
| `Atp2a2` | 187 | SERCA2-specific ER-stress/UPR-ISR state, with `Ddit3`, `Chac1`, `Xbp1`, `Hspa5`, `Asns`, `Shmt2` up |
| `Cacna1a` | 0 | no FDR 0.05 genes |
| `Cacna1d` | 0 | no FDR 0.05 genes |
| `Cacna1e` | 0 | no FDR 0.05 genes |
| `Cacna2d2` | 0 | no FDR 0.05 genes |
| `Cacnb2` | 0 | no FDR 0.05 genes |
| `Cacnb4` | 1 | `Cacnb4` self-transcript only |
| `Thap1` | 7 | isolated-dystonia transcription-factor signature, including `Prepl` and `Cuedc2` down, `Tomm40l`, `Pet100`, `Fam117a` up |
| `Gnal` | 0 | no 151-class FDR 0.05 genes |
| `Sgce` | 0 | no 151-class FDR 0.05 genes |
| `Slc2a1` | 0 | no 151-class FDR 0.05 genes |
| `Pde10a` | 0 | no 151-class FDR 0.05 genes |
| `Pnkd` | 0 | no 151-class FDR 0.05 genes |

I also compared FDR 0.05 signatures pairwise within this panel. The closest
training genes to ANO3's channel-regulatory biology were not hiding a common
subthreshold program: `Kcnt1` and `Kcnt2` both had empty FDR sets, `Kcnma1`
shared no FDR gene with `Cacna1g`, and `Kcnt1` shared no FDR gene with
`Cacna1g`, `Atp2b1`, `Ppp3r1`, or `Calm1`. The only notable small overlap in
the positive calcium branch was a single shared gene, `Ptprn`, between
`Cacna1g` and `Atp2b1`; the broad overlap was restricted to the SERCA2 ER
stress outlier, where `Atp2b1` and `Atp2a2` shared five FDR genes
(`Chml`, `Fos`, `Gpr88`, `Vgf`, `Xylt2`).

## Ano3-specific reasoning

`Ano3` encodes anoctamin-3/TMEM16C, a TMEM16-family protein. TMEM16 members
split between Ca2+-activated chloride channels and Ca2+-activated phospholipid
scramblases; Suzuki et al. showed that TMEM16C/ANO3 falls on the scramblase
side in a heterologous assay rather than the TMEM16A/B chloride-channel side
(Suzuki 2013, DOI 10.1074/jbc.M113.457937, PMID 23532839). Later work found
human TMEM16C isoforms at the plasma membrane can expose phosphatidylserine
without robust ion transport (Kim 2022, DOI 10.3390/membranes12101005, PMID
36295764). In neurons, the most direct functional data connect TMEM16C to local
excitability control: Huang et al. reported that TMEM16C in rat sensory neurons
enhances the Slack/KCNT1 sodium-activated K+ current and dampens excitability
(Huang 2013, DOI 10.1038/nn.3468, PMID 23872594). A rodent study of neuronal
Tmem16c deletion found thermoregulation and febrile-seizure susceptibility
phenotypes, again pointing to excitability and circuit physiology rather than
a constitutive broad stress transcriptome (Wang 2021, DOI
10.1073/pnas.2023342118, PMID 33972431).

The human genetics also argue for a movement-disorder/excitability axis.
Heterozygous ANO3 variants cause the DYT24 form of autosomal dominant dystonia
with tremor and craniocervical onset in many families (Stamelou 2014, DOI
10.1002/mds.25802, PMID 24442708; Blackburn 2016, DOI
10.1186/s12881-016-0354-7, PMID 27919237). More recent functional work reports
that disease variants can disrupt Ca2+ signalling and Ca2+-dependent K+ channel
activation (Ousingsawat 2024, DOI 10.1093/brain/awad412, PMID 38079528).
Those disease observations increase confidence that ANO3 matters in neurons,
but they mostly involve heterozygous missense variants, human basal-ganglia
and movement networks, and electrophysiological mechanisms rather than a
juvenile mosaic loss-of-function RNA response in a thalamic glutamatergic cell
class.

Within the supplied experiment, the biologically nearest measured training
perturbations are therefore the Slack/Slo/SK/KCa channel branch
(`Kcnt1`, `Kcnt2`, `Kcnma1`, `Kcnn2`, `Kcnn3`) and the Ca2+-calmodulin
regulators that could plausibly couple to Ca2+-dependent ANO3 function
(`Calm1`, `Calm2`, `Calm3`, `Ppp3r1`, `Ppp3ca`). The Slack/Slo/SK branch was
almost completely FDR-null in the exact focal group: 0, 0, 0, 0, and one
self-only gene for `Kcnma1`. The Distributed Agents corpus independently summarizes this
as a lack of a shared neuronal loss-of-function transcriptional module among
represented Na+- and Ca2+-activated potassium-channel perturbations in the
same experiment. That is the strongest training evidence because ANO3's best
documented neuronal molecular neighbor is Slack/KCNT1.

The Ca2+-calmodulin branch provides positive counterexamples rather than direct
analogs. `Calm1`, `Ppp3r1`, and `Ppp3ca` crossed FDR in the focal group, but
with small, branch-specific gene sets, while `Calm2`, `Calm3`, `Ppp3cc`,
`Kcnn2`, and `Kcnn3` were zero or self-only. The same-experiment corpus reports
that these perturbations do not collapse into one shared Ca2+-calmodulin RNA
signature. That argues against assigning ANO3 the 9-14 DEG counts from
`Ppp3r1` or `Calm1` just because ANO3 is Ca2+ regulated.

The voltage-gated calcium-channel comparators show why I allowed a nonzero
ANO3 prediction only if a target is thalamus-specific in the way `Cacna1g` is.
`Cacna1g` has a real 12-gene 151-class response, but the other represented
CaV pore or auxiliary perturbations are 0 or self-only in the same cell group.
The Distributed Agents corpus calls the `Cacna1g` state Cav3.1-specific and narrowly
thalamic, not a generic Ca2+-channel response. ANO3 has no comparable role as a
defining thalamic burst-firing CaV3.1 pore, so `Cacna1g` is an upper-bound
counterexample rather than a direct donor.

Finally, disease-category analogs do not rescue a positive call. The isolated
or paroxysmal dystonia genes represented in the focal training set were mostly
silent: `Gnal`, `Sgce`, `Slc2a1`, `Pnkd`, and `Pde10a` each had 0 focal DEGs,
while `Thap1` had a 7-gene transcription-factor module unrelated to ANO3.
The same-experiment corpus also separates `Gnal` and `Thap1` rather than
merging all dystonia genes into one signature. ANO3's DYT24 relationship is
therefore not enough to expect a shared 151-class RNA footprint.

Taken together, the direct local analogs favor the training distribution's
`none` class. A prediction of 1 would only be justified if ANO3's own nuclear
transcript were expected to be detectably knocked down in `151 TH Prkcd Grin2c
Glut`; the available data do not establish that expression or RNA engagement,
and the closest channel comparators frequently had no downstream or self call.
I therefore assign the point prediction to zero.

## Final point prediction

| target | predicted `n_degs` |
|---|---:|
| `Ano3` | 0 |

## Limits of the reasoning

- No same-experiment `Ano3` Finding or Claim existed in the selected Distributed Agents
  corpus, and `Ano3` itself is completely absent from the training DE profiles
  by design. The prediction is an extrapolation from mechanism-matched
  training genes.
- No other `Ano*` paralog was present as a non-held-out training perturbation
  in the focal count table, so I could not calibrate Anoctamin-family paralogs
  directly.
- The closest external literature for ANO3 is dominated by sensory-neuron,
  striatal, hypothalamic, heterologous-cell, or human missense-variant
  contexts. Those are imperfect matches to acute P16 mosaic CRISPR loss of
  function in mouse thalamic glutamatergic neurons.
- The endpoint is a BH-FDR count at one postnatal harvest. A zero prediction
  means I do not expect any measured gene to pass `pvals_adj < 0.05`; it does
  not mean ANO3 editing would be ineffective, that ANO3 has no
  electrophysiological consequence, or that evoked activity, K+ currents, Ca2+
  fluxes, or phospholipid scrambling would be normal.
