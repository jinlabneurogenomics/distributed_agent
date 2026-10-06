# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out target list for this run contains one mouse perturbation:

| target_name |
| --- |
| `Guk1` |

I interpreted the endpoint as the integer number of genes with `pvals_adj < 0.05`
after `Guk1` CRISPR loss-of-function in `151 TH Prkcd Grin2c Glut` cells,
using the same Wilcoxon/BH testing convention as the supplied training counts.
`Guk1` is absent from both the parquet differential-expression table and the
training count CSV by design, so I used only non-held-out targets to calibrate
the prediction.

Two conventions mattered:

- A predicted `0` means that I do not expect even one measured transcript,
  including the target transcript, to cross FDR 0.05.
- `n_degs` is an assay-power endpoint, not a viability or biological-essentiality
  endpoint. I therefore treated external evidence that GUK1 can be essential as
  a reason to ask whether a nucleotide-stress RNA program is visible in this
  dataset, not as proof of many DEGs in postmitotic NeuN+ nuclei.

## Sources used

- Input count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input DE table:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested target manifest:
  `[local file: 102_Guk1.csv]`
- Same-experiment Distributed Agents corpus:
  `perturbai-july-260713-sourceguard-1773-v1`; I queried `Guk1`, the
  represented purine and cAMP/cGMP neighbors `Adk`, `Nt5c2`, `Pde10a`, and the
  induced topology among `Adk`, `Nt5c2`, `Pde1c`, `Pde4b`, `Pde4d`, `Pde10a`,
  `Gucy2c`, and `Gucy2e`.
- PubMed literature for GUK1 enzymology and disease biology:
  Sekulic et al. 2002, DOI `10.1074/jbc.M204668200`, PMID `12036965`;
  Hidalgo-Gutierrez et al. 2024, DOI `10.1002/ana.27071`,
  PMID `39230499`.

## Computations over the input data

I first loaded the held-out manifest and the focal-cell training counts.  The
training endpoint has 1,674 non-held-out targets and is strongly zero-inflated:
the median is `0`, the 75th percentile is `1`, the 90th percentile is `2`, the
95th percentile is `18`, the mean is `14.05`, and `1205 / 1674 = 72.0%` of
training perturbations have `n_degs = 0`.  Thus a zero prediction is the
background state unless there is either direct same-pathway evidence for a
visible response or a strong target-specific reason to expect a larger stress
or identity shift.

To inspect focal signatures, I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and then to biologically nominated
training targets.  This is the core filter; the rest of the script only sorted
by adjusted p-value and joined the training endpoint:

```python
import pyarrow.dataset as ds

dset = ds.dataset("training_de_all_cell_groups.parquet", format="parquet")
expr = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(targets)
)
tbl = dset.scanner(
    columns=[
        "names",
        "gene_target",
        "logfoldchanges",
        "pvals_adj",
        "scores",
        "n_pert_matched",
        "n_ctrl_matched",
    ],
    filter=expr,
).to_table()
```

I also checked target-self rows in the focal group by filtering
`names == gene_target`.  Among 1,642 training targets with a measured self row,
319 had self-RNA FDR < 0.05; all of those had nonzero `n_degs`.  Conversely,
1,175 zero-DEG targets had no significant self row.  A one-gene prediction for
`Guk1` would therefore mostly be a prediction that the direct `Guk1` mRNA
knockdown alone passes FDR.  The closest purine analogs below did not self-score
in this cell group.

Finally, I used the run-local profile-comparison tool on the focal profiles for
`Adk`, `Nt5c2`, `Pde1c`, `Pde4b`, `Pde4d`, `Pde10a`, `Gucy2c`, and `Gucy2e`.
All eight were classified as `no_significant_features` in
`151 TH Prkcd Grin2c Glut`.  Their pairwise signed-tail similarities had zero
FDR-significant intersections, so I treated weak whole-profile similarities as
flat-background structure rather than a hidden `Guk1`-like module.

