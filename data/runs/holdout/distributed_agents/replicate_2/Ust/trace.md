# Predicting held-out DEG counts for 151 TH Prkcd Grin2c Glut

## Question and interpretation

The requested run contains one held-out perturbation:

```text
Ust
```

I interpreted the requested endpoint as the integer number of measured genes with
`pvals_adj < 0.05` after an acute, sparse AAV CRISPR loss-of-function
perturbation in `151 TH Prkcd Grin2c Glut` neurons. I treated self-RNA loss as
part of the count, matching the supplied training-count CSV: for example,
`Bpnt2` has one DEG in the focal cell group, and direct parquet inspection shows
that the one FDR-significant gene is `Bpnt2` itself.

I did not interpret a missing downstream DEG as a failed edit. In this assay many
genes show target-RNA changes or plausible biochemical functions without a broad
3-4 week nuclear RNA response.

## Sources used

- Held-out target manifest:
  `[local file: 259_Ust.csv]`
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Full training differential-expression table:
  `[local file: training_de_all_cell_groups.parquet]`
- Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the high-confidence
  GAG/heparan-sulfate/proteoglycan claim that represented single-node pathway
  perturbations do not collapse into a shared acute postnatal neuronal
  transcriptional module.
- Distributed Agents runtime profile comparison of focal-cell signed log-fold-change
  vectors for the represented pathway genes `B3gat3`, `Bpnt2`, `Ext1`, `Ext2`,
  `Glce`, `Gpc6`, `Hs6st2`, and `Xylt1`.
- PubMed literature on UST and chondroitin/dermatan-sulfate biosynthesis:
  Kobayashi et al. 1999, J Biol Chem, DOI `10.1074/jbc.274.15.10474`,
  PMID `10187838`; Mikami and Kitagawa 2013, Biochim Biophys Acta,
  DOI `10.1016/j.bbagen.2013.06.006`, PMID `23774590`; Habicher et al.
  2015, PLoS One, DOI `10.1371/journal.pone.0121957`, PMID `25793894`.
- HSPG / GAG neural-development background summarized in Saied-Santiago and
  Bulow 2017, Dev Dyn, DOI `10.1002/dvdy.24555`, PMID `28736980`, and
  Condomitti and de Wit 2018, Front Mol Neurosci,
  DOI `10.3389/fnmol.2018.00014`.

## Computational checks

The focal training distribution is strongly zero-inflated: among 1,674
non-held-out focal-cell perturbations, 1,205 have `n_degs = 0`, the median is
0, the 75th percentile is 1, and the 95th percentile is 18. That sets a low
base rate for any held-out Golgi sulfation enzyme unless close in-dataset
neighbors show a strong state.

I then queried the focal training CSV for a curated GAG / proteoglycan enzyme
set. The represented genes nearest to `Ust` biology were:

| training perturbation | focal `n_degs` | relevance to UST |
| --- | ---: | --- |
| `B3gat3` | 0 | Common GAG linker enzyme needed before HS and CS/DS chain extension |
| `Xylt1` | 0 | Common initiating xylosyltransferase for GAG attachment |
| `Bpnt2` | 1 | Golgi PAP phosphatase; affects sulfotransferase reactions and GAG sulfation |
| `Ext1` | 0 | HS polymerase subunit |
| `Ext2` | 0 | HS polymerase subunit |
| `Glce` | 0 | HS C5 epimerase |
| `Hs6st2` | 0 | HS sulfotransferase |
| `Gpc6` | 0 | Glypican HSPG core protein, a less direct proteoglycan comparator |

CS/DS-specific enzymes such as `Chst11`, `Dse`, `Dsel`, `Csgalnact1`,
`Csgalnact2`, and `Ust` itself were absent from the training perturbation set,
so the closest focal-cell calibration has to come from shared linker, sulfation,
and HS/proteoglycan genes rather than a true UST paralog.

For the eight represented analogs, I counted significant rows directly in the
parquet after filtering to `group_name = "151 TH Prkcd Grin2c Glut"`:

```sql
SELECT gene_target,
       COUNT(*) FILTER (WHERE pvals_adj < 0.05) AS n_sig
FROM training_de_all_cell_groups
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ('B3gat3','Bpnt2','Ext1','Ext2',
                      'Glce','Gpc6','Hs6st2','Xylt1')
GROUP BY gene_target;
```

This reproduced the CSV counts exactly. The one `Bpnt2` DEG was only `Bpnt2`
itself (`logfoldchanges = -1.09`, adjusted `p = 3.5e-17`); no non-self
transcript in the `Bpnt2` perturbation passed FDR 0.05. `Ext2` self-RNA was
near the threshold but did not pass (`logfoldchanges = -0.453`, adjusted
`p = 0.0559`), while `B3gat3`, `Ext1`, `Glce`, `Gpc6`, `Hs6st2`, and `Xylt1`
had no focal-cell FDR genes.

