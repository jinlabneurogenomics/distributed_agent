# Reasoning trace

## Question and scope

The task is to predict, for each target in
`180_Pnpt1.csv`, the number of genes that would have
`pvals_adj < 0.05` in the held-out Perturb-seq signature for
`151 TH Prkcd Grin2c Glut` neurons.  The only requested target in this
run is `Pnpt1`.  I treated the endpoint as exactly the focal-cell-group
Benjamini-Hochberg-adjusted Wilcoxon DEG count, including a possible
on-target decrease of `Pnpt1` itself if it cleared FDR.  I did not treat the
count as a direct proxy for biological essentiality: the screen is sparse,
postnatal, postmitotic, and measured 3-4 weeks after AAV CRISPR delivery.

## Sources used

- Focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Focal differential-expression rows filtered from:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 180_Pnpt1.csv]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`
- PubMed literature searches for PNPT1/PNPase mitochondrial RNA import,
  mitochondrial RNA degradation, the SUV3-PNPase degradosome, and
  mitochondrial dsRNA signalling

The Distributed Agents corpus had no direct `Pnpt1` target card and no first-hop
`Pnpt1` graph neighbors in this release, so the target-specific biology below
comes from the public literature and from manually matched in-panel
mitochondrial perturbations.

## Training-set calibration

The focal count table contains 1,674 non-held-out targets.  The endpoint is
heavily zero inflated:

| DEG count bin | Number of targets |
| --- | ---: |
| 0 | 1,205 |
| 1 | 276 |
| 2 | 31 |
| 3-10 | 59 |

The median is 0 DEGs, the 75th percentile is 1 DEG, and the 95th percentile is
18 DEGs.  Strong broad signatures exist, for example `Uba5` with 2,677 DEGs
and `Sin3a` with 1,433 DEGs, but they are unusual in this cell group.

I then inspected training perturbations that put the same cellular subsystem
under stress as PNPT1 loss.  I used the count CSV to find mitochondrial
respiratory-chain, mitochondrial RNA/translation, mitochondrial proteostasis,
and mitochondrial dynamics/import factors that were actually screened.  Among
105 such in-panel targets, 66 had 0 DEGs, 37 had exactly 1 DEG, `Atp6ap2` had
2, and `Opa1` had 37.  This makes mitochondrial localization alone a weak
reason to predict a broad focal response in this endpoint.

For selected candidates, I pulled their focal log fold changes and adjusted
p-values from the parquet and checked the significant genes:

| Training perturbation | Observed `n_degs` | Expression evidence in `151 TH Prkcd Grin2c Glut` | Relevance to `Pnpt1` |
| --- | ---: | --- | --- |
| `Lrpprc` | 0 | No FDR-significant genes; the on-target `Lrpprc` row had log2FC -0.355 but `pvals_adj = 1`. | Mitochondrial RNA-binding factor needed for mitochondrial mRNA stability and expression; the closest available mt-RNA maintenance analog. |
| `Rars2` | 0 | No FDR-significant genes; on-target log2FC -0.140, `pvals_adj = 1`. | Mitochondrial arginyl-tRNA synthetase; an mt-translation counterexample showing that a disease mitochondrial translation factor need not move this assay. |
| `Fars2` | 0 | No FDR-significant genes; on-target log2FC -0.045, `pvals_adj = 1`. | Another mitochondrial aminoacyl-tRNA synthetase, again with no broad neuronal signature. |
| `Gfm2` | 0 | No FDR-significant genes; on-target log2FC -0.225, `pvals_adj = 1`. | Mitochondrial translation elongation/recycling factor; no detectable response. |
| `Clpp` | 0 | No FDR-significant genes; on-target log2FC -0.255, `pvals_adj = 1`. | Mitochondrial matrix protease; tests a mitochondrial unfolded-protein-stress axis and was inactive here. |
| `Lonp1` | 0 | No FDR-significant genes; on-target log2FC -0.465, `pvals_adj = 0.507`. | Matrix protease and mitochondrial proteostasis factor; closer to stress surveillance than ETC subunits but still zero. |
| `Cox5a` | 1 | Only `Cox5a` itself was significant, with log2FC -1.231. | Electron-transport complex IV subunit; a clean example of an on-target-only mitochondrial response. |
| `Ndufs2` | 1 | Only `Ndufs2` itself was significant, with log2FC -0.728. | Complex I core subunit; respiratory-chain loss did not propagate into many nuclear DEGs. |
| `Ndufb11` | 1 | Only `Ndufb11` itself was significant, with log2FC -0.563. | Complex I accessory subunit; on-target-only. |
| `Uqcrc2` | 1 | Only `Uqcrc2` itself was significant, with log2FC -0.576. | Complex III subunit; on-target-only. |
| `Tomm40` | 1 | Only `Tomm40` itself was significant, with log2FC -0.923. | Mitochondrial outer-membrane protein-import pore; on-target-only despite a core mitochondrial function. |
| `Chchd2` | 1 | Only `Chchd2` itself was significant, with log2FC -0.880. | Mitochondrial intermembrane-space stress and cristae factor; on-target-only. |
| `Opa1` | 37 | Significant up-regulation of ISR-like genes including `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2`, and `Slc7a5`; `Opa1` itself was also significant. | Important mitochondrial counterexample, but OPA1 directly controls inner-membrane fusion/cristae organization and apoptotic remodeling, not mtRNA decay. |
| `Nrf1` | 138 | Broad signature with significant down-regulation of mitochondrial/nuclear genes such as `Sdha`; 138 total DEGs. | Boundary case rather than a positive analog: NRF1 is a nuclear transcription factor that directly controls many respiratory genes. |

I also ran a run-local profile comparison over
`Lrpprc`, `Rars2`, `Fars2`, `Gfm2`, `Opa1`, `Nrf1`, `Cox5a`, `Ndufs2`,
`Uqcrc2`, `Chchd2`, `Tomm40`, `Slc25a46`, `Lonp1`, and `Clpp` using the focal
log2FC vectors with `pvals_adj < 0.05` as the significance cutoff.  Six of the
fourteen selected profiles had no significant features, six had 1-9
significant features, only `Opa1` fell in 10-49, and only `Nrf1` exceeded 50.
The zero-count mtRNA and translation genes did not share a recurrent
significant DEG program that would justify borrowing `Opa1` or `Nrf1`'s
larger counts for `Pnpt1`.

## PNPT1 biology used for transfer

`Pnpt1` encodes mammalian PNPase, a mitochondrial polynucleotide
phosphorylase.  Multiple public studies place it in mitochondrial RNA
handling rather than as a nuclear transcription factor:

- Chen et al. 2006, DOI `10.1128/MCB.01002-06`, showed that mammalian PNPase
  localizes mainly to the mitochondrial intermembrane space and that RNAi
  reduction can impair membrane potential, respiratory-chain activity, ATP
  generation, and mitochondrial morphology.
- Wang et al. 2010, DOI `10.1016/j.cell.2010.06.035`, showed that PNPase
  supports import of nuclear-encoded RNAs into mitochondria and that its
  reduction impairs mitochondrial RNA processing.
- Wang et al. 2009, DOI `10.1074/jbc.M109.009605`, biochemically connected
  human PNPase with the mitochondrial SUV3 helicase in a complex able to
  degrade structured double-stranded RNA.
- Vedrenne et al. 2012, DOI `10.1016/j.ajhg.2012.09.001`, found human
  `PNPT1` mutations that impair RNA import and mitochondrial translation and
  cause combined respiratory-chain deficiency.
- Dhir et al. 2018, DOI `10.1038/s41586-018-0363-0`, identified SUV3 and
  PNPase as suppressors of mitochondrial dsRNA accumulation; loss of either
  can activate MDA5-dependent type-I interferon signalling.
- Krieger et al. 2024, DOI `10.26508/lsa.202302396`, further showed that
  PNPase depletion favors export of mitochondrial dsRNA to the cytosol and
  activation of a type-I interferon stress response in cultured cells.

Complete or strong PNPT1 loss therefore can be consequential.  The issue is
that the focal endpoint is not complete loss in a dividing cultured cell.  The
screen perturbs sparse juvenile postmitotic neurons, gives modest target RNA
depletion on average, and computes single-nucleus Wilcoxon DEGs.  In that
regime, the closest observed mitochondrial RNA/translation factors
(`Lrpprc`, `Rars2`, `Fars2`, `Gfm2`) and mitochondrial proteostasis factors
(`Clpp`, `Lonp1`) produced zero significant genes, while respiratory-chain
and import perturbations usually produced either zero or the targeted
transcript alone.  The large PNPT1 literature argues that a very strong
perturbation could trigger mitochondrial dysfunction or dsRNA signalling, but
the training data argue that the perturbation strength and cell context here
often fail to convert mitochondrial maintenance lesions into a BH-significant
focal signature.

## Target-specific prediction

### `Pnpt1`

I predict `Pnpt1` will have no genes below FDR 0.05 in
`151 TH Prkcd Grin2c Glut`.

The main in-dataset support is the zero-DEG behavior of the most relevant
available mitochondrial RNA/translation analogs: `Lrpprc` had 0 DEGs despite
a detectable on-target negative log2FC, and `Rars2`, `Fars2`, and `Gfm2` were
also 0.  `Clpp` and `Lonp1` show that mitochondrial stress-protease loss did
not reliably induce a nuclear stress response in this assay.  The many ETC
examples with 0-1 DEG, including `Cox5a`, `Ndufs2`, `Uqcrc2`, and `Tomm40`,
support a low count if the only reproducible effect is direct mitochondrial
impairment or target transcript knockdown.

I treated `Opa1` and `Nrf1` as counterexamples, not as the best quantitative
analogs.  `Opa1` produced 37 DEGs and an ISR-like `Asns`/`Chac1`/`Ddit3`
program, but OPA1 is a mitochondrial dynamics and cristae factor with a
stronger acute membrane stress route than PNPase depletion.  `Nrf1` produced
138 DEGs but is a nuclear transcriptional regulator.  PNPT1's specialized
mtRNA import/degradosome function is closer to the zero-count mtRNA and
translation genes than to these larger, more transcriptionally coupled
perturbations.

The final point estimate is therefore `0`.  A one-DEG on-target-only result is
plausible because `Pnpt1` itself is measured in the focal DE matrix, but the
closest mtRNA genes often did not pass BH correction for their own transcript
even with negative log2FCs, so I did not add a forced on-target DEG.

## Limits and uncertainty

- `Supv3l1`, the closest PNPase mitochondrial degradosome partner, was not an
  in-panel focal training perturbation, so I had to infer from the more
  distant `Lrpprc`/mitochondrial-translation/proteostasis genes.
- The public PNPT1 studies largely use stronger depletion, patient fibroblasts,
  or non-neuronal cultured cells.  Their mitochondrial dsRNA and interferon
  mechanisms are real but may overstate the cell-autonomous response to
  mosaic AAV CRISPR in postmitotic neurons.
- The NeuN-enriched screen under-samples microglia and other innate-immune
  responders, so paracrine amplification of a PNPT1-triggered dsRNA signal
  would be muted relative to whole tissue.
- The prediction is particularly sensitive to guide performance and PNPase
  protein half-life.  Efficient `Pnpt1` frameshift/NMD in the sampled neurons
  could yield one on-target DEG or a small stress program; weak editing would
  be indistinguishable from the observed zero-DEG mtRNA analogs.
