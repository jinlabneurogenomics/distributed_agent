# Sec31a DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested held-out target list contains one gene:

- `Sec31a`

I interpreted the requested endpoint as the exact focal-cell count in
`151 TH Prkcd Grin2c Glut`: the number of measured genes with
`pvals_adj < 0.05` after Benjamini-Hochberg correction in the Wilcoxon
rank-sum DE table. `Sec31a` was absent from both supplied training files, so I
used only other perturbations in the parquet and CSV to calibrate the expected
breadth of a sparse postnatal neuronal AAV CRISPR loss-of-function response.

## Sources

- Supplied focal endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This gave the observed `n_degs` for 1,674 non-held-out perturbations.
- Supplied DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I queried rows from the focal cell group for COPII, ER-Golgi, and
  ER-stress comparators and inspected their adjusted p-values and marker-gene
  directions.
- Same-experiment semantic layer:
  Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  I used its curated `Sec23a`, `Sar1b`, `Tfg`, `Copa`, and `Hspa5` findings and
  the claim `claim:6ad7068adcc1a43c2bbe`, which summarizes that the represented
  `Tfg`/`Sec23a`/`Sar1b` COPII-initiation and ER-exit branch was
  transcriptionally buffered whereas `Sec63` was ER-stress positive.
- Same-dataset profile tools:
  Distributed Agents runtime profile comparison over 18 nominated ER-Golgi and
  ER-stress targets in `151 TH Prkcd Grin2c Glut`, with
  `logfoldchanges` as the signed profile and `pvals_adj < 0.05` defining
  significant features.
- External literature for biological role:
  Haucke 2003, DOI `10.1016/s0962-8924(02)00011-9`, PMID `12559754`;
  Townley et al. 2008, DOI `10.1242/jcs.031070`, PMID `18713835`;
  la Cour et al. 2013, DOI `10.1371/journal.pone.0075309`, PMID `24069399`;
  Hutchings et al. 2018, DOI `10.1038/s41467-018-06577-4`, PMID `30297805`;
  Shibata 2018, DOI `10.1080/09168451.2018.1525274`, PMID `30259798`;
  Tobias et al. 2024, DOI `10.1007/s12020-024-03701-x`, PMID `38400880`.

## Computation over the supplied data

The focal training distribution was zero inflated: 1,205/1,674 training
perturbations had `n_degs = 0`, the median was 0, the 75th percentile was 1,
and broad responses were rare outliers.

I first nominated mechanistic comparators from COPII/ER exit and ER-Golgi
traffic, then looked up their focal observed counts:

| training perturbation | focal `n_degs` | reason for comparison |
|---|---:|---|
| `Sec23a` | 0 | inner COPII coat; binds SAR1/SEC24 and couples to SEC13/SEC31 outer coat |
| `Sar1b` | 0 | SAR1 family COPII GTPase; initiates ER-export coat assembly |
| `Tfg` | 0 | ER-exit scaffold that organizes COPII carriers downstream of coat formation |
| `Copa` | 0 | COPI retrograde coat; indirect ER-Golgi counterexample |
| `Copg1` | 1 | COPI same-pathway counterexample |
| `Cog4` | 0 | conserved oligomeric Golgi tethering |
| `Cog5` | 0 | conserved oligomeric Golgi tethering |
| `Stx5a` | 0 | ER-Golgi SNARE traffic |
| `Trip11` | 0 | Golgi tether/large-cargo ER-Golgi axis |
| `Tmem165` | 0 | Golgi ion/glycosylation homeostasis |
| `Ssr4` | 1 | ER translocon associated |
| `Vcp` | 2 | ERAD/proteostasis adjacent |
| `Sec63` | 11 | ER translocation/BiP cofactor positive boundary |
| `Hspa5` | 5 | BiP; positive ER folding/ERAD boundary |
| `Gfpt1` | 311 | N-glycan/hexosamine stress positive boundary |
| `Atp2a2` | 187 | ER calcium stress positive boundary |
| `Dhdds` | 116 | dolichol/N-glycosylation stress positive boundary |
| `Manf` | 3 | small ER-chaperone response |

For the marker-gene slice I used a structured PyArrow filter rather than
string parsing:

```python
flt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
    & pc.field("names").isin(markers)
)
```

That query confirmed that the COPII analogs were not missing a subthreshold
canonical UPR/ERAD module. In the focal cell group, `Sec23a`, `Sar1b`, and
`Tfg` had 307, 112, and 118 perturbed nuclei matched against 23,679 controls;
each had zero FDR-significant genes. `Hspa5`, `Hsp90b1`, `Pdia4`, `Derl3`,
`Creld2`, `Herpud1`, `Asns`, `Ddit3`, `Chac1`, and `Xbp1` were all
non-significant after `Sec23a`, `Sar1b`, and `Tfg`, with adjusted p-values of
1.0 for the representative `Hspa5` and `Chac1` rows in all three perturbations.
There was also no focal induction of the measured COPII transcripts `Sar1a`,
`Sar1b`, `Sec13`, `Sec23a`, `Sec23b`, `Sec24a`, `Sec24b`, `Sec24c`, `Sec24d`,
or `Sec31b`.

The same marker genes were detectable in matched positive controls:

- `Gfpt1` in the focal class up-regulated `Herpud1`, `Asns`, `Hspa5`, `Chac1`,
  `Hsp90b1`, `Creld2`, `Xbp1`, `Derl3`, and `Pdia4` at FDR < 0.05 and produced
  311 total DEGs.
