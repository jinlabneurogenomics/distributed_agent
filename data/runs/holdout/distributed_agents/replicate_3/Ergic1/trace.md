# Trace

## Question and endpoint

The requested held-out perturbation set for this run is the single mouse target `Ergic1`. I interpreted the endpoint as the focal-cell count of measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, using the same Benjamini-Hochberg-adjusted Wilcoxon calculation that produced `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.

The held-out `Ergic1` signature is absent from both the all-cell differential-expression parquet and the focal training-count CSV, so the prediction has to be transferred from non-held-out perturbations. I treated `0` as a prediction that no gene, including `Ergic1` itself, would pass the focal FDR threshold; weak target-RNA depletion was therefore not counted unless the analogous training target actually cleared FDR.

## Sources used

- Input count endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE signatures: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 072_Ergic1.csv]`.
- Same-experiment Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, queried for ER-Golgi, COPI, COG, SNARE, Golgi, and retrograde-trafficking claims and candidate topology.
- Distributed Agents run-local profile comparison over the focal log-fold-change vectors for ER-Golgi candidate training targets.
- PubMed-indexed literature:
  - Breuza et al. 2004, J. Biol. Chem., DOI `10.1074/jbc.M406644200`, PMID `15308636`: ERGIC-32/ERGIC1 is an ER-Golgi intermediate-compartment cycling membrane protein that partially colocalizes with human Erv41/Erv46 and stabilizes hErv46.
  - Peotter et al. 2019, Traffic, DOI `10.1111/tra.12654`, PMID `31059169`: review of COPII-mediated ER-to-ERGIC trafficking and the ER/ERGIC interface.
  - Fu et al. 2019, Biochem. Biophys. Res. Commun., DOI `10.1016/j.bbrc.2019.02.053`, PMID `30791981`: neuronal cargo-receptor evidence for LMAN1/ERGIC-53 in trafficking endogenous Cys-loop neuroreceptors.

I found no direct `Ergic1` node in the selected Distributed Agents corpus release, and direct `Ergic1`, `Ergic2`, `Ergic3`, or `Lman1` perturbations were not present as focal training targets. The prediction below is therefore a pathway transfer from sampled early secretory-pathway and Golgi-trafficking perturbations.

## Computational checks

The focal training endpoint contains 1,674 observed non-held-out targets. It is very sparse: 1,205 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and the top few perturbations are much broader chromatin, RNA-processing, proteostasis, or signaling nodes rather than generic endomembrane targets.

I searched the training-count symbols for ERGIC/ER-Golgi-adjacent targets, then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and those `gene_target` values:

```python
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
    & (pc.field("pvals_adj") < 0.05)
)
```

This retrieved the FDR-significant genes for each candidate so that singleton self-target effects and biologically different counterexamples would not be mistaken for a shared secretory-pathway state.

The relevant focal training counts were:

| target | focal `n_degs` | interpretation for `Ergic1` |
| --- | ---: | --- |
| `Sec23a` | 0 | COPII coat, ER-to-Golgi export; direct early secretory analog but no focal DEG |
| `Sar1b` | 0 | COPII initiator GTPase; direct early secretory analog but no focal DEG |
| `Copa` | 0 | COPI retrograde coatomer subunit; ERGIC/Golgi recycling analog but no focal DEG |
| `Copg1` | 1 | COPI subunit; the only FDR gene was `Copg1` itself, log2FC -0.668 |
| `Stx5a` | 0 | ER-Golgi SNARE; no focal DEG |
| `Trip11` | 0 | GMAP-210 golgin, ER-Golgi/ERGIC tether; no focal DEG |
| `Cog4` | 0 | conserved oligomeric Golgi tether; no focal DEG |
| `Cog5` | 0 | COG subunit; no focal DEG |
| `Tmem165` | 0 | Golgi ion/glycosylation homeostasis; no focal DEG |
| `Vps53` | 0 | GARP/EARP retrograde transport subunit; no focal DEG |
| `Lman2l` | 0 | ERGIC-53-like lectin family cargo receptor; no focal DEG |
| `Tango2` | 0 | secretory/ER-Golgi associated candidate found by symbol search; no focal DEG |
| `Sec63` | 11 | ER translocon/ER-proteostasis counterexample; induced `Hspa5`, `Canx`, `Hyou1`, and `Chac1`, unlike the ER-Golgi analogs |
| `Vps35` | 17 | retromer counterexample; the signature contained `Atp2a2`, `Grin2b`, target-gene `Vps35`, and other private hits |
| `Vps54` | 31 | GARP counterexample; the signature included `Egr1`, `Jun`, `Atp2a2`, tubulin/neurofilament genes, and other neuronal-process genes |

