# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question interpreted

The held-out target for this run is:

```text
Guk1
```

I interpreted the endpoint as the exact focal-cell count of measured genes with
`pvals_adj < 0.05` after acute AAV-CRISPR loss of `Guk1`, including the
target transcript itself if it would have crossed that threshold. `Guk1` was not
present as a `gene_target` in the supplied differential-expression parquet and
was absent from the focal training-count CSV, so the estimate must be transferred
from non-held-out perturbations and from external biology.

## Sources

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact observed
  `n_degs` for 1,674 non-held-out perturbations in the focal cell group.
- `training_de_all_cell_groups.parquet`: focal-cell Wilcoxon signatures for
  mechanistic comparator perturbations. I used only rows with
  `group_name == "151 TH Prkcd Grin2c Glut"` for the final calibration.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`: target-centric findings for
  observed perturbations including `Opa1`, `Sucla2`, `Suclg1`, `Slc25a4`, and
  `Nt5c2`. The corpus had no direct `Guk1` context.
- PubMed literature for GUK1 biology:
  - Brady et al. 1996, JBC, PMID:8663313, DOI:10.1074/jbc.271.28.16734.
    Cloned mouse and human guanylate kinase; mammalian GUK1 is a conserved,
    broadly expressed enzyme catalyzing GMP/dGMP phosphorylation to GDP/dGDP.
  - Stolworthy and Black 2001, Protein Engineering, PMID:11742110,
    DOI:10.1093/protein/14.11.903. Demonstrated the mouse enzyme's GMP/dGMP
    kinase activity and the substrate-binding logic of mammalian GUK1.
  - Hidalgo-Gutierrez et al. 2024, Annals of Neurology, PMID:39230499,
    DOI:10.1002/ana.27071. Identified biallelic human GUK1 deficiency as an
    mtDNA depletion/deletions syndrome and showed that short and long GUK1
    isoforms support cytosolic and intramitochondrial nucleotide pools.
  - Lecoq et al. 2000, Genetics, PMID:11063676,
    DOI:10.1093/genetics/156.3.953. Yeast `guk1` alleles deplete GMP kinase
    activity and secondarily deregulate purine biosynthesis genes, supporting
    the expectation that severe loss of GUK1 can perturb guanine-purine pools.
  - Franchino et al. 2024, Brain, PMID:37804316,
    DOI:10.1093/brain/awad340. Provides an external mechanistic anchor for the
    OMA1-DELE1-HRI/eIF2alpha-ATF4 mitochondrial stress axis used to interpret
    the screen-internal `Opa1` positive response.

## Computation over the supplied data

1. Read the held-out manifest and found exactly one requested target, `Guk1`.
2. Summarized the focal training counts. The response distribution is sparse:
   1,205 of 1,674 observed perturbations have `n_degs = 0`; the median is 0,
   the 75th percentile is 1, 469 perturbations are nonzero, and only the long
   tail reaches hundreds to thousands of DEGs.
3. Queried the focal rows of the parquet for mechanistically related observed
   perturbations and the ATF4/ISR, one-carbon, mitochondrial-encoded, and target
   sentinel genes. There are 17,259 measured features per target in this focal
   group.
4. Ran `profile_compare`/`profile_inspect` from the Distributed Agents runtime over
   candidate observed signatures:
   `Adk`, `Nt5c2`, `Sucla2`, `Suclg1`, `Slc25a4`, `Slc25a36`, `Opa1`, `Mdh1`,
   `Dlat`, `Idh3a`, `Mdh2`, `Pdha1`, `Ndufs2`, `Ndufa4`, `Isca2`, `Sod2`,
   and `Nrf1`. I used the runtime profile counts and FDR-level feature
   intersections; I did not interpret high whole-vector correlations between
   nearly flat signatures as evidence of mechanism.

Key focal counts from the direct queries were:

| comparator | observed `n_degs` | interpretation for `Guk1` |
| --- | ---: | --- |
| `Adk` | 0 | Single purine/adenosine enzyme, flat in the same focal cell group. |
| `Nt5c2` | 0 | Cytosolic IMP/GMP 5'-nucleotidase, flat in the same focal group. |
| `Slc25a4` | 1 | Mitochondrial nucleotide carrier, self-transcript only. |
| `Slc25a36` | 0 | Mitochondrial pyrimidine nucleotide carrier family member, flat. |
| `Sucla2` | 1 | mtDNA-depletion-linked SUCL subunit, self-transcript only. |
| `Suclg1` | 0 | Same succinyl-CoA ligase complex, flat. |
| `Aco2`, `Dld`, `Dlst`, `Mpc1`, `Ogdh`, `Ndufs4`, `Mff`, `Coa8`, `Gfm2` | 0 each | Mitochondrial metabolism/OXPHOS comparators, flat. |
| `Dlat`, `Idh3a`, `Mdh2`, `Pdha1`, `Ndufs2`, `Ndufa4`, `Isca2`, `Sod2`, `Sdha` | 1 each | Mostly significant self-transcript depletion only. |
| `Mdh1` | 29 | Small but real TH-specific metabolic response, not a guanine-nucleotide module. |
| `Opa1` | 37 | Positive mitochondrial ISR-like benchmark in this same cell group. |
| `Nrf1` | 138 | Positive mitochondrial-regulatory benchmark, broader than direct metabolic enzymes. |

The sentinel-gene check sharpened the comparison. `Opa1` induced clear
ATF4/ISR-like genes in the focal cell group, including `Asns`, `Chac1`,
`Ddit3`, `Mars1`, `Cars`, `Mthfd2`, and `Slc7a5`, and down-regulated
`mt-Co2`. In contrast, `Adk`, `Dlat`, `Idh3a`, `Isca2`, `Mdh2`, `Ndufa4`,
and `Ndufs2` had FDR = 1.0 for `Asns`, `Chac1`, `Ddit3`, `Mthfd2`, `Shmt2`,
`Slc7a5`, `Fgf21`, `Gdf15`, and the queried mitochondrial transcripts, with
only their own target transcript crossing in most of the one-DEG cases. In the
profile inspection there was also no significant-feature intersection between
`Opa1` and the flat purine or SUCL/SLC25 candidates.

## Target-specific reasoning

### `Guk1`

`Guk1` encodes guanylate kinase, the monophosphate kinase that phosphorylates
GMP and dGMP to GDP and dGDP. Severe loss can disturb guanine pools: yeast
`guk1` mutants deregulate purine synthesis genes, and human GUK1 deficiency
causes a mitochondrial DNA depletion/deletion syndrome through unbalanced dGTP
availability. That external biology makes a nucleotide-pool or secondary
mitochondrial response conceivable.

The screen-internal analogs argue that such a secondary state should be weak in
this focal assay. The most direct represented purine enzymes, `Adk` and
`Nt5c2`, had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`; Distributed Agents corpus
findings for `Nt5c2` also report absence of broad purine, AMPK/mTOR/ISR/p53
programs and non-convergence with `Adk`. Mitochondrial nucleotide and
mtDNA-depletion-adjacent candidates were similarly small: `Slc25a4 = 1`,
`Slc25a36 = 0`, `Sucla2 = 1`, and `Suclg1 = 0` in the focal group. The
Distributed Agents `Sucla2` and `Suclg1` findings explicitly found no coherent shared
ATF4, UPRmt, OXPHOS, mitophagy, or mtDNA-depletion-like transcriptomic stress
program after acute sparse perturbation of represented single mitochondrial
metabolic nodes. That is a much closer calibration point than the broad
`Opa1` and `Nrf1` positive controls, which show that this cell group can mount
mitochondrial-regulatory transcription but only for particular upstream insults.

