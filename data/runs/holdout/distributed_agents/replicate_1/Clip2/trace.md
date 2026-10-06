# Clip2 DEG-count prediction

## Question and endpoint

I interpreted the task as a scalar prediction for the held-out mouse perturbation
`Clip2` in exactly `151 TH Prkcd Grin2c Glut` neurons.  The endpoint is the
number of measured genes with `pvals_adj < 0.05` in the postnatal AAV-CRISPR
Perturb-seq Wilcoxon contrast against matched non-targeting controls.  I counted
the target transcript itself when it passes FDR, because the supplied
`n_degs` training endpoint is defined over all measured genes and the focal
Parquet count for examples such as `Dctn1`, `Mapre2`, and `Tuba1a` matches the
training CSV only when the perturbed gene is included.

The held-out `Clip2` signature and DEG count are absent by design: `Clip2` is
not in the 1,674-row focal training-count CSV, and a direct DuckDB count over
the declared differential-expression Parquet found zero rows with
`gene_target = 'Clip2'`.  The requested endpoint is therefore not directly
observed for the target.  The observed training `n_degs` values are direct
measurements for analog perturbations; biological function is an external prior
used to decide which analogs are relevant.

## Sources used

- Declared input table
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`,
  the focal direct `n_degs` endpoint for non-held-out perturbations.
- Declared input Parquet
  `training differential-expression dataset`,
  queried directly for focal and all-cell DEG counts and the leading focal
  significant genes for selected cytoskeletal comparators.
- The run-local dataset portrait, task bindings, compact coverage index, and
  measurement registry.  These established that the table is a differential
  expression summary over recovered nuclei, that the self-transcript fold
  change is not an editing-efficiency measure, and that the same-experiment
  corpus is a semantic layer rather than independent replication.
- The July 260713 Sourceguard v1 same-experiment Findings corpus, queried only
  for compact reports around observed analogs `Dctn1`, `Mapre2`, and `Tuba1a`.
- External PubMed-indexed literature: De Zeeuw et al. 1997
  PMID:9427243, DOI:10.1016/S0896-6273(00)80411-0; Hoogenraad et al. 2000
  PMID:10825300, DOI:10.1242/jcs.113.12.2285; Akhmanova et al. 2001
  PMID:11290329, DOI:10.1016/S0092-8674(01)00288-4; Hoogenraad et al. 2002
  PMID:12195424, DOI:10.1038/ng954; Lansbergen et al. 2004 PMID:15381688,
  DOI:10.1083/jcb.200402082; Komarova et al. 2005 PMID:16148041,
  DOI:10.1091/mbc.e05-07-0614; Peris et al. 2006 PMID:16954346,
  DOI:10.1083/jcb.200512058; Stepanova et al. 2010 PMID:20471267,
  DOI:10.1016/j.cub.2010.04.024.

## Quantitative calibration from the training perturbations

The focal training response is mostly silent: 1,205 of 1,674 training
perturbations have `n_degs = 0`; 469 are nonzero.  The largest responses are
housekeeping, splicing, proteasome, and chromatin regulators such as `Uba5`
with 2,677 DEGs, `Tpr` with 1,768, and `Sin3a` with 1,433.  A cytoskeletal
target therefore needs target-specific evidence before being assigned a broad
hundreds-of-genes response.

I queried the Parquet for represented microtubule, motor, dynactin, and
plus-end-adjacent perturbations using:

```sql
SELECT gene_target,
       COUNT(*) FILTER (WHERE group_name = '151 TH Prkcd Grin2c Glut') AS focal_rows,
       SUM(CASE WHEN group_name = '151 TH Prkcd Grin2c Glut'
                 AND pvals_adj < 0.05 THEN 1 ELSE 0 END) AS focal_degs,
       SUM(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS all_cell_degs,
       COUNT(DISTINCT group_name) AS cell_groups
FROM read_parquet(...)
WHERE gene_target IN (...)
GROUP BY gene_target;
```

Closest canonical `Clip2` paralogs or binding partners would have been `Clip1`,
`Clasp1`, `Clasp2`, `Mapre1`/EB1, `Mapre3`/EB3, `Ckap5`, and additional
dynactin subunits, but none of these were in the focal training-count table.
The informative represented perturbations were therefore:

| training target | focal n_degs | all-cell DEGs | expression-pattern evidence and relation to Clip2 |
| --- | ---: | ---: | --- |
| `Mapre2` | 1 | 1 | EB2 is a microtubule plus-end protein in the same +TIP network.  Its only focal FDR<0.05 gene was its own transcript, `Mapre2`, logFC -0.464, so acute EB-family plus-end perturbation was buffered at the nuclear-RNA level.  The July report further found no meaningful convergence with `Dctn1`, kinesin, tubulin, or other microtubule perturbations. |
| `Dctn1` | 75 | 382 | DCTN1/p150Glued has CAP-Gly microtubule-binding architecture related to CLIP proteins and is a core dynactin subunit.  It is a stronger, less redundant trafficking intervention than `Clip2`.  In 151 cells its top calls were sterol/lipid feedback genes up after knockout: `Insig1` logFC 1.16, `Msmo1` 1.10, `Hmgcs1` 0.86, `Cyp51` 0.74, `Hmgcr` 0.78, and `Fdft1` 1.14, with `Dctn1` itself down at -0.59.  The July report annotated this as an SREBF2-like lipid response rather than a generic cytoskeletal-injury program. |
| `Tuba1a` | 7 | 16 | A major neuronal alpha-tubulin; the 151 response consisted of `Tuba1a` down and compensatory tubulin transcripts up (`Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, `Tubb5`).  This is a narrow tubulin-dosage program, not a broad stress state. |
| `Kifbp`, `Kif1a`, `Kif5a`, `Kif5c` | 1 to 2 each | 2 to 11 | Axonal-transport kinesin or kinesin-associated genes were mostly self-only or nearly silent, consistent with the July `Dctn1` report's negative result that canonical kinesins did not phenocopy `Dctn1`. |
| `Dync2h1`, `Dync2i1`, `Map6`, `Kif1b` | 0 each | 0 to 2 | These are same-broad-system counterexamples: cytoskeletal or dynein/kinesin membership alone did not imply any focal DEG response. |

