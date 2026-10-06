# DEG-count prediction for held-out `Mboat7`

## Question and endpoint

The requested prediction is the integer number of measured genes expected to
pass BH-adjusted Wilcoxon `pvals_adj < 0.05` after an acute CRISPR loss of
`Mboat7` in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons. The
held-out target was absent from both supplied inputs, so I treated the
training DEG counts as direct observations for visible perturbations and the
parquet expression signatures as same-experiment context for selecting and
falsifying analogs. No requested ordering was supplied; the requested-target
CSV contained one unranked target, exactly `Mboat7`.

The endpoint is directly observed for the 1,674 non-held-out perturbations in
`151 TH Prkcd Grin2c Glut` by
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. For `Mboat7` itself the
endpoint and expression signature are absent by construction, so the estimate
below is a prediction from visible postnatal neuronal perturbations plus
external gene-function knowledge.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE table:
  `training differential-expression dataset`.
  I extracted only rows whose `group_name` was `151 TH Prkcd Grin2c Glut`,
  yielding 28,891,566 measured-gene by perturbation rows over the same 1,674
  training targets as the endpoint CSV.
- Run-local manifests and context:
  `task_bindings.json`, `coverage.json`, `capabilities.json`,
  `measurement_registry.json`, and the PerturbAI atlas dataset portrait.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used bounded Finding reports
  only for phosphoinositide, endocytic, and lipid-metabolic visible
  perturbations that were already nominated by biochemical proximity to
  MBOAT7; this corpus is an interpretation layer over the same screen, not an
  independent experiment. A graph query for same-experiment Findings that
  reported `Mboat7` returned no rows.
- PubMed-indexed external literature for MBOAT7/LPIAT1 function:
  Lee et al. 2012, doi:10.1091/mbc.E12-09-0673, PMID 23097495; Anderson et
  al. 2013, doi:10.1371/journal.pone.0058425, PMID 23472195; Hirata et
  al. 2013, doi:10.1111/gtc.12046, PMID 23510452; Johansen et al. 2016,
  doi:10.1016/j.ajhg.2016.07.019, PMID 27616480; Caddeo et al. 2021,
  doi:10.1016/j.bbalip.2021.158891, PMID 33513444.

## Quantitative calibration from the focal training set

The focal training distribution is extremely zero-inflated and skewed:
1,205 of 1,674 visible targets had `n_degs = 0`, the median was 0, the 75th
percentile was 1, and only 132 targets had at least 5 DEGs. Large signatures
were concentrated in unrelated nuclear, proteasomal, splicing, trafficking, or
transcriptional perturbations such as `Uba5` at 2,677, `Tpr` at 1,768,
`Sin3a` at 1,433, `Rab7` at 501, and `Cic` at 576.

I therefore treated "no significant downstream transcript" as the local prior
for a membrane phospholipid enzyme unless a closer visible analog showed that
loss of a comparable lipid node normally drives a broad nuclear-RNA state in
this same postnatal cell group.

## MBOAT7 biology and causal transfer

`Mboat7` encodes LPIAT1, a membrane O-acyltransferase that preferentially
transfers polyunsaturated fatty acyl chains, especially arachidonoyl-CoA, onto
lysophosphatidylinositol. The product is arachidonoylated phosphatidylinositol;
loss of LPIAT1 in mouse brain and liver shifts PI and PI-phosphate species
away from 38:4 species and raises lyso-PI pools. This is a direct lipid
remodeling event on endomembranes, not a transcription factor or an obligate
component of a chromatin or RNA-processing complex.

Complete germline Lpiat1/Mboat7 deficiency is not benign: Lee et al. showed
that `Lpiat1-/-` mice have nearly absent arachidonoyl-CoA-dependent LPIAT
activity, reduced arachidonic acid in PI/PI phosphates, abnormal cortical
lamination, reduced neurite outgrowth, and death within a month; Anderson et
al. found reduced total PtdIns and PtdInsP2 and increased lyso-PtdIns in
`Lpiat1-/-` brain and liver; biallelic human MBOAT7 mutations cause
intellectual disability often accompanied by epilepsy or autistic features in
the Johansen et al. cohort. Hirata et al. additionally identified ssSPTa as an
LPIAT1 interactor that helps place LPIAT1 at mitochondria-associated membranes
where arachidonic-acid-selective acyl-CoA synthetase is enriched, and Caddeo
et al. biochemically confirmed that the conserved N321/H356 catalytic dyad is
needed for PUFA transfer to LPI.

For this task, the causal chain has several gaps between those mechanisms and
a large `151 TH Prkcd Grin2c Glut` DEG count:

1. The intervention here is sparse AAV CRISPR at P16 with roughly partial
   on-target RNA reduction on average, not inherited complete enzyme absence.
2. The direct MBOAT7 consequence is altered PI acyl-chain remodeling and LPI
   turnover.
3. The expected propagation is through phosphoinositide signaling, membrane
   trafficking, and possibly neurite/synaptic membrane physiology.
4. The nuclei sampled at P37-P44 are surviving, postmitotic, NeuN-positive
   neurons; embryonic migration failure, non-neuronal lipid inflammation, and
   lipidomic changes without stable nuclear-RNA feedback are either earlier,
   outside the sampled lineage, or outside the measured modality.

That chain predicts a possible subtle effect, but not a strong same-direction
transfer from germline cortical lamination phenotypes to a broad acute thalamic
snRNA-seq response.

## Visible perturbation analogs and counterexamples

The training set contained no focal-cell endpoint for `Mboat1`, `Mboat2`,
`Mboat4`, `Mboat5`, `Lpcat1`-`Lpcat4`, `Cdipt`, `Ptdss1`, `Ptdss2`,
`Pik3c3`, `Pikfyve`, `Pip4k2a`, `Pip4k2b`, `Pip4k2c`, `Pten`, `Inpp5e`,
`Sacm1l`, `Mtmr2`, or `Mtmr3`. I therefore inspected the closest visible
lipid/phosphoinositide and membrane-trafficking genes:

| visible perturbation | observed `n_degs` in `151 TH Prkcd Grin2c Glut` | focal expression-pattern evidence | relationship to `Mboat7` |
| --- | ---: | --- | --- |
| `Acsl4` | 1 | The only FDR<0.05 gene was `Acsl4` itself (`logfoldchanges = -0.995`, `p_adj = 3.8e-16`); the next-best candidate `Fbxo3` had `p_adj = 0.163`. | Supplies arachidonoyl-CoA to phospholipid remodeling and to MBOAT7/MMD-dependent AA-PI remodeling in non-neuronal cells, but this single-gene focal signature shows that disrupting a related AA-CoA activation step did not create a broad transcriptional state. |
| `Synj1` | 1 | The sole significant gene was the self transcript (`Synj1`, `logfoldchanges = -0.583`, `p_adj = 3.1e-07`); all downstream genes had `p_adj = 1.0`. | A neuronal PI(4,5)P2/Sac phosphatase at synaptic vesicle endocytosis. The corpus report likewise summarized a pan-neuronal downstream FDR-flat profile, so an acute phosphoinositide-enzyme hit can remain silent in nuclear RNA. |
| `Dgke` | 1 | Only `Dgke` itself passed FDR (`logfoldchanges = -0.586`, `p_adj = 6.0e-08`); `Fmn2` was subthreshold at `p_adj = 0.110`. | DAG kinase linked to phosphoinositide cycling; its buffered signature is a closer calibration point than broad lysosomal genes. |
| `Abhd12` | 1 | Only `Abhd12` itself passed FDR (`logfoldchanges = -0.846`, `p_adj = 3.4e-22`). | Lipid hydrolase with neurological phenotypes, but its canonical neuroinflammatory lipid consequences are microglial; the same corpus reported a globally buffered acute neuronal response. |
| `Pld3` | 1 | Only `Pld3` itself passed FDR (`logfoldchanges = -1.052`, `p_adj = 2.2e-16`). | Endomembrane phospholipase D family member; visible as a self hit without downstream response. |
| `Sptlc2` | 1 | Only `Sptlc2` itself passed FDR (`logfoldchanges = -0.685`, `p_adj = 1.5e-04`). | Its ssSPTa partner can bind LPIAT1, but the visible catalytic subunit perturbation did not broaden beyond a self transcript in the focal group. |
| `Pik3cb` | 0 | No gene was FDR-significant; minimum focal `p_adj = 1.0`. | Class I PI3K catalytic lipid kinase. The internal report described a pan-neuronal negative result, arguing that receptor-proximal PI lipid signaling losses were largely buffered. |
| `Pik3r1` | 0 | No gene was FDR-significant; minimum focal `p_adj = 0.776`. | Class IA PI3K regulatory subunit. The internal report contrasted its null with downstream `Tsc2`, showing that mTOR-related responses can be seen when the perturbed node is sufficiently coupled. |
| `Pik3r2` | 0 | No gene was FDR-significant; minimum focal `p_adj = 0.887`. | Second class IA PI3K regulatory subunit; also pan-neuronally buffered in the same corpus. |
| `Ocrl` | 0 | No gene was FDR-significant; minimum focal `p_adj = 0.200`. | PI(4,5)P2 5-phosphatase with endosomal functions; its report showed no lysosomal/autophagy or PI-phosphatase program despite those genes being measured. |

