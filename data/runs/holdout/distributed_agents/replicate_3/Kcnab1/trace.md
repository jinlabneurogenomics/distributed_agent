# Kcnab1 held-out DEG-count prediction

## Question interpreted

The manifest for this run contains one held-out target:

- `Kcnab1`

The requested endpoint is the integer number of genes with `pvals_adj < 0.05`
in the `151 TH Prkcd Grin2c Glut` differential-expression table for the
`Kcnab1` perturbation. I treated the target transcript itself as eligible to be
counted, because the supplied training endpoint counts every measured gene in
the same way: for example, `Kcnab2`, `Kcnc2`, `Kcnc3`, `Kcnq2`, `Kcnq3`,
`Hcn2`, `Scn1a`, `Scn2a`, and `Scn8a` each have one DEG in this cell group and
that single DEG is their own target transcript.

## Sources used

- Input training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input training DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 117_Kcnab1.csv]`
- Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`;
  I used the target, claim, and target-comparison views for `Kcnab2`, `Kcna1`,
  and `Kcna2`. There was no Kcnab1-specific corpus node in this release.
- Distributed Agents runtime profile comparison over the focal-cell DE parquet for the
  exact Kv candidate cohort `Kcnab2`, `Kcna1`, `Kcna2`, `Kcnc2`, `Kcnc3`,
  `Kcnb1`, `Kcnb2`, `Kcnq2`, `Kcnq3`.
- External literature retrieved through NCBI PubMed:
  - Rhodes et al. 1997, PMID 9334400, DOI 10.1523/JNEUROSCI.17-21-08246.1997.
    This paper coimmunoprecipitated and localized Kvbeta1/Kvbeta2 with Kv1
    alpha subunits in mammalian brain.
  - Baehring et al. 2001, PMID 11294861, DOI 10.1074/jbc.M100483200. This
    work tested the Kvbeta oxidoreductase site and the rapid N-type
    inactivation conferred by Kvbeta1.1.
  - Pongs and Schwarz 2010, PMID 20393197,
    DOI 10.1152/physrev.00020.2009. This review summarizes Kv ancillary
    subunits as cytoplasmic or membrane-associated modulators of channel
    assembly, trafficking, localization, and gating.

## Computations over the training data

I first read the manifest and confirmed that `Kcnab1` was the only requested
held-out target.

From the focal count CSV I summarized the 1,674 observed training targets. The
distribution is sparse in this cell group: 469 / 1,674 training perturbations
had any FDR < 0.05 genes, the median was 0, the 75th percentile was 1, and the
95th percentile was 18. This matters because a prediction of 0 or 1 is not a
rare edge case in this assay; it is the ordinary outcome for many neuronal
genes.

I then filtered the DE parquet to `group_name == "151 TH Prkcd Grin2c Glut"`
and to biologically relevant channel targets. The direct Kv results were:

| training target | observed `n_degs` | focal expression evidence |
|---|---:|---|
| `Kcnab2` | 1 | the sole DEG was `Kcnab2` itself, log2FC -0.744, Wilcoxon score -8.73, FDR 4.38e-14 in 227 perturbed versus 23,679 control nuclei; the next smallest FDRs were 0.302 for `Cdk5r1` and `Extl3` |
| `Kcna1` | 0 | no FDR < 0.05 genes; `Kcna1` itself was only log2FC -0.143, FDR 1 |
| `Kcna2` | 0 | no FDR < 0.05 genes; `Kcna2` itself was log2FC -0.190, FDR 1 |
| `Kcnb1` | 0 | no significant focal-cell genes |
| `Kcnb2` | 0 | no significant focal-cell genes |
| `Kcnc2` | 1 | the single significant gene was the self-transcript `Kcnc2`, log2FC -0.421, FDR 4.6e-5 |
| `Kcnc3` | 1 | the single significant gene was the self-transcript `Kcnc3`, log2FC -0.562, FDR 6.2e-7 |
| `Kcnq2` | 1 | the single significant gene was the self-transcript `Kcnq2`, log2FC -0.776, FDR 2.1e-28 |
| `Kcnq3` | 1 | the single significant gene was the self-transcript `Kcnq3`, log2FC -0.379, FDR 0.0072 |

Across all `Kcn*` training perturbations in the focal cell group, 14 / 20 had
zero DEGs and 6 / 20 had one DEG. I also checked nearby excitability genes:
`Hcn1` had 0, `Hcn2` had 1, `Scn1a` had 1, `Scn2a` had 1, `Scn8a` had 1, and
most calcium-channel subunits had 0 or 1, with `Cacna1g` as the notable focal
exception at 12. This provides a counterexample showing that a channel gene can
produce a multi-gene thalamic signature, but that this is not the typical
Kv/Kvbeta pattern.

