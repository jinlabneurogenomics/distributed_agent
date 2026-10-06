# Reasoning trace

## Question as interpreted

The held-out target list for this run contains a single requested perturbation:
`Thoc2`. I need to predict, for `151 TH Prkcd Grin2c Glut`, the integer
number of measured genes with `pvals_adj < 0.05` after acute AAV-PHP.eB
CRISPR-Cas9 loss of function.

I treated the endpoint as a screen-specific count of BH-significant 10x Flex
snRNA-seq abundance changes in surviving, matched nuclei. I did not interpret a
zero count for a related target as proof that the edit failed, and I did not use
germline or strong conditional knockouts as quantitative equivalents to this
P16-to-P37/44 sparse postmitotic assay.

## Sources used

- Input parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Input endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 238_Thoc2.csv]`
- Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the `Thoc1` and
  `Ddx39b` target contexts and the TREX/RNA-processing claim connecting
  `Thoc1`, `Ddx39b`, `Rnpc3`, and `Prpf6`.
- NCBI PubMed literature searches for THOC2/THO/TREX biology.

Key external references:

- Strasser et al. 2002, DOI `10.1038/nature746`, PMID `11979277`: defined the
  conserved TREX complex coupling transcription with mRNA export.
- Dufu et al. 2010, DOI `10.1101/gad.1898610`, PMID `20844015`: showed ATP-
  dependent UAP56 interactions with conserved export proteins during TREX
  assembly.
- Guria et al. 2011, DOI `10.1261/rna.2607011`, PMID `21525145`: described the
  mammalian/Drosophila TREX composition as the THO subcomplex, including
  THOC1, THOC2, THOC5, THOC6, THOC7, plus THOC3, UAP56/DDX39B, and
  ALY/THOC4, and showed that Thoc5 loss affects a selective export-dependent
  transcript subset rather than all transcripts equally.
- Chi et al. 2012, DOI `10.1093/nar/gks1188`, PMID `23222130`: showed that
  Aly, THO, and UAP56 are mutually required for efficient human TREX assembly
  on spliced mRNA.
- Kumar et al. 2015, DOI `10.1016/j.ajhg.2015.05.021`, PMID `26166480`, and
  Kumar et al. 2020, DOI `10.3389/fnmol.2020.00012`, PMID `32116545`: linked
  partial-loss THOC2 variants to neurodevelopmental disease and reported that
  some THOC2 variants reduce THOC2 stability with a flow-on effect on other
  TREX-complex subunits.
- Bhattacharjee et al. 2024, DOI `10.1038/s41467-024-45121-5`, PMID
  `38331934`: generated a mouse hypomorphic `Thoc2` deletion model and linked
  compromised THOC2/TREX function in brain development to R-loop accumulation,
  DNA damage, and cell death.

## Computations over the supplied dataset

I first confirmed that `Thoc2` is the only requested target in
`238_Thoc2.csv` and that it is absent from the 1,674 perturbations in the focal
training-count file. The focal endpoint is extremely sparse overall: 1,205 of
1,674 training perturbations have zero DEGs, the median is 0, the 75th
percentile is 1, but a small RNA-processing/proteostasis tail reaches hundreds
to thousands of DEGs.

I then queried the parquet for `151 TH Prkcd Grin2c Glut` and checked the
training perturbations that are mechanistically nearest to THOC2:

| training target | focal `n_degs` | matched perturbed nuclei | reason for comparison |
| --- | ---: | ---: | --- |
| `Thoc1` | 303 | 121 | Core THO/TREX subunit; the only represented THO subcomplex member |
| `Ddx39b` | 0 | 48 | UAP56/TREX helicase, but partly paralog-buffered and underpowered here |
| `Rnpc3` | 868 | 149 | strong RNA-processing/minor-spliceosome responder |
| `U2af2` | 828 | 222 | splice-acceptor machinery; broad RNA-processing stress comparator |
| `Cdc40` | 624 | 159 | spliceosome/Prp19-associated RNA-processing comparator |
| `Prpf6` | 454 | 72 | tri-snRNP spliceosome comparator |
| `Snrnp70` | 213 | 135 | U1 snRNP comparator with RNA-biogenesis convergence |
| `Hnrnpu` | 733 | 163 | broad nuclear RNP comparator |
| `Tpr` | 1768 | 114 | nuclear-pore mRNA-export-adjacent positive comparator |
| `Tardbp` | 210 | 153 | RBP counterexample; same broad class, weaker mechanistic match |

The focal `Thoc1` response itself has 303 BH-significant genes, 233 up and
70 down. Its top FDR genes include `Sart1`, `Sf3b2`, `Srrm2`, `Anxa6`,
`Gtf2i`, `Noc2l`, and `Kif1a`, matching the Distributed Agents corpus finding that
`Thoc1` produced a mixed THO/TREX-compatible RNA-biogenesis program rather
than a simple generic stress or apoptosis program.

To test whether the `Thoc1` focal signature was a private outlier or part of a
broader RNA-processing state, I intersected the 303 significant `Thoc1` genes
with every other target's significant set in the same focal group:

```sql
WITH focal AS (
  SELECT *
  FROM read_parquet(training_parquet)
  WHERE group_name = '151 TH Prkcd Grin2c Glut'
),
thoc AS (
  SELECT names, sign(logfoldchanges) AS thoc_sign
  FROM focal
  WHERE gene_target = 'Thoc1' AND pvals_adj < 0.05
),
all_sig AS (
  SELECT gene_target, names, sign(logfoldchanges) AS s
  FROM focal
  WHERE pvals_adj < 0.05
)
SELECT gene_target, count(*) AS thoc1_overlap,
       sum(CAST(s = thoc_sign AS int)) AS same_direction
