# Prediction task

The requested output is a point prediction for the number of genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` after acute P16
AAV-CRISPR loss of each held-out target in the focal
`151 TH Prkcd Grin2c Glut` neuronal group.  The manifest contained one
held-out target, in order:

```text
Hmgb1
```

I treated the endpoint exactly as the supplied training-count CSV defines it:
all measured genes are counted, including the target's own RNA row if that row
passes FDR.  This matters because the training data contain many near-null
perturbations whose only focal DEG is the edited transcript itself.

# Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for exact focal-cell `n_degs` values of all 1,674 non-held-out training
  perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal expression signatures and per-gene Wilcoxon/FDR statistics.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`, queried with
  `target_context`, for interpreted reports around `Set`, `Tlr2`,
  `Arid1a`, `Arid1b`, and `Smarcc2`.
- Distributed Agents Runtime profile tools, using signed Wilcoxon `scores` in the focal
  group, to compare HMGB1-adjacent training perturbations and their nearest
  in-dataset expression neighbors.
- External literature from PubMed:
  - Calogero et al. 1999, *Nature Genetics*, doi:10.1038/10338, PMID
    10391216.
  - Agresti and Bianchi 2003, *Current Opinion in Genetics & Development*,
    doi:10.1016/S0959-437X(03)00023-6, PMID 12672494.
  - Bianchi and Agresti 2005, *Current Opinion in Genetics & Development*,
    doi:10.1016/j.gde.2005.08.007, PMID 16102963.
  - Ross et al. 2020, *Investigative Ophthalmology & Visual Science*,
    doi:10.1167/iovs.61.5.50, PMID 32460314.
  - Ross et al. 2021, *Cells*, doi:10.3390/cells10082010, PMID 34440779.
  - Zhang et al. 2022, *Journal of Neuroinflammation*,
    doi:10.1186/s12974-022-02596-7, PMID 36131309.
  - Paudel et al. 2020, *International Journal of Molecular Sciences*,
    doi:10.3390/ijms21134609, PMID 32610502.

The Distributed Agents corpus did not contain an `Hmgb1`, `Hmgb2`, or `Hmgb3` target
report in this held-out-filtered release.  `Hmgb2` and `Hmgb3` also were not
present in the 1,674-row focal training-count table, so I could not transfer a
measured same-paralog count directly.

# Computational checks

The focal endpoint is very sparse.  In the training-count CSV, 1,205 of 1,674
visible perturbations had `n_degs = 0`; 276 had exactly one DEG; the median was
0; the 95th percentile was only 18; and only 43 perturbations had at least 100
DEGs.  A held-out gene therefore needs strong same-pathway evidence to be moved
into the broad-response tail.

I used Distributed Agents Runtime `profile_compare` over the focal rows of the parquet
with:

- entity column: `gene_target`
- feature column: `names`
- value column: signed Wilcoxon `scores`
- significance column: `pvals_adj < 0.05`
- context: `group_name == "151 TH Prkcd Grin2c Glut"`

The hand-selected profile cohort contained an HMGB1-adjacent inflammatory axis
(`Trp53`, `Nfkb1`, `Rel`, `Irf3`, `Stat1`, `Tlr2`, `Tlr4`, `Ager`), the
available general nuclear comparator `Set`, and a chromatin-remodeler
counterexample panel (`Arid1a`, `Arid1b`, `Arid2`, `Smarcc2`, `Smarca4`,
`Bicra`, `Smarce1`, `Smarcd1`, `Brd4`, `Chd8`, `Chd4`, `Ctcf`).

I also checked whether training counts include target self-transcript hits with:

```sql
SELECT gene_target, names, logfoldchanges, pvals_adj, scores
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND names = gene_target;
```

In the focal group, 319 of 1,642 present self rows passed FDR 0.05.  `Arid1b`
is the important calibration example: its training count is `n_degs = 1`, and
the one significant feature in the profile inspection was the `Arid1b` RNA row
itself.  This kept me from equating "no expected downstream response" with an
automatic point prediction of zero.

# Local analogs and counterexamples

| training perturbation | focal `n_degs` | relevance to `Hmgb1` |
| --- | ---: | --- |
| `Set` | 0 | Nuclear chromatin-associated SET was the closest visible "small abundant nuclear regulator" analog.  In the Distributed Agents corpus it caused no focal FDR 0.05 genes and only a single resolved downstream hit in another cell group; profile-neighbor cosines to focal broad responders were tiny, for example `Set` to `Brd4` Pearson r = 0.058 and `Set` to `Ctcf` r = 0.045. |
| `Trp53` | 0 | HMGB1 can modulate p53-linked DNA-damage biology, but acute `Trp53` loss was focal-null. |
| `Nfkb1`, `Rel`, `Irf3`, `Tlr2`, `Tlr4`, `Ager` | 0 each | Extracellular HMGB1 signals through TLR2/TLR4/RAGE and NF-kappaB in glial or injury contexts.  These represented receptor/transcription-factor nodes were all focal-null and had no meaningful mutual expression similarity in the focal profile inspection; all Pearson r values among `Tlr2`, `Tlr4`, `Ager`, `Nfkb1`, `Rel`, `Irf3`, and `Stat1` were near zero. |
| `Stat1` | 1 | One weak focal DEG; useful as a ceiling for the quiescent innate-interferon comparison. |
| `Arid1b` | 1 | A strong developmental chromatin-disease gene was nearly buffered in this same acute P16 NeuN+ context; its one focal hit was the self RNA.  The same-experiment corpus explicitly reports that `Arid1b` did not phenocopy active BAF relatives. |
| `Smarca4`, `Bicra`, `Smarcd1` | 0, 0, 1 | Additional mSWI/SNF relatives showing that chromatin-family membership alone does not imply a focal response. |
| `Smarce1`, `Arid1a`, `Arid2`, `Chd8`, `Chd4`, `Smarcc2`, `Ctcf`, `Brd4` | 11, 22, 56, 61, 100, 185, 270, 311 | Counterexamples proving that the 151 thalamic group can produce real chromatin/regulatory signatures.  They are not direct HMGB1 analogs: these factors are remodeler subunits or strong regulatory proteins with compact recurrent focal modules, whereas HMGB1 is a dynamic DNA-bending architectural protein. |

