# Mapk8ip1 151 TH Prkcd Grin2c Glut forecast

## Evidence

- Target: `Mapk8ip1`, from the one-row holdout manifest. The target was absent from the declared 1,674-row 151 TH training count table and from the declared training DE Parquet as a profiled `gene_target`.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Biology bundle: Mapk8ip1/JIP1 is a dynamic JNK signaling and kinesin-linked transport scaffold. The stock card judged intact JIP1 likely to be substantially depleted over the 21-28 day P16-to-P37/P44 editing window, but with partial evidence because no target-specific JIP1 half-life was available. JIP1 single loss has mouse neural phenotypes under stress or hippocampal signaling assays, while its functions are stimulus- and context-gated rather than known to impose a constitutive thalamic transcriptional program.
- Exact focal expression from the target bundle was high: 22,938 of 23,679 non-target 151 TH nuclei expressed `Mapk8ip1` (`96.8706%`), with mean `2.9914` CP10K. I used this only as observability for the self transcript, not as editing-efficiency evidence.
- The declared 151 TH training count table was heavily concentrated at zero or one DEG: 1,205/1,674 targets had `n_degs = 0`, 276/1,674 had `n_degs = 1`, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and only 46/1,674 training targets reached 80 or more DEGs.
- In the focal Parquet rows, a single-DEG result usually meant target transcript only: 319/1,674 training perturbations had a significant self transcript, and 237/276 of the `n_degs = 1` perturbations were self-only.
- Represented JNK/MAPK and AP-1 neighbors in the focal count table were null or sparse: `Mapk9 = 0`, `Mapk1 = 0`, `Map2k1 = 4`, `Map2k2 = 0`, `Map2k6 = 0`, `Map3k7 = 0`, `Jund = 0`, and `Fosl2 = 0`.
- Represented kinesin or kinesin-adjacent perturbations were also null to self-scale in the focal count table: `Kif1a = 1`, `Kif5a = 1`, `Kif5c = 1`, `Kifbp = 2`, and the remaining queried `Kif*` examples were zero or one.
- Same-experiment corpus Findings for those training analogs were used as interpretation of the same profiles, not as replication. They describe `Mapk9` as FDR-silent with expected AP-1, apoptosis, and FoxO/autophagy transcripts absent; `Mapk1` as broadly buffered despite self-transcript loss in one group; `Map2k1` as a real but narrow four-gene 151 TH RAF/MEK exception; and `Kif5a`/`Kif5c`/`Kifbp` as transport-pathway perturbations that did not produce a common soma-detectable nuclear RNA module.

## Synthesis

The target should be functionally engaged enough to remove new JIP1 supply, and its high focal expression makes a significant `Mapk8ip1` self-transcript decrease plausible. The analog evidence did not justify borrowing a broad stress, AP-1, or transport response: the closest represented MAPK/JNK node, `Mapk9`, was FDR-silent; terminal `Mapk1` was silent; AP-1 member `Jund` was silent in 151 TH; and the detectable RAF/MEK branch around `Map2k1` was a distinct narrow ERK-output module rather than a generic MAPK-scaffold phenotype.

I therefore forecast a self-transcript-scale response with no confident downstream thalamic module.

`predicted_n_degs = 1`
