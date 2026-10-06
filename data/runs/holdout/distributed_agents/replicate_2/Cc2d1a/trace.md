# Cc2d1a DEG-count prediction

## Question and resolved ambiguities

The requested held-out perturbation was the single target `Cc2d1a` from `031_Cc2d1a.csv`. I interpreted `n_degs` as the number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` class after acute, sparse, postnatal AAV-CRISPR loss of function. The held-out `Cc2d1a` rows were not in the training-count CSV and a direct Parquet query for `gene_target = 'Cc2d1a'` returned 0 rows, so I did not use any Cc2d1a outcome or Cc2d1a expression profile.

The endpoint is response breadth in recovered NeuN+ nuclei, not protein loss, cell survival, behavior, synaptic physiology, or editing efficiency. I therefore treated germline and Cre-lox mouse phenotypes as biological priors about Cc2d1a function and transferred the numerical scale only from non-held-out Perturb-seq targets measured in the same assay.

## Sources used

- Differential-expression Parquet: `training_de_all_cell_groups.parquet`, especially `151 TH Prkcd Grin2c Glut` rows for biologically selected comparator targets.
- Training focal counts: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Run manifest: `031_Cc2d1a.csv`.
- Same-experiment semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`; Cc2d1a itself was absent from the corpus, but Chmp4b, Htr1a, Nfkb1, App, Atg5, Mib1, Tsc2, and Rab7 target contexts and higher-order Claims were used to interpret measured comparator surfaces.
- PubMed for external biology: Basel-Vanagaite et al. 2005, DOI `10.1136/jmg.2005.035709`; Rogaeva et al. 2007, DOI `10.1002/jnr.21277`; Zhao et al. 2010, DOI `10.1074/jbc.M109.100057`; Al-Tawashi et al. 2012, DOI `10.1074/jbc.M111.261875`; Martinelli et al. 2012, DOI `10.1016/j.jmb.2012.02.044`; Manzini et al. 2014, DOI `10.1016/j.celrep.2014.06.039`; Deshar et al. 2016, DOI `10.1016/j.bbrc.2016.10.053`; Oaks et al. 2017, DOI `10.1093/cercor/bhw009`; Yang et al. 2019, DOI `10.1523/JNEUROSCI.2395-18.2019`; Yang et al. 2021, DOI `10.1007/s13311-021-01072-z`.

## Computations over the training data

The focal training endpoint is strongly zero-inflated: 1,205/1,674 training targets have `n_degs = 0`, 363 have 1-9, 63 have 10-99, and 43 have at least 100. Thus a zero prediction is the background expectation unless a target has a close assayed analogue with a demonstrable focal RNA response.

For Cc2d1a I enumerated training perturbations covering the main known axes of the gene: CHMP4B/ESCRT, serotonin and dopamine receptor transcription, NF-kB/TLR signaling, cAMP/PKA/CREB and Rac1, autophagy, Notch and APP processing, PI3K/mTOR, and late endosome/lysosome stress. I queried their exact focal DEG counts from the training CSV and their focal DE rows from the Parquet. The Parquet count recomputation matched the CSV counts.

The non-obvious Parquet operation was a filtered DuckDB scan over the focal group and curated target list:

