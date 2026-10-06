# Tfap2a DEG-count prediction trace

## Target and endpoint

The declared held-out target is `Tfap2a` in `151 TH Prkcd Grin2c Glut`. The
forecasted endpoint is the number of measured genes in that class with
BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The one-row manifest names only `Tfap2a`; `Tfap2a` is absent from the
  1,674-row training count table.
- The exact in-assay reach card reports extremely sparse focal expression:
  `81 / 23679` matched non-target nuclei expressed `Tfap2a`
  (`0.342075%`), with pseudobulk expression only `0.314969` cpm and
  `119` total target UMIs across the matched non-target focal population.
- The functional-stock card supports eventual target engagement: TFAP2A is a
  soluble AP-2 DNA-binding transcription factor, editing should stop new
  functional protein synthesis, and the P16-to-P37/44 interval is long relative
  to ordinary adult thalamic protein turnover. The evidence is still partial
  because no TFAP2A-specific half-life was found.
- The same target card does not establish a mature thalamic requirement.
  Reported mouse neural phenotypes are neural-crest or embryonic-retinal, not
  acute postnatal thalamic loss, and the available retinal work shows AP-2
  paralog buffering in another neural context rather than a guaranteed
  single-gene thalamic response.
- The `151 TH Prkcd Grin2c Glut` training counts are strongly zero-inflated:
  `1205 / 1674 = 71.98%` of assayed training perturbations had `0` DEGs,
  `90.32%` had at most `2`, and only `42 / 1674 = 2.51%` exceeded `100`.
  The largest outliers were broad housekeeping or chromatin/RNA-processing
  regulators such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`,
  `Psmb4`, and `Hnrnpu`.
- No direct `Tfap2b/c/d/e` AP-2 paralog appeared in the training table. In the
  next-best group of observed developmental or regionally patterned
  transcription-factor perturbations, the declared count table and the Parquet
  rows for this exact class agreed on a near-null response:
  `Alx1`, `Alx3`, `Alx4`, `Arx`, `Atoh1`, `Lhx3`, `Lhx4`, `Neurod1`,
  `Neurod2`, `Pou3f3`, `Pou3f4`, `Tfap4`, `Vsx1`, `Vsx2`, `Zic2`, `Zic3`,
  and `Zic4` all had `0` FDR-significant genes; `Zic1` had `2`.

## Synthesis

`Tfap2a` is a plausible functional CRISPR target by protein-turnover logic, but
the postnatal thalamic transcriptomic footprint should be heavily diluted: only
about one third of one percent of focal control nuclei had any detected
`Tfap2a` RNA, and the target card gives no transferable evidence that a larger
hidden TFAP2A-positive population in this thalamic aggregate undergoes a broad
state transition by 21-28 days. The relevant training background is already
mostly `0`, and the closest measured class of sparse developmental TFs is also
almost uniformly `0`.

I therefore placed `Tfap2a` at the null mode of the focal training endpoint.

Point prediction: `0` DEGs.
