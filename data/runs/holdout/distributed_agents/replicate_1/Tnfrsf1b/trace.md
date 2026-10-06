# Reasoning trace

## Question and endpoint

The held-out perturbation in this run is `Tnfrsf1b`. I interpreted the task as a
point prediction of the focal-cell endpoint:

`n_degs = count(pvals_adj < 0.05)` in `151 TH Prkcd Grin2c Glut` for the
held-out CRISPR loss-of-function perturbation.

`Tnfrsf1b` is completely held out from both the differential-expression Parquet
and the focal training-count CSV, so its own DEG count and expression signature
cannot be read directly. The endpoint is directly observed for non-held-out
training perturbations in the focal CSV; held-out prediction requires transfer
from measured training perturbations and external gene-function knowledge.

## Sources used

- Direct input endpoint: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`,
  the observed `n_degs` for 1,674 non-held-out perturbations in the focal
  thalamic glutamatergic group.
- Direct input signatures:
  `training_de_all_cell_groups.parquet`, queried only for the focal-cell
  signatures of candidate TNF receptor / TNF-to-NF-kappaB analogs.
- Same-experiment semantic corpus: PerturbAI July 260713 sourceguard 1773 v1
  Findings, Evidence, and Reference ledgers. I used bounded corpus entries for
  `Tnfrsf1a`, `Cd40`, `Fas`, `Nfkb1`, and `Traf3`; these are interpreted
  surfaces over the same screen, not independent replication.
- External literature through NCBI PubMed and packaged references:
  Gough and Myles 2020, DOI `10.3389/fimmu.2020.585880`, for TNFR1/TNFR2
  signaling complexes; Ting and Bertrand 2016, DOI `10.1016/j.it.2016.06.002`,
  for TNFR1 NF-kappaB/death/necroptosis branch logic; Smilovic et al. 2022,
  PMID `36221961`, DOI `10.1002/cne.25424`, as evidence that constitutive
  TNFR2 deficiency can affect dentate granule-cell spine morphology but in a
  germline hippocampal anatomy endpoint rather than this acute transcriptional
  assay.
- I did not rely on STRING, Gene Ontology, KEGG, or graph topology as a scoring
  source.

## Computation over the supplied dataset

The training-count CSV is sparse and zero-inflated: 469 of 1,674 perturbations
have at least one focal-cell DEG, the median is 0, the 75th percentile is 1,
and the maximum is 2,677.

I then checked TNF-receptor and reachable TNFR/NF-kappaB comparators in the
training endpoint. The focal `n_degs` values were:

| training perturbation | relation to `Tnfrsf1b` | focal `n_degs` |
|---|---|---:|
| `Tnfrsf1a` | closest measured TNF receptor paralog and TNF receptor 1 | 0 |
| `Cd40` | another TNFR-family receptor upstream of TRAF/NF-kappaB signaling | 0 |
| `Fas` | death-domain TNFR-family receptor | 0 |
| `Tnfrsf11a` | TNFR-family receptor | 0 |
| `Tnfrsf13c` | TNFR-family receptor that can use TRAF/NF-kappaB modules | 0 |
| `Tnfrsf4` | TNFR-family receptor | 0 |
| `Tnfrsf9` | TNFR-family receptor | 0 |
| `Traf3` | represented TNFR/TLR adaptor | 0 |
| `Map3k7` | TAK1, canonical cytokine-to-NF-kappaB/MAPK transducer | 0 |
| `Nfkb1` | canonical NF-kappaB transcription-factor subunit | 0 |

For the focal-cell Parquet signatures I computed, per candidate target, the
number of rows at FDR 0.05 and FDR 0.10 plus the smallest adjusted p-value:

```sql
SELECT gene_target,
       COUNT(*) AS measured,
       SUM(pvals_adj < 0.05) AS n_fdr05,
       SUM(pvals_adj < 0.10) AS n_fdr10,
       MIN(pvals_adj) AS min_padj,
       MAX(n_pert_matched) AS n_pert_matched,
       MAX(n_ctrl_matched) AS n_ctrl_matched
