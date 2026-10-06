# Nalcn direct DEG-count forecast

## Target and context

- Target: `Nalcn` from the one-row declared manifest.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, defined as measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared focal expression card put `Nalcn` squarely in the assayed population: 19,324 of 23,679 non-target nuclei expressed `Nalcn` in this class, 81.61% expression reach, mean raw UMI 2.12, mean CP10k 1.316.
- The biology card supports functional realization: NALCN itself supplies a voltage-independent sodium/cation leak conductance, no close paralogous replacement was identified, and postnatal neural knockdown in another glutamatergic population produced target/function changes within an 8-21 day interval. I therefore treated a P16 disruptive edit as likely to deplete channel supply by the P37-P44 harvest window, but the link to a large survivor snRNA-seq program remained uncertain.

## Same-endpoint training evidence

The direct-count table for the declared 151 class is sparse: among 1,674 training targets the median count is 0, the 75th percentile is 1, the 90th percentile is 2, and only 106 targets reached 10 or more DE genes. Strong biology therefore cannot be translated directly into a broad FDR response.

The closest exact NALCN-channel subunits or required partners named by the biology card, `Unc79`, `Unc80`, and `Fam155a`, were not present in the 151 training-count table, so I used measured excitability and ion-channel losses as scale anchors rather than as direct complex analogues.

Observed `n_degs` values from the declared count table for the 151 class:

| Perturbation | Rationale | `n_degs` |
|---|---:|---:|
| `Hcn1`, `Hcn2` | subthreshold cation conductance channels | 0, 1 |
| `Scn1a`, `Scn1b`, `Scn2a`, `Scn3a`, `Scn8a`, `Fgf12`, `Fgf13` | Nav pore/beta/FHF excitability axis | 1, 2, 1, 0, 1, 0, 2 |
| `Kcnq1`, `Kcnq2`, `Kcnq3`, `Kcnb1`, `Kcnb2`, `Kcnj6` | Kv/KCNQ/GIRK membrane-excitability comparators | 0, 1, 1, 0, 0, 0 |
| `Cacna1a`, `Cacna1d`, `Cacna1e`, `Cacnb2`, `Cacnb4` | represented CaV relatives other than Cav3.1 | 0, 0, 0, 0, 1 |
| `Cacna1g` | T-type calcium pore with a thalamic 151 response | 12 |
| `Grin1` | obligatory NMDAR subunit; positive synaptic upper comparator | 89 |
| `Atp1a3` | Na/K ATPase alpha subunit; positive ionic upper comparator | 80 |

The selected focal Parquet rows confirmed the sign and composition of that count table. The one-gene cases were usually the perturbed transcript itself: `Hcn2`, `Kcnq2`, `Kcnq3`, `Scn1a`, `Scn2a`, and `Scn8a` each had only the self gene significant at `pvals_adj < 0.05` in the 151 group. `Scn1b` had two significant rows, self plus `Jun`. By contrast, `Cacna1g` had 12 significant rows, `Atp1a3` had 80, and `Grin1` had 89.

The same-experiment corpus put the low counts in context rather than treating them as failed evidence: represented Nav, HCN, KCNQ, and CaV-family losses were reported as sparse, target-specific, or buffered at the steady nuclear RNA level despite expected electrophysiological importance, while `Cacna1g` was the selective thalamic CaV exception. Bounded profile comparison of 29 Nav/HCN/KCNQ/GABAB/cAMP/CaV/Atp1a3/Grin1 targets in the exact 151 class also showed no FDR-level overlap between `Cacna1g` or `Kcnq2` and the Nav/HCN/Kv/CaV comparators in the inspected pairs, so there was no coherent broad channel module to project onto `Nalcn`.

## Forecast

`Nalcn` is highly expressed and likely functionally depleted, so I did not use the zero median of all genes as the point. Its operation is nevertheless a standing leak conductance, closer to HCN/Nav/KCNQ channel perturbations that generally showed self-only or null nuclear responses than to the much broader `Atp1a3` ion-pump and `Grin1` synaptic receptor states. `Cacna1g` keeps the upper tail real for thalamic conductance genes, but NALCN lacks the Cav3.1-specific low-threshold calcium/bursting evidence that made `Cacna1g` an exception among calcium channels.

I therefore forecast a self-transcript-dominated sparse response with essentially no downstream FDR program: predicted `n_degs = 1`.
