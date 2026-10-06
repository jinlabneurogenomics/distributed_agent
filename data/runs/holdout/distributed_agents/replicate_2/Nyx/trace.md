# Prediction task

I predicted the held-out endpoint for `Nyx` in `151 TH Prkcd Grin2c Glut` cells: the number of measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05` after the acute AAV CRISPR loss-of-function perturbation. `Nyx` was fully held out as a perturbation target, so I did not use a `Nyx` target signature or `Nyx` target count. I interpreted a zero prediction as "no measured transcript passes the experiment's FDR 0.05 cutoff in this focal cell group", not as evidence that Nyx is biologically irrelevant in retina.

# Sources

- Input manifest: `[local file: 161_Nyx.csv]`; this run contains only `Nyx`.
- Training endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`, 1,674 non-held-out perturbations in the focal cell group.
- Training differential expression: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` and to mechanistic comparator targets.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`; I used the `Gpr179`, `Grm6`, and `Gnb5` ledgers plus corpus claims linking the ON-bipolar mGluR6/TRPM1/RGS-GNB5 signalplex.
- Distributed Agents runtime profile comparison over `logfoldchanges` in the focal cell group for the hand-selected ON-bipolar/Gbeta5-adjacent cohort. The local artifacts were `nyx_on_bipolar_comparison.json` and `nyx_on_bipolar_inspect.json`.
- PubMed/NCBI literature for Nyx and retinal ON-bipolar signaling: Bech-Hansen et al. 2000, DOI `10.1038/81619`, PMID `11062471`; Gregg et al. 2003, DOI `10.1167/iovs.02-0501`, PMID `12506099`; Gregg et al. 2007, DOI `10.1152/jn.00608.2007`, PMID `17881478`; Pearring et al. 2011, DOI `10.1523/JNEUROSCI.1014-11.2011`, PMID `21734298`; Cao et al. 2011, DOI `10.1523/JNEUROSCI.1682-11.2011`, PMID `21832182`; Orlandi et al. 2013, PMID `24114537`; Ray et al. 2014, DOI `10.1523/JNEUROSCI.4044-13.2014`, PMID `24790204`; Dhingra and Vardi 2012, DOI `10.1002/wmts.43`; Masu et al. 1995, DOI `10.1016/0092-8674(95)90354-2`, PMID `7889569`.

# Computation

I first read the endpoint CSV and searched for targets in Nyx's native retinal ON-bipolar cascade and nearby protein families. The focal training counts were:

| comparator | focal `n_degs` | relevance to `Nyx` |
| --- | ---: | --- |
| `Gpr179` | 0 | ON-bipolar scaffold that forms a macromolecular complex with mGluR6, TRPM1, and RGS proteins |
| `Grm6` | 0 | mGluR6 is the upstream glutamate receptor that gates TRPM1 in ON bipolar cells |
| `Gnb5` | 0 | obligatory Gbeta partner of R7 RGS complexes; linked to GPR179/RGS signaling |
| `Gnao1` | 1 | Go alpha subunit downstream of mGluR6; the one focal hit was the target transcript itself |
| `Gpr158` | 1 | brain-enriched GPR179 paralog and RGS7/GNB5 scaffold |
| `Rgs6` | 0 | assayed R7 RGS family member; the exact retinal RGS7/RGS11 genes were not training targets |
| `Kcnj6` | 0 | GIRK channel adjacent to Gbeta5/R7 signaling, but not a retinal ON-bipolar scaffold |
| `Grm1` | 1 | mGluR paralog |
| `Grm5` | 0 | mGluR paralog |
| `Grm7` | 1 | mGluR paralog |
| `Grm8` | 0 | mGluR paralog |
| `Prkca` | 0 | rod-bipolar marker and signaling gene, downstream rather than a Nyx complex component |
| `Vsx1` | 0 | retinal bipolar-lineage transcription factor |
| `Vsx2` | 0 | retinal bipolar-lineage transcription factor |
| `Otx2` | 0 | retinal/photoreceptor-bipolar developmental regulator |
| `Lrrtm1` | 1 | neural leucine-rich-repeat family comparator, not the Nyx signalplex |
| `Lrrtm4` | 0 | neural leucine-rich-repeat family comparator, not the Nyx signalplex |
| `Cacna1a` | 0 | channel-family counterexample |
| `Cacna1d` | 0 | channel-family counterexample |
| `Cacna1e` | 0 | channel-family counterexample |
| `Trpm3` | 0 | assayed TRPM-family member; exact TRPM1 was not a target |
| `Trpm7` | 0 | assayed TRPM-family member; exact TRPM1 was not a target |

