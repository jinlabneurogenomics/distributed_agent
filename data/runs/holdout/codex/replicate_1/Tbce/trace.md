# Tbce direct forecast

Target and endpoint:

- Manifest target: `Tbce`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: genes in the focal class with BH-adjusted Wilcoxon `pvals_adj < 0.05`
- Declared training table: 1,674 visible targets; `Tbce` is held out

Target biology used:

- The canonical `Tbce` bundle reports exact focal reach: `Tbce` is detected in
  21,553 of 23,679 matched non-target nuclei, or 91.0%, with mean CP10k 1.85.
  Thus target RNA availability should not be the main downward factor.
- TBCE is a tubulin-specific chaperone/routing factor. The bundle adjudicates
  the P16 to P37-P44 functional stock as `likely_substantially_depleted` but
  only partially evidenced: the best timing evidence is from destabilized
  `Tbce-pmn` motor neurons, not acute thalamic CRISPR.
- Existing TBCE, already folded tubulin, and pre-existing microtubules can
  persist after editing; the screen samples recovered neurons only. I therefore
  treated the biology as compatible with a visible response but not with a
  proteasome-like hundreds-of-genes response.

Training observations that set the scale:

- The typed analog nomination put `Tbcd` first for `Tbce`; it shares a
  pre-materialized ortholog-projected CORUM `TBCD-ARL2-tubulin(beta)-TBCE`
  complex and post-chaperonin tubulin-folding annotations. `Tuba1a` and
  `Tubb5` were the other exact-complex/paralog-tier available nominees near the
  top; `Tuba4a`, `Tubb4b`, `Mapt`, `Map1b`, `Kif2a`, and `Spast` were broader
  cytoskeletal fallbacks.
- In the declared thalamic count table the close tubulin/folding perturbations
  were small: `Tbcd = 12`, `Tuba1a = 7`, `Tuba4a = 2`, `Tubb5 = 1`,
  `Tubb4b = 1`. Broader microtubule-associated fallbacks were also mostly
  flat: `Spast = 0`, `Kif2a = 0`, `Mapt = 1`, `Map1b = 1`, `Nefh = 1`.
- Same-experiment Findings describe the `Tbcd` surface as sparse and real, with
  `151 TH Prkcd Grin2c Glut` carrying 12 of its 19 FDR<0.10 atlas-wide
  downstream rows. The recurrent `Tbcd` output was alpha-tubulin mRNA induction
  plus a small thalamic adaptation module, and `Tbcd` lacked a coordinated
  UPR/ISR, autophagy, redox, or proteasome-subunit program.
- Same-experiment Claims around the tubulin neighborhood show that `Tuba1a`
  produces a restricted tubulin-isotype compensation program, while represented
  tubulin, MAP, kinesin, dynactin, CAMSAP, and MARK perturbations generally do
  not collapse into one shared postnatal mRNA stress module.

Profile checks:

- A matched profile comparison in `151 TH Prkcd Grin2c Glut` recovered
  `Tbcd` with 12 significant features, `Tuba1a` with 7, `Tubb5` with 1, and
  the off-axis high-burden boundaries `Dctn1 = 75` and `Grin1 = 89`.
- `Tbcd`'s leading positive significant features were `Tuba1a`, `Tuba1b`,
  `Ypel4`, `Nfil3`, `Kctd16`, `Satb1`, `Slc25a23`, `Mturn`, and `Jun`; its
  negative significant features were `Lrrc7`, `Ptprn2`, and `Samd5`.
- The direct tubulin comparators were not transcriptomic phenocopies in this
  focal class: `Tbcd` versus `Tuba1a` Pearson was 0.008 and `Tbcd` versus
  `Tubb5` Pearson was 0.011 within the focused comparison. `Tbcd` was closer
  to secondary thalamic state neighbors such as `Hspa5` and `Grin1` than to
  structural tubulin knockdowns.

Forecast:

The closest operation-bearing donor is `Tbcd` at 12 focal DEGs; the structural
tubulin perturbations and broader cytoskeletal fallbacks argue downward into
the single digits; the target's high in-assay expression and likely stock loss
argue against a true zero. I therefore forecast a sparse but visible `Tbce`
response, below the `Tbcd` count but above the flat tubulin/MAP background:

`predicted_n_degs = 10`
