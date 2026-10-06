# Gad1 held-out DEG-count prediction trace

## Question and resolved ambiguities

The held-out manifest for this run contains one target:

```text
Gad1
```

I interpreted the requested endpoint as the integer number of measured genes with
`pvals_adj < 0.05` in the parquet rows where
`group_name == "151 TH Prkcd Grin2c Glut"` after a sparse, acute,
postnatal AAV-CRISPR loss-of-function perturbation of the requested target.
The held-out target itself was absent as a `gene_target`, so I did not use a
`Gad1` perturbation signature. I treated self-transcript DE in training
perturbations as assay evidence, but not as a required endpoint: the requested
count is the number of all FDR 0.05 genes, whether or not a self row is one of
them.

## Sources used

Internal, experiment-matched sources:

- `training_de_all_cell_groups.parquet`
  - Queried the focal cell group for mechanistic analogs of `Gad1`.
  - Queried `Gad1`, `Gad2`, `Slc32a1`, `Slc6a1`, and `Abat` as measured genes
    across all 1,674 non-held-out perturbations in the focal group.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - Used the observed FDR 0.05 DEG counts for all 1,674 non-held-out
    perturbations in the focal cell group.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`
  - `target_context(Gad2)` for same-experiment evidence that `Gad2` was
    effectively self-only and did not induce a robust downstream RNA program.
  - `target_context(Slc32a1)` for same-experiment evidence that VGAT loss was
    a downstream pan-null and that synaptic-vesicle/GABA-handling perturbations
    did not converge on a robust RNA module.
  - `target_context(Abat)` for the boundary case that GABA catabolism produced
    only a singleton, Pvalb-restricted FDR 0.10 signal and was flat in
    `151 TH Prkcd Grin2c Glut`.
  - `target_context(Gabrb2)` as the main counterexample showing that this focal
    cell group can report a small GABA_A receptor-linked activity program.
  - `target_context(Dlx6)` for a developmental GABAergic-transcription-factor
    counterexample.
- Distributed Agents runtime profile comparison
  - Ran an explicit profile comparison in
    `151 TH Prkcd Grin2c Glut` over `Gad2`, `Slc32a1`, `Slc6a1`, `Abat`, `Gls`,
    represented GABA receptor subunits, `Arhgef9`, `Dlx6`, `Arx`, and `Mef2c`
    using signed Wilcoxon `scores`, `pvals_adj < 0.05`, and the full
    training-count target universe.

External biology sources:

- Asada et al., 1997, PNAS, DOI `10.1073/pnas.94.12.6496`, PMID `9177246`:
  conventional mouse `Gad1`/GAD67 loss greatly reduces neonatal cortical GABA
  but causes perinatal cleft palate rather than a broad reported postnatal
  neuronal transcriptional phenotype.
- Obata et al., 2008, BBRC, DOI `10.1016/j.bbrc.2008.03.110`, PMID `18384748`:
  conditional postnatal cerebellar GAD67 deletion reduces GABA and impairs
  inhibitory synaptic transmission without grossly changing Purkinje-cell
  morphology or synaptic-terminal density.
- Kakizaki et al., 2014, Neuroscience, DOI
  `10.1016/j.neuroscience.2014.12.030`, PMID `25545713`: `Gad1`/GAD67 and
  `Gad2`/GAD65 jointly account for brain GABA synthesis in knockout models.
- Le et al., 2017, Journal of Neuroscience, DOI
  `10.1523/JNEUROSCI.2125-16.2017`, PMID `28821666`: `Dlx1` and `Dlx2`
  directly regulate `Gad1` and `Gad2` during embryonic forebrain GABAergic
  differentiation.

## Computational summary

I first read the training-count CSV. The focal endpoint is very sparse:

- 1,674 observed training perturbations.
- 1,205 had `0` DEGs at FDR 0.05.
- The median target had `0` DEGs and the 75th percentile was `1`.
- Large responses were dominated by core chromatin, RNA-processing,
  proteostasis, transcription, and viability-adjacent perturbations such as
  `Uba5` with 2,677 DEGs, `Tpr` with 1,768, and `Sin3a` with 1,433.

I then queried only the focal cell group from the parquet for available
GABA-synthesis, GABA vesicle-loading/reuptake/catabolism, GABA receptor, and
GABA developmental-regulator perturbations. Counts from those rows reproduced
the training-count CSV and gave the matched positive and negative controls:

| training target | focal FDR 0.05 DEGs | relevant interpretation |
| --- | ---: | --- |
| `Gad2` | 0 | closest assayed paralog; GAD65 catalyzes the same glutamate-to-GABA reaction |
| `Slc32a1` | 0 | vesicular inhibitory amino-acid transporter/VGAT, downstream of GABA synthesis |
| `Slc6a1` | 0 | neuronal GABA reuptake transporter/GAT1 |
| `Abat` | 0 | GABA catabolism; focal `Abat` self row had `pvals_adj = 0.831` |
| `Gls` | 0 | produces glutamate, the substrate for GAD enzymes |
| `Dlx6` | 0 | assayed DLX-family GABAergic developmental regulator; did not move `Gad1` in this focal group |
| `Arx` | 0 | forebrain GABAergic developmental regulator, but embryonic and not `Gad1`-proximal in this assay |
| `Nkx2-1` | 0 | MGE/Pvalb-Sst developmental regulator, null in this focal group |
| `Gabra2` | 0 | GABA_A alpha subunit |
| `Gabra3` | 0 | GABA_A alpha subunit |
| `Gabra5` | 0 | GABA_A alpha subunit |
| `Gabrb1` | 0 | GABA_A beta subunit |
| `Gabrb3` | 0 | GABA_A beta subunit |
| `Gabrg3` | 0 | GABA_A gamma subunit |
| `Gabrr2` | 0 | GABA_A-rho receptor subunit |
| `Gphn` | 0 | inhibitory postsynaptic scaffold |
| `Gabra1` | 1 | only its self row, despite strong `Gabra1` RNA reduction |
| `Gabrg2` | 1 | only its self row, despite strong `Gabrg2` RNA reduction |
| `Gabbr1` | 1 | only its self row at FDR 0.05 |
| `Gabbr2` | 1 | only its self row at FDR 0.05 |
| `Arhgef9` | 1 | only its self row, a collybistin inhibitory-synapse scaffold |
| `Mef2c` | 1 | only its self row at FDR 0.05 in the focal group |
| `Gabrb2` | 4 | small positive-control GABA_A beta2 response: self-down plus `Nr4a1`, `Vgf`, `Nalf1` |
| `Gabrd` | 2 | self-down plus one downstream gene |

The GABA_A/GABA_B positive controls were deliberately treated as
counterexamples, not as direct analogs. `Gabrb2` had a focal-cell response
consistent with altered postsynaptic inhibition and an activity-like program:
`Nr4a1` and `Vgf` passed FDR 0.05 and `Fos`, `Npas4`, and `Homer2` were just
above that threshold at FDR 0.056 to 0.058. However, the more direct
presynaptic and metabolic targets all had zero FDR 0.05 genes in the same
focal group.

Two additional parquet checks were informative:

- `Gad1` was not significantly changed as a measured transcript by any of the
  1,674 training perturbations in `151 TH Prkcd Grin2c Glut`; its best adjusted
  p-value anywhere in the focal group was `0.9089`.
- The expected GABA-handling marker rows stayed null under direct pathway
  perturbations in the focal group. For example, under `Gad2`, every queried
  marker row among `Gad1`, `Gad2`, `Slc32a1`, `Slc6a1`, `Abat`, `Gls`, `Vgf`,
  `Nr4a1`, `Fos`, `Npas4`, `Homer2`, `Bdnf`, `Arc`, and `Egr1` had
  `pvals_adj = 1.0`.

The runtime profile comparison gave the same boundary. In the focal group,
`Gad2`, `Slc32a1`, `Slc6a1`, and `Abat` had zero significant features, and
their signed Wilcoxon-score profiles had near-zero cosine/pearson similarity
to the receptor positive control `Gabrb2` and to `Dlx6`. This argues against a
weak hidden GABA-synthesis module under the FDR threshold.

## Target-specific reasoning

### Gad1

`Gad1` encodes GAD67, one of the two glutamate decarboxylases that synthesize
GABA from glutamate; `Gad2` encodes GAD65. Complete developmental loss of
GAD67 or combined GAD65/GAD67 loss greatly lowers brain GABA and causes
developmental phenotypes in mice or rats (Asada et al. 1997; Kakizaki et al.
2014; Jiang et al. 2022), so this is a genuine GABA-synthesis enzyme, not a
biologically inert gene. That external prior by itself is not enough to
predict a focal snRNA-seq response, because the requested assay cut single
genes sparsely at P16 and read out nuclear RNA in postmitotic neurons at
P37-P44 rather than deleting both isoforms during GABAergic specification.

The closest direct comparator is `Gad2`. Its focal endpoint was exactly
`0` DEGs. In the Distributed Agents same-experiment corpus, `Gad2` produced target-RNA
loss only in inhibitory neuron classes and no significant self-drop in any
glutamatergic group; a full-universe signature-neighbor search found no
meaningful `Gad2` neighbors, with best whole-profile correlations only around
noise scale. That is highly relevant because `151 TH Prkcd Grin2c Glut` is a
glutamatergic thalamic group and is therefore a transmitter mismatch for
GAD65/GAD67 biology.

The next most relevant available perturbations also point to zero:
`Slc32a1`/VGAT, `Slc6a1`/GAT1, `Abat`, and `Gls` all had `0` focal FDR 0.05
genes. Corpus findings for `Slc32a1` describe a downstream pan-null across 23
cell groups despite target-transcript reductions in inhibitory classes, and
the `Gad2` and `Abat` findings explicitly note that GABA synthesis, vesicular
loading, reuptake, catabolism, glutaminase, GABA_A, and GABA_B perturbations
did not form a shared robust nuclear RNA program. This is the strongest
within-dataset evidence: perturbing the assayed steps adjacent to `Gad1` in
GABA production and vesicle filling generally remained transcriptionally
silent in the same Perturb-seq experiment.

The main counterexample is `Gabrb2`, which had `4` FDR 0.05 genes in the focal
group and an FDR 0.10 activity-associated program led by `Nr4a1`, `Vgf`,
`Fos`, `Npas4`, and `Homer2`. I did not transfer this count to `Gad1` because
`Gabrb2` is postsynaptic in a GABA_A receptor complex and showed a
subunit-specific receptor response: `Gabra1`, `Gabrg2`, `Gabbr1`, `Gabbr2`,
and `Arhgef9` all had significant self-transcript drops or near self-only
responses in the focal group without the multi-gene `Gabrb2` activity program.
If even receptor-complex membership was not exchangeable for `Gabrb2`, a
presynaptic GABA-synthesis enzyme in a glutamatergic group is a weaker match.

I also considered a developmental-transcription-factor route in which `Gad1`
could be an endpoint of DLX-family regulation. Le et al. 2017 showed that
DLX1/DLX2 directly activate `Gad1` and `Gad2` during forebrain GABAergic
differentiation, but the represented postnatal proxies were null here:
`Dlx6`, `Dlx3`, `Arx`, `Nkx2-1`, and `Six3` each had `0` focal FDR 0.05 genes.
The `Dlx6` Distributed Agents finding specifically reported that expected forebrain
GABAergic markers including `Gad1`, `Gad2`, and `Slc32a1` were nonsignificant
after postnatal singleton `Dlx6` loss. That makes embryonic DLX-GAD regulation
an imperfect extrapolation for the P16-to-P37/P44 sparse perturbation.

Taken together, I expect `Gad1` loss to look at least as quiet as `Gad2` in
`151 TH Prkcd Grin2c Glut`: the focal cells are annotated glutamatergic, the
measured `Gad1` row never became differentially expressed under any training
perturbation in these cells, and the within-assay metabolic/presynaptic GABA
axis is all zero at FDR 0.05. The point prediction is therefore `0`.

## Limits of the reasoning

This prediction is much stronger for a cell-autonomous nuclear RNA endpoint
than for GABA biology in general. The experiment did not assay DNA indels,
GAD67 protein, GABA content, vesicle filling, inhibitory postsynaptic currents,
network activity, or behavior. Mosaic P16 loss can also be buffered by
remaining GAD65/GAD67 protein or by the paralogous enzyme in cells that express
both.

`Gad1` itself was held out, `Gad2` is a close but not identical isoform, and
the focal cell group is a glutamatergic thalamic cluster rather than the
GABAergic cells where Gad enzymes are most abundant. Developmental literature
on `Gad1`, `Dlx1/2`, and GABAergic specification is largely embryonic and
germline or conditional, so I treated it as mechanism-setting background and
let the postnatal Perturb-seq analogs drive the final zero/nonzero call.