For the closer subset I filtered the parquet to the focal cell group and confirmed that `Gpr179`, `Grm6`, `Gnb5`, `Prkca`, `Vsx2`, `Otx2`, and `Rgs6` had zero focal genes at FDR 0.05 across 17,259 measured transcripts; the minimum adjusted p-values were 0.519 for `Gpr179`, 1.0 for `Grm6`, 0.343 for `Gnb5`, 1.0 for `Prkca`, 1.0 for `Vsx2`, 0.885 for `Otx2`, and 1.0 for `Rgs6`. `Gnao1` had exactly one FDR hit, `Gnao1` itself, at log2FC -0.591 and FDR `9.42e-07`; no other readout moved.

The parquet pull was a direct filter of target rows, not a global model:

```python
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(comparator_targets)
)
```

I also checked the canonical retinal readout genes `Gnao1`, `Gnb3`, `Gnb5`, `Gng13`, `Gpr179`, `Grm6`, `Lrit3`, `Nyx`, `Rgs11`, `Rgs7`, and `Trpm1` within the focal `Gpr179`, `Grm6`, `Gnb5`, `Gnao1`, `Prkca`, `Vsx2`, `Otx2`, `Rgs6`, and `Lrrtm4` perturbations. All of those specific readouts had FDR 1.0 except for on-target `Gnao1`; the very large log-fold changes assigned to genes such as `Trpm1`, `Grm6`, or `Gpr179` were paired with FDR 1.0 and are therefore consistent with low-count numerical tails rather than interpretable regulation.

Finally, I ran a Distributed Agents runtime profile comparison on `Gpr179`, `Grm6`, `Gnb5`, `Gnao1`, `Prkca`, `Vsx2`, `Otx2`, `Rgs6`, `Lrrtm4`, and `Cacna1a`, using `logfoldchanges` as the signed profile and `pvals_adj < 0.05` as the significant-feature definition. Nine of the ten selected profiles had no significant focal features; only `Gnao1` had 1. Whole-profile correlations among flat profiles were not treated as positive biology, because the top signed features were nonsignificant in the query nodes.

# Nyx-specific reasoning

Nyx encodes nyctalopin, a membrane-attached leucine-rich-repeat extracellular protein. Human `NYX` mutations cause X-linked complete congenital stationary night blindness with an ON-pathway defect (Bech-Hansen et al. 2000), and the mouse `nob` allele is an `Nyx` lesion that removes the electroretinogram b-wave and reduces visual sensitivity (Gregg et al. 2003). Rescue experiments showed that expressing nyctalopin at depolarizing bipolar-cell dendritic tips restores the `nob` retinal phenotype, placing the core requirement postsynaptically in retinal ON bipolar cells rather than in a broad brain transcriptional program (Gregg et al. 2007).

The most appropriate in-dataset analogs were the ON-bipolar mGluR6/TRPM1 signalplex genes. `Gpr179` had 0 DEGs in the focal group, and Distributed Agents corpus findings `Gpr179:F002` and `Gpr179:F003` report that the canonical mGluR6/TRPM1/RGS-GNB5 signalplex transcripts did not move after `Gpr179` perturbation and that `Gpr158`, `Gnb5`, `Grm6`, and `Gnao1` were flat or one-gene sparse across matched groups. This is a close negative analog because GPR179 forms retinal ON-bipolar complexes with mGluR6, TRPM1, and RGS proteins (Orlandi et al. 2013) and helps recruit RGS7/RGS11 to gate TRPM1 with high sensitivity (Ray et al. 2014).

`Grm6` was an independent close negative analog with 0 focal DEGs. In retina, mGluR6 is required for the ON response (Masu et al. 1995) and lies upstream of the same TRPM1 effector channel that nyctalopin localizes. Distributed Agents `Grm6:F001` through `Grm6:F004` report no FDR-level `Grm6` downstream response in any recovered non-retinal neuronal class, no robust transcriptomic similarity to `Gpr179` or `Gnb5`, and no movement of canonical ON-bipolar cascade readouts including `Nyx`, `Trpm1`, `Lrit3`, `Gnb5`, `Gnao1`, `Rgs7`, and `Rgs11`. That directly argues that loss of one retinal signalplex component in postnatal NeuN+ brain nuclei does not induce a compensatory retinal-cascade RNA state.

