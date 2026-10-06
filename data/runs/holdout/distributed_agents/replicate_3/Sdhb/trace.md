# DEG-count prediction trace

## Question interpreted

The requested held-out target list contains one mouse gene, `Sdhb`. I interpreted the task as predicting the official `n_degs` endpoint for a sparse AAV-CRISPR loss-of-function perturbation of `Sdhb` in the `151 TH Prkcd Grin2c Glut` focal cell group: the number of measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in perturbed nuclei versus matched non-targeting controls. The response signature and count for `Sdhb` itself were held out completely, so I treated all `Sdhb` rows as unavailable and transferred information from non-held-out training perturbations.

The main ambiguity is that the count includes the target transcript if it is measured and significantly depleted. In the visible training data, several oxidative-phosphorylation and TCA targets with `n_degs = 1` have only their own transcript below FDR 0.05. I therefore separated "self knockdown is likely visible" from "a downstream stress program is likely visible" in the prediction.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene Wilcoxon differential-expression statistics for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: official `151 TH Prkcd Grin2c Glut` FDR 0.05 DEG counts for 1674 non-held-out perturbations.
- `204_Sdhb.csv`: requested target manifest.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, especially curated findings for `Sdha`, `Ndufs2`, and `Opa1`.
- PubMed-indexed mechanism literature:
  - Rutter et al. 2010, "Succinate dehydrogenase - Assembly, regulation and role in human disease", DOI `10.1016/j.mito.2010.03.001`, PMID `20226277`.
  - Selak et al. 2005, "Succinate links TCA cycle dysfunction to oncogenesis by inhibiting HIF-alpha prolyl hydroxylase", DOI `10.1016/j.ccr.2004.11.022`, PMID `15652751`.
  - Hoekstra and Bayley 2012, "The role of complex II in disease", DOI `10.1016/j.bbabio.2012.11.005`, PMID `23174333`.
  - Fullerton et al. 2020, "The genetic basis of isolated mitochondrial complex II deficiency", DOI `10.1016/j.ymgme.2020.09.009`, PMID `33162331`.

## Computation over the supplied data

I first read the requested-target CSV and confirmed that the single held-out target is `Sdhb`.

I loaded the focal-cell training count CSV and used it to calibrate the endpoint. The distribution is highly zero-inflated:

- Training perturbations: 1674.
- Mean: 14.05 DEGs.
- Median: 0 DEGs.
- 75th percentile: 1 DEG.
- 90th percentile: 2 DEGs.
- 95th percentile: 18 DEGs.
- Max: 2677 DEGs.

This makes the difference between 0 and 1 biologically meaningful but also reminds us that `1` commonly means detectable on-target depletion, not a broad expression program.

I then inspected the parquet row-group statistics and read only rows matching `group_name == "151 TH Prkcd Grin2c Glut"` for a respiratory-chain/TCA panel. The focal group has 17,259 measured genes per perturbation. For each comparator I counted genes with `pvals_adj < 0.05` and inspected the leading adjusted p-values to check whether the count reflected a direct target transcript or recurrent secondary markers.

## Sdhb-specific reasoning

### Mechanistic position

`Sdhb` encodes the iron-sulfur protein of succinate dehydrogenase, mitochondrial complex II. Complex II is both a TCA-cycle enzyme, oxidizing succinate to fumarate through the SDHA flavoprotein and SDHB Fe-S relay, and a respiratory-chain enzyme, transferring electrons to ubiquinone through the membrane subunits SDHC and SDHD. This subunit relationship makes `Sdha` the closest visible training analog. Severe SDH loss can accumulate succinate and inhibit HIF-alpha prolyl hydroxylases, causing pseudohypoxia in SDH-deficient tumor settings, and biallelic SDHA/SDHB defects can cause isolated complex-II mitochondrial disease. Those disease mechanisms are real but come from complete or near-complete complex-II loss, not from this assay's mosaic, postnatal partial mRNA depletion.

### Same-complex and pathway comparators

`Sdha` was the only visible `Sdh*` perturbation in the focal training-count CSV; `Sdhc`, `Sdhd`, `Sdhaf1`, and `Sdhaf2` were not available as direct training perturbations. `Sdha` had `n_degs = 1` in `151 TH Prkcd Grin2c Glut`, with 195 perturbed and 23,679 control nuclei. The only FDR 0.05 call was the target itself:

- `Sdha`: log2FC `-0.7809`, q `2.11e-12`.

The next candidate, `Edem2`, was below FDR 0.10 but not the official threshold used here, with q `0.0646`. Canonical stress genes were absent in the same signature: `Asns`, `Chac1`, `Ddit3`, `Slc7a5`, `Mthfd2`, `Lonp1`, `Hif1a`, `Vegfa`, and `Sdhb` all had q `1.0`.

The Distributed Agents corpus independently summarized `Sdha` as a buffered catalytic complex-II perturbation: all measured `Sdha` self-logFC values were negative across groups, but only two exploratory downstream genes crossed FDR 0.10 anywhere; the `151 TH Prkcd Grin2c Glut` hit was `Edem2` and it did not carry ER-UPR, ISR, NRF2, or HIF/pseudohypoxia marker induction. The corpus also noted that represented TCA and respiratory-chain targets did not phenocopy `Sdha`; this is important because it argues against treating a one-gene `Sdha` trace as a reusable mitochondrial-stress module.

Nearest TCA and carbon-entry training perturbations also sat at 0 or 1 official DEG in the focal group:

- `Aco2`: 0
- `Dlat`: 1
- `Dld`: 0
- `Dlst`: 0
- `Idh3a`: 1
- `Mdh2`: 1
- `Mpc1`: 0
- `Ogdh`: 0
- `Pdha1`: 1
- `Sucla2`: 1
- `Suclg1`: 0

Most of these one-DEG cases were self-transcript calls rather than coherent TCA compensation. The cytosolic malate dehydrogenase gene `Mdh1` had a larger focal count, 29, including `Cars`, `Gls`, and `Atp2a2`, but it is an imperfect counterexample: it is not a complex-II subunit, and the curated corpus placed `Mdh1` outside the strong `Opa1`-like ATF4/ISR state. I therefore did not let `Mdh1` override the direct `Sdha` evidence.

### Respiratory-chain and mitochondrial-stress boundary checks

Respiratory-chain structural and assembly perturbations in the same focal group were also mostly flat:

- Complex I examples: `Ndufa10` 1, `Ndufa11` 0, `Ndufa12` 0, `Ndufa4` 1, `Ndufa6` 1, `Ndufa8` 0, `Ndufa9` 0, `Ndufaf2` 0, `Ndufaf4` 0, `Ndufaf5` 0, `Ndufb10` 1, `Ndufb11` 1, `Ndufb3` 0, `Ndufb7` 0, `Ndufb8` 1, `Ndufb9` 1, `Ndufc2` 1, `Ndufs2` 1, `Ndufs4` 0, `Ndufs7` 0, `Ndufs8` 1, `Ndufv1` 0, `Ndufv2` 1.
- Complex III examples: `Uqcrb` 0, `Uqcrc2` 1, `Uqcrfs1` 0, `Uqcrh` 0, `Uqcrq` 1.
- Complex IV examples: `Cox11` 0, `Cox4i1` 0, `Cox5a` 1, `Cox6a1` 0, `Cox7b` 0, `Cox8a` 0.
- Other mitochondrial checks: `Tomm40` 1, `Timmdc1` 0, `Park7` 1.

The closest complex-I analog, `Ndufs2`, had `n_degs = 1` in the focal group, again its own transcript only. In the same-experiment corpus, `Ndufs2` anchored a high-confidence claim that represented nuclear complex-I subunit and assembly-factor perturbations were broadly buffered and failed to produce a shared acute OXPHOS-stress module. This supported interpreting the complex-II near-null not as a special failure of `Sdha` but as a broader property of partial P16 CRISPR hits to single nuclear respiratory-chain subunits.

`Opa1` was the key counterexample showing the assay could detect mitochondrial stress in `151 TH Prkcd Grin2c Glut`: it had `n_degs = 37`, with `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Mthfd2`, `Slc7a5`, and multiple aminoacyl-tRNA synthetases up. However, `Opa1` perturbs inner-membrane fusion and cristae maintenance rather than the succinate dehydrogenase holoenzyme. The corpus explicitly used `Opa1` as a positive benchmark whose ATF4/amino-acid program was absent from `Aco2`, `Ndufs2`, `Sucla2`, `Ndufv1`, and other same-organelle comparators. I therefore used it as a boundary: mitochondrial stress is detectable, but `Sdhb` should stay on the buffered respiratory-chain side unless the SDH lesion is much stronger than `Sdha`.

The pseudohypoxia branch also did not look active in the focal training data. `Sdha` did not alter `Hif1a` or `Vegfa` at FDR 0.05, and direct perturbations of `Hif1a` and `Arnt` each had 0 DEGs in the focal endpoint. That does not disprove succinate accumulation, but it makes a large HIF-driven nuclear response unlikely in this acute postmitotic screen.

### Final call

The evidence for a nonzero call is the very close analogy to `Sdha`: SDHA and SDHB are the two catalytic SDH subunits, both nuclear-encoded and broadly expressed, and loss of either structural subunit can impair complex II. `Sdha` itself was strongly and significantly depleted in the focal group, so a high-expression `Sdhb` target transcript is likely to be detected as an on-target negative DEG.

The evidence against a broad nonzero call is stronger: nearly all visible TCA, complex-I, complex-III, and complex-IV neighbors had 0 or 1 official DEG; `Sdha` lacked HIF, NRF2, UPR, and ATF4 markers in the exact focal group; and same-experiment corpus findings place represented respiratory-chain perturbations in a buffered, nonconvergent class.

I therefore predict one official DEG for `Sdhb`, corresponding to the depleted `Sdhb` transcript itself and no confident secondary program.

Predicted `n_degs`: 1.

## Limits

The closest available training perturbation was `Sdha`; the actual membrane subunits `Sdhc` and `Sdhd` and the SDH assembly factors were not visible, so this is same-complex transfer from one catalytic partner rather than a full complex-II series. The training data also report RNA abundance, not indel rates, SDHB protein, succinate/fumarate, oxygen consumption, ROS, or HIF protein. A true SDH-null neuron could accumulate succinate and trigger stress or pseudohypoxia, but the supplied AAV screen is sparse and partial, with an average target-RNA decrease of only about 18 percent per guide. Finally, because the endpoint includes the target transcript, the difference between a 0 and a 1 prediction depends on gRNA/NMD performance for `Sdhb`; the prediction assumes that `Sdhb` mRNA behaves more like the significantly depleted `Sdha`, `Ndufs2`, `Cox5a`, and `Uqcrc2` targets than like weakly detected subunits such as `Ndufs4` or `Uqcrfs1`.
