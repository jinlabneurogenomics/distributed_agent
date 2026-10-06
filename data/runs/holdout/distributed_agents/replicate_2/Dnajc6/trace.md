# DEG-count prediction trace

## Question and setup

The held-out manifest for this run contains one perturbation, `Dnajc6`. I
interpreted the endpoint as the exact training-count definition: the number of
measured genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` after
knockout of the target gene, including the target transcript itself when it is
significant. The cell label is the thalamic glutamatergic class whose atlas name
starts with `151`; `TH` is an anatomic thalamus tag rather than tyrosine
hydroxylase.

`Dnajc6` was held out completely as a perturbation, so no `Dnajc6` row as
`gene_target` was used. The prediction is therefore a transfer from training
perturbations that remained in the parquet/count CSV.

## Sources used

Training measurements:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`

Same-experiment semantic layer:

- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`
- The corpus had no `Dnajc6` or `Gak` entry, but it did have interpreted
  findings for the related training targets `Cltc`, `Hspa8`, `Dnajc5`,
  `Dnajc13`, `Synj1`, `Dnm1`, `Bin1`, `Vps35`, `Rab7`, and `Stxbp1`.

External literature, found through NCBI PubMed E-utilities:

- Morgan et al. 2001, PMID:11683998, DOI:10.1016/S0896-6273(01)00467-6:
  Hsc70-auxilin interaction is required for clathrin-coated-vesicle uncoating
  in presynaptic terminals.
- Eisenberg and Greene 2007, PMID:17488288,
  DOI:10.1111/j.1600-0854.2007.00568.x: auxilin/DNAJC6 and
  GAK are J-domain cofactors for Hsc70-mediated clathrin uncoating.
- McMahon and Boucrot 2011, PMID:21779028, DOI:10.1038/nrm3151: clathrin-
  mediated endocytosis proceeds through adaptor recruitment, clathrin coat
  assembly, dynamin scission, and auxilin/HSC70-dependent uncoating.
- Yim et al. 2010, PMID:20160091, DOI:10.1073/pnas.1000738107:
  auxilin knockout mice accumulate clathrin-coated vesicles and have impaired
  synaptic-vesicle endocytosis; brain GAK is up-regulated, indicating partial
  compensation by the ubiquitous auxilin homolog.
- Park et al. 2015, PMID:26345367, DOI:10.1242/jcs.171058: the GAK
  clathrin-binding and J domains can support Hsc70-mediated clathrin uncoating
  in brain even without full GAK/auxilin domain structure.
- Olgiati et al. 2016, PMID:26528954, DOI:10.1002/ana.24553; Ng et al. 2020,
  PMID:32472658, DOI:10.1002/mds.28063; Vidyadhara et al. 2023,
  PMID:36920906, DOI:10.1016/j.celrep.2023.112231: loss of DNAJC6/auxilin is
  linked to juvenile or early-onset parkinsonism and dopamine/synaptic-vesicle
  defects.
- Roosen et al. 2019, PMID:31120186, DOI:10.1111/febs.14936: several DNAJC
  family proteins converge on synaptic trafficking and clathrin dynamics, but
  family members are not interchangeable.

## Computation

I first read the requested-target CSV and the focal training counts. There were
1,674 non-held-out training targets in the focal CSV. The endpoint is extremely
zero-inflated in this cell group:

- `n_degs == 0`: 1,205 / 1,674 targets, 72.0%
- `1 <= n_degs < 10`: 363 / 1,674 targets, 21.7%
- `10 <= n_degs < 100`: 63 / 1,674 targets, 3.8%
- `n_degs >= 100`: 43 / 1,674 targets, 2.6%

Then I used the parquet only in narrow filtered scans. The main slice pulled
`151 TH Prkcd Grin2c Glut` rows for mechanistic candidate targets and sorted
significant rows by `pvals_adj`:

```python
expr = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(candidate_targets)
)
```

This verified the observed training counts and showed whether each close
comparator was self-only or had downstream genes.

## Target-specific evidence and prediction

### `Dnajc6`

`Dnajc6` encodes neuronal auxilin, a J-domain co-chaperone that recruits
Hsc70/HSPA8 to clathrin-coated vesicles after fission so that clathrin can be
removed and vesicle components recycled. The closest possible perturbation
would have been `Gak`/auxilin-2, because GAK can carry the same Hsc70/clathrin
uncoating activity and can compensate in auxilin-null brain, but `Gak` was not
available in the training-count file or Distributed Agents corpus for this run.

I therefore anchored the estimate on three measured parts of the same vesicle
cycle.

| Training target | Focal `n_degs` | Focal expression evidence | Role in the comparison |
| --- | ---: | --- | --- |
| `Hspa8` | 9 | `Dnaja1`, `Hspa4l`, `Syt4`, and `Hsp90aa1` were the leading up-regulated genes; no large endolysosomal/autophagy program was induced. | Hsc70 is the direct ATPase recruited by auxilin, but loss of the whole Hsc70 chaperone is broader than loss of one J-domain targeting factor. Distributed Agents `Hspa8:F001` and `Hspa8:F005` also describe a small, cytosolic Hsp70-quality-control response rather than a clathrin-specific one. |
| `Cltc` | 3 | The 151-class hits were `Gabra4`, `Rbms1`, and `Ero1b`, all down-regulated; `Cltc` itself was not one of the significant focal genes. | Clathrin heavy chain is the core coat, a more direct structural lesion than auxilin. The Distributed Agents `Cltc:F007` comparison found that canonical uncoating/endocytosis targets did not phenocopy the Cltc stress/downshifting response. |
| `Synj1` | 1 | The only focal hit was `Synj1` down-regulation. | Synaptojanin functions at the same late uncoating stage by removing PI(4,5)P2 after vesicle fission. Distributed Agents `Synj1:F001` to `Synj1:F003` reported a pan-surface downstream zero and a shared downstream-zero state with `Dnm1`. |
| `Dnm1` | 1 | The only focal hit was `Dnm1` down-regulation. | Dynamin 1 is the canonical synaptic-vesicle scission GTPase upstream of auxilin. Its self-only profile is a strong warning that severe vesicle-recycling physiology need not become a soma RNA program in this sparse P16-to-P37/P44 assay. |
| `Dnajc5` | 1 | The only focal hit was `Dnajc5` down-regulation. | CSPalpha is a synaptic Hsp40 co-chaperone, but it acts on SNAP-25/SNARE maintenance rather than clathrin uncoating. Distributed Agents `Dnajc5:F003` to `Dnajc5:F005` found no Hspa8, Cltc, Synj1, or Hsp40-family phenocopy. |
| `Dnajc13` | 1 | The only focal hit was `Dnajc13` down-regulation. | RME-8 is another trafficking-linked DNAJ protein, on endosomes rather than synaptic clathrin uncoating. Distributed Agents `Dnajc13:F002` to `Dnajc13:F004` showed it did not evoke the Rab7/Vps35/Hspa8/Cltc lysosomal or chaperone programs. |

Several slightly more distal presynaptic or vesicle-cycle genes reinforced the
same calibration: `Bin1`, `Syp`, `Syn1`, `Stxbp1`, `Vamp1`, and `Cplx1` each
had exactly 1 focal DEG, and `Syn2`, `Cplx2`, `Unc13a`, and `Unc13b` had 0.
The Distributed Agents induced graph over `Bin1`, `Cltc`, `Dnajc5`, `Dnajc13`, `Dnm1`,
`Hspa8`, `Rab7`, `Stxbp1`, `Synj1`, and `Vps35` was connected, with
`Bin1`/`Cltc`/`Dnajc5`/`Dnm1`/`Synj1` forming a fully connected interpreted
subset, but those links mainly encoded explicit non-convergence or boundary
claims rather than positive signature similarity.

The main counterexamples were `Vps35` and `Rab7`: they are endosomal pathway
neighbors with 17 and 501 focal DEGs respectively. I did not project those large
counts onto `Dnajc6` because they are late endosome/retromer defects with
endolysosomal stress features. Both the raw 151 signatures and the Distributed Agents
corpus separated `Dnajc13`, `Synj1`, and `Dnajc5` from those Rab7/Vps35 states.

Zero/nonzero call: I predict a nonzero but self-limited footprint. Auxilin is
neuron-enriched and close to HSPA8/CLTC biochemistry, so a complete zero is a
bit too low; however the most position-matched training perturbations,
especially `Synj1` and `Dnm1`, show that the synaptic-vesicle uncoating cycle
can be physiologically important yet almost transcriptionally silent in this
juvenile NeuN+ snRNA endpoint. `Gak` compensation gives an additional reason
for `Dnajc6` to be weaker than core `Cltc`.

Final point prediction for `Dnajc6`: **1 DEG**.

## Limits

The `Dnajc6` perturbation itself and the exact homolog `Gak` were absent from
the training perturbations available to me, so this is an extrapolation from
neighboring steps of the pathway rather than a paralog-calibrated prediction.
The DE readout is a nuclear RNA state in recovered neurons; it will miss
presynaptic vesicle-recycling defects, coated-vesicle accumulation, dopamine
transporter misrouting, and other protein- or ultrastructure-level phenotypes.
Several one-DEG comparator signatures are target-transcript events, and target
RNA loss is not a general measure of editing efficiency; I used it only because
the requested endpoint explicitly counts any measured gene passing FDR 0.05.
Finally, the focal count is sensitive to recovered perturbed-nucleus number, and
the held-out `Dnajc6` focal-cell recovery was not observable in the supplied
inputs.
