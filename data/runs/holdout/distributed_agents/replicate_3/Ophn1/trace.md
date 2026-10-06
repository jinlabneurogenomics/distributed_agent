# DEG-count prediction for held-out `Ophn1`

## Question interpreted

The manifest `[local file: 162_Ophn1.csv]` contains one requested held-out target:

```tsv
target_name
Ophn1
```

I interpreted the endpoint exactly as the focal-cell `n_degs`: the number of measured genes, including the perturbed gene itself if it would pass, with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`. `Ophn1` is absent from both training inputs, so I used only non-held-out perturbations for calibration and treated OPHN1 biology as prior information.

One minor naming point: `151 TH Prkcd Grin2c Glut` is the Allen-style thalamic glutamatergic group name; `TH` is thalamus, not tyrosine hydroxylase.

## Sources used

- Input DE parquet: `[local file: training_de_all_cell_groups.parquet]`
- Focal training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest: `[local file: 162_Ophn1.csv]`
- Same-experiment semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`
- Run-local Distributed Agents profile-neighbor analysis over the focal 151 expression profiles
- External biological knowledge from PubMed-indexed literature and Reactome, especially OPHN1/RhoGAP, Rho-GTPase, postsynaptic-density, AMPAR-endocytosis, and mGluR-LTD biology

## Training-data computations

The focal count table has 1,674 eligible non-held-out targets. It is very sparse:

- 1,205 / 1,674 targets have `n_degs = 0`.
- 469 / 1,674 are nonzero.
- Median `n_degs = 0`; the 75th percentile is 1.
- Only 63 training targets are in the 10-89 DEG range and only 43 are `>=100`.

I queried the large parquet with DuckDB, filtering to `group_name = '151 TH Prkcd Grin2c Glut'`, to verify that `Ophn1` has no row as `gene_target` and to inspect OPHN1-relevant training genes. The aggregation was conceptually:

```sql
select
  gene_target,
  count(*) as measured,
  sum(pvals_adj < 0.05) as n_degs_focal,
  min(pvals_adj) as min_padj,
  any_value(n_pert_matched) as n_pert_matched,
  any_value(n_ctrl_matched) as n_ctrl_matched
from training_de_all_cell_groups
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (<OPHN1-relevant training targets>)
group by gene_target;
```

Each focal target slice had 17,259 measured genes and 23,679 matched control nuclei. The mechanistic neighborhood looked like this:

| training target | focal `n_degs` | most relevant focal expression evidence |
|---|---:|---|
| `Arhgap32` | 0 | closest represented synaptic RhoGAP/NMDAR/GABA-A trafficking comparator; best focal adjusted p-value was 0.607, and the self transcript `Arhgap32` was not significant |
| `Arhgap18` | 0 | RhoGAP-family comparator; no focal FDR hits |
| `Cdc42` | 1 | the only focal hit was the `Cdc42` self-transcript |
| `Rac1` | 0 | no focal FDR hits |
| `Pak1` | 1 | the only focal hit was the `Pak1` self-transcript |
| `Pak2` | 0 | no focal FDR hits |
| `Pak3` | 0 | no focal FDR hits |
| `Limk1` | 0 | no focal FDR hits |
| `Kalrn` | 0 | Rac/Rho GEF tied to NMDAR and dendritic spines; no focal FDR hits |
| `Dock3` | 0 | Rac GEF; no focal FDR hits |
| `Tiam1` | 0 | Rac GEF; no focal FDR hits |
| `Arhgef9` | 1 | the only focal hit was the `Arhgef9` self-transcript |
| `Fmr1` | 0 | FMRP/local-translation/mGluR-LTD comparator; no focal FDR hits |
| `Cyfip1` | 0 | FMRP/WAVE regulatory complex comparator; no focal FDR hits |
| `Cyfip2` | 1 | the only focal hit was the `Cyfip2` self-transcript |
| `Syngap1` | 0 | PSD/NMDAR RasGAP comparator; no focal FDR hits; `Syngap1` self p_adj was 0.117 |
| `Dlg4` | 1 | the only focal hit was the PSD-95 self-transcript |
| `Shank2` | 0 | postsynaptic scaffold comparator; no focal FDR hits |
| `Shank3` | 2 | weak focal output: `Shank3` itself and `Uba5` |
| `Dnm1` | 1 | synaptic-vesicle endocytosis comparator; the only focal hit was the `Dnm1` self-transcript |
| `Grm5` | 0 | group-I mGluR comparator; no focal FDR hits |
| `Grm1` | 1 | the only focal hit was the `Grm1` self-transcript |
| `Grin1` | 89 | strong counterexample: direct obligatory NMDAR subunit; induced a real 151-class state headed by self-depletion plus `Scg2`, `Stmn4`, `Kctd16`, `Gpm6a` |
| `Grin2a` | 1 | the only focal hit was the `Grin2a` self-transcript |
| `Grin2b` | 2 | `Grin2b` self-transcript plus `Pianp` in this focal class |

