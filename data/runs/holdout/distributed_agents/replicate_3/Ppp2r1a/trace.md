# Ppp2r1a DEG-count prediction

## Question and resolved ambiguities

The requested held-out target list contains one perturbation, `Ppp2r1a`. I interpreted the task as predicting the integer number of measured genes with `pvals_adj < 0.05` after acute sparse CRISPR-Cas9 loss of `Ppp2r1a` in the focal `151 TH Prkcd Grin2c Glut` cell group. The endpoint is the assay-specific Wilcoxon/BH DEG count, not a direct score of knockout efficiency or biological importance.

`Ppp2r1a` is absent as a perturbation from both supplied training inputs, but `Ppp2r1a` can still appear as a measured transcript in other perturbation signatures. I treated those occurrences only as downstream-expression evidence, not as the held-out perturbation itself. I used the focal training-count CSV as the authoritative observed `n_degs` values and the parquet for gene-level expression-pattern evidence.

## Sources used

- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal-cell training endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest: `[local file: 184_Ppp2r1a.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`; I queried `target_context`, `search_claims`, and `candidate_set_topology` for PP2A, phosphatase, Wnt/beta-catenin, and mTOR boundary targets.
- Distributed Agents runtime observed-profile tools; I used a selected focal signature extract to compute pairwise signed Wilcoxon-score similarities and FDR-feature activity among PP2A/phosphatase/Wnt/mTOR comparators.
- PubMed/NCBI literature for PP2A structure and neuronal PP2A biology: Cho and Xu 2006, Nature, DOI `10.1038/nature05351`; Xu et al. 2006, Cell, DOI `10.1016/j.cell.2006.11.033`; Stanevich et al. 2014, PLoS One, DOI `10.1371/journal.pone.0086955`; Kauko et al. 2020, J. Biol. Chem., DOI `10.1074/jbc.RA119.011265`; Dacol et al. 2021, BBA Reviews on Cancer, DOI `10.1016/j.bbcan.2021.188578`; Hayne and DiAntonio 2021, Neurobiology of Disease, DOI `10.1016/j.nbd.2021.105586`; Iqbal et al. 2009, Acta Neuropathologica, DOI `10.1007/s00401-009-0486-3`.

## Computation over the supplied data

1. I verified that the requested CSV has exactly one held-out row: `Ppp2r1a`.

2. I summarized the 1,674 focal training counts. The endpoint is very zero-heavy:
   - mean `n_degs`: 14.1
   - median: 0
   - 75th percentile: 1
   - 469/1,674 perturbations had any FDR 0.05 DEG
   - only the top tail was broad, with examples such as `Uba5` = 2677, `Tpr` = 1768, `Sin3a` = 1433, `Ctnnb1` = 383, and `Tsc2` = 86.

3. I used the parquet metadata to avoid scanning all 616 million rows. `151 TH Prkcd Grin2c Glut` was stored in row groups 547-580, so I streamed just those row groups, keeping `gene_target`, `names`, `scores`, `logfoldchanges`, and `pvals_adj` for nominated analogs.

4. I extracted the focal signatures for represented PP2A or phosphatase comparators (`Ppp2r2b`, `Ppp2r5d`, `Set`, `Ppm1g`, `Ppp3r1`, `Ppp3ca`, `Ppp3cc`), pathway-boundary comparators (`Gsk3b`, `Ctnnb1`, `Lrp6`, `Lrp5`, `Mtor`, `Rptor`, `Tsc2`, `Akt3`, `Pik3r1`, `Pik3r2`, `Pik3cb`, `Igf1r`), and a few tau/APP/mitochondrial/Rack1 counterexamples called out by the corpus (`Mapt`, `App`, `Dnm1`, `Prkar1a`, `Mff`, `Opa1`, `Rack1`).

5. For the selected profiles, I compared signed Wilcoxon-score vectors over the 17,259 measured focal genes. I used scores, not raw log fold-change correlations, because the parquet contains huge logFC values for genes with near-zero expression and adjusted p-values of 1.

## In-dataset analogs and counterexamples