The runtime profile comparison of the eight log-fold-change vectors likewise
found seven "no_significant_features" profiles and one "1_to_9_significant"
profile, `Bpnt2`, again because of the self feature. The signed top-100 tails
had only small overlaps among these nearly null perturbations, which argues
against a hidden shared GAG module in this cell group.

Finally, I checked `Ust` as a measured response feature in the focal parquet.
It was present for all 1,674 training perturbations, so the held-out UST
experiment would in principle have been able to count `Ust` self-RNA if it were
detectable. As a response to other training perturbations, `Ust` was not a
common pathway sentinel: it passed FDR 0.05 in only two of 1,674 perturbations,
with the strongest being unrelated transcriptional/chromatin perturbations
`Zfp423` and `Ctcf`.

## Target-specific reasoning

### Ust

UST is a Golgi type-II membrane uronyl 2-O-sulfotransferase. The original human
biochemical cloning paper found strong activity on dermatan sulfate, weaker
activity on chondroitin sulfate, and no activity on the desulfated
N-resulfated heparin acceptor used in that assay, placing UST as a CS/DS uronic
acid 2-O-sulfation enzyme rather than a nuclear transcriptional regulator
itself (Kobayashi et al. 1999, PMID `10187838`). Reviews of CS biosynthesis
place uronic-acid 2-O-sulfation downstream of chain polymerization and
epimerization as one of several modifications that tunes extracellular matrix
GAG structure (Mikami and Kitagawa 2013, PMID `23774590`). In zebrafish
development, `ust` is a conserved CS/DS modification enzyme with restricted
expression, and disaccharides containing the 2-O-sulfated uronic acid product
were rare relative to common 4-O- and 6-O-sulfated CS/DS units (Habicher et al.
2015, PMID `25793894`).

The best training analogs point to a zero focal response:

- The common GAG linker perturbations `Xylt1` and `B3gat3`, which should lie
  upstream of both HS and CS/DS chain synthesis, each had `n_degs = 0`.
  Distributed Agents corpus findings for `B3gat3` report that its response in the whole
  screen was extremely restricted and did not feed back on linker, HS/CS enzyme,
  proteoglycan core, UPR/ISR, or autophagy transcripts.
- `Bpnt2` is a strong counterexample to "sulfation gene means broad response".
  BPNT2/gPAPP loss perturbs Golgi PAP disposal and GAG sulfation biochemistry,
  but in the focal cell group its only FDR gene was its own transcript
  (`n_degs = 1`), so the related sulfation defect was effectively
  transcriptionally silent downstream.
- `Ext1` and `Ext2`, the core EXT1/EXT2 HS polymerase subunits, had `n_degs = 0`
  in the focal cell group. Corpus summaries emphasize that even postnatal
  `Ext1` loss, despite known effects on HSPG biology and glutamatergic synaptic
  function in conditional mouse models, produced no FDR-level downstream
  neuronal RNA response across recovered groups in this assay.
- The HS modification enzymes or proteoglycan comparators `Glce`, `Hs6st2`, and
  `Gpc6` also had `n_degs = 0`, providing pathway-boundary evidence that
  changing GAG sulfation or HSPG structure does not by itself induce a sustained
  151 TH Prkcd Grin2c Glut RNA state.

External biology does not rescue a positive prediction. CS/DS and HS chains can
regulate FGF, Wnt, Hedgehog, axon-guidance, and synaptic ligands, but UST is a
fine-structure sulfotransferase rather than the shared linker or polymerase
step. The experiment also begins at P16 in postmitotic sparse neurons, excludes
most ECM-rich non-neuronal populations by NeuN sorting, and reads out nuclear
mRNA rather than GAG abundance, disaccharide composition, pericellular matrix,
or synaptic physiology. Those details make a nontranscriptional glycan defect
much more plausible than a broad cell-autonomous DEG signature.

I therefore predict no genes below FDR 0.05 for held-out `Ust` in the focal
cell group.

## Limits

The comparison is imperfect because no CS/DS-specific sulfotransferase, DSE/DSEL
epimerase, or true UST paralog was present in the focal training counts. Most of
the observed analogs are HS-biased rather than CS/DS-biased. The CRISPR screen
did not assay DNA indels, Golgi enzyme activity, sulfated GAG composition,
extracellular matrix structure, or synaptic physiology, so a zero DEG prediction
does not imply that UST loss is biochemically inert. Finally, UST self-RNA in
the held-out perturbation may or may not be strongly captured; if the gRNAs
happened to reduce the measured transcript as efficiently as the `Bpnt2` gRNAs
did, a singleton self hit would be possible. The directly relevant pathway
evidence, however, favors complete transcriptional buffering.

## Final prediction

| target_name | predicted_n_degs |
| --- | ---: |
| Ust | 0 |
