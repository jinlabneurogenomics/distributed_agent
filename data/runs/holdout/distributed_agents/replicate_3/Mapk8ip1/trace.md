# DEG-count prediction reasoning

## Question and interpretation

The held-out manifest for this run contains one target:

```tsv
target_name
Mapk8ip1
```

I interpreted the requested endpoint as the integer number of measured genes with `pvals_adj < 0.05` after CRISPR loss of the target in the focal `151 TH Prkcd Grin2c Glut` thalamic glutamatergic class. The count includes the perturbed gene's own transcript if that row passes FDR; this is visible in the training table because several transport genes have `n_degs = 1` in 151 and the only significant row is the target transcript itself.

`Mapk8ip1` was held out and has no measured differential-expression surface in the supplied parquet or in the training count table. I therefore used the focal-cell training counts and DE signatures of mechanistic neighbors, then used external biology to decide which neighbors are relevant rather than pooling every MAPK- or kinesin-named gene.

## Sources

- Input parquet: `[local file: training_de_all_cell_groups.parquet]`
- Focal training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Held-out manifest: `[local file: 131_Mapk8ip1.csv]`
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`
- PubMed-indexed literature:
  - Whitmarsh et al. 2001, Genes & Development, DOI `10.1101/gad.922801`, PMID `11562351`
  - Mooney & Whitmarsh 2003, Journal of Biological Chemistry, DOI `10.1074/jbc.M311841200`, PMID `14699111`
  - Chiba et al. 2014, Molecular Biology of the Cell, DOI `10.1091/mbc.E14-06-1111`, PMID `25165140`
  - Sun et al. 2017, Cellular and Molecular Life Sciences, DOI `10.1007/s00018-017-2568-z`, PMID `28638935`

## Computational checks

The focal training CSV has 1,674 non-held-out perturbations. Its observed `n_degs` distribution is sparse:

- 1,205 / 1,674 perturbations have `0` DEGs.
- 363 have `1-9` DEGs.
- 63 have `10-99` DEGs.
- 43 have `>=100` DEGs.

To avoid reading the full 616M-row parquet, I inspected row-group metadata and found that row groups 546-580 cover `151 TH Prkcd Grin2c Glut`. I then read only those row groups and filtered to JIP1/JNK/kinesin/APP/endolysosomal comparison targets:

```python
pf = pyarrow.parquet.ParquetFile(parquet_path)
rows = []
for i in range(546, 581):
    tbl = pf.read_row_group(i, columns=[
        "names", "gene_target", "group_name", "logfoldchanges",
        "pvals_adj", "scores", "n_pert_matched", "n_ctrl_matched",
    ])
    df = tbl.to_pandas()
    rows.append(df[
        (df.group_name == "151 TH Prkcd Grin2c Glut")
        & df.gene_target.isin(candidate_targets)
    ])
