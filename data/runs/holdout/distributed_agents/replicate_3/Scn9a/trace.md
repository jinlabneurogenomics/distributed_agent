# Scn9a prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The task is to predict, for each gene in the held-out manifest, the integer `n_degs`: the number of measured genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after acute sparse CRISPR loss of function in `151 TH Prkcd Grin2c Glut` nuclei.

This run has one requested target:

```tsv
target_name
Scn9a
```

`Scn9a` was absent as a `gene_target` in the supplied differential-expression parquet and absent from the training-count CSV, so its own `151` DEG count and signature cannot be read directly. I treated the endpoint as the exact FDR count used in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, including target-self transcript depletion when that transcript itself passed FDR.

## Sources used

- Supplied training count table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied training DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 202_Scn9a.csv]`.
- Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`, especially the Scn1a, Scn1b, Scn2a, Scn3a, and Scn8a target contexts and their curated claim that represented Nav alpha/beta and intracellular FHF perturbations give sparse, target-specific neuronal RNA responses rather than a pan-Nav transcriptional module.
- PubMed literature on Nav1.7/SCN9A biology:
  - Cox et al. 2006, Nature, DOI `10.1038/nature05413`, PMID `17167479`.
  - Weiss et al. 2011, Nature, DOI `10.1038/nature09975`, PMID `21441906`.
  - Ahn et al. 2011, Molecular Pain, DOI `10.1186/1744-8069-7-32`, PMID `21569247`.
  - MacDonald et al. 2021, Neuron, DOI `10.1016/j.neuron.2021.03.012`, PMID `33823138`.
  - Koenig et al. 2015, PLoS One, DOI `10.1371/journal.pone.0128830`, PMID `26035178`.

## Dataset checks

I first read the held-out manifest and confirmed that the only target is `Scn9a`.

The focal training CSV contained 1,674 non-held-out targets. The distribution was highly zero-inflated: median 0 DEGs, mean 14.1 DEGs, 469/1,674 nonzero targets, and a maximum of 2,677 DEGs. Thus most perturbations in this cell group are silent, while a small number of RNA-processing or essential-cell-state genes give broad responses.

I then filtered the parquet to the focal cell group and the direct sodium-channel comparators. The exact FDR counts and significant rows were:

| training perturbation | observed `n_degs` in `151` | FDR < 0.05 rows in `151` |
| --- | ---: | --- |
| `Scn1a` | 1 | `Scn1a` down, log2FC -1.075, adjusted p `5.87e-38` |
| `Scn2a` | 1 | `Scn2a` down, log2FC -0.401, adjusted p `6.46e-06` |
| `Scn3a` | 0 | none |
| `Scn8a` | 1 | `Scn8a` down, log2FC -0.458, adjusted p `1.34e-05` |
| `Scn1b` | 2 | `Scn1b` down and `Jun` up |
| `Fgf12` | 0 | none |
| `Fgf13` | 2 | `Fgf13` down and `Rell2` down |
| `Kcnq2` | 1 | `Kcnq2` down |
| `Kcnq3` | 1 | `Kcnq3` down |
| `Snta1` | 0 | none |
| `Ank2` | 0 | none |
| `Fgf1` | 0 | none |
| `Fgfr1` | 0 | none |
| `Cacna1g` | 12 | `Cacna1g` itself plus 11 downstream genes |

I also ran Distributed Agents runtime `profile_compare` on `Scn1a`, `Scn1b`, `Scn2a`, `Scn3a`, `Scn8a`, `Fgf12`, `Fgf13`, `Cacna1g`, and `Kcnq2` using the exact `group_name == "151 TH Prkcd Grin2c Glut"` context, `logfoldchanges` as the signed values, `names` as features, and `pvals_adj < 0.05` as the significance rule. This confirmed that the directly relevant Scn profiles have 0 to 2 significant features in `151`, with no shared significant downstream genes among the measured Nav alpha subunits. The significant genes were target-self for `Scn1a`, `Scn2a`, and `Scn8a`; none for `Scn3a`; and target-self plus isolated `Jun` for `Scn1b`. The `Cacna1g` result is the important positive control: `151` can produce a real channel-perturbation response in the same data, but sodium-channel alpha subunit loss generally did not.

