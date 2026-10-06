# DEG-count prediction trace

## Question and endpoint

The task asks for a point prediction of `n_degs` for each requested held-out
perturbation in `151 TH Prkcd Grin2c Glut` cells. Here `n_degs` means the number
of measured genes with Scanpy Wilcoxon Benjamini-Hochberg adjusted `pvals_adj <
0.05` in perturbed nuclei versus matched non-targeting controls.

This run has one held-out target:

| target_name |
|---|
| Chrnb4 |

I treated file order in that single unranked target list only as required output
order. `Chrnb4` is absent as a `gene_target` from the supplied Parquet and as a
`target_name` from the training-count CSV, so there is no direct observed DEG
count for this target in the declared inputs.

The requested endpoint is directly observed for non-held-out training
perturbations in the focal class through the training DEG-count CSV and can also
be recomputed from the declared DE Parquet. It is absent for `Chrnb4`, so the
prediction below transfers from biologically related training perturbations.

## Sources

Internal declared inputs:

- `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - Direct focal-cell endpoint for 1,674 non-held-out training perturbations.
- `training differential-expression dataset`
  - Differential-expression rows for non-held-out perturbations across neuronal
    classes; this was queried for the raw focal signatures and for other-cell
    checks of nicotinic-receptor perturbations.
- `single-target request for Chrnb4`
  - The run's requested-target manifest.

Same-experiment semantic layer:

- PerturbAI July corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, used through the declared
  `corpus.findings`, `corpus.calibration`, and BioKG graph capabilities.
  The graph lookup for `Chrna5` returned no comparator records. Finding records
  for `Chrna3`, `Chrna4`, `Chrnb2`, and `Ache` were used as compact
  interpretations of the same DE experiment, especially to check whether the
  obvious cholinergic receptor subunits had a hidden broad response or curated
  convergence that was not obvious from the focal DEG counts. These records are
  not independent replication of the Parquet.

External literature found through NCBI PubMed:

- Gahring, Persiyanov, and Rogers 2004, J Comp Neurol,
  DOI: `10.1002/cne.10942`, PMID: `14681928`: beta4 nicotinic acetylcholine
  receptor protein is present in discrete adult mouse brain populations,
  including medial habenula/interpeduncular projections, auditory nuclei, and
  cell bodies of the ventral thalamic nucleus.
- Marks, Whiteaker, and Collins 2006, Mol Pharmacol,
  DOI: `10.1124/mol.106.025338`, PMID: `16728647`: deleting beta4 reduces
  subsets of epibatidine-binding nicotinic receptor sites, including analyses in
  thalamus, and shows beta4 contributes to receptor pharmacology rather than to
  a direct transcriptional-regulator role.
- Slimak et al. 2014, Front Hum Neurosci,
  DOI: `10.3389/fnhum.2014.00012`, PMID: `24478678`: beta4 with alpha3 is
  enriched in the medial habenula-interpeduncular tract; habenular beta4
  expression and Chrnb4 missense variants alter alpha3/beta4 receptor currents
  and nicotine consumption phenotypes in mice.
- Tsuzuki et al. 2024, Sci Rep,
  DOI: `10.1038/s41598-024-65076-3`, PMID: `38902419`: endogenous alpha3- and
  beta4-containing nAChRs are abundant along the mouse medial habenula to
  interpeduncular pathway and are localized largely outside synaptic junctions.
- Muldoon et al. 2014, Br J Pharmacol,
  DOI: `10.1111/bph.12741`, PMID: `24750073`: alpha3/beta4* nAChRs influence
  morphine physical-withdrawal behavior; beta4 knockout mice had reduced
  somatic withdrawal signs.

## Quantitative checks over the declared dataset

I first read the 1,674-row focal training-count CSV to establish the response
breadth scale. The distribution is very sparse: 1,205/1,674 training
perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, and
the largest responses are rare high-count regulators such as `Uba5` at 2,677,
`Tpr` at 1,768, and `Sin3a` at 1,433.

I then looked up direct acetylcholine and nicotinic-receptor neighbors in that
training count table:

| training perturbation | focal `n_degs` | relationship to `Chrnb4` |
|---|---:|---|
| `Chrna3` | 0 | closest represented alpha partner for alpha3/beta4-containing nAChRs |
| `Chrnb2` | 1 | beta nAChR subunit; forms heteromeric neuronal nicotinic receptors |
| `Chrna4` | 2 | alpha partner of beta2-containing high-affinity nAChRs |
| `Chrna7` | 0 | neuronal nAChR subunit, but primarily a different homomeric/alpha-bungarotoxin-sensitive class |
| `Chrnb3` | 0 | accessory neuronal beta subunit |
| `Chrna2` | 0 | neuronal alpha subunit |
| `Chrna6` | 0 | neuronal alpha subunit |
| `Ache` | 1 | acetylcholine hydrolysis upstream of nicotinic and muscarinic receptors |
| `Chrna1`, `Chrnb1`, `Chrnd`, `Chrne`, `Chrng` | 0 each | muscle-type receptor subunits; weak CNS analogs/counterexamples |

To verify that the count-table nulls represented the Parquet rows rather than a
join artifact, I filtered the Parquet to `group_name = '151 TH Prkcd Grin2c
Glut'` and these receptor targets. Each target had 17,259 measured-gene rows in
the focal class. The FDR 0.05 rows were:

| training perturbation | matched perturbed nuclei in focal class | FDR 0.05 genes |
|---|---:|---|
| `Chrna3` | 148 | none |
| `Chrna4` | 293 | `Chrna4` and `Cyp46a1` |
| `Chrnb2` | 222 | `Chrnb2` |
| `Chrnb3` | 120 | none |
| `Chrna7` | 212 | none |
| `Ache` | 117 | `Ache` |