- `Dhdds` up-regulated `Hspa5`, `Ddit3`, `Hsp90b1`, `Herpud1`, `Asns`,
  `Creld2`, `Xbp1`, `Derl3`, and `Pdia4` at FDR < 0.05 and produced 116 DEGs.
- `Atp2a2` produced 187 DEGs, including `Ddit3`, `Chac1`, `Xbp1`,
  `Herpud1`, `Hspa5`, `Asns`, and `Slc38a2`.
- `Sec63` produced an 11-gene tail that included `Hspa5`, `Canx`, `Hyou1`,
  and `Chac1`, even with only 72 matched perturbed nuclei.
- `Hspa5` itself had only 47 matched perturbed nuclei but still called 5 genes.

I then used the Distributed Agents runtime profile comparison as a check on the full
log-fold-change surface of the nominated ER-Golgi cohort. In the focal class,
`Sec23a`, `Sar1b`, and `Tfg` were all classified as
`no_significant_features`, whereas `Sec63` had 11 significant features and
`Hspa5` had 5. The whole-profile correlations among flat signatures are not
mechanistic evidence, because weak all-gene vectors are dominated by
low-amplitude noise and pseudocount behavior; I used this artifact only to
verify response activity and to ensure the positive ER-stress comparators were
not being collapsed into the zero-COPII set.

## Target-specific reasoning

### `Sec31a`

`SEC31A` is a core outer-coat COPII protein. Classical COPII assembly begins
with SAR1, adds the SEC23-SEC24 inner coat, and then recruits the SEC13-SEC31
outer coat for ER export; SEC13/SEC31 bridges and organizes SAR1/SEC23/SEC24
inner-coat units, and biochemical work shows calcium-dependent regulators such
as ALG-2 can bind the proline-rich region of Sec31A and stabilize the
Sec23/Sec31A relationship. Those roles are well established by the COPII
literature cited above.

The most relevant measured perturbations were not broad responders. `Sec23a`
is upstream in the same COPII coat, `Sar1b` is the small GTPase that starts
COPII assembly, and `Tfg` acts at ER exit sites connected to COPII carrier
organization. All three had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`. The
Distributed Agents corpus independently curated the same pattern: `Sec23a:F003`,
`Sar1b:F004`, and `Tfg:F003` support the same release claim that represented
COPII-initiation/ER-exit nodes were transcriptionally buffered in this
postnatal neuronal screen. `Tfg` is not a coat subunit and `Sar1b` is not the
only SAR1 paralog, so these are imperfect analogs, but their concordant focal
zeros argue that perturbing one node of the basal COPII route was usually
absorbed without a durable nuclear RNA program.

The counterexamples point the same way rather than overturning that inference.
`Sec63`, `Hspa5`, `Gfpt1`, `Atp2a2`, and `Dhdds` show that the focal cell type
could call an ER folding/ERAD/ISR state, including chaperones and amino-acid
stress genes, when the perturbation directly hit ER-client folding,
N-glycosylation, or ER calcium. Those biology branches are adjacent to
secretion but not the same as an outer COPII structural subunit in a sparse,
survivor-conditioned postmitotic neuron. The COPI, COG, Golgi, and SNARE
comparators were also zero or singletons (`Copa = 0`, `Copg1 = 1`,
`Cog4 = 0`, `Cog5 = 0`, `Stx5a = 0`, `Trip11 = 0`, `Tmem165 = 0`), which argues
against a common ER-Golgi trafficking collapse signature in this readout.

External knowledge adds two caveats. First, complete loss of an essential
COPII outer coat can be severe in development: `Sec31a` CRISPR disruption was
reported to be homozygous embryonic lethal in mice by Tobias et al. 2024.
Second, mammalian SEC31A has specialized regulation for bulky cargo such as
collagen, and SEC13/SEC31 coupling is important for collagen secretion and
craniofacial development in systems with high extracellular-matrix demand
(Townley et al. 2008). Those settings do not map cleanly onto P16 sparse
knockout in recovered NeuN-positive thalamic neurons, which are not assayed for
large-cargo secretion, edited-cell loss, or protein trafficking. The screen's
own evidence therefore gets more weight than developmental lethality.

The strongest within-dataset transfer is from the `Sec23a`/`Sar1b`/`Tfg`
triple-zero COPII branch, with ER-stress positive controls serving as a
boundary. Because those analogs had no focal FDR genes and no focal UPR/ERAD
marker induction, I predict that `Sec31a` will also be transcriptionally
buffered at the FDR < 0.05 endpoint.

Prediction: `Sec31a -> 0` DEGs.

## Limits

- No outer COPII subunit perturbation was directly observed in the training
  table: `Sec31a` was held out, and `Sec13`, `Sec31b`, and `Sec24` family
  members were not available as focal training targets. The prediction
  extrapolates from the SAR1/SEC23/Tfg side of ER exit to the SEC31A outer
  coat.
- The assay is an acute, mosaic, P16-to-P37/44 neuronal CRISPR readout over
  surviving nuclei. It cannot rule out transient secretion defects, local
  axonal or dendritic trafficking phenotypes, large-cargo export defects,
  protein-level compensation, or selective loss of successfully edited cells.
- Whole-profile similarities among flat perturbations are weak evidence; I used
  them only to audit the presence or absence of FDR-level activity. The
  predicted zero is driven primarily by exact focal DEG counts and marker-gene
  nulls of mechanistic COPII and ER-Golgi analogs.
- The external Sec31A literature is dominated by developmental, high-secretory,
  collagen, endocrine, or non-neuronal contexts. Those data establish that
  SEC31A is a real COPII component but do not imply a broad durable snRNA-seq
  response in postmitotic thalamic neurons under partial sparse knockout.
