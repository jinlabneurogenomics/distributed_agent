# Usp9x DEG-count forecast

Target and endpoint: `Usp9x` in `151 TH Prkcd Grin2c Glut`; `n_degs` counts measured genes with BH-adjusted Wilcoxon `p < 0.05` in that thalamic glutamatergic class.

Evidence used:

- The canonical Usp9x biology bundle reports exact focal-population reach in the assay: `Usp9x` was detected in 22,208 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut` / 93.79%, with mean raw UMI 3.61 and mean CP10k 2.26. Functional-stock adjudication called pre-edit USP9X likely substantially depleted by P37-P44 because mouse-neuron USP9X half-lives of 31-39 h make the 21-28 day P16-to-harvest interval many half-lives long.
- That made failed expression or immutable protein stock an unlikely explanation for a null, but the same bundle also marked the direct phenotype evidence as context-limited: the strongest mouse data are developmental neural progenitor or forebrain deletions, not an acute P16 perturbation in thalamic Prkcd/Grin2c neurons.
- The full `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table has 1,674 training perturbations. It is very zero-inflated: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, 469/1,674 nonzero, with a mean of 14.1 driven by rare right-tail responses.
- I nominated Usp9x comparators from the explicit training universe with the mouse gene-analog annotation skill. The usable buckets were broad rather than exact: direct deubiquitinase activity candidates, TGF/SMAD candidates matching a documented developmental axis, proteostasis/ubiquitin-core candidates, and postsynaptic or ankyrin-repeat substrate-side candidates.
- Deubiquitinase-side training counts were low: `Cyld=0`, `Usp48=10`, `Uchl1=1`, `Otulin=0`, `Otud7a=0` in the declared count table. In the Parquet slice for `151 TH Prkcd Grin2c Glut`, those profiles had 141-250 matched perturbed nuclei and no coherent shared FDR-supported program; `Uchl1`'s only significant feature was `Uchl1` itself.
- The TGF/SMAD module was an even lower endpoint donor despite dense same-corpus links among its members: `Smad1=0`, `Smad2=1`, `Smad3=0`, `Smad4=0`, `Tgfbr1=0`, `Tgfbr2=0`, `Acvr1=0`, `Acvr2a=0`, `Acvr2b=0`, `Acvrl1=0`, `Tgif1=0`. This argued that the TGF-beta abnormalities in developmental Usp9x models should not be transferred as a large acute thalamic transcriptional response.
- Direct postsynaptic/substrate-side perturbations were also mostly quiet: `Ank=1`, `Ank1=0`, `Ank2=0`, `Shank2=0`, `Shank3=2`, `Ankrd12=1`, `Map1b=1`; `Ankrd11=20` supplied a local upper analogue but was not enough to make the whole Usp9x forecast a 10-50 DEG response.
- I treated large ubiquitin/proteostasis hits as ceilings rather than donors: `Psmb4=742`, `Psmc1=430`, `Ufc1=572`, and `Uba5=2677` show that this thalamic class can mount a large proteostatic stress program, but USP9X is a substrate-selective deubiquitinase, not a core proteasome, UFMylation, or translation-stress component.

Synthesis:

The biology supports real target engagement in most assayed 151-class Usp9x-expressing neurons, so I placed the point above the modal all-training null. The closest available endpoint evidence, however, is the 0-10 DEG deubiquitinase cluster plus nearly null TGF/SMAD and ankyrin/SHANK substrate perturbations. I therefore forecast a small nonzero response, below `Usp48` and well below the 95th percentile / `Ankrd11` scale:

`predicted_n_degs = 6`
