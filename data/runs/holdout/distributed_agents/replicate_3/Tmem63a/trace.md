# Prediction trace

## Question and resolved ambiguities

The requested held-out perturbation list contained one target, `Tmem63a`. I interpreted the endpoint as the exact assay endpoint in the focal cell group, i.e. the number of measured genes with `pvals_adj < 0.05` for the `gene_target` in `151 TH Prkcd Grin2c Glut`, using the same Scanpy/Wilcoxon, Benjamini-Hochberg-corrected differential-expression table as the training perturbations.

I treated target-gene knockdown rows the same way the supplied training `n_degs` file does: the count is a thresholded property of all measured genes for that perturbation in the focal group, not a count of pathway genes or a germline disease severity measure. I did not treat a near-null transcriptional signature as failed editing, because the experiment is sparse postnatal CRISPR loss-of-function and the design does not directly report DNA indels or channel physiology.

## Sources used

- Input endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 non-held-out targets.
- Input DE table: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for direct focal signatures.
- Requested target list: `242_Tmem63a.csv`, which contained only `Tmem63a`; it was absent from both training input tables.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried for `Tmem63a`, `Tmem63b`, and `Tmem63c`.
- PubMed literature for TMEM63 family biology:
  - Zhao et al. 2016, Cell Biochem Funct, doi:10.1002/cbf.3185, PMID:27045885.
  - Murthy et al. 2018, eLife, doi:10.7554/eLife.41844, PMID:30382938.
  - Zheng et al. 2023, Neuron, doi:10.1016/j.neuron.2023.07.006, PMID:37543036.
  - Wu et al. 2022, J Biol Chem, doi:10.1016/j.jbc.2022.102781, PMID:36496074.
  - Vetro et al. 2023, Am J Hum Genet, doi:10.1016/j.ajhg.2023.06.008, PMID:37421948.
  - Li et al. 2024, Nat Cell Biol, doi:10.1038/s41556-024-01353-7, PMID:38388853.
  - Chen et al. 2024, J Clin Invest, doi:10.1172/JCI174508, PMID:38127458.

## Computation over the supplied DE data

I loaded the training counts and confirmed that the focal endpoint is zero-inflated: 1,205/1,674 training perturbations had `n_degs = 0`, 276 had `n_degs = 1`, and 469 had any nonzero focal response. The top of the training distribution was made up of broad housekeeping or nuclear-regulatory states such as `Uba5`, `Tpr`, `Sin3a`, spliceosome factors, proteasome factors, and chromatin regulators; that tail is not a good prior for a conditional mechanosensitive channel.

For the focal cell group, I counted FDR-significant rows and inspected the measured signatures for the two represented TMEM63 paralogs:

```python
import pyarrow.dataset as ds

dset = ds.dataset(
    "[local file: 260901_predict]"
    "holdout_task/Inputs/training_de_all_cell_groups.parquet",
    format="parquet",
)
focal = dset.to_table(
    columns=["names", "group_name", "gene_target", "logfoldchanges",
             "pvals_adj", "scores", "n_pert_matched", "n_ctrl_matched"],
    filter=ds.field("group_name") == "151 TH Prkcd Grin2c Glut",
).to_pandas()
```

This yielded 28,891,566 focal rows, 17,259 measured genes per perturbation, and 1,674 training targets. `Tmem63a` was not present as a perturbation; `Tmem63b` and `Tmem63c` were.

I then used the Distributed Agents runtime profile tools to compare the `Tmem63b` and `Tmem63c` focal log-fold-change profiles against all 1,674 eligible training targets and against each other. The direct focal comparison had high whole-vector Pearson/cosine values on raw log-fold-changes, but the shared signed extremes were tiny, with only 5/100 positive-tail and 4/100 negative-tail overlaps; the top extreme rows for both paralogs all had `pvals_adj = 1` except the edited `Tmem63b` self transcript. This made the whole-vector match a weak dropout/subthreshold similarity, not a robust shared downstream program.

The same-experiment Distributed Agents corpus gave the broader 22-cell-group check. It found no `Tmem63a` target node, but its curated TMEM63 paralog claim states that represented `Tmem63b` and `Tmem63c` loss produce non-interchangeable postnatal neuronal transcriptomic surfaces despite family relatedness. The resolved evidence for `Tmem63c:F002` reported that `Tmem63a` had zero represented perturbation rows, `Tmem63b` was the only measurable TMEM63-family comparator, the `Tmem63b`-versus-`Tmem63c` signed-score cosine across 22 matched groups was 0.00275, and same-direction robust overlap was 0.

## Target-specific reasoning

### Tmem63a

Relevant in-dataset analogs and counterexamples:

