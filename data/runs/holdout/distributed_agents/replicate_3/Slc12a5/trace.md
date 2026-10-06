## Question and interpretation

The held-out target for this run is `Slc12a5`. I interpreted the task as a
point prediction of the number of genes that would pass `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` after acute AAV/CRISPR loss of `Slc12a5`, using the
same Scanpy Wilcoxon/BH differential-expression endpoint as the supplied
training data. `Slc12a5` is absent from both the supplied all-cell-group DE
parquet and the focal-cell DEG-count CSV, so no direct `Slc12a5` row was used.

I resolved the main ambiguity as follows: `n_degs` counts all measured genes
that pass the BH threshold, including the targeted transcript itself when it is
measured and significant. Therefore a predicted value of `1` means a
self/transporter-local response but no reproducible secondary transcriptional
module.

## Sources

- Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  This contained 1,674 non-held-out targets for the focal cell group.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` and inspected
  focal signed Wilcoxon-score/log2FC profiles for chloride-transporter,
  GABA_A, glutamate-receptor, calcium-channel, and Na/K/Ca pump comparators.
- Requested-target manifest:
  `[local file: 209_Slc12a5.csv]`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`. I queried target contexts and
  claims for `Slc12a2`, `Wnk1`, `Wnk3`, and `Stk39`. There was no precomputed
  direct `Slc12a5` target card, while the corpus did contain a high-confidence
  claim that acute perturbation of the represented WNK/SPAK/cation-chloride
  cotransporter pathway members failed to produce a shared basal neuronal
  nuclear-RNA signature in this screen.
- PubMed literature for external biology:
  Rivera et al. 1999, DOI `10.1038/16697`, PMID `9930699`, established that
  developmental induction of KCC2 makes mature GABA_A responses
  hyperpolarizing by extruding chloride.
  Hubner et al. 2001, DOI `10.1016/s0896-6273(01)00297-5`, PMID `11395011`,
  showed that KCC2 disruption in mice impairs early inhibitory signaling and is
  lethal at birth, demonstrating essential chloride-extrusion biology.
  Kahle et al. 2005, DOI `10.1073/pnas.0508307102`, PMID `16275911`, showed
  that WNK3 can activate NKCC1 while inhibiting KCC1/KCC2 through altered
  phosphorylation and surface expression, placing `Slc12a5` in a
  post-translational chloride-homeostasis pathway.
  Sinha et al. 2022, DOI `10.3389/fnmol.2022.856262`, PMID `36311015`, found
  altered chloride reversal potential and intrinsic/synaptic excitability in
  WNK3 knockout layer V pyramidal neurons, while not detecting altered
  SPAK/OSR1, NKCC1, or KCC2 phosphorylation in that basal context.

## Dataset calculations

I first checked the endpoint distribution in the focal count table. The median
target had zero DEGs, the 75th percentile was one DEG, 469/1674 targets were
nonzero, only 106/1674 had at least ten DEGs, and the strongest broad-response
targets were chromatin, RNA-processing, proteasome, and protein-homeostasis
genes such as `Uba5`, `Tpr`, `Sin3a`, `Rnpc3`, `Zbtb7a`, `U2af2`, `Psmb4`,
`Hnrnpu`, `Yy1`, and `Elp1`.

I then filtered the parquet to the focal cell group and the mechanistic
comparators below. For each comparator I recomputed the number of focal rows
with `pvals_adj < 0.05` and examined the significant rows and largest absolute
Wilcoxon-score rows to separate self-only signals from secondary-expression
programs. The useful focal comparator counts were:

| comparator | focal `n_degs` | expression-pattern evidence |
| --- | ---: | --- |
| `Slc12a2` | 0 | NKCC1, the nearest SLC12 cation-chloride cotransporter in the training endpoint, had no focal FDR genes; its largest absolute focal scores all had `pvals_adj = 1`. |
| `Wnk1` | 0 | Canonical CCC regulator; no focal FDR genes and no convincing focal signed-score program. |
| `Wnk3` | 1 | The only focal FDR gene was `Ppp2cb` down, log2FC `-0.554`, adjusted `p = 0.0315`; this is a one-gene state, not a broad KCC/NKCC program. |
| `Stk39` | 0 | SPAK kinase downstream of WNKs; no focal FDR genes. |
| `Gabra1` | 1 | Self-only GABA_A alpha-subunit response: `Gabra1` down, adjusted `p = 4.26e-18`. |
| `Gabrg2` | 1 | Self-only GABA_A gamma-subunit response: `Gabrg2` down, adjusted `p = 4.66e-24`. |
| `Gabrd` | 2 | `Gabrd` self plus one weak secondary gene. |
| `Gabrb2` | 4 | `Gabrb2` self, `Nr4a1`, `Vgf`, and `Nalf1`; `Fos`/`Npas4` were nominal activity-gene shifts but just missed FDR at about 0.056. |
| `Slc6a1` | 0 | GABA transporter perturbation was flat. |
| `Grin2a` | 1 | NMDAR subunit, self-only. |
| `Grin2b` | 2 | NMDAR subunit, mostly self with one secondary gene. |
| `Grin1` | 89 | A counterexample: an obligatory NMDAR subunit drove a larger thalamic program including `Scg2`, `Stmn4`, `Kctd16`, `Gpm6a`, `Dync1li2`, and `Tspan7`. |
| `Atp1a1` | 1 | Na/K pump paralog, self-only. |
| `Atp1a2` | 0 | Na/K pump paralog, flat. |
| `Atp1a3` | 80 | Neuronal Na/K pump alpha subunit, a broad counterexample with `Atp2a2`, `Ache`, `Prkcg`, `Rgs16`, `Notum`, `Mtmr11`, and other genes. |
| `Cacna1g` | 12 | T-type calcium-channel perturbation produced a modest activity-like state including `Ptprn`, `Stmn4`, `Cpne7`, `Ly6e`, `Jun`, and `Notum`. |

The same-experiment Distributed Agents corpus agreed with the direct parquet
inspection. It summarized `Slc12a2` as pan-neuronally null at FDR < 0.10, noted
that `Wnk1`, `Wnk3`, `Stk39`, and `Slc12a2` did not converge on a common
WNK/SPAK/CCC transcriptional module, and highlighted that `Gabrb2` can create a
small focal thalamic activity-gene response whereas `Slc12a2` and most GABA_A
subunit perturbations do not phenocopy it.

## Target-specific prediction

### `Slc12a5`

`Slc12a5` encodes KCC2, the main neuronal potassium-chloride cotransporter that
exports chloride and makes GABA_A receptor currents inhibitory in mature
neurons. That makes it a much better-matched neuronal chloride target than
`Slc12a2`/NKCC1, and because KCC2 is neuron-specific and focal glutamatergic
neurons measure `Slc12a5` robustly enough for DE rows, a complete zero seemed
less likely than a self-detectable perturbation.

The within-dataset evidence argued strongly against a broad response, though.
Directly represented chloride-transporter machinery was almost silent:
`Slc12a2 = 0`, `Wnk1 = 0`, `Stk39 = 0`, and `Wnk3 = 1` in this exact cell
group. Distributed Agents further found no shared WNK/SPAK/CCC nuclear-RNA state across
these genes in the wider screen. That is mechanistically relevant because the
literature places KCC2 under WNK/SPAK/OSR1 phosphorylation control; a chloride
flux or KCC2 phosphorylation phenotype can therefore be real without producing
a broad snRNA-seq module.

The GABAergic counterfactual panel pointed in the same direction. Removing
major GABA_A receptor subunits in `151 TH Prkcd Grin2c Glut` was mostly
self-only to very small: `Gabra1 = 1`, `Gabrg2 = 1`, `Gabrd = 2`, and
`Gabrb2 = 4`; removing `Slc6a1` gave `0`. Those perturbations can plausibly
change inhibitory signaling more directly than KCC2 transcript reduction, yet
only `Gabrb2` induced a few secondary activity-associated genes. Broader
excitability perturbations proved the assay could see a large state when the
biology drove one: `Grin1 = 89`, `Atp1a3 = 80`, and `Cacna1g = 12`. I therefore
used those as upper counterexamples, not as close phenocopies.

My point prediction is `1`: `Slc12a5` is expected to be a detectable nonzero
perturbation, most likely through the targeted KCC2 transcript itself, but not
to cross the threshold into the 4- to 12-gene activity-like band or the
80-plus-DEG NMDAR/Na-pump band.

## Limits

The strongest limitation is that no `Slc12a5` perturbation signature is present
in either supplied input, and the Distributed Agents corpus also had no held-out
`Slc12a5` finding. `Slc12a6`, `Slc12a7`, `Wnk2`, `Wnk4`, and `Oxsr1` were not
training perturbations in the focal count table, so the same-family panel is
incomplete. The experiment measured nuclear RNA after sparse partial CRISPR,
not KCC2 protein, membrane localization, transporter phosphorylation, chloride
flux, GABA reversal potential, or seizure/network activity. Finally, KCC2 has
developmental and structural roles that may require stronger, earlier, or
cell-type-specific loss than this P16-to-P37/44 mosaic screen delivered.
