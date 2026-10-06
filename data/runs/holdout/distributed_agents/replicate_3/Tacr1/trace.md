# Question and resolved ambiguities

The requested endpoint is the exact focal-cell DEG count for each held-out
perturbation in `151 TH Prkcd Grin2c Glut`: the number of measured genes with
Wilcoxon `pvals_adj < 0.05` in perturbed nuclei versus matched controls.  The
only requested target in `230_Tacr1.csv` is `Tacr1`, and `Tacr1` is completely
absent as a perturbation from both the training DE parquet and the focal
training-count CSV.  I therefore treated all Tacr1 rows in the parquet as rows
where Tacr1 was a measured transcript under other perturbations, not as Tacr1
knockout measurements.

The cell-group label was interpreted literally from the dataset context:
`TH` is thalamus and `Glut` is glutamatergic, so the endpoint is a basal,
postmitotic thalamic glutamatergic nuclear-RNA response, not tyrosine
hydroxylase-positive dopaminergic cells and not ligand-evoked GPCR physiology.

# Sources used

- `training_de_all_cell_groups.parquet`: the per-measured-gene Wilcoxon DE
  table for non-held-out perturbations.  The parquet is the authoritative
  source for focal-cell expression-pattern evidence.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the observed
  `pvals_adj < 0.05` focal-cell DEG count for each available training target.
