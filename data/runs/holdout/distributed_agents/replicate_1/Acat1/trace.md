# Acat1 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The requested endpoint is the number of measured genes with Wilcoxon BH-adjusted
`pvals_adj < 0.05` after each held-out perturbation in `151 TH Prkcd Grin2c
Glut` nuclei. The single held-out target in this run is `Acat1`.

`n_degs` is directly observed for visible training perturbations in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. `Acat1` itself was held out:
it is absent from the training-count CSV and absent as a `gene_target` in
`training_de_all_cell_groups.parquet`. The parquet is therefore direct evidence
for training analogs but contains no direct `Acat1` perturbation result.

I treated the supplied DEG-count CSV as the authoritative endpoint for visible
targets and used focused parquet slices only to identify which genes drove
analog counts and whether ketone-body or mitochondrial-stress readouts moved.
The endpoint counts include the perturbed transcript itself when it passes FDR;
for example, `Pdha1`, `Idh3a`, `Mdh2`, `Sdha`, `Sucla2`, `Cox5a`, `Cpt1c`, and
several `Slc25` mitochondrial carrier targets each have one focal-cell DEG
largely because the self transcript, rather than a downstream module, passed
FDR 0.05.

## Sources

- Input training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Input DE parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Acat1`.
- Run-local metadata: `task_bindings.json`, `coverage.json`,
  `capabilities.json`, and `measurement_registry.json`.
- Same-experiment semantic layer: the internal
  `perturbai-july-260713-sourceguard-1773-v1` Finding/report corpus, used only
  as a compact interpretation of training perturbations from the same PerturbAI
  atlas.
- KEGG REST, queried on 2026-09-03, for the mouse `Acat1` entry
  `mmu:110446`. KEGG annotates Acat1 to fatty-acid degradation, valine/leucine/
  isoleucine degradation, lysine degradation, tryptophan metabolism, pyruvate
  metabolism, glyoxylate/dicarboxylate metabolism, butanoate metabolism,
  terpenoid-backbone biosynthesis, general metabolic pathways, carbon
  metabolism, fatty-acid metabolism, and cholesterol metabolism.
- PubMed literature for ACAT1/beta-ketothiolase biology: Abdelkreem et al.,
  2019, DOI `10.1002/humu.23831`, PMCID `PMC6790690`; Grunert and Sass, 2020,
  DOI `10.1186/s13023-020-01357-0`, PMID `32345314`; Wojcik et al., 2017, DOI
  `10.1007/8904_2017_45`, PMID `28726122`; Mick et al., 2020, DOI
  `10.7554/eLife.49178`, PMID `32463360`.

## Computation over the supplied data

1. Loaded the requested-target CSV and found exactly one target: `Acat1`.
2. Loaded the focal training-count CSV. It contains 1,674 visible biological
   perturbations. The count distribution is extremely zero-inflated:
   1,205/1,674 are zero, 276 are one, the median is zero, the 75th percentile is
   one, the 95th percentile is 18, and 88.5% of targets have zero or one DEG.
3. Searched the visible training universe for metabolic analogs and extracted
   the exact `151 TH Prkcd Grin2c Glut` parquet rows for those targets. I
   counted `pvals_adj < 0.05` per target and inspected the lowest-FDR rows so
   that a one-gene result could be distinguished from a broad downstream state.
4. Queried Acat1/ketone-body readout genes as measured genes in the same focal
   cell type to check whether the visible analog perturbations moved the
   ketolysis module. `Acat1`, `Acat2`, `Bdh1`, `Bdh2`, `Hmgcl`, `Hmgcs2`, and
   `Oxct1` were not FDR-regulated by any inspected mitochondrial-carbon analog;
   the focal `Acat1` transcript had `pvals_adj = 1.0` after `Etfa`, `Ivd`,
   `Dlat`, `Pdha1`, `Dld`, `Dlst`, `Hmgcr`, `Aco2`, `Idh3a`, `Mdh2`, `Mpc1`,
   `Ogdh`, `Sdha`, `Sucla2`, `Suclg1`, `Opa1`, `Nrf1`, `Esrra`, `Ppara`,
   `Ppard`, `Pparg`, `Ppargc1a`, and `Srebf2` perturbation.
5. Read the compact internal Finding summaries for the most relevant visible
   analogs: `Etfa`, `Dlat`, `Sdha`, and `Sucla2`. The report corpus has no
   `Acat1` report, as expected for a held-out target.

## Target-specific reasoning

### `Acat1`

**Biological role.** KEGG places mouse `Acat1` in mitochondrial carbon branches
including fatty-acid degradation, ketone-body/butanoate metabolism, valine/
leucine/isoleucine degradation, and central carbon metabolism. The human
literature on ACAT1, also called mitochondrial acetoacetyl-CoA thiolase or T2,
is concordant: beta-ketothiolase deficiency impairs isoleucine catabolism and
ketone-body utilization and produces episodic ketoacidosis, usually under
infection, fasting, or ketogenic stress rather than a constitutive isolated
neuronal transcriptional syndrome (Abdelkreem et al. 2019; Grunert and Sass
2020; Wojcik et al. 2017).

That biology made the most appropriate within-dataset analogs the available
enzymes and regulators in adjacent mitochondrial-carbon, ETF, pyruvate, TCA, and
lipid-oxidation pathways. Exact same-step ketone-body perturbations were not in
the visible training set: `Hmgcl`, `Hmgcs2`, `Oxct1`, `Bdh1`, `Acat2`, `Acaa2`,
`Etfb`, `Etfdh`, and the major `Acad*` donors were not represented as
`gene_target` values in the focal training counts.

**Relevant visible analogs in `151 TH Prkcd Grin2c Glut`.**

| analog | observed `n_degs` | focal expression-pattern evidence | relationship to Acat1 |
|---|---:|---|---|
| `Etfa` | 0 | no FDR 0.05 or 0.10 genes; the internal corpus reports no ETF, ISR, UPRmt, redox, or fatty-acid-response program across 21 measured neuronal classes | ETF accepts electrons from fatty-acid and amino-acid dehydrogenases; like Acat1, it is a substrate-entry mitochondrial branch expected to matter most under fatty-acid/amino-acid catabolic demand |
| `Ivd` | 0 | no FDR 0.05 or 0.10 genes; best focal row `Apbb1` had FDR 0.275 | proximal isoleucine-catabolism comparator upstream of 2-methylacetoacetyl-CoA cleavage |
| `Bckdhb` | 0 | no FDR 0.05 or 0.10 genes; best focal rows all FDR 1.0 | branched-chain amino-acid oxidation comparator, still upstream of Acat1's T2 reaction |
| `Dlat` | 1 | one DEG, the self transcript `Dlat`; `Jarid2` was the only near-threshold downstream gene at FDR 0.0577; PDC/TCA comparators did not phenocopy it | core mitochondrial pyruvate dehydrogenase subunit, a counterexample showing one isolated self/transcript event rather than generic carbon-metabolism stress |
| `Pdha1` | 1 | one DEG, the self transcript `Pdha1`; all downstream rows were FDR 1.0 | same PDC reaction as Dlat but did not produce the Dlat-Jarid2 near-hit or a stress module |
| `Dld`, `Dlst`, `Mpc1`, `Ogdh`, `Aco2` | 0 each | no focal FDR 0.05 or 0.10 genes for these PDC/TCA/pyruvate-entry targets | visible carbon-oxidation neighbors that argue against a shared TCA or pyruvate-defect RNA state |
| `Idh3a`, `Mdh2`, `Sdha`, `Sucla2` | 1 each | one significant self transcript in the focal cell class; `Sdha` additionally had `Edem2` at FDR 0.0646, but not a broad ER/ISR or HIF program | core mitochondrial TCA/complex-II comparators; their response was buffered to isolated self or edge single-gene signals |
| `Suclg1` | 0 | no focal FDR 0.05 or 0.10 genes | same succinyl-CoA ligase complex neighborhood as `Sucla2`, serving as a zero counterexample to over-transfer from one-gene mitochondrial results |
| `Hmgcr` | 0 | no focal FDR 0.05 or 0.10 genes; the same-experiment corpus shows `Srebf2`, not `Hmgcr`, elicited sterol-transcription feedback | HMG-CoA reductase is not mitochondrial T2, but it tests whether a CoA/sterol branch perturbation produces an `Acat1`-like broad response; it did not |
| `Cpt1c`, `Ppara`, `Ppard`, `Pparg`, `Ppargc1a` | 1, 0, 0, 0, 0 | `Cpt1c` had a self-only focal call; PPAR/PGC1 lipid regulators were focal-cell nulls | lipid-utilization comparators; the visible set does not support a strong neuronal fatty-acid-oxidation transcriptional module |
| `Opa1`, `Nrf1`, `Esrra` | 37, 138, 57 | broad ISR/mitochondrial regulatory signatures | counterexamples: this assay can generate many focal DEGs for a mitochondrial perturbation, but these targets regulate cristae or nuclear respiratory programs rather than a buffered ketolysis/isoleucine branch |

The key causal comparison is intervention to endpoint:

`Acat1` CRISPR should impair mitochondrial acetoacetyl-CoA thiolase activity,
which limits ketone-body utilization and late isoleucine catabolism; that could
propagate to acetoacetyl-CoA/2-methylacetoacetyl-CoA-derived metabolite changes
under ketogenic or branched-chain-amino-acid load. In this experiment the
intervention is partial, mosaic, postmitotic, and assayed in recovered NeuN+
nuclei at baseline. The relevant flux may therefore remain below the threshold
for an ATF4/ISR, UPRmt, HIF, redox, or fatty-acid regulatory RNA response.
This is not because the platform is blind to mitochondrial stress: `Opa1`,
`Nrf1`, and `Esrra` produced 37 to 138 focal DEGs, and Mick et al. 2020 show
that mitochondrial ISR activation is defect- and metabolic-state-dependent,
not automatic for every mitochondrial enzyme lesion.

The direct analog evidence points downward. The nearest represented substrate
entry and isoleucine/fatty-acid oxidation perturbations, `Etfa`, `Ivd`, and
`Bckdhb`, were completely FDR-null in this cell group. Available TCA/PDC
comparators were also zero or one-gene calls, usually self transcript only, and
they did not co-regulate `Acat1` or the ketone-body genes as measured
transcripts. More distant regulators such as `Opa1`, `Nrf1`, and `Esrra`
establish detectability of secondary mitochondrial transcription, but their
broad outputs should not be transferred to `Acat1` because a buffered
ketolysis/isoleucine branch is not the same limiting function as cristae
remodeling or nuclear respiratory-gene control in the assay window.

I therefore predict that `Acat1` will behave like the visible ETF/TCA branch
targets and stay at zero rather than produce a broad downstream program. The
main residual uncertainty is the self transcript: visible metabolic targets
with strong self depletion often score as exactly one DEG. I still assigned
zero because many mechanistically closer branch targets had no self or
downstream FDR call, the held-out endpoint is FDR-strict, and no available
training perturbation produced a ketolysis-module response that would push the
expected count above one.

Predicted `n_degs`: **0**.

## Limits

- `Acat1`, `Hmgcl`, `Hmgcs2`, `Oxct1`, `Bdh1`, `Acaa2`, `Etfb`, `Etfdh`, and
  the major acyl-CoA dehydrogenases were not visible training perturbations, so
  the prediction transfers from nearby but imperfect mitochondrial-carbon
  analogs.
- The parquet reports nuclear RNA in recovered, class-assigned nuclei. It does
  not measure ACAT1 protein, enzyme flux, ketone bodies, isoleucine-derived
  organic acids, acylcarnitines, absolute RNA, guide exposure, or pre-assay
  depletion.
- Human beta-ketothiolase deficiency is recessive, systemic, developmental, and
  stress-triggered. It is informative for ACAT1 biochemistry but not a direct
  match to partial acute P16 CRISPR in mouse thalamic glutamatergic neurons.
- A zero prediction is a statement about the FDR 0.05 DEG count, not about
  absence of a biochemical consequence.
