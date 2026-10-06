# Held-out DEG-count prediction

## Question and endpoint

The requested held-out target list contains one perturbation, `Smpd3`. I interpreted the endpoint as the integer count of measured genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` contrast in the same Wilcoxon/BH workflow used for the supplied training counts. The supplied `Smpd3` knockout rows are absent from both the all-cell DE Parquet and the focal-cell training count CSV, so the prediction has to be transferred from visible non-held-out perturbations.

I treated the training CSV as a direct observation of the requested endpoint for visible targets. I treated the all-cell-group DE Parquet as direct evidence for the expression pattern behind those counts, especially whether a count was a broad downstream state or only the targeted transcript. The selected July 2026 PerturbAI same-experiment corpus is a packaged interpretation of the same Perturb-seq experiment, not independent replication. PubMed literature was used only as external gene-function prior.

## Sources used

- `training_de_all_cell_groups.parquet`: visible Perturb-seq differential-expression rows, filtered to `151 TH Prkcd Grin2c Glut` and to sphingolipid/lysosomal/stress analog perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for 1,674 visible perturbations in the requested focal cell group.
- Held-out manifest `b0193.csv`: the only target is `Smpd3`, not present in the training counts.
- PerturbAI July 2026 same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, queried through `corpus.findings` and `corpus.report_evidence` for `Asah1`, `Cert1`, `Psap`, and `Sptlc2`.
- External literature from PubMed:
  - Aubin et al. 2005, Nat Genet, DOI `10.1038/ng1603` / PMID `16025116`, identified the murine `fragilitas ossium` deletion as loss of `Smpd3` and loss of neutral sphingomyelinase activity.
  - Khavandgar et al. 2011, J Cell Biol, DOI `10.1083/jcb.201102051` / PMID `21788370`, showed a cell-autonomous requirement for `Smpd3` in osteoblast mineralization.
  - Alebrahim et al. 2014, Genesis, DOI `10.1002/dvg.22765` / PMID `24585429`, showed transient inducible `Smpd3` expression prevents the early skeletal/perinatal lethality of `fro/fro` mice on a C57BL/6 background.
  - Li et al. 2016, Mol Cell Biol, DOI `10.1128/MCB.01077-15` / PMID `27325675`, separated chondrocyte and osteoblast requirements for normal endochondral bone development.
  - Leidal et al. 2020, Nat Cell Biol, DOI `10.1038/s41556-019-0450-y` / PMID `31932738`, linked nSMase2 activity to LC3-dependent extracellular-vesicle cargo loading.
  - Wang et al. 2023, Nat Metab, DOI `10.1038/s42255-023-00808-9` / PMID `37188818`, found hepatic ER/mitochondrial stress after excess `Smpd3` expression downstream of impaired m6A-mediated decay; this is the opposite direction from a CRISPR loss-of-function.

## Dataset calculations

From the 1,674 training targets in the focal-cell count CSV, the median `n_degs` is 0 and 72.0% of targets are zero, so a missing target needs a strong within-dataset analog to justify a broad positive count. Obvious visible neutral sphingomyelinase paralogs `Smpd1` and `Smpd2` were not perturbation targets; neither were `Asah2`, `Acer1-3`, `Gba/Gba1`, `Galc`, `Hexa`, `Hexb`, `Arsa`, `Sphk2`, `Tfeb`, or `Mcoln1` according to the same-experiment Psap/Asah1 comparator audits.

I therefore queried the Parquet narrowly for focal-cell rows from represented sphingolipid and lysosomal comparators:

```python
filter = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
```

The biologically closest visible analogs were almost all null at the requested cutoff:

| visible perturbation | `n_degs` in 151 TH | focal-cell pattern |
|---|---:|---|
| `Asah1` | 0 | no genes below FDR 0.05 or 0.10; leading rows were unrelated and BH-adjusted to 1 |
| `Cert1` | 0 | no genes below FDR 0.05; `Cert1` itself had FDR 0.248 |
| `Sphk1` | 0 | no genes below FDR 0.10 |
| `Psap` | 1 | only `Psap` itself was significant, logFC -1.277, FDR 1.70e-28 |
| `Sptlc2` | 1 | only `Sptlc2` itself was significant, logFC -0.685, FDR 1.45e-4 |
| `Lamp2` | 0 | `Lamp2` and `Ppm1g` approached but missed 0.05, FDR 0.0537 and 0.0545 |
| `Ppt1` | 1 | self-transcript only, `Ppt1` FDR 1.34e-5 |
| `Ctsb` | 1 | self-transcript only, `Ctsb` FDR 8.54e-43 |
| `Scarb2` | 1 | self-transcript only, `Scarb2` FDR 0.00246 |
| `Grn` | 1 | self-transcript only, `Grn` FDR 5.27e-5 |
| `Atp6v0a1` | 1 | self-transcript only, `Atp6v0a1` FDR 4.52e-12 |
| `Manba`, `Sort1`, `Atp6v1a`, `Atp6v1b2`, `Atp6v1e1` | 0 | no focal-cell genes below FDR 0.05 |

The same-experiment corpus was concordant with these direct rows. Its `Asah1` evidence records state that `Asah1`, `Psap`, `Sphk1`, `Sptlc2`, and multiple lysosomal comparators were flat or singleton-only across neuronal cell groups. The `Psap` report explicitly found no shared Psap/Asah1/Ppt1/Grn/Sort1/Lamp2/v-ATPase storage-stress module. `Sptlc2` had no canonical UPR, ISR, autophagy, lysosomal, or sphingolipid-compensation transcripts significant in 336 queried gene-by-cell tests, and those same markers were detectable elsewhere in the screen. `Cert1` was also flat in the focal cell group despite direct queries of UPR genes such as `Hspa5`, `Hsp90b1`, `Herpud1`, `Ddit3`, `Atf4`, and `Xbp1`.

## Target-specific transfer for `Smpd3`

`Smpd3` encodes neutral sphingomyelinase 2, a membrane sphingomyelin hydrolase that generates ceramide and participates in extracellular-vesicle biogenesis. Complete mouse `Smpd3` loss is not benign: the `fro` deletion causes severe osteogenesis and dentinogenesis imperfecta, and later rescue/conditional work localized the strongest developmental requirement to osteoblasts, odontoblasts, and chondrocytes. That mechanism is developmentally and anatomically distant from sparse P16 AAV CRISPR in postmitotic NeuN-positive thalamic glutamatergic neurons.

The closest in-screen biochemical transfers point to a null or near-null readout:

- `Asah1`, the lysosomal acid ceramidase in the salvage arm, had `n_degs = 0`; the all-cell corpus additionally reported 0 downstream genes at FDR<0.10 in every recovered neuronal group.
- `Psap`, which supplies saposins for lysosomal sphingolipid catabolism and stimulates ASAH1-mediated ceramide hydrolysis in Reactome reaction R-HSA-1606602, had `n_degs = 1`; in the focal cell this was only the `Psap` transcript, not downstream storage, TFEB/CLEAR, autophagy, or ISR induction.
- `Sptlc2`, an essential serine palmitoyltransferase component upstream of de novo sphingolipid synthesis, had `n_degs = 1`; again the focal-cell count was only the target transcript.
- `Cert1`, which transports ER ceramide into the Golgi sphingomyelin branch, had `n_degs = 0` and lacked the ER-stress/chaperone rebound seen after a direct chaperone perturbation such as `Hspa5`.
- `Sphk1` had `n_degs = 0`, and visible lysosomal controls such as `Ppt1`, `Ctsb`, `Scarb2`, `Grn`, `Lamp2`, `Atp6v0a1`, and v-ATPase subunits were either null or self-only in the focal cell group.

This is a transfer from pathway neighbors rather than an obligate same-complex prediction: Smpd3 acts at neutral membranes, not at the lysosomal PSAP/ASAH1 step or at the ER SPT/CERT steps. The intervention is CRISPR loss of `Smpd3`; the direct molecular consequence should be reduced nSMase2-dependent sphingomyelin-to-ceramide flux and reduced ceramide-dependent vesicle production; propagation could alter membrane microdomains or extracellular vesicle output; the endpoint would only move if recovered thalamic glutamatergic neurons converted that lipid change into a nuclear stress or differentiation program by P37-P44. The in-dataset analogs show that related partial perturbations of sphingolipid flux did not cross that transcriptional threshold.

External literature does not reverse the direction. Hepatic and intestinal SMPD3 upregulation can promote stress pathology, and Smpd3 inhibition can be protective in those settings; Wang et al. 2023 specifically found that toxic hepatic ceramide accumulation followed increased Smpd3 mRNA stability, the opposite of a loss-of-function. nSMase2-dependent extracellular-vesicle biology is real, but the training perturbations most likely to produce lysosomal/autophagy or ER-stress secondary states show that this single-nucleus screen can miss lipid flux changes or see them without a broad mRNA response.

I therefore predicted `0` for `Smpd3`. The stronger evidence is dataset-local: visible lipid-metabolism perturbations in the focal class had zero or one DEG and the one-gene cases were target transcript calls. The external prior mainly prevents over-transferring severe skeletal `fro/fro` phenotypes or stress-induced overexpression models into this sparse postnatal neuronal loss-of-function assay.

## Limits and uncertainty

The main uncertainty is that no direct visible neutral sphingomyelinase paralog was available: `Smpd1`, `Smpd2`, and `Smpd3` were all outside the visible perturbation set used for training. I also did not have lipidomics, extracellular-vesicle secretion, DNA-indel rates, or per-cell survival, so a true membrane-ceramide or vesicle phenotype could be present without producing any FDR-significant nuclear RNA change. The predicted zero is therefore an endpoint prediction for the supplied DE-count assay, not a claim that Smpd3 is biologically inactive in neurons.
