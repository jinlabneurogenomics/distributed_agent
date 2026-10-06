# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question interpreted

The requested held-out perturbation list contains one gene, `Atp6ap1`. I interpreted `n_degs` as the number of measured genes, including the perturbed target transcript itself if it passes, with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` single-nucleus differential-expression table. `Atp6ap1` is absent from both supplied training inputs, so the prediction has to be transferred from non-held-out targets.

I treated zeros as assay endpoints rather than as evidence that the perturbed biology is harmless: this is sparse P16 AAV CRISPR loss-of-function in recovered NeuN+ nuclei, and the count is a BH-corrected nuclear RNA breadth metric.

## Sources used

- Input target manifest: `020_Atp6ap1.csv`.
- Training endpoint table: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Training differential-expression parquet: `training_de_all_cell_groups.parquet`.
- Same-experiment semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  - No `Atp6ap1` report, claim, or comparator edge was present in this release.
  - `Atp6ap2`, `Atp6v0a1`, `Atp6v1a`, and `Atp6v1e1` reports were used to check the corpus interpretation of direct V-ATPase components.
- Distributed Agents runtime profile comparison over `Atp6ap2`, `Atp6v0a1`, `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` in the focal cell group, written as `vatpase_profile_compare.json` and inspected through `vatpase_profile_inspect.json`.
- External biology from PubMed-indexed literature:
  - Jansen et al. 2016, Nature Communications, DOI `10.1038/ncomms11600`, PMID `27231034`: human ATP6AP1/Ac45 is the ortholog of the yeast V-ATPase assembly factor Voa1, and ATP6AP1 variants cause an X-linked immunodeficiency/hepatopathy/glycosylation disorder with variable neurocognitive findings.
  - Abbas et al. 2020, Science, DOI `10.1126/science.aaz2924`, PMID `32165585`: rat-brain V-ATPase structure places ATP6AP1/Ac45 and ATP6AP2/PRR in the V0 membrane region and shows how they help assemble the catalytic V1 and membrane V0 sectors.
  - Jansen and Martens 2012, Current Protein & Peptide Science, DOI `10.2174/138920312800493160`, PMID `22044156`: review of ATP6AP1/Ac45 and ATP6AP2/PRR as distinct V-ATPase accessory subunits, including neuroendocrine vesicle-acidification roles.
  - Zoncu et al. 2011, Science, DOI `10.1126/science.1207056`, PMID `22053050`: V-ATPase-Ragulator signaling couples lysosomal amino acid sensing to mTORC1, making lysosomal acidification capable of producing growth-state transcriptional outputs.

## Dataset computations

I first read the requested manifest and confirmed that the only target was `Atp6ap1`. I then scanned the focal-cell training count CSV for V-ATPase subunits/accessory genes and nearby lysosomal or trafficking genes. Directly relevant focal-cell counts were:

| training target | 151 TH Prkcd Grin2c Glut `n_degs` | focal signature summary from the parquet |
|---|---:|---|
| `Atp6ap2` | 2 | `Atp6ap2` itself down, logFC -1.667, FDR 1.90e-28; `Atp6v0a1` down, logFC -0.341, FDR 1.30e-4 |
| `Atp6v0a1` | 1 | only `Atp6v0a1` itself down, logFC -0.640, FDR 4.52e-12 |
| `Atp6v1a` | 0 | no focal gene below FDR 0.05 |
| `Atp6v1b2` | 0 | no focal gene below FDR 0.05 |
| `Atp6v1e1` | 0 | no focal gene below FDR 0.05 |
| `Atp13a2` | 1 | only `Atp13a2` itself down |
| `Ctsb` | 1 | only `Ctsb` itself down |
| `Lamp2` | 0 | `Lamp2` was the nearest row but remained just above threshold, logFC -0.380, FDR 0.0537 |
| `Becn1` | 0 | no focal genes below FDR 0.05 |
| `Mtor` | 2 | `Rims3` up and `Tmed8` down; not a V-ATPase/lysosome expression module |
| `Vps41` | 0 | no focal genes below FDR 0.05 |
| `Vps35` | 17 | retromer/trafficking state; some overlap with thalamic activity/ion-handling genes, not a direct pump phenocopy |
| `Vps54` | 31 | GARP/endosome-traffic response with `Egr1`, `Jun`, and cytoskeletal genes; indirect counterexample |
| `Rab7` | 501 | broad late-endosome response, with V-ATPase/lysosomal genes up (`Atp6ap1`, `Atp6v0a1`, `Atp6v0b`, `Atp6v1a`, `Atp6v1b2`, `Lamp2`, `Map1lc3b`, `Sqstm1`) |

The parquet inspection was restricted to `group_name == "151 TH Prkcd Grin2c Glut"` and biologically nominated training targets, then sorted genes by `pvals_adj`. I also queried candidate lysosomal and stress sentinel rows (`Atp6ap1`, `Atp6ap2`, `Atp6v0a1`, `Atp6v1a`, `Atp6v1b2`, `Atp6v1e1`, `Lamp2`, `Map1lc3b`, `Sqstm1`, `Tfeb`, `Tfe3`, `Atf4`, `Ddit3`, `Hspa5`) to distinguish a real lysosomal compensation program from one self-transcript hit.

The critical pattern was that `Rab7` showed the assay could detect thalamic lysosome/V-ATPase compensation when it became transcriptional, but direct perturbations of the represented pump subunits did not produce that state. `Atp6ap2` did not move `Atp6ap1` in the focal class (`Atp6ap1` logFC 0.035, FDR 1), and direct `Atp6v0a1` loss left `Atp6ap1`, `Atp6ap2`, the V1 subunits, `Lamp2`, `Map1lc3b`, `Sqstm1`, `Tfeb`, `Tfe3`, `Atf4`, `Ddit3`, and `Hspa5` at FDR 1. The five-target V-ATPase runtime profile audit likewise found only two of five targets with any focal FDR<0.05 features, with 2, 1, 0, 0, and 0 significant genes.

## Target-specific reasoning

### `Atp6ap1`

ATP6AP1/Ac45 is not just a remote lysosomal annotation; it is an accessory component of the V-ATPase V0 sector, next to ATP6AP2/PRR in mammalian brain V-ATPase structures, and ATP6AP1 disease alleles impair V-ATPase assembly and organelle acidification. That makes `Atp6ap2`, `Atp6v0a1`, and the three represented V1 subunit targets the most appropriate first analogs.

The closest in-dataset analog is `Atp6ap2`, another V-ATPase accessory protein. In the focal cell class `Atp6ap2` produced exactly two FDR<0.05 genes, its own self-transcript and `Atp6v0a1`. This supports a small nonzero count for an accessory-factor perturbation, but the signature was not a full TFEB/autophagy/UPR response: `Map1lc3b`, `Sqstm1`, `Tfeb`, `Tfe3`, `Atf4`, `Ddit3`, and `Hspa5` were all FDR 1 after `Atp6ap2` perturbation in the same cells.

`Atp6v0a1` is an even more direct pump subunit counterweight. It is the neuronal V0 a1 subunit, but in the focal cell class its only FDR<0.05 row was `Atp6v0a1` itself. The same-experiment corpus summarized the whole surface as self-detected in several groups but downstream-flat, and it explicitly found that represented V-ATPase relatives and lysosomal disease comparators were flat or near-flat rather than a common proton-pump transcriptomic module.

The V1 subunits are a floor estimate. `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` had zero FDR<0.05 genes in `151 TH Prkcd Grin2c Glut`; `Atp6v1a` and `Atp6v1e1` had sparse responses elsewhere, but they did not share the `Atp6ap2` focal `Atp6v0a1` decrease. These targets argue that same-pump membership alone should not be inflated into a dozens-of-DEGs prediction.

Nearby lysosomal/autophagy controls supported the same calibration. `Atp13a2` and `Ctsb` each produced self-only focal counts; `Lamp2` and `Becn1` were at zero; `Mtor` was two genes but not a lysosomal acidification signature. `Rab7` is the main positive counterexample: it induced 501 focal DEGs and up-regulated `Atp6ap1`, V-ATPase subunits, `Lamp2`, `Map1lc3b`, and `Sqstm1`. I treated that as evidence that the screen can report late-endosomal stress, but not as the quantitative template for `Atp6ap1`, because the direct pump/accessory perturbations were much smaller and the corpus reports specifically warn that Rab7, retromer/HOPS, and V-ATPase components do not phenocopy each other at the FDR level.

My zero/nonzero decision is therefore nonzero but minimal. `Atp6ap1` is likely expressed in the focal cells, since it was significantly up-regulated after `Rab7` loss, and its closest accessory paralog `Atp6ap2` yielded a focal self hit plus `Atp6v0a1`. However, all direct evidence says acute sparse disruption of V-ATPase components in recovered juvenile neurons stays at the self-transcript / one-neighbor boundary. I predict one FDR<0.05 gene for `Atp6ap1`, most plausibly the self row or the same `Atp6v0a1` secondary row, not a broad TFEB, UPR, autophagy, or Rab7-like program.

## Final prediction

| target | predicted `n_degs` |
|---|---:|
| `Atp6ap1` | 1 |

## Limits and extrapolation

- The Distributed Agents corpus contained no direct `Atp6ap1` report in this held-out-aware release, so the target-specific call extrapolates from `Atp6ap2` and represented V-ATPase subunits.
- The prediction is about BH-corrected snRNA DE in recovered `151 TH Prkcd Grin2c Glut` nuclei. It does not measure V-ATPase protein, lysosomal pH, autophagic flux, glycosylation, synaptic-vesicle acidification, or edited-cell depletion.
- `Atp6ap1` and `Atp6ap2` are both V0-associated accessory proteins, but they are not interchangeable: ATP6AP2 also has PRR/Wnt/RAS annotations, while ATP6AP1 is the Ac45/Voa1-like factor. The shared V-ATPase location justified a low-count analog, not a pooled average.
- Several direct pump comparators had low focal perturbed-nucleus counts, and V1-subunit self-transcripts did not pass FDR in the focal class. Their zeros reduce confidence in a broad response, but they cannot prove that a stronger biallelic `Atp6ap1` lesion would be transcriptionally silent.
- Large positive endolysosomal signatures from `Rab7`, `Vps35`, and `Vps54` could mark pathway-adjacent injury states that `Atp6ap1` might partially enter under stronger loss. The direct accessory and core V-ATPase perturbations in this exact screen were more relevant for this prediction, so I kept the point estimate near one.
