# Nalcn prediction trace

## Question and resolved ambiguities

The requested held-out target list contains one perturbation, `Nalcn`, from
`143_Nalcn.csv`. I interpreted the endpoint as the exact focal-cell count of
measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, using the
same convention as the training CSV. That count includes the perturbed target
transcript itself when it is a significant row; several training ion-channel
examples with `n_degs = 1` were self-transcript-only events. I did not exclude
self rows or switch to a downstream-only endpoint.

I also treated `151 TH Prkcd Grin2c Glut` as the thalamic glutamatergic class
described in the atlas metadata. The requested `Nalcn` perturbation is absent
from both the training count CSV and the DE parquet, so no observed Nalcn
signature was used.

## Sources used

- Focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Full training differential expression:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested target manifest:
  `[local file: 143_Nalcn.csv]`
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, used for pre-interpreted
  Findings and Claims around represented calcium-channel, NMDAR, and calcium
  pump perturbations.
- Distributed Agents runtime profile analysis, used to compare Wilcoxon-score signatures
  among candidate analog perturbations in the exact focal cell group.
- External literature on the NALCN channelosome and regulation:
  - Lu et al. 2008, Nature, doi:10.1038/nature07579, PMID:19092807.
  - Ford et al. 2018, Pain, doi:10.1097/j.pain.0000000000001258,
    PMID:29746349.
  - Kschonsak et al. 2021, Nature, doi:10.1038/s41586-021-04313-5,
    PMID:34929720.
  - Monteil et al. 2023, Physiological Reviews,
    doi:10.1152/physrev.00014.2022, PMID:37615954.
  - Usher et al. 2025, Science Advances, doi:10.1126/sciadv.ads6004,
    PMID:40085699.

## Computational checks

The focal training table has 1,674 non-held-out perturbations. Its count
distribution is strongly zero-inflated:

- `n_degs = 0`: 1,205 targets
- `n_degs = 1`: 276 targets
- `1 <= n_degs < 10`: 363 targets
- `10 <= n_degs < 100`: 63 targets
- `n_degs >= 100`: 43 targets

Thus the median count is 0 and the 75th percentile is 1. A prediction of a
single DEG is not a claim of a broad downstream state; it is the common
self/singleton regime of this endpoint.

For mechanistic analogs I filtered the parquet to the exact focal cell group
and a hand-curated set of NALCN-adjacent perturbations: voltage-gated and leak
channels, calcium-channel subunits, GPCR/Src-side regulators of NALCN, SNARE
or vesicle-release genes present in training, calcium pumps, and NMDAR
counterexamples. The non-obvious part of the operation was simply:

```python
filt = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(analog_targets)
n_fdr05 = (target_rows["pvals_adj"] < 0.05).sum()
```

That recovered 535,029 focal rows for 31 analog perturbations, 17,259 measured
features per available perturbation. I also ran Distributed Agents `profile_compare` on
27 focal ion-channel/receptor analogs with `scores` as the signed profile,
`pvals_adj < 0.05` as significance, and the 1,674 training targets as the
eligible universe.

The pairwise signature analysis reinforced the count-level result. Related
channel perturbations were close to orthogonal in Wilcoxon-score space: within
the candidate cohort, `Hcn1` versus `Hcn2` had cosine 0.006, `Kcnq2` versus
`Kcnq3` had cosine 0.044, `Scn1a` versus `Scn2a` had cosine -0.027, and
`Cacna1g` versus `Atp2b1` had cosine -0.009. Whole-profile positive neighbors
from the full eligible universe were also weak for quiet channel anchors:
`Hcn1`'s best eligible cosine was only 0.050 and `Fyn`'s was 0.086. The
stronger `Cacna1g` signature was real but still only modestly recurrent, with
eligible whole-profile cosines 0.194 to `Wdfy3` and 0.163 to `Atp1a3`.

## Target-specific reasoning

### Nalcn

