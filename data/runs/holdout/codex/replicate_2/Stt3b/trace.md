# Stt3b forecast trace

Target: `Stt3b`

Cell group: `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `1`

## Evidence used

- The declared biology bundle, `[local file: Stt3b.json]`, identifies STT3B as the OST-B catalytic subunit for post-translocational N-linked glycosylation, with partial STT3A overlap. It judged operative STT3B-dependent stock as `likely_substantially_depleted` by the P16 to P37/P44 harvest window, but only with partial evidence: existing STT3B protein and pre-edit glycoproteins can persist, target turnover in the matched neurons is unknown, carrier turnover is a bulk thalamus-inclusive proxy, and the only direct mouse null phenotype is systemic midgestation lethality rather than acute postnatal thalamic neuron loss.
- The same bundle gives exact focal-population target reach for the readout population: in non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Stt3b` was detected in 20,103 of 23,679 cells, or 84.898%, with mean raw UMI 2.706 and mean CP10K 1.637. I used this as evidence that the target is present in most recovered cells, not as a quantitative edit-efficiency proxy.
- The strict `pvals_adj < 0.05` training count table, `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, contains 1,674 training perturbations; 1,205 are zero at this exact endpoint, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the mean is pulled up to 14.054 by a small high-response tail.
- Direct OST-B complex partners and the paralog/substrate-site factors exposed by the Stt3b biology card (`Stt3a`, `Rpn1`, `Rpn2`, `Ddost`, `Dad1`, `Ostc`, `Magt1`, `Tusc3`, `Krtcap2`, `Tmem258`, `Ost4`) are absent from that 151 training-count table, so no measured training perturbation is a direct single-step OST-B comparator.
- The nearest available N-glycan/ER shell was small at the task threshold. In the count table:
  - `Dpm1`, a glycosylation donor-supply gene, had 0 DEGs.
  - `Atf6`, a UPR sensor, had 0.
  - `Edem3`, `Sec23a`, `Sil1`, `Sar1b`, and `Nfe2l2` each had 0.
  - `Amfr`, `Bcap31`, `Ssr4`, `Stub1`, and `Hsp90ab1` were 1-gene profiles, usually dominated by the perturbed transcript itself.
  - `Vcp` had 2, `Hspa5` had 5, and `Sec63` had 11.
  - `Marchf6` had 14 but was dominated by a sterol/SREBP program, not an OST-like glycosylation response.
- A direct Parquet slice from `[local file: training_de_all_cell_groups.parquet]` confirmed the exact significant 151 rows for these comparators. The `Hspa5` and `Sec63` rows carried the clearest small ER folding and ER-associated stress tails: `Hspa5` up-regulated `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3`, while `Sec63` up-regulated `Hspa5`, `Canx`, `Hyou1`, and `Chac1`. The zero and singleton comparators did not show a hidden broad ER response at `pvals_adj < 0.05`.
- The matched 151 profile-neighborhood analysis over 18 ER/N-glycan/UPR training perturbations wrote `./stt3b_er_profile_neighbors.json`. It found a connected but weak local profile space; the strongest all-view recurrent pair was `Hspa5`/`Sec63`, with full-profile Pearson 0.1875 and cosine 0.2063. That argues for a modest shared ER-quality-control state among a few perturbations, not a robust large module common to all ER-associated losses.
- Same-experiment corpus Findings, interpreted as packaged context rather than replication, matched the Parquet picture for the training comparators: `Atf6:F001`, `Amfr:F001`, `Bcap31:F001`, `Edem3:F001`, and `Hsp90ab1:F001` are buffered or null postnatal neuronal responses; `Dpm1:F001` reports only a very small 151-specific glycosylation-linked response at the looser FDR<0.10 threshold; `Hspa5:F001`/`F002` and `Sec63:F001`/`F004` place the strongest relevant measured response in a selective ER chaperone/UPR-like state. `Sec63:F005` and `Sec63:F006` explicitly separate that ER-client stress from a simple duplicate of `Hspa5` or basal `Atf6` loss.
- Broader upstream supply perturbations form the high-response boundary, not the central analog: `Dhdds` had 116 DEGs, `Atp2a2` 187, and `Gfpt1` 311. Those perturb the shared dolichol, ER-calcium, or hexosamine support state upstream of many clients and are less specific than an STT3B-OST loss with partial STT3A redundancy.

## Reasoning

The focal neurons express `Stt3b` broadly enough that target reach is not the main reason to expect a null, and the functional-stock card makes realized loss over 21 to 28 days more likely than preservation of the full pre-edit enzyme/glycoprotein pool. That moved the forecast off the genome-wide zero mode.

The magnitude evidence points the other way. The direct OST-B subunits were not measured in training, and the nearest available single-gene losses in ER glycoprotein handling were flat or one-gene at the exact `pvals_adj < 0.05` endpoint. Detectable ER-stress signatures were present for `Hspa5` and `Sec63`, but remained only 5 to 11 DEGs in this strict count table. Large glycosylation-associated responses were confined to less specific upstream supply perturbations such as `Gfpt1` and `Dhdds`, which should overstate a substrate-selective STT3B lesion.

I therefore treated `Dpm1`/`Atf6`/`Edem3` as the low boundary, `Hspa5`/`Sec63` as the closest detectable ER-stress boundary, and `Dhdds`/`Gfpt1` as broader high-side falsifiers. With STT3B expected to be present and at least partly depleted, but buffered by persistent glycoprotein carriers, unknown STT3B turnover, and partial STT3A coverage, the most defensible strict-BH forecast is a tiny nonzero response:

`predicted_n_degs = 1`
