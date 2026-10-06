# Direct forecast trace

Target: `Usp9x`

Cell group: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `12`

## Evidence used

- The task manifest contains one held-out target, `Usp9x`, and the requested endpoint is the count of measured genes with Wilcoxon BH-adjusted `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- The canonical Usp9x biology bundle reports exact focal-population target reach: `Usp9x` is detected in 22,208 of 23,679 non-target nuclei in this class, `93.7877%`, with mean log1p CP10K `1.08799`.
- The Usp9x functional-stock card judges USP9X protein to be `likely_substantially_depleted` by the P37-P44 harvest after a P16 edit. The relevant protein half-lives in non-dividing primary mouse neurons were about 31-39 hours, so the 21-28 day Perturb-seq window spans many half-lives.
- The same Usp9x bundle makes the main caveat explicit: mouse loss phenotypes come from neural progenitor or developmental forebrain deletions, not from acute P16 editing of the exact thalamic class, so they support Usp9x as a real neuronal loss-of-function perturbation but do not prove a large short-window transcriptional state here.
- The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` has 1,674 measured training targets. Its response distribution is extremely sparse: 1,205 have zero DEGs, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18. The high tail is real but rare, with only 3 training targets above 1,000.
- Annotation-based analog nomination over the exact 1,674-gene training universe found only broad functional, not exact-complex or paralog, matches for Usp9x. The closest deubiquitinase-activity candidates were quiet in the count table: `Cyld` 0, `Usp48` 10, `Uchl1` 1, and `Otud7a` 0. Developmental/TGF-beta candidates linked to published Usp9x biology were also mostly 0 or 1: `Smad3` 0, `Smad2` 1, `Tgif1` 0, `Smad1` 0, `Smad6` 0, `Smad4` 0, and `Acvr1` 0.
- The large ubiquitin/proteostasis training responses in the focal class were broader machinery perturbations: `Uba5` 2,677, `Ufc1` 572, `Psmb4` 742, and `Psmc1` 430. They show that proteostasis damage is highly visible in this class, but direct loss of a core UFMylation or proteasome component is a more proximal global lesion than loss of one substrate-selective deubiquitinase.
- A profile comparison on the declared parquet, restricted to `151 TH Prkcd Grin2c Glut`, found no missing profiles among the selected ubiquitin-system comparators. The same comparison recovered the same FDR-defined activity split: `Usp48` had 10 significant genes, `Uchl1` 1, `Cyld`/`Otud7a`/`Ube3a`/`Ube2e2`/`Ubr1`/`Wdr48` 0, `Marchf6` 14, `Vcp` 2, while the UFMylation/proteasome rows carried hundreds to thousands. `Usp48` was not embedded in a high-response local profile neighborhood; its nearest whole-profile eligible neighbors included `Il1rapl2` 0, `Gtf2i` 10, `Sall1` 0, `Uqcrh` 0, and `Robo4` 0.

## Synthesis

Usp9x is expressed in nearly all assayed non-target nuclei and its pre-edit enzyme pool should mostly turn over within the experiment, so I did not treat it as a stock-persistent or expression-restricted null. At the same time, the strongest target-specific phenotypes are developmental and the closest task-available deubiquitinase/TGF-beta comparators are concentrated at 0-10 DEGs. I therefore used the `Usp48`/`Marchf6` low-nonzero rows as the local scale and treated `Uba5`, `Ufc1`, `Psmb4`, and `Psmc1` as upper-state context for much broader proteostasis collapse rather than equal-scale anchors.

The forecast is a low but nonzero response, slightly above `Usp48` to reflect Usp9x's high reach, efficient expected protein depletion, and broader neuronal substrate set:

`predicted_n_degs = 12`
