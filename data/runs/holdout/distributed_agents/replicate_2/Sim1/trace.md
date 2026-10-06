# Sim1 DEG-count prediction

## Question as interpreted

The requested endpoint is the number of genes with `pvals_adj < 0.05` after a
held-out acute CRISPR loss-of-function perturbation in the focal
`151 TH Prkcd Grin2c Glut` cell group. In this run the manifest contains a
single held-out target:

```tsv
target_name
Sim1
```

I treated a prediction of `0` as an explicit prediction that no measured
transcript will cross Benjamini-Hochberg FDR 0.05 in the focal group. The
signature and count for `Sim1` were not in the training parquet or the focal
training-count table, so the estimate has to come from non-held-out
perturbations and from the biology of SIM1.

## Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: 1,674 non-held-out focal
  targets with observed `n_degs`.
- `training_de_all_cell_groups.parquet`: per-gene DE statistics for those
  targets. I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` for the
  candidate analogs and marker genes below.
- Manifest `206_Sim1.csv`: confirmed that `Sim1` was the only requested target.
- Distributed Agents internal corpus
  `perturbai-july-260713-sourceguard-1773-v1`: no direct `Sim1` target context
  was present, but the corpus summarized Arnt, Bmal1, Clock, and Rora
  perturbations and the relevant bHLH-PAS / circadian contrasts in this same
  experiment.
- PubMed-indexed mechanism literature:
  - Michaud et al. 2000, PMID 10640708, DOI
    `10.1016/S0925-4773(99)00328-7`: SIM1 and ARNT2 dimerize and act together
    during PVN/SON hypothalamic neuroendocrine development.
  - Hosoya et al. 2001, PMID 11318878, DOI
    `10.1046/j.1365-2443.2001.00421.x`: Arnt2 knockout eliminates
    neurosecretory lineages in PVN/SON, paralleling Sim1 developmental
    phenotypes.
  - Liu et al. 2003, PMID 12947113, DOI `10.1074/jbc.M304489200`: inducible
    SIM1/ARNT2 experiments identified candidate transcriptional targets and
    loss of selected targets in Sim1 mutant hypothalamus.
  - Tolson et al. 2010, PMID 20220015, DOI
    `10.1523/JNEUROSCI.5444-09.2010`: postnatal CNS Sim1 deficiency causes
    hyperphagic obesity and reduces hypothalamic `Oxt` and PVN `Mc4r`,
    showing a post-developmental SIM1 role but in PVH circuitry.
  - Ramachandrappa et al. 2013, PMID 23778139, DOI `10.1172/JCI68016`, and
    Matharu et al. 2018, PMID 30545847, DOI `10.1126/science.aau0629`: human
    SIM1 variants and hypothalamic CRISPRa rescue support dosage-sensitive
    SIM1 function in appetite-regulating hypothalamic neurons.
  - Son et al. 2021, PMID 34705510, DOI `10.1126/sciadv.abh4503`: Sim1
    haploinsufficiency changes Sim1+ PVH neurons and ectopically induces Irx3
    and Irx5.
  - Yao et al. 2023, PMID 38092916, DOI `10.1038/s41586-023-06812-z`: the
    Allen whole-mouse-brain atlas and taxonomy place TH glutamatergic classes
    in a different anatomical/transcriptomic context from PVH Sim1+
    hypothalamic neurons.

## Training-set calibration

The focal training table is zero-inflated: 469 of 1,674 targets had any
FDR-significant gene, the median was 0, the 75th percentile was 1, the 90th
percentile was 2, the 95th percentile was 18, and the top responses were broad
housekeeping or chromatin/RNA/proteostasis perturbations such as `Uba5`, `Tpr`,
`Sin3a`, `Rnpc3`, `Zbtb7a`, and `U2af2`.

For exact focal-cell inspection I used a pyarrow dataset filter of the form:

```python
dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj"],
    filter=(pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
           & pc.field("gene_target").isin(candidate_targets),
)
```

Key focal counts among Sim1-relevant or counterexample targets were:

```tsv
training_target	n_degs	relevance
Arnt	0	available ARNT paralog/ARNT-family cofactor; ARNT itself is not the SIM1 in-vivo partner
Ahr	0	ARNT-dependent bHLH-PAS branch counterexample
Ahrr	0	AHR feedback branch counterexample
Hif1a	0	ARNT-dependent HIF branch counterexample
Npas3	0	neuronal bHLH-PAS family counterexample
Bmal2	0	BMAL paralog counterexample
Clock	3	active bHLH-PAS/circadian positive-limb control
Bmal1	103	active bHLH-PAS/circadian positive-limb control
Cry1	1	small clock-loop response
Cry2	3	small clock-loop response
Nr1d1	116	active REV-ERB thalamic/circadian branch
Rora	278	active ROR thalamic/circadian branch
Rorb	0	ROR paralog counterexample
Rorc	0	ROR paralog counterexample
Pou3f3	0	neurodevelopmental TF counterexample
Pou3f4	0	neurodevelopmental TF counterexample
Otx2	0	neurodevelopmental TF counterexample
Isl1	0	hypothalamic/neuroendocrine-development TF counterexample
Arx	0	neurodevelopmental TF counterexample
Rax	0	hypothalamic-development TF counterexample
Six3	0	forebrain/hypothalamic-development TF counterexample
Sox2	2	neural-development TF with only singleton-level output
```

The relevant unavailable direct analogs were also informative: `Arnt2`,
`Sim2`, `Otp`, and `Pou3f2` were absent as perturbation targets, so there was no
training perturbation of the obligate SIM1 partner or of the closest PVN
specification factors.

I also checked the actual focal DE rows for several candidates:

- `Arnt`, `Ahrr`, and `Npas3` had `min(pvals_adj) = 1` and no significant
  focal genes. `Ahr` and `Hif1a` also had no significant genes
  (`min(pvals_adj) = 0.221` and `0.306`, respectively).
- `Clock` had exactly three focal hits: `Dbp`, `Nr1d2`, and `Tef`, all
  down-regulated.
- `Bmal1` had 103 focal hits dominated at the top by canonical clock-output and
  feedback genes such as down-regulated `Dbp`, `Nr1d2`, and `Nr1d1`, plus
  up-regulated `Npas2`.
- `Rora` had 278 focal hits, including down-regulation of `Prkcg`, `Adgrb1`,
  `Rasa4`, `Pcp4`, `Nr1d1`, and other thalamic effector genes.

The run-local `profile_neighbors` comparison over all 1,674 eligible focal
training targets gave the same boundary. `Arnt`, `Ahr`, `Hif1a`, `Stat3`, and
`Isl1` were all profiles with zero significant focal features. Their closest
whole-profile neighbors were almost all 0- or 1-DEG perturbations, indicating
background-level rank correlations. In contrast, the active `Clock`, `Bmal1`,
and `Rora` perturbations were true FDR-positive controls rather than artifacts
of the profile search.

Finally, I asked whether the focal group showed any training-set movement of
PVH/SIM1 pathway transcripts as measured genes. Across all 1,674 non-held-out
training perturbations in this focal cell group, `Sim1`, `Otp`, `Pou3f2`,
`Oxt`, `Avp`, `Crh`, `Trh`, `Mc4r`, `Irx3`, and `Irx5` each had no
FDR-significant row; for most of these genes the minimum adjusted P value was
exactly 1.0. `Sim2` was not in the measured gene universe. That argues that the
canonical SIM1/PVH neuropeptide program is not an active DE axis in the
thalamic `151 TH Prkcd Grin2c Glut` profile.

## Sim1-specific reasoning

SIM1 is a bHLH-PAS transcription factor with very strong hypothalamic biology:
it partners with ARNT2 in PVN/SON neuroendocrine differentiation, postnatal loss
in the CNS can alter `Oxt` and `Mc4r`, and partial loss of dosage affects
feeding circuitry. Those literature facts make `Arnt2`, `Sim2`, `Otp`, and
`Pou3f2` the best mechanistic perturbation analogs. Unfortunately they were not
available as focal training perturbations here.

The nearest available cofactor was `Arnt`, but it is an imperfect comparator
because ARNT2, not ARNT, is the SIM1 developmental partner in PVN/SON. Its
observed focal endpoint was nevertheless useful: `Arnt` had 0 DEGs, and the
same internal corpus found that ARNT/AHR/HIF-axis genes were transcriptionally
flat under the basal juvenile NeuN+ conditions, while `Bmal1` and `Clock`
proved that the assay can detect an active bHLH-PAS transcriptional module when
that module is engaged.

The active clock and ROR examples are therefore counterexamples, not reasons to
predict a broad `Sim1` response. `Bmal1`, `Clock`, `Cry1`, `Cry2`, `Nr1d1`, and
`Rora` perturbations hit canonical thalamic clock/accessory-loop outputs such
as `Dbp`, `Nr1d1`, `Nr1d2`, `Tef`, `Per2`, and ROR-sensitive thalamic effector
genes. They do not converge on the SIM1/ARNT2/PVH neuropeptide program, and the
available ROR-family contrasts (`Rora` active, `Rorb` and `Rorc` flat) show that
even close transcription-factor families are not interchangeable in this
screen.

The decisive context is anatomical and developmental. The held-out experiment
perturbed postmitotic P16 neurons and read out broad adult thalamic
Prkcd/Grin2c glutamatergic cells, not embryonic PVN/SON precursors or adult PVH
Sim1+ appetite neurons. Because the focal training DE surface has no detectable
activity of SIM1's canonical downstream PVH transcripts and because available
same-fold or developmental TFs are mostly FDR-flat in this cell group, I
predict that sparse postnatal `Sim1` loss will sit on the zero side of the
zero/nonzero boundary.

## Prediction

```tsv
target_name	predicted_n_degs
Sim1	0
```

## Limits and extrapolation

This is a negative prediction made without the most direct same-complex
perturbation: `Arnt2` was not represented as a perturbation target, and neither
were `Sim2`, `Otp`, or `Pou3f2`. The inference that `151 TH Prkcd Grin2c Glut`
is outside the PVH SIM1 maintenance program comes from atlas/literature
context and from the absence of PVH-neuropeptide rows in the focal training DE
surface, not from measuring baseline `Sim1` protein or indels. A rare
Sim1-expressing subtype could also be diluted inside a broad cell group.
Finally, this CRISPR screen measures a single 3-4 week postnatal nuclear-RNA
endpoint with partial average target-RNA reduction, so it can miss changes in
development, firing, peptide release, metabolism, or behavior that are central
to SIM1 biology.
