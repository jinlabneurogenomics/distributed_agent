# Stim1 DEG-count prediction

## Question and resolved ambiguities

I interpreted the requested endpoint as the total number of measured genes with
`pvals_adj < 0.05` after a held-out `Stim1` CRISPR loss-of-function
perturbation in `151 TH Prkcd Grin2c Glut` cells. The focal label is an Allen
atlas thalamic glutamatergic class; `TH` is thalamus rather than tyrosine
hydroxylase. I kept the target row in scope because the supplied training
`n_degs` counts include significant self-target rows when they pass FDR.

The manifest `[local file: 226_Stim1.csv]`
contains one target, `Stim1`. `Stim1` does not appear in the focal training
count file and is not present as a `gene_target` in the differential-expression
parquet.

## Sources

- Input differential-expression table:
  `[local file: training_de_all_cell_groups.parquet]`.
- Input focal count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest:
  `[local file: 226_Stim1.csv]`.
- Same-experiment Distributed Agents corpus
  `perturbai-july-260713-sourceguard-1773-v1`. It had no direct `Stim1`
  Finding or Claim, so I used its packaged Claims for calcium-pump,
  ER-stress, calcium-release, CaM/CaMK, and calcineurin comparator behavior.
- External literature retrieved through PubMed, used only to decide which
  observed perturbations were mechanistically appropriate analogs or
  counterexamples for `Stim1`.

## Parquet and count computations

I read the focal group from the parquet for curated calcium-homeostasis,
ER-stress, CaM/CaMK, calcineurin, and postsynaptic calcium-signaling training
targets. For each selected perturbation I counted `pvals_adj < 0.05`, listed
its significant genes, and computed score correlations and same-direction FDR
overlaps among the selected signatures.

The key operation was:

```python
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(selected_training_targets)
)
tab = dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj", "scores"],
    filter=filt,
)
```

I also summarized the focal training counts over all 1,674 non-held-out
targets. The endpoint is very sparse: the median target has 0 DEGs, the 75th
percentile has 1 DEG, and only 5% of training targets have more than 18 DEGs.
Among 1,642 training perturbations whose target transcript was also measured in
`151`, only 319 self-rows were FDR-significant; therefore a singleton
self-target call is possible but not inevitable.

## Within-dataset analogs and counterexamples

`Atp2a2`, encoding SERCA2, is the clearest positive ER-calcium comparator but
is deliberately not the quantitative template for `Stim1`. In `151`,
`Atp2a2` had 187 DEGs and induced the expected ER-stress/ISR/UPR genes:
`Ddit3`, `Chac1`, `Xbp1`, `Herpud1`, `Hspa5`, `Asns`, `Slc38a2`, and `Mthfd2`
were all up. The same-experiment Distributed Agents corpus captures this as Claim
`claim:16ed634c5b3dc2e0831c`: Atp2a2/SERCA2 loss selectively activates an
ER-stress ISR/UPR neuronal state that assayed PMCA, SPCA1, calcium-release
channel, and isolated `Atf6` perturbations do not reproduce. The direct focal
counts agree: `Itpr1` = 0, `Ryr2` = 0, `Ryr3` = 0, `Atf6` = 0, `Atp2b2` = 1,
`Atp2b3` = 1, and `Atp2c1` = 1.

The Atp2a2 state converged strongly with ER-proteostasis and glycosylation
stress signatures, not with generic calcium signaling. In the focal parquet,
`Gfpt1` had 311 DEGs and shared 94 FDR genes with `Atp2a2`, all 94 in the same
direction; `Dhdds` had 116 DEGs and shared 47/47 same-direction FDR genes;
`Elp1` had 645 DEGs and shared 105/105; `Elp2` had 150 DEGs and shared 53/53.
The Distributed Agents ER-quality-control Claim `claim:a359fec939ed97abdb05` likewise
places `Atp2a2` with `Gfpt1`, `Dhdds`, `Hspa5`, `Sec63`, and `Elp2`.
`Stim1` loss could reduce refilling after ER-store depletion, but it is not a
SERCA pump lesion and should not directly empty the ER at rest the way partial
`Atp2a2` loss can. The strong Atp2a2/Gfpt1/Dhdds/Elp signatures therefore
serve mainly as upper-bound stress-state counterexamples.

Training perturbations in the downstream Ca2+/calmodulin/calcineurin branch
argue against a hidden steady-state NFAT-like transcriptional response. In
`151`, `Ppp3r1` had only 9 DEGs, `Ppp3ca` 4, `Ppp3cc` 0, and `Nfatc3` 0.
`Calm1` had 14 DEGs, while `Calm2`, `Calm3`, `Camk2a`, `Camk2b`, and `Camk2g`
had 0-1. Distributed Agents Claims `claim:3560237f131488d500c4` and
`claim:39f5d2c49bf9e67844f9` make the same point from the screen reports:
calcineurin-axis RNA responses were subunit-selective and weak, and
CaM/CaMK/calcineurin-adjacent effectors did not collapse onto a common
steady-state neuronal RNA readout.

