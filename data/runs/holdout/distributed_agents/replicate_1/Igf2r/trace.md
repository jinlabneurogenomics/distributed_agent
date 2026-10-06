# Prediction target

The held-out readout is the integer `n_degs` for each requested perturbation in
`151 TH Prkcd Grin2c Glut`: the number of measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in perturbed nuclei
versus matched controls. The requested manifest contained exactly one held-out
mouse perturbation, `Igf2r`. I treated the manifest order as the required output
order and did not treat it as a rank.

I resolved one ambiguity conservatively: `n_degs` is an assay endpoint for
single-nucleus DE breadth among recovered postnatal neuronal nuclei, not a
direct measure of viability, absolute lysosomal flux, editing efficiency, or
biological importance. Thus the training count CSV is direct evidence for this
endpoint for non-held-out perturbations; the all-cell differential-expression
Parquet is direct evidence for the signatures underlying those training counts;
and external gene-function knowledge is prior evidence for choosing which
training perturbations are mechanistically informative for held-out `Igf2r`.

# Sources used

- Declared Perturb-seq DE Parquet:
  `training differential-expression dataset`.
  I queried the exact focal cell group and the mechanistic analog targets below.
- Declared focal training endpoint CSV:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  It contained 1,674 non-held-out biological perturbations; `Igf2r` was absent.
- Declared requested-target CSV:
  `single-target request for Igf2r`.
  It contained the single held-out target `Igf2r`.
- Run-local generated context and guards: `task_bindings.json`,
  `dataset_context.md`, `dataset_context.json`, `coverage.json`, and
  `measurement_registry.json`.
- Internal same-experiment corpus: July PerturbAI ledger/corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. I used it only as packaged
  interpretation of the same Perturb-seq experiment, not as independent
  replication. It had no report for `Igf2r`; I inspected compact Findings for
  `Rab7`, `Vps35`, and `Cltc` to interpret measured non-held-out analogs.
- External literature from PubMed through `bioeval_literature.search_pubmed`:
  Ghosh, Dahms and Kornfeld 2003, DOI `10.1038/nrm1050`, PMID `12612639`;
  Brown, Jones and Forbes 2009, DOI `10.1016/S0083-6729(08)00625-0`,
  PMID `19251056`; Arighi et al. 2004, DOI `10.1083/jcb.200312055`,
  PMID `15078903`; Cui et al. 2018, DOI `10.1083/jcb.201806153`,
  PMID `30559172`; Coutinho, Prata and Alves 2012,
  DOI `10.1016/j.ymgme.2012.07.012`, PMID `22884962`; Zhu et al. 2001,
  DOI `10.1126/science.1060896`, PMID `11387476`; Stockli, Honing and
  Rohrer 2004, DOI `10.1074/jbc.M313525200`, PMID `15044437`;
  Stahlschmidt et al. 2014, DOI `10.1074/jbc.M113.535211`,
  PMID `24407285`.

# Dataset calculations

The training response was sparse. In the focal training CSV, the median count
was 0, the 75th percentile was 1, the 90th percentile was 2, the 95th percentile
was 18, and 469 of 1,674 targets had any DEG at all.

For candidate analogs, I recomputed focal DEG counts from the Parquet as a
guardrail:

```sql
SELECT gene_target,
       sum(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS n_degs_calc
FROM read_parquet(training_de_all_cell_groups.parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

The recomputed counts matched the training endpoint for the analogs I used:

| analog | focal n_degs | matched perturbed nuclei | endpoint relationship to Igf2r |
|---|---:|---:|---|
| Igf1r | 0 | 112 | IGF receptor branch counterexample |
| Tgfbr1 | 0 | 180 | growth-factor receptor counterexample |
| Tgfbr2 | 0 | 298 | TGF-beta receptor counterexample |
| Tgfbr3 | 0 | 164 | TGF-beta receptor counterexample |
| Sort1 | 0 | 124 | alternative lysosomal cargo receptor |
| Lamp2 | 0 | 203 | lysosomal/autophagy membrane target |
| Manba | 0 | 130 | lysosomal hydrolase target |
| Ctsb | 1 | 207 | lysosomal hydrolase target; its only focal hit was Ctsb itself |
| Ap1s2 | 0 | 140 | clathrin adaptor branch |
| Ap1b1 | 1 | 143 | clathrin adaptor branch; its only focal hit was Ap1b1 itself |
| Cltc | 3 | 32 | broad clathrin coat branch |
| Vps35 | 17 | 133 | retromer receptor-recycling branch |
| Vps54 | 31 | 161 | endosome-to-Golgi/GARP branch |
| Rab7 | 501 | 215 | late-endosome/lysosome stress counterexample |

The expression-pattern evidence also separated a weak receptor/adaptor branch
from a global endolysosomal stress branch. `Cltc` had only 3 focal DEGs
(`Rbms1`, `Ero1b`, `Gabra4`) despite clathrin's broad role. `Ap1b1`, `Ap1s2`,
`Sort1`, `Lamp2`, and `Manba` did not create a downstream focal signature.
`Vps35` had 17 focal hits, including its own transcript plus `Atp2a2`,
`Grin2b`, `Brsk1`, and a small set of membrane/synaptic genes, and the July
corpus described this as a selective retromer response rather than a bulk
lysosomal program. `Rab7`, by contrast, had 501 focal DEGs and induced
vacuolar-ATPase, lysosomal hydrolase, cholesterol, ISR/autophagy, and
proteasome transcripts; that broad program is a counterexample showing what
late endosomal collapse looks like in this assay, not a good same-size analog
for perturbing one cargo receptor.

# Igf2r reasoning

`Igf2r` encodes the cation-independent mannose-6-phosphate receptor
CI-MPR/MPR300. Its major cell-biological job is to bind mannose-6-phosphate
tagged acid hydrolases in the Golgi/TGN and traffic them to endosomes and
lysosomes; it also binds IGF-II, giving it a growth-factor-regulatory role
separate from lysosomal enzyme transport (Ghosh et al. 2003; Brown et al.
2009).

That biology points first to the M6P receptor and cargo-sorting axis, but the
closest receptor paralog `M6pr` was not in the training endpoint file. The
nearest measured branches were:

- `Sort1`, an alternative M6P-independent lysosomal targeting receptor
  (Coutinho et al. 2012), with 0 focal DEGs.
- `Ap1b1` and `Ap1s2`, AP-1 adaptor components for clathrin-coated TGN/endosome
  traffic, with 1 and 0 focal DEGs. AP-1 and GGA adaptors sort mannose
  6-phosphate receptors through acidic/dileucine cytosolic motifs and connect
  them to clathrin coats (Zhu et al. 2001; Stockli et al. 2004;
  Stahlschmidt et al. 2014).
- `Cltc`, the clathrin heavy chain, with 3 focal DEGs. This is farther upstream
  and much broader than CI-MPR because clathrin is used for many neuronal
  membrane-trafficking routes, yet it still produced only a tiny focal
  signature.
- `Vps35`, the retromer cargo-selective subunit, with 17 focal DEGs. Retromer
  binds the CI-MPR tail and retrieves CI-MPR from endosomes, preventing its
  lysosomal turnover; `Vps35` KO causes CI-MPR trafficking and lysosomal
  hydrolase defects in cell systems (Arighi et al. 2004; Cui et al. 2018).
  `Vps35` is mechanistically related to `Igf2r`, but it should be at least as
  strong and more pleiotropic because it recycles multiple cargos, so its
  17-DEG count is an upper-bound-like weak positive rather than a direct
  expectation for `Igf2r`.

The high-count counterexamples all argue against mapping `Igf2r` to the full
`Rab7`-like lysosomal stress state. `Rab7` sits at the late-endosome switch and
touches HOPS, retromer recruitment, degradative maturation, sterol trafficking,
and autophagic stress; its 501 focal DEGs include `Lamp2`, `Ctsd`, `Ctsa`,
`Hexb`, `Gaa`, `Atp6v0*`, `Atp6v1*`, `Sqstm1`, and `Map1lc3b`. Loss of one M6P
cargo receptor is upstream and partially redundant with `M6pr`, sortilin, and
LIMP-2 routes for lysosomal targeting, so the causal chain is expected to be:

`Igf2r` CRISPR loss of function -> reduced CI-MPR cargo sorting and IGF-II
binding -> partial impairment of a subset of lysosomal hydrolase delivery and
receptor recycling -> compensation through parallel receptors and retromer/AP
machinery -> surviving thalamic glutamatergic nuclei either remain below the
FDR threshold or show only self/gene-sparse changes.

The growth-factor branch is also not a reason to predict a broad focal
signature. `Igf1r`, `Tgfbr1`, `Tgfbr2`, and `Tgfbr3` all had 0 focal DEGs, and
postmitotic mosaic neurons at P37-P44 are less likely to convert a partial
acute receptor perturbation into a large cell-cycle or growth transcriptome
than a developmental or proliferative model would.

I therefore predicted a true-zero endpoint, `0` DEGs. The decision is driven
mostly by within-dataset evidence: the most receptor-like non-held-out
perturbations were 0-1 DEG, the AP-1/clathrin branch was 0-3 DEGs, and even
retromer was only 17 DEGs in this cell group. External literature was used to
decide that those measured perturbations were the relevant analogs and to
downgrade `Rab7` as too broad and too downstream.

# Limits

The prediction is extrapolative because neither `Igf2r` nor its closest paralog
`M6pr` was in the training endpoint file, and no July same-experiment report was
available for `Igf2r`. The focal Parquet rows for non-held-out targets contain
only DE summaries among recovered nuclei; they do not measure lysosomal enzyme
missorting, IGF-II uptake, protein loss, or pre-harvest selection. A small
positive `Igf2r` response is plausible if this neuronal class depends unusually
strongly on CI-MPR-mediated hydrolase delivery, but the measured AP-1,
clathrin, Sort1, lysosomal hydrolase, and TGF/IGF receptor perturbations keep
that effect below the nearest robust training responses.
