# Question and resolved ambiguities

The requested prediction is the integer number of genes with `pvals_adj < 0.05` after each held-out perturbation in `151 TH Prkcd Grin2c Glut` neurons. The held-out perturbation in this run is exactly:

```tsv
target_name
Rab28
```

`Rab28` was absent from both supplied training inputs, so I treated all `Rab28` DEG counts and `Rab28` expression signatures as unobserved. I counted the target transcript itself when present, because the training endpoint does so: in the focal training data the one FDR-significant event after `Arl3` perturbation is `Arl3` itself and the one event after `Ttc8` perturbation is `Ttc8` itself.

# Sources used

- Supplied endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, with 1,674 non-held-out focal-cell counts.
- Supplied DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 193_Rab28.csv]`.
- Distributed Agents same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Rab28)` returned `target_found=false`; the useful same-experiment semantic records were around measured ciliary comparators, especially `Ift88:F003`, `Ttc8:F003`, `Bbs5:F003`, `Arl3:F003`, and `Rab7:F002-F009`.
- Distributed Agents runtime profile comparison `workbench/rab28_profile_compare.json`, comparing 19 focal-cell profiles from the measured Rab/ciliary candidate set.
- NCBI PubMed literature searches for `RAB28`, with target-function support from Roosing et al. 2013, DOI `10.1016/j.ajhg.2013.05.005`, PMID `23746546`; Jensen et al. 2016, DOI `10.1371/journal.pgen.1006469`, PMID `27930654`; Ying et al. 2018, DOI `10.1074/jbc.RA118.005484`, PMID `30228185`; Akella et al. 2020, DOI `10.7554/eLife.50580`, PMID `32101165`; Carter et al. 2020, DOI `10.3389/fcell.2020.00136`, PMID `32258030`; Jespersgaard et al. 2020, DOI `10.1167/iovs.61.2.29`, PMID `32084271`; and Moran et al. 2022, DOI `10.1096/fj.202101897R`, PMID `35471581`.

# Computation over the training data

The focal training counts are zero-inflated: 1,205 of 1,674 targets, 71.98%, have `n_degs = 0`; the median is 0, the 75th percentile is 1, and only 106 targets have 10 or more DEGs. That background makes a zero prediction the default unless measured mechanistic analogs show a broader focal-cell response.

The full parquet has 616,253,184 rows. I used PyArrow metadata to avoid a whole-table load; `group_name` is row-group clustered, and the requested `151 TH Prkcd Grin2c Glut` block lies in row groups 546-580. For exact ciliary and Rab comparator checks I used predicate-filtered DuckDB queries of the form:

```sql
SELECT
  gene_target,
  SUM(pvals_adj < 0.05)::INTEGER AS n_05,
  MIN(pvals_adj) AS min_q
FROM read_parquet($parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ($candidate_set)
GROUP BY gene_target;
```

The focal-cell counts for direct or mechanistically relevant `Rab28` comparators were:

| comparator set | training perturbations and focal `n_degs` | interpretation for `Rab28` |
| --- | --- | --- |
| Core BBSome / BBSome-adjacent | `Bbs5 0`, `Ttc8/Bbs8 1` | `Rab28` is BBSome-dependent at ciliary/periciliary membranes in nematode sensory cilia; loss of a core BBSome component itself was essentially silent in the focal neuronal RNA endpoint. The single `Ttc8` hit was `Ttc8` self-downregulation, not a downstream module. |
| Intraflagellar transport and ciliary motors | `Ift43 0`, `Ift81 0`, `Ift88 0`, `Kif3b 0`, `Ttc21b 0` | These are more central to ciliary assembly/transport than `Rab28`; if acute ciliary transport failure produced a broad basal RNA state in `151 TH Prkcd Grin2c Glut`, these perturbations should have exposed it. |
| Retinal/ciliary gate and ciliopathy genes | `Cep290 0`, `Rpgr 0`, `Rpgrip1l 0`, `Iqcb1 0`, `Spata7 0`, `Rho 0`, `Ttll5 0`, `Kiz 0`, `Sclt1 0` | `Rab28` disease biology is concentrated in photoreceptor outer segments and RPE phagocytosis; the represented retinal/ciliary-gate genes were flat in the postnatal brain-neuron endpoint. |
| ARL3 ciliary cargo cycle | `Arl3 1`, `Arl2bp 0` | ARL3/PDE6D/UNC119 biology is closer to lipidated ciliary cargo delivery than lysosomal Rabs. `Arl3` had only its own transcript significant in the focal class. `Pde6d`, a reported RAB28 interactor, was not a training target. |
| Other measured Rab-family or Rab-regulator perturbations | `Rab18 0`, `Rab27a 0`, `Rab3gap1 0`, `Rab3gap2 0`, `Rab7 501` | The quiet Rab18/Rab27/Rab3GAP surfaces argue that Rab-family membership alone does not imply a response. `Rab7` was rejected as a scale donor: the Distributed Agents corpus resolves it as a late-endosomal/lysosomal sterol, V-ATPase and stress compensation state, a different biology from Rab28 periciliary/photoreceptor outer-segment trafficking. |