- `230_Tacr1.csv`: the ordered held-out target manifest for this run.
- Distributed Agents same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`: used for pre-interpreted
  Findings around `Tacr3`, `Ntsr1`, and `Oprm1`.  This is a curated layer over
  the same Perturb-seq experiment, not independent replication.
- NCBI PubMed via the `bioeval_literature` tool for independent Tacr1/NK1R
  biology:
  Hershey and Krause 1990, doi:10.1126/science.2154852; Sundelin et al. 1992,
  doi:10.1111/j.1432-1033.1992.tb16592.x; Gerard et al. 1991,
  doi:10.1021/bi00108a006; Macdonald et al. 1996, doi:10.1021/bi952351+;
  Khawaja and Rogers 1996, doi:10.1016/1357-2725(96)00017-9; Choi et al.
  2020, doi:10.1038/s41586-020-2860-1; Bayless et al. 2023,
  doi:10.1016/j.cell.2023.07.021.

# Computational use of the training data

The focal training counts were first summarized to calibrate the response
scale.  Among 1,674 non-held-out targets, 1,205 were zero in `151 TH Prkcd
Grin2c Glut`, the median count was 0, the 90th percentile was 2, the 95th
percentile was 18, and only 43 targets had at least 100 DEGs.  This makes a
zero prediction a common but not automatic class; I only used it for Tacr1
after checking receptor and signaling analogs.

For the raw signature check, I used parquet metadata to find the row groups
covering the focal cell group, read row groups 546 to 580 inclusive, and
filtered the in-memory Arrow tables to

```python
group_name == "151 TH Prkcd Grin2c Glut"
and gene_target in biology_selected_panel
```

The selected panel contained the same tachykinin family member `Tacr3`, the
KNDy/GnRH neuropeptide receptor comparators `Gnrhr`, `Kiss1r`, `Oprk1`, and
`Plcb1`, the peptide/Gq receptors `Ntsr1`, `Htr2a`, `Htr2c`, and `Grm5`,
opioid and other Gi/o receptors, and proximal signaling nodes such as `Prkca`,
`Mapk1`, `Adcy1`, `Adcy5`, `Gnao1`, `Gnas`, `Gnb5`, `Gabbr1`, `Gabbr2`,
`Prkaca`, and `Creb1`.  For each training target I recomputed the number of
focal rows with `pvals_adj < 0.05` and `< 0.10`, inspected the best adjusted
p value, and inspected activity/immediate-early sentinel rows
`Fos`, `Jun`, `Junb`, `Jund`, `Egr1`, `Egr2`, `Egr3`, `Arc`, `Npas4`,
`Nr4a1`, and `Dusp1`.

# Tacr1 reasoning

## Biological prior

`Tacr1` encodes the substance-P-preferring neurokinin-1 receptor, NK1R, a
tachykinin G-protein-coupled receptor.  Rat and human substance P receptors
were cloned as seven-transmembrane GPCRs with high substance P affinity
(Hershey and Krause 1990; Gerard et al. 1991, doi:10.1021/bi00108a006), and
the mouse substance P receptor gene was cloned together with the substance K
receptor gene by Sundelin et al. 1992.  NK1R signals through ligand-evoked
Gq/G11-phospholipase C/Ca2+ pathways, supported both by biochemical coupling
of substance P receptor to Gq and G11 (Macdonald et al. 1996) and tachykinin
receptor signaling reviews (Khawaja and Rogers 1996).

The strongest Tacr1 roles in recent mouse CNS work are circuit-defined and
state-dependent: Tacr1 marks spinoparabrachial pain/touch projection neurons
in the spinal cord/parabrachial axis (Choi et al. 2020), and POA Tacr1 neurons
can be activated by BNST substance P release in a male mating circuit (Bayless
et al. 2023).  Those facts make Tacr1 biologically meaningful, but they do
not make it a good prior for a broad unstimulated transcriptional response in
postnatal thalamic glutamatergic recovered nuclei.

## Training analogs and counterexamples

The closest represented tachykinin-family receptor is `Tacr3`, NK3R.  In the
focal raw data, `Tacr3` had 0 DEGs at FDR < 0.05 and also 0 genes at FDR <
0.10; the smallest adjusted p value was 1.0, and the top focal row was
`Rap2b`, log2FC 0.583, FDR 1.0, in 115 perturbed cells versus 23,679 controls.
The Distributed Agents corpus found that Tacr3 produced only a single robust
screen-level downstream event, `Dazap1` up-regulation in a hypothalamic GABA
bin, and no robust cross-perturbation neighbor.  Its KNDy/GnRH comparators
`Kiss1r`, `Oprk1`, `Plcb1`, and `Gnrhr` were flat in the matched responding
group and did not phenocopy Tacr3; across the queried groups, `Kiss1r`,
`Oprk1`, and `Plcb1` each had no FDR < 0.10 downstream genes, and `Gnrhr`
had only one FDR 0.098 singleton outside the focal cell type.  That corpus
comparison cites the established KNDy loop in which neurokinin B/NK3R,
kisspeptin/GPR54, and dynorphin/KOR coordinate GnRH pulse generation
(Uenoyama et al. 2021, doi:10.3389/fendo.2021.724632).

The focal-cell counts for those Tacr3/KNDy/Gq comparators all matched a zero
Tacr1 prior:

| training perturbation | relevance to Tacr1 | observed focal `n_degs` | focal expression evidence |
| --- | --- | ---: | --- |
| `Tacr3` | same tachykinin GPCR family, NK3R | 0 | min FDR 1.0; no immediate-early sentinel below FDR 1.0 |
| `Gnrhr` | Gq neuropeptide receptor in the reproductive axis | 0 | min FDR 0.7116 |
| `Kiss1r` | Gq neuropeptide receptor paired with NK3R/KOR in KNDy signaling | 0 | min FDR 0.7593 |
| `Oprk1` | KOR, KNDy dynorphin receptor and opioid GPCR | 0 | min FDR 1.0 |
| `Plcb1` | direct phospholipase C pathway node downstream of Gq receptors | 0 | min FDR 1.0 |

Other neuropeptide and Gq receptor perturbations bounded the same point.  In
the focal class, `Ntsr1`, `Htr2a`, `Htr2c`, and `Grm5` each had 0 DEGs.  Their
best adjusted p values were 1.0, 0.8899, 1.0, and 1.0, respectively, and the
activity sentinels `Fos`, `Jun`, `Egr1`, `Arc`, and `Npas4` were all
non-significant.  The corpus describes `Ntsr1` as a globally buffered
postmitotic GPCR: 22 of 23 measured cell groups had no FDR < 0.10 downstream
gene, the only subthreshold response was `Prr7` in a limbic/hippocampal
aggregate, and 0/460 immediate-early or MAPK-responsive gene-by-cell-group
rows reached FDR < 0.10.  This is highly analogous to Tacr1 because NTSR1 is
another ligand-activated neuropeptide receptor whose acute calcium,
phosphorylation, electrophysiology, and trafficking endpoints are mostly
outside a basal snRNA-seq contrast.

Gi/o GPCRs supplied a second receptor-family boundary.  `Oprm1`, `Oprd1`,
`Oprl1`, `Drd2`, `Chrm2`, `Sstr5`, `Galr1`, `Npy1r`, `Avpr1a`, and `Oxtr`
were all zero in the focal class, and `Cnr1` had only one isolated DEG.  The
corpus found that single-gene loss of represented opioid receptor paralogs was
broadly buffered at the basal neuronal nuclear-RNA level and that `Oprd1`,
`Oprk1`, and `Oprl1` were also FDR-flat rather than Oprm1-like or
anti-Oprm1-like signatures.  Different G-protein coupling prevents direct
quantitative transfer from opioid receptors to NK1R, but the shared lesson is
useful: druggable neuromodulatory GPCRs can be functionally central while
leaving no chronic single-receptor RNA module in this assay.

Finally, proximal signaling perturbations argued against a hidden generic GPCR
response in `151`.  `Prkca`, `Mapk1`, `Adcy1`, `Adcy5`, `Gnas`, `Gnal`, and
`Gnb5` were zero.  `Gnao1`, `Gabbr1`, `Gabbr2`, and `Prkaca` each had only a
self-transcript DEG, and `Mtor` had two isolated DEGs.  `Creb1` had 10 DEGs,
but direct loss of the CREB transcription factor is expected to be much closer
to the transcriptome than loss of a ligand-gated surface receptor, so I used
it as a counterexample rather than as a numeric Tacr1 template.

## Zero/nonzero decision and point estimate

I predict `Tacr1` will have 0 DEGs in `151 TH Prkcd Grin2c Glut`.

This is driven primarily by within-dataset evidence: all tachykinin/KNDy/Gq
comparators present in training were zero in the focal class, `Tacr3` did not
produce a broad module elsewhere, other peptide GPCRs were focal-cell null,
and the expected immediate-early/AP-1 sentinels were absent in the closest Gq
receptor surfaces.  External knowledge supplies the reason to trust those
zeros rather than search for a transcription-factor-like analog: Tacr1/NK1R is
a ligand-activated substance P GPCR, so its most plausible missing phenotype
is altered acute peptide responsiveness or circuit excitability, not hundreds
of constitutive nuclear RNA changes in unstimulated juvenile thalamic neurons.

# Limits

`Tacr1` itself, the substance P ligand gene `Tac1`, `Tacr2`, and `Tac2` were
not represented as training perturbations, so the closest family evidence is
from `Tacr3`, not from another NK1R perturbation.  The training comparisons
test single-gene loss under basal conditions; they cannot rule out Tacr1
effects after substance P release, pain, mating, emesis, stress, or other
behavioral challenges.  The screen excluded olfactory bulb and hindbrain and
used NeuN-positive recovered nuclei, so classic NK1R effects in excluded,
under-sampled, non-neuronal, spinal, or low-abundance populations are not
represented.  The zero call is therefore a prediction about this exact
`151 TH Prkcd Grin2c Glut` Wilcoxon FDR endpoint, not a claim that Tacr1 is
biologically inert.
