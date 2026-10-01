Task: produce an integrated, findings-centered perturbation report for a single
target that covers both its positive biology and why its null/weak results are null, grounded in how this specific dataset was generated.

Target perturbation:
`{gene_target}`

You are an expert perturbation biologist analyzing one target in a mouse-brain
Perturb-seq screen. Your goal is to produce an integrated scientific report and
structured ledgers that preserve the biological interpretation, dataset evidence,
and literature grounding — for the responders and for the nulls, which are the
majority of this dataset.

Dataset context:
- The parquet at `{parquet_path}` is the FULL screen — ALL ~2046 target perturbations × 23 cell groups
  (whole-transcriptome Wilcoxon DE per target × cell group), NOT a single-target slice. Filter for
  `{gene_target}` to get its own response; every OTHER target's DE surface is in the same parquet and is
  directly queryable, which is what makes the cross-perturbation comparison in the analysis procedure
  (steps 1-3) possible.
- The full dataset taxonomy is 23 cell groups: `001 L5-6 IT Glut`, `005 L4-5 IT CTX Glut`,
  `007 L2-3 IT CTX Glut`, `008 L2-3 IT ENT PPP RSP Glut`, `009 L2-3 IT PIR AON ENT Glut`,
  `012 MEA LA CA1 DG Glut`, `017 CA3 CA2-FC DG Glut`, `022 L5 ET CTX Glut`,
  `027 NP-CT-L6b-OB Glut`, `046 CTX-CGE GABA`, `052 Pvalb Gaba`, `053 Sst Gaba`,
  `054 CNU-MGE GABA`, `059 CNU-LGE LSX GABA`, `066 CNU-HYa HY GABA`, `110 CNU-HYa HY MM Glut`,
  `145 MH-LH TH Glut`, `151 TH Prkcd Grin2c Glut`, `155 MB Glut`, `191 MB P MY GABA`,
  `215 MB Dopa`, `217 P MY Pineal Glut`, `308 CB GABA`. A cell group with no `{gene_target}` rows
  was not measured/recovered for this target, not a biological zero.

Experimental context (how this dataset was generated — ground every interpretation in it):
- Species/strain: mouse, C57BL/6J × Cas9 transgenic, mixed sexes.
- Timing: AAV-PHP.eB delivered retro-orbitally at post-natal day 16 (P16); brains harvested
  P37-44 (3-4 weeks post-perturbation). Postmitotic, juvenile-to-young-adult brain — NOT
  embryonic, NOT aged. The gene is removed only AFTER cortical neurons are specified and postmitotic.
- Modality: acute, mosaic, sparse CRISPR-Cas9 loss-of-function via pooled gRNAs (4/gene). NOT
  germline KO, NOT conditional Cre-lox, NOT siRNA/shRNA, NOT pharmacological. Average on-target
  knockdown is only ~18% per gRNA at the mRNA level — so weak/flat on-target transcript is the
  EXPECTED norm, not evidence of assay failure. A functional knockout via indels can leave the
  transcript intact or up-regulated; low target engagement alone is at most a caveat — do NOT use
  it by itself to call a null technical or biologically silent, and do NOT read "the target's own
  transcript did not drop" as "the perturbation did not work". True engagement is unmeasured here
  (it needs DNA indel-seq, not available); the modest self-drop neither confirms nor excludes an
  active knockout.
- Tissue scope: whole brain minus olfactory bulb and hindbrain; NeuN+ neuronal nuclei FACS-enriched.
  Non-neuronal types (astrocytes, microglia, oligodendrocytes, vascular) are largely absent/under-sampled.
- Readout: snRNA-seq (10x Flex V2). DEGs by Wilcoxon rank-sum (Scanpy `rank_genes_groups`) at the
  single-nucleus level vs pooled non-targeting controls, Benjamini-Hochberg corrected.
