## Question

I interpreted the held-out readout as the focal-cell count of genes with
`pvals_adj < 0.05` after acute AAV-CRISPR loss of the requested gene, with the
count computed in `151 TH Prkcd Grin2c Glut` nuclei only.  The manifest for this
run contains one held-out target:

```tsv
target_name
Ppp2r1a
```

I treated `Ppp2r1a` as absent experimental evidence: its own 151 TH signature
and DEG count were not used because they are not present in the supplied
training parquet or the supplied training count table.

## Sources Used

- Supplied endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied all-cell differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out target manifest:
  `[local file: 184_Ppp2r1a.csv]`.
- The same-experiment Distributed Agents semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, for precomputed Ppp2r2b,
  Ppp2r5d, Set, and Rack1 Findings/Claims.
- PubMed for external PP2A biology.
- NCBI Gene annotations as cited inside the Distributed Agents corpus for PP2A subunit
  identities.

## Dataset Computation

I first read the 1,674 held-in focal-cell counts.  The 151 TH endpoint is very
zero-heavy: median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`,
and only 469/1,674 held-in perturbations have any FDR 0.05 DEG.

I then searched the held-in target list for PP2A subunits and close pathway
members.  The direct PP2A holoenzyme perturbations available for focal-cell
calibration are only:

| training target | relationship to Ppp2r1a | observed 151 TH `n_degs` |
| --- | --- | ---: |
| `Ppp2r2b` | PP2A B55-beta regulatory subunit | 0 |
| `Ppp2r5d` | PP2A B56-delta regulatory subunit | 0 |
| `Set` | endogenous PP2A inhibitor, an imperfect opposite-direction comparator | 0 |

The catalytic and scaffold paralogs `Ppp2ca`, `Ppp2cb`, and `Ppp2r1b` were not
held-in targets, so there is no perfect scaffold/catalytic loss-of-function
analog in the training count table.

For expression-pattern checks, I projected focal-cell rows from the parquet with
a PyArrow filter:

```python
focal = pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
targets = pc.field("gene_target").isin([... PP2A and pathway comparators ...])
table = dataset.to_table(
    columns=["names", "gene_target", "scores", "logfoldchanges", "pvals_adj"],
    filter=focal & targets,
)
```

I also used the Distributed Agents runtime profile tools on Wilcoxon `scores` to compare
whole signed profiles and leading 200-gene tails in the same focal group.

## Target Reasoning

### `Ppp2r1a`

External biology makes `Ppp2r1a` a plausible neuronal perturbation but also
argues for caution when transferring from congenital missense disease to this
acute indel assay.  PPP2R1A encodes the A-alpha/PR65 scaffold of PP2A:
canonical PP2A holoenzymes contain a scaffold A subunit, a catalytic C subunit,
and one substrate-routing regulatory B subunit.  Pathogenic human PPP2R1A
variants are mostly de novo heterozygous missense alleles that change B- or
C-subunit binding and can behave biochemically like dominant-negative
holoenzyme assembly defects, not simple postnatal null alleles.  Houge et al.
2015 identified PPP2R5D and PPP2R1A de novo missense alleles in intellectual
disability and showed that mutant A-alpha subunits can uncouple B56-delta from
phosphatase activity through defective C-subunit binding
(PMID 26168268, DOI 10.1172/JCI79860).  Lenaerts et al. 2020 expanded the
PPP2R1A neurodevelopmental spectrum and found that variants with stronger
B55-alpha binding defects were associated with more severe neurodevelopmental
phenotypes (PMID 33106617, DOI 10.1038/s41436-020-00981-2).  Verbinnen et al.
2021 reviewed PP2A mutations in brain development and emphasized that the
phenotypes of PPP2CA, PPP2R1A, and PPP2R5D variants depend on altered PP2A
structure and substrate specificity (PMID 34241636,
DOI 10.1042/BST20201313).

The closest within-dataset evidence points to a transcriptionally buffered
PP2A loss-of-function response in recovered postnatal neurons:

- `Ppp2r2b`, the B55-beta PP2A regulatory subunit, had `n_degs = 0` in 151 TH.
  Its focal-cell profile used 151 perturbed nuclei and 23,679 controls; no gene
  passed FDR 0.05, the strongest downstream row was only `Nfat5`
  (`score = -4.25`, `pvals_adj = 0.362`), and the target transcript itself was
  subthreshold (`Ppp2r2b logFC = -0.428`, `pvals_adj = 1`).  The Distributed Agents
  corpus reports a stronger screen-wide negative result: `Ppp2r2b` produced no
  FDR 0.10 downstream genes in any of 22 measured neuronal groups.

- `Ppp2r5d`, the B56-delta PP2A regulatory subunit, also had `n_degs = 0` in
  151 TH.  Its focal-cell profile used 141 perturbed nuclei and 23,679 controls;
  again no gene passed FDR 0.05, and the target transcript was the leading
  negative row but only at `pvals_adj = 0.405`.  The Distributed Agents corpus found that
  Ppp2r5d was not globally inert, but its whole screen-wide signal was tiny:
  only three FDR 0.10 downstream genes across all neuronal groups, restricted
  to superficial intratelencephalic glutamatergic classes rather than 151 TH.
  Ppp2r5d and Ppp2r2b did not define a shared latent PP2A signature in 151 TH;
  their focal score vectors had Pearson `r = 0.0066`, cosine `= 0.0038`, and no
  shared FDR 0.05 genes.

- `Set` had `n_degs = 0` in 151 TH.  SET is not a knockout-equivalent comparator
  for `Ppp2r1a`, because SET loss would release some PP2A activity rather than
  remove a holoenzyme subunit.  It is still a useful boundary: the Distributed Agents
  claim over `Set`, `Ppp2r2b`, and `Ppp2r5d` concluded that represented PP2A
  regulatory-subunit perturbations and Set perturbation do not collapse into a
  shared acute neuronal mRNA axis.

I used mTOR, AKT, GSK3/tau, MAPK, and APP pathway members as counterexamples
because PP2A can oppose these phosphorylation systems, but the observed counts
again argue against a broad PP2A-like transcriptional state in 151 TH:
`Akt3 = 0`, `Pik3cb = 0`, `Pik3r1 = 0`, `Pik3r2 = 0`, `Rptor = 0`,
`Mapk1 = 0`, `Mapk9 = 0`, `Mtor = 2`, `App = 1`, `Mapt = 1`, and `Gsk3b = 6`.
`Tsc2` was much larger at `n_degs = 86`, showing that this cell group and
pipeline can detect an mTOR-axis RNA response when it is present; however,
`Ppp2r5d` was explicitly nonconvergent with `Tsc2` in the Distributed Agents corpus and
was negatively correlated with `Tsc2` in my 151 TH profile comparison
(`cosine = -0.0349`, no shared FDR genes).

I also treated `Rack1` as a narrow counterexample rather than a positive
phenocopy.  Rack1 perturbation produced only two focal FDR 0.05 DEGs in the
training table, `Aplp2` and `Ppp2r1a` itself, and the Distributed Agents `Rack1:F003`
Finding reports that neither data-driven neighbors nor PP2A, mTOR/translation,
APP, Fyn/PKC, FMRP, or CNOT1 pathway comparators converged on that two-gene
thalamic `Aplp2`/`Ppp2r1a` signature.  Thus 151 TH neurons can show a modest
Ppp2r1a transcript decrease after some perturbations, but that observation did
not mark a broad PP2A-holoenzyme response.

Balancing these lines, the scaffold role of `Ppp2r1a` makes its knockout
potentially more central than knocking out a single B subunit, but the actual
held-in PP2A and PP2A-linked perturbations are either completely flat or have
singleton-scale focal responses.  The focal whole-profile comparisons also put
the PP2A regulatory subunits at the correlation noise floor, so there is no
subthreshold PP2A module to rescue.  I therefore predict no BH-corrected 151 TH
DEGs for acute `Ppp2r1a` CRISPR loss:

`Ppp2r1a -> 0`.

## Limits

This prediction extrapolates across PP2A subunit classes.  The held-in dataset
contains no `Ppp2r1b`, `Ppp2ca`, or `Ppp2cb` perturbation, and `Ppp2r1a` is a
common scaffold rather than a substrate-selective B subunit, so a stronger
effect than `Ppp2r2b`/`Ppp2r5d` is possible.  The assay measures survivor
nuclear RNA three to four weeks after sparse P16 editing; it does not measure
DNA indels, PP2A protein turnover, holoenzyme assembly, phosphatase activity,
GSK3/tau/AKT phosphorylation, or mitochondrial morphology.  Human PPP2R1A
neurodevelopmental alleles are usually developmental missense alleles with
altered complex binding, so they are only a functional prior, not a direct
count prior for postmitotic mouse neuronal CRISPR loss.
