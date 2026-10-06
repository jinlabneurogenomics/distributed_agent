# Question and endpoint

The held-out target for this run is `Vapb`.  I interpreted the task as a
target-specific point prediction of the number of measured genes that would
pass `pvals_adj < 0.05` after `Vapb` CRISPR loss-of-function in
`151 TH Prkcd Grin2c Glut` neurons.  The count includes any measured gene,
including the perturbed target itself if the target transcript is significantly
reduced.  I treated zero as "no measured transcript crosses the FDR 0.05
threshold", not as failed editing.

The key ambiguity was how strongly to transfer ALS, ER-stress, and
membrane-contact biology onto a 3-4 week, sparse, postnatal, NeuN+ CRISPR
readout.  I resolved that by giving the same-experiment focal counts priority:
literature links were used to pick mechanistically relevant comparators, but
the final scale was calibrated to training perturbations in the same cell group.

# Sources used

* Input endpoint table:
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
* Input differential-expression parquet:
  `training_de_all_cell_groups.parquet`; I read only row groups whose
  `group_name` statistics overlapped `151 TH Prkcd Grin2c Glut`, then pulled
  rows for ER-stress, lipid-transfer, endolysosomal, and ALS/proteostasis
  comparator targets.
* Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`; `target_context` for `Sec63`,
  `Hspa5`, `Vcp`, and `Pitpna` supplied curated same-experiment findings that
  separated real 151-cell ER stress from null ER-adjacent perturbations.
* Distributed Agents runtime profile comparison; I compared
  `Atf6,Hspa5,Sec63,Vcp,Tardbp,Pitpna,Atl1,Atl3,Sqstm1,Vps35,Rab7,Vps54`
  in the focal group using full log-fold-change vectors plus the FDR mask.
* External literature from PubMed:
  * Kaiser et al. 2005, DOI `10.1016/j.str.2005.04.010`, and Loewen &
    Levine 2005, DOI `10.1074/jbc.M500147200`, for the conserved FFAT-binding
    surface on ER VAP proteins.
  * Kawano et al. 2006, DOI `10.1074/jbc.M605032200`, Peretti et al. 2008,
    DOI `10.1091/mbc.e08-05-0498`, Murphy & Levine 2016, DOI
    `10.1016/j.bbalip.2016.02.009`, and Di Mattia et al. 2020, DOI
    `10.15252/embj.2019104369`, for VAPA/VAPB/MOSPD2 as ER FFAT receptors
    that organize lipid-transfer membrane-contact sites.
  * Lindhout et al. 2019, DOI `10.15252/embj.2018101345`, for a neuronal
    VAP-SCRN1 contact-site role in ER remodeling, presynaptic calcium, and
    synaptic-vesicle cycling.
  * Suzuki et al. 2009, DOI `10.1111/j.1471-4159.2008.05857.x`, and
    Kanekura et al. 2009, DOI `10.1007/s12035-009-8054-3`, for the ALS8
    P56S-VAPB connection to aggregation, loss of normal VAPB function, and
    ER-stress/IRE1-XBP1 vulnerability.
  * Kabashi et al. 2013, DOI `10.1093/hmg/ddt080`, for vertebrate Vapb
    loss-of-function models in which loss weakens the motor system but, by
    itself, is insufficient for a full ALS phenotype.

# Computation over the training data

The focal training table contained 1,674 non-held-out perturbations.  Of these,
1,205 had `n_degs = 0`; the median was 0, the 75th percentile was 1, the 95th
percentile was 18, and the maximum was 2,677.  Thus a one- or few-gene answer
is a common outcome and does not need to be explained as missing perturbation.

The parquet is sorted by `group_name`, so I used row-group min/max statistics
to read only the 35 row groups spanning `151 TH Prkcd Grin2c Glut` rather than
the full 616,253,184-row file.  The relevant filter was:

```python
for i in range(pf.num_row_groups):
    stats = pf.metadata.row_group(i).column(group_name_index).statistics
    if stats.min <= "151 TH Prkcd Grin2c Glut" <= stats.max:
        read_row_group(i)