`Gnb5` was also 0 in the focal endpoint. It is a less exact analog than `Gpr179` or `Grm6`, because Gbeta5/R7 RGS biology exists in non-retinal neurons, but it bounds the possibility that a GPR179/RGS/GNB5 scaffold defect alone would yield a broad nuclear response. The same-experiment corpus found `Gnb5` flat across measured neuronal groups and reported that `Rgs6`, `Gpr158`, `Gnao1`, `Gpr179`, and `Kcnj6` produced at most one downstream FDR<0.10 gene apiece in matched groups. Published Gbeta5/RGS work supports strong GPCR timing and developmental phenotypes in other assays, including Gbeta5 dependence of RGS proteins (Chen et al. 2003, DOI `10.1073/pnas.0631825100`) and GIRK-channel timing (Xie et al. 2010, DOI `10.1038/nn.2549`), but those are rapid signaling or germline phenotypes rather than evidence for a 3-4 week postnatal snRNA transcriptional module in this thalamic cluster.

The expression-pattern evidence matched the endpoint counts. In focal 151 cells, the top adjusted p-values for `Gpr179`, `Grm6`, and `Gnb5` were nonsignificant, and the ON-bipolar readout genes stayed at FDR 1.0. The only near-pathway nonzero comparator, `Gnao1`, was a one-gene self-hit, so I did not extrapolate it to a multi-gene Nyx effect. Broader family comparisons were likewise silent or nearly silent: `Vsx1`, `Vsx2`, and `Otx2` did not recover retinal-lineage programs; `Prkca` had no focal hits; represented mGluR paralogs had 0 or 1 focal DEG; and assayed LRR genes such as `Lrrtm1` and `Lrrtm4` did not show a family-wide LRR surface that would make an extracellular LRR perturbation broadly active.

The external Nyx literature also favors a zero focal RNA response. Pearring et al. 2011 showed that nyctalopin is needed for TRPM1 localization on retinal depolarizing bipolar-cell dendrites, and Cao et al. 2011 showed that TRPM1 forms complexes with nyctalopin in vivo and that nyctalopin also interacts with mGluR6. The experimental dataset excluded retina, olfactory bulb, and hindbrain and was NeuN+ enriched from brain nuclei; it therefore missed the native ON-bipolar compartment where Nyx loss is expected to act. AAV perturbation at P16-P37/P44 is also later and more mosaic than the germline `Nyx`/`nob` retinal studies, further reducing the likelihood that a structural retinal synapse defect would appear as a broad basal mRNA change in `151 TH Prkcd Grin2c Glut` thalamic neurons.

Therefore I predicted `Nyx` at the same floor as its closest represented ON-bipolar signalplex analogs:

```text
Nyx -> 0 DEGs
```

# Limits

- `Nyx` itself was held out, so this is transfer from `Gpr179`, `Grm6`, `Gnb5`, `Gnao1`, and broader retinal/LRR/channel comparators, not a direct observed Nyx signature.
- Several exact Nyx partners, including `Trpm1`, `Lrit3`, `Rgs7`, `Rgs11`, `Gnb3`, and `Gng13`, were present as readout genes but not as perturbation targets, so the closest perturbed scaffold was `Gpr179`.
- The same-experiment corpus had no direct `Nyx` node because `Nyx` was held out. Its claims entered only through training genes, chiefly `Gpr179`, `Grm6`, and `Gnb5`.
- Flat snRNA-seq at 3-4 weeks does not exclude changes in protein localization, mGluR6/TRPM1 gating, dendritic-tip structure, electroretinogram b-waves, or visual behavior. Those are exactly the expected native outputs of Nyx loss in retina.
- Some rank-tail log-fold changes for unexpressed retinal genes were numerically huge but had FDR 1.0; I treated significance and pathway coherence, not those isolated ratios, as the reliable evidence.
- The prediction extrapolates from non-retinal juvenile brain neuronal nuclei to an ON-bipolar retinal gene. That extrapolation is imperfect, but every assayed close comparator says this screen is transcriptionally insensitive to the retinal signalplex.
