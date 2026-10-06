# Held-out DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested held-out perturbation manifest contained one target:

| target_name |
| --- |
| Rara |

The value to predict is the integer number of genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` row-space of the Perturb-seq differential-expression result after acute AAV CRISPR loss of the mouse target. I treated `0` as an explicit prediction that no measured feature will pass the experiment's Wilcoxon/BH threshold; I did not interpret it as absence of all retinoic-acid biology.

The held-out target `Rara` was absent from both supplied training inputs, so its own DEG count and its own signature could not be queried. All quantitative comparisons below therefore use assayed neighboring perturbations in the same cell group.

## Sources used

- Training endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 194_Rara.csv]`.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents runtime profile comparison over the focal group, with `logfoldchanges` as the signed profile value and `pvals_adj < 0.05` as the activity threshold.
- External literature from PubMed for retinoic-acid receptor mechanism and RARalpha neuronal function:
  - Chambon 1996, PMID 8801176.
  - Kurokawa et al. 1995, DOI 10.1038/377451a0.
  - le Maire and Bourguet 2014, DOI 10.1007/978-94-017-9050-5_3.
  - Pohl and Tomlinson 2020, DOI 10.1016/bs.mie.2020.03.008.
  - Maghsoodi et al. 2008, DOI 10.1073/pnas.0804801105.
  - Soden and Chen 2010, DOI 10.1523/JNEUROSCI.3660-10.2010.
  - Sarti et al. 2013, DOI 10.1523/JNEUROSCI.1710-13.2013.
  - Arendt et al. 2015, DOI 10.1073/pnas.1510239112.
  - Suzuki et al. 2021, DOI 10.1016/j.celrep.2021.109918.
  - Duester 2023, DOI 10.1016/j.yfrne.2023.101099.
  - Koshy et al. 2022, DOI 10.26508/lsa.202201627.

## Computational evidence

I first verified that `194_Rara.csv` has exactly one data row and that `Rara` was not present as a `gene_target` in the focal slice of the parquet. The focal slice has 28,891,566 rows over 1,674 assayed training perturbations and 17,259 measured genes per perturbation.

I then read the training DEG-count CSV and extracted counts for the mechanistically nearest assayed receptors and cofactors:

| training perturbation | relationship to `Rara` | observed `n_degs` |
| --- | --- | ---: |
| `Rarb` | RAR paralog; binds RAREs with RXR | 0 |
| `Rarg` | RAR paralog; binds RAREs with RXR | 0 |
| `Rxra` | canonical RAR heterodimer partner | 0 |
| `Rxrb` | canonical RAR heterodimer partner | 0 |
| `Rxrg` | canonical RAR heterodimer partner | 0 |
| `Ppara` | RXR-partner nuclear receptor | 0 |
| `Ppard` | RXR-partner nuclear receptor | 0 |
| `Pparg` | RXR-partner nuclear receptor | 0 |
| `Vdr` | RXR-partner nuclear receptor | 0 |
| `Nr1h2` | RXR-partner LXR nuclear receptor | 0 |
| `Nr1h4` | RXR-partner FXR nuclear receptor | 0 |
| `Nr1i2` | RXR-partner xenobiotic receptor | 0 |
| `Nr1i3` | RXR-partner xenobiotic receptor | 0 |
| `Thra` | RXR-partner thyroid receptor; weak positive control for this axis | 3 |
| `Thrb` | RXR-partner thyroid receptor | 0 |
| `Rora` | orphan nuclear receptor, not a RAR paralog; broad counterexample | 278 |
| `Ncoa1` | nuclear-receptor coactivator | 0 |
| `Ncoa3` | nuclear-receptor coactivator | 0 |
| `Ep300` | histone acetyltransferase recruited by many TFs | 0 |
| `Crebbp` | paralog of `Ep300`; weak broad coactivator effect | 8 |

To check whether there was a subthreshold retinoid/RXR signature rather than only a zero count, I used `profile_compare` on the full log-fold-change profiles for 17 retinoid/RXR/partner nodes in the exact focal context:

```text
context: group_name == "151 TH Prkcd Grin2c Glut"
entity_column: gene_target
feature_column: names
value_column: logfoldchanges
significance_column: pvals_adj
significance_threshold: 0.05
nodes: Rarb, Rarg, Rxra, Rxrb, Rxrg, Ppara, Ppard, Pparg, Vdr,
       Thra, Thrb, Nr1h2, Nr1h4, Nr1i2, Nr1i3, Rora, Gpx4
```

In that profile comparison, the five direct RAR/RXR analogs `Rarb`, `Rarg`, `Rxra`, `Rxrb`, and `Rxrg` each had `0` significant positive and `0` significant negative features among 17,259 genes. Their strongest apparent log-fold changes had `pvals_adj = 1.0`, and their top 200 signed tails overlapped only weakly with other nuclear-receptor tails: for the five direct analogs, positive top-tail overlap to peers was usually about 0.07-0.08 and negative top-tail overlap about 0.12-0.15. That supports the interpretation that the zero DEG counts are genuine near-null signatures in this cell group rather than five coordinated programs just under threshold.

