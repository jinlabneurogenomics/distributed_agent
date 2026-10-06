# Nup93 DEG-count prediction trace

## Question and interpretation

The requested held-out target file contains one perturbation:

```tsv
target_name
Nup93
```

I interpreted `predicted_n_degs` as the number of measured genes in `151 TH Prkcd Grin2c Glut` cells with `pvals_adj < 0.05`, exactly matching the endpoint in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. I preserved the requested target name and order. I did not exclude the target transcript itself from the count, because the supplied training endpoint is the raw count of FDR-significant measured genes.

## Sources used

- The supplied training DEG-count CSV for exact focal-cell counts of the 1,674 observed non-held-out targets.
- The supplied all-cell differential-expression parquet for focal-cell significant DEG sets and effect directions.
- The Distributed Agents internal same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`. This release had no `Nup93` finding or claim, but it did contain curated reports for observed comparators including `Tpr`, `Tnpo3`, `Thoc1`, `Ranbp2`, and `Xpo7`.
- NCBI PubMed literature for nuclear pore and RNA-export biology:
  - Grandi et al., 1997, PMID 9348540, DOI `10.1091/mbc.8.10.2017`: vertebrate Nup93/Nic96 forms a NUP205-containing complex and is required for correct NPC assembly.
  - Vollmer and Antonin, 2014, PMID 24572986, DOI `10.1515/hsz-2013-0285`: the Nup93/Nic96 complex is an essential scaffold linking the nuclear membrane and central pore.
  - Sonawane et al., 2020, PMID 33085133, DOI `10.1002/pro.3983`: the N-terminal region of mammalian Nup93 anchors central-channel Nup62/Nup58/Nup54 assemblies.
  - Braun et al., 2016, PMID 26878725, DOI `10.1038/ng.3512`: disease variants in `NUP93`, `NUP205`, and `XPO5` cause steroid-resistant nephrotic syndrome; NUP93 and NUP205 interact physically.
  - Zanni et al., 2019, PMID 30741391, DOI `10.1007/s12311-019-1010-5`: biallelic NUP93 variants can cause congenital ataxia, showing nervous-system relevance for NUP93 hypomorphs.
  - Aksenova et al., 2020, PMID 32917881, DOI `10.1038/s41467-020-18266-2`: acute TPR depletion causes transcriptomic changes related to NXF1 and TREX-2 mRNA export.
  - Kosar et al., 2021, PMID 34168151, DOI `10.1038/s41467-021-24224-3`: TPR connects mRNA export/RNA processing to genome stress through GANP/TREX-2.
  - Snow and Paschal, 2014, PMID 24563354, DOI `10.1007/978-1-4899-8032-8_14`: TPR is a nuclear-basket nucleoporin with transport, chromatin, transcriptional, and mitotic roles.
  - Toyama et al., 2013, PMID 23993091, DOI `10.1016/j.cell.2013.07.037`: scaffold nucleoporins in brain are exceptionally long-lived and only slowly exchanged, which is relevant to an acute postmitotic perturbation.

## Dataset computations

I first checked the focal training counts for nuclear-pore and nuclear-transport targets. In the exact `151 TH Prkcd Grin2c Glut` endpoint, the most relevant observed counts were:

| observed perturbation | focal `n_degs` | interpretation |
|---|---:|---|
| `Tpr` | 1768 | nuclear-basket nucleoporin; strong visible RNA/nuclear-logistics state |
| `Tnpo3` | 618 | nuclear importer for SR-domain splicing factors; converges with `Tpr` |
| `Thoc1` | 303 | THO/TREX mRNP-biogenesis and export factor |
| `U2af2` | 828 | spliceosome / RNA processing |
| `Cdc40` | 624 | spliceosome-associated comparator |
| `Prpf6` | 454 | spliceosome-associated comparator |
| `Snrnp70` | 213 | spliceosome-associated comparator |
| `Hnrnpu` | 733 | nuclear RNP comparator |
| `Ranbp2` | 0 | cytoplasmic-filament nucleoporin; focal-cell null counterexample |
| `Xpo7` | 0 | exportin; focal-cell null counterexample |
| `Kpna3` | 0 | importin-alpha; focal-cell null counterexample |

To make sure that the comparison used the endpoint itself rather than whole-profile artifacts, I extracted all focal rows satisfying:

```python
group_name == "151 TH Prkcd Grin2c Glut"
pvals_adj < 0.05
```

This produced 23,526 significant focal rows across 469 non-held-out targets. I then intersected the `Tpr` focal significant set with every other observed target's focal significant set. `Tpr` had 1,768 focal DEGs. Its strongest FDR-set overlaps were broad stress/RNA states, not other NPC scaffold genes:

| target | focal `n_degs` | overlap with the 1768 `Tpr` focal DEGs |
|---|---:|---:|
| `Uba5` | 2677 | 742 |
| `Sin3a` | 1433 | 284 |
| `Tnpo3` | 618 | 265 |
| `Psmb4` | 742 | 261 |
| `U2af2` | 828 | 252 |
| `Rnpc3` | 868 | 243 |
| `Ufc1` | 572 | 242 |
| `Cdc40` | 624 | 216 |
| `Hnrnpu` | 733 | 191 |
| `Prpf6` | 454 | 167 |
| `Thoc1` | 303 | 114 |
| `Snrnp70` | 213 | 82 |
| `Matr3` | 149 | 37 |
| `Ranbp2` | 0 | 0 |
| `Xpo7` | 0 | 0 |

This was consistent with the Distributed Agents same-experiment corpus: the curated `Tpr` report calls its data-driven neighbors proteasome, UFMylation, and RNA-export/splicing perturbations rather than another nucleoporin; the `Tnpo3` report specifically lists `Tpr`, `U2af2`, `Cdc40`, `Rnpc3`, `Snrnp70`, and `Thoc1` as same-direction nuclear RNA-processing neighbors, while `Kpna3`, `Xpo7`, and `Ranbp2` did not act as focal phenocopies.

I did not use unconstrained whole-profile Pearson ranking for the point estimate: in this sparse DE table it can make flat perturbations appear spuriously similar because extreme positive/negative rank tails dominate the correlation even when the candidate has no FDR-significant genes. The FDR-set overlap was a better match to the endpoint being predicted.

## Target-specific reasoning

### Nup93

`Nup93` was absent from both the training DEG-count file and the DE parquet as a perturbation target, and the Distributed Agents corpus had no held-out `Nup93` claim. I therefore treated all within-dataset comparisons as analogs or counterexamples, not as direct measurements.

Mechanistically, NUP93 is a core NPC scaffold, not a peripheral mRNA-export factor. The external literature puts it in the Nup93/Nic96 inner-ring complex with NUP205 and other large scaffold nucleoporins, required for nuclear pore assembly and for anchoring the central transport channel. Disease work also shows that NUP93/NUP205 perturbation can disrupt NPC assembly and specific transcription-factor traffic. Those facts argue that complete Nup93 loss is potentially severe.

The closest observed positive analog by organelle is `Tpr`: it is an NPC component, had 1,768 focal DEGs, and its focal response overlapped strongly with `Tnpo3`, `U2af2`, `Cdc40`, `Prpf6`, and `Thoc1`. Its top focal hits included `Xpo1` up and multiple RNA-processing genes down, a pattern consistent with TPR's known TREX-2/NXF1 role. However, `Tpr` is a nuclear-basket protein whose depletion directly perturbs mRNA export and transcript handling on existing NPCs; that is not the same as an inner-ring assembly subunit.

The most important within-dataset counterexamples were `Ranbp2`, `Xpo7`, and `Kpna3`. `Ranbp2` is another nucleoporin and produced 0 focal DEGs; `Xpo7` and `Kpna3` are nuclear-transport genes and also produced 0 focal DEGs. The observed screen therefore does not support a rule that any acute nuclear pore or transport hit yields a `Tpr`-scale focal transcriptome. The focal `Tpr` state instead sits next to RNA maturation, spliceosome, proteostasis, and UFMylation responses.

The assay timing further pushed the prediction downward. NUP93 is a structural NPC scaffold expected to be much slower-turnover than TPR-like peripheral basket machinery; long-lived brain NPC proteins are inefficiently replenished over adult life. In a P16-to-P37/44 postmitotic CRISPR design, existing NPCs can therefore buffer a loss of new `Nup93` synthesis, while a dividing cell or embryonic germline deletion would require de novo pore assembly and should be much more sensitive. That makes congenital ataxia and nephrotic-syndrome genetics informative about NUP93 importance but too strong a prior for the acute survivor-conditioned neuronal snRNA endpoint.

I predict `Nup93` will be transcriptionally buffered in the focal thalamic glutamatergic population at the FDR 0.05 DEG-count threshold. I used `Tpr` and RNA-export/splicing perturbations as the nonzero upper-bound evidence, but the same-experiment nulls for `Ranbp2`, `Xpo7`, and `Kpna3`, plus the expected stability of core scaffold NPCs in postmitotic neurons, outweighed that analogy. The point estimate is therefore **0 DEGs** rather than a weak singleton response or a broad `Tpr`-like response.

## Limits

The main limitation is the lack of a measured Nup93-complex target in the training set: `Nup205`, `Nup188`, `Nup155`, `Nup35`, `Nup62`, `Nup54`, `Nup58`, and `Ndc1` were not focal training perturbations, so `Tpr` and `Ranbp2` are both imperfect NPC analogs. I also could not observe NUP93 protein depletion, nuclear transport rates, NPC density, cell survival, or editing genotype. The prediction extrapolates from dynamic peripheral nuclear-pore and RNA-export targets to a core scaffold whose turnover in juvenile thalamic neurons is unknown. A real 1-gene self-transcript call or a delayed scaffold-depletion stress response would not be surprising; I only predict that neither will cross the supplied FDR 0.05 count threshold in this cell group.