The Distributed Agents runtime profile comparison used signed Wilcoxon scores over all
17,259 focal measured genes. `Kcnab2` had one significant negative feature.
Its whole-profile Pearson correlations to the candidate Kv peers were all near
zero: `Kcna1` 0.0408, `Kcna2` 0.0262, `Kcnc3` 0.0215, `Kcnq3` 0.0191,
`Kcnb2` -0.0005, `Kcnq2` -0.0117, `Kcnb1` -0.0158, `Kcnc2` -0.0432. I used
these only to rule out a recurrent downstream Kv expression program; they do
not mean that `Kcnab2` is mechanistically unrelated to `Kcna1` or `Kcna2`.

Finally, I checked whether `Kcnab1` is at least a measurable feature in this
focal DE matrix. It is: across the 1,674 non-held-out perturbations the
measured `Kcnab1` row has a roughly null centered score distribution, and in
strong broad responders `Kcnab1` itself passed FDR, for example `Uba5`,
`Rnpc3`, `Prpf6`, `Tardbp`, and `Sin3a`. That made a self-transcript hit
plausible for the held-out `Kcnab1` KO rather than forcing a zero simply
because of absent focal expression.

## Biological transfer to Kcnab1

`Kcnab1` encodes Kvbeta1, a cytoplasmic auxiliary subunit of voltage-gated
potassium channels. Rhodes et al. showed that Kvbeta1 and Kvbeta2 associate
with Kv1 alpha subunits in mammalian brain. Baehring et al. showed that Kvbeta
subunits couple an oxidoreductase active site to Kv gating, and specifically
that a Kvbeta1.1 N-terminal inactivation domain can confer rapid N-type
inactivation on otherwise non-inactivating Kv channels. Pongs and Schwarz
reviewed the larger principle that Kv ancillary subunits influence assembly,
trafficking, compartmental targeting, and gating rather than acting as direct
transcriptional regulators.

That biology makes the observed `Kcnab2` perturbation the closest represented
training analog: `Kcnab2` is the other measured neuronal Kvbeta gene in the
training DEG table. The next most relevant comparators are `Kcna1` and
`Kcna2`, the represented Kv1 alpha-subunit partners. Their observed focal-cell
counts were 1, 0, and 0, respectively.

The Distributed Agents corpus independently makes the same separation. Its high-
confidence Kv1/Kvbeta claims state that represented voltage-gated potassium
channel and Kv-complex perturbations did not produce a robust shared downstream
neuronal nuclear mRNA program, and that Kv1-channel or juxtaparanodal
structural relationships did not become a shared basal snRNA-seq state in this
screen. The `Kcnab2:F001` finding reports that `Kcnab2` CRISPR generated no
downstream FDR < 0.10 genes in any of 22 recovered neuronal groups despite
significant `Kcnab2` self-transcript depletion in five groups. The `Kcnab2:F004`
finding explicitly notes that `Kcnab1` and `Kcnab3` were absent as perturbation
targets but that the represented same-axis genes `Kcna1`, `Kcna2`, and
`Kcnab2` were flat or self-only.

I therefore expect `Kcnab1` loss to resemble `Kcnab2` at the nuclear RNA level:
the primary effect should be on Kv1 channel gating/localization physiology, and
the sparse postnatal mosaic perturbation should not launch a sustained
activity, stress, synaptic, or homeostatic transcriptional module in `151 TH
Prkcd Grin2c Glut` nuclei. Because `Kcnab1` is measurable in the focal matrix
and because the closest Kvbeta perturbation, `Kcnab2`, had exactly one DEG
from self-transcript loss, my point prediction is one DEG total, not zero.

## Prediction

| target | predicted count | rationale |
|---|---:|---|
| `Kcnab1` | 1 | likely self-transcript depletion only; no predicted downstream FDR < 0.05 genes |

## Limits of the reasoning

The central limitation is that the best analog, `Kcnab2`, is not identical to
`Kcnab1`: Kvbeta1 has inactivating N-terminal isoforms, Kvbeta2 is more often a
trafficking/localization partner, and the subunits have different brain-region
distributions. The data also do not report the hidden `Kcnab1` perturbation's
matched nucleus count, indel rate, or protein loss. A low cell count or weak
self-RNA destabilization could turn the predicted single self hit into zero,
whereas a stronger perturbation in a more `Kcnab1`-dependent thalamic subset
could add one or a few downstream activity-regulated genes. External
electrophysiology predicts Kv-current changes, not necessarily snRNA-seq DEG
counts, so the downstream-null part of the prediction is driven mainly by
within-dataset `Kcnab2`/`Kcna1`/`Kcna2` evidence and the Distributed Agents same-
experiment corpus.
