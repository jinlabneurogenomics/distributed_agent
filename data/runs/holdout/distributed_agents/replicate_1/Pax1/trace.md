# Pax1 held-out DEG-count prediction

## Question and endpoint alignment

The task asks for a point prediction of `n_degs` for each requested held-out
perturbation in the `151 TH Prkcd Grin2c Glut` cell group. The endpoint is
directly defined by the supplied experiment: the number of measured genes whose
Wilcoxon differential-expression test had Benjamini-Hochberg adjusted
`pvals_adj < 0.05` in the focal group.

There is only one requested target in
`single-target request for Pax1`:
`Pax1`. `Pax1` was absent from both the focal training-count CSV and from the
training differential-expression parquet, as expected for the held-out target.
Its closest paralog, `Pax9`, was also absent from the visible training panel, so
the prediction uses second-ring in-dataset analogs rather than a direct
Pax1-versus-Pax9 within-experiment comparison.

The requested quantity is directly observed for training perturbations in
`151 TH Prkcd Grin2c Glut`; it is absent for `Pax1`. I therefore treated the
training DEG counts as endpoint-supervised calibration evidence, the all-cell
parquet as exact same-experiment expression evidence for visible analogs, the
PerturbAI July 260713 sourceguard-1773 corpus v1 as a same-experiment
interpretive layer over the same parquet, and PubMed-indexed literature as an
external prior over gene function. No withheld Pax1 DEG count or Pax1
expression signature was available or used.

## Quantitative context from the supplied tables

The focal training CSV contained 1,674 visible perturbations. Its response
distribution was highly zero-inflated: 469 targets had any nonzero focal DEG
count, the median was 0, the 75th percentile was 1, the 95th percentile was 18,
and the maximum was 2,677.

I queried
`training differential-expression dataset`
only for rows in `151 TH Prkcd Grin2c Glut` and for mechanistically relevant
training perturbations. For each comparator I counted rows with
`pvals_adj < 0.05` and `< 0.10`, checked the minimum adjusted p-value, and
recorded the matched perturbed and control nucleus counts. The visible Pax
family and pharyngeal/developmental controls were flat in the requested focal
class:

| training perturbation | focal `n_degs` | minimum focal `pvals_adj` | matched perturbed nuclei | why checked |
|---|---:|---:|---:|---|
| `Pax2` | 0 | 0.936979 | 251 | paired-box developmental factor; closest visible Pax comparator with report-level evidence |
| `Pax3` | 0 | 1.000000 | 196 | Pax developmental regulator, but neural-crest/myogenic rather than Pax1-like |
| `Pax4` | 0 | 1.000000 | 214 | Pax factor with endocrine-pancreas specialization; negative Pax-family control |
| `Pax6` | 0 | 1.000000 | 138 | Pax neurodevelopmental factor; tests whether acute P16 neurons expose a generic Pax response |
| `Pax7` | 0 | 1.000000 | 237 | Pax factor mostly outside the Pax1/Pax9 pharyngeal/sclerotome program |
| `Pax8` | 0 | 1.000000 | 195 | Pax2/5/8 subgroup member, not a Pax1/Pax9 paralog |
| `Hoxa3` | 0 | 1.000000 | 228 | embryonic thymus/parathyroid regulator linked to Pax1 in third-pouch biology |
| `Tbx1` | 0 | 1.000000 | 185 | embryonic pharyngeal/FGF regulator; expected to be active upstream of pharyngeal programs rather than in mature thalamic neurons |
| `Foxn1` | 0 | 0.810708 | 140 | thymic epithelial transcription factor downstream in a Pax1-containing tissue program |
| `Six3` | 0 | 1.000000 | 167 | Six-family developmental regulator; negative developmental-control perturbation |
| `Six5` | 0 | 1.000000 | 215 | Six-family developmental regulator; negative developmental-control perturbation |
| `Foxa2` | 0 | 1.000000 | 213 | lineage transcription factor control with a known neuronal developmental role but no focal effect |
| `Nkx2-1` | 0 | 1.000000 | 246 | developmental transcription factor control |
| `Ptch1` | 0 | 1.000000 | 159 | Hedgehog-pathway receptor; Pax1 is induced downstream of Shh in sclerotome biology |
| `Ptch2` | 0 | 1.000000 | 192 | Hedgehog-pathway receptor control |
| `Gli1` | 0 | 1.000000 | 234 | Hedgehog transcriptional effector control |
| `Gli2` | 0 | 1.000000 | 205 | Hedgehog transcriptional effector control |

