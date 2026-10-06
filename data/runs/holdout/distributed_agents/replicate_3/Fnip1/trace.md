# Held-out DEG-count prediction for Fnip1

## Question and resolved ambiguities

The task asks for an integer prediction of `n_degs` in `151 TH Prkcd Grin2c Glut` for each perturbation in the held-out manifest. In this run the manifest contains exactly one target, `Fnip1`. I interpret the endpoint exactly as the training CSV defines it: the number of measured genes, including the target transcript itself if it passes, with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in this thalamic glutamatergic neuronal group.

`Fnip1` itself was held out from both input training surfaces, and I found no `Fnip2` or `Flcn` perturbation in the 1,674 focal training counts. I therefore did not have a same-complex one-hop measurement and treated all observed analogs as imperfect pathway or process comparators. I also did not use self-transcript knockdown as a measure of editing success; it only matters because a target transcript can contribute one DEG to the endpoint when it is significant.

## Sources used

- Input training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input per-gene differential expression: `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest: `[local file: 077_Fnip1.csv]`
- Same-experiment semantic layer: Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`
- PubMed literature for FLCN-FNIP, AMPK, TFEB, and mTORC1 biology:
  - Tsun et al. 2013, Molecular Cell, DOI 10.1016/j.molcel.2013.09.016, PMID 24095279
  - Napolitano et al. 2020, Nature, DOI 10.1038/s41586-020-2444-0, PMID 32612235
  - Malik et al. 2023, Science, DOI 10.1126/science.abj5559, PMID 37079666
  - Park et al. 2012, Immunity, DOI 10.1016/j.immuni.2012.02.019, PMID 22608497
  - Schmidt and Linehan 2017, Gene, DOI 10.1016/j.gene.2017.09.044, PMID 28970150

## Computational steps over the supplied data

I loaded the focal count CSV and confirmed its sparsity: 1,674 training perturbations, median `n_degs = 0`, 1,205 zeros, 363 weak responses with 1-9 DEGs, 63 medium responses with 10-99 DEGs, and 43 strong responses with at least 100 DEGs.

I queried the count table for FLCN/FNIP, AMPK, mTOR, GATOR, V-ATPase, lysosome, and autophagy targets. `Fnip1` was held out and `Fnip2`, `Flcn`, `Tsc1`, `Rheb`, `Rraga-d`, `Tfeb`, `Tfe3`, and Ragulator components were not represented in the training endpoint. The direct measured candidates in the focal group were therefore pathway relatives such as `Tsc2`, `Depdc5`, `Mtor`, `Rptor`, `Prkaa2`, `Prkag2`, `Strada`, V-ATPase genes, and core autophagy genes.

To inspect expression-pattern evidence, I read only the focal cell group's rows from the parquet with a PyArrow predicate:

```python
tab = ds.dataset(parquet_path, format="parquet").to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=ds.field("group_name") == "151 TH Prkcd Grin2c Glut",
)
```

This produced 28,891,566 focal rows covering 1,674 perturbations and 17,259 measured genes. For each candidate comparator I joined the exact focal log-fold changes and FDR values back to the count table and listed genes with `pvals_adj < 0.05`. I also ran a Distributed Agents runtime profile comparison on 22 candidate pathway perturbations using the top 200 positive and top 200 negative log-fold-change genes from each perturbation, treating `pvals_adj < 0.05` as the significant program. This was used only to test whether nominated comparators really shared signed focal expression structure.

## Fnip1-specific analogs and counterexamples

### Closest missing biology

FNIP1 binds folliculin and FNIP2. The FLCN-FNIP complex is a GAP for RagC/D GTPases that lets amino-acid signaling recruit/activate mTORC1 at lysosomes (Tsun et al. 2013). FLCN loss can dysregulate TFEB/TFE3 through RagC/D-dependent, substrate-specific mTORC1 control of TFEB, a mechanism linked to Birt-Hogg-Dube disease phenotypes (Napolitano et al. 2020; Schmidt and Linehan 2017). AMPK phosphorylation of FNIP1 suppresses FLCN-FNIP1 and is required for mitochondrial poison-induced TFEB nuclear translocation and subsequent `Ppargc1a`/`Esrra` induction in cultured systems (Malik et al. 2023). Germline `Fnip1` disruption also causes a strong metabolic checkpoint phenotype in B-cell development (Park et al. 2012).

Those mechanisms argue that `Fnip1` is not a random silent metabolic gene. However, the screen measured acute, partial, sparse, postnatal neuronal loss under basal conditions. The closest direct tests of the FLCN-FNIP complex, `Flcn` and `Fnip2`, were absent from the training set, so I anchored the prediction on pathway direction and on whether related branches were visible in this exact readout.

### TSC/GATOR mTORC1 negative regulators

`Tsc2` was the high-side positive comparator with 86 focal DEGs. Its significant genes included sterol and PI3K-feedback markers such as `Cyp51`, `Pik3r3`, `Nsdhl`, `Slc2a6`, and `Slc16a1`. `Depdc5`, the GATOR1 negative regulator, was smaller with 13 DEGs and overlapped `Tsc2` on 8 significant focal genes: `Pik3r3`, `Pik3r1`, `Ldlr`, `Msmo1`, `Tubb3`, `Rnpc3`, `Snhg11`, and `Amy1`. The profile comparison also found this was the one real same-direction mTORC1 pair among the chosen comparators, with 5 shared positive and 3 shared negative FDR-supported genes.

