# Sp4 prediction trace

## Question and scope

The requested held-out perturbation list contains one target:

```tsv
target_name
Sp4
```

I interpreted `n_degs` as the count of measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, with positive log fold changes meaning higher expression after the knockout. `Sp4` was held out completely, so I treated all `Sp4` rows as unavailable and transferred from non-held-out perturbations only.

The final integer for `Sp4` is therefore an assay-calibrated point prediction, not a measure of Sp4 importance, viability, or editing strength.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene DE statistics for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed focal-cell DEG counts for the same non-held-out perturbations.
- `220_Sp4.csv`: the ordered held-out target list for this run.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`, including Klf9, Klf7, Grin1, Nrf1, Esrra, and Zbtb7a perturbation findings.
- Distributed Agents runtime profile comparison over the focal cell group for `Klf9`, flat KLF-family counterexamples, `Sin3a`/`Zbtb7a`/`Smarcc2`, and `Sp4`-nominated NMDAR and mitochondrial comparators.
- PubMed-indexed literature on Sp4 neuronal function and direct targets:
  - Supp et al. 1996, DOI `10.1006/dbio.1996.0134`, PMID `8660867`: cloned mouse `Sp4`, showed CNS-enriched developmental expression, adult brain expression, and postnatal viability and growth phenotypes in null mice.
  - Ramos et al. 2007, DOI `10.1073/pnas.0701946104`, PMID `17535924`: Sp4 controls dendritic patterning and activity-dependent pruning in cerebellar granule neurons.
  - Priya et al. 2013, DOI `10.1016/j.bbamcr.2013.07.002`, PMID `23871830`: Sp4 functionally regulates `Grin1`, `Grin2a`, and `Grin2b` promoters in neurons.
  - Sun et al. 2014, DOI `10.1002/dneu.22212`, PMID `25045015`: a Sp4-Nwk2/Fchsd1-NMDAR1 pathway controls dendrite patterning and NMDAR1 surface expression.
  - Saia et al. 2014, DOI `10.1111/jnc.12657`, PMID `24475768`: NMDA receptor signaling regulates Sp4 phosphorylation.
  - Johar et al. 2013, DOI `10.1111/jnc.12433`, PMID `24032355`: Sp4 regulates all cytochrome-c-oxidase subunit genes and mitochondrial transcription factors in primary neurons.
  - Priya et al. 2014, DOI `10.1016/j.bbamcr.2014.02.008`, PMID `24576410`: Sp4 regulates `Gria2`.
  - Nair et al. 2015, DOI `10.1016/j.bbamcr.2015.10.005`, PMID `26469128`: Sp4 regulates `Gabra1` and `Gabra2`.

## Computational checks

I read the training count table and confirmed that the focal endpoint is very sparse overall:

- 1,674 observed non-held-out perturbations.
- Median `n_degs = 0`.
- 75th percentile `n_degs = 1`.
- 90th percentile `n_degs = 2`.
- Only 469 of 1,674 targets had any focal-cell DEG.

To extract target-specific expression-pattern evidence without loading the full multi-cell-type parquet, I scanned only the focal cell group and a selected target set:

```python
scanner = ds.dataset(path, format="parquet").scanner(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj"],
    filter=(
        pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
    ) & pc.field("gene_target").isin(targets),
)
```

This recovered the expected `n_degs` values from the training-count CSV and the actual FDR<0.05 overlap among analog signatures.

## Within-dataset analogs and counterexamples

| training perturbation | 151 TH Prkcd Grin2c Glut `n_degs` | relevance to `Sp4` |
| --- | ---: | --- |
| `Klf9` | 19 | Closest observed small neuronal SP/KLF-like C2H2/GC-rich DNA-binding response. The same-experiment corpus reports a 19-gene, mostly up-regulated, focal-cell-restricted response and convergence with `Sin3a`, `Zbtb7a`, and `Smarcc2`. In the exact FDR<0.05 focal set, `Klf9` had 18 up and 1 down DEG, and shared 13 DEGs with `Sin3a` and 12 with `Zbtb7a`, nearly all in the up direction: for example `Wsb1`, `Rasgrp2`, `Pld3`, `Dzip1`, `Maged2`, `Mest`, `Hcn3`, `Phf1`, `Plxna3`, `Aplp1`, `Plppr3`, and `Vgf` across the two overlaps. This shows that a small transcription-factor derepression module is detectable in the focal cell group. |
| `Klf7` | 1 | Related SP/KLF zinc-finger factor and an explicit Klf9 counterexample in the Distributed Agents corpus. The only FDR<0.05 gene was `Tuba1a` down. This supports the idea that neuronal KLF-family membership alone usually does not imply a broad response in this assay. |
| `Klf13`, `Klf11`, `Klf12`, `Klf1` | 0 each | `Klf13` is a Klf9 paralog but was flat in the focal group, and the corpus explicitly notes that the represented KLF-family perturbations were paralog-specific rather than a generic knockdown state. |
| `Sp7` | 0 | The only represented Sp-family symbol in the training endpoint. It is an osteoblast-lineage Sp factor rather than a neuronal Sp4 paralog, so it is mainly a lineage/off-axis counterexample. |
| `Zbtb7a` | 841 | A broad C2H2/chromatin transcription-factor response that shares the Klf9 up-regulated module. Its size shows that C2H2 TFs can be very detectable, but the corpus reports a broad endomembrane/lysosome and neurosecretory response whose nearest positive neighbors were UFMylation/proteostasis nodes, not SP/KLF factors, so I did not use 841 as a Sp4-scale estimate. |
| `Sin3a` | 1433 | Shares 13 exact Klf9 FDR<0.05 coordinates in the same direction and is a strong chromatin corepressor perturbation. Its count is much larger than any reasonable Sp4 single-TF expectation. |
| `Smarcc2` | 185 | SWI/SNF component and Klf9-associated comparator in the corpus. It overlapped only one `Klf9` FDR<0.05 gene, so it is weaker direct numeric evidence than `Klf9`. |
| `Grin1` | 89 | Relevant because Sp4 can regulate NMDAR biology. The same-experiment `Grin1` response is a focal-cell-biased synaptic/homeostatic state, but the corpus says other NMDA subunits did not phenocopy `Grin1`; `Grin2a`, `Grin2b`, `Grin2d`, and `Grin3a` had 1, 2, 0, and 0 focal DEGs. The exact `Klf9`-`Grin1` FDR overlap was only `Mest`, so I treated `Grin1` as a pathway boundary rather than a direct proxy. |
| `Nrf1`, `Esrra` | 138, 57 | Relevant because Sp4 has been reported to regulate cytochrome-c-oxidase and mitochondrial transcription-factor genes in primary neurons. In the focal dataset the Distributed Agents corpus found that the ERR/PGC/PPAR/NRF network was node-specific: `Nrf1` did not phenocopy `Esrra`, and PPAR/ESRR relatives were flat or divergent. Exact overlap with `Klf9` was only `Pld3`/`Ttc3` for `Nrf1` and none for `Esrra`. |
| `Atp1a3`, `Atp1a1`, `Gria2`, `Gabra1`, `Gabra2` | 80, 1, 0, 1, 0 | These cover selected ion-pump, AMPA, and GABA-A targets that Sp4 can regulate in the literature. Their training counts show that only `Atp1a3` has a material focal-cell response, while `Atp1a1`, `Gria2`, `Gabra1`, and `Gabra2` are flat or singletons. That argues against a broad shared Sp4-regulated receptor/ion-homeostasis signature in this particular thalamic glutamatergic readout. |

The runtime profile comparison over the same focal rows gave the same qualitative boundary: `Klf9` shares many FDR DEGs with `Sin3a` and `Zbtb7a`, but only two FDR genes with `Nrf1`, one with `Grin1`, none with `Esrra`, and nothing material with `Sp7` despite broad whole-profile correlations that also appeared for flat nodes. I therefore gave exact FDR overlap and biological mechanism more weight than whole-vector correlation.

## Target-specific prediction

### `Sp4`

`Sp4` is biologically plausible as nonzero: it is a neuronal Sp-family transcription factor, mouse loss perturbs postnatal CNS phenotypes, and the literature places it upstream of dendrite patterning, NMDA receptor signaling, AMPAR/GABA-A receptor transcription, and mitochondrial oxidative-phosphorylation genes. Those mechanisms are aligned with neurons and with a glutamatergic thalamic subtype, not an off-axis lineage.

I nevertheless expect a sparse response rather than a Klf9-or-larger response for four reasons.

First, the experimental perturbation is acute postnatal mosaic CRISPR with modest mean target RNA depletion, whereas many Sp4 papers used germline hypomorphs, cultured neurons, or shRNA/overexpression. Sp4 effects on NR1 surface protein through `Nwk2` are partly post-transcriptional, which can be missed by a nuclear RNA DEG endpoint.

Second, the direct receptor and ion-homeostasis analogs are mostly weak in this exact dataset. `Gria2`, `Gabra2`, and `Atp1a1` perturbations had no or one focal DEG, and NMDA-subunit perturbations did not converge with each other. `Grin1` is a real 89-DEG state, but it was specific to the obligatory receptor subunit and shared only `Mest` with the Klf9-like TF response.

Third, mitochondrial transcription in 151 cells is detectable but node-specific. `Nrf1` and `Esrra` were 138- and 57-DEG perturbations, yet their focal signatures were distinct from each other and from `Klf9`. Acute `Sp4` loss should not be assumed to phenocopy direct NRF1/ERRalpha loss.

Fourth, SP/KLF-family evidence inside the assay is mostly buffered. `Klf9` is the strongest nearby small-TF anchor at 19 DEGs, but `Klf7` had 1 DEG, `Klf13`, `Klf11`, `Klf12`, and `Klf1` had 0, and the only training Sp-family member, `Sp7`, had 0. Sp4 has stronger neuronal prior than `Sp7` and a better functional prior than the flat blood/off-axis KLFs, so I predict nonzero, but below `Klf9`.

I used a low integer in the 1-5 range and chose `3`: enough to represent a few activity/synaptic or mitochondrial transcripts crossing FDR in `151 TH Prkcd Grin2c Glut`, but much closer to the empirical sparse-TF baseline than to the 57-138 DEG mitochondrial/NMDAR responses.

## Limits and extrapolation

- There is no same-experiment `Sp4` or `Sp1`/`Sp3` perturbation, so the closest within-dataset analog is `Klf9`, not a true paralog.
- The direct Sp4 literature was mostly outside postnatal thalamic glutamatergic neurons and often used cultured neurons, germline alleles, or stronger knockdown than this sparse AAV CRISPR design.
- The Distributed Agents same-experiment corpus had no held-out `Sp4` claim; all corpus support is from training perturbations used as analogs or boundaries.
- DEG count is power-dependent. A prediction of `3` should be read as "barely nonzero and assay-fragile", not as confidence that exactly three biological pathways respond.