## Target-specific reasoning

### `Guk1`

**External target function.**  `Guk1` encodes the canonical mammalian guanylate
kinase/GMP kinase, a nucleoside monophosphate kinase that transfers phosphate
from ATP to GMP to generate ADP and GDP.  The mouse enzyme structure directly
supports this GMP + ATP to GDP + ADP chemistry and places GUK1 in the NMP kinase
fold family (Sekulic et al. 2002, DOI `10.1074/jbc.M204668200`,
PMID `12036965`).  The gene is therefore a guanine-nucleotide supply enzyme, not
a MAGUK scaffold or a signaling pseudokinase.  Severe biallelic human GUK1
deficiency was recently shown to impair cytosolic/mitochondrial nucleotide
handling, unbalance mitochondrial dNTP pools, and cause mtDNA depletion/deletion
disease (Hidalgo-Gutierrez et al. 2024, DOI `10.1002/ana.27071`,
PMID `39230499`).

That external biology makes a nonzero effect plausible in principle: loss of
GUK1 could lower GDP/GTP or dGDP/dGTP supply deeply enough to elicit a metabolic
or mitochondrial stress response.  It is imperfectly matched, though, because
the Perturb-seq assay used acute sparse AAV-CRISPR at P16 in postmitotic
neurons and the average per-guide mRNA decrease is modest.  It does not model
a germline biallelic enzyme deficiency, proliferating cultured cells, muscle, or
lymphocytes.

**Same-experiment `Guk1` coverage.**  The Distributed Agents target graph had no
`Guk1`-centered Finding, Claim, or explicit comparator reference.  I therefore
did not have an internally curated `Guk1` expression module or direct
same-experiment analog and had to reason from pathway-adjacent non-held-out
perturbations.

**Most relevant purine analogs.**

The cleanest represented purine/nucleotide enzyme neighbors were `Nt5c2` and
`Adk`.

| training perturbation | focal `n_degs` | focal min `pvals_adj` | focal matched perturbed cells | relationship to `Guk1` |
| --- | ---: | ---: | ---: | --- |
| `Nt5c2` | 0 | 1.000 | 205 | Cytosolic 5-prime nucleotidase acting on IMP/GMP pools; nearest available GMP/IMP turnover analog, but it dephosphorylates rather than phosphorylates monophosphates. |
| `Adk` | 0 | 0.203 | 186 | Adenosine kinase in purine salvage and adenosine/AMP control; same broad purine economy, but not guanine-specific. |

The same-experiment corpus was directly informative here.  `Nt5c2:F002` states
that `Nt5c2` perturbation did not induce AMPK/mTOR/ISR/p53 or purine-enzyme
transcriptional programs, arguing that nucleotide-pool imbalance did not become
a cell-wide stress in the postmitotic NeuN+ nuclear RNA readout.  `Nt5c2:F004`
contrasts `Nt5c2` and `Adk` and reports that `Adk` was transcriptionally silent
across all recovered cell groups.  `Adk:F003` similarly reports that represented
cAMP, phosphodiesterase, purine, and methylation-node perturbations failed to
phenocopy `Adk`.

In the focal raw DE table, both of these closer analogs were completely flat:
`Nt5c2` had 17,259 measured rows with no adjusted p-value below 1, and `Adk`
had a best adjusted p-value of only 0.203.  This is stronger evidence for zero
than a mere lack of many DEGs; there were no borderline focal purine-response
genes that would make a prediction of a few DEGs compelling.

**Cyclic-nucleotide and downstream boundary perturbations.**

Guanine nucleotides also feed cGMP, and adenosine biology can feed cAMP, so I
checked the represented guanylyl cyclases and phosphodiesterases rather than
assuming they were equivalent to `Guk1`.

