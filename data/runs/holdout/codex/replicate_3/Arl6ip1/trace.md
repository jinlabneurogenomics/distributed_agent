# Arl6ip1 forecast for 151 TH Prkcd Grin2c Glut

## Declared target and endpoint

- Target in the one-row holdout manifest: `Arl6ip1`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.
- `Arl6ip1` was absent from the declared 1,674-target focal count table, as intended.

## Evidence used

### Target biology

The canonical Arl6ip1 bundle supports a reachable neuronal perturbation but not a guaranteed acute stress response.

- ARL6IP1 is an integral ER membrane-shaping factor that binds/remodels membranes and promotes FAM134B/RETREG1-dependent ER remodeling and ER-phagy.
- Exact same-assay baseline reach is moderate to broad: `Arl6ip1` was detected in 15,296 of 23,679 matched non-target nuclei in the focal class, with `pct_cells_expressing = 64.6%` and `mean_cp10k = 0.734`.
- The operation stops new Arl6ip1 supply but does not instantly inactivate ER-embedded protein or already-shaped ER. No quantitative ARL6IP1 half-life, ER-complex residence time, or postmitotic-neuron ER remodeling clock was available, so functional-stock loss by P37-P44 after P16 editing was adjudicated as indeterminate.
- Constitutive mouse loss causes progressive neural and neuromuscular degeneration, so the gene is biologically consequential in neurons, but that germline, later phenotype does not establish a 21-28 day thalamic nuclear-RNA program.

### Focal training count table

The focal endpoint was highly sparse in the declared training counts:

- 1,205 / 1,674 training perturbations had `n_degs = 0`.
- 1,481 / 1,674 had `n_degs <= 1`.
- 1,546 / 1,674 had `n_degs <= 5`.
- Only 43 / 1,674 had `n_degs >= 100`.

The ER-shaping / HSP-like structural perturbations most analogous to ARL6IP1 were quiet in the same focal class:

| target | focal `n_degs` |
|---|---:|
| `Retreg1` | 1 |
| `Atl1` | 1 |
| `Atl3` | 0 |
| `Reep1` | 1 |
| `Reep2` | 1 |
| `Spast` | 0 |
| `Atf6` | 0 |
| `Vcp` | 2 |

The one-count `Retreg1`, `Atl1`, and `Reep1` signatures were self-transcript-only in the profile inspection: each had one significant negative gene, its own target transcript, and no significant positive genes in the focal class.

The focal class can detect ER/proteostasis stress when the lesion directly creates it:

| target | focal `n_degs` |
|---|---:|
| `Hspa5` | 5 |
| `Sec63` | 11 |
| `Marchf6` | 14 |
| `Atp2a2` | 187 |
| `Dhdds` | 116 |
| `Gfpt1` | 311 |
| `Psmc1` | 430 |
| `Psmb4` | 742 |
| `Ufc1` | 572 |
| `Uba5` | 2677 |

Those are not equal-scale Arl6ip1 analogs: they perturb ER chaperoning/translocation, ER Ca2+, glycosylation supply, proteasomes, or UFMylation more directly than an ER-shaping/ER-phagy membrane factor.

### Same-experiment corpus and profile context for training comparators

The packaged Retreg1 report said solitary Retreg1 loss produced an almost empty central-neuron surface, did not induce ER-stress/UPR/ER-phagy/autophagy or lysosomal transcriptional compensation, and in `151 TH Prkcd Grin2c Glut` reached significant self-mRNA depletion with zero downstream FDR<0.10 genes.

The packaged Atl1 report gave the same boundary for another structural ER/HSP module: acute postnatal `Atl1` CRISPR was pan-measured transcriptionally null beyond self, and `Atl1`, `Atl3`, `Reep1`, `Spast`, and `Vcp` were all transcriptionally buffered or very small across recovered groups.

The packaged Atf6, Hspa5, Sec63, Marchf6, and Atp2a2 reports showed that this boundary is not a blind spot for all ER stress:

- `Atf6` itself was a basal-state neuronal null, even though matched `Hspa5` and `Atp2a2` perturbations induced ER chaperone / ERAD / UPR genes.
- `Hspa5` induced a small focal ER folding/ERAD program.
- `Sec63` partially phenocopied the ER-chaperone arm in the focal class.
- `Atp2a2`, `Gfpt1`, and `Dhdds` entered much larger UPR/ISR glycosylation / ER-Ca2+ stress states.
- `Marchf6` induced a compact sterol program rather than a broad Hspa5/Ddit3/Herpud1 ER-stress state.

I compared the ER-shaping, ER-stress, ERAD, and proteostasis perturbations in the declared expression parquet within the exact focal class using signed Wilcoxon score vectors and `pvals_adj < 0.05` as the significance definition. The low ER-structural nodes had near-zero whole-profile correlations with the large stress nodes and no same-direction significant-gene overlap with them. For example, `Retreg1` had Pearson correlations of -0.003 with `Sec63`, 0.001 with `Gfpt1`, 0.007 with `Psmb4`, and 0.035 with `Dhdds`; `Atl1` and `Reep1` were similarly disconnected. By contrast, true stress states were mutually coherent, e.g. `Atp2a2` with `Gfpt1` had Pearson 0.493 with 94 same-direction significant overlaps, and `Hspa5` with `Gfpt1` had Pearson 0.378 with all four of Hspa5's positive significant genes shared in the same direction.

## Synthesis

The target is expressed broadly enough in the focal class that a self-transcript hit is plausible, and the high-yield focal group often registers such self decreases for measurable ER-structural targets. I therefore did not set the point at the all-training median of 0.

The downstream forecast stays low. Arl6ip1 shares its closest training biology with `Retreg1` and structural ER/HSP genes, whose focal outcomes were 0-1 and whose report-level signatures lacked UPR, autophagy, lysosomal, and ER-phagy compensation. The larger ER stress responses are real internal positive controls, but they come from lesions that more directly impair BiP/Sec63 chaperone cycling, ER Ca2+ loading, glycosylation, proteasomes, or UFMylation. ARL6IP1 loss could eventually disturb ER architecture and neural health, but the functional-stock card leaves the 21-28 day depletion of pre-existing ER membrane machinery unresolved.

Point forecast: one significant gene, most likely the `Arl6ip1` target transcript without a broader corrected downstream program.
