target_name: Tubb4a
predicted_n_degs: 1

Evidence used

- Task and bindings: the target manifest is the one-row file for Tubb4a, and the endpoint is the count of measured genes with BH-adjusted Wilcoxon p < 0.05 in `151 TH Prkcd Grin2c Glut`.
- Biology bundle: the canonical Tubb4a bundle, sha256 `2c56cc8e70e72077c2f23f12c3ebd1b6769718f566bd0cbd0dd1429414ced93f`, reports exact focal-population expression of Tubb4a in non-target cells: 22,311 / 23,679 nuclei expressing, 94.22% expressing, mean raw UMI 5.06, mean CP10K 2.98.
- Biology bundle: TUBB4A is a beta-tubulin structural subunit. A P16 disruptive edit should stop new functional TUBB4A production but should not directly disable already installed heterodimers and microtubules.
- Biology bundle: operative beta-tubulin capacity is expected to persist through the 21-28 day harvest window more often than collapse. The main reasons are germline Tubb4a-null mouse neural tissue maintaining total beta-tubulin with cell-type-specific induction of Tubb2a, Tubb2b, and Tubb5, no detected baseline neural deficit through one year, and total brain tubulin turnover on a days-to-weeks scale. The bundle explicitly notes that acute thalamic compensation was not measured, so this is a strong downward bearing with residual uncertainty rather than proof of a zero response.
- Declared count table, focal population only: among the 1,674 training perturbations, 1,205 were zero; the median was 0; the 75th percentile was 1; the 90th percentile was 2; and only 5% exceeded 18 DEGs. The unconditional training distribution is therefore dominated by null or self-only signatures.
- Declared count table and Parquet, direct cytoskeletal comparators in the same focal population:
  - `Tubb4b`: 1 DEG, only Tubb4b itself significant in the inspected Parquet rows.
  - `Tubb5`: 1 DEG, only Tubb5 itself significant.
  - `Tuba4a`: 2 DEGs.
  - `Tuba1a`: 7 DEGs: Tuba1a down plus a small tubulin-isotype response including Tubb3, Tubb2a, Tuba4a, Tubb4a, Tubb4b, and Tubb5.
  - Other available cytoskeletal or microtubule-associated perturbations were similarly small: Map6 0, Spast 0, Actg1 1, Kif5a 1, Kif5c 1, Map1b 1, and Stmn2 1. I treated Dctn1, at 75 DEGs with a sterol/cholesterol program, as an upper-tail boundary rather than the right scale for loss of one buffered beta-tubulin isotype.

Reasoning

Tubb4a is abundantly transcribed in the exact assayed thalamic population, so a self-feature effect is plausible if edited alleles reduce nuclear Tubb4a RNA. However, expression reach is not functional dependence: the carded biology points to a replaceable structural beta-tubulin contribution, pre-existing microtubules are not acutely poisoned by a loss-of-function edit, and mouse null data support beta-tubulin compensation with preserved neural function.

The same-population training rows fit that biology. Perturbing individual tubulin subunits in 151 TH Prkcd Grin2c Glut produced self-only or very small compensation signatures, not the hundreds-of-DEGs stress state seen after loss of RNA-processing, proteasome, or trafficking genes. The most relevant beta-tubulin comparators, Tubb4b and Tubb5, were both exactly 1 DEG; the one alpha-tubulin response with a visible beta-tubulin compensation program, Tuba1a, was still only 7 DEGs.

I therefore placed Tubb4a in the self-only / near-null regime and used 1 as the point forecast. The main ways this could miss are a zero outcome if Tubb4a transcript is not itself detectably depleted, or a low single-digit outcome if acute Tubb2a/Tubb2b/Tubb5 compensation crosses FDR in this thalamic class.
