# Reasoning trace

## Question and resolved ambiguities

The manifest for this run contains one held-out perturbation:

| target_name |
|---|
| Dync1h1 |

The requested value is the `151 TH Prkcd Grin2c Glut` endpoint only: the number of measured genes with `pvals_adj < 0.05` after acute AAV-CRISPR loss of the target in the postnatal mouse neuronal Perturb-seq assay. I treated the task as a point prediction of this assay-specific FDR count, not as a prediction of biological severity, viability, target knockdown, or the number of genes expected to move in a germline or conditional knockout.

The exact `Dync1h1` signature is absent from both supplied inputs and the Distributed Agents same-experiment corpus had no Dync1h1-scoped claims or findings, so the prediction is a transfer from non-held-out genes.

## Sources used

- Held-out manifest: `[local file: 063_Dync1h1.csv]`.
- Training endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, especially the Dctn1 findings `Dctn1:F001`, `Dctn1:F003`, `Dctn1:F008`, and `Dctn1:F009`.
- PubMed literature:
  - Reck-Peterson, Redwine, Vale & Carter 2018, `10.1038/s41580-018-0004-3`, PMID 29662141: dynein-1 plus dynactin and cargo adaptors as the canonical minus-end-directed cytoplasmic transport machine.
  - Urnavicius et al. 2015, `10.1126/science.aaa4080`, PMID 25814576: structural basis for a dynein-dynactin-adaptor complex.
  - Maday, Twelvetrees, Moughamian & Holzbaur 2014, `10.1016/j.neuron.2014.10.019`, PMID 25374356: axonal transport and retrograde organelle/autophagosome transport requirements in neurons.
  - Caviston et al. 2007, `10.1073/pnas.0610628104`, PMID 17548833: HTT facilitates dynein/dynactin-mediated vesicle movement with HAP1.
  - Jordens et al. 2001, `10.1016/S0960-9822(01)00531-0`, PMID 11696325: Rab7/RILP recruits dynein-dynactin motors to late endosomes and lysosomes.

## Dataset computations

1. I read the one-row held-out manifest and verified that `Dync1h1` is absent from the 1,674-gene training count CSV.
2. I computed the focal training-count distribution from the CSV:
   - 1,205 of 1,674 perturbations had 0 DEGs.
   - 363 had 1-9 DEGs.
   - 63 had 10-99 DEGs.
   - 43 had at least 100 DEGs.
   This makes the endpoint heavily zero-inflated; a medium positive call needs a specific analog.
3. I scanned the training target list for dynein/dynactin, motors, microtubule tracks, and endolysosomal transport candidates. Most direct dynein-1 regulators were not represented; the important represented analog was `Dctn1`.
4. I read only rows matching `group_name == "151 TH Prkcd Grin2c Glut"` and selected candidate `gene_target`s from the parquet. For each candidate I recomputed `sum(pvals_adj < 0.05)` and checked that it matched the count CSV.
5. For the `Dctn1` module comparators named by the Distributed Agents corpus, I counted positive and negative FDR genes and their signed overlap with `Dctn1` in the focal cell group. I used these FDR-level overlaps more than all-gene Pearson correlations, because the full vectors include many non-significant, tied, high-magnitude log-fold changes from extremely sparse features.

The key observed focal-cell counts were:

| training target | n_degs | up / down FDR genes | Dctn1 same / opposite FDR overlap | interpretation |
|---|---:|---:|---:|---|
| `Dctn1` | 75 | 49 / 26 | self | direct dynactin p150/Glued cofactor for cytoplasmic dynein-1 |
| `Rab7` | 501 | 311 / 190 | 39 / 4 | late-endosome/lysosome node with a much broader sterol/endolysosomal response |
| `Tsc2` | 86 | 58 / 28 | 13 / 0 | lysosomal mTORC1/sterol-adjacent convergence, not a motor complex member |
| `Mib1` | 27 | 26 / 1 | 21 / 0 | strong overlap on sterol genes, but weaker total focal response |
| `Marchf6` | 14 | 13 / 1 | 12 / 0 | sterol feedback comparator downstream of the SREBF2 branch |
| `Srebf2` | 7 | 0 / 7 | 0 / 7 | inverse control: the genes induced by `Dctn1` include SREBF2 targets |
| `Htt` | 3 | 2 / 1 | 2 / 0 | HTT dynein/dynactin vesicle partner, but very sparse in this focal group |
| `Vps35` | 17 | 8 / 9 | 6 / 0 | retromer perturbation, modest and only partially overlapping |
| `Vps54` | 31 | 6 / 25 | 3 / 3 | GARP/EARP branch, modest and mixed relative to `Dctn1` |
| `Vps41` | 0 | 0 / 0 | 0 / 0 | HOPS/late-endosome counterexample |
| `Dync2h1`, `Dync2i1`, `Dnal1` | 0 each | 0 / 0 | not material | ciliary/axonemal dynein counterexamples, not cytoplasmic dynein-1 |
| `Kif1a`, `Kif5a`, `Kif5c`, `Kifbp` | 1, 1, 1, 2 | mostly down singletons | essentially none | kinesin / kinesin-associated counterexamples |
| `Hmgcr`, `Srebf1`, `Amfr` | 0, 0, 1 | no sterol-module phenocopy | none | lipid/SREBF-adjacent counterexamples |