The training mGluR/IP3R/RyR/post-synaptic calcium-plasticity neighborhood was
also quiet in this assay. `Homer2` = 0, `Plcb1` = 0, `Grm5` = 0, `Itpr1` = 0,
`Ryr2` = 0, `Ryr3` = 0, `Grm1` = 1, `Prkcg` = 1, and `Shank2` = 0 in `151`.
The Distributed Agents Claim `claim:5361d0a42e47eed4d932` summarizes this as buffered
basal snRNA output for core calcium-release and postsynaptic
calcium-plasticity perturbations. Voltage-gated calcium-channel targets were
likewise mostly silent, except for the focal but small `Cacna1g` response:
`Cacna1a` = 0, `Cacna1d` = 0, `Cacna1e` = 0, `Cacna1g` = 12, `Cacna2d1` = 1,
`Cacna2d2` = 0, `Cacnb2` = 0, and `Cacnb4` = 1.

No direct `Stim2`, `Orai1`, `Orai2`, `Orai3`, `Trpc1`, or `Trpc5` perturbation
was present in the training counts, so there is no in-dataset SOCE-complex
phenocopy to copy from. `Stim1`, `Stim2`, and `Orai1-3` were present as
measured genes in the `151` parquet, but those rows under other perturbations
do not establish the held-out `Stim1` loss-of-function endpoint.

## Stim1 biology used for transfer

STIM proteins are ER-luminal Ca2+ sensors that move to ER-plasma-membrane
junctions after store depletion and gate Orai-family CRAC/store-operated
channels; STIM1-Orai1 is the minimal canonical SOCE unit (Putney et al. 2016,
doi:10.1016/j.bbamcr.2016.11.028; Derler et al. 2016,
doi:10.1152/ajpcell.00007.2016). Neurons express both `Stim1` and `Stim2`, and
rat cortical-neuron experiments found differential roles, with STIM1 more tied
to evoked SOCE and STIM2 more tied to resting ER Ca2+ handling
(Gruszczynska-Biegala et al. 2011, doi:10.1371/journal.pone.0019285).
Excitatory-neuron work further found STIM2, not STIM1, to be the central
organizer of a dendritic-spine AMPAR/PKA complex (Garcia-Alvarez et al. 2015,
doi:10.1091/mbc.E14-07-1222), and cultured hippocampal-neuron work associated
STIM1 with younger neurons and STIM2 with maintenance of Ca2+ entry into stores
in older neurons (Kushnireva et al. 2021, doi:10.3389/fnsyn.2020.573714).
Endogenous STIM tracking in hippocampal neurons similarly found a substantial
resting ER-PM-contact fraction of STIM2 but recruitment of STIM1 mainly during
strong NMDAR activation (Chhikara et al. 2025,
doi:10.1016/j.celrep.2025.116290).

There is real evidence that chronic, cell-type-specific STIM1 loss can reshape
neurons: Purkinje-neuron-specific `Stim1` knockout produced age-dependent
expression and synaptic-connectivity changes (Dhanya and Hasan 2021,
doi:10.1523/JNEUROSCI.2401-20.2021). I treated that as a warning against
calling STIM1 biologically inert, but it is an imperfect analog for acute,
sparse P16 AAV-CRISPR editing assayed 3-4 weeks later in thalamic glutamatergic
neurons.

## Target-specific prediction

For `Stim1`, I predict `n_degs = 0`.

The decision is driven mostly by within-dataset counterexamples. This screen
does detect a broad ER Ca2+-stress state when the ER loading pump `Atp2a2` is
perturbed, and that state aligns with strong ER/glycosylation stress targets
such as `Gfpt1`, `Dhdds`, `Elp1`, and `Elp2`. But represented IP3R/RyR release
channels, CaM/CaMK effectors, calcineurin/NFAT components, mGluR/Homer
neighbors, PMCA/SPCA pumps, and most voltage-gated calcium channels were
zero-to-singleton perturbations in the same cell group. External STIM biology
places `Stim1` upstream of store-operated entry after store depletion rather
than as the pump that constitutively loads ER stores; neuronal data also point
to STIM2 as more active at rest in mature excitatory neurons. With no direct
SOCE-component training perturbation, that leaves `Stim1` closest to the
well-buffered calcium-signaling branch rather than to the Atp2a2 ER-depletion
stress branch.

I considered a singleton prediction to allow a significant `Stim1` self row,
but chose zero because self-target significance was present in only about 19%
of measured training targets in `151`, `Stim1` is not a high-confidence
downstream-response target from any same-experiment Claim, and no represented
mechanistic neighbor forces even a one-gene effect.

## Limits

This is an extrapolation from neighboring calcium biology, not a direct
signature transfer: `Stim2`, `Orai`, and canonical SOCE-channel subunits were
absent as training perturbations. The external studies above are mostly
cultured hippocampal/cortical neurons, dorsal-root-ganglion or Purkinje
contexts, or chronic conditional knockouts rather than juvenile sparse AAV
editing of thalamic `151` nuclei. The snRNA readout does not assay ER Ca2+
load, SOCE current, NFAT localization, channel gating, synaptic physiology,
protein loss, indel rate, or depletion of edited neurons before nuclei
recovery. A zero prediction therefore means that no gene is expected to clear
BH FDR 0.05 in the recovered-nucleus Wilcoxon contrast; it does not mean that
STIM1 has no neuronal function.