FROM all_sig JOIN thoc USING (names)
GROUP BY gene_target;
```

The largest mechanistically interpretable same-direction overlaps with `Thoc1`
were `Rnpc3` with 115 overlapping DEGs, `Tpr` with 114, `Hnrnpu` with 78,
`U2af2` with 75, `Cdc40` with 60, `Snrnp70` with 62, and `Prpf6` with 49.
Most of these overlaps were same-direction, not sign-flipped. `Ddx39b` had no
FDR-significant genes in this exact focal group, so it contributed no focal
overlap despite sharing a TREX/splicing/export-sensitive response with `Thoc1`
in the Distributed Agents corpus for `191 MB P MY GABA`.

I also compared raw log-fold-change vectors among the same focal signatures.
`Thoc1` had positive Pearson correlations with the broad RNA-processing and
nuclear-transport comparators, including `Tpr` 0.687, `Hnrnpu` 0.685,
`Cdc40` 0.677, `Prpf6` 0.647, and `Ddx39b` 0.623. I treated those whole-vector
correlations only as weak corroboration because lowly expressed nonsignificant
features can carry extreme clipped fold changes; the FDR-overlap result is the
more endpoint-proximal evidence.

## Distributed Agents corpus evidence

The corpus had no direct `Thoc2` entry, no `Thoc2`-scoped finding, and no
`Thoc2` claim. The useful internal evidence therefore came from represented
neighbors:

- `Thoc1:F001` reports that acute `Thoc1` loss gave a sharply selective but
  broad neuronal response across a few cell groups, with 1,353 FDR-significant
  rows in the full same-experiment surface and strong activity in `151 TH
  Prkcd Grin2c Glut`.
- `Thoc1:F002` reports a THO/TREX-compatible RNA-biogenesis program: induced
  `Sart1`, `Sf3a3`, `Dhx38`, `Exosc10`, and `Ncbp1`, plus recurrent repression
  of mRNA-export/spliceosome genes such as `Nxf1`, `Rnpc3`, `Snrnp70`,
  `Srrm2`, and `Ddx17`.
- `Thoc1:F005` is an important negative control: the `Thoc1` neuronal
  signature did not show an overt p53/apoptosis, DNA-damage, UPR, or integrated
  stress program. I therefore did not scale `Thoc2` up to the largest lethal
  perturbations merely because THO/TREX can cause R-loops and DNA damage.
- `Thoc1:F006` and `Ddx39b:F003` show that the closest direct TREX accessory
  comparison, `Ddx39b`, converged with `Thoc1`, `Tpr`, and `U2af2` most
  clearly in `191 MB P MY GABA`, while `Ddx39b` was flat in `151 TH Prkcd
  Grin2c Glut`.

## Target-specific decision: `Thoc2`

The zero/nonzero decision was driven mainly by within-dataset `Thoc1`.
`Thoc2` encodes a core member of the same THO subcomplex, not a remote RNA
binding protein or a generic DEAD-box helicase. Human biochemical studies place
THOC2 within the UAP56/ALY/THO TREX unit on spliced mRNA, and THOC2 pathogenic
variants reduce stability of THOC2 and other TREX subunits, so a partial acute
loss of `Thoc2` should plausibly perturb the same mRNP export and nuclear RNA
handling pathway as `Thoc1`.

The exact count estimate was calibrated down from `Thoc1`'s 303 DEGs. The
reason is not that `Ddx39b` makes `Thoc2` look safe, but that the same screen
shows TREX-related perturbations are context- and target-specific: `Ddx39b`
had only 48 perturbed nuclei and 0 focal DEGs even though it is a TREX helicase
and does converge with `Thoc1` elsewhere. Broader spliceosome/nuclear RNP
perturbations often produced 200-900 focal DEGs, which says this thalamic group
is able to mount a large RNA-processing response, but those are less direct
analogs than `Thoc1` because they target splice-site recognition or snRNP
machinery rather than the THO scaffold itself.

I therefore predicted a clear positive response in the same order as, but
modestly below, `Thoc1`: 240 DEGs.

## Limits and extrapolation

- The strongest limitation is the absence of `Thoc2` itself from both the
  parquet and the Distributed Agents corpus; the prediction transfers from `Thoc1` and
  TREX literature rather than from any measured `Thoc2` guide behavior.
- `Thoc1` is a good same-complex analog but not interchangeable with `Thoc2`.
  The relative sensitivity of core THO subunits can differ, and the assay does
  not report THOC2 protein depletion or indel rates.
- `Ddx39b` is an imperfect counterexample. Its 0-DEG focal result could reflect
  paralog buffering by DDX39A/AREX, lower power from only 48 perturbed nuclei,
  weaker target engagement, or real cell-state specificity.
- The readout is 3-prime nuclear RNA abundance. It cannot see nuclear export
  flux directly, cytoplasmic retention, R-loops, DNA damage, protein
  destabilization, or alternative isoform changes.
- The final integer is approximate. The evidence strongly favors nonzero over
  zero, but distinguishing 150 from 300 DEGs is an extrapolation from a single
  THO-core training target.
