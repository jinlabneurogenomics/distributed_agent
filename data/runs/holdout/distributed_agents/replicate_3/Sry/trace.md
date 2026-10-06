# Held-out prediction: 151 TH Prkcd Grin2c Glut

## Question and interpretation

The requested held-out target list contains one perturbation, `Sry`.  I interpreted
`n_degs` as the exact endpoint used for the training CSV: the number of measured
genes with `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` group.
The target was held out completely, so I did not look for a direct `Sry` row in
the count table or treat an absent `Sry` signature as a measured zero.  The cell
group name uses Allen taxonomy nomenclature; the `TH` in the label denotes a
thalamic population, not necessarily tyrosine hydroxylase-positive dopamine
neurons.

I resolved the main ambiguity as follows: a Y-linked target in a mixed-sex AAV
screen should be predicted for the pooled perturbation label, not for male nuclei
alone.  Thus any male-limited biology of Sry would be diluted by female cells
that carry Sry guide RNAs but have no Sry locus.

## Sources

Local data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for focal training counts.
- `[local file: training_de_all_cell_groups.parquet]`
  for log2 fold changes and BH-adjusted p-values in matched focal comparisons.
- `224_Sry.csv` for the requested target order.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`.  `Sry` itself had no frozen
  corpus target context, but the corpus had curated findings for `Sox2` and
  `Sox5` and a SOX-family claim useful as within-dataset calibration.
- Run-local Distributed Agents profile comparison
  `sry_analog_profile_compare.json`, comparing represented SOX, steroid receptor,
  and gonadal-axis perturbations in `151 TH Prkcd Grin2c Glut`.

External biological evidence came from PubMed-indexed literature:

- Milsted et al. 2004, Neuroscience Letters, DOI `10.1016/j.neulet.2004.07.052`,
  PMID `15464265`: Sry can activate the tyrosine hydroxylase promoter in
  catecholaminergic-cell models.
- Dewing et al. 2006, Current Biology, DOI `10.1016/j.cub.2006.01.017`, PMID
  `16488877`: Sry is expressed in adult male rodent substantia nigra TH-positive
  neurons and antisense Sry knockdown in substantia nigra reduces tyrosine
  hydroxylase expression and motor output.
- Czech et al. 2012, Journal of Neurochemistry, DOI
  `10.1111/j.1471-4159.2012.07782.x`, PMID `22568433`: human SRY localizes to
  midbrain dopaminergic neurons and can regulate catecholamine-synthesis and
  metabolism genes in vitro.
- Lee et al. 2019, PNAS, DOI `10.1073/pnas.1900406116`, PMID `31371505`: in
  toxin models, nigral SRY contributes to male-specific dopaminergic-neuron
  vulnerability.

## Dataset calibration

The focal training-count table has 1,674 perturbations.  Its distribution is very
zero-inflated:

- 1,205/1,674 training perturbations have `n_degs = 0`.
- The median is 0 and the 75th percentile is 1.
- Only 5% of training perturbations have more than 18 DEGs.
- The extreme upper tail is made of broad essential regulators such as `Uba5`
  with 2,677, `Tpr` with 1,768, `Sin3a` with 1,433, spliceosome/proteasome
  factors, and core transcriptional regulators.

I queried the count CSV for SOX-family, steroid-receptor, and gonadal
developmental comparators in the focal group.  The relevant observed counts were:

| training target | n_degs in 151 |
| --- | ---: |
| Ar | 0 |
| Esr1 | 0 |
| Esr2 | 0 |
| Esrrb | 0 |
| Foxl2 | 0 |
| Gata4 | 0 |
| Gata6 | 0 |
| Nr5a1 | 0 |
| Sox2 | 2 |
| Sox4 | 0 |
| Sox5 | 2 |
| Sox9 | 0 |
| Sox10 | 0 |
| Sox11 | 0 |
| Sox17 | 0 |
| Sox18 | 0 |

`Esrra` was the clear steroid-receptor-family exception at 57 DEGs and `Rora`
was a thalamic positive benchmark at 278 DEGs, but both are orphan/nuclear
receptors with focal neuronal programs rather than SRY sex-determination or SOX
HMG-box analogs.

For the focal DE parquet I used a targeted scan over `group_name`,
`gene_target`, and a small gene list to recover the actual local expression
pattern:

```sql
SELECT gene_target, names, logfoldchanges, pvals_adj
FROM training_de_all_cell_groups
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ('Sox2','Sox5','Rora','Esrra','Ar','Esr1','Esr2','Nr5a1')
  AND (pvals_adj < 0.05
       OR names IN ('Th','Ddc','Slc6a3','Tnnt1','Stam','Dgkh'));
