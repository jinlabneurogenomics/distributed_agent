# Tlr9 held-out DEG-count prediction

## Question interpreted

The held-out manifest contains one requested target:

| target_name |
|---|
| Tlr9 |

I interpreted the requested endpoint as the exact focal-cell endpoint used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: for a perturbation of a
given gene, count the measured genes in `151 TH Prkcd Grin2c Glut` whose
Wilcoxon Benjamini-Hochberg adjusted p-value is below 0.05. `Tlr9` is completely
held out, so no `Tlr9` knockout signature or endpoint count from this Perturb-seq
screen was used.

Two ambiguities were resolved conservatively.

- A zero prediction means no measured gene passes FDR 0.05 in the focal cell
  group; it does not mean Tlr9 is biologically irrelevant.
- Training perturbations with small or isolated single-gene effects in other
  cell groups were not converted into positive evidence for `151 TH Prkcd
  Grin2c Glut` unless the focal-cell endpoint itself was nonzero.

## Sources used

- Direct focal endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Differential-expression surfaces: `[local file: training_de_all_cell_groups.parquet]`
- Same-experiment interpretation: Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`. I used the high-confidence
  claims that represented TLR/CD14/NF-kappaB/IRF comparators are flat in basal
  neuronal Perturb-seq conditions, and the target-centered findings for `Tlr7`
  and `Tlr3`.
- Dataset metadata: `codex_runtime/pipeline/measurement_registry.json`, used
  only to confirm the DE parquet represents per-gene perturbation DE statistics.
- External mechanism checks from PubMed:
  - Hemmi et al. 2000, Nature, DOI `10.1038/35047123`, PMID `11130078`: TLR9
    is required for CpG DNA responses in mice.
  - Latz et al. 2004, Nature Immunology, DOI `10.1038/ni1028`, PMID `14716310`:
    CpG DNA binds TLR9 in endosomal/lysosomal compartments where TLR9 recruits
    MyD88.
  - Kim et al. 2008, Nature, DOI `10.1038/nature06726`, PMID `18305481`:
    UNC93B1 delivers nucleic-acid-sensing TLR7 and TLR9 from the ER to
    endolysosomes.
  - Kawai et al. 2004, Nature Immunology, DOI `10.1038/ni1118`, PMID
    `15361868`: MyD88 and TRAF6 couple TLR7/8/9-family signaling to IRF7 and
    interferon-alpha induction.

## Computational checks over the training data

The training DEG-count table contains 1,674 non-held-out perturbations in the
focal group. Its response distribution is strongly zero-inflated:

- `n_degs = 0`: 1,205 perturbations, 72.0%
- `1 <= n_degs < 10`: 363 perturbations, 21.7%
- `10 <= n_degs < 100`: 63 perturbations, 3.8%
- `n_degs >= 100`: 43 perturbations, 2.6%

To inspect focal-cell expression evidence without loading the full 616,253,184
row parquet, I used the parquet row-group statistics to read only row groups
whose `group_name` range contained `151 TH Prkcd Grin2c Glut`, then filtered to
TLR/innate-pathway candidate perturbations.

```python
pf = pq.ParquetFile(de_path)
row_groups = []
for i in range(pf.num_row_groups):
    stats = pf.metadata.row_group(i).column(5).statistics  # group_name
    if stats.min <= "151 TH Prkcd Grin2c Glut" <= stats.max:
        row_groups.append(i)

