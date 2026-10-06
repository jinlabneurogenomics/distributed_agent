# Reasoning trace

## Question and resolved ambiguities

The held-out manifest for this run contains one perturbation:

```tsv
target_name
Dock7
```

I interpreted the requested value as the exact endpoint used in the supplied
training-count table: for a `Dock7` CRISPR loss-of-function perturbation in
`151 TH Prkcd Grin2c Glut`, predict the number of measured genes with
`pvals_adj < 0.05` in the single-nucleus Wilcoxon differential-expression
result.  I counted the perturbed target's own mRNA as eligible for this endpoint
when it passes the same FDR cutoff, because the training CSV does the same
thing; for example `Cdc42`, `Pak1`, and `Cyfip2` each have one focal DEG and in
each case that single DEG is the target transcript itself.

## Sources used

- Focal requested-target manifest:
  `[local file: 061_Dock7.csv]`
- Per-cell-group differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile-neighbor/profile-compare tools over the local
  parquet
- PubMed-indexed DOCK7 literature:
  - Watabe-Uchida et al. 2006, DOI `10.1016/j.neuron.2006.07.020`
  - Yamauchi et al. 2008, DOI `10.1083/jcb.200709033`
  - Yang et al. 2012, DOI `10.1038/nn.3171`
  - Zhou et al. 2013, DOI `10.1021/bi301688g`
  - Tai et al. 2014, DOI `10.1016/j.celrep.2013.12.034`
  - Perrault et al. 2014, DOI `10.1016/j.ajhg.2014.04.012`
  - Gadea and Blangy 2014, DOI `10.1016/j.ejcb.2014.06.003`
  - Kukimoto-Niino et al. 2019, DOI `10.1016/j.str.2019.02.001`

## Computational steps

1. Read the manifest and confirmed that the only held-out target was `Dock7`.

2. Read the focal training-count CSV to get the observed endpoint for all
   eligible non-held-out perturbations.  The endpoint distribution is extremely
   zero-inflated in this cell type: among 1,674 training targets the median was
   `0`, the 75th percentile was `1`, the 90th percentile was `2`, the 95th
   percentile was `18`, and the largest response was `2677`.

3. Queried the focal parquet rows for biologically plausible `Dock7` analogs
   and counterexamples using a PyArrow dataset filter:

   - `group_name == "151 TH Prkcd Grin2c Glut"`
   - `gene_target` in the direct Rac/Cdc42, PAK/LIMK/cofilin, WAVE/GEF,
     NRG/ErbB, and Wnt/beta-catenin comparator set

   This returned 293,403 focal DE rows, exactly 17,259 measured genes for each
   of 17 training perturbations.  I then counted rows with `pvals_adj < 0.05`
   and inspected whether those rows were on-target self effects or downstream
   genes.

4. Ran Distributed Agents `profile_compare` on the same 17 analog/counterexample
   perturbations using focal `logfoldchanges`, the training target universe as
   eligible nodes, `pvals_adj < 0.05` as the significance threshold, and
   `names` as the feature column.  This was a signed whole-profile check to
   determine whether near-zero endpoints such as `Rac1` and `Dock3` nevertheless
   had a reproducible subthreshold expression pattern.  In this comparison, 11
   of the 17 candidate perturbations had no focal FDR features, five had only
   1 to 9 FDR features, and only `Ctnnb1` had a broad response with more than 50
   features.

5. Queried the Distributed Agents corpus for the direct observed contexts of `Cdc42`,
   `Rac1`, `Dock3`, and `Erbb4`, and searched corpus claims containing
   Rac/Cdc42/PAK actin signaling.  These searches provided same-experiment
   calibration that the represented Rac/Cdc42 cytoskeletal branch is generally
   transcriptionally buffered in the juvenile neuronal snRNA-seq assay.

## Within-dataset analogs and target-specific prediction

### Dock7

**Biological prior.**  DOCK7 is an atypical DOCK-family guanine-nucleotide
exchange factor.  Its DHR2 domain can activate Rac1 and Cdc42, with structural
work explaining its dual GTPase specificity (Zhou et al. 2013; Kukimoto-Niino
et al. 2019).  In neurons, DOCK7 was first tied to axon specification through a
Rac/stathmin pathway (Watabe-Uchida et al. 2006).  Other experimentally defined
roles place it in TACC3-dependent radial-glial interkinetic nuclear migration
and neurogenesis (Yang et al. 2012), NRG1/ErbB2-dependent Schwann-cell migration
(Yamauchi et al. 2008), and ErbB4-dependent chandelier-cell cartridge/bouton
development (Tai et al. 2014).  Human biallelic truncating DOCK7 variants cause
an epileptic encephalopathy with cortical blindness, supporting a real
neurodevelopmental requirement for the gene (Perrault et al. 2014).

Those mechanisms point mostly to Rac/Cdc42 loading, phosphorylation, local
cytoskeletal remodeling, axon/interneuron morphogenesis, radial-glial
development, and peripheral Schwann-cell migration.  They are biologically
important, but they are not obvious broad basal nuclear mRNA programs in
sparsely edited postmitotic thalamic glutamatergic neurons.

**Directly relevant focal training counts.**

