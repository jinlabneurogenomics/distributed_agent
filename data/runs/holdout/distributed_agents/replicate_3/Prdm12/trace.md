# Question and resolution

The held-out manifest for this run contains one requested perturbation,
`Prdm12`. I interpreted the task as a point prediction of the number of genes
with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute AAV
CRISPR loss of `Prdm12` in the focal class `151 TH Prkcd Grin2c Glut`.
`TH` was treated as thalamus, not tyrosine hydroxylase, following the supplied
PerturbAI atlas context.

I predicted the held-out focal-cell DEG count, not effect size, viability,
baseline expression, or a germline knockout phenotype. I did not treat weak
target RNA depletion as failed editing because the dataset context states that
self-transcript depletion is not a quantitative on-target measure in this
mosaic Cas9 assay.

# Sources used

- Requested targets: `[local file: 185_Prdm12.csv]`.
- Training endpoints: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE table: `[local file: training_de_all_cell_groups.parquet]`.
- Internal same-experiment interpretation layer: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for `Prdm12`,
  `Prdm10`, `Ctnnb1`, `Ehmt1`, and related claims.
- NCBI PubMed/Entrez literature searches for external `PRDM12` function.

# Computational checks over the training data

The training count file had 1,674 focal-cell perturbations. Its response
distribution was sparse: 1,205/1,674 were zero, the median was 0, the 95th
percentile was 18, and only 43 perturbations had `n_degs >= 100`. This makes
zero the experimental default unless a held-out gene has either a direct
training analog or a biology that should be active in this thalamic postnatal
class.

I filtered the 616M-row DE parquet to `group_name == "151 TH Prkcd Grin2c Glut"`
and to mechanistic comparator targets, then recomputed each comparator's
FDR<0.05 count to verify that it matched the training CSV. I also pulled the
top significant rows to check whether comparators altered shared or unrelated
expression programs.

The `Prdm12` row itself was present as a measured RNA feature for all 1,674
training perturbations in the focal class, but none altered it at FDR<0.05 and
all adjusted P values were 1.0. That is not the held-out `Prdm12` knockout
signature, but it argues that no strong focal-class training perturbation was
running through a measurable `Prdm12` RNA node.

# Target-specific reasoning

## Prdm12

`Prdm12` is a PR-domain zinc-finger transcriptional regulator with very strong
developmental evidence in sensory neurogenesis. Human biallelic PRDM12
mutations cause congenital insensitivity to pain, and Chen et al. 2015
(Nature Genetics, DOI 10.1038/ng.3308) and Nagy et al. 2015 (Cell Cycle, DOI
10.1080/15384101.2015.1036209) connected PRDM12 to sensory-neuron specification
and pain perception across species. Two mouse/Xenopus studies then placed
`Prdm12` at the initiation of the nociceptor lineage: Bartesaghi et al. 2019
(Cell Reports, DOI 10.1016/j.celrep.2019.02.098) found that mouse `Prdm12`
loss eliminates the nociceptive lineage while leaving proprioceptive and touch
neurons, and Desiderio et al. 2019 (Cell Reports, DOI
10.1016/j.celrep.2019.02.097) showed that `Prdm12` maintains `Ntrk1`/TrkA by
modulating Neurogenin activity. `Prdm12` can also specify caudal p1/V1
interneuron progenitors in the embryonic neural tube by cross-repressing
`Dbx1` and `Nkx6` genes (Thelie et al. 2015, Development, DOI
10.1242/dev.121871), and `Prdm` genes including `Prdm12` have restricted
embryonic CNS progenitor expression (Kinameri et al. 2008, PLoS One, DOI
10.1371/journal.pone.0003859).

Those functions are real, but they are a poor direct match to this endpoint:
the screen edited postmitotic juvenile brain neurons after P16, excluded
hindbrain and spinal cord, did not sample dorsal root ganglia, and measured
thalamic glutamatergic nuclei in `151 TH Prkcd Grin2c Glut`. Even in the true
Prdm12 lineage, adult conditional DRG deletion is much less transformative than
embryonic deletion and produces an age-dependent transcriptome (Landy et al.
2021, Cell Reports, DOI 10.1016/j.celrep.2021.108913; Latragna et al. 2021,
Pain, DOI 10.1097/j.pain.0000000000002536). I therefore treated
`Prdm12` primarily as a developmental sensory-lineage factor rather than as an
expected maintainer of thalamic Prkcd/Grin2c identity.

The closest within-dataset PRDM-family comparator was `Prdm10`, which had a
medium focal response:

- `Prdm10`: 52 DEGs in `151`, led by down-regulation of `Madd`,
  `Cadm3`, `Ptov1`, `Uchl1`, `Kcnt1`, `Rnasek`, `Stmn2`, `Myt1`,
  `Shisa7`, `Hap1`, and `Ackr1`.
- `Prdm2`: 0 DEGs.
- `Prdm5`: 0 DEGs.
- `Prdm16`: 0 DEGs.

