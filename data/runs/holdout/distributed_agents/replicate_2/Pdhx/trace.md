# Question and resolved ambiguities

The held-out target for this run is `Pdhx`. I interpreted the requested endpoint as the exact focal-cell count in `151 TH Prkcd Grin2c Glut`: the number of measured mouse genes, including the perturbed target transcript itself, with `pvals_adj < 0.05` after Wilcoxon testing against matched control nuclei.

The main ambiguity was whether the target gene's own mRNA is counted. I treated it as counted because the training count CSV agrees with direct parquet queries in the focal group: `Pdha1`, `Dlat`, `Idh3a`, `Mdh2`, `Sdha`, `Sucla2`, `Got1`, `Got2`, `Slc25a12`, `Slc25a4`, and `Slc25a46` each had exactly one FDR 0.05 row and, in each of those cases, the one row was the targeted transcript itself.

# Sources used

- Input manifest: `172_Pdhx.csv`, which contains only `Pdhx`.
- Input training endpoint: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Input differential-expression parquet: `training_de_all_cell_groups.parquet`.
- Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`:
  - `target_context` for `Pdha1`, `Dlat`, `Dld`, and `Mpc1`.
  - `candidate_set_topology` for the PDC / mitochondrial-carbon cohort `Aco2`, `Dlat`, `Dld`, `Dlst`, `Idh3a`, `Mdh2`, `Mpc1`, `Ogdh`, `Pdha1`, `Sdha`.
- Distributed Agents runtime profile analysis:
  - `profile_compare` over the same focal-cell `logfoldchanges` for `Pdha1`, `Dlat`, `Dld`, `Mpc1`, `Dlst`, `Ogdh`, `Aco2`, `Idh3a`, `Mdh2`, and `Sdha`.
  - `profile_inspect` on the direct PDC and pyruvate-entry nodes.
- External literature from PubMed:
  - Brown et al. 2002, DOI `10.1007/s00439-001-0665-3`, PMID `11935326`.
  - Brown et al. 2006, DOI `10.1017/S0012162206001617`, PMID `16904023`.
  - Gopalakrishnan et al. 1989, DOI `10.1016/0006-291x(89)92492-3`, PMID `2719694`.
  - Hiromasa et al. 2003, DOI `10.1074/jbc.M308172200`, PMID `14638692`.
  - Ciszak et al. 2005, DOI `10.1074/jbc.M507850200`, PMID `16263718`.
  - Brautigam et al. 2006, DOI `10.1016/j.str.2006.01.001`, PMID `16442803`.
  - Park and Patel 2010, DOI `10.1016/j.bbrc.2010.04.038`, PMID `20385101`.

# Dataset computations

I first checked the training-count distribution for the focal class. It is extremely zero-inflated: 1205 of 1674 training perturbations are exactly zero, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only a small tail reaches hundreds to thousands of genes. That distribution made a broad response for `Pdhx` implausible unless direct PDC or adjacent mitochondrial targets had shown one.

I then queried the parquet for rows satisfying

```python
(group_name == "151 TH Prkcd Grin2c Glut")
& gene_target.isin([
    "Pdha1", "Dlat", "Dld", "Mpc1", "Dlst", "Ogdh", "Aco2",
    "Idh3a", "Mdh2", "Sdha", "Sucla2", "Suclg1", "Bckdhb",
    "Bckdk", "Got1", "Got2", "Mdh1", "Slc25a12", "Slc25a13",
    "Slc25a4", "Slc25a46", "Ndufs4"
])
```

This read 379,698 focal rows for 22 comparator perturbations. The core table was:

| training target | focal `n_degs` | FDR 0.05 interpretation |
|---|---:|---|
| `Pdha1` | 1 | self-transcript only, log2FC -1.039, q=1.31e-6 |
| `Dlat` | 1 | self-transcript only, log2FC -0.673, q=2.81e-7; `Jarid2` was close at q=0.0577 but is not in this endpoint |
| `Dld` | 0 | no FDR 0.05 row; self log2FC -0.397, q=1 |
| `Mpc1` | 0 | no FDR 0.05 row; self log2FC -0.209, q=1 |
| `Dlst` | 0 | no FDR 0.05 row |
| `Ogdh` | 0 | no FDR 0.05 row |
| `Aco2` | 0 | no FDR 0.05 row |
| `Idh3a` | 1 | self-transcript only |
| `Mdh2` | 1 | self-transcript only |
| `Sdha` | 1 | self-transcript only |
| `Sucla2` | 1 | self-transcript only |
| `Suclg1` | 0 | no FDR 0.05 row |
| `Bckdhb` | 0 | no FDR 0.05 row |
| `Bckdk` | 0 | no FDR 0.05 row |
| `Ndufs4` | 0 | no FDR 0.05 row |

I also checked canonical mitochondrial-stress and pyruvate-response markers in the same comparator rows: `Atf4`, `Atf5`, `Ddit3`, `Trib3`, `Asns`, `Hspa5`, `Hspa9`, `Hspd1`, `Hspe1`, `Clpp`, `Lonp1`, `Hmox1`, `Nqo1`, `Gclc`, `Gclm`, `Txnrd1`, `Prdx5`, `Ldha`, `Slc16a1`, and `Pdk1`-`Pdk4`. None passed FDR 0.05 for `Pdha1`, `Dlat`, `Dld`, `Mpc1`, `Dlst`, `Ogdh`, `Aco2`, `Sdha`, `Mdh2`, `Sucla2`, or `Suclg1`. The Distributed Agents runtime comparison of 17,259 shared focal features also found that `Pdha1` and `Dlat` each had one significant negative feature and `Dld`, `Mpc1`, and `Ogdh` had no significant feature; significant-gene intersections between these nodes and the TCA peers were zero.

# Target-specific reasoning

## `Pdhx`

`Pdhx` encodes the mammalian pyruvate dehydrogenase complex E3-binding protein, historically protein X/E3BP. Biochemically this places it inside PDC rather than merely next to it: mammalian PDC has E1, E2/DLAT, E3/DLD, and E3BP/PDHX, with E3BP helping build the E2/E3BP core and recruit the E3 homodimer. E3BP loss or disruption causes bona fide PDC deficiency in patients, and structural work shows that the E3BP binding domain directly docks onto DLD/E3. Those facts made the direct PDC targets, not the broader TCA or respiratory-chain tail, the primary comparators.

The best measured analogs were:

- `Dlat`: same PDC core neighborhood, 1 DEG in the focal group, and that DEG was `Dlat` itself. The near-downstream candidate `Jarid2` missed the requested FDR 0.05 threshold at q=0.0577. The Distributed Agents corpus reports that `Dlat` had a narrowly 151-biased FDR 0.10 `Jarid2` signal but that PDC/carbon comparators did not phenocopy it.
- `Pdha1`: PDC E1alpha catalytic subunit, 1 DEG in the focal group, `Pdha1` itself. Distributed Agents corpus finding `Pdha1:F004` states that measured PDC comparators `Dlat`, `Dld`, and `Mpc1`, plus related TCA comparators `Dlst`, `Ogdh`, `Sdha`, and `Idh3a`, were flat or nearly flat and did not form a shared postmitotic neuronal PDH module.
- `Dld`: E3 subunit recruited by PDHX, but also reused by alpha-ketoglutarate dehydrogenase and branched-chain ketoacid dehydrogenase. It had 0 focal DEGs. Its self-transcript moved only to q=1, and the Distributed Agents corpus describes a downstream-null DLD surface with absent ISR, UPRmt, ER-stress, and antioxidant transcripts.
- `Mpc1`: immediately upstream pyruvate carrier, 0 focal DEGs. The corpus specifically links the missing `Mpc1` response with absent or near-absent `Pdha1`, `Dlat`, and `Dld` responses, placing basal pyruvate-entry stress largely off the nuclear snRNA axis in this screen.

The broader counterexamples were also sparse in the focal class: `Aco2`, `Dlst`, `Ogdh`, `Suclg1`, `Bckdhb`, `Bckdk`, and `Ndufs4` all had 0 FDR 0.05 genes, while `Idh3a`, `Mdh2`, `Sdha`, and `Sucla2` each had only self-transcript hits. `Mdh1` was the one stronger nearby-carbon outlier at 29 DEGs, but it is cytosolic malate dehydrogenase / malate-aspartate shuttle biology rather than the PDC core, so I treated it as proof that this thalamic group can respond to a metabolic target, not as a direct estimate for `Pdhx`.

I therefore split the endpoint into two components:

- Downstream genes: predicted 0. This is driven mostly by within-dataset evidence. PDC, DLD-axis, pyruvate-carrier, and TCA perturbations did not produce a reproducible focal stress module, did not induce ATF4/DDIT3/ASNS, UPR, mitochondrial chaperone, antioxidant, lactate/pyruvate, or PDK transcripts, and did not share FDR 0.05 genes across the Distributed Agents profile comparison.
- Self-transcript: predicted 1. This is a less certain extrapolation from `Pdha1`, `Dlat`, `Idh3a`, `Sdha`, and other mitochondrial enzymes whose only focal DEG was the guide-targeted mRNA. `Pdhx` is an expressed core mitochondrial PDC transcript, and the closest structural PDC analogs that were recovered in training gave single self-DEG counts rather than downstream zeros.

Final point prediction: `1`.

# Limits

The strongest claim is the downstream null; the weakest part is the self-transcript call. The CRISPR assay did not measure indels, PDHX protein, lipoic-acid occupancy, PDH flux, pyruvate/lactate, acetyl-CoA, ATP, mitochondrial ultrastructure, or electrophysiology, so a predicted 0 downstream DEGs is not a prediction of no biochemical phenotype. Conversely, a true `Pdhx` self mRNA drop could fail FDR because target transcript detectability varies sharply across genes and guide sets: nearby targets such as `Dld`, `Mpc1`, `Dlst`, and `Ogdh` had negative self log2FCs but no FDR 0.05 self row. `Pdhb`, the PDKs, PDPs, and `Mpc2` were not available training perturbations, so the exact PDC subunit/regulator neighborhood is incomplete. Finally, all same-experiment evidence is from basal postnatal sparse AAV CRISPR in NeuN+ nuclei; germline PDH deficiency, severe cell-autonomous enzyme ablation, or non-neuronal stress models would be expected to have much larger metabolic consequences than this endpoint reports.
