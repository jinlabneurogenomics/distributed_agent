## Direct forecast for Gabra4 in 151 TH Prkcd Grin2c Glut

Target: `Gabra4`

Predicted `n_degs`: **2**

### Evidence used

- The held-out manifest contains the single target `Gabra4`.
- In the declared Gabra4 biology bundle, the exact focal-population expression measurement reports `Gabra4` as available and broadly expressed in `151 TH Prkcd Grin2c Glut`: 23,570 / 23,679 non-target nuclei express it, with 99.54% expressing cells, mean log1p CP10K 2.18, and pseudobulk CPM 860.9. I treated this as strong reach across the focal assayed nuclei, not as editing efficiency.
- The same bundle describes alpha-4 as an integral subunit of extrasynaptic GABA(A) receptor chloride channels mediating tonic inhibition in thalamic relay neurons. Its functional-stock conclusion is `likely_substantially_depleted` by the P37-P44 harvest after P16 editing: installed receptors are initially spared, but the common alpha-4/delta surface pool is dynamic enough that new synthesis should matter over 21-28 days. Evidence completeness is only partial because alpha-4-specific thalamic turnover was not directly measured.
- The 1,674-row `151 TH Prkcd Grin2c Glut` training count table is very sparse: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, and only 132 / 1,674 targets have at least 5 DEGs.
- In the exact focal training count table, directly represented inhibitory receptor and GABA-system perturbations are almost all flat or self-only:
  - `Gabra1`: 1
  - `Gabra2`: 0
  - `Gabra3`: 0
  - `Gabra5`: 0
  - `Gabrb1`: 0
  - `Gabrb2`: 4
  - `Gabrb3`: 0
  - `Gabrd`: 2
  - `Gabrg2`: 1
  - `Gabrg3`: 0
  - `Gabrr2`: 0
  - `Gphn`: 0
  - `Arhgef9`: 1
  - `Slc6a1`: 0
  - `Slc32a1`: 0
  - `Gad2`: 0
  - `Abat`: 0
- Querying the declared parquet for the same focal group showed that, at BH FDR < 0.05, `Gabrd` had exactly its self row plus `Cttnbp2`, `Gabrb2` had its self row plus `Nr4a1`, `Vgf`, and `Nalf1`, `Gabrg2` and `Gabra1` were self-only, and the other represented alpha/beta/gamma/rho subunits were zero. The self rows are part of the requested endpoint because `n_degs` counts all measured genes passing the adjusted Wilcoxon threshold.
- The packaged same-experiment Findings/Claims for held-in receptor perturbations put a clear boundary on analog transfer:
  - `Gabrb2` is the GABA-A outlier in this thalamic class, with a selective sparse activity/neuropeptide response.
  - `Gabrd` is weaker than `Gabrb2` and `Gabrg2`; its focal response was essentially a delta self row plus one `Cttnbp2` downstream row.
  - `Gabra1`, `Gabra2`, `Gabra3`, `Gabra5`, `Gabrb3`, `Gabrr2`, `Gphn`, and related GABA/inhibitory-synapse genes do not form a common postnatal snRNA-seq module or a robust receptor-subunit mRNA compensation program.
- A symmetric focal-profile comparison over 20 held-in GABA/inhibitory-synapse nodes confirmed the same boundary quantitatively. Thirteen of the 20 nodes had no FDR 0.05 feature, seven had only 1-9 significant features, and among the 11 represented GABA-A subunits all 55 selected pairs had zero significant-program overlap. Gabrb2 and Gabrd also had no FDR 0.05 positive or negative intersection with the other focal alpha/beta/gamma/delta/rho subunits inspected.

### Reasoning

The prior for an arbitrary held-in target in `151 TH Prkcd Grin2c Glut` is zero or one DEG, and the represented GABA-A/GABA-system sector sits in that same sparse regime. The biology bundle nevertheless argues that Gabra4 is not an absent-context target: alpha-4 is highly expressed in almost every focal nucleus and supplies a thalamic extrasynaptic tonic conductance whose operative receptor stock should substantially renew over the perturbation window. That made a pure biological zero less plausible than a self-row or tiny alpha/delta-like response.

For magnitude, the strongest direct held-in anchor was `Gabrd`, the usual alpha-4 partner. Its focal outcome was a two-row response, and the corpus explicitly cautions that beta-2's activity-gene induction is subunit- and context-specific rather than a pan-GABA-A signature. Because `Gabrb2` reached 4 DEGs at the requested FDR threshold and nine downstream genes only at FDR 0.10, while `Gabra1`, `Gabra2`, `Gabra3`, and `Gabra5` were zero or self-only, I interpreted beta-2 as an upper sparse comparator rather than the center for alpha-4.

I therefore predicted that Gabra4 would be detectable but still very small: its own row plus one downstream thalamic alpha/delta receptor response, matching the scale of `Gabrd` and staying below the beta-2-specific activity state.
