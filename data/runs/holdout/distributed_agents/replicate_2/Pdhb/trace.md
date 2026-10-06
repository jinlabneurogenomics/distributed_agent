# Question and interpretation

The held-out target list for this run contains one perturbation, `Pdhb`.

I interpreted the requested endpoint as the exact focal-cell endpoint in the
training-count CSV: for each perturbation, count every measured gene with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, including the targeted
transcript itself if it passes the threshold. The focal readout is therefore an
assay/power-specific nuclear snRNA-seq DEG count after acute sparse AAV-CRISPR
loss of function, not a direct readout of pyruvate flux, protein abundance, cell
fitness, or disease severity.

The only requested target, `Pdhb`, was absent as a perturbation from both
supplied training files, so I inferred its count from measured perturbations of
the same pyruvate dehydrogenase complex and neighboring mitochondrial carbon
metabolism genes.

# Sources used

- `[local file: training_de_all_cell_groups.parquet]`
  for per-gene log-fold changes and adjusted Wilcoxon p values in the focal
  group.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for the observed `n_degs` endpoint of non-held-out perturbations.
- `[local file: 171_Pdhb.csv]`
  for the requested target list.
- Distributed Agents corpus MCP release
  `perturbai-july-260713-sourceguard-1773-v1`, especially Pdha1 and Dlat
  same-experiment findings and claims:
  - `Pdha1:F004`: measured PDC comparators `Dlat`, `Dld`, `Mpc1` and related
    `Dlst`, `Ogdh`, `Sdha`, `Idh3a` were flat or nearly flat and did not form a
    coherent postmitotic neuronal PDH module.
  - `Dlat:F004`: literature-obvious PDC and adjacent mitochondrial-carbon
    comparators failed to phenocopy Dlat in `151 TH Prkcd Grin2c Glut`; `Pdhb`
    and several exact regulators were absent from the parquet.
  - claim `5e92ede610df7967282e`: represented mitochondrial carbon-entry, PDC,
    TCA, and Fe-S perturbations generally failed to induce a coherent
    postmitotic neuronal nuclear DE module in this assay, with isolated
    singleton exceptions.
- Distributed Agents runtime profile tools for same-context log-fold-change profile
  comparison among observed PDH/TCA analogs in `151 TH Prkcd Grin2c Glut`.
- External mechanism literature:
  - Patel, Nemeria, Furey, and Jordan, 2014, *J. Biol. Chem.*,
    doi:10.1074/jbc.R114.563148, PMID:24798336: PDC is built from E1, E2, and
    E3 catalytic components; E1/E2 generate acetyl-CoA and E3 recycles the
    lipoyl cofactor.
  - Patel, Korotchkina, and Sidhu, 2009, *J. Mol. Catal. B Enzym.*,
    doi:10.1016/j.molcatb.2009.05.001, PMID:20160912: human PDC uses an
    alpha2/beta2 E1 pyruvate dehydrogenase tetramer that binds the E2 core.
  - Patel and Korotchkina, 2006, *Biochem. Soc. Trans.*,
    doi:10.1042/BST20060217, PMID:16545080: mammalian PDC flux is tightly
    regulated by E1 phosphorylation/dephosphorylation and by the mitochondrial
    redox/metabolite state.
  - Okajima et al., 2008, *Mol. Genet. Metab.*,
    doi:10.1016/j.ymgme.2007.10.135, PMID:18164639: pathogenic PDHB variants
    cause PDC deficiency with lactic acidosis and developmental neurologic
    phenotypes.
  - Ronowska et al., 2018, *Front. Cell. Neurosci.*,
    doi:10.3389/fncel.2018.00169, PMID:30050410: mitochondrial PDC is a major
    source of acetyl-CoA for neuronal energy metabolism and related
    acetylation-dependent pathways.

# Computational steps

1. Loaded the manifest and confirmed it contained exactly `Pdhb`.

2. Loaded the training endpoint counts for the focal group and summarized the
   empirical response scale. Among 1,674 observed perturbations, 469 were
   nonzero, 276 had exactly one DEG, the median was 0 DEGs, the 75th percentile
   was 1 DEG, and the maximum was 2,677 DEGs. Summing the per-target counts
   matched a direct scan of the parquet for `pvals_adj < 0.05`, giving 23,526
   significant focal rows.