```

The significant focal genes for the two closest SOX perturbations were tiny and
not a shared positive module:

- `Sox2`: two DEGs, both down, `Tnnt1` with logFC -1.006 and q
  2.77e-06, and `Stam` with logFC -0.567 and q 0.0147.
- `Sox5`: two DEGs, both up, `Dgkh` with logFC 0.387 and q 5.37e-04, and
  `Tnnt1` with logFC 0.566 and q 0.0284.

The catecholamine genes checked because of the SRY literature were not moved
detectably in this thalamic group by these analogs:

- `Sox2`, `Sox5`, `Ar`, `Esr1`, `Esr2`, `Nr5a1`, `Esrra`, and `Rora` all had
  `Th`, `Ddc`, and `Slc6a3` at adjusted p-value 1.0.
- `Rora` had a broad focal response, but its `Tnnt1` overlap with `Sox2` was
  a one-gene thalamic edge; it did not supply a dopamine/Sry-like program.

The Distributed Agents corpus sharpened this calibration.  In claim
`claim:4ede4fcc4ed2d623a8eb`, the same-experiment corpus states that measured
SOX-family perturbations do not define a generic neuronal SOX transcriptomic
response in P16 NeuN-enriched postnatal neurons.  The supporting findings report
that `Sox2` has a two-gene 151-thalamic effect, `Sox5` has a two-gene effect
with `Tnnt1` in the opposite direction, `Sox4/Sox9/Sox10/Sox11/Sox17` were flat,
and `Sox18` had only a one-gene off-context event.  This makes broad family
transfer from an HMG-box factor to `Sry` inappropriate.

## Target-specific reasoning

### Sry

Mechanistic expectation:

- Sry is the Y-linked HMG-box male sex-determination transcription factor.  In
  the nervous system, the best-described postnatal axis is male-specific
  expression in substantia nigra dopaminergic neurons and regulation of
  catecholamine genes such as `Th` and dopamine-metabolism components.
- The focal screen cell group is thalamic `Prkcd/Grin2c` glutamatergic, not
  substantia nigra or ventral tegmental dopamine neurons.  In the training data,
  dopamine-synthesis and dopamine-transporter readouts were not FDR-supported
  downstream genes of the relevant SOX or sex-steroid comparators in this focal
  group.
- The guide label was pooled across mixed sexes.  Because Sry is Y-linked,
  female nuclei assigned Sry guides would provide no on-target Y-locus loss of
  function, diluting any male-specific thalamic response even if one existed.
- The perturbation is acute, mosaic, sparse AAV CRISPR delivered at P16.  That
  timing is mismatched to Sry's canonical embryonic gonadal sex-determination
  role, and the juvenile screen generally buffered many developmental
  transcription-factor programs outside their active developmental or lineage
  context.

Within-dataset analogs and counterexamples:

- `Sox2` and `Sox5` are the best represented HMG/SOX neuronal analogs in the
  focal data, but each had only 2 DEGs.  They touched `Tnnt1` in opposite
  directions and did not move `Th`, `Ddc`, or `Slc6a3`.
- Other represented SOX-family members that could have revealed a generic HMG
  transcription-factor response were null in the focal group: `Sox4`, `Sox9`,
  `Sox10`, `Sox11`, `Sox17`, and `Sox18` all had 0 DEGs.
- The classical sex-hormone and gonadal-axis comparators represented in the
  training table were also focal nulls: `Ar`, `Esr1`, `Esr2`, `Nr5a1`, `Gata4`,
  `Gata6`, and `Foxl2` all had 0 DEGs.
- `Rora` and `Esrra` prove that this thalamic cell group can produce a
  transcriptional response to nuclear receptors, but they are counterexamples
  rather than close positives: their significant genes form local thalamic and
  metabolic programs and had no SRY/catecholamine overlap in the focal query.

Decision:

The local evidence points to no detectable postnatal 151 response for
out-of-context SOX, gonadal, and steroid-axis factors, while the external Sry
brain literature points to a specialized male nigral catecholaminergic function.
Because that mechanism is not matched to `151 TH Prkcd Grin2c Glut` and would
be diluted in females, I predict that no measured gene will pass BH FDR 0.05.

Prediction: `Sry -> 0`.

## Limits

The prediction is extrapolative.  `Sry` itself was not present in the training
DE parquet, the Distributed Agents corpus had no `Sry` target context, and the most direct
Sry-related brain experiments used antisense, overexpression, or toxin injury in
midbrain dopamine systems rather than AAV CRISPR in thalamic glutamatergic
neurons.  `Sox1`, `Sox3`, `Sox6`, and `Sox13` were not represented as perturbation
targets, so the SOX comparison is incomplete.  Finally, the pooled mixed-sex
design means a real but very small male-only thalamic effect could be hidden
below the FDR threshold; the point prediction is for the assay endpoint, not for
Sry having no biological function anywhere in the brain.
