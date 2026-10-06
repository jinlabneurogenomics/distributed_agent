# DEG-count prediction trace

## Question and resolved ambiguities

The held-out target manifest for this run contains one requested perturbation:

| target | requested cell group |
| --- | --- |
| `Sim1` | `151 TH Prkcd Grin2c Glut` |

I interpreted `predicted_n_degs` as the integer number of measured genes that would pass Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after acute AAV CRISPR-Cas9 loss of the indicated target, using the same analysis that produced the training CSV. `Sim1` was held out completely, so I did not assume access to a `Sim1` perturbation signature or count in the parquet.

The main ambiguity I resolved was how to use developmental Sim1 biology. SIM1 is a strong embryonic hypothalamic-neuroendocrine determinant, but the readout here is a sparse, partial, postnatal P16-to-P37/P44 neuronal perturbation in an Allen thalamic glutamatergic group, not a germline null and not a hypothalamic PVN/SON developmental assay. I therefore treated embryonic PVN/SON phenotypes as mechanism for choosing comparators, not as direct evidence for a broad focal-cell response.

## Sources used

- Training endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 206_Sim1.csv]`.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`, especially claims `claim:87c7269c6c7a2b19a33c`, `claim:06b0ea118b0d1e4ca1c6`, and `claim:d674c40db82e7f33c758`.
- PubMed literature for external Sim1/Otp/Arnt2/Pou3f2 biology:
  - Michaud et al. 1998, PMID:9784500, DOI:10.1101/gad.12.20.3264.
  - Michaud et al. 2000, PMID:10640708, DOI:10.1016/s0925-4773(99)00328-7.
  - Acampora et al. 1999, PMID:10557207, DOI:10.1101/gad.13.21.2787.
  - Goshu et al. 2004, PMID:14988428, DOI:10.1210/me.2003-0372.
  - Duplan et al. 2009, PMID:20092567, DOI:10.1111/j.1460-9568.2009.07028.x.

## Dataset computations

I first read the requested manifest and the focal-cell training DEG-count CSV. The manifest contained exactly `Sim1`. In the training endpoint table there were 1,674 non-held-out perturbations in `151 TH Prkcd Grin2c Glut`; 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, and only 5% of perturbations had more than 18 DEGs. This made the zero/nonzero decision the dominant calibration step.

I inspected the parquet metadata rather than scanning all 616,253,184 rows. The focal cell group is stored in row groups 546-580, covering roughly the focal 29 million rows. I then used the Distributed Agents runtime `profile_neighbors` tool on only the focal context for candidate bHLH-PAS and hypothalamic/developmental transcription-factor analogs:

```text
context = {"group_name": "151 TH Prkcd Grin2c Glut"}
anchors = eligible nodes =
  Arnt, Hif1a, Npas3, Bmal1, Bmal2, Clock, Ahr, Ahrr,
  Pou3f3, Pou3f4, Pou6f2, Nkx2-1, Otx2, Rax
value = logfoldchanges; significance = pvals_adj < 0.05
```

That computed signed whole-profile and top-tail similarities in the focal cell group and confirmed the exact significant-feature counts for those perturbations. I used the profile-neighborhood output qualitatively: the zero-DEG candidates had no FDR-significant focal features, while the one nonzero comparator, `Bmal1`, represented a distinct circadian-output branch rather than a SIM1-like branch.

## Sim1-specific reasoning

### External mechanism

`Sim1` encodes a bHLH-PAS transcription factor. In mouse embryonic hypothalamus, SIM1 is required for terminal differentiation of paraventricular, supraoptic, and anterior periventricular neuroendocrine lineages and acts upstream of `Pou3f2`/`Brn2` in a subset of those lineages (Michaud et al. 1998). `Arnt2`, not the screen-represented `Arnt`, is the in vivo dimerization partner implicated in SIM1-dependent PVN/SON neuroendocrine development (Michaud et al. 2000). `Otp` acts in parallel with `Sim1` to maintain `Brn2` during PVN/SON/aPV/ARN development (Acampora et al. 1999), and `Sim2` is a paralog in the anterior hypothalamic neuroendocrine network, partly downstream of `Sim1`/`Otp` for `Trh`/`Ss` cell expression (Goshu et al. 2004). `Sim1` gene dosage also affects mature PVN/SON cell numbers and projections in chronic heterozygous mice (Duplan et al. 2009).

Several of those ideal analogs were not perturbation targets in the training table: `Sim2`, `Arnt2`, `Otp`, and `Pou3f2` were unavailable. I therefore anchored the estimate on the closest measured bHLH-PAS partner branch, measured PAS-family contrasts, and measured developmental transcription factors that ask whether postnatal neuronal nuclei generally preserve a large acute developmental-TF module.

### Within-dataset analogs and counterexamples

