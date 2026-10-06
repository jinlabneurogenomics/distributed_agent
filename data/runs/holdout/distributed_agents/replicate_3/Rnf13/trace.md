# Rnf13 DEG-count prediction trace

## Question and scope

The requested held-out perturbation set contains one mouse target, `Rnf13`. I treated the endpoint as the integer number of focal-cell genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, using the same 17,259 measured genes per perturbation that appear in the training parquet. `Rnf13` was absent from both the parquet `gene_target` column and the focal training-count CSV, so no direct `Rnf13` expression signature was available.

The ambiguity I resolved was how to use endolysosomal/ER literature for RNF13. I did not assign it the `Rab7` or `Atp2a2` broad response simply because RNF13 can localize to lysosomes or ER: those training perturbations are direct core trafficking or ER-Ca2+ lesions. I used them as positive detectability controls and used the represented E3, AP-adaptor, SNARE, and autophagy genes as closer basal-neuron counterexamples.

## Sources used

- Input data: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`, and `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`; direct `Rnf13` target lookup returned no target context, so I used curated claims and findings for candidate analogs including `Rab7`, `Atp2a2`, `Dhdds`, `Manf`, `Becn1`, `Rb1cc1`, `Herc1`, `Herc2`, `Huwe1`, `Ube3a`, `Hectd4`, `Atg5`, `Atg16l1`, `Ap3b1`, and SNARE/AP-adaptor groups.
- Run-local Distributed Agents profile tools:
  - `profile_neighbors_rnf13_anchors.json`: nearest expression-profile neighborhoods for `Rab7`, `Atp2a2`, `Dhdds`, `Marchf6`, `Vps35`, `Vps54`, `Herc1`, `Ube3a`, `Atg5`, `Lamp2`, and `Vcp`.
  - `profile_compare_rnf13_analogs.json` and two bounded inspections over a 45-target panel spanning E3 ligases, AP/SNARE genes, autophagy, lysosome/retrograde trafficking, and ER/proteostasis positives.
- External lookup: UniProtKB entry `O54965` for mouse RNF13 and NCBI Gene ID `24017`.
- PubMed/literature for RNF13 mechanisms: Bocock et al. 2009, FEBS J, DOI `10.1111/j.1742-4658.2009.06913.x`, PMID `19292867`; Bocock et al. 2010, Traffic, DOI `10.1111/j.1600-0854.2010.01060.x`, PMID `20230530`; Zhang et al. 2012, CMLS, DOI `10.1007/s00018-012-1103-5`, PMID `22890573`; Arshad et al. 2013, JBC, DOI `10.1074/jbc.M112.368829`, PMID `23378536`; Cabana et al. 2021, Cells, DOI `10.3390/cells10113063`, PMID `34831286`; Cabana and Lussier 2022, Cells, DOI `10.3390/cells11030380`, PMID `35159190`; Liu et al. 2024, Adv Sci, DOI `10.1002/advs.202309560`, PMID `39031743`; Wang et al. 2024, Cell Commun Signal, DOI `10.1186/s12964-024-01905-2`, PMID `39511649`; Trinh et al. 2025, Cell Reports, DOI `10.1016/j.celrep.2025.116053`, PMID `40714633`; Cabana et al. 2025, FEBS J, DOI `10.1111/febs.70365`, PMID `41387381`.

## Training-data computations

I loaded the focal group from the parquet and recomputed candidate-gene exact DEG lists with:

```python
pd.read_parquet(
    parquet,
    filters=[
        ("group_name", "==", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", selected_analogs),
    ],
)
```

The focal training table has 1,674 perturbations. Its median `n_degs` is 0; 469/1,674 training targets are nonzero; the 75th percentile is 1, the 90th percentile is 2, and the high tail is dominated by broad stress/RNA/proteostasis perturbations such as `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Ufc1` 572, `Rab7` 501, `Psmc1` 430, and `Atp2a2` 187. Thus the prior for an arbitrary held-out target is zero or one unless a strong within-dataset module is biologically justified.

## Rnf13 evidence and analogs

`Rnf13` encodes a PA-TM-RING E3 ubiquitin ligase. UniProtKB places mouse RNF13 on ER, late-endosome, lysosome, and inducible inner nuclear membranes; Bocock et al. showed that it is a labile type-I membrane ligase in the endosomal/lysosomal system whose RING-containing fragment can be proteolytically released, and that PKC/ionomycin stimulation routes it to recycling endosomes and the inner nuclear membrane. Arshad et al. placed RNF13 upstream of the IRE1-alpha/TRAF2/JNK apoptosis arm during induced ER stress. Zhang et al. found hippocampal synaptic ultrastructural and spatial-learning phenotypes in germline Rnf13-null mice, with impaired Snapin/SNAP25 SNARE assembly but no change in SNARE-protein abundance. Cabana et al. and Cabana/Lussier tie the DEE-associated dileucine variants to AP-3/AP-1-dependent RNF13 lysosomal routing; Liu et al. and Trinh et al. found more stress-gated lysosomal substrates in immune/cell-line systems, LAMP-1 and ARL8B. Wang et al. and injury studies nominate a p62/NRF2-protective role under ischemic or cardiac stress. These data make RNF13 a conditional endomembrane ubiquitin ligase, not a direct core HOPS/Rab7, SERCA, or N-linked-glycosylation enzyme.

The nearest represented ubiquitin-ligase comparators were mostly flat in the focal group:

| training target | focal `n_degs` | use as analog |
| --- | ---: | --- |
| `Rnf216` | 0 | RING/E3 counterexample; no RNF13-specific PA-TM-RING paralog was available. |
| `Rnf220` | 0 | RING/E3 counterexample, but nuclear AMPAR-related biology makes it mechanistically distant. |
| `Ube3a` | 0 | neuronal E3 with disease biology; Distributed Agents claims show it does not phenocopy broad HECT/E3 responses. |
| `Herc1`, `Herc2` | 0, 0 | large E3 counterexamples; corpus claim `claim:912f...` says they are not interchangeable in this assay. |
| `Hectd4` | 1 | singleton self-transcript E3 result. |
| `Marchf6` | 14 | ER-membrane E3, but its significant genes were sterol feedback genes (`Insig1`, `Cyp51`, `Msmo1`, `Fdft1`, `Hmgcs1`, `Ldlr`, `Sqle`) plus target depletion, unlike RNF13's known substrates. |
| `Huwe1` | 158 | a distant HECT ligase and a positive E3 detectability control; Distributed Agents claim `claim:6d2d...` marks HUWE1 as target-specific rather than generic E3 biology. |

The relevant trafficking, SNARE, AP-adaptor, and lysosome/autophagy perturbations also argued for a very small focal-cell response. `Ap3b1`, the adaptor connection closest to the DEE-associated RNF13 sorting motif, had 0 DEGs; `Ap1b1` had 1 and `Ap1s2` had 0. Fast release/SNARE or vesicle markers were flat or target-only: `Stx1b` 0, `Stx5a` 0, `Nsf` 0, `Cplx2` 0, `Vamp1` 1, `Syp` 1, `Cplx1` 1, `Stxbp1` 1. Autophagy and lysosome genes were similarly weak in this exact cell group: `Atg5` 0, `Atg16l1` 0, `Becn1` 0, `Lamp2` 0, `Sqstm1` 1, `Ctsb` 1, `Tmem106b` 1, and `Rb1cc1` 4. The Distributed Agents autophagy claim `claim:9ba...` explicitly records that represented autophagy and lysosome perturbations were not transcriptomically interchangeable, and the Becn1 context notes that absence of LAMP/UPR/ISR mRNA induction does not rule out changed LC3 lipidation, PtdIns3P, p62 turnover, or endosome morphology.

The high positives were useful mainly as boundaries:

- `Rab7` had 501 DEGs and a clear endolysosomal/sterol response in the focal data: `Atp6v1b2`, `Dpp7`, `Insig1`, `Atp6v0b`, `Msmo1`, `Fdft1`, `Lamp2`, `Sqstm1`, `Grn`, `Hmgcs1`, `Sqle`, `Mcoln1`, `Cyp51`, `Dhcr7`, `Pld3`, and `Ldlr` were all FDR-significant and up. Distributed Agents reports the same recurrent late-endosomal/lysosomal and sterol compensation modules. RNF13 is a lysosomal/endosomal ligase, but neither `Lamp2`, `Ap3b1`, nor autophagy perturbations reproduced this terminal Rab7/HOPS-like state.
- `Atp2a2` had 187 DEGs with `Ddit3`, `Chac1`, `Xbp1`, `Herpud1`, `Hspa5`, `Asns`, `Cars`, `Slc7a5`, `Slc1a4`, `Shmt2`, `Mthfd2`, and `Psph` induction; `Dhdds` had 116 with a similar ER client-handling/ATF4 arm. Distributed Agents claims `claim:a7a...` and `claim:d49...` use these as positive UPR/ISR detectability controls. `Rnf13` can modulate IRE1-alpha/JNK apoptosis in induced stress, but acute basal RNF13 loss is not an ER-Ca2+ depletion or dolichol-supply lesion, and nearby `Manf` had only 3 focal DEGs while `Atf6` and `Eif2ak4` were 0.
- `Vps35`, `Vps53`, `Vps54`, `Cog4`, `Cog5`, and TRAPP genes show that retrograde/Golgi trafficking perturbations do not collapse into one response: focal counts were `Vps35` 17, `Vps53` 0, `Vps54` 31, `Cog4` 0, `Cog5` 0, `Trappc6b` 0, `Trappc9` 0, and `Trappc10` 0. Distributed Agents claim `claim:1d7...` records the same boundary.

As a measured feature in other focal-cell perturbations, `Rnf13` itself is detectable: it was up after `Rab7` (`logfoldchange` +0.376, `q` 0.0059) and down after `Ctnnb1` (`logfoldchange` -0.449, `q` 0.0208). Since several flat perturbations in this training set report only the target transcript, I assigned one expected DEG for the direct guide effect and did not add a downstream endolysosomal or UPR module.

## Point prediction

I predict `Rnf13` will have 1 FDR-significant gene in `151 TH Prkcd Grin2c Glut`: either the `Rnf13` transcript itself or, equivalently, a singleton weak local response. The zero/nonzero call is driven mostly by within-dataset flatness of `Ap3b1`, core SNARE/synaptic-vesicle, autophagy, `Lamp2`, generic RING/E3, `Atf6`, and `Eif2ak4` perturbations. The decision to keep it at 1 rather than 10-100+ is driven by external RNF13 biology being conditional/substrate-specific and by the lack of a training perturbation that makes an RNF13-like basal neuronal PA-TM-RING lesion look like direct `Rab7`, `Dhdds`, or `Atp2a2` stress.

## Limits

No same-complex PA-TM-RING paralog such as `Rnf167` or `Znrf4`, no direct RNF13 substrate such as `Snapin`, `Lamp1`, `Arl8b`, `Tmem173`, or `Ern1`, and no `Rnf13` perturbation signature were represented in the training data. `Ap3b1`, `Lamp2`, `Stx1b`, and `Syp` are pathway-adjacent, not true RNF13 phenocopies. RNF13's strongest literature roles often come from germline models, cultured stressed cells, macrophages, liver, heart, or ischemia rather than from acute partial loss in postmitotic thalamic neurons. Finally, the assay reads steady-state nuclear RNA 3-4 weeks after AAV CRISPR and can miss post-translational changes in ubiquitination, endosomal routing, SNARE assembly, LAMP-1/ARL8B abundance, p62 turnover, or apoptosis of edited cells before harvest.
