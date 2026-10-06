# DEG-count prediction for `Pdss2`

## Question and resolved ambiguities

The requested held-out target file contained one perturbation, `Pdss2`.  I
interpreted `predicted_n_degs` as the integer number of measured genes expected
to pass Benjamini-Hochberg FDR 0.05 in the `151 TH Prkcd Grin2c Glut` focal
population after acute AAV-CRISPR loss of `Pdss2`.

I used the training CSV as the authoritative focal endpoint for non-held-out
genes and used the parquet only for focal expression-pattern checks.  The
endpoint counts include the targeted gene itself when the target transcript is
significant; therefore a prediction of 0 means I am predicting neither a
detectable target-self RNA drop nor a downstream RNA response at FDR 0.05.

## Sources used

- Input endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest:
  `[local file: 174_Pdss2.csv]`.
- Distributed Agents internal corpus release
  `perturbai-july-260713-sourceguard-1773-v1`; this had no `Pdss2`
  target-centered record but had a detailed `Coq5` negative report and
  CoQ/mitochondrial comparator records.
- PubMed-indexed CoQ biology and mouse `Pdss2` literature:
  Saiki et al. 2008, DOI `10.1152/ajprenal.90445.2008`; Peng et al. 2008,
  DOI `10.1371/journal.pgen.1000061`; Lu et al. 2011, DOI
  `10.1016/j.nbd.2011.08.006`; Ziegler et al. 2011, DOI
  `10.1016/j.mito.2011.09.011`; Nguyen et al. 2014, DOI
  `10.1016/j.bbalip.2014.08.007`; Malicdan et al. 2018, DOI
  `10.1002/humu.23345`.
- Clinical/pathway overview: Salviati, Trevisson, Agosto et al.,
  *Primary Coenzyme Q10 Deficiency Overview*, GeneReviews, 2017;
  updated 2023.
- Mitochondrial ISR interpretive literature used only for stress-program
  expectations: Fessler et al. 2020, DOI `10.1038/s41586-020-2076-4`,
  and Sasaki et al. 2020, DOI `10.1042/BSR20201289`.

## Computational checks

I first confirmed that the held-out list was exactly:

| target_name |
| --- |
| `Pdss2` |

The focal training file contained 1,674 unique perturbations.  Its response
distribution was extremely zero-inflated in this population: median `n_degs =
0`, 75th percentile `= 1`, 469 / 1,674 perturbations had any DEG at FDR 0.05,
106 had at least 10, and 43 had at least 100.

I then queried the endpoint file for direct CoQ genes:

| CoQ-biosynthesis target | training status in focal counts |
| --- | ---: |
| `Coq5` | present, `n_degs = 0` |
| `Pdss1`, `Coq2`, `Coq3`, `Coq4`, `Coq6`, `Coq7`, `Coq8a`, `Coq8b`, `Coq9`, `Coq10a`, `Coq10b`, `Adck3`, `Adck4`, `Hpdl` | absent |

For the represented mitochondrial comparators I scanned the focal rows of the
parquet with a filter equivalent to:

```python
group_name == "151 TH Prkcd Grin2c Glut"
and gene_target in ["Coq5", "Uqcrfs1", "Uqcrc2", "Cyc1", "Ndufs2",
                    "Ndufc2", "Uqcrb", "Uqcrq", "Clpp", "Lonp1",
                    "Opa1", "Aco2", "Ndufv1", "Sod2", "Gfm2", "Coa8"]
```

This extracted, for each comparator, the focal count from the training CSV, the
minimum adjusted p-value in the focal signature, and the target-self log fold
change when available.  It also confirmed that `Pdss2` was not a held-in
`gene_target` but was present as a measured gene in the focal DE matrix for all
1,674 training perturbations.

The Distributed Agents corpus was used to avoid over-reading noisy raw log-fold-change
similarity.  Its `Coq5` report found zero downstream genes at FDR 0.10 in all
22 neuronal groups in which `Coq5` was recovered; in `151 TH Prkcd Grin2c
Glut`, `Coq5` had 200 perturbed nuclei, 23,679 control nuclei, target-self
`logFC = -0.473`, `FDR = 1.000`, and no downstream FDR 0.10 genes.  It also
reported that a Coq5-matched score-space search had no meaningful neighbor:
the top positive correlations were only `r = 0.0296`, `0.0288`, and `0.0285`,
and pathway-obvious comparators `Uqcrfs1`, `Uqcrc2`, `Cyc1`, `Ndufs2`,
`Ndufc2`, `Clpp`, and `Lonp1` all had near-zero correlations to `Coq5`.

## Target-specific reasoning

### `Pdss2`

`Pdss2` encodes one of the two prenyl diphosphate synthase subunits that, with
`Pdss1`, make the polyisoprenyl tail of coenzyme Q.  Loss of this step lowers
CoQ, and Pdss2 mutant mice and tissue knockouts show strong CoQ-dependent
phenotypes in sensitized settings, especially kidney podocytes and selected
neurons; CoQ10 supplementation rescues renal pathology in the `Pdss2(kd/kd)`
model (Saiki et al. 2008; Peng et al. 2008; Ziegler et al. 2011; Lu et al.
2011).  Thus `Pdss2` is a bona fide mitochondrial CoQ-biosynthesis gene, not a
biologically inert target.