- Direction: `logfoldchanges` = perturbed vs non-targeting control (positive = up in perturbation).
- Perturbation timing (P16, postmitotic) is ONE fact among several to weigh per gene. Whether a null
  reflects timing, expression level, redundancy, survivorship, buffering, readout modality, or a
  genuine no-effect must be derived from THIS gene's own biology and the dataset evidence — do not
  assume any particular cause by default.

A biological finding is a dataset-grounded claim that changes biological
interpretation. It may be a strong positive result, a contradiction, a
convergence, a negative result, a buffered response, a cell-type restriction, a
literature refinement, a therapeutic direction warning, or a biomarker
hypothesis. Do not limit findings to pathways or cell types.

Analysis procedure (work in this order; it is a BOUNDED cycle — one return to the data
after literature, not open-ended iteration):

1. PHENOTYPE FIRST — characterize the response before consulting priors, so the data nominates what matters.
   - Inspect the parquet directly for `{gene_target}`. Quantify on-target perturbation where
     the target transcript is measured — read a flat/weak self-transcript through the ~18% /
     LoF-indel lens above, not as failed KO.
   - Enumerate the full response surface across cell groups: perturbed-cell count, on-target
     logFC/FDR, and the number of downstream genes at FDR<0.10 per group. Mark each measured
     group as `effect` (>=1 downstream FDR<0.10), `weak` (only nominal / sub-threshold), or
     `null` (0 downstream FDR<0.10); mark groups with no rows as `not_tested_missing`.
   - Identify cell-type-specific effects, strongest genes, negative or buffered responses,
     and caveats such as low cell count.
   - Compute data-driven comparators: the top positive and top negative signature neighbors of
     `{gene_target}` across the screen (targets whose DE profile most converges with / diverges
     from this one). Record these before literature — they are often not the textbook-obvious
     relatives.

2. LITERATURE — now consult priors, to name expectations against the observed surface.
   - Identify known target function, complexes, pathway membership, paralog family, disease
     links, druggability, and expected directionality — and the downstream program(s) and genes the
     literature would predict after loss of function, so you can ask whether this assay
     recovered them.
   - From this, NAME the literature-obvious comparators to test: same-complex members,
     paralogs, receptor subunits, pathway neighbors, disease-family members. Many are
     perturbation targets in this screen and therefore directly measurable.
   - Pay special attention to whether prior literature implies similarity, interchangeability,
     cell-type specificity, or a particular direction of effect.
   - Prefer PubMed, PubMed Central, OpenAlex, review articles, authoritative biological
     databases, and accessible abstracts. Do not keep retrying blocked, paywalled,
     robots-denied, or reCAPTCHA pages. Do not invent references.

3. RETURN TO THE DATA — measure the comparators and programs you now know to look for (this is
   the one cycle-back; do it once, thoroughly).
   - For EVERY comparator that is a target in the screen — both the data-driven neighbors from
     step 1 AND the literature-obvious relatives from step 2 — query its DE surface in the
     matched cell groups and KEEP or REJECT it with measured statistics: convergence
     (shared-direction DE overlap, for responders) or divergence (a related target that DOES
     respond where `{gene_target}` is flat, or vice versa). Do not name a measurable comparator
     you did not measure; a literature relative that turns out NOT to converge is an
     informative, first-class result ("the expected paralog does not phenocopy in this assay"),
     not an omission.
   - Test the EXPECTED-BUT-ABSENT programs from step 2: for each program the literature predicts
     after loss of function, state whether the measured DE surface recovers it, and if not,
     whether the assay would have detected it (this feeds the null gate in step 5).
   - Cross-perturbation convergence/divergence — especially among same-complex or same-pathway
     members — is first-class, load-bearing biology here; a report that never measures the
     target against related perturbations is incomplete.

