# DEG-count prediction trace

## Question and resolved ambiguities

The held-out target list for this run contains one gene:

```text
Minpp1
```

I interpreted `n_degs` exactly as the endpoint in the focal training-count file: the number of measured `names` rows with `pvals_adj < 0.05` for the target in `151 TH Prkcd Grin2c Glut`, counting the perturbed gene itself if it was assayed and significant. I made a point prediction for the acute P16 mosaic AAV-CRISPR loss-of-function assay, not for germline, developmental, conditional, RNAi, or drug perturbations.

## Sources used

Internal experimental data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest: `[local file: 137_Minpp1.csv]`

Internal corpus:

- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`. I queried `Minpp1` directly, then pathway-centered contexts and claims for `Inpp5k`, `Ocrl`, `Synj1`, `Ppip5k2`, `Pi4kb`, `Itpr1`, `Plcb1`, `Pitpna`, `Atp2a2`, `Hspa5`, `Manf`, and `Sec63`.

External biology:

- PubMed-indexed MINPP1 and inositol-polyphosphate literature:
- Chi et al. 1999, `10.1006/geno.1998.5736`, PMID 10087200: mouse and human MINPP1 are conserved histidine phosphatases with an ER-retention signal and broad mouse tissue expression.
- Chi et al. 2000, `10.1128/MCB.20.17.6496-6507.2000`, PMID 10938126: ER-localized Minpp1 metabolizes InsP5 and InsP6 in vivo, but constitutive Minpp1-null mice were viable, fertile, and grossly normal.
- Wundenberg et al. 2014, `10.1042/BJ20130992`, PMID 24865181: IP6 kinases can dephosphorylate InsP6 under low ATP/ADP, providing a non-MINPP1 route for cytosolic/nuclear InsP6 turnover.
- Appelhof et al. 2020, `10.1038/s41431-020-00749-x`, PMID 33168985, and Ucuncu et al. 2020, `10.1038/s41467-020-19919-y`, PMID 33257696: biallelic human MINPP1 variants cause pontocerebellar hypoplasia; MINPP1-deficient human cells accumulate highly phosphorylated inositols, especially IP6, and edited iPSC-derived neurons show impaired differentiation and increased death.
- Nguyen Trung et al. 2022, `10.1021/acscentsci.2c01032`, PMID 36589890: stable-isotope tracing uncovered a MINPP1-dependent branch of human inositol-phosphate dephosphorylation.
- Yu et al. 2023, `10.3390/biom13060885`, PMID 37371464: ER compartmentalization keeps MINPP1's InsP activity separated from cytosolic phosphoinositide lipid signaling; cytosolic MINPP1 can dephosphorylate PIP3 and inhibit growth in HIT cells.

## Computation over the training data

I first read the focal training-count CSV to get the empirical response scale:

- 1,674 non-held-out perturbations were present.
- 469 had nonzero DEG counts in `151 TH Prkcd Grin2c Glut`.
- The distribution is very zero-inflated: median `0`, 75th percentile `1`, 90th percentile `2`, 95th percentile `18`, maximum `2677`.

I then scanned the parquet at `group_name == "151 TH Prkcd Grin2c Glut"` for mechanistically nominated targets. For each candidate target I recomputed:

```python
n_degs = int((sub.pvals_adj < 0.05).sum())
```

and inspected the leading signed Wilcoxon rows to see whether the count was a self-transcript call, a single downstream singleton, or a broader pathway state.

Key focal counts were:

```text
Inpp5k      0
Ocrl        0
Ppip5k2     0
Plcb1       0
Pik3cb      0
Pik3r1      0
Pik3r2      0
Pitpnm3     0
Itpr1       0
Pi4kb       1
Synj1       1
Pitpna     21

Atf6        0
Edem3       0
Lman2l      0
Mttp        0
Suco        0
Amfr        1
Manf        3
Hspa5       5
Sec63      11
Atp2a2    187

Gnptab      0
Manba       0
Sort1       0
Ppt1        1
Psap        1
Tmem106b    1