```sql
select gene_target, count(*) as rows, sum(pvals_adj < 0.05) as n_degs,
       max(n_pert_matched) as n_pert, max(n_ctrl_matched) as n_ctrl
from read_parquet(PARQUET)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

I also ran a Distributed Agents runtime profile comparison on a 36-target Cc2d1a-neighborhood panel. It found 25/36 with no FDR-significant focal features, 5/36 with 1-9 features, 4/36 with 10-49, and only 2/36 with 50 or more. This was used as a consistency check: the panel is mostly flat at the actual signature level rather than merely low in the scalar count table.

Key focal comparator counts were:

| Axis | training perturbations in `151 TH Prkcd Grin2c Glut` |
| --- | --- |
| Direct ESCRT interactor | `Chmp4b` 0 |
| cAMP/PKA/CREB and Rac1 | `Pde4b` 0, `Pde4d` 0, `Camk2a` 0, `Camk2b` 1, `Creb1` 10, `Rac1` 0, `Tnik` 0 |
| Freud-1 receptor targets | `Htr1a` 0, `Htr2a` 0, `Drd2` 0; all represented Htr-family receptors were 0 in the focal group |
| NF-kB/TLR | `Nfkb1` 0, `Rel` 0, `Chuk` 0, `Map3k7` 0, `Traf3` 0, `Cyld` 0, `Tlr2`/`Tlr3`/`Tlr4`/`Tlr5`/`Tlr7`/`Tlr8` all 0 |
| Notch and APP processing | `Dll1` 0, `Notch1` 0, `Notch2` 0, `Notch4` 0, `Psen1` 0, `Adam10` 0, `App` 1, `Mib1` 27, `Tm2d1` 1 |
| Autophagy and mTOR | `Atg5` 0, `Atg16l1` 0, `Becn1` 0, `Mtor` 2, `Akt3` 0, `Tsc2` 86 |
| Endosomal/lysosomal traffic | `Vps35` 17, `Vps54` 31, `Rab7` 501 |

The nonzero comparators showed biology-specific signatures rather than a generic CC2D1A-like state. `Mib1` up-regulated sterol/cholesterol synthesis genes such as `Insig1`, `Fdft1`, `Dhcr24`, `Msmo1`, `Hmgcr`, `Cyp51`, and `Ldlr`. The Distributed Agents Mib1 findings state that this is a recurrent SREBF2-like cholesterol module and is uncoupled from canonical Dll1/Notch/Adam10/Psen1 transcriptional signaling in the same assay. `Tsc2` and especially `Rab7` were broad metabolic, sterol, and late-endosomal/lysosomal stress responses. Those responses are useful positive controls showing that the focal cell class can display endomembrane stress, but loss of CC2D1A is not equivalent to deleting the late-endosomal GTPase RAB7 or releasing the core TSC2 brake on mTORC1.

## Target-specific biological reasoning

### `Cc2d1a`

Basel-Vanagaite et al. 2005 identified truncating human `CC2D1A` mutations causing autosomal-recessive nonsyndromic intellectual disability, so the gene has a real neuronal disease prior. Cc2d1a is also functionally important in mice: complete neural progenitor deletion is lethal, while postnatal CamKIIa-driven forebrain deletion causes cortical dendritic/spine defects and cognitive and social phenotypes (Oaks et al. 2017). Forebrain excitatory-neuron deletion impairs hippocampal LTP and dendritic arborization via Rac1 hyperactivation (Yang et al. 2019), and Emx1-Cre glutamatergic deletion produces autistic-like behavior and cortical/mPFC morphological and E/I changes (Yang et al. 2021). These data argue that Cc2d1a perturbation can matter in neurons, but the phenotypes are dominated by development, morphology, circuit physiology, and forebrain hippocampal/cortical readouts rather than a proven broad thalamic single-nucleus mRNA response 3-4 weeks after P16 sparse CRISPR.

The closest endosomal evidence points downward for this endpoint. Martinelli et al. 2012 showed that CC2D1A binds ESCRT-III CHMP4B; Deshar et al. 2016 found that combined CC2D1A/CC2D1B depletion changes EGFR and TLR4 receptor degradation by altering CHMP4B-associated endosomal sorting. In the same Perturb-seq assay, however, `Chmp4b` had 0 focal DEGs, and the Distributed Agents Chmp4b finding reports no robust recurrent ESCRT/autophagy/cargo signature with Atg5, Becn1, Sqstm1, App, Grin1, Ntrk1, or Notch receptor comparators. Direct loss of central late-endosomal `Rab7` yielded 501 focal DEGs and `Vps35`/`Vps54` yielded 17/31, so some endosomal damage is detectable in `151 TH Prkcd Grin2c Glut`; the key distinction is that Rab7/Vps35/Vps54 are core trafficking failures, whereas CC2D1A is an ESCRT-III-associated scaffold with partial paralog buffering by Cc2d1b and only indirect effects on cargo sorting.

The NF-kB, receptor, and PKA/CREB hypotheses were also weak on the measured scale. Zhao et al. 2010 and Manzini et al. 2014 place CC2D1A in NF-kB signaling and show altered NF-kB homeostasis after Cc2d1a disruption; Al-Tawashi et al. 2012 links CC2D1A to cAMP/PKA/CREB signaling; Rogaeva et al. 2007 reviews Freud-1/CC2D1A repression of `HTR1A`. But the dataset's exact pathway anchors were flat: `Nfkb1`, `Rel`, `Chuk`, `Map3k7`, `Traf3`, `Cyld`, all measured TLRs, all measured focal Htr receptors, `Drd2`, `Pde4b`, `Pde4d`, `Camk2a`, `Rac1`, and `Tnik` had 0 focal DEGs. The corpus high-confidence NF-kB Claim states that represented TNFR/TLR/IL-1/CD40-to-TAK1/IKK/NF-kB/JNK/p38 perturbations are broadly transcriptionally silent as a basal module in unchallenged postnatal NeuN+ neurons. Its Htr1a Claim likewise states that represented serotonin receptors do not form a shared basal neuronal transcriptomic module.

The main positive same-process counterexamples do not transfer well. `Creb1` itself had 10 focal DEGs, but CC2D1A is a scaffold that can affect PKA/CREB localization and activation, not the core CREB transcription factor. `Mib1` had 27 focal DEGs, but its measured response is a sterol module separated by the corpus from canonical Notch output; `Dll1`, `Notch1`, `Notch2`, `Notch4`, `Adam10`, and `Psen1` were all zero. `Tsc2` had 86 focal DEGs, but TSC2 loss is a direct mTORC1 hyperactivation state, while `Mtor` loss had only 2 and `Akt3` loss was 0. `Atg5`, `Atg16l1`, and `Becn1` were all 0 in the focal group, limiting any prediction of a broad autophagy readout.

Putting these together, the biologically relevant measured perturbations are overwhelmingly zero or singleton in the focal cell group, and the broad endolysosomal or sterol responders are stronger, different lesions rather than direct analogues. I therefore predict that acute sparse Cc2d1a loss in `151 TH Prkcd Grin2c Glut` will not have any gene crossing BH FDR 0.05.

Predicted point: `Cc2d1a = 0`.

## Limits and extrapolation

- There was no same-experiment Cc2d1a expression signature, no Cc2d1b perturbation, and no exact same-complex loss-of-function analogue for the CC2D1A scaffold.
- The strongest published mouse phenotypes use germline, Nestin-Cre, Emx1-Cre, or CamKIIa-Cre deletions and assay cortical or hippocampal development, dendrites, spines, LTP, behavior, and circuits. They are imperfect proxies for P16 mosaic AAV CRISPR in a thalamic glutamatergic cell class.
- snRNA-seq would miss CC2D1A effects that remain at phospho-CREB, Rac1 activity, receptor residence time, dendritic spine morphology, or electrophysiology without a persistent nuclear mRNA adaptation.
- The zero is a point prediction, not a claim that CC2D1A is biologically unimportant in neurons. A few subthreshold or protein-level changes are plausible; the prediction is only that none will pass the focal Wilcoxon BH threshold at 0.05 in this held-out endpoint.
