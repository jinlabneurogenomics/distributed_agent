# Tbck 151 TH Prkcd Grin2c Glut n_degs forecast

## Endpoint

Predicted endpoint: `n_degs` for `Tbck` in `151 TH Prkcd Grin2c Glut`, defined as the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

The target outcome and target perturbation signature were not used. Evidence came from the declared `Tbck` biology bundle, the declared held-in 151 TH count table, same-experiment Findings for measured comparator perturbations, and a run-local profile comparison of selected held-in endosome/lysosome/autophagy/mTOR profiles in the exact 151 TH context.

## Target biology

The canonical `Tbck` bundle places TBCK in two related RAB5/early-endosome assemblies:

- the TBCK-PPP1R21-C12orf4 RAB5-GAP complex, where TBCK is the catalytic GAP subunit restraining RAB5 activity and supporting early-to-late endosome progression, lysosomal enzyme delivery, and autophagic flux;
- the pentameric FERRY Rab5 effector complex, linking mRNA to early endosomes.

The exact in-assay non-target expression card shows `Tbck` is measurable but not ubiquitous in the target population: 10,831 of 23,679 non-target 151 TH nuclei expressed the feature, or 45.74%, with mean log1p-CP10K 0.282.

The same bundle argues against treating developmental or human phenotypes as a quantitative match for the P16-to-P37/P44 Perturb-seq endpoint. Disruptive editing should stop new intact TBCK production, but pre-existing TBCK-containing GAP/FERRY complexes may remain active until protein clearance or complex exchange; no target-specific protein half-life, FERRY residence time, or acute neuronal clearance curve was found. Thus TBCK loss is biologically plausible in postmitotic thalamic neurons, but the realized perturbation strength after 21-28 days is uncertain.

## Held-in 151 TH outcomes used as scale references

The declared training table contains 1,674 151 TH targets. Its empirical baseline is very sparse:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- 43/1,674 targets had at least 100 DEGs

Measured vesicle/endosome/autophagy/mTOR-related scale points at the task's BH<0.05 cutoff were:

| target | 151 TH n_degs | interpretation |
| --- | ---: | --- |
| `Rab7` | 501 | direct late-endosome/lysosome hub; broad lysosomal, sterol, proteasome, and synaptic remodeling response |
| `Tsc2` | 86 | strong mTORC1/sterol/lysosomal downstream state, same direction as part of `Rab7`, but not an endosomal sorting analog |
| `Vps54` | 31 | GARP perturbation with a 151 TH-restricted neuronal downshift, not a canonical lysosomal rescue program |
| `Vps35` | 17 | retromer perturbation with a modest 151 TH membrane/synaptic signature, not a bulk lysosomal response |
| `Tbcd` | 12 | non-endosomal essential-complex reference with a small 151 TH stress/adaptation signature |
| `Mtor` | 2 | direct mTOR kinase loss with only a tiny RNA response in this group |
| `Atp6v0a1` | 1 | V-ATPase a1; essentially flat in 151 TH |
| `Atp6v1a` | 0 | V-ATPase A subunit; flat in 151 TH |
| `Tbc1d23` | 0 | TBC-domain trafficking gene; flat in 151 TH |
| `Vps41` | 0 | HOPS/RAB7-axis gene; flat at FDR<0.05 in 151 TH |
| `Vps35l` | 0 | Retriever/Commander analog of Vps35 branch; flat |
| `Vps53` | 0 | GARP component; flat |
| `Washc4` | 0 | WASH-related recycling component; flat |
| `Atg5`, `Atg16l1`, `Becn1` | 0 | autophagy-adjacent perturbations; flat |
| `Ap3b1`, `Ankfy1`, `Appl1`, `Abca7`, `Ocrl` | 0 | adjacent endosomal or trafficking perturbations; flat |

## Same-experiment report and profile checks

The same-experiment Findings supported `Rab7` as the high positive boundary: `Rab7` loss recurrently induced a late-endosomal/lysosomal compensation module with V-ATPase, `Lamp2`, and hydrolase genes, plus sterol/lipid and proteostasis branches. Its 501 DEGs in 151 TH are therefore a visible severe late-endosomal stress state, not a generic property of every endosomal perturbation.

The comparator reports also supplied the important lower boundaries:

- `Vps35` produced only a sharply restricted 151 TH retromer response, with receptor, excitability, calcium, and synaptic-neurite genes rather than broad lysosomal compensation.
- `Vps54` produced a 151 TH-restricted GARP response biased toward loss of mature neuronal signaling/secretory/axon transcripts and explicitly lacked UPR/ISR, proteasome, lysosomal hydrolase, and sphingolipid programs expected from a severe GARP collapse.
- `Atp6v1a` was sparse across recovered neurons and flat in 151 TH, and same-pump V-ATPase membership was not enough to produce a shared snRNA-seq response.
- `Tbc1d23`, `Ap3b1`, `Ankfy1`, and `Appl1` show that nearby endosomal, TBC-domain, AP-3, and RAB5-adaptor annotations can be fully buffered in this assay.

The 151 TH profile comparison recapitulated this separation. `Rab7` was broad and partially aligned with `Tsc2` and `Vps41` on continuous score vectors, but `Vps41` still had zero FDR<0.05 genes. `Vps35` and `Vps54` were much smaller active profiles, and the TBC/V-ATPase/AP/autophagy nulls had near-zero pairwise cosine or no shared FDR features. The offline analogue pass found no training-available same-complex, narrow-module, direct-interaction, or reciprocal-corpus comparator for `Tbck`, only broad annotation fallbacks.

## Forecast synthesis

`Tbck` should not be assigned the empirical median of 0: it is expressed in nearly half of non-target 151 TH nuclei, has no established close compensating paralog, and occupies ongoing RAB5 early-endosome complexes whose loss can plausibly create an endolysosomal transcriptional response within 3-4 weeks.

I also do not transfer the `Rab7` or `Tsc2` magnitudes. `Tbck` is not measured as loss of RAB7 itself or as mTORC1 activation, its exact FERRY/GAP partners are absent from training, and the biology card leaves TBCK protein/complex depletion unresolved. The relevant measured boundary is the modest endomembrane-trafficking band: `Vps35` at 17 and `Vps54` at 31, counterbalanced by fully flat TBC, AP-3, V-ATPase, HOPS, autophagy, RAB5-adaptor, and retromer-adjacent perturbations.

My point forecast is therefore a low but nonzero response, slightly below the 151 TH `Vps35` branch because TBCK's realized stock loss is less certain and the held-in adjacent endosomal targets are mostly zero.

Predicted `n_degs`: **12**
