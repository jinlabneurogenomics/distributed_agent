# Reasoning trace

## Question and resolved ambiguities

The requested held-out perturbation list contains one target:

```tsv
target_name
Chrnb4
```

I interpreted the task as a point prediction of `n_degs` for loss of mouse
`Chrnb4` in `151 TH Prkcd Grin2c Glut`, where `n_degs` is the number of genes in
that focal cell group with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05`. The
held-out target itself is absent from both training inputs as a perturbation, so
I used non-held-out perturbations of related nicotinic acetylcholine receptor
subunits and cholinergic pathway genes to calibrate the expected response
breadth.

Two ambiguities mattered:

- I counted the target transcript itself as a possible DEG, because the training
  endpoint does so. For example, the single `Chrnb2` DEG in the focal group was
  `Chrnb2` itself.
- A zero prediction does not imply that the guide failed or that beta4 nicotinic
  receptors are unimportant; it means I predict no transcript will pass the
  assay's FDR 0.05 threshold in this unchallenged, postnatal, sparse CRISPR
  setting.

## Sources used

- Input endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`,
  1,674 non-held-out perturbations with focal-cell `n_degs`.
- Input DE table:
  `[local file: training_de_all_cell_groups.parquet]`,
  queried with `pyarrow.dataset` filters rather than reading all 616,253,184
  rows.
- Internal same-experiment knowledge layer:
  Distributed Agents Corpus release `perturbai-july-260713-sourceguard-1773-v1`. The
  corpus had no direct `Chrnb4` record, as expected for a held-out target, but it
  contained bottom-up findings for `Chrna3`, `Chrnb2`, `Chrna4`, `Chrna6`,
  `Chrna7`, `Chrnb3`, and `Ache`.
- Distributed Agents Runtime `profile_neighbors`, run on the focal group for the
  represented cholinergic receptor cohort.
- External literature from NCBI PubMed:
  Frahm et al. 2011, DOI `10.1016/j.neuron.2011.04.013`; Fowler et al. 2011,
  DOI `10.1038/nature09797`; Husson et al. 2020, DOI
  `10.1523/JNEUROSCI.0356-19.2020`, PMID `32184221`.

## Dataset calibration

The focal training distribution is extremely zero-heavy: of 1,674 perturbations,
1,205 had zero DEGs, the median was 0, the 75th percentile was 1, and only 162
perturbations exceeded 2 DEGs. A broad count therefore needs a real
transcriptional analog, not just an annotation link.

For a receptor-specific calibration, I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to a hand-declared set of
cholinergic/nicotinic comparators:

```python
flt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
```

For each comparator I counted rows with `pvals_adj < 0.05` and inspected the
identity of the significant genes. Each target had 17,259 measured genes in the
focal group. The relevant observed counts were:

| training perturbation | focal `n_degs` | expression-pattern evidence |
| --- | ---: | --- |
| `Chrna3` | 0 | Direct alpha3 partner of beta4; no FDR<0.05 genes in the focal group. Whole-score Pearson correlations to other receptor perturbations were near zero, including `Chrna4` r = 0.0168, `Chrnb3` r = 0.0099, `Ache` r = 0.0041, and `Chrnb2` r = -0.0946. |
| `Chrnb2` | 1 | Only `Chrnb2` itself was significant (`log2FC = -0.517`, `q = 7.4e-07`); no non-self downstream DEG was detected. |
| `Chrna4` | 2 | `Chrna4` self-depletion and `Cyp46a1` down-regulation were significant; the response did not overlap the `Chrnb2` or `Chrna3` patterns. |
| `Chrna2` | 0 | No focal DEGs despite being a neuronal nicotinic alpha subunit. |
| `Chrna6` | 0 | No focal DEGs; informative as an alpha6-beta2-beta3 receptor subunit, but not a beta4 partner. |
| `Chrna7` | 0 | No focal DEGs; a homomeric alpha7 receptor counterexample to a generic nAChR stress or compensation program. |
| `Chrnb3` | 0 | No focal DEGs; beta-family comparator that assembles in a different alpha6/beta2 module. |
| `Ache` | 1 | Only `Ache` itself was significant (`log2FC = -0.674`, `q = 0.0041`); this argues against a broad cholinergic-state response. |
| `Chrm2`, `Chrm3` | 0, 0 | Muscarinic receptor counterexamples; cholinergic receptor loss was generally silent. |

