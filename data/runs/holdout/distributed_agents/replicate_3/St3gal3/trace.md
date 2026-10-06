# Reasoning trace

## Question interpreted

The requested held-out manifest contains one target, `St3gal3`. I interpreted the task as predicting the integer number of measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after the held-out `St3gal3` perturbation in `151 TH Prkcd Grin2c Glut` neurons. The count includes all measured genes, including the target transcript itself if it passes FDR. The `151 TH Prkcd Grin2c Glut` label was treated as a thalamic glutamatergic class; `TH` is the atlas thalamus abbreviation here.

The endpoint is assay-specific and survivor-conditioned. I did not treat germline or patient phenotypes as direct DEG-count evidence, and I did not use target-RNA loss as an editing-efficiency score; self-transcript hits are only relevant because they can contribute one row to the observed endpoint.

## Sources used

- Input manifest: `[local file: 225_St3gal3.csv]`.
- Training endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Run-local Distributed Agents dataset metadata, especially `codex_runtime/pipeline/dataset_context.md`, `measurement_registry.json`, and `scalar_prior_calibration.json`.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`; I queried `target_context`, `expand_candidate_set`, and `candidate_set_topology`.
- Distributed Agents runtime profile tools, used to compare the focal DE profiles of `St3gal5`, `B3gat3`, `Cog4`, `Cog5`, and `Stx5a`.
- PubMed via NCBI E-utilities for external ST3GAL3/ST3GAL biology.

## Computations over the supplied data

1. The manifest was read directly and contains only:

   ```tsv
   target_name
   St3gal3
   ```

2. The training-count CSV has 1,674 non-held-out focal targets. Its DEG-count distribution is highly zero-inflated:

   | class | definition | training targets |
   |---|---:|---:|
   | none | `n_degs == 0` | 1205 |
   | weak | `1 <= n_degs < 10` | 363 |
   | medium | `10 <= n_degs < 100` | 63 |
   | strong | `n_degs >= 100` | 43 |

   The median count is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and the maximum is 2677. Thus a held-out Golgi/glycan enzyme needs specific evidence to be moved far above zero.

3. I searched the focal training targets for glycosylation and trafficking terms. The only represented `St3gal` enzyme in the focal training endpoint was `St3gal5`, with `n_degs = 1`; `St3gal2`, `St3gal4`, and `St3gal6` were not present as training perturbations.

4. I queried the DE parquet for the exact focal rows of the candidate analogs and counterexamples:

   ```sql
   SELECT names, gene_target, logfoldchanges, pvals_adj, scores,
          n_pert_matched, n_ctrl_matched
   FROM read_parquet($training_de_parquet)
   WHERE group_name = '151 TH Prkcd Grin2c Glut'
     AND gene_target IN (...)
   ```

   The key focal counts were:

   | training perturbation | focal `n_degs` | focal expression-pattern evidence |
   |---|---:|---|
   | `St3gal5` | 1 | The only FDR<0.05 row was its own transcript, `St3gal5`, down in the knockout: log2FC -0.788, FDR 1.96e-14. The strongest non-self rows all had FDR 1. |
   | `B3gat3` | 0 | No significant focal rows; all leading nominal rows had FDR 1. |
   | `Ext1` | 0 | No significant focal rows; all leading nominal rows had FDR 1. |
   | `Ext2` | 0 | No significant focal rows; its own transcript was nearest but still subthreshold at FDR 0.0559. |
   | `Xylt1` | 0 | No significant focal rows; all leading nominal rows had FDR 1. |
   | `Glce` | 0 | No significant focal rows; best adjusted P was 0.162. |
   | `Gpc6` | 0 | No significant focal rows; all leading nominal rows had FDR 1. |
   | `Hs6st2` | 0 | No significant focal rows; all leading nominal rows had FDR 1. |
   | `Cog4` | 0 | No focal COG/Golgi RNA response; all leading nominal rows had FDR 1. |
   | `Cog5` | 0 | No focal COG/Golgi RNA response; best adjusted P was 0.377. |
   | `Stx5a` | 0 | No focal SNARE/Golgi response; all leading nominal rows had FDR 1. |
   | `Dpm1` | 0 | No focal N-glycosylation response; best adjusted P was 0.0866. |
   | `Tmem165` | 0 | No focal Golgi/CDG response; all leading nominal rows had FDR 1. |
   | `Copa` | 0 | No focal COPI response; best adjusted P was 0.364. |
   | `Trip11` | 0 | No focal Golgi-tethering response; all leading nominal rows had FDR 1. |
   | `Atp2c1` | 1 | Self-only call, `Atp2c1`, log2FC -0.385, FDR 0.00641. |
   | `Stx16` | 1 | Self-only call, `Stx16`, log2FC -0.476, FDR 0.00149. |
   | `Copg1` | 1 | Self-only call, `Copg1`, log2FC -0.668, FDR 9.24e-17. |
   | `Vps35` | 17 | A broader retromer response, including `Atp2a2`, `Brsk1`, `Grin2b`, `Ccdc136`, and `Vps35`. |
   | `Vps54` | 31 | A broader GARP response with immediate-early/synaptic rows such as `Egr1`, `Jun`, and `Kctd16`. |
   | `Gfpt1` | 311 | Strong positive control for glycosylation-linked ER/ISR transcription in this exact cell group; top hits included `Ogt` down and `Herpud1`, `Asns`, `Ddit3`, `Shmt2`, and `Hspa5` up. |

5. I also checked neurodevelopmental/epilepsy counterexamples represented in the focal training endpoint: `Arx = 0`, `Cdkl5 = 1`, `Kcnq2 = 1`, `Cntnap2 = 1`, `Mecp2 = 16`, and `Grin1 = 89`. These show that sharing a seizure or neurodevelopmental disease label does not force a broad acute thalamic DEG response.

## Same-experiment corpus evidence

- `St3gal3` itself was absent from the selected Distributed Agents corpus release, so there was no packaged same-experiment neighborhood or claim for this held-out target.
- `St3gal5` had five same-experiment findings. The relevant conclusions were that its surface was ultra-sparse, that the only FDR-supported signal in the corpus was a one-gene `Pggt1b` induction in `155 MB Glut`, and that it lacked canonical GM3-ganglioside, glucose/mitochondrial, immediate-early, UPR/ISR, or apoptosis transcriptional programs despite on-target St3gal5 RNA reduction in many groups. A cross-perturbation contrast reported that `Sptlc2`, `Asah1`, and `Psap` did not phenocopy `St3gal5`.
- The corpus claim containing `St3gal5`, `Asah1`, `Cert1`, `Sphk1`, `Sptlc2`, and `Stard7` stated that represented sphingolipid-pathway and lipid-transfer perturbations do not form a coherent shared multi-gene neuronal transcriptomic module in this screen.
- `B3gat3` anchored a glycosaminoglycan/heparan-sulfate claim stating that single-node perturbations of represented GAG, heparan-sulfate, and proteoglycan pathway genes did not collapse into a common acute postnatal neuronal transcriptional module. This was useful as an extracellular/Golgi glycan counterexample rather than as a direct ganglioside analog.
- `Cog4` and `Cog5` anchored COG/Golgi findings. The corpus specifically reported a pan-null steady-state snRNA profile for `Cog4`, near-null `Cog5` behavior, and no generic broad secretory-pathway module across COG/SNARE/ER-Golgi trafficking perturbations.
- A corpus expansion from `St3gal5`, `B3gat3`, `Cog4`, and `Cog5`, intersected with the 1,674 focal training targets, yielded only one recurrent extra candidate, `Stx5a`, nominated by both `Cog4` and `Cog5`. `Stx5a` was also zero in the focal endpoint.
- The induced explicit-reference topology over `St3gal5`, `B3gat3`, `Cog4`, `Cog5`, and `Stx5a` had a connected `Cog4`/`Cog5`/`Stx5a` component, while `St3gal5` and `B3gat3` were isolates. This supports treating the COG/SNARE group as a Golgi-buffering boundary and `St3gal5` as the only close ganglioside comparator, rather than averaging all five as one homogeneous module.
- The run-local cohort profile over those five focal signatures had 0 significant overlapping genes in every pair. Four of the five profiles had no FDR<0.05 rows at all, and `St3gal5` had only its self transcript. Subthreshold leading rows were not coherent enough to move the prediction away from the `0` to `1` regime.

## External biology used

- `ST3GAL3` encodes beta-galactoside alpha-2,3-sialyltransferase III, a Golgi sialyltransferase that can generate alpha-2,3 sialylated glycans. Edvardson et al. identified biallelic loss of ST3GAL3 in West syndrome and showed that the mutation affected an essential sialyl-motif and abolished enzymatic activity (Edvardson et al., 2012, Epilepsia, DOI 10.1111/epi.12050, PMID 23252400).
- Human patient-derived ST3GAL3-deficient cortical neurons showed altered lectin staining, enhanced adherence on poly-L-ornithine/laminin, and altered TBR1-positive neuron abundance in vitro, supporting a developmental surface-glycosylation/adhesion model rather than an obligate mature-neuron stress-transcription model (van Diepen et al., 2018, European Journal of Human Genetics, DOI 10.1038/s41431-018-0220-5, PMID 30089820).
- The human disease is a rare autosomal-recessive developmental and epileptic encephalopathy with epilepsy, motor and language impairment, hypotonia, and behavioral features, summarized across the small published case set by Khamirani et al. 2021 and Whitney et al. 2023 (DOI 10.1016/j.ejmg.2021.104250, PMID 34022416; DOI 10.1002/epi4.12747, PMID 37067065).
- Sturgill et al. showed in mouse that St3gal2 and St3gal3 together synthesize almost all terminal alpha-2,3 sialylation of the major brain gangliosides GD1a and GT1b. Crucially for this prediction, adult `St3gal3` single-null brains did not differ significantly from wild type in ganglioside expression, whereas `St3gal2` single-null brains had about half-normal GD1a/GT1b and `St3gal2;St3gal3` double-null brains were more than 95% depleted of GD1a/GT1b (Sturgill et al., 2012, Glycobiology, DOI 10.1093/glycob/cws103, PMID 22735313).
- Blazetic et al. connected this terminal-sialylation biology to inhibitory-neuron maturation in mouse cortex, hippocampus, and striatum, with calcium-binding interneuron changes strongest in the `St3gal2` and `St3gal2;St3gal3` mutant settings (Blazetic et al., 2023, International Journal of Molecular Sciences, DOI 10.3390/ijms242417218, PMID 38139047).

## Target-specific prediction for St3gal3

The direct, pathway-nearest training perturbation is `St3gal5`, the GM3 synthase that initiates ganglioside a- and b-series synthesis upstream of complex brain gangliosides. In the focal cell group, `St3gal5` had `n_degs = 1`, and that one hit was just `St3gal5` itself; there was no downstream GM3/ganglioside or stress signature. Corpus findings independently described `St3gal5` as ultra-sparse and non-convergent with represented sphingolipid comparators. This argues that acute partial loss of a neuronal sialyltransferase can make a biochemical glycan lesion without producing a broad nuclear snRNA-seq state after P16 perturbation.

The Golgi/glycosylation boundary targets reinforce that interpretation. `Cog4`, `Cog5`, `Dpm1`, `Tmem165`, `Stx5a`, `Copa`, `Trip11`, `B3gat3`, `Ext1`, and `Ext2` were all zero in the same focal endpoint. The screen can detect ER/glycosylation stress when present, because `Gfpt1` yielded 311 DEGs with UPR/ISR genes such as `Herpud1`, `Asns`, `Ddit3`, and `Hspa5`; therefore the lack of a broad response around St3gal enzymes is not just a blind spot of the cell group or Wilcoxon pipeline.

The main countervailing prior is that biallelic ST3GAL3 loss is a real human epileptic encephalopathy gene. I downweighted that prior for this endpoint because those observations are congenital, often complete loss-of-function, and likely pass through altered surface sialylation, adhesion, and circuit development. Sturgill et al.'s mouse result also indicates partial redundancy in adult brain ganglioside terminal sialylation: `St3gal3` becomes essential for GD1a/GT1b synthesis mainly when `St3gal2` is also absent. The P16-to-P37/44 sparse perturbation in already postmitotic NeuN-positive neurons is therefore more likely to be buffered on steady-state nuclear RNA than to replay germline cortical development.

Given that evidence, I predicted no multi-gene downstream program for `St3gal3`. I did not set the count to exactly zero because `St3gal5`, `Atp2c1`, `Stx16`, `Copg1`, `Cdkl5`, `Kcnq2`, and `Cntnap2` show that expressed membrane/Golgi/synaptic targets often register as a single self-transcript call in this focal group while still lacking downstream DE. The final point prediction is:

| target | predicted `n_degs` |
|---|---:|
| `St3gal3` | 1 |

## Limits

This prediction is an extrapolation because `St3gal3`, `St3gal2`, `St3gal4`, and `St3gal6` were all absent as training perturbations, leaving `St3gal5` as the only close local sialyltransferase analog. `St3gal5` acts at the GM3 branch point, while `St3gal3` terminally sialylates glycoprotein and glycolipid acceptors, so they are not paralog-equivalent. The training data also measure nuclear RNA, not ganglioside abundance, protein sialylation, Golgi morphology, axonal adhesion, or synaptic physiology. Human ST3GAL3 disease and mouse germline data strongly establish biological importance but are imperfect for estimating an acute partial postnatal thalamic DEG count. The difference between zero and one DEG is especially uncertain because a self-transcript call depends on baseline expression, guide-induced transcript decay, and matched-cell power more than on the downstream glycan phenotype.