The top `Dctn1` DEGs in `151 TH Prkcd Grin2c Glut` were an induced sterol/lipid cassette: `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`, `Sqle`, `Dhcr24`, `Ldlr`, and `Fdps`. The Distributed Agents Dctn1 report captured the same pattern across responding neuronal groups: `Dctn1:F001` called a recurrent up-regulated SREBF2-like cholesterol biosynthesis and uptake module; `Dctn1:F003` noted only a limited lysosome/autophagy/proteostasis echo despite canonical dynein/dynactin roles in axonal organelle transport; `Dctn1:F008` linked the Dctn1 signature to partial convergence with `Htt`, `Marchf6`, `Rab7`, and `Tsc2`; and `Dctn1:F009` treated canonical kinesins and several lipid-pathway genes as explicit non-phenocopies.

## Target-specific prediction

### Dync1h1

`Dync1h1` encodes the heavy chain of cytoplasmic dynein-1, the ATPase motor subunit of the minus-end-directed microtubule motor. Dynactin is the obligatory activating cofactor for long-distance processive dynein transport, with cargo adaptors stabilizing a dynein-dynactin-adaptor complex; that made the measured `Dctn1` perturbation the most direct training analog rather than a superficial family match.

I made a nonzero call because the closest measurable component, `Dctn1`, was not silent: it produced 75 focal DEGs, including 49 induced and 26 repressed genes. The Dctn1 response was also internally coherent, not just a single target-RNA hit: 21 of its focal FDR genes were shared in the same direction with `Mib1`, 39 with the broader `Rab7` response, and 12 with the narrow sterol regulator `Marchf6`; `Srebf2` loss repressed seven of the same sterol genes that `Dctn1` induced. This puts the Dctn1 state on a recurrent vesicle/endolysosome/sterol-feedback axis in the dataset.

I did not use the very large `Rab7` count of 501 as the scale for `Dync1h1`. Rab7 is a late-endosome/lysosome GTPase that can recruit dynein-dynactin motors, but its perturbation produced a much broader endolysosomal program than Dctn1. Conversely, I did not collapse Dync1h1 to the kinesin or microtubule-track baseline: `Kif1a`, `Kif5a`, `Kif5c`, `Kifbp`, `Tuba1a`, `Mapt`, and `Map1b` were all 1-7 DEGs, but the same-experiment Dctn1 findings explicitly showed that canonical kinesins failed to phenocopy dynactin even though acute Dctn1 loss generated a detectable sterol/lipid module. `Dync2h1` and `Dync2i1` were zero-DEG controls for ciliary dynein-2, not close substitutes for the cytoplasmic dynein-1 heavy chain.

I therefore predicted that partial Dync1h1 loss would land in the same medium focal-count class as Dctn1 and Tsc2, close to Dctn1 itself and far below Rab7. I nudged the count slightly above Dctn1 because Dync1h1 is the nonredundant dynein-1 motor subunit rather than an accessory cargo-coupling subunit, but I kept it below 100 because the direct Dctn1 branch was 75 DEGs, the represented dynein-linked HTT branch was only 3 in this focal group, and most endosomal or motor counterexamples were weak.

Prediction: **80 DEGs**.

## Limits

This is an extrapolation from `Dctn1`; the training set did not contain `Dync1i1`, `Dync1i2`, `Dync1li1`, `Dync1li2`, `Pafah1b1/Lis1`, `Nde1`, `Ndel1`, `Bicd1`, `Bicd2`, `Hook1`, or `Hook3`, so the nearest cytoplasmic dynein-1 subcomplex series could not be tested. The Dctn1 comparison is mechanistically close but imperfect: dynactin couples and activates dynein on cargo, whereas Dync1h1 is the motor heavy chain itself and could have different protein stability, guide editing, survivor bias, and cargo selectivity in the 3-4 week mosaic assay. The dataset also measures nuclear RNA only; local axonal transport, autophagosome motility, sterol abundance, and SREBP2 processing were not directly measured. Finally, the final integer should be read as a calibrated point estimate under squared log1p error, not as evidence that exactly 80 genes will cross FDR in every replicate.
