# Vps13d prediction trace

## Question and resolved ambiguities

The held-out target list for this run contains one mouse perturbation, `Vps13d`. I interpreted the endpoint as the integer number of measured genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` differential-expression contrast after acute sparse AAV-CRISPR loss of function. This includes the perturbed target transcript itself if it would have crossed FDR, matching cases such as `Atp13a2`, `Park7`, `Map1lc3a`, `Pex14`, and `Tomm40` in the training table where the single counted DEG is the target RNA.

I treated `151 TH Prkcd Grin2c Glut` as the focal thalamic glutamatergic Allen-taxonomy class, with `TH` meaning thalamus. I did not treat weak or absent self-transcript knockdown as evidence of failed editing, because the experiment was sparse Cas9 editing of postmitotic neurons and target transcript abundance is not a direct editing-efficiency measure.

## Sources used

Internal data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: focal-cell observed `n_degs` for the 1,674 non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`: row-level log-fold changes and adjusted Wilcoxon p-values for non-held-out perturbations.
- `[local file: 261_Vps13d.csv]`: the requested held-out target list.

Same-experiment semantic layer:

- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`. `Vps13d` was not represented as a target in that corpus, so I used it for the assayed VPS13 paralogs and pathway comparators. The most relevant packaged claims were:
- `claim:a4d0bcbd5f9bf5142b7e`: represented `Vps13a`, `Vps13b`, and `Vps13c` perturbations do not elicit a shared basal neuronal transcriptomic module.
- `claim:726468d7afc216bc3be2`: `Rab7` and `Vps41` weakly share a selective late-endosomal/lysosomal compensation branch, while several adjacent endolysosomal perturbations do not.
- `claim:30ab45a3b952026ae47a` and related `Opa1` claims: the screen can detect an Opa1-associated ATF4/ISR-like mitochondrial stress program, but that program is not a generic consequence of perturbing every mitochondrial gene.

External literature:

- Gauthier et al., 2018, `doi:10.1002/ana.25204`, PMID 29518281; and Seong et al., 2018, `doi:10.1002/ana.25220`, PMID 29604224: recessive VPS13D variants cause childhood-onset movement disorders and ataxia/spasticity-spectrum disease with mitochondrial defects.
- Guillen-Samander et al., 2021, `doi:10.1083/jcb.202010004`, PMID 33891013: Miro recruits VPS13D to ER-mitochondria and ER-peroxisome contacts through a VAP-dependent ER bridge, connecting VPS13D to organellar lipid transfer.
- Baldwin et al., 2021, `doi:10.1083/jcb.202001188`, PMID 33891012: among single VPS13 knockouts in cell models, VPS13D loss strongly affected mitochondrial morphology and peroxisome abundance/biogenesis.
- Shen et al., 2021, `doi:10.1083/jcb.202104073`, PMID 34459871; and Insolera et al., 2021, `doi:10.1371/journal.pgen.1009731`, PMID 34383748: Drosophila Vps13D participates in Pink1-dependent mitophagy and in mitochondrial fission/phagophore elongation in neurons.
- Du et al., 2021, `doi:10.1091/mbc.E21-03-0097`, PMID 34133214: VPS13D can regulate ER-mitochondria contacts through VCP/p97 and VAPB/PTPIP51-linked contact-site control.
- Miao et al., 2025, `doi:10.1038/s41594-025-01602-9`, PMID 40563011: neuron-specific Vps13d loss in mice produces mitochondrial defects followed by cGAS-STING/microglial inflammatory cell death, emphasizing that glial feedback and degeneration can be major downstream biology in full conditional models.

## Dataset computations

The focal training endpoint is very sparse:

- 1,674 training perturbations were present.
- 469 of 1,674 were nonzero.
- Median `n_degs` was 0; 75th percentile was 1; 90th percentile was 2; 95th percentile was 18; 99th percentile was 436.5.
- The largest focal responses were outliers such as `Uba5` at 2,677, `Tpr` at 1,768, `Sin3a` at 1,433, and several spliceosome, proteasome, and chromatin/transcriptional regulators.

To avoid loading the full 7.8 GB parquet, I used PyArrow row-group statistics to verify that `151 TH Prkcd Grin2c Glut` occupies a contiguous block of row groups and then read only rows for the focal group and a declared set of VPS13, endolysosomal, autophagy, mitophagy, peroxisomal, Miro, and mitochondrial-dynamics analogs:

```python
table = dataset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges",
        "pvals_adj", "scores", "n_pert_matched", "n_ctrl_matched"
    ],
    filter=(
        (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & ds.field("gene_target").isin(targets)
    ),
)
```

This yielded 17,259 measured genes per queried training target in the focal group. I counted `pvals_adj < 0.05` for each analog and inspected the leading adjusted-p rows to tell whether a nonzero count was a broad downstream state or merely a self-transcript hit.

## Target-specific reasoning

### Vps13d

`Vps13d` itself is held out, so no row for it was used from the focal training count table or from the DE parquet. The direct within-family evidence available in this exact experiment points to a null acute neuronal mRNA state:

| training target | focal `n_degs` | focal expression evidence |
|---|---:|---|
| `Vps13a` | 0 | no gene below FDR 0.05; smallest focal adjusted p-value was 0.896 |
| `Vps13b` | 0 | no gene below FDR 0.05; smallest focal adjusted p-value was 0.374 |
| `Vps13c` | 0 | no gene below FDR 0.05; smallest focal adjusted p-value was 0.485 |

The Distributed Agents same-experiment corpus extends this beyond the one focal count: represented `Vps13a`, `Vps13b`, and `Vps13c` were interpreted as flat or non-phenocopying across the juvenile postmitotic neuronal panel, and their whole-surface neighbor scans sat near the empirical null. This does not prove `Vps13d` must be flat, because VPS13D is the VPS13 paralog most tied to mitochondria/peroxisomes and was explicitly absent from the screen. It does, however, argue strongly against assigning a broad response purely from VPS13 family membership or recessive movement-disorder status.

I then compared `Vps13d` against more pathway-proximal but not paralogous perturbations:

| training target | focal `n_degs` | interpretation for `Vps13d` |
|---|---:|---|
| `Rhot1` | 0 | direct Miro/VPS13D adaptor family member represented in training; no focal FDR response |
| `Pex1` | 0 | peroxisome-biogenesis perturbation, no focal FDR response |
| `Pex14` | 1 | self-transcript-only focal hit, not a peroxisome stress module |
| `Tomm40` | 1 | self-transcript-only mitochondrial import hit |
| `Atp13a2` | 1 | self-transcript-only in focal and pan-neuronal downstream null in the corpus despite lysosomal/Parkinson relevance |
| `Atp13a3` | 0 | P5B/polyamine paralog of `Atp13a2`; no focal FDR response |
| `Park7` | 1 | self-transcript-only focal hit |
| `Snca`, `Psen1`, `Pank2` | 0, 0, 0 | Parkinson/endolysosomal disease comparators, focal null |
| `Atg5`, `Atg16l1`, `Becn1` | 0, 0, 0 | core autophagy perturbations did not pass FDR in the focal group |
| `Lamp2` | 0 | the two leading rows were `Lamp2` and `Ppm1g`, but both stayed just above FDR 0.05 |
| `Sqstm1`, `Map1lc3a` | 1, 1 | self-transcript-only focal hits, not broad autophagy states |
| `Mff`, `Yme1l1`, `Timmdc1` | 0, 0, 0 | mitochondrial fission/OPA1-processing or mitochondrial-adjacent controls, focal null |
| `Slc25a46` | 1 | self-transcript-only focal hit |
| `Vcp` | 2 | a tiny response, despite VCP/p97 being reported as a VPS13D interactor |

There are clear positive trafficking and mitochondrial stress states in the same focal cell class, so the zero call is not based on assuming the assay is blind. `Rab7` had 501 focal DEGs with strong induction of V-ATPase/lysosomal genes such as `Atp6v1b2`, `Dpp7`, and `Atp6v0b` plus sterol/stress genes; `Dctn1` had 75 DEGs dominated by sterol biosynthesis genes; `Tsc2` had 86 DEGs; `Vps35` had 17; and `Vps54` had 31. `Opa1` had 37 DEGs, led by the ATF4/ISR-like genes `Asns`, `Mars1`, `Chac1`, `Ddit3`, and `Slc7a5`. These are important positive controls, but they are weaker analogs for `Vps13d` than the silent VPS13 paralogs and the quiet `Rhot1`/peroxisome/autophagy/Parkinson comparators. The Distributed Agents corpus also treats `Opa1` as a branch-specific mitochondrial ISR state, not a generic consequence of perturbing any mitochondrial or mitochondrial-adjacent target, and it separates `Rab7`'s broad late-endosomal compensation state from many nearby lysosomal/autophagy single-gene perturbations.

The external biology raises the prior that full VPS13D loss can perturb neuronal organelles. Human recessive disease genetics and Drosophila/cell-line studies support roles in movement disorders, mitochondrial morphology, peroxisome biogenesis, ER-organelle lipid-transfer contacts, and mitophagy. Those findings are not exact analogs to this endpoint. Many are complete knockouts, chronic organismal models, fibroblasts or transformed cells, or Drosophila neurons under developmental mitophagy paradigms. Miao et al. also showed that microglia can drive inflammatory death after neuron-specific Vps13d loss, whereas this snRNA-seq assay is NeuN-enriched and largely lacks microglia. Thus Vps13d loss may have organelle, flux, survival, axonal, or glial-coupled consequences without creating enough cell-autonomous nuclear mRNA changes in recovered juvenile `151 TH Prkcd Grin2c Glut` nuclei to pass BH FDR.

### Zero/nonzero decision and point estimate

I predict no FDR-significant genes for `Vps13d` in this cell group, so the point prediction is:

| target | predicted `n_degs` |
|---|---:|
| `Vps13d` | 0 |

The decision is mainly driven by within-dataset evidence: all assayed VPS13 paralogs were focal zeroes and corpus-level neuronal nulls; the Miro/peroxisome/autophagy/Parkinson controls closest to VPS13D biology were null or self-only in the focal group; and the nonzero `Rab7`/`Opa1`/`Tsc2`/`Dctn1` responses represented stronger or different organelle stress branches rather than a family-level transcriptional template. External literature was used to choose the comparator set and to avoid ignoring Vps13d's mitochondrial/peroxisomal disease biology, but it did not override the exact-screen calibration.

## Limits

- `Vps13d` is not the same as `Vps13a`, `Vps13b`, or `Vps13c`: among VPS13 proteins it has particularly strong mitochondrial, peroxisomal, and mitophagy annotations.
- The screen did not include several direct VPS13D interactors or effectors as useful matched perturbations, including `Vapb`, `Rhot2`, `Pink1`, `Prkn`, `Mfn1`, `Mfn2`, and `Mtch2`.
- A zero DEG prediction does not imply no editing, no protein loss, or no biology. Lipid transfer, peroxisome abundance, mitochondrial morphology, mitophagic flux, axonal transport, and survival were not assayed directly.
- Some Distributed Agents corpus findings summarize the same experiment at the source-report threshold of FDR 0.10. I used those qualitative findings to identify flat versus pathway-positive neuronal states, but used the supplied FDR 0.05 training count table and direct `pvals_adj < 0.05` parquet rows for the numeric point prediction.
- The assay is survivor-conditioned and short relative to many VPS13D disease phenotypes. A severe Vps13d organelle defect that selects cells out of the recovered NeuN-positive pool, requires microglial feedback, or accumulates slowly would be under-read by this endpoint.
- The nonzero comparator states are imperfect: `Rab7` is late endosome/lysosome fusion, `Opa1` is inner-membrane fusion and cristae stress, `Tsc2` is mTORC1 regulation, and `Dctn1` is dynein/dynactin transport. Their focal DEG burdens show assay capacity but are not point estimates for `Vps13d`.
