# Prediction trace for Thoc2 in `151 TH Prkcd Grin2c Glut`

## Question and ambiguity resolution

The held-out readout to predict is the number of genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after a held-out CRISPR perturbation in `151 TH Prkcd Grin2c Glut` nuclei. The requested manifest contains one target, `Thoc2`; I therefore made one target-specific prediction and preserved that order in `answer.txt`.

I treated the supplied focal-cell DEG counts and the supplied differential-expression parquet as the quantitative evidence. Germline mouse phenotypes, human genetics, and cell-culture studies were used only to decide which held-in perturbations are mechanistically appropriate analogs, because their dose, developmental timing, and cell populations do not match this sparse postnatal AAV-PHP.eB CRISPR screen.

## Sources used

- Input training DEG counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Held-out target manifest: `[local file: 238_Thoc2.csv]`.
- Same-experiment mechanistic summaries from the Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`.
- PubMed literature on THO/TREX:
  - Strasser et al., 2002, Nature, DOI `10.1038/nature746`, PMID `11979277`: defined the conserved TREX complex coupling transcription and mRNA export.
  - Guria et al., 2011, RNA, DOI `10.1261/rna.2607011`, PMID `21525145`: described mammalian/drosophila THO/TREX composition including THOC1, THOC2, THOC5, THOC6, THOC7, THOC3, UAP56/DDX39B, and ALY/THOC4.
  - Di Gregorio et al., 2013, Journal of Medical Genetics, DOI `10.1136/jmedgenet-2013-101542`, PMID `23749989`: connected reduced THOC2 with neurodevelopmental phenotypes and showed neuronal effects in worm, rat hippocampal neuron, and neural stem-cell models.
  - Kumar et al., 2015, American Journal of Human Genetics, DOI `10.1016/j.ajhg.2015.05.021`, PMID `26166480`: showed that THOC2 variants cause X-linked intellectual disability and can reduce THOC2 and partner stability.
  - Kumar et al., 2020, Frontiers in Molecular Neuroscience, DOI `10.3389/fnmol.2020.00012`, PMID `32116545`: expanded THOC2 NDD presentations and reported that pathogenic THOC2 variants can destabilize other TREX/THO subunits.
  - Bhattacharjee et al., 2024, Nature Communications, DOI `10.1038/s41467-024-45121-5`, PMID `38331934`: modeled a hypomorphic patient-like Thoc2 deletion in mouse and connected compromised THOC2/TREX function with R-loops, DNA damage, cell death, and adverse neurodevelopment.

## Computation over the training data

I first read the requested-target CSV and found a single held-out perturbation, `Thoc2`.

The focal training endpoint table contains 1,674 held-in perturbations. In `151 TH Prkcd Grin2c Glut`, 469 of them have at least one DEG, the median is 0, the mean is 14.05, and the largest focal responses are `Uba5` 2,677, `Tpr` 1,768, `Sin3a` 1,433, `Rnpc3` 868, `Zbtb7a` 841, `U2af2` 828, `Psmb4` 742, `Hnrnpu` 733, `Yy1` 720, and `Elp1` 645. The direct THO-complex analog `Thoc1` is also a substantial responder with 303 DEGs.

The all-cell parquet has 616,253,184 rows. Row-group statistics put the focal group in row groups 546-580; reading only `151 TH Prkcd Grin2c Glut` gives 28,891,566 rows, i.e. 1,674 targets by 17,259 measured genes. For the focal comparison I predicate-filtered to the biologically nominated targets:

```python
filter = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(targets)
)
columns = ["names", "gene_target", "logfoldchanges", "pvals_adj",
           "n_pert_matched", "n_ctrl_matched"]