These two targets show that derepressing mTORC1 upstream can be detected in 151 neurons, especially through a sterol/SREBP-like branch. They are not close enough to make `Fnip1` medium-sized, because `Tsc2` works through the Rheb/growth-factor side of mTORC1 and `Depdc5` through GATOR1, whereas FLCN-FNIP primarily controls RagC/D and TFEB. The Distributed Agents corpus made the same boundary explicit: the `Tsc2` report described `Depdc5` as a partial same-direction neighbor but `Mtor`, `Rptor`, `Igf1r`, `Irs1`, and `Akt3` as not producing robust matched overlap in this assay.

### Core mTORC1 and lysosomal-acidification comparators

Loss of positive mTORC1 components did not give a reciprocal large program. In the same focal count table, `Mtor` had only 2 DEGs (`Rims3`, `Tmed8`) and `Rptor` had 0. The Distributed Agents corpus also reported that `Mtor` loss failed to recover expected translation-initiation, sterol/SREBP, lysosome-autophagy, or UPR/ISR secondary RNA programs despite the fact that `Tsc2` and `Depdc5` could recover the sterol arm when the pathway was sufficiently engaged.

The measured V-ATPase/lysosomal acidification genes were similarly bounded. `Atp6ap2` had 2 DEGs, its own transcript plus `Atp6v0a1`; `Atp6v0a1` had a single self DEG; `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` had 0. That makes a broad FLCN-FNIP-to-lysosome stress response unlikely under basal postnatal neuronal conditions.

### Autophagy and lysosome-stress comparators

The canonical autophagy branch was mostly silent in 151: `Atg5 = 0`, `Atg16l1 = 0`, `Becn1 = 0`, `Map1lc3a = 1`, `Sqstm1 = 1`, `Lamp2 = 0`, and `Rb1cc1 = 4` with a small `Calr`/`Hspa5`/`Pdia6` endoplasmic-reticulum signature. In the Distributed Agents corpus, represented autophagy and lysosome perturbations were explicitly annotated as not transcriptomically interchangeable in this postnatal neuronal screen, and disease lysosomal/NCL/hydrolase perturbations did not elicit a shared acute neuronal TFEB/MiT, autophagy, lysosomal-stress, ISR, or UPR nuclear RNA program.

`Vps35` and `Vps54` are looser lysosomal-trafficking counterexamples. They had nonzero focal signatures, 17 and 31 DEGs respectively, but their top genes were retromer/GARP and neuronal-remodeling features (`Atp2a2`, `Brsk1`, `Grin2b` for `Vps35`; `Egr1`, `Jun`, `Stmn4`, `Atp2a2` for `Vps54`) rather than the `Tsc2`/`Depdc5` sterol genes or a TFEB module. They therefore do not justify transferring a medium count to `Fnip1`.

### AMPK and mitochondrial/ERR axis

Because FNIP1 can act downstream of AMPK in the TFEB-mitochondrial stress axis, I checked the represented AMPK/LKB1 neighbors. `Prkaa2`, `Prkag2`, and `Strada` were all 0 in 151. `Esrra` itself was visible with 57 DEGs, but `Esrra` loss is a downstream transcription-factor perturbation and the two genes shared by `Esrra` and `Tsc2` in 151 (`Mpc1`, `Nceh1`) moved in opposite directions. The Distributed Agents corpus grouped AMPK/LKB1-adjacent perturbations as transcriptionally uncoupled from the `Tsc2`/mTOR-axis response in postmitotic neurons. Malik et al. 2023 also framed strong FNIP1-dependent TFEB/ERR induction as a mitochondrial-damage AMPK response; that stress was not imposed here.

## Zero/nonzero decision

The best measured positive analogs, `Tsc2` and `Depdc5`, show that 151 neurons can express an mTORC1/SREBP output, but `Fnip1` loss should perturb the FLCN-FNIP RagC/D/TFEB arm rather than strongly phenocopy TSC or GATOR1 loss. The candidates that are closer to FLCN-FNIP's basal lysosomal and AMPK positioning were flat or nearly flat in this assay. I therefore predicted no focal gene passing FDR 0.05 for acute `Fnip1` loss.

Point prediction for `Fnip1`: `0`.

## Limits

The main limitation is that no training perturbation hit `Flcn` or `Fnip2`, so the closest complex member was unavailable and the prediction is an extrapolation from pathway neighbors. A second limitation is that FNIP1 biology is stress- and tissue-dependent: the training data were basal postnatal NeuN-positive neurons, whereas much of the mechanistic literature uses nutrient or mitochondrial stress, kidney, muscle, immune, adipose, or cell-line contexts. Finally, `n_degs` is a power-dependent FDR count; a prediction of zero does not imply no molecular role for FNIP1, failed editing, or absence of TFEB/mTOR/lysosome protein effects that this single-nucleus RNA endpoint did not measure.
