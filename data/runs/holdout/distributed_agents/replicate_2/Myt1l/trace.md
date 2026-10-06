# Task interpretation

The requested endpoint is the number of measured genes with `pvals_adj < 0.05`
after each held-out CRISPR loss-of-function perturbation in `151 TH Prkcd
Grin2c Glut` neurons.  I treated the value as the same assay-defined
Wilcoxon/BH count supplied in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, not as a generic estimate
of target importance, viability, or edit efficiency.

The requested manifest contains one held-out target:

| target_name |
| --- |
| Myt1l |

No direct `Myt1l` perturbation signature or DEG count was present in the
training parquet or the focal-cell count table.

# Sources used

* Training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
* Training DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
* Requested-target manifest:
  `[local file: 140_Myt1l.csv]`
* Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`: no
  target-scoped `Myt1l` findings were available after held-out filtering, but I
  used target-specific findings for `Klf9`, `Sin3a`, and `Rest` as same-assay
  evidence about postnatal neuronal repressor/chromatin perturbations.
* PubMed / NCBI E-utilities for MYT1-family biology and MYT1L disease models.

# Computational calibration

I read the focal-cell counts for all 1,674 non-held-out perturbations and used
them to set the scale of the endpoint.  The distribution is zero-heavy:

| statistic | value |
| --- | ---: |
| nonzero / zero targets | 469 / 1205 |
| mean `n_degs` | 14.1 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436 |
| maximum | 2677 |

The top of the distribution is dominated by broad stress, RNA-processing,
proteostasis, and chromatin regulators; for example `Uba5` had 2677 DEGs,
`Tpr` 1768, `Sin3a` 1433, `Rnpc3` 868, and `Zbtb7a` 841.  Thus a count in the
tens is already above most training perturbations in this cell group.

I then checked mechanistic analogs and boundaries in the focal cell group by
counting parquet rows with `pvals_adj < 0.05` for selected targets and by
examining overlap of their significant genes.  Direct Myt/NZF-family and
Myt1l-SIN3B comparators were missing as perturbations: `Myt1`, `St18`, and
`Sin3b` were measured genes in the matrix but not training `gene_target`
values.

| training perturbation | focal `n_degs` | why it was considered |
| --- | ---: | --- |
| `Sin3a` | 1433 | broad SIN3/HDAC scaffold perturbation; an upper-bound rather than a direct Myt1l analog |
| `Zbtb7a` | 841 | broad same-cell transcriptional repressor/chromatin state, but not a MYT-family protein |
| `Smarcc2` | 185 | detectable BAF/mSWI-SNF chromatin response in the same cell group; useful as a chromatin positive control |
| `Klf9` | 19 | sequence-specific repressor with a narrow 151 TH module converging with `Sin3a`/`Zbtb7a`/`Smarcc2` |
| `Klf13` | 0 | close KLF comparator with a near-threshold but still non-significant surface; an important lower boundary |
| `Mecp2` | 16 | neurodevelopmental chromatin regulator with a small rather than broad focal response |
| `Chd8`, `Chd2`, `Adnp`, `Kmt2a`, `Arid1a` | 61, 34, 25, 24, 22 | ASD/NDD chromatin or transcriptional regulators in the same moderate-low response class |
| `Rest` | 0 | literature-obvious SIN3/CoREST recruiter but inactive in this P16 postmitotic neuronal assay |
| `Notch1`, `Notch2`, `Notch4` | 0, 0, 0 | the direct Notch-receptor axis did not produce a detectable basal postnatal neuronal response |
| `Neurod1`, `Neurod2`, `Atoh1`, `Ptf1a`, `Tcf3`, `Tcf4`, `Tfap4` | all 0 | represented developmental/proneural bHLH and E-protein perturbations were flat in this focal cell group |

For the nearest small repressor-like positive control, `Klf9`, the strict
FDR-0.05 significant set overlapped the large chromatin responders but did not
inherit their full breadth: 12/19 `Klf9` DEGs also passed FDR in `Zbtb7a`
with 11 same-direction changes, 13/19 overlapped `Sin3a` with 12 in the same
direction, and only 1/19 overlapped `Smarcc2`.  This matches the Distributed Agents
corpus `Klf9` claim that loss of `Klf9` produces a restricted, mostly
up-regulated thalamic de-repression module converging with
`Sin3a`/`Zbtb7a`/`Smarcc2`.

The same corpus release also reported two useful boundary observations.  First,
`Sin3a` loss weakly induced `Sin3b` and some associated SIN3-corepressor
transcripts, but direct `Sin3b` perturbation was unavailable; I therefore did
not treat the 1433-gene `Sin3a` count as a proxy for a sequence-specific
SIN3B recruiter.  Second, acute P16 `Rest` perturbation produced no
FDR-threshold genes in any of 23 assayed neuronal groups, and in matched
comparisons did not phenocopy `Sin3a`, `Mecp2`, or other chromatin-repressor
perturbations.  That makes `Rest` a counterexample to a simple
"corepressor-associated gene = broad DEG response" rule.

# Biological reasoning for Myt1l

`Myt1l` encodes a neural MYT/NZF zinc-finger transcription factor.  MYT-family
members bind related AAAGTTT-containing motifs and regulate neuronal
differentiation programs; the assayed training set unfortunately lacked the
closest paralogous or same-family perturbations `Myt1`, `St18`/`Nzf3`, and
`Sin3b`.  The MYT1L-specific literature argues against a confident zero:
Mall et al. showed that Myt1l promotes and maintains neuronal identity by
actively repressing many non-neuronal programs, that its repressive activity
uses a Sin3b-containing complex, and that depletion in primary postmitotic
neurons can de-repress non-neuronal programs and impair neuronal gene
expression/function (Mall et al., 2017, Nature, doi:10.1038/nature21722,
PMID:28379941).  Chen et al. generated a Myt1l haploinsufficient mouse model
and found disrupted developmental gene expression plus adult defects in
transcriptional/chromatin maturation and neuronal physiology (Chen et al.,
2021, Neuron, doi:10.1016/j.neuron.2021.09.009, PMID:34614421).

At the same time, this endpoint is a weak, acute postnatal CRISPR perturbation
read 3-4 weeks after P16 editing, not an embryonic null or a fibroblast-to-neuron
conversion assay.  Within the training set, many classical identity or Notch
axis TF perturbations were exact zeros in `151 TH Prkcd Grin2c Glut`, and
`Rest` was flat even though REST is mechanistically tied to SIN3/CoREST
repression in progenitor or stress contexts.  Those same-assay negatives pull
the estimate far below the broad `Sin3a` and `Zbtb7a` responders.  Because
Myt1l is expressed pan-neuronally and the literature supports a persistent
maintenance role in postmitotic neurons, I still predicted a detectable
response, calibrated to the small `Klf9`/`Mecp2`/`Adnp`/`Kmt2a`/`Chd2`
response class rather than to a zero.

I used 24 as the integer point estimate.  It is just above the observed
95th percentile of the training endpoint and close to several NDD/chromatin
training perturbations with narrow but real focal signatures.

# Limits

The prediction is extrapolative because no direct Myt/NZF-family perturbation
was available in the non-held-out training table, and the central MYT1L
biochemistry points to SIN3B rather than the assayed `Sin3a`.  The best
within-dataset positives are therefore pathway-level or response-shape analogs,
not paralogs.  The Notch and bHLH negatives are also imperfect because they
test receptor/progenitor differentiation components after neuronal identity is
already established, whereas Myt1l may bind many mature neuronal loci directly.
Finally, the parquet counts depend on guide activity, recovered nuclei, nuclear
RNA detectability, and FDR power; a small point estimate should be read as a
prediction of response breadth in this exact assay, not as evidence that Myt1l
biology is intrinsically weak.

