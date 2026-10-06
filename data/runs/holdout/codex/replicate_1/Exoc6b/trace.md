# Exoc6b direct n_degs forecast

## Target and endpoint

- Target: `Exoc6b`
- Cell class: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of focal-class measured genes with Wilcoxon BH-adjusted `pvals_adj < 0.05` in the perturbation differential-expression table.
- Point prediction: `1`

## Target biology used

Provenance: declared `Exoc6b` biology bundle,
`[local file: Exoc6b.json]`,
served as biology-only characterization with sha256
`973bb7ec632854f39bc32dde074a180b1adb677cc35d632737cb85602566ae2a`.

- Exact target reach in the focal class is high enough that `Exoc6b` is a real assayed transcript, not an absent target: `19,493 / 23,679` non-target nuclei expressed it (`82.3219%`), with mean `1.27594` CP10K and mean `1.99274` raw UMI.
- The molecular prior is compatible with loss being realized by harvest: EXOC6B is a Sec15-family dynamic exocyst component, the edit would stop new functional protein synthesis, and a 21-28 day interval is likely long enough to substantially deplete a renewable component.
- The same prior is weak for a large thalamic survivor-state RNA response: the card found no matched postnatal mouse-neuronal Exoc6b loss study, only systemic germline mouse lethality and human fibroblast/ciliary evidence, and EXOC6 can buffer EXOC6B for constitutive cargo delivery in cultured non-neural cells.

## Focal training counts

Provenance: declared focal count table,
`[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.

- The focal class is sparse over the 1,674 training perturbations:
  `1,205` have zero DEGs, the median is `0`, the 75th percentile is `1`,
  the 90th percentile is `2`, the 95th percentile is `18`, and the maximum is
  `2,677`.
- There was no measured training knockout of an `Exoc*` exocyst subunit, so I used mechanistically broader vesicle-tethering, Rab, SNARE, coat/adaptor, COG/TRAPP, and endosomal-sorting perturbations as local scale references.
- Direct synaptic vesicle or plasma-membrane exocytosis machinery was almost all null or self-only: `Cplx1 1`, `Cplx2 0`, `Stx1b 0`, `Stxbp1 1`, `Syn1 1`, `Syn2 0`, `Syt2 0`, `Unc13a 0`, `Unc13b 0`, `Unc13c 0`, `Vamp1 1`.
- Related non-exocyst traffic genes were likewise mostly quiet in the count table: `Ap1b1 1`, `Ap1s2 0`, `Ap3b1 0`, `Ap4s1 0`, `Cog4 0`, `Cog5 0`, `Rab18 0`, `Rab27a 0`, `Rab3gap1 0`, `Rab3gap2 0`, `Sec23a 0`, `Stx16 1`, `Vps35l 0`, `Vps41 0`, `Vps53 0`, `Trappc10 0`, `Trappc6b 0`, `Trappc9 0`.
- The larger trafficking responses were off-axis upper references rather than direct Exoc6b scale matches: `Rab7 501` for an endolysosomal lesion, `Vps54 31` and `Vps35 17` for Golgi/endosomal retrograde sorting, and `Sec63 11` for ER translocation or stress.

## Focal expression-table checks

Provenance: declared expression parquet,
`[local file: training_de_all_cell_groups.parquet]`,
queried only at `group_name = '151 TH Prkcd Grin2c Glut'` for training perturbations.

- Each selected training perturbation had `17,259` measured focal-class rows.
- For 33 closer coat/Rab/SNARE/synaptic-release/COG/TRAPP/VPS genes queried in the focal parquet, `25` had no BH<0.05 rows, `7` had exactly one row, and the only member with more than one was `Vps35` with `17`.
- The one-row responses for `Ap1b1`, `Arl3`, `Cplx1`, `Stx16`, `Stxbp1`, `Syn1`, and `Vamp1` were all driven by the perturbed target transcript itself rather than a downstream program.
- Across the full focal training table, exactly-one-DEG perturbations were common (`276 / 1,674`), and most of them (`237 / 276`) were self-target-only. This makes a one-DEG forecast the natural way to represent a likely quiet downstream state with a potentially significant self transcript.

## Synthesis

I predicted no broad downstream response from `Exoc6b` loss in the recovered
thalamic glutamatergic nuclei. The target is present and probably depleted by
the harvest window, but the postnatal neuronal consequence is unresolved, the
nearest assayed exocytosis/release machinery is overwhelmingly 0-1 DEG in this
same cell class, and the broader 11-501 DEG trafficking hits are mechanistically
different endosomal, Golgi, lysosomal, ER, or tubulin-maintenance lesions.

Because the endpoint includes all measured genes, the high exact focal
expression of `Exoc6b` leaves a self-transcript hit plausible even if no
downstream gene clears FDR. I therefore placed the point at one significant
gene rather than zero or an off-axis trafficking scale.

The withheld `Exoc6b` differential-expression profile, `Exoc6b` DEG count, and
same-experiment `Exoc6b` report were not queried or used.
