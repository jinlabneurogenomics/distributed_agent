# Question

Predict `n_degs` for each perturbation in `204_Sdhb.csv` in the focal cell group
`151 TH Prkcd Grin2c Glut`. The manifest has one held-out target:

| target_name |
| --- |
| Sdhb |

I treated `n_degs` exactly as defined in the task: the number of measured genes,
including the targeted transcript itself if it is measured, with
`pvals_adj < 0.05` from the Wilcoxon differential-expression table for
perturbed versus matched control nuclei in the focal group. `Sdhb` itself was
held out as a perturbation, so neither its own focal signature nor its observed
count is present in the input. `Sdhb` is still present as a measured transcript
in other perturbation profiles, which only establishes that the transcript is
assayed.

# Sources

- Required local inputs:
  - `[local file: training_de_all_cell_groups.parquet]`
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: 204_Sdhb.csv]`
- Same-experiment internal corpus: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the `Sdha`,
  `Ogdh`, `Ndufb11`, and respiratory-chain/TCA cross-perturbation findings.
- Run-local profile tools over the parquet:
  - `profile_neighbors` anchored on observed `Sdha`
  - `profile_compare` for a 16-node mitochondrial comparator cohort in the
    exact `151 TH Prkcd Grin2c Glut` context
- External mechanism literature:
  - Ackrell 2002, `10.1016/s0098-2997(02)00012-2`, PMID 12231007:
    complex II/succinate dehydrogenase is a four-subunit, nuclear-encoded
    enzyme that links the TCA cycle to the respiratory chain; SDHA is the
    flavoprotein and SDHB carries the iron-sulfur relay to the ubiquinone
    membrane module.
  - Bardella, Pollard, and Tomlinson 2011,
    `10.1016/j.bbabio.2011.07.003`, PMID 21771581: SDHA-D loss-of-function
    mutations abolish SDH function and can act through oncometabolite
    accumulation in SDH-deficient tumors.
  - Selak et al. 2005, `10.1016/j.ccr.2004.11.022`, PMID 15652751:
    succinate accumulation after SDH inhibition can inhibit HIF-alpha prolyl
    hydroxylases and stabilize HIF-1alpha.
  - MacKenzie et al. 2007, `10.1128/MCB.01927-06`, PMID 17325041:
    alpha-ketoglutarate derivatives can reverse succinate- or
    fumarate-mediated inhibition of HIF-alpha prolyl hydroxylases in
    SDH/FH-deficient cells, supporting the metabolite competition mechanism.
  - Zhou et al. 2022, `10.1016/j.arr.2022.101702`, PMID 35908669:
    mammalian mitochondrial stress/UPRmt signaling commonly engages
    eIF2alpha-ATF4-CHOP/ATF5 transcriptional programs.

# Local computations

I first read the focal DEG-count CSV and compared `Sdhb` with observed
mitochondrial subunits, assembly factors, and adjacent metabolic enzymes. I then
queried the parquet only for `group_name == "151 TH Prkcd Grin2c Glut"` and a
small set of comparator `gene_target` values, retaining genes with
`pvals_adj < 0.05`, so the evidence below is in the same cell group and uses the
same FDR threshold as the requested endpoint.

The exact SDH training coverage was sparse: among targets beginning with
`Sdh`, only `Sdha` was in the training count file. Same-complex `Sdhb`, `Sdhc`,
`Sdhd`, and SDH assembly factors were not visible as perturbations, so the
closest direct comparator is the catalytic complex-II partner `Sdha`.

The local comparator counts were:

| Comparator set in `151 TH Prkcd Grin2c Glut` | Observed counts and focal expression evidence |
| --- | --- |
| `Sdha` | `n_degs = 1`; the only focal FDR<0.05 row among the queried DEGs was `Sdha` itself, log2FC `-0.780939`, BH FDR `2.11e-12`. |
| Complex I structural/assembly genes | Mostly zero or one: `Ndufa10 1`, `Ndufa11 0`, `Ndufa12 0`, `Ndufa4 1`, `Ndufa6 1`, `Ndufa8 0`, `Ndufa9 0`, `Ndufaf2 0`, `Ndufaf4 0`, `Ndufaf5 0`, `Ndufb10 1`, `Ndufb11 1`, `Ndufb3 0`, `Ndufb7 0`, `Ndufb8 1`, `Ndufb9 1`, `Ndufc2 1`, `Ndufs2 1`, `Ndufs4 0`, `Ndufs7 0`, `Ndufs8 1`, `Ndufv1 0`, `Ndufv2 1`. In the focal FDR rows, several one-count cases were target self-knockdown only, including `Ndufa10`, `Ndufa6`, `Ndufb10`, `Ndufb11`, and `Ndufc2`. |
| Complex III and IV comparators | `Uqcrc2 1`, `Uqcrq 1`, `Uqcrb 0`, `Uqcrfs1 0`, `Uqcrh 0`; `Cox5a 1`, `Coa8 0`, `Cox11 0`, `Cox4i1 0`, `Cox6a1 0`, `Cox7b 0`, `Cox8a 0`. `Cox5a` and `Uqcrc2` were self-only one-DEG responses. |
| TCA, pyruvate-entry, PDC, and Fe-S neighbors | `Aco2 0`, `Bckdhb 0`, `Bckdk 0`, `Dlat 1`, `Dld 0`, `Dlst 0`, `Idh3a 1`, `Isca2 1`, `Mdh2 1`, `Mpc1 0`, `Nfs1 0`, `Ogdh 0`, `Pdha1 1`, `Sucla2 1`, `Suclg1 0`. The focal FDR rows for `Dlat`, `Idh3a`, `Mdh2`, `Pdha1`, and `Sucla2` were self-knockdown only. |
| Mitochondrial counterexamples | `Mdh1` had `29` focal DEGs, including `Mdh1`, `Cars`, `Gls`, and synaptic/neural transcripts such as `Grin2b` and `Nrxn1`. `Opa1` had `37` focal DEGs, including the ISR/amino-acid-stress genes `Asns`, `Chac1`, `Ddit3`, `Slc7a5`, and `Mthfd2`, plus `mt-Co2` down-regulation. |

I also compared signed focal log2FC profiles within a 16-node cohort:
`Sdha`, `Ndufb11`, `Ogdh`, `Dld`, `Idh3a`, `Mdh1`, `Opa1`, `Cox5a`,
`Uqcrc2`, `Uqcrq`, `Ndufa10`, `Ndufa6`, `Ndufb10`, `Ndufc2`, `Mpc1`, and
`Aco2`. This was mainly a sanity check against borrowing a non-SDH stress
module. `Sdha` and `Ndufb11` were in the `1_to_9_significant_features` activity
class with one focal DEG each, `Ogdh` and `Dld` were in the
`no_significant_features` class, and `Mdh1` and `Opa1` were in the
`10_to_49_significant_features` class. Pairwise focal correlations among flat
profiles were dominated by shared near-zero genes and had no FDR-level
downstream gene intersections, so I used them only as evidence of broad
buffering, not as evidence for a shared named marker module.

# Same-experiment corpus evidence

The Distributed Agents corpus had no `Sdhb` target entry, consistent with complete
holdout. It did have several directly relevant same-experiment findings:

- `Sdha:F001-F006`: `Sdha` produced a broadly buffered neuronal RNA response.
  Across all 23 measured neuronal groups it had only two FDR<0.10 downstream
  genes, and in `151 TH Prkcd Grin2c Glut` the signal was a single `Sdha`
  self-knockdown at FDR<0.05. The corpus specifically reported no HIF/
  pseudohypoxia, NRF2/redox, UPR, or mitochondrial ISR module and noted that
  represented TCA and respiratory-chain targets did not phenocopy the isolated
  `Sdha` rows.
- `Cox8a:F004` and the high-confidence complex-I/complex-IV claims:
  represented `Cox`, `Nduf`, `Ndufaf`, `Uqcr`, `Sdha`, `Coa8`, and `Lrpprc`
  perturbations were dataset-wide sparse, arguing that acute perturbation of a
  nuclear OXPHOS subunit in recovered juvenile neurons rarely becomes a broad
  nuclear stress program.
- `Ndufb11:F001-F005`: complex-I structural perturbation was almost flat,
  with a single non-focal downstream hit across 22 groups and no ATF4/ISR
  marker induction. The observed `151 TH Prkcd Grin2c Glut` count was again a
  one-gene self-transcript row.
- `Ogdh:F001-F006` and corpus claim
  `claim:5e92ede610df7967282e`: represented mitochondrial carbon-entry, PDC,
  DLD-linked, TCA, Fe-S, and adjacent metabolic targets generally failed to
  induce a coherent postmitotic neuronal nuclear DE module, although narrow
  target-specific singleton effects occurred.

# Target-specific reasoning for Sdhb

`Sdhb` encodes the iron-sulfur subunit of mitochondrial complex II. Complete
loss of SDH activity should affect both succinate oxidation in the TCA cycle and
electron transfer to ubiquinone; severe SDH loss can accumulate succinate,
inhibit prolyl hydroxylases, and stabilize HIF-alpha in SDH-deficient tumor or
cell-culture settings. Those external facts make `Sdhb` biologically closer to
`Sdha` than to complex I/III/IV subunits and raise plausible downstream routes
through pseudohypoxia, redox stress, or mitochondrial ISR/UPRmt.

The observed acute neuronal data argue that those routes usually did not cross
the RNA-DE threshold in this assay:

- The exact complex-II catalytic partner `Sdha` had `n_degs = 1` in the focal
  group, and that DEG was `Sdha` itself. The Distributed Agents `Sdha` findings also
  rejected a broad HIF, NRF2, UPR, or ATF4/ISR state across the measured
  neuronal groups.
- Other ETC genes were almost exclusively zero or self-only one-count
  perturbations in the same focal group, even when their own transcripts were
  significantly depleted.
- TCA, PDC, Fe-S, and carbon-entry perturbations adjacent to the succinate node
  were also zero or one DEG in `151 TH Prkcd Grin2c Glut`; `Ogdh` and `Dld`
  were complete zeroes there.
- `Opa1` and `Mdh1` show that a mitochondrial perturbation can give dozens of
  DEGs in this exact cell type when a stress or amino-acid response is engaged,
  so the low `Sdha`/ETC/TCA counts are not explained by a universal lack of
  statistical power in `151 TH Prkcd Grin2c Glut`.

I therefore predicted a nonzero but minimal effect. The nonzero call is driven
by the likelihood that `Sdhb` is detected as a measured transcript and will be
reduced by its own CRISPR guides, analogous to `Sdha`, `Cox5a`, `Ndufa10`,
`Ndufa6`, `Ndufb10`, `Ndufb11`, `Ndufc2`, `Dlat`, `Idh3a`, `Mdh2`, `Pdha1`,
and `Sucla2`. I did not add extra downstream DEGs because the best available
same-complex and pathway evidence says acute SDH/OXPHOS perturbation was
buffered at the postnatal neuronal nuclear-RNA level.

Final prediction: `Sdhb -> 1`.

# Limits

- No SDHB/C/D or SDH assembly-factor perturbation was present in training; the
  exact same-complex prior comes from `Sdha` alone.
- The DE endpoint includes the targeted transcript. A prediction of `1` is
  therefore mostly a self-knockdown prediction, not a claim that one
  non-target downstream gene will reproducibly move after `Sdhb` loss.
- The experiment measured RNA in recovered nuclei 3-4 weeks after sparse AAV
  CRISPR, not SDH enzyme activity, succinate/fumarate levels, membrane
  potential, ROS, or cell survival. A flat RNA surface could reflect buffering,
  incomplete functional protein loss, selective loss of highly perturbed cells,
  or a metabolic phenotype below the DE threshold.
- External SDH-null tumor and siRNA/overexpression systems are much more severe
  and often proliferative; they justify looking for HIF and stress routes but
  are not direct quantitative priors for this postmitotic neuronal assay.
