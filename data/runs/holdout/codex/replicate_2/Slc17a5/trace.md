# Slc17a5 n_degs forecast

Target perturbation: `Slc17a5`

Focal population: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `1`

## Evidence used

- The declared manifest and biology bundle both identify the only target as `Slc17a5`; the selected same-experiment corpus release had no `Slc17a5` Finding, Claim, or explicit report reference, so no report-derived target outcome was available or used.
- The target biology bundle says Slc17a5 function is sialin in lysosomal and neuronal vesicular membranes. A P16 disruptive edit should stop production of new functional transporter while pre-existing transporter persists until membrane turnover; neuronal lysosomal-proteome proxies make substantial stock decline by the P37-P44 harvest plausible over the 21-28 day interval, but target-specific sialin kinetics are not known.
- Exact focal expression reach was moderate: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, Slc17a5 was detected in 11,054 of 23,679 cells, 46.6827%, with mean raw UMI 0.6972, mean CP10K 0.4327, and pseudobulk CPM 43.6960. This supports a possible self-transcript call but does not establish a large downstream response.
- Slc17a5's closest direct in-assay biology was not a broad stress class. The strongest prior modules were sialic-acid metabolism, SLC17/organic-anion transport, vesicular loading, and broader lysosomal annotations.

## Training endpoint measurements

The focal training count table contained 1,674 perturbations. The overall count distribution was heavily zero-inflated:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- zero-DEG rows: 1,205 / 1,674 = 71.98%
- rows with at most one DEG: 1,481 / 1,674 = 88.47%

Curated Slc17a5-related training groups were quieter than the full background:

- Reactome `R-MMU-4085001`, sialic acid metabolism: only `St3gal5` was present in the training count table, and it had `n_degs=1`.
- GO `GO:0098700`, neurotransmitter loading into synaptic vesicle: only `Slc32a1` was present, and it had `n_degs=0`.
- KEGG `mmu04142`, lysosome, after excluding unavailable targets and `Slc17a5`: 18 training targets had median 0 and mean 0.5. The focal counts were `0` for `Ap1s2`, `Ap3b1`, `Ap4s1`, `Asah1`, `Gnptab`, `Gnptg`, `Lamp2`, `Litaf`, `Manba`, `Sort1`, and `Tbx1`; `1` for `Ap1b1`, `Atp6v0a1`, `Ctsb`, `Gaa`, `Ppt1`, and `Scarb2`; and `3` for `Cltc`.
- GO `GO:0005765`, lysosomal membrane, contributed 46 available training targets with median 0. Its mean was 14.696 only because the broad trafficking and mTOR outliers `Rab7=501`, `Tsc2=86`, and `Prox1=50` were included; the hydrolase, M6P, V-ATPase, and storage-disease-like genes in the same set were mostly 0 or 1 in this focal class.

The selected same-experiment Findings and Claims are interpreted only as the semantic layer over the same Perturb-seq dataset, not as independent replication. They sharpened which high-DE analogs should not be transferred to Slc17a5:

- A high-confidence Claim over `Gnptab`, `Manba`, `Ppt1`, `Psap`, `Sort1`, and `Tmem106b` states that represented lysosomal disease-related perturbations did not elicit a shared neuronal lysosomal-stress, storage-stress, autophagy, TFEB/MiT, or ISR/UPR nuclear RNA program in this assay.
- `Gaa`, `Ppt1`, `Gnptab`, `Gnptg`, `Manba`, `Psap`, `Sort1`, `Scarb2`, and `Tmem106b` Findings each describe pan-neuronal or nearly pan-neuronal downstream buffering rather than a common storage-stress transcriptome.
- V-ATPase Findings for `Atp6v0a1`, `Atp6v1a`, `Atp6v1e1`, and `Atp6v1b2` describe flat, sparse, divergent, or subunit-specific responses rather than a shared lysosomal-collapse signature.
- `Rab7` had a large focal count and an endolysosomal/sterol compensation program, but packaged Findings explicitly place it apart from HOPS, retromer, V-ATPase, lysosomal hydrolase, and lysosomal disease comparators.

## Parquet profile check

I compared 36 available lysosomal, vesicular, V-ATPase, hydrolase, NCL, M6P, endosomal trafficking, and mTOR/autophagy training profiles from the declared Parquet in the exact focal cell group.

- All 36 profiles were present.
- Activity classes were sparse: 15/36 had zero significant focal features, 17/36 had 1-9, 2/36 had 10-49, and only 2/36 had at least 50.
- Across all 630 within-cohort signed profile pairs, the median positive top-200 tail overlap coefficient was 0.025 and the median negative top-200 tail overlap coefficient was 0.030.
- `St3gal5`, `Atp6v0a1`, `Gaa`, and `Ppt1` each had exactly one significant focal feature in the inspected profile table, and the feature was the perturbed transcript itself.
- `Rab7` had 501 focal significant features and was nearest to `Tsc2` and then `Vps35` among the biologically selected peers; those large trafficking-state profiles did not pull the hydrolase or direct Slc17a5-like candidates into a coherent significant program.

## Synthesis

The Slc17a5 perturbation is likely realized enough by harvest to reduce newly supplied lysosomal or vesicular sialin, and focal baseline expression is high enough that a self-transcript DEG is plausible. The closest measured lysosomal disease, hydrolase/cargo, M6P, V-ATPase, transporter, and sialic-acid/ganglioside perturbations argue against a detectable shared downstream storage-stress program in this acute sparse neuronal assay. I therefore forecast a single FDR-significant gene, most likely the self transcript, and no confident downstream DEG in `151 TH Prkcd Grin2c Glut`.
