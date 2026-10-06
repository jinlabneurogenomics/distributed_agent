# Direct Dnajc6 n_degs forecast

## Target and endpoint

- Target manifest: `[local file: Dnajc6.csv]`, one row: `Dnajc6`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Held-out protection check: `Dnajc6` was absent from the declared focal training count table.

## Evidence that set the scale

The declared focal count table
`[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
contained 1,674 training perturbations. Its thalamic DEG-count distribution was
very sparse: 1,205 zeroes, median 0, 75th percentile 1, 90th percentile 2, 95th
percentile 18, and mean 14.05. Single-gene calls were the dominant nonzero
outcome, with 276/1,674 perturbations at `n_degs = 1`.

The Dnajc6 biology-only bundle
`[local file: Dnajc6.json]`
made a real effect plausible: Dnajc6/auxilin is the clathrin-uncoating Hsc70
cochaperone, its mRNA was detected in 21,198/23,679 non-target nuclei in the
focal population, and proxy turnover evidence favored substantial auxilin-stock
depletion by 21-28 days after a disruptive P16 edit. The same card tempered the
forecast because Gak was documented as partial compensation in Dnajc6-null mouse
brain, the transferable timing evidence for an acute thalamic edit was
unresolved, and the readout is survivor-conditioned nuclear RNA.

The directly relevant measured training perturbations were small in the focal
population:

| perturbation | 151 n_degs | interpretation |
| --- | ---: | --- |
| `Hspa8` | 9 | direct auxilin partner, but its 151 program was a cytosolic HSP/proteostasis counterinduction program (`Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1`, `Cct6a`) |
| `Cltc` | 3 | the coat target of auxilin/Hsc70 uncoating, but broader Cltc Findings linked its large responses to secondary proteostasis/stress states rather than to a simple vesicle-cycle transcriptome |
| `Dnm1` | 1 | self-only in 151 |
| `Synj1` | 1 | self-only in 151 |
| `Bin1` | 1 | self-only in 151 |
| `Dnajc5` | 1 | self-only-sized focal count for another vesicle Hsp70 cochaperone |
| `Nsf` | 0 | flat in 151 |
| `Syp` | 1 | self-only in 151 |
| `Syn1` | 1 | self-only in 151 |
| `Cplx1` | 1 | self-only in 151 |
| `Cplx2`, `Syn2`, `Unc13a`, `Unc13b`, `Unc13c` | 0 | flat in 151 |

These count-table values came from the declared focal count table; the
self/downstream interpretation of the 151 significant genes came from the
declared training Parquet
`[local file: training_de_all_cell_groups.parquet]`.

Same-experiment July corpus Findings for the same measured profiles gave the
same boundary, not independent replication. Hspa8 produced a small real response
restricted to 4/21 measured groups, with its maximum in 151; Cltc responded in
some groups but explicitly did not phenocopy the canonical synaptic endocytosis
and uncoating targets Hspa8, Dnm1, Synj1, Nsf, Dnajc5, Bin1, and Stxbp1; Dnm1
and Synj1 were transcriptomically buffered across the neuronal surface despite
self-transcript depletion; Syp, Syn1/Syn2, Cplx1/Cplx2, and the Unc13 paralogs
were also flat or nearly flat. A symmetric profile comparison of
`Hspa8/Cltc/Dnm1/Synj1/Cplx/Syp/Syn/Unc13/Bin1` in `151` confirmed that the
cohort had only 0-9 significant focal features per node and that the few Hspa8
and Cltc FDR hits did not define a shared high-count endocytic module.

The high-count Hspa8 and Cltc neighbors were useful only as upper-scale
references. In 151, their proteostasis-linked neighbors were orders of
magnitude larger than the vesicle-cycle analogs: `Uba5` 2677, `Psmb4` 742,
`Ufc1` 572, and `Psmc1` 430. Dnajc6 has a more local auxilin operation and a
Gak bypass, so projecting those proteasome/UFMylation counts would overstate
the expected nuclear RNA footprint.

## Synthesis

Dnajc6 should be reachable in the focal thalamic cells and by harvest time, so
the all-target zero prior is too low. At the same time, the closest measured
vesicle-recycling and synaptic perturbations in this dataset were usually
self-only or silent, and the broader Hspa8/Cltc stress responses reflect more
global chaperone, clathrin, or proteostasis disruption than loss of the
partially compensated auxilin cochaperone. I therefore expect at most a tiny
151 signature, centered on one FDR call rather than a transferred Hspa8-like
or Cltc-like multi-gene response.

Predicted `n_degs`: `1`.
