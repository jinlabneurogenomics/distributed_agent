# Stim1 n_degs forecast

Target and endpoint: `Stim1` in `151 TH Prkcd Grin2c Glut`; `n_degs` is the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Stim1 prior

The supplied biology bundle supports a real but buffered perturbation. STIM1 is an ER Ca2+ sensor/channel-coupler for store-operated Ca2+ entry; it is a dynamic protein stock, so a P16 edit should stop new supply and the P37-P44 harvest interval likely depletes much of the pre-edit pool. The evidence is incomplete because no target-specific thalamic neuronal half-life was resolved.

Exact in-assay reach is moderate rather than broad: in the matched non-target nuclei for this class, `Stim1` was detected in 10,441 of 23,679 nuclei, 44.09%, with mean `0.402` CP10K. That raises the floor above a completely unexpressed target but leaves the aggregate 151-class signature exposed to dilution across Stim1-negative or weakly dependent thalamic subpopulations.

Two downward biological bearings kept the forecast small: forebrain conditional data showed Stim1 single loss was milder than combined Stim1/Stim2 loss, consistent with partial Stim2 buffering, and the closest neural phenotypes were forebrain or Purkinje rather than the assayed thalamic Prkcd/Grin2c population.

## Training evidence

The direct STIM/SOCE partners in the mouse annotation store, such as `Orai1`, `Orai2`, `Orai3`, `Stim2`, and `Trpc1`, were not usable training comparators in the one-row holdout. The exact curated store-operated-calcium-entry neighborhood therefore mostly collapsed to `Stim1` itself plus downstream/regulatory nodes: `Homer2` and `Nfatc3` had 0 DEGs in the requested 151 class.

I used a broader, biology-selected calcium cohort from ER/PM calcium handling, calmodulin/calcineurin/NFAT, glutamate calcium entry, and voltage-gated calcium channels. The focal 151-class training counts were highly sparse:

- SOCE regulation: `Homer2` 0, `Nfatc3` 0.
- ER/PM Ca2+ handling: `Atp2a2` 187, `Atp2b1` 22, `Atp2b2` 1, `Atp2b3` 1, `Itpr1` 0, `Ryr2` 0, `Ryr3` 0, `Plcb1` 0.
- Calmodulin/calcineurin/NFAT: `Calm1` 14, `Calm2` 0, `Calm3` 1, `Camk2a` 0, `Camk2b` 1, `Camk2g` 0, `Ppp3ca` 4, `Ppp3cc` 0, `Ppp3r1` 9, `Nfatc3` 0.
- Glutamate/Ca2+ entry and metabotropic signaling: `Grin1` 89, `Grin2a` 1, `Grin2d` 0, `Grm1` 1, `Grm5` 0, `Homer2` 0.
- Voltage-gated Ca2+ channel cohort: `Cacna1a` 0, `Cacna1d` 0, `Cacna1e` 0, `Cacna1g` 12, `Cacna2d1` 1, `Cacna2d2` 0, `Cacnb2` 0, `Cacnb4` 1, `Cacng2` 0, `Cacng3` 0.

Atp2a2 and Grin1 were the two high outliers, but both are poor scale donors for Stim1. The same-experiment corpus interprets `Atp2a2` loss as a 151-class ER-stress/UPR and ATF4-like salvage program; it also records that calcium relatives including `Itpr1`, `Ryr3`, `Atp2b2`, and `Atp2b1` did not reproduce that Atp2a2 program. `Grin1` was a specific NMDA-receptor response, and other Grin subunits did not phenocopy it. In contrast, `Grm1`, `Grm5`, `Plcb1`, `Itpr1`, `Ryr3`, `Homer2`, and `Nfatc3` were pan-null or near-null across their recovered neuronal surfaces, and `Ppp3ca`/`Ppp3r1` gave only small, noncanonical calcineurin signatures.

The matched expression-profile comparison over 28 selected calcium nodes confirmed that this was not a coherent high-response module: 15/28 nodes had no significant features and only 2/28 had at least 50. Across all 378 available selected pairs, positive significant-program overlap was usually absent, while negative-tail similarity was mostly a broad background effect rather than a shared SOCE state. Thus the large Atp2a2 and Grin1 counts looked like endpoint-specific outliers, not a reason to project a large response onto Stim1.

## Point estimate

The 28 biology-selected nodes had median 0 DEGs; their log1p mean was 1.55 DEGs, and excluding the two outliers `Atp2a2` and `Grin1` reduced the log1p mean to 0.88. I placed Stim1 slightly above the exact SOCE-regulator zeros because its target stock should be at least partially depleted and 44% of the focal nuclei express it, but below the observed Atp2b1/Calm1/Cacna1g small responses because of partial Stim2 buffering and the many null metabotropic/IP3/RyR/NFAT comparators.

Predicted `n_degs`: 2.
