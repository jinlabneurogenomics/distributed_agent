# Cul3 prediction for `151 TH Prkcd Grin2c Glut`

## Question and assumptions

The requested manifest contains one held-out perturbation:

| target_name |
| --- |
| Cul3 |

I interpreted `n_degs` as the count of measured genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05`, using the same Wilcoxon/Benjamini-Hochberg endpoint as the supplied training count table. This count includes the perturbed target transcript itself when that row is measured and significant; for example, the one DEG for several held-in genes was the target mRNA row alone. `Cul3` was absent from both the training DEG parquet and the focal-cell training count CSV, so all prediction evidence had to come from other targets plus outside biology.

I predicted **1 DEG** for `Cul3`: a nonzero but essentially self- or singleton-sized response, not a broad CRL3 loss-of-function expression program.

## Sources used

Internal/same-experiment sources:

- `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for the held-in analogs.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` for the endpoint counts of all 1,674 held-in perturbations.
- Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`, which was queried for Cul3, KCTD/GABA-B, and E3-ligase comparison claims.
- Distributed Agents runtime profile-comparison MCP, used to compute signed log-fold-change similarities among held-in E3/ubiquitin neighborhood genes in the focal cell type.

External literature:

- Xu et al. 2003, *Nature*, DOI `10.1038/nature01985`, PMID `13679922`: BTB proteins act as substrate-specific adaptors for CUL3 ubiquitin ligases.
- Canning et al. 2013, *JBC*, DOI `10.1074/jbc.M112.437996`, PMID `23349464`: structural basis for Cul3 assembly with BTB-Kelch adaptors, including KLHL-family proteins.
- Escamilla et al. 2017, *Nature*, DOI `10.1038/nature24470`, PMID `29088697`: KCTD13/CUL3 regulates neuronal RhoA, and Kctd13 deletion alters synaptic transmission through increased RhoA.
- Amar et al. 2021, *Molecular Psychiatry*, DOI `10.1038/s41380-021-01052-x`, PMID `33727673`: germline Cul3 haploinsufficiency affects cortical neurogenesis/cytoskeleton/RhoA signaling.
- Morandell et al. 2021, *Nature Communications*, DOI `10.1038/s41467-021-23123-x`, PMID `34031387`: Cul3 controls cytoskeletal protein homeostasis and neuronal migration during a developmental critical window; later induction of Cul3 haploinsufficiency did not produce the same ASD-relevant behavioral phenotypes.

## Computation over the training data

I first read the focal training counts. The endpoint in this cell type is very sparse:

- 1,674 held-in targets
- median `n_degs = 0`
- 75th percentile `n_degs = 1`
- 90th percentile `n_degs = 2`
- 95th percentile `n_degs = 18`
- a thin upper tail headed by `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, `Rnpc3 = 868`, and `Zbtb7a = 841`

No held-in target began with `Cul`, so there was no direct cullin paralog knockout for calibration. I therefore assembled held-in genes from the closest represented neighborhoods:

- CRL3-like or BTB/Kelch/KCTD adaptors: `Kctd1`, `Kctd16`, `Kctd8`, `Klhl20`, `Klhl7`
- other Cullin-RING adaptor classes: `Fbxo11`, `Fbxo38`, `Fbxw7`, `Dcaf8`, `Ddb2`
- unrelated E3 ligase controls/counterexamples: `Huwe1`, `Hectd4`, `Hecw2`, `Ube3a`, `Herc1`, `Herc2`, `Trim2`, `Trim37`, `Rnf216`, `Rnf220`, `Ubr1`
- broader ubiquitin/proteasome or E3 pathway counterexamples: `Uba5`, `Psmb4`, `Psmc1`, `Usp48`, `Marchf6`, `Amfr`, `Srebf2`, `Mttp`
- same-experiment GABA-B/KCTD pathway comparators from the corpus: `Gabbr1`, `Gabbr2`

For these 31 targets I scanned the parquet with:

```python
filter = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(candidate_targets)
```

and, for each target, counted `pvals_adj < 0.05`, recorded the matched perturbed-cell count, inspected the self row where `names == gene_target`, and listed the significant rows for the sparse analogs. I then ran `profile_compare` on signed `logfoldchanges`, again restricted to `151 TH Prkcd Grin2c Glut`, using the training count CSV as the eligible target universe and `pvals_adj < 0.05` as the significance criterion. That comparison was used only for observed similarity and nonconvergence checks; the final prediction was target-specific rather than an average over all listed genes.

## Target-specific evidence and reasoning

### Direct CRL3-adaptor analogs

`Cul3` is the scaffold for BTB-domain substrate receptors: BTB/Kelch proteins combine the Cullin-binding and substrate-binding functions that are split across Skp1/F-box or Elongin/SOCS modules in other Cullin-RING ligases (Xu et al. 2003; Canning et al. 2013). The represented BTB/KCTD/Kelch targets in the training data were therefore the closest within-dataset perturbations, even though none is a scaffold knockout.

| held-in target | why compared | `n_degs` in 151 TH Prkcd Grin2c Glut | focal expression evidence |
| --- | --- | ---: | --- |
| `Kctd16` | KCTD auxiliary protein; BTB-containing KCTD family, same broad domain class as CUL3 adaptors although this one is a GABA-B auxiliary | 0 | no FDR genes |
| `Kctd8` | KCTD auxiliary protein in the same GABA-B auxiliary branch | 0 | no FDR genes |
| `Kctd1` | BTB/KCTD target with a CRL3-adaptor-like fold | 2 | only `Resp18` up and `Cluap1` down; no shared significant genes with F-box/DCAF/KLHL/HECT controls |
| `Klhl20` | bona fide KLHL-family CRL3 substrate adaptor in other contexts | 0 | no FDR genes |
| `Klhl7` | KLHL-family CRL3 substrate adaptor; structural KLHL7-Kelch domain was studied as part of the Cul3/BTB-Kelch assembly class | 0 | no FDR genes |

The Distributed Agents corpus independently reported that the represented `Kctd16`, `Kctd8`, `Gabbr1`, and `Gabbr2` GABA-B receptor/auxiliary cassette did **not** generate a shared stable nuclear RNA program in this neuronal CRISPR screen. In the focal count table `Gabbr1` and `Gabbr2` each had exactly one DEG, their own strongly depleted receptor transcript, while `Kctd16` and `Kctd8` had zero. This matters for Cul3 because one important neuronal CUL3 axis is KCTD13-RhoA (Escamilla et al. 2017), but the KCTD family and GABA-B auxiliary branch were not transcriptionally loud in this exact postnatal sparse-CRISPR/snRNA-seq assay.

The other Cullin-RING adaptor proxies were also flat:

| held-in target | complex class | `n_degs` | focal expression evidence |
| --- | --- | ---: | --- |
| `Fbxo11` | F-box, CUL1/SCF adaptor class | 1 | one weak singleton, `Ppib` down |
| `Fbxw7` | F-box, CUL1/SCF adaptor class | 1 | one weak singleton, `Trp53inp2` up |
| `Fbxo38` | F-box, CUL1/SCF adaptor class | 0 | no FDR genes |
| `Dcaf8` | DDB1-CUL4-associated factor | 0 | no FDR genes |
| `Ddb2` | CUL4/DDB complex component | 0 | no FDR genes |

These are not mechanistic Cul3 analogs in the strict sense because their scaffolds and substrate adaptors differ, so I used them as boundary evidence: knocking out single Cullin-RING substrate receptors in this experiment was usually buffered at the snRNA level. The CRL3 target differs because a scaffold could hit many BTB adaptors simultaneously, but the guide design only produces partial acute loss and the readout is nuclear RNA rather than accumulated ubiquitination substrates.

### E3-ligase counterexamples

Broad ubiquitin-stress phenotypes do exist in the training set, but the mechanistic matches were poor.

| held-in target | `n_degs` | interpretation for Cul3 |
| --- | ---: | --- |
| `Uba5` | 2677 | very broad UFM1-activation/ubiquitin-like response; not a CRL3 scaffold or BTB-adaptor perturbation |
| `Psmb4` | 742 | core proteasome subunit, broad proteostasis stress; too global for partial `Cul3` loss |
| `Psmc1` | 430 | proteasome ATPase, broad proteostasis stress; too global for partial `Cul3` loss |
| `Huwe1` | 158 | a transcriptionally visible HECT E3, but Distributed Agents corpus release says the HUWE1 state is target-specific and not a generic HECT/E3 phenotype |
| `Marchf6` | 14 | ER-membrane E3 with a clear sterol rebound (`Insig1`, `Dhcr24`, `Cyp51`, `Msmo1`, `Hmgcr`, etc. up); this sterol program is pathway-specific and not a CRL3/RhoA state |
| `Usp48` | 10 | sparse deubiquitinase response; no CUL3-specific mechanism |
| `Hectd4`/`Hecw2`/`Ube3a`/`Herc1`/`Herc2` | 1/0/0/0/0 | HECT/HERC E3 controls that were flat or target-self-only in the same focal cell type |
| `Trim2`/`Trim37` | 2/1 | sparse TRIM-family E3 controls with singleton or two-gene thalamic signatures |
| `Rnf216`/`Rnf220`/`Ubr1` | 0/0/0 | additional unrelated E3 controls that were flat |

The same-experiment Distributed Agents corpus agreed with this separation. It reported that the HUWE1 postmitotic signature was not a generic HECT/E3-ligase response: represented `Ube3a`, `Hectd4`, `Hecw2`, `Herc1`, and `Herc2` were flat, sparse, or nonconvergent while `Huwe1` alone was transcriptionally visible. A second claim similarly separated `Trim2` and `Trim37` from represented TRIM/E3/peroxisomal comparators. Those corpus claims argue against mapping `Cul3` to the largest E3 or proteasome responses just because all involve ubiquitin biology.

### Expected Cul3 state

The external biology says a complete or developmental Cul3 perturbation is important in neurons: CUL3-BTB complexes can control many substrates, KCTD13/CUL3 regulates RhoA in synaptic phenotypes, and germline Cul3 haploinsufficiency alters brain development and cytoskeletal signaling. That raises the prediction above a confident zero.

But most of those phenotypes involve embryonic neurogenesis, neuronal migration, cytoskeletal protein abundance, or synaptic physiology rather than an acute P16-to-P37 basal nuclear RNA state. Morandell et al. found that constitutive Cul3 haploinsufficiency produced neurodevelopmental phenotypes that were not reproduced by later induction, which matches the idea that a 3-4 week postnatal mosaic perturbation could miss the large germline migration program. The direct held-in training analogs strengthen that caution: represented BTB/KCTD/KLHL adaptors, F-box/DCAF adaptors, and most unrelated E3s had 0 to 2 DEGs in this exact focal cell group.

I therefore predict a **singleton-sized** response. The nonzero call reflects that `Cul3` itself is likely expressed broadly enough for the CRISPR perturbation to register as a self-transcript or very small cytoskeletal/stress readout. The low point estimate reflects the lack of a held-in CRL3 adaptor module, the absence of represented `Cul3` paralog scaffolds, the postmitotic timing, and the fact that strong training responses such as `Huwe1`, `Marchf6`, `Uba5`, `Psmb4`, and `Psmc1` all carried mechanisms that should not be pooled with Cul3.

## Limits

This is an extrapolation because the training set contains no `Cul1`, `Cul2`, `Cul3`, `Cul4a/b`, `Cul5`, `Rbx1`, `Nedd8`, `Cand1`, `Keap1`, `Kctd13`, `Klhl2`, `Klhl3`, `Klhl12`, or `Lztr1` perturbation in the focal training count table. The represented `Klhl7`, `Klhl20`, and KCTD genes test only a small, adapter-level slice of CRL3 biology, and `Kctd8`/`Kctd16` are GABA-B auxiliary proteins rather than known KCTD13-like RhoA adaptors. Published Cul3 mouse phenotypes are largely germline or developmental and cannot be directly transplanted into this acute, sparse, postnatal neuronal CRISPR assay. Finally, the assay is a single-cell nuclear RNA rank-sum readout; it is insensitive to many protein-stability, morphology, migration, and electrophysiology consequences that are plausible direct outcomes of CUL3 loss.
