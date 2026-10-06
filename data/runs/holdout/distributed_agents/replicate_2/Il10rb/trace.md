# Task

Predict, for each requested held-out perturbation, the number of genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd
Grin2c Glut`.

The manifest for this run contains one target:

| target | held out from training? |
| --- | --- |
| Il10rb | yes; 0 focal rows in the DE parquet and no row in the focal training-count CSV |

I treated `n_degs` as the assay endpoint supplied in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, not as an intrinsic measure
of pathway importance. A prediction of zero therefore means that I do not expect
any measured transcript, including the target transcript, to pass the same FDR
threshold in this focal cell group.

# Sources Used

- Raw training-count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Raw differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 112_Il10rb.csv]`
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. `Il10rb` itself was absent from
  the corpus graph, so I used the corpus only for relevant measured comparators:
  especially `Il10ra`, `Ifnar1`, `Ifnar2`, `Ifngr2`, and `Il6st`.
- Distributed Agents runtime `profile_neighbors`, written to
  `cytokine_profile_neighbors.json`, comparing cytokine/IRF/STAT candidate
  training signatures in the focal group.
- PubMed literature queried through NCBI E-utilities:
  - Kotenko et al. 1997, EMBO Journal, DOI `10.1093/emboj/16.19.5894`,
    PMID `9312047`: identification of IL-10R2/IL10RB as the accessory chain
    required for a functional IL-10 receptor complex.
  - Kotenko et al. 2000, Journal of Biological Chemistry,
    DOI `10.1074/jbc.M007837200`, PMID `11035029`: IL10R2 is also part of the
    functional IL-22 receptor complex.
  - Kotenko et al. 2002, Nature Immunology, DOI `10.1038/ni875`,
    PMID `12483210`, and Sheppard et al. 2002, Nature Immunology,
    DOI `10.1038/ni873`, PMID `12469119`: IFN-lambda/IL-28/IL-29 signals
    through a class-II cytokine receptor containing IL10R2.
  - Donnelly et al. 2004, Journal of Leukocyte Biology,
    DOI `10.1189/jlb.0204117`, PMID `15123776`: review of class-II cytokines
    sharing the IL-10R2 chain and their STAT3/STAT1-biased signaling.
  - Ouyang et al. 2011, Annual Review of Immunology,
    DOI `10.1146/annurev-immunol-031210-101312`, PMID `21166540`: IL-10-family
    cytokines are primarily inflammatory, host-defense, and epithelial-barrier
    context regulators.

# Computational Checks

The focal count table has 1,674 non-held-out perturbations. In `151 TH Prkcd
Grin2c Glut`, its `n_degs` distribution is heavily zero-inflated:

| summary | value |
| --- | ---: |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| nonzero targets | 469 / 1,674 |

I queried the 616M-row parquet with DuckDB, projecting only the focal
`group_name` and cytokine/JAK/STAT-adjacent `gene_target` rows. The focal group
occupies 34 of 712 row groups, so the scan remained limited to about 29M
candidate rows. For each comparator I counted focal rows where `pvals_adj <
0.05` and inspected the best adjusted p-values to distinguish true FDR support
from sparse, high-log-fold-change artifacts.

The closest represented IL10RB/JAK-STAT comparators in the focal cell group were
nearly all exact zeros:

| comparator | focal n_degs | focal expression-pattern evidence |
| --- | ---: | --- |
| Il10ra | 0 | same IL-10 receptor complex; minimum adjusted p-value 0.432, then all remaining rows at FDR 1 |
| Ifnar1 | 0 | no type-I-IFN receptor response; best adjusted p-values all 1 in the focal group |
| Ifnar2 | 0 | same as `Ifnar1`; no IFNAR/ISGF3-like loss signature |
| Ifngr1 | 0 | no focal IFN-gamma receptor response |
| Ifngr2 | 0 | no focal IFN-gamma receptor response |
| Il6ra | 0 | no focal IL-6R response |
| Il6st | 0 | gp130 common-chain perturbation flat in this focal group |
| Osmr | 0 | OSM/gp130-family receptor component flat |
| Crlf1 | 0 | gp130-family ligand-adjacent perturbation flat |
| Il2ra, Il2rb, Il2rg, Il4ra, Il12b, Il12rb1, Il17ra, Il21r, Il23r | 0 each | other immune cytokine axes flat in this focal group |
| Stat1 | 1 | the only significant focal gene was `Stat1` itself, log2FC -1.3004, adjusted p 0.027 |
| Stat2, Stat3, Stat4, Stat5b | 0 each | downstream STAT relatives flat |
| Irf1, Irf2, Irf9, Nfkb1 | 0 each | no ISG/IRF/NF-kB transcriptional module |

The Distributed Agents runtime comparison used these 27 cytokine/IRF/STAT-adjacent
training nodes as the eligible universe and `logfoldchanges` as the signed
profile value. The neighborhood artifact recovered a connected set dominated by
zero- or singleton-response surfaces; I used this as a sanity check that no
strong, same-experiment ligand-gated cytokine module was sitting next to
`Il10ra` or the IFN receptor perturbations.

# Same-Experiment Corpus Evidence

The corpus contained no `Il10rb` node, which is expected because the perturbation
was held out from this run's training data. It did contain several relevant
negative comparator findings:

- `Il10ra:F001`: high-confidence negative result; `Il10ra` loss was
  transcriptionally silent at FDR 0.10 in every neuronal cell group in which it
  was recovered.
