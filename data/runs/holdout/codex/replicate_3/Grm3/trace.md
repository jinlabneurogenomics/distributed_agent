# Direct forecast for Grm3 in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Manifest target: `Grm3`.
- Requested cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes, including the self-transcript row, with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

### Target biology

The declared `Grm3` biology bundle characterizes mGluR3 as a membrane glutamate
GPCR coupled to Gi/o signaling rather than a nuclear, proteostasis, spliceosome,
or chromatin process expected to create a broad standing nuclear RNA state.
Exact in-assay target reach was low in the focal thalamic class: 2,034 of
23,679 non-target nuclei expressed `Grm3` RNA, or 8.5899%, with mean CP10k
0.0694.

The functional-stock card made the edit biologically plausible but not complete
by the 21-28 day harvest. A disruptive edit should stop new mGluR3 production,
but existing surface/recycling receptor pools can persist acutely; the best
stock conclusion was `partially_depleted_or_leading_edge`, with no matched
juvenile thalamic 21-28 day depletion curve. This favors a real but weak or
diluted perturbation in the recovered thalamic nuclei.

### Exact focal-population training counts

The declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` contains 1,674
training targets. Its distribution is strongly zero-inflated:

- 1,205 / 1,674 targets had `n_degs = 0`.
- The median was 0 and the 75th percentile was 1.
- The 90th percentile was 2.
- Only 29 targets had at least 200 DEGs.

The strongest responders in this cell class were core cellular regulators such
as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, `Psmb4`, and `Hnrnpu`,
not synaptic GPCRs.

### Local metabotropic-glutamate and receptor comparators

The closest represented metabotropic-glutamate receptors were quiet in the same
focal count table:

| target | n_degs |
|---|---:|
| `Grm1` | 1 |
| `Grm5` | 0 |
| `Grm7` | 1 |
| `Grm8` | 0 |

The selected broader receptor/synaptic cohort
`Grm1/5/7/8`, `Gabbr1/2`, `Adcy1/3/5`, ionotropic glutamate receptor subunits,
`Dlg4`, `Homer2`, and `Shank2/3` had mean `n_degs = 0.409`, median 0, and
21 of 22 members at `n_degs <= 1` in `151 TH Prkcd Grin2c Glut`.

I also checked the declared Parquet rows for these comparators in the focal
class. The significant hits for `Grm1` and `Grm7` were only their self
transcripts; the other one-hit receptor comparators I inspected were likewise
dominated by self rows (`Gabbr1`, `Gabbr2`, `Grid1`, `Grik5`, `Dlg4`), with
`Shank3` the only inspected synaptic comparator carrying one additional hit.
Thus the relevant empirical precedent is near-zero downstream response, with
the difference between 0 and 1 usually decided by whether the self transcript
crosses the FDR threshold.

### Same-experiment corpus interpretation of training comparators

The packaged Grm1/Grm5/Grm7/Grm8 reports, which are semantic summaries of the
same experiment rather than independent measurements, all support the same
boundary: represented metabotropic-glutamate receptor and nearby
PLC/IP3/PKC/CaMK/postsynaptic-scaffold perturbations generally did not form a
shared basal neuronal snRNA-seq module. Grm5 and Grm8 were pan-null across
recovered neuronal groups at the downstream level, and Grm7's downstream
surface was also FDR-flat despite measurable self-transcript movement.

## Synthesis

I placed `Grm3` with the receptor-family quiet cases rather than with the large
core-regulator tail. Biology argues against a broad cell-body RNA program:
mGluR3 is a low-reach class-C GPCR in this exact aggregated thalamic class, its
loss at 3-4 weeks should be at most partially realized at the functional-stock
level, and represented mGluR/Gi-o/cAMP/synaptic-neighbor perturbations in
training were overwhelmingly buffered in basal nuclear RNA.

The only reason to move the count from 0 to 1 would be a self-transcript hit.
For `Grm3`, exact baseline expression in `151 TH Prkcd Grin2c Glut` was sparse,
so a self row was less compelling than for the one-count Grm1 and Grm7 cases.
My point forecast is therefore:

```text
Grm3 n_degs = 0
```
