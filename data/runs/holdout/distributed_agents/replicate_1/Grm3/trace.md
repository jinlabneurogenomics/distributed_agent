# Grm3 DEG-count prediction

## Question and endpoint

The held-out target list for this run contains one gene, `Grm3`. I interpreted
the task as a point prediction for the exact focal-cell endpoint:

```
n_degs = count of measured genes with Wilcoxon BH-adjusted pvals_adj < 0.05
         in 151 TH Prkcd Grin2c Glut for the Grm3 perturbation
```

`Grm3` was completely held out: its own perturbation signature and count are
not in the Parquet or the training-count CSV. The training CSV counts include
the targeted transcript when that transcript itself passes FDR, so a visible
one-gene count for related GPCRs can be only the self-transcript rather than a
downstream program.

## Sources used

- Declared differential-expression Parquet:
  `training differential-expression dataset`.
  This is the direct same-experiment source for focal-cell Wilcoxon statistics
  in non-held-out perturbations.
- Declared training endpoint CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This gives the observed `n_degs` for the 1,674 visible training targets in
  `151 TH Prkcd Grin2c Glut`.
- Declared held-out manifest:
  `single-target request for Grm3`.
- Run-local dataset portrait, bindings, coverage, and measurement registry
  under `codex_runtime/pipeline/`.
- Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, specifically packaged Findings
  and target reports for `Grm1`, `Grm5`, `Grm6`, `Grm7`, `Grm8`, and `Gnao1`.
  I used this as bounded interpretation of visible training perturbations, not
  as independent replication of the Parquet.
- External literature from PubMed:
  - Tanabe et al. 1993, J Neurosci, DOI 10.1523/JNEUROSCI.13-04-01372.1993,
    PMID 8463825.
  - Liu, Munoz and Jones 1998, J Comp Neurol, DOI
    10.1002/(sici)1096-9861(19980615)395:4<450::aid-cne3>3.0.co;2-0,
    PMID 9619499.
  - Tamaru et al. 2001, Neuroscience, DOI
    10.1016/s0306-4522(01)00305-0, PMID 11591452.
  - Harrison et al. 2008, J Psychopharmacol, DOI
    10.1177/0269881108089818, PMID 18541626.
  - Mazzitelli et al. 2018, Front Mol Neurosci, DOI
    10.3389/fnmol.2018.00383, PMID 30356691.

## Dataset calculations

I first summarized the focal-class training counts. The distribution was very
zero-inflated: 1,205/1,674 visible biological perturbations had `n_degs = 0`,
the median was 0, the 75th percentile was 1, and the 90th percentile was 2.
Thus a single receptor perturbation needs positive same-experiment evidence
before predicting a broad DEG response.

I then queried the Parquet for `151 TH Prkcd Grin2c Glut` and a mechanistically
chosen set of metabotropic glutamate receptors, ionotropic glutamate receptors,
Gi/o-cAMP branch genes, and calcium/calcineurin genes. The exact DuckDB query
was a column-filtered Parquet read:

```sql
select gene_target,
       sum(pvals_adj < 0.05) as sig05,
       sum(pvals_adj < 0.10) as sig10,
       min(pvals_adj) as min_fdr,
       count(*) as tested,
       min(n_pert_matched) as n_pert,
       max(n_ctrl_matched) as n_ctrl
from read_parquet('training_de_all_cell_groups.parquet')
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target
```

The focal-class observations most relevant to `Grm3` were:

| training target | focal `n_degs` at FDR<0.05 | pattern in `151 TH Prkcd Grin2c Glut` |
| --- | ---: | --- |
| `Grm1` | 1 | only the `Grm1` self-transcript passed FDR; no downstream gene passed 0.05 |
| `Grm5` | 0 | no FDR<0.05 genes |
| `Grm6` | 0 | no FDR<0.05 genes |
| `Grm7` | 1 | only the `Grm7` self-transcript passed FDR; no downstream gene passed 0.05 |
| `Grm8` | 0 | no FDR<0.05 genes |
| `Gnao1` | 1 | only the `Gnao1` self-transcript passed FDR |
| `Gnas` | 0 | no FDR<0.05 genes |
| `Gnb5` | 0 | no FDR<0.05 genes |
| `Adcy1` | 0 | no FDR<0.05 genes |
| `Adcy3` | 0 | no FDR<0.05 genes |
| `Adcy5` | 0 | no FDR<0.05 genes |
| `Gabbr1` | 1 | self-transcript-only at FDR<0.05 |
| `Gabbr2` | 1 | self-transcript-only at FDR<0.05 |
| `Grin1` | 89 | many downstream genes; obligate NMDA-receptor subunit, not a GPCR analog |
| `Grin2a` | 1 | self-transcript-only at FDR<0.05 |
| `Grin2b` | 2 | `Grin2b` plus one downstream gene |
| `Grin2d` | 0 | no FDR<0.05 genes |
| `Grin3a` | 0 | no FDR<0.05 genes |

This separates two kinds of glutamate-receptor perturbation. `Grin1` can
generate a substantial durable RNA state in this thalamic glutamatergic class,
consistent with its obligate role in NMDA receptors. In contrast, loss of
single metabotropic glutamate receptors, G-protein subunits, adenylyl cyclases,
or non-obligate NMDA subunits mostly landed at zero or at a self-transcript
only count.

As a weak proxy for whether `Grm3` RNA is even visible in the focal class, I
also queried rows where `Grm3` was the measured gene under all visible
perturbations. There were 1,674 `151 TH Prkcd Grin2c Glut` tests for measured
`Grm3`, and none had FDR<0.10; the minimum adjusted p-value was 0.967. That is
not baseline expression, but such uniformly uninformative DE tests are more
consistent with sparse/low neuronal nuclear detection than with a strongly
measured focal-cell transcript.