Xpr1        0
Slc20a2     0
Pdgfrb      0
Ank         1
```

I also verified that `Minpp1` itself is in the measured gene set: the parquet contains 36,472 `names == "Minpp1"` rows across the 1,674 training targets and all 23 groups, including the focal group. In focal rows from the main inositol/ER comparators, `Minpp1`, `Ipmk`, `Itpk1`, `Ppip5k2`, `Inpp5k`, and the UPR markers `Hspa5`, `Ddit3`, `Xbp1`, `Chac1`, and `Herpud1` were all nonsignificant after `Inpp5k`, `Ocrl`, `Ppip5k2`, `Synj1`, `Pi4kb`, `Pitpna`, `Plcb1`, and `Itpr1` perturbation; the positive ER-quality-control controls were instead `Manf`, `Sec63`, `Hspa5`, and especially `Atp2a2`.

## Minpp1 reasoning

### Closest inositol-phosphate and phosphoinositide evidence

MINPP1 is an ER-luminal inositol polyphosphate phosphatase that mainly dephosphorylates soluble higher inositol phosphates such as InsP5 and InsP6. The training universe did not contain a strict MINPP1 paralog, and the closest soluble inositol pyrophosphate gene was `Ppip5k2`, the IP7/IP8 kinase-phosphatase rather than an IP6 phytase. `Ppip5k2` had `0` DEGs in the focal cells. The Distributed Agents `Ppip5k2:F004` finding further reported that the PPIP5K2-InsP8-XPR1 phosphate-efflux axis was transcriptionally quiet: neither `Ppip5k2` nor `Xpr1` produced a robust neuronal phosphate-homeostasis RNA response. In the focal training counts, `Xpr1`, `Slc20a2`, and `Pdgfrb` were also `0`, while `Ank` had only `1`.

I treated the membrane phosphoinositide phosphatases as indirect counterexamples rather than direct analogs. `Inpp5k`, `Ocrl`, and `Synj1` all touch phosphoinositide/endocytic or ER-contact biology, but their own focal counts were `0`, `0`, and `1`, respectively; the lone `Synj1` hit was `Synj1` itself, with no downstream response. The Distributed Agents claim `c26b2c662b0c9f96a92d`, anchored by `Inpp5k:F004`, `Ocrl:F004`, and `Synj1:F004`, summarized the same-experiment conclusion: represented membrane-associated phosphoinositide and endocytic pathway perturbations did not produce an interchangeable neuronal transcriptional module. `Pi4kb:F005` reached the same boundary from the PI4P side: `Pitpna`, `Ocrl`, `Synj1`, `Itpr1`, `Plcb1`, `Inpp5k`, `Ppip5k2`, `Pitpnm3`, and PI3K/14-3-3 comparators did not converge on the tiny `Pi4kb` signature.

`Pitpna` was the main nonzero phosphoinositide-linked perturbation in the focal cells at `21` DEGs, including loss of `Atp2a2` and `Prkcg` and induction of `Scg2`/`Stmn4`-like features. I did not use `21` as the Minpp1 prior because `Pitpna` is a PI-transfer protein that supports PI4P and PIP2 lipid supply, whereas MINPP1 sits on soluble InsP degradation in the ER lumen. The Distributed Agents `Pitpna:F008` finding explicitly shows that `Pitpna` was not phenocopied by `Pitpnm3`, `Pi4kb`, `Ocrl`, `Synj1`, `Plcb1`, `Prkca`, or `Prkcg`, so a single positive lipid-transfer phenotype should not be generalized to every inositol-pathway enzyme.

### ER and calcium-stress evidence

The ER location of MINPP1 raised the question of whether `Minpp1` loss should be projected to the ER-quality-control programs from `Hspa5`, `Manf`, `Sec63`, or `Atp2a2`. The same training data argue against that. `Atp2a2` was broad in the focal cells (`187` DEGs) with a CHOP/UPR/ISR signature involving `Ddit3`, `Chac1`, `Xbp1`, `Herpud1`, `Hspa5`, `Asns`, and amino-acid/one-carbon genes. `Hspa5`, `Manf`, and `Sec63` gave smaller ER-chaperone responses (`5`, `3`, and `11`). But `Atf6`, `Edem3`, `Lman2l`, `Mttp`, and `Suco` were all `0`, and the Distributed Agents ER claims make clear that UPR-like transcription is recoverable but not a generic consequence of perturbing an ER-associated target.

The cleanest calcium counterexample is `Itpr1`. It had `0` focal DEGs, and Distributed Agents `Itpr1:F004`/`Atp2a2:F007` showed that blocking IP3-gated ER calcium release did not reproduce the `Atp2a2` SERCA2 stress program in 151 TH Prkcd Grin2c Glut. Since MINPP1 hydrolyzes IP6/IP5 rather than refilling the ER calcium store, I kept `Atp2a2 = 187` as a detectability control, not as a quantitative analog.

### Disease context and extrapolation to this assay

External literature cuts both ways. Human biallelic MINPP1 disease and MINPP1-null human differentiating neurons show that inositol-polyphosphate imbalance can be severe in neurodevelopmental contexts. However, the assay here perturbs a subset of already postmitotic juvenile neurons for 3-4 weeks and reads steady-state nuclear RNA. That is a poor match to a congenital PCH mechanism, and the Chi et al. germline Minpp1 mouse knockout being viable and grossly normal lowers the expectation of a strong autonomous stress response after partial acute depletion. The Wundenberg et al. finding that IP6 kinases can also degrade cytosolic/nuclear InsP6 further makes a complete, cell-wide IP6 catastrophe from ER-luminal Minpp1 loss less certain in this short sparse assay.

The held-out target transcript itself is the main residual source of one possible DEG. `Minpp1` is measured in these focal profiles, so a highly efficient gRNA set could count the target gene even if no downstream program appears. I still predicted `0` rather than `1`: among the pathway-neighbor enzymes, `Inpp5k`, `Ppip5k2`, `Ocrl`, `Pi4kb`, `Plcb1`, `Itpr1`, and `Sec63` did not score their own target mRNA as a focal FDR hit, despite many having 100-200 matched perturbed nuclei. The within-dataset evidence for this part is weak but points to a flat or subthreshold self row more often than to a guaranteed singleton.

## Prediction

`Minpp1`: predicted `0` DEGs.

The prediction is driven mostly by within-dataset evidence from flat soluble inositol-phosphate, phosphoinositide, IP3/calcium, and ER-adjacent perturbations. External MINPP1 biology was used to reject `Pitpna` and `Atp2a2` as overbroad analogs: they prove that lipid-transfer and ER-calcium stress states are detectable in these cells, but their mechanisms are too far from ER-luminal IP6/IP5 hydrolysis to justify importing their DEG counts to `Minpp1`.

## Limits

Direct evidence is absent: `Minpp1` itself was held out, no direct MINPP1 paralog exists in the training set, and several ideal comparators such as `Ppip5k1`, `Ipmk`, `Ip6k1/2/3`, and multiple `Itpk` genes were not present as perturbation targets. The strongest human MINPP1 evidence is developmental disease and iPSC differentiation, while this screen is sparse acute loss in postmitotic juvenile NeuN+ nuclei. The data also do not measure InsP5, InsP6, IP7/IP8, calcium chelation, DNA indels, or MINPP1 protein. Finally, a one-gene answer is exposed to self-transcript sampling: `0` assumes Minpp1 knockdown remains below the FDR threshold in the focal cells.
