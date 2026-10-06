# Irf6 held-out DEG-count prediction

## Question and resolved ambiguities

The requested endpoint is the number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after CRISPR loss of each held-out target in `151 TH Prkcd Grin2c Glut` neurons.  The only requested target in `113_Irf6.csv` is `Irf6`, and it is absent from both the focal-cell training count CSV and the all-cell-group DE parquet as a perturbation target.

I interpreted the prediction as an assay-calibrated focal-cell point count, not a generic estimate of IRF6 biological importance.  Therefore zero is a legitimate prediction when the closest measured postnatal neuronal analogs are FDR-null, even though germline or epithelial Irf6 disruption is severe.

## Sources used

- Exact observed endpoint for non-held-out perturbations: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Raw same-experiment DE signatures: `training_de_all_cell_groups.parquet`, queried at `group_name == "151 TH Prkcd Grin2c Glut"` for biologically nominated training perturbations.
- Same-experiment interpretation layer: Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`.  It had no `Irf6` target-context records, but it contained curated reports for relevant measured analogs including `Trp63`, `Grhl2`, `Chuk`, `Pbx1`, `Fgfr1`, `Fgfr2`, `Irf1`, and `Irf2`.
- External literature found through NCBI PubMed E-utilities:
  - Kondo et al. 2002, Nature Genetics, DOI `10.1038/ng985` / PMID `12219090`.
  - Richardson et al. 2009, Human Molecular Genetics, DOI `10.1093/hmg/ddp201` / PMID `19439425`.
  - Thomason et al. 2010, Journal of Clinical Investigation, DOI `10.1172/JCI40266` / PMID `20424327`.
  - Moretti et al. 2010, Journal of Clinical Investigation, DOI `10.1172/JCI40267` / PMID `20424325`.
  - Hammond, Dixon and Dixon 2017, Seminars in Cell & Developmental Biology, DOI `10.1016/j.semcdb.2017.08.021` / PMID `28803895`.
  - Kousa et al. 2017, Journal of Dental Research, DOI `10.1177/0022034517719870` / PMID `28732181`.
  - Kousa, Moussa and Schutte 2017, Developmental Dynamics, DOI `10.1002/dvdy.24537` / PMID `28643456`.

## Computational checks over the training data

I used the scalar training CSV as the exact `n_degs` source for focal-cell calibration.  The 1,674 visible targets are strongly zero-inflated in this cell group: 1,205 targets, or 72.0%, have `n_degs = 0`; 88.5% have `n_degs <= 1`; 90.3% have `n_degs <= 2`; and only 43 targets, 2.6%, have 100 or more DEGs.

I then queried the parquet only for the focal group and the candidate analog perturbations.  The selected focal signatures each contained 17,259 measured genes.  For the primary analogs, there was no hidden near-threshold expression program:

| training perturbation | focal `n_degs` | best focal BH q value | why it was compared with `Irf6` |
|---|---:|---:|---|
| `Trp63` | 0 | 1.000 | p63 directly activates an upstream IRF6 enhancer and forms an epithelial proliferation/differentiation feedback loop with IRF6. |
| `Grhl2` | 0 | 1.000 | Grainyhead factor in the epithelial/periderm differentiation axis; `Grhl3`, the closer Van der Woude partner, was not in the training target universe. |
| `Chuk` | 0 | 0.727 | IKKalpha/NF-kappaB-side periderm and ectodermal disease node with similar craniofacial/skin developmental context to IRF6/RIPK4. |
| `Pbx1` | 0 | 1.000 | Member of a PBX-WNT-p63-IRF6 craniofacial developmental network; indirect upstream comparator. |
| `Fgfr1` | 0 | 1.000 | FGF/RTK signaling can intersect with Irf6/Grhl3 in periderm; indirect upstream comparator. |
| `Fgfr2` | 0 | 1.000 | FGFR paralog and craniofacial RTK comparator; indirect and allele/stage-shifted. |
| `Irf1` | 0 | 1.000 | IRF-family transcription factor; useful mainly as a counterexample because mammalian IRF6 is not a basal interferon-response IRF. |
| `Irf2` | 0 | 1.000 | IRF-family counterexample. |
| `Irf3` | 0 | 1.000 | IRF-family counterexample. |
| `Irf5` | 0 | 0.789 | IRF-family counterexample. |
| `Irf8` | 0 | 0.121 | IRF-family counterexample. |
| `Irf9` | 0 | 1.000 | IRF-family counterexample. |

Second-ring same-pathway checks were also quiet in the focal count table: `Eda`, `Map3k7`, `Nfkb1`, `Rel`, `Traf3`, `Tnfrsf1a`, `Ovol2`, `Tfcp2`, `Ubp1`, `Fgf1`, `Fgfr3`, `Fgfrl1`, `Meis1`, `Meis2`, `Pbx3`, `Pknox2`, `Hoxb8`, `Trp53`, and `Trp73` all had `n_degs = 0`.  I did not treat the string-neighbor `Irf2bpl` as an IRF-family analog; it is mechanistically unrelated here.

## Same-experiment corpus evidence

The Distributed Agents corpus returned no `Irf6` Finding, Claim, or explicit related-target paths, so there was no direct same-experiment Irf6 semantic record to transfer.

For `Trp63`, the corpus summarized a pan-measured neuronal null in the acute P16-to-P37/44 CRISPR assay and specifically reported absence of p53/PUMA apoptotic, precursor-loss, and epithelial target programs.  This is a close boundary for `Irf6`: a transcription factor can be central in embryonic epithelia without maintaining a detectable basal mRNA program in mature NeuN-positive neurons.

For `Grhl2`, the corpus reported that its canonical epithelial-barrier and EMT-suppression program was absent from every measured neuronal group and that represented GRHL2-adjacent regulators did not phenocopy it.  This is relevant because the best external biological placement for IRF6 is a TP63/GRHL3/periderm regulatory network, yet the represented Grainyhead member was silent in the focal group.

For `Chuk`, the corpus reported no robust downstream response and a missing canonical NF-kappaB feedback/inflammatory/survival transcript panel in postnatal neurons.  It also placed `Nfkb1`, `Rel`, `Traf3`, and `Tnfrsf1a` as shared-null neighbors, arguing that ectodermal NF-kappaB/IKK biology is not tonically active in this unchallenged neuronal assay.

For `Irf1` and `Irf2`, the corpus showed that represented IFN receptor, STAT, NF-kappaB, TLR, RNA-sensing, and IRF-family perturbations are flat or singleton-only in basal NeuN-enriched nuclei and do not form a coherent interferon/ISG/MHC module.  These IRFs are not close developmental analogs of IRF6, but they guard against over-predicting a response just because the held-out symbol is an IRF.

## Irf6 biological rationale and prediction

External genetics places IRF6 in epithelial morphogenesis rather than in an autonomous postmitotic neuronal pathway.  Kondo et al. identified IRF6 mutations as causes of Van der Woude and popliteal pterygium syndromes and reported strong embryonic expression in palate, tooth buds, hair follicles, genitalia, and skin.  Richardson et al. showed that Irf6 is required for oral epithelial differentiation and periderm maintenance.  Thomason et al. and Moretti et al. connected IRF6 to p63 during palate development and keratinocyte proliferation/differentiation.  Hammond et al. reviewed the p63-controlled periderm program in which IRF6, CHUK, SFN, RIPK4, and GRHL3 prevent pathological epithelial adhesions.  Kousa et al. connected IRF6 to SPRY4/RTK signaling and GRHL3 in periderm.

That mechanism points to `Trp63`, `Grhl2`, `Chuk`, `Pbx1`, and `Fgfr1/Fgfr2` as the most informative training analogs available, and every one of those perturbations is FDR-null in the requested thalamic glutamatergic group.  The corpus-level reports for `Trp63`, `Grhl2`, and `Chuk` additionally argue that the nulls are coherent developmental/lineage boundaries rather than isolated failed comparisons.  The all-zero IRF-family perturbations make an interferon-like alternative unlikely.

I therefore predict that knocking out `Irf6` in the P16 sparse mosaic whole-brain NeuN-positive assay will land on the zero-count mass in `151 TH Prkcd Grin2c Glut`, with no measured gene passing BH FDR 0.05:

| target | predicted `n_degs` |
|---|---:|
| `Irf6` | 0 |

## Limits and extrapolations

- `Irf6` itself had no Distributed Agents corpus entry in this release, so the same-experiment semantic evidence comes entirely from measured analogs and counterexamples.
- Several ideal comparators were not visible as focal-cell training targets, especially `Grhl3`, `Tfap2a`, `Ripk4`, `Sfn`, `Spry4`, `Prkci`, and `Krt14`.
- `Grhl2`, `Chuk`, `Pbx1`, and the FGFRs are pathway neighbors, not IRF6 paralogs or direct substitutes.  Their zero counts support a lineage/stage boundary, not molecular equivalence.
- The known IRF6 phenotypes are embryonic, epithelial, adhesion, and periderm phenotypes.  The assay perturbs juvenile postmitotic NeuN-positive nuclei and reads nuclear RNA from recovered cells; it cannot measure palatal adhesions, epidermal barrier formation, keratinocyte migration, neural-crest development, or glial/immune responses.
- The parquet provides DE contrasts but not baseline raw expression, so I did not quantify Irf6 baseline expression in the focal neurons.  The prediction rests on pathway placement plus measured analog behavior.
