# Slc12a5 forecast for `151 TH Prkcd Grin2c Glut`

## Evidence used

- Target and endpoint: the one held-out target is `Slc12a5`; the endpoint is the count of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Dataset scope: the count table used for the numeric training surface was `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`; the row-level DE table used for endpoint checks was `[local file: training_de_all_cell_groups.parquet]`. These are same-experiment representations, not independent replication.
- Exact Slc12a5 reach: the declared characterization bundle reports `feature_available=true` in the focal class, `mean_cp10k=2.564049388708852`, `mean_raw_umi=4.246674268339034`, and `22251/23679`, or `93.96933992144939%`, non-target nuclei expressing Slc12a5. Thus the target transcript is broadly present in the assayed thalamic neurons.
- Slc12a5 biology prior: the same bundle adjudicates KCC2 functional stock as `likely_substantially_depleted` by the P37-P44 harvest after a P16 disruptive edit. The operative stock is a renewable membrane chloride transporter; adult or postnatal conditional-loss studies show major KCC2 protein depletion over days to a few weeks and mature-neuron functional phenotypes on a similar clock. This supports real cell biology in edited, Slc12a5-expressing survivors, but does not itself guarantee a nuclear-RNA response.
- Same-experiment corpus around Slc12a5: the selected release had no Slc12a5 Finding, Claim, or explicit comparator records. Corpus evidence therefore entered through visible pathway comparators, not through a Slc12a5 outcome.
- Global `151` training scale: among 1,674 visible perturbations, 1,205 had `n_degs=0`, the median was `0`, the 75th percentile was `1`, and only 5% exceeded `18`. Large responses were concentrated in broad RNA, proteasome, chromatin, and essential-cell-state genes rather than in most neuronal excitability genes.
- Chloride-transporter pathway comparators were nearly blank in the same count table:

```tsv
target_name	n_degs
Slc12a2	0
Wnk1	0
Wnk3	1
Stk39	0
Strada	0
Prkca	0
```

  The same-experiment Slc12a2 and Wnk3 Findings explicitly interpret WNK1/WNK3/STK39/SLC12A2-centered cation-chloride-cotransporter signaling as biologically plausible but mostly invisible to basal postnatal neuronal nuclear RNA. That is the closest direct warning for KCC2: transporter phosphorylation and chloride flux can matter without generating a shared FDR-level transcriptomic program.
- Represented GABA-A receptor subunits and nearby inhibitory signaling genes gave only sparse focal-class responses:

```tsv
target_name	n_degs
Gabra1	1
Gabra2	0
Gabra3	0
Gabra5	0
Gabrb1	0
Gabrb2	4
Gabrb3	0
Gabrd	2
Gabrg2	1
Gabrg3	0
Gabrr2	0
Slc6a1	0
```

  Direct parquet inspection of `151 TH Prkcd Grin2c Glut` at `pvals_adj < 0.05` showed Gabrb2 contributed `Gabrb2`, `Nr4a1`, `Vgf`, and `Nalf1`; Gabra1 and Gabrg2 contributed only their self-transcripts. The Gabrb2 and Gabrg2 Findings call these activity-associated but sparse, receptor-subunit- and context-specific outputs rather than a pan-GABAergic module.
- Other high-relevance ion-homeostasis and thalamic excitability comparators bounded the plausible upper tail. Kcnq2, Kcnq3, Scn1a, Scn2a, and Scn8a had one DEG each in the focal class. Cacna1g had 12, giving a real but narrow thalamic CaV3.1 transcriptional footprint. Atp1a3 was much larger with 80 BH<0.05 genes in the count table, but its corpus records place it in a distinct Na,K-ATPase state with calcium-pump, membrane, Wnt/adhesion, and redox components; it is therefore a loose upper-bound comparator rather than a close KCC2 donor.

## Synthesis

Slc12a5 is much more likely to be functionally reached than Slc12a2 because KCC2 is abundant in this thalamic glutamatergic population and is a continuously renewed mature-neuron membrane transporter. That pushed the forecast above the pure chloride-pathway average, where all represented WNK/SPAK/NKCC1 nodes were zero or singleton.

The downward evidence was stronger for DEG burden. The closest measured perturbations say that chloride handling, potassium/sodium channels, and most GABA-A subunits can be electrophysiologically meaningful while leaving at most a target-row or one-gene survivor RNA trace after sparse P16 editing. Gabrb2 demonstrated that the assay can convert impaired inhibition into a few focal thalamic activity genes, so a small Slc12a5 response is plausible; however, Gabrb2 was the exception within a GABA-A family whose focal-class median remained zero, and the WNK/CCC surface showed no broad transporter module.

I therefore placed Slc12a5 at the low visible end rather than at the Cacna1g or Atp1a3 scale: a self/singleton-scale call, with no expectation of a resolved multi-gene program.

## Point prediction

`predicted_n_degs = 1`