| training perturbation | `151` observed `n_degs` | expression-pattern evidence | relevance to `Ppp2r1a` |
| --- | ---: | --- | --- |
| `Ppp2r2b` | 0 | No focal FDR genes; the direct `Ppp2r2b` transcript was score -3.65 with `pvals_adj = 1`. Distributed Agents reports high-confidence absence of an FDR<0.10 downstream response across measured neuronal groups and no strong whole-universe signature neighbor. | Best represented PP2A regulatory B-subunit loss-of-function comparator. It argues that losing a neuronal PP2A targeting subunit need not cross a nuclear RNA threshold. |
| `Ppp2r5d` | 0 | No focal FDR genes; direct transcript `pvals_adj = 0.405`. Focal score correlation to `Ppp2r2b` was 0.0066, and Distributed Agents states B55/B56 subunits did not converge. | Another PP2A B-subunit comparator, in the B56 family. It is a counterexample to simple "PP2A family produces a shared transcriptome" reasoning. |
| `Set` | 0 | No focal FDR genes; nearest nominal rows had `pvals_adj = 0.657`. Distributed Agents found `Set` disjoint from `Ppp2r2b`/`Ppp2r5d`; `Ppp2r2b`-`Set` and `Ppp2r5d`-`Set` focal score correlations were only 0.017 and 0.022 in the selected profile comparison. | SET is an endogenous PP2A inhibitor, so its loss should release rather than remove PP2A activity. The flat, disjoint response is still useful because it shows that this assay did not reveal a generic PP2A-axis mRNA state. |
| `Ppm1g` | 3 | `Col4a2` and `Col4a1` were down, `H2ac25` was up. Its focal profile had no significant intersection with PP2A or mTOR peers and had only tiny score correlations, such as 0.028 to `Ppp2r5d`. | A broader Ser/Thr phosphatase comparator. The three-gene matrix-like signature is not an obvious match to core PP2A loss. |
| `Ppp3r1`, `Ppp3ca`, `Ppp3cc` | 9, 4, 0 | Calcineurin perturbations were small in `151`; `Ppp3r1` changed nine genes including self, `Pcsk1n`, and `Ptprs`, while `Ppp3ca` changed four including self. | Not PP2A, but they calibrate neuronal Ser/Thr phosphatase loss: even a major Ca2+/calmodulin-dependent phosphatase gave only single-digit focal counts. |
| `Mtor`, `Rptor`, `Akt3`, `Pik3r1`, `Pik3r2`, `Pik3cb`, `Igf1r`, `Tsc2` | 2, 0, 0, 0, 0, 0, 0, 86 | Most receptor-proximal or core PI3K-AKT-mTOR nodes were flat; `Tsc2` was the clear broad positive with a sterol/mTOR-axis response. Distributed Agents claims distinguish the detectable `Tsc2` response from buffered upstream/core nodes. | PP2A can act on AKT/mTOR signaling, but the dataset warns that pathway adjacency does not imply a broad basal snRNA response. |
| `Gsk3b`, `Lrp6`, `Ctnnb1` | 6, 4, 383 | `Ctnnb1` gave a strong Wnt/beta-catenin signature with `Lef1`, `Axin2`, `Nkd1`, `Notum`, `Wnt9b`, and `Vangl1` down. `Lrp6` was a weak but same-direction Wnt comparator; `Gsk3b` did not activate canonical Wnt output. Distributed Agents explicitly bounds the Wnt state to the Lrp6-Ctnnb1/Tcf7l2 branch. | PP2A can intersect Wnt/beta-catenin biology, but in `151` a broad Wnt count is restricted to direct beta-catenin loss rather than every destruction-complex or PP2A-adjacent perturbation. |
| `Rack1` | 2 | The only focal FDR genes were `Aplp2` and `Ppp2r1a`, both down; the Rack1-Ctnnb1 and Rack1-Ppp2r5d score correlations were only 0.077 and 0.036. Distributed Agents found no convergence of Rack1 with PP2A-family, mTOR/translation, APP, tau, or PKC/Fyn comparators. | This shows `Ppp2r1a` transcript itself is detectable in `151`, but a two-gene `Aplp2`/`Ppp2r1a` state did not expose a broad PP2A-like module. |
| `Opa1` | 37 | Opa1 loss gave an ISR/amino-acid response including `Asns`, `Mars1`, `Chac1`, and `Ddit3`. | Positive control for the candidate set: the focal cell group can produce a medium-sized phosphatase-neighborhood counterexample, so zero PP2A B-subunit counts are not a global lack of power. |

