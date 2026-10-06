# Prediction trace

## Question and resolved ambiguities

The requested endpoint is `n_degs` for held-out genetic perturbations in `151 TH Prkcd Grin2c Glut` cells: the number of measured genes whose Wilcoxon p-value in the held-out perturbation would pass Benjamini-Hochberg FDR < 0.05. The only held-out target in this run was `Atp6v0c`, and the prediction must include any significant self-target RNA effect if the real held-out `Atp6v0c` contrast had one.

I treated the supplied focal-cell count CSV as the directly observed training endpoint for the 1,674 non-held-out perturbations. I used the large Parquet only for measured expression signatures and QC around candidate analogs, because `Atp6v0c` itself is intentionally absent from the Parquet and count CSV.

## Sources

- Declared count table: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared DE table: `training differential-expression dataset`
- Requested-target manifest: `single-target request for Atp6v0c`
- Dataset portrait and measurement registry in `codex_runtime/pipeline`, which define the CRISPR, snRNA-seq, matched-control, and recovered-nucleus semantics.
- Same-experiment internal corpus: `perturbai-july-260713-sourceguard-1773-v1`, queried only for named V-ATPase analogs.
- External literature from PubMed:
  - Forgac 2007, PMID 17912264, DOI `10.1038/nrm2272`: V-ATPases are multisubunit ATP-driven rotary proton pumps that acidify endosomes, lysosomes, and other compartments.
  - Galli, McPherson and De Camilli 1996, PMID 8567678, DOI `10.1074/jbc.271.4.2193`: the V0 c subunit is present on rat synaptic vesicles in complexes with synaptobrevin 2/synaptophysin.
  - Morel, Dedieu and Philippe 2003, PMID 14600261, DOI `10.1242/jcs.00791`: the V0 a1 isoform is sorted to nerve terminals and associates with synaptic vesicles and presynaptic plasma membrane.
  - Di Giovanni et al. 2010, PMID 20670834, DOI `10.1016/j.neuron.2010.06.024`: the V0 c subunit can interact with VAMP2/synaptobrevin and acute blockade of that interaction reduces neurotransmitter release probability without blocking proton pumping.
  - Poea-Guyon et al. 2013, PMID 24165939, DOI `10.1083/jcb.201303104`: acute inactivation of V0 a1-I decreases neurotransmitter release and links V0 membrane-sector status to exocytosis.
  - Zoncu et al. 2011, PMID 22053050, DOI `10.1126/science.1207056`: lysosomal V-ATPase participates in amino-acid signaling to mTORC1.

## Quantitative checks

The held-out manifest contains exactly one target, `Atp6v0c`. A direct Parquet check confirmed that `Atp6v0c` contributes zero rows as a `gene_target`; it is absent because it was held out, not because it lacked a response.

I queried the focal group for training genes encoding V-ATPase or nearby endolysosomal machinery. The most relevant observed `151 TH Prkcd Grin2c Glut` counts were:

| analog | relationship to Atp6v0c | observed n_degs |
|---|---|---:|
| Atp6v0a1 | V0 membrane-sector a1 subunit, the closest held-in V0 proton-translocation subunit | 1 |
| Atp6ap2 | V-ATPase accessory assembly factor/pro-renin receptor | 2 |
| Atp6v1a | V1 ATP-hydrolysis A subunit | 0 |
| Atp6v1b2 | V1 ATP-hydrolysis B2 subunit | 0 |
| Atp6v1e1 | V1 E1 subunit | 0 |
| Lamp2 | lysosomal membrane comparator | 0 |
| Clcn3 | endolysosomal chloride transporter comparator | 0 |
| Clcn4 | endolysosomal chloride transporter comparator | 1 |
| Becn1 | autophagy comparator | 0 |
| Cltc | endocytic/synaptic-vesicle membrane trafficking comparator | 3 |
| Vps35 | retromer endosomal sorting comparator | 17 |
| Vps54 | endosome-to-Golgi trafficking comparator | 31 |
| Rab7 | late-endosome/lysosome trafficking comparator with a strong detectable lysosomal compensation signature | 501 |

For the five closest V-ATPase analogs I also pulled all `151 TH Prkcd Grin2c Glut` rows with adjusted p-value below 0.5 and all rows for lysosomal/stress sentinels. In the focal group:

- `Atp6v0a1` had one significant gene, `Atp6v0a1` itself, down 0.640 log2-fold at FDR `4.5e-12`; there were no significant downstream lysosomal, autophagy, UPR, or ISR genes.
- `Atp6ap2` had two significant genes, `Atp6ap2` itself and `Atp6v0a1`, with `Atp6v0c` unchanged.
- `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` had no focal-cell gene below FDR 0.05, including their own transcripts.
- Pairwise score-vector correlations among `Atp6v0a1`, `Atp6ap2`, `Atp6v1a`, `Atp6v1b2`, and `Atp6v1e1` were only 0.017-0.109 by Pearson and 0.019-0.070 by Spearman, so the matrix does not contain a coherent multi-gene "generic V-ATPase loss" signature.

