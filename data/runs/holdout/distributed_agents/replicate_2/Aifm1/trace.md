# Held-out DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The requested manifest contains one held-out target:

- `Aifm1`

I interpreted `n_degs` exactly as the training endpoint defines it: in `151 TH Prkcd Grin2c Glut`, count measured genes with `pvals_adj < 0.05` for the perturbation versus matched controls. I counted the perturbed target's own transcript if it passed the FDR threshold, because the supplied training counts do the same. A prediction of 0 means no measured gene is expected to pass this threshold in this assay; it is not a statement that the gene is unimportant.

The focal input parquet and the training-count CSV omit `Aifm1` completely, so I transferred information from mechanistically related non-held-out perturbations and from external AIFM1 biology.

## Sources

- Supplied `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: calibration of the focal endpoint over 1,674 non-held-out targets.
- Supplied `training_de_all_cell_groups.parquet`: focal-cell differential-expression rows for candidate mitochondrial, complex-I, apoptosis, and proteostasis comparators.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
  - `Aifm1` itself had no corpus claims or findings in this release.
  - `Opa1`, `Ndufs2`, `Uba5`, and `Ufc1` contexts were used to check same-experiment claims about mitochondrial-stress, complex-I, and UFMylation response classes.
- Distributed Agents runtime profile comparisons over the focal parquet rows:
  - `profiles/mitochondrial_anchor_neighbors.json`
  - `profiles/mitochondrial_compare.json`
  - `profiles/mitochondrial_cohort.json`
- External biology from PubMed and curated mitochondrial annotation:
  - Klein et al., 2002, Nature, DOI `10.1038/nature01034`: Harlequin mice downregulate AIF/Aifm1 by about 80% and develop oxidative-stress-associated degeneration of terminally differentiated cerebellar and retinal neurons.
  - Meyer et al., 2015, Cell Death & Disease, DOI `10.1038/cddis.2015.170`: AIF interacts with the MIA40/CHCHD4 oxidoreductase; AIF deficiency lowers MIA40 protein and respiratory subunits in Harlequin-derived tissues/cells.
  - Salscheider et al., 2022, EMBO Journal, DOI `10.15252/embj.2022110784`: AIFM1 and MIA40/CHCHD4 form a stable disulfide-relay complex needed for efficient NDUFS5 import and complex-I assembly.
  - Wang et al., 2021, Cell Metabolism, DOI `10.1016/j.cmet.2021.01.005`: the redox-sensitive AIFM1/CHCHD4 pathway imports C9orf72 and links that pathway to TIMMDC1 stabilization and complex-I assembly.
  - Wischhof et al., 2022, EBioMedicine, DOI `10.1016/j.ebiom.2022.104231`: review of AIFM1 as both an apoptosis factor and a mitochondrial OXPHOS-supporting factor in neurometabolic disease.
  - MitoCarta3.0 was used as a curated mitochondrial-protein/pathway annotation reference for separating respiratory-chain, import, cristae, and other organelle comparators.

## Computational checks

I first loaded the focal training counts. The endpoint is highly zero-inflated:

- 1,674 training perturbations.
- Median `n_degs`: 0.
- 75th percentile: 1.
- 90th percentile: 2.
- 95th percentile: 18.
- Maximum: `Uba5`, 2,677 DEGs.

I then extracted the `151 TH Prkcd Grin2c Glut` rows from the parquet for a candidate set spanning AIFM1-relevant lanes: complex I, complex-I assembly, mitochondrial import, cristae/mitochondrial dynamics, oxidative stress, BCL/caspase-adjacent survival, and the strongest UFMylation stress controls. For each target I recomputed:

```python
n_degs = (pvals_adj < 0.05).sum()
```

on the focal rows and verified that these counts matched the training-count CSV.

Key observed comparators in the focal cell group:

| comparator | observed n_degs | focal evidence |
|---|---:|---|
| `Opa1` | 37 | A real but modest mitochondrial inner-membrane/cristae response. Its strongest significant genes were ISR/amino-acid-stress markers and one-carbon/translation genes: `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Mthfd2`, `Slc7a5`; `Opa1` itself was down, log2FC -0.51, FDR 6.6e-4. |
| `Ndufs2` | 1 | Core complex-I subunit; only `Ndufs2` itself passed FDR in the focal group, log2FC -0.73, FDR 8.3e-12. |
| `Ndufa6` | 1 | Complex-I subunit; only `Ndufa6` itself passed, log2FC -0.43, FDR 1.4e-3. |
| `Ndufc2` | 1 | Complex-I subunit; only `Ndufc2` itself passed, log2FC -0.57, FDR 3.3e-5. |
| `Ndufv2` | 1 | Complex-I subunit; one off-target downstream call, `Cdc40`; the target RNA did not pass. |
| `Ndufv1` | 0 | Complex-I subunit; no FDR-significant downstream genes. |
| `Ndufs4` | 0 | Complex-I subunit; no FDR-significant downstream genes. |
| `Ndufa9` | 0 | Complex-I subunit; no FDR-significant downstream genes. |
| `Ndufaf2` | 0 | Complex-I assembly factor; no FDR-significant downstream genes. |
| `Ndufaf4` | 0 | Complex-I assembly factor; no FDR-significant downstream genes. |
| `Timmdc1` | 0 | Complex-I assembly/stability factor in the AIFM1/CHCHD4/C9orf72 neighborhood; no FDR-significant downstream genes. |
| `Tomm40` | 1 | Mitochondrial outer-membrane import pore; only `Tomm40` itself passed, log2FC -0.92, FDR 5.5e-7. |
| `Chchd2` | 1 | Mitochondrial intermembrane-space/cristae/Parkinson-related comparator; only `Chchd2` itself passed. |
| `Yme1l1` | 0 | Mitochondrial inner-membrane protease and OPA1-processing comparator; no FDR-significant downstream genes. |
| `Sod2` | 1 | Mitochondrial superoxide dismutase; only `Sod2` itself passed. |
| `Park7` | 1 | Mitochondrial/redox Parkinson-related comparator; only `Park7` itself passed. |
| `Bcl2` | 0 | Apoptosis regulator; no FDR-significant downstream genes. |
| `Xiap` | 0 | Apoptosis inhibitor; no FDR-significant downstream genes. |
| `Ufc1` | 572 | UFMylation E2 and a broad proteostasis/ER-stress state, useful as a positive stress control but not a mechanistic match to AIFM1. |
| `Uba5` | 2677 | UFMylation E1 and the strongest training perturbation in the focal group; again a positive stress control, not an AIFM1-like respiratory perturbation. |

The runtime comparison used these 20 targets, 200 signed tail genes per target, and the focal parquet log fold changes. The selected mitochondrial/apoptotic cohort was not a tight same-state module: mean positive-tail overlap coefficient across pairs was 0.07, and FDR-level significant-program overlaps were rare. That matters because it prevents a large response for `Uba5`/`Ufc1` from being transferred to every mitochondrial-stress gene. In the same comparison, `Opa1` had Pearson correlations around 0.64-0.69 to complex-I/import nodes, but these broad all-gene correlations came mostly from background ranking; the complex-I nodes did not share `Opa1`'s formal `Asns`/`Chac1`/`Ddit3`/aminoacyl-tRNA synthetase FDR program.

The Distributed Agents corpus independently supported this separation:

- `Opa1` was described as an anchor of an assay-detectable ATF4/ISR-like mitochondrial amino-acid stress program.
- `Ndufs2` was described as near-flat and non-convergent with 21 represented `Nduf`/`Ndufaf` complex-I comparators.
- A corpus claim over represented nuclear complex-I subunits and assembly factors stated that these perturbations are broadly buffered at the postnatal neuronal nuclear transcriptome level and do not produce a shared acute OXPHOS-stress module.
- A second corpus claim stated that `Opa1` crosses the mitochondrial-stress transcriptional threshold whereas represented mitochondrial comparators including `Ndufs2`, `Ndufv1`, `Sod2`, `Ndufa4`, `Coa8`, `Gfm2`, `Mff`, `Isca2`, and `Sucla2` do not.

## Target-specific reasoning

### Aifm1

`Aifm1` encodes mitochondrial apoptosis-inducing factor. Despite its name, the strongest steady-state mitochondrial role relevant here is survival/OXPHOS support: AIFM1 is an intermembrane-space flavoprotein that interacts with MIA40/CHCHD4, supports CHCHD4-dependent import of substrates including NDUFS5, and thereby promotes respiratory-chain, especially complex-I, assembly. Loss of AIFM1 also changes mitochondrial redox biology and can eventually produce neuronal degeneration in Harlequin mice.

The closest literal AIFM1 interactors were mostly absent from the training perturbation universe: `Chchd4`, `Ak2`, `Ndufs5`, and `C9orf72` were not training targets in the focal count table. I therefore treated the following as imperfect but informative analogs:

- `Timmdc1`, because C9orf72 imported through the AIFM1/CHCHD4 pathway stabilizes TIMMDC1 and complex-I assembly. `Timmdc1` had 0 DEGs in the focal group.
- `Ndufs2`, `Ndufa6`, `Ndufc2`, `Ndufv1`, `Ndufs4`, `Ndufa9`, `Ndufaf2`, and `Ndufaf4`, because AIFM1 deficiency ultimately impairs complex-I assembly/function. These were 0- or 1-DEG perturbations, with the 1-DEG cases usually reflecting only the target transcript itself.
- `Tomm40`, because it tests whether disturbing mitochondrial import machinery was broadly visible; it had 1 DEG, again its own transcript.
- `Opa1`, because it is the clearest same-assay example of a mitochondrial inner-membrane defect that did cross into an ATF4/ISR-like nuclear response. It had 37 DEGs, far below the broad proteostasis hits and biologically downstream of a cristae/fusion axis rather than the AIFM1-CHCHD4 disulfide relay.
- `Chchd2`, `Sod2`, `Park7`, `Bcl2`, `Xiap`, and `Yme1l1` as redox, cristae, Parkinson/mitochondrial, apoptotic, and OPA1-processing counterexamples. They were all flat except for occasional self-transcript calls.
- `Uba5` and `Ufc1` as stress positive controls in the same 151 thalamic population. Their huge counts show that this cell group can mount thousands of DE genes in this assay, but their ER/ribosome/UFMylation state is not the AIFM1 mechanism.

This points to a response just above zero rather than to an `Opa1`-scale count. The external AIFM1 literature argues that complete or chronic AIFM1 loss is biologically serious, so I did not call a hard 0. However, the same-experiment data say that sparse P16 CRISPR of respiratory-chain subunits and assembly factors is usually transcriptionally buffered by P37-P44, even when the target mRNA itself is measurably reduced. AIFM1 is upstream of complex-I assembly, not a direct UFMylation or proteasome stressor, and the AIFM1-specific readout could be further blunted if the most damaged edited cells are depleted before nuclear capture.

I therefore predict that `Aifm1` will look like the one-DEG complex-I/import comparators: most likely only `Aifm1` itself, or a single isolated stress gene, reaches FDR 0.05.

Final point estimate: **1 DEG**.

## Limits

- The actual `Aifm1` differential-expression signature is held out, so all signature comparisons are analogies.
- `Chchd4/Mia40`, `Ndufs5`, `Ak2`, and `C9orf72`, the most direct AIFM1 mitochondrial interactors identified in the literature, were not available as training perturbations in the focal count table.
- Most represented complex-I genes are structural subunits, while AIFM1 is an intermembrane-space oxidoreductase/import factor with apoptotic and redox roles; this makes the 0-1 DEG complex-I lane a conservative but imperfect lower analog.
- `Opa1` demonstrates that mitochondrial perturbations can produce an ISR-like nuclear response in this cell group, but it alters cristae dynamics more directly than AIFM1. Using `Opa1` would likely overestimate `Aifm1`.
- The endpoint is a Wilcoxon/FDR count among recovered nuclei after sparse AAV CRISPR. It does not measure editing rate, AIFM1 protein, CHCHD4 protein, respiratory-chain activity, ROS, cell loss before harvest, or caspase-independent apoptosis.
