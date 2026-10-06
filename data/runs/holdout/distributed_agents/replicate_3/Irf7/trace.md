# DEG-count prediction for held-out `Irf7`

## Question and resolved ambiguities

The requested target list contains one held-out perturbation, `Irf7`. I interpreted the endpoint as the exact training-count definition: the number of measured genes in `151 TH Prkcd Grin2c Glut` with Scanpy Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05`, including the perturbed target transcript itself if it would pass. The held-out `Irf7` perturbation was absent from both the all-cell differential-expression parquet and the focal-cell DEG-count CSV, so all numerical calibration below uses only non-held-out perturbations.

`Irf7` was not represented in the selected Distributed Agents same-experiment corpus, which is also expected for this held-out run; I therefore used corpus reports for held-in IFN/IRF/TLR/JAK-STAT/NF-kB neighbors and direct parquet/count observations for those same held-in targets.

## Sources used

- Differential-expression input: `[local file: training_de_all_cell_groups.parquet]`.
- Training endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested targets: `[local file: 114_Irf7.csv]`.
- Internal same-experiment knowledge layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, especially high-confidence claims that unchallenged NeuN-enriched neurons lack a detectable basal type-I-IFN/IFNAR-ISGF3 program and that represented IFN-receptor, STAT, IRF, NF-kB-neighbor, pathogen-sensor, and TLR perturbations do not form a coherent inflammatory or PRR-to-IRF module.
- PubMed and curated mechanism priors:
  - Honda et al., 2005, Nature, DOI `10.1038/nature03464`, PMID `15800576`: mouse `Irf7` is essential for virus- and TLR-driven IFN-alpha/beta induction and systemic type-I-IFN responses.
  - Ivashkiv and Donlin, 2014, Nat Rev Immunol, PMID `24362405`: type-I IFN signaling through IFNAR, JAK1/TYK2, STAT1/STAT2/IRF9, ISGs, and the context dependence of tonic IFN.
  - Schneider et al., 2014, Annu Rev Immunol, PMID `24555472`: ISG products form a broad antiviral effector network downstream of IFN signaling.
  - Au-Yeung et al., 2013, JAKSTAT, PMC `PMC3772101`: STAT1/STAT2/IRF9 transcriptional regulation in the interferon JAK-STAT pathway.
  - Daffis et al., 2009, PLoS Pathog, DOI `10.1371/journal.ppat.1000607`: IRF3/IRF7 are required for IFN-alpha/beta and ISG induction in West Nile virus-infected primary cortical neurons.

## Dataset calibration

I first read the 1,674 non-held-out focal-cell counts. The distribution is extremely sparse:

- median `n_degs`: `0`
- 75th percentile: `1`
- 90th percentile: `2`
- 95th percentile: `18`
- maximum: `2677`

So the prior for a random target in this population is zero unless there is either direct pathway evidence or a strong within-dataset neighbor pointing away from the null.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for held-in perturbations in the relevant antiviral and cytokine circuitry. For each analog, I checked both the provided endpoint count and the lowest adjusted p-value across all 17,259 genes in the focal group. The biologically closest held-in comparators were:

| held-in perturbation | focal `n_degs` | focal min `pvals_adj` | why it matters for `Irf7` |
|---|---:|---:|---|
| `Irf1` | 0 | 1.000 | IRF transcription factor; corpus `Irf1:F003` found no shared IFN/MHC response across IRFs, IFN receptors, STATs, `Nfkb1`, `Rel`, `Chuk`, and `Ifih1`. |
| `Irf2` | 0 | 1.000 | IFN/ISRE transcriptional brake; loss did not derepress ISGs in Distributed Agents claim `claim:5ae625868e0586fef8b7`. |
| `Irf3` | 0 | 1.000 | canonical PRR-to-IFNB1 factor immediately upstream of `Irf7` induction/amplification; held-in pathway members were flat. |
| `Irf5` | 0 | 0.789 | IRF/TLR inflammatory factor; no shared neuronal IRF/TLR module. |
| `Irf8` | 0 | 0.121 | immune IRF-family factor; related IRFs and STATs were null or singleton-only in matched neuronal groups. |
| `Irf9` | 0 | 1.000 | ISGF3 DNA-binding subunit downstream of IFNAR; Distributed Agents `Irf9:F001` reported absent canonical ISG down-regulation after loss. |
| `Ifnar1` | 0 | 1.000 | type-I-IFN receptor subunit; Distributed Agents `Ifnar1:F002/F003` reported absent ISG loss and flat IFNAR-axis comparators. |
| `Ifnar2` | 0 | 1.000 | type-I-IFN receptor subunit; direct IFNAR/JAK-STAT/ISGF3 comparator for tonic IFN signaling. |
| `Stat1` | 1 | 0.027 | only the `Stat1` self-transcript passed FDR 0.05 in this focal group; canonical ISGs and MHC-I genes did not. |
| `Stat2` | 0 | 1.000 | ISGF3 partner with STAT1/IRF9; null in the focal group. |
| `Ifih1` | 0 | 1.000 | MDA5/RLR RNA sensor upstream of MAVS/TBK1/IRF3/IRF7; its null was pathway-wide rather than a hidden IFN response. |
| `Adar` | 0 | 0.184 | ADAR1 loss can unmask dsRNA and induce MDA5/IFN, but this screen showed no AGS-like IFN state. |
| `Tlr3` | 0 | 1.000 | endosomal dsRNA receptor signaling through TRIF/IRF3/NF-kB; Distributed Agents `Tlr3:F003` found no TLR/IFN phenocopy. |
| `Tlr7` | 0 | 1.000 | endosomal ssRNA receptor with MyD88-to-IRF7 biology in immune cells; flat in the focal group. |
| `Tlr8` | 0 | 1.000 | TLR7-family endosomal sensor; flat in the focal group. |
| `Traf3` | 0 | 1.000 | adaptor linking TLR/RLR pathways to IRF activation; flat in the focal group. |
| `Nfkb1` | 0 | 1.000 | innate inflammatory transcription-factor pathway member; flat in the focal group. |
| `Rel` | 0 | 0.140 | NF-kB-family comparator; no focal FDR hit. |
| `Chuk` | 0 | not refiltered | IKK/NF-kB comparator from the same corpus neighborhood; endpoint was null. |

I also directly inspected focal-cell rows for a representative IFN/ISG/MHC panel under the held-in pathway perturbations: `Irf7`, `Ifnb1`, `Isg15`, `Ifit1`, `Ifit2`, `Ifit3`, `Mx1`, `Mx2`, `Oas1a`, `Oasl1`, `Oasl2`, `Rsad2`, `Usp18`, `Rtp4`, `Stat1`, `Stat2`, `Irf9`, `B2m`, `H2-K1`, and `Tap1`. None of these canonical outputs reached FDR 0.05 for any of the represented IRF, IFN-receptor, IFNGR, TLR, RLR, or NF-kB perturbations that were queried in the focal class; most adjusted p-values were exactly `1.0`. In particular, the measured `Irf7` transcript itself was also FDR-null in every queried related perturbation, consistent with little tonic IFN amplification in `151 TH Prkcd Grin2c Glut` nuclei.

The same-experiment Distributed Agents corpus matched the raw count picture. Three internal claims were especially relevant:

- `claim:5ae625868e0586fef8b7`: basal postnatal NeuN-enriched neurons lack a detectable tonic type-I-IFN/IFNAR-ISGF3-driven ISG program. This claim is anchored by `Ifnar1`, `Ifnar2`, `Irf2`, `Irf9`, and `Stat2` findings.
- `claim:304ba198cd28519c1837`: basal loss of represented IFN-receptor, STAT, IRF, NF-kB-neighbor, and pathogen-sensor genes does not engage a coherent neuronal IFN/ISG/MHC-I inflammatory module. This is anchored by `Irf1` and `Stat1` negative results and supported by `Irf8` and `Irf9` cross-perturbation contrasts.
- `claim:3ac1aaff5686e4bbeb6f`: represented TLR/CD14 and innate receptor perturbations in unchallenged neuronal conditions do not form a shared TLR/PRR-to-NF-kB/IRF module.

## Target-specific prediction

### `Irf7`

`Irf7` has a strong external role as a master amplifier of antiviral type-I-interferon induction. The Honda et al. `Irf7-/-` study and later IFN pathway reviews make it an obvious factor to test in any PRR-to-IFN or IFNAR-ISGF3 model. That mechanism, however, is highly stimulus- and lineage-gated: IRF7 becomes central after viral, IFN, or TLR9-family activation, especially in interferon-producing immune states, and Daffis et al. showed the same IRF3/IRF7 dependence for West Nile virus-infected cortical neurons.

The held-in perturbations most likely to uncover tonic IRF7 biology in this focal assay were all quiet. Loss of `Ifnar1`, `Ifnar2`, `Stat2`, or `Irf9` should have reduced an active IFNAR-ISGF3 feedback loop that maintains `Irf7` and ISGs; all have `0` focal DEGs. Loss of `Irf1`, `Irf2`, `Irf3`, `Irf5`, or `Irf8` should have perturbed adjacent IRF inflammatory or antiviral regulation; all have `0` focal DEGs. Loss of `Ifih1`, `Tlr3`, `Tlr7`, `Tlr8`, `Traf3`, `Nfkb1`, `Rel`, and `Chuk` should have exposed basal PRR/TLR/NF-kB coupling if it were active; each has `0` focal DEGs. `Stat1` is the only nearby nonzero endpoint, and its one passing gene is its own down-regulated transcript rather than a downstream ISG or MHC-I module, so it is a counterexample to a broad IFN prediction rather than support for one.

The most likely outcome is therefore that sparse acute `Irf7` loss in unchallenged juvenile thalamic glutamatergic neurons leaves no gene below BH FDR 0.05. I predict `0` DEGs.

## Limits

- `Irf7` itself was held out, so no direct `Irf7` perturbation signature or self-transcript p-value was available.
- The closest RLR/TLR adaptors `Mavs`, `Tbk1`, `Ikbke`, `Ticam1`, `Myd88`, and `Traf6` were not in the training-count table, so the comparison relies on held-in receptors, IRFs, IFN receptors, STATs, and NF-kB neighbors.
- The assay was an unchallenged, NeuN-enriched postnatal neuronal perturbation screen. It does not test viral infection, exogenous IFN-alpha/beta, endosomal TLR ligands, systemic IFN production, plasmacytoid dendritic cells, microglia, astrocytes, or injury contexts where IRF7 biology is expected to be much stronger.
- A prediction of `0` means no measured transcript is expected to pass this assay's FDR 0.05 threshold in recovered `151 TH Prkcd Grin2c Glut` nuclei; it is not a claim that IRF7 is biologically irrelevant or unedited.

