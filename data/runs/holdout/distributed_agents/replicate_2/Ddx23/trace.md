# Reasoning trace

## Question and resolved ambiguities

The requested target CSV contains one held-out perturbation, `Ddx23`. I interpreted the task as a point prediction of `n_degs` for `Ddx23` loss of function in `151 TH Prkcd Grin2c Glut`: the number of measured genes whose Scanpy/Wilcoxon Benjamini-Hochberg-adjusted p value would be below 0.05 for this perturbation in this cell group.

I treated `0` as a prediction that no measured gene would pass the exact focal FDR threshold, not as an assertion that DDX23 biology is irrelevant or unedited. The estimate below is for the P16 acute sparse CRISPR, P37-P44 surviving-nucleus, gene-level snRNA-seq assay described in the prompt, not for a germline null, a junction-level splicing assay, or a viability assay.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene log fold changes, Wilcoxon scores, and adjusted p values for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for the 1,674 non-held-out perturbations in the focal cell group.
- `054_Ddx23.csv`: the requested held-out target list; it contains only `Ddx23`.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`, especially the target contexts and pathway ledgers for `Prpf6`, `Cdc40`, `U2af2`, `Rnpc3`, `Snrnp70`, `Thoc1`, `Ddx39b`, `Snrpb`, `Hnrnpc`, and `Ctnnbl1`.
- PubMed literature on PRP28/DDX23 and spliceosome assembly:
  - Mathew et al. 2008, DOI `10.1038/nsmb.1415`, PMID `18425142`: PRP28/DDX23 phosphorylation by SRPK2 is required for stable U4/U6.U5 tri-snRNP association and B-complex formation.
  - Mohlmann et al. 2014, DOI `10.1107/S1399004714006439`, PMID `24914973`: structural and functional analysis of human PRP28 as a spliceosomal DEAD-box helicase needed for active spliceosome formation.
  - Zhan et al. 2018, DOI `10.1038/s41422-018-0094-7`, PMID `30315277`: human pre-B and B spliceosome structures, with the pre-B-to-B transition driven by Prp28.
  - Wilkinson, Charenton, and Nagai 2019, DOI `10.1146/annurev-biochem-091719-064225`, PMID `31794245`: review of spliceosome assembly and the handoff from U1 at the 5-prime splice site to U6/U5 during tri-snRNP recruitment.

## Computations over the training data

I first read the focal training counts. The focal endpoint is heavily zero-inflated:

| quantity | value |
|---|---:|
| training targets | 1,674 |
| nonzero targets | 469 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436.5 |
| maximum | 2,677 |

Thus any prediction in the several-hundred range is a top-percentile response for this cell type and needs a strong within-dataset spliceosome analogy.

I then loaded focal rows from the parquet for spliceosome, RNA-processing, and counterexample targets:

```python
expr = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(targets)
)
```

For each selected observed perturbation I counted rows with `pvals_adj < 0.05`, verifying the counts in the endpoint CSV and recording the matched perturbed-cell counts. I also checked exact FDR<0.05 gene overlap and hallmark spliceosome-response genes in the focal group.

## Relevant observed analogs

`Ddx23` is absent from both the parquet and the Distributed Agents corpus, so the prediction was transferred from observed perturbations with a measured focal `n_degs`.

| training target | focal `n_degs` | matched perturbed nuclei | how it informs `Ddx23` |
|---|---:|---:|---|
| `U2af2` | 828 | 222 | Core splice-site recognition factor. Strong upper analog for a major-spliceosome lesion; its 151 signature had `Rsrp1`, `Srrm2`, `Luc7l2`, `Atp11b`, `Cyp46a1`, and synaptic effector genes among top FDR hits. |
| `Rnpc3` | 868 | 149 | Core minor-spliceosome factor. Mechanistically farther from DDX23 than major-spliceosome factors, but it shows that acute loss of an essential snRNP/RNP component can yield a very broad 151 TH response. |
| `Cdc40` | 624 | 159 | CDC40/PRP17 is a spliceosome factor at a later catalytic stage. In the Distributed Agents corpus, its responders converged with `Prpf6`, `U2af2`, and `Snrnp70`, while the Sm target `Snrpb` was flat, demonstrating selective rather than generic snRNP transfer. |
| `Prpf6` | 454 | 72 | Closest observed major-spliceosome analog: a U4/U6.U5 tri-snRNP protein from the same particle into which PRP28/DDX23 is recruited. The same-experiment corpus reports `Prpf6` convergence with `Cdc40`, `U2af2`, `Snrnp70`, and `Rnpc3`, and the focal count of 454 shows a broad but not maximal response even with only 72 matched perturbed nuclei. |
| `Snrnp70` | 213 | 135 | U1-specific 70K factor; PRP28/DDX23 promotes the transition in which U1 leaves the 5-prime splice site. This is a lower positive spliceosome analog in the focal group. |
| `Thoc1` | 303 | 121 | TREX/mRNA-export factor, not a spliceosomal helicase, but it shares RNA-biogenesis/nuclear-export stress signatures with spliceosome targets and with `Ddx39b` in the Distributed Agents corpus. Its 303 DEGs show that adjacent mRNP-handling biology can be broad in 151 TH. |
| `Hnrnpu` | 733 | 163 | Broad hnRNP/RNA-processing perturbation. Useful only as a positive RNA-processing context because Distributed Agents found hnRNP family members were not interchangeable. |

Observed focal counterexamples were just as important:

| training target | focal `n_degs` | why it was not pooled as a positive analog |
|---|---:|---|
| `Ddx39b` | 0 | A DEAD-box helicase and TREX/export factor, but its Distributed Agents state is mainly 191 MB P MY GABA and does not generalize to 151 TH. This rejects the generic "DDX helicase" label for `Ddx23`. |
| `Ddx3x` | 8 | Another DEAD-box RNA helicase with a tiny focal surface; also argues against using helicase family membership alone. |
| `Snrpb` | 0 | Sm-core snRNP target that was essentially flat across the assay despite broad `Prpf6`, `U2af2`, and `Snrnp70` responses. Same-particle or snRNP membership by itself is not enough. |
| `Snrpn` | 1 | SmN paralog target; also nearly flat and nonconvergent with the broad spliceosome factors. |
| `Ctnnbl1` | 1 | PRP19-complex member that Distributed Agents explicitly marked as buffered relative to `Cdc40`, `Prpf6`, `Rnpc3`, `Snrnp70`, `U2af2`, and `Hnrnpu`. |
| `Hnrnpa2b1` | 11 | Weak hnRNP-family perturbation; family-level RNA binding was a poor predictor. |
| `Hnrnph2` | 4 | Weak hnRNP-family perturbation; family-level RNA binding was a poor predictor. |
| `Hnrnpc` | 122 | Spliceosome-adjacent but much weaker than core-spliceosome responders and partially divergent from `U2af2`. |

The exact focal FDR<0.05 overlap among the positive core analogs was nonzero but mixed, consistent with overlapping secondary RNA-stress states rather than one duplicated signature. Examples were `U2af2`/`Rnpc3` sharing 194 significant genes in 151 TH, `Cdc40`/`U2af2` sharing 130, `Prpf6`/`Rnpc3` sharing 127, `Prpf6`/`U2af2` sharing 121, and `Cdc40`/`Prpf6` sharing 107. Hallmark focal genes recurring across this module included decreases of `Rsrp1`, `Srrm2`, `Luc7l2`, `Luc7l3`, `Pnisr`, `Grin1`, and `Slc17a6`, and increases of compensatory RNA-processing genes such as `Sart1`, `Srsf10`, and `Snrnp200`.

## Target-specific prediction for `Ddx23`

External mechanism makes `Ddx23` a stronger analog of `Prpf6`, `U2af2`, `Cdc40`, and `Snrnp70` than of `Ddx39b` or `Ddx3x`. Human PRP28/DDX23 is a spliceosomal DEAD-box helicase acting during U4/U6.U5 tri-snRNP integration into the spliceosome and the pre-B-to-B transition; it participates in release of U1 snRNP from the 5-prime splice site and handoff to U6/U5. That places it in the major-spliceosome activation machinery, immediately adjacent to the U5/U4/U6 tri-snRNP axis represented by `Prpf6`, rather than in a broad and weakly predictive DDX-family bucket.

The zero/nonzero decision is therefore nonzero. The focal group clearly can mount hundreds of gene-level DEGs after acute CRISPR perturbation of several core spliceosome factors, including `Prpf6` despite only 72 matched perturbed nuclei. `Ddx23` does not have the obvious SmB/SmN paralog-buffering argument that made `Snrpb`/`Snrpn` poor analogs, and it is more proximal to B-complex assembly than `Hnrnpa2b1`, `Hnrnph2`, or the focal-null `Ddx39b`.

For magnitude, I did not take the median of every RNA-processing gene because that would mix true core-spliceosome hits with null counterexamples. I centered the estimate below `U2af2`/`Rnpc3`/`Cdc40` because DDX23 is a transient helicase whose residual protein or phosphorylation-dependent recruitment could buffer partial CRISPR loss, and above `Snrnp70` because PRP28/DDX23 directly supports the major U5/U4/U6 spliceosome transition rather than a U1-only branch. The closest observed focal count, `Prpf6 = 454`, was treated as the main calibration point, with `Thoc1 = 303` and `Snrnp70 = 213` pulling the estimate downward from the 600-900 range of `Cdc40`, `U2af2`, and `Rnpc3`.

**Prediction:** `Ddx23` -> **400 DEGs** in `151 TH Prkcd Grin2c Glut`.

## Limits

The evidence for `Ddx23` is extrapolative. The held-out gene has no direct DE surface, Distributed Agents had no target-centered `Ddx23` finding, and several closest U4/U6.U5 components that would be ideal PRP28 controls, including `Prpf8`, `Snrnp200`, `Eftud2`, `Prpf31`, `Prpf3`, and `Prpf4`, were not represented as perturbation targets in the supplied training parquet. The screen reports gene-level nuclear abundance in surviving postnatal neurons; it does not measure guide indels, DDX23 protein, PRP28 phosphorylation, splice-junction usage, U1 displacement, or cell loss. Counts in this endpoint also depend strongly on matched perturbed-cell number and on how the secondary stress state crosses an FDR threshold, so the 400 value should be read as a calibrated response-breadth point estimate rather than a direct measurement of primary spliceosome failure.
