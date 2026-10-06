## Question

The requested readout is the integer number of genes with `pvals_adj < 0.05`
after perturbing each held-out target in `151 TH Prkcd Grin2c Glut` neurons.
The only target in
`[local file: 218_Sos2.csv]`
is:

```tsv
target_name
Sos2
```

`Sos2` was absent from both supplied training inputs, so I treated this as a
single-target transfer problem. The endpoint is an assay-specific BH/Wilcoxon
count, not a statement that complete SOS2 loss has no biochemical consequence.
When the Distributed Agents corpus used an FDR < 0.10 exploratory statement, I used it
only as expression-pattern context; the final count calibration used the task
definition, `pvals_adj < 0.05`.

## Sources

- Training DEG endpoint file:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Distributed Agents same-experiment corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents run-local profile comparison over focal-cell Wilcoxon score
  signatures for Ras/MAPK candidates
- PubMed via NCBI E-utilities for external SOS/RAS biology

Key external citations:

- Qian et al., 2000, EMBO J, DOI `10.1093/emboj/19.4.642`: Sos1 null
  mouse cells can use Sos2 for short EGF responses, but Sos1 supports more
  durable EGFR/Shc coupling and long-term ERK output.
- Esteban et al., 2000, Mol Cell Biol, DOI
  `10.1128/MCB.20.17.6410-6413.2000`: Sos2 catalytic-domain knockout mice
  are viable, fertile, and grossly histologically normal, unlike embryonic
  lethal Sos1 mutants.
- Baltanas et al., 2013, Mol Cell Biol, DOI `10.1128/MCB.01026-13`:
  individual Sos1 or Sos2 knockout in adult mice is much milder than combined
  Sos1/Sos2 ablation, demonstrating redundancy and a dominant contribution of
  Sos1 in lymphocyte development.
- Sheffels et al., 2018, Sci Signal, DOI `10.1126/scisignal.aar8371`: Sos2
  can have context-specific functions in mutant KRAS-driven MEF and cancer-cell
  transformation through PI3K/AKT, so SOS2 is not biologically inert; that is a
  proliferative oncogenic Ras context rather than resting postmitotic neurons.
- Baltanas et al., 2020, Biochim Biophys Acta Rev Cancer, DOI
  `10.1016/j.bbcan.2020.188445`, and Baltanas et al., 2021, Int J Mol Sci,
  DOI `10.3390/ijms22126613`: reviews summarizing SOS1/SOS2 as broadly
  expressed Ras/Rac GEFs with substantial redundancy and generally stronger
  SOS1 phenotypes.
- Yamamoto et al., 2015, J Med Genet, DOI
  `10.1136/jmedgenet-2015-103018`: activating SOS2 variants can cause
  Noonan syndrome, reinforcing that developmental gain-of-function Rasopathy
  alleles should not be equated with the present postnatal loss-of-function
  screen.

## Computation

I first read the 1,674-target training count CSV to calibrate the endpoint. The
focal distribution is highly zero-inflated: median 0 DEGs, 75th percentile
1 DEG, 90th percentile 2 DEGs, and mean 14.1 because of a small tail of very
broad transcriptional regulators. Thus a zero prediction is the modal outcome
and needs to be rejected only by a close in-dataset positive analog.

For direct expression evidence, I queried the focal cell group in the parquet
for represented Ras/MAPK, RTK, and Ras-regulator training targets. The parquet
is grouped by `group_name`; `151 TH Prkcd Grin2c Glut` spans row groups 546
through 580, so I read those row groups, filtered on `group_name`, then counted
`pvals_adj < 0.05` per `gene_target` and sorted each candidate signature by
adjusted p value.

I also ran a run-local `profile_compare` over focal-cell Wilcoxon `scores` for
`Sos1`, `Braf`, `Map2k1`, `Map2k2`, `Mapk1`, `Raf1`, `Hras`, `Kras`,
`Ptpn11`, `Shoc2`, `Ntrk2`, `Spred1`, `Spred2`, and `Rapgef2`. This compared
the signed whole-gene score vectors and the significant-gene intersections
inside the nominated Ras/MAPK cohort.

## Training Analogs And Counterexamples

**Closest paralog: Sos1.** `Sos1` is the most direct in-dataset analog for
`Sos2` because SOS1 and SOS2 are homologous Ras/Rac GEFs coupled to RTK/Grb2
signaling. `Sos1` had `0` focal DEGs at FDR 0.05. Its best row in the focal
parquet was `Cul7` up, log2FC `1.004961`, adjusted `p = 0.077842`; every
gene remained above the requested FDR threshold. The Distributed Agents corpus likewise
reported `Sos1:F001/F002`: a weak thalamic `Cul7`-only response at FDR < 0.10
that did not recapitulate the RAF/MEK output module. Because SOS1 is usually
the dominant member in knockout studies, the complete lack of a 0.05-level
`Sos1` response is the strongest same-experiment argument that acute partial
`Sos2` loss will be below detection.