- `Il10ra:F002`: expected IL-10/STAT3 inflammatory and neuronal-survival
  transcriptional programs were absent after `Il10ra` perturbation.
- `Il10ra:F003`: neither full-universe signature search nor represented
  cytokine/STAT relatives yielded a convincing `Il10ra` phenocopy; `Ifnar1`,
  `Ifnar2`, `Ifngr1`, `Ifngr2`, `Il6ra`, `Il6st`, `Stat1`, `Stat2`, and `Stat3`
  were zero or singleton-only.
- `Ifnar1:F002`, `Ifnar2:F002`, and claim
  `claim:5ae625868e0586fef8b7`: basal NeuN-enriched neurons lacked a detectable
  tonic type-I-IFN/IFNAR/ISGF3 transcriptional program.
- `Ifngr2:F002` and claims `claim:00185d4f97d4e028c8d4`,
  `claim:327e424dee82bce929fe`, and `claim:6dbd95d05cf6c6a6bccd`: represented
  interferon receptor, STAT, IRF, and cytokine-receptor perturbations did not
  produce a recurrent IFN/JAK-STAT module in basal postnatal neurons.
- `Il6st:F003` and claim `claim:e19f1a45d54a29258057`: represented IL-6-family
  receptor and gp130/JAK-STAT perturbations did not converge on a shared
  ligand-gated mRNA phenotype.

The corpus findings often summarize a slightly more permissive FDR 0.10 screen
across multiple cell groups; I used them for mechanistic orientation only. The
point prediction is calibrated against the raw focal FDR 0.05 count CSV.

# Target-Specific Prediction

## Il10rb

`Il10rb` encodes IL-10 receptor beta / IL-10R2, the shared accessory subunit for
several class-II cytokine receptors. It is recruited by ligand-bound primary
chains such as IL-10RA in the IL-10 receptor, IL-22RA1 in the IL-22 receptor,
and IFNLR1 in the IFN-lambda receptor; the active complexes signal mainly
through JAK/STAT transcriptional outputs. This prior makes `Il10ra` the most
specific represented analog for the canonical IL-10 arm, and `Ifnar1`/`Ifnar2`,
`Ifngr1`/`Ifngr2`, `Il6ra`/`Il6st`/`Osmr`, and `Stat1`/`Stat3` useful pathway
counterexamples for whether this neuronal assay has tonic cytokine-to-STAT
flux.

The direct IL-10R comparison argues for a zero. `Il10ra` had `n_degs = 0` in the
focal cell group, its best focal adjusted p-value was only 0.432, and the
Distributed Agents same-experiment findings reported no downstream FDR 0.10 response in
any recovered neuronal group. If the IL-10 receptor were actively shaping basal
`151 TH Prkcd Grin2c Glut` expression, loss of its ligand-binding alpha chain
should have been at least as likely as loss of the common beta chain to expose
an IL-10/STAT3 program.

The IL10RB arms not directly covered by `Il10ra` also do not pull the prediction
upward. `Ifnlr1`, `Il22ra1`, and `Il20r*` receptors were not in the focal
training-count table, so the IFN-lambda and IL-22 complexes lack exact same
complex perturbations. However, `Ifnar1`, `Ifnar2`, `Ifngr1`, and `Ifngr2` each
had 0 focal DEGs, and the IRF/STAT machinery around antiviral and IFN-gamma
responses was flat apart from `Stat1` counting its own on-target depletion as a
single DEG. That makes a hidden, broad IFN-lambda-like response unlikely in
unstimulated NeuN-positive neurons. Similarly, gp130/IL-6-family receptor
components and other immune cytokine receptors had 0 focal DEGs, which supports
the idea that these ligand-gated immune axes are mostly context-mismatched in
this cell group rather than just missed one gene at a time.

External biology fits the same call. IL10RB is a broadly reused receptor chain,
but it is not a transcription factor or constitutive chromatin regulator; it
needs the appropriate ligand-binding partner and cytokine exposure. IL-10,
IL-22, and IFN-lambda biology is strongest in inflammatory, host-defense, and
barrier contexts. The experiment here was an acute sparse neuronal CRISPR assay
without an IL-10-family ligand, IFN, infection, or injury challenge, and most
glial/immune cells that would supply or respond to these cytokines were depleted
by NeuN enrichment.

I therefore predict `Il10rb` to be indistinguishable from the direct `Il10ra`
and cytokine-receptor zeros in this focal endpoint:

| target | predicted_n_degs |
| --- | ---: |
| Il10rb | 0 |

# Limits

- The exact `Il10rb` perturbation signature was held out, so every estimate is a
  transfer from other targets.
- `Ifnlr1`, `Il22ra1`, the JAK kinases, TYK2, SOCS genes, and several
  IL-10-family receptor components were not represented as focal training
  perturbations; IFN-lambda and IL-22 branches are therefore extrapolations.
- The DE parquet reports signed single-nucleus RNA changes but not absolute
  receptor expression, DNA indel rates, protein loss, phospho-STAT activity, or
  acute signaling after ligand stimulation.
- Large absolute log fold changes on FDR-1.0 rows were present in many zero
  signatures and were treated as sparse-gene rank artifacts rather than
  downstream evidence.
- This prediction only applies to unchallenged P16-to-P37/44 NeuN-enriched
  postmitotic mouse neurons. IL10RB loss could be highly consequential in
  epithelial, hematopoietic, glial, infected, injured, or cytokine-stimulated
  contexts while still producing `0` focal DEGs here.
