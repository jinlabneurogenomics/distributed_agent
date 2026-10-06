# Tfap2a held-out DEG-count prediction

## Question and interpretation

The requested readout is the integer number of genes with `pvals_adj < 0.05` after CRISPR loss of `Tfap2a` in `151 TH Prkcd Grin2c Glut` nuclei. I treated `151` as the Allen class identifier and `TH` as thalamus, so the focal group is a thalamic glutamatergic neuronal class, not a tyrosine-hydroxylase or dopaminergic population. `Tfap2a` was completely held out, so I did not look for a hidden `Tfap2a` row and inferred from training perturbations plus TFAP2A biology.

There was exactly one requested target:

| target | final predicted `n_degs` |
|---|---:|
| `Tfap2a` | 0 |

## Sources used

- Training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, 1674 non-held-out perturbations.
- Training expression signatures: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for the mechanistic analog panel.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. `target_context("Tfap2a")` and `story_count(["Tfap2a"])` returned no held-out-gene findings or claims, so there was no direct internal semantic annotation for `Tfap2a`.
- Distributed Agents runtime profile comparison. I compared 26 observed training perturbations chosen from AP-2/neural-crest, AP-2/retinoic-acid/BMP, and thalamic/Wnt counterexample biology across the 17,259 measured focal-cell features.
- NCBI PubMed literature for TFAP2A/AP-2 alpha biology.

## Computations over the training data

The training counts in the focal class are zero-inflated: `1205/1674` training perturbations had `n_degs = 0`, only `469/1674` were nonzero, and only `43` had at least 100 DEGs. Thus a broad response needed target-specific support rather than a default transcription-factor prior.

I curated AP-2-relevant observed targets and extracted their focal rows from the Parquet:

```python
table = ds.dataset(parquet, format="parquet").to_table(
    columns=[
        "gene_target", "names", "logfoldchanges",
        "pvals_adj", "scores", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & pc.field("gene_target").isin(nodes)
    ),
)
n_degs = (rows_for_target.pvals_adj < 0.05).sum()
```

The Parquet-derived counts agreed with the supplied count CSV. For zero-count targets I inspected minimum adjusted p-values and the largest absolute log-fold-change rows; the very large `|logfoldchanges|` rows were all `q = 1` sparse-gene artifacts and were not treated as biological support.

Key task-matched analogs and counterexamples:

| role for `Tfap2a` | training perturbation(s) | observed focal `n_degs` | expression evidence in `151 TH Prkcd Grin2c Glut` |
|---|---|---:|---|
| Direct AP-2 craniofacial/neural-crest ALX effectors | `Alx1`, `Alx3`, `Alx4` | `0`, `0`, `0` | no FDR 0.05 genes; `Alx1` and `Alx3` had minimum `q = 1`, `Alx4` minimum `q = 0.488` |
| AP-2/DLX neural-crest branchial-arch effectors | `Dlx3`, `Dlx6` | `0`, `0` | no FDR 0.05 genes; minimum `q = 1` |
| AP-2-associated coactivator and crest/ectodermal markers | `Ep300`, `Snai2`, `Twist2`, `Msx2`, `Six3`, `Six5`, `Ednra`, `Kit` | all `0` | all absent from the FDR surface in the focal class |
| Retinoic-acid and BMP/TGF-beta pathways that intersect AP-2 patterning biology | `Rarb`, `Rarg`, `Rxra`, `Rxrb`, `Rxrg`, `Bmpr1a`, `Bmpr1b`, `Bmpr2`, `Smad1`, `Smad3`, `Smad4` | all `0`; `Smad2 = 1` | pathway perturbations were overwhelmingly flat in the focal class |
| Midbrain dopamine specification genes, a CNS developmental counterfactual rather than neural crest | `En1`, `Foxa2`, `Lmx1b`, `Otx2`, `Pitx3` | all `0` | no FDR-supported focal transcriptional state |
| Thalamic/Wnt broad-response boundaries | `Ctnnb1`, `Tcf7l2` | `383`, `106` | real responses: `Ctnnb1` had 100 up and 283 down significant genes; `Tcf7l2` had 39 up and 67 down |
| Weak nonzero TF/cofactor boundaries | `Zeb1`, `Creb1`, `Crebbp` | `15`, `10`, `8` | small signatures show weak TF responses are possible, but they are not AP-2-family or neural-crest effectors |

The runtime profile comparison reinforced the boundary. In a cohort containing `Alx1/3/4`, `Dlx3/6`, `Ep300`, `En1`, `Foxa2`, `Lmx1b`, `Otx2`, `Pitx3`, PAX and RA/BMP representatives, `Ctnnb1`, `Tcf7l2`, `Zeb1`, `Creb1`, and `Tfap4`, 22/26 nodes had no significant features. `Alx1`, `Dlx3`, and `Ep300` shared zero significant positive or negative features with the Wnt counterexamples, and the selected AP-2-neural-crest nodes shared zero significant features with each other because each was simply flat.

