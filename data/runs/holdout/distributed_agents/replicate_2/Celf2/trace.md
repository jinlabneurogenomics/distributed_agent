## Question

I predicted the held-out `n_degs` endpoint for the requested perturbations in the
`151 TH Prkcd Grin2c Glut` cell group. In this run the manifest contained one
held-out target, `Celf2`. The endpoint is the number of measured genes whose
Wilcoxon Benjamini-Hochberg adjusted p-value is below 0.05 in that cell group,
so this is a gene-level differential-expression breadth prediction, not a
prediction of editing efficiency, target mRNA knockdown, alternative splicing, or
translation.

The only ambiguity I needed to resolve was how to use RNA-binding/splicing
biology for a factor that has no direct within-dataset family member. I treated
generic RNA-binding proteins and core spliceosome subunits as calibration
points, but not as interchangeable matches: CELF2 is a sequence-specific CELF
family post-transcriptional regulator, whereas `U2af2`, `Snrnp70`, `Rnpc3`,
`Cdc40`, and `Prpf6` are core spliceosome factors whose perturbations produced a
much broader assay-level state.

## Sources

- The held-out manifest:
  `[local file: 034_Celf2.csv]`.
- The focal-cell training endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- The full training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`. `target_context`
  for `Celf2` returned no Celf2-specific claims, findings, or explicit
  comparator references, so it did not provide a direct internal mechanistic
  neighbor.
- NCBI PubMed literature searches for `Celf2`/`CUGBP2`, CELF-family neuronal
  splicing, and `Celf4` mutant phenotypes.

External literature used:

- Chen et al. 2016, DOI 10.7554/eLife.16072: CELF/UNC-75 proteins regulate
  Syntaxin alternative splicing and support axon regeneration; mouse `Celf2`
  is induced after peripheral nerve injury and `Celf2` mutant mice have impaired
  axon regeneration.
- Syed et al. 2026, DOI 10.1007/s12035-026-05933-6: constitutive mouse
  `Celf2` loss causes neonatal lethality, altered cortical architecture,
  widespread transcriptomic and splicing changes, reduced upper layer excitatory
  neurons, and reduced `Camk2a`.
- Loria et al. 2003, DOI 10.1016/s0960-9822(03)00532-3, and Norris et al.
  2014, DOI 10.1016/j.molcel.2014.05.004: the C. elegans CELF ortholog
  `unc-75` is a neuronal nuclear RNA-binding/splicing factor that works with
  ELAV/Hu-family factors to tune neuron-type-specific splicing and synaptic
  transmission.
- Mallory et al. 2015, DOI 10.1073/pnas.1423695112: CELF2 can drive a program
  of alternative-splicing changes after T-cell activation, supporting a direct
  splicing-regulatory role outside the nervous system.
- Wagnon et al. 2011, DOI 10.1111/j.1601-183X.2011.00717.x: the CELF paralog
  `Celf4` is CNS-enriched in adults; adult and excitatory-neuron deletion are
  sufficient for convulsive seizure phenotypes, showing that CELF-family loss can
  matter in postmitotic neurons rather than only during embryogenesis.

## Dataset Analysis

I first confirmed that the manifest has exactly one requested target,
`Celf2`, and that `Celf2` is held out from the focal DEG-count training table.
The training table contains 1,674 non-held-out perturbations. Its focal-cell
endpoint is sparse:

| statistic | value |
| --- | ---: |
| nonzero training perturbations | 469 / 1,674 |
| median `n_degs` | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| 99th percentile | 436.5 |
| maximum | 2,677 |

I then searched the focal counts for available RNA-processing perturbations and
queried the parquet for only the focal cell group and those candidate targets.
For each candidate I counted rows with `pvals_adj < 0.05` and retained the
matched perturbed/control nucleus counts. Each candidate below had 17,259
measured genes and 23,679 matched control nuclei in this cell group.

| perturbation | `n_degs` | matched perturbed nuclei | how it was used |
| --- | ---: | ---: | --- |
| `Tia1` | 0 | 85 | sequence-specific RBP; weak post-transcriptional analog |
| `Cstf2` | 0 | 174 | RNA 3-prime end processing counterpoint |
| `Fmr1` | 0 | 178 | neuronal mRNA-binding/translational regulator |
| `Fxr1` | 0 | 85 | FMRP-family mRNA regulator |
| `Upf3b` | 1 | 81 | NMD/post-transcriptional regulator |
| `Ddx3x` | 8 | 138 | RNA helicase with low but nonzero response |
| `Hnrnpa2b1` | 11 | 124 | non-core nuclear RBP/splicing analog |
| `Hnrnpc` | 122 | 196 | stronger hnRNP counterexample |
| `Matr3` | 149 | 130 | stronger nuclear RBP counterexample |
| `Tardbp` | 210 | 153 | stronger RNA/DNA-binding counterexample |
| `Snrnp70` | 213 | 135 | core spliceosome/U1 snRNP boundary |
| `Prpf6` | 454 | 72 | core spliceosome boundary |
| `Cdc40` | 624 | 159 | core spliceosome boundary |
| `Hnrnpu` | 733 | 163 | broad architectural hnRNP boundary |
| `U2af2` | 828 | 222 | essential spliceosome 3-prime splice-site factor |
| `Rnpc3` | 868 | 149 | minor spliceosome boundary |

For expression-pattern evidence, I compared complete focal log-fold-change
profiles for the same RNA-processing cohort with the Distributed Agents runtime profile
tools: 17,259 gene-level `logfoldchanges` per perturbation, all 120 pairwise
comparisons among 16 candidate targets, top 200 positive/negative signed tails,
and FDR-significant feature overlaps. This was useful mainly for boundary
setting. `Tia1`, `Cstf2`, `Fmr1`, and `Fxr1` had no FDR-significant genes;
`Upf3b` had only one; `Hnrnpa2b1` had 11. Their apparent largest log-fold-change
tails were dominated by nonsignificant rows with adjusted p-values of 1.0 rather
than reproducible shared hits. By contrast, the high-count spliceosome and broad
hnRNP perturbations had dozens to hundreds of significant genes.

The low-response RBPs were also not simply dilute versions of the core
spliceosome state. For example, in the top-200 signed-tail comparison `Tia1`
shared only 3 top features with `U2af2`; `Upf3b` shared 6 with `U2af2`; and
`Hnrnpa2b1` shared 7 with `U2af2`. Significant-feature intersections between
`Hnrnpa2b1` and the broad RNA-processing hits were tiny, ranging from zero to a
few genes per pair, and `Upf3b` shared only a single positive significant gene
with `Hnrnpc` while sharing none with the other high-response RNA factors. I
therefore treated `Hnrnpc`, `Hnrnpu`, `Tardbp`, `Matr3`, and the spliceosome
genes as evidence that some RNA-processing knockouts can be very broad in this
assay, but not as direct count estimates for `Celf2`.

## Celf2

`Celf2` encodes a CELF-family RNA-binding protein. External evidence supports a
real neuronal role: C. elegans UNC-75/CELF regulates neuron-type-specific
alternative splicing and synaptic transmission, mammalian CELF2 participates in
Syntaxin splicing during axon regeneration, constitutive mouse `Celf2` loss
disrupts cortical maturation, and adult/excitatory-neuron loss of the related
CELF protein CELF4 can alter excitatory neurotransmission strongly enough to
produce seizures.

Those data make a pure "functionless in neurons" prior inappropriate, but they
do not point to a broad acute gene-expression response in this particular
Perturb-seq endpoint. Most of the direct CELF2 literature concerns full
germline or developmental loss, peripheral nerve injury, or splicing/isoform
readouts. The supplied endpoint is gene-level mRNA abundance 3-4 weeks after
sparse AAV CRISPR in postmitotic juvenile neurons, with an average on-target
mRNA reduction of only about 18 percent per guide. A CELF2 perturbation could
therefore alter exon choice or translation without creating many genes that
pass a BH-adjusted Wilcoxon expression test.

Within the focal dataset, the most appropriate available scale-setters were the
low-response, non-core post-transcriptional regulators. `Tia1`, `Fmr1`, `Fxr1`,
and `Cstf2` each produced 0 DEGs; `Upf3b` produced 1; `Ddx3x` produced 8; and
`Hnrnpa2b1` produced 11. I viewed `Hnrnpa2b1` and `Ddx3x` as the upper end of
the plausible local bracket for a nonessential RNA-binding/splicing regulator,
not as evidence for a hundreds-of-genes response. The hundreds-count cases were
less specific boundaries: `U2af2`, `Rnpc3`, `Cdc40`, `Prpf6`, and `Snrnp70`
encode spliceosome machinery, and `Hnrnpu`, `Tardbp`, `Matr3`, and `Hnrnpc`
produced stronger, idiosyncratic expression programs that were not reproduced by
the lower-impact RBPs.

I therefore predicted no FDR-significant gene-level changes for `Celf2`, with
the expectation that any acute effect would be below this assay's DEG-count
threshold or would appear primarily as splicing/post-transcriptional changes
rather than a robust abundance signature.

Predicted `n_degs` for `Celf2`: **0**.

## Limits

- There was no direct `Celf2` signature in the training differential-expression
  parquet, no `Celf2` count in the training endpoint table, no CELF-family
  paralog in the available training counts, and no `Celf2` entry in the
  Distributed Agents corpus release. The estimate is extrapolated from broader
  RNA-processing perturbations.
- Gene-level snRNA-seq DE is a poor readout for many CELF functions. CELF2 may
  cause exon-inclusion, UTR, stability, or translation changes that leave total
  gene abundance nearly unchanged.
- The strongest direct `Celf2` mouse evidence comes from constitutive
  developmental knockout, while the experiment here is mosaic, postnatal,
  partial acute CRISPR in already postmitotic neurons.
- The literature cell types are not exact matches for `151 TH Prkcd Grin2c
  Glut`: the direct `Celf2` mouse work emphasizes developing cortex and
  peripheral nerve injury, and the `Celf4` paralog evidence is mostly cortical
  and hippocampal.
- The zero call is therefore a threshold prediction, not a claim that CELF2 is
  biologically irrelevant in these neurons.
