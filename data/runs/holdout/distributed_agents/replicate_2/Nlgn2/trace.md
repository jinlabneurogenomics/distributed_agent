# DEG-count prediction trace

## Question and interpretation

The requested endpoint is the integer number of genes with
`pvals_adj < 0.05` after acute AAV/CRISPR loss of a held-out target in
`151 TH Prkcd Grin2c Glut` nuclei. The held-out manifest for this run contains
one target:

```text
Nlgn2
```

I interpreted the count exactly as the training endpoint is defined: the count
includes the perturbed target transcript if that transcript itself passes the
FDR cutoff. I did not use any held-out `Nlgn2` differential-expression rows,
because the task states that they are absent from both inputs.

## Sources

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`:
  the focal-cell training count table, used to calibrate the count scale.
- `[local file: training_de_all_cell_groups.parquet]`:
  the per-gene differential-expression statistics. I filtered this file to
  `group_name == "151 TH Prkcd Grin2c Glut"` for `Nlgn2`-related training
  perturbations and inspected which measured genes, if any, passed FDR 0.05.
- Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`, especially the
  claims that represented neuroligin/neurexin/LRRTM/CADM/PSD-near perturbations
  and represented GABA receptor or inhibitory-scaffold perturbations lack a
  broad shared postnatal neuronal nuclear-RNA module in this same experiment.
  The corpus had no direct `Nlgn2` claim, so I used it only for analogs such as
  `Nlgn3`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Gphn`, `Arhgef9`, and GABA receptor
  subunits.
- PubMed literature for target biology:
  - Varoqueaux, Jamain, and Brose 2004, DOI `10.1078/0171-9335-00410`,
    PMID `15540461`: neuroligin 2 is localized to inhibitory synapses.
  - Chubykin et al. 2007, DOI `10.1016/j.neuron.2007.05.029`,
    PMID `17582332`: neuroligin 2 selectively supports inhibitory, rather than
    excitatory, synaptic responses.
  - Poulopoulos et al. 2009, DOI `10.1016/j.neuron.2009.08.023`,
    PMID `19755106`: neuroligin 2 organizes perisomatic inhibitory synapses
    through gephyrin and collybistin and loss perturbs GABAergic/glycinergic
    transmission.
  - Loh et al. 2016, DOI `10.1016/j.cell.2016.07.041`, PMID `27565350`:
    spatial proteomics of synaptic clefts recovered inhibitory-synapse
    composition relevant to NLGN2 recruitment.
  - Halff et al. 2019, DOI `10.1016/j.celrep.2019.10.096`,
    PMID `31775031`: SNX27-mediated recycling regulates NLGN2 abundance at
    inhibitory synapses.
  - Troyano-Rodriguez, Wirsig-Wiechmann, and Ahmad 2019,
    DOI `10.1016/j.biopsych.2019.01.022`, PMID `30878196`: mature conditional
    deletion of `Nlgn2` in the mouse lateral septum impairs postsynaptic
    inhibitory transmission and stress-evoked circuit activation.
  - Ali, Marth, and Krueger-Burg 2020, DOI `10.1126/scisignal.abd8379`,
    PMID `33443230`: review of NLGN2 as a central organizer of inhibitory
    synapses.

## Computation over the training data

1. I read the held-out target CSV and confirmed that only `Nlgn2` must be
   predicted.
2. I read the 1,674-row focal training count table. Its distribution is highly
   zero-inflated: 1,205 perturbations have `n_degs == 0`; the median is 0; the
   75th percentile is 1; the 90th percentile is 2; and only 43 perturbations
   have at least 100 DEGs. Thus counts of 0 or 1 are the calibrated default
   for perturbations without evidence for a broad RNA state.
3. From the parquet I extracted, for `151 TH Prkcd Grin2c Glut`, 17,259
   measured genes per biologically relevant observed perturbation and recomputed
   `sum(pvals_adj < 0.05)`. The recomputed counts matched the training CSV.
4. I inspected the FDR-significant rows for the analog set rather than using
   count magnitudes alone. This separated target-transcript hits from genuine
   downstream RNA responses.

The key focal-cell observations were:

| training target(s) | observed `n_degs` | focal expression-pattern evidence | relevance for `Nlgn2` |
| --- | ---: | --- | --- |
| `Nlgn3` | 1 | The only FDR-significant gene was `Nlgn3` itself, down by log2FC -0.896. No downstream gene passed FDR. | Closest available neuroligin-family perturbation. It supports the idea that a single neuroligin can show detectable target-transcript loss without a broad steady-state nuclear response. |
| `Nrxn1`, `Nrxn2`, `Nrxn3` | 1, 0, 0 | `Nrxn1` had only the `Nrxn1` self transcript significant, down by log2FC -0.518; `Nrxn2` and `Nrxn3` had no FDR-significant genes. | Neurexins are presynaptic binding partners for neuroligins, including NLGN2. Their flat/singleton signatures argue against a shared transsynaptic adhesion RNA program in this assay. |
| `Arhgef9`, `Gphn` | 1, 0 | `Arhgef9` had only its self transcript significant, down by log2FC -0.571; `Gphn` had no significant gene. | Collybistin/ARHGEF9 and gephyrin/GPHN are core NLGN2-linked inhibitory postsynaptic organizers. This is the most direct inhibitory-scaffold comparison and it is null to singleton. |
| `Gabra1`, `Gabra2`, `Gabra3`, `Gabra5`, `Gabrb1`, `Gabrb2`, `Gabrb3`, `Gabrd`, `Gabrg2`, `Gabrg3` | 1, 0, 0, 0, 0, 4, 0, 2, 1, 0 | Most GABA_A receptor subunit perturbations were self-only or null. `Gabrb2` was the clearest exception, with `Gabrb2` down plus `Nr4a1` and `Vgf` up and `Nalf1` down; `Gabrd` had `Gabrd` down plus a single `Cttnbp2` increase. | They test a direct inhibitory-receptor route downstream of NLGN2. `Gabrb2` shows the assay can detect a weak activity-like response, but the lack of the same response after other GABA_A subunits or `Gphn` makes it a receptor-specific upper bound rather than the best estimate for `Nlgn2`. |
| `Gabbr1`, `Gabbr2`, `Slc6a1`, `Slc6a5`, `Gad2` | 1, 1, 0, 0, 0 | The two GABA_B receptors had only their self transcripts significant; the transport/synthesis/glycine-side comparators were null. | These bound more distant inhibitory-transmission perturbations: even related neurotransmission genes usually do not produce broad DE in this focal class. |
| `Cadm2`, `Lrrtm1`, `Lrrtm3`, `Lrrtm4`, `Dlg4`, `Shank3`, `Dag1` | 1, 1, 0, 0, 1, 2, 0 | `Cadm2` and `Dlg4` were self-only; `Lrrtm1` had one nonself singleton; `Shank3` had `Shank3` itself plus one unrelated `Uba5` row. | Less direct synaptic adhesion/scaffold counterexamples. They agree with the Distributed Agents claims that many structural synapse perturbations affect protein localization or physiology without becoming a broad nuclear mRNA module at this age and readout. |

The Distributed Agents corpus candidate topology over
`Nlgn3/Nrxn1/Nrxn2/Nrxn3/Arhgef9/Gphn/Gabr*` also recovered a connected
neuroligin/neurexin subgraph and a connected inhibitory-scaffold/GABA receptor
subgraph, confirming that these were annotated as recurring within-experiment
comparators. The corresponding claims explicitly caution that the observed
relationships are mostly flat, singleton, sparse, or non-overlapping RNA
surfaces, not phenocopies.

## Target-specific reasoning

### `Nlgn2`

External biology places NLGN2 at the postsynaptic side of inhibitory synapses:
it binds presynaptic neurexins across the synaptic cleft and works with
gephyrin and collybistin to cluster inhibitory postsynaptic machinery
(Varoqueaux et al. 2004; Chubykin et al. 2007; Poulopoulos et al. 2009; Ali
et al. 2020). That makes `Nlgn3`, `Nrxn1`, `Nrxn2`, `Nrxn3`, `Arhgef9`, and
`Gphn` the strongest in-dataset analogs, with GABA receptor subunits providing
functional downstream counterexamples.

Those analogs point to a very small count. The exact neuroligin/neurexin
neighbors in this cell group had counts 1, 1, 0, and 0, and their significant
signatures were at most target-transcript-only. The closest NLGN2 intracellular
scaffold partners were also singleton/null: `Arhgef9` had 1 DEG, itself, while
`Gphn` had 0. GABA_A subunits establish that a weak nonself response is
detectable in `151 TH Prkcd Grin2c Glut`, because `Gabrb2` induced an
`Nr4a1/Vgf/Nalf1` response in addition to its own mRNA, but that was not shared
by `Gabra1`, `Gabrg2`, `Gabrd`, other GABA_A subunits, or `Gphn`.

My zero/nonzero decision is therefore positive but only barely positive. `Nlgn2`
is likely an expressed synaptic target in glutamatergic thalamic neurons and
its paralog `Nlgn3`, neurexin partner `Nrxn1`, receptor subunits `Gabra1` and
`Gabrg2`, and scaffold partner `Arhgef9` each reached FDR only for their own
transcripts. I predict the same outcome for `Nlgn2`: one FDR-significant row,
most plausibly `Nlgn2` itself, and no coordinated downstream inhibitory-synapse
RNA module.

Predicted `n_degs` for `Nlgn2`: **1**.

## Limits

- This is an extrapolation from partners and paralogs. The same-experiment
  Distributed Agents corpus had no direct `Nlgn2` claim, and the parquet contains no
  held-out `Nlgn2` perturbation profile.
- NLGN2 is more inhibitory-synapse-specific than NLGN3, so `Nlgn3` is an
  imperfect paralog. Conversely, `Gphn` and `Arhgef9` are intracellular scaffold
  genes, not transsynaptic adhesion molecules.
- The endpoint is nuclear mRNA after sparse postnatal CRISPR. It does not
  directly measure inhibitory synapse number, GABA_A receptor clustering,
  synaptic currents, or activity-dependent phenotypes that are well documented
  for NLGN2.
- A count of 1 depends on the self transcript crossing FDR in this cell group.
  The dataset shows many examples of significant target-transcript depletion,
  but target RNA loss is not a reliable quantitative measure of editing, and
  `Gphn`, `Nrxn2`, and `Nrxn3` show that close synaptic genes can score zero.
