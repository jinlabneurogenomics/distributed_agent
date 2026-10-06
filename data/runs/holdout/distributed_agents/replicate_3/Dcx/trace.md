# Prediction trace

## Question and resolution

The requested endpoint is the exact `151 TH Prkcd Grin2c Glut` focal-cell DEG burden for held-out `Dcx`: the number of measured genes with `pvals_adj < 0.05` in the Wilcoxon differential-expression table after acute mosaic AAV-CRISPR loss of function.

I treated `151 TH Prkcd Grin2c Glut` as thalamic glutamatergic neurons, not dopaminergic TH neurons, following the supplied Allen-taxonomy context. I also treated target-transcript knockdown as a possible significant row but not as a direct editing-efficiency score; weak target mRNA in this assay can coexist with functional indels, and the endpoint is simply the thresholded single-nucleus RNA signature.

Only one target was requested:

```tsv
target_name
Dcx
```

`Dcx` is not present in the training DEG-count CSV and the Distributed Agents same-experiment corpus had no `Dcx` target card, so all prediction is transfer from observed analogs plus external doublecortin biology.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: authoritative training `n_degs` in the focal cell group for 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`: authoritative per-gene focal-cell log2 fold changes and adjusted p-values. I filtered it to `group_name = '151 TH Prkcd Grin2c Glut'`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`: same-experiment semantic Findings and Claims for `Map1b`, `Mapt`, `Tuba1a`, and `Dctn1`. The corpus explicitly returned `target_found: false` for `Dcx`.
- Distributed Agents runtime `profile_neighbors`: signed-profile neighbor audit over candidate microtubule, motor, dynactin, Reelin/LIS1-adjacent, and Rho-GTPase training perturbations in the focal cell group; artifact `cytoskeletal_profile_neighbors.json`.
- PubMed literature:
  - Friocourt et al. 2003, DOI `10.1093/cercor/13.6.620`: doublecortin as a developmentally regulated postmitotic-neuron microtubule-associated protein localized to growing neuritic/leading processes.
  - Moores et al. 2004, DOI `10.1016/j.molcel.2004.06.009`: DCX stabilizes 13-protofilament microtubules by binding at a stabilizing inter-protofilament site.
  - Deuel et al. 2006, DOI `10.1016/j.neuron.2005.10.038`: Dcx and Dclk show partial genetic redundancy in mouse; double mutants have severe neuronal migration and axon-outgrowth/transport phenotypes.
  - Koizumi et al. 2006, DOI `10.1016/j.neuron.2005.10.040`: Dcx and Dclk interact dosage-dependently in fiber-tract decussation, neuronal migration, and axonal wiring.
  - Baek et al. 2014, DOI `10.1016/j.neuron.2014.04.036`: some in utero Dcx/Dclk shRNA migration phenotypes are shRNA/miRNA-pathway off-target effects, reinforcing that Dcx single-gene loss in mouse is milder than knockdown literature can imply.

## Computations

I first summarized the training endpoint in the focal group. The distribution is sparse and strongly right-skewed:

- 1,674 training perturbations.
- Median `n_degs = 0`; 469/1,674 are nonzero.
- 75th percentile = 1 DEG, 90th percentile = 2, 95th percentile = 18.
- A few generic RNA-processing/proteostasis/chromatin targets account for the large right tail, with `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`.

For repeated signature inspection, I materialized the focal-cell rows:

```sql
COPY (
  SELECT names, gene_target, logfoldchanges, pvals_adj, scores,
         n_pert_matched, n_ctrl_matched
  FROM read_parquet('training_de_all_cell_groups.parquet')
  WHERE group_name = '151 TH Prkcd Grin2c Glut'
) TO 'focal_151_TH_Prkcd_Grin2c_Glut.parquet'
  (FORMAT PARQUET, COMPRESSION ZSTD);
```

That slice contains 28,891,566 rows: 1,674 targets by 17,259 measured genes. I then counted and listed rows with `pvals_adj < 0.05` for candidate Dcx analogs, and ran `profile_neighbors` on `Map1b`, `Mapt`, `Tuba1a`, `Kif1a`, `Dctn1`, `Rac1`, `Cdc42`, `Mark3`, `Dab1`, `Reln`, `Vldlr`, `Lrp8`, `Stmn2`, and `Spast`.

The neighbor audit was used as falsification rather than as a tuned score. It confirmed the Distributed Agents-corpus finding that measured MAP/tubulin/motor perturbations do not collapse into a coherent shared cytoskeletal-stress mRNA module in this postnatal snRNA-seq surface; `Tuba1a` and `Dctn1` are visible, but with narrow tubulin-isotype and sterol/SREBF2-like programs, respectively.

## Dcx-specific analogs

`Dcx` encodes doublecortin, a neuronal microtubule-associated protein for migration, leading-process/neurite dynamics, and axonal wiring. The closest mechanistic comparison would have been `Dclk1`, because Dcx and Dclk genetically compensate in mouse neurodevelopment, but `Dclk1`/`Dclk2` were not present as training perturbations. I therefore compared `Dcx` to represented partial analogs and counterexamples:

```tsv
training_target	151_TH_n_degs	signature evidence in the focal group	interpretation for Dcx
Map1b	1	Only Map1b itself was significant, logFC -0.358.	The best present structural MAP analog was self-only; argues against a broad postnatal MAP compensation program.
Mapt	1	Only Mapt itself was significant, logFC -0.533.	Tau loss was self-only; the same-experiment corpus reports no MAP-family/tubulin mRNA compensation after Mapt perturbation.
Map6	0	No significant focal-cell genes.	Another structural microtubule-associated perturbation that was buffered at this RNA endpoint.
Mapre2	1	Only Mapre2 itself was significant, logFC -0.464.	EB-family microtubule plus-end biology did not produce a secondary transcriptome.
Stmn2	1	Only Stmn2 itself was significant, logFC -1.001.	Direct microtubule-dynamics/growth-cone node but no broad module.
Spast	0	No significant focal-cell genes.	Microtubule severing did not generate a focal-cell RNA program.
Kif1a	1	Only Kif1a itself was significant, logFC -0.561.	KIF1A is a DCX/DCLK-dependent synaptic-vesicle transport effector in the literature, but perturbing Kif1a was self-only.
Kif5a	1	Only Kif5a itself was significant, logFC -0.445.	Kinesin perturbation counterexample; no shared motor-stress response.
Kif5c	1	Only Kif5c itself was significant, logFC -0.528.	Same as Kif5a.
Dctn1	75	Up-regulated Insig1, Msmo1, Hmgcs1, Cyp51, Hmgcr, Fdft1, Fdps, Ldlr and other sterol/lipid genes; Dctn1 itself was down.	Positive detectability control for microtubule transport, but the SREBF2-like sterol response is a dynactin/endolysosomal trafficking state, not a Dcx/MAP state.
Tuba1a	7	Tuba1a was down and six other alpha/beta tubulins were up.	Positive detectability control for tubulin dosage, but the response is structural-tubulin feedback and is not seen for most MAPs or motors.
Tuba4a	2	Tuba4a itself plus one isolated Mast1 call.	Tubulin paralog perturbation was much weaker than Tuba1a.
Tubb4b	1	Only Tubb4b itself was significant.	Another tubulin counterexample.
Tubb5	1	Only Tubb5 itself was significant.	Another tubulin counterexample.
Cdc42	1	Only Cdc42 itself was significant.	Rho-family migration/polarity signaling was self-only.
Rac1	0	No significant focal-cell genes.	Rho-family migration/polarity signaling was silent.
Pak1	1	Only Pak1 itself was significant.	Downstream actin/cytoskeleton kinase was self-only.
Pak2	0	No significant focal-cell genes.	Counterexample in same kinase family.
Pak3	0	No significant focal-cell genes.	Counterexample in same kinase family.
Mark3	0	No significant focal-cell genes.	The represented MARK kinase did not engage tau/MAP-polarity transcriptional axes.
Dab1	0	No significant focal-cell genes.	Reelin-positioning pathway perturbation was silent.
Reln	0	No significant focal-cell genes.	Reelin-positioning pathway perturbation was silent.
Vldlr	0	No significant focal-cell genes.	Reelin receptor perturbation was silent.
Lrp8	0	No significant focal-cell genes.	Reelin receptor perturbation was silent.
Ywhae	0	No significant focal-cell genes.	LIS1/migration-adjacent adaptor counterexample.
```

Two corpus-level Findings were especially relevant. First, the `Map1b`/`Mapt`/`Tuba1a`/`Tubb4b` component contains a high-confidence Claim that represented microtubule-associated and tubulin perturbations generally do not form a coherent postnatal neuronal cytoskeletal-stress module, apart from the restricted `Tuba1a` tubulin-isotype response. Second, the `Dctn1` corpus record shows that a microtubule-transport perturbation can be very visible in the same assay, but through a sterol/cholesterol homeostasis program that many cytoskeletal neighbors fail to phenocopy.

## Zero/nonzero decision

The external biology pushes `Dcx` toward an early developmental structural role: it binds and stabilizes neuronal microtubules, is important for migration and axonal wiring, and is buffered in mouse by DCLK-family proteins. Those are real functions, but they are poorly matched to this endpoint for three reasons.

First, the assay perturbed sparse postmitotic neurons at P16 and harvested at P37-P44. `Dcx` phenotypes are strongest during embryonic and newborn-neuron migration; the focal group is mature thalamic glutamatergic neurons, not a neurogenic population. Second, the represented postnatal cytoskeletal analogs were mostly zero or self-only, so the training data provide a concrete local prior that single MAP, motor, and migration-pathway perturbations usually do not produce many focal-cell DEGs. Third, the two counterexamples with visible signatures do not transfer cleanly: `Tuba1a` reports tubulin stoichiometry feedback, and `Dctn1` reports a vesicle/endolysosomal sterol response.

The main positive risk is a one-gene self-target call: several analogs have `n_degs = 1` solely because their own transcript was depleted. I chose `0` rather than `1` because `Dcx` is developmentally regulated and is not a marker of this mature thalamic class, so a robust Dcx self-transcript depletion at FDR 0.05 is less likely than for `Map1b`, `Mapt`, or `Kif1a`, which were expressed enough to self-call.

## Limits

- Baseline expression for `Dcx` in `151 TH Prkcd Grin2c Glut` was not supplied; the DE table can show perturbation responses but not direct unperturbed abundance for a held-out target.
- `Dclk1`, the closest paralog and partial functional compensator, was absent from the observed training perturbations in the focal cell group, so the comparison is through less direct MAP, motor, and migration-pathway genes.
- The external Dcx literature is mostly embryonic, germline, in utero knockdown, or cultured-neuron work. Acute sparse P16 CRISPR in recovered juvenile thalamic nuclei could miss axon-transport, morphology, or protein-localization defects that would matter biologically.
- This prediction is a point estimate for a thresholded, power-dependent DEG count. A true count of 1 from a self-transcript effect would not materially contradict the biological conclusion that Dcx is expected to lack a broad downstream RNA state here.

Predicted `n_degs` for `Dcx`: **0**.