FROM read_parquet(training_de_all_cell_groups.parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (
    'Tnfrsf1a','Traf3','Nfkb1','Map3k7','Tnfrsf11a',
    'Tnfrsf13c','Tnfrsf4','Tnfrsf9','Cd40','Fas')
GROUP BY gene_target;
```

Every queried analog had 17,259 measured genes, 0 genes at FDR 0.05, and 0 at
FDR 0.10 in `151 TH Prkcd Grin2c Glut`. `Tnfrsf1a`, `Traf3`, `Nfkb1`,
`Map3k7`, `Tnfrsf11a`, `Tnfrsf4`, `Cd40`, and `Fas` had no borderline signal at
all: their minimum adjusted p-value was exactly 1.0. The two least-flat
TNFR-family rows were still far from FDR support: `Tnfrsf13c` had minimum
adjusted p-value 0.8156 and `Tnfrsf9` had minimum adjusted p-value 0.3910.

The July same-experiment corpus was consistent with this direct query. Its
`Tnfrsf1a` report summarized acute `Tnfrsf1a` loss of function as a pan-neuronal
transcriptomic null at FDR 0.10, and its TNF/NF-kappaB evidence explicitly
checked 405 tested rows spanning sentinel response genes including `Nfkbia`,
`Tnfaip3`, `Birc2`, `Birc3`, `Ccl2`, `Ccl5`, `Cxcl10`, `Cxcl1`, `Cxcl2`, `Il6`,
`Icam1`, `Jun`, `Fos`, `Traf1`, `Nfkb1`, `Rel`, `Rela`, `Relb`, and `Irf1`;
none had adjusted p-value below 0.10 after `Tnfrsf1a` perturbation. The same
report noted that measured intracellular pathway neighbors `Chuk`, `Cyld`,
`Map3k7`, `Nfkb1`, and `Traf3` were flat across their matched neuronal groups.
Separate corpus reports described `Cd40`, `Fas`, `Nfkb1`, and `Traf3` as flat
or nearly flat basal neuronal TNFR/TLR/NF-kappaB contexts, reinforcing the
interpretation that this axis is not tonically transcriptionally engaged in
uninjured P16-to-P37/44 NeuN-positive neurons.

## Target-specific prediction

### `Tnfrsf1b`

`Tnfrsf1b` encodes TNFR2. TNFR2 is a ligand-gated TNF receptor that lacks the
TNFR1 intracellular death domain and signals through TRAF/cIAP/NF-kappaB
complexes in cell types and states where the receptor and TNF-family ligand
axis are engaged. The acute perturbation chain I considered was:

`Tnfrsf1b` CRISPR loss -> reduced TNFR2 function -> less TNF/TRAF/cIAP/NF-kappaB
signal -> possible inflammatory/survival transcriptional changes -> recovered
NeuN-positive thalamic glutamatergic nuclei -> Wilcoxon DEG count.

The strongest within-dataset analog is `Tnfrsf1a`, the other measured TNF
receptor. `Tnfrsf1a` perturbation has the same ligand family and lies closer
to the canonical TNF receptor immediate signaling problem than generic
downstream NF-kappaB components. In the exact focal endpoint, `Tnfrsf1a` had
0 DEGs, and even relaxed to FDR 0.10 there were 0 of 17,259 genes. Its
expected immediate TNF/NF-kappaB outputs were also absent in the
same-experiment report. Because TNFR1 is generally the receptor more often
capable of death-domain and inflammatory NF-kappaB/JNK outputs, a flat
`Tnfrsf1a` state in these same recovered neurons is a strong counterexample to
expecting a broad basal `Tnfrsf1b` response.

Other receptor comparators supported the same zero decision rather than a
nonzero rescue. `Cd40`, `Fas`, `Tnfrsf11a`, `Tnfrsf13c`, `Tnfrsf4`, and
`Tnfrsf9` were all zero in the focal training-count CSV. `Cd40` and `Fas` are
imperfect analogs: their ligand usage and proximal receptor complexes differ
from TNFR2. They are useful here only as falsifiers of a broad expectation that
TNFR-family receptor loss should yield a detectable basal neuronal signature.

The downstream comparators were also zero. `Traf3`, `Map3k7`, and `Nfkb1` each
had `n_degs = 0` in the focal endpoint and 0 genes below FDR 0.10 in the direct
focal Parquet query. These are not obligate one-to-one TNFR2 effectors:
`Tnfrsf1b` can recruit TRAF2/cIAP complexes, and many TNF-induced NF-kappaB
branches were not individually perturbed as training targets. But their flat
signatures argue that the assayed postnatal neuronal context lacks a tonic
TNFR/TLR-to-NF-kappaB transcriptional module. That is the key endpoint link:
even if TNFR2 is biologically meaningful in immune, endothelial, oligodendrocyte,
or injured CNS settings, this screen largely excludes non-neuronal cells and
does not supply TNF, injury, demyelination, or other cytokine challenge.

External biology did not overturn the same-experiment nulls. The published
TNFR literature supports strong ligand- and cell-state dependence of TNFR
signaling rather than constitutive TNFR2 control of thalamic glutamatergic
neuron nuclear RNA. Smilovic et al. found dentate-granule spine changes in
germline TNFR2-deficient mice, which shows that the receptor can matter in a
neuronal CNS phenotype, but that evidence is chronic, hippocampal, anatomical,
and developmental/constitutive; it does not establish a 3-4 week acute CRISPR
loss-of-function DEG response in `151 TH Prkcd Grin2c Glut`.

I therefore predict no FDR-significant genes:

| target | predicted `n_degs` |
|---|---:|
| `Tnfrsf1b` | 0 |

## Limits

- The prediction extrapolates from `Tnfrsf1a`, other TNFR-family receptors, and
  reachable downstream pathway components; `Tnfrsf1b` itself has no supplied
  DE signature or observed count.
- TNFR2 is not mechanistically identical to TNFR1, CD40, FAS, or TRAF3. A
  TNFR2-specific effect through TRAF2/cIAP or noncanonical NF-kappaB components
  could be missed because several exact proximal effectors were not visible
  training perturbations.
- The dataset is NeuN-enriched and survivor-conditioned. It is weak evidence
  about TNFR2 functions in microglia, astrocytes, endothelial cells,
  oligodendrocytes, T cells, stroke, demyelination, or inflammatory ligand
  challenge.
- A point prediction of zero means I expect no gene to pass BH FDR 0.05 in this
  assay. It does not imply absent TNFR2 biology, absent editing, or absence of
  subtle sub-FDR shifts.
