# Prediction trace

## Question and interpretation

The requested held-out target file contains one perturbation, `Dlx5`. I interpreted the endpoint as the integer number of genes with `pvals_adj < 0.05` in the supplied focal cell group, `151 TH Prkcd Grin2c Glut`, under the same Wilcoxon/BH pipeline used for the training targets.

`Dlx5` is completely held out: it is not in the training DEG-count CSV and not a `gene_target` in the differential-expression parquet. I therefore treated the measured focal signatures of related *training* perturbations as the calibrator and used Dlx biology only to decide which of those measured perturbations should or should not transfer.

## Sources used

- Held-out manifest: `057_Dlx5.csv`, one row, `Dlx5`.
- Training endpoint: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`; 1,674 training perturbations, 469 with a nonzero focal response, median `n_degs = 0`, maximum `n_degs = 2677`.
- Differential-expression parquet: `training_de_all_cell_groups.parquet`; for the focal group I filtered row groups 546-580 and inspected the `Dlx3`, `Dlx6`, `Arx`, `Nkx2-1`, `Isl1`, `Meis1`, `Meis2`, `Otx2`, `Pax6`, `Mef2c`, `Ctnnb1`, and `Tcf7l2` signatures.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`; the relevant internal claim was `claim:109e0d52757bfdeba9e1`, which states that represented postnatal Dlx-family and adjacent forebrain GABAergic developmental TF perturbations did not reconstitute a shared Dlx/Nkx2-1/Arx program in this perturbation corpus.
- PubMed-indexed Dlx literature:
  - Eisenstat et al. 1999, PMID 10516593, DOI `10.1002/(sici)1096-9861(19991115)414:2<217::aid-cne6>3.0.co;2-i`: Dlx1, Dlx2, and Dlx5 mark sequential stages in embryonic basal forebrain differentiation.
  - Zerucha et al. 2000, PMID 10632600, DOI `10.1523/JNEUROSCI.20-02-00709.2000`: the conserved Dlx5/Dlx6 intergenic enhancer mediates cross-regulation by Dlx proteins in embryonic forebrain.
  - Wang et al. 2010, PMID 20392955, DOI `10.1523/JNEUROSCI.5963-09.2010`: Dlx5 and Dlx6 double loss perturbs parvalbumin cortical interneuron development and function.
  - Wang et al. 2011, PMID 21452241, DOI `10.1002/cne.22618`: Dlx6 is expressed in ganglionic-eminence derivatives and helps specify striatal and central-amygdala molecular properties.
  - Lindtner et al. 2019, PMID 31433982, DOI `10.1016/j.celrep.2019.07.022`: Dlx1/2 organize a forebrain GABAergic developmental gene-regulatory network.
  - Puelles et al. 2020, PMID 32420617, DOI `10.1002/cne.24952`: a Dlx5/6-LacZ line marks postnatal prethalamic subdivisions, providing context for the diencephalic rather than purely cortical use of the Dlx5/6 locus.
  - Aouci et al. 2022, PMID 35681437, DOI `10.3390/cells11111739`: Dlx5/6 continue to act in adult telencephalic GABAergic neurons, especially parvalbumin neurons.

## Computational checks

To avoid loading the full 616-million-row parquet, I used Parquet row-group metadata for `group_name`, kept row groups whose min/max enclosed `151 TH Prkcd Grin2c Glut`, then filtered exactly to that group and the comparator `gene_target`s. For each comparator I recomputed the focal `n_degs` as:

```python
int((rows_for_target.pvals_adj < 0.05).sum())
```

