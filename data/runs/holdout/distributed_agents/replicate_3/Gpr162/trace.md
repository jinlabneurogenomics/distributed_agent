# Gpr162 DEG-count prediction

## Question and interpretation

The requested manifest contains one held-out perturbation:

| target_name |
| --- |
| Gpr162 |

I interpreted `n_degs` as the number of measured genes, including the perturbed
target transcript itself if it is measured, with `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` cells after acute AAV-CRISPR loss of function. The
held-out `Gpr162` perturbation has no rows in the training parquet or the
training-count CSV, so the prediction has to be transferred from non-held-out
perturbations and from external knowledge of GPR162 biology.

I resolved the main integer ambiguity as follows: a prediction of 1 means I
expect a direct Gpr162 mRNA decrease to clear FDR, but I do not expect a broader
secondary transcriptional state.

## Sources used

- `training_de_all_cell_groups.parquet`: filtered with PyArrow to
  `group_name == "151 TH Prkcd Grin2c Glut"` and queried for matched receptor,
  G-protein, interferon, and Gpr162-as-readout rows.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: used as the observed
  endpoint for all 1,674 non-held-out focal-cell perturbations.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`: no Gpr162-specific claims were
  present; I used corpus claims on represented GPCR/cAMP and IRF/IFN
  perturbations as same-experiment context.
- Distributed Agents runtime profile-neighbor analysis over the focal parquet rows for
  `Gpr158`, `Gprasp2`, `Gpr161`, `Gnao1`, `Gnas`, `Adrb2`, `Cnr1`, and `Irf3`.
- External literature from NCBI PubMed:
  - Caruso et al. 2014, DOI `10.1016/j.gene.2014.09.042`, PMID `25275856`.
  - Caruso et al. 2016, DOI `10.1016/j.gene.2016.01.044`, PMID `26827797`.
  - Lindqvist et al. 2023, DOI `10.1016/j.isci.2023.108416`, PMID `38077141`.
  - Long et al. 2023, DOI `10.1038/s41392-022-01224-3`, PMID `36725837`.
  - Kakarala and Jamil 2014, DOI `10.1016/j.ympev.2014.01.022`,
    PMID `24503482`.

## Dataset checks and calibration

The training count file has 1,674 focal-cell perturbations. It is extremely
zero-inflated: 1,205 targets have `n_degs = 0`, 366 have `1 <= n_degs <= 10`,
and only 103 have more than 10. The median is 0, the 90th percentile is 2, and
the mean is 14.1 only because rare perturbations such as `Uba5`, `Tpr`,
`Sin3a`, `Rnpc3`, and `Zbtb7a` produce hundreds to thousands of DEGs.

Filtering the parquet to `151 TH Prkcd Grin2c Glut` yielded 28,891,566
rows, 1,674 training perturbations, and 17,259 measured genes per perturbation.
I then queried biologically relevant receptor and signaling comparators in that
focal slice rather than using all perturbations as an undifferentiated pool.

The assayed GPCR/receptor comparators were quiet in this focal group:

| comparator class | focal training observations |
| --- | --- |
| `Gpr*` targets | `Gpr158 = 1`, `Gprasp2 = 1`, `Gpr156 = 0`, `Gpr161 = 0`, `Gpr179 = 0`, `Gpr45 = 0`, `Gprc5b = 0` |
| adrenergic receptors | `Adra1a = 0`, `Adra2a = 0`, `Adra2b = 0`, `Adrb2 = 0`, `Adrb3 = 0` |
| serotonin receptors | `Htr1a`, `Htr1b`, `Htr1f`, `Htr2a`, `Htr2b`, `Htr2c`, `Htr3a`, `Htr3b`, `Htr4`, `Htr6`, `Htr7` were all 0 |
| dopamine receptors | `Drd2 = 0`, `Drd4 = 0`, `Drd5 = 0` |
| other neuromodulator receptors | `Sstr5 = 0`, `Galr1 = 0`, `Npy1r = 0`, `Cnr1 = 1` |
| core GPCR transducers | `Gnao1 = 1`, `Gnal = 0`, `Gnas = 0`, `Gnb5 = 0`, `Rgs6 = 0` |

For expression-pattern evidence, I inspected the top focal features of these
same comparators. The one-hit signatures for `Gpr158`, `Gprasp2`, and `Gnao1`
were self-transcript effects:

| target | n_degs | best focal evidence |
| --- | ---: | --- |
| `Gpr158` | 1 | `Gpr158` down, log2FC `-0.991`, FDR `3.39e-26`; no other FDR genes |
| `Gprasp2` | 1 | `Gprasp2` down, log2FC `-0.491`, FDR `0.0071`; no other FDR genes |
| `Gnao1` | 1 | `Gnao1` down, log2FC `-0.591`, FDR `9.42e-07`; no other FDR genes |
| `Cnr1` | 1 | one isolated `Srcap` increase, log2FC `0.300`, FDR `0.0098`; not a GPCR module |
| `Gpr161` | 0 | minimum focal FDR was 1.0 |
| `Adrb2` | 0 | minimum focal FDR was 0.551 |
| `Gnas` | 0 | minimum focal FDR was 1.0 |
| `Irf3` | 0 | minimum focal FDR was 1.0 |

The Gpr162 transcript itself was measurable as a readout in this focal cell
group: it was significantly down after broad high-DEG perturbations such as
`Sin3a` (log2FC `-0.408`, FDR `3.08e-12`), `Hnrnpu` (log2FC `-0.369`, FDR
`6.51e-10`), `Thap11` (log2FC `-0.187`, FDR `3.60e-05`), and `Zbtb7a`
(log2FC `-0.154`, FDR `1.55e-04`). I therefore did not treat Gpr162 as an
unexpressed receptor in the focal group.

The profile-neighbor run confirmed that the selected GPCR and IRF anchors have
zero or one significant genes each in this context. I used it as a diagnostic
check, not as a signature match for Gpr162, because Gpr162 itself is held out
and has no observed profile to correlate.

The Distributed Agents corpus supplied useful negative context:

- Claim `claim:944ca6185dd70e5a895c` reports that represented
  Gbeta5/R7-adjacent GPCR/RGS/GIRK perturbations, including `Gpr158`,
  `Gpr179`, `Gnb5`, and `Rgs6`, were largely uncoupled from a shared
  postnatal neuronal transcriptomic program.
- Claim `claim:5778f7e46773642bd0bd` reports that dopamine/GPCR and
  cAMP-pathway perturbations did not collapse into one durable basal neuronal
  mRNA module.
- Claim `claim:9f69c85a0a28574c603c` reports that neuromodulatory GPCRs and
  proximal Gq/PLC/cAMP effectors generally lacked a common basal nuclear-RNA
  output.
- Claim `claim:f6c096810947e5d88efb` reports that basal juvenile NeuN+
  neuronal nuclei did not show a shared MDA5/type-I-interferon/IRF module after
  represented RNA-sensing or interferon-pathway perturbations.

## Target-specific reasoning

### Gpr162

GPR162 is an orphan rhodopsin-family/class-A GPCR with broad neuronal
expression in mouse brain, including hypothalamic, amygdalar, ventral-tegmental,
and hippocampal regions implicated in feeding and reward (Caruso et al. 2014;
Caruso et al. 2016). Lindqvist et al. identified GPR162 as a CART receptor in
pancreatic beta cells and tied it to CART-dependent exocytosis and cytoskeletal
arrangement, not to a canonical large transcription-factor module. Long et al.
found that GPR162 overexpression can interact with STING and amplify
radiotherapy-induced DNA-damage/IRF3/type-I-IFN signaling in cancer models, but
that is an overexpression plus ionizing-radiation setting, not basal Gpr162
loss in postmitotic NeuN+ neurons. A sequence-structure GPCR phylogeny grouped
GPR162 nearest predicted adrenergic-like orphan receptors (Kakarala and Jamil
2014), which made adrenergic and cAMP/G-protein training perturbations useful
counterexamples.

The best same-experiment analogs were therefore receptor and GPCR-transducer
perturbations rather than chromatin or proteostasis hits that happen to regulate
the Gpr162 transcript. Those analogs argue against a broad effect:

- Other assayed `Gpr*` genes in `151 TH Prkcd Grin2c Glut` were 0 to 1 DEG.
  The nonzero cases were dominated by the target transcript itself
  (`Gpr158`, `Gprasp2`) rather than a shared downstream program; `Gpr161`,
  `Gpr156`, `Gpr179`, `Gpr45`, and `Gprc5b` were FDR-flat.
- Adrenergic receptor perturbations, the closest literature-suggested
  receptor family proxy, were all zero DEG in this focal group despite 154 to
  274 matched perturbed cells for `Adra1a`, `Adra2a`, `Adra2b`, `Adrb2`, and
  `Adrb3`.
- Gs/Golf/Gi/o-adjacent perturbations were also zero or self-only
  (`Gnas = 0`, `Gnal = 0`, `Gnb5 = 0`, `Gnao1 = 1`). This makes it unlikely
  that loss of an orphan GPCR in its basal ligand environment will propagate
  into a stable cAMP/CREB-like nuclear RNA response.
- If the Long et al. STING connection were relevant here, IRF/IFN receptor
  loss or RNA-sensing perturbations might have exposed an antiviral module.
  Instead `Irf3`, `Ifnar1`, `Ifnar2`, `Ifngr1`, and `Ifngr2` were all zero in
  this focal group, matching the same-experiment corpus conclusion that this
  basal neuronal IFN axis was off.

The point estimate is `1`: I expect no secondary Gpr162-driven state but do
expect the focal Gpr162 transcript, which is detectable and regulatable in this
cell group, to be knocked down enough to pass FDR as the only DEG. This is the
same response shape as `Gpr158`, `Gprasp2`, and `Gnao1`.

## Limits

This is a weak extrapolation because no close Gpr162 paralog, no CART ligand
perturbation, and no Tmem173/STING perturbation are present in the focal
training set. GPR162 is an orphan or recently deorphanized receptor with
limited neuronal loss-of-function literature; its ligand occupancy in the
`151 TH Prkcd Grin2c Glut` state is unknown. The one-versus-zero call also
depends on direct target-mRNA detection, which varies with guide position,
transcript abundance, nonsense-mediated decay, and the number of recovered
perturbed nuclei. If the Gpr162 transcript itself misses FDR, the predicted
downstream count would collapse to zero.
