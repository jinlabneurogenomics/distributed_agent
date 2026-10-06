# Prediction trace

## Question and endpoint

The task asks for the held-out value of `n_degs` for each requested genetic
perturbation in `151 TH Prkcd Grin2c Glut` cells. I treated `n_degs` as the
exact training endpoint: the number of measured genes in this focal thalamic
glutamatergic class with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`
after the target was perturbed by sparse postnatal AAV-CRISPR. A zero prediction
therefore means no recovered nuclear transcript is expected to survive FDR 0.05
in that one cell group; it does not mean the gene is biologically irrelevant in
retina or in electrophysiology.

The requested-target CSV contained a single held-out target:

| target | in training count CSV | rows as `gene_target` in DE parquet |
|---|---:|---:|
| `Nyx` | no | 0 |

The held-out readout is absent by design, so I transferred from non-held-out
training perturbations and from external knowledge of nyctalopin biology.

## Sources used

- Declared training count table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This directly measured the endpoint for 1,674 non-held-out perturbations.
- Declared full differential-expression parquet:
  `training differential-expression dataset`.
  I queried the focal-cell rows for retinal ON-bipolar signalplex genes and
  mGluR-family counterexamples, and I also checked other cell groups for the
  closest represented signalplex targets.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through
  `corpus.findings`, `corpus.calibration`, and bounded packaged reports. This
  is the July semantic layer over the same PerturbAI atlas, not an independent
  replicate.
- External literature retrieved from PubMed for the identity of `Nyx` and the
  ON-bipolar mGluR6/TRPM1 signalplex:
  Bech-Hansen et al. 2000, DOI `10.1038/81619`, PMID `11062471`;
  Gregg et al. 2007, DOI `10.1152/jn.00608.2007`, PMID `17881478`;
  Pearring et al. 2011, DOI `10.1523/JNEUROSCI.1014-11.2011`, PMID `21734298`;
  Cao et al. 2011, DOI `10.1523/JNEUROSCI.1682-11.2011`, PMID `21832182`;
  Bojang and Gregg 2012, DOI `10.1371/journal.pone.0033137`, PMID `22485138`;
  Hasan et al. 2020, DOI `10.1523/ENEURO.0002-20.2020`, PMID `31959619`.

## Dataset calibration

The focal training endpoint is extremely sparse: 469 of 1,674 training targets
were nonzero, the median was 0, the 75th percentile was 1, the 90th percentile
was 2, and the mean was inflated to 14.1 by a small high-response tail
(`Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, and similar core genes). A generic small count
would already be easy to overpredict in this table, so I looked specifically for
training perturbations in the known `Nyx` pathway.

The relevant biology is retinal ON-bipolar synaptic signaling. Human `NYX`
encodes nyctalopin, a leucine-rich repeat proteoglycan mutated in X-linked
complete congenital stationary night blindness (Bech-Hansen et al. 2000).
Mouse nyctalopin is a membrane extracellular protein needed on depolarizing
bipolar-cell dendritic tips for normal transmission from photoreceptors to ON
bipolar cells; expression of an EYFP-nyctalopin fusion in bipolar-cell dendritic
tips rescued the `Nyx` no-b-wave mouse phenotype (Gregg et al. 2007). Pearring
et al. and Cao et al. showed that nyctalopin interacts with TRPM1, and Cao et
al. further showed interaction with mGluR6 and mGluR6-dependent TRPM1
postsynaptic accumulation. Bojang and Gregg confirmed murine nyctalopin as a
membrane-anchored small leucine-rich repeat protein. Hasan et al. placed LRIT3
upstream of nyctalopin/TRPM1 expression at depolarizing-bipolar dendritic tips.

That causal model does not naturally predict a nuclear RNA response in the
requested cells:

`Nyx` loss -> defective nyctalopin scaffold at retinal ON-bipolar dendrites ->
mislocalized or ineffective mGluR6/TRPM1 signalplex -> loss of light-evoked ON
response -> no retinal b-wave, with no required transcription-factor program in
juvenile thalamic glutamatergic neurons.

The PerturbAI experiment assayed NeuN-positive brain nuclei after P16 AAV
editing and explicitly omitted retina, so the cell type in which nyctalopin is
obligate is outside the input. I therefore treated the training perturbations of
`Grm6`, `Gpr179`, `Gnb5`, and `Gnao1` as the strongest available mechanistic
analogs, not as proof of independent replication.

## Target-specific reasoning

### `Nyx`

Training perturbations compared:

