# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The held-out target manifest contains one perturbation, `Ndufs1`. I interpreted the requested endpoint as the exact focal-cell count used in the training CSV: for a gene knockout, count every measured gene in `151 TH Prkcd Grin2c Glut` whose Scanpy Wilcoxon `pvals_adj` is below 0.05. The perturbed target transcript itself is included in that count if it passes FDR. The held-out `Ndufs1` differential-expression rows and count were not available, so I transferred from non-held-out perturbations with special emphasis on Complex-I subunits and assembly factors.

## Sources used

- Input count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 146_Ndufs1.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
- Run-local Distributed Agents profile comparison over 39 respiratory-chain and mitochondrial perturbations, saved as `artifacts/respiratory_chain_profile_compare.json` with inspection table `artifacts/respiratory_chain_profile_inspect.json`.
- External biology:
  - MitoCarta3.0, the Rath et al. 2021 mitochondrial proteome and pathway annotation resource, DOI `10.1093/nar/gkaa1011`, PMID `33174596`.
  - Pagniez-Mammeri et al. 2011, review of nuclear structural Complex-I disease genes, DOI `10.1016/j.ymgme.2011.11.188`, PMID `22142868`.
  - Martin et al. 2005, NDUFS1-associated Leigh syndrome with muscle Complex-I deficiency, DOI `10.1001/archneur.62.4.659`, PMID `15824269`.
  - Alkhaldi and Vik 2022, modeling of pathogenic NDUFS1/NDUFS2/NDUFS8/NDUFV1 peripheral-arm mutations, DOI `10.1016/j.mito.2022.11.007`, PMID `36462614`.
  - Internal Distributed Agents corpus references for `Ndufs4`, including Kahlhoefer, Gansen and Zickermann 2021 on NDUFS4 and the Complex-I matrix arm, DOI `10.3390/life11050455`, and Yin et al. 2024 on Ndufs4-/- Complex-I assembly, DOI `10.1038/s44318-023-00001-4`.

The same-experiment corpus had no direct `Ndufs1` node, so I used it through neighboring represented targets, especially `Ndufs4` and `Ndufs2`.

## Computations on the supplied data