I also ran a Distributed Agents profile comparison on these focal log2 fold-change vectors. Among 14 ER/Golgi candidates, 11 had no FDR-significant focal features, one had only the `Copg1` singleton, and only `Vps35` and `Vps54` reached the 10-to-49-DEG bin. The pairwise tables showed no FDR-scale overlap between `Vps54` and the flat direct ER-Golgi comparators and only one negative significant overlap between `Vps54` and `Vps35`, supporting the same-experiment corpus conclusion that `Vps54` is a target-specific later-retrograde outlier rather than the expected breadth for any ERGIC loss.

## Distributed Agents corpus evidence

Several same-experiment corpus claims directly bounded the analog choice.

The broadest relevant claim, `claim:6a94b158a9de9a66a6c3`, states with moderate confidence that represented ER-Golgi trafficking and Golgi glycosylation-homeostasis perturbations do not produce a shared broad secretory-pathway transcriptional module in postmitotic neurons. Its scope explicitly covers ER-Golgi transport, COPI, COG, SNARE, and Golgi/CDG perturbations, and its target set includes `Cog4`, `Copa`, `Copg1`, `Stx5a`, `Tmem165`, and `Trip11`.

Two narrower claims were useful guards against over-transfer:

- `claim:b89761117684a2c84377`: `Copa` and `Copg1` do not produce a shared COPI-collapse transcriptional signature in matched postnatal neuronal groups. This made the one-gene `Copg1` focal result look like a target-RNA singleton, not a hidden COPI module.
- `claim:1d7844ef6515526be72d`: represented Golgi and retrograde-trafficking perturbations do not collapse into a generic neuronal transcriptional stress state. The supporting `Vps53`/`Vps54` findings note that same-GARP-complex membership was insufficient for an FDR-scale shared neuronal phenotype: `Vps54` was active in 151, whereas `Vps53` was weak or flat.

The candidate-set topology audit over `Cog4`, `Cog5`, `Copa`, `Copg1`, `Lman2l`, `Sar1b`, `Sec23a`, `Stx5a`, `Tmem165`, `Trip11`, `Vps35`, `Vps53`, and `Vps54` placed all 13 represented nodes in one report-derived component, but the largest fully connected ER-Golgi set was the flat six-node group `Cog4/Copa/Copg1/Stx5a/Tmem165/Trip11`. I therefore treated the topology as confirmation that the chosen comparators were mechanistically relevant, not as a reason to average in `Vps54` or `Vps35`.

## Target-specific prediction

### `Ergic1`

`Ergic1` encodes ERGIC-32, a cycling membrane protein of the ER-Golgi intermediate compartment that modulates the Erv41/Erv46 complex in the early secretory pathway (Breuza et al. 2004). The most appropriate training analogs are therefore the sampled ER-to-Golgi and ERGIC/Golgi recycling components: `Sec23a` and `Sar1b` for COPII export, `Copa` and `Copg1` for COPI recycling, `Stx5a` for ER-Golgi SNARE fusion, `Trip11` for an ERGIC/Golgi tether, and `Cog4`/`Cog5`/`Tmem165` as nearby Golgi-homeostasis perturbations. In `151 TH Prkcd Grin2c Glut`, all of these were flat except for the one-gene `Copg1` self-repression call.

The nonzero counterexamples were less compelling for `Ergic1`. `Sec63` produced a small ER proteostasis/UPR-like response including `Hspa5`, `Canx`, `Hyou1`, and `Chac1`, but `Sec63` is an ER translocon factor rather than an ERGIC recycling protein. `Vps35` and `Vps54` are later retromer/GARP perturbations with private thalamic signatures; the `Vps54` response was explicitly not reproduced by same-complex `Vps53` or by the COG/COPI/SNARE neighbors. Those signatures argue that the assay can detect selected trafficking perturbations, but they do not justify assigning a nonzero effect to every endomembrane component.

The strongest evidence is thus within-dataset: the direct ER-Golgi/COPII/COPI/SNARE/TMEM165/TRIP11 neighborhood was almost uniformly `0`, and the same-experiment Distributed Agents claims call out absence of a broad postmitotic neuronal secretory-pathway transcriptional module. The external ERGIC1 literature places the held-out target in that buffered early secretory-pathway class and does not identify a specific basal thalamic transcriptional regulator role that would override the data.

I predict `Ergic1` will have no downstream or self FDR<0.05 calls in the focal group: `predicted_n_degs = 0`.

## Limits

The prediction is extrapolative because the closest same-complex ERGIC1 partners `Ergic2` and `Ergic3`, and the ERGIC cargo receptor `Lman1`, were not available as training perturbations. The focal endpoint is also sensitive to guide efficiency, target transcript abundance, and the recovered perturbed-nucleus count; a strong enough target-RNA depletion alone could turn a biologically flat perturbation into `n_degs = 1`. Finally, the screen reports nuclear RNA several weeks after sparse postnatal CRISPR loss and does not assay ERGIC morphology, cargo-receptor protein stability, glycan state, or membrane-trafficking kinetics, so a biochemical trafficking defect could be present even when `n_degs` is zero.
