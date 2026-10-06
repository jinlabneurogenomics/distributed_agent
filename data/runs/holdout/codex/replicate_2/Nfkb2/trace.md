# Nfkb2 direct DEG-count forecast

## Target and endpoint

- Target: `Nfkb2`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: count of measured genes with Wilcoxon BH-adjusted `p < 0.05` in the same cell class.
- Output point: `0`

## Evidence used

### Declared Nfkb2 biology bundle

The biology bundle was outcome-blind (`serving.target_outcome_exposed=false`, `serving.labeled_neighbors_exposed=false`) and had exact expression reach for the requested focal population.

Its functional-stock card says an effective edit should stop new production of both NFKB2 products, p100 and p52, and that functional stock is `likely_substantially_depleted` by P37-P44 after a P16 edit. That makes the perturbation biologically plausible rather than a presumed null.

The same bundle also made the neural endpoint uncertain:

- established phenotype evidence is mostly immune/non-neural;
- p100 turnover evidence is from cultured mouse-cell systems rather than thalamic neurons;
- Nfkb1 compensation is documented in selected osteoclast and B-cell settings, not postmitotic thalamus;
- exact in-assay reach is extremely low in `151 TH Prkcd Grin2c Glut`: `301 / 23679` non-target nuclei expressed `Nfkb2`, or `1.271%`, with pseudobulk CPM `0.8629` and mean raw UMI `0.01377`.

I therefore treated Nfkb2 loss as molecularly possible but likely diluted in the recovered thalamic aggregate.

### Same-experiment corpus

`corpus.target_context(Nfkb2)` and a Findings-ledger query returned no Nfkb2 Findings, Claims, or explicit comparator references in the selected July corpus. There was no target-local same-experiment report to transfer from.

### Background training counts

The declared same-cell training table contains `1674` perturbations. It is highly zero-inflated in this focal class:

- `1205 / 1674` have `n_degs = 0`;
- median `n_degs = 0`;
- `469 / 1674` are nonzero;
- only `106 / 1674` reach `10` or more DEGs.

That background makes a 0-DEG forecast ordinary unless Nfkb2 has a close, endpoint-active analog.

### Typed Nfkb2 analogs in the training universe

I ran the deterministic gene-analog nominator against the exact 1,674-gene training universe. It reported `Nfkb2` itself as absent from the training universe and produced 36 non-fallback measured nominees:

- `8` best in `exact_complex_or_paralog`
- `28` best in `narrow_module`

The closest NF-kappaB actors were quiet in the count table:

| analog | typed relation to Nfkb2 | observed n_degs |
|---|---|---:|
| `Nfkb1` | exact complex/paralog; shared CORUM-projected NF-kappaB complexes; STRING physical link | 0 |
| `Chuk` | exact complex; shared TNF/NF-kappaB complexes and narrow modules | 0 |
| `Rel` | exact complex; shared NF-kappaB complexes; STRING physical link | 0 |

The leading narrow NF-kappaB/TLR signaling nominees were also mostly quiet. The top 14 non-fallback nominees were:

`Nfkb1=0`, `Irf3=0`, `Chuk=0`, `App=1`, `Ager=0`, `Map3k7=0`, `Tlr4=0`, `Rel=0`, `Tlr2=0`, `Traf3=0`, `Ep300=0`, `Tlr3=0`, `Hsp90ab1=1`, `Mapk1=0`.

That set has 12 zeros, median 0, and a log1p-mean back-transform of 0.104 DEGs.

### Profile and topology check on outliers

I compared all 36 non-fallback nominees in `151 TH Prkcd Grin2c Glut` using the declared Parquet, with `gene_target` as the entity, `names` as features, `logfoldchanges` as signed values, and `pvals_adj < 0.05` as significance.

All 36 requested analog profiles were present. The observed response categories were:

- 23 with no significant features;
- 8 with 1-9 significant features;
- 1 with 10-49 significant features;
- 4 with at least 50 significant features.

The active high-count rows inside the 36-gene non-fallback set were `Psmb4=742`, `Psmc1=430`, `Ctnnb1=383`, and `Setd1a=368`. I did not use them as equal-scale Nfkb2 donors because their operations are proteasome or chromatin/Wnt module perturbations rather than loss of an NF-kappaB2 p100/p52 transcription-factor precursor. Profile inspection also showed no significant-program overlap between quiet close NF-kappaB analogs and the high proteasome rows: for example `Nfkb1`, `Chuk`, and `Rel` each had zero significant features, whereas `Psmb4` had 742 and `Psmc1` had 430.

The report-derived topology audit of the first 20 specific nominees separated interpretation in the same way. The NF-kappaB/TLR/MAPK component contained the close nodes with 0-1 DEG outcomes, while `Psmb4` and `Psmc1` formed a smaller proteasome/stress neighborhood.

## Forecast synthesis

The card supports realized depletion of new NFKB2 p100/p52 supply, so I did not forecast a technical no-op. The endpoint-relevant evidence pushes the count to the bottom of the distribution anyway:

- the exact target transcript is detected in only `1.271%` of focal non-target nuclei;
- available phenotypic support is not postnatal or thalamic;
- the closest measured NF-kappaB analogs in the same cell class are all zero;
- the top narrow NF-kappaB/TLR analog cohort has median 0 and only two single-DEG rows;
- high-response nominees are broader stress/chromatin or proteasome states rather than direct p100/p52 analogs.

My point estimate is therefore the modal and biologically best-supported value:

`Nfkb2	0`
