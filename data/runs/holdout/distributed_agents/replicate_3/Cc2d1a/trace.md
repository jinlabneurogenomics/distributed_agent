# Held-out DEG-count prediction

## Question and endpoint

The held-out manifest for this run contains one requested perturbation:
`Cc2d1a`. I interpreted the requested endpoint as the exact count that would
be obtained in the focal `151 TH Prkcd Grin2c Glut` differential-expression
contrast by counting measured genes with `pvals_adj < 0.05`, including the
target transcript itself if it passed that threshold. A prediction of `0`
therefore means no measured gene is expected to pass the focal-cell FDR 0.05
threshold, not that the gene is biologically irrelevant or that editing failed.

I treated target-transcript fold change only as one row in the DE table. In
this sparse AAV CRISPR design, weak target mRNA change is not a quantitative
readout of knockout strength, and self-only DE signatures were interpreted as
weak transcriptional evidence.

## Sources used

- The held-out request file,
  `[local file: 031_Cc2d1a.csv]`,
  for the exact target and output order.
- The focal training endpoint file,
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`,
  for observed `n_degs` among the 1,674 non-held-out perturbations.
- The all-cell training differential-expression parquet,
  `[local file: training_de_all_cell_groups.parquet]`,
  filtered to `group_name == "151 TH Prkcd Grin2c Glut"` and to
  candidate analog targets, for the signed expression evidence behind those
  DEG counts.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, queried for packaged findings
  on training analogs. This release had no `Cc2d1a` findings or claims, so it
  was used only for non-held-out analogs such as `Htr1a`, `Nfkb1`, `Rac1`,
  `Mtor`, and `Tsc2`.
- Distributed Agents runtime profile tools, used for a symmetric profile comparison of
  the Cc2d1a-relevant training cohort in the focal cell group.
- PubMed literature:
  - Rogaeva, Galaraga and Albert, 2007, DOI `10.1002/jnr.21277`:
    CC2D1A/Freud-1 family review; Freud-1 represses `Htr1a` through the
    5-prime repressor element and its DNA-binding/repressor activities are
    CaMK-regulated.
  - Rogaeva et al., 2007, DOI `10.1074/jbc.M610038200`: Freud-1/CC2D1A binds
    and represses an intronic element in human `DRD2`.
  - Al-Tawashi et al., 2012, DOI `10.1074/jbc.M111.261875`: CC2D1A mutant
    cells have impaired cAMP/PKA signaling and reduced CREB phosphorylation.
  - Yang et al., 2019, DOI `10.1523/JNEUROSCI.2395-18.2019`: excitatory
    forebrain conditional Cc2d1a deletion impairs hippocampal plasticity and
    dendritic arborization through Rac1 hyperactivation.

## Computation over the input tables

1. I read the manifest and confirmed that `Cc2d1a` is the only requested target.

2. I summarized the focal training counts. Of 1,674 non-held-out targets,
   1,205 had `0` DEGs in `151 TH Prkcd Grin2c Glut`, 363 had 1-9, 63 had
   10-99, and 43 had at least 100. The focal endpoint is therefore strongly
   zero-inflated, and weak mechanistic evidence should default near the null
   rather than to a broad response.

3. I selected candidate training perturbations from the external Cc2d1a
   biology and filtered the parquet to those genes in the focal group. The
   essential operation was:

   ```python
   pd.read_parquet(
       parquet_path,
       columns=["gene_target", "names", "logfoldchanges", "pvals_adj", "scores"],
       filters=[
           ("group_name", "==", "151 TH Prkcd Grin2c Glut"),
           ("gene_target", "in", candidate_targets),
       ],
   )
   ```

   I then counted `pvals_adj < 0.05` per `gene_target` and inspected the
   FDR-passing rows. This reproduced the supplied counts for the candidates.

4. I ran a Distributed Agents runtime `profile_compare` in the same focal context over
   a candidate cohort spanning monoamine receptors, cAMP/PKA/CREB genes,
   NF-kappaB genes, Rac/PAK genes, and the `Mtor`/`Tsc2` contrast:
   `Htr1a`, `Drd2`, `Creb1`, `Crebbp`, `Camk2a`, `Camk2b`, `Prkaca`,
   `Prkar1a`, `Ntrk2`, `Nfkb1`, `Rel`, `Chuk`, `Map3k7`, `Traf3`, `Rac1`,
   `Cdc42`, `Pak1`, `Pak2`, `Pak3`, `Mtor`, and `Tsc2`. Whole-vector
   correlations among these sparse signatures were not decisive because most
   measured genes were unchanged, so I used the actual FDR-passing counts and
   signed DEG rows as the main expression-pattern evidence.

## Target-specific reasoning

### Cc2d1a

`Cc2d1a` has no exact paralog or same-complex perturbation in the training
count table. `Cc2d1b` was not a focal training target, and the Distributed Agents
same-experiment corpus had no `Cc2d1a` records in this release. I therefore
anchored the prediction on four mechanistic neighborhoods.

**Direct Freud-1 receptor targets and monoamine receptors.** Rogaeva,
Galaraga and Albert described CC2D1A/Freud-1 as a transcriptional repressor of
`Htr1a`; Rogaeva et al. showed Freud-1 repression of `DRD2`. In the focal
training data, however, loss of those receptor genes was silent:

| training perturbation | focal `n_degs` | expression evidence |
| --- | ---: | --- |
| `Htr1a` | 0 | no gene passed FDR 0.05 |
| `Drd2` | 0 | no gene passed FDR 0.05 |
| `Htr1b` | 0 | no gene passed FDR 0.05 |
| `Htr2a` | 0 | no gene passed FDR 0.05 |
| `Htr2c` | 0 | no gene passed FDR 0.05 |

The same-experiment corpus also annotated `Htr1a` as a high-confidence
buffered response: across recovered neuronal cell groups, `Htr1a` had
0 downstream FDR 0.10 genes, and represented serotonin receptors were flat or
singleton responders rather than robust phenocopies. These observations are
appropriate lower-bound analogs because they test the most concrete direct
Freud-1 receptor axis in the same perturbation modality. They are imperfect
because Cc2d1a loss may derepress receptor expression rather than phenocopy
receptor loss; nevertheless, if focal thalamic neurons had a high-gain
Htr1a/Drd2 output, at least the receptor knockouts or related serotonin
receptor knockouts would be expected to show some local RNA consequence.

**cAMP/PKA/CREB branch.** Al-Tawashi et al. linked CC2D1A to cAMP/PKA
signaling and CREB phosphorylation. The focal training counts for this pathway
were:

| training perturbation | focal `n_degs` | expression evidence |
| --- | ---: | --- |
| `Adcy1`, `Adcy3`, `Adcy5`, `Gnas`, `Camk2a` | 0 each | no FDR 0.05 genes |
| `Camk2b` | 1 | only `Camk2b` itself was down |
| `Prkaca` | 1 | only `Prkaca` itself was down |
| `Prkar1a` | 1 | only `Prkar1a` itself was down |
| `Ntrk2` | 3 | `Ntrk2`, `Atp2a2`, and `Vgf` were down |
| `Crebbp` | 8 | a small mixed signature, led by `Stxbp2` up and `Rtn4rl1`, `Stmn4`, `Rbfox2`, `Ccdc141`, `Dgkz` down |
| `Creb1` | 10 | `Crem` was up; `Tmem181a`, `Txndc12`, `Chkb`, `Nceh1`, `Ppox`, `Rnf139`, and `Sez6l2` were down |

This neighborhood argues for, at most, a weak nonzero effect from acute partial
`Cc2d1a` loss. The more proximal cyclase, G-protein, PKA, and CaMK
perturbations were all null or self-only, while direct loss of `Creb1` or
`Crebbp` was only an 8-10 gene event. `Creb1` is a downstream transcription
factor whose knockout removes CREB itself; Cc2d1a loss is expected to modulate
PKA-to-CREB signaling rather than delete CREB, so `Creb1` is an upper-bound
counterexample rather than a direct quantitative analog.

**NF-kappaB branch.** CC2D1A was originally identified as an NF-kappaB
activator, but the focal and same-experiment data make the canonical
NF-kappaB branch look transcriptionally buffered under postnatal sparse CRISPR:

| training perturbation | focal `n_degs` | expression evidence |
| --- | ---: | --- |
| `Nfkb1` | 0 | no FDR 0.05 genes |
| `Rel` | 0 | no FDR 0.05 genes |
| `Chuk` | 0 | no FDR 0.05 genes |
| `Map3k7` | 0 | no FDR 0.05 genes |
| `Traf3` | 0 | no FDR 0.05 genes |

The Distributed Agents corpus summarized `Nfkb1` as 0 downstream FDR 0.10 genes in all
22 recovered groups and reported that represented canonical NF-kappaB/TNF/TLR
comparators phenocopied the `Nfkb1` flat state rather than revealing a hidden
related-target response. That makes NF-kappaB an argument for zero in this
assay and cell group, not for a large immune-like module.

**Rac1 / actin-plasticity branch.** Yang et al. found that conditional
Cc2d1a deletion in forebrain excitatory neurons hyperactivated Rac1 and
impaired hippocampal structure and plasticity. The focal Perturb-seq analogs
were again flat or self-only:

| training perturbation | focal `n_degs` | expression evidence |
| --- | ---: | --- |
| `Rac1` | 0 | no FDR 0.05 genes |
| `Cdc42` | 1 | only `Cdc42` itself was down |
| `Pak1` | 1 | only `Pak1` itself was down |
| `Pak2` | 0 | no FDR 0.05 genes |
| `Pak3` | 0 | no FDR 0.05 genes |

The corpus likewise described postnatal neuronal `Rac1` perturbation as
transcriptionally buffered, with only one FDR 0.10 event outside this focal
group and no meaningful transcriptomic neighbor. Because Rac1 hyperactivation
downstream of Cc2d1a is a structural and synaptic-plasticity mechanism rather
than an obligatory acute nuclear RNA module, these flat CRISPR profiles weigh
strongly against predicting a broad focal DEG count.

**Counterexamples used to cap the prediction.** I also checked signaling and
chromatin perturbations that could have produced large effects if Cc2d1a
behaved like a global transcriptional cofactor or mTOR/endosomal regulator:
`Mtor` had only 2 focal DEGs (`Rims3` up, `Tmed8` down), whereas `Tsc2` had
86 DEGs with 58 positive and 28 negative hits, including an mTORC1 metabolic
program (`Cyp51`, `Pik3r3`, `Slc2a6`, `Nsdhl` up). Very broad transcriptional
regulators were much larger: `Sin3a` 1,433, `Ctnnb1` 383, and `Setd1a` 368.
Those are useful counterexamples because they show that this cell group could
produce a large count for the right target, but Cc2d1a lacks evidence for the
same genome-wide chromatin role in postmitotic thalamic neurons.

## Final decision

I predicted `Cc2d1a` as `0` DEGs. The decision was driven mainly by
within-dataset evidence: every direct or pathway-proximal training analog in
the monoamine-receptor, NF-kappaB, Rac/PAK, and PKA branches was zero or a
1-gene self-target signature, with only the downstream `Creb1`/`Crebbp` pair
reaching a weak 8-10 gene response. External literature justified why those
training genes were the relevant comparators, but did not provide a reason to
upgrade Cc2d1a into the high-count class seen for broad chromatin regulators or
for `Tsc2`.

## Limits

This is an extrapolation because the exact paralog `Cc2d1b` was absent from
the focal training table and the same-experiment corpus had no `Cc2d1a`
finding to retrieve. The known Cc2d1a mouse phenotypes come mostly from
germline, conditional, or shRNA systems in hippocampus, not from sparse AAV
CRISPR in juvenile thalamic `Prkcd`/`Grin2c` glutamatergic neurons. `Cc2d1a`
could in principle have direct transcriptional targets outside `Htr1a` and
`Drd2`, or a thalamus-specific role that is not represented by the training
analogs. The zero call therefore means that the best matched evidence places
the focal response below the assay's FDR 0.05 detection threshold; it does not
rule out electrophysiological, dendritic, receptor-level, or subthreshold RNA
changes.
