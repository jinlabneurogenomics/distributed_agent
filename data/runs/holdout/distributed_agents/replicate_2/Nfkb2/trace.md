# Task interpretation

The requested endpoint is a point prediction of `n_degs` for each held-out
perturbation in `151 TH Prkcd Grin2c Glut`, where `n_degs` is the count of
measured genes with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05`.
The only requested held-out target in
`[local file: 150_Nfkb2.csv]`
is:

```tsv
target_name
Nfkb2
```

I treated the task as a target-specific transfer problem: `Nfkb2` itself is
absent from both the training differential-expression parquet and the focal
training count CSV, so the prediction must come from biologically matched
training perturbations plus prior knowledge about NF-kappaB signaling. I used
the supplied 151-cell training counts as the exact endpoint for non-held-out
genes and the large parquet only for focal-cell expression-pattern support,
not to infer any hidden `Nfkb2` outcome.

# Sources

Local input data:

- `training_de_all_cell_groups.parquet`, the supplied per-gene DE table.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the exact focal
  `n_degs` values for 1,674 non-held-out targets.
- `150_Nfkb2.csv`, the one-row requested-target manifest.

Same-experiment semantic layer:

- Distributed Agents corpus MCP release
  `perturbai-july-260713-sourceguard-1773-v1`, queried for `Nfkb1`, `Chuk`,
  `Rel`, `Traf3`, `Map3k7`, and `Cd40`.
- Distributed Agents profile-neighbor runtime, run locally on the focal cell group over
  all 1,674 training targets with signed Wilcoxon `scores` as the profile
  value and `pvals_adj < 0.05` as the significance cutoff.

External mechanism checks:

- PubMed via the BioEval literature gateway for primary and review literature
  on Nfkb2/p100/p52 and noncanonical NF-kappaB.
- Xiao, Harhaj & Sun 2001, DOI `10.1016/S1097-2765(01)00187-3`, PMID
  `11239468`: NIK stimulates phosphorylation, ubiquitination, and processing
  of NF-kappaB2 p100 to p52.
- Senftleben et al. 2001, DOI `10.1126/science.1062677`, PMID `11520989`:
  IKKalpha/CHUK is required for a second NF-kappaB pathway based on NF-kappaB2
  processing rather than IkappaB degradation.
- Coope et al. 2002, DOI `10.1093/emboj/cdf542`, PMID `12374738`: CD40
  ligation induces NIK-dependent processing of p100 to p52 and delayed nuclear
  RelB:p52 dimers in B cells.
- Dejardin et al. 2002, DOI `10.1016/S1074-7613(02)00423-5`, PMID `12387745`:
  LTbetaR engages the NIK/IKKalpha/NF-kappaB2 branch to induce lymphoid
  organogenesis genes.
- He et al. 2006, DOI `10.1084/jem.20061166`, PMID `17015635`: TRAF3 loss
  constitutively activates the noncanonical pathway through NIK accumulation,
  and the early lethality of `Traf3` knockout mice is rescued by loss of
  NF-kappaB2 p100.
- Sun 2010, DOI `10.1038/cr.2010.177`, PMID `21173796`, and Sun 2012, DOI
  `10.1111/j.1600-065X.2011.01088.x`, PMID `22435551`: reviews of the
  noncanonical NF-kappaB pathway, emphasizing RelB:p52, NIK stabilization, and
  the TRAF-cIAP destruction complex.
- Paxian et al. 2002, DOI `10.1053/gast.2002.33651`, PMID `12055593`: in vivo
  evidence that NF-kappaB2 has essential immune/lymphoid-organ functions.
- Sarnico et al. 2009, DOI `10.1016/S0074-7742(09)85024-1`, PMID `19607980`:
  review of NF-kappaB dimers in neuronal survival and the context dependence
  of neuronal NF-kappaB activity.

# Computation

I first verified that the held-out target was absent from the training endpoint
table and that the focal table was zero-heavy but not all zero:

- 1,674 training targets.
- 1,205/1,674 targets had `n_degs = 0`.
- Median `n_degs` was `0`, the 75th percentile was `1`, the 95th percentile
  was `18`, and the largest responses were broad neuronal perturbations such
  as `Uba5` with 2,677 DEGs and `Tpr` with 1,768 DEGs.

I then selected NF-kappaB, TNFR, IL-1/TLR, TAK1/IKK, and stress-MAPK training
perturbations that are mechanistically adjacent to `Nfkb2` and looked up their
observed 151-cell `n_degs`. For exact focal expression support, I loaded only
the focal group and these candidate target rows from the parquet:

```python
expr = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
)
table = ds.dataset(parquet, format="parquet").to_table(
    columns=[
        "names",
        "gene_target",
        "scores",
        "logfoldchanges",
        "pvals",
        "pvals_adj",
        "n_pert_matched",
        "n_ctrl_matched",
    ],
    filter=expr,
)
```

For the six closest represented same-axis anchors
`Nfkb1`, `Chuk`, `Rel`, `Traf3`, `Map3k7`, and `Cd40`, I also computed
whole-profile Pearson/cosine neighborhoods in the focal cell group using
Wilcoxon score vectors over the 17,259 measured genes. All six anchors had
zero significant features. Their pairwise correlations were near zero
(`-0.0111` to `0.0451`), and their nearest all-training positive neighbors
were also weak: top whole-profile Pearson correlations were `0.0681` for
`Nfkb1`, `0.0610` for `Chuk`, `0.0821` for `Rel`, `0.1281` for `Traf3`,
`0.1063` for `Map3k7`, and `0.0601` for `Cd40`. I interpreted this as absence
of a coherent basal NF-kappaB-like expression pattern, not as positive evidence
for any of those weakly correlated neighbors.

# Nfkb2 analogs and prediction

## Biologically relevant training perturbations

`Nfkb2` encodes p100, the precursor of p52. The best-known noncanonical route
is receptor-driven stabilization of NIK/MAP3K14, phosphorylation of p100 by
IKKalpha/CHUK, and p100 processing to RelB:p52 transcriptional dimers. TRAF3
is a proximal negative regulator whose loss can release NIK and activate this
branch in lymphoid cells. That makes the represented targets `Chuk`, `Traf3`,
and the receptor-side `Cd40`/TNFRSF nodes especially informative for `Nfkb2`;
`Nfkb1` and `Rel` are the represented nuclear NF-kappaB subunits, but they are
less exact because the most diagnostic `Relb`, `Rela`, `Map3k14`, `Ikbkb`,
`Ikbkg`, `Nfkbia`, `Bcl3`, `Traf2`, `Traf5`, `Traf6`, `Birc2`, and `Birc3`
perturbations were not in the 1,674-target focal training table.

The focal training counts for the most relevant represented comparators were:

| training perturbation | focal n_degs | focal minimum adjusted p-value | perturbed nuclei | why it mattered for `Nfkb2` |
| --- | ---: | ---: | ---: | --- |
| `Nfkb1` | 0 | 1.0 | 181 | Closest represented NF-kappaB precursor/paralog; the Distributed Agents corpus reported no FDR<0.10 downstream genes in all recovered neuronal groups and flat `Rel`/`Chuk`/`Map3k7`/TLR/TNFR comparators. |
| `Chuk` | 0 | 0.727 | 156 | IKKalpha is the kinase that phosphorylates p100 for noncanonical processing; the corpus reported no FDR<0.10 response in any measured neuronal group. |
| `Rel` | 0 | 0.140 | 205 | Nuclear Rel-family comparator; its direct focal data had no FDR<0.05 genes and the corpus described no FDR<0.10 downstream response in any of 23 neuronal groups. |
| `Traf3` | 0 | 1.0 | 211 | TRAF3 restrains basal noncanonical NF-kappaB in immune cells by limiting NIK. Its loss should be an activating counterexample if this branch were tonically poised, but the focal and pan-neuronal surfaces were null. |
| `Cd40` | 0 | 1.0 | 226 | CD40 can induce NIK-dependent p100-to-p52 processing; its own perturbation and `Traf3`/`Map3k7`/`Chuk`/`Nfkb1`/`Rel` comparators were jointly flat in the corpus. |
| `Map3k7` | 0 | 1.0 | 160 | TAK1 links IL-1/TLR/TNF receptors to canonical IKK and JNK/p38; zero DE here supported the same basal receptor-to-kinase silence, though it is upstream of canonical rather than p52-specific signaling. |

Wider receptor and MAPK counterexamples were also quiet in the same focal
readout. `Tnfrsf1a`, `Tnfrsf11a`, `Tnfrsf13c`, `Tnfrsf4`, `Tnfrsf9`, `Tlr2`,
`Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`, `Il1r1`, `Il1rap`, `Map2k6`,
`Mapk9`, `Mapk1`, `Bcl2`, `C3`, `Cd14`, `Cyld`, `Eda`, and `Ager` all had
`n_degs = 0` in `151 TH Prkcd Grin2c Glut`.

## Reason for the zero/nonzero decision

The decision is driven mainly by same-experiment evidence. In the exact target
cell group, all represented proximal and downstream NF-kappaB-axis analogs had
zero genes at FDR 0.05, including the p100-processing kinase `Chuk` and the
same-family precursor `Nfkb1`. Their smallest adjusted p-values were generally
far above 0.05; for `Nfkb1`, `Traf3`, `Cd40`, and `Map3k7` the minimum focal
adjusted p-value was exactly 1.0, and `Chuk` also had no borderline signal
with minimum FDR 0.727.

The Distributed Agents corpus reinforced that this is not a peculiarity of the 151
thalamic group. `Nfkb1` was reported as having 0 downstream FDR<0.10 genes in
all recovered neuronal groups; `Chuk` and `Traf3` were pan-neuronal FDR-null;
`Rel` had no robust response in any of 23 neuronal groups; and the corpus'
shared claim was that represented TNFR/TLR/IL-1/CD40-to-TAK1/IKK/NF-kappaB/JNK/
p38 perturbations were broadly transcriptionally silent as a basal module in
unchallenged postnatal NeuN-positive neurons.

The external biology makes those local zeros mechanistically relevant to
`Nfkb2` rather than merely family-name matches. `Nfkb2` is activated when
NIK and IKKalpha induce p100 processing to p52, downstream of specific TNFR
superfamily receptors such as CD40 and LTbetaR, and TRAF3 loss is a canonical
route to constitutive NIK/noncanonical NF-kappaB activity in lymphoid settings.
If juvenile thalamic glutamatergic neurons carried a tonic noncanonical
NF-kappaB program, `Chuk` or `Traf3` would be plausible perturbations to reveal
it. They did not.

The biological interpretation is therefore that this pathway is present in the
genome but not tonically deployed as a detectable autonomous mRNA program in
homeostatic, postmitotic, NeuN-enriched neurons 3-4 weeks after P16 sparse
CRISPR loss. The immune and lymphoid phenotypes of NF-kappaB2 are real, but
they sit in B cells, lymphoid-organ stromal contexts, and ligand-stimulated
TNFR-family signaling that are absent or strongly under-sampled here.

Prediction for the only held-out target:

| target | predicted n_degs | rationale |
| --- | ---: | --- |
| `Nfkb2` | 0 | Zero focal counts for `Nfkb1`, `Chuk`, `Rel`, `Traf3`, `Cd40`, `Map3k7`, and wider TNFR/TLR/stress-MAPK comparators; no coherent same-axis score-neighborhood in the focal data; literature places p100/p52 activity downstream of stimulus-gated NIK/IKKalpha signaling rather than as a constitutive young-neuron transcriptional dependency. |

# Limits

- The closest missing comparators are important. `Relb`, `Rela`,
  `Map3k14`/NIK, `Ikbkb`, `Ikbkg`, `Nfkbia`, `Bcl3`, and TRAF/cIAP complex
  members were held out or absent from this training slice, so the prediction
  extrapolates from `Chuk`, `Traf3`, `Nfkb1`, `Rel`, receptor-side nodes, and
  TAK1 rather than from a complete noncanonical complex.
- All in-dataset analogs used here were null in the focal group, which is
  strong for a zero/nonzero call but weak for estimating a small nonzero count;
  if `Nfkb2` has a p100-inhibitor-specific effect that its represented
  neighbors lack, this analysis would miss it.
- The assay measured steady-state nuclear RNA in recovered neurons. It did not
  measure DNA indels, p100/p52 protein processing, NIK stabilization, RelB
  nuclear translocation, acute receptor stimulation, microglia, astrocytes,
  endothelium, B cells, or inflammatory disease states.
- Null self-transcript changes were not used as editing-failure evidence.
  Sparse CRISPR indels can leave nuclear mRNA abundance nearly unchanged.