Expanding the panel to all ciliary, Hedgehog/ciliary-GPCR, and retinal-ciliary comparator targets named in the same-experiment corpus gave the same result: in the exact focal-cell count table every such target had `0` DEGs except `Arl3 = 1` and `Ttc8 = 1`, and those two singleton counts were self-transcript calls. A Distributed Agents runtime focal-cell profile comparison of 19 hand-nominated Rab/ciliary candidates found 16 profiles with no significant genes, two with 1-9 significant genes (`Arl3`, `Ttc8`), and only the rejected counterexample `Rab7` with at least 50 significant genes.

# Biology and comparator choice

Human RAB28 loss-of-function causes autosomal-recessive cone-rod dystrophy, and rat retina staining localized RAB28 to the photoreceptor basal body/ciliary rootlet, nominating ciliary trafficking rather than a housekeeping Rab program as the disease-relevant axis (Roosing et al. 2013, DOI `10.1016/j.ajhg.2013.05.005`). Subsequent model work is also photoreceptor- and sensory-cilium-centered. Mouse `Rab28` knockout caused cone outer-segment shedding/phagocytosis defects and progressive retinal degeneration, with PDE6D required for RAB28 delivery to outer segments (Ying et al. 2018, DOI `10.1074/jbc.RA118.005484`). Zebrafish `rab28` mutants had reduced cone outer-segment shedding material while retaining gross visual function and retinal structure at early timepoints (Carter et al. 2020, DOI `10.3389/fcell.2020.00136`), and cone-specific Rab28 restoration was sufficient to rescue outer-segment phagocytosis and visual-cycle defects (Moran et al. 2022, DOI `10.1096/fj.202101897R`; Moran et al. 2023, DOI `10.1016/j.visres.2023.108270`).

`Rab28` also has a direct ciliary link outside photoreceptors. In *C. elegans*, RAB-28 behaves as a ciliary GTPase with BBSome-dependent periciliary targeting and intraflagellar-transport association; Jensen et al. placed it closest to the BBS protein RABL4/IFT27 (Jensen et al. 2016, DOI `10.1371/journal.pgen.1006469`). Akella et al. showed that ciliary Rab28 and the BBSome negatively regulate extracellular-vesicle shedding from sensory-organ cilia, with lipidated Rab28 targeting dependent on the BBSome and PDE6D (Akella et al. 2020, DOI `10.7554/eLife.50580`). A patient RAB28 missense variant disrupted RAB28 localization to primary cilia while ciliogenesis in fibroblasts appeared unaffected, again fitting a specialized cargo/localization defect rather than wholesale cilium loss (Jespersgaard et al. 2020, DOI `10.1167/iovs.61.2.29`).

