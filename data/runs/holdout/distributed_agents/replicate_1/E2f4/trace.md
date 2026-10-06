## Question

I predicted the held-out focal-class endpoint for `E2f4`: the number of measured
genes that would pass Benjamini-Hochberg FDR 0.05 after acute mosaic
CRISPR-Cas9 loss of `E2f4` in recovered `151 TH Prkcd Grin2c Glut` mouse
neurons. I treated this as a one-target scalar count prediction, not as a
ranking task. The held-out `E2f4` DE signature itself is absent from the
declared parquet and the focal-cell training-count CSV, so the task requires
transfer from non-held-out perturbations and external biology.

The ambiguity I resolved was how to use known E2F biology. `E2f4` is a
canonical cell-cycle transcription factor, but the relevant assay is not a
cycling cell system: it perturbed sparse postmitotic postnatal NeuN+ nuclei and
measured only survivor-conditioned nuclear RNA after 3-4 weeks. I therefore
used cell-cycle biology to choose E2F/DP and pocket-protein analogs, then let
the training counts and focal-class expression signatures determine whether
that axis was detectably active in this cell class.

## Sources

Input data:

- `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  for observed non-held-out `151 TH Prkcd Grin2c Glut` DEG counts.
- `training differential-expression dataset`
  for exact per-gene Wilcoxon scores, log2 fold changes, adjusted P values, and
  matched nucleus counts for the E2F/DP/DREAM-adjacent visible perturbations.
- `single-target request for E2f4`
  for the requested held-out target list.

Internal same-experiment corpus:

- PerturbAI July 260713 SourceGuard v1 Finding ledger, queried for the visible
  non-held-out analogs `E2f1`, `E2f5`, `Tfdp1`, and `Tfdp2`. I used it as a
  compact interpretation layer over the same Perturb-seq experiment, not as
  independent replication and not as evidence for the withheld `E2f4` outcome.

External mechanism sources:

- Sadasivam, Duan, and DeCaprio 2012, Genes & Development,
  DOI `10.1101/gad.181933.111`, PubMed `22391450`: mammalian MuvB joins p130,
  E2F4, and DP1 as the quiescent DREAM complex and switches to B-Myb/FoxM1
  during S/G2/M.
- Litovchick et al. 2011, Genes & Development, DOI `10.1101/gad.2034211`,
  PubMed `21498570`: DYRK1A-dependent LIN52 phosphorylation promotes DREAM
  assembly during quiescence and senescence.
- Cuitino et al. 2019, Cell Reports, DOI `10.1016/j.celrep.2019.05.004`,
  PubMed `31130414`: E2F3A, E2F4, and E2F8 form developmentally regulated E2F
  modules for cell-cycle gene expression in vivo.
- Danielian, Hess, and Lees 2016, Cell Cycle,
  DOI `10.1080/15384101.2015.1121350`, PubMed `26825228`: `E2f4` and `E2f5`
  have overlapping in-vivo roles in a differentiated epithelial system.
- Ruzhynsky et al. 2009, Developmental Neuroscience,
  DOI `10.1159/000210186`, PubMed `19325228`: `E2f4` knockout perturbs early
  embryonic eye patterning through Shh-associated patterning effects.
- Persengiev et al. 2001, Oncogene, DOI `10.1038/sj.onc.1204663`, PubMed
  `11526501`: in PC12-derived neurons, E2F4 enhanced neuronal differentiation
  without the cell-cycle or survival effects seen after forced E2F2.

## Computation

I first read the requested-target CSV and confirmed that it contains exactly
one held-out perturbation:

```text
target_name
E2f4
```

I then used the training focal-cell counts to place mechanistic analogs on the
observed endpoint scale. The `n_degs` distribution across 1,674 visible
training perturbations was highly zero-inflated: median 0, 75th percentile 1,
90th percentile 2, 95th percentile 18, and 469/1674 targets nonzero. The
E2F/DP and nearby cell-cycle comparators in the training endpoint were:

| comparator | `151 TH Prkcd Grin2c Glut` training `n_degs` | relevance |
|---|---:|---|
| `E2f1` | 0 | E2F family activator; opposite side of the E2F module from E2F4 but tests whether acute E2F loss exposes G1/S or apoptotic transcripts |
| `E2f5` | 0 | closest visible canonical repressor paralog and alternate DREAM E2F subunit |
| `Tfdp1` | 2 | DP1, the high-affinity DNA-binding partner of E2F4 in DREAM and RB-E2F complexes |
| `Tfdp2` | 0 | DP2 paralog; tests the same DP-dependent E2F axis |
| `Dyrk1a` | 0 | upstream kinase that promotes DREAM assembly through LIN52 phosphorylation |
| `Myc` | 0 | growth/cell-cycle transcriptional neighbor |
| `Cdkn2a` | 0 | RB/E2F pathway regulator |
| `Trp53` | 0 | upstream stress regulator that can repress cell-cycle genes through p21 and DREAM in cycling contexts |

For the core analogs I also filtered the parquet to the focal cell class and
the listed `gene_target` values, then inspected the lowest adjusted P values
and the expression pattern of the two nonzero `Tfdp1` genes. This checks
whether a zero count is a true FDR-null signature or whether it hides many
near-threshold E2F-program genes.

The focal-class signatures were:

- `E2f1`: 253 matched perturbed nuclei, 23,679 matched controls, no genes with
  `pvals_adj < 0.05`. The top rows were all `pvals_adj = 1.0`, led by `E2f6`,
  `Ywhab`, and `Psmd2`, so there was no near-threshold signal.
- `E2f5`: 117 perturbed nuclei, no FDR-significant genes. Top adjusted P values
  were also all 1.0, led by `Ckap5`, `Ndfip2`, and `Zmat4`.
- `Tfdp1`: 203 perturbed nuclei and exactly two FDR-significant genes,
  `Cntrob` with log2 fold change 0.663 and `pvals_adj = 0.0114`, and `Dcaf15`
  with log2 fold change 0.534 and `pvals_adj = 0.0346`. The next gene, `Trrap`,
  had `pvals_adj = 0.118`, so this was a narrow two-gene tail rather than a
  broad E2F signature.
- `Tfdp2`: 184 perturbed nuclei, no FDR-significant genes; the best adjusted P
  values were 1.0.
- `Dyrk1a`: 90 perturbed nuclei, no FDR-significant genes; the lowest adjusted
  P value was 0.642.
- `Trp53`: 251 perturbed nuclei, no FDR-significant genes; the lowest adjusted
  P value was 0.338.

The July same-experiment Finding ledger adds two relevant checks over these
same measurements. First, the `E2f1`, `E2f5`, and `Tfdp2` reports each describe
pan-neuronal robust negative results rather than 151-only absences. Second,
the `Tfdp1` report states that the two 151 TH hits, `Cntrob` and `Dcaf15`, were
uncoupled from canonical G1/S markers such as `Mcm2-7`, `Pcna`, `Cdc6`,
`Ccne1`, `Ccna2`, `Rrm2`, and `Mki67`, and that represented relatives
`Tfdp2`, `E2f1`, and `E2f5` did not phenocopy `Tfdp1`. This argues against
assigning `E2f4` a broad count simply because it belongs to the E2F family.

## Target-specific reasoning

### E2f4

`E2f4` encodes a pocket-protein-associated E2F transcription factor. With DP1,
p130/p107, and MuvB it forms the quiescent DREAM complex that represses early
and late cell-cycle genes; when cells enter cycle, MuvB leaves p130/E2F4 and
joins B-Myb and FoxM1 to activate mitotic transcription. That makes `Tfdp1`,
`Tfdp2`, `E2f5`, and `Dyrk1a` the most relevant training perturbations, because
they perturb the same E2F-DP/DREAM regulatory chain. `E2f5` is the closest
training analog: it can occupy the same repressor side of the pathway and has
overlapping in-vivo functions with `E2f4` in some differentiated tissues.
`E2f1` is less direct because it is an activator E2F rather than the E2F4-like
DREAM repressor, but it is a useful counterexample: if this neuronal assay were
highly sensitive to basal E2F-dependent G1/S or apoptosis changes, loss of
`E2f1` should not be perfectly flat.

The E2F-axis training evidence is consistently low:

- same-direction, close-family analog `E2f5`: 0 DEGs in the focal cell class,
  and no FDR<0.10 genes in any measured NeuN-enriched neuronal group in the
  July corpus report;
- obligate DNA-binding partner `Tfdp1`: only 2 focal-class DEGs, neither a
  canonical E2F cell-cycle gene;
- DP paralog `Tfdp2`: 0 focal-class DEGs and no broad signature neighbor;
- E2F activator `E2f1`: 0 focal-class DEGs and no movement of MCM, PCNA,
  cyclin, or apoptotic target panels in the same-experiment report;
- upstream DREAM-assembly kinase `Dyrk1a` and stress/upstream cell-cycle
  regulators `Trp53`, `Myc`, and `Cdkn2a`: all 0 focal-class DEGs.

Causal transfer from these analogs therefore predicts either no recovered-cell
RNA effect or a count at the assay noise boundary. The intervention is acute
partial loss of one E2F4 family member; the direct molecular consequence should
weaken E2F4-DP and DREAM-mediated transcriptional repression, but postmitotic
P37-44 thalamic glutamatergic neurons have a very low active cell-cycle
program and contain alternate RB/E2F family members. The expected propagation
to a measured endpoint is thus redundancy/buffering plus very low expression of
the canonical S-phase and mitotic target transcripts, not wholesale cell-cycle
derepression. `Tfdp1`'s two-gene escape keeps a one- or two-DEG outcome
possible, but because the escape does not involve canonical E2F targets and
does not transfer to `E2f1`, `E2f5`, or `Tfdp2`, I treated it as insufficient
to make the single `E2f4` point prediction positive.

External biology mostly sets the analog choice and does not override the
within-dataset near-null axis. Germline `E2f4` phenotypes in fetal
erythropoiesis and embryonic eye patterning occur in proliferating or
developmental tissues, and `E2f4`/`E2f5` overlap in male reproductive duct
development is off-lineage from NeuN+ thalamic neurons. The PC12 observation
that E2F4 can enhance neuronal differentiation without driving cell-cycle exit
or survival also fits a weak postmitotic transcriptional endpoint. None of
these sources establishes an obligate `151 TH Prkcd Grin2c Glut` DEG burden
under sparse P16 AAV CRISPR.

Predicted count: `0`.

## Limits

The prediction is an extrapolation from related visible perturbations, not a
measurement of the held-out `E2f4` perturbation. `E2f4` itself may be less
redundant than `E2f5` in a subset of thalamic neurons, and an isolated
near-threshold effect like the two `Tfdp1` genes could make the true integer
count nonzero even if the E2F-DREAM program as a whole is buffered. Several
direct DREAM components and pocket proteins were absent as training targets
in the focal count table, including `Rb1`, `Rbl1`, `Rbl2`, `Lin9`, `Lin37`,
`Lin52`, and `Lin54`, so the same complex was represented only through E2F/DP
subunits and `Dyrk1a`. The assay is survivor-conditioned and did not measure
DNA indels, E2F4 protein depletion, cell loss before nuclei recovery, or raw
single-cell counts; all conclusions are about the recovered 10x Flex nuclear
RNA DEG-count endpoint only.
