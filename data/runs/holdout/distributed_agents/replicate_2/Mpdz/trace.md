# Question and scope

The run asks for the held-out endpoint for the single requested perturbation in
`151 TH Prkcd Grin2c Glut` cells:

| held-out target | predicted `n_degs` |
| --- | ---: |
| `Mpdz` | 0 |

I treated `n_degs` exactly as the task defines it: the number of measured genes
with `pvals_adj < 0.05` in the focal cell group, including the targeted
transcript itself if the target row is significant. A prediction of zero means
that no measured RNA feature is expected to cross that FDR cutoff in this assay;
it is not a claim that MPDZ has no neuronal, ependymal, or epithelial function.

# Sources

Local experimental evidence:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, the observed focal `n_degs` values for 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for focal per-gene log fold changes and BH-adjusted Wilcoxon p-values.
- The Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`. It had no direct `Mpdz` claim, but it did contain same-experiment claims for the GABA_B cassette, serotonin receptors, hydrocephalus-linked E2f5/Trp73, and post-synaptic scaffold or receptor-scaffold targets.
- A Distributed Agents runtime profile comparison over 20 nominated analogs in the focal cell group. I used it only to audit recurrence and same-direction expression-pattern support among the nominated training perturbations.

External mechanism evidence from PubMed:

- Hamazaki et al. 2001, JBC, DOI `10.1074/jbc.M109005200`, PMID `11689568`: MUPP1/MPDZ is a 13-PDZ tight-junction scaffold that binds claudin-1 and junctional adhesion molecule.
- Balasubramanian et al. 2006, JBC, DOI `10.1074/jbc.M607695200`, PMID `17145756`: MPDZ/MUPP1 binds the GABA_B receptor subunit GABBR2 and modulates receptor stability and signaling duration.
- Parker et al. 2003, JBC, DOI `10.1074/jbc.M210973200`, PMID `12682077`: HTR2C association with MUPP1 is regulated by agonist-induced phosphorylation.
- Adachi et al. 2009, MCB, DOI `10.1128/MCB.01505-08`, PMID `19255144`: MPDZ/MUPP1 and PATJ share tight-junction partners including JAM1, ZO-3, PALS1, Par6, and nectins but are not functionally interchangeable in epithelial polarity.
- Feldner et al. 2017, EMBO Molecular Medicine, DOI `10.15252/emmm.201606430`, PMID `28500065`: mouse Mpdz loss impairs ependymal integrity and causes early postnatal hydrocephalus.
- Yang et al. 2019, EMBO Molecular Medicine, DOI `10.15252/emmm.201809540`, PMID `30518636`: Mpdz-linked hydrocephalus in mice involves choroid-plexus hyperpermeability.
- Marivin and Garcia-Marcos 2019, Molecular Biology of the Cell, DOI `10.1091/mbc.E19-02-0091`, PMID `31268831`: MPDZ directly binds DAPLE/CCDC88C and cooperates with it at apical junctions during neurulation.

# Dataset computations

I loaded the count CSV to calibrate the focal endpoint. The distribution is very
zero-heavy: among 1,674 training perturbations the median is 0 DEGs, the 75th
percentile is 1, the 90th percentile is 2, and the 95th percentile is 18. Thus
a prediction near zero is common for membrane, scaffold, adhesion, and receptor
genes unless a target sits in one of the few recurrent high-response modules.

I then filtered the Parquet file to
`151 TH Prkcd Grin2c Glut` and to mechanistically nominated training targets.
The focal slice contains 28,891,566 rows, one for each measured RNA feature in
each of the same 1,674 training perturbations. For every comparator below I
counted `pvals_adj < 0.05` and inspected whether the significant rows were true
downstream genes or only the target transcript.

I also checked target-transcript behavior in the focal slice. Only 319 of 1,642
training perturbations with a measured self row significantly reduced their own
target transcript at FDR 0.05; 1,175 of those 1,642 had neither a significant
self row nor any DEG. `Mpdz`, as a measured feature in non-Mpdz perturbations,
was stable: all 1,674 training targets had an `Mpdz` row, only three unrelated
perturbations changed it at FDR 0.05, and its median absolute log2 fold change
over those rows was 0.089.

# Same-experiment analogs

## MPDZ receptor partners

The most direct neuronal biochemical analogs are `Gabbr2`, because MPDZ binds
the GABA_B receptor subunit, and `Htr2c`, because 5-HT2C uses a regulated MPDZ
interaction.

| training target | focal `n_degs` | focal FDR genes | why compared |
| --- | ---: | --- | --- |
| `Gabbr2` | 1 | `Gabbr2` only | Direct MPDZ-binding receptor subunit; heterodimerizes with GABBR1. |
| `Gabbr1` | 1 | `Gabbr1` only | Obligate GABA_B partner for GABBR2. |
| `Kctd8` | 0 | none | GABA_B auxiliary subunit. |
| `Kctd16` | 0 | none | GABA_B auxiliary subunit. |
| `Htr2c` | 0 | none | Direct MPDZ/MUPP1-binding receptor. |
| `Htr2a` | 0 | none | Closest assayed 5-HT2/Gq paralog branch. |
| `Htr2b` | 0 | none | Closest assayed 5-HT2/Gq paralog branch. |

Distributed Agents corpus claim `claim:2a5e4f5ac5f372496d27` reports that represented
GABA_B receptor, KCTD auxiliary, GIRK/channel, and proximal effector
perturbations do not form a shared stable neuronal RNA program. The focal
counts above are a strong example: even the strongly depleted `Gabbr2` row
produces no downstream FDR gene. Distributed Agents claims `claim:13062652c8d6749e2518`
and `claim:9f69c85a0a28574c603c` similarly report that serotonin receptors and
neuromodulatory GPCR/second-messenger perturbations are flat, sparse, or
nonconvergent in the basal postnatal snRNA-seq assay. The focal `Htr2a/b/c`
counts agree: no gene crossed FDR 0.05 for any of the three assayed 5-HT2
receptor perturbations.

These are appropriate analogs because they test neuronal plasma-membrane
signaling complexes that physically recruit MPDZ. They are also counterexamples
to a naive interaction rule: loss of a membrane GPCR scaffold or its immediate
receptor partner can change protein stability or evoked signaling without a
steady-state nuclear expression program at this time point.

## MPDZ tight-junction, apical-junction, and hydrocephalus biology

MPDZ's clearest organismal phenotypes come from epithelial or ependymal
junctions and CSF-barrier contexts. The exact MPDZ partners `Ccdc88c`/DAPLE,
`Inadl`/PATJ, and `Mpp5`/PALS1 were not available as training perturbations,
so I used the represented neighboring disease and junction targets as weaker
counterexamples.

| training target | focal `n_degs` | focal FDR genes | why compared |
| --- | ---: | --- | --- |
| `L1cam` | 1 | `L1cam` only | Hydrocephalus gene and neural adhesion comparator. |
| `Ap1s2` | 0 | none | Hydrocephalus-associated trafficking gene. |
| `E2f5` | 0 | none | Hydrocephalus/ciliary-choroid comparator in the corpus. |
| `Trp73` | 0 | none | Multiciliogenesis/ependymal hydrocephalus comparator. |
| `Dll1` | 0 | none | MPDZ can modulate DLL/Notch localization in junctional cells; Dll1 is the represented ligand. |
| `Notch1` | 0 | none | Junctional Notch receptor comparator. |
| `Notch2` | 0 | none | Junctional Notch receptor comparator. |
| `Notch4` | 0 | none | Junctional Notch receptor comparator. |
| `Nectin1` | 0 | none | Nectin/JAM-like adhesion comparator represented in the training set. |
| `Cdc42` | 1 | `Cdc42` only | Polarity/Rho-family effector near apical-junction organization. |

Distributed Agents corpus claim `claim:d24b8df702b0d0760e9e` is especially relevant:
hydrocephalus-linked `Trp73`/`E2f5` ciliary and choroid-plexus programs were not
detectable as cell-autonomous neuronal programs in the NeuN-positive screen.
That is exactly the boundary expected for MPDZ. Feldner et al. and Yang et al.
place the severe Mpdz phenotypes in ependyma or choroid plexus, whereas the
current experiment samples sparse postmitotic NeuN-positive neuronal nuclei and
largely excludes choroid plexus epithelial and ependymal cells.

The represented junctional comparators are therefore negative evidence rather
than precise MPDZ phenocopies. They show that the training set has no sign of a
hidden apical-junction, hydrocephalus, or Notch-adhesion response leaking into
the focal thalamic neuronal group.

## Postsynaptic scaffold counterexamples

MPDZ is a multi-PDZ scaffold, but PDZ-domain membership alone is too broad, so I
used PSD and receptor-scaffold genes only as counterexamples for the idea that
single scaffold losses are generically transcriptionally active.

| training target | focal `n_degs` | focal FDR genes | why compared |
| --- | ---: | --- | --- |
| `Dlg4` | 1 | `Dlg4` only | Canonical PSD-95 PDZ scaffold. |
| `Dlgap4` | 2 | `Dlgap4`, `Vgf` | PSD-associated scaffold; sparse positive exception. |
| `Shank2` | 0 | none | PSD scaffold. |
| `Shank3` | 2 | `Shank3`, `Uba5` | PSD scaffold; sparse positive exception. |
| `Magi2` | 0 | none | Multi-PDZ synaptic scaffold. |
| `Homer2` | 0 | none | mGluR/PSD scaffold. |
| `Frmpd4` | 0 | none | FERM and PDZ-domain synaptic scaffold. |
| `Gphn` | 0 | none | Inhibitory-synapse scaffold. |

Distributed Agents claims `claim:da426d57898fc5cde54d` and
`claim:c0a95241aec700bec1c8` summarize this assay-level boundary: many
represented synaptic adhesion and PSD-associated receptor-scaffold perturbations
were flat, singleton, or non-overlapping, rather than forming a shared broad
downstream module. The focal data are consistent with that: these PDZ/scaffold
comparators produced zero to two DEGs, and usually the only significant row was
the targeted transcript itself.

# Expression-pattern audit

I profiled a 20-node cohort covering the nominated GABA_B, serotonin,
hydrocephalus/junction, and PSD analogs with the Distributed Agents runtime. Thirteen of
the twenty had no significant focal RNA feature and the remaining seven had
only one or two in the direct FDR count. Across all 190 pairwise comparisons,
the selected cohort had no recurrent significant positive program and only
zero-overlap negative significant pairs; mean top-tail overlap was low
(`0.075` for positive tails and `0.133` for negative tails among the top 200
features). This did not identify any expression-defined submodule that would
justify moving `Mpdz` above the zero-to-singleton range.

# Target-specific prediction

## `Mpdz`: predicted `0`

The external biology says MPDZ/MUPP1 is a scaffold at cell junctions and at
selected receptor complexes, not a transcription factor or chromatin component.
Its direct neuronal receptor partners were the most informative training
comparators, and they were effectively null in the focal group: `Gabbr2` and
`Gabbr1` each had only a self-transcript DEG, while the auxiliary `Kctd8` and
`Kctd16` perturbations had zero; `Htr2c`, `Htr2a`, and `Htr2b` were also zero.
Its strongest developmental and disease functions map to ependymal,
choroid-plexus, epithelial, or neurulation junctional contexts that are absent
or badly under-sampled in NeuN-enriched postnatal nuclei; the assayed
hydrocephalus and junction comparators `E2f5`, `Trp73`, `Ap1s2`, `Dll1`,
`Notch1`, `Notch2`, `Notch4`, and `Nectin1` all had zero focal DEGs.

I therefore expect acute sparse CRISPR loss of `Mpdz` in juvenile postmitotic
`151 TH Prkcd Grin2c Glut` neurons to be buffered at the nuclear RNA level. I
considered a singleton prediction for possible depletion of the `Mpdz`
transcript itself, but the training set shows that target self-detection is not
automatic, and the closest low-level scaffold or receptor analogs are split
between self-only and complete null. Because the downstream evidence is
overwhelmingly zero and MPDZ-specific ependymal partners were not active or not
represented in this focal neuronal context, the best integer point prediction
is:

`Mpdz = 0`

# Limits

The main uncertainty is target-transcript detectability. Held-out `Mpdz`
perturbed nuclei are absent from the Parquet, so the focal data cannot say
whether the pooled Mpdz guides would have made `Mpdz` itself cross FDR 0.05.
A true one-DEG self-only result is plausible.

The best MPDZ-specific epithelial/apical partners, `Ccdc88c`/DAPLE,
`Inadl`/PATJ, and `Mpp5`/PALS1, were not non-held-out training perturbations in
this focal count table. I therefore had to use weaker hydrocephalus, junction,
Notch, adhesion, receptor, and generic scaffold counterexamples.

MPDZ protein loss could perturb local receptor retention, tight-junction
composition, ependymal barrier integrity, CSF flow, or apical constriction
without producing a stable snRNA-seq signature in postnatal NeuN-positive
thalamic glutamatergic nuclei. The prediction is an assay-specific FDR-count
prediction under partial mosaic CRISPR loss, not an estimate of MPDZ biological
importance.