| training perturbation | focal `n_degs` | focal min `pvals_adj` | relationship to `Guk1` |
| --- | ---: | ---: | --- |
| `Gucy2c` | 0 | 1.000 | Guanylyl cyclase receptor; cyclic-GMP production, far downstream of GDP/GTP supply. |
| `Gucy2e` | 0 | 1.000 | Guanylyl cyclase receptor; photoreceptor-biased biology, distant from thalamic glutamatergic GUK1 demand. |
| `Pde1c` | 0 | 0.180 | cAMP/cGMP phosphodiesterase. |
| `Pde4b` | 0 | 0.922 | cAMP phosphodiesterase. |
| `Pde4d` | 0 | 1.000 | cAMP phosphodiesterase. |
| `Pde10a` | 0 | 0.304 | Dual-substrate PDE with a known striatal cAMP/cGMP role. |

The induced Distributed Agents topology among these genes was connected, but the edges
mostly represented explicit "did not phenocopy" Findings or response-boundary
Claims, not a shared active response.  For example, `Pde10a:F003` says that
represented PDE and dopamine/cAMP/PKA pathway perturbations did not phenocopy
`Pde10a` in a striatal-associated group, and the same target has a compact
`Scg2`/`Crem` effect outside this focal cell group.  In `151 TH Prkcd Grin2c
Glut`, however, all six cyclic-nucleotide targets above had `n_degs = 0`.  I
therefore used them as counterexamples against propagating a broad
cyclic-nucleotide response into `Guk1`.

Other cAMP/CREB and purine-adjacent nodes in the same focal count table were
also small or flat: `Adcy1 = 0`, `Adcy3 = 0`, `Adcy5 = 0`, `Dnmt3a = 0`,
`Drd2 = 0`, `Drd5 = 0`, `Gnal = 0`, `Gnas = 0`, `Prkaca = 1`,
`Prkar1a = 1`, and `Creb1 = 10`.  These are weaker mechanistic matches than
`Nt5c2`/`Adk`, but they further show that this focal cell group is not turning
single perturbations of every nucleotide-linked signaling node into a broad DEG
signature.

**Zero/nonzero call and point estimate.**

I predict no FDR-significant genes for `Guk1` in the focal cell group:

- The nearest in-library purine enzyme analogs, `Nt5c2` and `Adk`, were zero in
  the same focal endpoint and were also described by the same-experiment corpus
  as buffered rather than as hidden nucleotide-stress responders.
- More distant cGMP/cAMP pathway perturbations were also zero in the focal
  group and often served as non-phenocopy counterexamples in the internal
  corpus.
- The external literature supports a possible effect only after deeper or
  chronic GUK1 deficiency.  It does not override the matched P16-to-P37/P44
  evidence that sparse single-enzyme nucleotide perturbations usually remain
  below the nuclear mRNA FDR threshold in postmitotic neurons.
- I did not assign `1`, because a lone self-transcript call would require
  detectable `Guk1` RNA loss.  The two closest purine analogs failed to produce
  such a self call in this focal cell type, and the experiment's average mRNA
  downregulation is modest.

Final point prediction: `Guk1 = 0`.

## Limits of the reasoning

- There is no direct `Guk1` perturbation profile, no Distributed Agents `Guk1` Finding,
  and no close assayed paralog, so the prediction extrapolates from neighboring
  nucleotide enzymes rather than from a direct phenocopy.
- The closest assayed purine targets are imperfect.  `Nt5c2` reverses
  nucleotide phosphorylation, `Adk` is centered on adenosine/AMP rather than
  GMP/GDP, and guanylyl cyclases/PDEs report cyclic-nucleotide signaling rather
  than guanine nucleotide biosynthesis.
- snRNA-seq at a single chronic endpoint cannot measure GMP, GDP, GTP, dGTP,
  mitochondrial dNTP pools, editing efficiency, protein abundance, or selective
  loss of successfully edited cells.
- Human GUK1 deficiency involves different allelic depth and affected tissues.
  It shows that GUK1 can matter biologically, but it does not calibrate this
  exact sparse postnatal neuronal RNA endpoint.
