# Cask DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

I interpreted the task as a single scalar holdout prediction: estimate the
number of measured genes that would pass Benjamini-Hochberg adjusted Wilcoxon
`pvals_adj < 0.05` after acute sparse CRISPR loss of `Cask` in the focal
`151 TH Prkcd Grin2c Glut` neuronal population.

The endpoint is assay- and power-dependent. The training CSV counts all
measured FDR-significant rows in this cell group, including a target's own
transcript when it passes FDR. I therefore predicted an integer total for
`Cask`, not a self-excluded downstream-gene count.

## Sources used

- Declared task inputs:
  - `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
  - `training differential-expression dataset`
  - `single-target request for Cask`
- Internal same-experiment corpus:
  - `perturbai-july-260713-sourceguard-1773-v1` Findings ledger and bounded target reports for `Caskin1`, `Dlg4`, and `Grin1`. `Cask` itself had no internal report.
- External literature found through PubMed:
  - Hsueh et al. 2000, DOI 10.1038/35005118, PMID 10749215.
  - Wang et al. 2004, DOI 10.1016/s0896-6273(04)00139-4, PMID 15066269.
  - Hsueh 2006, DOI 10.2174/092986706777585040, PMID 16842202.
  - Atasoy et al. 2007, DOI 10.1073/pnas.0611003104, PMID 17287346.
  - Stafford et al. 2011, DOI 10.1016/j.jmb.2011.07.005, PMID 21763699.
  - Srivastava et al. 2016, DOI 10.1186/s40478-016-0295-6, PMID 27036546.
  - Gao et al. 2018, DOI 10.1038/s41380-018-0027-3, PMID 29610457.
  - Katano et al. 2018, DOI 10.1186/s13041-018-0407-2, PMID 30359304.
  - Bencsik et al. 2019, DOI 10.1038/s41598-019-53317-9, PMID 31727973.
  - Mori et al. 2019, DOI 10.1038/s41380-018-0338-4, PMID 30610199.

## Computation over the training data

I first confirmed that the requested manifest contains only `Cask`, and that
`Cask` is absent from the focal-cell training count table. The focal training
distribution is highly zero-inflated: among 1674 non-held-out perturbations,
1205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 95th
percentile was 18, and a few outliers reached hundreds to thousands of DEGs.

Because this is a count prediction with an unranked requested list, the
ranking workbench was not an authorized capability. I used the parquet only for
exact focal-cell rows around literature-supported CASK analogs:

```python
filter = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(analog_targets)
)
```

The relevant focal-cell training counts were:

| training perturbation | `n_degs` in `151` | interpretation for `Cask` |
|---|---:|---|
| `Caskin1` | 1 | Direct CASK-binding scaffold. The sole FDR 0.05 hit in `151` was `Caskin1` itself; the same-experiment report found zero downstream FDR 0.10 genes in `151` despite detectable `Caskin1` RNA depletion. This is the closest available measured partner. |
| `Dlg4` | 1 | Postsynaptic MAGUK scaffold. The focal row had only the self transcript significant, and the report classified `Dlg4` as globally flat at the downstream snRNA level. |
| `Nrxn1` | 1 | Presynaptic neurexin that can sit in the CASK/Mint/Veli or CASK/Caskin/Veli complex. It again produced only a self-RNA hit in `151`. |
| `Nrxn2` | 0 | Neurexin-family comparator; no FDR 0.05 hit. |
| `Nrxn3` | 0 | Neurexin-family comparator; no FDR 0.05 hit, with only `Vps4a` near threshold at FDR 0.0908. |
| `Nlgn3` | 1 | Trans-synaptic neurexin partner; only the self transcript was significant. |
| `Cntnap1` | 1 | Neurexin-superfamily/CASK-adjacent membrane protein; only the self transcript was significant. |
| `Cntnap2` | 1 | CNTNAP2 can stabilize interneuron dendrites through CASK; only the self transcript was significant in the focal group. |
| `Dlgap4` | 2 | PSD95/DLG-associated scaffold; a small two-gene result, not a broad state. |
| `Shank2` | 0 | Postsynaptic density scaffold; no focal FDR 0.05 hit. |
| `Shank3` | 2 | Postsynaptic density scaffold; only a minimal focal response. |
| `Tbr1` | 0 | CASK nuclear cofactor in developmental forebrain transcription; no focal FDR 0.05 hit. |
| `Grin1` | 89 | Important counterexample. Obligatory NMDAR subunit loss caused a broad focal response, but same-receptor comparators such as `Grin2a` and `Grin2b` were not thalamic `Grin1` phenocopies, so a synaptic or NMDAR-adjacent relationship was not enough to transfer the 89-gene response. |
| `Grin2a` | 1 | NMDAR subunit; self-only in `151`. |
| `Grin2b` | 2 | NMDAR subunit and reported CASK/Tbr1/CINAP transcriptional target; minimal focal response. |

This pattern put the mechanistically specific single-gene CASK neighborhood
near zero or one count, even in the same high-yield cell group where `Grin1`,
`Ctnnb1`, `Rab7`, and many RNA-processing or proteostasis genes had large
responses. I therefore treated broad focal responsiveness as available but not
expected after loss of a synaptic MAGUK scaffold.

## Target-specific reasoning for `Cask`

`Cask` is not present as a perturbation in either declared input, so the
prediction is transfer rather than direct interpolation. Biologically, CASK is
a multidomain MAGUK that can bind neurexin, Mint1, Veli/LIN7 proteins,
Caskin1, and Tbr1/CINAP; the Tbr1/CASK/CINAP complex has been tied to
transcriptional regulation of `Reln` and `Grin2b` in developmental neurons
(Hsueh et al. 2000; Wang et al. 2004; Hsueh 2006). Complete CASK loss is much
more severe than loss of some PSD scaffolds: CASK knockout mice are perinatally
lethal and show altered inhibitory and excitatory spontaneous release (Atasoy
et al. 2007), CASK haploinsufficiency and hypomorph states affect postnatal
brain growth and metabolism (Srivastava et al. 2016), and CASK-deficient
neurons in heterozygous female slices showed altered E/I balance with reduced
GluN2B (Mori et al. 2019).

Those external data made `Cask` less trivially buffered than `Caskin1`, but the
causal stage mattered. The present experiment perturbs postmitotic juvenile
neurons sparsely at P16 and reads resting nuclear RNA from recovered nuclei
3-4 weeks later. The external CASK phenotypes above include perinatal survival,
developmental circuit formation, synaptic release, receptor localization, and
systemic/non-neuronal growth effects. Those are plausible off-axis phenotypes
for NeuN-enriched thalamic snRNA-seq. In the training data, the available genes
that sit closest to those mechanisms did not yield a durable focal nuclear
state:

- `Caskin1`, CASK's direct scaffold partner, had `n_degs = 1` in `151`, and
  the same-experiment corpus explicitly found no downstream focal response
  despite significant `Caskin1` self-RNA depletion.
- `Dlg4`, another MAGUK synaptic scaffold, had `n_degs = 1`; the report
  interpreted the single-gene focal result as self-RNA only and no persistent
  downstream RNA state.
- Neurexin and neurexin-adjacent perturbations were self-only or fully null in
  `151`: `Nrxn1 = 1`, `Nrxn2 = 0`, `Nrxn3 = 0`, `Cntnap1 = 1`, `Cntnap2 = 1`.
- The CASK nuclear cofactor `Tbr1` was completely flat in `151`
  (`n_degs = 0`). That argues against an easily observed CASK/Tbr1 `Reln` or
  `Grin2b` transcriptional cascade in this thalamic postnatal context.
- `Grin1 = 89` showed that some receptor perturbations can create a broad
  thalamic state. I did not transfer this response to `Cask`: Grin1 directly
  removes the obligatory NMDAR channel subunit, while CASK loss perturbs a
  scaffold/coactivator upstream of receptor localization and some transcription;
  the internal `Grin1` report also found that `Grin2a`, `Grin2b`, `Grin2d`,
  and `Grin3a` did not phenocopy the thalamic `Grin1` signature.

My resulting prior for `Cask` in `151 TH Prkcd Grin2c Glut` is a zero or
self-only FDR result rather than a broad compensatory state. I predicted
`n_degs = 1` instead of 0 because direct partners with clear transcript
ablation in the same focal class, especially `Caskin1`, `Dlg4`, `Nrxn1`,
`Nlgn3`, `Cntnap1`, and `Cntnap2`, often contribute exactly one count through
the target transcript itself. I did not add a downstream gene for `Grin2b`,
`Reln`, an NMDAR activity module, or a stress module, because the corresponding
training perturbations were focal-cell null or nearly null.

## Limits

This is an extrapolation from partners and pathway neighbors: the closest
possible perturbation, `Cask` itself, was held out, and `Caskin2`, `Dlg1`,
`Dlg2`, `Dlg3`, `Lin7`, and `Apba/Mint` family members were not focal training
targets in the count table. Sparse AAV CRISPR at P16 can disrupt CASK protein
without a measured loss of nuclear `Cask` RNA, so the predicted count depends
on whether the self transcript is visible; the self transcript is the main
reason the point estimate is 1 rather than 0. Finally, severe CASK biology in
the literature often acts through early development, survival, synaptic
ultrastructure, E/I physiology, retinal or cerebellar circuits, or systemic
metabolism; the thalamic NeuN+ snRNA DEG-count endpoint may miss those effects.
