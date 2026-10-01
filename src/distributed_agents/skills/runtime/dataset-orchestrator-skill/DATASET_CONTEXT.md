<!-- DISTRIBUTED_AGENTS_DATASET_CONTEXT:perturbai-atlas-v5 -->
# PerturbAI atlas dataset portrait

This is a reusable, model-independent context selected at runtime for tasks over
the PerturbAI whole-brain atlas or a declared derivative. It supplies shared
identity, design, schema, vocabulary, and calibration once. The exact task
remains authoritative. Task-specific differences belong in the task profile and
plan, not in this portrait.

## Identity and representations

- The differential-expression Parquets, full reports, canonical report text,
  Findings, Claims, Evidence, References, Literature Comparisons, and findings
  ledger are derived representations of the same perturbation experiment.
- Agreement between these internal surfaces is not cross-dataset replication.
  The Parquet is authoritative for exact numerical effects; the corpus is the
  pre-interpreted, literature-grounded semantic layer over those measurements.
- External databases, screens, literature, and ontologies are priors or
  definitions, not measurements from this experiment.

The selected semantic corpus is a separately versioned snapshot of this
experiment. Read its release manifest for exact report, target, Finding,
Evidence, Reference, Claim, and graph coverage; do not reuse counts or graph
capabilities from another release. Corpus coverage may be a strict subset of
the raw dataset universe. The graph, when the selected release exposes one, is
a structured view of that release's ledger rather than independent evidence.

Native alignment does not guarantee one explicit record for every requested
unit. Missing retrieval or an unannotated pair is not automatically no
literature, no transcriptional response, or a biological null. Reuse packaged
grounding first; retrieve fresh external evidence only for an explicit gap,
conflict, unresolved reference, or cutoff-sensitive claim.

## Frozen scale and candidate universe

- The genome-scale table contains approximately 745.8 million rows.
- It covers 2,046 perturbation labels, 23 broad neuronal classes, and 17,994
  measured genes.
- The screen-wide inventory contains 1,946 biological targets and 100
  `Safe_target_*` controls. It is the candidate universe unless the task
  explicitly narrows it.
- `Non_target` is a matched control label, not a biological knockout target.
- Eligibility is defined by the inventory, not by DE presence in one cell
  class. Quiet or missing survivor DE changes uncertainty, not eligibility.

## Experimental design

- Species/strain: mouse, C57BL/6J × Cas9 transgenic, mixed sexes.
- Four guides per target were delivered by retro-orbital AAV-PHP.eB at
  postnatal day 16.
- The perturbation is acute, sparse, mosaic CRISPR-Cas9 loss of function in
  postmitotic postnatal neurons, not germline/embryonic knockout or
  pharmacological inhibition.
- Harvest was at postnatal day 37–44, approximately 3–4 weeks after delivery.
- Tissue is whole brain excluding olfactory bulb and hindbrain. NeuN-positive
  neuronal nuclei were enriched by FACS, so glial, vascular, and immune
  populations are absent or under-sampled.
- The assay is 10x Flex V2 single-nucleus RNA-seq. It observes nuclear RNA in
  nuclei that survived, were recovered, and retained a class assignment.
- Average observed target-mRNA reduction is approximately 18% per guide.
  Functional CRISPR disruption often does not reduce measured nuclear target
  transcript: only a subset of knockout alleles are visible through
  nonsense-mediated decay, and the readout is further affected by mosaic
  editing and survivor-conditioned sampling. Dataset-wide, measured
  self-knockdown is uncorrelated with downstream transcriptional effect.
  Therefore self-target log-fold change is not a quantitative measure of
  editing efficiency, functional knockout strength, or biological effect.
  Weak or unchanged target transcript neither implies assay failure nor rules
  out effective target engagement; strong transcript loss does not imply a
  stronger functional knockout or larger effect. Do not use self-target
  transcript loss to filter, promote, demote, or weight candidates for a
  biological endpoint; it is limited QC context only.

## Parquet semantics and variants

Each row is one measured-gene × cell-class × perturbation result:

