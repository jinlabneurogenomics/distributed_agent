# DEG-count prediction trace

## Question and held-out target

The requested endpoint is the number of genes with Benjamini-Hochberg-adjusted
Wilcoxon `pvals_adj < 0.05` after each held-out CRISPR perturbation in
`151 TH Prkcd Grin2c Glut` nuclei.  The single target in
`080_Foxj1.csv` is:

```tsv
target_name
Foxj1
```

I treated `151 TH Prkcd Grin2c Glut` as a thalamic glutamatergic neuronal
class, not as dopaminergic TH cells, and used `n_degs` as a count of
FDR-significant measured transcripts in recovered snRNA-seq nuclei, including a
self-transcript if one passes FDR.  The held-out target was not used as an
observed perturbation because `Foxj1` has no rows in the supplied non-held-out
DE parquet and no row in the training DEG-count CSV.

## Sources used

- Supplied endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Supplied held-out manifest:
  `[local file: 080_Foxj1.csv]`.
- The Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, queried with
  `target_context`/`inventory` for the represented ciliary and RFX perturbations.
  This corpus is a curated semantic layer over the same experiment, not
  independent replication.
- PubMed literature retrieved through NCBI E-utilities for Foxj1 and ciliated
  ependymal biology: Brody et al. 2000, DOI `10.1165/ajrcmb.23.1.4070`,
  PMID `10873152`; Yu et al. 2008, DOI `10.1038/ng.263`, PMID `19011630`;
  Jacquet et al. 2009, DOI `10.1242/dev.041129`, PMID `19906869`;
  Baas et al. 2006, DOI `10.1111/j.1460-9568.2006.05002.x`,
  PMID `16930429`; Kyrousi et al. 2015, DOI `10.1242/dev.126342`,
  PMID `26395491`.

## Computation over the supplied tables

I first read the focal training-count CSV and the held-out manifest.  The focal
training endpoint is strongly zero-inflated: 1,205 of 1,674 training
perturbations have `n_degs == 0`, the median is 0, the 75th percentile is 1,
and the mean is pulled up to 14.1 by a small number of broad responders.

I then filtered the training counts for a hand-curated set of mechanistic
comparators:

- forkhead family members present in training:
  `Foxa2`, `Foxc2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`, `Foxl2`,
  `Foxn1`, `Foxp2`, `Foxp3`;
- the closest represented ciliary transcription-factor analogs:
  `Rfx3`, `Rfx7`, plus `Nfix` as an upstream ependymal maturation regulator
  reported to activate `Foxj1`;
- structural and trafficking ciliary genes:
  `Bbs5`, `Cep120`, `Cep290`, `Cspp1`, `Dync2h1`, `Dync2i1`, `Ift43`,
  `Ift81`, `Ift88`, `Lztfl1`, `Rpgrip1l`, `Ttc8`, `Ttc21b`;
- ciliary Hedgehog and ciliary-GPCR pathway genes:
  `Gpr161`, `Gli1`, `Gli2`, `Htr6`, `Lepr`, `Ptch1`, `Ptch2`, `Smo`.

Every forkhead target in training had 0 DEGs in the focal class.  The core
ciliary and Hedgehog set was also flat in the focal class except for `Ttc8`,
whose one focal DEG was the `Ttc8` self-transcript rather than a downstream
motile- or primary-cilia expression program.

For expression-pattern evidence, I queried the DE parquet with:

```python
filter = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(candidate_targets)
```

For each candidate I counted FDR<0.05 and FDR<0.10 genes, recorded the best
adjusted P value, and compared Wilcoxon `scores` vectors.  The focal results
for the closest comparators were:

```tsv
training_target	focal_n_degs	min_focal_padj	interpretation
Rfx3	0	1	ciliogenic TF; no focal FDR signal
Rfx7	0	0.211	RFX-family comparator; no focal FDR signal
Nfix	0	0.148	upstream ependymal maturation regulator; no focal FDR signal
Foxj3	0	1	closest assayed Foxj paralog by name; no focal FDR signal
Ift43	0	0.847	IFT-B component; no focal FDR signal
Ift81	0	0.391	IFT-B component; no focal FDR signal
Ift88	0	1	IFT-B component; no focal FDR signal
Dync2h1	0	0.348	retrograde ciliary dynein-2 heavy chain; no focal FDR signal
Dync2i1	0	1	dynein-2 intermediate chain; no focal FDR signal
Cep290	0	0.65	ciliary transition-zone gene; no focal FDR signal
Rpgrip1l	0	0.184	ciliary transition-zone gene; no focal FDR signal
Bbs5	0	0.22	BBSome component; no focal FDR signal
Cspp1	0	1	centrosome/cilia-associated comparator; no focal FDR signal
Lztfl1	0	0.195	BBSome regulator; no focal FDR signal
Ttc8	1	3.07e-05	BBSome component; only significant hit was Ttc8 itself
Gli1	0	1	Hedgehog GLI effector; no focal FDR signal
Gli2	0	1	Hedgehog GLI effector; no focal FDR signal
Gpr161	0	1	ciliary Hedgehog regulator; no focal FDR signal
Ptch1	0	1	Hedgehog receptor; no focal FDR signal
Ptch2	0	1	Hedgehog receptor; no focal FDR signal
Smo	0	1	Hedgehog transducer; no focal FDR signal
```