I also inspected the smallest raw and adjusted p-values, matched perturbed nucleus counts, target-locus rows such as `Dlx5`, `Dlx6`, `Gad1`, and `Gad2`, and pairwise log-fold-change correlations/top-tail overlaps among the comparator signatures. The Distributed Agents profile comparison over the same focal rows used `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the significant-feature definition.

## Target-specific reasoning

### Dlx5

**Best direct analogs in training**

| training perturbation | observed `n_degs` | matched perturbed nuclei | focal expression evidence | transfer to `Dlx5` |
| --- | ---: | ---: | --- | --- |
| `Dlx6` | 0 | 294 | No genes passed FDR 0.05; the smallest raw p-value was `Nbas`, raw `p = 1.60e-4`, `p_adj = 1`; `Dlx5`, `Dlx6`, `Gad1`, and `Gad2` were all `p_adj = 1`. | Strongest in-dataset paralog. `Dlx5` and `Dlx6` are the linked bigene pair at the Dlx5/6 locus and share developmental forebrain enhancers, so a flat `Dlx6` single-gene CRISPR response is strong evidence for a flat `Dlx5` response in this acute P16 thalamic glutamatergic assay. |
| `Dlx3` | 0 | 161 | No genes passed FDR 0.05; the smallest raw p-value was `Arl15`, raw `p = 9.1e-5`, `p_adj = 1`. | A weaker Dlx-family analog because `Dlx3` is a developmental homeobox paralog but is not the forebrain Dlx5/6 locus partner. It is useful mainly as a countercheck that a Dlx homeobox knockout did not produce a broad response in this focal cell group. |

`Dlx1`, `Dlx2`, and `Lhx6` would have been closer forebrain GABAergic-developmental comparators, but they were not present as training perturbations in the endpoint CSV. Among available adjacent regulators, all were also flat in the focal group:

| training perturbation | observed `n_degs` | matched perturbed nuclei | why considered |
| --- | ---: | ---: | --- |
| `Arx` | 0 | 269 | A Dlx-linked forebrain inhibitory-neuron developmental effector/proxy; no focal FDR-significant genes. |
| `Nkx2-1` | 0 | 246 | MGE identity/homeobox comparator upstream of many inhibitory interneuron programs; no focal FDR-significant genes. |
| `Isl1` | 0 | 208 | Ventral-telencephalic/striatal developmental comparator and a gene reduced by Dlx5/6 enhancer disruption in embryonic work; no focal FDR-significant genes. |
| `Meis1` | 0 | 115 | Homeobox cofactor and striatal marker affected by Dlx5/6 enhancer perturbation; no focal FDR-significant genes. |
| `Meis2` | 0 | 194 | Related TALE/homeobox and striatal-developmental comparator; no focal FDR-significant genes. |
| `Otx2` | 0 | 162 | Diencephalic developmental homeobox counterexample; no focal FDR-significant genes. |
| `Pax6` | 0 | 138 | Neurodevelopmental TF counterexample from the same assay; no focal FDR-significant genes. |

The Dlx3 and Dlx6 signatures also did not reveal a subthreshold shared Dlx response that was merely missed by the final DEG count. Across all 17,259 measured focal genes the Dlx3/Dlx6 Spearman correlation was only 0.182, their top 200 positive tails shared 9 genes, their top 200 negative tails shared 12 genes, and neither perturbation had a significant positive or negative set to intersect. This made a small positive count for `Dlx5` less plausible than an exact zero.

**Counterexamples that show the focal assay can respond**

The absence of DEGs for Dlx-family and adjacent developmental TFs is not a global failure of this cell group to call DEGs. In the same focal group, `Ctnnb1` had 383 DEGs from 171 matched perturbed nuclei and `Tcf7l2` had 106 DEGs from 111 matched perturbed nuclei. Both are transcriptional Wnt-pathway regulators active in thalamic neuronal programs, and they shared leading genes such as `Ramp3` and `Plekhg1`. Mechanistically, however, Wnt/TCF perturbations are not Dlx5 analogs; I used them only to calibrate that 100- to 400-DEG responses were detectable when a relevant pathway was perturbed.

**Biological transfer**

The literature supports `Dlx5` as a real neuronal transcription factor, but the well-established programs are embryonic basal-forebrain GABAergic specification/migration and telencephalic GABAergic interneuron maintenance. Dlx proteins cross-regulate the Dlx5/Dlx6 locus through conserved enhancers in embryonic forebrain (Zerucha et al. 2000), Dlx factors control GABAergic developmental programs downstream of Dlx1/2 (Lindtner et al. 2019), and chronic Dlx5/6 double deletion affects parvalbumin interneuron development and adult GABAergic phenotypes (Wang et al. 2010; Aouci et al. 2022). The requested endpoint, by contrast, is a sparse acute P16 single-gene perturbation read out only 3-4 weeks later in a `TH ... Glut` cluster. The available postnatal perturbations that best approximate Dlx-family or Arx/Nkx2-1 GABAergic developmental biology were all FDR-flat there.

I therefore predict that acute `Dlx5` loss will be transcriptionally buffered or irrelevant in this specific thalamic glutamatergic population and will yield no BH-significant DEGs.

Predicted `Dlx5 n_degs`: **0**

## Limits and extrapolation

- The closest possible single-gene training analogs, `Dlx1` and `Dlx2`, were not assayed as available perturbations, and `Dlx6` is similar to `Dlx5` but not identical.
- Germline or conditional Dlx5/6 double-knockout studies are chronic, developmental, and often GABAergic-cell-specific; they can reveal cell-fate and circuit phenotypes that this mosaic P16 single-gene CRISPR assay would not convert into a nuclear RNA program.
- The training evidence is strongest for a zero call in the focal `151 TH Prkcd Grin2c Glut` group only. It should not be read as claiming that `Dlx5` has no effect in embryonic ventral forebrain, adult interneurons, prethalamic subdivisions, or craniofacial/osteogenic tissues.
- The precise zero/nonzero boundary depends on sampling depth and the Wilcoxon/BH test. Some raw p-values in analogs reached approximately `1e-4`, but after testing 17,259 genes they did not approach FDR 0.05, so I did not extrapolate them into a positive count for `Dlx5`.
