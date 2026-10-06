# DEG-count prediction trace

## Question and resolved ambiguities

The run asks for a point prediction of `n_degs`, the number of measured genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after each held-out CRISPR
perturbation.  The requested manifest contains one held-out target:

```text
Hoxc13
```

I treated `151 TH Prkcd Grin2c Glut` as the Allen-style thalamic
glutamatergic focal class, not as a tyrosine-hydroxylase dopaminergic label.
Because `Hoxc13` was held out, there is no `Hoxc13` row in either the
focal-cell training count CSV or the DE parquet's `gene_target` column; the
prediction below is a transfer from training perturbations, not a lookup of a
hidden `Hoxc13` signature.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for the exact focal-cell training endpoints.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell expression signatures of biologically related non-held-out
  targets.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially the HOX and
  PBX/MEIS claims retrieved through `target_context` for `Hoxa13`, `Hoxd13`,
  `Hoxd10`, `Hoxb8`, and `Pbx3`.
- PubMed-indexed HOXC13 literature: Godwin and Capecchi 1998,
  DOI `10.1101/gad.12.1.11`, PMID `9420327`; Godwin and Capecchi 1999,
  DOI `10.1038/sj.jidsp.5640221`, PMID `10674376`;
  Jave-Suarez et al. 2001, DOI `10.1074/jbc.M101616200`, PMID `11714694`;
  Potter et al. 2010, DOI `10.1038/jid.2010.391`, PMID `21191399`.

## Dataset computations

I used the count CSV to inspect the empirical scale of the endpoint in this
cell group.  Among the 1,674 training perturbations, 1,205 were exact zero,
363 had 1-9 DEGs, 63 had 10-99 DEGs, and 43 had at least 100 DEGs.  The
median count was 0 and the 95th percentile was 18, so a positive prediction
needs either a same-pathway positive analog or a reason to expect `Hoxc13` to
escape the broad zero mode.

I then filtered the parquet to the focal class and to represented HOX genes and
HOX/TALE cofactors:

```text
group_name == "151 TH Prkcd Grin2c Glut"
gene_target in Hoxa1,Hoxa3,Hoxa13,Hoxb8,Hoxd10,Hoxd13,
               Pbx1,Pbx3,Meis1,Meis2
```

For each target I recomputed `sum(pvals_adj < 0.05)`, checked the minimum
adjusted p-value, and inspected the top nominal genes.  The focal evidence was
flat for the mechanistically relevant neighborhood:

| training perturbation | focal `n_degs` | minimum focal `pvals_adj` | why it is informative |
|---|---:|---:|---|
| `Hoxa13` | 0 | 1.000 | Hox13-family paralog; its only same-experiment signal was a two-gene sub-FDR-0.10 pineal response, not a thalamic response. |
| `Hoxd13` | 0 | 1.000 | Hox13-family paralog with limb/posterior patterning biology; the Distributed Agents corpus reports no robust response across 22 sampled neuronal groups. |
| `Hoxd10` | 0 | 1.000 | Posterior HOX control; no focal response and no shared directional HOX/PBX/MEIS signature in the corpus. |
| `Hoxb8` | 0 | 0.8797 | More anterior HOX comparator; the corpus reports no FDR-supported neuronal response in all 23 recovered groups and no meaningful whole-surface neighbor. |
| `Hoxa1` | 0 | 1.000 | Anterior HOX comparator; useful as a boundary against a generic postnatal HOX response. |
| `Hoxa3` | 0 | 1.000 | Group-3 HOX comparator; similarly zero in the focal class. |
| `Pbx1` | 0 | 1.000 | PBX TALE cofactor that could expose residual HOX/PBX dependence if such a program were active in these neurons. |
| `Pbx3` | 0 | 1.000 | TALE cofactor; corpus reports a pan-sampled null and failed phenocopying by TALE, HOX, and Phox comparators. |
| `Meis1` | 0 | 0.5697 | MEIS TALE cofactor; zero in the focal class. |
| `Meis2` | 0 | 1.000 | MEIS TALE cofactor; zero in the focal class. |

The top nominal focal genes for these perturbations were isolated and
non-overlapping; none reached FDR 0.05.  For example, the smallest focal
adjusted p-values for `Hoxa13`, `Hoxd13`, and `Hoxd10` were 1.0, 1.0, and 1.0,
respectively, despite 136-278 matched perturbed nuclei and 23,679 matched
controls in this class.  This is expression-pattern evidence against a hidden
HOX13-like state in `151 TH Prkcd Grin2c Glut`, not just a family-name prior.

