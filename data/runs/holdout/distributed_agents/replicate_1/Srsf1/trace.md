# Prediction trace

## Question interpreted

The task asks for the held-out value of `n_degs` for each requested perturbation
in the focal `151 TH Prkcd Grin2c Glut` cell group. Here `n_degs` means the
number of measured genes with Benjamini-Hochberg-adjusted Wilcoxon
`pvals_adj < 0.05` in perturbed nuclei versus matched controls. The sole
requested held-out perturbation is `Srsf1`; it is absent as a perturbation
target from both the differential-expression Parquet and the focal
training-count CSV, so the endpoint for `Srsf1` is not directly observed in the
declared inputs.

I treated the focal training-count CSV as the directly observed endpoint for
non-held-out targets. I treated the Parquet as direct evidence for expression
signatures of those visible targets. I treated the July 260713 SourceGuard v1
PerturbAI corpus as a same-experiment interpretation layer, not as independent
replication. Literature on SR proteins and transportin-SR2 was used only to
decide which visible perturbations are mechanistically transferable to `Srsf1`.
I did not use self-target RNA reduction as an editing-efficiency score.

## Sources used

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE table:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Srsf1`.
- Internal same-experiment corpus: PerturbAI July 260713 SourceGuard 1773 v1.
  I used bounded Finding records for `U2af2`, `Tnpo3`, and `Snrnp70` to check
  the packaged interpretation of RNA-processing comparator relationships.
- External literature:
  Long and Caceres 2009, DOI 10.1042/BJ20081501 / PMID 19061484; Shepard and
  Hertel 2009, DOI 10.1186/gb-2009-10-10-242 / PMID 19857271; Kataoka,
  Bachorik and Dreyfuss 1999, DOI 10.1083/jcb.145.6.1145 / PMID 10366588; Lai,
  Lin and Tarn 2001, DOI 10.1073/pnas.181354098 / PMID 11517331; Maertens et
  al. 2014, DOI 10.1073/pnas.1320755111 / PMID 24449914; Kanadia et al. 2008,
  DOI 10.1242/dev.024620 / PMID 18987029.

## Quantitative calibration from the declared inputs

The held-out list had one row, `Srsf1`. The focal training table had 1,674
unique visible perturbations. It was heavily zero-inflated: 469/1,674 visible
targets were nonzero, the median was 0, the 75th percentile was 1, the 95th
percentile was 18, and the maximum was 2,677. Therefore an `Srsf1` prediction
cannot be set from a smooth global average; it has to be assigned by transfer
from the small set of visible perturbations that plausibly stress the same RNA
biogenesis machinery.

I filtered the Parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and
counted rows with `pvals_adj < 0.05` for visible RNA-processing targets. The
counts exactly matched the supplied training CSV for every target checked.

| visible target | focal `n_degs` | relationship to `Srsf1` |
|---|---:|---|
| `U2af2` | 828 | core U2AF 3-prime splice-site factor |
| `Rnpc3` | 868 | core minor-spliceosome factor |
| `Tnpo3` | 618 | nuclear import receptor for phosphorylated SR proteins including SRSF1 |
| `Cdc40` | 624 | spliceosome-associated pre-mRNA processing factor |
| `Prpf6` | 454 | U4/U6-U5 tri-snRNP spliceosome factor |
| `Snrnp70` | 213 | U1 snRNP-specific spliceosome factor |
| `Thoc1` | 303 | THO/TREX mRNA export machinery |
| `Hnrnpu` | 733 | abundant hnRNP/mRNP factor, not a direct SRSF1 substitute |
| `Hnrnpc` | 122 | hnRNP splice-site antagonist to U2AF at cryptic sites |
| `Tardbp` | 210 | RNA-binding/splicing regulator |
| `Matr3` | 149 | RNA-binding nuclear matrix protein |
| `Hnrnpa2b1` | 11 | RNA-binding hnRNP counterexample with a small footprint |
| `Hnrnph2` | 4 | RNA-binding hnRNP counterexample with a tiny footprint |
| `Ddx3x` | 8 | RNA helicase counterexample with a tiny footprint |
| `Ddx39b` | 0 | RNA export/splicing counterexample with no focal FDR hits |
| `Cstf2` | 0 | 3-prime-end processing counterexample with no focal FDR hits |
| `Snrpb` | 0 | Sm-ring snRNP counterexample with no focal FDR hits |
| `Rbm28` | 0 | RNA-binding counterexample with no focal FDR hits |

I also checked whether the strongest comparators were isolated to the focal
population. They were not. `U2af2` had 828 focal DEGs and 802 in `155 MB Glut`;
`Prpf6` had 454 focal and 1,159 in `155 MB Glut`; `Rnpc3` had 868 focal and
smaller signatures in `155 MB Glut`, `052 Pvalb Gaba`, and `066 CNU-HYa HY
GABA`; `Tnpo3` had 618 focal, 288 in `191 MB P MY GABA`, and 215 in `155 MB
Glut`; `Snrnp70` had 213 focal and 386 in `155 MB Glut`. Thus the focal
responses of the transferable anchors are part of a subcortical RNA-processing
stress pattern rather than single-cell-class artifacts.

Across all 17,259 focal measured genes, pairwise Spearman correlations among
`U2af2`, `Rnpc3`, `Prpf6`, `Snrnp70`, `Tnpo3`, `Hnrnpu`, `Hnrnpc`, `Tardbp`,
`Matr3`, `Thoc1`, `Cdc40`, and `Cdk13` were consistently but only modestly
positive. Examples were `Prpf6` with `Cdc40`, rho = 0.318; `Prpf6` with
`Thoc1`, rho = 0.317; `Prpf6` with `U2af2`, rho = 0.267; `U2af2` with
`Tnpo3`, rho = 0.249; `Rnpc3` with `Snrnp70`, rho = 0.275. FDR sets also
overlapped in the focal cells: `U2af2` shared 194 significant genes with
`Rnpc3`, 121 with `Prpf6`, 133 with `Tnpo3`, and 76 with `Snrnp70`.

These correlations are not high enough to treat any one visible gene as a
literal phenocopy of `Srsf1`, but they show that the large spliceosome,
mRNA-export, and SR-import perturbations enter a shared neighborhood of
whole-gene stress signatures in the focal neurons.

## Same-experiment corpus checks

The July SourceGuard corpus summarized `U2af2` as a broad but cell-state-graded
whole-gene response enriched in `151 TH Prkcd Grin2c Glut`, `155 MB Glut`, `191
MB P MY GABA`, and `217 P MY Pineal Glut`, with down-regulation of RNA
processing markers such as `Rsrp1`, `Srrm2`, `Luc7l2`, `Srsf5`, and `Tial1`
and down-regulation of mature neuronal effector genes. Its cross-perturbation
record placed `Prpf6` and `Cdc40` among the top positive `U2af2` neighbors, but
also explicitly flagged nonconvergence of generic RNA-processing comparators
such as `Snrpb`, `Hnrnpa2b1`, `Hnrnph2`, `Ddx39b`, and `Rbm28`.

The `Tnpo3` corpus record was especially informative for `Srsf1`. It described
`Tnpo3` loss as down-regulating an SR-splicing and RNA-processing module led by
`Srrm2`, `Srsf5`, `Srsf1`, `Srsf7`, `Srsf2`, `Akap8l`, `Clk1`, and `Cstf2`;
in the focal Parquet rows, `Tnpo3` significantly reduced `Srsf1` itself
(`logfoldchanges = -0.58`) as well as `Srsf2` (-0.44), `Srsf5` (-0.39),
`Srsf7` (-0.38), `Srrm2` (-0.54), `Akap8l` (-0.48), and `Clk1` (-0.34). The
internal same-experiment interpretation also found that `Tnpo3` converged with
`Prpf6`, `U2af2`, `Cdc40`, `Rnpc3`, `Snrnp70`, and `Thoc1`, but not with
generic karyopherin perturbations. That matches the external mechanism:
transportin-SR2/TNPO3 imports phosphorylated RS-domain SR proteins rather than
being a general nuclear-transport factor.

The `Snrnp70` corpus records added a useful boundary. `Snrnp70` converged with
`Thoc1`, `Prpf6`, `U2af2`, `Hnrnpu`, `Tpr`, `Rnpc3`, and `Cdc40`, but `Snrpb`,
a represented Sm-core snRNP subunit, had 0 focal DEGs and did not phenocopy
`Snrnp70`. This is the strongest local warning against scoring `Srsf1` only by
being spliceosome-associated.

## Biological transfer to `Srsf1`

`Srsf1` encodes the prototypical serine/arginine-rich SR protein ASF/SF2. SR
proteins bind pre-mRNA with their RNA-recognition motifs and use RS domains to
couple constitutive and alternative splicing with downstream RNA processing,
including nuclear export, nonsense-mediated decay, and translation (Long and
Caceres 2009; Shepard and Hertel 2009). Transportin-SR and transportin-SR2
recognize RS-domain cargoes and import phosphorylated SR proteins into the
nucleus (Kataoka, Bachorik and Dreyfuss 1999; Lai, Lin and Tarn 2001;
Maertens et al. 2014), so `Tnpo3` loss is a mechanistically proximal in-dataset
proxy for impaired SRSF-family function. `Sfrs1` is not simply redundant in
neurons: conditional loss in the embryonic mouse retina caused apoptosis of
early-born retinal neurons (Kanadia et al. 2008), supporting the idea that a
neuron can be sensitive to SRSF1 dosage, while the embryonic retinal setting is
not the same endpoint as survivor-conditioned juvenile thalamic snRNA-seq.

The causal transfer I used was:

`Srsf1` CRISPR loss of function -> impaired SRSF1-dependent splice-site choice
and altered SR-factor autoregulatory/cross-regulatory RNA processing -> an
RNA-biogenesis imbalance resembling, but narrower than, `Tnpo3` cargo-import
failure and core-spliceosome perturbation -> secondary depression of
RNA-processing and synaptic-effector transcripts in recovered thalamic
glutamatergic nuclei -> a large but not extreme FDR-significant whole-gene
count.

That chain predicts the same endpoint direction as `U2af2`, `Prpf6`, `Cdc40`,
`Snrnp70`, and `Tnpo3`: a broad nonzero response in `151 TH Prkcd Grin2c Glut`.
I placed `Srsf1` near `Tnpo3` and `Cdc40` because the held-out gene is an
obligate member of the SR splicing program whose mRNA is one of the strongest
SR-family decreases after `Tnpo3` loss in the focal data. I did not place it as
high as `U2af2`/`Rnpc3`, because those hit core 3-prime splice-site or minor
spliceosome recognition and produced 828-868 focal DEGs; SRSF1 is one
nonredundant SR factor, but paralogous SR proteins and compensatory AS-NMD
circuits should buffer some substrates. I did not place it down with `Snrpb`,
`Ddx39b`, or `Cstf2`, because those are either different spliceosome subunits
or adjacent 3-prime/export factors that lack the direct SR-factor dependency
shown by `Tnpo3`.

## Final point estimate and limits

I predict `Srsf1` will be a high nonzero focal responder with about the same
breadth as the `Tnpo3`/`Cdc40` anchor pair:

| target | predicted `n_degs` |
|---|---:|
| `Srsf1` | 620 |

This is still extrapolation. No direct `Srsf1` knockout signature is present in
the declared inputs, and the Parquet is a whole-gene abundance readout rather
than an isoform, intron-retention, protein-localization, editing-indel, or
cell-survival assay. The best visible analog, `Tnpo3`, impairs import of many
SR-domain cargoes and is therefore broader than a single SRSF1 lesion, whereas
`U2af2`, `Prpf6`, `Cdc40`, `Rnpc3`, and `Snrnp70` perturb different spliceosome
assembly steps. The zero signatures of `Snrpb`, `Ddx39b`, and `Cstf2` show that
even close RNA-processing annotations can be quiet in this CRISPR/snRNA
endpoint. For those reasons the zero/nonzero call is better supported than the
exact integer, and 620 should be read as a calibrated point prediction in the
several-hundred-DEG regime rather than as a precise mechanistic count.