tab = pf.read_row_groups(
    row_groups,
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched", "group_name",
    ],
)
```

Those row groups covered 28,562,358 pure focal-cell rows plus two short boundary
groups. After filtering to 26 TLR, NF-kappaB, IRF, interferon, and STAT
comparators, every selected target had 17,259 tested genes in this cell group.

## Training perturbations compared with Tlr9

All counts below are observed `n_degs` in `151 TH Prkcd Grin2c Glut`.

| comparator set | training targets and focal observed counts | expression-pattern evidence | interpretation for Tlr9 |
|---|---:|---|---|
| Closest represented endosomal TLRs | `Tlr7` 0, `Tlr8` 0, `Tlr3` 0 | Direct parquet re-counts found 0 genes at FDR 0.05 and 0 at FDR 0.10 for all three. The Distributed Agents `Tlr7` findings report no FDR<0.10 downstream genes in all 19 measured neuronal groups and no meaningful whole-universe signature neighbors; the `Tlr3` findings report only one robust call outside the focal group, with no shared IFN/NF-kappaB signature among represented TLR and IFN relatives. | `Tlr7` and `Tlr8` are the closest represented endosomal nucleic-acid-sensing relatives to Tlr9. Their complete focal silence is the strongest within-dataset evidence for a zero Tlr9 call. `Tlr3` uses TRIF rather than MyD88, so it is a more distant counterexample; its lack of a focal response still supports pathway quiescence. |
| Surface TLR and CD14/CD36 innate-receptor context | `Tlr2` 0, `Tlr4` 0, `Tlr5` 0, `Cd14` 0, `Cd36` 0 | All had 0 focal genes at FDR 0.05 and 0 at FDR 0.10. The Distributed Agents high-confidence claim `claim:f0ea791345477e6bfc20` summarizes that `Cd36`, `Tlr2`, and `Tlr4` perturbations do not sustain a basal neuronal cytokine, chemokine, NF-kappaB, IFN, TLR, or inflammasome RNA response under unstimulated neuronal conditions. | These are not direct Tlr9 paralogs, but they test whether a tonic innate-inflammatory TLR module is active in the same neuronal assay. They argue against a hidden receptor-side inflammatory state that Tlr9 loss would expose. |
| Shared downstream NF-kappaB/TAK1/adaptor side | `Chuk` 0, `Map3k7` 0, `Nfkb1` 0, `Traf3` 0 | Every target had 0 focal genes at FDR 0.05 and 0 at FDR 0.10. The Distributed Agents high-confidence claim `claim:778b2c45f226febe4372` reports that represented TNFR/TLR/IL-1/CD40-to-TAK1/IKK/NF-kappaB/JNK/p38 perturbations are broadly transcriptionally silent as a basal module in postnatal NeuN-positive neurons. | TLR9 signals through the MyD88/IRAK/TRAF6 axis into NF-kappaB and AP-1 and, in plasmacytoid dendritic cells, toward IRF7. The represented downstream kinases and transcriptional endpoints show that this inducible arm is not tonically controlling the focal neuronal transcriptome. |
| IRF/interferon comparators | `Irf1` 0, `Irf3` 0, `Irf5` 0, `Irf8` 0, `Irf9` 0, `Ifnar1` 0, `Ifnar2` 0, `Ifngr1` 0, `Ifngr2` 0, `Stat1` 1, `Stat2` 0, `Stat3` 0, `Stat4` 0, `Stat5b` 0 | Direct endpoint counts are zero except for a singleton `Stat1` call. In the focal DE rows, canonical inflammatory and IFN-stimulated readouts queried around the TLR set, including `Tnf`, `Il1b`, `Il6`, `Ccl2`, `Cxcl10`, `Nfkbia`, `Irf7`, `Isg15`, `Ifit1`, `Ifit3`, `Oas1a`, and `Oasl2`, were all BH-adjusted `p = 1.0` after perturbation of `Tlr7`, `Tlr8`, `Tlr3`, `Tlr2`, `Tlr4`, `Tlr5`, `Cd14`, `Chuk`, `Map3k7`, `Nfkb1`, `Traf3`, `Irf3`, `Irf5`, `Ifnar1`, `Stat1`, and `Stat2`. | A strong Tlr9 effect could have emerged indirectly as an interferon or ISG program. The represented IFN receptor, STAT, and IRF losses instead show a mostly flat basal IFN module in this neuronal state, making a broad Tlr9-driven ISG count unlikely. |

The same-experiment Distributed Agents claim
`claim:3ac1aaff5686e4bbeb6f` is the most compact description of these
comparisons: represented TLR/CD14 and innate-receptor perturbations in
unchallenged neuronal Perturb-seq conditions do not form a coherent shared
TLR/PRR-to-NF-kappaB/IRF transcriptional module, aside from isolated,
target-specific singleton responses. That agrees with the focal-cell training
counts, where the directly relevant receptor and downstream comparators are
all at zero.

## Target-specific prediction for Tlr9

`Tlr9` encodes an endosomal DNA sensor. In innate immune cells it is trafficked
to endolysosomes by UNC93B1, recognizes unmethylated CpG-rich DNA, and signals
through a MyD88/IRAK/TRAF6 complex to NF-kappaB and IRF7-dependent cytokine and
type-I-interferon programs. That canonical mechanism is well suited to
ligand-stimulated macrophages, dendritic cells, plasmacytoid dendritic cells,
and B cells. The present assay is different: it is a sparse loss-of-function
screen in juvenile, NeuN-enriched postmitotic neurons, with no added CpG DNA,
infection, injury, B-cell/plasmacytoid-DC compartment, or microglial readout.

Within the training data, the closest available Tlr9 analogs point to no focal
effect rather than a weak nonzero effect:

- `Tlr7`, the closest represented MyD88-dependent endosomal TLR, has
  `n_degs = 0` in the focal cell group and no FDR<0.10 downstream genes across
  all 19 neuronal groups summarized by the Distributed Agents corpus.
- `Tlr8` also has `n_degs = 0` in the focal group; its corpus-level singleton
  effects did not align with Tlr7/Tlr3/Tlr4/NF-kappaB/IRF comparators.
- `Tlr3`, `Tlr2`, `Tlr4`, `Tlr5`, `Cd14`, `Chuk`, `Map3k7`, `Nfkb1`, and `Traf3`
  all have `n_degs = 0` in the focal group, rejecting a basal shared TLR or
  NF-kappaB module in these neurons.
- Focal-cell rows for the measured `Tlr9` transcript itself are present in
  these comparator perturbations and remain non-significant with adjusted
  `p = 1.0`, so none of the represented TLR/NF-kappaB/IRF losses feed back on
  `Tlr9` RNA in this state.

I therefore predict that acute neuronal `Tlr9` loss will not push any measured
gene below the FDR 0.05 cutoff in `151 TH Prkcd Grin2c Glut`:

```tsv
target_name	predicted_n_degs
Tlr9	0
```

## Limits of the reasoning

- This is an extrapolation from relatives: `Tlr9`, `Myd88`, `Unc93b1`, `Irak1`,
  `Irak4`, `Traf6`, `Ticam1`, and `Irf7` were not represented as perturbation
  targets in the training endpoint, so the most direct MyD88-dependent TLR9
  scaffold was not itself observed.
- `Tlr7` and `Tlr8`, the closest represented endosomal TLRs, each had only 89
  matched perturbed nuclei in the focal group. Their zeros are consistent with
  the all-neuronal corpus summaries, but a very weak effect could still have
  fallen below power.
- The assay perturbs only recovered NeuN-positive neuronal nuclei after P16
  AAV-PHP.eB delivery. It cannot test Tlr9 biology in microglia, astrocytes,
  plasmacytoid dendritic cells, macrophages, B cells, vascular cells, or
  ligand-rich disease states.
- No CpG oligonucleotide, mitochondrial-DNA DAMP, microbial DNA, or injury
  stimulus was supplied. The prediction is only for tonic consequences of
  neuronal Tlr9 loss in this assay, not for a TLR9 agonist or antagonist under
  inflammatory challenge.
- CRISPR editing efficiency was not measured directly in the DE parquet; weak
  or unchanged target RNA is not proof of failed editing. The zero call rests
  on pathway-wide same-experiment silence, not on target-RNA depletion.