I also inspected the retinoid-receptor genes themselves inside the focal DE slice. Perturbing `Rarb`, `Rarg`, `Rxra`, `Rxrb`, or `Rxrg` did not produce a significant change in any of `Rara`, `Rarb`, `Rarg`, `Rxra`, `Rxrb`, or `Rxrg`; every adjusted p-value in that 5 x 6 table was exactly `1.0`. This matters because it argues against an obvious compensatory receptor cross-induction being the dominant measured output of this module.

The Distributed Agents same-experiment corpus independently points in the same direction. Candidate expansion from `Rarb`/`Rarg`/`Rxra`/`Rxrb`/`Rxrg` returned a connected nuclear-receptor neighborhood including PPAR, LXR, VDR, thyroid, and xenobiotic receptors. The induced graph had all 17 targets represented in the corpus, and key RXR findings summarized the assayed family as flat or nonconvergent:

- `Rxra:F002`: `Rxra` was "uncoupled from measured RXR paralogs and canonical RXR partner receptors"; it explicitly named `Rarb`, `Rarg`, `Rxrb`, `Rxrg`, PPARs, LXRs, thyroid receptors, and `Vdr` as comparators.
- `Rxrb:F003`: RXR-family and heterodimer-pathway perturbations did not phenocopy `Rxrb`; `Thra`, not `Rxrb`, was the only comparator with a detectable Hr-containing thyroid-like signal in `151 TH Prkcd Grin2c Glut`.
- `Rxrg:F002`: the obvious retinoid/RXR relatives mostly failed to yield a coherent single-gene transcriptional phenocopy after individual loss.
- Higher-order corpus claim `claim:1352cb7a13bac707d254`: represented retinoid/RAR/RXR and lipid nuclear-receptor single-gene perturbations did not produce a coherent shared acute neuronal transcriptional module in this assay. The claim explicitly notes that `Rara` itself was not tested.

## Target-specific reasoning

### `Rara`

`Rara` encodes retinoic acid receptor alpha, a ligand-regulated nuclear receptor. Canonically, RAR proteins heterodimerize with RXR proteins on retinoic-acid response elements; unliganded complexes recruit NCOR/SMRT-type corepressors and histone deacetylases, and retinoic-acid binding promotes exchange for coactivators and transcriptional activation. That basic mechanism is well established for RAR/RXR nuclear receptors (Chambon 1996; Kurokawa et al. 1995; le Maire and Bourguet 2014; Pohl and Tomlinson 2020). RARalpha also has neuronal literature, especially in hippocampal homeostatic synaptic plasticity and retinoic-acid-dependent local translation/synaptic scaling (Maghsoodi et al. 2008; Soden and Chen 2010; Sarti et al. 2013; Arendt et al. 2015; Suzuki et al. 2021), although the proposed non-genomic RARalpha mechanism has been questioned in review by Duester 2023.

Those mechanisms made `Rara` plausible a priori: it is not a housekeeping target, but it is a direct transcription factor and a retinoid receptor can regulate many genes when ligand and cellular context are appropriate. The experiment-matched evidence, however, pushed the prediction to zero:

- The closest assayed RAR paralogs, `Rarb` and `Rarg`, were both `0` DEG perturbations in `151 TH Prkcd Grin2c Glut`.
- All three measured RXR heterodimer partners, `Rxra`, `Rxrb`, and `Rxrg`, were also `0`.
- Most RXR-sharing nuclear receptors that would reveal a basal RXR/nuclear-receptor vulnerability were also `0`: `Ppara`, `Ppard`, `Pparg`, `Vdr`, `Nr1h2`, `Nr1h4`, `Nr1i2`, `Nr1i3`, and `Thrb`.
- `Thra` gave only a very small response with 3 DEGs, while `Rora` produced 278 DEGs. I treated these as boundary observations: the assay can detect nuclear-receptor responses in this cell type, but the response is receptor- and pathway-specific rather than a generic property of all nuclear receptors.
- The nuclear-receptor coactivators represented in the training set were also mostly flat (`Ncoa1` 0, `Ncoa3` 0, `Ep300` 0; `Crebbp` only 8), which argues against a broad dependence on this coactivator class in the focal nuclei.
- The strongest external RARalpha neuronal phenotypes are synaptic and ligand/activity dependent. This snRNA-seq endpoint measures steady-state nuclear transcripts 3-4 weeks after a partial acute perturbation in sparse postmitotic thalamic neurons; it would not be expected to capture local dendritic translation directly.

The final point prediction is therefore:

| target_name | predicted_n_degs |
| --- | ---: |
| `Rara` | 0 |

## Limits

This is an extrapolation from RAR/RXR neighbors, not a profile match to `Rara` itself. `Rara` may be more highly expressed or less redundant than `Rarb`/`Rarg` in a subset of these thalamic cells; RAR isotypes can have both redundant and isotype-specific functions in other systems, including differentiating stem-cell models (Koshy et al. 2022) and epithelial contexts (Ganti et al. 2017, DOI 10.1073/pnas.1620697114). The supplied training data also lack perturbations for several direct corepressors and retinoid-metabolic genes such as `Ncor1`, `Ncor2`, `Hdac3`, `Aldh1a1-3`, `Cyp26a1`, `Crabp1`, and `Crabp2`, so the RA ligand-metabolism axis is incompletely sampled. Because the CRISPR perturbation is acute and only partially reduces target RNA on average, a small effect from `Rara` could fall below FDR despite real receptor biology. I chose `0` because all closest assay-matched paralog and heterodimer evidence was flat, not because RARalpha is biologically irrelevant.
