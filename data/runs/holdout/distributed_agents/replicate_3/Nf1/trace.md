# Nf1 DEG-count prediction trace

## Question and interpretation

The requested manifest contains one held-out perturbation, `Nf1`. I interpreted the
endpoint as the exact training endpoint used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of genes in the
`151 TH Prkcd Grin2c Glut` Wilcoxon result with `pvals_adj < 0.05`. Because
`Nf1` is completely absent from both the parquet and the training count CSV, I
did not use any direct `Nf1` DEG count or signature. The count below is a point
prediction for the same sparse P16 AAV CRISPR, P37-P44 NeuN+ snRNA-seq assay,
not a prediction of germline phenotypic severity or of protein/phospho pathway
activity.

## Sources used

- Supplied training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Supplied all-cell differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest:
  `[local file: 148_Nf1.csv]`
- Distributed Agents corpus, release `perturbai-july-260713-sourceguard-1773-v1`.
  `target_context(Nf1)` had no released Nf1 records under the holdout policy, so
  I used corpus contexts for assayed comparator genes including `Braf`,
  `Spred1`, `Syngap1`, `Depdc5`, and `Tsc2`.
- PubMed literature for external mechanism:
  Bollag et al. 1993, EMBO J, DOI `10.1002/j.1460-2075.1993.tb05841.x`,
  showed that full-length neurofibromin has Ras-GAP activity.
  Stowe et al. 2012, Genes Dev, DOI `10.1101/gad.190876.112`, showed that
  SPRED1 recruits neurofibromin to the plasma membrane to down-regulate
  Ras-GTP.
  Johannessen et al. 2005, PNAS, DOI `10.1073/pnas.0503224102`, showed that
  NF1 loss can constitutively activate PI3K-AKT-TSC2-mTOR signaling.
  Costa et al. 2002, Nature, DOI `10.1038/nature711`, connected Nf1
  haploinsufficiency, excess Ras function, altered inhibition, and learning
  defects in mice.
  Bar-Peled et al. 2013, Science, DOI `10.1126/science.1232044`, identified
  DEPDC5/NPRL2/NPRL3 GATOR1 as a Rag-GAP brake on mTORC1.

## Dataset computations

I first confirmed that the requested list is only `Nf1` and that `Nf1` is absent
from the training endpoint and from the parquet's `gene_target` column. The
training endpoint is sparse in this focal cell group: among 1,674 training
perturbations the median `n_degs` is 0, only 469 are nonzero, and the 95th
percentile is 18.

For pathway calibration I filtered the parquet to `151 TH Prkcd Grin2c Glut`
and counted `pvals_adj < 0.05` for Ras/MAPK, SPRED, RasGAP, PI3K, mTOR, and
synaptic Ras/Rap-GAP candidates that were actually assayed:

```python
import pyarrow.dataset as ds

dset = ds.dataset(training_parquet, format="parquet")
filt = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(targets)
)
tbl = dset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj"],
    filter=filt,
)
```

The relevant observed focal counts were:

| class | target | `n_degs` | interpretation for Nf1 |
| --- | ---: | ---: | --- |
| NF1-adjacent Ras brakes | `Spred1`, `Spred2` | 0, 0 | Same sign for Ras/MAPK release but single SPRED loss was completely buffered |
| NF1-adjacent Ras/Rap GAPs | `Rasa2`, `Syngap1` | 0, 0 | Same sign or overlapping biochemical logic, but no nuclear RNA response |
| Ras/MAPK positive branch | `Braf`, `Map2k1`, `Shoc2`, `Ntrk2` | 4, 4, 1, 3 | Downstream or receptor/scaffold loss exposes only a tiny thalamic ERK-output module |
| Other Ras/MAPK positives | `Hras`, `Kras`, `Raf1`, `Map2k2`, `Mapk1`, `Ptpn11`, `Sos1` | all 0 | Most single upstream/core pathway losses are silent |
| mTORC1 release | `Depdc5`, `Tsc2` | 13, 86 | Same sign for mTORC1 disinhibition, but much more direct than NF1-to-PI3K/mTOR |
| mTORC1 or PI3K positives | `Mtor`, `Rptor`, `Pik3r1`, `Akt3` | 2, 0, 0, 0 | Positive core/upstream perturbations did not produce a reciprocal module |

The most interpretable expression-pattern evidence was local rather than
whole-transcriptome similarity:

- `Braf` had four significant focal genes: `Atp2a2`, `Ptpn5`, `Vgf`, and
  `Unc13a`, all down.
- `Map2k1` also had four: `Vgf`, `Ptpn5`, `Unc13a`, and `Etv5`, all down.
- `Shoc2` had one, `Vgf` down.
- `Depdc5` had 13 and carried a sterol/PI3K-feedback branch including
  `Ldlr`, `Insig1`, `Hmgcs1`, `Pik3r1`, and `Pik3r3`.