These facts made `Bbs5`, `Ttc8/Bbs8`, IFT components, `Arl3`/`Arl2bp`, `Cep290`, `Rpgr`, and `Rpgrip1l` appropriate analogs. The same-experiment corpus independently treats that set as a dense retinal/ciliary comparator component: `candidate_set_topology` over `Arl2bp, Arl3, Bbs5, Cep290, Ift43, Ift81, Ift88, Kif3b, Rpgr, Rpgrip1l, Ttc21b, Ttc8` found one connected component with 60 of 66 possible within-set pairs connected by explicit Finding references or shared Claims. Crucially, the corpus Claims say that those relationships did not become a robust neuronal RNA module. For example:

- `Ift88:F003` states that IFT, dynein-2, BBSome, Cep290, Ptch/Gli/Smo-related perturbations converged mainly by being transcriptionally buffered rather than by inducing a shared IFT-B knockout transcriptome.
- `Ttc8:F003` states that measured BBSome/IFT comparators were nearly orthogonal to `Ttc8` and flat or singleton-only.
- `Arl3:F003` states that expected ARL3/ciliopathy comparators were orthogonal or flat despite belonging to overlapping ciliary systems.
- `Bbs5:F003` states that membership in ciliary trafficking was insufficient to define a shared neuronal DE program.

I treated `Rab7` as a counterexample, not as a `Rab28` donor. `Rab7` loss in this same dataset induced lysosomal hydrolase, V-ATPase, sterol/lipid, ISR/UPR, autophagy, redox/apoptotic, and synaptic-downshift programs (`Rab7:F002-F006`). Those are exactly the kinds of broad nuclear compensation that the assay can detect, but RAB7 controls late endosome and lysosome traffic, whereas RAB28 is farnesylated, BBSome/PDE6D-linked, and ciliary/photoreceptor-skewed.

# Target-specific prediction

## Rab28

I predict `0` DEGs.

The zero/nonzero decision is driven primarily by within-dataset evidence. The closest assayed ciliary comparators in the exact focal class were zero (`Bbs5`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Cep290`, `Rpgr`, `Rpgrip1l`, `Iqcb1`, `Arl2bp`) or singleton self-only (`Ttc8`, `Arl3`). The profile reviewer confirmed that this hand-nominated neighborhood lacked an FDR-level expression module in `151 TH Prkcd Grin2c Glut`. The ciliary same-experiment corpus turns those matched nulls into a repeated pathway observation rather than an isolated table lookup.

External biology points in the same direction for this endpoint. Known RAB28 phenotypes are most interpretable in photoreceptor outer-segment shedding, RPE phagocytosis, sensory-cilium extracellular-vesicle control, and ciliary cargo localization. Those processes are either absent from NeuN-enriched thalamic glutamatergic nuclei, protein/localization-level rather than steady-state nuclear RNA endpoints, or likely to need retinal, glial/RPE, evoked-signaling, or long-latency structural readouts. I did not round the prediction up to one for a presumed self-transcript hit because the experiment's ciliary singletons were the exception, not the rule, and the dataset portrait explicitly cautions that measured target-RNA change is not a reliable guide to downstream perturbation strength.

# Limits of the reasoning

- `Rab28` itself has no same-experiment DE signature, no focal DEG count, and no released Distributed Agents corpus target card in this run. The prediction is therefore transfer from analogs.
- The most direct RAB28 trafficking partners, including `Pde6d`, `Arl13b`, `Unc119`, `Unc119b`, `Rp2`, `Bbs1`, `Bbs2`, `Bbs4`, `Bbs7`, and `Bbs9`, were not in the training-count table, so the measured analog set is close by organelle and pathway, not a complete Rab28 biochemical module.
- Many ciliary phenotypes are structural or signaling phenotypes; this assay measured basal nuclear RNA in recovered postnatal neurons and did not image cilia, measure receptor localization, measure protein depletion, measure cAMP, or challenge Hedgehog/ciliary GPCR signaling.
- Photoreceptor outer segments and RPE phagocytosis are the best-supported mammalian RAB28 phenotypes, but retina, RPE, olfactory bulb, hindbrain, and non-neuronal lineages were outside or underrepresented in this experiment.
- A zero FDR prediction is assay-specific. It should not be read as a claim that Rab28 has no biological role in thalamic neurons or that the CRISPR guides would fail.