The closest direct perturbation in the training universe was `Coq5`.
`Coq5` catalyzes a downstream C-methyltransferase step and participates in the
eukaryotic CoQ biosynthetic machinery (Nguyen et al. 2014); human `COQ5`
loss causes primary CoQ10 deficiency with neurologic disease (Malicdan et al.
2018).  Mechanistically it is not the same enzyme as `Pdss2`, because `Pdss2`
contributes to side-chain synthesis rather than ring methylation, but it is in
the same endogenous CoQ production pathway and was the only direct pathway
member present in the training counts.  In the focal group `Coq5` had
`n_degs = 0`, no FDR 0.05 target-self effect, and no convincing subthreshold
signature.  The Distributed Agents corpus further reported a pan-neuronal `Coq5`
negative result: 0 genes at FDR 0.10 in every recovered neuronal group and no
canonical `Atf4`/`Ddit3`/`Herpud1`/`Shmt2` mitochondrial-stress induction.

The broader ubiquinone-linked respiratory-chain genes also argued against a
large acute nuclear response in this assay.  Focal counts were:

| comparator | role | observed `151 TH Prkcd Grin2c Glut` `n_degs` | interpretation |
| --- | --- | ---: | --- |
| `Uqcrfs1` | Complex III Rieske Fe-S protein | 0 | direct Complex III / ubiquinol-oxidation comparator; no focal response |
| `Uqcrb` | Complex III subunit | 0 | direct Complex III comparator; no focal response |
| `Uqcrh` | Complex III subunit | 0 | direct Complex III comparator; no focal response |
| `Uqcrc2` | Complex III core protein | 1 | only a singleton, the target self-transcript |
| `Uqcrq` | Complex III subunit | 1 | singleton-scale response |
| `Cyc1` | Complex III cytochrome c1 | 1 | only a singleton, the target self-transcript |
| `Ndufs2` | Complex I core ubiquinone-module subunit | 1 | only a singleton, the target self-transcript |
| `Ndufc2` | Complex I subunit | 1 | only a singleton, the target self-transcript |
| `Ndufv1` | Complex I flavoprotein subunit | 0 | Complex I comparator; no focal response |

These are imperfect analogs because they perturb the respiratory chain
downstream of ubiquinone synthesis rather than the CoQ pool itself, but they
are useful counterexamples: blocking enzymes that feed electrons into or out
of ubiquinone usually did not recruit a multi-gene `151 TH Prkcd Grin2c Glut`
response under this acute mosaic protocol.

Finally, I considered mitochondrial stress positives and negatives.  `Opa1`
was a real positive in the same focal cell group with `n_degs = 37`, and the
best focal gene was `Asns` at FDR `2.39e-07`, consistent with the ATF4-like
amino-acid/mitochondrial-stress module described in the Distributed Agents corpus.
However, OPA1 cristae/fusion biology is not a CoQ-biosynthesis phenocopy, and
many other mitochondrial targets were null or singleton in the same endpoint:
`Aco2 = 0`, `Clpp = 0`, `Lonp1 = 0`, `Gfm2 = 0`, `Coa8 = 0`, `Afg3l2 = 0`,
`Yme1l1 = 0`, `Mff = 0`, and `Sod2 = 1`.  The appropriate conclusion is that
the assay can detect a mitochondrial ISR-like state when a perturbation crosses
threshold, but same-organelle identity alone does not predict such a state.

I therefore predict zero rather than a small nonzero count.  The zero is driven
mostly by the in-dataset `Coq5` pan-neuronal null and by the zero/singleton
Complex I/III training counts.  External `Pdss2` knowledge raises the prior
that a complete, cell-autonomous CoQ lesion can be important, but those
studies involve germline, conditional, or disease-stage deficiencies with
substantial CoQ depletion.  The benchmark perturbation is acute, sparse,
postmitotic CRISPR at P16-P37/44, and average target mRNA loss in the screen is
partial; the long-lived lipid CoQ pool and juvenile postmitotic neurons could
buffer a several-week partial loss enough to leave no focal Wilcoxon hit.

## Limits

- `Pdss2` itself was held out, so no self-knockdown size, indel rate, CoQ
  abundance, respiratory flux, or hidden focal signature was available.
- `Coq5` is a close pathway analog but not a `Pdss2`/`Pdss1` synthase-complex
  subunit.  Upstream side-chain deficiency could deplete different
  intermediates from a `Coq5` methyltransferase lesion.
- Respiratory-chain comparators test consequences of impaired electron
  transport around ubiquinone, not loss of CoQ-dependent sulfide oxidation or
  lipid antioxidant chemistry.
- A prediction of zero does not mean `Pdss2` is nonessential or that editing
  would fail.  It means that, calibrated to the observed acute neuronal
  Perturb-seq endpoint, I expect no measured gene to pass FDR 0.05 in this one
  focal cell group.

