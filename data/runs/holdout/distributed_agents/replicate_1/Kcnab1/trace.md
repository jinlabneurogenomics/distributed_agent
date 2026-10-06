# Kcnab1 DEG-count prediction

## Question and resolved ambiguities

The requested held-out perturbation set contained one target:

- `Kcnab1`

I interpreted `predicted_n_degs` as the integer number of measured genes expected to have
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after the same P16 sparse
AAV-PHP.eB CRISPR loss-of-function design used in the PerturbAI atlas. The focal cell
label was treated as the thalamic glutamatergic group named exactly in the dataset; `TH`
was not interpreted as tyrosine hydroxylase. The held-out endpoint is absent for Kcnab1
by construction, but Kcnab1 remained a measured transcript in the non-held-out DE rows.

## Sources

- Declared focal training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE table:
  `training differential-expression dataset`.
- Run-local dataset portrait, task bindings, capability manifest, and measurement
  registry under `codex_runtime/pipeline`.
- Same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through the declared
  `corpus.findings` and `corpus.report_evidence` tools for Kcnab2, Kcna1, Kcna2,
  and Cacna1a.
- External mechanism priors from PubMed-indexed literature:
  Sewing et al. 1996, DOI `10.1016/S0896-6273(00)80063-X`, PMID 8789960;
  Heinemann et al. 1996, DOI `10.1113/jphysiol.1996.sp021409`, PMID 8799886;
  Campomanes et al. 2001, DOI `10.1074/jbc.M110276200`, PMID 11748234;
  McCormack et al. 2002, PMID 11825900; Connor et al. 2005,
  DOI `10.1111/j.1601-183X.2004.00094.x`, PMID 15720404; Dwenger et al. 2022,
  PMID 35883673; Yee et al. 2022, PMID 35788155.

External literature was used to decide which visible potassium-channel perturbations are
mechanistically interpretable analogs. The count magnitude itself came from the local
training endpoint and focal DE rows.

## Dataset calculations

I first summarized the focal training counts. There were 1,674 non-held-out targets.
The distribution was heavily zero-inflated: 1,205 targets had `n_degs = 0`, 1,481 had
`n_degs <= 1`, the median was 0, the mean was 14.1, and the maximum was 2,677.

The potassium-, sodium-, calcium-, and HCN-channel targets present in the focal training
CSV were mostly null or self-only:

| target class | focal training counts |
| --- | --- |
| closest Kv1/Kv-beta | Kcnab2 1, Kcna1 0, Kcna2 0 |
| broader potassium channels | Kcnb1 0, Kcnb2 0, Kcnc1 0, Kcnc2 1, Kcnc3 1, Kcnd3 0, Kcnh1 0, Kcnh5 0, Kcnj6 0, Kcnma1 1, Kcnn2 0, Kcnn3 0, Kcnq2 1, Kcnq3 1, Kcnt1 0, Kcnt2 0 |
| other excitability channels | Scn1a 1, Scn1b 2, Scn2a 1, Scn3a 0, Scn8a 1, Cacna1a 0, Cacna1d 0, Cacna1e 0, Cacna1g 12, Cacna2d1 1, Cacna2d2 0, Hcn1 0, Hcn2 1 |

To inspect the expression-pattern evidence behind those counts, I filtered the Parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and visible analog `gene_target` values. The
operation was a predicate-filtered Parquet scan over the declared input, restricted to
`names`, Wilcoxon statistics, adjusted p values, and matched-cell columns:

```python
filter = (
    (field("group_name") == "151 TH Prkcd Grin2c Glut")
    & field("gene_target").isin(visible_ion_channel_analogs)
)
```

The closest visible analog, `Kcnab2`, had 227 matched perturbed nuclei against 23,679
controls in 151 cells. Its sole `pvals_adj < 0.05` row was the self transcript:
Kcnab2 log2 fold change -0.744, Wilcoxon score -8.73, `pvals_adj = 4.38e-14`.
The next rows, `Cdk5r1` and `Extl3`, were only FDR 0.302. `Kcna1` had 119 matched
perturbed nuclei and 0 focal DEGs; its best row was `Ppp1r16a`, FDR 0.357. `Kcna2`
had 113 matched perturbed nuclei and 0 focal DEGs; every tested row had FDR 1.0.

I also checked Kcnab1, Kcnab2, Kcna1, Kcna2, Fos, Jun, and Egr1 rows inside the focal
surfaces of the visible ion-channel analogs. Neither `Kcna1` nor `Kcna2` perturbed the
Kcnab1/Kcnab2/Kcna1/Kcna2 neighborhood or the canonical immediate-early sentinels.
`Kcnab2` depletion likewise did not change Kcnab1, Kcna1, Kcna2, Fos, Jun, or Egr1
at FDR level; all had `pvals_adj = 1`.

## Target-specific reasoning

### Kcnab1