As a local check on a hidden Scn compensation program, I also inspected measured sodium-channel transcripts under the `151` Scn perturbations. `Scn9a` was present as a measured row but never significant under `Scn1a`, `Scn1b`, `Scn2a`, `Scn3a`, `Scn8a`, or `Cacna1g`; all of those rows had adjusted p = 1.0.

## Distributed Agents corpus evidence

The Distributed Agents corpus did not contain a held-out `Scn9a` target context, so no internal same-experiment finding was available for `Scn9a` itself.

The represented sodium-channel relatives were well curated:

- `Scn1a`: corpus findings described a sharply buffered postnatal mosaic LoF transcriptome, with detectable Scn1a self-depletion in several groups but only three non-target FDR<0.10 genes genome-wide; its sodium-channel comparators `Scn1b`, `Scn2a`, `Scn3a`, `Scn8a`, and `Fgf13` did not phenocopy it.
- `Scn2a`: corpus findings likewise described only three downstream FDR<0.10 genes genome-wide and explicitly noted that in `151 TH Prkcd Grin2c Glut`, `Scn2a` knocked down its own RNA without downstream FDR<0.10 genes, whereas `Cacna1g` produced a modest downstream response.
- `Scn3a`: the corpus reported only a single robust downstream mark in a different cortical L2/3 IT class and no channel-family compensation or activity-regulated program after postnatal Scn3a CRISPR loss.
- `Scn8a`: the corpus reported Scn8a self-transcript knockdown in a few neuronal classes but no FDR<0.10 downstream genes anywhere, including no persistent immediate-early or channel-homeostatic program.
- `Scn1b`: despite beta1 coupling to Nav alpha subunits, Scn1b loss gave only four downstream genes genome-wide and did not move sodium-channel, AIS/nodal, FHF, Kv4, or KCNQ machinery transcripts in the assayed neuronal groups.

The bottom-up corpus claim tying these findings together was high confidence: represented Nav-channel subunits and intracellular FHF modulators produce sparse, target- and cell-context-specific neuronal RNA responses, not a shared pan-Nav or Nav-complex transcriptional module. That claim is important because it argues against predicting a broad `Scn9a` DEG count merely because Nav1.7 is a voltage-gated sodium channel.

## External biological rationale for Scn9a

`Scn9a` encodes the Nav1.7 voltage-gated sodium-channel alpha subunit. Its best-established biology is peripheral sensory and olfactory:

- Human SCN9A loss-of-function causes congenital inability to experience pain, and Cox et al. showed that Nav1.7 is strongly expressed in nociceptive neurons and that the patient nonsense alleles abolish Nav1.7 current (Cox et al. 2006, DOI `10.1038/nature05413`, PMID `17167479`).
- Loss of Nav1.7 also causes anosmia; deleting Nav1.7 from mouse olfactory sensory neurons prevents synaptic signaling at the first olfactory synapse even though odor-evoked action potentials remain (Weiss et al. 2011, DOI `10.1038/nature09975`, PMID `21441906`).
- Ahn et al. found Nav1.7 to be the predominant sodium-channel transcript in rat and mouse olfactory sensory neurons, while summarizing its preferential expression in DRG and sympathetic neurons of the peripheral nervous system (Ahn et al. 2011, DOI `10.1186/1744-8069-7-32`, PMID `21569247`).
- MacDonald et al. further placed the analgesic mechanism of Nav1.7 nulls at reduced nociceptor central-terminal transmission rather than a broad cell-autonomous CNS transcriptional state (MacDonald et al. 2021, DOI `10.1016/j.neuron.2021.03.012`, PMID `33823138`).
- Koenig et al. studied a conserved Scn9a natural antisense transcript in dorsal root ganglia, again reinforcing DRG enrichment of the Scn9a regulatory circuit (Koenig et al. 2015, DOI `10.1371/journal.pone.0128830`, PMID `26035178`).

