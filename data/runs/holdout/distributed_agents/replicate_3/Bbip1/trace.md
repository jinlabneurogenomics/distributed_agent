# Bbip1 held-out DEG-count prediction

## Question and resolved ambiguities

The requested readout is the number of genes with `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` for each held-out target in the manifest.  The run
manifest contains one target, `Bbip1`, and that target is absent from both the
training differential-expression parquet and the focal training count CSV.

I treated `n_degs` exactly as the focal training CSV does: every measured gene
whose Benjamini-Hochberg-adjusted Wilcoxon p value is below 0.05 counts,
including the perturbed transcript itself if the target mRNA passes the
threshold.  This matters because the closest represented BBSome perturbation,
`Ttc8`, has one focal DEG and that DEG is `Ttc8` itself.

## Sources used

- Input parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Input focal count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest:
  `[local file: 023_Bbip1.csv]`.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, especially the `Bbs5`, `Ttc8`, `Ift88`, `Lztfl1`, and global ciliary-buffering claims.
- NCBI PubMed literature for BBIP1/BBS18 and the BBSome:
  Nachury et al. 2007, Cell, doi:10.1016/j.cell.2007.03.053, PMID 17574030;
  Loktev et al. 2008, Developmental Cell, doi:10.1016/j.devcel.2008.11.001, PMID 19081074;
  Scheidecker et al. 2013, Journal of Medical Genetics, doi:10.1136/jmedgenet-2013-101785, PMID 24026985;
  Katoh et al. 2015, Journal of Cell Science, doi:10.1242/jcs.168740, PMID 25964651.
- Reactome pathway `BBSome-mediated cargo-targeting to cilium`, R-HSA-5620922, as curated pathway support that BBS5/TTC8/BBIP1 are BBSome members.

The corpus did not contain a direct `Bbip1` target report because `Bbip1` was
held out; the useful corpus evidence came from represented BBSome and
ciliary-transport perturbations.

## Computations over the training data

I first read the held-out manifest and confirmed that this run asks for only
`Bbip1`.  The focal training CSV has 1,674 perturbations; it is strongly
zero-inflated in this cell group:

- `n_degs = 0`: 1,205 perturbations
- `n_degs = 1`: 276 perturbations
- `n_degs = 2`: 31 perturbations
- nonzero: 469 perturbations
- median: 0
- 95th percentile: 18

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for
BBSome, IFT, transition-zone, dynein-2, Hedgehog, and ciliary-GPCR comparator
targets.  All comparators below had the same 23,679 matched control nuclei; the
perturbed-nucleus counts are from the focal parquet rows.

| training target | focal n_degs | focal perturbed nuclei | why it was compared with Bbip1 |
|---|---:|---:|---|
| Bbs5 | 0 | 121 | Core BBSome subunit; closest represented same-complex analog besides Ttc8. |
| Ttc8 | 1 | 180 | Core BBSome subunit BBS8; Katoh et al. found BBIP1/BBS18 links BBS4 to BBS8. |
| Lztfl1 | 0 | 199 | BBSome trafficking regulator, not a core BBSome subunit. |
| Ift43 | 0 | 328 | IFT-A/ciliary transport comparator. |
| Ift81 | 0 | 152 | IFT-B/ciliary transport comparator. |
| Ift88 | 0 | 143 | IFT-B/ciliary transport comparator. |
| Kif3b | 0 | 156 | Anterograde ciliary motor comparator. |
| Dync2h1 | 0 | 98 | Dynein-2 retrograde IFT comparator. |
| Dync2i1 | 0 | 229 | Dynein-2 retrograde IFT comparator. |
| Cep290 | 0 | 99 | Transition-zone/ciliopathy comparator. |
| Rpgrip1l | 0 | 137 | Transition-zone/ciliopathy comparator. |
| Ttc21b | 0 | 131 | IFT-A/retrograde ciliary trafficking comparator. |
| Alms1 | 0 | 110 | Ciliary basal-body/BBS-like ciliopathy comparator. |
| Adcy3 | 0 | 223 | Neuronal ciliary signaling effector. |
| Smo | 0 | 284 | Ciliary Hedgehog signaling effector. |
| Gli1 | 0 | 234 | Hedgehog transcriptional output comparator. |
| Gli2 | 0 | 205 | Hedgehog transcriptional output comparator. |
| Ptch1 | 0 | 159 | Hedgehog receptor comparator. |
| Ptch2 | 0 | 192 | Hedgehog receptor comparator. |
| Gpr161 | 0 | 187 | Ciliary GPCR/Hedgehog regulator. |
| Htr6 | 0 | 351 | Neuronal ciliary GPCR. |
| Mchr1 | 0 | 196 | Neuronal ciliary GPCR. |
| Lepr | 0 | 202 | BBSome-linked metabolic receptor axis. |
| Glp1r | 0 | 132 | Hypothalamic/metabolic GPCR comparator. |

The focal expression surfaces are therefore not just low-count but nearly null.
`Ttc8` has one significant focal row, its own transcript
(`log2FC = -0.663`, Wilcoxon score `-6.017`, `pvals_adj = 3.07e-05`), while
the next-best `Ttc8` row is already nonsignificant (`Strada`, `pvals_adj =
0.415`).  `Bbs5` has no focal hit; the most significant row is `Ptprn` at
`pvals_adj = 0.220`, and the `Bbs5` self-transcript has `log2FC = -0.425`,
Wilcoxon score `-2.547`, but `pvals_adj = 1`.

