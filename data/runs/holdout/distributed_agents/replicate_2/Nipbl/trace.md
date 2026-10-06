# Prediction trace

## Question interpreted

The held-out manifest contains one target, `Nipbl`. I interpreted the task as:

- predict the `151 TH Prkcd Grin2c Glut` endpoint for `Nipbl`, namely the number of measured genes with `pvals_adj < 0.05` after acute P16 AAV-CRISPR loss of the target gene;
- use only the non-held-out training differential-expression signatures and training `n_degs` counts for calibration;
- use external biology only to decide which observed perturbations are appropriate mechanistic analogs or counterexamples.

The perturbation is sparse, postnatal, in-vivo CRISPR loss of function in NeuN+ nuclei. I did not treat germline or complete-depletion cohesin phenotypes as quantitatively interchangeable with this assay.

One wording ambiguity is that some same-experiment Distributed Agents corpus summaries use an exploratory `FDR < 0.10` signature while the requested endpoint is the stricter `FDR < 0.05` count. I used the corpus for qualitative same-experiment context, but all numeric endpoint counts below come from the supplied `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` or from directly recomputing `pvals_adj < 0.05` over the focal-cell rows of the parquet.

## Sources used

Internal/run-local data:

- `[local file: 151_Nipbl.csv]`
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`
- `cohesin_profile_neighbors.json`, generated with the Distributed Agents runtime `profile_neighbors` tool for the available cohesin/chromatin-loop anchors in `151 TH Prkcd Grin2c Glut`.

Internal Distributed Agents knowledge layer:

- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- `target_context(Nipbl)` returned no stored finding in this release.
- `target_context(Smc1a)`, `target_context(Stag2)`, `target_context(Ctcf)`, and `candidate_set_topology([Smc1a, Stag1, Stag2, Pds5a, Hdac8, Ctcf])` were used for same-experiment interpretation of represented cohesin-axis perturbations.

External literature from NCBI PubMed:

- Tonkin et al. 2004, Nature Genetics, DOI `10.1038/ng1363`, PMID `15146185`: `NIPBL` encodes a vertebrate Scc2/Nipped-B homolog mutated in Cornelia de Lange syndrome.
- Davidson et al. 2019, Science, DOI `10.1126/science.aaz3418`, PMID `31753851`: purified human cohesin extrudes DNA loops and loop formation/maintenance requires cohesin ATPase activity plus `NIPBL`-`MAU2`.
- Shi et al. 2020, Science, DOI `10.1126/science.abb0981`, PMID `32409525`: structural work showed extensive cohesin-NIPBL-DNA contacts and NIPBL/DNA-mediated engagement of the cohesin ATPase heads.
- Parenti et al. 2020, Cell Reports, DOI `10.1016/j.celrep.2020.107647`, PMID `32433956`: `NIPBL` and `MAU2` form the vertebrate cohesin-loader heterodimer, and disruption of the NIPBL-MAU2 interface is CdLS-relevant.
- Luppino et al. 2022, PLoS Genetics, DOI `10.1371/journal.pgen.1010528`, PMID `36449519`: in HCT116 cells, NIPBL depletion rewired thousands of genes and was functionally balanced by WAPL or CTCF co-depletion, supporting transcriptional sensitivity to altered cohesin extrusion.
- Alonso-Gil et al. 2023, Nature Communications, DOI `10.1038/s41467-023-36900-7`, PMID `36898992`: low NIPBL perturbs STAG1- and STAG2-containing cohesin differently; STAG2 is diminished genome-wide while STAG1 can remain at CTCF sites despite impaired folding.

## Dataset calculations

I confirmed that the manifest has exactly one requested held-out target:

```text
target_name
Nipbl
```

The focal training count table contains 1,674 perturbations. Its endpoint is heavily zero-inflated:

- 1,205/1,674 training targets had `n_degs = 0`.
- 469/1,674 had at least one DEG.
- median `n_degs = 0`; 75th percentile = 1; 90th percentile = 2; 95th percentile = 18; 99th percentile = 436.
- The broadest responses were large outliers: `Uba5` = 2677, `Tpr` = 1768, `Sin3a` = 1433.

Using DuckDB predicate pushdown on `training_de_all_cell_groups.parquet`, the focal cell group has 28,891,566 rows across the same 1,674 training perturbations and 17,259 measured genes.

I then queried focal rows for the available cohesin and chromatin-loop comparators and verified the FDR 0.05 counts:

| training target | focal perturbed nuclei | observed `n_degs` |
|---|---:|---:|
| `Smc1a` | 135 | 24 |
| `Stag1` | 126 | 0 |
| `Stag2` | 193 | 37 |
| `Pds5a` | 137 | 0 |
| `Hdac8` | 111 | 0 |
| `Ctcf` | 129 | 270 |
| `Chd4` | 163 | 100 |
| `Brd4` | 93 | 311 |
| `Med13` | 154 | 11 |
| `Kmt2a` | 161 | 24 |
| `Wac` | 124 | 384 |
| `Yy1` | 265 | 720 |

The direct `Nipbl` binding partner `Mau2` and the most direct core-ring targets `Rad21` and `Smc3` were not represented in the training endpoint. Among represented cohesin-machinery perturbations, `Smc1a` and `Stag2` were the only clearly positive ones. At `FDR < 0.05`, `Smc1a` and `Stag2` shared 9 significant downstream genes, all in the same direction:

```text
Adamts19, Adamts2, Inhbb, Necab2, Ptprm, Sema5a, Smtn, Sox13, Utp14b
```

The largest effects were a down-regulated adhesion/extracellular-matrix/guidance module: `Ptprm`, `Necab2`, `Adamts2`, `Sema5a`, `Smtn`, and `Adamts19`. Distributed Agents same-experiment summaries, computed over a slightly looser signature, make the same qualitative call: the `Smc1a`/`Stag2` module is a restricted thalamic postmitotic neuronal program; `Stag1`, `Pds5a`, `Hdac8`, `Ncapd3`, `Prr12`, `Smchd1`, and `Zfp609` do not reproduce it; and `Ctcf` is a broader Pcdh-heavy response rather than a simple phenocopy of represented cohesin subunits.

I also generated `cohesin_profile_neighbors.json` by comparing `Smc1a`, `Stag1`, `Stag2`, `Pds5a`, `Hdac8`, and `Ctcf` to all 1,674 eligible observed perturbations in the focal cell group with signed log-fold-change profiles. I used this mainly as an audit artifact, because `Nipbl` has no profile to compare directly and the whole-profile correlations among observed targets were inflated by shared extreme low-support fold-change coordinates with `pvals_adj = 1`. The significant-program evidence and endpoint counts were more trustworthy for the point estimate.

## Target-specific reasoning

### `Nipbl`

`Nipbl` is not in either training input, and the selected Distributed Agents corpus release has no direct `Nipbl` finding, so the prediction is extrapolated from represented cohesin components plus outside mechanism.

`Nipbl` is still mechanistically closer to the responding `Smc1a`/`Stag2` pair than to the null accessory factors. NIPBL-MAU2 is the cohesin loader and an ATPase activator for loop extrusion; purified cohesin requires NIPBL-MAU2 to extrude loops, and the human cohesin-NIPBL-DNA structure shows extensive NIPBL contacts with the ring and DNA. A direct link to the `Stag2` training signature is also plausible: NIPBL depletion affects STAG1- and STAG2-cohesin differently and reduces genome-wide STAG2 cohesin, matching the observation that the represented thalamic module is `Stag2`/`Smc1a`-linked rather than `Stag1`-linked.

The null training relatives are important counterexamples rather than reasons to set `Nipbl` to zero. `Pds5a` and `Hdac8` regulate cohesin residence or recycling rather than supplying the loader's DNA-loop-extrusion activity, and `Stag1` is an alternate SA paralog rather than the STAG2-containing complex implicated by the dataset. Their focal sample sizes were comparable to `Smc1a` and `Ctcf`, so their zeros show that this assay separates cohesin-axis perturbations; they do not eliminate the positive `Smc1a`/`Stag2` prior.

I used `Ctcf` = 270, `Brd4` = 311, `Wac` = 384, and `Yy1` = 720 as upper-bound counterexamples. They all participate in chromatin organization or enhancer regulation, but their much broader 151 TH signatures show pan-regulatory or CTCF-specific outputs that the represented core cohesin perturbations did not phenocopy. `Bptf` = 65, `Chd4` = 100, `Setdb1` = 22, `Nsd1` = 23, `Ankrd11` = 20, and `Kmt2a` = 24 provided a more compact chromatin-regulator band.

Putting those pieces together, I predict a positive but compact response: bigger than the single best direct observed subunit, `Stag2` at 37, because NIPBL acts upstream of loop extrusion and can affect both CTCF-anchored and enhancer-loaded cohesin, but still far below `Ctcf` and broad enhancer/transcription cofactors. I used a point estimate of **58 DEGs**, near the upper end of the `Smc1a`/`Stag2` module and just below the compact `Bptf` chromatin response.

## Limits

This is a real extrapolation. The cleanest `Nipbl` analogs, `Mau2`, `Rad21`, `Smc3`, and `Wapl`, are absent from the training counts. The screen is a partial, sparse, AAV-CRISPR perturbation in already postmitotic neurons, whereas most external NIPBL/cohesin data use complete depletion, cultured cell lines, cycling cells, or developmental models. `n_degs` is also highly power-dependent: the observed zeros for `Stag1`, `Pds5a`, and `Hdac8` could hide weak biology or lower effective editing, and the nonzero prediction for `Nipbl` assumes that loader loss crosses the FDR 0.05 threshold in this thalamic class. Finally, the prediction transfers pathway structure but not a measured `Nipbl` expression profile, because the held-out target was absent from the supplied signatures by design.
