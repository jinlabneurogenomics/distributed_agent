# Fth1 DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

The task is to predict `n_degs` for the held-out perturbation `Fth1` in the focal thalamic glutamatergic cell group `151 TH Prkcd Grin2c Glut`.

I treated `n_degs` exactly as defined in the prompt: the number of measured genes with `pvals_adj < 0.05` in the held-out `Fth1` CRISPR perturbation signature for this cell group. The count includes the target transcript if it is measured and passes FDR, but the held-out experiment contains no `Fth1` rows, so the target-RNA call itself had to be predicted rather than observed.

## Sources used

- Input training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest: `[local file: 082_Fth1.csv]`
- Internal Distributed Agents corpus: `perturbai-july-260713-sourceguard-1773-v1`
- PubMed literature for ferritin heavy chain, ferritinophagy, and neuronal Fth loss:
  - Ferreira et al. 2000, J Biol Chem, DOI `10.1074/jbc.275.5.3021`, PMID `10652280`
  - Mancias et al. 2014, Nature, DOI `10.1038/nature13148`, PMID `24695223`
  - Santana-Codina et al. 2021, Adv Exp Med Biol, DOI `10.1007/978-3-030-62026-4_4`, PMID `34370287`
  - Rui et al. 2020, J Pineal Res, DOI `10.1111/jpi.12704`, PMID `33206394`

## Dataset calibration

The focal training file contained 1,674 non-held-out perturbations. The endpoint was highly zero-inflated in this cell group:

- 1,205 / 1,674 targets had `n_degs = 0`
- 469 / 1,674 had a nonzero count
- quartiles were 0, 0, and 1
- the 90th percentile was 2
- broad signatures were rare but present, with Uba5, Tpr, Sin3a, Rnpc3, Zbtb7a, U2af2, Psmb4, and Hnrnpu ranging from 733 to 2,677 DEGs

I then checked represented perturbations in the FTH1 neighborhood:

```python
targets = ["Tfrc", "Ireb2", "Aco2", "Gpx4", "Acsl4", "Nfe2l2", "Sqstm1", "Atg5"]
flt = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & (ds.field("gene_target").isin(targets))
)
table = ds.dataset(de_parquet, format="parquet").to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=flt,
)
```

That pulled 17,259 measured genes for each of the eight biologically chosen analogs. Their observed focal `pvals_adj < 0.05` counts were:

| target | focal n_degs | relevant focal expression evidence |
|---|---:|---|
| `Tfrc` | 0 | Its best focal hit was `Pfkp` up, but it stopped just short of this task's cutoff (`p_adj = 0.0523`); `Vegfa` was nominal at best (`p_adj = 0.250`), and `Fth1`, `Ncoa4`, `Sqstm1`, `Atg5`, `Gpx4`, `Aco1`, `Aco2`, `Hmox1`, `Gclc`, `Gclm`, `Ddit3`, and `Hspa5` were all FDR-negative. |
| `Ireb2` | 1 | The one focal hit was `Abhd12b` down (`p_adj = 1.68e-4`), not an iron-storage or ferroptosis marker. `Fth1`, `Tfrc`, `Ncoa4`, `Aco1`, `Aco2`, `Hmox1`, `Hif1a`, `Vegfa`, `Pfkp`, `Gclc`, and `Gclm` were all FDR-negative. |
| `Acsl4` | 1 | The one focal hit was the `Acsl4` target transcript itself (`p_adj = 3.83e-16`); downstream sterol and ferroptosis markers were absent in this cell group. |
| `Sqstm1` | 1 | The one focal hit was the `Sqstm1` target transcript itself (`p_adj = 7.93e-4`); `Sfxn5` was next but did not pass 0.05 (`p_adj = 0.0923`). |
| `Gpx4` | 0 | No focal gene approached FDR 0.05; the smallest adjusted p-value was 0.767. |
| `Nfe2l2` | 0 | No focal NRF2/ARE or redox response was detected; the smallest adjusted p-value was 0.367. |
| `Atg5` | 0 | No focal autophagy/UPR response was detected; the smallest adjusted p-value was 0.105. |
| `Aco2` | 0 | No focal Fe-S/TCA stress response was detected; the smallest adjusted p-value was 0.330. |

The exact ferritin complex and ferritinophagy genes were poorly represented as perturbations: `Ftl1`, `Ncoa4`, `Slc11a2`, `Slc40a1`, `Hmox1`, `Hfe`, `Hfe2`, `Tfr2`, `Steap3`, `Cp`, and `Hamp` were absent from the focal training-count table. `Ncoa4` and `Fth1` were measured as expression features, and neither was induced by any of the focal iron-axis analogs above.

As a guard against missing a common ferritin response elsewhere, I also filtered the focal parquet to the measured genes `Fth1` and `Ncoa4` across all 1,674 training perturbations. `Fth1` was FDR-significant after only two focal perturbations, `Uba5` and `Elp1`, which are very broad proteostasis/splicing responders rather than direct iron-homeostasis perturbations. `Ncoa4` was FDR-significant after only three broad focal perturbations, `Tpr`, `Cic`, and `Uba5`.

## Corpus and literature interpretation

The internal Distributed Agents corpus had no `Fth1` target card in `perturbai-july-260713-sourceguard-1773-v1`, so the FTH1-specific mechanism came from PubMed.

