# Held-out DEG-count prediction for `Cep83`

## Question and resolved ambiguity

The requested held-out readout is the number of measured genes with
`pvals_adj < 0.05` after `Cep83` perturbation in the focal
`151 TH Prkcd Grin2c Glut` thalamic glutamatergic cell group.  `Cep83`
was absent from both the parquet of non-held-out differential-expression
surfaces and the focal-cell training-count CSV, so I treated every exact
`Cep83` count as unknown and transferred only from non-held-out training
perturbations plus external biology.

I interpreted a count of 1 as positive only if any measured gene passed
the same BH FDR 0.05 threshold in the focal cell group.  Training singletons
that are just the perturbed transcript itself, such as the on-target `Arl3`
and `Ttc8` hits below, were therefore kept as evidence about the numerical
endpoint but not as a broad downstream ciliary RNA program.

## Sources used

- Training count endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested target manifest:
  `[local file: 036_Cep83.csv]`
- PerturbAI same-experiment Distributed Agents corpus:
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents curated gene-annotation and analog-nomination layers:
  GO, Reactome, CORUM v5.0 projected from human complexes through MGI
  one-to-one homology classes downloaded 2026-09-13, and STRING physical
  v12.0
- External mechanism literature from PubMed:
  Tanos et al. 2013, *Genes & Development*, PMID 23348840; Joo et al. 2013,
  *PNAS*, doi:10.1073/pnas.1220927110, PMID 23530209; Failler et al. 2014,
  *American Journal of Human Genetics*, doi:10.1016/j.ajhg.2014.05.002,
  PMID 24882706

## Computation over the training data

The focal training distribution is highly concentrated at zero: 1205 of
1674 training perturbations are zero in `151 TH Prkcd Grin2c Glut`, 363
are weak with 1-9 DEGs, 63 have 10-89 DEGs, and 43 have at least 100 DEGs.
The 75th percentile is only 1 DEG, so a positive prediction for a held-out
gene needs target-specific support.

I nominated mechanistic analogs for held-out `Cep83` against the exact
1674-gene training universe rather than by symbol matching.  The strongest
available exact-complex analogs were `Sclt1` and `Cep290`: their human
orthologs share CORUM complex 8470, `Distal appendage`, with CEP83.  The
same nomination run put `Ift88`, `Ift81`, `Ift43`, `Kif3b`, `Dync2h1`,
`Dync2i1`, `Bbs5`, `Cplane1`, `B9d1`, `Ttc21b`, `Dzip1`, and `Pibf1` in
the nearby cilium assembly, basal-body anchoring, and transition-fiber
neighborhood through Reactome/GO memberships plus same-experiment graph
support.

For those nominated analogs I re-opened the DE parquet with a PyArrow
filter:

```python
f = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
)
n_degs = (rows_for_target.pvals_adj < 0.05).sum()
```

This recomputation used the focal adjusted p-values directly rather than
only the precomputed count CSV.  The focal evidence for the biologically
closest analogs was:

| training perturbation | relation to CEP83 | focal `n_degs` | best focal `pvals_adj` | matched perturbed nuclei |
| --- | --- | ---: | ---: | ---: |
| `Sclt1` | distal-appendage member; ciliary transition fiber | 0 | 1.000 | 122 |
| `Cep290` | distal-appendage CORUM member and transition-zone ciliary disease gene | 0 | 0.650 | 99 |
| `Dzip1` | basal-body/cilium-assembly neighbor | 0 | 1.000 | 141 |
| `Pibf1` | centrosome/cilium-assembly neighbor | 0 | 1.000 | 123 |
| `Ift88` | IFT-B, cilium elongation/maintenance | 0 | 1.000 | 143 |
| `Ift81` | IFT-B | 0 | 0.391 | 152 |
| `Ift43` | IFT-A | 0 | 0.847 | 328 |
| `Kif3b` | anterograde kinesin-II IFT motor | 0 | 1.000 | 156 |
| `Dync2h1` | retrograde dynein-2 | 0 | 0.348 | 98 |
| `Dync2i1` | retrograde dynein-2 | 0 | 1.000 | 229 |
| `Bbs5` | BBSome/ciliary trafficking | 0 | 0.220 | 121 |
| `Cplane1` | ciliogenesis and PCP-related CPLANE complex | 0 | 1.000 | 179 |
| `B9d1` | MKS transition-zone module | 0 | 1.000 | 180 |
| `Cep120` | centriole/ciliary assembly comparator | 0 | 1.000 | 184 |
| `Ttc21b` | IFT-A | 0 | 0.459 | 131 |

The only near-neighborhood focal positives were not persuasive models for
`Cep83`: `Arl3` and `Ttc8` each had exactly one focal DEG, and in both cases
that gene was the perturbed transcript itself; the broader DCTN/tubulin
perturbations such as `Dctn1` and `Tuba1a` are cytoskeletal transport
counterexamples from much broader annotation terms, not distal-appendage or
basal-body docking phenocopies.

