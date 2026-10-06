# P2rx2 prediction trace

## Question and interpretation

The run asks for the number of genes that would pass `pvals_adj < 0.05`
after acute AAV-CRISPR loss of `P2rx2` in `151 TH Prkcd Grin2c Glut`
neurons.  The requested target list has a single held-out gene:

```tsv
target_name
P2rx2
```

I treated `n_degs` as the exact endpoint used in the supplied
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the count of measured
features with a Benjamini-Hochberg-adjusted Wilcoxon p-value below 0.05 in
this cell group.  I did not treat absence of a wide DEG response as failed
editing; many on-target rows in this experiment show a significant target
transcript reduction while producing only the target gene itself as a DEG.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 164_P2rx2.csv]`
- Internal Distributed Agents corpus:
  `perturbai-july-260713-sourceguard-1773-v1`; `target_context`,
  `related_targets`, and `story_count` returned no node, related targets, or
  claims for `P2rx2`, so the target was reasoned from the raw training DE
  signatures rather than from preassembled corpus claims.
- Internal Distributed Agents runtime profile tools:
  a focal-cell comparison of 20 selected purinergic and ligand-gated receptor
  perturbations, written to `p2rx2_candidate_profile_compare.json` and
  inspected in `p2rx2_candidate_profile_inspect.json`.
- Literature:
  North 2002, Physiological Reviews, DOI
  `10.1152/physrev.00015.2002`, PMID `12270951`; Khakh 2001, Nature Reviews
  Neuroscience, DOI `10.1038/35058521`, PMID `11256077`; Kanjhan et al. 1999,
  Journal of Comparative Neurology, PMID `10213185`.

## Dataset checks

I materialized the focal cell group from the 7.8 GB all-cell parquet using a
PyArrow equality filter on `group_name == "151 TH Prkcd Grin2c Glut"`.  The
focal slice contains 28,891,566 rows, 1,674 training perturbations, and 17,259
measured genes.

As a sanity check, I recomputed:

```sql
select gene_target, sum(pvals_adj < 0.05) as n_degs
from focal_151_TH_Prkcd_Grin2c_Glut
group by gene_target
```

for every non-held-out target.  The recomputed counts matched the supplied
training count CSV for all 1,674 targets with maximum absolute difference 0.
The endpoint is sparse: the median training target has 0 DEGs, the 75th
percentile has 1 DEG, 72.0% of targets are exactly 0, and the mean is pulled up
to 14.1 only by a small number of very broad perturbations such as `Uba5`,
`Tpr`, `Sin3a`, `Rnpc3`, and `Zbtb7a`.

`P2rx2` is present as a measured transcript in the focal DE tables for all
1,674 observed perturbations, but it is never significantly changed by any
training knockout.  Its best adjusted p-value across the 1,674 signatures is
0.906.  This does not predict the on-target fold change directly, because
`P2rx2` itself was held out, but it argues that the transcript is sparse or
noisy in this cell group and not part of a recurring observed downstream
program.

## Relevant observed analogs

There are no P2X ion-channel subunits in the training-count table, so the
closest internal comparisons are P2Y purinoceptors and other ligand-gated
cation channel subunits.

| class | observed training perturbations in `151 TH Prkcd Grin2c Glut` | interpretation |
|---|---|---|
| Purine-related genes | `P2ry12`: 0, `P2ry14`: 0, `Adk`: 0, `Nt5c2`: 0 | Closest by extracellular purine signaling or purine metabolism.  `P2ry12` and `P2ry14` are only superficial family analogs because they encode metabotropic P2Y GPCRs rather than trimeric P2X ATP-gated channels, but both are complete zeroes in this neuronal endpoint. |
| Ionotropic glutamate receptors | `Gria1`: 0, `Gria2`: 0, `Gria3`: 0, `Grik1`: 0, `Grik3`: 0, `Grik4`: 0, `Grik5`: 1, `Grin1`: 89, `Grin2a`: 1, `Grin2b`: 2, `Grin2d`: 0, `Grin3a`: 0 | These are better functional analogs because they are ligand-gated cation channels in neurons.  The obligatory NMDAR subunit `Grin1` is the only broad case; most paralogous or auxiliary AMPA/kainate/NMDA subunits have zero or target-only signatures. |
| Nicotinic acetylcholine receptors | `Chrna1`: 0, `Chrna2`: 0, `Chrna3`: 0, `Chrna4`: 2, `Chrna6`: 0, `Chrna7`: 0, `Chrnb1`: 0, `Chrnb2`: 1, `Chrnb3`: 0 | Another ligand-gated cation-channel family.  These perturbations are silent to nearly silent; the few significant rows are dominated by the perturbed receptor subunit itself. |
| GABA/glycine ligand-gated channels | `Gabra1`: 1, `Gabra2`: 0, `Gabra3`: 0, `Gabra5`: 0, `Gabrb1`: 0, `Gabrb2`: 4, `Gabrb3`: 0, `Gabrg2`: 1, `Gabrg3`: 0, `Glra1`: 0, `Glra2`: 0, `Glra3`: 0 | Less close in ion selectivity but still synaptic ligand-gated channels.  They again show that subunit loss usually does not create a wide nuclear RNA state in this focal excitatory group. |
| Ion-homeostatic ATPases, retained as counterexamples | `Atp1a3`: 80, `Atp2a2`: 187, `Atp2b1`: 22, `Atp2b2`: 1, `Atp2b3`: 1, `Atp2c1`: 1 | These are ATP-dependent pumps, not ATP receptors.  `Atp2a2` induced ER-stress and amino-acid/starvation genes such as `Ddit3`, `Xbp1`, `Herpud1`, `Hspa5`, `Asns`, and `Chac1`; `Atp1a3` and `Atp2b1` regulate bulk ionic homeostasis.  They are useful upper-bound counterexamples but are mechanistically inappropriate anchors for `P2rx2`. |

The runtime profile comparison of 20 selected purinergic and receptor-channel
perturbations classified 12/20 as having no significant focal features and only
`Grin1` as having at least 50 significant features.  Among the inspected P2Y,
AMPA, kainate, NMDA, and GABA receptor pairs, there was no shared
FDR-significant feature overlap.  The sparse significant hits in `Grin2a`,
`Grin2b`, `Grik5`, `Chrna4`, `Chrnb2`, `Gabra1`, and `Gabrg2` were mostly the
perturbed receptor transcript itself.  Thus the exact experiment supports a
near-zero prior for receptor-subunit perturbations unless the gene is an
obligatory core subunit like `Grin1`.

## Biological rationale for `P2rx2`

`P2rx2` encodes P2X2, one of the seven vertebrate P2X subunits.  P2X receptors
are trimeric membrane ion channels opened by extracellular ATP and permeable to
small cations, including calcium in many subtypes; P2X2 can form homomeric
channels and some heteromers such as P2X2/3 (North 2002; Khakh 2001).
Anatomical work detected P2X2 mRNA and protein in many adult rat neuronal
populations, including thalamic and subthalamic nuclei and the habenula
(Kanjhan et al. 1999), so expression in forebrain neurons is plausible.

I nevertheless predict no FDR-significant genes for the held-out perturbation:

- The direct purinergic training perturbations, `P2ry12` and `P2ry14`, are both
  0 DEG rows.  They are not close mechanistic substitutes for P2X2, but they
  rule against a broad generic purinergic-receptor effect in this endpoint.
- The stronger exact-assay analogs are ionotropic receptor subunits.  Of 33
  glutamate, nicotinic, GABA, glycine, and Htr3 receptor subunit perturbations
  I checked, 26 have 0 DEGs and most of the nonzero counts are 1 or 2.
- `Grin1` is the clear positive counterexample at 89 DEGs, but it is the
  obligatory NMDA receptor subunit and directly defines a major glutamatergic
  channel class.  `P2rx2` is a modulatory ATP-gated receptor and is not
  analogous to removing all NMDAR signaling.
- The high-count ATPase examples are broad because they hit ER calcium stores,
  Na/K gradients, or calcium extrusion.  P2X2 is a ligand-gated surface
  conductance and should not by itself impose the sustained ER-stress or ionic
  collapse signatures seen after `Atp2a2`, `Atp1a3`, or `Atp2b1` loss.
- In the focal DE table, measured `P2rx2` was not significantly altered by any
  of 1,674 other perturbations; that makes it unlikely that there is an
  endogenous `P2rx2`-centered transcriptional module in this cell group that the
  observed targets often engage.

Combining those internal observations with the external mechanism, I expect
acute mosaic `P2rx2` loss to alter ATP-evoked excitability if the receptor is
present, but not to push any gene past the Wilcoxon BH 0.05 threshold in the
`151 TH Prkcd Grin2c Glut` snRNA-seq endpoint.  My point prediction is
therefore:

```tsv
target_name	predicted_n_degs
P2rx2	0
```

## Limits

This is an extrapolation because the training data contain no P2X-family
subunit and the Distributed Agents same-experiment corpus has no `P2rx2` node.  The P2Y
receptors are weak mechanistic analogs, and the glutamate/GABA/nicotinic
subunits match the channel-subunit concept rather than extracellular ATP
pharmacology.  Published P2X2 expression maps are mostly rat adult tissue,
whereas this experiment is mouse, juvenile-to-young-adult, and sparse AAV
CRISPR in neuronal nuclei.  Finally, a prediction of 0 is brittle at the single
gene level: if `P2rx2` is expressed in a larger fraction of this cell type than
the training readout suggests, the target transcript itself could become one
significant row even without a secondary response.