1. Read the manifest and confirmed that `Ndufs1` was the only held-out row.
2. Loaded the focal count CSV. It contains 1,674 training perturbations; the distribution is strongly zero-inflated in this focal cell group: median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`, 95th percentile `= 18`, and maximum `= 2677`.
3. Queried the parquet only for `group_name == "151 TH Prkcd Grin2c Glut"` and a respiratory-chain panel of `Nduf*`, `Ndufaf*`, `Cox*`, `Uqcr*`, `Sdha`, `Coa8`, `Lrpprc`, `Timmdc1`, `Opa1`, and `Elp1`. I recomputed `sum(pvals_adj < 0.05)` for these rows and confirmed the result matched the training-count CSV.
4. Ran a Distributed Agents `profile_compare` over 39 respiratory-chain or mitochondrial profiles in the same focal context with `logfoldchanges` as the signed vector and `pvals_adj < 0.05` as the activity threshold. No selected profile was missing. The activity states were 23/39 with no FDR genes, 15/39 with 1-9 FDR genes, and only `Opa1` in the 10-49 bin.
5. Checked sentinel genes for a mitochondrial integrated-stress response: `Asns`, `Ddit3`, `Chac1`, `Slc7a5`, `Shmt2`, `Herpud1`, `Atf4`, selected chaperones, `mt-Co2`, and `mt-Cytb`.

## Within-dataset analogs

In `151 TH Prkcd Grin2c Glut`, the represented Complex-I family was nearly null:

| training target | focal `n_degs` | relevant pattern |
|---|---:|---|
| `Ndufs2` | 1 | The only FDR hit was `Ndufs2` itself, logFC -0.728, FDR `8.26e-12`. No downstream FDR genes. |
| `Ndufs8` | 1 | The only FDR hit was `Ndufs8` itself, logFC -0.650, FDR `3.06e-08`. No downstream FDR genes. |
| `Ndufs4` | 0 | Self logFC was -0.623 but not FDR significant; no downstream FDR genes. The corpus reports no FDR<0.10 downstream genes for `Ndufs4` in any of 20 recovered neuronal groups. |
| `Ndufs7` | 0 | No focal FDR genes. |
| `Ndufv1` | 0 | Same N-module neighborhood as `Ndufs1`; no focal FDR genes. |
| `Ndufv2` | 1 | Singleton `Cdc40`, not the target transcript and not recurrent in Complex-I comparators. |
| `Ndufa10` | 1 | Only its own transcript, logFC -0.650, FDR `4.84e-07`. |
| `Ndufa12` | 0 | No focal FDR genes; proximal to the NDUFS4/NDUFAF2 assembly branch and still silent. |
| `Ndufb10` | 1 | Only its own transcript, logFC -0.843, FDR `6.79e-19`. |
| `Ndufb11` | 1 | Only its own transcript, logFC -0.563, FDR 0.0207. |
| `Ndufaf2`, `Ndufaf4`, `Ndufaf5` | 0, 0, 0 | Assembly-factor perturbations did not produce focal FDR genes. |
| `Timmdc1` | 0 | A Complex-I assembly target with no focal FDR genes. |

Across all 23 represented `Nduf*` targets in the focal count table, no target produced more than one DEG. There were 11 total FDR hits: 10 were self-transcript decreases, and the only non-self singleton was `Cdc40` under `Ndufv2`. Adding `Ndufaf2`, `Ndufaf4`, `Ndufaf5`, and `Timmdc1` contributed four more zeros. This is the strongest numerical prior for `Ndufs1`.

The same-experiment corpus supports the same calibration outside the single focal cell group. Its high-confidence Complex-I claim states that represented nuclear-encoded Complex-I subunit and assembly-factor perturbations are broadly buffered at the postnatal neuronal nuclear-transcriptome level. The resolved `Ndufs4` evidence counted 21 non-`Ndufs4` Complex-I subunit or assembly targets in `Ndufs4`-matched groups and found only 16 downstream FDR<0.10 genes in 419 target-by-cell tests; expected ATF4 or mitochondrial-stress marker rows were 0/3352 at FDR<0.10.

## Counterexamples and stress-positive controls

The near-null Complex-I behavior is not because the dataset cannot detect any mitochondrial stress state. In the same focal cell group:

- `Opa1` had 37 DEGs. It induced `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Slc7a5`, `Herpud1`, and aminoacyl-tRNA synthetases, and decreased `mt-Co2`.
- `Elp1` had 645 DEGs and strongly induced ISR genes such as `Asns`, `Atf4`, `Chac1`, `Ddit3`, `Herpud1`, `Shmt2`, and `Slc7a5`.

By contrast, `Asns`, `Chac1`, `Ddit3`, `Herpud1`, `Slc7a5`, `Shmt2`, `mt-Co2`, and `mt-Cytb` all had FDR 1.0 under the focal `Ndufs2`, `Ndufs4`, `Ndufs8`, `Ndufv1`, and `Ndufv2` perturbations. The correct comparison for `Ndufs1` is therefore not "any mitochondrial lesion" but specifically this acutely buffered nuclear Complex-I class.

## Target-specific rationale

### `Ndufs1`

`Ndufs1` encodes a nuclear, mitochondrial Complex-I structural subunit. MitoCarta3.0 annotates NDUFS1 within the respiratory-chain Complex-I pathway, and external genetics make it clear that sufficiently strong NDUFS1 loss is pathogenic: Pagniez-Mammeri et al. review NDUFS1, NDUFS2, NDUFV1, and NDUFS4 as nuclear structural-gene hotspots for isolated Complex-I deficiency, while Martin et al. report Leigh syndrome with muscle Complex-I deficiency from a homozygous `NDUFS1` mutation. Alkhaldi and Vik also note that disease substitutions in NDUFS1, NDUFS2, NDUFS8, and NDUFV1 often lie at peripheral-arm subunit interfaces and can reduce enzyme activity or disrupt assembly.

Those facts make `Ndufs2`, `Ndufs8`, `Ndufv1`, and `Ndufv2` the most direct training analogs, with `Ndufs4`, `Ndufs7`, the `Ndufa*` and `Ndufb*` subunits, the `Ndufaf*` assembly factors, and `Timmdc1` as broader Complex-I counterchecks. In the focal cell group those analogs did not show a downstream nuclear OXPHOS, ATF4/ISR, redox, or mitophagy program. The only repeatedly observed effect was on-target transcript loss in high-expression structural subunits.

I therefore predict a minimal nonzero count, `1`. The held-out `Ndufs1` perturbation is close enough to `Ndufs2` and `Ndufs8` that its own transcript has a reasonable chance to cross FDR, but the family evidence argues against any additional downstream genes in this focal cell group. Numerically, this is taking the core structural-subunit analogs with counts 0-1 as the operative range and choosing the singleton self-hit outcome rather than the all-zero outcome.

## Limits

- `Ndufs1` itself had no held-out profile in the input and no direct node in the Distributed Agents corpus, so this is an extrapolation from other Complex-I subunits rather than a direct signature neighbor.
- A prediction of `1` depends on the `Ndufs1` gRNAs measurably lowering `Ndufs1` RNA in this exact cell group. Several real Complex-I targets had self logFC values near -0.3 to -0.6 that still did not pass FDR, so failure of the self hit would make the realized count `0`.
- The training data measure nuclear RNA in recovered NeuN-positive nuclei. They do not measure DNA editing, NDUFS1 protein, Complex-I assembly, NADH oxidation, oxygen consumption, ROS, viability, or loss of cells before harvest. A transcriptional null in this assay must not be read as evidence that Complex-I biology is unperturbed.
- `Opa1` and `Elp1` prove that the assay can detect a mitochondrial or amino-acid stress program, but neither is a same-complex comparator. They only bound the interpretation of the Complex-I nulls.
