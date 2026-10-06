# DEG-count prediction for held-out `Cxcr2`

## Question and interpretation

The requested held-out readout is the number of genes passing
Benjamini-Hochberg FDR 0.05 after `Cxcr2` CRISPR loss of function in
`151 TH Prkcd Grin2c Glut` nuclei. I treated the endpoint as a focal-cell
assay readout, not as a generic score of CXCR2 biological importance. The
manifest for this run contains exactly one held-out target:

```text
Cxcr2
```

`Cxcr2` is absent from the training endpoint table and from the training
perturbation signatures, as expected for a held-out target. Direct CXCR2 ligands
such as `Cxcl1`, `Cxcl2`, and `Cxcl5` were not represented as perturbation
targets in the training count file, so I used the represented chemokine
receptors, innate cytokine receptors, and downstream inflammatory signaling
nodes as imperfect but assay-matched analogs.

## Sources used

- `training_de_all_cell_groups.parquet`: per-gene DE signatures for the
  non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the focal-cell observed
  `n_degs` labels for non-held-out perturbations.
- `049_Cxcr2.csv`: the held-out target list for this run.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`, especially `target_context`,
  `search_claims`, and `candidate_set_topology` for represented chemokine,
  TLR/IL-1/TNF/NF-kappaB, and cytokine/JAK-STAT training targets.
- Distributed Agents runtime profile comparison over the focal `scores` profiles for
  `Ccr2`, `Cx3cr1`, `Cxcr4`, `Tlr2`, `Tlr4`, `Il1r1`, `Il1rap`,
  `Nfkb1`, `Stat1`, `Il6ra`, and `Il6st`.
- Independent PubMed literature for CXCR2 mechanisms:
  Matsushima, Yang & Oppenheim 2022, DOI `10.1016/j.cyto.2022.155828`;
  Rajarathnam et al. 2018, DOI `10.1016/j.cellsig.2018.11.004`;
  Eash et al. 2010, DOI `10.1172/JCI41649`;
  Semple, Kossmann & Morganti-Kossmann 2009, DOI
  `10.1038/jcbfm.2009.240`; Veenstra & Ransohoff 2012, DOI
  `10.1016/j.jneuroim.2012.02.016`; Semple et al. 2010, DOI
  `10.1016/j.nbd.2010.06.015`; Xia & Hyman 2002, DOI
  `10.1016/s0165-5728(01)00463-5`; Cao et al. 2016, DOI
  `10.1016/j.brainresbull.2016.09.016`; Chai et al. 2019, DOI
  `10.1096/fj.201802359RR`; Perez-Nievas et al. 2021, DOI
  `10.1186/s12974-021-02371-0`; Cao et al. 2023, DOI
  `10.1186/s12974-023-02780-3`.

## Dataset checks and computations

I first loaded the training DEG-count CSV and used it as the scalar calibration
surface. The focal training endpoint is sparse:

- 1,674 total non-held-out perturbations.
- 1,205 targets had `n_degs = 0`.
- 363 had weak responses from 1 to 9 DEGs.
- 63 had medium responses from 10 to 89 DEGs.
- 43 had strong responses of at least 100 DEGs.

I then read only rows satisfying:

```python
group_name == "151 TH Prkcd Grin2c Glut"
```

from the DE parquet for a hand-chosen mechanistic comparator set. Every
queried target had 17,259 measured genes and matched-control size
`n_ctrl_matched = 23679`; the perturbed-cell sizes ranged from 113 for `Tlr4`
to 258 for `Cx3cr1`. For the central comparators, the focal-cell DE evidence
was:

| training target | observed `n_degs` | focal FDR<0.05 genes | strongest focal-row evidence |
|---|---:|---:|---|
| `Ccr2` | 0 | 0 | 313 nominal genes but min adjusted p = 1.0 |
| `Cx3cr1` | 0 | 0 | 294 nominal genes but min adjusted p = 1.0 |
| `Cxcr4` | 0 | 0 | `Pum1` was the top gene, score 4.62, log2FC 0.45, but q = 0.067 |
| `Rac1` | 0 | 0 | min adjusted p = 1.0 |
| `Tlr2` | 0 | 0 | min adjusted p = 1.0 |
| `Tlr4` | 0 | 0 | min adjusted p = 1.0 |
| `Il1r1` | 0 | 0 | `Kdm3b` nearly reached correction, q = 0.081 |
| `Il1rap` | 0 | 0 | min adjusted p = 1.0 |
| `Nfkb1` | 0 | 0 | min adjusted p = 1.0 |
| `Il6ra` | 0 | 0 | min adjusted p = 1.0 |
| `Il6st` | 0 | 0 | min adjusted p = 1.0 |
| `Stat1` | 1 | 1 | only `Stat1` itself passed, q = 0.027, log2FC -1.30 |

I also checked other same-pathway counts in the endpoint table. `Chuk`,
`Map3k7`, `Mapk1`, `Mapk9`, `Rel`, `Stat2`, `Stat3`, `Stat4`, `Stat5b`,
`Tlr3`, `Tlr5`, `Tlr7`, `Tlr8`, and `Tnfrsf1a` all had `n_degs = 0` in
`151 TH Prkcd Grin2c Glut`.

The focal profile comparison used full Wilcoxon-score vectors rather than only
significant genes. This matters because a target with zero FDR hits could still
share a broad subthreshold pattern. The chemokine and inflammatory comparator
profiles did not show such a pattern: the selected pairwise Pearson and cosine
similarities were essentially at zero. Examples include `Ccr2` vs `Cxcr4`
Pearson 0.0249, `Cx3cr1` vs `Cxcr4` Pearson 0.0051, `Cxcr4` vs `Nfkb1`
Pearson 0.0017, `Tlr2` vs `Nfkb1` Pearson 0.0277, and `Tlr4` vs `Stat1`
Pearson 0.0326. The full-universe nearest neighbors for `Ccr2` were also weak:
the top whole-profile Pearson neighbor was `Gabrd` at only 0.0667.

The same-experiment Distributed Agents corpus agreed with the raw focal inspection:

- `Ccr2`, `Cx3cr1`, and `Cxcr4` are connected by claim
  `claim:72c3acfe50f5f2be2163`, which states that represented chemokine
  receptors and a Rac-arm comparator did not produce a common postmitotic
  neuronal transcriptional program.
- `Ccr2:F001` reports a pan-measured neuronal null for `Ccr2`, and
  `Ccr2:F003` reports that `Cx3cr1` was flat and `Cxcr4` produced only
  isolated single-gene hits, with near-zero similarity to `Ccr2`.
- `Cxcr4:F001` through `Cxcr4:F004` describe `Cxcr4` as sparse, with one
  focal `Pum1` event and no recurrent CXCL12/CXCR4/ACKR3 or generic
  chemokine-GPCR/Rac program.
- `Tlr2:F001`, `Tlr4:F001`, and `Tlr4:F002` establish that TLR2/TLR4 loss did
  not expose a basal cytokine, chemokine, NF-kappaB, or interferon module in
  unstimulated postnatal NeuN-positive nuclei.
- The corpus search over cytokine receptor and STAT claims found that
  IL-6/gp130/JAK-STAT, IL-1/TIR/NF-kappaB/MAPK, TNFR/TLR, and broader
  interferon/STAT comparators were null, singleton-only, or nonconvergent in
  the same juvenile neuronal assay surface.

## Target-specific reasoning

### `Cxcr2`

CXCR2 is a G protein-coupled ELR+ CXC chemokine receptor. In human neutrophil
biology it responds strongly to CXCL8/IL-8; in rodents, which lack a direct
IL-8 ortholog, related ligands such as CXCL1/KC, CXCL2/MIP-2, and CXCL5/LIX
signal through CXCR2. The canonical downstream effect is not a stable
transcriptional differentiation state but acute G-protein and beta-arrestin
signaling through PI3K, PLC, Rac/Rho-family GTPases, MAPK, calcium, adhesion,
actin remodeling, granule exocytosis, and neutrophil chemotaxis
(Matsushima et al. 2022; Rajarathnam et al. 2018). CXCR2 and CXCR4 can oppose
one another in bone-marrow neutrophil retention versus release (Eash et al.
2010), but that is a hematopoietic trafficking circuit rather than a tonic
program in mature thalamic glutamatergic neurons.

The CNS literature makes CXCR2 plausible in brain disease but mostly in contexts
missing from this experiment. CXCR2/CXCR2-ligand networks can promote leukocyte
entry after CNS injury, and Cxcr2 deficiency attenuates neutrophil infiltration
and cortical damage after closed head injury (Semple, Kossmann &
Morganti-Kossmann 2009; Veenstra & Ransohoff 2012; Semple et al. 2010). Other
papers report neuronal or glial CXCR2 signaling after ligand addition, stress,
amyloid, peripheral inflammation, or ischemia: CXCL1 can activate ERK/PI3K and
tau phosphorylation in cultured cortical neurons (Xia & Hyman 2002), DRG
CXCL1/CXCR2 contributes to inflammatory pain (Cao et al. 2016), hippocampal
CXCL1/CXCR2 is implicated in chronic-stress depression-like behavior (Chai et
al. 2019), astrocytic CXCL1 can drive neuronal CXCR2-dependent synaptotoxicity
in amyloid models (Perez-Nievas et al. 2021), and astrocyte-derived CXCL5 can
signal through microglial CXCR2 during chronic cerebral ischemia (Cao et al.
2023). Those studies support context-gated CXCR2 biology, but they are
ligand-rich, injury/inflammation, glial, immune, peripheral sensory, or chronic
stress systems. The supplied screen instead sampled sparse P16 AAV CRISPR
loss-of-function in mostly NeuN-positive, postmitotic, unchallenged juvenile
brain nuclei.

The most appropriate within-dataset analogs therefore argue for zero rather
than a weak positive count:

- The closest represented chemokine GPCRs were silent in the focal cell class:
  `Ccr2 = 0`, `Cx3cr1 = 0`, and `Cxcr4 = 0` DEGs. `Cxcr4` is the best receptor
  counterexample because it has strong developmental CNS biology, but after P16
  perturbation it only produced a nonsignificant focal `Pum1` trend
  (`q = 0.067`) and no CXCR4/CXCL12 migration module.
- `Rac1`, an indirect branch downstream of chemokine-GPCR migration signaling,
  also had 0 DEGs in the focal cell class.
- The receptor-to-transcription arms that would be expected if CXCR2 loss were
  perturbing basal inflammatory signaling were flat: `Tlr2`, `Tlr4`,
  `Il1r1`, `Il1rap`, `Nfkb1`, `Chuk`, `Map3k7`, `Mapk1`, `Mapk9`, `Rel`,
  `Il6ra`, and `Il6st` all had focal `n_degs = 0`; `Stat1` had only a
  self-depletion hit, and `Stat2`, `Stat3`, `Stat4`, and `Stat5b` had 0.
- The Distributed Agents candidate topology connected these comparators as chemokine and
  innate/cytokine modules, but the corresponding claim statements describe
  shared absence of tonic neuronal cytokine, chemokine, NF-kappaB, interferon,
  and JAK-STAT programs, not a nonzero module that `Cxcr2` should inherit.

Given that the endpoint is BH-adjusted single-nucleus DE breadth, an acute loss
of `Cxcr2` in this focal glutamatergic thalamic population is very likely to sit
in the same assay-null class as `Ccr2`, `Cx3cr1`, `Tlr2`, `Tlr4`, and
`Il6ra`. I therefore predict no FDR 0.05 DEGs:

```text
Cxcr2 -> 0
```

## Limits

- `Cxcr2` itself was completely held out, so no direct signature, no direct DEG
  count, and no direct same-experiment Distributed Agents `Cxcr2` target card were
  available.
- The closest represented chemokine receptor, `Cxcr4`, is not a paralog and
  signals through a different homeostatic ligand system; `Ccr2` and `Cx3cr1`
  are family-level rather than ligand-level comparators.
- Direct CXCR2 ligands (`Cxcl1`, `Cxcl2`, `Cxcl5`), the atypical chemokine
  context, and several immediate GPCR effectors were absent as perturbation
  targets, so the pathway comparison is partial.
- Published neuronal CXCR2 functions usually come from ligand addition, disease
  challenge, chronic stress, peripheral ganglia, glia-neuron coculture, or
  infiltrating leukocytes. Extrapolating those settings to unchallenged
  juvenile NeuN-positive thalamic neurons would likely overpredict the snRNA-seq
  DEG count.
- A zero-DEG prediction is not a claim that editing would fail or that CXCR2 is
  biologically irrelevant; it is a prediction that no measured transcript will
  pass BH FDR 0.05 in this assay and cell group.
