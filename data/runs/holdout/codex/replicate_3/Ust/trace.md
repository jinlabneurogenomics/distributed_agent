# Direct held-out DEG-count prediction for `Ust`

## Target and endpoint

- The one-row holdout manifest names `Ust`.
- The requested endpoint is `n_degs` in `151 TH Prkcd Grin2c Glut`: the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- `Ust` is absent from the declared focal count table, which contains 1,674 training perturbations.

## Biology prior from the declared bundle

The supplied `Ust` bundle supports an intervention that should eventually reduce the active biochemical product, but not one that is expected to create an acute, whole-population nuclear RNA response in every assayed thalamic nucleus.

- Ust installs a covalent 2-O-sulfate state on chondroitin/dermatan glycosaminoglycan chains in the Golgi.
- A disruptive P16 edit should stop new Ust production, but it does not erase pre-existing sulfated carriers; the functional-stock card judged renewable stock `likely_substantially_depleted` by the P37-P44 harvest, with partial evidence because Ust protein decay and juvenile thalamic carrier kinetics are not directly measured.
- The exact focal expression measurement is low and sparse: Ust is detected in 3,922 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei, or 16.56%, with mean raw UMI 0.223 and mean log1p CP10K 0.0975.
- The observability card gives only low-confidence postnatal neural support and keeps loss latency unresolved for a 21-28 day postmitotic thalamic perturbation.

I therefore treated Ust as biologically reachable but diluted by focal-population reach and by persistence of pre-edit extracellular glycosaminoglycan material.

## Training perturbations used

I nominated available analogs from the actual 1,674-gene training universe rather than from symbol spelling. The strongest Ust-proximal candidates were extracellular-carbohydrate and glycosaminoglycan perturbations:

| training perturbation | typed relation to Ust | `151 TH Prkcd Grin2c Glut` `n_degs` |
| --- | --- | ---: |
| `Cspg4` | Reactome DS-GAG / CS-GAG / chondroitin sulfate-dermatan sulfate module | 0 |
| `B3gat3` | KEGG chondroitin sulfate / dermatan sulfate GAG biosynthesis | 0 |
| `Xylt1` | KEGG chondroitin sulfate / dermatan sulfate GAG biosynthesis | 0 |
| `Hs6st2` | sulfotransferase activity and broader glycosaminoglycan metabolism | 0 |
| `Ext1` | broader glycosaminoglycan polymerization/metabolism | 0 |
| `Ext2` | broader glycosaminoglycan polymerization/metabolism | 0 |
| `Glce` | broader glycosaminoglycan modification/metabolism | 0 |
| `Gpc6` | proteoglycan/GAG reference | 0 |

Those count-table zeros were checked against the declared Parquet through a focal-class profile comparison. For the inspected GAG nodes, each available focal profile had 17,259 measured features and zero BH < 0.05 positive or negative features, matching the count endpoint. Corpus topology over the same eight nodes showed that `B3gat3`, `Ext1`, `Ext2`, `Glce`, `Gpc6`, `Hs6st2`, and `Xylt1` form a densely connected explicit-Finding component in the same-experiment report layer, while `Cspg4` is a typed annotation analog without internal report edges to the heparan/proteoglycan cluster.

I considered broad fallbacks from the nominator such as `Gsk3b`, `Cdc42`, and `Epha4`, but used them only as scale checks. Their observed focal counts were 6, 1, and 1 respectively, which shows that the class can register small nonzero responses, but their kinase/Rho/Eph signaling operations are too far from Ust-dependent CS/DS 2-O-sulfation to transfer quantitatively.

For context, the whole focal training table is sparse: 1,205 of 1,674 training targets have `n_degs = 0`; 276 have exactly one DEG; 87 have 2-9; 63 have 10-99; and 43 have at least 100. The eight closest retained GAG/CS-DS references all fall in the zero bin despite this being one of the dataset's highest-yield cell classes.

## Forecast

The biology bundle prevents treating Ust as a failed or irrelevant perturbation: loss of new Ust-dependent 2-O-sulfation should be at least partly realized by harvest. The decisive quantitative evidence, however, is that same-endpoint perturbations of the nearest training-available glycosaminoglycan and proteoglycan machinery all have no FDR-significant survivor transcriptome in `151 TH Prkcd Grin2c Glut`. Ust is also expressed in only about one sixth of focal non-target nuclei, and the durable extracellular product should further blur the recovered snRNA-seq contrast. With no exact Ust profile available and no close positive CS/DS-GAG analog to justify lifting the point above the local zero cohort, I predict the held-out focal DEG count as:

`predicted_n_degs = 0`