I therefore predict no multi-gene downstream transcriptional response. I set
the point estimate just above zero, at `1`, because several highly expressed
single metabolic enzymes in the same neighborhood crossed the focal FDR cutoff
only by depletion of their own mRNA (`Slc25a4`, `Sucla2`, `Dlat`, `Idh3a`,
`Mdh2`, `Ndufs2`, `Ndufa4`, `Isca2`, and `Sod2` each had a one-gene focal
surface), and a direct `Guk1` self-transcript call is more plausible than a
full Opa1-like ISR state.

## Limits

- `Guk1` itself was completely held out and absent from the Distributed Agents
  same-experiment corpus, so no empirical Guk1 signature, guide count, or
  self-depletion value was available.
- The observed perturbation set lacks the closest de novo guanine-pathway
  enzymes such as `Gmps`, `Impdh1`, `Impdh2`, and `Hprt`, so `Adk` and
  `Nt5c2` are purine-neighborhood proxies rather than same-reaction controls.
- Human GUK1 deficiency and yeast `guk1` mutants are severe systemic or
  organismal contexts. They establish pathway direction, but they overstate the
  likely impact of an acute, mosaic, partially edited postnatal neuronal CRISPR
  perturbation.
- A prediction of `1` rests on an expected self-transcript effect. The direct
  downstream biology points to zero, and if the four `Guk1` guides did not
  reduce nuclear `Guk1` mRNA strongly enough in this cell group, the measured
  count would instead be `0`.
