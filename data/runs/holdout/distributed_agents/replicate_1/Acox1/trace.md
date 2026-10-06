# DEG-count prediction for held-out Acox1

## Question and endpoint

I interpreted the requested endpoint as the exact `n_degs` count used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: for a held-out perturbation,
predict how many measured genes in recovered `151 TH Prkcd Grin2c Glut`
neuronal nuclei will have `pvals_adj < 0.05` in the Wilcoxon differential
expression table.  The count includes the target transcript itself if that row
passes FDR; for example, `Pex14` has one focal DEG in the training endpoint even
though its only `pvals_adj < 0.05` focal row in my raw extraction was the `Pex14`
self transcript.

The held-out manifest has one requested target, `Acox1`, and it is absent from
both the training count CSV and the training DE parquet.  This is therefore a
scalar response-breadth prediction, not a ranking.

## Sources

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE parquet:
  `training differential-expression dataset`.
- Held-out target manifest:
  `single-target request for Acox1`.
- Distributed Agents PerturbAI dataset portrait and measurement registry, which identify
  the parquet as per-gene relative-expression DE over recovered NeuN+ nuclei and
  warn that this assay does not directly measure lipid species, indels, protein
  loss, guide-exposure denominators, cell loss before recovery, or absolute RNA
  content.
- Same-experiment internal corpus
  `perturbai-july-260713-sourceguard-1773-v1`, release date 2026-09-01.  I used
  its Findings, Pathways, and resolved Evidence/References for peroxisomal
  training perturbations; these are interpreted views of the same experiment,
  not independent replication.
- External mechanism priors from PubMed-indexed literature, especially reviews
  of peroxisomal beta-oxidation and brain peroxisome biology plus papers on
  ACBD5, HSD17B4/MFP2, PEX14/PEX1, and ACOX1 listed below.

## Dataset calculations

I first read the held-out manifest and verified it contained exactly:

```text
Acox1
```

Then I summarized the focal training endpoint.  Among 1,674 non-held-out
perturbations in `151 TH Prkcd Grin2c Glut`, 469 had any `pvals_adj < 0.05`
DEG.  The distribution is very zero-inflated: median 0, 75th percentile 1, 90th
percentile 2, 95th percentile 18, 99th percentile 436.48, and maximum 2,677.

I searched the training target names for peroxisome and lipid-metabolism
neighbors of `Acox1`.  The closest represented focal endpoint counts were:

| training target | focal `n_degs` | relationship to ACOX1 |
| --- | ---: | --- |
| `Abcd3` | 0 | peroxisomal ABC transporter delivering fatty-acyl substrates |
| `Acbd5` | 0 | peroxisome-ER/VLCFA handling factor upstream of VLCFA beta-oxidation |
| `Hsd17b4` | 0 | D-bifunctional protein, core peroxisomal beta-oxidation enzyme |
| `Pex1` | 0 | peroxin AAA ATPase needed for matrix-protein import |
| `Pex14` | 1 | PEX5/PEX7 docking factor needed for peroxisomal matrix import; the one focal call is the target transcript |
| `Ppara` | 0 | lipid-catabolic nuclear receptor regulating `Acox1` in liver |
| `Ppard` | 0 | PPAR/RXR lipid-regulatory nuclear receptor, flat in neurons here |

I extracted a narrow focal-cell subset from the parquet for these targets,
retaining FDR < 0.10 rows and sentinel rows for `Acox1`, `Abcd1`, `Abcd2`,
`Abcd3`, `Acbd5`, `Hsd17b4`, `Pex1`, `Pex5`, `Pex6`, `Pex14`, `Ppara`,
`Ppard`, `Srebf1`, `Srebf2`, `Ddit3`, `Atf4`, `Hspa5`, `Sqstm1`, and `Cat`.
In `151 TH Prkcd Grin2c Glut`, `Abcd3`, `Acbd5`, `Hsd17b4`, `Pex1`, `Ppara`,
and `Ppard` had no FDR < 0.10 rows among either the sentinel genes or all
non-self measured genes.  `Pex14` had a strong self-transcript decrease
(`logfoldchanges = -0.907`, `pvals_adj = 3.74e-7`) but no downstream sentinel
or non-self FDR row.  The measured `Acox1` row under all seven neighbor
perturbations had `pvals_adj = 1.0`, so these neighboring perturbations did not
drive transcriptional compensation of `Acox1` itself.

