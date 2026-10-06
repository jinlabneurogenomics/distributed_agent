# DEG-count prediction trace

## Question and resolved ambiguities

The held-out manifest `069_Epb41l1.csv` contains one requested target:
`Epb41l1`. I interpreted the task as a point prediction of the exact number of
genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` focal cell
group after acute AAV CRISPR loss of function of `Epb41l1`.

I treated the count exactly as it is defined in the training file: the target's
own transcript can contribute one DEG if its row is significant. I did not use
weak or absent self-target RNA depletion as a guide-efficiency filter, because
this CRISPR/snRNA-seq readout can edit protein-coding sequence without changing
the assayed nuclear transcript.

## Sources used

- Input training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for exact focal `n_degs` values of candidate analogs.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`
  for focal log-fold-change vectors and the identities of significant genes.
- Requested-target CSV:
  `[local file: 069_Epb41l1.csv]`.
- Same-experiment Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`.
  There was no direct `Epb41l1` Claim, but I used high-confidence corpus Claims
  on represented ankyrin/spectrin/adducin membrane-skeleton perturbations
  (`claim:0e5b111907d6d3ffebf7`), represented AMPAR-core and
  AMPAR-trafficking/scaffold perturbations (`claim:a9367c3aeaad95bfae9c`),
  and represented PSD/synaptic-adhesion scaffolds
  (`claim:60396794c5493932dc07`).
- PubMed via NCBI E-utilities for public 4.1N biology:
  Shen et al., 2000, DOI `10.1523/JNEUROSCI.20-21-07932.2000`,
  PMID `11050113`; Maximov et al., 2003, DOI
  `10.1016/S1044-7431(02)00027-1`, PMID `12676536`; Wozny et al., 2009,
  DOI `10.1242/jcs.037382`, PMID `19225127`; Copits and Swanson, 2013,
  DOI `10.1074/jbc.M112.440719`, PMID `23400781`; Pushkin et al., 2023,
  DOI `10.1523/JNEUROSCI.0185-23.2023`, PMID `37845032`.

## Dataset computations

1. I confirmed that `Epb41l1` is absent from the 1,674-row focal training-count
   CSV, as expected for a complete holdout, and that close 4.1-family paralogs
   `Epb41`, `Epb41l2`, `Epb41l3`, and `Epb41l4` were also not available as
   training perturbations.
2. I seeded a comparison set from represented membrane-skeleton and AMPAR/PSD
   neighbors: `Ank1`, `Ank2`, `Sptan1`, `Dlg4`, and `Gria1`. Distributed Agents
   corpus expansion against the exact training-target universe added
   `Sptb`, `Add1`, `Add2`, `Add3`, `Gria2`, `Gria3`, `Cacng2`, `Grin1`,
   `Grin2a`, `Grin2b`, and `Wdr26`.
3. I ran a focal profile comparison over the DE parquet, restricted to
   `group_name == "151 TH Prkcd Grin2c Glut"`, using `gene_target` as the
   perturbed entity, `names` as the measured feature, `logfoldchanges` as the
   signed profile value, and `pvals_adj < 0.05` as the significance threshold.
   The 16-node cohort had 10 zero-response perturbations, four 1-9-DEG
   perturbations, one 13-DEG perturbation (`Wdr26`), and one 89-DEG
   perturbation (`Grin1`). The profile diagnostic found low shared positive
   tail structure across the cohort: mean positive top-tail overlap coefficient
   0.074 across all 120 pairs and no positive significant-program overlap.
4. For the candidate genes most relevant to `Epb41l1`, I filtered the parquet
   directly to recover the significant gene names:

```python
table = ds.dataset(path, format="parquet").to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj"],
    filter=(pc.field("group_name") == focal)
    & pc.field("gene_target").isin(targets),
)
```

   The one-DEG cases `Sptan1`, `Dlg4`, `Grin2a`, `Nlgn3`, `Prkcg`, and
   `Abhd12` were self-target-only; `Grin2b` had its own transcript plus
   `Pianp`; `Dlgap4` had its own transcript plus `Vgf`. Thus most small
   nonzero counts around this neighborhood were not broad downstream states.

## Target-specific reasoning

### `Epb41l1`

`Epb41l1` encodes neuronal protein 4.1N, a FERM-domain member of the protein
4.1 membrane/cytoskeleton adaptor family. Public work places 4.1N at
glutamatergic synapses and at the spectrin-actin membrane skeleton: Shen et al.
showed that 4.1N/4.1G bind the GluR1/Gria1 AMPA-receptor C terminus and can
link AMPARs to actin; Maximov et al. found an association between 4.1N and the
type 1 IP3 receptor; Copits and Swanson showed regulation of GluK1/GluK2
kainate-receptor trafficking through 4.1N; and Pushkin et al. found a
cell-type-specific 4.1N requirement for dentate granule glutamatergic synapse
function through the FERM domain. Wozny et al. also showed that a mouse line
with complete 4.1G loss and residual 4.1N expression had only a moderate
synaptosomal GluR1 reduction at three weeks and no major basal hippocampal
transmission or LTP defect, reinforcing that this axis can be buffered.

The closest same-experiment analogs were membrane-skeleton perturbations rather
than pore-forming glutamate receptors. In the focal training counts,
`Sptan1` had `n_degs = 1`, and the only significant row was `Sptan1` itself;
`Ank1`, `Ank2`, `Sptb`, `Add1`, `Add2`, and `Add3` all had `n_degs = 0`.
The Distributed Agents membrane-skeleton Claim over `Add1`, `Ank1`, `Ank2`, `Sptan1`,
and `Sptb` summarized the same-experiment reports as flat, sparse, or
non-overlapping rather than as a shared postnatal neuronal nuclear RNA program.
Because protein 4.1N is itself a spectrin/actin-linked membrane adaptor, this
seven-gene block was my primary quantitative anchor.

The AMPAR and postsynaptic-scaffold side gave the same sign. `Gria1`, `Gria2`,
`Gria3`, and `Cacng2` each had `0` focal DEGs, while other AMPAR-axis training
members were also null or singleton-only: `Cacng3 = 0`, `Ica1 = 0`,
`Rnf220 = 0`, and `Abhd12 = 1` with only `Abhd12` significant. PSD-scaffold
neighbors were likewise small: `Dlg4 = 1` with only `Dlg4` significant,
`Dlgap4 = 2`, `Homer2 = 0`, `Lrrc7 = 0`, `Nlgn3 = 1` with only `Nlgn3`
significant, `Shank2 = 0`, `Shank3 = 2`, and `Frmpd4 = 0`. These are not
direct 4.1-family paralogs, but they are the represented perturbations closest
to the AMPAR/PSD protein-localization functions that make `Epb41l1`
interesting.

I treated `Grin1` as a boundary rather than a pooled analog. It had 89 focal
DEGs including `Grin1`, `Scg2`, `Stmn4`, `Kctd16`, and `Gpm6a`, so the assay
could detect a glutamate-receptor perturbation in this cell group. However,
`Grin2a` and `Grin2b` had only one and two DEGs respectively, the corpus
contrasts separate NMDAR-core responses from AMPAR/scaffold responses, and
4.1N is a receptor-trafficking/membrane-linker protein rather than the NMDAR
ion-channel core. I also rejected `Wdr26` despite its 13 DEGs: it entered
through weak expanded edges and is not a protein 4.1, AMPAR, or
spectrin-actin analog.

The prediction is therefore a zero/near-zero call. A count of exactly one is
plausible if `Epb41l1`'s own transcript is detectably reduced, as happened for
`Sptan1` and `Dlg4`; nevertheless the closer membrane-skeleton and AMPAR
training perturbations were mostly literal zeros, and their singletons did not
carry a transferable downstream expression signature. I predict no gene will
pass BH FDR 0.05.

## Limits

The largest limitation is the absence of a true 4.1-family paralog in the
focal training-count file, so the prediction transfers from protein-neighborhood
and membrane-skeleton biology rather than from `Epb41l1` itself. The public
4.1N literature is mostly from hippocampal, cerebellar, or cultured neuronal
systems and measures receptor localization, synaptic currents, morphology, or
viability, not acute thalamic juvenile snRNA-seq after sparse CRISPR editing.
The focal readout is also insensitive to protein redistribution and synaptic
physiology, which are precisely the endpoints most likely to move after loss
of a membrane-cytoskeletal scaffold. Finally, self-transcript significance is
part of `n_degs` but is hard to transfer gene by gene because CRISPR editing,
nonsense-mediated decay, baseline nuclear expression, and power vary by locus.
