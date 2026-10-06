# Prediction trace for Srsf1 in 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The requested manifest contains one held-out perturbation, `Srsf1`. I interpreted the task as predicting the integer number of measured genes that would pass BH-adjusted Wilcoxon `pvals_adj < 0.05` after an acute P16 AAV-CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` cells, using only non-held-out perturbation profiles and training DEG counts as quantitative calibration. The endpoint is a whole-gene snRNA-seq response breadth, so a prediction near zero means "few total-mRNA changes pass FDR" rather than "no splice isoforms changed" or "no protein consequence".

`Srsf1` was absent from the training DEG-count CSV and no `Srsf*` gene appeared as a training target, so I could not use a within-dataset paralog count directly. I therefore treated `Tnpo3`, which imports phosphorylated SR proteins including ASF/SF2/SRSF1, and core spliceosome/RNA-processing factors as positive analogs, and weakly responding spliceosome/RBP targets as counterexamples.

## Sources used

- Input focal training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 223_Srsf1.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents runtime profile comparison over the focal cell group, written in this run as `srsf1_splicing_compare.json` and inspected as `srsf1_splicing_core_inspect.json`.
- PubMed literature for SR proteins, SRSF1, and TNPO3/Transportin-SR2 biology:
  - Sun et al. 1993, DOI `10.1101/gad.7.12b.2598`.
  - Caceres and Krainer 1993, DOI `10.1002/j.1460-2075.1993.tb06160.x`.
  - Zuo and Manley 1994, DOI `10.1073/pnas.91.8.3363`.
  - Lai et al. 2001, DOI `10.1073/pnas.181354098`.
  - Yun et al. 2003, DOI `10.1074/jbc.M211714200`.
  - Xu et al. 2005, DOI `10.1016/j.cell.2004.11.036`.
  - Sun et al. 2010, DOI `10.1038/nsmb.1750`.
  - Ghosh and Adams 2011, DOI `10.1111/j.1742-4658.2010.07992.x`.
  - Maertens et al. 2014, DOI `10.1073/pnas.1320755111`.
  - Howard and Sanford 2014, DOI `10.1002/wrna.1260`.
  - Jeong 2017, DOI `10.14348/molcells.2017.2319`.
  - Aznarez et al. 2018, DOI `10.1016/j.celrep.2018.04.039`.

## Computations over the supplied data

I loaded the focal training-count CSV and first checked the count distribution to put any nonzero prediction on the assay's native scale. Among 1,674 non-held-out targets, the median was 0 DEGs, the 75th percentile was 1, the 95th percentile was 18, and only a small upper tail produced hundreds of DEGs. Thus any prediction in the hundreds is a strong assertion that the held-out target should behave like the experiment's broad RNA-processing responders, not merely a generic housekeeping gene.

I then filtered the training-count file for spliceosome/RBP and RNA-processing names. The closest focal counts were:

| training target | focal `n_degs` | use in reasoning |
|---|---:|---|
| `Rnpc3` | 868 | strong minor-spliceosome positive analog |
| `U2af2` | 828 | strong 3-prime splice-site recognition positive analog |
| `Cdc40` | 624 | strong spliceosome positive analog |
| `Tnpo3` | 618 | SR-protein nuclear-import positive analog |
| `Prpf6` | 454 | U4/U6-U5 tri-snRNP positive analog |
| `Snrnp70` | 213 | weaker but still nonzero U1 snRNP/RNA-processing analog |
| `Tardbp` | 210 | RNA-binding counterpoint with similar moderate breadth |
| `Hnrnpc` | 122 | hnRNP splice-adjacent but narrower response |
| `Hnrnpa2b1` | 11 | abundant hnRNP counterexample |
| `Ddx3x` | 8 | RNA helicase counterexample |
| `Rp9` | 4 | spliceosome-associated but buffered counterexample |
| `Hnrnph2` | 4 | hnRNP counterexample |
| `Ctnnbl1` | 1 | PRP19-adjacent buffered counterexample |
| `Snrpn` | 1 | Sm-related buffered counterexample |
| `Snrpb` | 0 | core Sm counterexample |
| `Ddx39b` | 0 | TREX/RNA-export factor buffered in this exact focal group |

The Distributed Agents same-experiment corpus had no `Srsf1` node, as expected, but did contain a high-confidence claim that "a subset of core or adjacent RNA-splicing/RNA-processing perturbations produces a shared same-direction neuronal differential-expression module" in postnatal neuronal snRNA-seq, especially in `151 TH Prkcd Grin2c Glut` and related midbrain/thalamic groups. The `Prpf6`, `Rnpc3`, and `Cdc40` finding cards specifically placed `Cdc40`, `U2af2`, `Snrnp70`, `Rnpc3`, and `Prpf6` in a same-direction RNA-processing convergence class. The same claim also records the empirical boundary: `Ctnnbl1`, `Snrpb`, `Snrpn`, and `Rp9` are in or near spliceosome biology but were flat or nearly flat.

To check the raw focal signature geometry, I ran a Distributed Agents runtime `profile_compare` on the exact `151 TH Prkcd Grin2c Glut` parquet rows for the RNA-processing candidate set. The activity table reproduced the endpoint counts above. Inspecting selected pairs showed that the core broad perturbations share same-direction FDR genes with `Snrnp70`, `Hnrnpu`, `Tardbp`, and `Hnrnpc`, whereas the one-to-eleven-DEG comparators have little or no FDR-overlap despite sometimes looking similar in the unthresholded negative tail. That matters for `Srsf1`: I should borrow evidence from the FDR-scale spliceosome/SR-import module, not from every weak RBP whose all-gene ranks drift in the same direction.