**Downstream branch that was detectable but small: Braf and Map2k1.** `Braf`
had `4` focal DEGs: `Vgf`, `Ptpn5`, `Atp2a2`, and `Unc13a` were all
down-regulated. `Map2k1` also had `4`: `Vgf`, `Ptpn5`, `Etv5`, and `Unc13a`
were down-regulated. In the run-local profile comparison, `Braf` and `Map2k1`
shared 3 of their 5 unique negative significant features in the nominated view
with a negative-significant Jaccard of `0.6`. The Distributed Agents corpus high-
confidence claim `claim:5f4082f202c79d3b3fcc` captured the same finding as a
sparse, down-regulated `Vgf`/`Ptpn5`/`Unc13a` thalamic module. This shows the
assay can see a basal MAPK-linked output in these cells, but the response
breadth is only four genes even when MEK1 or BRAF is hit directly.

**Partial RAF activation and neurotrophin comparators: Shoc2 and Ntrk2.**
`Shoc2`, a Ras/RAF scaffold, had `1` focal DEG, `Vgf` down. `Ntrk2`, a TrkB
receptor upstream of Ras/MAPK and PI3K signaling in neurons, had `3` focal
DEGs: self knockdown plus down-regulated `Atp2a2` and `Vgf`. These partial
overlaps argue that the BRAF/MEK1 module can be fed by selected upstream
neuronal inputs, but even those closer positive controls remain at 1 to
3 DEGs. The same evidence argues against extrapolating from four MEK1/BRAF
DEGs to a broad `Sos2` response.

**Upstream and parallel Ras/MAPK counterexamples.** Many represented pathway
members were flat in the requested cell group: `Hras` `0`, `Kras` `0`,
`Rasa2` `0`, `Raf1` `0`, `Map2k2` `0`, `Mapk1` `0`, `Ptpn11` `0`,
`Rapgef2` `0`, `Fgfr1` `0`, `Fgfr2` `0`, `Fgfr3` `0`, `Spred1` `0`, and
`Spred2` `0`. The direct FGFR/GAB/SHC adaptor genes most proximal to SOS were
not all represented; for example `Grb2`, `Gab1`, `Shc1`, `Frs2`, and `Frs3`
were absent from the 1,674 training targets. Still, the represented GTPases,
RAF/MEK/ERK paralogs, RTKs, SHP2, SPRED negative regulators, and Rap/Ras GEFs
were enough to reject a generic "any Ras pathway gene perturbs 151 TH"
heuristic. The Distributed Agents high-confidence claim
`claim:4af1e0ceaef9adda14b9` made the same same-experiment point: detectable
basal Ras/MAPK RNA output was restricted to a sparse `Braf`-`Map2k1` branch,
not shared across upstream Ras/GEF, RAF1, MEK2, ERK2, or RasGAP relatives.

The run-local score-vector audit was consistent with that corpus summary.
`Sos1` had no significant focal genes and had nearly zero whole-profile
similarity to the positive branch: cosine `0.0068` to `Braf` and `0.0201` to
`Map2k1`, with zero significant-gene intersections in either direction.

## Sos2 Prediction

I predict `Sos2 = 0` DEGs.

Mechanistically, SOS2 can activate Ras and Rac downstream of receptors, and
external literature makes clear that it can matter in some proliferative or
oncogenic settings. But the best-matched Perturb-seq evidence points the other
way for this endpoint:

- The closest represented paralog, `Sos1`, had 0 DEGs at FDR 0.05.
- Many represented single-gene upstream Ras nodes, RTKs, and receptor-proximal
  comparators were also at 0.
- Even direct downstream hits in the responsive branch, `Braf` and `Map2k1`,
  yielded only four DEGs, with `Shoc2` and `Ntrk2` yielding one and three.
- External knockout data put SOS2 below SOS1 for organismal requirement and
  show substantial SOS1/SOS2 redundancy, so knocking out `Sos2` alone should
  be no stronger than the already-flat `Sos1` perturbation in a sparse,
  postmitotic, partial-CRISPR neuronal assay.

I therefore set the point estimate exactly at the floor rather than assigning
a small nonzero count.

## Limits

The evidence for `Sos2` is extrapolative because `Sos2` itself was held out
and absent from the same-experiment Distributed Agents corpus. Several direct adaptor
genes between RTKs and SOS were also not in the training set. The screen used
P16 mosaic AAV CRISPR with modest recovered perturbed nuclei and measured
steady-state nuclear RNA, not indel rates, SOS2 protein, Ras-GTP, AKT, or
phospho-ERK flux. A transient kinase or synaptic effect could therefore be real
while still giving 0 BH-significant snRNA-seq DEGs. Finally, SOS2 has reported
unique roles in KRAS-mutant proliferative systems, so the prediction should not
be read as a general SOS2-null phenotype outside juvenile postmitotic neurons.