- `Tsc2` had 86 and shared the mTORC1/sterol feedback direction, but its
  response was broader; in 151, significant genes included `Cyp51`, `Pik3r3`,
  `Slc2a6`, `Eno2`, and `Ptgds`.

I also ran a Distributed Agents runtime cohort profile over assayed Ras/Raf/ERK and
mTOR-pathway candidates. The 16-gene cohort was not a single strong expression
module: the positive top-tail overlap coefficient across the 120 within-cohort
pairs had median `0.07`, and only a few pairwise significant programs overlapped.
I therefore treated the training genes as individual analogs and counterexamples
rather than averaging them into one pathway score.

## Target-specific reasoning

### Nf1

`Nf1` encodes neurofibromin, a Ras-GTPase activating protein. NF1 loss removes a
major brake on Ras-GTP; SPRED1 normally helps recruit neurofibromin to activated
Ras at membranes, and NF1 loss can also feed through PI3K-AKT to inhibit TSC2
and activate mTORC1. That external mechanism makes `Nf1` a plausible
nonzero-response perturbation: it is more central than `Rasa2`, and it is
downstream of the potentially redundant SPRED adaptor paralogs.

The direct in-dataset evidence is much more modest:

- `Spred1` and `Spred2`, the most NF1-specific same-direction adaptor analogs
  that were assayed, both had `0` DEGs in 151. The Distributed Agents corpus summarizes
  this as a pan-measured-neuronal basal-transcriptome null for acute single
  `Spred1` loss and as reciprocal single-paralog flatness for `Spred1` and
  `Spred2`; that argues against a large basal hyper-ERK RNA program after a
  weak, sparse negative-feedback perturbation.
- `Rasa2` and `Syngap1` were also `0`. `Syngap1` is synaptic rather than a
  direct substitute for neurofibromin, but its null focal response is a useful
  warning that Ras/Rap-GAP loss can displace to synaptic physiology or local
  signaling without yielding FDR-level nuclear mRNA changes.
- The ERK positive branch was detectable but tiny. `Braf` and `Map2k1` each had
  exactly `4` DEGs and converged on down-regulation of `Vgf`, `Ptpn5`, and
  `Unc13a`; `Shoc2` shared only `Vgf` with `1` DEG. Because these are positive
  RAF/MEK branch losses, their direction is opposite of the expected ERK effect
  of `Nf1` loss, but their small counts calibrate how little of basal ERK flux
  appears at FDR 0.05 in this assay.
- The mTORC1 branch supplies the main nonzero same-direction counterexample:
  `Depdc5` loss produced `13` DEGs and `Tsc2` loss produced `86`. The corpus
  reports that `Depdc5` and `Tsc2` converge in 151 on an mTORC1 sterol/PI3K
  feedback module, while positive or upstream PI3K/mTOR nodes such as `Mtor`,
  `Rptor`, `Pik3r1`, and `Akt3` are flat or tiny. `Nf1` can activate mTORC1
  through Ras/PI3K/TSC2, but that route is indirect compared with removing
  `Tsc2` or the GATOR1 subunit `Depdc5`, so I used them as an upper-bound
  positive analog rather than as equal-weight phenocopies.

The zero/nonzero decision was therefore close. A zero would be credible from the
training data alone because every measured single negative Ras regulator was
FDR-silent. I still assigned a weak nonzero because neurofibromin sits at the
convergence point for SPRED-dependent membrane recruitment and intrinsic Ras-GAP
activity, and because the 151 cell group can register both a small ERK-output
program (`Braf`/`Map2k1`) and a modest same-direction mTORC1-release program
(`Depdc5`). I placed `Nf1` at `4` DEGs: comparable to the direct BRAF/MEK
branch, above the `Spred1`/`Spred2`/`Rasa2` nulls, below `Depdc5`, and far below
the direct `Tsc2` release.

## Limits

No held-out `Nf1` rows were available in either supplied dataset, and the
Distributed Agents corpus intentionally had no `Nf1` target context under this holdout.
The prediction extrapolates from incomplete Ras-pathway coverage: `Nras`,
`Rasa1`, `Rasa3`, `Tsc1`, `Rheb`, `Nprl2`, and `Nprl3` were not observed focal
training perturbations. All comparisons are transcriptomic; this experiment did
not measure Ras-GTP, phospho-ERK, phospho-S6, translation, cell size, synaptic
physiology, or evoked pathway responses. Germline NF1, tumor, and developmental
RASopathy literature establishes the direction of pathway wiring, but it is an
imperfect guide to mosaic, partial, postmitotic P16 CRISPR loss in juvenile
neurons. The final integer should therefore be read as a low-count calibrated
guess, not as evidence that NF1 biology is intrinsically weak.