3. Queried the endpoint count table for direct biochemical analogs:

   | training perturbation | relationship to Pdhb | observed focal `n_degs` |
   | --- | --- | ---: |
   | `Pdha1` | obligate E1 alpha partner of PDHB in PDC E1 | 1 |
   | `Dlat` | PDC E2 core, accepts the E1 acetyl group | 1 |
   | `Dld` | E3 redox subunit for PDC and other 2-oxoacid dehydrogenases | 0 |
   | `Mpc1` | mitochondrial pyruvate carrier upstream of PDC | 0 |
   | `Mdh2` | mitochondrial malate dehydrogenase/TCA-MAS enzyme | 1 |
   | `Ogdh` | 2-oxoglutarate dehydrogenase E1, another TCA 2-oxoacid enzyme | 0 |
   | `Aco2` | mitochondrial aconitase/TCA enzyme | 0 |
   | `Idh3a` | mitochondrial IDH3/TCA enzyme | 1 |
   | `Sdha` | TCA and respiratory complex II enzyme | 1 |
   | `Ndufa10`, `Ndufs2` | respiratory complex I controls | 1, 1 |
   | `Mdh1` | cytosolic MAS enzyme, thalamic response counterexample | 29 |

4. Scanned the focal rows of the parquet for the same genes to distinguish
   self-transcript effects from downstream effects. The key filter was:

   ```python
   f = (
       (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
       & pc.field("gene_target").isin(targets)
       & (pc.field("pvals_adj") < 0.05)
   )
   ```

   `Pdha1`, `Dlat`, `Mdh2`, `Idh3a`, `Ndufa10`, `Ndufs2`, and `Sdha` each
   called only their own targeted transcript significant. `Dld`, `Mpc1`,
   `Ogdh`, and `Aco2` called no significant genes. In the exact PDH/TCA analog
   lookup, non-targeted mitochondrial carbon genes, including `Pdhb`, had
   `pvals_adj = 1` under these perturbations, so there was no detectable
   cross-induction or compensatory repression among the assayed PDC/TCA
   transcripts.

5. Compared signed expression profiles, in the same focal group, for the
   observed cohort `Pdha1`, `Dlat`, `Dld`, `Mpc1`, `Mdh2`, `Ogdh`, `Aco2`, and
   `Idh3a` with Distributed Agents runtime `profile_compare`. The node-level activity
   summary again separated the group into four null perturbations and four with
   only 1-9 significant genes. Whole-profile similarities among this weak
   cohort were present but shallow: for example, `Pdha1` had Pearson 0.646 with
   `Dlat`, 0.648 with `Dld`, 0.640 with `Mpc1`, and 0.660 with `Mdh2`; the
   top-200 positive/negative tail overlaps were only 4.5-20%. I used these as
   evidence that the measured profiles occupy the same weak, near-null
   expression regime, not as evidence for a strong shared downstream program.

6. Broadened the endpoint-count query to mitochondrial respiratory controls.
   Across 43 PDC/TCA/OXPHOS perturbations represented in the training count
   table, the mean was 0.44 DEGs, the median was 0, the maximum was 1, and
   24/43 were zero. This is an important calibration point: many mitochondrial
   loss perturbations did not generate a nuclear stress program in this acute
   postmitotic assay.

# Target-specific reasoning

## Pdhb

External biology places `Pdhb` at the most direct possible analog of `Pdha1`.
PDHB is the beta subunit of the pyruvate dehydrogenase E1 alpha2/beta2
tetramer; E1 binds DLAT/E2 in the PDC core, and the complete PDC converts
glycolytic pyruvate into mitochondrial acetyl-CoA while reducing NAD+ through
the DLD/E3 recycling reaction. Severe or germline PDC lesions are neurologically
important, and human PDHB mutations can cause PDC deficiency, lactic acidosis,
and Leigh-like neurodevelopmental disease. Those external facts say that PDHB
is a real mitochondrial disease gene; they do not by themselves imply a broad
steady-state nuclear DEG program after sparse, mosaic, partial postnatal
editing.