## Target-specific biological reasoning

### `Grm3`

`Grm3` encodes mGluR3, a group-II metabotropic glutamate receptor. Group-II
mGluR2/3 receptors couple through Gi/o proteins to negatively regulate
adenylyl cyclase and typically suppress transmitter release rather than
directly encoding a nuclear transcription-factor pathway. Tanabe et al. showed
that cloned mGluR3 inhibits forskolin-stimulated cAMP formation and that
`Grm3` mRNA is widespread, with prominent glial expression. Harrison et al.
reviewed mGluR3 as a receptor expressed by glia and neurons with roles in
glutamate transmission, synaptic plasticity, long-term depression, glial
function, neuroprotection, and schizophrenia-related pharmacology. Mazzitelli
et al. similarly summarize mGlu2/3 as Gi/o-coupled presynaptic inhibitory
receptors.

The relevant experimental chain is therefore:

1. P16 AAV CRISPR produces mosaic `Grm3` loss of function in a minority of
   recovered nuclei.
2. The direct molecular consequence is reduced mGluR3 signaling, mostly a
   receptor-level and Gi/o-cAMP/presynaptic effect.
3. mGluR3 biology can propagate through glutamate release, synaptic plasticity,
   or glial-neuronal regulation; those are not obligate steady-state nuclear
   mRNA outputs.
4. NeuN enrichment keeps the measured surface focused on neuronal nuclei and
   under-samples the glial compartment where mGluR3 is repeatedly reported.
5. The endpoint is a recovered-cell Wilcoxon DEG count 3-4 weeks after editing,
   so transient synaptic or evoked cAMP effects would be missed unless they
   left a stable cell-body RNA state.

Within the focal DE dataset, the best available same-experiment analogs all
argue for a null or self-only count:

- `Grm1` is a strong biological comparator for "single mGluR loss", although
  it is group I rather than group II. It had one focal DEG, the `Grm1`
  self-transcript, and the internal July corpus reported that all recovered
  `Grm1` groups were downstream-null at FDR<0.10 after excluding `Grm1`.
  Its report also checked `Arc`, `Fos`, `Egr1`, `Bdnf`, `Fmr1`,
  `Homer1-3`, `Itpr1`, `Trpc3`, `Prkcg`, and `Grm5` and found no
  sustained expected group-I response.
- `Grm5`, the other group-I receptor, is another postsynaptic mGluR
  comparator. It had zero focal DEGs. Its internal report called it a pan-null
  basal-snRNA perturbation across 22 recovered neuronal groups and found the
  stimulated mGluR5 IEG/synaptic-plasticity panel absent.
- `Grm7` and `Grm8` are group-III presynaptic Gi/o mGluR comparators. `Grm7`
  had one focal DEG, again only the self-transcript; `Grm8` had zero. Their
  reports found no durable activity-state or cAMP-response program and no
  robust mGluR-family convergence.
- `Gnao1`, `Gnas`, `Gnb5`, `Adcy1`, `Adcy3`, and `Adcy5` sample the
  heterotrimeric G-protein/adenylyl-cyclase signaling layer downstream of
  Gi/o-coupled receptors. All were zero or self-only in the focal class; the
  `Gnao1` report likewise described the response as overwhelmingly buffered
  rather than a chronic GPCR/cAMP RNA program.
- `Grin1` is the main counterexample: it produced 89 focal DEGs and a clear
  survivor-state response. I did not transfer that count to `Grm3` because
  GluN1 is an obligate ion-channel subunit of NMDA receptors, whereas mGluR3 is
  one modulatory GPCR whose direct loss should first affect second-messenger
  tone and transmitter release. The weaker `Grin2a`, `Grin2b`, `Grin2d`, and
  `Grin3a` focal counts further reject a rule that every glutamate-receptor
  perturbation yields a broad thalamic RNA response.

The literature makes the same direction plausible rather than rescuing a
positive prediction. Liu et al. found that mGluR2/3 immunoreactivity in mouse
ventral posterior thalamus was mainly astrocytic throughout postnatal
development, with only a small number of labeled presynaptic terminals. Tamaru
et al. localized mGluR3 to pre- and postsynaptic elements and glial profiles in
mouse CNS, but also noted that presynaptic mGluR3 in striatum and thalamus was
mostly not closely associated with glutamate or GABA release sites. Those
papers support real mGluR3 biology, but they place a substantial part of it in
subcellular or glial compartments that this NeuN-enriched, basal snRNA assay is
not designed to count as a durable neuronal nuclear response.

I therefore predict `Grm3` will have no measured gene below BH FDR 0.05 in
`151 TH Prkcd Grin2c Glut`. A count of 1 would be plausible if the self
transcript were sufficiently expressed and depleted, as happened for `Grm1`
and `Grm7`; however, focal measured-gene rows for `Grm3` were uniformly
uninformative across all visible perturbations, and thalamic group-II
immunoreactivity is reported to be mostly glial, so I put the point estimate at
0 rather than 1.

## Limits

The prediction is an extrapolation from related visible targets, not a direct
`Grm3` measurement. `Grm2`, the closest group-II paralog, was not represented
as a visible perturbation, and the Parquet has no held-out `Grm3` self-row.
The focal-cell count is also assay- and power-dependent: weak editing,
low target expression, sparse cell recovery, or a real effect restricted to
astrocytes, presynaptic terminals, evoked signaling, local translation,
neuroprotection, or earlier development could all yield zero focal nuclear
DEGs. The same-experiment corpus is a curated interpretation of the same
Parquet surface and therefore helped choose analogs and summarize expression
patterns, but it was not treated as independent validation.
