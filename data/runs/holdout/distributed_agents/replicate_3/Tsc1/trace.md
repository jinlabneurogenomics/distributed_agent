# Tsc1 held-out DEG-count prediction

## Question and interpretation

The requested manifest contains one held-out perturbation, `Tsc1`. I interpreted the task as predicting the number of genes that would pass `pvals_adj < 0.05` for `Tsc1` in `151 TH Prkcd Grin2c Glut` neurons if the fully held-out same-experiment readout were present. The requested count is therefore an assay- and power-dependent FDR yield in the postnatal sparse AAV CRISPR Perturb-seq experiment, not a direct estimate of TSC1 biological importance or of the magnitude of mTORC1 activation.

I treated `TH` in the focal group name as thalamus, consistent with the PerturbAI atlas vocabulary, and did not use measured loss of the target transcript as an editing-efficiency weight because the dataset context warns that self-transcript fold change is uncoupled from downstream response size in this mosaic nuclear-RNA assay.

## Sources used

- Supplied focal training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied full differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 250_Tsc1.csv]`.
- Distributed Agents same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`, queried by `target_context`, `resolve_evidence`, `search_claims`, and `candidate_set_topology`.
- Distributed Agents gene-analog nomination over the mouse training universe, which used curated mouse/pathway annotations plus CORUM 5.0 human complexes projected through MGI one-to-one orthology classes downloaded 2026-09-13 and STRING v12.0 physical-interaction annotations.
- External PubMed literature for the TSC, Rheb, and GATOR1 mechanisms.

## Dataset computations

I first verified that the manifest had exactly the single requested target `Tsc1`, and that `Tsc1` was absent from the 1,674-gene focal training-count table. I then wrote the training target symbols to `training_targets.csv` so all corpus/runtime operations were intersected with the actual non-held-out universe.

For focal calibration I filtered the parquet to:

```
group_name == "151 TH Prkcd Grin2c Glut"
gene_target in {Tsc2, Depdc5, Mtor, Rptor, Strada, Fkbp1a, Akt3,
                Pik3cb, Pik3r1, Pik3r2, Rab7, Srebf2, Phf12,
                Wdr26, Psmc1, Psmb4, Sin3a}
```

and recounted `pvals_adj < 0.05`. This avoided scanning unrelated cell groups and gave the exact focal rows for the pathway anchors and the empirical stress/sterol neighbors discussed in the corpus. I also intersected the significant gene sets for the key same-direction comparators.

Relevant focal DEG counts from the training endpoint were:

| training target | focal `n_degs` | role in this prediction |
|---|---:|---|
| `Tsc2` | 86 | primary same-complex TSC anchor |
| `Depdc5` | 13 | same-direction negative mTORC1 regulator through GATOR1/Rag rather than TSC/Rheb |
| `Rab7` | 501 | lysosomal/endolysosomal sterol-state comparator, much broader than TSC |
| `Srebf2` | 7 | downstream sterol-branch inverse comparator |
| `Mtor` | 2 | loss of the kinase, expected opposite or weak |
| `Rptor` | 0 | mTORC1 positive core component, FDR-flat |
| `Strada` | 0 | LKB1/AMPK/TSC-adjacent, FDR-flat in the focal group |
| `Fkbp1a` | 1 | mTOR inhibitor-binding protein, only self-transcript significant |
| `Akt3` | 0 | upstream PI3K/AKT input, FDR-flat |
| `Pik3cb` | 0 | upstream PI3K catalytic subunit, FDR-flat |
| `Pik3r1` | 0 | upstream PI3K regulatory subunit, FDR-flat |
| `Pik3r2` | 0 | upstream PI3K regulatory subunit, FDR-flat |

The exact FDR<0.05 overlaps reinforced the same logic:

- `Tsc2` and `Depdc5` shared 8 focal FDR<0.05 genes: `Amy1`, `Ldlr`, `Msmo1`, `Pik3r1`, `Pik3r3`, `Rnpc3`, `Snhg11`, and `Tubb3`.
- `Tsc2` and `Rab7` shared 38 focal FDR<0.05 genes, including sterol or endolysosomal markers such as `Cyp51`, `Ldlr`, `Msmo1`, `Atp6v0b`, `Dpp7`, `Grn`, `Lamp2`, and `Rragd`.
- `Depdc5` and `Rab7` shared 5 focal FDR<0.05 genes: `Hmgcs1`, `Insig1`, `Ldlr`, `Msmo1`, and `Snhg11`.
- `Srebf2` opposed the sterol branch: its focal FDR<0.05 genes included down-regulated `Srebf2`, `Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`, `Cyp51`, and `Sqle`, whereas `Tsc2` and `Depdc5` increased the same sterol/LDL-uptake axis.

I also ran `profile_neighbors` with `Tsc2`, `Depdc5`, `Mtor`, `Rptor`, `Strada`, `Fkbp1a`, `Akt3`, `Pik3cb`, `Pik3r1`, and `Pik3r2` as anchors against all 1,674 eligible training targets in the focal group. The unbiased whole-profile neighbors of `Tsc2` and `Depdc5` were dominated by high background similarity among full 17,259-gene log-fold-change vectors and by top-tail coincidences in nonsignificant genes; for example, the leading full-vector neighbors of `Tsc2` were not TSC or GATOR members. I therefore used that calculation as a check against accidental omission, not as a quantitative estimator. The FDR-supported restricted-signature comparisons from the same-experiment corpus were more interpretable for `Tsc1`.

## Biological comparison for Tsc1

### Primary positive analog: Tsc2

The gene-analog nomination skill placed `Tsc2` as the highest exact-complex available comparator to held-out `Tsc1`. The retained provenance included CORUM 5.0 human complexes projected through MGI one-to-one orthology for `TSC1-TSC2`, `TBC1D7-TSC1-TSC2`, `AXIN1-GSK3B-TSC1-TSC2`, HSP90/TSC, and a STRING v12.0 mouse physical interaction between Tsc1 and Tsc2 with confidence 0.999. This is the only direct TSC complex partner available in the training universe; `Tbc1d7` and `Rheb` were absent from the parquet/training endpoint.

Mechanistically, TSC1/hamartin and TSC2/tuberin form the TSC complex that restrains mTORC1 by acting as a GAP for Rheb. TSC1 stabilizes TSC2 by reducing TSC2 ubiquitination, so losing TSC1 is expected to reduce functional TSC2 complex activity rather than merely touching the same pathway at a distance. That external prior is supported by Benvenuto et al. 2000, Oncogene, doi:10.1038/sj.onc.1204009; Inoki et al. 2003, Genes & Development, doi:10.1101/gad.1110003, PMID:12869586; the TSC/Rheb review by Huang and Manning 2008, Biochemical Journal, doi:10.1042/BJ20080281, PMID:18466115; and the identification of TBC1D7 as a third core TSC-complex subunit by Dibble et al. 2012, Molecular Cell, doi:10.1016/j.molcel.2012.06.009, PMID:22795129.

Within this dataset, `Tsc2` loss had 86 focal FDR<0.05 genes with 58 positive and 28 negative hits. The leading significant positive genes included `Cyp51`, `Pik3r3`, `Slc2a6`, `Ptgds`, `Dusp1`, `Tubb3`, `Nsdhl`, and `Abca2`; the negative side included `Nrbp2`, `Ccdc136`, `Amy1`, `Snhg11`, and `Pnisr`. The Distributed Agents corpus summarized the broader same-experiment evidence as a Tsc2 mTORC1/SREBP/lysosome-like neuronal module, strongest in caudal populations, and recorded focal same-direction overlap between `Tsc2` and `Depdc5` on sterol, PI3K-feedback, lysosome, and synaptic/microtubule genes.

`Tsc2` therefore carries the point prediction. I did not predict a zero for `Tsc1`: the only direct TSC partner is clearly nonzero and its response includes the expected mTORC1-SREBP feedback state.

### Secondary same-direction analog: Depdc5

