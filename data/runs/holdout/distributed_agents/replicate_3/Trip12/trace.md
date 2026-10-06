# Trip12 held-out prediction

## Question and resolved ambiguities

The held-out perturbation list for this run contains one target, `Trip12`. I interpreted the requested endpoint as the integer count of measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` cells after P16 AAV/CRISPR loss of `Trip12`, compared with matched non-targeting controls. The count includes the perturbed gene itself when that transcript is present in the measured gene universe and passes FDR; this matters because some training targets in the focal cell group had exactly one DEG consisting of the target transcript.

I treated this as a prediction for basal recovered neuronal nuclei at P37-P44, not for embryonic, germline, cancer-cell, DNA-damage-stimulated, or protein-turnover phenotypes.

## Sources used

- Training endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Training differential-expression parquet: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, especially the internal HECT/E3-ligase claim that `Huwe1` is a transcriptionally visible outlier and not a generic phenocopy of represented `Hectd4`, `Hecw2`, `Ube3a`, `Herc1`, or `Herc2` perturbations.
- Distributed Agents runtime profile comparison artifacts generated in this run:
  - `trip12_comparison.json`: profile comparison over HECT/E3, ARF-p53/MYC, Wnt, UFMylation, and proteasome counterexample targets.
  - `trip12_cohort.json`: cohort diagnostics for the same 20 training targets.
- PubMed literature:
  - Park et al. 2008, DOI `10.1016/j.bbrc.2008.07.019`: TRIP12 is a HECT E3 ligase for APP-BP1 and can modulate neddylation.
  - Chen et al. 2010, DOI `10.4161/cc.9.15.12355`: ULF/TRIP12 acts as an ARF E3 ligase in the ARF-p53 axis.
  - Kajiro et al. 2011, DOI `10.1371/journal.pone.0025871`: Trip12 E3 activity is required in mouse embryogenesis and affects p16/BAF57 and gene expression in developmental contexts.
  - Gudjonsson et al. 2012, DOI `10.1016/j.cell.2012.06.039`: TRIP12 and UBR5 restrain RNF168-dependent chromatin ubiquitylation spreading at DNA double-strand breaks.
  - Zhang et al. 2017, DOI `10.1007/s00439-017-1763-1`, and Aerden et al. 2023, DOI `10.1038/s41431-023-01307-x`: heterozygous pathogenic TRIP12 variants cause a haploinsufficient neurodevelopmental syndrome.

## Computation over the training data

The focal count distribution is zero-inflated: 1,205 of 1,674 training perturbations had `n_degs = 0`; the median was 0, the 75th percentile was 1, and only the 95th percentile exceeded 18 DEGs. A nonzero prediction is therefore already more assertive than the baseline training target.

I filtered the parquet to focal rows for biologically nominated comparators and counted their FDR 0.05 DEGs:

```python
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut") &
    pc.field("gene_target").isin(targets)
)
```

I also pulled rows with `names == gene_target` to check whether a one-DEG endpoint commonly corresponded to the target transcript. In the focal training data, 237 of 275 one-DEG perturbations had a significant self-transcript row; `Hectd4` was exactly such a HECT example.

## Comparator evidence for Trip12

`Trip12` is a HECT-domain E3 ubiquitin ligase, so represented HECT and ubiquitin-system perturbations were the most direct within-dataset analogs.

- `Huwe1`: 158 DEGs. This was the strongest relevant HECT-family response in `151 TH Prkcd Grin2c Glut`, with corrected changes including `Rsrp1`, `Tcea2`, `Dusp11`, `Aifm3`, `Sf3b1`, `L1cam`, and other RNA-processing/mitochondrial or trafficking genes. The Distributed Agents corpus explicitly separates this as a target-specific HUWE1 postmitotic signature rather than a generic HECT/E3-ligase response. I used it as the high-side counterexample: HECT ligases can be detected in this assay, but this signature should not simply be transferred to every HECT ligase.
- `Hectd4`: 1 DEG, `Hectd4` itself. This is a closer qualitative match to a target-transcript-only prediction: an expressed HECT E3 can be edited enough for its own RNA to pass FDR while not causing a downstream RNA program.
- `Hecw2`: 0 DEGs; `Herc1`: 0; `Herc2`: 0; `Ube3a`: 0; `Ubr1`: 0. These flat or nearly flat ligase perturbations argue that HECT/E3 membership and neurodevelopmental-disease relevance are insufficient to predict a broad basal neuronal signature.
- `Uba5`: 2677, `Ufc1`: 572, `Psmb4`: 742, `Psmc1`: 430. These proteostasis perturbations show that the focal cell group can mount very broad ubiquitin/proteasome-linked RNA responses, but they are core UFMylation or proteasome stresses rather than substrate-specific HECT-ligase knockouts, so I treated them as assay-positive counterexamples rather than close quantitative analogs.

I separately checked direct TRIP12 substrate-side or pathway-adjacent outputs:

- `Cdkn2a`: 0, `Trp53`: 0, `Myc`: 0, `Mycn`: 0. TRIP12/ULF suppresses ARF protein in proliferative cells, and Trip12 mutant embryos up-regulate p16, but the represented ARF/p53/MYC-side nodes were silent in basal postmitotic 151 neurons.
- `Notch1`: 0 and `Notch2`: 0. Developmental signaling components can be essential earlier without producing a tonic P16-to-P37/44 mRNA response in this neuronal endpoint.
- `Ctnnb1`: 383, `Lrp6`: 4, `Gsk3b`: 6. The same cell group can show a direct pathway response to selected developmental signaling nodes, but the broad `Ctnnb1` state is not mechanistically close to TRIP12 loss.

The profile comparison among these 20 nodes split the panel into 11 nodes with no significant features, 3 with 1-9 features, and 6 with at least 50. HECT-family and ARF/p53-side targets fell on the flat or singleton side, while the broad responders were the positive controls above.

## Target-specific prediction

External biology makes `Trip12` credible as an important neural gene: human loss-of-function causes a haploinsufficient intellectual-disability/autism syndrome, and Trip12 E3 activity is essential for mouse embryogenesis. Those facts did not make me transfer a large count, because the strongest characterized TRIP12 mechanisms are either protein-level and stimulus-gated, such as ARF turnover and RNF168 restriction after DNA breaks, or developmental rather than maintenance requirements in already specified NeuN+ neurons.

Inside the same experiment, the most appropriate analogy is not the `Huwe1` 158-DEG program but the mostly flat HECT-family behavior: `Hectd4` had only its own RNA as a corrected hit and `Hecw2`, `Herc1`, `Herc2`, `Ube3a`, and `Ubr1` had none in the focal group. `Trip12` itself is one of the 17,259 measured genes in this focal parquet slice, and target-self rows are a common source of one-DEG calls in training. I therefore predict that acute `Trip12` CRISPR loss will not create a convincing downstream ARF/p53, DNA-damage, Notch, proteostasis, or HUWE1-like expression program, but that the `Trip12` transcript itself is likely enough to be the single FDR-passing row.

Final point prediction:

| target_name | predicted_n_degs |
| --- | ---: |
| Trip12 | 1 |

## Limits

`Trip12` was absent from the supplied DE parquet, training count table, and Distributed Agents target corpus, so all reasoning is extrapolation from relatives and pathway neighbors. Most represented HECT comparators are distant family-level analogs, not paralogs in a stable TRIP12 complex; several closer genes such as `Ubr5`, `Hectd1`, `Ube3b`, and `Ube3c` were not training perturbations. The assay measures steady-state nuclear RNA, not target DNA indels, TRIP12 protein, ubiquitinated ARF/RNF168/APP-BP1, DNA-break repair foci, or transient early injury responses. Finally, predicting one DEG rather than zero is driven by target-self behavior in the training data, and target mRNA detectability/editability is noisy in this screen.