```

The relevant focal-cell counts and sign-concordant overlaps with the 303 `Thoc1` DEGs were:

| training target | focal `n_degs` | role in reasoning | overlap with `Thoc1` FDR genes |
|---|---:|---|---:|
| `Thoc1` | 303 | direct same-THO-subcomplex anchor | 303 / 303 by definition; 233 up, 70 down |
| `Ddx39b` | 0 | TREX/UAP56 helicase, not a THO core subunit; a same-pathway focal-null counterexample | 0 |
| `Tpr` | 1,768 | nuclear-pore/export-adjacent broad upper bound | 114 shared, 103 same-direction |
| `Rnpc3` | 868 | minor-spliceosome RNA-processing state, adjacent rather than same complex | 115 shared, 110 same-direction |
| `U2af2` | 828 | major-spliceosome factor, adjacent | 75 shared, 66 same-direction |
| `Cdc40` | 624 | spliceosome factor, adjacent | 60 shared, 48 same-direction |
| `Hnrnpu` | 733 | hnRNP/RNA-processing factor, adjacent | 78 shared, 64 same-direction |
| `Prpf6` | 454 | spliceosome factor, adjacent | 49 shared, 45 same-direction |
| `Snrnp70` | 213 | U1 snRNP factor, adjacent and closest in size to `Thoc1` | 62 shared, 59 same-direction |
| `Sin3a` | 1,433 | chromatin regulator with an RNA-processing arm, but not a direct THO analog | 69 shared, 50 same-direction |
| `Setx` | 0 | R-loop-resolution target; counterexample for a generic R-loop signature | 0 |
| `Xpo7` | 0 | nuclear-export-adjacent but mechanistically distant counterexample | 0 |
| `Ranbp2` | 0 | nuclear-pore transport counterexample in this focal group | 0 |

The strongest `Thoc1` rows by FDR in the focal cell group include `Sart1`, `Snhg11`, `Anxa6`, `Dgkz`, `Gtf2i`, `Noc2l`, `Brsk1`, `Kif1a`, `Map7d1`, `Sf3b2`, `Srrm2`, and `Rsrp1`, a mixture of RNA-processing, chromatin/transcriptional, and neuronal remodeling genes. The `Thoc1` perturbation did not measurably induce the other measured THO/export transcripts (`Thoc2`, `Thoc3`, `Thoc5`, `Thoc6`, `Thoc7`, `Alyref`, `Ddx39b`, `Nxf1`) in this focal group, so the observed 303-DEG response is not simply autoregulatory THO-subunit mRNA compensation.

## Same-experiment corpus evidence

The Distributed Agents corpus has no direct `Thoc2` node, as expected for a completely held-out target. It does have high-confidence `Thoc1` evidence from the same Perturb-seq data:

- `Thoc1:F001` reports that acute `Thoc1` loss produced a sharply selective neuronal response: 1,331 of 1,353 FDR-significant rows across the assayed data came from only four cell groups, one of which was `151 TH Prkcd Grin2c Glut`.
- `Thoc1:F002` describes the major `Thoc1` responders as a THO/TREX-compatible RNA-biogenesis program, inducing genes such as `Sart1`, `Sf3a3`, `Dhx38`, `Exosc10`, and `Ncbp1`, while repeatedly repressing RNA-export or spliceosome genes such as `Nxf1`, `Rnpc3`, `Snrnp70`, `Srrm2`, and `Ddx17`.
- `Thoc1:F005` reports that the `Thoc1` neuronal signature lacked overt p53/apoptosis, DNA-damage, unfolded-protein-response, or integrated-stress signatures at FDR < 0.10, making the postnatal neuronal state different from stronger embryonic or dividing-cell THO/TREX disruption.
- `Thoc1:F006` and the high-confidence synthesized claim `claim:7e7c77ce9c2e84d3a5d6` connect `Thoc1` to `Ddx39b` most strongly in `191 MB P MY GABA`; the same exact TREX accessory `Ddx39b` was flat in `066`, `110`, `151`, and `155`.

That last point was important for the target-specific call: the corpus argues for a real TREX/splicing/nuclear-export state, but it also says that one cannot transfer the `Thoc1` count wholesale to every associated export factor. `Ddx39b` is an accessory helicase with possible buffering by `Ddx39a`/AREX; `Thoc2`, in contrast, is a core THO subunit with no close paralog in the library, so I treated `Ddx39b` as a counterexample rather than as the main quantitative anchor.

The corpus also places `Rnpc3`, `Prpf6`, `U2af2`, `Snrnp70`, `Cdc40`, and `Hnrnpu` in a recurrent RNA-splicing/RNA-processing response in midbrain/thalamic groups. Those profiles give positive evidence that perturbing RNA biogenesis is visible in the focal cell group and that `Thoc1`'s 303 DEGs are not an isolated outlier; they are less direct than `Thoc1` because they hit spliceosome or hnRNP biology rather than the THO subcomplex itself. `Tpr` is even broader and therefore mainly an upper-bound nuclear-export control, not an estimate of the expected THOC2 count.

## Thoc2-specific biological rationale

`Thoc2` encodes the largest subunit of the THO subcomplex within TREX. The best measured in-dataset proxy is therefore `Thoc1`, not generic RNA-binding proteins or unrelated nuclear transporters. Mammalian TREX includes THOC1/2/5/6/7, THOC3, UAP56/DDX39B, and ALY/THOC4; THOC2 variants in human neurodevelopmental disease reduce THOC2 stability and can destabilize multiple partner THO proteins. A patient-like hypomorphic `Thoc2` allele in mouse perturbs brain development, consistent with neuronal sensitivity to partial THOC2/TREX loss.

The predicted response should be nonzero because:

- the focal cell group was permissive for a core THO perturbation: `Thoc1` gave 303 DEGs with many RNA-biogenesis markers;
- the `Thoc1` state has substantial same-direction overlap with focal spliceosome/RNA-processing perturbations, especially `Rnpc3` and `Snrnp70`;
- `Thoc2` is a core THO/TREX component and NDD gene, so a silent `Setx`/`Xpo7`/`Ranbp2`-like call would ignore the direct complex anchor.

The count should not be in the thousand-gene `Tpr`/`Rnpc3`/`Sin3a` range because:

- `Thoc1` itself was intermediate, not broad, at 303 DEGs in this focal cell group;
- exact TREX-associated `Ddx39b` was focal-null despite producing a small concordant TREX/export-like state in another cell group, so the pathway has target- and cell-context-specific buffering;
- this experiment perturbs postmitotic neurons mosaically and captures survivor nuclei after modest average mRNA knockdown, whereas the strongest published THOC2 phenotypes involve germline or hypomorphic developmental exposure.

Balancing the direct `Thoc1` anchor against the focal-null `Ddx39b` counterexample, I predicted a `Thoc2` response just below `Thoc1`: 287 DEGs.

## Limits and extrapolation

The key limitation is that no other core THO-subcomplex gene besides `Thoc1` was a held-in focal perturbation: `Thoc3`, `Thoc5`, `Thoc6`, and `Thoc7` were not available as training targets, and neither `Alyref` nor `Nxf1` was targeted. Thus the prediction is mostly a one-anchor transfer from `Thoc1` to `Thoc2`, moderated by less direct spliceosome/export comparisons.

The differential-expression readout is whole-gene nuclear RNA abundance. It cannot directly measure mRNA-export flux, RNA localization, R-loops, or splice isoforms, and the average guide effect in this screen is partial. Strong THOC2 developmental models and R-loop/DNA-damage papers therefore support the nonzero call but are imperfect evidence for the exact DEG count in P16-edited juvenile postmitotic thalamic neurons.
