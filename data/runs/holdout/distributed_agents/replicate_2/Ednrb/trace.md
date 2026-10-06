# Trace

## Question as interpreted

The requested readout is the number of genes with `pvals_adj < 0.05` after
Benjamini-Hochberg correction in the `151 TH Prkcd Grin2c Glut` differential
expression table for each held-out perturbation.  In this run the manifest
contains one held-out target, `Ednrb`, and the `Ednrb` perturbation itself is
absent from both the training count table and the DE parquet.  I therefore
predicted a focal-cell point count for `Ednrb` by comparing it with measured
training perturbations that are mechanistically close enough to constrain the
answer.

I treated a prediction of `0` as "no measured gene survives FDR 0.05", not as a
claim that EDNRB is biologically irrelevant.  The assay is sparse, acute,
postnatal AAV-CRISPR loss of function in NeuN-enriched brain nuclei; it is not
a germline Ednrb knockout, it does not sample the enteric nervous system, and
astrocytes, vascular cells, melanocytes, oligodendrocytes, and Schwann cells are
largely absent.

## Sources used

- Input endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 066_Ednrb.csv]`.
- Distributed Agents same-experiment corpus,
  release `perturbai-july-260713-sourceguard-1773-v1`.  `Ednrb` itself had no
  corpus target card, but the corpus had relevant cards for `Ednra`, `Ret`, and
  `Sox10`.
- Literature from PubMed and the Distributed Agents Ednra references:
  Davenport et al. 2016, doi:10.1124/pr.115.011833, PMID:26956245;
  Hosoda et al. 1994, doi:10.1016/0092-8674(94)90017-5, PMID:8001159;
  Baynash et al. 1994, doi:10.1016/0092-8674(94)90018-3, PMID:8001160;
  Nakagomi et al. 2000, doi:10.1016/S0306-4522(00)00345-6, PMID:11074166;
  Hostenbach et al. 2016, doi:10.1016/j.pneurobio.2016.04.009,
  PMID:27132521; and Koyama 2021, doi:10.3390/ijms22094333,
  PMID:33919338.

## Dataset computations

- Loaded the held-out manifest and confirmed that this run asks only for
  `Ednrb`.
- Loaded the focal-cell training count CSV.  It contains 1,674 training targets;
  469 have a nonzero DEG count and the median count is 0, so most represented
  perturbations are transcriptionally silent at FDR 0.05 in this cell group.
- Inspected the parquet metadata.  Row groups are homogeneous for
  `group_name`, so I selected the 35 row groups whose `group_name` statistic was
  `151 TH Prkcd Grin2c Glut`, yielding 28,891,566 focal rows:
  1,674 perturbations times 17,259 measured genes.
- Within that focal slice I checked the direct endothelin-receptor analog
  `Ednra` and other represented proximal comparators.  For `Ednra`, the best
  raw Wilcoxon p-value in the focal group was 2.22e-4, but all 17,259 genes had
  `pvals_adj = 1.0`, matching the endpoint count of 0.
- I also inspected represented developmental and GPCR comparators in the focal
  endpoint table rather than using family membership alone.  The key observed
  counts were:

| comparator | focal `n_degs` | relevance to `Ednrb` |
| --- | ---: | --- |
| `Ednra` | 0 | The other canonical endothelin receptor; same peptide-ligand system, also a GPCR. |
| `Plcb1` | 0 | Downstream PLC effector of Gq-coupled receptor signaling. |
| `Prkca` | 0 | PKC effector downstream of PLC/Ca2+/DAG signaling. |
| `Mapk1` | 0 | MAPK effector commonly engaged downstream of endothelin receptors. |
| `Calm2` | 0 | Calmodulin comparator from represented endothelin-pathway signaling. |
| `Calm3` | 1 | A near-null Ca2+/calmodulin comparator. |
| `Dlx6` | 0 | A represented neural-crest transcriptional endpoint of endothelin signaling. |
| `Sox10` | 0 | Neural-crest, glial, and melanocyte lineage regulator close to Ednrb disease biology. |
| `Ret` | 0 | Enteric-neural-crest receptor tyrosine kinase pathway and Hirschsprung comparator. |
| `Gfra1` | 0 | GDNF co-receptor for RET; phenocopies Ret as flat in the corpus. |
| `Erbb3` | 0 | Neural-crest/Schwann-cell signaling comparator represented in the assay. |
| `Kit` | 0 | Melanocyte-lineage comparator. |
| `Pax3` | 0 | Neural-crest and melanocyte transcriptional comparator. |
| `Phox2b` | 0 | Autonomic/enteric neural-crest transcriptional comparator. |
| `Zeb2` | 0 | Neural-crest developmental comparator. |

## Target-specific reasoning

### Ednrb

`Ednrb` encodes the endothelin type-B receptor, a seven-transmembrane GPCR
activated by endothelin peptides.  The canonical mammalian endothelin pathway
has two receptors, `Ednra`/ET_A and `Ednrb`/ET_B; EDNRB can signal through Gi
and Gq-family pathways and into PLC, PKC/Ca2+, and MAPK modules, depending on
cell type (Davenport et al. 2016; Koyama 2021).  The strongest loss-of-function
mouse prior for Ednrb is developmental rather than an acute mature-neuron
phenotype: targeted or natural Ednrb mutations cause aganglionic megacolon and
coat spotting by disrupting neural-crest-derived enteric neurons and
melanocytes, and Edn3 ligand mutants phenocopy that pathway (Hosoda et al.
1994; Baynash et al. 1994).

The closest measured target in the training set is `Ednra`, not because ET_A is
identical to ET_B, but because it is the other receptor for the same endothelin
peptide system.  `Ednra` was completely flat in the focal cell group:
`n_degs = 0`, with no gene below FDR 0.05 and all adjusted p-values equal to
1.0.  The Distributed Agents Ednra card agreed at the broader same-experiment level:
19 of 20 Ednra-measured neuronal groups had no genes below FDR 0.10, the
remaining group had a single `Dhtkd1` hit, whole-universe signature neighbors
were near zero, and represented endothelin-proximal targets `Plcb1`, `Prkca`,
`Mapk1`, `Calm1`, `Calm2`, `Calm3`, and `Dlx6` did not phenocopy the Ednra
surface.  That corpus card also recorded that `Ednrb`, `Edn1`, `Edn2`, `Edn3`,
`Gnaq`, `Gna11`, `Gna12`, and `Gna13` were not available as perturbation
targets, so `Ednra` is the only direct receptor analog.

The larger developmental neighborhood gives the same direction.  In the focal
training endpoint, `Sox10`, `Ret`, `Gfra1`, `Erbb3`, `Kit`, `Pax3`, `Phox2b`,
and `Zeb2` all have 0 DEGs.  The Distributed Agents `Sox10` findings describe `Sox10` as
a pan-neuronal null across recovered NeuN+ groups and explicitly place the
expected myelin, Schwann-cell, and neural-crest target program outside the
sampled neuronal assay.  The Distributed Agents `Ret` findings likewise found no robust
downstream FDR response to postnatal mosaic `Ret` loss in assayed neuronal
groups, despite the well-known enteric/kidney/adrenal RET developmental prior.
Those two same-experiment results are good counterweights to the human and
mouse disease priors: they show that related neural-crest and enteric-neuron
biology is largely not model-visible in these postnatal forebrain neurons.

Finally, EDNRB is especially associated with non-neuronal or injury-responsive
central compartments.  In rat brain, Ednrb mRNA was reported mainly in
astrocytes, Bergmann glia, choroid plexus, and ependymal cells rather than in
the neurons that express endothelin-converting enzymes (Nakagomi et al. 2000).
Astrocytic endothelin signaling is prominent in reactive astrocytes and injury
models (Hostenbach et al. 2016; Koyama 2021), contexts not represented by the
NeuN-enriched AAV-PHP.eB experiment.  The focal GPCR panel in training also did
not show a hidden peptide-receptor vulnerability: `Adra1a`, `Adra2a`, `Adra2b`,
`Agtr1a`, `Agtr2`, `Chrm2`, `Chrm3`, `Npy1r`, `Npy2r`, `Npy5r`, `Oprd1`,
`Oprk1`, `Oprl1`, `Oprm1`, `Pth1r`, `Sstr5`, `Tacr3`, and many serotonin
receptor perturbations were all 0 in the same endpoint.

Together these observations favor no focal FDR-significant response from acute
`Ednrb` loss.  I therefore predict:

| target | predicted focal `n_degs` |
| --- | ---: |
| `Ednrb` | 0 |

## Limits

- `Ednrb` itself was held out, so the prediction has no direct Ednrb signature.
- `Ednra` is the best measured receptor analog but is not a paralog with
  identical ligand selectivity or cell expression; ET_A and ET_B biology diverge
  strongly in vascular, glial, and developmental compartments.
- The most direct EDNRB ligands and G proteins, including `Edn1`, `Edn2`,
  `Edn3`, `Gnaq`, `Gna11`, `Gna12`, and `Gna13`, were absent as training
  perturbation targets.
- The major Ednrb phenotypes are in embryonic neural crest, enteric nervous
  system, melanocytes, vasculature, and reactive glia.  Those are exactly the
  contexts that the sparse P16-to-P37 NeuN+ screen undersamples.
- A prediction of 0 still allows very weak subthreshold shifts, a response in a
  rare unsampled cell state, or a response that would appear with stronger
  biallelic editing, ligand stimulation, injury, or a glial/vascular readout.
