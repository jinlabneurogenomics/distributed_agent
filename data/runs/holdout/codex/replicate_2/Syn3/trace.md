# Syn3 direct DEG-count forecast

Target: `Syn3`

Focal population: `151 TH Prkcd Grin2c Glut`

Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- The target bundle reports exact focal-population reach for `Syn3`: the feature is available in `151 TH Prkcd Grin2c Glut`, with `Syn3` detected in 9,542 of 23,679 matched non-target nuclei, or 40.297%, with mean raw UMI 0.577 and mean CP10k 0.369. This made complete transcriptional invisibility less likely, but the expression level is still modest.
- The same endpoint-blind biology bundle adjudicates Syn3 as a dynamic synaptic-vesicle regulator whose functional stock is likely substantially depleted over the P16 to P37-P44 interval. Its supporting phenotypes are mature hippocampal or germline-adult rather than thalamic conditional loss, so this supports target engagement and possible observability, not a large thalamic survivor-state RNA program.
- The declared 151 training count table is very sparse: among 1,674 training perturbations, 1,205 have zero DEGs, 1,481 have at most one DEG, and 1,527 have at most three DEGs. The broad high-count tail is dominated by spliceosome, transcriptional, proteasome, and nuclear/essential regulators rather than presynaptic vesicle genes.
- I treated the represented Syn3-adjacent perturbations as the most relevant count anchors: `Syn1`, `Syn2`, `Syp`, `Sv2a`, `Cplx1`, `Cplx2`, `Dnm1`, `Stx1b`, `Stxbp1`, `Vamp1`, `Nsf`, `Syt2`, `Unc13a`, `Bsn`, `Pclo`, `Cltc`, `Scamp5`, `Dnajc5`, `Napb`, `Rab3gap1`, `Rab3gap2`, `Synj1`, `Unc13b`, `Unc13c`, and `Cadps2`. Their 151 counts were:

| target | n_degs |
|---|---:|
| Bsn | 0 |
| Cadps2 | 0 |
| Cltc | 3 |
| Cplx1 | 1 |
| Cplx2 | 0 |
| Dnajc5 | 1 |
| Dnm1 | 1 |
| Napb | 0 |
| Nsf | 0 |
| Pclo | 0 |
| Rab3gap1 | 0 |
| Rab3gap2 | 0 |
| Scamp5 | 3 |
| Stx1b | 0 |
| Stxbp1 | 1 |
| Sv2a | 1 |
| Syn1 | 1 |
| Syn2 | 0 |
| Synj1 | 1 |
| Syp | 1 |
| Syt2 | 0 |
| Unc13a | 0 |
| Unc13b | 0 |
| Unc13c | 0 |
| Vamp1 | 1 |

- The same-experiment corpus already summarizes this neighborhood: most represented acute presynaptic vesicle-cycle, active-zone, and release-machinery perturbations are flat or self-only in the neuronal snRNA-seq readout, while `Stxbp1` is the main transcriptionally visible presynaptic exception in other matched groups. `Syn1`, `Syn2`, `Syp`, `Sv2a`, `Cplx1`, `Cplx2`, `Vamp1`, `Syt2`, `Bsn`, and `Pclo` Findings all support that these synaptic-vesicle phenotypes usually remain electrophysiological or protein-localization endpoints rather than broad steady-state nuclear RNA states.
- A profile comparison over 18 of the presynaptic/release anchors in the exact 151 group did not find a shared FDR-supported program: across 153 selected pairs, the positive leading-tail overlap mean was 0.0417, no pair had a positive significant-program overlap, and the nonzero significant overlap coefficients on the negative side were all 0. This reinforced the count-table interpretation that these anchors are sparse independently, rather than members of a hidden convergent 151 RNA module.
- Querying the 151 Parquet self rows showed that several one-DEG anchors were simply significant negative target-transcript rows: `Cplx1`, `Dnajc5`, `Dnm1`, `Stxbp1`, `Sv2a`, `Syn1`, `Synj1`, `Syp`, and `Vamp1` had BH-adjusted self `p < 0.05` while their total 151 counts stayed at 1. `Syn2`, the closest paralog besides `Syn1`, had count 0 and a nonsignificant 151 self row. Thus the most likely Syn3 outcomes were 0 if the target transcript failed BH correction and 1 if the Syn3 row itself was detected.

## Synthesis

I predicted a self-only, not a downstream, Syn3 response. Syn3 is expressed in a real minority of focal non-target nuclei and its vesicle-associated protein stock should turn over during the experiment, which moved the forecast above a pure null. However, its family and pathway neighbors in the exact same thalamic class are overwhelmingly 0 to 1 DEG, and the packaged same-experiment Findings caution that perturbing this presynaptic vesicle layer generally fails to create broad compensatory or activity/stress mRNA programs.

The high-count `Grin1` thalamic response was not used as a Syn3 surrogate even though `Grin2c` appears in the focal-class label: corpus Findings show NMDA-receptor subunit effects are context- and subunit-specific, and the 151 `Grin1` state belongs to a receptor/calcium-response axis rather than to the Syn3/Syn1/Syn2 vesicle-reserve branch.

The point forecast is therefore one significant gene: the target transcript or a single weak sentinel. A count of 0 remains plausible if the Syn3 self row is not BH-significant, and counts above 3 look unlikely from the matched presynaptic training set.
