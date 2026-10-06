# Ank3 direct DEG-count forecast

Target and endpoint:

- Target: `Ank3`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Point prediction: `1`

Evidence that set the scale:

1. Canonical Ank3 biology, from `biology_bundles/Ank3.json` and the prediction-safe `characterization_bundle(view="biology")`, supports reach but also delayed molecular realization. Ank3 was expressed in 23,624 of 23,679 non-target focal nuclei, 99.77%, with mean raw UMI 11.32 and pseudobulk CPM 709.29, so the transcript itself was broadly detectable in the assayed thalamic population. The bundle did not expose the target outcome.

2. The same bundle adjudicates Ank3 as an installed axon-initial-segment and nodal membrane-domain scaffold. A P16 CRISPR loss-of-function edit can stop new Ank3 supply, but pre-existing AIS/nodal structures are already installed; the functional-stock card therefore places harvest at partial depletion or the leading edge rather than near-complete loss. This pushes the expected 3-4 week nuclear RNA response downward relative to rapidly turning-over nuclear regulators.

3. The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table is extremely zero-heavy in this endpoint: 1,205/1,674 training targets had `n_degs = 0`, 1,481/1,674 had `n_degs <= 1`, the median was 0, the 75th percentile was 1, and the 90th percentile was 2. Large responses were dominated by classes such as core RNA/proteostasis/chromatin regulators, not by local axonal scaffold or excitability genes.

4. I used the AIS/node and nearby neuronal-scaffold training genes as the most task-relevant measured comparators. Their declared focal counts were:

| Comparator set | Training counts |
| --- | --- |
| Ankyrin / spectrin-actin neighborhood | `Ank=1`, `Ank1=0`, `Ank2=0`, `Ankfy1=0`, `Add1=0`, `Add2=0`, `Add3=0`, `Sptan1=1`, `Sptb=0` |
| AIS/node channels and adhesion | `Scn1a=1`, `Scn1b=2`, `Scn2a=1`, `Scn3a=0`, `Scn8a=1`, `Kcnq2=1`, `Kcnq3=1`, `Kcna1=0`, `Kcna2=0`, `Kcnc1=0`, `Kcnc2=1`, `Hcn1=0`, `Hcn2=1`, `Cntnap1=1`, `Cntnap2=1` |
| Nearby synaptic scaffolds | `Dlg4=1`, `Shank3=2`, `Syngap1=0`, `Nrxn1=1`, `Nrxn2=0`, `Nrxn3=0` |

5. I checked these 30 comparators in the declared expression Parquet, restricted to `151 TH Prkcd Grin2c Glut`, with `gene_target` as the profiled entity, `names` as measured features, `logfoldchanges` as signed values, and `pvals_adj < 0.05` as the significant-feature criterion. The profile comparison found all 30 comparator profiles available; 15 had no significant features and 15 had only 1-9 significant features. A cohort diagnostic over 435 comparator pairs had no meaningful shared significant program: mean significant-program overlap was 0.0 in both positive and negative directions, with median top-tail overlap only 0.02.

Synthesis:

Ank3 is more plausibly engaged than many silent targets because the focal population expresses it broadly and because ankyrin-G has a direct neuronal AIS/nodal maintenance function. That argues against using a hard zero as the point. The same biology is stock-limited, structurally buffered, and probably heterogeneous over the P16-to-P37/P44 interval, and the closest measured scaffold/channel comparators in this thalamic class almost all landed at 0-2 DEGs with no recurrent high-DEG program in the Parquet. I therefore forecast a tiny nonzero response and rounded to `1` measured DEG.