I also compared focal log2-fold-change profiles for ciliary anchors with
`profile_neighbors`.  For the structural cilium set
`Cep290`, `Ift88`, `Kif3b`, `Bbs5`, `Rpgrip1l`, `Sclt1`, `Dync2h1`,
`Dync2i1`, `Ift43`, `Ift81`, `Cplane1`, and `Cspp1`, the focal profiles all
had `significant_feature_count: 0`.  Whole-vector or signed-tail neighbors
were dominated by weak, non-significant, FDR-flat profiles and did not reveal
a hidden ciliary transcriptional module.  An induced Distributed Agents corpus
topology over the main ciliary analogs was dense
`100/120` connected pairs, but the paths mostly encode explicit reports that
these genes were flat, sparse, or nonconvergent in postnatal neuronal
snRNA-seq.  I therefore used the topology as support for choosing the ciliary
comparison set, not as a positive signature to average.

## Target-specific reasoning

### `Cep83`

`Cep83` encodes a conserved distal-appendage / transition-fiber protein at
the mother centriole.  CCDC41/CEP83 was shown to localize to the distal end of
the mother centriole, interact with CEP164, recruit IFT20, and support ciliary
vesicle docking at the onset of ciliogenesis (Joo et al. 2013,
doi:10.1073/pnas.1220927110, PMID 23530209).  CEP83 is also one member of the
hierarchical distal-appendage assembly pathway identified by Tanos et al.
2013 (PMID 23348840), which is why `Sclt1` is a particularly close training
perturbation: it is another distal-appendage protein in the same
ortholog-projected CORUM `Distal appendage` complex.  Human loss-of-function
mutations in CEP83 cause nephronophthisis and intellectual disability,
consistent with a ciliopathy mechanism rather than a generic transcriptional
regulator role (Failler et al. 2014, doi:10.1016/j.ajhg.2014.05.002,
PMID 24882706).

The within-dataset transfer evidence is more important than that external
essentiality.  In the exact focal cell group, both closest distal-appendage /
transition-fiber analogs were silent: `Sclt1` had 0 DEGs with no focal gene
below adjusted p = 1, and `Cep290` had 0 DEGs with best adjusted p = 0.65.
The silence extended across the represented cilium assembly and transport
machinery: `Ift88`, `Ift81`, `Ift43`, `Kif3b`, `Dync2h1`, `Dync2i1`, `Bbs5`,
`Cplane1`, `B9d1`, `Ttc21b`, and `Cep120` were all zero in the same focal
endpoint.  Distributed Agents corpus findings for `Cep290`, `Ift88`, `Kif3b`,
`Rpgrip1l`, `Sclt1`, `Bbs5`, `Dync2h1`, and `Cplane1` repeatedly describe the
same pattern: acute P16 CRISPR of ciliary trafficking, intraflagellar
transport, BBSome, and Hedgehog-adjacent genes in recovered postnatal NeuN+
neurons was buffered at the basal nuclear RNA level, while broad proteasome
and RNA-processing perturbations generated large signatures in the same assay
universe.

The zero call is therefore driven primarily by same-experiment evidence.  I
expect loss of CEP83 to disrupt distal-appendage mediated ciliary vesicle
docking, but in this Perturb-seq design that organelle defect is likely to be
observed as cilium assembly, receptor trafficking, or evoked signaling rather
than a steady-state thalamic nuclear mRNA program.  A singleton on-target
`Cep83` transcript could occur if the guide alleles trigger enough nonsense
mediated decay, but closest same-compartment comparators did not show such a
singleton in the focal group and self-transcript loss is not predictable in
this acute mosaic CRISPR assay.

## Limits

- The held-out `Cep83` knockout itself was not measured in either supplied
  input.  `Sclt1` and `Cep290` are mechanistic analogs, not the same gene, and
  CEP83 is upstream in distal-appendage recruitment, so the final count is an
  extrapolation.
- The assay does not image primary cilia, quantify distal-appendage proteins,
  measure ciliary receptor localization, sequence edited alleles, or assay
  embryonic progenitors, retina, kidney, glia, ependyma, olfactory epithelium,
  or ligand-evoked Hedgehog/cAMP physiology.
- Most ciliary training signatures are null or singleton.  That repeated
  absence is directly useful for this DEG-count endpoint, but it leaves little
  positive expression-pattern structure to distinguish one distal-appendage
  component from another.
- Corpus statements are derived from the same PerturbAI experiment, so I used
  them as an interpreted same-dataset knowledge layer, not as independent
  replication of the focal CSV or parquet.

## Final point prediction

The best point prediction for `Cep83` is `0` DEGs in
`151 TH Prkcd Grin2c Glut`.
