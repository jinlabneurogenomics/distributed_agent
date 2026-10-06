# Direct n_degs forecast for Zfhx4

Target and endpoint:

- Target: `Zfhx4`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`

Evidence used:

- The declared biology bundle identifies ZFHX4 as a nuclear DNA-binding transcription factor. The perturbation should stop new ZFHX4 production, and the P16-to-P37/P44 interval is long enough that a soluble nuclear protein stock is likely to decline substantially, although no ZFHX4-specific thalamic protein-turnover measurement exists.
- Exact focal reach was present but not ubiquitous: in matched non-target 151-class nuclei, `Zfhx4` was detected in 13,397 of 23,679 nuclei, 56.58%, with mean CP10K 0.708 and mean log1p CP10K 0.430.
- The positive loss phenotypes in the biology bundle are context-distant for this acute postnatal assay. The neural evidence is germline embryonic/neonatal brainstem respiratory-center development; the other direct loss phenotype is skeletal/cartilage. Neither establishes a maintenance requirement in postmitotic thalamic glutamatergic neurons.
- The 151-class training count table is sparse: 1,205 of 1,674 training perturbations had `n_degs = 0`, the median was 0, the 75th percentile was 1, and the 90th percentile was 2. A biologically plausible perturbation therefore still needs local postnatal demand to escape zero.
- The closest represented biology-derived comparators were quiet in the same endpoint. `Zfhx2`, the ZFHX-family member present in training, had `n_degs = 0` in 151. `Phox2b`, a direct ZFHX4-regulated respiratory-development gene, had `n_degs = 0`; `Runx2` and `Sp7`, skeletal cofactors from the ZFHX4 evidence, also had `n_degs = 0`.
- Direct Parquet checks confirmed those comparator zeros were measured local contrasts rather than missing rows: `Zfhx2`, `Phox2b`, `Runx2`, and `Sp7` each had 17,259 measured-gene rows in `151 TH Prkcd Grin2c Glut`, 166-233 matched perturbed nuclei, 23,679 controls, and no gene with adjusted `p < 0.05`.
- The same-experiment Finding layer reinforced that this quietness was not only 151-local for the developmental comparators: `Phox2b` had no corrected downstream response across its 22 measured neuronal groups; `Runx2` was a whole-transcriptome null across 23 groups; `Sp7` was essentially absent outside a two-gene cerebellar GABA response; and `Zfhx2` had only one weak 009-class hit.
- Positive transcription-factor precedents in this class exist, but they look more locally anchored than ZFHX4: `Tcf7l2` had 106 151-class DEGs, `Zfp423` had 150, `Zfp236` had 19, `Zfp148` had 8, `Adnp` had 25, and `Zbtb18` had 5. These show that the assay can detect thalamic transcription-factor responses, but they do not overcome the lack of a demonstrated ZFHX4 adult thalamic maintenance module.

Synthesis:

`Zfhx4` has real focal expression and a likely realized loss of a renewable nuclear regulator, so a small response is possible. The decisive evidence for the point estimate, however, is the mismatch between its established phenotypes and the assayed postnatal thalamic neurons, together with the exact zeros for the closest ZFHX-family and known developmental/cofactor comparators in the same count table and Parquet. I therefore place the forecast at the modal sparse-count outcome rather than at the low positive tail.

Predicted `n_degs`: 0
