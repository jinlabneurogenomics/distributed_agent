# Question

I interpreted the task as: for each requested held-out perturbation, predict the number of genes in `151 TH Prkcd Grin2c Glut` cells whose Wilcoxon test has `pvals_adj < 0.05`, using only the non-held-out perturbations in the supplied parquet and focal-cell DEG-count table plus outside biological knowledge. The only requested target in `054_Ddx23.csv` is `Ddx23`.

The key ambiguity I resolved is that `n_degs` is an endpoint of this particular sparse P16 AAV CRISPR/snRNA-seq assay, not a general measure of essentiality or spliceosome importance. I therefore calibrated `Ddx23` against measured focal-cell spliceosome/RNA-processing perturbations rather than assigning a value from textbook essentiality alone.

# Sources

- Input DEG parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Input endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Request manifest: `[local file: 054_Ddx23.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, via `target_context`, `expand_candidate_set`, and `candidate_set_topology`.
- Distributed Agents runtime profile analysis over the focal `151 TH Prkcd Grin2c Glut` profiles, via `profile_neighbors`, `profile_compare`, and `profile_inspect`.
- PubMed-indexed spliceosome literature:
  - Teigelkamp et al. 1997, PMID 9409622: human U5-100K is the U5 snRNP DEAD-box protein homologous to yeast Prp28.
  - Mathew et al. 2008, DOI `10.1038/nsmb.1415`: SRPK2-dependent PRP28/DDX23 phosphorylation is required for stable association with U4/U6-U5 tri-snRNP and for B-complex formation.
  - Moehlmann et al. 2014, DOI `10.1107/S1399004714006439`: human Prp28 is essential for spliceosome activation and gains ATP-binding activity in the assembled spliceosomal complex.
  - Zhan et al. 2018, DOI `10.1038/s41422-018-0094-7`: the Prp28 and Brr2 helicases drive the human pre-B-to-B and B-to-Bact spliceosome transitions.
  - Charenton et al. 2019, DOI `10.1126/science.aax3289`: structural mechanism in which Prp28 promotes transfer of the 5-prime splice site from U1 snRNA to the U6 ACAGAGA sequence.
  - Wilkinson et al. 2019, DOI `10.1146/annurev-biochem-091719-064225`: review of spliceosome assembly and activation.

# Computational Checks

I first confirmed that the held-out list has exactly one target, `Ddx23`, and that the focal-cell training counts contain 1,674 observed perturbations. The focal endpoint is sparse: median `n_degs` is 0, the mean is 14.05, and 72% of training perturbations have zero DEGs. The strong right tail nevertheless contains several RNA-processing/spliceosome perturbations:

| training target | focal `n_degs` |
|---|---:|
| `Rnpc3` | 868 |
| `U2af2` | 828 |
| `Cdc40` | 624 |
| `Prpf6` | 454 |
| `Thoc1` | 303 |
| `Snrnp70` | 213 |
| `Hnrnpc` | 122 |
| `Ddx3x` | 8 |
| `Snrpn` | 1 |
| `Ctnnbl1` | 1 |
| `Ddx39b` | 0 |
| `Rbm28` | 0 |
| `Snrpb` | 0 |

To avoid reading the 616M-row parquet wholesale, I filtered it by `group_name = '151 TH Prkcd Grin2c Glut'` and a hand-curated RNA-processing candidate list, then recomputed for each candidate:

```python
n_sig = (pvals_adj < 0.05).sum()
pos_sig = ((pvals_adj < 0.05) & (logfoldchanges > 0)).sum()
neg_sig = ((pvals_adj < 0.05) & (logfoldchanges < 0)).sum()
```

The exact focal splits for the main analogs were:

| training target | total | up | down |
|---|---:|---:|---:|
| `Rnpc3` | 868 | 390 | 478 |
| `U2af2` | 828 | 446 | 382 |
| `Cdc40` | 624 | 446 | 178 |
| `Prpf6` | 454 | 243 | 211 |
| `Snrnp70` | 213 | 127 | 86 |
| `Thoc1` | 303 | 233 | 70 |
| `Hnrnpu` | 733 | 483 | 250 |
| `Hnrnpc` | 122 | 77 | 45 |
| `Matr3` | 149 | 105 | 44 |
| `Tardbp` | 210 | 131 | 79 |
| `Snrpb` | 0 | 0 | 0 |
| `Ddx39b` | 0 | 0 | 0 |
| `Ctnnbl1` | 1 | 1 | 0 |

I also intersected FDR-significant gene sets between the core spliceosome analogs and counted same- versus opposite-direction overlaps. The module is coherent in the focal group:

| pair | shared FDR genes | same direction | opposite direction |
|---|---:|---:|---:|
| `Prpf6` / `Cdc40` | 107 | 103 | 4 |
| `Prpf6` / `U2af2` | 121 | 113 | 8 |
| `Prpf6` / `Rnpc3` | 127 | 118 | 9 |
| `Prpf6` / `Snrnp70` | 46 | 45 | 1 |
| `Cdc40` / `U2af2` | 130 | 113 | 17 |
| `Cdc40` / `Rnpc3` | 136 | 117 | 19 |
| `U2af2` / `Rnpc3` | 194 | 157 | 37 |
| `Rnpc3` / `Snrnp70` | 85 | 79 | 6 |

Recurrent same-direction genes among three to five of `Prpf6`, `Cdc40`, `U2af2`, `Rnpc3`, and `Snrnp70` included down-regulated `Rsrp1`, `Snhg11`, `Ogt`, `Agrn`, `Atp2a2`, `Slc17a6`, `Vamp1`, `Srrm2`, `Luc7l2`, `Coro6`, and `Spock3`, plus up-regulated RNA-processing/stress or homeostatic genes such as `Cherp`, `Dhx16`, `Grk2`, and `Zfp335`. This matches the Distributed Agents corpus claims that `Prpf6`, `Cdc40`, `U2af2`, `Rnpc3`, and `Snrnp70` produce a shared same-direction neuronal RNA-processing module rather than isolated target-specific noise.

# Ddx23 Reasoning

`Ddx23` encodes human/mouse Prp28, the DEAD-box U5 snRNP helicase. It is much closer mechanistically to the strong observed spliceosome module than to unrelated DEAD-box genes in the screen: PRP28 is recruited with U4/U6-U5 tri-snRNP, its phosphorylation stabilizes its tri-snRNP association, and its ATP-dependent RecA-domain closure participates in releasing the 5-prime splice site from U1 so U6 can engage during human pre-B to B complex formation. That places it near the same assembly/activation window sampled by `Prpf6` and `Snrnp70`, and upstream of the `Cdc40`/PRP17 catalytic-step phenotype.

The strongest direct quantitative anchor is `Prpf6` with 454 DEGs. It is the only high-confidence U5/tri-snRNP structural comparator present in the focal training set; Prpf8, Snrnp200/Brr2, Eftud2, Prpf31, Prpf3, and Prpf4 were not training perturbations. Distributed Agents `Prpf6:F003` reports that `Cdc40`, `U2af2`, `Snrnp70`, and `Rnpc3` converge with `Prpf6` in the same thalamic/midbrain responders, and the exact focal rows confirm that `Prpf6` shares 103/107, 113/121, 118/127, and 45/46 overlapping FDR genes in the same direction with `Cdc40`, `U2af2`, `Rnpc3`, and `Snrnp70`, respectively. This makes a nonzero `Ddx23` response highly likely.

I did not simply average every broad RNA-processing perturbation. `Rnpc3` at 868 DEGs is a minor-spliceosome factor and has a much broader, U12-intron-linked trafficking signature; `U2af2` at 828 acts at 3-prime splice-site recognition and is also broader; `Cdc40` at 624 acts in the PRP19/PRP17 activation/catalysis neighborhood rather than as a U5 Prp28 helicase. These support the sign of the decision and the few-hundred-gene scale but are probably high-side comparators for `Ddx23`.

The low-side boundaries are also informative. `Snrnp70`, a core U1 snRNP factor at the 5-prime splice-site side of the Prp28 reaction, has 213 DEGs and shares its focal DE program directionally with the major spliceosome hits. `Thoc1` has 303 DEGs but is TREX/export-adjacent rather than a core tri-snRNP component. `Hnrnpc`, `Matr3`, and `Tardbp` are RNA-binding or nuclear-matrix factors with 122-210 DEGs and only partial overlap, so they argue against forcing every RBP into the 600-900 range.

I treated `Snrpb`, `Snrpn`, `Ctnnbl1`, `Ddx39b`, `Ddx3x`, `Rbm28`, `Son`, and `Upf3b` as counterexamples rather than analogs. `Snrpb` is an Sm protein and was explicitly described in the Distributed Agents Cdc40/Prpf6 neighborhood as an almost-flat boundary; it has zero focal DEGs here. `Ctnnbl1` is PRP19-complex-associated but has only one focal DEG. `Ddx39b` is a spliceosome/TREX RNA helicase yet is flat in `151 TH Prkcd Grin2c Glut`, with its same-experiment response concentrated in `191 MB P MY GABA`. The DEAD-box family alone is particularly unhelpful: the represented `Ddx3x` and `Ddx39b` perturbations have 8 and 0 focal DEGs.

Taking these together, I predict that `Ddx23` will be a clear nonzero hit in the focal thalamic glutamatergic population, somewhat weaker than `Prpf6`/`Cdc40` but stronger than the adjacent `Snrnp70` and `Thoc1` boundaries. I used 420 as the integer point prediction, effectively placing DDX23 near the lower U5/core-spliceosome anchor rather than near the unrelated DEAD-box or Sm/CTNNBL1 nulls.

# Limits

- `Ddx23` itself is completely held out, and the Distributed Agents filtered corpus has no `Ddx23` target-centered findings, so this is an extrapolation from adjacent observed perturbations.
- No true same-complex Prp28 partner such as `Prpf8`, `Snrnp200`, `Eftud2`, `Prpf31`, `Prpf3`, or `Prpf4` was available as a focal training perturbation; `Prpf6` is therefore close but not sufficient by itself.
- The parquet is gene-abundance snRNA-seq, not junction-resolved RNA-seq. Splicing defects, intron retention, and unproductive isoforms could differ while whole-gene DEG counts look similar.
- DEG counts are assay- and power-dependent. They combine biological response breadth, editing outcomes, target-cell survival, guide behavior, and matched nucleus counts; the target transcript’s own log-fold change cannot validate or invalidate the prediction.
- The profile-neighbor all-gene correlations include many nonsignificant rows and sometimes rank focal-null genes such as `Snrpb` or `Ddx39b` near broad spliceosome profiles. I therefore used them only as a rough orientation and relied on FDR-significant overlaps plus mechanistic fit for the final call.
