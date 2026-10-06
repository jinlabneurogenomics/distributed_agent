# Lyst direct DEG-count forecast

Target: `Lyst`
Focal population: `151 TH Prkcd Grin2c Glut`
Predicted `n_degs`: `1`

## Biology used

- The declared manifest target is `Lyst`.
- The exact in-assay focal-population expression bundle reports detectable `Lyst` in `151 TH Prkcd Grin2c Glut`: 13,941 of 23,679 non-target cells expressing, 58.875% expressing, mean log1p CP10K 0.404, mean raw UMI 0.993, and pseudobulk CPM 62.26. That supports target reach in the class but does not score guide editing or downstream response size.
- The canonical biology card places LYST at lysosome fission and autophagic lysosome reformation. `Lyst` is a recruited, dynamic regulator with continuing renewal demand, so a P16 disruptive edit could matter during the P37-P44 window.
- The same card leaves functional stock at harvest indeterminate. Existing LYST protein is not directly disabled by the DNA edit; no neuronal LYST half-life was found; and the transferable mouse neural timing evidence is weak because germline phenotypes arise over months and are mainly cerebellar or peripheral rather than an acute thalamic neuron assay.
- `Nbea` is only a BEACH-domain relative in the card. No same-context compensation or lack-of-compensation experiment is supplied, and the 151 training count for `Nbea` is 0.

## Training measurements used

- The declared 151-class count table has 1,674 training perturbations. Its `n_degs` distribution is highly zero-inflated: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, mean 14.05, and only 59 targets reach at least 50 DEGs.
- Exact counts from the table for lysosome/autophagy/endolysosomal references were:
  - Broad Rab7-like exception: `Rab7` 501.
  - Restricted trafficking positives: `Vps54` 31, `Vps35` 17.
  - mTOR/sterol reference: `Tsc2` 86.
  - Near-null or null lysosome/autophagy/storage/Rab-cycle references: `Atp6ap2` 2, `Atp6v0a1` 1, `Ctsb` 1, `Gdi1` 1, `Ppt1` 1, `Psap` 1, `Sqstm1` 1, `Lamp2` 0, `Atg5` 0, `Atg16l1` 0, `Atp6v1a` 0, `Atp6v1b2` 0, `Atp6v1e1` 0, `Becn1` 0, `Gnptab` 0, `Manba` 0, `Ocrl` 0, `Vps41` 0, `Vps53` 0.
- In the exact 151 Parquet slice, the 1-count references above were dominated by the perturbed self transcript:
  - `Atp6v0a1`, `Ctsb`, `Gdi1`, `Ppt1`, `Psap`, and `Sqstm1` each had one BH<0.05 feature, their own transcript.
  - `Atp6ap2` had two hits, `Atp6ap2` and `Atp6v0a1`.
  - `Lamp2`, `Atg5`, `Abca7`, `Nbea`, and `Vps41` had no BH<0.05 feature in the focal class.
- The same-experiment corpus reports that `Rab7` perturbation induces a real late-endosomal/lysosomal, V-ATPase, sterol, ISR/autophagy/proteostasis response in 151 and 155, but the corresponding pathway relatives mostly fail to phenocopy it at FDR scale. It specifically records flat or near-flat acute juvenile neuronal surfaces for `Lamp2`, `Atp6v0a1`, `Atp6ap2`, `Ctsb`, `Ppt1`, `Psap`, `Atg5`, `Abca7`, `Atp13a2`, `Gdi1`, and related represented lysosomal/storage perturbations.
- A matched `151 TH Prkcd Grin2c Glut` profile comparison over 15 hand-selected endolysosomal/autophagy/BEACH candidates confirmed low signature interchangeability:
  - Across 105 candidate pairs, median positive-tail and negative-tail overlap coefficients were 0.05 and 0.06.
  - `Rab7` had only weak to modest whole-profile similarity to the nearest selected trafficking positives: cosine 0.143 with `Vps35`, 0.177 with `Vps54`, 0.321 with `Vps41`.
  - `Vps41` showed the closest continuous `Rab7` direction among the selected genes but still had 0 BH<0.05 genes in the 151 count table, which argues against projecting the 501-gene `Rab7` burden onto every late-lysosome component.
  - `Vps35` and `Vps54` were not mutually similar in this focal population despite both being trafficking positives: cosine 0.030.

## Synthesis

`Lyst` has adequate focal expression and a plausible recurring lysosome-remodeling operation, so I do not treat it as hematopoietic/off-axis. The limiting evidence is that represented postnatal neuronal perturbations in nearby lysosome, autophagy, V-ATPase, storage, NCL, Rab-cycle, and BEACH-family biology usually sit exactly at the BH<0.05 floor under this sparse P16-to-P37/P44 snRNA-seq design. The few visible trafficking genes in 151 are narrow (`Vps35`, `Vps54`) or a much stronger Rab7-like late-endosomal stress state, and the measured profile geometry shows they are not an interchangeable lysosomal module.

Because LYST stock by harvest is unresolved and germline `Lyst` neural disease is late, I discounted a high Rab7-scale endpoint. Because `Lyst` is expressed in over half of focal non-target cells and is used in ongoing lysosome/autolysosome fission, I kept the point slightly above a confident zero. The resulting biology-weighted point is the one-gene floor, `n_degs = 1`.

The target `Lyst` perturbation signature and target DEG count were not present in the declared count table or Parquet input and were not used.