To check for a weak shared expression state below the FDR cutoff, I pivoted the
focal ciliary subset to gene-by-target Wilcoxon-score vectors and computed
Pearson correlations over the 17,259 measured genes.  The same-complex and same
organelle analogs are essentially uncorrelated in the focal cell group:

- `Bbs5` vs `Ttc8`: `r = 0.0309`
- `Bbs5` vs `Ift88`: `r = 0.0615`
- `Bbs5` vs `Lztfl1`: `r = 0.0480`
- `Ttc8` vs `Ift88`: `r = 0.0594`
- `Ttc8` vs `Lztfl1`: `r = 0.0553`
- `Ttc8` vs `Kif3b`: `r = 0.0347`

These correlations are consistent with the Distributed Agents corpus finding that
whole-atlas `Bbs5` and `Ttc8` neighbors were near zero and that represented
BBSome/IFT/transition-zone targets did not form a hidden mRNA module.

## Target-specific reasoning for Bbip1

BBIP1, also called BBS18 or BBIP10, is a BBSome subunit.  Nachury et al. 2007
defined the BBSome as a BBS protein complex cooperating with Rab8 in ciliary
membrane biogenesis; Loktev et al. 2008 discovered BBIP10 as an additional
BBSome-associated ciliary protein and found that BBIP10 depletion gives
BBS-like zebrafish phenotypes.  Scheidecker et al. 2013 identified a homozygous
null human `BBIP1` mutation as Bardet-Biedl syndrome 18, and Katoh et al. 2015
mapped BBIP1/BBS18 as a linker between BBS4 and TTC8/BBS8 inside the BBSome.
External biology therefore makes `Bbs5` and especially `Ttc8` the most relevant
training perturbations, with `Lztfl1` as a close BBSome-trafficking regulator
and the IFT/transition-zone genes as same-organelle but more indirect controls.

The same-experiment evidence points to a zero or singleton self-only response,
not to a broad downstream RNA state:

- `Bbs5`, the only represented core BBSome subunit besides `Ttc8`, has
  `n_degs = 0` in the focal group.
- `Ttc8` has `n_degs = 1`, but that is `Ttc8` itself.  No downstream transcript
  passes FDR 0.05.
- `Lztfl1` and all represented IFT/transition-zone comparators above have
  `n_degs = 0` in the focal group.
- `Bbs5` and `Ttc8` focal score vectors are nearly orthogonal to each other
  and to IFT/BBSome-regulator vectors, so there is no subthreshold focal
  signature suggesting that the FDR-null calls are hiding a coherent ciliary
  transcriptional state.
- The Distributed Agents corpus reports the same pattern at the whole-atlas level:
  `Bbs5:F003` found that `Ttc8`, `Lztfl1`, `Ift88`, `Kif3b`, `Cep290`,
  `Gli1/Gli2`, `Smo`, `Lepr`, `Glp1r`, and `Htr6` did not phenocopy `Bbs5`;
  `Ttc8:F003` found that `Bbs5`, `Ift43`, `Ift81`, `Dync2h1`, `Kif3b`,
  `Lztfl1`, `Rpgrip1l`, `Ttc21b`, `Ift88`, and `Cep290` were nearly orthogonal
  to `Ttc8`; and a high-confidence corpus claim states that represented
  ciliary trafficking/signaling genes are largely buffered at the basal nuclear
  RNA level in postnatal NeuN+ neurons.

I considered whether `Bbip1` should be assigned one DEG for its own transcript,
by analogy with `Ttc8`.  The training ciliary self-RNA evidence is mixed rather
than uniformly self-positive: in the focal slice, `Ttc8` and `Arl3` pass FDR on
their own transcripts, but `Bbs5`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`,
`Dync2i1`, `Cep290`, `Rpgrip1l`, `Ttc21b`, `Lztfl1`, `Alms1`, `Adcy3`,
`B9d1`, and `Cplane1` are all negative after multiple-testing correction
despite mostly negative self log-fold changes.  With no direct `Bbip1`
signature and with the strongest same-complex downstream evidence exactly
zero, the better point prediction is that neither a downstream gene nor the
`Bbip1` target transcript itself crosses FDR 0.05 in this cell group.

## Prediction

`Bbip1`: predicted `n_degs = 0`.

## Limits

This is an extrapolation from `Bbs5`, `Ttc8`, and other ciliary genes; the
actual `Bbip1` perturbation profile is deliberately absent from the supplied
DE parquet.  The prediction also depends on an assay-specific endpoint.  A zero
FDR-level snRNA response would not imply that BBIP1 is dispensable, that the
guides failed, or that BBSome trafficking is intact; BBSome loss can change
ciliary cargo localization, cilium structure, photoreceptor and olfactory
biology, hypothalamic receptor routing, or organismal phenotypes without a
basal multi-gene nuclear-RNA program in sparse postnatal NeuN+ nuclei.  The
one-DEG alternative remains plausible if `Bbip1` self-RNA depletion happens to
be as strong and well powered as `Ttc8`, but the broader training set does not
support assigning extra downstream DEGs.