## Target-specific prediction

### Hoxc13

**Biologically relevant training perturbations.**  The closest represented
losses of function were the Hox13 paralogs `Hoxa13` and `Hoxd13`; both had
`n_degs = 0` in the focal class.  The represented broader HOX neighborhood was
also zero in this class: `Hoxa1`, `Hoxa3`, `Hoxb8`, and `Hoxd10` each had
`n_degs = 0`.  The represented DNA-binding cofactors most likely to reveal a
generic postnatal HOX/TALE program, `Pbx1`, `Pbx3`, `Meis1`, and `Meis2`, also
each had `n_degs = 0`.

The Distributed Agents corpus independently summarizes these same-experiment surfaces
as follows:

- Claim `claim:000706d189e9650b75ed`: represented HOX-family and
  TALE/homeobox-cofactor perturbations did not form a shared P16 postnatal
  neuronal transcriptional response module.
- `Hoxa13:F002`: the weak 217 P MY Pineal Glut `Acp6`/`Slc49a4` signature of
  `Hoxa13` was not shared by represented HOX-family targets or by `Pbx`,
  `Meis`, and `Pknox2` cofactors.
- `Hoxd13:F004`: represented HOX paralogs and PBX/MEIS cofactors did not
  converge with `Hoxd13`; the expected Hox13 and HOX/PBX relationships were
  developmentally gated in this assay.
- `Hoxb8:F003` and `Hoxd10:F002`: null or singleton HOX responses did not hide
  a shared HOX/TALE signature.
- `Pbx3:F003`: literature-obvious TALE, HOX, and Phox comparators failed to
  phenocopy `Pbx3`, again bounding the single-gene perturbation space against
  a shared homeobox-cofactor module.

**External biological rationale.**  `Hoxc13` is a posterior HOX transcription
factor, but its clearest postnatal mammalian function is in ectodermal
appendage differentiation rather than in thalamic neurons.  `Hoxc13` mutant
mice have brittle or absent external hair, nail/tail/vibrissal/tongue
expression phenotypes, and severe hair-follicle differentiation defects
reported by Godwin and Capecchi in 1998 and reviewed by the same group in
1999.  Direct target work tied HOXC13 to hair keratin and keratin-associated
protein regulation, and Potter et al. 2010 placed `Foxn1` downstream of HOXC13
in a hair-follicle and nail differentiation cascade.  Those programs require
skin or nail epithelium, which is absent from a NeuN-enriched juvenile
whole-brain neuronal assay.

**Zero/nonzero decision.**  I therefore predict an exact zero.  The decision is
driven mostly by within-dataset evidence: every represented focal HOX/Hox13
and PBX/MEIS analog has 0 FDR-0.05 DEGs in this cell group, and the
same-experiment corpus reports no broader postnatal neuronal HOX/TALE response
that could be transferred to a held-out HOX-family member.  External knowledge
reinforces the zero because the well-established HOXC13 pathway is a
hair/nail keratinocyte differentiation program rather than a thalamic
glutamatergic maintenance pathway.

I considered weakly positive alternatives because `Hoxa13` had a tiny
217 P MY Pineal Glut two-gene signal at the looser FDR 0.10 threshold, and
because sparse P16 CRISPR can uncover private one-gene responses.  I did not
carry that forward for `Hoxc13` in the focal class: the `Hoxa13` response was
outside `151 TH Prkcd Grin2c Glut`, was not shared by `Hoxd13`, and did not
extend to PBX/MEIS perturbations.

Predicted `n_degs`: **0**.

## Limits of reasoning

- `Hoxc13` itself is held out from the same-experiment DE parquet and has no
  Distributed Agents target-context entry, so the prediction extrapolates from paralogs
  and cofactors rather than from a measured `Hoxc13` signature.
- The exact posterior paralog `Hoxc13` does not have a same-paralog-group C
  cluster neighbor represented in the focal training set; `Hoxa13` and
  `Hoxd13` are strong Hox13 comparisons but not identical genes.
- The CRISPR assay did not measure DNA indels or HOXC13 protein, and an FDR
  zero in recovered nuclei cannot rule out rare edited-cell effects, selection
  before recovery, or biology in the absent hindbrain, olfactory bulb,
  spinal cord, skin, and nail lineages.
- Most HOX-family signatures in the screen are themselves null, which makes
  it easy to reject a large shared postnatal HOX module but impossible to
  distinguish a truly inert `Hoxc13` perturbation from a private effect below
  detection power.
