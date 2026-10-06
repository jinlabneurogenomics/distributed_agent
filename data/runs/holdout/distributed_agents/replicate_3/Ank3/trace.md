# Question and resolved ambiguity

The manifest for this run contains one requested held-out target:

- `Ank3`

I interpreted the endpoint exactly as the supplied scalar training file defines it:
`n_degs` is the count of measured genes in `151 TH Prkcd Grin2c Glut` with
`pvals_adj < 0.05`. This includes the perturbed target transcript itself when
that row is significant. I therefore separated likely target-transcript-only
calls from broader downstream programs.

The requested `Ank3` perturbation is absent from both training inputs. The
prediction below transfers from training perturbations of Ankyrin/AIS membrane
scaffold genes, AIS/node adhesion molecules, and voltage-gated channel partners;
it does not use `Ank3` DE rows or an `Ank3` training count.

# Sources used

- Input focal count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 010_Ank3.csv]`
- Distributed Agents same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents runtime profile tools for matched-context profile comparisons over
  `151 TH Prkcd Grin2c Glut`.
- PubMed literature for ANK3/ankyrin-G and AIS biology.

External biological references used:

- Jenkins and Bennett, 2001, Journal of Cell Biology, DOI
  `10.1083/jcb.200109026`, PMID `11724816`: ankyrin-G coordinates assembly of
  beta IV spectrin, Nav1.6, neurofascin, and NrCAM at Purkinje-neuron AISs.
- Jenkins et al., 2014, PNAS, DOI `10.1073/pnas.1416544112`, PMID `25552556`:
  giant ankyrin-G is required for AIS and node assembly in mice.
- Gasser et al., 2012, Journal of Neuroscience, DOI
  `10.1523/JNEUROSCI.5434-11.2012`: an ankyrin-G-binding motif is sufficient
  for Nav1.6 AIS/node targeting.
- Leterrier et al., 2017, Frontiers in Cellular Neuroscience, DOI
  `10.3389/fncel.2017.00006`, PMID `28184187`: Nav and neurofascin-186 membrane
  partners help establish and maintain ankyrin-G at the AIS.
- Stevens and Rasband, 2022, Channels, DOI
  `10.1080/19336950.2022.2120467`: review of ankyrin-family scaffolding of ion
  channels and transporters.
- Zhu et al., 2017, PNAS, DOI `10.1073/pnas.1700689114`, PMID `28894008`:
  adult forebrain Ank3 disruption removes AIS voltage-gated channels and alters
  excitability and behavior.
- Ferreira et al., 2008, Nature Genetics, DOI `10.1038/ng.209`, PMID
  `18711365`: human GWAS support for ANK3 and CACNA1C in bipolar disorder.

# Computation over the input data

The training count table was read directly to get the endpoint for candidate
analogs in the focal cell type. I then read the parquet only in the focal
context for a hand-curated Ankyrin/AIS/channel comparator panel. The essential
operation was:

```sql
select gene_target, names, logfoldchanges, pvals_adj,
       n_pert_matched, n_ctrl_matched