I also computed focal whole-profile neighbors with the Distributed Agents runtime profile-neighbor tool, using the signed Wilcoxon `scores` over all 17,259 measured genes and the 1,674 training targets as the eligible universe. Null or singleton OPHN1-neighborhood anchors had only noise-scale focal similarities:

- `Arhgap32`: 0 significant features; strongest whole-profile Pearson neighbor was `Rora`, `r = 0.0799`.
- `Rac1`: 0 significant features; strongest whole-profile Pearson neighbor was `Rab7`, `r = 0.0549`.
- `Cdc42`: 1 significant feature; strongest whole-profile Pearson neighbor was `Kif1a`, `r = 0.0911`.
- `Fmr1`: 0 significant features, and `Syngap1`: 0 significant features.
- `Grin1`, by contrast, had 89 focal features at the endpoint and a more visible nearest-neighbor structure, with `Vps54` at `r = 0.2320`.

This matters because it separates the OPHN1-like Rho/endocytic nodes from the assay-positive thalamic states. Their focal profiles do not hide a coherent near-threshold OPHN1-like module.

## Same-experiment corpus evidence

The Distributed Agents corpus has no `Ophn1` target report, consistent with the held-out setup. I therefore queried reports and Claim topology for represented analogs.

- `Arhgap32` is the closest represented RhoGAP comparator. The same-experiment corpus calls it a pan-surface negative: 1,543 `Arhgap32` perturbed nuclei across 22 groups and 0 / 371,796 downstream FDR<0.10 gene-by-cell-group tests. The report explicitly contrasted `Arhgap32` with NMDAR subunits, PSD scaffolds, beta-catenin, GABA-A receptor, Rho-GTPase, and dynein/dynactin perturbations; `Ctnnb1`, `Grin1`, `Grin2b`, `Grin2a`, and `Dctn1` could respond in the same taxonomy while `Arhgap32` did not. This is the same-experiment reason not to transfer the strong `Grin1` or `Ctnnb1` counts directly to another synaptic RhoGAP.
- `Cdc42`, `Rac1`, `Pak1`, `Pak2`, `Pak3`, `Limk1`, `Kalrn`, `Dock3`, `Cyfip1`, `Cyfip2`, `Tiam1`, `Arhgap18`, `Arhgap32`, and `Arhgef9` were explicitly queried in the Cdc42/Rac1 corpus reports. They were flat or singleton responders and did not form a shared Rac/Cdc42/PAK/WAVE/LIMK nuclear RNA module. Reactome also places RAC1/CDC42 upstream of PAK1 and RAC1 upstream of the WAVE regulatory complex, so this is the right biochemical neighborhood even though the snRNA signal is absent.
- `Pak1` and `Pak3` are boundaries: each can make one isolated cerebellar GABAergic event elsewhere in the atlas, but group-I PAK paralogs do not phenocopy each other or RAC/CDC42/LIMK transcriptionally.
- `Syngap1` was pan-null in the same-experiment surface and was contrasted with `Grin1` and `Grin2b`: NMDAR receptor subunits can produce RNA signatures, whereas the PSD/SynGAP scaffold branch was transcriptionally quiet.
- `Fmr1`, `Cyfip1`, `Cyfip2`, group-I mGluRs, and local-translation comparators likewise did not form a robust acute neuronal nuclear RNA module; this is relevant because OPHN1 is one of the proteins translated during mGluR-LTD rather than a constitutive transcription-factor-like driver.

I also ran a corpus expansion from `Arhgap32`, `Cdc42`, `Rac1`, and `Kalrn`. It recovered the expected Rho/PAK/WRC/GEF/GAP nodes (`Pak1`, `Pak2`, `Pak3`, `Limk1`, `Tiam1`, `Dock3`, `Cyfip1`, `Cyfip2`, `Arhgap18`, `Arhgef9`) and several NMDAR/PSD/CaMKII counterexamples. I kept the first group as relevant analogs and used `Grin1`, `Grin2a`, `Grin2b`, `Dlg4`, `Dctn1`, and `Camk2a/b` only as boundaries showing which related biology was active or still flat. The induced topology over the curated 19-node synaptic/Rho cohort was connected, with the densest fully connected set being `Cdc42`, `Kalrn`, `Limk1`, `Pak1`, `Pak2`, `Pak3`, `Rac1`, and `Tiam1`; I did not treat density as a weight, only as an audit that the nodes were repeatedly compared in the underlying reports.

## External OPHN1 biology

OPHN1 encodes oligophrenin-1, a BAR-domain RhoGAP for Rho-family GTPases. Its established neuronal roles are largely local and synaptic:

- OPHN1 loss impairs clathrin-mediated endocytosis, AMPAR internalization, and hippocampal LTD through excess RhoA/ROCK activity; ROCK inhibition rescued the endocytic and LTD defects in an `Ophn1` null mouse model (Khelfaoui et al., 2009, PMID: 19401298, DOI: 10.1093/hmg/ddp189).
- Presynaptic OPHN1 binds endophilin A1 and controls synaptic-vesicle endocytosis through both the endophilin interaction and its RhoGAP activity (Nakano-Kobayashi et al., 2009, PMID: 19481455, DOI: 10.1016/j.cub.2009.05.022).
- OPHN1 is recruited by NMDAR activity into dendritic spines, stabilizes synaptic AMPARs, and supports activity-dependent glutamatergic synapse maturation (Nadif Kasri et al., 2009, PMID: 19487570, DOI: 10.1101/gad.1783809).
- During hippocampal mGluR-LTD, translation controlled by eIF2alpha phosphorylation includes `Ophn1`, and OPHN1 mediates AMPAR removal in that plasticity paradigm (Di Prisco et al., 2014, PMID: 24974795, DOI: 10.1038/nn.3754).
- More broadly, RhoA, Rac1, and Cdc42 are actin and microtubule regulators for neuronal outgrowth, dendrites, and spines (Govek, Newey, and Van Aelst, 2005, DOI: 10.1101/gad.1256405); Reactome curates RAC1/CDC42 to PAK1 signaling and RAC1 binding to the WAVE regulatory complex through CYFIP1/CYFIP2.

That prior makes `Ophn1` important for synaptic function, but it points to Rho-GTP loading, ROCK activity, BAR-domain membrane trafficking, AMPAR endocytosis, synaptic-vesicle recycling, and spine morphology. Those are precisely the classes that were usually invisible in the P16 sparse CRISPR nuclear-RNA readout.

## Target-specific prediction

### `Ophn1`

My prediction is `0`.

The decision is driven mainly by within-dataset evidence. `Ophn1` is mechanistically closest to a local RhoGAP/endocytosis/spine node. The best available same-experiment comparator, `Arhgap32`, had 0 DEGs in the focal class and 0 FDR<0.10 downstream calls across its entire 22-group surface despite literature links to NMDARs, RhoA, dendritic spines, and GABA-A receptor trafficking. The directly represented Rho/Cdc42/Rac pathway around OPHN1 was also quiet in the focal class: `Rac1`, `Pak2`, `Pak3`, `Limk1`, `Dock3`, `Kalrn`, `Tiam1`, and `Arhgap18` had no focal DEGs; `Cdc42` and `Pak1` had only their own transcript as a singleton. PSD and mGluR/local-translation boundaries reinforced the same calibration: `Syngap1`, `Fmr1`, `Cyfip1`, `Grm5`, `Shank2`, and `Dnm1` produced 0 or only self-transcript events rather than a broad nuclear state.

The positive counterexamples do not transfer cleanly. `Grin1` gave 89 focal DEGs because it is the obligatory NMDA receptor subunit in a `Grin2c`-marked thalamic class, and `Grin2b`/`Grin2a` were subunit- and context-specific. `Tsc2`, `Ctnnb1`, and `Dctn1` also produced strong or medium 151-class footprints, but their stress/growth, beta-catenin, and dynactin/sterol outputs are not the core OPHN1 RhoGAP/endocytic mechanism. The local profile-neighbor search made the same point numerically: null OPHN1-neighborhood anchors had top focal whole-profile correlations around 0.05-0.09, while an active target such as `Grin1` had a visibly larger structured neighborhood.

The only reason to predict `1` would be the chance of a significant self-transcript. Several focal singletons in this neighborhood are only target mRNA decreases (`Cdc42`, `Pak1`, `Arhgef9`, `Dlg4`, `Dnm1`, `Grm1`, `Grin2a`). However, the platform warns against using target RNA loss as a functional effect proxy, and the closest RhoGAP/PSD examples (`Arhgap32`, `Syngap1`) had moderate self decreases that still did not pass focal FDR 0.05. I therefore kept the endpoint prediction at zero rather than adding a speculative self hit.

## Limits

- OPHN1 itself was held out, so no `Ophn1` expression profile, target knockdown estimate, or guide-specific behavior from this experiment was available.
- Many OPHN1 functions are presynaptic, postsynaptic, or glial. The assay sampled NeuN-positive recovered nuclei, not synaptic vesicles, AMPAR surface levels, RhoA-GTP, ROCK activity, F-actin, spine morphology, or astrocytes.
- Several exact OPHN1 partners were absent as perturbation targets. The represented analogs cover adjacent Rho/PAK/WRC/GEF/GAP and endocytic biology, but not every BAR/SH3 clathrin-endocytosis component.
- DEG counts include self-transcripts. A self hit could make the true count 1 even if the downstream state is flat; this is the main residual uncertainty.
- The prediction is for acute sparse postnatal CRISPR loss in surviving mouse neurons. Germline `Ophn1` phenotypes, human OPHN1 syndromic disease, pharmacological ROCK rescue, and evoked plasticity paradigms inform mechanism but are not direct DEG-count measurements.