The absence of focal FDR hits was not a global lack of power in this cell
class: broad positive controls in the same `151 TH Prkcd Grin2c Glut` query
were readily detected, including `Uba5` with 2,677 DEGs at 245 perturbed nuclei,
`Tpr` with 1,768 DEGs at 114 perturbed nuclei, `Sin3a` with 1,433 DEGs at 176
perturbed nuclei, `Brd4` with 311 DEGs at 93 perturbed nuclei, `Rora` with 278
DEGs at 139 perturbed nuclei, and `Zfp423` with 150 DEGs at 160 perturbed
nuclei.

I also counted significant genes across all recovered cell groups for the
same comparator set. The Pax1-relevant developmental factors stayed nearly
pan-neuronal nulls in the broader parquet: `Pax3`, `Pax4`, `Pax6`, `Foxa2`,
`Foxn1`, `Hoxa3`, `Six5`, `Ptch1`, `Ptch2`, and `Gli2` had 0 genes at
FDR < 0.05 across all their recovered neuronal groups; `Pax2` had 0 at
FDR < 0.05 and one gene at FDR < 0.10 across all 23 groups; `Pax7`, `Six3`,
and `Tbx1` each had only one FDR < 0.05 gene outside the requested focal group.

## Same-experiment corpus evidence

I used the PerturbAI July 260713 sourceguard-1773 corpus v1 only as a packaged
interpretation of the same training experiment, not as independent replication.
Its Hoxa3 report is the most directly relevant internal comparator because
embryonic thymus/parathyroid work places Pax1 in the Hoxa3-linked
third-pharyngeal-pouch network. The corpus summarizes `Hoxa3` as a
pan-measured neuronal null in the P16-to-P37/P44 screen and explicitly reports
that the expected third-pouch and thymus/parathyroid markers `Gcm2`, `Foxn1`,
`Pax1`, `Pax9`, `Tbx1`, `Six1`, `Bmp4`, `Fgf8`, `Ephb2`, and `Pbx1` were not
mobilized by Hoxa3 loss in any measured neuronal group. It also reports no
convergence between `Hoxa3` and visible broader Hox/TALE/pharyngeal relatives
such as `Hoxa1`, `Pbx1`, `Pbx3`, `Meis1`, `Meis2`, `Tbx1`, and `Foxn1`.

The corpus report for `Foxn1`, another tissue-neighbor rather than a neuronal
Pax1 paralog, states that Foxn1 loss of function produced no FDR-supported
downstream transcriptional response in any recovered neuronal class and that
canonical thymic epithelial and hair-keratin Foxn1 effector genes, including
`Pax1` and `Aire`, did not move after Foxn1 perturbation. The `Tbx1` report
similarly describes only a single all-screen hit, no focal `151` response, and
no detectable embryonic Tbx1-FGF/ERK program. The `Pax2`, `Pax3`, `Pax4`, and
`Pax6` reports reinforce the same timing-and-lineage point: visible Pax genes
with well established embryonic functions were silent or nearly silent after
acute mosaic CRISPR in postnatal NeuN-positive neurons.

## External biological prior

`Pax1` and `Pax9` define the paired-box subgroup most relevant to Pax1 biology.
Neubueser, Koseki, and Balling 1995 cloned mouse `Pax9`, described its close
homology to `Pax1`, and reported embryonic expression in pharyngeal pouches,
the developing vertebral column, tail, head, and limbs (Developmental Biology,
doi:10.1006/dbio.1995.1248; PMID:7649395). Muller et al. 1996 showed that
avian `Pax1` and `Pax9` are activated in pharyngeal endoderm and sclerotome by
developmental patterning mechanisms, with sclerotome expression depending on
notochord induction (Developmental Biology, doi:10.1006/dbio.1996.0227;
PMID:8812138). Wallin et al. 1996 reported Pax1 protein in thymic epithelial
development and adult cortical thymic stroma, and showed that Pax1-mutant
undulated mice have thymic and T-cell maturation defects
(Development, doi:10.1242/dev.122.1.23; PMID:8565834).

