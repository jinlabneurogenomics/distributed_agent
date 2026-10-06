# Atp6v0c held-out prediction trace

## Question and resolved ambiguities

The held-out target list for this run contains one gene, `Atp6v0c`. I interpreted the endpoint as the integer number of genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, including the perturbed gene itself if its measured RNA was called significant. The target was completely absent from the supplied training signatures and from `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, so the prediction has to be transferred from non-held-out perturbations rather than estimated from an `Atp6v0c` row.

## Sources used

- Supplied focal-count table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Supplied differential-expression parquet: `training_de_all_cell_groups.parquet`.
- Requested-target manifest: `021_Atp6v0c.csv`.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`; relevant retrieved records were `Atp6v0a1:F003`, `Atp6ap2:F004`, and `Rab7:F009`.
- PubMed literature for external mechanism:
  - Forgac 2007, PMID:17912264, DOI:10.1038/nrm2272.
  - Cotter, Stransky, McGuire and Forgac 2015, PMID:26410601, DOI:10.1016/j.tibs.2015.08.005.
  - Mattison et al. 2023, PMID:36074901, DOI:10.1093/brain/awac330.
  - Xu et al. 2019, PMID:31327526, DOI:10.1016/j.cell.2019.06.007.

## Computational checks

I first used the count CSV as the calibration set. It contains 1,674 non-held-out targets in the focal cell group; the response distribution is zero-heavy: 469 targets were nonzero, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and the maximum was 2,677.

I then used `pyarrow.dataset` to scan only focal-cell rows and only mechanistically relevant targets or features from the large parquet. The non-obvious part was the row filter:

```python
scanner = ds.dataset(parquet, format="parquet").scanner(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj",
             "pvals", "scores", "n_pert_matched", "n_ctrl_matched"],
    filter=(
        pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
    ) & pc.field("gene_target").isin(targets),
)
```

`Atp6v0c` itself was a measured transcript in this focal cell group for all 1,674 training signatures, so predicting a singleton target-RNA DEG is at least measurable. Across the five direct V-ATPase training perturbations, `Atp6v0c` was not FDR-significantly changed: log2FCs were -0.017 for `Atp6ap2`, -0.103 for `Atp6v0a1`, -0.072 for `Atp6v1a`, -0.296 for `Atp6v1b2`, and -0.167 for `Atp6v1e1`, all with adjusted `p = 1`. `Atp6v0c` was significant in broader stress programs such as `Uba5`, `Gfpt1`, `Sin3a`, `Ufc1`, and in the lysosomal-compensatory `Rab7` signature, confirming that the feature can move when the cell enters a broader state.

## Analog and counterexample perturbations

| training perturbation | focal `n_degs` | focal signature evidence | use for Atp6v0c |
|---|---:|---|---|
| `Atp6v0a1` | 1 | 197 perturbed nuclei; only significant gene was `Atp6v0a1` itself, log2FC -0.640, FDR 4.52e-12; next best rows were nonsignificant, with `Kcnc2` at FDR 0.125. | Best same-domain anchor. `Atp6v0a1` is a V0 membrane-sector subunit, so its near-flat postnatal neuronal RNA surface argues against a large generic V-ATPase stress program. |
| `Atp6ap2` | 2 | 116 perturbed nuclei; `Atp6ap2` log2FC -1.667, FDR 1.90e-28, and `Atp6v0a1` log2FC -0.341, FDR 1.30e-4; other rows were not called. | V-ATPase accessory/pro-renin receptor comparator. It produced only a two-gene mini-signature and did not secondarily repress `Atp6v0c`. |
| `Atp6v1a` | 0 | 76 perturbed nuclei; minimum FDR was 0.855 and no V-ATPase transcript was significant. | Same holoenzyme, V1 ATP-hydrolysis sector. This is a counterweight against assuming every core pump subunit yields even one called DEG. |
| `Atp6v1b2` | 0 | 32 perturbed nuclei; all FDR values were 1.0. | Same V1 sector but underpowered; useful only as weak evidence that no broad signal was seen. |
| `Atp6v1e1` | 0 | 52 perturbed nuclei; all FDR values were 1.0. | Same V1 sector but underpowered; weak near-flat evidence. |
| `Atp13a2` | 1 | Only its own transcript passed FDR, log2FC -0.613, FDR 2.23e-21. | Lysosomal transporter comparator; supports a "self RNA only" rather than broad lysosomal state. |
| `Lamp2` | 0 | `Lamp2` was knocked down but just missed FDR 0.05, log2FC -0.380, FDR 0.0537. | Lysosome/autophagy comparator that was effectively flat. |
| `Clcn3`, `Clcn4` | 0, 1 | `Clcn4` was a self-only signature; `Clcn3` had no significant genes. | Endosomal pH/ion-channel controls showing that acidification annotation alone did not produce a common module. |
| `Vps41`, `Vps35`, `Vps54`, `Rab7` | 0, 17, 31, 501 | `Rab7` strongly induced V-ATPase transcripts including `Atp6v1b2`, `Atp6v0b`, and `Atp6v0c`; `Vps35` and `Vps54` were modest; `Vps41` had no FDR genes. | Late endosomal/lysosomal trafficking counterexamples. They show the assay can detect a lysosomal response when present, but the breadth is concentrated at a GTPase convergence point and does not transfer to V-ATPase subunits. |