| training perturbation | focal `n_degs` | why it is relevant to `Sim1` |
| --- | ---: | --- |
| `Arnt` | 0 | General bHLH-PAS dimerization partner and the measured alternative to missing `Arnt2`. Its focal perturbation had 0 FDR-significant features. The Distributed Agents same-experiment corpus reports that canonical AHR/HIF target programs were not recovered after `Arnt` perturbation and that `Ahr`, `Hif1a`, `Ahrr`, and `Npas3` were also flat in this basal neuronal assay. |
| `Hif1a` | 0 | ARNT-dependent bHLH-PAS axis member. A same-pathway comparator for whether an ARNT-containing transcriptional program is tonically active in the postnatal NeuN+ setting. |
| `Ahr` | 0 | Another ARNT-dependent bHLH-PAS transcription factor; it was flat with no focal DEGs, arguing against a broad basal ARNT/AHR-like PAS response. |
| `Ahrr` | 0 | AHR feedback repressor; also flat, further bounding the AHR-ARNT branch as quiescent in the same assay. |
| `Npas3` | 0 | A neuronal bHLH-PAS family member. The corpus places it in the flat ARNT/AHR/HIF/NPAS3/AHRR/BMAL2 branch rather than the detectable CLOCK/BMAL1 branch. |
| `Bmal2` | 0 | A bHLH-PAS/circadian paralog that might have been expected to share clock output but had no focal DEGs. This is a counterexample to extrapolating from PAS or BMAL-family membership alone. |
| `Bmal1` | 103 | Positive assay-sensitivity counterexample. The focal cell group can detect a bHLH-PAS transcription-factor program, specifically CLOCK/BMAL1 circadian output, so the ARNT/AHR/HIF/NPAS3 nulls are not just failure to detect any PAS-family TF. |
| `Clock` | 3 | CLOCK is the direct BMAL1 partner, but in the focal endpoint it produced only 3 DEGs. This weak partner response keeps the `Bmal1` count from being a good numerical analog for non-circadian `Sim1`. |
| `Cry1`, `Cry2` | 1, 3 | Circadian feedback genes with singleton/small focal responses, again showing that even pathway-adjacent clock components can be sparse. |
| `Pou3f3`, `Pou3f4`, `Pou6f2` | 0, 0, 0 | Represented POU developmental factors. `Pou3f2`/`Brn2`, the canonical downstream Sim1/Otp effector, was absent, but the measured POU factors did not reveal a generic postnatal POU developmental program. The same-experiment corpus explicitly reports sparse, non-overlapping POU-III responses rather than a shared POU developmental-network response. |
| `Nkx2-1`, `Otx2`, `Rax` | 0, 0, 0 | Hypothalamic/forebrain developmental TF comparators. They were all focal zeroes, supporting the idea that this thalamic postnatal group usually does not mount a large acute response when an embryonic patterning TF is targeted. |

The profile-neighborhood calculation was consistent with the table: `Arnt`, `Hif1a`, `Npas3`, `Ahr`, `Ahrr`, `Bmal2`, `Pou3f3`, `Pou3f4`, `Pou6f2`, `Nkx2-1`, `Otx2`, and `Rax` each had `significant_feature_count = 0` in `151 TH Prkcd Grin2c Glut`. The broad whole-profile Pearson similarities among these low-signal perturbations were modest and dominated by near-null structure rather than by a shared set of FDR-significant genes. The clearest nonzero PAS-family signal, `Bmal1` with 103 DEGs, is mechanistically a circadian positive-limb perturbation; the corpus claim `claim:87c7269c6c7a2b19a33c` separates this CLOCK/BMAL1 output from the flat ARNT/AHR/HIF/NPAS3/AHRR/BMAL2 branch.

### Zero/nonzero and count choice

I predicted `0` for `Sim1`.

The decision is driven mostly by within-dataset evidence. The measured bHLH-PAS branch most analogous to SIM1's dimerization logic was locally flat; the focal cell group did not show a tonic ARNT/AHR/HIF/NPAS3 response, and developmental POU/hypothalamic TF perturbations were also flat. External biology points to a strong Sim1 role in embryonic PVN/SON/aPV neuroendocrine specification through ARNT2, OTP, BRN2, and SIM2, but the exact partners and paralog were not perturbed and the focal readout is a postnatal thalamic glutamatergic group rather than the hypothalamic neuroendocrine nuclei where Sim1 is classically required. The assay does detect selected transcription-factor programs, including 103 focal DEGs for `Bmal1`, so I did not treat the prediction as an automatic transcription-factor zero; I treated `Bmal1` as a counterexample whose circadian mechanism is less appropriate than the flat ARNT/AHR/HIF/NPAS3 and developmental-TF analogs.

## Limits and extrapolation

- `Sim2`, `Arnt2`, `Otp`, and `Pou3f2` would have been the most direct training analogs, but they were unavailable as perturbation targets. The estimate therefore extrapolates from weaker bHLH-PAS and developmental-TF relatives.
- The Distributed Agents corpus had no held-out `Sim1` target context, so all corpus evidence was from neighboring represented perturbations.
- Germline null and heterozygous Sim1 studies report developmental anatomy, neuroendocrine peptide loss, and obesity-related physiology; they are imperfect proxies for an acute, sparse, partial CRISPR perturbation in postmitotic neurons.
- A zero DEG-count prediction means no measured gene is expected to pass BH FDR 0.05 in this powered snRNA-seq endpoint. It does not imply that Sim1 is biologically unimportant, that editing would fail, or that small direct target-gene changes are impossible.

## Final point prediction

| target_name | predicted_n_degs |
| --- | ---: |
| `Sim1` | 0 |