The thymus/parathyroid literature places Pax1 in a pharyngeal epithelial
developmental circuit rather than a postmitotic thalamic-neuron maintenance
circuit. Su et al. 2001 found that Hoxa3 and Pax1 regulate epithelial cell
survival, proliferation, and differentiation during thymus and parathyroid
organogenesis (Developmental Biology, doi:10.1006/dbio.2001.0342;
PMID:11476574). Zou et al. 2006 showed that Eya1/Six genes and Pax1/Pax9 have
distinct relationships during third-pharyngeal-pouch patterning
(Developmental Biology, doi:10.1016/j.ydbio.2005.12.015; PMID:16530750).

Taken together, the intervention-to-endpoint causal model is:

1. `Pax1` CRISPR loss primarily removes a DNA-binding developmental
   transcription factor.
2. The direct molecular consequence is most consequential in embryonic
   pharyngeal endoderm, thymic/parathyroid epithelium, and sclerotome-like
   mesenchymal contexts where Pax1/Pax9 programs are open.
3. Propagation through Hoxa3, Eya/Six, Foxn1, Tbx1/FGF, or Hedgehog-related
   developmental circuits requires those embryonic tissue programs to be
   accessible.
4. The requested experiment perturbed sparse postmitotic neurons at P16 and
   measured recovered NeuN-positive nuclei at P37-P44, so it largely excludes
   the epithelial, neural-crest, mesenchymal, and early organizer contexts in
   which Pax1 biology is strongest.
5. The measured endpoint is an FDR-count in surviving `151 TH Prkcd Grin2c Glut`
   nuclei. A closed Pax1 developmental program is therefore expected to yield
   no broad focal differential-expression footprint even if some Pax1 alleles
   were edited.

## Target-specific decision

`Pax1`: predict `0` DEGs.

The prediction is driven mainly by within-dataset negative controls, with
external knowledge used to choose which controls were mechanistically
appropriate. Every visible Pax-family perturbation in the requested cell group
had zero DEGs at FDR < 0.05 and also zero at FDR < 0.10. The most relevant
developmental neighbors of Pax1 were not merely weakly positive in the focal
class; `Hoxa3`, `Tbx1`, `Foxn1`, `Six3`, `Six5`, `Ptch1`, `Ptch2`, `Gli1`, and
`Gli2` all had minimum adjusted p-values of 0.81 to 1.0 in the same focal
group. The few nonzero Sox-family controls, `Sox2` and `Sox5`, produced only
two focal DEGs each and are neurodevelopmental comparators rather than
Pax1/Pax9 subgroup or third-pouch/sclerotome analogs.

I did not transfer the strong embryonic Pax1 phenotypes directly to the
requested endpoint because the causal chain is expected to fail at propagation
and exposure: acute Pax1 loss in recovered juvenile thalamic glutamatergic
neurons should not reopen the embryonic pharyngeal/sclerotome epithelial
program that makes Pax1 essential in other tissues. The known role of Pax1
therefore supports choosing the flat Pax/Hoxa3/Tbx1/Foxn1 neighborhood, not the
broad stress-like or chromatin-like perturbations that dominate the upper tail
of the training-count distribution.

## Limits

The closest paralog `Pax9` was also held out, so there was no direct Pax1/Pax9
training signature. The parquet is a survivor-conditioned single-nucleus
readout; it cannot exclude effects on unassayed thymic or skeletal tissues,
earlier embryonic windows, guide-exposed nuclei lost before recovery, or
nontranscriptional phenotypes. DNA indel rates were not measured, and target
RNA self-knockdown is not a valid edit-efficiency score in this atlas. Finally,
all same-experiment corpus statements derive from the same Perturb-seq dataset
as the parquet, so they helped select and interpret analogs but did not provide
independent replication.