## Target-specific reasoning for `Ppp2r1a`

`Ppp2r1a` encodes the A-alpha scaffold subunit of protein phosphatase 2A. Structural work shows that the scaffold A subunit binds the catalytic C subunit and a variable B regulatory subunit into PP2A heterotrimers and that this architecture underlies substrate recruitment by B/B56-family regulatory subunits (Cho and Xu 2006; Xu et al. 2006). The A subunit also couples PP2A core-enzyme assembly with C-tail methylation and holoenzyme assembly (Stanevich et al. 2014). Thus `Ppp2r1a` loss is potentially more central than `Ppp2r2b` or `Ppp2r5d` loss, because it could perturb multiple PP2A holoenzymes rather than one substrate-targeting regulatory arm.

That centrality is the main reason I did not force the prediction to exactly match the two represented PP2A B-subunit zeros. In non-neuronal HeLa cells, PPP2R1A depletion changes a broad phosphoproteome that is not redundant with releasing PP2A from SET, CIP2A, or PME-1 inhibition (Kauko et al. 2020), and neuronal PP2A inhibition can activate DLK stress signaling in cultured neurons (Hayne and DiAntonio 2021). PP2A also dephosphorylates tau and intersects GSK3B-linked tau biology (Iqbal et al. 2009). Those external facts make a truly core PP2A scaffold perturbation a little more likely to have at least a narrow readout than the represented B-subunit perturbations.

However, the same-experiment evidence strongly argues against a broad `Ppp2r1a` response in this assay. `Ppp2r2b` and `Ppp2r5d` were both 0 in the focal group and nonconvergent with each other. `Set` was also 0 in the focal group and was disjoint from the PP2A regulatory-subunit perturbations, consistent with the expectation that SET loss is not the same operation as PP2A subunit loss. `Ppm1g` had only three FDR genes. Calcineurin subunits had only 0-9 focal DEGs. mTOR and receptor-proximal PI3K/AKT nodes were flat or nearly flat except for `Tsc2`, and Wnt/beta-catenin output was branch-specific: `Ctnnb1` was broad, `Lrp6` was four genes, and `Gsk3b` was six genes without canonical Wnt induction. The selected-profile score correlations keep the PP2A-proximal zeros near zero rather than revealing a hidden shared subthreshold module.

My final point estimate is therefore a very narrow nonzero call, `predicted_n_degs = 1`. The most likely route to one FDR gene is the target transcript or another immediate PP2A-scaffold consequence in this well-powered cell group, not a large Wnt-, TSC/mTOR-, APP/tau-, or DLK-like transcriptional state.

## Limits and extrapolation

- The exact `Ppp2r1a` perturbation is held out, and the closest training genes are PP2A B regulatory subunits or the SET inhibitor rather than the shared A scaffold. `Ppp2ca`, `Ppp2cb`, and `Ppp2r1b` were not present as training perturbations in the focal count table.
- Acute AAV CRISPR with average target-RNA downregulation around 18% may leave enough Ppp2r1a protein and A-beta-containing PP2A complexes to buffer the RNA readout. Conversely, indels in a highly used scaffold could have phosphoproteomic effects that the snRNA Wilcoxon endpoint misses.
- The focal endpoint is single-nucleus mRNA after basal juvenile neuronal perturbation. It does not assay tau phosphorylation, beta-catenin protein stabilization, PP2A activity, DLK phosphorylation, synaptic structure, ischemia/excitotoxic stress, glia, or developmental progenitor phenotypes.
- The positive count of 1 is an extrapolation from core PP2A scaffold biology and the detectability of `Ppp2r1a` as an mRNA in the tiny `Rack1` signature. The within-dataset analogs alone would support 0-3 DEGs, and the difference between 0 and 1 is therefore low confidence.