The focal score vectors also did not reveal a subthreshold shared ciliary state:
among the relevant cilia/Hedgehog targets above, the largest absolute pairwise
Pearson correlation was `r = 0.127` for `Ift88` versus `Ptch2`, and most
literature-obvious pairs were closer to zero.  This matches the Distributed Agents
corpus summaries: `Rfx3` had no FDR<0.10 downstream genes in any recovered
postmitotic neuronal group; `Dync2h1` was a complete measured transcriptional
null across 21 recovered groups; `Cep290` produced no robust downstream program
across 20 recovered groups; and IFT/BBSome/transition-zone/Hedgehog
perturbations in this assay were summarized as buffered at the basal nuclear
RNA level rather than as a coherent shared ciliary transcriptome.

## Target-specific reasoning

### Foxj1

`Foxj1` is the canonical forkhead transcription factor for motile
ciliogenesis.  Hfh4/Foxj1-null mice lack classic 9+2 motile cilia in epithelial
tissues including the airway, where centrioles fail in migration and apical
docking (Brody et al. 2000).  Zebrafish Foxj1 factors can drive a motile-cilia
gene program and ectopic motile-cilia-like differentiation (Yu et al. 2008).
In the postnatal mouse brain, FoxJ1-dependent transcription is needed for
radial glia to differentiate into multiciliated ependymal cells and a small
FoxJ1-positive astrocyte subset (Jacquet et al. 2009), and Mcidas/GemC1 act
upstream of Foxj1 in multiciliated ependymal cell generation (Kyrousi et al.
2015).

Those mechanisms point to a lineage mismatch rather than to a strong TH
glutamatergic neuronal perturbation.  The experiment FACS-enriched NeuN+
neuronal nuclei from postnatal brain and under-sampled ependymal, choroid
plexus, glial, and airway-like multiciliated cells: exactly the contexts in
which Foxj1 is expected to be a master regulator.  Among represented training
genes, `Rfx3` is a particularly relevant counterfactual because RFX factors
also regulate ciliogenesis, and Rfx3-deficient mice have hydrocephalus with
abnormal ciliated ependymal differentiation (Baas et al. 2006).  Yet acute
postnatal `Rfx3` perturbation had `0` focal DEGs, best focal `pvals_adj = 1`,
and the Distributed Agents same-experiment corpus reports no FDR<0.10 downstream genes
for `Rfx3` in any recovered neuronal cell group plus no recovery of an
RFX/ciliary target panel.  `Rfx7`, another RFX-family comparator, was also
focal-zero.

The broader ciliary machinery gives the same boundary.  `Ift43`, `Ift81`,
`Ift88`, `Dync2h1`, `Dync2i1`, `Cep290`, `Rpgrip1l`, `Bbs5`, `Lztfl1`,
`Cspp1`, `Ttc21b`, and ciliary Hedgehog nodes all had `0` focal DEGs; the only
nominal exception in this ciliary neighborhood was a single `Ttc8` self-hit.
Because the supplied parquet can detect broad signatures in this same focal
cell class for other kinds of perturbations, these zeros are target- and
pathway-informative rather than a universal failure of power.  They suggest
that perturbing cilia-linked targets after P16 in recovered NeuN+ neurons
rarely produces a stable nuclear-RNA program, even when the genes are essential
for ciliary structure or signaling in the appropriate developmental or
non-neuronal lineage.

I therefore predict no FDR-significant genes for `Foxj1` in
`151 TH Prkcd Grin2c Glut`: `0`.

## Limits and uncertainty

- `Foxj1` itself is held out, so there is no direct Foxj1 perturbation profile
  in the parquet.  The prediction transfers from training analogs and external
  Foxj1 biology.
- The best biological setting for Foxj1 is multiciliated ependyma and airway or
  oviduct epithelium, but this assay is NeuN-enriched postmitotic neurons.
  That makes a null likely for the requested readout, but it also means the
  prediction does not say Foxj1 loss is harmless in its endogenous ciliated
  lineages.
- Many direct multiciliogenesis regulators and Foxj1 targets, including
  `Gmnc`, `Mcidas`, `Myb`, and many axonemal dyneins, were absent from the
  training perturbation list, so `Rfx3`/`Rfx7` and core IFT/BBS/CEP genes are
  imperfect proxies.
- Single-nucleus RNA cannot observe cilium length, basal-body docking, ciliary
  receptor localization, GLI protein trafficking, or cell loss before recovery.
  A predicted `0` means no stable FDR<0.05 nuclear transcript in the recovered
  TH glutamatergic nuclei, not no cellular phenotype.
- A self-transcript can count as a DEG.  Some training targets produce a lone
  self-hit, as `Ttc8` did here, but the forkhead and RFX comparators did not,
  and Foxj1 is expected to be low or lineage-restricted in this focal neuronal
  class.
