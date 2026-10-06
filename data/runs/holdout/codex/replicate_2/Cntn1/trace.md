# Cntn1 direct forecast for `151 TH Prkcd Grin2c Glut`

## Declared endpoint and admissible measurements

- Target: `Cntn1`, from the one-row holdout manifest.
- Endpoint: `n_degs`, the number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- Direct training outcome source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Matched signed-profile source: `[local file: training_de_all_cell_groups.parquet]`.
- Target biology source: `biology_bundles/Cntn1.json`, checksum `d7901c236143ddd87047cdc58c41aaf66f03a192c96b83e21f7dd1e17045dbef`; the served biology view reported `target_outcome_exposed=false`.

The visible 151-TH count table is very sparse: 1,205/1,674 training perturbations have `n_degs = 0`, the median is 0, the 75th percentile is 1, and only the far upper tail carries tens to thousands of DEGs. So this forecast should default low unless the target biology puts Cntn1 into a strong, acute, nuclear-RNA response state.

## Cntn1 biological reach

The exact focal-population measurement shows that `Cntn1` is an available, broadly expressed feature in the matched non-target nuclei: mean log1p(CP10K) 1.619, mean raw UMI 7.36, and 23,335/23,679 nuclei expressing it. This makes a target-transcript DEG countable if the perturbation leaves a detectable RNA effect, but it is not evidence for a larger downstream state by itself.

The endpoint-blind Cntn1 card argues for only partial acute functional realization in the P16 to P37-P44 window:

- Cntn1 operates in installed cell-surface/paranodal Contactin-1-Caspr1-NF155 complexes and a neuronal-surface perineuronal-net anchoring complex.
- A disruptive edit should stop new Contactin-1 supply, but installed GPI-linked protein is not directly removed.
- A paranodal-partner proxy enters structural disassembly within 10-20 days, yet retains substantial axonal complex material later; no target-specific Contactin-1 clearance series was found.
- The functional-stock conclusion was `partially_depleted_or_leading_edge`.

I treated that as compatible with a small measured response in thalamic neurons, not with a high-DEG stress or remodeling program.

## Training perturbations used

I nominated Cntn1 analogs from the 1,674-gene training universe with the local typed gene-analog nomination resource, then prioritized exact or direct Cntn1 relationships over broad adhesion/myelination fallbacks.

The strongest specific training analogs were:

| training target | typed Cntn1 relationship | 151-TH `n_degs` | significant 151-TH genes |
| --- | --- | ---: | --- |
| `Nrcam` | exact `Cntn1-Nrcam-Ptprb` CORUM complex plus adhesion annotations | 2 | `Nrcam`, `Letm2` |
| `Cntnap1` | direct Contactin-1/Caspr1 paranodal partner | 1 | `Cntnap1` |
| `Cntnap2` | direct physical/contactin-associated relationship but juxtaparanodal rather than Cntn1-Caspr1-NF155 | 1 | `Cntnap2` |
| `Prnp` | direct GPI-surface physical relationship, mechanistically more distant | 1 | `Prnp` |

The same-experiment Finding ledger for these visible training perturbations also described this neighborhood as transcriptionally buffered rather than as a recurring downstream module: `Cntnap1:F001` reported no downstream FDR<0.10 genes across recovered groups, `Cntnap1:F002` reported that the expected paranodal/juxtaparanodal neighborhood did not phenocopy `Cntnap1`, `Nrcam:F001` reported a broadly buffered acute `Nrcam` perturbation, `Nrcam:F003` localized the only thalamic `Nrcam` downstream event to one increased `Letm2`, and `Cntnap2:F003` reported no convergence with `Cntnap1`/Kv1-complex genes despite the structural relationship.

The leading broader nominees were also small in the declared count table: `Dscam=0`, `Bsg=1`, `Tlr2=0`, `Cd47=1`, `Scn1b=2`, `Tenm4=0`, `Itgb1=0`, `Adgrl1=1`, `Fyn=0`, `Psen1=0`, `Nectin1=0`, `Nrg1=0`, `Nrxn1=1`, and `Ncam1=1`. Where these had one DEG, it was usually the target transcript itself; the two-gene analogs added only one downstream gene.

## Matched profile check

I compared the visible 151-TH signed profiles for the exact/direct and leading broad Cntn1 nominees. The Cntn1-near profiles had no shared significant downstream feature intersections in the inspected pairs:

- `Nrcam`, `Cntnap1`, `Cntnap2`, `Prnp`, and `Scn1b` each had 1-2 significant 151-TH features.
- `Nrcam` versus the inspected broad adhesion/myelination peers had zero positive or negative significant-feature intersections.
- `Cntnap1`, `Cntnap2`, `Prnp`, and `Scn1b` likewise shared no significant positive or negative feature with the inspected peers.
- Whole-profile correlations within this close cohort were near zero: for example `Nrcam`-`Cntnap1` Pearson 0.022, `Nrcam`-`Ncam1` Pearson 0.042, and `Cntnap1`-`Adgrl1` Pearson 0.029.

That profile evidence made the Nrcam `Letm2` extra call look like an isolated event, not a reason to project a two-gene Cntn1 signature.

## Forecast

I placed Cntn1 at `n_degs = 1`.

The upward bearing from broad focal-population expression and ongoing postnatal Contactin-1 demand makes an exact zero less likely than a one-feature call. The downward bearing is that the closest visible perturbations of installed neuronal surface/paranodal machinery were all buffered in the nuclear transcriptome, with `Cntnap1`, `Cntnap2`, and `Prnp` at 1 DEG and `Nrcam` at only 2 DEGs in the exact focal class. Because the literal endpoint includes the self transcript and because high Cntn1 expression makes one measurable self-feature response plausible, I kept one DEG rather than rounding to zero. I did not add a recurrent downstream gene because no close comparator supplied a coherent shared downstream program.