**External biology.** NALCN is the pore-forming sodium leak channel that
conducts a depolarizing background Na+ current and helps set resting membrane
potential in neurons. The pore associates with FAM155A, UNC79, and UNC80 in the
NALCN channelosome; Kschonsak et al. 2021 resolved the approximately 1 MDa
human complex and showed UNC79/UNC80 dock intracellularly onto the
NALCN-FAM155A subcomplex. NALCN can also be gated by neuropeptides: Lu et al.
2008 showed that substance P and neurotensin activate an NALCN/UNC80 channel
in mouse hippocampal and ventral tegmental neurons through TACR1 and Src-family
kinases rather than through a canonical G-protein mechanism. Ford et al. 2018
showed that NALCN current raises the excitability of spinal projection neurons
and is required for substance-P-evoked firing in that circuit. Monteil et al.
2023 review the channel's roles in respiratory rhythm, sleep, locomotor
behavior, and neuronal excitability. Usher et al. 2025 add a modulatory link to
SNARE proteins, with syntaxin/SNAP25 inhibiting NALCN current in heterologous
systems and primary neurons.

**Direct same-complex evidence in training.** There was no direct
channelosome proxy: `Unc79`, `Unc80`, `Fam155a`, and `Fam155b` were absent from
the focal training-count table. The same-experiment Distributed Agents corpus also had
no `Nalcn` Finding or Claim because `Nalcn` was held out. This removes the
strongest possible source of within-dataset transfer and makes the prediction
an extrapolation from looser channel and receptor analogs.

**Upstream or regulatory analogs.** The receptor/Src side of NALCN activation
was quiet in the focal endpoint:

| training perturbation | observed `n_degs` | focal expression-pattern evidence | relationship to Nalcn |
| --- | ---: | --- | --- |
| `Ntsr1` | 0 | no FDR<0.05 genes; leading adjusted p-values were 1 | neurotensin can activate NALCN, but this receptor perturbation did not leave a sustained 151 TH RNA state |
| `Chrm3` | 0 | no FDR<0.05 genes; leading adjusted p-values were 1 | M3 muscarinic receptors can gate NALCN in heterologous or endocrine contexts, but the focal neuronal perturbation was flat |
| `Chrm2` | 0 | no FDR<0.05 genes; leading adjusted p-values were 1 | acetylcholine-side GPCR counterexample; not the direct M3 mechanism |
| `Fyn` | 0 | no FDR<0.05 genes; `Fyn` itself was only subthreshold at adjusted p = 0.0899 | Src-family kinase candidate; loss did not mimic an NALCN-coupled transcriptional response |
| `Tacr3` | 0 | no FDR<0.05 genes | weak counterexample only, because `Tacr1`, the Lu et al. substance-P receptor, was not a represented training target |
| `Stx1b` | 0 | no FDR<0.05 genes | syntaxin-family perturbation related to the Usher et al. SNARE/NALCN mechanism, but not exact `Stx1a` or `Snap25` |
| `Stxbp1` | 1 | the only hit was `Stxbp1` itself | vesicle-release regulator; argues against a broad basal SNARE-to-NALCN RNA state |

The pairwise profiles among `Fyn`, `Chrm2`, `Chrm3`, and `Ntsr1` were
noise-level rather than a hidden receptor-channel module. For example,
`Fyn`-`Ntsr1` cosine was 0.027, `Fyn`-`Chrm3` was 0.020, and
`Chrm2`-`Chrm3` was -0.008.

**Ion-channel and excitability analogs.** Direct perturbation of mature
channels in the same focal class was usually null or target-transcript-only:

| training perturbation | observed `n_degs` | focal expression-pattern evidence | relationship to Nalcn |
| --- | ---: | --- | --- |
| `Hcn1` | 0 | no FDR<0.05 genes | leak/pacemaker-current analog; flat despite related resting-potential biology |
| `Hcn2` | 1 | only `Hcn2` was significant, log2FC -0.853, adjusted p = 3.11e-31 | pacemaker-current analog, self-only |
| `Kcnq2` | 1 | only `Kcnq2` was significant, log2FC -0.776, adjusted p = 2.12e-28 | subthreshold M-current analog, self-only |
| `Kcnq3` | 1 | only `Kcnq3` was significant, log2FC -0.379, adjusted p = 0.00717 | subthreshold M-current analog, self-only |
| `Scn1a` | 1 | only `Scn1a` was significant, log2FC -1.075, adjusted p = 5.87e-38 | voltage-gated Na+ channel, self-only |
| `Scn2a` | 1 | only `Scn2a` was significant, log2FC -0.401, adjusted p = 6.46e-06 | voltage-gated Na+ channel, self-only |
| `Scn8a` | 1 | only `Scn8a` was significant, log2FC -0.458, adjusted p = 1.35e-05 | voltage-gated Na+ channel, self-only |
| `Scn1b` | 2 | `Scn1b` and `Jun` passed FDR | Na-channel beta subunit, still only a singleton downstream response |
| `Cacna1a` | 0 | no significant focal genes | CaV pore-subunit counterexample |
| `Cacna1d` | 0 | no significant focal genes | CaV pore-subunit counterexample |
| `Cacna1e` | 0 | no significant focal genes | CaV pore-subunit counterexample |
| `Cacna2d1` | 1 | only `Cacna2d1` itself passed FDR | CaV auxiliary subunit, self-only |
| `Cacna2d2` | 0 | no significant focal genes | CaV auxiliary subunit, flat |
| `Cacnb2` | 0 | no significant focal genes | CaV auxiliary subunit, flat |
| `Cacnb4` | 1 | only `Cacnb4` itself passed FDR | CaV auxiliary subunit, self-only |
| `Cacna1g` | 12 | 12 FDR<0.05 hits including `Cacna1g` down, `Ptprn` up, `Stmn4` down, `Cpne7` down, `Jun` down, and `Iyd` up | best positive thalamic-channel example, but a T-type Ca2+ channel with a narrow Cav3.1-specific state |

