# Nrl prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one target, `Nrl`. I interpreted the requested value as a point prediction for the number of genes with `pvals_adj < 0.05` after acute sparse CRISPR loss of `Nrl` in the focal `151 TH Prkcd Grin2c Glut` neuronal group. Because `Nrl` was completely held out, there is no `Nrl` row in either the focal DEG-count training CSV or the differential-expression parquet; all quantitative evidence below comes from non-held-out perturbations measured in the same cell group, and the biological extrapolation is from the role of NRL in retinal photoreceptor identity.

The answer file therefore needs one row, preserving the manifest spelling exactly:

- `Nrl`

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene Wilcoxon differential-expression results for non-held-out perturbations. I used the rows with `group_name == "151 TH Prkcd Grin2c Glut"` to examine the focal expression signatures and their adjusted p values.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for 1,674 non-held-out perturbations in the focal cell group. The distribution is zero-heavy: 1,205/1,674 perturbations have `n_degs = 0`, while strong general perturbations such as `Uba5`, `Tpr`, and `Sin3a` have 2,677, 1,768, and 1,433 DEGs.
- `159_Nrl.csv`: the requested held-out target list.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`: I used same-experiment bottom-up findings for retinal and photoreceptor-lineage targets, especially `Crx`, `Nr2e3`, and `Otx2`, and an induced topology query over represented photoreceptor-axis perturbations.
- Distributed Agents runtime profile comparison: I compared Wilcoxon score vectors among the focal-cell analog cohort `Crx`, `Nr2e3`, `Otx2`, `Rorb`, `Thrb`, `Rho`, `Opn1sw`, `Maf`, `Mafa`, `Mafb`, `Mafg`, `Rora`, and `Nr1d1` using `scores` as the signed profile value and `pvals_adj < 0.05` as the significant tail. The run-local artifact is `profile_compare_photoreceptor_maf.json`.
- PubMed via NCBI E-utilities for external biology:
  - Mears et al., 2001, *Nature Genetics*, DOI `10.1038/ng774`, PMID `11694879`: mouse `Nrl` is required for rod photoreceptor development; `Nrl-/-` retinas lose rod function and acquire an S-cone-like fate, with `Nrl` proposed to drive rod genes and suppress the S-cone pathway through `Nr2e3`.
  - Montana et al., 2011, *Journal of Biological Chemistry*, DOI `10.1074/jbc.M111.279026`, PMID `21865162`: `Crx`, `Otx2`, and `Rorb` directly regulate the mouse `Nrl` promoter in retina.
  - Liang et al., 2022, *Human Molecular Genetics*, DOI `10.1093/hmg/ddac143`, PMID `35776116`: NRL is a Maf-family bZIP transcription factor that cooperates with CRX and other factors to establish rod morphogenesis and maturation programs in mammalian retina.

## Computational checks

I first verified that the manifest contains exactly one held-out target and that `Nrl` is absent from the focal training-count CSV. I then filtered the parquet to the focal cell group and to biologically obvious retinal or Maf-family comparators, counting `pvals_adj < 0.05` for each target. In pandas/pyarrow terms, the central operation was:

```python
filter = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(comparator_targets)
)
```

For each retained `gene_target`, I counted significant rows and inspected the smallest adjusted p values and largest absolute Wilcoxon-score genes to make sure zeros in the count file corresponded to flat focal signatures rather than a mismatch between inputs. I also inspected measured photoreceptor sentinel transcripts such as `Nrl`, `Crx`, `Nr2e3`, `Gnat1`, `Pde6b`, `Rho`, and `Opn1sw` across all 1,674 focal-cell training perturbations; `Nrl` itself had `pvals_adj = 1.0` in every training signature, consistent with a transcript at the assay floor in this non-retinal group rather than a regulated focal-cell marker.

## Target-specific reasoning

### `Nrl`

**Biological prior.** `Nrl` encodes a neural retina leucine zipper, Maf-family bZIP transcription factor. Its best established autonomous role is not a broad thalamic one: it is a rod-photoreceptor fate determinant that partners with CRX and other retinal factors to activate rod genes, and germline mouse loss converts would-be rods toward an S-cone-like state rather than simply producing a generic stress response (Mears et al. 2001; Liang et al. 2022). The upstream regulators that initiate or maintain retinal `Nrl` expression include `Crx`, `Otx2`, and `Rorb` acting on the `Nrl` promoter in retinal explants (Montana et al. 2011). That makes the correct within-dataset analogs the CRX/OTX/RORB/NR2E3 photoreceptor specification axis and the large-Maf relatives, not arbitrary high-DEG transcription factors.

**Observed focal-cell analogs.** In the `151 TH Prkcd Grin2c Glut` DEG-count training set, the retinal axis is almost completely FDR-null:

| training perturbation | `n_degs` | focal-cell interpretation |
| --- | ---: | --- |
| `Crx` | 0 | direct NRL partner and photoreceptor/pineal regulator; no focal FDR genes |
| `Nr2e3` | 0 | canonical NRL downstream rod-vs-cone nuclear receptor; no focal FDR genes |
| `Otx2` | 0 | upstream retinal/pineal regulator of `Nrl`/`Crx`; no focal FDR genes |
| `Rorb` | 0 | upstream retinal regulator of `Nrl`; no focal FDR genes |
| `Thrb` | 0 | cone/retinal nuclear receptor comparator; no focal FDR genes |
| `Rho` | 0 | NRL/CRX rod phototransduction output gene; no focal FDR genes |
| `Opn1sw` | 0 | S-cone opsin comparator for the cone fate derepressed in `Nrl-/-` retina; no focal FDR genes |
| `Rxra`, `Rxrb`, `Rxrg` | 0, 0, 0 | retinoid/nuclear receptor family comparators; no focal FDR genes |
| `Rax`, `Pax6`, `Neurod1`, `Vsx2` | 0, 0, 0, 0 | broader retinal developmental comparators; no focal FDR genes |

The same negative call holds when looking at expression-pattern evidence in the parquet, not just the final count file. In the focal cell group, `Crx`, `Nr2e3`, `Otx2`, `Rorb`, `Thrb`, `Rho`, and `Opn1sw` each have 17,259 measured gene rows and zero genes with `pvals_adj < 0.05`. Their smallest adjusted p values were weak to exactly null: `Crx` 1.0, `Rorb` 1.0, `Thrb` 1.0, `Otx2` 0.885, `Nr2e3` 0.830, `Rho` 0.661, `Opn1sw` 1.0. The Distributed Agents corpus summarizes the same experimental result at the whole-brain level: `Crx:F001` found no downstream gene at FDR < 0.10 in any recovered brain group; `Crx:F002` found no canonical phototransduction or pineal melatonin output; `Nr2e3:F001/F002` found no accepted rod/cone response in recovered neuronal groups; and `Otx2:F001/F004/F005` found an all-null Otx2 surface and no Otx/retinal phenocopy. A Distributed Agents candidate-set topology over ten represented retinal-axis genes placed all ten in one explicit-reference component, but that component describes a negative, off-lineage module: the connected pair fraction was 24/45, driven by findings such as `Crx:F003`, `Nr2e3:F002`, `Otx2:F005`, and `Opn1sw:F003`, all of which reject a hidden shared photoreceptor-like brain signature.

`Nrl` is Maf-family, so I also treated the large-Maf and bZIP relatives as a countercheck. The focal training counts were `Maf = 0`, `Mafa = 0`, `Mafb = 0`, and `Mafg = 1`; the broader CNC/small-Maf or AP-1-like represented targets `Nfe2l1`, `Nfe2l2`, `Bach2`, `Fosl2`, `Jund`, and `Atf6` were also 0. The focal score-vector comparison did not reveal a hidden convergent transcriptional state among these flat vectors: among the inspected anchors, `Crx`, `Nr2e3`, `Otx2`, and `Maf` each had zero significant features; their within-cohort whole-profile Pearson correlations were near zero, for example `Crx` to `Nr2e3` was 0.012 and `Nr2e3` to `Otx2` was 0.023. The nearest all-eligible neighbors of `Crx` in the focal score vector had similarly tiny Pearson values around 0.06-0.07, which is the expected scale for null-vector noise.

**Counterexamples considered.** The focal group is capable of showing strong transcription-factor and nuclear-receptor phenotypes. `Rora`, a nuclear receptor with a strong response in this same focal group, had 278 focal DEGs, and `Nr1d1` had 116. Those are inappropriate positive templates for `Nrl` because they operate in focal neuronal programs rather than the retina-specific NRL rod-fate module, but they are important controls: a zero prediction for `Nrl` is not based on a belief that postmitotic neuronal CRISPR cannot yield detectable transcriptional responses.

**Zero/nonzero decision and point estimate.** I predict `Nrl` will have no genes passing FDR 0.05 in `151 TH Prkcd Grin2c Glut`. This is driven primarily by within-dataset evidence: every represented direct regulator, partner, downstream rod/cone output, and large-Maf paralog that would make a photoreceptor-like NRL module plausible was flat in the same focal cell group. The external literature pushes in the same direction because it places NRL in a retinal rod-developmental circuit that is absent from this P16 NeuN+ whole-brain assay. The appropriate integer is therefore exactly 0 rather than a small positive singleton.

## Limits

`Nrl` itself was held out, so the prediction is an extrapolation from pathway members and paralogs rather than a direct Nrl-gRNA measurement. The CRISPR experiment did not measure DNA indels or protein loss per cell, and the average mRNA depletion per gRNA is modest; a weak unobserved NRL effect cannot be excluded. The focal `151 TH Prkcd Grin2c Glut` cells are not retinal photoreceptors, and the pineal compartment is sparse and coarse in this assay, so the comparison says the NRL retinal/pineal program should be off-lineage here, not that `Nrl` is unimportant in its native tissues. Finally, most null-vector correlations are dominated by rank noise; I used them only as evidence against strong hidden convergence, not as positive biology.

## Final prediction

| target | predicted `n_degs` |
| --- | ---: |
| `Nrl` | 0 |
