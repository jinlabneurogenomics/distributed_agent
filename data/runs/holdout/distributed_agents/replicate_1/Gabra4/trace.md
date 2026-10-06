# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The held-out target for this run is `Gabra4`. I interpreted the task as a point
prediction of `n_degs`, the number of measured genes with Wilcoxon
Benjamini-Hochberg `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut`
comparison of postnatal sparse AAV CRISPR perturbation against matched
non-targeting controls. The count includes the perturbed target transcript
itself when it passes the same threshold.

`Gabra4` is absent from both supplied training inputs, so its endpoint is not
directly observed in the declared files. The declared differential-expression
Parquet and the focal-cell training count CSV directly measure the same endpoint
for non-held-out perturbations and are the quantitative basis. The PerturbAI
July 260713 sourceguard-1773 v1 corpus is a same-experiment interpretation
surface over those measurements, not independent replication. PubMed literature
was used only to decide which represented subunits are the closest biological
analogs for the held-out alpha4 subunit.

## Quantitative checks over the supplied inputs

I read `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
and confirmed that it contains 1,674 unique training perturbations and no
`Gabra4`. The requested manifest
`single-target request for Gabra4`
contains exactly one row, `Gabra4`.

The focal training-count distribution is sharply zero-inflated:
median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, and maximum
2677 DEGs. This means a prediction of 1-4 genes for a receptor subunit is not a
generic "small but nonzero" midpoint; it is already above most training
perturbations in this particular cell group.

I then queried the declared Parquet for the focal cell group and represented
GABA-system targets. The directly relevant observed `151 TH Prkcd Grin2c Glut`
counts were:

| training target | focal `n_degs` | FDR<0.05 genes in the focal group |
|---|---:|---|
| `Gabra1` | 1 | `Gabra1` down |
| `Gabra2` | 0 | none |
| `Gabra3` | 0 | none |
| `Gabra5` | 0 | none |
| `Gabrb1` | 0 | none |
| `Gabrb2` | 4 | `Gabrb2` down; `Nr4a1` up; `Vgf` up; `Nalf1` down |
| `Gabrb3` | 0 | none |
| `Gabrd` | 2 | `Gabrd` down; `Cttnbp2` up |
| `Gabrg2` | 1 | `Gabrg2` down |
| `Gabrg3` | 0 | none |
| `Gabrr2` | 0 | none |
| `Gabbr1` | 1 | `Gabbr1` down |
| `Gabbr2` | 1 | `Gabbr2` down |
| `Gad2` | 0 | none |
| `Slc6a1` | 0 | none |
| `Slc32a1` | 0 | none |

The same-experiment corpus reports the same pattern at the cross-cell-type
level: `Gabra1`, `Gabra2`, `Gabra3`, `Gabra5`, and `Gabrb1` were
transcriptionally buffered across the recovered atlas, while `Gabrb2`, `Gabrd`,
and `Gabrg2` had sparse, context-dependent leakage into activity or postsynaptic
sentinel genes. The corpus specifically flags that same GABA-A receptor-family
membership did not create a common transcriptomic program in this assay:
alpha, beta, gamma, delta, rho, gephyrin/collybistin, GABA-B, and GABA-handling
perturbations were mostly flat and mutually non-convergent.

## Biological transfer for `Gabra4`

`Gabra4` encodes the GABA-A receptor alpha4 subunit. The closest molecular
transfer chain is:

`Gabra4` loss -> impaired alpha4-containing extrasynaptic GABA-A receptors ->
reduced tonic inhibition in thalamic relay neurons -> possible disinhibition
or compensatory postsynaptic transcription in recovered `151 TH Prkcd Grin2c
Glut` nuclei -> sparse FDR-significant snRNA-seq genes.

Two external observations make `Gabrb2` and `Gabrd` the most relevant
represented partners rather than distant family members. Chandra et al. 2006
showed that Gabra4-null mice lose tonic inhibition in dentate granule cells and
thalamic relay neurons and lose gaboxadol sensitivity, supporting alpha4 as a
functional extrasynaptic subunit in exactly thalamic circuitry
(PNAS, DOI 10.1073/pnas.0604304103; PubMed 17005728). Jia et al. 2008 found
that taurine-evoked extrasynaptic currents in mouse ventrobasal thalamus were
gabazine-sensitive, alpha4-dependent, and consistent with alpha4-beta2-delta
GABA-A receptors; a companion study found that ethanol modulation of thalamic
tonic inhibition was absent in alpha4 knockouts (J. Neurosci.,
DOI 10.1523/JNEUROSCI.3996-07.2008, PubMed 18171928; JPET,
DOI 10.1124/jpet.108.139303, PubMed 18477766). Jia, Pignataro, and Harrison
2007 also reviewed heavy thalamic expression of alpha1, alpha4, beta2, and
delta and the role of alpha4-beta2-delta receptors in thalamic tonic inhibition
(Alcohol, DOI 10.1016/j.alcohol.2007.03.010; PubMed 17521848).

That biology predicts that an alpha4 edit can have a real channel-level effect
in thalamic glutamatergic neurons. It does not predict a broad nuclear RNA
state. In the same focal cell group, the beta2 and delta partners showed only
4 and 2 FDR<0.05 calls. The beta2 response was the broadest on-axis
counterexample and was led by an immediate-early/neuropeptide pattern
(`Nr4a1`, `Vgf`) plus one additional downstream gene (`Nalf1`). The delta
response was weaker and consisted of target self-reduction plus `Cttnbp2`.
The represented alpha subunits are an even lower baseline: `Gabra1` produced
only its own target-transcript call and `Gabra2`, `Gabra3`, and `Gabra5` were
zero in the focal group.

I therefore predict a nonzero but very narrow response for `Gabra4`. I expect
the target transcript itself to pass the FDR threshold because alpha4 is a
thalamic relay-neuron subunit, unlike alpha2/alpha3/alpha5 in this focal group.
I also allow one sparse downstream sentinel because the alpha4-beta2-delta
extrasynaptic receptor is closer to the observed `Gabrd` and `Gabrb2` thalamic
signals than to an arbitrary silent alpha paralog. I do not transfer the full
`Gabrb2` count of 4 because beta2 participates in many alpha-beta-gamma and
alpha-beta-delta receptor classes, whereas alpha4 is more specialized; the
dataset itself shows that even obligatory GABA-A subunits were not
interchangeable at the snRNA endpoint.

## Limits and uncertainty

The endpoint for `Gabra4` is absent from the supplied inputs, so this is an
extrapolation from partners and paralogs rather than a direct signature match.
The Parquet contains no raw per-nucleus counts or indel rates, and measured
target-mRNA loss is not a quantitative edit-efficiency measure. The strongest
external evidence for alpha4 function comes from germline knockout and
pharmacology/electrophysiology studies, while the requested assay is acute,
mosaic postnatal CRISPR and survivor-conditioned snRNA-seq 3-4 weeks after
infection. The partner responses in training were themselves tiny, so moving by
one DEG would be plausible in either direction; the point estimate below should
be read as "target plus at most one downstream gene", not as evidence of a broad
transcriptional state.

