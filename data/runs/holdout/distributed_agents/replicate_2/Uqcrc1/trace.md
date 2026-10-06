# Uqcrc1 DEG-count prediction

## Question and resolved ambiguities

The requested held-out target set contains one perturbation, `Uqcrc1`.  I interpreted the endpoint as the exact training-count endpoint in `151 TH Prkcd Grin2c Glut`: the number of measured genes, including the perturbed transcript if it passes, with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal cell group.  The held-out `Uqcrc1` rows were absent from both supplied assay tables, so I estimated its count from measured perturbations in the same focal cell type plus the known placement of UQCRC1 in mitochondrial respiratory complex III.

I did not treat target-transcript knockdown as an editing-efficiency filter.  I used significant self rows only because the requested endpoint counts all measured genes.  Thus a predicted value of `1` here means "a singleton hit is most likely"; it does not mean I expect a resolved downstream mitochondrial stress program.

## Sources used

- `[local file: training_de_all_cell_groups.parquet]`, queried in `151 TH Prkcd Grin2c Glut` for focal signatures, FDR counts, and the identity of the few significant genes in candidate analogs.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, used as the authoritative observed `n_degs` labels for non-held-out perturbations.
- `[local file: 257_Uqcrc1.csv]`, used for requested-target order and exact symbol spelling.
- Distributed Agents same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`, queried through `target_context`, `search_claims`, and `candidate_set_topology` for the experiment's curated complex-III comparisons.
- Distributed Agents deterministic annotation/analog store:
  - CORUM v5.0 native mouse complex `495`, "Cytochrome bc1-complex, mitochondrial".
  - Reactome mouse `R-MMU-9865881`, "Complex III assembly".
  - GO cellular component `GO:0045275`, "respiratory chain complex III".
  - STRING physical v12.0 high-confidence UQCRC1 interactions with other complex-III subunits.
- External mechanism literature:
  - Xia et al. 1997, DOI `10.1126/science.277.5322.60`, PMID `9204897`: crystal structure of the bovine mitochondrial cytochrome bc1 complex, including core 1 and core 2 proteins.
  - Ghezzi et al. 2011, DOI `10.1038/ng.761`, PMID `21278747`: TTC19 mutations cause complex III deficiency and neurological impairment.
  - Fernandez-Vizarra and Zeviani 2018, DOI `10.1080/15384101.2017.1417707`, PMID `29243944`: UQCRFS1 processing/assembly, with TTC19 linked to post-assembly complex III quality control and the UQCRFS1 precursor fragment retained between UQCRC1 and UQCRC2.
  - Burska et al. 2021, DOI `10.1016/j.bbadis.2021.166147`, PMID `33865955`: a human UQCRC2 core-protein mutation caused a complex III assembly defect with reduced UQCRC1/UQCRC2/UQCRFS1-containing assemblies.

## Computational steps

1. I read the held-out manifest and confirmed that `Uqcrc1` was the only requested target.
2. I nominated analogs against the actual 1,674-target training universe, rather than by symbol prefix.  The strongest eligible exact native CORUM complex mates were `Uqcrb`, `Uqcrc2`, `Uqcrh`, `Uqcrq`, `Cyc1`, and `Uqcrfs1`; the leading complex-III assembly factors in the training set were `Ttc19`, `Lyrm4`, and `Nfs1`.
3. I queried the focal training counts for those analogs:

| group | focal training targets and `n_degs` |
| --- | --- |
| Native complex III, CORUM 495 | `Cyc1` 1; `Uqcrb` 0; `Uqcrc2` 1; `Uqcrfs1` 0; `Uqcrh` 0; `Uqcrq` 1 |
| Reactome complex III assembly extension | `Lyrm4` 0; `Nfs1` 0; `Ttc19` 1, in addition to the structural subunits above |
| Broader OXPHOS counterexamples | Most complex-I/IV and respiratory-chain candidates had 0 or 1 focal DEG; `Opa1`, a mitochondrial-dynamics target rather than a complex-III target, was the positive mitochondrial-stress counterexample with 37 focal DEGs |

The exact native complex-III analogs therefore had a mean of `0.5`, a median of `0.5`, and no member above `1`; the nine-member complex-III/assembly set had a mean of `0.444`, median `0`, and no member above `1`.

4. I cross-checked the same counts directly from the parquet in `151 TH Prkcd Grin2c Glut`.  The four one-hit events in the complex-III/assembly set were:

| perturbation | focal FDR<0.05 gene | FDR |
| --- | --- | --- |
| `Cyc1` | `Cyc1`, self | `2.94e-15` |
| `Ttc19` | `Ttc19`, self | `1.42e-22` |
| `Uqcrc2` | `Uqcrc2`, self | `2.997e-03` |
| `Uqcrq` | `Gpr180` | `4.29e-02` |

The remaining direct analogs were below threshold in the focal group: `Uqcrfs1` had its own transcript at FDR `0.199`, `Nfs1` had its own transcript at FDR `0.233`, and `Uqcrb`, `Uqcrh`, and `Lyrm4` had no gene below FDR 0.25.

5. I compared the focal signed profiles of `Uqcrb`, `Uqcrc2`, `Uqcrh`, `Uqcrq`, `Cyc1`, `Uqcrfs1`, `Ttc19`, `Lyrm4`, `Nfs1`, `Opa1`, and `Lrpprc` with the run-local profile-review tool.  This did not reveal a shared significant complex-III program: pairwise significant-feature intersections within the complex-III cohort were zero, while top-tail overlaps were small and dominated by subthreshold ranks.  I therefore used the profile evidence as support for the corpus result that the measured complex-III perturbations are singleton or null profiles, not as a continuous similarity score.

## Target-specific reasoning

### `Uqcrc1`

`Uqcrc1` encodes the core 1 subunit of respiratory complex III.  CORUM v5.0 places mouse Uqcrc1 with `Cyc1`, `Uqcrb`, `Uqcrc2`, `Uqcrfs1`, `Uqcrh`, and `Uqcrq` in the native mouse cytochrome bc1 complex; the analog nominator also retrieved high-confidence STRING v12.0 physical links from UQCRC1 to the other measured structural subunits.  UQCRC1 and UQCRC2 are the two large core proteins in the bc1 dimer structure, and complex-III disease/assembly literature connects the UQCRC1-UQCRC2 core with Rieske protein maturation and with UQCRC2-dependent stability of UQCRC1-containing assemblies.  For that reason `Uqcrc2` is the closest measured structural analog, with `Cyc1`, `Uqcrfs1`, `Uqcrb`, `Uqcrh`, and `Uqcrq` as same-complex comparators and `Ttc19`, `Lyrm4`, and `Nfs1` as related assembly/Fe-S comparators.

The focal experimental evidence is narrow.  `Uqcrc2`, the nearest measured core-protein analog, had exactly one focal DEG, `Uqcrc2` itself.  `Cyc1` and `Ttc19` also registered only self-transcripts in the focal class.  `Uqcrq` had a single non-self `Gpr180` hit that the corpus explicitly treats as private: represented same-complex perturbations did not reproduce it.  `Uqcrb`, `Uqcrfs1`, `Uqcrh`, `Lyrm4`, and `Nfs1` were focal zeros.  Broader nuclear OXPHOS comparators such as `Ndufs4`, `Ndufa9`, `Ndufv1`, `Cox4i1`, `Cox6a1`, `Cox7b`, `Cox8a`, `Coa8`, `Cox11`, and `Lrpprc` were likewise zero or singleton in this focal class, whereas `Opa1` reached 37 and served as the counterexample showing that a mitochondrial perturbation can trigger a medium ATF4/ISR-like RNA state in this assay.

The Distributed Agents same-experiment corpus independently supported this interpretation.  Its high-confidence claim `claim:34681374c398d1920b0b` states that represented respiratory complex III components are largely transcriptionally buffered in neuronal nuclei and do not induce a shared complex-III depletion RNA signature.  Target contexts for `Uqcrc2`, `Uqcrh`, `Uqcrq`, `Uqcrfs1`, `Cyc1`, and `Ttc19` all either anchor or support that claim; a second, moderate-confidence claim `claim:4818d59945fdf5715f28` notes that the few FDR-supported hits among these targets were private rather than same-complex phenocopies.  The exact-reference topology over `Cyc1`, `Ttc19`, `Uqcrb`, `Uqcrc2`, `Uqcrfs1`, `Uqcrh`, and `Uqcrq` formed a fully connected report-derived set, but the connections were mostly explicit contrasts of absent or non-overlapping transcriptomic effects, so I did not pool them as a positive signature module.

Those data argue strongly against a medium or broad Uqcrc1 response.  The remaining decision is `0` versus `1`.  I put `Uqcrc1` on the positive side because the nearest core analog `Uqcrc2` produced a significant self-transcript in this focal class, `Cyc1` also had a self singleton, and UQCRC1 is a core, highly integrated bc1 component rather than a distal, redundant regulator.  The expected count is still just a singleton: I do not expect a canonical mitochondrial ISR, UPRmt/chaperone, redox, mitophagy, or nuclear OXPHOS compensation program to cross FDR<0.05 in `151 TH Prkcd Grin2c Glut`.

Predicted `n_degs`: `1`.

## Limits and uncertainty

The prediction extrapolates from other complex-III genes; no `Uqcrc1` differential-expression rows or hidden endpoint counts were used.  Most analogs have 0 or 1 focal DEG, so the distinction between `0` and `1` is driven by a single self-transcript expectation, not by a robust downstream module.  The single significant analog counts may depend on guide efficiency, Uqcrc1 baseline expression, nonsense-mediated decay, and recovered perturbed-cell number, none of which are observed for the held-out target.

The postnatal sparse CRISPR assay measured survivor nuclear RNA, not DNA indels, complex-III protein, enzyme activity, ROS, ATP, membrane potential, mitochondrial translation, or pre-assay cell loss.  Human complex-III disease and strong biochemical loss show that UQCRC1/UQCRC2 biology can be essential, but those facts do not imply a broad snRNA-seq footprint in recovered juvenile thalamic glutamatergic nuclei.  Conversely, a flat RNA profile in the measured analogs does not prove that the complexes were biochemically intact; it only calibrates the endpoint requested here.
