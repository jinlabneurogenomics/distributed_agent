# Glmn held-out DEG-count prediction

## Question and resolution

The requested held-out perturbation list contains one target:

| target_name |
|---|
| Glmn |

I interpreted the endpoint as the integer number of measured genes with
`pvals_adj < 0.05` for a `Glmn` CRISPR loss-of-function perturbation in
`151 TH Prkcd Grin2c Glut` neurons. `Glmn` itself was absent from both the
training DE parquet as a `gene_target` and the focal training-count CSV, so I
did not use any `Glmn` expression signature or held-out count.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene Wilcoxon DE rows for
  held-in perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs`
  for the focal cell group.
- `092_Glmn.csv`: the ordered held-out target manifest.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`: I queried `Glmn`,
  `Fbxw7`, `Fbxo11`, `Mtor`, `Tek`, and `Tsc2`. `Glmn` had no direct
  corpus node in this filtered release; the other targets supplied
  same-assay findings used as mechanistic anchors or counterexamples.
- Distributed Agents runtime `profile_neighbors`: I compared the held-in focal
  expression profiles of `Fbxw7`, `Fbxo11`, `Mtor`, and `Tek` against the
  1,674 eligible focal profiles as a check for hidden strong expression
  neighborhoods.
- External literature from PubMed:
  - Brouillard et al. 2002, *American Journal of Human Genetics*,
    DOI 10.1086/339492, PMID 11845407. Identified loss-of-function
    glomulin mutations as the cause of glomuvenous malformations and
    framed the phenotype around cutaneous venous lesions with abnormal
    vascular smooth-muscle-like glomus cells.
  - Tron et al. 2012, *Molecular Cell*, DOI
    10.1016/j.molcel.2012.02.005, PMID 22405651. Showed that GLMN binds
    RBX1, inhibits RBX1 E3 activity, modulates CRL1/SCF(FBW7), and that
    GLMN loss lowers FBW7 while increasing Cyclin E and c-Myc.
  - Duda et al. 2012, *Molecular Cell*, DOI
    10.1016/j.molcel.2012.05.044, PMID 22748924. Solved the
    GLMN-RBX1-CUL1 structure and showed that GLMN masks the E2-binding
    surface of RBX1 to inhibit RBX1-containing cullin-RING ligases.

## Computation over the training data

The focal-count CSV has 1,674 held-in targets. It is sparse:

| focal `n_degs` bin | number of held-in targets |
|---|---:|
| 0 | 1205 |
| 1 | 276 |
| 2 | 31 |
| 3-9 | 56 |
| >=10 | 106 |
| >=100 | 43 |

The median is 0, the mean is 14.1, and the maximum is 2,677. This matters
because the most likely response for a target without a known broad neuronal
transcriptional program is zero or a singleton.

To avoid scanning the full 616,253,184-row parquet, I read the Parquet
metadata and found that `151 TH Prkcd Grin2c Glut` is concentrated in row
groups 546 through 580. I then read only the `gene_target` column from those
row groups, materialized full columns only when a selected analog appeared,
and filtered to `group_name == "151 TH Prkcd Grin2c Glut"`. The key operation
was:

```python
gt = pf.read_row_group(i, columns=["gene_target"])["gene_target"]
present = [x for x in targets if pc.any(pc.equal(gt, x)).as_py()]
tbl = pf.read_row_group(i, columns=cols)
mask = pc.and_(
    pc.equal(tbl["group_name"], "151 TH Prkcd Grin2c Glut"),
    pc.is_in(tbl["gene_target"], value_set=pa.array(present)),
)
```

The focal rows for the nearest mechanistic anchors showed:

| training target | why compared with Glmn | focal n_degs | FDR<0.05 genes in focal group |
|---|---|---:|---|
| Fbxw7 | GLMN directly regulates the RBX1/CUL1 SCF(FBW7) ligase axis | 1 | `Trp53inp2` up |
| Fbxo11 | another held-in F-box substrate receptor in an SCF/CRL context | 1 | `Ppib` down |
| Mtor | weak indirect comparator through FBW7/mTOR/SREBP biology | 2 | `Rims3` up, `Tmed8` down |
| Tek | vascular-malformation receptor comparator; useful as an off-lineage counterexample | 0 | none |
| Tsc2 | upstream mTORC1 brake; tests whether this cell group can mount mTORC1/SREBP responses | 86 | sterol, PI3K feedback, neuronal genes |
| Marchf6 | ER ubiquitin ligase with a sterol-feedback program | 14 | `Insig1`, `Dhcr24`, `Cyp51`, `Marchf6`, `Msmo1`, etc. |
| Psmb4 | core proteasome-subunit stress counterexample | 742 | broad proteostasis/synaptic signature |
| Psmc1 | proteasome ATPase counterexample | 430 | broad proteostasis/synaptic signature |
| Uba5 | UFMylation/proteostasis stress counterexample | 2677 | extremely broad response |
| Atg5 | autophagy counterexample | 0 | none |