## Target-specific reasoning

### `Acox1`

`Acox1` encodes acyl-CoA oxidase 1, the first/rate-limiting enzyme for
straight-chain very-long-chain acyl-CoA oxidation in peroxisomes and a generator
of peroxisomal H2O2.  That places an `Acox1` perturbation in the same causal
module as peroxisomal fatty-acid import and HSD17B4/MFP2-mediated beta-oxidation:

1. the intervention is acute sparse CRISPR loss of `Acox1`;
2. the direct molecular consequence should be reduced ACOX1 enzyme activity in
   edited neurons;
3. pathway propagation should be accumulation of some straight-chain VLCFA
   substrates and reduced peroxisomal beta-oxidation flux, with possible
   secondary redox, lipid-feedback, sterol, ISR/UPR, autophagy, or glial
   inflammatory biology depending on context;
4. the requested endpoint is much later nuclear RNA in recovered postmitotic
   thalamic glutamatergic nuclei, not lipidomics, glia, or survivor depletion.

The decisive within-dataset evidence is that directly represented lesions
around this module were transcriptionally buffered in the same endpoint:

- `Hsd17b4`, the beta-oxidation enzyme immediately downstream in peroxisomal
  fatty-acid oxidation, had `n_degs = 0` in 151 cells.  Its report called it a
  pan-measured neuronal transcriptional null with 0 downstream genes at
  FDR < 0.10 in all 21 recovered groups.  The HSD17B4 expected program panel,
  including `Acox1`, `Scp2`, `Abcd1`, `Abcd2`, `Abcd3`, `Acbd5`, `Pex1`,
  `Pex5`, `Pex14`, `Pex19`, `Ppara`, `Ppard`, `Ppargc1a`, `Srebf2`, `Hmgcr`,
  `Hspa5`, `Atf4`, and `Ddit3`, had 0 rows at FDR < 0.10 and minimum adjusted
  p value 1.0 across the Hsd17b4 contrasts.
- `Abcd3`, a peroxisomal fatty-acyl importer tied to HSD17B4-containing
  oxidation, had `n_degs = 0` in 151 cells and 0 downstream genes at FDR < 0.10
  in 22 measured neuronal groups.  Its peroxisomal transporter, beta-oxidation,
  antioxidant, ether-lipid, and peroxin sentinel genes, including `Acox1`, had
  adjusted P = 1.0 in each measured group.
- `Acbd5`, which handles VLCFA-CoA binding and ER-peroxisome tethering, had
  `n_degs = 0` in 151 cells and no robust downstream response in 22 recovered
  cell groups.  Its expected peroxisomal beta-oxidation, sterol, UPR/ISR, and
  autophagy/lysosome sentinel rows were all at FDR = 1.0.
- `Pex1` and `Pex14`, upstream peroxisomal matrix-import perturbations, are
  expected to impair import of peroxisomal beta-oxidation enzymes more broadly
  than `Acox1` itself.  Yet `Pex1` had `n_degs = 0` in the focal group, and
  `Pex14` had `n_degs = 1` only because its own transcript crossed FDR in the
  focal group; both were reported as failing to trigger peroxisome-import,
  lipid, redox, pexophagy/autophagy, ISR, or UPR modules in the neuronal RNA
  surface.
- `Ppara` and `Ppard`, which bound the possibility that ACOX1 loss might feed
  back through a PPAR/RXR lipid-catabolic transcriptional circuit, had focal
  `n_degs = 0`.  Their reports found no canonical `Acox1`, fatty-acid transport,
  beta-oxidation, or lipid-droplet target-gene response in this basal postnatal
  neuronal assay.

