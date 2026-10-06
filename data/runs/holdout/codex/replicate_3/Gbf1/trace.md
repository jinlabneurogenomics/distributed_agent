# Gbf1 n_degs forecast

Point prediction: 0

## Endpoint

The requested endpoint is the count of measured genes with BH-adjusted Wilcoxon
`p < 0.05` for `Gbf1` in `151 TH Prkcd Grin2c Glut`. The target contrast and
target DEG count were held out, so the forecast below uses only the declared
biology bundle, the visible focal-class training count table, and training-only
rows from the declared differential-expression parquet.

## Target biology

The canonical `Gbf1` bundle supports molecular realization within the screen
window: GBF1 is an ARF guanine-nucleotide exchange factor acting at the
cis-Golgi/ERGIC to recruit COPI, it cycles dynamically on early secretory
membranes, and its only curated protein-stability measurement is on the order
of hours rather than the 21-28 day edit-to-harvest interval. In the exact focal
control population, the `Gbf1` transcript is measurable in 20,134 of 23,679
non-target nuclei, with 85.03% of cells expressing it and mean raw UMI 2.27.

Those facts make a productive perturbation biologically plausible; I did not
treat them as evidence that it must produce a broad survivor-state signature.
The same bundle has no direct P16 thalamic-neuron loss phenotype, flags
survivor conditioning as unknown, and leaves postnatal requirement and
compensation by related ARF GEFs unresolved.

## Training measurements that set the scale

The focal count table is highly zero-inflated: among 1,674 visible training
targets, the median count is 0, the 75th percentile is 1, and only 469 targets
have any DEG in this cell class.

The closest assayed genes to GBF1's early-secretory operation were quiet:

| Perturbation | Training `n_degs` in `151 TH Prkcd Grin2c Glut` | Interpretation |
|---|---:|---|
| `Copa` | 0 | COPI coatomer core |
| `Copg1` | 1 | COPI coatomer; only significant row was `Copg1` itself |
| `Sec23a` | 0 | COPII/ER export |
| `Sar1b` | 0 | COPII initiation |
| `Cog4` | 0 | Golgi tethering |
| `Cog5` | 0 | Golgi tethering |
| `Nsf` | 0 | vesicle fusion machinery |
| `Stx5a` | 0 | ER-Golgi SNARE |

I also checked more distant trafficking or stress-adjacent perturbations. `Vcp`
had 2 DEGs, `Sec63` had 11, `Vps35` had 17, `Vps54` had 31, and `Rab7` had
501. I down-weighted these for the GBF1 point because they are late
endosomal, retromer/GARP, ER-translocon, or proteostasis perturbations rather
than direct GBF1/COPI loss. A profile comparison over 16 trafficking candidates
confirmed that the core early-secretory nodes had no significant shared program;
their largest fold changes were nonsignificant, low-support tail values.

## Self-transcript check

One-DEG outcomes in this focal class are often only target self-knockdown:
237 of 276 one-DEG training targets had a significant self transcript. That
makes a one-count forecast possible for `Gbf1`, whose transcript is present in
the focal population. I kept the integer point at 0 because the direct donor
set has mean 0.125 and median 0, and the screen portrait warns that self-mRNA
loss is not a quantitative readout of target engagement or response strength.

## Synthesis

GBF1 loss should be molecularly realized in successfully edited cells, but the
nearest visible perturbations to COPI/early secretory traffic produce no
downstream FDR-significant program in recovered `151 TH Prkcd Grin2c Glut`
nuclei. The best direct forecast is therefore a null focal-class count, with
residual uncertainty that the held-out row could contain a lone self-transcript
DEG or a small ER-stress-like footprint.
