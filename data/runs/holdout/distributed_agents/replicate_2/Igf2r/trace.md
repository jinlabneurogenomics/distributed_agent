# Igf2r prediction trace

## Question and resolved ambiguities

The held-out manifest `[local file: 111_Igf2r.csv]` contains one requested target:

```tsv
target_name
Igf2r
```

I interpreted the task as a point prediction for the exact Perturb-seq endpoint: the integer number of measured genes in `151 TH Prkcd Grin2c Glut` with Scanpy/Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` after acute sparse AAV-CRISPR loss of `Igf2r`. The prediction is therefore an assay-calibrated transcriptional breadth, not an estimate of biological indispensability or of the strength of complete germline `Igf2r` deletion.

The held-out `Igf2r` signature and count were not present in the training CSV. I used only the 1,674 non-held-out `151 TH Prkcd Grin2c Glut` counts and focal slices of the differential-expression parquet for assayed mechanistic neighbors.

## Sources used

- Input endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. The corpus had no direct `Igf2r` record, so I used `Sort1`, `Lrp1`, `Rab7`, and `Vps35` target contexts plus an induced topology check over measured lysosomal/endosomal candidates.
- Distributed Agents runtime profile comparator over the focal-cell signatures for selected receptors, lysosomal genes, V-ATPase genes, retromer/GARP genes, and `Rab7`.
- PubMed literature returned through the BioEval Literature gateway for CI-MPR/M6P-IGF2R and lysosomal enzyme sorting.

Key external citations:

- Ludwig et al. 1994, EMBO J., DOI `10.1002/j.1460-2075.1994.tb06648.x`, PMID `8062819`: cation-independent and cation-dependent mannose-6-phosphate receptors both contribute to soluble lysosomal-enzyme sorting; single-receptor fibroblasts were partially impaired, whereas double-receptor loss caused massive missorting and storage.
- Lobel et al. 1989, Cell, DOI `10.1016/0092-8674(89)90793-9`, PMID `2541923`: the CI-MPR cytoplasmic tail contains separable information for lysosomal enzyme sorting and rapid endocytosis.
- Zhu et al. 2001, Science, DOI `10.1126/science.1060896`, PMID `11387476`: GGA2 binds the acidic-cluster dileucine motif of CI-MPR and links the receptor to Golgi-to-endosome lysosomal enzyme targeting.
- Nielsen et al. 2001, EMBO J., DOI `10.1093/emboj/20.9.2180`, PMID `11331584`: sortilin can mediate Golgi-endosome lysosomal enzyme transport and its tail binds GGA2, making `Sort1` the closest assayed M6P-independent sorting-receptor analog.
- Wylie et al. 2003, Am. J. Pathol., DOI `10.1016/S0002-9440(10)63823-0`, PMID `12507915`: complete murine M6P/IGF2R loss causes fetal overgrowth and neonatal lethality, while tissue-specific liver or skeletal/cardiac muscle inactivation was viable without an obvious gross phenotype.
- Hirst et al. 2018, PLoS Biol., DOI `10.1371/journal.pbio.2004411`, PMID `29381698`: AP-5 and retromer-related routes retrieve CI-MPR and sortilin from endosomes to the Golgi, providing pathway context for why global retrieval machinery is a much broader perturbation than a single cargo receptor.
- Yu et al. 2020, eLife, DOI `10.7554/eLife.54781`, PMID `32369018`: neuronal CIM6P/IGF2R has an IGF2-dependent hippocampal memory-consolidation role through regulated protein metabolism, but this is ligand/activity gated rather than a constitutive basal snRNA-seq signature.

## Dataset computations

I first summarized the training labels in the focal cell group:

- non-held-out targets in `151 TH Prkcd Grin2c Glut`: 1,674
- nonzero labels: 469
- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- maximum: 2,677

Thus this cell type can show very broad responses, but most perturbations produce no FDR-significant downstream genes.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for 38 training perturbations chosen before looking at `Igf2r`: `Sort1`, LDL-receptor family members, `Igf1r`/`Insr`, lysosomal hydrolase or cargo genes, V-ATPase genes, AP/TRAPP/RAB/VPS traffic genes, and a small number of broad endolysosomal counterexamples. This produced `655842` rows, exactly `38 * 17259` measured genes. For each training target I counted `pvals_adj < 0.05` and inspected the lowest adjusted p-values.

Important focal-cell counts and leading-row evidence:

| training perturbation | focal `n_degs` | focal expression evidence |
| --- | ---: | --- |
| `Sort1` | 0 | closest assayed M6P-independent lysosomal sorting receptor; target transcript itself was the top row but only subthreshold, `Sort1` log2FC `-0.366`, adjusted p `0.0939` |
| `Lrp1` | 0 | closest assayed receptor for secreted lysosomal cargo/progranulin routes with CI-MPR; no gene had adjusted p below 1.0 in this focal slice |
| `Sorl1` | 0 | VPS10/APP sorting receptor, absent from my filtered profile CSV but present in the training endpoint with 0 DEGs |
| `Igf1r`, `Insr` | 0, 0 | IGF/insulin receptor-arm counterexamples; no focal FDR response |
| `Lrp2`, `Lrp4`, `Lrp5`, `Lrp8`, `Vldlr` | 0 each | LDLR-family counterexamples; zero DEG focal signatures |
| `Lrp6` | 4 | small Wnt-flavored receptor response; useful as a boundary because it is not CI-MPR-like cargo traffic |
| `Gaa`, `Ctsb`, `Psap` | 1, 1, 1 | each count was the target transcript itself, with no shared lysosomal-stress program |
| `Lamp2` | 0 | near boundary but still no FDR hit; minimum adjusted p `0.0537` |
| `Atp6ap2`, `Atp6v0a1` | 2, 1 | mostly on-target; `Atp6ap2` additionally down-regulated `Atp6v0a1` |
| `Atp6v1a`, `Atp6v1b2`, `Atp6v1e1`, `Ap1s2`, `Ap3b1`, `Ap4s1`, `Trappc6b`, `Trappc9`, `Trappc10`, `Vps35l`, `Vps41`, `Vps53` | 0 each | represented AP/V-ATPase/HOPS/retriever/GARP-adjacent nodes stayed silent in the focal group |
| `Vps35` | 17 | retromer-core loss produced a detectable but modest receptor/synaptic signature; top hits included `Atp2a2`, `Brsk1`, `Grin2b`, `Ccdc136`, and `Vps35` |
| `Vps54` | 31 | GARP-associated Golgi/endosome perturbation with a modest `Egr1`/`Jun`/`Atp2a2`-containing response |
| `Rab7` | 501 | a strong boundary case; induced a large late-endosomal/lysosomal/V-ATPase and sterol compensation program, including `Atp6v1b2`, `Dpp7`, `Atp6v0b`, and stress/lipid genes |

The Distributed Agents runtime comparison over the selected focal signatures agreed with the direct counts. `Sort1` and `Lrp1` had 0 significant positive and 0 significant negative features, `Gaa` had 1 significant negative feature, `Atp6ap2` had 2 significant negative features, and `Rab7` had 311 positive plus 190 negative significant features. This split argues that mild cargo receptor or individual hydrolase loss did not create a hidden shared FDR module, while strong late-endosome disruption did.

The Distributed Agents corpus supported the same interpretation:

- `Sort1:F002` reported detectable `Sort1` RNA depletion in `151 TH Prkcd Grin2c Glut` without downstream FDR signal.
- `Sort1:F003` anchored a high-confidence claim that represented lysosomal disease-related genes, including `Sort1`, `Gnptab`, `Manba`, `Ppt1`, `Psap`, and `Tmem106b`, do not elicit a shared neuronal lysosomal-stress, storage-stress, TFEB/MiT, ISR, or UPR nuclear RNA program in this acute assay.
- `Sort1:F005` contrasted flat `Sort1` with stronger core membrane-trafficking perturbations such as `Cltc` and `Vps35`.
- `Lrp1:F005` reported that LDLR-family relatives and sorting receptors in the parquet, including `Lrp2`, `Lrp4`, `Lrp5`, `Lrp6`, `Lrp8`, `Vldlr`, `Sorl1`, and `Sort1`, did not phenocopy `Lrp1`.
- `Rab7:F002` and `Rab7:F009` showed that the assay can detect a real lysosome/V-ATPase compensation program after a core `Rab7` perturbation, but that measured HOPS, retromer, WASH, V-ATPase, `Lamp2`, `Gaa`, `Grn`, and `Becn1` perturbations mostly failed to phenocopy `Rab7` at FDR level.
- In an induced Distributed Agents-corpus topology over `Atp6ap2`, `Atp6v0a1`, `Ctsb`, `Gaa`, `Lamp2`, `Lrp1`, `Psap`, `Rab7`, `Sort1`, `Vps35`, `Vps41`, and `Vps54`, all 12 were represented in one report-derived component, but only 29 of 66 candidate pairs were connected. I treated this as a connected but heterogeneous lysosome/traffic cohort rather than a pool to average.

## Target-specific reasoning

### Igf2r

`Igf2r` encodes CI-MPR/M6P-IGF2R, a recycling trans-Golgi, endosomal, and surface receptor that delivers mannose-6-phosphate-marked soluble hydrolases to endosomes/lysosomes and can internalize ligands including IGF2. This makes the missing `M6pr` gene the ideal paralog-like comparator, but `M6pr` was not a training perturbation.

The closest measured comparator was therefore `Sort1`: sortilin is a different receptor family but uses Golgi/endosomal dileucine and tyrosine motifs, binds GGA adaptors, and can support M6P-independent delivery of lysosomal cargo. In the exact focal group, `Sort1` produced 0 DEGs, and even the on-target row missed FDR 0.05. The Distributed Agents Sort1 context also found no lysosomal, autophagy, UPR/ISR, AP-1, PGRN, p75NTR/Trk, or neurotensin-receptor mRNA module. This is the strongest within-dataset evidence that a single lysosomal sorting receptor can be buffered in this P16-to-P37/44 neuron assay.

`Lrp1` was a second relevant receptor-level comparator because it participates in endocytosis of extracellular protein ligands and PGRN/prosaposin-linked lysosomal traffic with CI-MPR/Sort1-adjacent biology. It also had 0 DEGs in the focal group; the broader corpus showed that `Lrp1`, `Sort1`, `Sorl1`, and LDLR-family relatives do not form an interchangeable receptor transcriptomic module in the same dataset. I therefore did not transfer the small `Lrp6` Wnt response or any generic LDLR-family average onto `Igf2r`.

Downstream lysosomal hydrolase and lysosome-gene perturbations were also too quiet to justify a nonzero broad estimate. `Gaa`, `Ctsb`, and `Psap` each had exactly 1 DEG, and in each case the sole focal hit was the target transcript itself. `Lamp2`, `Gnptab`, `Manba`, `Asah1`, `Vps41`, `Atg5`, `Atg16l1`, and `Becn1` had 0 focal DEGs. This agrees with the known partial redundancy of M6P-dependent enzyme delivery: single CI-MPR or CD-MPR loss only partially impairs hydrolase targeting, while double loss is much more disruptive in fibroblasts (Ludwig et al. 1994).

The nonzero counterexamples argue against the alternative that the assay was simply unable to see endosomal stress. `Rab7` generated 501 DEGs in this exact group with a clear lysosomal/V-ATPase and sterol response, and `Vps35`/`Vps54` generated 17/31 DEGs. Those genes are more global trafficking hubs than `Igf2r`: `Rab7` controls late-endosome maturation, `Vps35` retromer affects retrieval of many cargoes including CI-MPR and sortilin, and GARP affects retrograde endosome-to-Golgi flow. Their focal responses define a boundary for strong organelle disruption, not the expected count for a single cargo receptor with M6P-receptor and sortilin backups.

The IGF2-receptor arm did not push the estimate up. CI-MPR/IGF2R is important for hippocampal IGF2-dependent memory consolidation and protein metabolism in adult neurons (Yu et al. 2020), but the assayed endpoint is a basal 3-to-4 week nuclear RNA state in sparse juvenile thalamic `Prkcd/Grin2c` glutamatergic neurons. Direct `Igf1r` and `Insr` perturbations had 0 DEGs in the focal group, supporting the idea that basal IGF/insulin receptor signaling was not an active transcriptomic driver here.

Combining those points, I predict that acute partial `Igf2r` loss will be buffered below the `pvals_adj < 0.05` threshold in the focal group. The closest assayed receptors are 0, the hydrolase/cargo genes mostly show only on-target self effects, and the strong `Rab7` response is mechanistically too pleiotropic. I therefore assign `Igf2r` to the modal zero class:

```tsv
target_name	predicted_n_degs
Igf2r	0
```

## Limits

The most important missing comparator is `M6pr`, the cation-dependent M6P receptor. Without it, I had to infer CI-MPR buffering from `Sort1`, `Lrp1`, individual lysosomal enzyme perturbations, and broader trafficking nodes. `Igf2r` is imprinted in mouse and multifunctional, so its guide efficiency, target-transcript down-regulation, and self-DE probability need not match `Sort1` or `Lrp1`. The screen also measures nuclear mRNA only; it does not assay hydrolase missorting, extracellular cross-correction, IGF2 uptake, lysosomal storage material, receptor protein, or surface trafficking. Finally, this prediction is for sparse postnatal NeuN-positive neurons at one harvest window and should not be extrapolated to complete embryonic `Igf2r` knockout or to glial, vascular, macrophage, or ligand-rich disease contexts.
