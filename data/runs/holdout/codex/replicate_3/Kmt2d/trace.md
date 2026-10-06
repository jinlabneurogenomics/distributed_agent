# Direct Kmt2d n_degs forecast

## Target and endpoint

- Target: `Kmt2d`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- The declared training count table has 1,674 focal-class training targets. It is sparse: 1,205/1,674 have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the 95th percentile is 18.

## Biology bundle evidence

The canonical Kmt2d bundle supports target reach and a biologically reachable perturbation in the requested assay. In the exact focal non-target population, `Kmt2d` is available and broadly detected: 20,842 of 23,679 nuclei express it, or 88.0189%, with mean 1.594 CP10K. The functional-stock adjudication is `likely_substantially_depleted`: a P16 disruptive edit stops new KMT2D supply, a four-week adult hippocampal knockdown reduced Kmt2d RNA plus an H3K4 mark, and neuronal H3.3 carriers have measurable four-week turnover.

The same bundle also keeps the prior moderate rather than large. KMT2D acts through enhancer H3K4 mono-/dimethyltransferase and scaffold functions, pre-edit chromatin can persist, and KMT2C was flagged as a partial redundant activity. The strongest mouse neural evidence is adult hippocampal shRNA at four weeks, not P16 thalamic CRISPR in this population.

## Training perturbations used

I gave the most weight to measured training targets whose biology is closest to KMT2D enhancer/COMPASS function, then used broader chromatin regulators only as scale checks:

- `Kmt2c`, the closest named paralog and partial redundant enhancer methyltransferase, has `n_degs = 0` in `151 TH Prkcd Grin2c Glut`. The same-experiment Findings ledger reports that acute P16 `Kmt2c` loss is broadly buffered, with only one FDR<0.10 downstream gene in one cortical group and no meaningful data-driven neighbor.
- `Kmt2a`, another H3K4 writer, has `n_degs = 24` in the focal class. Its report describes a sparse thalamic-biased program and explicitly notes that `Kmt2a` did not phenocopy the represented H3K4 writer relatives: `Setd1a` was broad and largely non-overlapping whereas `Kmt2c` was almost flat.
- The focal count table gave a mixed chromatin range: `Kdm6b = 0`, `Ep300 = 0`, `Kat6b = 0`, `Crebbp = 8`, `Kdm5c = 18`, `Kmt2a = 24`, `Chd2 = 34`, `Chd8 = 61`, `Chd4 = 100`, `Setd1a = 368`, `Wac = 384`, and `Phf12 = 403`.

I also ran a focal-class profile-neighborhood projection for `Kmt2c`, `Kmt2a`, `Setd1a`, `Wac`, `Phf12`, and `Kdm6b` against the 1,674 training nodes. It confirmed that `Kmt2c` is an FDR-null profile in the endpoint class and that its closest whole-profile neighbors were themselves almost all null in the direct count table: `Or51e2 = 0`, `Cspp1 = 0`, `Dock3 = 0`, `Unc13b = 0`, and `Hspa5 = 5`. The large `Setd1a`/`Wac`/`Phf12` footprints therefore looked like distinct promoter-COMPASS, WAC/SETD1, or RNA/proteostasis chromatin responses rather than direct scale donors for KMT2D.

## Synthesis

The target is highly expressed in the focal class and the four-week biology argues against treating Kmt2d as an unavailable edit, so I moved upward from the strict zero suggested by the population baseline and by `Kmt2c`. However, the direct paralog was null, several chromatin enzymes were null or single-digit, and the high-count chromatin perturbations were not close enhancer-KMT2C/KMT2D analogs. I therefore forecast a low but nonzero response, below `Crebbp` and far below `Kmt2a`.

Predicted `n_degs`: **4**