The same-experiment corpus was consistent with those direct counts. Its `Atp6v0a1` and `Atp6ap2` Findings summarize V-ATPase perturbations as strongly buffered in recovered postnatal neurons, explicitly noting absent TFEB/CLEAR, lysosomal cathepsin, autophagy, unfolded-protein-response, and integrated-stress-response programs and weak or divergent same-complex comparisons. A `Rab7` counterexample is important because the focal DE assay clearly can detect a broad endolysosomal response: `Rab7` loss up-regulated `Atp6v0a1`, `Atp6v0c`, `Atp6v1a`, `Atp6v1b2`, `Lamp1`, `Lamp2`, `Ctsd`, `Ddit3`, and `Sqstm1` in `151 TH Prkcd Grin2c Glut`. Therefore the near-null V-ATPase counts are not just because lysosomal transcripts were unmeasurable.

## Target-specific reasoning

### Atp6v0c

`Atp6v0c` encodes the V0 c-ring proteolipid, an obligate membrane-sector component of the rotary V-ATPase proton pump. It is biologically close to `Atp6v0a1`: ATP6V0A1 supplies the neuronally enriched V0 a-subunit that works with the c ring to move protons, while the c subunit itself has also been biochemically associated with synaptobrevin/synaptophysin-containing synaptic-vesicle complexes and with VAMP2-dependent neurotransmitter release. External biology therefore argues that real ATP6V0C loss could perturb vesicle acidification, endolysosomal acidification, and synaptic release.

The quantitative evidence from this exact CRISPR/snRNA-seq endpoint points the other way for DEG breadth. Direct `Atp6v0a1` perturbation in `151 TH Prkcd Grin2c Glut` produced only one counted DEG, the self transcript; `Atp6ap2`, a V-ATPase accessory factor, produced two DEGs; three V1 subunit perturbations had zero focal DEGs. None of those close analogs activated a focal TFEB, lysosome, autophagy, UPR, ISR, or coordinated synaptic-compensation program, and their full score vectors barely correlated. More distal endolysosomal genes such as `Rab7`, `Vps35`, and `Vps54` gave larger DEG counts but are not same-intervention analogs: they change vesicle trafficking and lysosomal biogenesis from outside the proton pump, and `Rab7` in fact drives a compensatory V-ATPase/lysosome mRNA program not seen after direct V-ATPase subunit loss.

My causal model was: AAV CRISPR disrupts `Atp6v0c` in a mosaic subset of P16 neurons; surviving edited neurons may lose c-ring protein and weaken V0 proton pumping or V0/SNARE coupling; acidification or exocytosis defects could propagate to lysosomal, synaptic, ISR, or TFEB-dependent nuclear programs; only nuclei still present and classified at P37-P44 contribute to the Wilcoxon test. The held-in V0 and V1 subunits show that in this assay the propagation-to-nuclear-DE step was buffered or survivor-conditioned, even for an obligate complex. I therefore did not transfer the 501-gene `Rab7` response to `Atp6v0c`; the relevant same-complex intervention predicts the same near-zero endpoint as `Atp6v0a1`.

I nevertheless made the point prediction slightly above a strict null. `Atp6v0c` is measured in the focal Parquet rows, and the nearest V0 analog, `Atp6v0a1`, crossed FDR solely through its own guide-induced RNA loss. Because the requested `n_degs` includes self-target transcripts and because the closest membrane-sector analog had exactly one DEG, the best integer prediction is `1`: a likely isolated `Atp6v0c` self-transcript hit with no broad downstream transcriptional program.

## Limits

The prediction is a narrow assay prediction, not a claim that ATP6V0C is biologically inert. The Parquet does not measure edited allele fraction, ATP6V0C protein, lysosomal or synaptic-vesicle pH, neurotransmitter release, autophagic flux, mTORC1 activity, or depletion of edited neurons before snRNA-seq. Complete or pharmacologic V-ATPase collapse should not be equated with the postnatal, sparse, mosaic CRISPR perturbation used here. `Atp6v0c` may differ from `Atp6v0a1` because it is the c-ring proteolipid rather than an a-isoform; conversely, target mRNA detectability and guide placement could move the observed count from 1 to 0. The prediction is therefore strongest for the qualitative "zero or one DEG, no large stress signature" decision and weakest for the exact self-hit integer.
