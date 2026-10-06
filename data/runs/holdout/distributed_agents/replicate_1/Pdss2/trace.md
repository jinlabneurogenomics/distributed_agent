# Pdss2 held-out DEG-count prediction

## Question and endpoint

The held-out target list for this run contains one perturbation, `Pdss2`. I
interpreted the endpoint as an integer count of measured genes with
`pvals_adj < 0.05` after `Pdss2` perturbation in the recovered
`151 TH Prkcd Grin2c Glut` nuclei. The count is specific to this focal cell
class, the AAV-PHP.eB postnatal mosaic CRISPR design, the P16-to-P37/44 time
window, and the Scanpy Wilcoxon/BH pipeline. I did not treat weak measured
self-transcript loss as failed editing, and I treated survivor-state snRNA-seq
as a differential-expression endpoint rather than a direct assay of CoQ level,
respiration, cell loss, or viability.

## Sources used

- Declared endpoint counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared per-gene differential-expression parquet:
  `training differential-expression dataset`.
- Requested held-out manifest:
  `single-target request for Pdss2`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, especially the packaged
  `Coq5` report and Findings `Coq5:F001`-`Coq5:F004`. This corpus is a
  curated interpretation of the same Perturb-seq experiment, not independent
  replication.
- External literature from PubMed/GeneReviews for the CoQ pathway:
  Lopez et al. 2006, DOI `10.1086/510023`, PMID `17186472`; Peng et al. 2008,
  DOI `10.1371/journal.pgen.1000061`, PMID `18437205`; Nguyen et al. 2014,
  DOI `10.1016/j.bbalip.2014.08.007`, PMID `25152161`; Malicdan et al. 2017,
  DOI `10.1002/humu.23345`, PMID `29044765`; Ziosi et al. 2017, DOI
  `10.15252/emmm.201606356`, PMID `27856618`; Fessler et al. 2020, DOI
  `10.1038/s41586-020-2076-4`, PMID `32132706`; Sasaki et al. 2020, DOI
  `10.1042/BSR20201289`, PMID `33165592`; and Salviati, Trevisson, and Agosto,
  *Primary Coenzyme Q10 Deficiency Overview*, GeneReviews, updated 2023.

## Computational checks

The requested-target CSV contains exactly one row, `Pdss2`, with no duplicate
targets and no overlap with the 1,674-row training count table. I summarized
the training table in the focal cell group and found a zero-heavy endpoint
distribution:

- 469 of 1,674 training perturbations had `n_degs > 0`.
- median `n_degs` was 0, the 75th percentile was 1, the 90th percentile was 2,
  and the 95th percentile was 18.
- The endpoint was highly skewed; only the top 1% exceeded about 436 DEGs.

For pathway-local analogs, the focal-cell training count table contained no
`Pdss1`, `Coq2`, `Coq3`, `Coq4`, `Coq6`, `Coq7`, `Coq8a`, `Coq8b`, `Coq9`,
`Coq10a`, `Coq10b`, `Adck1`, `Adck2`, `Adck5`, or `Ubiad1` rows. The only
direct CoQ-biosynthesis perturbation present was `Coq5`, with 0 DEGs.

I then read the focal-cell parquet rows for the most relevant represented
mitochondrial comparators and counted `pvals_adj < 0.05` per target. The direct
CoQ anchor and nearby electron-transport perturbations were almost all
silent or self-transcript-only:

| training perturbation | focal `n_degs` | strongest focal-cell evidence |
| --- | ---: | --- |
| `Coq5` | 0 | no gene below FDR 0.05; best focal hit `Wasl`, FDR 1.000 |
| `Uqcrb` | 0 | no gene below FDR 0.05 |
| `Uqcrfs1` | 0 | self-target `Uqcrfs1` was still only FDR 0.199 |
| `Uqcrh` | 0 | no gene below FDR 0.05 |
| `Uqcrc2` | 1 | only self-target `Uqcrc2`, FDR 0.0030 |
| `Cox5a` | 1 | only self-target `Cox5a`, FDR 5.39e-21 |
| `Ndufa10` | 1 | only self-target `Ndufa10`, FDR 4.84e-7 |
| `Ndufs2` | 1 | only self-target `Ndufs2`, FDR 8.26e-12 |
| `Sdha` | 1 | only self-target `Sdha`, FDR 2.11e-12 |
| `Clpp` | 0 | no gene below FDR 0.05 |

The same-experiment `Coq5` report provided a broader check beyond the focal
class. `Coq5` was measured in 22 neuronal groups and all 22 had zero downstream
genes at FDR < 0.10; the focal group had 200 perturbed nuclei and 23,679
matched controls with `Coq5` logFC -0.473 and FDR 1.000. The internal corpus
also reported that `Coq5` did not induce the expected mitochondrial
ATF4/CHOP/ISR genes (`Atf4`, `Ddit3`, `Trib3`, `Herpud1`, `Asns`, `Shmt2`,
`Aldh1l2`, `Mthfd2`, `Lonp1`, `Hspd1`, `Hspa5`, `Clpp` all had minimum
FDR 1.000 across measured `Coq5` groups) even though the same parquet detected
those transcripts after other perturbations. In score-vector space across
matched groups, `Coq5` also had essentially zero correlation with represented
ubiquinone-linked or mitochondrial-stress comparators: `Uqcrfs1` r=0.0169,
`Uqcrc2` r=0.0187, `Cyc1` r=0.0077, `Uqcrb` r=0.0031, `Ndufs2` r=0.0068,
`Ndufc2` r=0.0146, `Clpp` r=0.0088, and `Lonp1` r=0.0015.

