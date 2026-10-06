# Prediction trace

## Question

The held-out manifest for this run contains one perturbation:

| target_name |
|---|
| Ptpa |

I interpreted the requested endpoint as the exact focal-cell endpoint used in the
training CSV: for a target gene, predict how many measured genes in `151 TH
Prkcd Grin2c Glut` cells would have `pvals_adj < 0.05` in the Scanpy/Wilcoxon
DE table. A prediction of 0 means that I expect no downstream gene to pass that
FDR threshold. I did not reinterpret this as effect size, editing efficiency,
viability, or target knockdown.

One ambiguity was that the same-experiment Distributed Agents corpus often summarizes
findings at FDR < 0.10 across many cell groups, whereas the requested endpoint
is FDR < 0.05 in this one cell group. I used the corpus for mechanistic
neighborhood evidence, then returned to the focal `pvals_adj < 0.05` count in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` whenever assigning a count.

## Sources

- Input manifest:
  `[local file: 191_Ptpa.csv]`.
- Focal training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- All-cell DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`.
- PubMed literature searches for PTPA/PPP2R4, PP2A activation, and UBE3A-PTPA
  neuronal biology.

External citations used for mechanism:

- Chao et al. 2006, `Molecular Cell`, DOI `10.1016/j.molcel.2006.07.027`:
  human PTPA is a conserved PP2A activator; binding of PTPA to the PP2A A-C
  core alters catalytic specificity and forms an ATPase-like PP2A/PTPA complex.
- Longin et al. 2004, `Biochemical Journal`, DOI `10.1042/BJ20031643`:
  PTPA can reactivate an inactive PP2A population associated with the PP2A
  methylesterase PME-1.
- Guo et al. 2013, `Cell Research`, DOI `10.1038/cr.2013.138`: PTPA acts as an
  ATP-dependent PP2A activation chaperone, stabilizing the catalytic subunit in
  a state that acquires the proper catalytic metals.
- Jordens et al. 2005, `Journal of Biological Chemistry`, DOI
  `10.1074/jbc.M507760200`: PTPA/Ypa proteins have PP2A reactivation activity
  linked to a peptidyl-prolyl isomerase activity near the PP2A active site.
- Wang et al. 2019, `PNAS`, DOI `10.1073/pnas.1820131116`: UBE3A ubiquitinates
  PTPA; maternal `Ube3a` loss in mouse increases PTPA, promotes PP2A holoenzyme
  assembly and PP2A activity, and PTPA reduction can rescue dendritic-spine
  phenotypes.
- Fevga et al. 2023, `Brain`, DOI `10.1093/brain/awac326`: biallelic human
  PTPA/PPP2R4 variants impair PP2A activation and cause early-onset
  parkinsonism with intellectual disability.

## Computation over the supplied data

The focal training count table has 1,674 non-held-out perturbations:

- 1,205/1,674 have `n_degs = 0`.
- 469/1,674 have at least one focal DEG.
- Median `n_degs` is 0; 75th percentile is 1; 90th percentile is 2; 95th
  percentile is 18.

I first looked up every available perturbation with obvious PP2A, PP4,
phosphatase, `Set`, and AKT/mTOR adjacency. Most exact PP2A core genes were not
available as training endpoints in this focal count table: `Ppp2ca`, `Ppp2cb`,
`Ppp2r1a`, `Ppp2r1b`, `Ppp2r5a`, `Ppp2r5b`, `Ppp2r5c`, `Ppp4c`, `Ppp4r1`,
`Ppp4r2`, `Ppp4r3a`, `Ppp4r3b`, `Ppp6c`, and `Igbp1` were absent. The closest
available same-assay targets and their `151 TH Prkcd Grin2c Glut` counts were:

| training target | focal `n_degs` | relevance to `Ptpa` |
|---|---:|---|
| `Ppp2r2b` | 0 | PP2A/B55-family neuronal regulatory subunit |
| `Ppp2r5d` | 0 | PP2A/B56-family neuronal regulatory subunit |
| `Set` | 0 | endogenous PP2A inhibitor |
| `Ppm1g` | 3 | serine/threonine phosphatase with B56delta literature adjacency |
| `Ywhaz` | 1 | abundant neuronal 14-3-3 adapter that is linked to phospho-signaling |
| `Ube3a` | 0 | upstream E3 ligase that targets PTPA for degradation |
| `Gabrb3` | 0 | Angelman/Dup15q comparator |
| `Fmr1` | 0 | synaptic/translation NDD comparator |
| `Akt3` | 0 | AKT/mTOR pathway comparator |
| `Pik3cb` | 0 | PI3K/mTOR pathway comparator |
| `Pik3r1` | 0 | PI3K/mTOR pathway comparator |
| `Pik3r2` | 0 | PI3K/mTOR pathway comparator |
| `Rptor` | 0 | mTORC1 component |
| `Mtor` | 2 | core mTOR kinase |
| `App` | 1 | PP2A/tau/amyloid-adjacent comparator |
| `Mapt` | 1 | tau comparator |
| `Gsk3b` | 6 | tau/Wnt kinase comparator |
| `Tsc2` | 86 | strong mTORC1-counterexample target |

For the closest focal analogs, I filtered the parquet to `group_name == "151 TH
Prkcd Grin2c Glut"` and examined the per-gene rows for `Ppp2r2b`, `Ppp2r5d`,
`Set`, `Ppm1g`, `Ube3a`, `Ywhaz`, `Mtor`, and `Tsc2`. The direct PP2A-related
targets were not near the FDR threshold:

| target | matched perturbed nuclei | focal DEGs at FDR 0.05 | smallest focal `pvals_adj` |
|---|---:|---:|---:|
| `Ppp2r2b` | 151 | 0 | 0.3617 |
| `Ppp2r5d` | 141 | 0 | 0.4050 |
| `Set` | 163 | 0 | 0.6570 |
| `Ppm1g` | 182 | 3 | 0.00539 |
| `Ywhaz` | 129 | 1 | 0.000097 |
| `Mtor` | 188 | 2 | 0.0185 |
| `Tsc2` | 177 | 86 | 0.0000033 |

`Ppm1g` was the only phosphatase-adjacent perturbation in this subset with more
than one focal DEG, and those three genes were `Col4a2` down, `Col4a1` down,
and `H2ac25` up. This matched the Distributed Agents corpus finding that `Ppm1g` has a
small 151-TH-restricted collagen/H2A response rather than a broad PP2A-like
signature. A profile comparison of `Ppp2r2b`, `Ppp2r5d`, `Set`, `Ppm1g`,
`Ywhaz`, `Mtor`, and `Tsc2` also found no overlap among significant positive or
negative focal programs. I did not use the high whole-vector cosine values from
that comparison as biological evidence, because for these mostly null
signatures those values were dominated by extreme logFC rows with adjusted
`p = 1` for genes essentially absent from the focal population.

## Ptpa-specific reasoning

`Ptpa` encodes the phosphotyrosyl phosphatase activator PTPA, the PP2A
activation chaperone also called PPP2R4 in the human literature. In biochemical
systems PTPA directly binds the PP2A A-C core dimer and helps convert inactive
PP2A catalytic subunit into a metal-loaded active state; loss of PTPA can lower
PP2A activity and complex levels. That makes `Ptpa` more central than loss of a
single B-subunit gene, so I treated the zero counts for `Ppp2r2b` and
`Ppp2r5d` as strong but imperfect analogs rather than as exact phenocopies.

The same-experiment evidence nevertheless points to a buffered acute RNA
response:

- `Ppp2r2b` had 0 DEGs in the focal group, its best focal adjusted p-value was
  only 0.3617, and the Distributed Agents corpus records a high-confidence finding that
  `Ppp2r2b` produced no FDR<0.10 downstream transcriptional response in any of
  22 measured neuronal groups.