The same-experiment Distributed Agents findings matched this manual readout. The
`Chrna3` corpus record reported a pan-surface basal-transcriptome null and
noted that `Chrnb4`/`Chrna5`, the closest alpha3-beta4-alpha5 partners, were
absent as perturbations. The `Chrnb2` findings stated that alpha2, alpha3,
alpha4, alpha6, alpha7, and beta3 nAChR relatives did not converge with `Chrnb2`
and had zero shared-direction downstream overlap. The `Chrna4` findings
described the focal `Cyp46a1` hit as an isolated thalamic response that was not
phenocopied by `Chrnb2` or other represented nicotinic relatives. At the
higher-order level, the corpus claim for `Ache`, `Chrna2`, `Chrna3`, `Chrna4`,
`Chrna6`, `Chrna7`, `Chrnb2`, and `Chrnb3` was that single-subunit nicotinic
receptor perturbations do not produce a shared basal neuronal transcriptional
state in this assay.

## Target-specific reasoning for `Chrnb4`

`Chrnb4` encodes the beta4 nAChR subunit. Externally, it is a bona fide neuronal
channel gene: the `CHRNA5-CHRNA3-CHRNB4` locus encodes the alpha5/alpha3/beta4
nicotinic receptor cluster, beta4 is a functional component of alpha3-beta4
receptors, and MHb-IPN beta4-containing receptors modulate nicotine aversion and
reinforcement (Frahm et al. 2011; Husson et al. 2020). Fowler et al. 2011 showed
that the same habenulo-interpeduncular pathway is a nicotine-intake circuit for
alpha5-containing nAChRs. That literature makes `Chrna3` the best represented
training analog and makes `Chrna5` an obvious missing analog; it does not make
`Chrnb4` a generic transcription factor or predict a broad basal response in a
thalamic Prkcd/Grin2c glutamatergic class.

The focal training evidence points to no above-threshold effect. `Chrna3`, the
nearest represented alpha3-beta4 receptor subunit, had 0 DEGs in the focal group
and 0 FDR<0.10 downstream genes across all recovered postnatal central neuronal
groups in the Distributed Agents corpus. The other neuronal nAChR genes in training were
also flat or self-only: `Chrna2`, `Chrna6`, `Chrna7`, and `Chrnb3` were 0;
`Chrnb2` was a beta2 self-transcript hit only; and `Chrna4` had just its own
transcript plus one isolated `Cyp46a1` edge. `Ache`, `Chrm2`, and `Chrm3`
reinforced the same conclusion for the broader cholinergic pathway. I therefore
do not see a recurrent nicotinic-subunit signature to transfer to `Chrnb4`.

The zero/nonzero decision was `zero`. A one-gene self-transcript hit is possible
for any targeted receptor, but `Chrna3` itself had no self hit in this cell
group and beta4 biology is strongest in MHb-IPN/VTA nicotine circuits rather
than in the `151 TH Prkcd Grin2c Glut` cell group. Sparse P16 CRISPR assayed at
P37-P44 also differs from germline or region-rescue beta4 mouse models and from
nicotine-evoked physiology. Given the complete absence of a Chrna3 response and
the near-null behavior of represented nAChR subunits, I set the point prediction
to:

```tsv
target_name	predicted_n_degs
Chrnb4	0
```

## Limits of the reasoning

- `Chrnb4` and `Chrna5` were deliberately held out or absent as perturbation
  targets, so the closest alpha3-beta4-alpha5 complex was only partially
  represented by `Chrna3`.
- The corpus and the focal parquet measure basal nuclear RNA, not indels,
  receptor assembly, acetylcholine-evoked current, nicotine dose response, or
  MHb-IPN/VTA behavior; a flat prediction is compatible with strong
  electrophysiologic beta4 function.
- `151 TH Prkcd Grin2c Glut` is not an isolated medial-habenula beta4-rich
  population. External habenular rescue and overexpression studies are therefore
  informative about mechanism but imperfect for this focal thalamic readout.
- The focal `Chrna4` two-gene response leaves a small possibility that another
  nAChR subunit can create an idiosyncratic singleton in this cell group. I
  judged that to be less likely than a zero count for `Chrnb4` because the direct
  `Chrna3` comparator was completely flat.