I also checked candidates that mark the boundary where the assay does respond
to membrane trafficking or lipid-metabolic stress:

- `Rab7` produced 501 focal DEGs and induced lysosomal/vacuolar ATPase genes
  such as `Atp6v1b2`, `Dpp7`, `Scpep1`, `Dusp1`, `Insig1`, and `Atp6v0b`.
  This is a strong late endolysosomal perturbation, not an LPI acyltransferase
  or same-complex MBOAT7 partner, so it is a counterexample showing assay
  sensitivity rather than a same-outcome prior.
- Retromer/GARP trafficking genes were weaker but nonzero: `Vps54` had
  31 DEGs and `Vps35` had 17, with focal hits including `Egr1`, `Jun`, and
  `Atp2a2`. These losses perturb broad vesicle sorting, which is a different
  intervention stage than changing the arachidonoyl chain composition of PI.
- mTOR/SREBP-axis genes show that a lipid-adjacent transcriptional feedback
  can appear in this cell group when the screen hits the right node:
  `Tsc2` had 86 DEGs and `Srebf2` had 7, whereas `Mtor` had only 2 and
  `Srebf1` had 0. MBOAT7 loss activates SREBP-1c lipogenesis in hepatocytes
  in published liver-specific models, but focal postnatal neurons lack a
  visible reason to copy that hepatocyte triglyceride pathway.

## Target-specific decision

### `Mboat7`

Prediction: `0`.

The within-dataset evidence drove the zero/nonzero call. The closest visible
perturbations that touch phosphoinositides, arachidonic-acid handling, or
endomembrane lipid biology were mostly `0` or isolated self-transcript hits in
the focal group: `Pik3cb = 0`, `Pik3r1 = 0`, `Pik3r2 = 0`, `Ocrl = 0`,
`Synj1 = 1`, `Dgke = 1`, `Abhd12 = 1`, `Pld3 = 1`, `Sptlc2 = 1`, and
`Acsl4 = 1`. The FDR-significant genes in the nonzero members of that set were
the targeted transcripts themselves rather than coherent downstream programs.
Because a held-out `Mboat7` signature would not be able to contribute a
self-DEG as evidence for the requested count unless the assay happened to call
its transcript significant, this neighborhood supports an expected downstream
count at the lower boundary rather than a modest 5-20 DEG estimate.

External MBOAT7 biology raised the prior above an arbitrary lipid-enzyme null:
full loss is a real neuronal developmental lesion and directly perturbs a
nonredundant PI acyl-chain remodeling route. I did not transfer that full-loss
developmental phenotype as a broad DEG count, because the relevant causal
steps either precede the P16 intervention window, occur as membrane lipid and
neurite physiology without required nuclear-RNA propagation, or are strongest
in liver/adipose/microglia contexts that are not the recovered NeuN-positive
thalamic population. The stronger same-assay counterexamples, `Rab7`, `Vps54`,
`Vps35`, `Tsc2`, and `Srebf2`, are less specific to MBOAT7's limiting
LPI-to-AA-PI reaction and show that the assay can detect lysosomal or
cholesterol responses without implying that MBOAT7 should trigger them.

On balance I expect acute sparse `Mboat7` loss in `151 TH Prkcd Grin2c Glut`
neurons to resemble the buffered phosphoinositide/acyl-chain training nodes
more than the broad endolysosomal or mTOR/SREBP stress nodes. The point
estimate is therefore 0 genes passing FDR 0.05.

## Limits and uncertainty

- No MBOAT-family paralog and no direct PI-synthesis enzyme was represented in
  the visible focal training endpoint, so the closest calibration points are
  adjacent PI phosphatases, PI3K nodes, acyl-CoA/sphingolipid enzymes, and
  broader endomembrane-trafficking genes.
- The training distribution is zero-inflated. A prediction of 0 means "no gene
  crosses this assay-specific FDR threshold", not no lipidomic or synaptic
  effect.
- MBOAT7 has strong complete-loss brain biology, but those data are germline,
  embryonic, and lipidomic/developmental. The postnatal AAV CRISPR experiment
  samples surviving P37-P44 NeuN-positive nuclei and may miss early migration,
  neurite morphology, electrophysiology, microglial, or pure membrane-lipid
  consequences.
- The internal corpus reports and the parquet are same-experiment
  representations. Agreement between a report calling `Synj1`, `Pik3cb`,
  `Pik3r1`, `Pik3r2`, `Ocrl`, or `Abhd12` buffered and the focal DEG count is
  interpretation of the same PerturbAI screen, not replication.
