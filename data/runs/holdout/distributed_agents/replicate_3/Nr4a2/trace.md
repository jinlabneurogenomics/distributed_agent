# Nr4a2 prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one target, `Nr4a2`.  The requested
readout is the number of genes in `151 TH Prkcd Grin2c Glut` with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute sparse
AAV-CRISPR loss of that target.  `Nr4a2` is completely held out: it has zero
`gene_target` rows in `training_de_all_cell_groups.parquet` and no row in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.

I interpreted `TH` in the Allen-style cell label as the thalamic atlas
abbreviation, not as the tyrosine hydroxylase gene.  Thus canonical
`Nr4a2`/Nurr1 biology in midbrain dopaminergic neurons is relevant mainly as a
specificity check; the focal readout is a thalamic glutamatergic group, not the
`215 MB Dopa` population.

## Sources used

* Input DEG-count CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
* Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
* Requested-target manifest:
  `[local file: 158_Nr4a2.csv]`
* Same-experiment Distributed Agents corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, especially `Nr4a1`, `Nr4a3`,
  and `Pitx3` findings and claims.
* Run-local Distributed Agents profile analysis:
  `nr4a_landmark_neighbors.json`, generated with signed log-fold-change
  comparisons in `151 TH Prkcd Grin2c Glut`.
* External literature:
  Zetterstrom et al. 1996, DOI `10.1210/mend.10.12.8961274`; Smits et al.
  2003, DOI `10.1046/j.1460-9568.2003.02885.x`; Sacchetti et al. 2001,
  DOI `10.1046/j.1471-4159.2001.00181.x`; Hawk et al. 2012,
  DOI `10.1172/JCI64145`, PMID `22996661`; Chen et al. 2014,
  DOI `10.1016/j.neuron.2014.05.027`; Jacobs et al. 2009,
  DOI `10.1242/dev.029769`, PMID `19144721`.

## Computation over the supplied data

1. I loaded the held-out manifest and found exactly one target:
   `Nr4a2`.

2. I counted training endpoints in the focal group.  The focal training set has
   1,674 represented perturbations; 469 have at least one DEG, 106 have
   `n_degs >= 10`, and 69 have `n_degs >= 25`.  The focal group is therefore
   sparse enough that zero is a common endpoint and small nonzero calls need
   direct support.

3. I filtered the parquet with PyArrow to
   `group_name == "151 TH Prkcd Grin2c Glut"` and pulled DE rows for candidate
   analogs.  For each analog I verified that the CSV `n_degs` matched the
   count of parquet rows with `pvals_adj < 0.05`.

4. I compared the focal log2-fold-change profiles for the nearest observed
   analogs (`Nr4a1`, `Nr4a3`, `Creb1`, `Crebbp`, `Mef2a`) against all 1,674
   eligible training signatures using Distributed Agents runtime profile-neighbor
   analysis.  The tool compared whole-profile Pearson/cosine similarity and
   signed top-feature overlaps without building a composite score or tuned
   cutoff.

The key focal training counts were:

| training perturbation | focal `n_degs` | perturbed nuclei | why inspected |
| --- | ---: | ---: | --- |
| `Nr4a1` | 0 | 200 | closest represented NR4A paralog |
| `Nr4a3` | 0 | 218 | closest represented NR4A paralog |
| `Creb1` | 10 | 126 | upstream CREB/activity-regulated node |
| `Crebbp` | 8 | 61 | CREB coactivator, chromatin/plasticity node |
| `Mef2a` | 4 | 138 | activity-dependent neuronal TF comparator |
| `Mef2c` | 1 | 223 | MEF2-family comparator |
| `Mef2d` | 0 | 262 | MEF2-family comparator |
| `Egr2` | 0 | 184 | immediate-early TF comparator |
| `Fosl2` | 0 | 211 | AP-1/Fos-family comparator |
| `Jund` | 0 | 261 | AP-1/Jun-family comparator |
| `Rxra` | 0 | 247 | nuclear-receptor partner comparator |
| `Rxrb` | 0 | 249 | nuclear-receptor partner comparator |
| `Rxrg` | 0 | 229 | nuclear-receptor partner comparator |
| `Ncoa1` | 0 | 189 | nuclear-receptor coactivator |
| `Ncoa3` | 0 | 147 | nuclear-receptor coactivator |
| `Rarb` | 0 | 273 | retinoid nuclear receptor comparator |
| `Pitx3` | 0 | 184 | Nurr1/PITX3 midbrain dopamine network |
| `Lmx1b` | 0 | 271 | dopamine-neuron developmental comparator |

`Nr4a1` and `Nr4a3` had no BH-significant genes in the focal group despite
adequate recovered cell numbers.  Expected activity/plasticity transcripts were
not even subthreshold focal hits: after `Nr4a1` perturbation, `Nr4a2`, `Nr4a3`,
`Bdnf`, `Arc`, `Egr1`, `Fos`, `Npas4`, and `Jund` all had adjusted p-values of
1.0; the same was true for `Nr4a2`, `Bdnf`, `Arc`, `Egr1`, `Fos`, `Npas4`, and
`Jund` after `Nr4a3` perturbation.  The signed profile-neighbor run gave
unrelated weak profiles as the top whole-profile neighbors of `Nr4a1`
(`Iqsec1`, `Dag1`, `Stag2`, `Ncapd3`, `Mtnr1b`) and `Nr4a3` (`Suclg1`,
`Irf2`, `Zkscan16`, `Atxn1`, `Fgfr3`), so the all-gene similarity view did not
uncover a hidden NR4A-like FDR module.