The Distributed Agents corpus independently captured the same local structure: `Atp6v0a1:F003` and `Atp6ap2:F004` support a high-confidence same-experiment claim that V-ATPase subunit membership was not sufficient for a shared postnatal neuronal snRNA-seq module, and `Rab7:F009` reports that measured HOPS, retromer, WASH, V-ATPase, and lysosomal comparator targets mostly failed to phenocopy broad `Rab7` at FDR level.

## Target-specific rationale

`Atp6v0c` encodes the proteolipid c subunit of the membrane V0 sector of vacuolar H+-ATPase. The V-ATPase is an ATP-driven rotary proton pump with a cytosolic V1 ATPase sector and a membrane V0 proton-translocation sector that acidifies lysosomes, endosomes, secretory vesicles, and related organelles (Forgac 2007; Cotter et al. 2015). ATP6V0C variants impair V-ATPase function and cause neurodevelopmental disease with epilepsy, and bacterial SopF blockade of ATP6V0C Gln124 can disable the V-ATPase-ATG16L1 xenophagy axis (Mattison et al. 2023; Xu et al. 2019), so the target is biologically central rather than a peripheral annotation hit.

Despite that central biochemical role, the same-experiment data point toward a very sparse nuclear RNA phenotype in acute, mosaic, P16 neuronal CRISPR. The nearest represented V0 subunit, `Atp6v0a1`, gave only one FDR gene in the focal group, and represented V1 subunits had no called genes. `Atp6ap2` produced two genes but did not look like a shared core-pump response. If `Atp6v0c` editing were converted into a `Rab7`-like late-endosome collapse, I would expect secondary induction of V0/V1 transcripts; that pattern was absent from the direct V-ATPase perturbations. Conversely, a strict zero seems slightly too low because `Atp6v0c` is present in the measured feature space and `Atp6v0a1`, `Atp6ap2`, `Atp13a2`, `Ctsb`, `Clcn4`, `Stx16`, and `Vamp1` demonstrate a common local pattern where an efficiently depleted target RNA contributes the only called gene.

My point prediction is therefore `Atp6v0c = 1`: nonzero because the edited target transcript itself is likely to be detectable, but still a singleton rather than a multi-gene lysosomal or stress program.

## Limits

This is an extrapolation from other pump subunits because no `Atp6v0c` expression signature or count is present in the inputs or in the Distributed Agents corpus. `Atp6v0c` is more universal than `Atp6v0a1`, so complete biallelic loss could have a stronger acidification phenotype than the assayed V0 a1 perturbation. The screen, however, uses sparse AAV CRISPR in postmitotic neurons with modest average mRNA depletion; loss of edited cells, long V-ATPase protein half-life, incomplete editing, or a phenotype expressed at vesicle pH rather than nuclear mRNA could all collapse a real biological effect to zero or one FDR gene. The `Atp6v1b2` and `Atp6v1e1` anchors also had only 32 and 52 matched perturbed nuclei, so their zeros are weaker than the higher-powered `Atp6v0a1` and `Atp6ap2` observations.