`Kcnab1` encodes a cytosolic voltage-gated potassium-channel beta subunit. Kv-beta
proteins bind Shaker-related Kv1 alpha subunits and modulate Kv1 assembly, surface
trafficking, axonal targeting, gating, and inactivation rather than acting as classical
transcriptional regulators. Sewing et al. mapped Kv-beta-1 binding to Kv1/Shaker alpha
subunits; Heinemann et al. showed that Kv-beta-1.1 induces fast inactivation on several
Kv1 channels; Campomanes et al. linked Kv-beta subunits to Kv1.2 trafficking and axonal
targeting in hippocampal neurons. McCormack et al. and Connor et al. established that
loss of the closely related Kcnab2/Kv-beta-2 in mice has nervous-system phenotypes, and
Connor et al. further showed that Kcnab1.1 loss can modify the Kcnab2-null phenotype.
Thus Kcnab2, Kcna1, and Kcna2 are the correct visible local analogs: they intervene on
the same Kv1 auxiliary or pore-forming channel complexes.

The intervention chain I used was:

`Kcnab1 CRISPR loss -> reduced Kv-beta-1 contribution to Kv1 channel gating and
inactivation -> altered axonal/somatic excitability in neurons that use those complexes
-> possible activity-dependent nuclear adaptation -> Wilcoxon DE among recovered 151
nuclei`.

The first two steps are biologically credible, but the last step is weak in this assay.
The same-experiment Kcnab2 corpus report summarized 22 recovered neuronal groups with
uniformly negative Kcnab2 self-transcript shifts, significant Kcnab2 RNA loss in five
groups, and 0 downstream genes at FDR 0.10. In the exact focal cell group, Kcnab2 was
strongly self-depleted but had no downstream FDR 0.10 genes. The report also explicitly
tested activity-regulated genes, including Fos, Junb, Egr1, Egr2, Npas4, Arc, Bdnf, Vgf,
Scg2, and Homer1, and found FDR 1.0 for all of them in every measured Kcnab2 cell group.
The Kcna1 and Kcna2 reports reached the same conclusion from the pore-forming side of
the channel complex: Kcna1 produced no downstream FDR genes in 22 groups, while Kcna2
produced just one weak singleton, Man1a2 in `110 CNU-HYa HY MM Glut`, and neither
produced a shared Kv1-like nuclear program. Those nulls are imperfect because axonal
currents, channel localization, seizure susceptibility, and spike timing were not
measured, but they are directly matched to the P16 mosaic CRISPR/single-nucleus RNA
readout and to the visible perturbation geometry.

Broader counterexamples reinforced that a dramatic 151-cell response should not be
expected from this class. Focal counts for Kcnb1, Kcnb2, Kcnc1, Kcnd3, Kcnh1, Kcnh5,
Kcnn2, Kcnn3, Kcnt1, Kcnt2, Cacna1a, Cacna1d, Cacna1e, Hcn1, and Scn3a were all zero.
Other ion-channel genes such as Kcnc2, Kcnc3, Kcnq2, Kcnq3, Scn1a, Scn2a, Scn8a, and
Hcn2 mostly registered only their self-transcript as the FDR 0.05 event in the 151
group. `Scn1b` had one downstream hit, Jun, and `Cacna1g` was the clearest exception
with 12 focal DEGs, so the screen can see a durable activity-related state for a subset
of channels. Kcnab1 nevertheless belongs much closer to the Kcnab2/Kcna1/Kcna2 Kv1
axis than to the exceptional Cacna1g response.

My zero/nonzero decision is therefore:

- Downstream 151-cell response: predict zero detectable downstream genes. The
  within-dataset Kv1 beta and alpha analogs were flat, and external Kv-beta biology
  predicts a primary electrophysiological/channel-localization endpoint rather than a
  direct gene-expression program.
- Self transcript: allow one possible counted DEG. Kcnab1 is present as a measured
  transcript in the 151 surfaces, and the training endpoint counts self rows. The only
  significant Kcnab2 row in the focal group was its own transcript; several other
  channel genes with otherwise flat focal surfaces behaved similarly. Kcnab1 may be
  less robust than Kcnab2 because Kv-beta-2 is the predominant mammalian nervous-system
  beta subunit, so this is not a high-confidence self-hit.

I set `Kcnab1` to **1 DEG**, effectively a self-only prediction with no broad secondary
signature.

## Limits

- Kcnab1 itself was held out: its true 151-cell matched nucleus count, target mRNA
  change, and complete DE signature are not in the supplied inputs.
- Kcnab2 is the closest visible paralog, but Kcnab1 isoforms and Kv-beta-2 are not
  interchangeable; Kcnab2 is more broadly predominant in mammalian nervous system, while
  Kcnab1 may be more cell-type or isoform restricted.
- The main biology of Kv1 alpha/beta complexes is electrical and subcellular. This
  snRNA-seq endpoint misses fast channel gating, axonal localization, action-potential
  changes, transmitter release, and seizure/circuit phenotypes.
- The prediction of one DEG relies on expected self-transcript detectability, not on a
  downstream expression program. If the Kcnab1 self transcript was not significantly
  depleted in recovered 151 nuclei, the expected count would collapse to zero.
