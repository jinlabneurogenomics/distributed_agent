# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The held-out target list for this run contains one perturbation, `Cntn1`. I
interpreted the requested value as the assay endpoint in the training CSV:
the integer number of measured genes whose Scanpy Wilcoxon
Benjamini-Hochberg adjusted p-value is below 0.05 in recovered
`151 TH Prkcd Grin2c Glut` nuclei. The target was held out as a perturbation,
so its own `Cntn1` knockout signature and true `n_degs` were absent from both
input files.

One ambiguity is whether a target's own transcript counts toward `n_degs`.
The supplied training counts and the parquet use the same definition: for
`Cntnap1`, `Cntnap2`, `L1cam`, `Robo1`, and `Tenm3`, the focal parquet has only
the self-transcript at FDR 0.05 and the training CSV reports `n_degs = 1`.
I therefore counted a possible `Cntn1` self decrease as one DEG.

## Sources

- Declared endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Cntn1`.
- The selected same-experiment interpretation corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, via its calibrated Finding
  ledger and graph interface. I used it as a compact annotation of visible
  training perturbations, not as an independent measurement.
- PubMed literature retrieved through NCBI E-utilities for external Cntn1
  biology:
  - Colakoglu et al. 2014, PNAS, PMID 24385581,
    DOI `10.1073/pnas.1313769110`.
  - Gollan et al. 2003, J Cell Biol, PMID 14676309,
    DOI `10.1083/jcb.200309147`.
  - Bhat et al. 2001, Neuron, PMID 11395000,
    DOI `10.1016/s0896-6273(01)00294-x`.
  - Hu et al. 2003, Cell, PMID 14567914,
    DOI `10.1016/s0092-8674(03)00810-9`.
  - Mohebiany et al. 2014, Adv Neurobiol, PMID 25300137,
    DOI `10.1007/978-1-4614-8090-7_8`.

## Computation over the declared data

I treated the training-count CSV as the exact focal endpoint for non-held-out
perturbations and the parquet as the exact source of their gene-level
signatures.

1. Counted the endpoint distribution across the 1,674 visible training
   perturbations in the focal class. It is strongly zero-inflated:
   1,205 targets have zero DEGs, 276 have one DEG, and only 193 have more than
   one DEG.
2. Looked up visible perturbations near `Cntn1` by mechanism: `Cntnap1`,
   `Cntnap2`, `L1cam`, `Nrcam`, `Notch1`, `Dscam`, `Robo1`, `Robo2`, `Tenm3`,
   `Tenm4`, `Cadm2`, `Ncam1`, `App`, `Sptan1`, `Sema6a`, and related genes
   represented in the training table.
3. Read only parquet row groups overlapping `151 TH Prkcd Grin2c Glut`, then
   filtered to the visible adhesion and guidance perturbations. This avoided
   a whole-file scan and gave exact focal signatures for the analogs:

   ```python
   mask = (
       pc.equal(tab["group_name"], "151 TH Prkcd Grin2c Glut")
       & pc.is_in(tab["gene_target"], value_set=pa.array(sorted(targets)))
   )
   ```

4. Queried the same focal row groups for measured `Cntn1`, `Cntn2`, `Cntn3`,
   `Cntn4`, `Cntn6`, `Cntnap1`, `Cntnap2`, `L1cam`, `Nrcam`, and other
   adhesion/guidance transcripts under every visible perturbation. This asked
   whether `Cntn1` is a gene in recurrent broad programs even though its own
   perturbation is held out.

## `Cntn1` analogs and counterexamples

`Cntn1` encodes contactin-1/F3, a GPI-anchored Ig-superfamily adhesion protein.
At myelinated axons it works with Caspr1/CNTNAP1 on the axonal side of the
paranode and with glial neurofascin-155; Cntn1-deficient mice have disrupted
paranodal junctions, mislocalized Kv channels, abnormal myelin terminal loops,
and CNS hypomyelination. F3/contactin can also signal through Notch to promote
oligodendrocyte maturation in glial systems. These external phenotypes are
structural, axoglial, and developmental. In the requested assay, the
intervention is sparse P16 neuronal CRISPR loss of function and the measured
material is NeuN-positive neuronal nuclei recovered three to four weeks later.
Thus the direct molecular consequence should be loss of an axonal surface
adhesion molecule, with any broad DEG count requiring propagation from axonal
contact or myelin-domain defects back to somatic nuclear RNA in surviving
thalamic neurons.

The most direct within-dataset analog is `Cntnap1`, because Caspr1 and Cntn1
form the same axonal paranodal adhesion complex. In the focal cell group,
`Cntnap1` had exactly one FDR 0.05 gene:

| training perturbation | focal `n_degs` | focal FDR genes | relevance to `Cntn1` |
|---|---:|---|---|
| `Cntnap1` | 1 | `Cntnap1`, logFC -0.822, FDR 1.09e-11 | direct paranodal Cntn1/Caspr1 partner; same-experiment corpus reports no downstream FDR 0.10 response in any recovered group |
| `Cntnap2` | 1 | `Cntnap2`, logFC -1.087, FDR 7.90e-06 | Caspr paralog, but juxtaparanodal rather than paranodal and paired with Cntn2/TAG-1; self-only in the focal class |
| `L1cam` | 1 | `L1cam`, logFC -0.749, FDR 1.44e-24 | neuronal Ig-superfamily axon-guidance CAM; target-transcript-only in the focal class and in the high-yield MB Glut class |
| `Nrcam` | 2 | `Nrcam`, `Letm2` | L1-family node/axon-guidance receptor; the extra focal event was a singleton (`Letm2`, logFC 0.459, FDR 0.049) rather than a recovered adhesion program |
| `Dscam` | 0 | none | Ig CAM and wiring molecule; no focal response |
| `Notch1` | 0 | none | Cntn1/F3 can act as a Notch ligand in oligodendrocyte maturation, but neuronal `Notch1` loss was flat in this endpoint |
| `Robo1` | 1 | `Robo1`, logFC -0.538, FDR 2.72e-06 | axon-guidance receptor, included as a structural counterexample with a self-only focal signature |
| `Robo2` | 0 | none | axon-guidance receptor counterexample |
| `Tenm3` | 1 | `Tenm3`, logFC -0.787, FDR 1.61e-09 | synaptic/axon-targeting CAM counterexample with self-only signal |
| `Tenm4` | 0 | none | synaptic/axon-targeting CAM counterexample |

The Cntnap1 corpus report is important because it covers the whole recovered
surface, not just the focal group: `Cntnap1` loss had zero non-self downstream
genes at FDR 0.10 in every recovered neuronal group. The same report notes that
`Cntnap2`, Kv1-channel comparators, `Nrcam`, `Nrxn1`, and `Ank2` did not define
a common Caspr-like transcriptional state. `L1cam` and `Nrcam` reports reached
the same qualitative conclusion for L1-family and ankyrin-associated neuronal
adhesion genes: the known biology is local membrane organization, guidance, or
node/paranode structure, while the postmitotic nuclear RNA readout is nearly
flat.

The measured-gene query showed that `Cntn1` can itself be regulated inside
large focal signatures, but almost always downstream of broad RNA-processing,
chromatin, proteostasis, or trafficking perturbations rather than adhesion
perturbations. In `151 TH Prkcd Grin2c Glut`, focal `Cntn1` was significantly
changed after `U2af2`, `Arid2`, `Sin3a`, `Rnpc3`, `Tcf7l2`, `Ufc1`,
`Snrnp70`, `Trim2`, `Uba5`, `Gfpt1`, `Prpf6`, `Dhdds`, `Psmb4`, `Esrra`,
`Rab7`, `Brd4`, and `Hnrnpu` perturbation. Those are upstream regulators or
cell-state stresses that can move an adhesion transcript; they are not
evidence that loss of the adhesion transcript feeds back into the same broad
program.

## Prediction

I predict `Cntn1` will have one DEG in the held-out focal signature.

The expected one gene is driven by the likely self-transcript decrease:
`Cntn1` is expressed enough in this cell group to be a repeatedly measurable
downstream DEG in other broad perturbations, and direct analogs with visible
target RNA in the focal group generally crossed the FDR threshold for their
own transcript. I did not add a downstream Cntn1/Caspr1/Notch/myelination
module. The best in-assay complex partner, `Cntnap1`, was self-only in the
same focal endpoint and transcriptionally buffered across all recovered
neuronal groups; the closest represented Ig-superfamily and guidance
counterexamples were also zero, self-only, or singleton responses.

## Limits

This is an extrapolation from Cntn1 partners because `Cntn1`, `Cntn2`, `Nfasc`,
and several other direct node/paranode components were not available as
training perturbations. A Cntn1 knockout could score zero if the sparse
postnatal CRISPR edit disrupts contactin protein without enough nonsense-
mediated decay of the nuclear transcript to cross FDR, and it could score above
one if loss of neuronal Cntn1 creates a detectable secondary response absent
from `Cntnap1`. The oligodendrocyte maturation literature is especially
imperfect for this endpoint: glia were under-sampled by NeuN sorting, and
the experiment perturbed neuronal genomes rather than oligodendrocytes.
The prediction is therefore strong for "no broad recovered neuronal nuclear
program" but weaker for the exact self-transcript count.
