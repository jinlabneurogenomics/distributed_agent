# Reasoning trace

## Question and resolved ambiguities

I predicted the held-out endpoint `n_degs` for the requested target in `151 TH Prkcd Grin2c Glut` cells. I interpreted `n_degs` as the number of measured genes whose `pvals_adj` in the focal cell group would be below 0.05 after acute P16 AAV-CRISPR loss of the target, with log fold changes in the parquet defined as perturbed over matched control.

The manifest for this run contains one held-out perturbation:

```tsv
target_name
Ppargc1b
```

The `TH` token in the focal cell label is the atlas abbreviation for thalamus, not tyrosine hydroxylase. I treated the endpoint as an assay-specific DEG count, not a direct measure of mitochondrial importance or guide activity.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: scalar `n_degs` labels for 1,674 non-held-out training perturbations in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`: per-gene Wilcoxon statistics used to inspect expression signatures of measured analogs and counterexamples.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`: `Ppargc1b` itself was not covered, but target contexts for `Ppargc1a`, `Esrra`, and `Nrf1` summarized the matched perturbation reports and cross-perturbation contrasts within the same atlas.
- Distributed Agents runtime `profile_neighbors`: I compared the focal-cell Wilcoxon-score profiles for a small declared analog set. This showed weak rather than tight whole-profile similarity among `Ppargc1a`, `Esrra`, `Nrf1`, `Opa1`, ESRR paralogs, PPAR receptors, NFE2L factors, and a few respiratory-chain genes, so I treated the analogs individually instead of pooling them.
- NCBI PubMed via `bioeval_literature` for external PGC-1 beta biology:
  - Lin et al. 2001, J. Biol. Chem., DOI `10.1074/jbc.C100631200`, PMID `11733490`: cloning of `PGC-1beta`/`Ppargc1b` as a `PGC-1alpha` homolog and nuclear-receptor coactivator.
  - Lelliott et al. 2006, PLoS Biology, DOI `10.1371/journal.pbio.0040369`, PMID `17090215`: germline PGC-1 beta loss perturbs basal mitochondrial gene expression and tissue metabolic responses in mouse.
  - Sonoda et al. 2007, PNAS, DOI `10.1073/pnas.0611623104`, PMID `17360356`: PGC-1 beta knockout alters nuclear-encoded mitochondrial and metabolic transcripts in several tissues including brain.
  - Scarpulla 2008, Physiological Reviews, DOI `10.1152/physrev.00025.2007`, PMID `18391175`: review of the PGC-1/ERR/NRF transcriptional network for nuclear-mitochondrial coordination.
  - Rowe et al. 2011, Am. J. Physiol. Endocrinol. Metab., DOI `10.1152/ajpendo.00681.2010`, PMID `21364124`: PGC-1 beta can require ERRalpha coactivation for a VEGF/angiogenic oxidative-metabolism program in skeletal muscle.

## Computational evidence from the training data

The focal training endpoint is strongly zero-inflated:

- 1,674 training targets
- 1,205 targets with `n_degs = 0`
- median `n_degs = 0`
- 90th percentile `n_degs = 2`
- 95th percentile `n_degs = 18`
- maximum `n_degs = 2677`

I then looked up measured perturbations in the PGC/ERR/PPAR/NRF and mitochondrial neighborhoods in the same training-count file:

```tsv
target_name	n_degs
Ppargc1a	0
Esrra	57
Esrrb	0
Esrrg	0
Nrf1	138
Nfe2l1	0
Nfe2l2	0
Ppara	0
Ppard	0
Pparg	0
Opa1	37
Rxra	0
Rxrb	0
Rxrg	0
Ncoa1	0
Ncoa3	0
Clpp	0
Lonp1	0
Yme1l1	0
Ndufs4	0
```

Most measured complex-I and complex-IV structural perturbations were also 0 or singleton self-target calls in the focal cell group. That is an important counterweight to a generic "mitochondrial genes are visible" transfer: `Esrra`, `Nrf1`, and `Opa1` were specific exceptions rather than representatives of a uniformly responsive mitochondrial class.

For expression-pattern evidence I filtered the full parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to a hand-built target list of measured analogs/counterexamples. The filtering was simple predicate pushdown:

```python
filt = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(targets)
```

Selected focal profiles:

```tsv
target_name	n_degs	n_pert_matched	top_focal_FDR_hits
Ppargc1a	0	135	none; strongest ranks included Bcan, Atp5b, Idh3a, Atp1b1, all FDR > 0.18
Esrra	57	275	Gas6, Bcan, Nceh1, Nsg2, Mdh1, Atp1b1, Atp2b3, Esrra
Nrf1	138	222	Snhg11, Rsrp1, Nrsn2, Kifc2, Haghl, Msra, Fam98a, Sdha
Opa1	37	195	Asns, Mars1, Chac1, Ddit3, Cars, Opa1, Mthfd2, Basp1
Esrrb	0	209	none; all adjusted p-values 1.0
Esrrg	0	183	none; all adjusted p-values 1.0
Ppara	0	158	none; all adjusted p-values 1.0
Ppard	0	315	none; all adjusted p-values 1.0
Pparg	0	109	none; all adjusted p-values 1.0
Nfe2l1	0	157	none; strongest q = 0.06198
Nfe2l2	0	207	none; strongest q = 0.367
```

