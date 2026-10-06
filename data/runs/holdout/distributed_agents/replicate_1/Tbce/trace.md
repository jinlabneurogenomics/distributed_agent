# DEG-count prediction trace

## Question and endpoint

The requested held-out perturbation is `Tbce`. I interpreted the requested
value as a point prediction for the exact benchmark endpoint:

- cell group: `151 TH Prkcd Grin2c Glut`
- endpoint: the number of measured genes with `pvals_adj < 0.05`
- statistic: Scanpy Wilcoxon differential expression in perturbed versus
  matched control nuclei
- perturbation: acute sparse AAV-CRISPR loss of function in postmitotic mouse
  neurons, delivered at P16 and read out 3-4 weeks later

The target itself was completely held out. It was absent from the supplied
training-count CSV, absent from `training_de_all_cell_groups.parquet`, and no
same-experiment Finding was available for `Tbce` in the selected internal
corpus. I therefore treated the endpoint for `Tbce` as absent from the declared
inputs and transferred from assayed mechanistic analogs.

The point prediction I finalized for `Tbce` is **12 DEGs**.

## Sources

- Declared Perturb-seq differential-expression parquet:
  `training differential-expression dataset`.
  This was direct evidence for the focal-cell signatures of candidate training
  analogs.
- Declared focal-cell training DEG counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This was direct evidence for the count scale of non-held-out perturbations.
- Requested-target manifest:
  `single-target request for Tbce`.
- Internal same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, especially packaged Findings
  and Evidence for `Tbcd`, `Tuba1a`, `Tubb4b`, `Tubb5`, `Map1b`, `Mapt`,
  `Map6`, and `Kif5a`. This corpus is an interpreted representation of the
  same experiment, not an independent replication.
- External mechanism sources:
  Reactome, post-chaperonin tubulin folding pathway `R-HSA-389977`; Kortazar et
  al. 2006, doi:10.1016/j.yexcr.2006.09.002; Tian et al. 2010,
  doi:10.1002/cm.20480; Taheri et al. 2025, doi:10.1038/s41467-025-68142-0;
  Martin et al. 2002, doi:10.1038/ng1016; Schaefer et al. 2007,
  doi:10.1523/JNEUROSCI.1599-07.2007; Sferra et al. 2016,
  doi:10.1016/j.ajhg.2016.08.006; Efentakis et al. 2022,
  doi:10.1093/eurheartj/ehab222.

## Computation over the declared inputs

I first read the requested-target CSV and confirmed it contains exactly one
held-out target, `Tbce`. I then summarized the training counts to calibrate the
focal endpoint:

- training targets in the focal CSV: 1,674
- zeros: 1,205
- median: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- maximum: 2,677

Thus a count near 10 is already in the high, but not extreme, tail of this
focal-cell endpoint.

I queried the parquet only for `151 TH Prkcd Grin2c Glut` rows from tubulin
biogenesis, tubulin-isotype, microtubule-associated, kinesin, and dynein
control perturbations. The operation was the focal-cell equivalent of:

```python
dataset = pyarrow.dataset.dataset(training_parquet, format="parquet")
table = dataset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & ds.field("gene_target").isin(selected_training_analogs)
    ),
)
```

The relevant focal-cell counts from the supplied training CSV and selected
parquet rows were:

| Training perturbation | focal `n_degs` | focal expression pattern |
| --- | ---: | --- |
| `Tbcd` | 12 | 146 perturbed vs 23,679 controls; 12 FDR<0.05 genes, led by `Tuba1a` logFC 0.488, q=1.96e-06 and `Tuba1b` logFC 0.675, q=1.96e-06; the remaining FDR<0.05 genes were `Ypel4`, `Nfil3`, `Kctd16`, `Lrrc7`, `Ptprn2`, `Samd5`, `Satb1`, `Slc25a23`, `Mturn`, and `Jun`. |
| `Tuba1a` | 7 | 121 perturbed; self-depletion plus up-regulation of `Tubb3`, `Tubb2a`, `Tuba4a`, `Tubb4a`, `Tubb4b`, and `Tubb5`. |
| `Tuba4a` | 2 | 199 perturbed; self-depletion plus only `Mast1` in the focal group. |
| `Tubb5` | 1 | 186 perturbed; strong self-RNA decrease, q=7.71e-23, with no focal downstream FDR<0.05 gene. |
| `Tubb4b` | 1 | 171 perturbed; self-RNA decrease only. |
| `Map1b` | 1 | 210 perturbed; `Map1b` self-RNA decrease only. |
| `Mapt` | 1 | 190 perturbed; `Mapt` self-RNA decrease only. |
| `Map6` | 0 | no focal FDR<0.05 gene. |
| `Kif1a` | 1 | 112 perturbed; `Kif1a` self-RNA decrease only. |
| `Kifbp` | 2 | 249 perturbed; `Kifbp` self-depletion and `Srebf2` down. |
| `Dctn1` | 75 | 182 perturbed; broad sterol/lipid response, including `Insig1`, `Msmo1`, `Hmgcs1`, `Hmgcr`, `Fdft1`, `Sqle`, `Fdps`, `Ldlr`, and many others. |

`Tbcd` is the dominant quantitative basis. The other rows calibrate what not
to do: direct tubulin paralogs and structural microtubule genes are not
interchangeable, and a dynein-dynactin transport state can be much broader than
a tubulin-folding state.

## Target-specific reasoning

### `Tbce`