The BAF/cBAF comparisons were especially useful as guardrails.  The corpus
claim over `Arid1a`, `Arid1b`, `Arid2`, `Bicra`, `Smarca4`, `Smarcc2`,
`Smarcd1`, and `Smarce1` describes a subunit-selective focal BAF/mSWI/SNF
module: `Smarcc2`, `Smarce1`, and `Arid1a` converge; `Arid2` is partial; but
`Smarca4`, `Bicra`, `Smarcd1`, and `Arid1b` are flat, weak, or divergent.  Thus
even members of one chromatin complex span 0 to 185 focal DEGs at FDR 0.05.
HMGB1 should not be imputed to the high end of the chromatin distribution
without a direct same-complex or same-module link.

For the inflammatory/extracellular axis, the Distributed Agents corpus has a high-
confidence TLR2 report: acute `Tlr2` loss produced 0 downstream FDR 0.10 genes
across all recovered NeuN+ neuronal groups, and represented TLR/IL1R/NF-kappaB
relatives did not converge on a basal neuronal inflammatory module.  The `Ager`
report similarly notes that `Hmgb1` ligands were absent as target perturbations
and that `Ager` had no convergence with represented RAGE, amyloid, TLR, or
NF-kappaB pathway comparators.  This is exactly the context boundary for
HMGB1's DAMP biology.

# Biological rationale for `Hmgb1`

HMGB1 is an abundant, non-histone HMG-box chromatin protein.  It binds distorted
or bent DNA and helps bend DNA for transcription-factor and nucleosome
transactions; HMG-box proteins are dynamic architectural factors rather than
stable, sequence-specific remodeler subunits (Agresti and Bianchi 2003; Bianchi
and Agresti 2005).  Germline Hmg1/Hmgb1-null mice are born but die within 24
hours from hypoglycaemia; Hmg1-null cell lines grow, and the original knockout
paper concluded that HMG1 was not required for overall nuclear chromatin
organization but was needed for particular transcriptional responses such as
glucocorticoid-receptor activation (Calogero et al. 1999).

That biology points away from a catastrophic, hundreds-of-DEGs thalamic
signature after sparse postnatal CRISPR.  The most relevant local facts agree:
the general nuclear comparator `Set` is focal-null, `Arid1b` is self-only, and
several chromatin-family members are flat despite others in the same focal
cell group being active.  HMGB1 is therefore better modeled as buffered or
self-only than as a `Brd4`/`Ctcf`/`Smarcc2`-scale chromatin perturbation.

HMGB1 also has a second, extracellular life as a damage-associated inflammatory
signal.  It can be released or translocated during injury, retinal detachment,
radiation, traumatic brain injury, or other stress, and it can activate
microglial TLR2/TLR4/RAGE signaling (Ross et al. 2020; Ross et al. 2021; Zhang
et al. 2022; Paudel et al. 2020).  I did not use that literature to raise the
prediction, because the focal experiment is an unstimulated NeuN-enriched
postnatal neuronal assay with glia under-sampled.  Consistently, `Tlr2`,
`Tlr4`, `Ager`, `Nfkb1`, `Rel`, and `Irf3` all had 0 focal DEGs in the training
set.

The only upward adjustment from a pure zero is the endpoint's inclusion of
the self-transcript row.  HMGB1 is a highly expressed nuclear gene, and the
training focal table contains many weak perturbations scored as `n_degs = 1`
because only the edited transcript itself crosses FDR.  I therefore predict
one FDR-significant gene, interpreted as a likely `Hmgb1` self-row with no
additional downstream focal program.

# Final target-specific decision

| held-out target | predicted `n_degs` | decision |
| --- | ---: | --- |
| `Hmgb1` | 1 | Weak nonzero.  The local and external evidence predict no broad downstream HMGB1 program in healthy P16-to-P37/44 thalamic glutamatergic neurons.  The count is set to 1 rather than 0 solely because an abundant self-transcript hit is plausible and self hits are included in the training endpoint. |

# Limits

- `Hmgb1`, `Hmgb2`, and `Hmgb3` were not present as measured training
  perturbations, so there was no same-family expression signature to transfer.
- HMGB1's chromatin role is broad but unusually architectural; `Set` and BAF
  relatives are imperfect proxies and mostly serve to bound likely response
  scale.
- The predicted `1` hinges on target self-RNA passing FDR.  The dataset
  portrait warns that self-RNA loss is a noisy QC feature under sparse CRISPR;
  it can be absent despite functional edits, so the true count could be 0 if
  the `Hmgb1` mRNA row is buffered.
- The inflammatory HMGB1 literature is mostly stress-, injury-, microglia-,
  astrocyte-, or photoreceptor-dependent.  It supports excluding a basal
  neuronal DAMP signature, but it cannot predict whether a challenged glial or
  retinal HMGB1 knockout would be broad.
- All reasoning is survivor-conditioned nuclear RNA 3-4 weeks after AAV
  delivery.  DNA indels, HMGB1 protein depletion, extracellular release,
  chromatin accessibility, autophagy flux, electrophysiology, and cell
  depletion were not measured in the supplied inputs.