from read_parquet(:training_de_all_cell_groups)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
```

I also compared the full signed log-fold-change profiles of the closest
Ankyrin/AIS membrane-skeleton nodes with the Distributed Agents runtime
`profile_compare` tool in the exact same `group_name`. The important profile
summary was the activity status, not the raw cosine between nearly flat vectors:
`Ank1`, `Ank2`, `Sptb`, `Add1`, `Add2`, and `Add3` had no FDR<0.05 genes;
`Sptan1`, `Scn1a`, `Scn2a`, `Scn8a`, `Kcnq2`, `Kcnq3`, `Cntnap1`, and
`Kcnab2` each had exactly one significant gene, their own transcript; `Nrcam`
and `Scn1b` had only two significant genes.

# Target-specific evidence and rationale

## Ank3

`Ank3` encodes ankyrin-G, the central AIS scaffold that clusters voltage-gated
Na+ channels, KCNQ/Kv7 channels, L1-family CAMs including neurofascin/NrCAM,
and the spectrin-actin membrane skeleton. The external biology therefore makes
`Ank3` more central than a generic ankyrin-family member: loss of ankyrin-G can
disassemble the AIS and mislocalize channels and adhesion molecules, and adult
forebrain deletion can perturb excitability. Those data argue against treating
`Ank3` as a developmentally irrelevant gene.

The training data in this exact snRNA endpoint, however, point strongly toward
a zero-to-self-only nuclear RNA footprint for AIS structural perturbations:

| training perturbation | focal `n_degs` | expression evidence in `151 TH Prkcd Grin2c Glut` |
| --- | ---: | --- |
| `Ank1` | 0 | no FDR<0.05 gene; its own row had logFC `+0.209`, FDR `1.0` |
| `Ank2` | 0 | no FDR<0.05 gene; its own row had logFC `-0.127`, FDR `1.0` |
| `Sptan1` | 1 | self-transcript-only, `Sptan1` logFC `-0.529`, FDR `2.03e-13` |
| `Sptb` | 0 | no FDR<0.05 gene; `Sptb` logFC `-0.201`, FDR `1.0` |
| `Add1` | 0 | no FDR<0.05 gene; `Add1` logFC `-0.486`, FDR `0.575` |
| `Add2` | 0 | no FDR<0.05 gene; `Add2` logFC `-0.287`, FDR `1.0` |
| `Add3` | 0 | no FDR<0.05 gene; `Add3` logFC `-0.012`, FDR `1.0` |
| `Nrcam` | 2 | `Nrcam` self logFC `-0.650`, FDR `2.94e-15`; one downstream gene, `Letm2`, just passed FDR with logFC `+0.459`, FDR `0.0490` |
| `Cntnap1` | 1 | self-transcript-only, `Cntnap1` logFC `-0.822`, FDR `1.09e-11` |
| `Cntnap2` | 1 | self-transcript-only, `Cntnap2` logFC `-1.087`, FDR `7.90e-06` |
| `Scn1a` | 1 | self-transcript-only, `Scn1a` logFC `-1.075`, FDR `5.87e-38` |
| `Scn2a` | 1 | self-transcript-only, `Scn2a` logFC `-0.401`, FDR `6.46e-06` |
| `Scn3a` | 0 | no focal FDR<0.05 gene |
| `Scn8a` | 1 | self-transcript-only, `Scn8a` logFC `-0.458`, FDR `1.34e-05` |
| `Scn1b` | 2 | `Scn1b` self logFC `-1.436`, FDR `7.36e-70`; only one downstream hit, `Jun`, FDR `0.0156` |
| `Kcnq1` | 0 | no focal FDR<0.05 gene |
| `Kcnq2` | 1 | self-transcript-only, `Kcnq2` logFC `-0.776`, FDR `2.12e-28` |
| `Kcnq3` | 1 | self-transcript-only, `Kcnq3` logFC `-0.379`, FDR `0.00717` |

The Distributed Agents corpus agreed with that boundary. The Ank2 report states that
represented ankyrin/spectrin/adducin/L1CAM structural comparators were flat or
minimally active and that sodium-channel and KCNQ perturbations had strong
target engagement in several cases but little downstream RNA output. The Scn8a
report called `151 TH Prkcd Grin2c Glut` a weak-self-only response: 90
perturbed nuclei versus 23679 controls, `Scn8a` logFC `-0.458`, FDR
`1.34e-05`, and no downstream gene at FDR<0.10. The Nrcam report found that
L1CAM, Sema3F, ankyrin, and node/paranode comparators did not phenocopy `Nrcam`
and that expected Sema3F/NrCAM, L1CAM, ankyrin, and postsynaptic scaffold genes
were not transcriptionally recruited after `Nrcam` loss.

I treated `Cacna1g` and `Grin1` as counterexamples, not as primary analogs.
`Cacna1g` had 12 focal DEGs, `Grin1` had 89, and `Atp1a3` had 80, proving that
the focal thalamic group could report ion-channel or excitability-associated
transcriptional states when the perturbed node fed back to the nucleus. The
same result also limits a simple "ion channel or excitability gene implies many
DEGs" rule: Nav alpha/beta subunits, Kv7 channels, and membrane-skeleton nodes
were one-gene or zero-gene perturbations under the same test.

The final call is therefore nonzero but minimal. `Ank3` is central enough, and
likely expressed enough in neurons, that a self-transcript FDR call is more
plausible than a hard zero; the closest downstream biology in training gives no
reason to expect a multi-gene AIS compensatory program. I predict one DEG,
interpreting it as most likely the `Ank3` self row rather than a secondary
program.

# Limits and extrapolation

- `Ank3` was completely held out, and `Sptbn4`, `Nfasc`, and `L1cam`, the
  strictest beta IV spectrin / neurofascin / L1-CAM partners of ankyrin-G, were
  not all available as focal training endpoints. The prediction extrapolates
  from partial AIS neighbors.
- Ankyrin-G is more central to the AIS than Ank1/Ank2, adducins, individual
  Nav channels, or individual Kv7 channels. A sparse RNA readout after P16
  deletion could miss channel clustering and action-potential phenotypes, but
  this also means the training analogs may understate structural severity while
  still correctly forecasting a small nuclear mRNA footprint.
- Full-vector similarities among extremely weak perturbations can be dominated
  by low-expression/pseudocount tails. I therefore used the profile comparison
  mainly to verify that significant downstream feature sets did not recur.
- The integer `1` is driven mostly by expectation of a detectable `Ank3`
  self-transcript row. If the guides generate functional indels without
  nonsense-mediated decay in the measured nuclear transcript, the hidden answer
  could be `0`; if AnkG loss secondarily crosses an activity threshold in these
  thalamic neurons, the hidden answer could be a few genes rather than one.