- `Ppp2r5d` had 0 focal DEGs, its best focal adjusted p-value was 0.4050, and
  the Distributed Agents corpus records only three FDR<0.10 genes total across other
  superficial intratelencephalic groups, not a thalamic response. The corpus
  also reports that `Ppp2r5d` did not phenocopy `Ppp2r2b`, represented mTOR
  genes, or tau-pathway relatives.
- `Set` loss should shift PP2A in the opposite biochemical direction from PTPA
  loss by relieving endogenous PP2A inhibition, yet `Set` was flat in the focal
  group and the same-experiment corpus reports that `Set`, `Ppp2r2b`, and
  `Ppp2r5d` do not collapse into a shared acute PP2A transcriptomic axis.
- `Ube3a` is a neuronal upstream regulator of PTPA protein abundance. Wang et
  al. 2019 showed that UBE3A loss increases PTPA and PP2A activity in mouse
  Angelman-model brain, but the training endpoint had `Ube3a = 0`, and the
  Distributed Agents corpus records 0 downstream FDR<0.10 genes for `Ube3a` across 18
  recovered neuronal groups.
- The AKT/mTOR/tau side of PP2A biology was not uniformly silent, so the screen
  could recover a response when one was present: `Tsc2` had 86 focal DEGs and
  `Gsk3b` had 6. However, direct `Mtor` loss had only 2 focal DEGs, and `Akt3`,
  `Rptor`, `Pik3cb`, `Pik3r1`, and `Pik3r2` were all 0. I therefore treated
  `Tsc2` as a counterexample showing assay sensitivity to some mTORC1 states,
  not as a template for `Ptpa`.

The best biological argument for a nonzero prediction is that PTPA sits upstream
of many PP2A holoenzymes and human PTPA variants can cause neurodevelopmental
and parkinsonian disease by impairing PP2A activation. The best assay-local
argument for zero is that the available perturbations around PP2A and its
neuronal regulator `Ube3a` were flat or extremely sparse in the same acute,
postnatal, mosaic snRNA-seq screen. The focal B-subunit perturbations were also
not borderline misses; neither had an adjusted p-value below 0.36. Given the
overall zero-heavy calibration of the endpoint, I expect partial post-P16
`Ptpa` loss to alter phosphorylation biochemistry more readily than it produces
a thalamic nuclear RNA program large enough to survive BH correction.

## Limits and extrapolation

- `Ptpa` itself was completely held out, and there was no same-assay `Ppp2ca`,
  `Ppp2cb`, `Ppp2r1a`, `Ppp2r1b`, `Ppme1`, `Lcmt1`, `Ppp4c`, or `Ppp4r*`
  perturbation available in the focal training count table. The prediction is
  therefore extrapolated from regulatory-subunit and pathway-neighbor targets,
  not from the exact PP2A catalytic activation machinery.
- PTPA is upstream of many PP2A holoenzymes, so it could be less buffered than
  `Ppp2r2b` or `Ppp2r5d`. The opposite risk is also real: this screen gives only
  a sparse acute LoF and did not measure indels, PTPA protein, PP2A catalytic
  metals, PP2A methylation, or substrate phosphosites.
- The focal cell group is thalamic and the perturbation is acute at P16.
  Chronic germline or biallelic PTPA/PPP2R4 disease mechanisms, cancer-cell PP2A
  tumor-suppressor mechanisms, Drosophila neuroblast polarity mechanisms, and
  biochemical PP2A activation can be important without forcing a 3-4 week
  juvenile neuron mRNA response.
- Many mostly-null DE vectors contain extreme logFC values for genes with
  `pvals_adj = 1`. I ignored those as expression-pattern analogs and weighted
  the FDR counts, smallest adjusted p-values, and curated same-experiment
  negative findings more heavily.

## Prediction

| target_name | predicted_n_degs |
|---|---:|
| Ptpa | 0 |