4. INTEGRATE phenotype, literature, and cross-perturbation into POSITIVE findings.
   - Ask what is surprising, confirming, contradictory, refining, or clinically directional.
   - Moderate-confidence findings are allowed if they are biologically high-value — INCLUDING a
     clinically or biologically important result that carries only a weak conventional signal —
     but label the confidence and limitation clearly.
   - Do not invent references, evidence, genes, statistics, or mechanistic links. Omit claims
     that cannot be grounded.
   - COVERAGE TRACKS THE MEASURED DE SURFACE (do not stop at the target's textbook function).
     For each cell group that has real downstream signal (FDR<0.10 genes), read the actual
     significant DE genes and identify the DISTINCT biological programs they represent — not
     only the target's canonical role, but the SECONDARY / compensatory / stress programs the
     data show: e.g. proteostasis or proteasome-bounce-back, integrated stress response,
     unfolded-protein response, autophagy / lysosomal, redox, translation, and synaptic /
     neuronal down-regulation. Interpret each program you find in the context of the experiment, ground it in the specific
     measured genes, and name the cell group(s) where it fires and its direction. The number
     of programs you interpret must track what the DE surface actually contains: a target with
     thousands of DEGs across many groups supports many more than three programs; do NOT
     collapse a broad, cell-type-varied response into a single canonical story plus three
     pathways. This is emphatically NOT a quota — do not manufacture programs to hit a number;
     interpret every distinct program the measured genes genuinely support, and no more.

5. Explain the NULL / weak surface (this is a required deliverable, not a caveat).
   For every measured cell group that is `null` or `weak`, decide WHY — reasoning FROM the
   expected effect (step 2) and whether this assay would detect it (step 3) to the observed
   non-result: given what this gene does, we expected X; why didn't X appear here? Prioritize
   non-trivial, gene-specific explanations.
   - Assign a concise `null_cause` label naming the real mechanism (OPEN vocabulary, not a
     fixed menu): e.g. `developmental_window_mismatch`, `essentiality_survivorship`,
     `cell_type_or_lineage_mismatch`, `not_expressed`, `variant_effect_not_phenocopied_by_LoF`,
     `paralog_or_family_redundancy`, `readout_mismatch_for_the_phenotype_class`, or `other` +
     narrative. GATE `readout_mismatch`: if loss of this gene would be expected to trigger a
     SECONDARY transcriptional program (stress / autophagy / UPR-ISR / compensation) that this
     assay WOULD detect, and that program is absent, the null is INFORMATIVE — readout-mismatch
     is not justified. TRIVIAL explanations (`dosage_insufficient`, `low_power`) apply to any
     perturbation and carry no gene-specific information; do NOT lead with them — the assay does
     not titrate dose (fixed ~18%), so weak self-transcript is expected, not a distinct mechanism.
     If the priors genuinely do not predict a strong effect here, say so plainly (`genuine_null`).
   - Assign `trust` — reliability of this null as evidence the gene is biologically INERT here:
     `effect` (a real response exists) | `weak_evidence_for_null` (a defensible, context-robust
     null) | `untrustworthy_null` (would likely flip under different timing/context/stronger
     perturbation).
   - Tag `displacement` — a CLOSED, multi-label axis naming WHERE the real effect lives, off the
     transcriptomic axis (do NOT invent values): `earlier_stage`, `unsampled_lineage`,
     `non_transcriptional_modality` (only if the readout gate above is satisfied),
     `viability_abundance` (requires neuronal survival-dependence over 3-4 wk + a survivor-biased
     pattern), `requires_stronger_perturbation` (a gene-specific threshold argument, NOT generic
     low-power), `combinatorial`, `specific_allele`, `genuine_negative` (TERMINAL; mutually
     exclusive with all others). Invariants: `trust=untrustworthy_null` ⟺ ≥1 axis other than
     `genuine_negative`; `trust=effect` → `displacement` empty; `genuine_negative` pairs with
     `weak_evidence_for_null`.
   - Coverage is mandatory: every `null`/`weak` measured group must be covered by exactly one
     null-cause finding (group cells sharing one cause into one finding, listing them in
     `cell_types`). Treat `weak`/nominal results with MORE skepticism than nulls.
   - NULL DISCIPLINE IS UNCHANGED: the DE-surface coverage expansion in step 3 applies ONLY to
     groups with real FDR<0.10 signal. Do NOT expand coverage into null/weak groups by mining
     nominal sub-threshold genes into programs — that is the over-claiming failure mode. In null
     groups, the deliverable remains the CAUSE of the null (trust / displacement), not a
     manufactured program. Coverage is proportional to MEASURED FDR<0.10 signal, not to effort.

6. Write the narrative report, then produce structured ledgers.
   - Keep direct observations, computations, and literature-grounded interpretation distinguishable.
   - Label each positive finding with a stable id like `[F001]`, each null-cause finding like
     `[N001]`; cite dataset evidence inline as `[E001]` and references as `[R001]`.
   - Evidence rows are atomic measured dataset facts. Reference rows are source facts. Biological
     finding rows are interpretive claims grounded in evidence and, when relevant, references;
     literature comparison is captured inline on each finding via `literature_claim` and the
     `lit_direction` / `lit_context` / `lit_novelty` flags. Pathway and cell-type rows are derived views over
     existing finding ids.

Output:
Return a Markdown scientific report with inline `[F###]`, `[N###]`, `[E###]`, and `[R###]`
citations, followed by a structured appendix.

Scientific report sections:

1. `Key Biological Findings`
2. `Direct Dataset Observations`
3. `Literature Context`
4. `Integrated Interpretation`
5. `Null and Weak Results` (why each non-result is a non-result; trust + displacement)
6. `Caveats`
7. `References`

Positive finding types (for `finding_type` on Biological Findings rows):
`cell_type_selectivity`, `cross_perturbation_contrast`, `convergent_module`,
`buffered_response`, `homeostatic_compensation`, `literature_direction_mismatch`,
`disease_mechanism_refinement`, `therapeutic_direction_warning`, `biomarker_candidate`,
`negative_result`, `pathway_uncoupling`, `other`.

Structured Appendix:

After the Markdown report, append a section titled `Structured Appendix` with exactly
SIX fenced JSONL blocks with these headings, in this exact order:

1. `Evidence JSONL`
2. `References JSONL`
3. `Biological Findings JSONL`
4. `Null-Cause Findings JSONL`
5. `Pathways JSONL`
6. `Cell Type Specificity JSONL`

Each JSONL block must contain one valid JSON object per line. Do not wrap the JSON objects
in an array. Use `null` rather than an empty string for unknown values. Reuse `finding_id`,
`ref_id`, and `evidence_id` consistently across the entire report.

Grounding rules:
- Every `Biological Findings` and `Null-Cause Findings` row must cite at least one `evidence_id`.
- Every literature-based claim must cite at least one `ref_id`.
- Every pathway row and cell-type row must cite only finding ids that actually appear in the
  findings blocks; they may summarize/group/reformat existing findings but must not introduce new
  genes, mechanisms, comparators, references, or interpretations absent from the cited findings.
- If a claim is nominal, weak, exploratory, restricted-signature-based, or hypothesis-generating,
  make that explicit in the prose and structured fields.
- Do not invent evidence to satisfy a schema. Omit unsupported rows; mark missing evidence as
  `not_tested_missing`.

`Evidence JSONL` schema (exactly these fields):
- `evidence_id`: string
- `evidence_slug`: string
- `cell_type`: string | null
- `genes`: list[string] | null
- `statistics`: string   (compact numeric support: n_pert, on-target logFC/FDR, #downstream FDR<0.10, logFC, recurrence, rank)
- `description`: string
Evidence must be derived from the dataset, not the literature. Keep rows atomic.

Example:
```jsonl
{"evidence_id":"E001","evidence_slug":"example_target_cell_a_signature","cell_type":"999 Example Cell Class","genes":["ExampleGene1","ExampleGene2"],"statistics":"42 perturbed cells versus 4200 controls; ExampleGene1 logFC 1.20 FDR 0.008; ExampleGene2 logFC -0.70 FDR 0.031.","description":"Measured response illustrating the expected evidence-row shape."}
```

`References JSONL` schema (exactly these fields):
- `ref_id`, `ref_slug`, `source`, `source_type` (`pubmed`|`pmc`|`openalex`|`review`|`database`|`clinicaltrials`|`other`), `citation`, `url`, `description`

Example:
```jsonl
{"ref_id":"R001","ref_slug":"example_review_2025_complex","source":"Example Review Journal","source_type":"review","citation":"Doe J. Example complex biology for prompt examples. Example Review Journal. 2025.","url":"https://example.org/example-review","description":"Example source showing how to describe literature context."}
```

`Biological Findings JSONL` schema (exactly these fields):
- `finding_id`, `finding_type`, `summary`, `why_it_matters`, `cell_types` (list|null),
  `genes` (list|null), `comparators` (list|null), `direction` (str|null),
  `confidence` (`high`|`moderate`|`low`|`exploratory`), `evidence_ids` (list),
  `ref_ids` (list), `literature_claim` (str|null), `lit_direction` (str|null),
  `lit_context` (list|null), `lit_novelty` (str|null), `main_caveats` (str)
- Findings are the first-class positive interpretation layer. Emit as many findings as the
  measured DE surface genuinely supports (see the coverage rule in analysis step 3): a null
  or weak target may support only one or two, while a broad multi-program responder supports
  many. Do NOT cap the count for brevity, and do NOT pad it — the count is set by the biology
  present, not by a target number. Include high-value moderate-confidence findings when
  biologically important (especially unexpected convergence/divergence among related
  perturbations), but mark confidence honestly.
- Literature comparison is carried INLINE on each finding via four fields (there is no separate
  comparisons block). State it on any finding that touches prior knowledge; leave the flags `null`
  only when there is genuinely no literature to compare. The three flag axes are ORTHOGONAL — do
  not collapse them into one another.
  - `literature_claim` (str|null): the prior-knowledge claim being compared against, in one line.
  - `lit_direction` (str|null): the DIRECTION verdict ONLY, independent of context —
    `agree` (data matches the literature's direction of effect), `disagree` (opposite or
    substantively different), `ambiguous` (literature exists but yields no directional verdict for
    the observed phenotype), `no_literature` (no claim to test against). Do NOT down-grade
    `agree`/`disagree` just because the context differs — that is exactly what `lit_context` records.
  - `lit_context` (list|null): which dimension(s) separate the data from the cited literature;
    `[]` when fully matched. Values: `species`, `cell_type`, `stage`, `modality` (KO/KD/drug,
    bulk vs snRNA), `indirect` (pathway/family-level literature, not this gene). 
  - `lit_novelty` (str|null): what this finding CONTRIBUTES relative to the record —
    `known` (confirms an established result), `new_context` (known biology, first shown in this
    cell type / stage / system), `refinement` (sharpens or qualifies a known claim),
    `gap_filling` (first evidence on an understudied gene/relationship), `novel` (a genuinely new
    mechanistic or relational claim). Novelty is independent of direction: a finding can `agree`
    yet be `new_context`, or `disagree` yet be `known`.

Example:
```jsonl
{"finding_id":"F001","finding_type":"cross_perturbation_contrast","summary":"ExampleTargetA and ExampleTargetB show opposing signatures in 999 Example Cell Class despite belonging to the same protein assembly.","why_it_matters":"Preserves an unexpected related-target divergence as a first-class finding rather than burying it in pathway rows.","cell_types":["999 Example Cell Class"],"genes":["ExampleGene1","ExampleGene2","ExampleGene3"],"comparators":["ExampleTargetB"],"direction":"opposing","confidence":"moderate","evidence_ids":["E001","E002"],"ref_ids":["R001"],"literature_claim":"A reference describes ExampleTargetA and ExampleTargetB as members of one assembly with overlapping, redundant roles.","lit_direction":"disagree","lit_context":["cell_type","modality"],"lit_novelty":"novel","main_caveats":"Restricted-signature comparison; transcriptomic support only."}
```

`Null-Cause Findings JSONL` schema (extends a finding row with null-specific fields):
- `finding_id`, `finding_type` (always `null_cause`), `null_cause` (open-vocabulary mechanism),
  `trust` (`effect`|`weak_evidence_for_null`|`untrustworthy_null`),
  `displacement` (list of `{"axis": <closed set>, "confidence": <high|moderate|low|exploratory>}`;
  `[]` when `trust=effect`; a single `genuine_negative` entry for terminal nulls),
  `summary`, `why_it_matters`, `cell_types` (list|null), `genes` (list|null),
  `comparators` (list|null), `direction` (str|null), `confidence`, `evidence_ids` (list, >=1),
  `ref_ids` (list, >=1 for any literature claim), `literature_claim` (str|null),
  `lit_direction` (str|null), `lit_context` (list|null), `lit_novelty` (str|null), `main_caveats`

Example:
```jsonl
{"finding_id":"N001","finding_type":"null_cause","null_cause":"developmental_window_mismatch","trust":"untrustworthy_null","displacement":[{"axis":"earlier_stage","confidence":"high"}],"summary":"ExampleTarget showed 0 downstream genes at FDR<0.10 in 999 Example Cell Class, with ~60 perturbed cells and a flat self-transcript (logFC -0.13, FDR 1.0).","why_it_matters":"The flat self-transcript is expected under ~18% LoF knockdown and is not evidence of a failed KO; this gene's canonical program runs during embryonic fate specification, before the P16 perturbation, so the postnatal zero reflects timing, not biological absence — an earlier-stage perturbation could reveal an effect.","cell_types":["999 Example Cell Class"],"genes":["ExampleTarget"],"comparators":null,"direction":"no_robust_direction","confidence":"moderate","evidence_ids":["E001"],"ref_ids":["R001"],"literature_claim":"The gene's canonical program is described in the literature as running during embryonic fate specification.","lit_direction":"ambiguous","lit_context":["stage"],"lit_novelty":"new_context","main_caveats":"Engagement is unmeasured at the DNA level; timing attribution is inferential, grounded in the gene's known developmental role."}
```

`Pathways JSONL` schema (exactly these fields):
- `pathway` (str|null), `finding_ids` (list), `cell_type` (list|null), `genes` (list|null),
  `direction` (str|null), `evidence_ids` (list)
- Derived view over the findings blocks. Include only pathways supported by cited findings. If
  direction is mixed/opposing across comparators, state that compactly rather than forcing up/down.

Example:
```jsonl
{"pathway":"example adaptive signaling","finding_ids":["F001"],"cell_type":["999 Example Cell Class"],"genes":["ExampleGene1","ExampleGene2"],"direction":"opposing_across_comparators","evidence_ids":["E001","E002"]}
```

`Cell Type Specificity JSONL` schema (exactly these fields):
- `cell_type` (str), `finding_ids` (list), `summary` (str), `evidence_ids` (list), `ref_ids` (list)
- Derived view. One line per substantively-discussed cell type; summarize which findings involve it
  and why it matters. Do not add a literature comparison here; literature comparison lives on the
  finding rows (`literature_claim` / `lit_direction` / `lit_context` / `lit_novelty`).

Example:
```jsonl
{"cell_type":"999 Example Cell Class","finding_ids":["F001"],"summary":"Cell class where the related-target contrast is concentrated.","evidence_ids":["E001","E002"],"ref_ids":["R001"]}
```

Output shape requirements:
- Return the Markdown scientific report first (including the `Null and Weak Results` section),
  then append the `Structured Appendix`.
- Structured-row count is set by the measured signal, not by brevity: keep every row that is
  grounded in real FDR<0.10 DE (on responders) or that explains a null (trust/displacement).
  Omit only rows built on sub-threshold nominal genes or ungrounded speculation.
- Do not return pure JSON without the prose report. Do not omit the report content just because a
  structured appendix is present.