Those tissues are poorly aligned to the experiment. The Perturb-seq data are NeuN-enriched postnatal brain nuclei, with olfactory bulb and hindbrain removed; dorsal root, trigeminal, sympathetic, and olfactory sensory neurons are not the focal population. `151 TH Prkcd Grin2c Glut` is a thalamic glutamatergic group, not a peripheral nociceptor or olfactory-sensory class.

## Target-specific prediction

### `Scn9a`

Biologically relevant training perturbations:

- The closest alpha-subunit paralogs in the training set are `Scn1a`, `Scn2a`, `Scn3a`, and `Scn8a`.
  - `Scn1a`, `Scn2a`, and `Scn8a` each had exactly one DEG in `151`, and that one DEG was the target transcript itself.
  - `Scn3a` had zero DEGs in `151`.
  - The Distributed Agents corpus reports that these Nav alpha perturbations did not phenocopy one another and did not launch a common Nav-family nuclear RNA program.
- `Scn1b` is a beta-subunit partner rather than an alpha paralog. It had two DEGs in `151`: target self and a single `Jun` induction. Its corpus context specifically warns that beta1's biochemical coupling to Nav alpha channels did not become a shared sodium-channel mRNA module.
- `Fgf12` and `Fgf13` are intracellular fibroblast growth factor homologous factors that modulate Nav channels. `Fgf12` was zero in `151`; `Fgf13` had two DEGs, target self and `Rell2`. They are mechanistic boundary cases, not evidence for broad Nav-state remodeling.
- `Kcnq2`, `Kcnq3`, `Ank2`, and `Snta1` probe axon-initial-segment or membrane-excitability-adjacent biology. Their `151` counts were 0 or 1, again mainly target self.
- `Cacna1g` is the counterexample: it had 12 DEGs in `151`, including its own transcript and downstream genes. This keeps the prediction from collapsing to "ion channels cannot be detected" and instead points to a sodium-channel/Scn9a-specific expectation of little or no nuclear response.

The zero/nonzero decision turns on whether `Scn9a` should at least knock down its own transcript in `151`. For the central Nav genes that are expressed in this group, target-self depletion alone creates an observed count of 1 even without downstream DE. Scn9a is different: Nav1.7 biology is concentrated in nociceptors, peripheral autonomic neurons, and olfactory sensory neurons, all outside or depleted from this assay's NeuN+ brain-minus-olfactory-bulb sampling. I therefore do not expect robust Scn9a expression in `151 TH Prkcd Grin2c Glut`; without target-self detection, the measured paralogs indicate essentially no downstream response to add.

I predict `Scn9a` will have no FDR<0.05 genes in the focal group:

```tsv
target_name	predicted_n_degs
Scn9a	0
```

## Limits and uncertainty

This prediction is an extrapolation because `Scn9a` itself was held out completely as a perturbation and the Distributed Agents corpus has no same-experiment `Scn9a` finding. I used Scn9a's known tissue distribution to distinguish it from the central Nav paralogs, but the parquet is a DE table rather than a raw expression matrix, so I did not directly estimate baseline Scn9a expression in the held-out edited nuclei.

The comparison to `Scn1a`, `Scn2a`, `Scn3a`, and `Scn8a` is mechanistically close at the channel-family level but imperfect at the expression level: those central alpha subunits are not Nav1.7 and were themselves weak RNA phenotypes. The absence of a DEG program also does not imply absence of altered firing, channel conductance, axonal localization, or synaptic release, because this assay measured only 3-4 week post-perturbation nuclear RNA in sparse edited postmitotic neurons.

The largest failure mode would be rare Scn9a expression within the broad `151` taxonomy label that is not obvious from canonical Nav1.7 biology; in that case the count could be 1 from Scn9a target self, analogous to `Scn1a`, `Scn2a`, and `Scn8a`. The within-dataset evidence and peripheral/olfactory external literature both make a downstream multi-gene response unlikely.