`Depdc5` is not in the TSC complex, but it is another negative regulator of mTORC1: the DEPDC5/NPRL2/NPRL3 GATOR1 complex is a RagA/B GAP that inhibits the amino-acid branch of mTORC1 activation (Bar-Peled et al. 2013, Science, doi:10.1126/science.1232044; Shen et al. 2018, Nature, doi:10.1038/nature26158, PMID:29590090). In the focal group it had 13 FDR<0.05 genes and a coherent positive sterol/LDL-uptake module: `Ldlr`, `Insig1`, `Hmgcs1`, `Msmo1`, plus PI3K feedback genes `Pik3r1` and `Pik3r3`.

The Distributed Agents corpus found that, across the 23 `Depdc5` FDR<0.10 downstream genes in `151 TH Prkcd Grin2c Glut`, `Tsc2` was the top same-direction overlap neighbor with 11 shared same-direction genes and restricted cosine 0.940. This made `Depdc5` useful evidence that derepressing mTORC1 can be seen in this thalamic cell group. Its smaller 13-DEG FDR<0.05 burden, however, argues that amino-acid/Rag derepression samples only part of the `Tsc2` program and should pull the `Tsc1` prediction below a perfect copy of the 86-DEG `Tsc2` count.

### Module comparators and counterexamples

`Rab7` had a much larger focal response, 501 FDR<0.05 genes, and overlapped `Tsc2` on 38 focal hits and `Depdc5` on 5. It supported the identity of the sterol/endolysosomal state, especially `Insig1`, `Msmo1`, `Hmgcs1`, `Ldlr`, `Lamp2`, `Grn`, and `Rragd`, but Rab7 is a broad lysosomal trafficking GTPase rather than a TSC-complex protein; its 501-DEG response is a poor quantitative analog for `Tsc1`.

`Srebf2` was the expected branch-level inverse control. Its 7 focal DEGs went down in sterol biosynthesis and uptake genes that `Tsc2`/`Depdc5` induce, confirming the sterol axis but not giving a same-direction count to transfer.

Several textbook-proximal mTOR genes were explicit counterexamples in the same assay. `Mtor` loss had only 2 focal FDR<0.05 genes and a different mixed module; `Rptor`, `Strada`, `Akt3`, `Pik3cb`, `Pik3r1`, and `Pik3r2` were all focal zeros; `Fkbp1a` had only its own transcript. The Distributed Agents corpus claim for these perturbations states that represented upstream PI3K/AKT and positive mTORC1-associated perturbations are buffered or mutually non-phenocopying in basal juvenile neurons. That prevented me from averaging all mTOR-pathway members together, which would have spuriously driven `Tsc1` toward zero.

## Prediction

I predict that `Tsc1` will be nonzero and moderately broad in `151 TH Prkcd Grin2c Glut`: closest to `Tsc2` but somewhat smaller because TSC1 is the stabilizing/regulatory TSC subunit whereas TSC2 carries the Rheb-GAP domain directly, because the acute partial CRISPR design may leave residual TSC1/TSC2 complex, and because the one other mTORC1-repressor comparison, `Depdc5`, showed that derepression can shrink to a 13-gene sterol-focused signature in this assay.

The chosen point estimate is:

- `Tsc1`: **64** FDR<0.05 genes.

## Limits of the reasoning

- `Tsc1` itself is absent from both the parquet and the Distributed Agents corpus, so the prediction is extrapolated from `Tsc2` and not from a measured Tsc1 signature.
- The most direct biochemical neighbors after `Tsc2`, namely `Tbc1d7` and `Rheb`, were not represented in training; no same-complex triangulation was possible.
- DEG counts are highly sensitive to recovered perturbed-cell counts and guide performance. `Tsc2` had 177 perturbed nuclei and `Depdc5` had 121 in the focal group, but the held-out `Tsc1` matched count is unknown.
- Whole-logFC profile correlations across all 17,259 measured genes were not reliable enough to define a numeric transfer function here, because the top full-vector neighbors for `Tsc2`/`Depdc5` were not mechanistic mTOR/TSC nodes.
- mTORC1 is strongly regulated at phosphorylation, translation, autophagy flux, and cell-size levels; snRNA-seq can miss on-axis biochemical effects. The positive prediction means "enough secondary nuclear RNA response to cross FDR 0.05", not necessarily stronger mTORC1 signaling than the focal-zero pathway genes.
