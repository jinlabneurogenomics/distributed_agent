# Trip12 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The held-out manifest contains one requested perturbation, `Trip12`. I interpreted the requested endpoint as the exact count of measured genes with `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` contrast, using the same Wilcoxon/BH statistics as the training DEG-count CSV. This count can include the perturbed target transcript itself if that row passes FDR; I did not exclude self rows.

`Trip12` is absent from the focal training-count CSV and from the differential-expression parquet, as expected for this held-out task, so the prediction is a transfer from non-held-out perturbations plus external `Trip12` biology.

## Sources used

- Input training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 247_Trip12.csv]`.
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried for represented HECT-family and ubiquitin-ligase comparators (`Huwe1`, `Hectd4`, `Hecw2`, `Herc1`, `Herc2`, `Ube3a`). The corpus had no `Trip12` card or claim because `Trip12` was held out.
- NCBI PubMed for external `TRIP12` mechanism and disease literature.

## Computations over the training data

1. I read the manifest and confirmed it requests only `Trip12`.
2. I loaded the focal training endpoint table and used it for exact `n_degs` values of candidate analogs. Among all 1,674 training perturbations in this cell group, the distribution is highly zero-inflated: 469 perturbations are nonzero, the median is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and the maximum is 2,677.
3. I scanned that table for biologically nominated `Trip12` comparators:
   - Represented HECT or HECT-like E3 ligases in the focal endpoint were `Huwe1`, `Hectd4`, `Hecw2`, `Herc1`, `Herc2`, and `Ube3a`; `Ubr5`, `Ube3b`, `Ube3c`, `Hectd1`, `Hectd2`, `Hectd3`, `Herc3`, `Herc4`, `Nedd4`, `Nedd4l`, `Wwp1`, `Wwp2`, `Itch`, `Smurf1`, and `Smurf2` were not available.
   - `Trip12` DNA-damage or ARF/p53 pathway nodes were sparsely represented: `Atr`, `Cdkn2a`, `Ddb2`, and `Trp53` were present; `Atm`, `Mdc1`, `Rnf8`, `Rnf168`, `Usp7`, `Asxl1`, `Asxl2`, `Nae1`, `Uba3`, and `Ubr5` were absent.
   - SWI/SNF and Wnt contextual comparators included `Arid1a`, `Smarca4`, `Smarcc1`, `Smarcc2`, `Smarce1`, `Ctnnb1`, `Gsk3b`, and `Tcf7l2`.
4. I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for those candidate genes and inspected the exact `pvals_adj`, `scores`, and log-fold changes. This gave the focal expression-pattern evidence listed below.

The parquet filtering was a direct Arrow predicate over `group_name` and `gene_target` followed by sorting rows by `pvals_adj`; no DEG counts were recomputed from raw UMI data, which are not present in the input.

## Target-specific reasoning

### Trip12

**Relevant within-dataset analogs and counterexamples**

- `Huwe1`, a neural HECT E3 ligase, is the only represented HECT comparator with a sizable `151` response: `n_degs = 158`. Its strongest focal rows were an RNA-processing and neuronal state program, led by `Rsrp1` up, logFC 0.462, FDR 2.07e-17; `Tcea2` up, logFC 0.764, FDR 5.60e-8; `Kcnk9` up, logFC 0.852, FDR 5.60e-8; `Dusp11` up, logFC 0.616, FDR 3.19e-7; and `Ccdc136` down, logFC -0.240, FDR 6.58e-7. The Distributed Agents corpus summarizes this as a reproducible postmitotic HUWE1 RNA/mitochondrial signature, but also as target-specific rather than a generic HECT-ligase phenotype: `Huwe1:F007` found that `Ube3a`, `Hectd4`, `Herc2`, `Ubr1`, `Trp53`, `Myc`, and `Mycn` did not reproduce the HUWE1 FDR module in matched groups.
- `Hectd4` had `n_degs = 1`, and the only focal FDR<0.05 row was the target transcript itself (`Hectd4` logFC -0.479, FDR 2.8e-5). The closest downstream row, `Omg`, was far above threshold at FDR 0.674. Across the Distributed Agents corpus HECT-family comparison, `Hectd4:F003` and evidence `Hectd4:E027` show the same split at FDR<0.10 across the assayed surface: `Huwe1` had 344 downstream genes, while `Hecw2` and `Ube3a` had 0, `Herc1` had 1, and `Herc2` had 2.
- `Hecw2`, a HECT NEDD4-subfamily E3, had `n_degs = 0` in the focal endpoint. Its best focal nominal rows all had adjusted p value 1.0. Corpus finding `Hecw2:F002` explicitly contrasts this null with the HUWE1 response and concludes that HUWE1 is visible but distant, not a family-wide proxy.
- `Herc1` and `Herc2` are large HERC-family HECT ligases. Both had `n_degs = 0` at the focal FDR<0.05 endpoint. `Herc2` did have a very close but subthreshold `Dlat` row in this group, logFC 0.378, FDR 0.056. Corpus findings `Herc1:F005` and `Herc2:F004` show that even these two paralogous large HERC genes did not give interchangeable endpoint genes.
- `Ube3a`, another disease-linked HECT E3 ligase, had `n_degs = 0`; its own transcript was the strongest focal row but was still non-significant, logFC -0.567, FDR 0.137. Corpus finding `Ube3a:F003` again contrasts the flat `Ube3a` result with the broad HUWE1 program.
- `Trp53`, `Atr`, and `Cdkn2a` each had `n_degs = 0`; `Ddb2` and `Nfe2l2` were also 0 and `Sqstm1` had only 1. These are important negative controls for the external `TRIP12` mechanisms around ARF/p53, PARP1/PolB/USP7/RNF168 DNA-damage signaling, NRF2, and autophagy. The focal assay can be very sensitive, but it did not turn basal p53 or DNA-damage pathway perturbations into a large thalamic mRNA state.
- SWI/SNF and Wnt nodes were a real possible upward counterexample: `Smarcc2` had 185 focal DEGs, `Ctnnb1` 383, `Tcf7l2` 106, `Arid1a` 22, and `Smarce1` 11. I treated these as evidence that this cell group can respond strongly to direct chromatin/Wnt perturbation, but not as a close `Trip12` phenocopy because TRIP12 is a ubiquitin ligase that only indirectly touches SWI/SNF/Wnt output through contexts such as BRG1 ubiquitylation.

**External biology used to map Trip12 onto those analogs**

- `TRIP12` encodes a large HECT E3 ubiquitin ligase. It can build atypical K29 and K29/K48 branched ubiquitin chains, and the 2025 TRIP12 structure work explicitly relates its chain-building logic to another HECT enzyme, UBR5 (Maiwald et al. 2025, doi:10.1038/s41594-025-01561-1, PMID 40419785). TRIP12 and UBR5 can also cooperate in K29/K48 branched turnover of OTUD5-associated substrates (Morita et al. 2025, doi:10.1038/s41467-025-57873-9, PMID 40128189). Unfortunately `Ubr5` was not a training perturbation, so I could not calibrate that closest biochemical partner directly.
- Human `TRIP12` haploinsufficiency causes Clark-Baraitser syndrome / neurodevelopmental disorder with intellectual disability, speech delay, autistic features, epilepsy in a subset, and dysmorphic features (Zhang et al. 2017, doi:10.1007/s00439-017-1763-1, PMID 28251352; Aerden et al. 2023, doi:10.1038/s41431-023-01307-x, PMID 36747006). This makes `Trip12` biologically credible in neurons, but the within-dataset `Ube3a`, `Hecw2`, and `Hectd4` nulls show that neurodevelopmental HECT-ligase disease genes are often silent after sparse P16 loss in recovered postmitotic neurons.
- The mouse `Trip12` catalytic mutant is embryonic lethal and embryonic stem cells show growth defects, altered global gene expression, elevated p16, and increased BAF57/Smarce1 protein (Kajiro et al. 2011, doi:10.1371/journal.pone.0025871, PMID 22028794). That points toward an early developmental and proliferative chromatin role, which is only partly aligned with P16-to-P37/44 thalamic neurons.
- TRIP12 and UBR5 restrain RNF168-dependent ubiquitin spreading after DNA double-strand breaks (Gudjonsson et al. 2012, doi:10.1016/j.cell.2012.06.039, PMID 22884692); TRIP12 also modulates USP7-dependent p53/53BP1/Chk1 stability (Liu et al. 2016, doi:10.1002/1873-3468.12471, PMID 27800609) and PARP1 stability (Gatti et al. 2020, doi:10.1016/j.celrep.2020.107985, PMID 32755579). These data are strong protein-level mechanisms in proliferating or damaged cells, but the relevant training perturbations in basal postnatal neurons were transcriptionally flat.
- TRIP12 was recently reported to ubiquitylate BRG1/SMARCA4 and promote Wnt-dependent beta-catenin transcriptional output (Kassel et al. 2025, doi:10.1038/s41467-025-60535-5, PMID 40473626). This was the main reason not to dismiss `Trip12` solely from flat HECT-family neighbors. However, direct `Smarca4` was 0 in the focal endpoint and the broader Wnt responders are not ubiquitin-ligase phenocopies.

**Zero/nonzero decision and approximate count**

The best direct analog class is the represented HECT E3 ligases, not the much broader Wnt or SWI/SNF responders. In that class, four of six focal training comparators were exactly 0, one was target-transcript-only at 1, and the one sizable member, `Huwe1`, is explicitly nonconvergent with the other HECT ligases in the same-experiment corpus. TRIP12 has important nuclear functions, but several of its best-characterized arms are either protein-stability and damage-induced readouts outside snRNA-seq, proliferative/embryonic programs that the P16 screen under-samples, or dependent on UBR5/RNF168/USP7 nodes that were unavailable for direct calibration.

I therefore predict that `Trip12` will be below the BH 0.05 threshold in `151 TH Prkcd Grin2c Glut`, with 0 counted DEGs.

## Limits of the prediction

- `Trip12` itself was held out and was absent from both the DE parquet and the Distributed Agents same-experiment corpus, so no same-experiment `Trip12` expression signature, target-RNA row, guide recovery, or corpus report could be inspected.
- The closest biochemical partners or pathway nodes, especially `Ubr5`, `Rnf168`, `Rnf8`, `Usp7`, `Asxl1`, `Asxl2`, `Nae1`, `Uba3`, `Polb`, and `Parp1`, were not training perturbations in the focal endpoint table.
- A zero prediction is most vulnerable to the possibility that `Trip12` behaves like an unmeasured UBR5/K29-K48 chain regulator or like the visible tail of Wnt/SWI/SNF chromatin regulators rather than like the measured HECT-family genes.
- The training readout is steady-state nuclear RNA in recovered NeuN-positive cells. It does not measure ubiquitinated substrates, DNA-damage foci, RNF168 spreading, PARP1 trapping, p53 protein stabilization, chromatin accessibility, synaptic physiology, or edited-cell loss before recovery.
- Several external `TRIP12` mechanisms were discovered in cancer cells, embryonic stem cells, damaged cells, or non-neuronal tissues. They are useful priors for substrate choice but imperfect predictors of a basal, sparse, postmitotic thalamic CRISPR signature.

## Final point prediction

`Trip12`: 0
