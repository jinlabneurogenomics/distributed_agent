# Question

I interpreted the task as: for each gene in `221_Srgap3.csv`, predict how many measured genes would have `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute AAV-CRISPR loss of that target, even though the target's own Perturb-seq differential-expression signature and endpoint count were removed from both supplied training inputs.

This run contains exactly one held-out target:

| target | prediction |
| --- | ---: |
| Srgap3 | 0 |

The main ambiguity was whether to treat Srgap3 as likely to yield a one-gene, target-self response. I counted self-DEG behavior as evidence, because `n_degs` includes the perturbed gene if it passes FDR, but I did not assume editing always makes the target transcript significant. Many focal training KOs in this screen have no detectable RNA endpoint despite known neuronal functions and despite the average direct target depletion in the experiment.

# Sources

Inputs and same-experiment evidence:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`
- `[local file: 221_Srgap3.csv]`
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime `profile_neighbors` over the 20 most relevant observed Slit/Robo and Rac/Cdc42/RhoGAP candidate perturbations

External biology:

- PubMed literature searches for `MEGAP/SRGAP3`, `WRP`, `Slit-Robo GAP`, `WAVE-1`, and `Rac1`.
- Endris et al. 2002, PNAS, DOI `10.1073/pnas.162241099`, PMID `12195014`: identified MEGAP/SRGAP3 as a brain-expressed RhoGAP disrupted in an intellectual-disability-associated 3p25 case and linked it to Slit-Robo biology.
- Wong et al. 2001, Cell, DOI `10.1016/s0092-8674(01)00530-x`, PMID `11672528`: showed Robo intracellular domains recruit srGAP-family RhoGAPs and that Slit-Robo signaling uses srGAP/Cdc42 signaling for repulsion of migratory neurons.
- Soderling et al. 2007, Journal of Neuroscience, DOI `10.1523/JNEUROSCI.3209-06.2006`, PMID `17215396`: connected WRP/SRGAP3 with WAVE-1 actin signaling and showed the complex regulates spine density, synaptic plasticity, and memory.
- Endris et al. 2011, Journal of Cell Science, DOI `10.1242/jcs.077081`, PMID `22159416`: reported SrGAP3/MEGAP at membrane protrusions and described Rac-dependent effects on lamellipodia.
- Waltereit et al. 2012, FASEB Journal, DOI `10.1096/fj.11-202317`, PMID `22820399`: found neurodevelopmental, Rac1, white-matter, spine, and behavioral phenotypes in germline Srgap3 knockout mice.
- Bacon, Endris and Rappold 2012, Mechanisms of Development, DOI `10.1016/j.mod.2012.10.005`, PMID `23127797`: reviewed Srgap3 as an actin and Rac1 regulator in neurite, dendrite, and Slit-Robo processes.
- Zhang et al. 2014, Asian Pacific Journal of Tropical Medicine, DOI `10.1016/S1995-7645(14)60106-1`, PMID `25149377`: reported Slit1/Robo2/SrGAP3 coupling to Rac1 in postnatal rat dorsal-root-ganglion neurite outgrowth.

# Same-experiment calibration

The focal training-count table has 1,674 non-held-out perturbations. The count distribution is zero-heavy:

| statistic | value |
| --- | ---: |
| mean | 14.05 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |
| nonzero fraction | 28.0% |

The mean is dominated by a small number of very broad responses such as `Uba5`, `Tpr`, `Sin3a`, spliceosome, proteasome, and chromatin perturbations. That tail is not a good prior for a postsynaptic/guidance RhoGAP such as Srgap3.

I queried the parquet only in `151 TH Prkcd Grin2c Glut` for Slit/Robo, netrin/UNC5, Rac/Cdc42, WAVE/PAK/LIMK, and RhoGAP/RhoGEF comparators. The focal rows have 17,259 measured genes per target. The query was:

```sql
select gene_target,
       sum(case when pvals_adj < 0.05 then 1 else 0 end) as n_degs,
       min(pvals_adj) as min_padj
from read_parquet('training_de_all_cell_groups.parquet')
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

The most direct observed analogs were all absent, target-self-only, or nearly absent in the focal cell group:

| neighborhood | observed perturbations | focal `n_degs` |
| --- | --- | ---: |
| Slit/Robo | Robo1, Robo2, Robo4, Slit2 | 1, 0, 0, 0 |
| Netrin/UNC5/axon guidance | Dcc, Neo1, Dscam, Unc5c, Unc5d | 0, 0, 0, 1, 0 |
| Rac/Cdc42 and Rac GEFs | Cdc42, Rac1, Tiam1, Kalrn | 1, 0, 0, 0 |
| Rac/EphB/PAK/WAVE/LIMK | Ephb2, Cfl2, Pak1, Pak2, Pak3, Limk1, Cyfip1, Cyfip2 | 0, 0, 1, 0, 0, 0, 0, 1 |
| GAP/GEF and actomyosin relatives | Arhgap18, Arhgap32, Arhgef9, Myo9a, Diaph2, Fmn1, Fmn2, Dock3, Rala | 0, 0, 1, 0, 0, 0, 0, 0, 0 |

For the one-DEG members, the DEG was the perturbed transcript itself:

| perturbation | direct target log2FC | direct target `pvals_adj` | `n_degs` |
| --- | ---: | ---: | ---: |
| Robo1 | -0.538 | 2.7e-06 | 1 |
| Unc5c | -0.536 | 2.0e-04 | 1 |
| Cdc42 | -0.593 | 8.6e-05 | 1 |
| Pak1 | -0.599 | 5.0e-08 | 1 |
| Cyfip2 | -0.489 | 4.4e-11 | 1 |
| Arhgef9 | -0.571 | 3.7e-08 | 1 |

By contrast, many close analogs either had weak target-mRNA changes or no target self signal after multiple testing:

| perturbation | direct target log2FC | direct target `pvals_adj` | `n_degs` |
| --- | ---: | ---: | ---: |
| Arhgap32 | -0.333 | 0.607 | 0 |
| Dscam | -0.419 | 0.090 | 0 |
| Kalrn | -0.267 | 0.424 | 0 |
| Dock3 | -0.430 | 0.709 | 0 |
| Neo1 | -0.447 | 0.792 | 0 |
| Robo2 | -0.407 | 1.000 | 0 |
| Slit2 | -0.128 | 1.000 | 0 |
| Rac1 | 0.161 | 1.000 | 0 |

Srgap3 itself was present among measured genes in the focal signatures, but none of the above candidate perturbations detectably moved it; every candidate row for measured `Srgap3` had adjusted `p=1`. That does not prove Srgap3-targeting guides will fail to lower Srgap3 RNA, but it argues against a broader Srgap3-centered compensatory RNA module.

The Distributed Agents runtime comparison over 20 directly relevant candidates used whole-profile Pearson/cosine similarity plus signed positive and negative tails among the top 200 features. It did not reveal an FDR-level module that cut across Slit/Robo and Rac/Cdc42/RhoGAP genes. The few weak whole-profile similarities among zero-count signatures were not accompanied by shared significant genes, so I treated the candidate cohort as a collection of flat or self-only readouts rather than as a robust latent Srgap3-like state.

# Corpus evidence

The Distributed Agents same-experiment corpus had no direct `Srgap3` findings or Srgap3-containing claims, so there was no within-corpus Srgap3 readout to copy.

Relevant same-experiment higher-order claims were:

- Claim `claim:a457807c15e3a9a8f204`, high confidence: represented P16 postmitotic neuronal axon-guidance perturbations spanning netrin/DCC/UNC5/Neo1/DSCAM and Slit/Robo comparators produced null, near-null, or non-overlapping nuclear RNA surfaces rather than a persistent neuronal soma guidance module.
- Claim `claim:1aeabad1e41e30f971bc`, high confidence: represented Rac/Cdc42-linked actin-cytoskeleton signaling perturbations, including `Cdc42`, `Rac1`, `Tiam1`, `Kalrn`, `Ephb2`, `Limk1`, and `Cfl2`, were transcriptionally buffered rather than forming a recurrent pathway-wide nuclear mRNA module.
- Claim `claim:767b4eb73b8456c34ded`, moderate confidence: represented Rho-family cytoskeletal and myosin-adjacent perturbations, including `Arhgap18`, `Cdc42`, and `Myo9a`, did not collapse into a shared postnatal neuronal mRNA program.

Those claims were a better match to Srgap3 than the global screen average because Srgap3 is a Slit-Robo-family RhoGAP acting through Rac/Cdc42 and actin remodeling, not a core splicing, proteasome, chromatin, ER-stress, or translation factor.

# Srgap3 reasoning

Srgap3 encodes a Slit-Robo GAP family protein with an F-BAR membrane-remodeling domain, a RhoGAP domain, and an SH3 domain. Literature places it at the interface of Robo/srGAP signaling, Rac1/Cdc42 regulation, WAVE-1 actin remodeling, membrane protrusions, neurite outgrowth, dendritic spine morphology, and neurodevelopmental phenotypes. The external evidence therefore says that Srgap3 is biologically relevant in neurons, but the Perturb-seq endpoint is nuclear mRNA in a postnatal, sparse, acute KO experiment.

The most mechanistically appropriate training perturbations do not show a broad focal transcriptome response:

- The Slit/Robo side is flat: `Slit2`, `Robo2`, and `Robo4` each have 0 DEGs; `Robo1` has exactly 1 DEG, Robo1 itself.
- The axon-guidance receptor context is flat: `Dcc`, `Neo1`, `Dscam`, and `Unc5d` have 0; `Unc5c` has exactly 1, Unc5c itself.
- The Rac/Cdc42 pathway is flat or self-only: `Rac1`, `Tiam1`, `Kalrn`, `Limk1`, `Ephb2`, and `Cfl2` have 0; `Cdc42` has only Cdc42 itself.
- The WAVE/PAK/Rho-regulatory neighborhood is also flat or self-only: `Cyfip1`, `Pak2`, `Pak3`, `Arhgap18`, `Arhgap32`, and `Myo9a` have 0; `Cyfip2`, `Pak1`, and `Arhgef9` have one self DEG apiece.

Given that pattern, the most likely biological interpretation is that Srgap3 loss can affect actin, protrusions, spines, and Rac1 activity without causing a soma-wide nuclear RNA state in this cell group over this time window. The remaining chance of `n_degs = 1` is a target-self Srgap3 transcript effect, not an inferred pathway program. I set the integer point prediction to `0` because most close zero-count counterexamples lack even a self DEG, and because the exact self effect is dominated by guide potency, baseline transcript detection, and statistical power rather than by Srgap3 pathway biology.

# Limits

- Srgap3 had no held-in paralog in the supplied focal counts. `Srgap1` and `Srgap2` were not available as direct training perturbations, so the prediction transfers through Slit/Robo receptors, Rac/Cdc42 signaling, WAVE/PAK/LIMK, and other Rho regulators rather than through a same-family knockout.
- The strongest Srgap3 biology in the literature is protein localization, actin remodeling, neurite and dendritic-spine morphology, Rac1-GTP biochemistry, and chronic germline-animal phenotypes. The screen readout is acute nuclear snRNA-seq in postmitotic neurons; structural neurite changes or synaptic physiology could be missed even when biologically real.
- The focal cell group is a thalamic glutamatergic population. Some Srgap3 functions have been demonstrated in cortical, hippocampal, dorsal-root-ganglion, fibroblast, or transformed cell systems, which are imperfect matches.
- The difference between predicting 0 and 1 is mostly whether Srgap3's own transcript crosses FDR 0.05. The same-experiment analogs show that one-gene self responses happen, but they are not guaranteed for moderately expressed cytoskeletal and guidance genes.