| analog or counterexample | focal `n_degs` at FDR 0.05 | focal matched nuclei | expression-pattern evidence | relevance to `Nyx` |
|---|---:|---:|---|---|
| `Grm6` | 0 | 201 perturbed / 23,679 control | no accepted gene in `151 TH Prkcd Grin2c Glut`; best scored focal rows all had adjusted p-value 1.0 | `Grm6` encodes retinal mGluR6, the receptor in the same ON-bipolar TRPM1 cascade that nyctalopin scaffolds |
| `Gpr179` | 0 | 206 / 23,679 | no accepted focal gene; the two best rows, `Arhgef17` and `Ufc1`, stopped at FDR 0.519 | ON-bipolar dendritic-tip scaffold for RGS7/RGS11/GNB5 and partner of the same mGluR6/TRPM1 postsynaptic complex |
| `Gnb5` | 0 | 202 / 23,679 | no accepted focal gene; the on-target `Gnb5` row had logFC -0.435 but FDR 0.343 | G beta subunit in R7-RGS complexes used in ON-bipolar mGluR6 signaling; more broadly a GPCR kinetic regulator |
| `Gnao1` | 1 | 181 / 23,679 | the sole focal DEG was `Gnao1` itself, logFC -0.591 and FDR `9.42e-07`; no downstream gene crossed FDR | G alpha-o is the G protein immediately downstream of mGluR6, but also a broad neuronal GPCR transducer |
| `Grm1`, `Grm5`, `Grm7`, `Grm8` | 1, 0, 1, 0 | 115-164 / 23,679 | `Grm1` and `Grm7` each had one self-transcript DEG; `Grm5` and `Grm8` were fully zero | same metabotropic-glutamate-receptor family but not the exact nyctalopin retinal complex |

The same signal was visible outside the focal count table. Scanning all groups
for the direct signalplex analogs showed that `Grm6` and `Gpr179` had zero
FDR<0.05 genes in every recovered group; `Gnb5` had a single significant
self-transcript in `052 Pvalb Gaba`; and `Gnao1` had one FDR<0.05 gene in each
of only three groups. Within the focal group, signed Wilcoxon-score correlations
among `Grm6`, `Gpr179`, `Gnb5`, `Gnao1`, `Grm1`, `Grm5`, `Grm7`, and `Grm8`
were all approximately noise-level, from -0.032 to 0.066 off the diagonal. Thus
the closest available perturbations did not simply have low counts; they also
lacked a coherent shared thalamic expression program to transfer.

The July PerturbAI reports agree with the direct queries. The `Grm6` report
described `Grm6` as having no downstream FDR<0.10 response in any recovered
non-retinal neuronal class and noted that ten canonical ON-bipolar cascade
readouts, including `Gnao1`, `Gnb5`, `Gng13`, `Gpr179`, `Lrit3`, `Nyx`, `Rgs7`,
`Rgs11`, and `Trpm1`, were all unchanged at RNA level after `Grm6`
perturbation. The `Gpr179` report likewise called `Gpr179` all-null across the
recovered juvenile brain groups and interpreted that flat surface as absence of
retina/ON-bipolar cell biology in this assay rather than failed biological
importance. The `Gnb5` and `Gnao1` reports gave a useful counterexample: even
broad GPCR-regulatory nodes can affect signaling kinetics without producing a
persistent postmitotic snRNA-seq stress or activity module.

My prediction is therefore `0` DEGs. The within-dataset evidence carries the
point estimate: the direct mGluR6/GPR179/GNB5/GNAO1 training perturbations had
0, 0, 0, and self-only 1 DEG in the exact focal cell group and were almost blank
screen-wide. External knowledge is used to decide that those are appropriate
analogs for `Nyx`: all sit in, scaffold, or regulate the ON-bipolar
mGluR6/TRPM1 cascade whose central readouts are TRPM1 localization, GPCR gating,
and electroretinography in retina. Because retina and bipolar cells were not
sampled and because the proximal `Nyx` phenotype is synaptic localization rather
than transcription, I did not promote any high-response training target as a
`Nyx` analog.

## Limits and uncertainty

- The input has no held-out `Nyx` DE signature or count, so this is an
  extrapolation from pathway members.
- `Trpm1`, `Lrit3`, `Rgs7`, `Rgs11`, `Gng13`, and `Rgs9bp` were measured genes
  but not represented as perturbation targets in the focal training-count CSV;
  the closest perturbation anchors are therefore `Grm6`, `Gpr179`, `Gnb5`, and
  `Gnao1`.
- Sparse AAV-CRISPR can leave the target transcript unchanged, so the lack of
  an on-target RNA decrease for `Grm6` or `Gpr179` is not by itself a failed
  perturbation call. The zero prediction instead rests on the full lack of a
  downstream focal program plus the retinal, non-transcriptional mechanism.
- A retinal ON-bipolar assay, an ERG b-wave endpoint, or dendritic-tip TRPM1
  localization would almost certainly give a non-null `Nyx` result. The
  prediction is only for FDR-significant nuclear RNA changes among recovered
  `151 TH Prkcd Grin2c Glut` nuclei.