```

This yielded 17,259 measured genes per represented candidate and exactly reproduced the focal training counts by summing `pvals_adj < 0.05`.

## Candidate evidence

### Direct biology of `Mapk8ip1`

`Mapk8ip1` encodes JIP1, a neuronal scaffold/adaptor. External literature puts it in two pathways that are relevant to this endpoint:

- JNK scaffold: JIP1 binds JNK, MKK7, and mixed-lineage kinases, and Jip1 disruption blocks stress- and anoxia-induced JNK activation rather than acting as a constitutive transcription factor in unstimulated neurons (Whitmarsh et al. 2001; Mooney & Whitmarsh 2003).
- Axonal cargo adaptor: JIP1 links APP and TrkB trafficking to kinesin-1/KLC motors; JIP1-deficient neurons show impaired fast APP axonal transport, and JIP1 cooperates with JIP3 to relieve kinesin-1 autoinhibition for TrkB transport (Chiba et al. 2014; Sun et al. 2017).

Those papers predict a real neuronal perturbation, but mostly at the level of stress-gated JNK phosphorylation and cargo localization/axonal transport. The supplied assay is steady-state nuclear RNA after sparse juvenile CRISPR, so the best empirical analogs are JNK-pathway and kinesin/APP perturbations rather than broad developmental KOs or acute excitotoxic stress models.

### JNK/stress-MAPK branch

Closest measured training perturbations in `151 TH Prkcd Grin2c Glut`:

| perturbation | focal `n_degs` | focal FDR<0.05 rows | interpretation |
|---|---:|---|---|
| `Mapk9` | 0 | none | JNK2 itself was flat |
| `Map2k6` | 0 | none | p38 MAP2K; stress-MAPK branch flat |
| `Map3k7` | 0 | none | TAK1 upstream of JNK/p38/NF-kappaB; flat |
| `Traf3` | 0 | none | TNFR/TLR/NF-kappaB/JNK adaptor; flat |
| `Map2k1` | 4 | `Vgf`, `Ptpn5`, `Unc13a`, `Etv5` down | ERK/MEK counterexample; MAPK signaling can be detected but only as a small Raf-MEK-ERK module |

The Distributed Agents corpus summarizes the same-experiment evidence as Claim `claim:73be997a6a0b095c36d2`: represented stress-MAPK/JNK-adjacent nodes, anchored by `Map2k6`, `Mapk9`, and `Taok1`, did not produce a shared basal neuronal transcriptional module. A related high-confidence Claim, `claim:778b2c45f226febe4372`, reports that represented TNFR/TLR/IL-1/CD40-to-TAK1/IKK/NF-kappaB/JNK/p38 perturbations are broadly silent in unchallenged postnatal NeuN-positive neurons. In the ledger, `Map2k6:F004` notes that `Map3k7`, `Taok1`, `Mapk9`, and `Tlr7` had no downstream genes at FDR<0.10, and `Map3k7:F003` notes that represented core downstream targets `Chuk`, `Nfkb1`, `Rel`, `Map2k6`, and `Mapk9` were null.

This is strong within-dataset evidence against a multi-gene JIP1-to-JNK/AP-1 steady-state RNA response in the focal cells. The exact JIP1 binders `Map2k7`, `Map2k4`, `Mapk8`, and `Mapk10` were not available as focal training perturbations, so this is pathway-adjacent rather than direct paralog evidence.

### Kinesin/APP cargo-adaptor branch

Closest measured focal perturbations:

| perturbation | focal `n_degs` | focal FDR<0.05 rows |
|---|---:|---|
| `App` | 1 | `App` down |
| `Kif5a` | 1 | `Kif5a` down |
| `Kif5c` | 1 | `Kif5c` down |
| `Klc1` | 1 | `Klc1` down |
| `Klc2` | 1 | `Klc2` down |
| `Kif1a` | 1 | `Kif1a` down |
| `Kif1b` | 0 | none |
| `Rhot1` | 0 | none |
| `Trak1` | 0 | none |
| `Kifbp` | 2 | `Kifbp` down, `Srebf2` down |

All of `App`, `Kif5a`, `Kif5c`, `Klc1`, and `Klc2` were self-only in the focal class at FDR<0.05. The actual adjusted p-values of their self rows were significant (`App` 8.4e-58, `Kif5a` 6.1e-5, `Kif5c` 4.5e-5, `Klc1` 6.6e-14, `Klc2` 4.1e-5), while the plausible transport stress markers and JNK/AP-1 transcripts were not jointly significant.

The same-experiment corpus reinforces this boundary. `Kif5a:F004` reports that represented kinesin-pathway targets, including `Kif5c`, `Kif1a`, `Kif1b`, `Kifbp`, `Klc1`, `Klc2`, `Rhot1`, and `Trak1`, did not phenocopy a hidden `Kif5a`-like nuclear RNA module. `Kif5c:F002` makes the same point for kinesin-1 heavy chains, light chains, and MIRO/TRAK adaptors. Claim `claim:064f16f0e8bfd08f9b64` generalizes these findings: acute perturbation of represented kinesin-1 and MIRO/TRAK transport-pathway genes does not produce a common soma-detectable neuronal nuclear transcriptional module.

`App` is relevant because JIP1 enhances APP anterograde transport (Chiba et al. 2014). In the training data, `App` perturbation in the focal class is self-only (`n_degs = 1`), and corpus record `App:F001` describes broad `App` self-transcript decrease without an FDR-supported downstream program in recovered neuronal classes. This argues that impairing the JIP1-APP axis alone is unlikely to create a large cell-body transcriptional response by the 3-4 week endpoint.

### Positive counterexamples that I down-weighted

`Dctn1` has 75 focal DEGs and is a transport/neurodegeneration gene, but its focal signature is headed by a sterol/lipid response: `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`, `Tecr`, `Sqle`, and `Dhcr24` are up. The corpus calls this an SREBF2-like cholesterol-biosynthesis and membrane-lipid program, with dynein/dynactin, Rab7, and lysosomal cholesterol export as better mechanistic context. That is not the same biochemical state as losing a kinesin-1/JNK scaffold, and `Dctn1:F009` explicitly lists canonical kinesins and `Kifbp` as non-phenocopies.

`Rab7` and `Tsc2` were even broader in the focal class (`501` and `86` DEGs), but they represent endolysosomal cholesterol and mTOR/lysosomal signaling states. I treated them as proof that the focal cell group can show broad stress or lipid programs, not as quantitative donors for `Mapk8ip1`.

`Map2k1` produced a small, coherent four-gene ERK output (`Vgf`, `Ptpn5`, `Unc13a`, `Etv5`). It is a useful counterexample showing that some MAPK nodes are visible in this assay, but same-experiment corpus record `Map2k1:F004` reports that most Ras/MAPK neighbors, including `Map2k2` and `Mapk1`, did not phenocopy `Map2k1`; I therefore did not transfer this narrow Raf-MEK-ERK count onto a JNK scaffold.

## Prediction for `Mapk8ip1`

I predict a very weak, likely self-transcript-only response:

- JIP1 biology makes an on-target mRNA row plausible because `Mapk8ip1` is neuronally expressed and represented among measured focal transcripts.
- The two expected downstream arms, JNK scaffolding and kinesin/APP cargo transport, are both transcriptionally quiet in the same postnatal basal snRNA-seq assay.
- Multiple direct kinesin/APP comparators in the focal class land at exactly one FDR<0.05 gene, generally the perturbed transcript itself.
- I did not see a mechanistic reason to borrow the `Dctn1`/`Rab7` sterol module or the `Map2k1` ERK/Vgf module.

The integer point prediction is therefore:

```tsv
target_name	predicted_n_degs
Mapk8ip1	1
```

## Limits

The biggest gap is that the closest JIP-family perturbations (`Mapk8ip2`, `Mapk8ip3`, `Spag9/JIP4`) and the most direct JIP1-bound kinases (`Mapk8/JNK1`, `Mapk10/JNK3`, `Map2k4/MKK4`, `Map2k7/MKK7`, and mixed-lineage/DLK kinases such as `Map3k12`) were not in the focal training-count table. The prediction consequently relies on represented branch neighbors (`Mapk9`, `Map2k6`, `Map3k7`, kinesin-1 subunits, MIRO/TRAK adaptors, and `App`) rather than on a measured JIP paralog.

The evidence is also mismatched in endpoint. External studies demonstrate that JIP1 can be important for excitotoxic/anoxic JNK activation and axonal transport, but this experiment measures surviving juvenile neuronal nuclei at baseline and does not assay phospho-JNK, APP or TrkB cargo movement, axonal localization, c-Jun phosphorylation, or protein loss. A `0` rather than `1` count would be plausible if the `Mapk8ip1` target transcript failed to pass FDR, and a larger nonzero count would be plausible if these thalamic cells are unusually dependent on a JIP1-specific cargo that was not represented by the measured kinesin/APP analogs. My point estimate keeps the downstream program at zero and assigns one expected self/on-target DEG.