## Target-specific reasoning

### Pdss2

`Pdss2` encodes a subunit of decaprenyl diphosphate synthase, the enzyme that
generates the polyprenyl side chain for coenzyme Q10 biosynthesis. Human
biallelic `PDSS2` mutations cause primary CoQ10 deficiency with Leigh syndrome,
nephropathy, severe reduction of CoQ10, and impaired decaprenyl diphosphate
synthase activity (Lopez et al. 2006). A mouse `Pdss2` missense model had
primary CoQ9/CoQ10 deficiency, with the renal phenotype traced to podocytes
(Peng et al. 2008), and severe Pdss2 deficiency can also impair sulfide
oxidation in a tissue-threshold-dependent way (Ziosi et al. 2017). The
biological prior is therefore that a strong and chronic biallelic hit to
`Pdss2` can matter greatly.

The experiment requested here is a much weaker and more buffered intervention:
four pooled CRISPR guides delivered sparsely to postmitotic neurons at P16 and
read out in survivor nuclei 3 to 4 weeks later. The causal chain for a
transcriptional response is:

`Pdss2` indels -> reduced decaprenyl diphosphate synthase activity -> reduced
ubiquinone/CoQ pool -> complex I/II-to-III electron-transfer, redox, sulfide,
or mitochondrial proteostasis stress -> survival and recovery of edited
thalamic glutamatergic nuclei -> enough coordinated nuclear-RNA shifts for
individual genes to pass BH FDR 0.05.

The strongest training perturbation in that chain is `Coq5`, a mitochondrial
CoQ C-methyltransferase that functions in the same CoQ synthome and whose loss
causes primary CoQ10 deficiency in humans (Nguyen et al. 2014; Malicdan et al.
2017). `Coq5` sits after the polyprenyl-tail step catalyzed by the
PDSS1/PDSS2 enzyme, so it is not an obligate physical partner of `Pdss2`, but
it should reduce the same metabolite pool if acute neuronal editing crosses
the CoQ-depletion threshold. In the actual training data `Coq5` caused 0 DEGs
in the requested focal class and no downstream FDR < 0.10 response in any of
22 measured neuronal classes. This is the decisive within-dataset analog.

I considered whether `Pdss2` should be higher than `Coq5` because it is at the
first committed polyisoprenoid-tail step. The external disease literature
supports the possibility under germline or near-complete biochemical
deficiency, but the in-dataset counterexamples argue against a broad focal
snRNA footprint from this acute perturbation strength. Complex III subunits
that consume ubiquinone-derived electrons were at 0 or 1 DEG in the focal
class (`Uqcrb` 0, `Uqcrfs1` 0, `Uqcrh` 0, `Uqcrc2` 1, `Uqcrq` 1 in the count
table), complex I subunits were similarly 0 or 1, `Sdha` was 1, and `Cox5a`
was 1. The single-DEG calls for `Uqcrc2`, `Cox5a`, `Ndufa10`, `Ndufs2`, and
`Sdha` were their own self-target transcripts rather than a shared
mitochondrial-stress program. `Clpp`, a mitochondrial proteostasis/stress
perturbation that the `Coq5` corpus report used as a stress counterexample,
also had 0 focal DEGs.

A mitochondrial integrated stress response would have been a biologically
plausible nonzero mechanism: OMA1-DELE1-HRI can relay mitochondrial stress to
eIF2alpha and CHOP/DDIT3 (Fessler et al. 2020), and mitochondrial translation
inhibition can activate ATF4-dependent ISR genes in mouse brain (Sasaki et al.
2020). The CoQ anchor specifically failed to show that program, whereas the
same Perturb-seq analysis could detect `Ddit3`, `Herpud1`, `Shmt2`, and
`Hspa5` after other perturbations. That makes `Coq5` an informative negative
analog rather than a generic low-power zero.

I therefore predict `Pdss2` to behave like `Coq5`: a CoQ-biosynthetic lesion
with plausible biochemical consequences but no gene reaching focal-cell
BH FDR 0.05 in this assay. The external pathway prior comes mainly from
complete or chronic CoQ10-deficiency models and patients; the count prediction
is driven primarily by the within-dataset observation that the closest
available CoQ perturbation and represented respiratory-chain comparators were
nearly silent.

Predicted focal-cell DEG count: **0**.

## Limits

- `Pdss1` and almost all other CoQ-synthome genes were absent from the
  non-held-out training set, so `Coq5` is a pathway analog, not a one-to-one
  obligate-complex transfer.
- The declared Parquet has no `Pdss2` rows by construction. I did not observe
  `Pdss2` editing, target transcript loss, CoQ abundance, respiratory flux,
  sulfide oxidation, or selective survival.
- The CoQ literature mostly concerns human fibroblasts, germline biallelic
  disease, mouse renal podocytes, Drosophila development, or systemic
  deficiency. Those sources define function and possible consequences, but the
  juvenile sparse neuronal CRISPR endpoint is assay- and threshold-dependent.
- A value of 0 is a point prediction for the BH FDR 0.05 count, not a claim
  that `Pdss2` is biologically inert or that CoQ metabolism is unperturbed.