The experiment-specific evidence was uniformly low-response around PDC.
`Pdha1`, the E1 alpha partner closest to `Pdhb`, produced exactly 1 DEG in the
focal group, and that DEG was `Pdha1` itself
(`logfoldchanges = -1.039`, `pvals_adj = 1.31e-6`; 208 perturbed nuclei).
`Dlat`, the E2 core of the same PDC, also produced exactly one DEG, again only
the target transcript
(`logfoldchanges = -0.673`, `pvals_adj = 2.81e-7`; 170 perturbed nuclei). `Dld`
had 0 DEGs; even its own transcript was only `logfoldchanges = -0.397` with
`pvals_adj = 1`. `Mpc1`, immediately upstream of PDH through pyruvate import,
also had 0 DEGs. The Pdha1/Dlat/Dld/Mpc1 quartet is therefore a self-transcript
or null PDC neighborhood in the exact requested cell type.

The same conclusion held for slightly more distant mitochondrial-carbon
counterparts. `Mdh2`, `Idh3a`, `Ndufa10`, `Ndufs2`, and `Sdha` each had a
single self-transcript DEG and no downstream genes; `Aco2` and `Ogdh` had no
focal DEGs. `Mdh1` was the lone local metabolic counterexample with 29 focal
DEGs, but it is the cytosolic malate-aspartate arm and in the Distributed Agents corpus
is specifically separated from mitochondrial enzyme/carrier components, so I
did not extrapolate its TH glutamatergic program to PDHB.

The Distributed Agents corpus supported this narrow interpretation rather than a generic
mitochondrial-response extrapolation. `Pdha1:F004` states that directly
measured PDC/TCA comparators were flat or nearly flat and did not form a shared
postmitotic neuronal PDH module; `Dlat:F004` states that same-complex and
adjacent mitochondrial-carbon comparators failed to phenocopy Dlat in
`151 TH Prkcd Grin2c Glut`; claim `5e92ede610df7967282e` generalizes the same
observation across represented carbon-entry, PDC, TCA, and Fe-S targets.

The final decision is therefore nonzero, but only barely. The nonzero part is
driven by the direct within-dataset observation that the two closest assayed PDC
subunits, `Pdha1` and `Dlat`, were each recovered as target-transcript-only
singletons. Because `Pdhb` is the measured gene being edited and is the obligate
E1 beta partner of `Pdha1`, one FDR-significant self-transcript row is more
likely than an absolute zero. The absence of downstream genes in `Pdha1`,
`Dlat`, `Dld`, `Mpc1`, and the wider mitochondrial controls argues strongly
against adding any extra downstream DEGs.

Prediction: `Pdhb -> 1`.

# Limits and extrapolations

- The exact held-out target `Pdhb` had no Distributed Agents target-centered corpus node
  in this release and no observed same-experiment profile in the supplied
  parquet, so the estimate is necessarily transferred from `Pdha1`, `Dlat`,
  `Dld`, `Mpc1`, and other represented neighbors.
- The direct analog panel is incomplete: `Pdhx`, `Mpc2`, the PDKs, and PDPs
  were not represented as training `gene_target` values, and the corpus also
  flagged these omissions.
- Predicting one DEG depends on a target-transcript effect. The experiment's
  average mRNA knockdown is modest, and CRISPR indel burden, PDHB protein, PDC
  flux, pyruvate/lactate, ATP, and acetyl-CoA were not measured. A real PDHB
  protein effect could exist with zero FDR-significant nuclear genes, or the
  self transcript could miss FDR if the guide pool happened not to reduce mRNA.
- The weak profile similarities among PDC/TCA genes were computed from
  near-null log-fold-change vectors. They are useful for rejecting a broad,
  reproducible transcriptional module, but the large extreme fold changes at
  `pvals_adj = 1` should not be read as biological marker genes.
- The prediction applies to the stated acute, sparse, juvenile,
  postmitotic-neuron snRNA-seq assay. It should not be extrapolated to germline
  or high-efficiency PDHB loss, to systemic metabolic stress, or to non-neuronal
  brain cells that were not well sampled here.
