# Chrna5 held-out DEG prediction

## Question and interpretation

The requested held-out target file contains one perturbation, `Chrna5`, for the
focal cell group `151 TH Prkcd Grin2c Glut`. I interpreted the endpoint as:

- count all measured genes, including the perturbed gene itself if it is
  measured;
- use the held-out perturbation's Wilcoxon differential-expression test in
  `151 TH Prkcd Grin2c Glut`;
- report the number of rows with Benjamini-Hochberg adjusted `pvals_adj < 0.05`;
- make a non-negative integer point prediction.

`Chrna5` was not present as a `gene_target` in the supplied parquet and was not
present in the focal-cell training-count CSV, so I treated all `Chrna5`
readout values as genuinely unobserved.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed training `n_degs` in the focal group.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell per-gene Wilcoxon scores, log fold changes, FDR values, and
  matched nucleus counts for biologically related training perturbations.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`,
  especially `claim:19d81f58855e7218ecbc`, which summarizes that represented
  single nicotinic acetylcholine receptor subunit perturbations did not produce
  a shared basal neuronal transcriptional state in this assay.
- Distributed Agents runtime score-profile comparison:
  `chrn_score_profile_compare.json` and `chrn_score_profile_inspect.json`.
  These were computed in this run from Wilcoxon `scores`, with the exact
  context `group_name == "151 TH Prkcd Grin2c Glut"`, over the Chrn/Ache/Lrp4/
  Musk training cohort.
- NCBI Gene and UniProtKB/Swiss-Prot records as represented in the Distributed Agents
  corpus for receptor-subunit identity and beta2-containing nAChR assembly
  annotations.
- External PubMed literature for Chrna5 mechanism:
  Kuryatov, Berrettini & Lindstrom 2010, DOI `10.1124/mol.110.066357`,
  PMID `20881005`; Scholze et al. 2012, DOI
  `10.1111/j.1471-4159.2012.07714.x`, PMID `22380605`; Fowler et al. 2011,
  DOI `10.1038/nature09797`, PMID `21278726`; Frahm et al. 2011, DOI
  `10.1016/j.neuron.2011.04.013`, PMID `21555077`; Hsu et al. 2013, DOI
  `10.1523/JNEUROSCI.2927-13.2013`, PMID `24227714`; Morton et al. 2018,
  DOI `10.1523/JNEUROSCI.0023-18.2018`, PMID `29954848`; and the Scholze &
  Huck 2020 review, DOI `10.3389/fnsyn.2020.607959`, PMID `33343327`.

## Computational evidence from the training set

I first used the focal training-count CSV to place `Chrna5`'s likely count on
the assay scale. Among all 1,674 non-held-out perturbations in
`151 TH Prkcd Grin2c Glut`, the median `n_degs` was 0, the 75th percentile was
1, the 90th percentile was 2, the 95th percentile was 18, and 469/1,674
perturbations had any focal DEGs at all. The very broad responses in this cell
type were general RNA-processing, chromatin, proteostasis, and essential
regulatory targets rather than neuronal receptor subunits.

I then extracted observed counts for represented nicotinic and cholinergic
comparators:

| training target | focal `n_degs` | relevance to `Chrna5` |
| --- | ---: | --- |
| `Chrna3` | 0 | part of the same human/mouse Chrna5/Chrna3/Chrnb4 nAChR gene cluster; alpha3beta4alpha5 receptors are a known alpha5 context |
| `Chrna4` | 2 | alpha5 can enter alpha4beta2* receptors |
| `Chrnb2` | 1 | beta2-containing receptors include alpha4beta2alpha5 and other neuronal nAChRs |
| `Chrna2` | 0 | neuronal nicotinic alpha subunit |
| `Chrna6` | 0 | neuronal beta2/beta3 partner |
| `Chrna7` | 0 | abundant homomeric neuronal nAChR subunit, a same-family counterexample |
| `Chrnb3` | 0 | beta accessory subunit in alpha6beta2beta3* receptors |
| `Chrna1`, `Chrnb1`, `Chrnd`, `Chrne`, `Chrng` | all 0 | muscle-type nAChR subunits, weaker counterexamples |
| `Chrm2`, `Chrm3` | both 0 | muscarinic receptor counterexamples in the cholinergic input pathway |
| `Ache` | 1 | acetylcholine hydrolysis; its only focal FDR hit was `Ache` itself |
| `Lrp4`, `Musk` | both 0 | neuromuscular-junction controls, not direct neuronal alpha5 analogs |

The direct parquet rows clarified those counts. In the focal cell group:

- `Chrna4` had two FDR<0.05 rows: `Chrna4` down
  (`score = -5.13`, `pvals_adj = 0.0037`) and `Cyp46a1` down
  (`score = -5.05`, `pvals_adj = 0.0037`).
- `Chrnb2` had one FDR<0.05 row: `Chrnb2` down
  (`score = -6.59`, `pvals_adj = 7.37e-7`).
- `Ache` had one FDR<0.05 row: `Ache` down
  (`score = -5.17`, `pvals_adj = 0.0041`).
- `Chrna1`, `Chrna2`, `Chrna3`, `Chrna6`, `Chrna7`, `Chrnb1`, `Chrnb3`,
  `Chrnd`, `Chrne`, `Chrng`, `Lrp4`, and `Musk` had no FDR<0.05 rows.

Those perturbations were all in a similar power range, with 117 to 293 matched
perturbed nuclei and 23,679 matched controls. Thus the zero or one-hit outcomes
are not just the consequence of having far fewer nuclei than the assay's broad
positive controls.

For expression-pattern evidence, I compared the 15 represented Chrn/Ache/Lrp4/
Musk profiles over all 17,259 measured genes using Wilcoxon `scores`, not raw
log fold changes. Score-vector Pearson correlations among the closest receptor
comparators were near zero: `Chrna4` to the family had a maximum r of 0.0357
and a mean r of 0.0125; `Chrnb2` had a maximum of 0.0146 and a mean of -0.0176;
`Chrna7` had a maximum of 0.0394 and a mean of 0.0059; `Chrna3` had a maximum
of 0.0826 and a mean of 0.0129. The Distributed Agents runtime comparison against all
1,674 eligible training profiles likewise found that the best whole-profile
Pearson neighbor of `Chrna4` had r = 0.0535, and top-200 signed-tail overlap
neighbors shared only 0.075 or less of the tail. This argues against a hidden,
coherent, broadly regulated nAChR module.

The internal Distributed Agents corpus independently supports this negative pattern.
Its high-confidence nicotinic claim states that represented single-subunit
nAChR perturbations do not produce a shared basal neuronal transcriptional
state among receptor-family members in this assay. The Chrnb2 finding anchors
that the direct alpha4/alpha6/alpha2/alpha3/beta3 relatives had zero
shared-direction downstream overlap with `Chrnb2`; the Chrna4 findings qualify
the family-level null with a small, cell-type-localized `Cyp46a1` effect that
did not converge with `Chrnb2`, `Chrna2`, `Chrna6`, `Chrna7`, `Chrnb3`, or
`Ache`.

## Target-specific reasoning for `Chrna5`

`Chrna5` encodes the alpha5 nicotinic acetylcholine receptor accessory subunit.
It can assemble into both alpha4beta2* and alpha3beta4* nAChRs, where it changes
receptor trafficking, calcium signaling, desensitization, and agonist responses
rather than creating a DNA-binding or cytosolic transcription-factor function
of its own. Kuryatov et al. 2010 showed functional effects of the human D398N
alpha5 variant in alpha4beta2alpha5 receptors; Scholze et al. 2012 found that
rodent habenular alpha5-containing receptors depend on beta4 and assemble with
alpha3, beta2, and beta4; Scholze & Huck 2020 reviewed the accessory alpha5
subunit's differential modulation of alpha4beta2* and alpha3beta4* receptors.

The closest same-complex training analogs are imperfect but consistently flat.
`Chrna3` is the represented member of the alpha3/beta4/alpha5 cluster and had
0 focal DEGs. `Chrna4` and `Chrnb2` are the represented alpha4beta2* partners
and had only 2 and 1 DEGs, respectively; two of those three rows were merely
the knocked-down target transcripts themselves. `Chrna6` and `Chrnb3`, another
beta2/beta3-containing nicotinic branch, were both 0. `Chrna7` was a same-family
neuronal receptor-subunit counterexample at 0. The focal score vectors of these
targets did not converge, which makes a shared receptor-homeostatic response
unlikely.

External biology makes `Chrna5` important, but in readouts that this experiment
does not assay. Fowler et al. 2011 showed that loss or knockdown of alpha5 in
the habenulo-interpeduncular pathway changes nicotine intake and nicotine-
induced interpeduncular nucleus activation. Frahm et al. 2011 linked balanced
beta4/alpha5 activity in the medial habenula to nicotine aversion. Hsu et al.
2013 and Morton et al. 2018 found strong `Chrna5`-lineage function in
GABAergic interpeduncular nucleus neurons and in aversion primed by nicotine or
prior stimulation. Those are ligand-evoked current, circuit, and behavior
phenotypes, not evidence that weak, mosaic, postnatal loss of one nAChR
accessory subunit should induce many resting nuclear RNA changes in a thalamic
glutamatergic class.

I therefore expect `Chrna5` to be either completely silent or, at most, to
register a self-transcript hit like `Chrnb2` or `Ache`. Because alpha5's most
established strong mouse expression and function are outside this thalamic
glutamatergic focal class, and because the closest represented subunits with
direct downstream consequences did not share a real downstream program, I put
the point estimate at the mode of the receptor-subunit analogs: 0 DEGs.

## Prediction

| target_name | predicted_n_degs |
| --- | ---: |
| `Chrna5` | 0 |

## Limits

- `Chrna5` itself and `Chrnb4`, its most direct alpha3beta4alpha5 partner, were
  absent as training perturbations; `Chrna3` is informative but cannot replace
  a same-pentamer beta4 or alpha5 observation.
- The supplied parquet contains DE statistics, not raw baseline expression or
  receptor currents, so I could not directly verify whether `Chrna5` target RNA
  is abundant enough in `151 TH Prkcd Grin2c Glut` to appear as a self hit.
- nAChR loss can have strong nicotine-challenge and circuit-level effects that
  would be invisible to this basal snRNA-seq endpoint.
- A count of 1 or 2 would be plausible if `Chrna5` behaves like `Chrnb2` or the
  sparse `Chrna4` outlier; the stronger within-dataset evidence is that the
  represented family is at the floor and lacks a convergent downstream program,
  so I used 0 as the integer point prediction.