## Target-specific biological reasoning

`Tfap2a` encodes AP-2 alpha, a TFAP2 family DNA-binding transcription factor. The strongest mouse evidence places it in embryonic ectoderm and cranial neural crest: `Tfap2a` knockout mice die perinatally with cranial closure, craniofacial, skull, sensory-organ, and cranial-ganglion defects (Schorle et al., 1996, DOI `10.1038/381235a0`, PMID `8622765`), and later TFAP2A/TFAP2B neural-crest work showed that AP-2 paralogs regulate branchial arch patterning via homeobox factors including `Dlx` genes and regulate midfacial morphogenesis in part through `Alx1`, `Alx3`, and `Alx4` (Van Otterloo et al., 2018, DOI `10.1242/dev.157438`, PMID `29229773`; Nguyen et al., 2024, DOI `10.1242/dev.202095`, PMID `38063857`). Human PSC differentiation experiments likewise found TFAP2A important for neural-crest and cranial placode specification under controlled BMP/WNT/TGF-beta/FGF conditions (Tchieu et al., 2017, DOI `10.1016/j.stem.2017.08.015`, PMID `28886367`).

That biology argues for a developmental, ectodermal/neural-crest AP-2 module, not for a maintained postnatal thalamic glutamatergic maintenance program. The training data are consistent with the latter interpretation: the direct ALX and DLX effectors from AP-2 neural-crest papers, RA receptors, BMP receptors, and SMAD mediators all had zero or near-zero DEG counts in the focal thalamic nuclei. Even `Ep300`, an AP-2 cofactor in several non-neuronal transcriptional contexts, had `0` focal DEGs. This is the main within-dataset driver of the zero prediction.

I also checked whether known neuronal AP-2 uses should override the neural-crest argument. AP-2 alpha/beta are expressed in and can regulate embryonic dorsal spinal interneuron specification (Xu et al., 2016, DOI `10.1016/j.neuroscience.2016.10.055`, PMID `27984181`), and `Tfap2a/2b` act downstream of `Ptf1a` in retinal amacrine and horizontal cell differentiation (Jin et al., 2015, DOI `10.1186/s13041-015-0118-x`, PMID `25966682`). These are still embryonic spinal-cord/retinal fate programs rather than the assayed juvenile thalamic glutamatergic state, and the observed focal perturbations of broad CNS fate genes such as `Pax6`, `Otx2`, `Foxa2`, `Lmx1b`, `En1`, and `Pitx3` were all zero.

The strongest counterexamples were `Ctnnb1` and `Tcf7l2`: both are developmental/Wnt regulators but had large focal signatures (`383` and `106` DEGs). I treated them as boundaries, not analogs. `Tcf7l2` is much closer to thalamic identity/Wnt activity in this class than AP-2 alpha is, and profile inspection showed that the AP-2-neural-crest candidate signatures did not share their FDR-supported genes with `Ctnnb1` or `Tcf7l2`. `Zeb1`, `Creb1`, and `Crebbp` show that weak nonzero TF/cofactor effects can happen, but their counts were only `15`, `10`, and `8`, and they lack the ALX/DLX/AP-2 mechanistic match.

The final zero/nonzero decision was therefore:

- no observed `Tfap2a` or TFAP2 paralog training perturbation was available;
- the closest TFAP2A-regulated training targets in neural crest and AP-2 patterning biology were uniformly `0`;
- upstream RA/BMP/TGF-beta and midbrain/retinal developmental TF controls were also flat;
- the only broad developmental counterexamples were mechanistically different thalamic/Wnt regulators.

I assigned `Tfap2a = 0` rather than a weak nonzero count because the positive within-dataset analogs were absent and the postnatal focal cell group is displaced from the embryonic AP-2 alpha programs described above.

## Limits

This is still an extrapolation. The training set did not contain `Tfap2b`, `Tfap2c`, or a direct `Tfap2a` perturbation, and the Parquet has differential-expression statistics rather than baseline expression, open chromatin, or AP-2 occupancy in the focal thalamic cells. Mosaic AAV CRISPR at P16 could reveal a subtle AP-2 alpha target in a small subset of recovered nuclei that none of the analogs capture. Conversely, a true developmental requirement could be invisible in this assay because the perturbation is late, sparse, and survivor-conditioned. The prediction should therefore be read as an assay-calibrated FDR-count prediction for this postnatal thalamic snRNA-seq endpoint, not as a claim that `Tfap2a` is biologically unimportant.
