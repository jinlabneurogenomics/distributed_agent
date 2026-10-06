# DEG-count prediction for `Mboat7`

## Question and resolved ambiguities

The held-out target list for this run contains one perturbation, `Mboat7`. I interpreted the requested endpoint as the exact `n_degs` that would have been reported for an `Mboat7` CRISPR loss-of-function contrast in `151 TH Prkcd Grin2c Glut` cells: the number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the same Scanpy differential-expression table used for all non-held-out perturbations.

The count includes the perturbed gene itself if its measured transcript passes FDR 0.05. However, self-transcript loss is not a reliable editing-efficiency measure in this AAV CRISPR snRNA-seq design, so I used it only as a possible contributor to the integer endpoint, not as evidence that a perturbation is biologically strong or weak.

## Sources used

- Training endpoint CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 133_Mboat7.csv]`.
- Internal same-experiment semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- Internal runtime profile-neighbor analysis over the focal DE profiles.
- External literature from PubMed, especially:
  - Gijon et al. 2008, JBC, DOI `10.1074/jbc.M806194200`, PMID `18772128`.
  - Lee et al. 2012, Molecular Biology of the Cell, DOI `10.1091/mbc.E12-09-0673`, PMID `23097495`.
  - Anderson et al. 2013, PLoS ONE, DOI `10.1371/journal.pone.0058425`, PMID `23472195`.
  - Johansen et al. 2016, AJHG, DOI `10.1016/j.ajhg.2016.07.019`, PMID `27616480`.
  - Caddeo et al. 2021, BBA Molecular and Cell Biology of Lipids, DOI `10.1016/j.bbalip.2021.158891`, PMID `33513444`.
  - Phadnis et al. 2023, Cell Reports, DOI `10.1016/j.celrep.2023.113023`, PMID `37691145`.

## Computational steps

1. Loaded the manifest and confirmed that `Mboat7` was the only held-out target.
2. Loaded the focal training count CSV. It contains 1,674 non-held-out perturbations. The endpoint is very sparse in this cell group: 1,205 perturbations have `n_degs = 0`, 363 have 1-9 DEGs, 63 have 10-99, and 43 have at least 100.
3. Inspected parquet row-group statistics and read only the row groups overlapping `151 TH Prkcd Grin2c Glut` into a compact temporary focal table. This yielded 28,891,566 rows: 1,674 perturbations by 17,259 measured genes.
4. Queried focal FDR-significant rows for lipid, phosphoinositide, and membrane-trafficking analogs of `Mboat7`.
5. Ran Distributed Agents `profile_neighbors` on `Acsl4`, `Abhd12`, `Dgke`, `Pld3`, `Synj1`, `Vps35`, and `Vps54` in the focal cell group against the full 1,674-target training universe, using signed log-fold-change profiles and `pvals_adj < 0.05` as the significance layer.
6. Queried the Distributed Agents same-experiment corpus for `Mboat7` and the relevant analogs. This release had no `Mboat7` Finding, so target-specific reasoning below combines direct parquet evidence from related assayed perturbations with external mechanism evidence.

## Mboat7 reasoning

`Mboat7` encodes LPIAT1, a membrane-bound acyltransferase in the Lands phospholipid-remodeling cycle. It preferentially transfers arachidonoyl-CoA and other polyunsaturated acyl chains to lysophosphatidylinositol, thereby maintaining the arachidonoyl-phosphatidylinositol pool (Gijon et al. 2008; Caddeo et al. 2021). Complete loss of the same enzyme has clear nervous-system consequences outside this assay: `Lpiat1` knockout mice have reduced arachidonic-acid-containing PI and phosphoinositides, cortical/hippocampal atrophy, delayed cortical migration, neurite defects, and early postnatal lethality (Lee et al. 2012), and biallelic human `MBOAT7` variants cause intellectual disability often accompanied by epilepsy and autistic features (Johansen et al. 2016). Anderson et al. 2013 likewise found lower total PtdIns and PtdInsP2 in `Lpiat1-/-` brain and liver.

Those facts make `Mboat7` a credible neuronal lipid target, but they do not imply a broad steady-state transcriptomic response here. The experiment perturbs sparse postmitotic neurons from P16 to P37-P44 with mosaic CRISPR, not constitutive embryonic loss, and its NeuN+ nuclei are not suited to recovering the microglial or liver programs that dominate several `Mboat7` disease mechanisms. The best in-dataset calibration therefore comes from the assayed phosphatidylinositol/arachidonate neighbors:

- `Acsl4`, `n_degs = 1`: the sole focal DEG was `Acsl4` itself (`logfoldchanges = -0.995`, `pvals_adj = 3.83e-16`). ACSL4 is mechanistically adjacent because it activates arachidonic acid to arachidonoyl-CoA and can act with MBOAT7 to push arachidonate into PI lipids; Phadnis et al. 2023 showed ACSL4- and MBOAT7-dependent polyunsaturated PI remodeling in a ferroptosis context. In the Distributed Agents corpus, `Acsl4` also had a restricted signature rather than a neuronal ferroptosis-like module: `Gpx4` and `Nfe2l2` were downstream-flat and the strongest full-coverage `Acsl4` neighbors had zero robust downstream genes.
- `Pi4kb`, `n_degs = 1`: this PI 4-kinase is not in the same remodeling reaction as MBOAT7, but it sits immediately downstream of PI availability. Its only focal FDR 0.05 hit was `Tmem50b`. The Distributed Agents corpus reported only three downstream FDR 0.10 events across all cell groups and no robust whole-transcriptome phenocopy or anti-phenocopy.
- `Dgke`, `n_degs = 1`: the only focal hit was the edited `Dgke` transcript itself (`pvals_adj = 5.97e-08`). DGKE recycles arachidonoyl-diacylglycerol in the PI cycle, making it a PI/DAG counterpoint. The same-experiment corpus summarized postnatal mosaic `Dgke` loss as having no robust steady-state neuronal transcriptional output and no detectable convergence module.
- `Synj1`, `n_degs = 1`; `Ocrl`, `n_degs = 0`; `Inpp5k`, `n_degs = 0`; `Plcb1`, `n_degs = 0`; `Pik3cb`, `Pik3r1`, and `Pik3r2`, all `n_degs = 0`; `Ppip5k2`, `n_degs = 0`: these phosphoinositide signaling enzymes are less directly connected to the arachidonoyl-PI Lands cycle, but they show that perturbing PI signaling did not usually create a large compensatory transcriptional program in these thalamic glutamatergic cells. The Distributed Agents `Synj1` Finding was especially strong: all 21 recovered neuronal groups were downstream-zero at FDR 0.10 despite a detectable target-transcript trend, and `Ocrl`/`Inpp5k` did not reveal a compensatory phosphoinositide module.
- `Abhd12`, `n_degs = 1`; `Pld3`, `n_degs = 1`; `Abhd2`, `n_degs = 0`; `Tecr`, `n_degs = 1`: other assayed lipid enzymes also sat at the zero or one-DEG floor.
- `Vps35`, `n_degs = 17`, and `Vps54`, `n_degs = 31`: these trafficking hits show that an endomembrane target can give a small multi-gene signature in the same cell group, but they are retromer/GARP genes rather than enzymes specific to arachidonoyl-PI remodeling. Their focal DEGs contained neuronal/stress markers such as `Atp2a2`, `Egr1`, and cytoskeletal genes, not a pathway that anchored the MBOAT7 call.

The profile-neighbor run was concordant with the count view. `Acsl4`, `Dgke`, `Abhd12`, `Pld3`, and `Synj1` each had exactly one significant focal feature. Their closest whole-profile neighbors were mostly unrelated weak signatures; `Pi4kb` did appear among the strongest whole-profile neighbors for both `Acsl4` and `Dgke`, but the top-500 signed-tail overlaps among anchors were small rather than a coherent high-DEG lipid cluster.

Because the focal endpoint counts self-target transcript hits and `Mboat7` itself is a measured gene in this cell group, a single significant event is plausible. I therefore predicted a one-DEG response. The call is nonzero because MBOAT7 is a real, expressed PI-remodeling enzyme with close `Acsl4`/`Pi4kb`/`Dgke` support for a detectable floor-level effect. The count is kept at 1 because every direct biochemical or phosphoinositide analog in the training data was 0 or 1 in this exact focal endpoint, and the stronger Vps35/Vps54 trafficking profiles are mechanistically too indirect to justify moving `Mboat7` into the 10-99 DEG class.

## Limits

The evidence is weakest at the point that matters most: no `Mboat7` perturbation profile or Distributed Agents `Mboat7` Finding was present in the held-in same-experiment corpus. `Acsl4`, `Pi4kb`, `Dgke`, and `Synj1` are pathway neighbors, not paralogs or complex members, and none is a perfect substitute for loss of lysophosphatidylinositol acyltransferase activity. Much of the external `Mboat7` biology comes from germline null mice, liver/adipocyte conditional knockouts, cancer cells, macrophages, or human biallelic disease, whereas the requested readout is acute partial loss in recovered juvenile postmitotic neurons. Finally, predicting `1` rather than `0` depends on the probability of a self-target or tiny compensation signal crossing this assay's FDR threshold; the mechanistic evidence supports a weak effect but cannot guarantee a single adjusted p-value call.