For the closest partner `Chrna3`, even the largest absolute Wilcoxon scores were
not near significance after multiple testing: `Aifm3`, `Inpp5f`, `Adam22`, and
`Virma` all had adjusted p-values of 0.499. The focal Wilcoxon-score
correlations among the relevant receptor perturbations were also essentially
zero, for example `Chrna3` versus `Chrna4` was 0.0168 and `Chrna3` versus
`Chrnb2` was -0.0946. I did not use the high correlations among raw log-fold
change vectors because many lowly detected cholinergic genes have extreme,
shared pseudocount-driven log-fold changes with Wilcoxon scores near zero and
`pvals_adj = 1.0`.

I also summarized these receptor perturbations across all neuronal classes in
the Parquet. `Chrna3`, `Chrna2`, `Chrna6`, `Chrna7`, `Chrnb1`, and `Chrnb3`
had no FDR 0.05 DEG in any assayed class. `Chrnb2` had only its self-transcript
called in `151 TH Prkcd Grin2c Glut`, `155 MB Glut`, and `191 MB P MY GABA`;
`Chrna4` had only the two focal hits. Thus the low focal counts do not hide a
strong nAChR response shifted into another broad class.

The packaged PerturbAI July Findings were concordant:

- `Chrna3` was reported as a pan-surface basal-transcriptome null across
  recovered postnatal central neurons, and its obvious nAChR family comparators
  failed to form a shared downstream transcriptional module.
- `Chrnb2` was reported as a self-transcript event with no non-self
  FDR-gated response; its literature-obvious alpha partners did not converge on
  a receptor-subunit, stress, or synaptic program.
- `Chrna4` had a sparse, thalamic `Cyp46a1`-down response, but `Chrnb2` and
  other represented nicotinic relatives did not phenocopy it, so the record
  warns against inferring a broad nAChR homeostatic module from the isolated
  `Cyp46a1` hit.
- `Ache` reduced its own transcript in several classes but produced no
  pan-neuronal downstream response, which makes persistent cholinergic
  overexcitation after sparse postnatal CRISPR unlikely as a DEG-count analog.

## Target-specific causal transfer

### Chrnb4

`Chrnb4` encodes the beta4 neuronal nicotinic acetylcholine receptor subunit.
The causal chain for this perturbation is:

`Chrnb4` CRISPR loss of function -> loss of beta4 subunit protein in edited
neurons -> reduced assembly and/or altered cation conductance of beta4-containing
heteromeric nAChRs, especially alpha3/beta4 or alpha3/alpha5/beta4 receptors in
cells where those subunits are coexpressed -> altered acetylcholine or nicotine
responsiveness and neuronal excitability -> any sustained transcriptional
adaptation among nuclei that survive, are sampled, and are assigned to `151 TH
Prkcd Grin2c Glut` -> FDR 0.05 DEG count.

External literature supports the first three links in the appropriate receptor
systems. Beta4 protein is present in parts of the mouse brain including ventral
thalamic neurons (Gahring et al. 2004), beta4 knockout changes nicotinic ligand
binding in thalamus and other regions (Marks et al. 2006), and beta4 with alpha3
has a strong functional role in medial habenula-interpeduncular nAChRs and in
nicotine or opiate-withdrawal behaviors (Slimak et al. 2014; Muldoon et al.
2014; Tsuzuki et al. 2024).

The last links in the chain are not supported as a broad basal snRNA-seq effect
in this screen. The best same-complex same-direction prior is `Chrna3`, because
loss of alpha3 and loss of beta4 should both impair alpha3/beta4 receptor
function where that receptor is limiting. `Chrna3` had 0 focal DEGs and 0 DEGs
across every broad cell class assayed. That is candidate-specific evidence that
removing this receptor subtype does not usually create a large, stable nuclear
RNA program 3-4 weeks after sparse P16 editing. `Chrnb2`, `Chrna4`, `Chrna7`,
`Chrnb3`, and `Ache` provide counterexamples to a generic cholinergic-receptor
homeostatic response: they are biologically related to acetylcholine-gated
signaling, but they were flat or nearly flat and did not share a coherent
focal-cell expression pattern.

My zero/nonzero decision is therefore driven primarily by within-dataset analogs:
the closest assayed nAChR perturbations are at 0, 1, and 2 DEGs in the focal
class, and the one non-self `Chrna4` hit looks idiosyncratic rather than a
shared receptor-module response. External knowledge prevents treating
`Chrnb4` as irrelevant, especially because beta4 is functional in thalamic and
habenular receptor physiology, but those endpoints are ligand binding,
ion-channel current, transmitter release, and behavior. They do not establish
that acute mosaic `Chrnb4` loss in recovered `151 TH Prkcd Grin2c Glut` nuclei
will cross the FDR 0.05 DEG threshold for even one downstream gene.

The point prediction is:

| target_name | predicted `n_degs` |
|---|---:|
| Chrnb4 | 0 |

## Limits and uncertainty

`Chrnb4` itself and `Chrna5` were held out or otherwise absent as perturbation
targets in the supplied training data, so the closest complete
alpha3/alpha5/beta4 loss-of-function comparison is missing. The atlas class
`151 TH Prkcd Grin2c Glut` is a broad thalamic glutamatergic group, not a
purified medial habenula or ventral thalamic beta4-positive population; a small
beta4-expressing subset could be diluted below an FDR-gated snRNA-seq response.
The experiment did not apply nicotine or acetylcholine, did not assay receptor
protein localization or currents, and did not count pre-assay loss of edited
neurons. The prediction is therefore strongest for the requested basal
survivor-conditioned DEG-count endpoint and should not be read as a prediction
of no electrophysiological or behavioral consequence of beta4 loss.