The Distributed Agents corpus has high-confidence same-experiment findings that
`Prdm10`'s recurrent neuronal module is not shared by represented `Prdm2`,
`Prdm5`, or `Prdm16`, with the closest PRDM10 literature paralog `Prdm15`
absent from the training set. That made `Prdm10` an important counterexample to
"all PRDM genes are flat", but not a numerical template for `Prdm12`.
The flat `Prdm2`/`Prdm5`/`Prdm16` surfaces showed the opposite counterexample:
PR-domain membership alone is not enough to create a postnatal thalamic RNA
response.

I next looked at the PRDM12-G9a/chromatin hypothesis. Developmental `Prdm12`
can recruit G9a/EHMT2, but Ehmt2 was not represented as a training target, and
Tsimpos et al. 2024 (Neural Development, DOI 10.1186/s13064-023-00179-7)
showed directly that neural-crest G9a loss does not phenocopy `Prdm12` loss in
nociceptor development. The available focal training counts were:

- `Ehmt1`: 4 DEGs, all up, led by `Abhd12b`, `Endou`, `Smtn`, and `Stxbp2`.
- `Setdb1`: 22 DEGs, sharing some repressive-chromatin markers such as
  `Abhd12b`, `Smtn`, and `Msra`.
- `Chd4`: 100 DEGs and `Zmynd8`: 74 DEGs, again with some `Ehmt1`-like
  thalamic marker induction.
- `Sin3a`: 1,433 DEGs, a very broad chromatin/corepressor response.
- `Zfp644`: 0 DEGs, despite being an EHMT1/2 recruitment cofactor.

The Distributed Agents corpus summarizes `Ehmt1` as a tiny thalamic
chromatin-repressor module rather than a broad neuronal identity collapse, and
as not reproduced by `Zfp644`. These chromatin comparators were useful for
calibration but not close enough to outweigh the lineage mismatch for
`Prdm12`.

I also checked whether training perturbations around the nociceptor cascade
were active in the focal thalamic group:

- `Ntrk1`, the TrkA receptor whose expression is PRDM12-dependent in
  developing nociceptors: 0 DEGs.
- `Ntrk2`: 3 DEGs; `Ntrk3`: 0 DEGs.
- `Neurod1`: 0 DEGs; `Neurod2`: 0 DEGs.
- `Pou4f3`, the represented POU4/Brn sensory paralog: 0 DEGs. The closer
  `Pou4f1` and `Pou4f2` were not in the training perturbations.
- `Runx2`: 0 DEGs; `Runx3`: 0 DEGs. Nociceptor-relevant `Runx1` was not in
  the training perturbations.
- `Lbx1`: 1 DEG.

This was the strongest within-dataset support for a zero prediction: the
available sensory/neurogenic comparators were quiet in exactly the same
Wilcoxon endpoint.

Finally, I used strong focal responders as assay-competence counterexamples,
not as analogs. `Ctnnb1` had 383 DEGs and `Tcf7l2` had 106 DEGs in a
Wnt/beta-catenin thalamic module; `Rora` had 278 DEGs; `Zfp423` had 150 DEGs
and directly moved `Grin2c`. The corpus places the `Ctnnb1` and `Tcf7l2`
responses in a real `151 TH Prkcd Grin2c Glut` Wnt-associated state. These
targets show that postmitotic developmental transcriptional regulators and
identity genes can be detected in the focal class when they are wired into its
adult thalamic state. I did not find comparable evidence wiring `Prdm12` into
that state.

# Prediction

I predict `Prdm12` will have no genes passing FDR 0.05 in
`151 TH Prkcd Grin2c Glut`: `predicted_n_degs = 0`.

The zero/nonzero call is driven mostly by within-dataset evidence from
Prdm12-adjacent training perturbations: `Ntrk1`, `Pou4f3`, `Neurod1`,
`Neurod2`, `Runx2`, `Runx3`, `Prdm2`, `Prdm5`, `Prdm16`, and `Zfp644` were all
zero, while `Lbx1`, `Ntrk2`, and `Ehmt1` were only 1-4 DEGs. External
literature supplied the reason to prefer those quiet sensory-lineage and
Prdm12-G9a comparators over broad thalamic regulators such as `Ctnnb1`, `Rora`,
`Zfp423`, or generic chromatin perturbations.

# Limits and uncertainty

The main uncertainty is that the closest exact PRDM12 pathway nodes were not all
available: `Ehmt2`, `Prdm15`, `Pou4f1`, `Pou4f2`, `Runx1`, `Prrxl1`,
`Neurog1`, and `Neurog2` were absent from the training focal-count table.
Available PRDM family members are same-domain comparators rather than close
paralogs, and the G9a/EHMT1 comparison is enzymatic-context evidence, not
direct PRDM12 epistasis.

The literature is dominated by embryonic sensory ganglia, embryonic caudal
neural tube, or adult DRG conditional knockouts. Transferring from those
systems to sparsely edited P16-P44 brain thalamic nuclei is an extrapolation.
The prediction would move upward if there were an unobserved postnatal
thalamic `Prdm12` expression domain or a Prdm12-specific effector among
Prkcd/Grin2c neurons, but neither the focal DE table nor the searched
literature supplied evidence for one.