Other pathway counts in the focal training file supported the same boundary:
`Rptor` 0, `Pik3r1` 0, `Pik3r2` 0, `Pik3cb` 0, `Akt3` 0, `Fkbp1a` 1,
`Srebf2` 7, `Depdc5` 13, `Mib1` 27, `Sqstm1` 1, `Becn1` 0, and `Nfe2l1` 0.

The runtime profile-neighbor artifact for `Fbxw7`, `Fbxo11`, `Mtor`, and
`Tek` reproduced the same focal significant-feature counts: 1, 1, 2, and 0.
The whole-profile nearest-neighbor lists were driven by low-level,
non-significant tails with many adjusted p-values equal to 1, so I used them
only as a check that these anchors were not hiding a coherent broad module.

## Target-specific reasoning

### Glmn

GLMN is a biochemical inhibitor of RBX1-containing cullin-RING ligases rather
than a core proteasome subunit. Duda et al. showed that GLMN binds the
E2-facing surface of RBX1 in a GLMN-RBX1-CUL1 complex, and Tron et al. showed
that the disease protein regulates CRL1(SCF-FBW7) activity and FBW7 turnover.
Therefore the closest represented training target is `Fbxw7`, not
`Psmb4`, `Psmc1`, or `Uba5`. `Fbxw7` produced exactly one focal DEG,
`Trp53inp2`; the Distributed Agents `Fbxw7` findings also reported no canonical MYC,
cyclin-E, Notch, mTOR/SREBP, or NFE2L1 program after acute postnatal Fbxw7
loss. That argues that losing a glomulin-controlled SCF substrate receptor is
almost transcriptionally silent in this cell class.

`Fbxo11` is a second informative F-box/SCF receptor. It also produced exactly
one focal DEG, `Ppib`, and the same-experiment corpus explicitly contrasted it
with `Fbxw7`, `Fbxo38`, p53, TGF/SMAD, and Snail-axis targets without a shared
FDR-supported program. This makes a one-gene idiosyncratic response more
plausible than a multi-gene F-box family state.

The mTOR/TIE2/vascular side of GLMN biology did not support a larger count.
The vascular phenotype described by Brouillard et al. is in cutaneous
venous/smooth-muscle lesions, while this experiment assayed NeuN-enriched
postmitotic neuronal nuclei. Consistently, the held-in vascular-malformation
receptor `Tek` had 0 DEGs in the focal group and was flat across neuronal
groups in the Distributed Agents corpus; endothelial relatives such as `Kdr`, `Flt4`,
and `Ephb4` were also non-phenocopying there. On the growth-control side,
loss of the direct kinase `Mtor` was only 2 DEGs in the focal training counts,
and upstream or same-complex nodes `Akt3`, `Pik3r1`, `Pik3r2`, `Pik3cb`,
and `Rptor` were all 0. `Tsc2` was a real 86-DEG positive counterexample, but
that is an on-axis loss of a strong mTORC1 brake and not a good amplitude
match for partial loss of a CRL inhibitor.

I therefore predict that `Glmn` is more likely just above the FDR threshold
than broadly active: RBX1/SCF biology gives it a better chance than an
unrelated silent vascular receptor, but all held-in direct analogs are at the
one- or two-gene edge. The point estimate is 1 DEG.

## Limits and extrapolations

The largest gap is that the training universe did not include the closest
biochemical core CRL nodes such as `Rbx1`, `Cul1`, `Skp1`, `Nedd8`, or the
CDC34/E2 enzymes in the focal count file. `Glmn` loss is also not the same
perturbation as `Fbxw7` or `Fbxo11` loss: removing an RBX1 inhibitor could
increase CRL activity and indirectly destabilize several adaptors, whereas
removing a substrate receptor disables one SCF complex. The estimate therefore
extrapolates from pathway-adjacent held-in genes, not from a same-complex
knockout.

The endpoint is a small integer count under an assay with many zeros, and the
distinction between 0 and 1 DEG is fragile. I chose a singleton because the
direct SCF/F-box comparators were both singleton focal responders, but a true
flat outcome would also be biologically unsurprising under partial, acute,
postnatal, protein-level CRL perturbation in neurons.
