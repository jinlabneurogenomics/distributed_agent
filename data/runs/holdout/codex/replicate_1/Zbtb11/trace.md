# Direct forecast for Zbtb11 in 151 TH Prkcd Grin2c Glut

Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05` in
`151 TH Prkcd Grin2c Glut`.

Point prediction: **420 DEGs**.

## Target biology used

The declared holdout manifest names one target, `Zbtb11`.  The prediction-safe
biology bundle resolves this packet target to GeneID 68193 / ENSMUSG00000098274,
the historical `Zbtb11` alias of **Rpl24**, not the current Zbtb11
transcription-factor locus.  The perturbed product is RPL24/eL24, a cytosolic
60S ribosomal-subunit protein installed in mature translating ribosomes.

Exact non-target expression reach in the requested population is high enough
for the locus to be targetable and observable:

- `pct_cells_expressing`: 66.7047%
- `mean_raw_umi`: 1.2465
- `mean_log1p_cp10k`: 0.4863
- `n_non_target_cells`: 23,679

The functional-stock adjudication concluded that a P16 edit should stop new
RPL24 supply while leaving pre-edit RPL24-bearing ribosomes initially intact;
because postnatal neuronal ribosomal proteins renew on an approximately
week-scale timescale and RPL24 rapidly associates with mature ribosomes, the
RPL24-bearing functional stock should be **likely substantially depleted** by
the P37-P44 harvest, with a residual long-lived tail.  That made `Zbtb11/Rpl24`
more endpoint-relevant than a lowly expressed or stock-persistent target, but
the stock card is partial and does not prove complete mature-ribosome loss in
all recovered thalamic neurons.

## Training measurements used

The declared count table has 1,674 held-in perturbations for the exact 151
population.  It is zero-heavy: median `n_degs = 0`; 1,205/1,674 perturbations
have zero DEGs; the 90th percentile is 2, the 95th percentile is 18, and the
right tail is very long.

Ribosome, translation, and proteostasis held-in counts from the declared
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`:

| target | training n_degs |
| --- | ---: |
| Uba5 | 2677 |
| Psmb4 | 742 |
| Ufc1 | 572 |
| Psmc1 | 430 |
| Elp1 | 645 |
| Rab7 | 501 |
| Gfpt1 | 311 |
| Atp2a2 | 187 |
| Nrf1 | 138 |
| Dhdds | 116 |
| Tsc2 | 86 |
| Nop56 | 25 |
| Sec63 | 11 |
| Eef2 | 9 |
| Polr3b | 8 |
| Hspa5 | 5 |
| Arih1 | 7 |
| Eif4g1 | 1 |
| Bcap31 | 1 |
| Rbm28 | 0 |
| Las1l | 0 |

Direct Parquet checks in the same 151 group confirmed the count table for the
main held-in comparators and gave their matched perturbed-nucleus counts:
`Uba5` 2677 DEGs with 245 nuclei, `Psmb4` 742 with 62, `Ufc1` 572 with 175,
`Psmc1` 430 with 89, `Nop56` 25 with 206, `Eef2` 9 with 87, `Eif4g1` 1 with
143, and `Rbm28` 0 with 143.  Thus the small ribosome/translation-adjacent
responses are not simply lower powered than the larger proteostasis responses.

The runtime profile comparison over twelve held-in translation/proteostasis
nodes in the 151 Parquet slice showed:

- `Uba5` and `Ufc1` form a strong UFMylation pair: 495 shared FDR<0.05 genes,
  all same-direction.
- `Psmb4` and `Psmc1` form a strong proteasome pair: 215 shared FDR<0.05
  genes, all same-direction.
- `Nop56` shares only 19 FDR<0.05 genes with `Uba5`, 11 with `Ufc1`, 6 with
  `Psmb4`, and 1 with `Psmc1`; its own anchor has only 25 DEGs.
- `Eef2`, `Eif4g1`, and `Rbm28` do not carry broad significant overlap with
  the UFMylation or proteasome modules.

The same-experiment corpus was used only to interpret held-in comparators.  It
summarized `Nop56` as a narrow, 151-concentrated nucleolar
ribosome-biogenesis response and explicitly contrasted it with flat or weak
large-subunit/rRNA-processing targets such as `Rbm28`.  It summarized `Uba5`
and `Ufc1` as a broad UFMylation/ER protein-quality-control state, and
`Psmb4`/`Psmc1` as core proteasome lesions with proteasome bounce-back, heat
shock/ISR, autophagy/lysosome, p53/apoptosis, and redox arms.  Those are
packaged interpretations of the same Perturb-seq experiment, not independent
replication.

## Synthesis

`Zbtb11/Rpl24` is not biologically close to the zero-like targets: it is strongly
expressed in the focal thalamic neurons, has no mature-ribosome replacement
documented from `Rsl24d1`, and should lose new RPL24 supply across several
ribosomal-protein renewal intervals before harvest.  That argues for a real
survivor-state transcriptional response rather than a near-zero call.

At the same time, the best measured ribosome-biogenesis and translation
perturbations in the training set are small: `Nop56` is 25, `Polr3b` is 8,
`Eef2` is 9, `Eif4g1` is 1, and `Rbm28`/`Las1l` are 0.  I therefore did not
use the `Uba5` 2677 extreme as a scale donor.  Those UFMylation genes are tied
to ER-associated stalled-ribosome quality control and produce a large
compensatory program; RPL24 loss should reduce cytosolic 60S capacity more
directly and gradually instead of reproducing the full UFMylation ISR/ER state.

The nearest high-confidence magnitude bracket is between the assayed
ribosome-biogenesis boundary (`Nop56`, 25) and the core proteostasis machinery
responses (`Psmc1`, 430; `Psmb4`, 742; `Ufc1`, 572).  Because RPL24 is a
structural mature-ribosome component with high exact reach and likely stock
depletion by harvest, I placed the point near the lower core-proteostasis
response rather than near the Nop56/Rbm28 boundary, while keeping it below the
large UFMylation and Psmb4 states to account for pre-edit ribosome persistence
and survivor conditioning.

Final point: **420**.