FTH1 is the ferritin heavy chain. It supplies the ferroxidase activity needed for the ferritin shell to oxidize and store iron safely; complete H-ferritin deletion in mouse is early embryonic lethal, while heterozygotes are viable (Ferreira et al. 2000). NCOA4 is the cargo receptor that delivers ferritin to autophagosomes for ferritinophagy and regulates intracellular bioavailable iron by ferritin turnover (Mancias et al. 2014; Santana-Codina et al. 2021). In neurons, conditional Fth deletion is compatible with viability but increases iron dysregulation and susceptibility to ferroptotic injury after traumatic brain injury (Rui et al. 2020), so FTH1 matters for neuronal iron stress without necessarily producing a large basal nuclear RNA program in uninjured juvenile neurons.

The Distributed Agents corpus strongly calibrated the represented pathway analogs toward sparse or absent neuronal DE in this exact PerturbAI assay:

- `Tfrc`: the corpus reported that P16 sparse `Tfrc` loss produced only five corrected downstream genes across 21 neuronal groups, one gene per responding group, and did not trigger broad IRP, ferritin, HIF, redox, or mGluR1-synaptic transcriptional programs. Its literature-obvious comparators `Ireb2`, `Hif1a`, `Abcb7`, and `Nfs1` were flat or nearly flat in matched groups.
- `Ireb2`: the corpus reported one robust downstream event, `Abhd12b` down in `151 TH Prkcd Grin2c Glut`, and no FDR<0.10 movement of canonical iron-homeostatic or stress mRNAs including `Tfrc`, `Fth1`, `Aco1`, `Ncoa4`, `Slc11a2`, `Slc40a1`, or `Hif1a` across measured groups.
- `Gpx4`, `Acsl4`, and `Nfe2l2`: the corpus described a high-confidence boundary in which represented glutathione, GPX4, ACSL4, ferroptosis, and NRF/redox perturbations did not form a shared basal neuronal transcriptomic module; `Gpx4` and `Nfe2l2` were transcriptionally silent, and `Acsl4` had a sparse sterol-linked response rather than a ferroptosis program.
- `Atg5` and `Sqstm1`: the corpus found autophagy and p62 perturbations to be restricted and non-interchangeable. `Atg5` did not produce a canonical autophagy, lysosomal, proteasome-rebound, UPR, or ISR transcriptional program; `Sqstm1` had only a few single-gene neuronal events and lacked NRF2/redox, lysosomal-autophagy, UPR, or ISR induction.
- `Aco2`: the corpus reported that acute perturbations of represented mitochondrial Fe-S, TCA, and pyruvate-dehydrogenase nodes generally failed to resolve into a coherent postmitotic neuronal iron-sulfur or mitochondrial-stress module.

## Target-specific prediction

`Fth1` is a direct iron-storage perturbation, not merely a generic ferroptosis marker, so `Tfrc` and `Ireb2` are imperfect analogs: TFRC loss reduces iron entry, whereas FTH1 loss should reduce buffering of labile iron. The exact ferritin light-chain partner `Ftl1` and the ferritinophagy receptor `Ncoa4` were not available as training perturbations. That forces extrapolation.

Still, every assayed route that should have revealed a secondary basal iron or lipid-peroxidation state was quiet in the focal group:

- direct iron entry through `Tfrc`: 0 DEGs in `151`, with only subthreshold `Pfkp`
- direct IRP regulation through `Ireb2`: 1 singleton, `Abhd12b`, with no ferritin or TFRC RNA program
- downstream ferroptosis capacity through `Gpx4` and `Acsl4`: 0 or self-only in `151`
- antioxidant transcription through `Nfe2l2`: 0 in `151`
- ferritinophagy/autophagy context through `Atg5` and `Sqstm1`: 0 or self-only in `151`
- Fe-S/TCA mitochondrial stress through `Aco2`: 0 in `151`

I therefore predict no downstream gene will pass FDR 0.05 after acute mosaic `Fth1` loss in recovered `151 TH Prkcd Grin2c Glut` nuclei.

The main remaining ambiguity is the `Fth1` target transcript itself. In the focal training set, 319 of 1,642 represented targets with a self row had significant self-RNA reduction, and 237 of the 276 one-DEG endpoints were self-only. That makes a self-only `Fth1` endpoint possible. I did not add one count for that alone, because the closest focal iron-axis perturbations `Tfrc`, `Ireb2`, `Atg5`, `Aco2`, and `Nfe2l2` did not produce significant self rows despite having log-fold changes of the same rough size as many edited targets, and because the prompt explicitly cautions that target-RNA loss is an unreliable engagement proxy in this assay.

## Final point estimate

| target | predicted_n_degs |
|---|---:|
| `Fth1` | 0 |

## Limits

This is a weak extrapolation at the exact-complex level. `Ftl1` and `Ncoa4`, the most natural ferritin-shell and ferritinophagy comparators, were not training perturbations. The PerturbAI screen assayed nuclear RNA in recovered NeuN-positive nuclei, not ferritin protein, ferritinophagic flux, labile iron, lipid peroxidation, edited-allele fractions, or cells lost before sorting. A true FTH1 protein defect could therefore alter iron buffering or stress susceptibility without creating a broad FDR-level survivor transcriptome. The final zero is driven mainly by within-dataset absence of basal neuronal iron/ferroptosis/autophagy RNA programs; PubMed literature was used to choose those analogs and to bound why a strong injury-conditioned ferritin phenotype need not appear in this basal P16-to-P37/44 readout.