## Target-specific reasoning

### `Nr4a2`

**Family and direct pathway analogs.**  `Nr4a2`/Nurr1 is an orphan NR4A nuclear
receptor related to `Nr4a1`/NGFI-B and `Nr4a3`/NOR-1; Zetterstrom et al. 1996
showed that these receptors have overlapping CNS expression, monomeric DNA
binding and constitutive transactivation properties, while `Nr4a2` and `Nr4a1`
can heterodimerize with RXR on DR5 elements.  In the focal training data,
however, the two represented NR4A paralogs were both completely flat:
`Nr4a1 = 0` DEGs and `Nr4a3 = 0` DEGs.  The same-experiment Distributed Agents corpus
also summarizes this as a broader basal pattern: `Nr4a1` had 0 downstream genes
at FDR < 0.10 in all 23 measured neuronal groups, and `Nr4a3` had only a
single FDR < 0.10 gene over its measured surface, an `Xpo6` decrease in
`217 P MY Pineal Glut`, not in the thalamic focal group.  The corpus claim
`claim:cbda42c33a331765635f` explicitly notes that individual represented
NR4A-family perturbations are largely buffered at baseline and were not
interchangeable with RXR/NCOA losses in this neuronal assay.

**Activity-regulated transcription as a counterexample, not a positive match.**
Public work makes NR4A biology plausible in neurons: Hawk et al. 2012 showed
that learning induces all three `Nr4a` genes, that blocking NR4A signaling
impairs long-term memory and the memory enhancement caused by HDAC inhibitors,
and nominated shared targets including `Bdnf`, `Fosl2`, and `Pak6`; Chen et al.
2014 showed that activity-induced `Nr4a1` regulates spine density in
hippocampal pyramidal neurons.  The training data argue that this stimulated
hippocampal program is not a standing basal program in the focal postnatal
thalamic nuclei.  `Creb1` and `Crebbp` were only small responders in the focal
group, with 10 and 8 DEGs respectively, and `Fosl2`, `Egr2`, and `Jund` were
all 0.  The same-experiment Distributed Agents `Nr4a1` finding `F004` and `Nr4a3`
finding `F005` likewise state that represented CREB/AP-1/EGR neighbors did not
phenocopy the NR4A perturbations.

**RXR/NCOA and retinoid nuclear-receptor comparisons.**  Because Nurr1 can
heterodimerize with RXR, I checked the represented RXR and NCOA perturbations.
`Rxra`, `Rxrb`, `Rxrg`, `Ncoa1`, `Ncoa3`, and `Rarb` were all 0 in the focal
CSV.  The corpus `Nr4a3:F004` comparison further reports that `Rxra`, `Rxrb`,
`Rxrg`, and `Ncoa1` did not phenocopy the one-gene `Nr4a3` response in basal
neurons.  This made a generic orphan nuclear-receptor or RXR-cofactor response
unlikely for focal `Nr4a2`.

**Dopaminergic Nurr1 biology.**  `Nr4a2` is essential for midbrain dopaminergic
identity: Smits et al. 2003 showed that Nurr1 is required for induction of
`Slc6a3`/DAT and `Slc18a2`/VMAT2 in mesencephalic dopaminergic neurons, and
Jacobs et al. 2009 placed `Pitx3` in a complex that potentiates Nurr1-dependent
terminal dopamine genes by releasing SMRT/HDAC repression.  That biology is
not in the right cell state for `151 TH Prkcd Grin2c Glut`.  The two focal
training perturbations closest to that developmental network, `Pitx3` and
`Lmx1b`, each had 0 focal DEGs, and the Distributed Agents `Pitx3:F003` same-experiment
finding reports no convergent acute module among represented midbrain
dopaminergic comparators.

## Prediction

The strongest evidence is within-dataset: every direct represented NR4A,
RXR/NCOA, and dopamine-development comparator was flat in `151 TH Prkcd Grin2c
Glut`.  External biology identifies contexts where `Nr4a2` is important, but
those contexts are either activity/challenge dependent or dopaminergic rather
than basal thalamic glutamatergic nuclei.  I therefore predict that the held-out
`Nr4a2` perturbation will have no genes passing BH FDR 0.05 in this focal cell
group:

`Nr4a2 -> 0 DEGs`

## Limits

This is an extrapolation from `Nr4a1` and `Nr4a3`, not a direct `Nr4a2`
measurement.  `Nr4a2` is not functionally identical to either paralog, and
Nurr1 has dopamine-neuron roles stronger than `Nr4a1` or `Nr4a3`.  The
same-experiment CRISPR modality is sparse and gives modest average transcript
depletion, so a protein-level or electrophysiological consequence could be
missed by single-nucleus RNA.  Finally, the prediction is specific to the
basal 3-4-week postnatal `151 TH Prkcd Grin2c Glut` readout; it should not be
read as evidence that `Nr4a2` is unimportant after activity stimulation,
oxidative stress, in microglia-neuron interactions, or in midbrain dopamine
neurons.
