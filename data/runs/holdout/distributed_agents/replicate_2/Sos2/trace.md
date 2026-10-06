# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out manifest contains one perturbation:

| target_name |
|---|
| Sos2 |

I interpreted the requested endpoint as the integer number of measured genes with `pvals_adj < 0.05` for the held-out `Sos2` CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` nuclei. Because `Sos2` was held out completely, I did not treat an absent `Sos2` signature as a zero observation; instead I transferred from training perturbations in the same focal group and from external knowledge of SOS2/SOS1 Ras-GEF biology.

## Sources used

- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal training-count CSV: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest: `[local file: 218_Sos2.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, especially the `Sos1`, `Braf`, `Map2k1`, `Shoc2`, `Spred2`, and Ras/MAPK claims.
- Distributed Agents runtime profile comparison over `151 TH Prkcd Grin2c Glut` Wilcoxon `scores`.
- External literature from PubMed:
  - Esteban et al. 2000, DOI `10.1128/MCB.20.17.6410-6413.2000`, PMID `10938118`.
  - Qian et al. 2000, DOI `10.1093/emboj/19.4.642`, PMID `10675333`.
  - Baltanas et al. 2013, DOI `10.1128/MCB.01026-13`, PMID `24043312`.
  - Rojas et al. 2011, DOI `10.1177/1947601911408078`, PMID `21779500`.
  - Baltanas, Garcia-Navas and Santos 2021, DOI `10.3390/ijms22126613`, PMID `34205562`.
  - Sheffels et al. 2018, DOI `10.1126/scisignal.aar8371`, PMID `30181243`.

## Computational steps

1. I read the held-out manifest and found exactly one requested row, `Sos2`.
2. I loaded the focal count CSV. It contains 1,674 training perturbations; the endpoint is sparse in this group: median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`, 95th percentile `= 18`, and the high tail is driven mostly by core RNA/proteostasis/transcriptional regulators rather than Ras/MAPK signaling genes.
3. I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to represented Ras/MAPK or neurotrophin/RTK comparators. For each comparator I recomputed the local count as `sum(pvals_adj < 0.05)`, checked that it matched the count CSV, and inspected the leading genes and sentinel ERK-output genes (`Vgf`, `Ptpn5`, `Unc13a`, `Etv5`, `Atp2a2`, `Dusp4`, `Dusp6`, `Spry2`, `Spry4`, `Fos`, `Egr1`, `Cul7`).
4. I ran a Distributed Agents runtime `profile_compare` on Wilcoxon `scores` in the focal cell group for 17 Ras/MAPK-adjacent training perturbations. I used exact same-cell profiles and `pvals_adj < 0.05` as the significance mask, then inspected `Sos1` against the ten closest mechanistic Ras/MAPK peers.

## Target-specific transfer to Sos2

`Sos2` encodes one of the two mammalian Son of sevenless Ras guanine nucleotide exchange factors. The most direct in-dataset analog is `Sos1`, because SOS1 and SOS2 are paralogous, ubiquitous Ras GEFs linking receptor tyrosine kinase and adaptor complexes to Ras-GTP. The focal endpoint for `Sos1` was:

| training perturbation | focal n_degs | expression evidence in 151 TH Prkcd Grin2c Glut |
|---|---:|---|
| `Sos1` | 0 | no q<0.05 genes among 210 perturbed nuclei; the top coordinate was `Cul7` up, logFC `+1.005`, BH q `0.0778`; `Vgf`, `Ptpn5`, `Unc13a`, `Etv5`, `Dusp6`, `Spry`, `Fos`, and `Egr1` were all nonsignificant |

The same-experiment Distributed Agents corpus makes the same point in `Sos1:F001-F006`: `Sos1` produced only a weak `Cul7` response and did not recapitulate the small thalamic RAF/MEK attenuation module. In the runtime profile comparison, `Sos1` also lacked a coherent weak signature: its best whole-profile Pearson neighbor among all 1,674 eligible training targets was only `r = 0.0646`, and the best cosine was only `0.0865`. Against mechanistic pathway comparators, the score-vector similarities were all near zero: `Sos1` versus `Braf` cosine `0.0068`, versus `Map2k1` `0.0201`, versus `Shoc2` `0.0042`, versus `Ntrk2` `-0.0442`, versus `Map2k2` `0.0108`, versus `Mapk1` `0.0004`, versus `Kras` `0.0362`, versus `Hras` `0.0422`, versus `Raf1` `-0.0087`, and versus `Ptpn11` `-0.0226`. Thus the closest observed paralog was not a positive responder and was not hiding in a broader related expression state.

The main positive counterexamples were downstream of Ras rather than at the SOS level:

| training perturbation | focal n_degs | focal significant genes |
|---|---:|---|
| `Braf` | 4 | `Atp2a2`, `Ptpn5`, `Vgf`, `Unc13a`, all down |
| `Map2k1` | 4 | `Vgf`, `Ptpn5`, `Unc13a`, `Etv5`, all down |
| `Shoc2` | 1 | `Vgf` down |
| `Ntrk2` | 3 | `Ntrk2`, `Atp2a2`, `Vgf`, all down |

Those observations are useful because they show that `151 TH Prkcd Grin2c Glut` and the Wilcoxon/FDR endpoint could detect a narrow trophic Ras/RAF/MEK-like state, especially the `Vgf`/`Ptpn5`/`Unc13a` arm. The Distributed Agents corpus claim `claim:5f4082f202c79d3b3fcc` summarizes this as a sparse Braf/Map2k1 module partially shared by `Ntrk2` and `Shoc2`.

However, the same dataset argues strongly against linear propagation from upstream RasGEFs or RTK/SHP2/Ras proteins to that module:

| comparator class | training perturbations and focal n_degs | interpretation for Sos2 |
|---|---|---|
| upstream Ras GTPases and SHP2 | `Hras = 0`, `Kras = 0`, `Ptpn11 = 0` | loss of single upstream positive regulators did not drive the `Braf`/`Map2k1` Vgf/Ptpn5/Unc13a module |
| upstream FGF receptors | `Fgfr1 = 0`, `Fgfr2 = 0`, `Fgfr3 = 0` | receptor-level RTK perturbations were buffered in the focal group |
| alternate RAF/MEK/ERK nodes | `Raf1 = 0`, `Map2k2 = 0`, `Mapk1 = 0` | the detectable response was not a generic MAPK-chain consequence |
| Ras negative regulators | `Rasa2 = 0`, `Spred1 = 0`, `Spred2 = 0` | single perturbations of other represented Ras-regulatory nodes were also silent |
| LZTR1/Rasopathy neighborhood | `Lztr1 = 1`, `Shoc2 = 1` | a SHOC2/BRAF arm can touch `Vgf`, but this remains far smaller than a broad ERK transcriptional collapse |
| PI3K/mTOR arm | `Pik3r1 = 0`, `Akt3 = 0`, `Mtor = 2`, `Tsc2 = 86` | a downstream mTOR hit can be broad, but proximal SOS-to-PI3K logic was not apparent in the same neuronal assay |

This matches Distributed Agents corpus claim `claim:4af1e0ceaef9adda14b9`: in these postnatal neuronal snRNA-seq data, the detectable basal Ras/MAPK RNA output is restricted to a sparse Braf/Map2k1 branch rather than being shared across represented upstream Ras/GEF/SHP2, RAF1, MEK2, ERK2, RasGAP, or RASopathy perturbations.

The external biology also pushes the point estimate toward zero rather than toward the 3-4 DEGs seen after direct BRAF/MEK1/NTRK2 perturbation. `Sos2` germline null mice are viable, fertile, and histologically normal in contrast to `Sos1` null embryonic lethality (Esteban et al. 2000; Qian et al. 2000). Adult single `Sos2` knockout is much milder than combined `Sos1/Sos2` loss, supporting functional redundancy and a dominant role for SOS1 in many contexts (Baltanas et al. 2013; Rojas et al. 2011; Baltanas, Garcia-Navas and Santos 2021). SOS2 can matter in KRAS-transformed fibroblast or cancer-cell PI3K/AKT signaling (Sheffels et al. 2018), but that context is proliferative, oncogenic, and often stimulated; it is a poor match to sparse P16 CRISPR loss in postmitotic NeuN-positive thalamic neurons, where `Pik3r1` and `Akt3` were themselves focal nulls.

## Prediction

I predict `Sos2` will have no measured gene crossing BH q<0.05:

| target_name | predicted_n_degs |
|---|---:|
| Sos2 | 0 |

The zero/nonzero decision is driven mainly by the within-dataset evidence from `Sos1 = 0`, the absence of `Vgf`/`Ptpn5`/`Unc13a` activation in `Sos1`, and the flat upstream Ras/RTK comparators. External SOS2 knowledge is secondary and is used to decide that SOS2 should not be elevated above SOS1 or downstream BRAF/MEK1 in this assay.

## Limits

- `Sos2` itself was held out, and the same-experiment Distributed Agents corpus had no direct `Sos2` perturbation finding. The prediction extrapolates from `Sos1` and neighboring training genes.
- Acute AAV CRISPR in sparse postmitotic neurons measures steady-state nuclear RNA only. It does not measure indel rate, SOS2 protein, Ras-GTP, pERK, pAKT, immediate ligand responses, morphology, or electrophysiology.
- The screen averaged only partial mRNA depletion per guide. If SOS1 and SOS2 are partly redundant, this design is especially likely to understate a phenotype that would require double loss or stronger protein depletion.
- Several canonical Ras/MAPK nodes were not represented as training perturbations in this focal universe, including `Nf1`, `Nras`, `Mapk3`, `Araf`, `Rasa1`, and `Dusp6`.
- A 0 versus 1 call is intrinsically fragile for this endpoint. The closest paralog `Sos1` had one subthreshold `Cul7` coordinate at q `0.0778`; a neighboring SOS2 perturbation could plausibly yield one marginal DEG even though the best integer point prediction is 0.