| training perturbation | focal `n_degs` | expression-pattern evidence | interpretation |
| --- | ---: | --- | --- |
| `Tmem63b` | 1 | 150 perturbed nuclei vs 23,679 controls in the focal group; the only `pvals_adj < 0.05` row was `Tmem63b` itself, log2FC -0.701 and FDR 4.16e-17. | Closest represented paralog with a strong target-transcript decrease in this cell group. It shows that a TMEM63-family channel perturbation can edit detectably without producing a multi-gene focal response. |
| `Tmem63c` | 0 | 243 perturbed nuclei vs 23,679 controls in the focal group; no measured gene passed FDR 0.05. The Distributed Agents corpus also reports 0 downstream FDR<0.10 genes for `Tmem63c` in all 22 measured cell groups. | Second represented TMEM63 paralog and the strongest null counterexample: family membership alone did not generate a sustained neuronal nuclear RNA response. |
| `Trpm3`, `Trpm7`, `Trpa1`, `Trpv1`, `Kcnn2`, `Kcnn3` | all 0 | These channel perturbations were focal training targets and none produced FDR-significant focal genes. | Less specific than `Tmem63b/c`, but they argue against assigning a broad response simply because the gene encodes an ion channel. |
| `Iqsec1`, `Acvr1`, `Kcnt2`, `Gsdme`, `Ccser1`; `Retreg1`, `Unc5d`, `Ankfy1`, `Zkscan16`, `Il17rd` | respectively 0, 0, 0, 0, 0; 1, 0, 0, 0, 0 | These were the nearest whole-profile training targets for focal `Tmem63b` or `Tmem63c` in raw log-fold-change space, but they are not TMEM63-family genes and were themselves null or near-null. | Their presence shows that nearest-neighbor structure around the paralogs is dominated by weak/null profiles; I did not use them as mechanistic positives. |

External function:

`Tmem63a`, `Tmem63b`, and `Tmem63c` belong to the animal OSCA/TMEM63 mechanosensitive channel family. Zhao et al. showed that mouse TMEM63A/B/C expression can confer hyperosmolarity-activated currents in HEK293 cells; Murthy et al. established OSCA/TMEM63 proteins as an evolutionarily conserved family of mechanically activated channels; and Zheng et al. structurally and functionally characterized TMEM63A/B/C as monomeric, small-conductance, high-threshold mechanosensitive channels. That places `Tmem63a` extremely close to the two in-dataset paralogs.

The key question was whether `Tmem63a` should be higher than those paralogs because of a `Tmem63a`-specific neuronal or organellar role. Li et al. found that mouse TMEM63A can mediate lysosomal mechanosensitivity in Neuro-2a cells, and Chen et al. showed a lamellar-body/surfactant phenotype in alveolar type 2 cells requiring TMEM63A/TMEM63B. Those are strong channel/organelle functions but are either in a cultured neuroblastoma system or in lung epithelial cells under mechanical stretch. The focal assay measured steady-state nuclear RNA in NeuN-enriched postnatal brain nuclei without a defined osmotic or mechanical challenge, and non-neuronal cells such as oligodendrocytes, lung epithelium, and macrophages are not the sampled population. Pu et al. linked Tmem63a to macrophage-associated inflammatory responses in injured dorsal-root-ganglion pain models, but the naive knockout had little basal pain phenotype and the Perturb-seq assay did not include peripheral nerve injury or macrophage infiltration. TMEM63B channelopathy literature likewise warns that missense gain/leak currents can be pathogenic without implying that acute postnatal loss-of-function creates a broad nuclear RNA program.

Within-dataset evidence therefore drove the zero/nonzero call: the two direct paralogs were 0 to 1 DEG in the same focal endpoint, `Tmem63b`'s lone significant gene was the knocked-down target transcript itself, `Tmem63c` was completely null, and broader channel perturbations were also null. External biology supported keeping the point estimate at the floor because TMEM63A's known effects are force/osmolarity/lysosomal channel events and cell-type- or challenge-dependent phenotypes, not constitutive transcriptional regulation. I predict no gene will cross FDR 0.05 for held-out `Tmem63a` in `151 TH Prkcd Grin2c Glut`.

Point prediction: `Tmem63a -> 0`.

## Limits of the reasoning

- `Tmem63a` itself was held out, and the Distributed Agents same-experiment corpus had no `Tmem63a` target node, so the prediction is an extrapolation from `Tmem63b`, `Tmem63c`, and general TMEM63 biology.
- TMEM63 family members are mechanistically related but not interchangeable. The same-experiment corpus explicitly found that represented `Tmem63b` and `Tmem63c` were nonconvergent across 22 groups, so the paralog comparison is a floor/scale calibration rather than proof that `Tmem63a` must be identical.
- The focal `Tmem63b`/`Tmem63c` raw log-fold-change vectors have weak tail overlap and many extreme nonsignificant sparse-gene rows. I used the observed focal `n_degs` and FDR-significant rows, not large FDR=1 log-fold-changes, for endpoint calibration.
- This assay is postnatal, mosaic, NeuN-enriched, and transcriptional. It could miss Tmem63a-dependent effects on acute channel currents, lysosomal mechanics, axons, myelin, peripheral sensory neurons, or injury/inflammatory states.
