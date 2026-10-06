# Acat1 n_degs forecast

Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with
BH-adjusted Wilcoxon `p < 0.05`.

## Target biology used

- Target: `Acat1`.
- Declared exact focal-population expression:
  - `mean_raw_umi = 3.361248363528865`
  - `mean_cp10k = 2.102047515541802`
  - `pseudobulk_cpm = 210.66135434407303`
  - `21744 / 23679` non-target nuclei expressing `Acat1`
    (`91.82820220448498%`)
- The biology bundle identifies ACAT1 as mitochondrial acetyl-CoA
  acetyltransferase in ketone-body and isoleucine metabolism.
- Functional-stock adjudication predicts that a disruptive P16 edit should
  substantially deplete operative ACAT1 protein by the P37-P44 harvest because
  the enzyme is a renewing mitochondrial catalytic stock. The support is only
  partial: the direct half-life datum is rat hepatocyte protein turnover and
  the loss phenotype prior is human systemic beta-ketothiolase deficiency, not
  a matched postnatal mouse thalamic-neuron experiment.

Interpretation: the perturbation is likely reachable in this cell class, so I
did not treat `Acat1` as absent or protected by durable pre-edit stock. The
biology points to mitochondrial carbon metabolism rather than an established
acute transcriptional regulator or spliceosome/proteostasis perturbation.

## Training measurements used

The declared training count table for the same focal class contains 1,674
non-held-out perturbations. It is highly zero-inflated:

| statistic | value |
| --- | ---: |
| minimum | 0 |
| median | 0 |
| mean | 14.053763440860216 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2677 |
| zero-count perturbations | 1205 / 1674 |

Large count values come from a long tail of genes such as `Uba5`, `Tpr`,
`Sin3a`, `Rnpc3`, proteasome, spliceosome, and chromatin regulators. I did not
transfer that tail to ACAT1 because the target biology gives no evidence for
the same recovered-neuron transcriptional state.

I then inspected training perturbations in the same thalamic class that are
closer to ACAT1's mitochondrial carbon-metabolism role and present in the
training table:

| analog | n_pert_matched | n_degs | minimum BH-adjusted p |
| --- | ---: | ---: | ---: |
| `Aco2` | 154 | 0 | 0.3300322 |
| `Bckdhb` | 111 | 0 | 1 |
| `Dlat` | 170 | 1 | 2.813889e-07 |
| `Dld` | 116 | 0 | 1 |
| `Idh3a` | 119 | 1 | 9.273100e-11 |
| `Ivd` | 244 | 0 | 0.2754293 |
| `Mdh2` | 206 | 1 | 7.368120e-05 |
| `Mpc1` | 199 | 0 | 1 |
| `Ogdh` | 161 | 0 | 0.563859 |
| `Pcca` | 138 | 0 | 1 |
| `Sucla2` | 151 | 1 | 5.119472e-05 |
| `Suclg1` | 170 | 0 | 1 |

For the singleton metabolic perturbations above, the significant feature was
the targeted transcript itself (`Dlat`, `Idh3a`, `Mdh2`, and `Sucla2`) rather
than a recurring downstream stress program. A separate exact profile comparison
over `Aco2`, `Bckdhb`, `Cox5a`, `Cpt1c`, `Dlat`, `Dld`, `Idh3a`, `Ivd`,
`Mdh2`, `Ndufs4`, `Ogdh`, and `Sdha` in this same cell class likewise found 6
of 12 analogs with no significant features and 6 of 12 in the `1_to_9` bin.
The direct profile rows showed that the `Cox5a`, `Cpt1c`, `Dlat`, `Idh3a`,
`Mdh2`, and `Sdha` singleton cases were all self-transcript hits.

## Synthesis

The prior from all measured focal-class perturbations is a point mass at zero,
and the carbon-metabolism analogs argue strongly against tens or hundreds of
DEGs. ACAT1 is better expressed in the focal population than many generic
metabolic enzymes and its stock should have turned over by harvest, so I allow
one significant measured gene as the most likely visible footprint. The point
forecast is therefore exactly one DEG, reflecting a probable singleton or
near-singleton response with no broad downstream program.
