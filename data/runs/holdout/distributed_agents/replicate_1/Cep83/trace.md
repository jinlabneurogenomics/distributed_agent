# Held-out DEG-count prediction

## Question and endpoint

The requested prediction is the number of genes expected to satisfy
`pvals_adj < 0.05` after acute AAV CRISPR loss of `Cep83` in
`151 TH Prkcd Grin2c Glut` neurons. The held-out `Cep83` perturbation is absent
from both supplied inputs, so I treated the focal-cell
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` file as the direct observed
endpoint for visible perturbations and the Parquet as the direct source for
per-gene signatures of candidate analogs.

The endpoint is an assay- and power-dependent count of significant nuclear RNA
changes in recovered nuclei; it is not a direct cilium-structure, Hedgehog,
viability, or editing-efficiency endpoint. I therefore used ciliary biology only
to choose within-dataset analogs, then let their observed DEG burdens in this
same postnatal NeuN+ CRISPR assay dominate the final scalar prediction.

## Sources used

- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared per-gene differential-expression Parquet:
  `training differential-expression dataset`
- Requested-target manifest:
  `single-target request for Cep83`
- Run-local dataset portrait, task bindings, measurement registry, and coverage
  summaries in `codex_runtime/pipeline`.
- Internal same-experiment interpretation corpus:
  `perturbai-july-260713-sourceguard-1773-v1`. I used its packaged Findings and
  Evidence for `Sclt1`, `Cep290`, `Ift88`, `Ift81`, `B9d1`, and `Rpgrip1l` as
  a compact interpretation of the same Perturb-seq experiment, not as an
  independent replicate.
- PubMed literature for the biological prior:
  Tanos et al. 2013, doi:10.1101/gad.207043.112, PMID 23348840;
  Joo et al. 2013, doi:10.1073/pnas.1220927110, PMID 23530209;
  Failler et al. 2014, doi:10.1016/j.ajhg.2014.05.002, PMID 24882706;
  Lo et al. 2019, doi:10.1083/jcb.201811142, PMID 31455668;
  Kumar et al. 2021, doi:10.1083/jcb.202011133, PMID 34241634.

## Computation over the declared inputs

I first read the one-column held-out manifest and confirmed that this run only
requests `Cep83`. The focal training-count CSV contains 1,674 unique visible
targets: 1,205 have `n_degs = 0`, 1,481 have `n_degs <= 1`, and the distribution
is strongly right-skewed, so a low biological prior should remain at zero unless
a held-out target has a close high-response analog.

To avoid using file order as evidence, I queried biologically chosen visible
ciliogenesis perturbations directly and counted their supplied focal
`n_degs`. I then filtered the Parquet by `gene_target` and
`group_name == "151 TH Prkcd Grin2c Glut"` to read the actual per-gene rows for
those analogs:

```python
dataset = pyarrow.dataset.dataset(parquet_path, format="parquet")
rows = dataset.to_table(
    filter=(pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
           & pc.field("gene_target").isin(targets),
    columns=["names", "gene_target", "logfoldchanges",
             "pvals_adj", "scores", "n_pert_matched"]
)
```

The relevant focal-cell analogs were flat or nearly flat:

| visible perturbation | mechanistic relationship to CEP83 | focal `n_degs` |
| --- | --- | ---: |
| `Sclt1` | direct distal-appendage component recruited downstream of CEP83 | 0 |
| `Kiz` | extended distal-appendage protein in the CEP83/SCLT1 assembly map | 0 |
| `Cplane1` | ciliogenesis-planar-cell-polarity effector | 0 |
| `Tbc1d32` | OFD ciliogenesis/transition-zone gene compared with SCLT1 | 0 |
| `Pibf1` | ciliogenesis/centriolar-satellite comparator in the SCLT1 report | 0 |
| `Cep290` | transition-zone ciliopathy component | 0 |
| `Rpgrip1l` | transition-zone ciliopathy component | 0 |
| `B9d1` | B9/MKS transition-zone component | 0 |
| `Bbs5` | BBSome ciliary-cargo trafficking component | 0 |
| `Ift88` | core IFT-B ciliogenesis component | 0 |
| `Ift81` | IFT-B tubulin-transport component | 0 |
| `Ift43` | IFT-A component | 0 |
| `Kif3b` | kinesin-II anterograde IFT motor subunit | 0 |
| `Dync2h1` | dynein-2 retrograde IFT motor subunit | 0 |
| `Dync2i1` | dynein-2 retrograde IFT component | 0 |
| `Arl3` | ciliary GTPase; only `Arl3` itself passed FDR | 1 |
| `Ttc8` | BBSome component; only `Ttc8` itself passed FDR | 1 |
| `Adcy3`, `Htr6`, `Gpr161`, `Mchr1` | neuronal ciliary signaling/cargo genes | all 0 |
| `Ptch1`, `Ptch2`, `Smo`, `Gli1`, `Gli2` | Hedgehog-pathway genes | all 0 |

For the closest analog, `Sclt1`, there were 122 matched perturbed nuclei and no
focal gene reached FDR 0.05; even the best focal row had adjusted `p = 1.0`.
`Kiz`, `Cplane1`, `Tbc1d32`, `Pibf1`, `Cep290`, `Rpgrip1l`, `B9d1`, `Ift88`,
`Ift81`, `Ift43`, `Kif3b`, and the dynein-2 perturbations likewise had no
focal-cell significant downstream signature. Across all neuronal groups in the
Parquet, the same analog family stayed sparse: among the selected canonical
cilium genes only `B9d1` had more than two FDR 0.05 hits in any group, with
9 genes in `308 CB GABA`; the focal cell remained zero for `B9d1`.

The July same-experiment corpus agrees with these direct counts at the
interpretive level. Its `Sclt1` report describes no Hedgehog, cilium-gene, UPR,
ISR, or immediate-early transcriptional program after acute `Sclt1` loss, and
its comparator evidence records that represented ciliary perturbations
including `Kiz`, `Cplane1`, `Tbc1d32`, `Cep290`, `Pibf1`, `Ift43`, `Ift81`,
`Ift88`, and `Bbs5` were flat or singleton-only. The `Cep290`, `Rpgrip1l`,
`Ift81`, and `Ift88` reports similarly interpret the screen as a postnatal
neuronal buffering of ciliary, transition-zone, IFT, and Hedgehog perturbations
at the nuclear RNA level.

## Target-specific reasoning

### Cep83

`CEP83` is a core centriolar distal-appendage component, previously called
`CCDC41`. Tanos et al. placed CEP83 at the top of the distal-appendage assembly
hierarchy: CEP83 recruits SCLT1 and CEP89, SCLT1 then supports CEP164 and FBF1,
and loss of CEP83 blocks ciliary vesicle docking, TTBK2 recruitment, and CP110
removal during cilia initiation. Joo et al. independently showed that CCDC41 is
needed for ciliary-vesicle docking and IFT20 recruitment to the centrosome.
Lo et al. later identified CEP83 as a TTBK2 substrate required downstream of
CEP164-dependent TTBK2 recruitment. Human genetics also supports CEP83 as a
ciliopathy gene: Failler et al. found biallelic CEP83 mutations in infantile
nephronophthisis with central nervous system findings.

The immediate intervention-to-readout chain is therefore:

1. AAV CRISPR loss of `Cep83` should impair a distal-appendage scaffolding
   function at the mother centriole.
2. That can block ciliary-vesicle docking and early ciliogenesis, a structural
   organelle consequence.
3. In embryonic or strongly Hedgehog-dependent contexts this would propagate
   through ciliary signaling pathways and alter GLI/PTCH transcription.
4. In the present experiment, the intervention occurs at P16 in sparse
   postmitotic neurons and is measured 3-4 weeks later only in recovered NeuN+
   nuclei.
5. The requested endpoint is a count of nuclear DEGs in thalamic glutamatergic
   cells, so a ciliary morphology defect only matters here if it induces a
   stable RNA program in that recovered focal population.

The visible perturbations argue that this propagation step is usually absent in
this assay. `Sclt1` is the most informative analog because it is directly below
`Cep83` in the distal-appendage hierarchy; it produced `n_degs = 0` in
`151 TH Prkcd Grin2c Glut`. The screen did not include `Cep164`, `Cep89`,
`Fbf1`, or `Ttbk2`, but `Kiz`, another distal-appendage comparator, was also
0 in the focal cell. Moving from distal appendages to the ciliary gate and
trafficking machinery did not reveal a counterexample: `Cep290`, `Rpgrip1l`,
`B9d1`, `Bbs5`, `Ift88`, `Ift81`, `Ift43`, `Kif3b`, `Dync2h1`, and `Dync2i1`
were all focal zeroes; `Arl3` and `Ttc8` reached one gene each and those were
their self-target transcripts. Direct Hedgehog perturbations were also zero
for `Gli1`, `Gli2`, `Ptch1`, `Ptch2`, and `Smo`.

Those are not perfect phenocopies of `Cep83`, because a distal-appendage root
protein is earlier than transition-zone and IFT components, and the strongest
CEP83 structural biology comes from cultured cells or developmental disease
contexts rather than P16 thalamic neurons. Still, the same-experiment negative
controls span the route by which a CEP83 lesion would have to reach the
requested endpoint: ciliary-vesicle docking, transition-zone gating, IFT
transport, BBSome cargo handling, ciliary GPCRs, and GLI/PTCH transcription all
failed to produce a broad focal nuclear RNA response. The focal training counts
therefore give no reason to assign even a small positive DEG burden to held-out
`Cep83`.

**Prediction:** `Cep83` -> `0` DEGs.

## Limits and uncertainty

- `Cep83` itself is held out, so the prediction is transferred from analogs,
  not observed.
- The best same-complex analog is `Sclt1`; other core distal-appendage genes
  (`Cep164`, `Cep89`, `Fbf1`, `Ttbk2`) were absent from the visible
  perturbation list, so the most exact biochemical controls are incomplete.
- A zero snRNA-seq DEG count does not mean normal primary cilia. The dataset
  lacks ciliary imaging, ciliary cargo localization, DNA-indel calls, and protein
  measurements, and acute mosaic postnatal editing could miss developmental
  phenotypes seen in germline ciliopathies.
- The final integer is most strongly driven by within-dataset evidence from the
  cilium perturbations' focal DEG counts. External PubMed evidence was used to
  establish that those perturbations are mechanistically appropriate analogs
  and to keep the cilium-to-RNA propagation step explicit.