The Distributed Agents Cacna1g Findings are important here. The selected corpus reports
that acute `Cacna1g` loss had a small thalamic footprint while represented
CaV-family perturbations mostly did not phenocopy it; Cacna1a, Cacna1d,
Cacna1e, Cacna2d1, Cacna2d2, Cacnb2, Cacnb4, Cacng2, and Cacng3 all had zero
downstream genes in the same 151 TH group at the corpus' FDR<0.10 downstream
threshold. Therefore `Cacna1g` is evidence that channel perturbations can be
visible in thalamic neurons, but it is not safe to transfer its 12-gene count
directly to NALCN. Its own profile was only weakly related to KCNQ, HCN, and
SCN perturbations; for instance `Cacna1g`-`Scn1a` cosine was -0.020 and
`Cacna1g`-`Hcn2` was -0.056.

**Stronger ion-homeostasis counterexamples.** The focal class is not globally
incapable of writing activity or ion stress into nuclear RNA. `Atp2b1` had 22
DEGs with an immediate-early/activity-like `Fos`, `Nr4a1`, and `Vgf` module;
`Atp1a3` had 80 DEGs; `Grin1` had 89 DEGs; and `Atp2a2` had 187 DEGs dominated
by an ER-stress/UPR/ISR program. The same-experiment corpus places `Atp2a2`
in a SERCA2-specific proteostasis state and `Grin1` in an NMDAR-specific,
mixed synaptic/stress state. These perturbations show that a Na+ pump, Ca2+
pump, or obligatory NMDAR-subunit loss can create tens to hundreds of focal
DEGs, but they are mechanistically more disruptive than reducing a background
Na+ leak conductance and they did not align with the Cacna1g or voltage-channel
profiles. I treated them as upper-bound counterexamples, not as count donors.

**Zero/nonzero and count call.** The relevant in-dataset evidence points away
from a coordinated NALCN downstream transcriptome: exact channelosome partners
were absent; represented GPCR/Src/SNARE-side nodes were flat; and the best
represented ion channels usually produced either zero or self-only counts.
External biology, however, makes NALCN a real neuronal excitability gene rather
than a random silent target, and several well-expressed ion-channel targets
with no downstream program still produced a single significant self-transcript
row. I therefore predict `Nalcn` lands in the same self/singleton regime rather
than at a Cacna1g-like 10-20 gene state or at a Grin1/Atp2b1/Atp2a2 state.

Point prediction: `Nalcn -> 1`.

## Limits and extrapolation

The main limitation is the lack of a same-complex training perturbation:
`Unc79`, `Unc80`, and `Fam155a` would have been the clean analogs for an NALCN
loss-of-function count, but they were not in the training table. `Tacr1`,
`Stx1a`, and `Snap25` were also unavailable, so the receptor and SNARE
comparisons are one step removed. The count of 1 relies partly on the chance
that the `Nalcn` transcript itself crosses FDR; target-RNA reduction is not a
reliable editing-efficiency measurement in this assay, and a true count of 0
would be plausible if `Nalcn` nuclear RNA is too sparse or not reduced enough.
Conversely, NALCN has strong electrophysiological roles that could create
activity-dependent transcription in a subset of thalamic neurons, but the
training HCN/KCNQ/SCN and GPCR/Src signatures argue that such physiology often
does not become a broad 3-4 week steady-state snRNA-seq footprint after sparse
juvenile CRISPR.