Finally, because `Srsf1` is a measured transcript in the parquet even though it is not a perturbation target, I asked which training perturbations changed SR-factor mRNAs in the focal group. `Tnpo3` significantly decreased `Srsf1` itself (`log2FC = -0.584`, `p_adj = 2.56e-5`) and also decreased `Srsf2`, `Srsf3`, `Srsf5`, `Srsf6`, `Srsf7`, `Srrm2`, `Akap8l`, and `Clk1`. `U2af2` and `Cdc40` overlapped on several SR-related decreases, especially `Srsf5`/`Srsf6`/`Srsf7` and `Rsrp1`. That puts SRSF1 in the measured SR-splicing arm downstream of broad RNA-processing stress, rather than making it a random family member with no representation in the observed signatures.

## Target-specific biological reasoning

SRSF1/SF2/ASF is the founding SR protein. It has two RRMs and an RS domain, binds exonic splicing enhancers and splice-site-proximal RNA to promote constitutive and alternative spliceosome assembly, and can antagonize hnRNP A1-dependent splice-site choices (Sun et al. 1993; Caceres and Krainer 1993; Zuo and Manley 1994). It is also a shuttling RNA-binding protein with roles after splicing, including export, translation, autoregulation of its own mRNA, and stimulation of nonsense-mediated decay for selected PTC-containing RNAs (Sun et al. 2010; Howard and Sanford 2014; Jeong 2017; Aznarez et al. 2018). Phosphorylation of its RS domain by SRPK-family kinases controls nuclear import, and Transportin-SR2/TNPO3 can directly import phosphorylated SR proteins; the crystal structure of human TNPO3 bound to ASF/SF2 shows recognition of both RRM and phosphorylated RS regions (Lai et al. 2001; Yun et al. 2003; Ghosh and Adams 2011; Maertens et al. 2014).

The strongest within-dataset analog for a direct `Srsf1` lesion is therefore `Tnpo3`: it produced 618 DEGs in the focal group and its corpus findings say its most canonical module was down-regulation of SR-splicing and RNA-processing transcripts led by `Srrm2`, `Srsf5`, `Srsf1`, `Srsf7`, `Srsf2`, `Akap8l`, `Clk1`, and `Cstf2`. `Tnpo3` should be broader than `Srsf1`, because it perturbs import of multiple phosphorylated RS-domain cargoes and couples SR-protein import to a nuclear RNA-logistics state. Still, the fact that the same experiment saw 618 DEGs after hitting the importer is strong evidence that this cell type can convert an SR-factor localization defect into a detectable whole-gene response.

`Prpf6`, `Cdc40`, `U2af2`, and `Rnpc3` are also positive but more severe analogs. Their observed counts, 454 to 868, show that loss of core spliceosome functions repeatedly lands in a broad 151-cell response with hundreds of DEGs. They are not exact biochemical matches: `Prpf6` and `Cdc40` act in major-spliceosome catalytic remodeling, `U2af2` recognizes the polypyrimidine tract at 3-prime splice sites, and `Rnpc3` is a minor-spliceosome component. A single SR protein should not be as globally disabling as `U2af2` or `Rnpc3`, and SRSF1 has paralogs whose RNA-binding motifs and SR domains can buffer subsets of exons. Those four targets nevertheless set the upper calibration for "RNA splicing is truly perturbed in this endpoint", and their recurrent down-regulation of `Srrm2`, `Rsrp1`, `Srsf5`, `Srsf7`, and synaptic maintenance genes argues that SRSF1 loss would not be invisible at total-gene level.

The main lower-bound counterexamples were `Snrpb` with 0 DEGs, `Snrpn` with 1, `Ctnnbl1` with 1, and `Rp9` with 4. The same-experiment corpus explicitly highlighted these as boundaries of the spliceosome/RNA-processing claim: Sm-related or PRP19-adjacent annotation alone did not guarantee a focal transcriptional phenotype. I discounted them for the final point estimate because SRSF1 is a core shuttling SR regulator and a TNPO3 cargo in the canonical SR-import pathway, while `Snrpn` is an imprinted Sm-like paralog, `Rp9` is retinal/U4-U6-U5-associated, and `Ctnnbl1` was empirically buffered despite PRP19-complex proximity. `Hnrnpa2b1`, `Hnrnph2`, and `Ddx3x` provided a softer warning that abundant RBPs can score near-null in this assay.

Putting those together, I called `Srsf1` nonzero but below the broad core-spliceosome/TNPO3 class. I placed it near the weaker end of the positive RNA-processing responders, close to `Snrnp70` and `Tardbp`, because direct loss of one SR protein should be less pleiotropic than disabling `TNPO3` or 3-prime splice-site recognition, but SRSF1 is more central to enhancer-dependent splicing than the flat Sm/PRP19-adjacent counterexamples. The resulting point estimate is **230 DEGs**.

## Limits and extrapolation

The biggest uncertainty is that the supplied training data contain no measured `Srsf1`, `Srsf2`, `Srsf3`, `Srsf5`, `Srsf6`, or `Srsf7` perturbation in the focal group, so the estimate cannot be anchored to an SR paralog knockout. The DE readout is 3-prime-biased total gene abundance and cannot count direct SRSF1-dependent exon inclusion, intron retention, or nuclear-export phenotypes; a real isoform phenotype could therefore produce fewer whole-gene DEGs than the biochemical centrality of SRSF1 suggests. Conversely, if acute SRSF1 loss triggers the same vulnerable-neuron stress state as `Tnpo3`, the true count could approach several hundred. I chose the middle of that asymmetric evidence: clearly nonzero, but substantially attenuated relative to `Tnpo3`, `U2af2`, and `Rnpc3`.