The significant FDR < 0.05 gene sets were not a single common oxidative-stress program: `Esrra` and `Nrf1` shared only four significant genes (`Cntnap1`, `Hook1`, `Ptpn3`, `Tecr`), while `Opa1` shared no significant genes with either `Esrra` or `Nrf1`. `Ppargc1a` was empty by construction in this thresholded comparison.

The Distributed Agents same-experiment corpus made the same point at the report level. Its `Ppargc1a:F002`, `Esrra:F005`, and `Nrf1:F007` findings support the claim that the represented ERR/PGC/PPAR/NRF mitochondrial network was transcriptionally node-specific in juvenile neuronal nuclei: `Esrra` loss produced a detectable partial oxidative-metabolism signature, but `Ppargc1a`, ESRR paralogs, PPAR neighbors, and `Nrf1`-related perturbations were flat or divergent rather than interchangeable single-perturbation phenocopies.

## Target-specific reasoning for Ppargc1b

`Ppargc1b` encodes PGC-1 beta, a non-DNA-binding transcriptional coactivator in the PGC-1 family. External literature says it is a bona fide `Ppargc1a` homolog and can coactivate nuclear receptors such as PPARalpha; the broader PGC-1 coactivator family regulates mitochondrial biogenesis through transcription factors including NRF-1 and ERRalpha. Germline PGC-1 beta knockout mice have altered mitochondrial/metabolic gene expression across tissues, and at least some PGC-1 beta effector programs require ERRalpha in metabolic tissue models. Those observations made a nonzero response biologically plausible before looking at this dataset.

The closest assayed paralog and mechanistic counterweight was `Ppargc1a`, with `n_degs = 0` in the focal 151 group despite 135 matched perturbed nuclei and analyzable focal-cell rows. `Ppargc1a` is not `Ppargc1b`, but it is the same coactivator family, lacks an obligate DNA-binding specificity of its own, and was also flat throughout the corpus reports. Because acute AAV-CRISPR in this experiment produces a mild mosaic lesion, a single coactivator perturbation can be buffered by residual protein, by PGC-family redundancy, or by the fact that basal juvenile thalamic neurons are not in an exercise/cold/fasting-like induction state.

`Esrra` was the strongest direct transcription-factor partner analog, with 57 DEGs in 151 cells. Its signature down-regulated `Gas6`, `Bcan`, `Mdh1`, `Atp1b1`, `Atp2b3`, `Slc1a1`, and the target transcript itself and included a partial metabolic/adhesion state. This proves that an ERR/PGC-linked nuclear receptor can be detected in the focal group, but the same corpus explicitly found that `Esrrb`, `Esrrg`, `Ppargc1a`, `Ppara`, `Ppard`, and `Pparg` did not phenocopy `Esrra`. Therefore I used `Esrra` to establish assay detectability and an upper bound for a direct ERRalpha perturbation, not as a direct scalar transfer to `Ppargc1b`.

`Nrf1` had an even larger focal count, 138, but its FDR genes were dominated by `Snhg11`, `Rsrp1`, `Nrsn2`, `Kifc2`, `Haghl`, `Msra`, and only a small mitochondrial strand such as `Sdha`. It shared only four FDR < 0.05 genes with `Esrra`. The Distributed Agents corpus also emphasized that `Nrf1` diverged from `Ppargc1a`, `Esrra`, and `Esrrg`, so this is not an assay-internal argument that loss of any upstream PGC-family coactivator should yield around 100 DEGs.

I treated `Opa1` as a mitochondrial-stress counterexample. Its 37-gene response was a CHOP/ISR-like up-regulation of `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2`, and amino-acid transport or tRNA-synthetase genes, which is mechanistically downstream of mitochondrial dynamics stress rather than a PGC/ERR basal transcriptional program. Numerous more proximal respiratory-chain targets were 0 or one self-target DEG, so `Opa1` did not justify lifting `Ppargc1b` above zero.

Putting these together, the zero/nonzero decision was driven mostly by assay-internal evidence. PGC-1 beta is connected to mitochondrial transcription, but every measured single PPAR/RXR receptor and the assayed PGC-1alpha paralog were exact zeros in the same 151-cell endpoint, while the two positive transcription-factor comparators were divergent direct DNA-binding nodes. The external PGC-1 beta literature is real but mostly from germline, metabolic-tissue, stress, or overexpression settings rather than sparse P16 loss in recovered NeuN+ thalamic nuclei. I therefore predict that acute `Ppargc1b` loss will not yield any genes passing Benjamini-Hochberg FDR 0.05 in the focal group.

Final point prediction:

```tsv
target_name	predicted_n_degs
Ppargc1b	0
```

## Limits

- `Ppargc1b` itself was held out from the parquet and absent from the selected Distributed Agents corpus, so all evidence is transferred from measured neighbors.
- The best measured analog, `Ppargc1a`, is a paralog rather than an exact substitute; PGC-1 beta has a stronger basal mitochondrial role than PGC-1 alpha in some tissues.
- `Esrra` and `Nrf1` show that the focal group can expose mitochondrial transcriptional regulators, so a small `Ppargc1b` response is plausible even though I predict zero.
- Whole-body and tissue-specific knockout papers involve development, chronic adaptation, metabolic organs, or challenge states. They may overstate the response to mild mosaic CRISPR loss in juvenile postmitotic neurons, but they also show functions that snRNA-seq at 3-4 weeks could miss.
- `n_degs` is thresholded and power-sensitive. A prediction of 0 means I expect no gene to cross adjusted p < 0.05, not that PGC-1 beta is biologically irrelevant in these neurons.
