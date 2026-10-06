# Direct forecast trace

Target: `Nyx` in `151 TH Prkcd Grin2c Glut`

Predicted `n_degs`: `0`

## Evidence used

- The declared biology bundle reports very low exact focal-population reach for `Nyx`: 738 of 23,679 non-target nuclei expressed `Nyx` in `151 TH Prkcd Grin2c Glut` (`3.1167%`), with mean raw UMI `0.0333`, mean CP10k `0.0212`, and only 788 total `Nyx` UMIs among 377,814,907 non-target UMIs. This makes a broad aggregated thalamic response unlikely even if a sparse `Nyx`-positive subpopulation is edited.
- The same bundle places Nyx biology mainly in the retina: nyctalopin is a GPI-linked extracellular accessory protein for TRPM1 localization/function at depolarizing bipolar-cell dendritic tips. Low brain expression and a retinal loss phenotype support possible neural function, but no source tied Nyx loss to a basal thalamic RNA program.
- The functional-stock card judged harvest-time loss as only `partially_depleted_or_leading_edge`: P16 genome editing should stop new functional Nyx supply in edited cells, but pre-edit synaptic membrane nyctalopin is not directly removed, synaptic proteins can be long lived, and no Nyx-specific residence time fixes depletion by P37-P44.
- The 151-class training count table is strongly zero-inflated: 1,205/1,674 training perturbations have `n_degs = 0`, 276 have exactly one DEG, the median is 0, the 75th percentile is 1, and the 90th percentile is 2. So a nonessential, sparse, cell-surface/synaptic perturbation should default near zero unless measured neighbors show otherwise.
- Retinal ON-bipolar and adjacent GPCR/RGS comparators that were present in the training set were flat or nearly flat in the same 151-class endpoint:
  - `Grm6`: `0`
  - `Gpr179`: `0`
  - `Gnb5`: `0`
  - `Gnao1`: `1`
  - `Gpr158`: `1`
  The exact 151-class parquet rows agree with those counts. `Grm6`, `Gpr179`, and `Gnb5` had no BH<0.05 gene; the lone `Gnao1` and `Gpr158` hits were the target transcripts themselves.
- Same-experiment packaged Findings for `Grm6`, `Gpr179`, and `Gnb5` are consistent with the raw training counts: represented ON-bipolar cascade and Gbeta5/R7-adjacent perturbations were reported as flat or sparse in postnatal brain neuronal snRNA-seq rather than as a shared basal transcriptomic module.
- Additional receptor/synaptic comparators were also weak in the focal table. `Grm5`, `Grm8`, `Lrrtm3`, `Lrrtm4`, `Nrxn2`, `Nrxn3`, `Vsx1`, and `Vsx2` all had `0`; `Grm1`, `Grm7`, `Lrrtm1`, `Nlgn3`, and `Nrxn1` had `1`. In the exact parquet slice, the `Grm1`, `Grm7`, `Nlgn3`, and `Nrxn1` singleton calls were only self-transcript decreases, again arguing for no transferable downstream DEG burden.
- `Cacna1g` is a useful positive boundary rather than the main analogue: it produced 12 focal DEGs and is a thalamic voltage-gated calcium-channel perturbation, showing that a membrane/signaling gene can register in this class when it is coupled to thalamic biology. Nyx has much lower focal reach and a retina-specific accessory role, so I did not transfer the `Cacna1g` scale.

## Synthesis

I placed the point forecast at zero. The strongest upward bearing is that Nyx has a real postnatal neuronal loss phenotype in retina and lacks a proven close compensator; that keeps a tiny response biologically possible. The stronger downward bearings are the 3.1% focal expression reach, uncertain depletion of installed synaptic stock within the 21-28 day CRISPR window, and direct training evidence that the represented ON-bipolar/Gbeta5 pathway members were silent or self-transcript-only in this thalamic class. A prediction of one would mostly be a bet on the `Nyx` self row crossing BH<0.05; given the very small RNA support for `Nyx` in the matched non-target focal nuclei, I chose no BH-significant measured gene.
