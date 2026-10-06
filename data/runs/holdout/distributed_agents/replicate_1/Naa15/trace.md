# DEG-count prediction trace

## Question and endpoint

The requested prediction is the number of genes expected to pass
Benjamini-Hochberg FDR 0.05 after acute AAV CRISPR loss of `Naa15` in the focal
`151 TH Prkcd Grin2c Glut` thalamic glutamatergic class. `n_degs` is a breadth
of recovered-nucleus transcriptional response, not a direct edit rate,
viability, or biochemical NatA activity measurement.

The requested-target manifest has one target, `Naa15`. I verified that `Naa15`
is absent from the 1,674-row focal training-count CSV and that filtering the
training DE parquet for `gene_target == "Naa15"` returns zero rows, so this is a
true held-out prediction.

## Sources used

- Direct quantitative source: the declared
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` focal training counts.
- Direct expression source: the declared
  `training_de_all_cell_groups.parquet`, filtered to
  `151 TH Prkcd Grin2c Glut` and relevant training perturbations.
- Same-experiment interpretation source: the internal
  `perturbai-july-260713-sourceguard-1773-v1` corpus, queried through
  `corpus.findings`, `corpus.direct_evidence`, and `corpus.report_evidence`.
  These are derived interpretations of the same Perturb-seq experiment, not
  independent replication.
- External literature from PubMed:
  - Cheng et al. 2018, `NAA15` truncating variants and NatA
    haploinsufficiency, DOI `10.1016/j.ajhg.2018.03.004`, PMID `29656860`.
  - Lyon et al. 2023, expanded `NAA10`/`NAA15` neurodevelopmental-syndrome
    spectrum, DOI `10.1038/s41431-023-01368-y`, PMID `37130971`.
  - Lentzsch et al. 2024, ribosome-associated NAC/MetAP1/NatA nascent-chain
    processing complex, DOI `10.1038/s41586-024-07846-7`, PMID `39169182`.

## Quantitative calibration

The focal training endpoint is very zero-inflated: 1,205 of 1,674 perturbations
have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th
percentile is 18, and a small tail contains the broad stress and proteostasis
responses. Against that background, predicting a nonzero count for a held-out
gene needs a close observed analog that itself produced a response, or a strong
external reason to expect an acute RNA program missed by the local analog.

The closest available perturbation is `Naa10`, the NatA catalytic subunit that
works with the `Naa15` auxiliary/ribosome-anchor subunit. `Naa10` is observed in
the focal count table with `n_degs = 0`. Re-querying the focal parquet recovered
17,259 measured genes for `Naa10` with 240 matched perturbed nuclei versus
23,679 controls; no gene passed FDR 0.10 or FDR 0.05. Even the smallest nominal
signals adjusted to 1.0, with `Pdcd7` as the top row
(`p = 9.67e-05`, `p_adj = 1.0`), and the measured `Naa10` transcript itself was
unchanged at FDR 1.0. This is not a one- or two-gene near miss.

The same-experiment Naa10 report also found a pan-neuronal FDR-level null:
across 22 measured neuronal classes and 2,123 matched perturbed nuclei, every
class had zero downstream genes at FDR 0.10. Nat-family or NatA-related
sentinel transcripts (`Naa15`, `Naa16`, `Naa20`, `Naa30`, `Naa40`, `Naa50`,
`Naa60`, `Btbd3`) were all present in the 22 measured `Naa10` groups and were
never significant at FDR 0.10. Integrated-stress, apoptosis, proteasome, and
deubiquitinase sentinels were also flat. That makes a large compensatory or
proteotoxic transcriptional program unlikely under this P16-to-P37/44 sparse
CRISPR design.

I used the corpus comparator evidence only as falsification context. The Naa10
report contrasts `Naa10` with `Psmb4`, `Psmc1`, and `Eef2`, which show the same
assay can detect protein-homeostasis or translation-associated RNA programs:
in the focal count table their `n_degs` are 742, 430, and 9, respectively. These
are counterexamples to an "the assay cannot see proteostasis" explanation, but
they are not NatA subunits and their positive signatures do not transfer to
`Naa15`.

The weak full-vector `Naa10` neighbors named by the corpus were other flat
signatures rather than a positive NatA module: `Mpc1`, `Rorb`, `Gli2`, and
`Diaph2` all have focal `n_degs = 0`. My direct focal score-correlation query
likewise did not identify a meaningful positive Naa10-like response: the best
score correlations to `Naa10` among non-held-out genes were tiny
(`Cic`, `r = 0.074`; `Uba5`, `r = 0.071`) and corresponded to unrelated broad
signatures. I therefore did not use signature correlation as a positive
predictor.

## Target-specific rationale

### Naa15 -> predicted `n_degs = 0`

Biological role: `Naa15` encodes the auxiliary subunit of the NatA
N-terminal acetyltransferase complex. It binds the `Naa10` catalytic subunit and
anchors NatA to the ribosome, where NatA modifies nascent polypeptide
N-termini; damaging `NAA15` variants in humans produce an autosomal dominant
neurodevelopmental syndrome with intellectual disability, delayed milestones,
autism spectrum features, seizures in some individuals, and congenital
anomalies through NatA haploinsufficiency.

Relevant observed analogs:

- `Naa10`: same NatA complex, focal `n_degs = 0`; all 17,259 focal adjusted
  p-values were at 1.0 and all 22 measured cell classes had zero downstream
  FDR 0.10 genes. This is the closest within-dataset anchor and argues for no
  robust secondary transcriptional state after partial NatA perturbation in
  recovered juvenile neurons.
- `Mpc1`, `Rorb`, `Gli2`, `Diaph2`: not mechanistic NatA genes, but they were
  the weak positive full-vector neighbors of the flat `Naa10` signature in the
  same-experiment report; each has focal `n_degs = 0`, consistent with a
  buffered or null signature class.
- `Psmb4`, `Psmc1`, `Eef2`: indirect protein-homeostasis/translation
  counterexamples with focal counts 742, 430, and 9. They show that broad
  proteostasis and translation perturbations can be detected in this focal
  class, but their large RNA programs did not appear under `Naa10`
  perturbation and are not mechanistically specific to NatA.

The causal transfer is: CRISPR disruption of `Naa15` should reduce NatA
scaffolding/ribosome recruitment -> NatA-mediated N-terminal acetylation should
be impaired -> protein-specific stability, turnover, and cytoskeletal effects
could occur -> only nuclei that survive, retain the thalamic glutamatergic
identity, and have a coherent RNA state are measured by the Wilcoxon DE
endpoint. `Naa10` perturbs the same limiting NatA enzymatic function one step
downstream and produced no significant RNA program in the focal class or
pan-neuronally. Published human genetics establishes that `NAA15` loss matters
developmentally, but it does not demonstrate an acute postmitotic
transcriptional response 3-4 weeks after a sparse partial CRISPR hit. The
mechanistic and assay-matched evidence therefore both point to another
FDR-level null, with no reason to round upward to a one- or few-gene effect.

## Limits and extrapolation

The requested `Naa15` perturbation is absent from both supplied input tables, so
the prediction is a transfer from observed `Naa10` plus external NatA biology.
`Naa10` is a close same-complex analog but not identical: `Naa15` is the
auxiliary/ribosome-anchor subunit, whereas `Naa10` is catalytic and also has
NatA-independent roles, so their knockout proteomes may not match exactly.
The assay measures nuclear RNA in recovered nuclei; it can miss altered
N-terminal acetylation, dendritic structure, proteome turnover, slow
developmental consequences, and early selection of heavily perturbed cells.
Finally, average target RNA knockdown in this experiment was partial, so a true
strong `Naa15` biochemical phenotype after complete biallelic loss could be
buffered below the FDR threshold here.