| training target | focal `n_degs` | interpretation for `Dock7` |
| --- | ---: | --- |
| `Dock3` | 0 | closest represented DOCK-family Rac GEF; no focal DEGs, and its own transcript was only nominally reduced (`logFC = -0.430`, raw `p = 2.4e-4`, `padj = 0.709`) |
| `Rac1` | 0 | direct DOCK7 substrate; no focal FDR genes and no detectable target self decrease |
| `Cdc42` | 1 | direct DOCK7 substrate; the lone focal DEG was `Cdc42` itself (`logFC = -0.593`, `padj = 8.6e-5`) |
| `Pak1` | 1 | group-I PAK downstream of Rac/Cdc42; one self-only focal DEG |
| `Pak2` | 0 | group-I PAK; no focal DEGs |
| `Pak3` | 0 | group-I PAK; no focal DEGs |
| `Limk1` | 0 | downstream PAK/cofilin effector; no focal DEGs |
| `Cfl2` | 0 | cofilin-family actin effector; no focal DEGs |
| `Tiam1` | 0 | represented Rac GEF at synaptic/Rac signaling; no focal DEGs |
| `Kalrn` | 0 | neuronal Rac/Rho GEF; no focal DEGs |
| `Cyfip1` | 0 | WAVE-regulatory-complex Rac effector; no focal DEGs |
| `Cyfip2` | 1 | WAVE-regulatory-complex Rac effector; one self-only focal DEG |
| `Fyn` | 0 | Src-family synaptic kinase and an NRG/ErbB-adjacent comparator; no focal DEGs |
| `Erbb4` | 0 | receptor in a published DOCK7-dependent chandelier-cell morphogenesis pathway; no focal DEGs in this thalamic glutamatergic class |

The same-experiment Distributed Agents corpus independently summarized this sector as
buffered: the high-confidence Rac/Cdc42 actin-cytoskeleton claim states that
represented Rho/Rac/Cdc42, Rac/EphB/PAK/WAVE, Kalirin/Tiam1, PAK/LIMK/cofilin,
and related perturbations are transcriptionally buffered in juvenile neurons
rather than forming a recurrent shared nuclear mRNA module.  `Cdc42`'s corpus
context specifically records that even though `Cdc42` mRNA was significantly
reduced in `151 TH Prkcd Grin2c Glut`, no robust downstream transcriptional
response appeared in any recovered neuronal class.  `Rac1`'s context similarly
reports a largely buffered surface: 21 of 22 groups had no FDR<0.10 downstream
genes and the only positive group had a single non-convergent `Ranbp1` event.
`Dock3`'s context reports no robust downstream snRNA-seq response in any
recovered neuronal cell group and no convergence with `Rac1`, WAVE components,
or `Gsk3b`.

The focal profile comparison did not rescue these near-zero counts into a
hidden coherent signature.  `Cdc42`, `Rac1`, and `Dock3` had zero shared
FDR-significant focal features pairwise.  Their leading positive and negative
features in the focal class were all nonsignificant (`padj = 1` in the bounded
inspection), and the top-feature overlaps among `Cdc42`, `Rac1`, `Dock3`,
`Pak1`, `Pak2`, `Pak3`, `Limk1`, and `Cfl2` were tiny.  This argues that the
low counts are not simply the visible tips of a subthreshold Dock-like or
Rac-like mRNA module.

**Counterexamples and boundaries.**  The assay can detect broad thalamic
transcriptional states when the perturbed target is a constitutive nuclear or
pathway hub: in the same focal class, `Ctnnb1` produced 383 DEGs and `Gsk3b`
produced 6, and `Lrp6` produced 4.  These were not treated as Dock7 analogs.
`Ctnnb1` is a beta-catenin transcriptional co-regulator and sits at the nuclear
output of canonical Wnt signaling, whereas DOCK7's literature-supported outputs
are primarily GTPase and morphology endpoints.  The corpus Wnt claims also
separate the strong `Ctnnb1`/`Lrp6` thalamic beta-catenin response from many
upstream receptor-layer Wnt perturbations that are flat or sparse.  Therefore
the `Ctnnb1` count is a positive-control boundary for detectability, not a
reason to assign `Dock7` a large Wnt-like count.

**Zero/nonzero call.**  I predict a zero FDR count for `Dock7` in the focal
class.  The prediction is mainly within-dataset: its directly assayed substrate
GTPases, group-I PAK/LIMK/cofilin branch, WAVE effectors, and the closest
represented DOCK-family GEF were all zero or self-only in
`151 TH Prkcd Grin2c Glut`.  External biology reinforced the direction of that
evidence, because DOCK7 is expected to alter Rac/Cdc42 activity, phosphorylation
and neuronal morphology more directly than steady-state nuclear RNA abundance.
I did consider a one-gene prediction for an on-target `Dock7` self-transcript
decrease, but the closest focal precedent, `Dock3`, had a nominal self decrease
that did not survive BH correction, and `Rac1`, `Pak2`, `Pak3`, `Limk1`, and
`Kalrn` similarly did not pass FDR for their own transcripts in this class.

Final point prediction: `Dock7 = 0`.

## Limits

- `Dock7` itself was held out and had no same-experiment perturbation signature
  in the parquet or in the focal training-count CSV.
- The Distributed Agents corpus had no `Dock7`-centered finding in the selected release;
  I therefore used corpus evidence from `Cdc42`, `Rac1`, `Dock3`, `Erbb4`, and
  related actin/Wnt/NRG claims.
- Most DOCK-family genes were not represented as focal training perturbations;
  `Dock3` is informative as a neuronal Rac GEF but is not a paralog with an
  identical effector scaffold.
- The public DOCK7 literature emphasizes embryonic cortical neurogenesis,
  axon specification in cultured neurons, chandelier-cell morphology, and
  Schwann-cell migration.  Those systems differ from sparse P16 CRISPR in
  postmitotic thalamic glutamatergic neurons harvested 3-4 weeks later.
- The prediction does not exclude a real `Dock7` phenotype in GTPase activity,
  microtubules, actin, axons, boutons, or electrophysiology.  Those endpoints
  were simply not measured by this endpoint.
- A self-only `Dock7` mRNA decrease is the main way the true held-out value
  could be `1` rather than `0`; without guide-level indel data or held-out
  perturbed-nucleus counts, that risk cannot be resolved directly.
