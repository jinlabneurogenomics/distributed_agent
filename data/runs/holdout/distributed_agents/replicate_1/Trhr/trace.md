# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

I interpreted the task as a one-gene held-out prediction problem: predict the focal-cell-group `n_degs` for the requested perturbation `Trhr`, where `n_degs` is the number of measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei. The requested target was completely held out, so no `Trhr` row as a perturbation exists in either the focal training-count CSV or the differential-expression parquet. Counts in the non-held-out CSV are direct observations of the same endpoint for visible training perturbations; any prediction for `Trhr` is therefore a transfer from related visible perturbations plus external biology.

I treated zero as a real prediction that no measured gene will pass BH FDR 0.05 in this exact assay. I did not treat `Trhr` self-transcript behavior as editing strength, because the assay is a sparse postnatal CRISPR loss-of-function screen and target-RNA loss is known to be an unreliable proxy for functional target engagement.

## Sources used

- Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE parquet: `training differential-expression dataset`.
- Requested-target manifest: `single-target request for Trhr`.
- Run-local dataset portrait, task bindings, coverage, capability manifest, and measurement registry in `codex_runtime/pipeline`.
- Internal same-experiment corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried through the declared Findings ledger. This is a packaged interpretation of the same Perturb-seq experiment, not an independent replicate.
- External literature from PubMed:
  - Aragay, Katz, and Simon 1992, PMID:1334076: biochemical evidence that TRH receptor couples through G-alpha-q/G-alpha-11 to phospholipase C.
  - Hinkle, Gehret, and Jones 2012, DOI:10.3389/fnins.2012.00180 / PMID:23248581: review of TRHR as a Gq/11 calcium-mobilizing GPCR with rapid phosphorylation, beta-arrestin binding, internalization, and recycling.
  - Kwon et al. 2021, DOI:10.1038/s41586-021-03413-6 / PMID:33790466: TRH-TRHR signaling in a specific COApm-to-medial-amygdala social-behavior circuit.
  - Mamedova, Dmytriyeva, and Rekling 2022, DOI:10.1016/j.npep.2022.102261 / PMID:35704969: TRH increases calcium in a subset of TRHR1-positive nodose ganglion neurons through Gq signaling.

## Dataset calculations

The requested-target CSV contained exactly one row:

```tsv
target_name
Trhr
```

The focal training endpoint was very sparse:

```text
1674 visible perturbations
1205 with n_degs = 0
469 with n_degs > 0
median = 0
75th percentile = 1
90th percentile = 2
95th percentile = 18
max = 2677
```

I then pulled focal-cell rows for mechanistic analogs by filtering the parquet to `group_name = '151 TH Prkcd Grin2c Glut'` and summarizing all measured rows per candidate:

```sql
SELECT gene_target,
       COUNT(*) AS n_measured,
       SUM(pvals_adj < 0.05) AS n_sig,
       AVG(ABS(logfoldchanges)) AS mean_abs_lfc,
       MAX(CASE WHEN names='Trhr' THEN logfoldchanges END) AS trhr_lfc,
       MAX(CASE WHEN names='Trhr' THEN pvals_adj END) AS trhr_padj,
       AVG(n_pert_matched) AS n_pert
FROM read_parquet(?)
WHERE group_name='151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

Key focal-cell counts were:

| training perturbation | rationale | focal `n_degs` |
| --- | --- | ---: |
| `Chrm3` | another Gq/PLC neuromodulatory GPCR | 0 |
| `Htr2a` | 5-HT2 Gq/PLC serotonin receptor | 0 |
| `Htr2c` | 5-HT2 Gq/PLC serotonin receptor | 0 |
| `Tacr3` | neuropeptide GPCR using Gq/Ca signaling | 0 |
| `Crhr1` | neuropeptide GPCR with sparse ligand-evoked second-messenger biology; mainly Gs but a useful receptor counterexample | 0 |
| `Tshr` | peptide-hormone GPCR, sparse neuronal singleton responses elsewhere | 0 |
| `Gnas` | heterotrimeric G-protein alpha subunit | 0 |
| `Plcb1` | proximal phospholipase C effector for Gq receptors | 0 |
| `Itpr1` | IP3 receptor downstream of PLC | 0 |
| `Gnao1` | Gi/o alpha subunit; GPCR branch counterexample | 1 |
| `Grm1` | metabotropic glutamate GPCR, Gq/PLC linked | 1 |
| `Camk2b` | calcium-dependent kinase downstream of many neuronal signals | 1 |
| `Grin1` | obligate NMDA ion-channel subunit in the same broad excitability space | 89 |

All 13 canonical immediate-early or activity-response sentinels I checked in the focal-cell parquet (`Fos`, `Fosb`, `Jun`, `Egr1`, `Egr2`, `Egr3`, `Arc`, `Npas4`, `Bdnf`, `Nr4a1`, `Nr4a2`, `Nr4a3`, `Crem`) had `pvals_adj = 1` after `Chrm3`, `Htr2a`, `Htr2c`, `Tacr3`, `Crhr1`, `Tshr`, `Gnas`, `Plcb1`, `Itpr1`, `Gnao1`, `Grm1`, and `Camk2b` loss in the focal cell group. The exception among the broader panel was `Grin1`, whose focal response included 89 DEGs and `Jun` at FDR 0.00017; this argues that this focal class can report a stable excitability-associated nuclear response for the right perturbation, but that response does not transfer from the NMDA receptor core to isolated TRHR loss.

As QC context only, measured `Trhr` transcript was never FDR-significant at 0.05 in any visible perturbation/cell-group signature in the supplied parquet. That says `Trhr` itself was not a recurrent downstream DEG in the training screen; it does not measure the missing `Trhr` knockout signature.

## Same-experiment corpus checks

There was no packaged Finding for held-out `Trhr` in the July 260713 sourceguard corpus.

The nearest target-specific packaged reports reinforced the focal CSV calculation:

- `Chrm3`: the report called M3 muscarinic receptor loss a class-wide basal neuronal-transcriptome null, with zero downstream genes at FDR 0.10 or even FDR 0.25 in every modeled neuronal group. It also explicitly found no convergence with represented cholinergic/Gq/excitability targets including `Plcb1`, `Itpr1`, `Grm1`, and `Grm5`.
- `Htr2c`: the 5-HT2C report found no corrected downstream response in any recovered broad neuronal class and no convergence with the 5-HT receptor family or proximal second-messenger comparators, despite known organismal phenotypes of HTR2C loss.
- `Tacr3`: the NK3R report found only a single robust event in hypothalamic/central-nuclei GABA neurons and no broad immediate-early, neuropeptide, Gq, or KNDy/GnRH-axis program.
- `Crhr1`: CRHR1 produced a single-gene event outside the focal class; the report stated that ligand-evoked cAMP/PKA/CREB immediate-early biology was absent after basal loss of function.
- `Tshr`: TSHR produced three singleton events in other classes, did not affect the focal class, and did not converge with obvious `Gnas`/adenylyl-cyclase/PKA/CREB pathway comparators.
- `Gnao1`: the Gi/o alpha-subunit report found a one-gene response in one cortical class and no chronic broad GPCR/cAMP transcriptome.

Those reports are not used as independent validation of the parquet. They are useful because they show that several represented peptide and monoamine GPCRs with established electrophysiological or ligand-evoked signaling are buffered or state-missing in this exact P16-to-P37/44 basal NeuN-positive nuclear-RNA assay.

## Target-specific prediction

### `Trhr`: predict 0 DEGs

Biology: `Trhr` encodes the thyrotropin-releasing hormone receptor. The receptor is a calcium-mobilizing GPCR: TRH receptor activation stimulates PIP2 hydrolysis through Gq/G11 and phospholipase C (Aragay, Katz, and Simon 1992, PMID:1334076), and its canonical proximal response is calcium and PKC activation followed by rapid GRK/arrestin-mediated desensitization and internalization (Hinkle, Gehret, and Jones 2012, DOI:10.3389/fnins.2012.00180). TRH/TRHR can clearly matter in selected neuronal circuits, including TRHR-dependent medial-amygdala suppression of mating with unhealthy partners (Kwon et al. 2021, DOI:10.1038/s41586-021-03413-6) and Gq-dependent calcium entry in TRHR1-positive nodose ganglion neurons (Mamedova, Dmytriyeva, and Rekling 2022, DOI:10.1016/j.npep.2022.102261).

Experimental transfer: the intervention is sparse CRISPR loss of `Trhr`, which would directly impair TRH receptor protein in edited, recovered neurons. The direct molecular consequence would be loss of ligand-gated Gq/PLC/IP3/Ca signaling. Propagation to a stable broad RNA program would require the focal `151 TH Prkcd Grin2c Glut` neurons to express TRHR at a functionally relevant level, receive enough TRH tone or post-editing compensatory input during the 3-4 week window, and convert that altered second-messenger signal into a chronic nuclear transcriptome that survives BH correction. The training data argue that this propagation step usually fails for single neuromodulatory GPCR perturbations in this assay: focal `Chrm3`, `Htr2a`, `Htr2c`, `Tacr3`, `Crhr1`, and `Tshr` perturbations all had 0 focal DEGs, as did proximal `Plcb1`, `Itpr1`, and `Gnas` perturbations. `Gnao1`, `Grm1`, and `Camk2b` each produced only a one-gene focal response.

Counterexamples considered: `Grin1` produced 89 focal DEGs, showing the cell class can produce a corrected transcriptome when a core ionotropic glutamate receptor is perturbed. I did not transfer that count to `Trhr`, because an obligate NMDA receptor pore subunit is continuously used by glutamatergic neurons and sits closer to excitatory synaptic transmission than a single TRH peptide receptor. Broader GPCR family membership also did not support a nonzero call: every serotonin, cholinergic, opioid, adrenergic, NPY, galanin, CRH, NK3, adenylyl-cyclase, PLC, and IP3 receptor training target I found by name in the focal training CSV was zero except `Gnao1`, `Gpr158`, and `Gprasp2` at one DEG.

I therefore predict a focal `Trhr` DEG count of `0`. This is driven mostly by within-dataset receptor and Gq-pathway nulls, with external TRHR literature used only to choose the appropriate analogs and to avoid overinterpreting the null as absence of ligand-evoked or circuit physiology.

## Limits and uncertainty

- The true `Trhr` perturbation signature is absent by construction, so the prediction is an extrapolation from other receptors rather than a direct expression-signature match.
- The supplied DE parquet has normalized differential expression, Wilcoxon statistics, adjusted p-values, and matched recovered nucleus counts; it does not contain raw counts, guide-level editing rates, ligand exposure, membrane calcium fluxes, receptor phosphorylation, or neuronal firing.
- `Trhr` could be expressed in a rare thalamic subpopulation or engaged only during a state not sampled by the basal P37-44 snRNA-seq snapshot. A state-locked or rare-subtype TRH effect could be missed while still being biologically real.
- The visible `Gnaq` and `Gna11` perturbations were not present in the focal training-count CSV, so I used `Plcb1`, `Itpr1`, calcium/CaMK, and represented Gq-coupled GPCRs as local pathway analogs.
- Same-experiment corpus Findings summarize the same Perturb-seq experiment as the parquet and are used as interpretation, not as independent replication.