`Tbce` encodes tubulin-specific cofactor E, an alpha-tubulin-binding cofactor
in the post-chaperonin tubulin folding/recycling pathway. Reactome places TBCE
in the same post-chaperonin alpha/beta-tubulin folding pathway as TBCD and
TBCC. Kortazar et al. showed that TBCE cooperates with TBCB to dissociate
native tubulin heterodimers and form a TBCE/TBCB/alpha-tubulin complex after
dissociation. Tian et al. showed that TBCD and TBCE can both act in the
reverse heterodimer-disruption reaction, and recent cryo-EM work by Taheri et
al. resolved a TBCD/TBCE/ARL2 assembly in which TBCD wraps beta-tubulin while
TBCE extends along alpha-tubulin.

That biochemical placement makes assayed `Tbcd`, not the TBC-domain Rab GAP
genes `Tbc1d23`, `Tbc1d24`, or `Tbc1d32`, the closest training analog. The
intervention chain is:

1. CRISPR loss of `Tbce` is expected to impair the tubulin cofactor machine on
   the alpha-tubulin side.
2. Impaired cofactor activity should perturb alpha/beta-tubulin heterodimer
   folding, recycling, or stability.
3. Postmitotic thalamic neurons should buffer that by the same kind of
   tubulin-RNA feedback detected after `Tbcd` perturbation.
4. The measured endpoint is survivor-conditioned nuclear RNA; axon-local
   microtubule loss, cell depletion, or Golgi fragmentation can be missed if
   they do not drive stable soma/nuclear DE.

The same-experiment `Tbcd` Finding package supports that third step in the
exact readout: `Tbcd` produced a sparse but real response across 6 cell groups,
with the strongest surface in `151 TH Prkcd Grin2c Glut`. The focal 12-gene
signature was not a generic proteotoxic-collapse signature; the strongest and
most recurrent events were alpha-tubulin compensation (`Tuba1a`, `Tuba1b`),
with a small thalamic `Ypel4`/`Nfil3`/`Kctd16`/`Lrrc7`/`Ptprn2`/`Samd5`/
`Satb1`/`Mturn`/`Slc25a23`/`Jun` remodeling module.

The assayed tubulin subunits were informative negative controls. `Tuba1a`
knockout had a smaller, seven-gene focal tubulin-paralog response. `Tuba4a`,
`Tubb5`, and `Tubb4b` were one- or two-gene focal responses; in the broader
packaged reports, `Tubb5` strongly depleted its own RNA in the focal cell group
but did not induce tubulin-paralog, p53-apoptosis, ISR/UPR, or broad stress
transcripts. `Map1b`, `Mapt`, `Map6`, `Kif1a`, and `Kif5a` further show that
microtubule-track, MAP, and motor phenotypes often remain local or
post-translational in this P16-to-P37/P44 snRNA-seq endpoint. Conversely,
`Dctn1` produced 75 focal DEGs, dominated by sterol/lipid genes, so the assay
can detect a larger microtubule-transport response when a perturbation drives
one; `Tbce` is not a dynactin adaptor, so I did not transfer the `Dctn1` count.

External mouse and human data argue that TBCE loss is a real neuronal
microtubule insult rather than a silent paralog. Martin et al. mapped the
progressive motor neuronopathy mouse to a destabilizing `Tbce` missense
variant and found reduced axonal microtubules rescued by a wild-type `Tbce`
transgene. Schaefer et al. localized TBCE to the Golgi in motor neurons and
showed that the pmn mutation, TBCE depletion, and Golgi disruption compromise
axonal tubulin routing. Sferra et al. identified human biallelic `TBCE`
variants that reduce TBCE protein and impair microtubule polymerization in a
progressive encephalopathy with distal spinal muscular atrophy. These external
results support a same-direction prior for a nonzero tubulin-folding response,
but they are not direct measurements of the held-out endpoint: they mostly use
germline or hypomorphic disease contexts, motor neurons or fibroblasts, and
structural microtubule/polymerization readouts.

I therefore predicted a positive count near `Tbcd`, not a zero like `Map6` or a
large `Dctn1`-like response. I kept the estimate at **12**, exactly matching
the focal `Tbcd` count, because `Tbcd` and `Tbce` are opposing-side cofactors
in the same limiting tubulin heterodimer cycle and no closer held-in
perturbation exists. The main downward uncertainty is that TBCE depletion may
manifest as axonal/Golgi microtubule-routing pathology with little stable
nuclear feedback in thalamic surviving nuclei. The main upward uncertainty is
that, if partial TBCE loss destabilizes alpha-tubulin more strongly than TBCD
loss in this neuronal state, the alpha-tubulin feedback module could become
larger than the 12-gene `Tbcd` surface.

## Limits

- `Tbce` itself is not in the declared parquet, the training-count CSV, or the
  same-experiment corpus, so the prediction is endpoint transfer rather than an
  observed value.
- `Tbcd` is the only assayed tubulin cofactor in the training set; `Tbca`,
  `Tbcb`, `Tbcc`, prefoldin subunits, CCT subunits, and `Arl2` were absent as
  directly assayed focal-count anchors. `Arl2bp` was present but indirect and
  had zero focal DEGs.
- The selected same-experiment corpus is derived from the same Perturb-seq
  experiment as the parquet; I used it for packaged interpretation and
  references, not as independent replication.
- Human TBCE disease, the pmn mouse, vascular smooth-muscle `Tbce` knockout,
  and structural cryo-EM/biochemistry establish mechanism, not the exact DEG
  yield in P16 sparse thalamic CRISPR.
- The endpoint counts FDR-thresholded nuclear RNA among recovered nuclei. It
  can miss protein-level tubulin pools, microtubule polymerization, distal
  axon transport, Golgi fragmentation, or selection of severely injured cells.
