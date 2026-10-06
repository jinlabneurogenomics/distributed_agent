# Direct DEG-count forecast for Atp6ap1

## Endpoint

- Target: `Atp6ap1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Point prediction: `1`

## Biology prior

The Atp6ap1 card describes ATP6AP1/Ac45 as a membrane-anchored V0-region
constituent of mammalian brain V-ATPase that helps form the V0/V1 assembly
interface with ATP6AP2. A P16 disruptive edit is expected to stop new ATP6AP1
supply, while pre-existing incorporated V-ATPase persists until protein or
complex turnover; by the P37-P44 harvest, substantial depletion is favored but
uncertain because ATP6AP1-specific residence and post-edit clearance kinetics
were not found.

The exact focal expression measurement argues that Atp6ap1 was present in the
assayed thalamic population: 23,268 of 23,679 non-target nuclei expressed it
(`98.264%`), with mean raw UMI `6.752`. I treated this as evidence that a
self-transcript DEG was detectable if the edit created a transcript-visible
loss allele, not as an editing-efficiency or downstream-magnitude estimate.

The phenotype prior is weaker for this short postnatal assay. Mouse loss
evidence for Atp6ap1 is developmental or germline/chimeric; no synchronized
postnatal thalamic-neuron failure clock was available, and Atp6ap1l is only an
untested paralog for this context.

## Training measurements used

The focal training table contains 1,674 perturbations, and its DEG burden is
very zero-inflated: 1,205 perturbations have `0` DEGs, the 80th percentile is
`1`, the 90th is `2`, the 95th is `18`, and the 99th is `430`. Thus a count
above a few DEGs needs target-specific evidence for a strong state.

Typed mouse gene-analog nomination put the five training-available V-ATPase
comparators first:

| target | relation to Atp6ap1 | focal n_degs |
| --- | --- | ---: |
| `Atp6v1a` | V-ATPase narrow-module / physical comparator | 0 |
| `Atp6v1e1` | V-ATPase narrow-module / physical comparator | 0 |
| `Atp6v0a1` | V-ATPase narrow-module / physical comparator | 1 |
| `Atp6v1b2` | V-ATPase narrow-module / physical comparator | 0 |
| `Atp6ap2` | V-ATPase accessory/interface partner | 2 |

The same-experiment report topology also placed `Atp6ap2`, `Atp6v0a1`,
`Atp6v1a`, and `Atp6v1e1` in one reciprocal explicit-reference component;
`Atp6v1b2` was unrepresented in that corpus layer. This supported keeping the
V-ATPase group together semantically, but the numerical scale still came from
the training count table and the declared Parquet.

A direct Parquet check in `151 TH Prkcd Grin2c Glut` confirmed that the two
nonzero V-ATPase counts were almost entirely self- or core-axis events:
`Atp6ap2` had 2 significant negative genes, including `Atp6ap2` itself and
`Atp6v0a1`; `Atp6v0a1` had only its self transcript significant; the three
V1 subunits had no significant genes. The matched recovered-nucleus counts for
these analogs were small, from 32 to 197 perturbed nuclei against 23,679
matched controls, so these rows are somewhat underpowered but still define the
observed direct-complex regime as essentially flat.

I also expanded the five V-ATPase anchors through recurrent same-corpus
outbound comparator links. The only eligible additions were:

| target | focal n_degs | use |
| --- | ---: | --- |
| `Atp13a2` | 1 | kept as low lysosomal ATPase module support |
| `Cltc` | 3 | kept as low endocytic boundary context |
| `Gfpt1` | 311 | rejected for the point; metabolic stress, not a direct V-ATPase component |
| `Psmb4` | 742 | rejected for the point; proteasome failure, not a direct V-ATPase component |
| `Rab7` | 501 | rejected for the point; broader late-endosome trafficking state with weak/opposing V-ATPase links |

The profile review of the ten-node V-ATPase-plus-expansion cohort likewise
separated the five direct V-ATPase comparators, which had `0-2` significant
features and no significant positive features, from the large bidirectional
programs in `Gfpt1`, `Psmb4`, and `Rab7`.

## Synthesis

I forecast a very small but nonzero response. The strongest quantitative
evidence is the direct V-ATPase cluster at `0, 0, 0, 1, 2` DEGs, plus the low
`Atp13a2` and `Cltc` boundary counts. Atp6ap1's high focal expression and its
accessory position at the V0/V1 interface make a transcript-visible event more
plausible than a strict zero, but the Atp6ap2/Atp6v0a1 rows show that even
measured V-ATPase self effects did not propagate into a large BH-significant
program under this sparse postnatal screen.

I therefore used `1` as the point estimate: one significant measured gene,
most plausibly the self transcript, with the broader lysosome/proteostasis
states treated as upper boundary context rather than transferred scale.

No Atp6ap1 target expression signature, Atp6ap1 DEG count, or Atp6ap1
same-experiment Finding/report was queried or used.