There are two relevant sparse counterexamples.  `Agps`, a peroxisomal
ether-lipid enzyme, caused three focal FDR < 0.10 genes (`Dhcr24`, `Cyp51`,
`Lmtk3`) in a small thalamic sterol/membrane response, and `Far1` caused two
FDR < 0.10 genes across all measured groups, including `Tial1` in 151 cells.
I did not transfer those small nonzero counts to `Acox1` because AGPS/FAR1 act
in ether-lipid/plasmalogen synthesis rather than straight-chain beta-oxidation,
and same-experiment contrast Findings explicitly concluded that `Agps` and
`Far1` did not phenocopy `Pex1`, `Pex14`, `Hsd17b4`, `Abcd3`, or `Acbd5`.
Their few calls show the assay could detect occasional peroxisome-linked lipid
responses, but those responses were not a generic consequence of weakening the
ACOX1/HSD17B4/ABCD3 axis.

The external literature argues that the gene is biologically real, not that the
acute neuronal DEG-count endpoint should be broad.  Peroxisomes chain-shorten
VLCFAs and related fatty acids, with acyl-CoA oxidases catalyzing the first
oxidation step (Reddy and Hashimoto 2001, DOI 10.1146/annurev.nutr.21.1.193;
Rao and Reddy 2001, DOI 10.1055/s-2001-12928).  `Acox1`-null mouse liver
develops steatohepatitis, PPARalpha activation, progressive ER stress, and
tumors (Vluggens et al. 2010, PMID 20195242; Huang et al. 2011, DOI
10.1016/j.ajpath.2011.04.030), and liver-specific Acox1 loss changes
peroxisome-derived acetyl-CoA and mTORC1/autophagy (He et al. 2020, DOI
10.1016/j.molcel.2020.05.007).  ACOX1 deficiency is linked to VLCFA
accumulation and neurodegeneration in glial or organismal settings (Raas et al.
2018, DOI 10.1016/j.bbalip.2018.10.005; Chung et al. 2020, DOI
10.1016/j.neuron.2020.02.021).  ACBD5, ABCD3, HSD17B4, and PEX factors provide
the training analogs because ACBD5 is a peroxisomal VLCFA-CoA/ER-tethering
factor (Yagita et al. 2017, DOI 10.1074/jbc.M116.760090; Hua et al. 2017, DOI
10.1083/jcb.201608128), ABCD3 and HSD17B4 feed into peroxisomal fatty-acid
oxidation (Violante et al. 2019, DOI 10.1096/fj.201801498R), and PEX1/PEX14
are core matrix-import factors whose disease phenotypes come from more complete
peroxisome biogenesis failure (Liu et al. 2012, DOI 10.1016/j.ceb.2012.05.003;
Braverman et al. 2016, PMID 26750748; Berger et al. 2016, DOI
10.1016/j.bbamcr.2015.12.005).

The causal transfer from those papers to the requested endpoint is limited:
the strongest ACOX1 phenotypes are hepatic, systemic, microglial, Schwann-cell,
or lipidomic; this input dataset depleted non-neuronal cells and measured
nuclear RNA in surviving P37-P44 neurons after sparse P16 editing.  However,
that limitation pushes away from a large DEG count, not toward it, because the
most analogous neuronal CRISPR perturbations in the training set were flat and
even the directly queried `Acox1`, PPAR/SREBP, UPR/ISR, autophagy, and
peroxisomal marker rows under those analogs were FDR-flat.

## Prediction

Given five straight peroxisome beta-oxidation/import analogs at 0 or self-only
1 focal DEG, two basal PPAR/RXR regulators at 0, and no focal sentinel gene
movement, I predict that held-out `Acox1` will not cross the FDR 0.05 threshold
in `151 TH Prkcd Grin2c Glut` cells.  The point prediction is therefore:

```text
Acox1 -> 0
```

## Limits

This is an extrapolation because `Acox1`, `Acox2`, `Acox3`, `Abcd1`, `Abcd2`,
`Pex5`, `Pex6`, `Pex13`, `Pex19`, `Scp2`, `Ehhadh`, and `Cat` were not present
as training perturbations.  The endpoint is a zero-inflated, assay-dependent DEG
count and weak singleton calls can appear even among mostly flat pathways, as
seen for `Agps`, `Far1`, and the `Pex14` self transcript.  The dataset cannot
exclude a real ACOX1 effect on VLCFA abundance, H2O2, organelle contacts,
microglia, oligodendrocytes, axons, synapses, pre-assay survivorship, or a
later degenerative process.  It only supports the narrower prediction that the
surviving focal thalamic glutamatergic neuronal nuclei will have zero measured
genes below BH FDR 0.05.