- `names`: measured mouse gene symbol;
- `group_name`: Allen-taxonomy-derived neuronal class;
- `gene_target`: perturbed target and usual ranking unit;
- `logfoldchanges`: perturbed versus matched non-targeting control, with
  positive values indicating higher expression after perturbation;
- `pvals`, `pvals_adj`: Wilcoxon raw and BH-adjusted p-values;
- `scores`: signed Wilcoxon ranking statistic;
- `control_label`: matched control group when present; and
- `n_pert_matched`, `n_ctrl_matched`: recovered matched-nucleus counts present
  only in the full-count variant.

The no-counts variant omits the matched-nucleus columns. The full-count variant
includes them. Neither contains raw per-nucleus UMI counts. Matched recovered
nuclei are not guide-exposure denominators or a direct abundance endpoint.
Library-size normalization makes DE compositional, so absolute RNA content
cannot be read from a mean log-fold change.

## Power, selection, and statistical calibration

- The transcriptional response is sparse rather than approximately complete.
  At BH FDR < 0.10, 43.9% of the 1,946 biological targets have no significant
  measured gene in any assayed cell class, and 90.2% of measured biological
  target × cell-class pairs have no significant gene. After excluding the
  self-target transcript, 54.1% of targets and 94.5% of measured target ×
  cell-class pairs have no significant downstream gene. These rates describe
  measured pairs; an unmeasured pair remains missing evidence rather than a
  zero.
- DE yield is strongly concentrated in `151 TH Prkcd Grin2c Glut` and
  `155 MB Glut`; their visibility partly reflects power and perturbed-cell
  recovery.
- An effect seen in either high-yield class is not automatically anatomically
  specific. Absence elsewhere supports selectivity only after accounting for
  matched power, target engagement, baseline expression, and comparable effect
  direction.
- Safe-target controls have a median of zero FDR-significant genes, while
  biological targets have a highly skewed DEG burden. DEG burden is a response
  strength/QC feature, not a universal proxy for another endpoint.
- DE remains primary evidence for tasks that directly ask about a
  transcriptional response. For a different or unobserved endpoint, DEG
  presence, burden, magnitude, or direction may describe the recovered-cell
  state or focus interpretation, but must not by themselves filter, promote,
  demote, or weight candidates. A declared, validated link to the requested
  endpoint is required before DE can be used as its quantitative surrogate.
- Broad averages over low-expression genes can be dominated by pseudocount and
  compositional behavior. Directional or module statistics require
  task-specific controls and falsification.
- Measurements are survivor-conditioned. Severe selection can leave a quiet
  recovered signature; a large survivor-state signature does not by itself
  establish death, abundance change, or increased absolute RNA.
- FDR support for one target, readout, or population cannot be transferred to
  every member of a multi-target Claim or story.
- Large footprints, famous targets, and recurrence in high-yield groups
  increase visibility, not necessarily novelty or priority.

## Dataset-local vocabulary

Atlas labels combine a numeric class identifier, anatomical abbreviations,
marker genes, and a neurotransmitter suffix.

For `151 TH Prkcd Grin2c Glut`:

- `151` is a class identifier, not a nucleus count;
- `TH` means thalamus, not tyrosine hydroxylase;
- `Prkcd` and `Grin2c` are marker-gene symbols; and
- `Glut` denotes a glutamatergic neuronal class.

Thus the label denotes thalamic glutamatergic neurons. `Dopa` explicitly marks
dopaminergic classes elsewhere. Never expand an unresolved dataset token from
generic biomedical memory.

## Interpretation and ranking guards

- Target-transcript loss alone does not establish a downstream mechanism; lack
  of target-transcript loss alone does not prove failed editing.
- Treat nulls as boundaries or uncertainty according to endpoint and power,
  never automatically as safety or positive mechanism.
- Describe power-confounded scope as observed restriction, not intrinsic
  cell-type specificity.
- When the task requests Novelty, Support, and Priority, score them
  independently using the user's definitions. Support 5 requires compelling
  target-specific evidence and treatment of major alternatives. Priority 5 is
  exceptional and should plausibly reshape an agenda if validated.
- A research-community section should explain what model would change, what
  question becomes tractable, and what experimental program follows rather than
  restating genes and generic assays.