I also checked genes near `CLIP2` in the Williams-Beuren region when present in
the training endpoint.  They were small in 151 cells: `Limk1` 0, `Baz1b` 1,
`Gtf2ird1` 4, and `Gtf2i` 10.  These genes are not biochemical substitutes for
CLIP2, but the screen does not show that a Williams-region developmental gene
automatically causes a broad postnatal 151-cell transcriptional footprint.

## Biological interpretation for Clip2

`Clip2` encodes CLIP-115, a brain-enriched cytoplasmic linker protein with two
N-terminal CAP-Gly microtubule-binding domains and a coiled-coil region
(De Zeeuw et al. 1997; Hoogenraad et al. 2000).  CLIP-115/CLIP2 and the
paralog CLIP-170/CLIP1 track growing microtubule plus ends; EB proteins help
control CLIP localization at tips, and CLASPs bind CLIPs/EB1 to regulate
plus-end behavior at the cortex (Akhmanova et al. 2001; Lansbergen et al. 2004;
Komarova et al. 2005).  The same CAP-Gly plus-end network is modulated by
tubulin tyrosination and by p150Glued/DCTN1 recruitment (Peris et al. 2006).
In cultured neurons, CLIP-115 and CLIP-170 affect axonal microtubule growth
rate and growth distance (Stepanova et al. 2010), and germline `Cyln2`/`Clip2`
loss or haploinsufficiency in mice causes mild Williams-syndrome-like brain,
hippocampal, and motor phenotypes with redistribution of CLIP-170 and dynactin
at growing microtubule tips (Hoogenraad et al. 2002).

That biology supports a possible neuronal consequence, but the causal transfer
to this screen's endpoint is weak:

- Intervention: the experiment is sparse P16 CRISPR loss of function in
  postmitotic neurons, sampled 3 to 4 weeks later.
- Direct consequence: CLIP2 loss should alter microtubule plus-end binding and
  dynamics, but CLIP1 can occupy the same class of plus-end structure and the
  expected defect is cytoskeletal/transport-local rather than a transcription
  factor lesion.
- Propagation: a core dynactin lesion can propagate to endolysosomal and ER
  sterol feedback in the dataset, explaining the 75-DEG `Dctn1` 151 response.
  CLIP2 is upstream/peripheral to dynactin localization and lacks the obligate
  motor-adaptor role of DCTN1, so it is not expected to drive the same sterol
  program at the same amplitude.
- Exposure and selection: the assay only observes recovered NeuN+ nuclei; local
  dendritic or axonal transport defects can be invisible to nuclear snRNA-seq.
- Measured endpoint: the most direct plus-end comparator present, `Mapre2`, was
  self-only in this cell class; represented kinesins and tubulin-adjacent genes
  were also zero or one-digit responses.

The balance of evidence is therefore a tiny nonzero count.  I assigned
`Clip2 = 1`, expecting at most the on-target `Clip2` transcript, if expressed
and depleted enough, to cross FDR in the focal class and not expecting a
multi-gene downstream state.  This is driven mainly by the within-dataset
`Mapre2`, kinesin, tubulin, and `Dctn1` calibration; external CLIP2 literature
constrains the analog choice and keeps `Dctn1` as an upper-bound
counterexample rather than a direct phenocopy.

## Limits

The closest paralog `Clip1`, the CLASP partners, EB1/EB3, `Ckap5`, and most
dynactin subunits were held out or absent from the training data, so there was
no direct CLIP2-family Perturb-seq analog.  `Mapre2` is a neighboring plus-end
protein, not an obligate CLIP2 partner; `Dctn1` shares the microtubule-plus-end
transport axis but is a core motor-adaptor complex member with a distinct
sterol-response signature.  Published CLIP2 phenotypes are largely germline,
developmental, heterozygous, or in vitro, whereas this readout is sparse acute
postnatal mouse CRISPR in survivor-conditioned thalamic glutamatergic nuclei.
Consequently the point estimate should be read as a low-count extrapolation,
not as evidence that CLIP2 is biologically inert.
