# Tfap2a direct DEG-count forecast

Target and endpoint:

- The one-row holdout manifest names `Tfap2a`.
- The requested endpoint is the number of genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The training count table has 1,674 available perturbations for this same endpoint and does not contain `Tfap2a`.

Biology that controlled the forecast:

- The declared biology bundle gives exact focal-population expression for `Tfap2a`: 81 of 23,679 matched non-target nuclei expressed the transcript in `151 TH Prkcd Grin2c Glut`, for 0.342% of nuclei, with mean raw UMI 0.0050 and mean CP10K 0.00267. That is a very small reachable population for a cell-aggregate DE test.
- `Tfap2a` encodes AP-2alpha, a soluble sequence-specific AP-2 transcription factor. The functional-stock adjudication concluded that pre-edit TFAP2A protein is likely substantially depleted over the P16 to P37-P44 interval, so I did not treat the edit as intrinsically too delayed to matter.
- The phenotype evidence is much less transferable: the mouse loss evidence is embryonic neural crest or embryonic retina rather than acute postnatal thalamus, and retinal `Tfap2b` buffering is not a demonstrated juvenile-thalamus mechanism. Thus the evidence supports possible engagement but not a high-burden thalamic response.

Endpoint-matched training evidence:

- The 151-class training count table is zero-heavy: median `n_degs` is 0; 1,205 of 1,674 training targets have zero DEGs; the 75th percentile is 1 and the 90th percentile is 2. The mean, 14.05, is dominated by a small heavy tail.
- Typed mouse annotation nomination found no assayed `Tfap2a` paralog and no `Tfap2b` training profile. The non-generic available AP-2 comparators were five Reactome AP-2 pathway members/regulators plus one native Kremen1-AP-2 CORUM complex member: `Wwox` 0 DEGs, `Ep300` 0, `Kctd1` 2, `Esr1` 0, `Kdm5b` 0, and `Kremen1` 0.
- Direct 151-class parquet inspection of those six profiles matched the count table. `Kctd1` had only `Resp18` and `Cluap1` significant at BH < 0.05; the other five had no significant genes despite 145-230 matched perturbed nuclei against 23,679 matched controls.

Synthesis:

I gave the exact in-assay reach the most weight because `Tfap2a` is expressed in only ~0.34% of the focal non-target nuclei. The AP-2-specific training comparators were likewise at 0-2 DEGs rather than in the training heavy tail. Since the direct analog average was 2 / 6 = 0.33 DEGs and the median was 0, I rounded the forecast to the nearest biologically plausible integer at the endpoint floor.

Predicted `n_degs`: 0
