# Pafah1b1 prediction trace

## Question and interpretation

The manifest for this run contains one held-out perturbation, `Pafah1b1`.  I interpreted the requested endpoint as:

- in the focal `151 TH Prkcd Grin2c Glut` population only,
- count the measured genes whose perturbed-versus-control Wilcoxon `pvals_adj` is below 0.05,
- predict that count for `Pafah1b1`, which is absent from both the focal training-count CSV and the differential-expression parquet.

The count is an assay-specific breadth measure, not a direct measure of editing, survival, neuronal importance, or the size of the largest fold changes.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - Used for the observed focal counts of all non-held-out perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  - Used for the exact focal signatures of mechanistic comparators and for same-direction/opposite-direction FDR overlap tests.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`
  - Used as the curated interpretation layer over the non-held-out Perturb-seq signatures, especially the `Dctn1` findings.
- Distributed Agents runtime profile comparison
  - Used to compare the signed focal profiles of `Dctn1`, `Rab7`, `Tsc2`, `Vps35`, `Vps54`, `Mib1`, `Marchf6`, `Htt`, `Srebf2`, `Tuba1a`, `Kif5a`, `Kif5c`, `Map1b`, `Map6`, and `Rac1`.
- External functional priors
  - NCBI Gene ID 18472 confirmed the mouse `Pafah1b1` identity.
  - UniProtKB/Swiss-Prot `LIS1_MOUSE`, accession `P63005`, entry version 197, identified PAFAH1B1/LIS1 as the reviewed mouse LIS1 protein.
  - STRING v12 mouse interaction data placed `Ndel1`, `Pafah1b2`, `Pafah1b3`, `Dync1h1`, `Dctn1`, `Nde1`, `Nudc`, dynein intermediate chains, and `Dynll1` among the strongest `Pafah1b1` partners.
  - Reiner et al. 1993, PMID: 8355785, DOI: 10.1038/364717a0, established `LIS1`/`PAFAH1B1` as a Miller-Dieker lissencephaly gene.
  - Liang et al. 2004, PMID: 14970193, showed that Nudel/NDEL-family regulation of membrane traffic depends on association with LIS1 and cytoplasmic dynein.
  - McKenney et al. 2010, PMID: 20403325, DOI: 10.1016/j.cell.2010.02.035, showed that LIS1 and NudE put dynein into a persistent force-producing state.

## Computational checks

The training-count table has 1,674 focal perturbations.  Its count distribution was highly zero-inflated:

- median: 0 DEGs
- 75th percentile: 1 DEG
- 95th percentile: 18 DEGs
- 99th percentile: 436 DEGs
- 469/1,674 perturbations had any focal FDR<0.05 DEG
- `Dctn1`, with 75 DEGs, was already in the 97th percentile of the training counts

`Pafah1b1` had zero rows in every cell group of the DE parquet, confirming that it was completely held out rather than merely missing in the focal count CSV.

For mechanistic comparators I filtered the parquet to `group_name = '151 TH Prkcd Grin2c Glut'`, selected `names`, `gene_target`, `logfoldchanges`, and `pvals_adj`, and counted `pvals_adj < 0.05`.  For expression-pattern evidence I joined the significant rows of two targets by `names` and compared `sign(logfoldchanges)` to count same-direction and opposite-direction overlaps.

## Target-specific reasoning: `Pafah1b1`

### Direct biology

`Pafah1b1` encodes LIS1, a dynein-1 regulator.  Its highest STRING mouse partners included the exact LIS1/NDE/NDEL/dynein-1 module: `Ndel1`, `Nde1`, `Dync1h1`, `Dctn1`, `Dync1i1`, `Dync1i2`, `Nudc`, and `Dynll1`, plus the platelet-activating-factor acetylhydrolase subunits `Pafah1b2` and `Pafah1b3`.  McKenney et al. mechanistically place LIS1/NudE on the dynein motor itself, and Liang et al. link the LIS1-Nudel-dynein interaction to dynein-dependent membrane traffic.  That made the dynein-1/dynactin transport perturbations the relevant local analogs, rather than the dynein-2 intraflagellar-transport genes.

Most of the exact LIS1 neighborhood was not directly represented in the focal training endpoint:

| training target | focal `n_degs` | interpretation |
|---|---:|---|
| `Dctn1` | 75 | close dynein/dynactin comparator and the main local anchor |
| `Ywhae` | 0 | 14-3-3/Miller-Dieker neighbor; not a dynein motor subunit, useful as a weak negative counterexample |
| `Pafah1b2`, `Pafah1b3`, `Ndel1`, `Nde1`, `Dync1h1`, `Dync1i1`, `Dync1i2`, `Dctn2`, `Nudc`, `Dynll1` | not in training | unavailable exact-complex comparators |

### Within-dataset analogs

`Dctn1` was the strongest biologically appropriate analog.  In the focal group it had 75 DEGs among 17,259 tested genes with 182 matched perturbed nuclei.  The most significant genes were a coherent SREBF2-like sterol/cholesterol module upregulated after `Dctn1` targeting: `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`, `Sqle`, `Dhcr24`, `Ldlr`, `Fdps`, and related enzymes.  The Distributed Agents corpus summarized this as a recurrent neuronal sterol/cholesterol biosynthesis and uptake module after `Dctn1`, and emphasized that it was not a generic consequence of every cytoskeletal or trafficking perturbation.

That `Dctn1` module was sign-coherent with several non-dynein perturbations in the same focal group:

| comparator | focal `n_degs` | focal relation to `Dctn1` |
|---|---:|---|
| `Rab7` | 501 | shared 43 FDR genes with `Dctn1`, 39 in the same direction, including `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Atp2a2`, `Lamp2`, `Grin2b` |
| `Tsc2` | 86 | shared 13 with `Dctn1`, all same direction |
| `Mib1` | 27 | shared 21 with `Dctn1`, all same direction, dominated by the sterol genes |
| `Marchf6` | 14 | shared 12 with `Dctn1`, all same direction, dominated by the sterol genes |
| `Vps35` | 17 | shared 6 with `Dctn1`, all same direction, mostly axon/endosomal genes rather than the sterol core |
| `Vps54` | 31 | shared 6 with `Dctn1`, 3 same and 3 opposite |
| `Htt` | 3 | only 2 shared `Dctn1` genes |
| `Srebf2` | 7 | flipped 7 `Dctn1` sterol genes in the opposite direction |

These analogs support a nonzero `Pafah1b1` call because dynein/dynactin and endolysosomal transport perturbations can cross the FDR threshold in this exact thalamic group.  They also argue against predicting a count as high as `Rab7`: the broad 501-gene `Rab7` response reflects direct late-endosome/lysosome cholesterol handling and many additional lysosomal features, not simply loss of retrograde dynein force.

### Counterexamples

The represented cytoskeletal and migration-associated genes were mostly much weaker than `Dctn1`:

| comparator | focal `n_degs` | relevance |
|---|---:|---|
| `Tuba1a` | 7 | tubulin perturbation produced reciprocal tubulin compensation, not the `Dctn1` sterol program |
| `Kif1a`, `Kif5a`, `Kif5c` | 1 each | kinesin motors were singletons in this focal group |
| `Kifbp` | 2 | weak and opposite to the `Dctn1`/`Mib1`/`Marchf6` sterol module on `Srebf2` |
| `Map1b`, `Mapt`, `Tubb4b`, `Tubb5`, `Mapre2` | 1 each | microtubule-associated or tubulin genes were only self/near-self hits |
| `Tuba4a` | 2 | sparse tubulin-isotype signal |
| `Map6`, `Rac1`, `Reln`, `Vldlr`, `Lrp8` | 0 | migration/cytoskeletal genes without focal transcriptional breadth |
| `Dync2h1`, `Dync2i1` | 0 | dynein-2/ciliary motor genes, not close LIS1 dynein-1 analogs |

These counterexamples are important because LIS1 is famous for embryonic neuronal migration and nuclear movement, but this experiment perturbs already postmitotic P16 neurons and reads out nuclear RNA 3-4 weeks later.  A mature-neuron transport defect is plausible; a full embryonic migration program is not.

### Zero/nonzero decision and count

I predicted a positive response.  The nonzero part is driven primarily by external LIS1 dynein-1 biology plus the focal `Dctn1` signature.  A `Pafah1b1` knockout should be much more dynein-relevant than flat comparators such as `Reln`, `Vldlr`, `Lrp8`, `Rac1`, `Map6`, or dynein-2 components, and dynein/dynactin perturbation is clearly capable of producing an FDR-supported RNA state in the focal thalamic group.

I did not predict that `Pafah1b1` would equal `Dctn1`.  The closest missing partners are absent from training, LIS1 is a regulator of dynein force production rather than the dynactin p150 subunit itself, and the assay occurs after the peak embryonic migration window in a survivor-conditioned NeuN+ population.  The count estimate was therefore placed between the weak focal dynein-associated responses (`Htt` 3, `Vps35` 17, `Mib1` 27, `Marchf6` 14) and direct `Dctn1` loss (75), with the direct dynein-1 link pulling it well above the singleton cytoskeletal perturbations.

Final point prediction: `Pafah1b1 = 45` DEGs.

## Limits

- The best exact mechanistic comparators, `Dync1h1`, `Dync1i1`, `Dync1i2`, `Dctn2`, `Nde1`, `Ndel1`, `Pafah1b2`, `Pafah1b3`, `Nudc`, and `Dynll1`, were not represented in the focal training endpoint.  The prediction leans heavily on `Dctn1`.
- `Dctn1` may overestimate `Pafah1b1` if the focal sterol response requires structural loss of dynactin/cargo coupling rather than impaired LIS1-mediated dynein activation.
- `Dctn1` may also underestimate `Pafah1b1` if PAFAH1B1 haploinsufficiency is unusually dosage-sensitive in these thalamic neurons.
- Literature on LIS1 is dominated by embryonic migration, mitosis, and nuclear movement.  Those mechanisms justify dynein relevance but do not directly specify a P16 postmitotic single-nucleus sterol signature.
- The endpoint is FDR-thresholded; counts around 20-80 can move substantially with matched nucleus counts, expression depth, and small shifts in p-values near 0.05.
