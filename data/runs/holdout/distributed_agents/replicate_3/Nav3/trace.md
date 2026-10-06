# Prediction trace

## Question and endpoint

The requested held-out perturbation list contains one target:

```text
Nav3
```

I interpreted the endpoint as the exact count, in `151 TH Prkcd Grin2c Glut` cells, of measured genes with `pvals_adj < 0.05` after acute AAV-PHP.eB CRISPR-Cas9 perturbation. I did not exclude the perturbed target's own transcript from this count, because the supplied endpoint definition counts measured genes and does not define a downstream-only count.

The main ambiguity I resolved was biological rather than syntactic: `Nav3` itself, and the direct paralogs `Nav1` and `Nav2`, are absent from the supplied training endpoints as perturbed targets, so the closest usable in-dataset analogs are more distant microtubule, motor, axon-guidance, and Rho-GTPase genes.

## Sources

- Primary endpoint calibration: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Primary expression-signature evidence: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Same-experiment semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- Same-experiment profile computations: Distributed Agents runtime `profile_compare` and `profile_neighbors` over focal-cell Wilcoxon-score vectors.
- External literature from NCBI PubMed:
  - Maes, Barcelo, and Buesa 2002, DOI `10.1006/geno.2002.6799`, PMID `12079279`.
  - Martinez-Lopez et al. 2005, DOI `10.1016/j.mcn.2004.09.016`, PMID `15797708`.
  - Muley et al. 2008, DOI `10.1002/dneu.20670`, PMID `18726912`.
  - McNeill et al. 2010, DOI `10.1186/1749-8104-5-6`, PMID `20184720`.
  - Powers et al. 2022, DOI `10.1091/mbc.E21-12-0623`, PMID `35352947`.
  - Powers, Hevner, and Halpain 2023, DOI `10.3389/fnmol.2022.1099554`, PMID `36710926`.
  - Ghaffar et al. 2024, DOI `10.1038/s42003-024-06466-1`, PMID `38977784`.

## Dataset calibration

The 1,674 non-held-out focal-cell training targets are dominated by zeros:

| class | definition | count |
|---|---:|---:|
| none | `n_degs == 0` | 1205 |
| weak | `1 <= n_degs < 10` | 363 |
| medium | `10 <= n_degs < 100` | 63 |
| strong | `n_degs >= 100` | 43 |

The median count is 0 and the 95th percentile is 18; the mean is 14.1 only because a small number of stress/essential-gene perturbations have hundreds to thousands of DEGs. A large prediction for `Nav3` would therefore require a close match to one of those recurrent broad modules.

I first checked exact endpoint counts for literature-obvious analogs:

| analog | `n_degs` | relevance |
|---|---:|---|
| `Dctn1` | 75 | cytoplasmic dynactin and microtubule transport counterexample with a real focal response |
| `Tuba1a` | 7 | tubulin structural gene with a narrow tubulin-isotype response |
| `Tbcd` | 12 | tubulin-folding perturbation, mild but larger than most MAPs |
| `Kifbp` | 2 | kinesin-binding protein |
| `Tuba4a` | 2 | alpha-tubulin paralog |
| `Map1b`, `Mapt`, `Mapre2`, `Kif1a`, `Kif5a`, `Kif5c`, `Stmn2`, `Tubb4b`, `Tubb5` | 1 each | microtubule/MAP/motor genes; all singleton-scale |
| `Map6`, `Kif2a`, `Macf1`, `Dst`, `Plec`, `Camsap1`, `Mark3`, `Nin`, `Ttll5` | 0 each | related structural regulators without focal FDR responses |
| `Dcc`, `Rac1` | 0 | Netrin/Rho pathway comparators |
| `Robo1`, `Cdc42` | 1 each | axon-guidance/Rho pathway comparators with self-like singleton responses |
| `Sema4d`, `Sema6a`, `Plxna1`, `Plxna4`, `Plxnd1`, `Nrp1`, `Nrp2`, `Fyn` | 0 each | semaphorin/plexin or kinase comparators |
| `Sema5a`, `Plxna2` | 1 each | semaphorin/plexin comparators with singleton-scale responses |
| `Gsk3b` | 6 | small CRMP/microtubule pathway response |
| `Dpysl5` | 0 | CRMP-family semaphorin/microtubule effector; broad negative comparator |

