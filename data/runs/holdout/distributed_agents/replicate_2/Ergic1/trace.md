# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question interpreted

The requested manifest contains one held-out target, `Ergic1`. I interpreted the task as a point prediction of the number of measured genes that would have `pvals_adj < 0.05` in the held-out `Ergic1` CRISPR loss-of-function contrast in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. The count includes any measured gene, including the perturbed transcript if it reaches FDR, but the held-out `Ergic1` contrast itself was not used because it is absent from both supplied training inputs.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene log2 fold changes, Wilcoxon statistics and BH-adjusted p-values for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact endpoint counts for 1,674 non-held-out training perturbations in the focal cell group.
- `072_Ergic1.csv`: requested target manifest; this contained only `Ergic1`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`: queried `Ergic1` and found no Claims, Findings, or explicit same-experiment references for this target.
- UniProtKB release `2026_03`, reviewed mouse entry `Q9DC16` / `ERGI1_MOUSE`, and its GO Central cross-references.
- PubMed literature search for ERGIC1 / ERGIC-32. The key target-specific paper was Breuza et al. 2004, which identified ERGIC-32 as a cycling ER-Golgi-intermediate-compartment membrane protein that interacts with human Erv46 and stabilizes it, DOI `10.1074/jbc.M406644200`, PMID `15308636`.
- For general ERGIC biology, I also checked Reiterer et al. 2008 showing neuronal GAT1 axonal sorting requires COPII export and passage through the ERGIC, DOI `10.1523/JNEUROSCI.3451-08.2008`, PMID `19020038`, and Camus et al. 2020 showing a role for an ERGIC-derived traffic route in GLUT4 pathway biogenesis, DOI `10.1083/jcb.201812135`, PMID `31863584`.

## Dataset calibration

The training endpoint is highly sparse and heavy-tailed in the focal group:

- 1,674 training perturbations.
- 1,205 had `n_degs = 0`.
- 363 had `1 <= n_degs < 10`.
- 63 had `10 <= n_degs < 100`.
- 43 had `n_degs >= 100`.
- Median `n_degs = 0`, 75th percentile `= 1`, 95th percentile `= 18`, maximum `= 2677`.

I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to manually selected ER/Golgi, ERGIC, COPII, COPI, COG/TRAPP, retrograde, and endolysosomal traffic targets that were present in the training target list. For each selected training target I recomputed the endpoint as `sum(pvals_adj < 0.05)` from the filtered rows and inspected the FDR-significant genes.

The nearest available early-secretory perturbations were quiet:

| training target | observed `n_degs` | focal expression evidence | why compared |
|---|---:|---|---|
| `Sar1b` | 0 | no FDR-significant genes; best adjusted p-value was the `Sar1b` transcript itself, `p_adj = 0.108`, logFC `-0.615` | COPII GTPase for ER export, upstream of ERGIC arrival |
| `Sec23a` | 0 | no FDR-significant genes; best adjusted p-value `0.873`; `Sec23a` logFC was `-0.351` | COPII inner-coat component for ER-to-Golgi vesicle formation |
| `Copa` | 0 | no FDR-significant genes; best adjusted p-value `0.364` | COPI coatomer alpha subunit for Golgi-to-ER recycling |
| `Copg1` | 1 | the only DEG was `Copg1` itself, logFC `-0.668`, `p_adj = 9.24e-17` | COPI coatomer gamma subunit; a useful boundary because only the targeted RNA passed FDR |
| `Lman2l` | 0 | no FDR-significant genes; best adjusted p-value was the `Lman2l` transcript, `p_adj = 0.603`, logFC `-0.629` | lectin-like early secretory cargo receptor rather than a core COP subunit |
| `Stx5a` | 0 | no FDR-significant genes | ER/Golgi SNARE traffic |
| `Cog4` | 0 | no FDR-significant genes | conserved oligomeric Golgi tethering complex; later Golgi recycling |
| `Cog5` | 0 | no FDR-significant genes | conserved oligomeric Golgi tethering complex; later Golgi recycling |
| `Trappc9` | 0 | no FDR-significant genes | TRAPP tethering complex; Golgi/endosome traffic rather than ERGIC-specific |
| `Trappc10` | 0 | no FDR-significant genes | TRAPP tethering complex; Golgi/endosome traffic rather than ERGIC-specific |
| `Rab18` | 0 | no FDR-significant genes | ER/lipid-droplet-associated Rab included as a small-GTPase trafficking boundary |

The strongest trafficking counts came from farther biology and did not justify transferring a broad effect to `Ergic1`:

| counterexample target | observed `n_degs` | focal expression evidence | interpretation for `Ergic1` |
|---|---:|---|---|
| `Sec63` | 11 | significant ER-stress/chaperone genes such as `Hspa5`, `Canx`, and `Hyou1` were induced | `Sec63` is an ER translocon/protein-folding factor; this mild UPR-like response is plausible for ER import stress, but is not the same as partial loss of an ERGIC cycling protein |
| `Vps35` | 17 | DEGs included `Atp2a2`, `Grin2b`, `Ccdc136`, and the target `Vps35` | retromer/endosomal recycling is downstream and farther from ERGIC cargo selection |
| `Vps54` | 31 | DEGs included `Egr1`, `Jun`, `Kctd16`, `Stmn4`, and cytoskeletal/neuropeptide-associated transcripts | Golgi-associated retrograde trafficking, broader than a non-core ERGIC cargo protein |
| `Vcp` | 2 | two weak DEGs, `Rasgef1b` and `Nsmf` | ubiquitous proteostasis/ERAD factor; not an ERGIC-specific analog |
| `Rab7` | 501 | broad lysosomal/endosomal signature with DEGs such as `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`, `Dusp1`, and `Insig1` | late endosome and lysosome regulation; biologically too far downstream and much broader than the COPII/COPI controls |

The runtime profile comparison among `Sar1b`, `Sec23a`, `Copa`, `Copg1`, `Lman2l`, `Cog4`, `Cog5`, `Vps35`, `Vps54`, `Sec63`, `Vcp`, and `Rab7` found that six of the twelve candidate profiles had no FDR-significant features and that the direct early-secretory controls were in this null or self-only class. The broad `Rab7` state did not share FDR-significant genes with the null COPII/COPI targets because those targets had no significant downstream genes in this focal cell group.

## Target-specific reasoning

### `Ergic1`

ERGIC1 is the mouse ortholog of ERGIC-32, a multi-pass membrane protein that cycles among ER, ERGIC, and Golgi membranes; UniProtKB `Q9DC16` annotates it to ER-to-Golgi vesicle-mediated transport (`GO:0006888`), retrograde Golgi-to-ER transport (`GO:0006890`), the COPII-coated ER-to-Golgi vesicle (`GO:0030134`), and the ERGIC membrane (`GO:0033116`). Breuza et al. 2004 identified human ERGIC-32 in purified ERGIC membranes and showed by siRNA that it affects turnover of hErv46, supporting a role as an ERGIC cycling/protein-stability factor rather than as the central COPII or COPI coat itself.

That biology makes the most relevant in-dataset analogs `Sar1b`, `Sec23a`, `Copa`, and `Copg1`: all perturb core transport between ER, ERGIC, and Golgi. All were null or nearly null in the exact held-out endpoint: `Sar1b = 0`, `Sec23a = 0`, `Copa = 0`, and `Copg1 = 1`, with `Copg1`'s lone DEG being the target transcript. `Lman2l = 0` provides a cargo-receptor-like early-secretory comparator, and `Stx5a`, `Cog4`, `Cog5`, `Trappc9`, `Trappc10`, and `Rab18` were also zero. These direct training observations are stronger for the count prediction than the generic expectation that membrane-traffic defects can stress neurons.

The medium and strong counterexamples were mechanistically farther from ERGIC1. `Sec63 = 11` looked like a mild ER-stress/quality-control response, consistent with the fact that SEC63 is an ER translocon partner rather than an ERGIC cycling protein. `Vps35 = 17`, `Vps54 = 31`, and especially `Rab7 = 501` involve retromer or late endosomal/lysosomal biology and had response genes that are not evidence that a partial acute `Ergic1` knockout should exceed FDR in this sparse nuclear-RNA assay.

Based on the direct COPII/COPI/cargo-receptor analogs, I expect `Ergic1` to be silent at FDR 0.05 in this focal readout. A possible alternative would be a one-DEG count if the perturbed `Ergic1` transcript itself were strongly depleted, analogous to `Copg1`; however, self-transcript loss is unreliable in this CRISPR/single-nucleus design and `Sar1b` and `Lman2l` both showed sub-threshold target-RNA changes without downstream DE. I therefore make the integer prediction:

`Ergic1 -> 0`

## Limits and extrapolations

- The selected Distributed Agents same-experiment corpus had no `Ergic1` Claim or Finding, so there was no internal curated mechanism or comparator for the held-out target.
- Perfect paralog or complex-member controls were missing: the training DEG table did not contain `Ergic2`, `Ergic3`, `Lman1`, `Mcfd2`, or `Tmed` targets.
- Several null analogs had modest matched perturbed-cell counts in the focal group, such as `Copa` with 75 and `Sar1b` with 112 matched nuclei versus 23,679 controls, so a small biological effect could fail to pass BH correction.
- ER/Golgi transport genes are not interchangeable. ERGIC1 could have a cargo-specific role not captured by `Sar1b`, `Sec23a`, or COPI perturbations, and human cancer-cell or HepG2 ERGIC-32 experiments are only functional priors for postnatal mouse neurons.
- The final zero is an endpoint prediction for FDR-significant DEG count, not a claim that ERGIC1 is biologically dispensable, unexpressed, or unedited in this experiment.