```

I then counted significant genes for curated comparator targets, inspected
their significant features and UPR/contact-site marker log fold changes, and
ran a Distributed Agents `profile_compare` on the same focal log-fold-change vectors.

# Target-specific reasoning: Vapb

`Vapb` encodes a tail-anchored ER membrane receptor for FFAT-motif proteins.
It is close to VAP-A and MOSPD2, binds many lipid-transfer and
organelle-contact proteins, and is biologically tied to ER-Golgi,
ER-endosome, ER-mitochondria, and presynaptic ER functions.  That made three
same-dataset neighborhoods potentially relevant: ER/UPR proteostasis,
ER-contact lipid transport, and ALS/endolysosomal proteostasis.

The strongest positive ER/UPR controls were real but not enormous in the exact
focal table unless a proximal ER-client pathway was hit.  `Hspa5` produced
5 DEGs: `Hsp90b1`, `Nfe2l1`, `Pdia4`, `Derl3`, and `Erc1`.  `Sec63`
produced 11 DEGs and directly induced `Hspa5`, `Canx`, and `Hyou1`.  Larger
ER-quality-control states existed elsewhere in the same cell group:
`Dhdds`, `Gfpt1`, and `Atp2a2` had 116, 311, and 187 DEGs, and `Uba5`,
`Ufc1`, `Psmb4`, and `Psmc1` had hundreds to thousands.  Those broad counts
argue that the thalamic readout can see ER/proteostasis stress when the lesion
forces a durable UPR or proteasome response.  They are not direct VAPB
quantitative analogs because VAPB is a redundant ER-contact receptor rather
than an ER lumenal chaperone, a translocon cofactor, dolichol/N-glycan supply,
UFMylation, or core proteasome component.

The negative ER controls were more predictive for `Vapb`.  `Atf6` had
0 DEGs in 151 despite 177 perturbed nuclei; the same-experiment corpus notes
that basal `Atf6` loss was a corrected-transcriptome null across recovered
neuronal groups.  Other ER-associated or ER-stress-adjacent perturbations were
also flat or singleton in 151: `Cert1` 0, `Acbd5` 0, `Osbpl2` 0, `Stard7` 0,
`Mttp` 0, `Lman2l` 0, `Edem3` 0, `Sil1` 0, `Bcap31` 1, and `Amfr` 1.  This
fits the biology: knocking out one ER membrane contact-site receptor under
basal conditions is expected to be buffered by VAPA/MOSPD2 and by many
alternative FFAT interactors, whereas perturbing the ER lumenal folding
capacity or glycoprotein supply is much more likely to drive a nuclear UPR.
`Vapa` and `Mospd2` themselves were not available as training perturbations,
so the exact paralog compensation could not be tested directly.

The lipid-transfer/contact-site side of the training data also pointed to a
near-null or small answer.  `Pitpna` had 21 DEGs and a clear self transcript
decrease, but its signature centered on phosphoinositide/Ca2+/secretory and
microtubule remodeling genes such as `Prkcg`, `Atp2a2`, `Gabra4`, `Lrrc7`,
`Pip5kl1`, `Stmn4`, `Tubb3`, and `Tubb4b`, not on `Hspa5`/`Xbp1`/`Herpud1`.
The same-experiment corpus explicitly found that represented
phosphoinositide-transfer, PI4P-turnover, PLC, and PKC perturbations did not
phenocopy `Pitpna`; so I treated `Pitpna` as an upper bound for a specialized
PI-transfer hit, not as a count to assign to every ER lipid-contact factor.
Several sterol/ceramide/contact-site-related perturbations were actually zero
in 151 (`Cert1`, `Osbpl2`, `Stard7`, `Acbd5`, `Rab18`), reinforcing that a
single contact-site component is often transcriptionally buffered.

Finally, ALS or proteostasis labels alone would overpredict `Vapb`.  `Tardbp`
was broad in this cell group with 210 DEGs, but its top genes
(`Ppp6c`, `Gabpa`, `Usp15`, `Uggt2`, `Snrnp70`, `Unc13a`) formed an RNA
processing/neuronal state and its ER stress markers were not induced.  `Vcp`
was much closer to VAPB disease biology through ERAD/autophagy, but had only
2 DEGs at FDR 0.05 in 151; the Distributed Agents corpus notes that acute `Vcp` loss
was sparse and did not induce canonical UPR, heat-shock, proteasome
bounce-back, p62/LC3, lysosomal, or TDP-43 transcripts at FDR < 0.10.
`Sqstm1` had 1 DEG and `Tmem106b` had 1 DEG.  Endolysosomal perturbations
such as `Rab7`, `Vps35`, and `Vps54` had 501, 17, and 31 DEGs respectively,
but their significant genes were lysosome/retromer or neuronal-trafficking
outputs rather than an FFAT/VAP-like ER-contact state, so they served mainly
as counterexamples.

Putting those together, I expect acute mosaic `Vapb` loss in
`151 TH Prkcd Grin2c Glut` to be essentially buffered at the level of nuclear
snRNA-seq.  The remaining reason for predicting a nonzero count is the target
transcript itself: `Vapb` is a measured focal gene, related singleton controls
such as `Bcap31`, `Amfr`, `Sqstm1`, `Tmem106b`, and `Atl1` often register one
self or near-self DEG without a broad downstream state, and the external
loss-of-function data suggest mild, slow vulnerability rather than an immediate
large UPR.  My point prediction is therefore a singleton response.

Prediction:

* `Vapb`: `1` DEG.

# Limits

The main limitation is the missing exact paralog test: neither `Vapa` nor
`Mospd2` was a visible training perturbation, so the strongest compensation
hypothesis could not be checked in the same dataset.  VAPB's best-studied
human ALS8 allele is P56S, a dominant aggregating mutation that can sequester
wild-type VAPB; that is not equivalent to the experiment's sparse CRISPR
loss-of-function.  The readout is nuclear RNA from surviving juvenile neurons,
so it could miss local axonal ER defects, lipid flux changes, ER-mitochondria
contact defects, synaptic-vesicle phenotypes, slow motor-neuron degeneration,
glial contributions, and protein-level aggregate or autophagy changes.  The
integer count is therefore driven more by the near-null ER/contact-site
training evidence than by a direct measured `Vapb` signature.