The single-DEG calls in this neighborhood are often only the perturbed target transcript: for example, in the focal group the self rows for `Map1b`, `Mapt`, `Kif1a`, `Kif5a`, `Kif5c`, `Robo1`, and `Cdc42` all pass FDR 0.05 with negative Wilcoxon scores. `Dcc` and `Rac1`, by contrast, had no significant focal feature. The held-out `Nav3` symbol is a measured feature in the focal-cell parquet, as are `Nav1` and `Nav2`, so a singleton self-transcript call is possible for `Nav3`.

## Focal-cell profile comparisons

Because `Nav3` has no observed training signature, I used profile comparisons to ask whether the available analogs form a coherent focal-cell expression state:

- Compared the 17,259-feature focal Wilcoxon-score vectors for `Dctn1`, `Tuba1a`, `Map1b`, `Mapt`, `Kif1a`, `Kif5a`, `Robo1`, `Dcc`, `Cdc42`, and `Rac1`.
- Used `pvals_adj < 0.05` only to summarize significant-feature overlap; the signed whole-profile metrics used the continuous Wilcoxon scores.
- Checked each anchor's nearest neighbors within the full eligible 1,674-target training universe and within the manually nominated cytoskeletal/guidance cohort.

Observed focal activity for the ten-node manual cohort:

| target | significant focal features |
|---|---:|
| `Dctn1` | 75 |
| `Tuba1a` | 7 |
| `Map1b`, `Mapt`, `Kif1a`, `Kif5a`, `Robo1`, `Cdc42` | 1 each |
| `Dcc`, `Rac1` | 0 |

The manual cohort did not behave as one shared transcriptional module. Cross-cluster pairs had zero same-direction FDR-gene intersections. Even the strongest same-cohort whole-profile similarities were tiny: `Dctn1` versus `Tuba1a` had Pearson `0.079` and cosine `0.096`; `Dctn1` versus `Kif1a` had Pearson `0.055`; `Dcc` was essentially orthogonal to `Dctn1` with Pearson `-0.0029`. The larger `Dctn1` response was therefore not an averageable cytoskeletal signature for `Nav3`.

This agreed with the Distributed Agents corpus:

- `Dctn1:F001/F006/F007/F009` report a real DCTN1 response but annotate it as SREBF2-like cholesterol/sterol feedback, with canonical kinesins, `Kifbp`, `Hmgcr`, `Srebf1`, and `Vps41` failing to phenocopy it.
- `Tuba1a:F001-F007` report a restricted tubulin-paralog dosage-compensation response, not a generic cytoskeletal injury state; `Tuba4a`, `Tubb4b`, `Tubb5`, `Map1b`, `Kif5a`, `Spast`, and `Stmn2` did not reproduce that signature.
- Corpus claim `claim:edf51d701dda34edf161` states that represented MAP, tubulin, EB, dynactin, kinesin, CAMSAP, and MARK-related perturbations generally do not form a coherent shared postnatal neuronal mRNA compensation or cytoskeletal-stress module apart from the narrow `Tuba1a` exception.
- `Dpysl5:F001-F004` and claim `claim:a7dd17e62ac7ac776021` report that represented semaphorin/plexin/neuropilin, CRMP, kinase, and microtubule comparators had near-zero or nonoverlapping snRNA signatures in this same experiment.

## Biology of `Nav3`

NAV3 is one of three vertebrate Neuron Navigator proteins, descendants of the axon-guidance gene `unc-53`. NAVs combine actin- and microtubule-associated N-terminal regions, SxIP-like microtubule plus-end interaction motifs, coiled-coils, and a C-terminal AAA+ ATPase-like domain; they are generally interpreted as cytoskeletal response proteins coupling extracellular cues, actin, microtubules, and membrane traffic during neuronal morphogenesis (Maes et al. 2002; Powers, Hevner, and Halpain 2023).

The external evidence supports a real neuronal morphogenesis function but points mostly to developmental morphology and growth-cone behavior, not to a late postmitotic nuclear-RNA feedback circuit:

- `Nav1` is a microtubule-associated growth-cone protein needed for Netrin-1-induced directional migration in mouse pontine migration assays (Martinez-Lopez et al. 2005).
- `Nav1` depletion changes growth-cone actin/microtubule behavior and BDNF/TrkB-associated macropinocytosis in cultured neurons (Powers et al. 2022).
- `Nav2` is an all-trans retinoic-acid-responsive neurite-outgrowth gene; human NAV2 rescues `unc-53` axon-elongation defects and NAV2 loss impairs atRA-driven neurite outgrowth in SH-SY5Y cells (Muley et al. 2008), while mouse `Nav2` hypomorphic embryos show reduced nerve-fiber density and cranial-nerve defects (McNeill et al. 2010).
- Direct `NAV3` human genetics now link pathogenic variants to intellectual disability, developmental delay, and microcephaly; in that study pathogenic NAV3 variants impaired microtubule stabilization in heterologous cells and zebrafish `nav3` knockdown caused microcephaly, impaired neuronal growth, and behavioral defects rescued by wild-type human NAV3 RNA (Ghaffar et al. 2024).

That biology puts `Nav3` closest to microtubule plus-end, neurite-outgrowth, and axon-guidance nodes. It does not tie `Nav3` to the `Dctn1`/`Rab7`/SREBF2 lipid-feedback arm or to the very specific `Tuba1a` loss-of-structural-tubulin compensation program.

## Target-specific prediction

### `Nav3`

Relevant within-dataset analogs:

- Nearest mechanistic class, microtubule/MAP/motor genes: `Map1b = 1`, `Mapt = 1`, `Mapre2 = 1`, `Kif1a = 1`, `Kif5a = 1`, `Kif5c = 1`, `Stmn2 = 1`, `Kifbp = 2`, while `Map6`, `Kif2a`, `Macf1`, `Dst`, `Plec`, `Camsap1`, `Mark3`, `Nin`, and `Ttll5` were 0.
- Direct cytoskeletal positive controls: `Tuba1a = 7`, `Tbcd = 12`, `Dctn1 = 75`. These show that the focal cell class can report some cytoskeletal perturbations, but the Distributed Agents corpus and the focal score-vector comparison indicate that those responses are special cases: `Tuba1a` up-regulates tubulin paralog transcripts and `Dctn1` activates a sterol/lipid module.
- Guidance/Rho comparators: `Dcc = 0`, `Rac1 = 0`, `Cdc42 = 1`, `Robo1 = 1`, `Robo2 = 0`, semaphorin/plexin/neuropilin targets mostly 0 or 1.
- CRMP/semaphorin downstream analog: `Dpysl5 = 0`, with Distributed Agents corpus evidence that it lacks a hidden semaphorin-plexin/microtubule mRNA state.

Zero/nonzero decision: I predicted a weak nonzero rather than a hard zero. The broader downstream `Nav3` response should be absent or extremely small in a P16-to-P37/P44 sparse postmitotic screen, because the local dataset repeatedly turns morphogenesis, microtubule-adaptor, and axon-guidance perturbations into 0- or 1-DEG surfaces. However, `Nav3` is a measured transcript in the focal cell group, and the most comparable 1-DEG motor/MAP/guidance examples often consist of significant self-transcript depletion with no substantial secondary program. That made exactly one FDR gene a better point estimate than 0 or a `Tuba1a`-like 7.

Predicted count: `1`.

## Limits and extrapolation

- There is no direct `Nav3`, `Nav1`, or `Nav2` training perturbation in either input file, and the same-experiment Distributed Agents corpus has no `Nav3` report. All training comparisons are therefore pathway-level rather than paralog-level.
- The external `NAV3` evidence is partly from human genetics, zebrafish knockdown, and heterologous or developmental models. Those establish morphogenetic plausibility but are displaced from an acute mosaic mouse neuron CRISPR perturbation at P16.
- The snRNA-seq endpoint is nuclear RNA in recovered cells; it can miss axon length, growth-cone guidance, membrane trafficking, electrophysiology, and late wiring phenotypes.
- I treated self-transcript calls as part of the requested count, but the hidden `Nav3` guides' actual indel spectrum, target-mRNA reduction, and matched cell recovery are unknown. If `Nav3` self RNA does not pass FDR, the biologically broader argument would favor 0.
