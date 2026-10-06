# Grip1 direct n_degs forecast

Target and endpoint:

- Target manifest: `Grip1`.
- Cell population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: count of measured genes with Wilcoxon BH-adjusted `p < 0.05` in the focal class.
- Forecast: `0`.

Same-experiment direct target evidence:

- The selected July corpus had no `Grip1` Findings, Claims, or explicit same-experiment references, so no same-experiment semantic report already interpreted this perturbation.
- The held-out target row and its expression signature were absent from the declared training count table and Parquet, so the point estimate was inferred from same-assay training perturbations and the biology bundle.

Grip1 biology and reach:

- The canonical `Grip1` bundle maps this perturbation to `Ncoa2/GRIP1`, a ligand-recruited p160 nuclear-receptor coactivator in reversible transcriptional complexes.
- The functional-stock card judged that a disruptive edit should stop new Ncoa2 production and likely substantially deplete the dynamic coactivator pool by 21-28 days, but with sparse direct evidence because no P16-P44 postmitotic neuronal Ncoa2 half-life measurement was found.
- Exact focal reach was not absent: in matched non-target `151 TH Prkcd Grin2c Glut` nuclei, `Grip1` was detected in 10,194 of 23,679 nuclei, with 43.05% expressing cells, mean 0.404 CP10k, and mean log1p-CP10k 0.270.
- Endpoint coupling remained uncertain. The loss phenotypes in the card were systemic or reproductive rather than postnatal neural or thalamic, and the Ncoa1/Ncoa3 p160 relatives provide a plausible but untested buffering route.

Training measurements that set the numerical scale:

- The focal-class count table was strongly zero-inflated: 1,205 of 1,674 training perturbations had `n_degs = 0`; the median was 0 and the 75th percentile was only 1, with a long high-count tail.
- The closest p160-family comparators named by the Grip1 card were exactly quiet in the focal endpoint:
  - `Ncoa1`: `n_degs = 0`.
  - `Ncoa3`: `n_degs = 0`.
- Matched profile review confirmed that the zeros were full focal profiles rather than missing rows: `Ncoa1`, `Ncoa3`, and `Ep300` each had 17,259 matched measured genes and zero FDR<0.05 significant features in `151 TH Prkcd Grin2c Glut`.
- Other nearby basal nuclear-receptor/coactivator perturbations in the same count table were also weak: `Ep300 = 0`, `Nr3c1 = 0`, `Ar = 0`, `Pgr = 0`, `Rxra = 0`, `Thrb = 0`, `Vdr = 0`, `Thra = 3`, and `Crebbp = 8`.
- Curated GO nuclear-receptor-binding targets available in the focal count table were mostly null as a class: 17 of 24 represented targets had `n_degs = 0`, with median 0. The larger exceptions, such as `Ctnnb1`, `Tcf7l2`, `Nsd1`, and `Arid1a`, are broader Wnt/TCF or chromatin regulators rather than operation-matched p160 coactivator losses.

Corpus checks on comparators:

- The same-experiment Ncoa1 report explicitly described the thalamic `Ncoa1` response as flat while related `Rora`, `Thra`, and `Crebbp` perturbations were detectable, and described no meaningful Ncoa1 module in unbiased signature search.
- The same-experiment Ncoa3 report described only a single FDR<0.10 downstream event outside the focal thalamic class and no strong positive or negative transcriptome-wide neighbor.
- The Ep300 report likewise treated `Ep300` as a flat responder, with Crebbp failing to broadly phenocopy it.

Synthesis:

`Grip1/Ncoa2` is expressed in a real fraction of the assayed thalamic neurons and loss of a renewed coactivator pool should be biologically reachable, so the forecast is not zero because the edit is presumed inert. The better scale-matched prior is that basal juvenile perturbation of this ligand-dependent p160/nuclear-receptor coactivator axis is often buffered in the survivor-conditioned focal assay. Both assayed p160 paralogs are at the exact zero floor in this cell population, Ep300 and Nr3c1 are also zero, and the only close CREBBP/KAT3 comparator is a single-digit response rather than a large program. Broader chromatin or Wnt regulators can be large in the same table, but they are off-axis for the specific Ncoa2 operation.

I therefore used the Ncoa1/Ncoa3/Ep300/Nr3c1 zero cohort as the dominant scale evidence, let Crebbp's 8-gene response keep the possibility of a tiny nonzero signature open, and rounded the biology-weighted point estimate to the focal table's modal floor:

`predicted_n_degs = 0`
