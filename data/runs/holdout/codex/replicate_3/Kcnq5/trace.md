# Kcnq5 direct DEG-count forecast

Endpoint: `n_degs` is the number of measured genes in `151 TH Prkcd Grin2c Glut`
with BH-adjusted Wilcoxon `pvals_adj < 0.05`.

## Evidence used

- **Declared Kcnq5 biology bundle**:
  `biology_bundles/Kcnq5.json`, also served through
  `distributed_agents_runtime.characterization_bundle(view="biology")`.
  - Exact focal reach: Kcnq5 was measurable in the focal non-target population,
    but weakly and in a minority of nuclei: mean raw UMI `0.339`, mean CP10k
    `0.213`, pseudobulk `21.25` cpm, and `4350 / 23679 = 18.37%` non-target
    nuclei expressing.
  - Operative entity: KCNQ5 is a pore-forming Kv7.5/M-current channel subunit
    that can form KCNQ3-containing complexes.
  - Functional stock: the card judged P16 disruptive editing likely to
    substantially deplete KCNQ5-containing channel stock by the P37-P44 harvest;
    the support is partial because direct protein-loss timing came from cultured
    mouse hippocampal neurons rather than juvenile in-vivo thalamus.
  - Endpoint coupling: postnatal channel physiology is established for
    KCNQ5-containing channels, but mostly in hippocampal dominant-negative
    models. The card does not establish that acute loss in aggregated thalamic
    glutamatergic nuclei should create a large stable nuclear-RNA state.

- **Declared focal training count table**:
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  - `Kcnq5` was absent from the 1,674 training rows.
  - The count distribution was highly zero-inflated: `1205 / 1674` rows were
    zero, `276 / 1674` were exactly one, the median was `0`, and the 75th
    percentile was `1`.
  - The high tail was dominated by broad nuclear, proteostasis, splicing, and
    transport perturbations such as `Uba5`, `Tpr`, `Sin3a`, `Psmb4`, `Ufc1`,
    and `Rnpc3`, not by pore-forming ion-channel genes.

- **Static prior-group selection from the declared PerturbAI annotation store**:
  - `Kcnq5` and `Kcnq3` share the projected human CORUM `KCNQ3-KCNQ5 complex`.
  - The Reactome voltage-gated potassium-channel target set contained
    `Kcna1`, `Kcna2`, `Kcnab1`, `Kcnab2`, `Kcnb1`, `Kcnb2`, `Kcnc1`, `Kcnc2`,
    `Kcnc3`, `Kcnd3`, `Kcnh1`, `Kcnh5`, `Kcnq1`, and `Kcnq5`.
  - The broader GO voltage-gated potassium-channel-complex set added channel
    regulators and partners including `Kcnq2`, `Kcnq3`, `Kcnma1`, `Calm1-3`,
    `Dlg4`, `Dpp6`, `Cntnap2`, and `Akap9`.

- **Exact focal counts for those training-available K-channel comparators**:
  - Kv7 comparators: `Kcnq1 = 0`, `Kcnq2 = 1`, `Kcnq3 = 1`.
  - The represented pore-forming voltage-gated K-channel genes were all zero or
    singleton in this focal class: `Kcna1 = 0`, `Kcna2 = 0`, `Kcnb1 = 0`,
    `Kcnb2 = 0`, `Kcnc1 = 0`, `Kcnc2 = 1`, `Kcnc3 = 1`, `Kcnd3 = 0`,
    `Kcnh1 = 0`, `Kcnh5 = 0`, `Kcnq1 = 0`, `Kcnq2 = 1`, `Kcnq3 = 1`.
  - Other GO complex members behaved similarly except the broader CaM
    perturbation: `Kcnab2 = 1`, `Kcnma1 = 1`, `Akap9 = 0`, `Calm2 = 0`,
    `Calm3 = 1`, `Cntnap2 = 1`, `Dlg4 = 1`, `Dpp6 = 1`, while `Calm1 = 14`.
  - A direct DuckDB read of the declared parquet showed that the singleton calls
    for `Kcnq2`, `Kcnq3`, `Kcnab2`, `Kcnc2`, `Kcnc3`, `Kcnma1`, `Calm3`,
    `Cntnap2`, `Dlg4`, and `Dpp6` were their own target transcripts. The
    KCNQ2 and KCNQ3 focal calls were therefore not multi-gene downstream
    signatures.

- **Same-experiment profile and report context for training comparators**:
  - `distributed_agents_runtime.profile_compare` on the 22 static K-channel / regulatory
    comparators in `151 TH Prkcd Grin2c Glut` found 11 focal-class null nodes,
    10 nodes with 1-9 significant features, and one 10-49 node (`Calm1`);
    `Kcnq1`, `Kcnq2`, and `Kcnq3` had 0, 1, and 1 significant focal features
    over 17,259 shared measured genes.
  - The same-experiment Finding ledger annotated `Kcnq2` as an extremely sparse
    glutamatergic-only surface, `Kcnq3` as almost transcriptionally buffered,
    `Kcnq1` as a pan-neuronal FDR-level null, and `Kcna1`/`Kcnc1` family reports
    as flat or singleton postnatal channel-loss surfaces. These records explain
    the same parquet/count-table experiment; I used them for interpretation, not
    as independent replication.

## Synthesis

The Kcnq5 edit should remove functional KCNQ5 stock within the assay window, so
I did not treat it as a failed or inert perturbation. The requested endpoint,
however, is a bulked survivor-conditioned nuclear-RNA DEG count in an aggregated
thalamic class. Kcnq5 is present at low abundance and in only 18.37% of focal
non-target nuclei, adult thalamic protein/RNA evidence is weak, and the strongest
KCNQ5 loss phenotypes come from hippocampal channel physiology rather than a
thalamic transcriptional state.

The most relevant measured training perturbations point to no broad downstream
signature. Kcnq2, the exact static partner Kcnq3, Kcnq1, and the represented
voltage-gated K-channel genes in the focal class are all 0/1-gene rows, and the
singleton rows are usually just the self-transcript. The one larger member,
Calm1, is a pleiotropic calcium sensor and not a KCNQ pore-forming subunit, so I
used it as a boundary showing that the assay can detect an ion-signaling response
but not as a scale analog for Kcnq5.

I therefore forecast no convincing downstream Kcnq5 program and at most a
self-transcript call. Because Kcnq5 is an expressed, feature-available target in
the exact focal population and Kcnq2/Kcnq3 both landed as singleton focal
self-transcript calls, I put the point just above zero:

`predicted_n_degs = 1`
