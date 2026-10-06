# Glmn DEG-count prediction

## Question and interpretation

The requested held-out target file contains one mouse perturbation, `Glmn`. I
interpreted the task as a point prediction of

`n_degs = count(pvals_adj < 0.05)`

in the `151 TH Prkcd Grin2c Glut` focal cell group after acute P16 AAV-CRISPR
loss of function, using only non-held-out perturbations for calibration. The
count is an assay endpoint: it may include the perturbed target transcript
itself if that transcript is an adjusted-significant row, and zero means "no
measured gene passes the BH-adjusted Wilcoxon cutoff", not that editing or
protein function had no effect.

## Sources used

- Training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training differential-expression rows:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested-target manifest:
  `[local file: 092_Glmn.csv]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`.
- Distributed Agents runtime profile comparison on the focal `151 TH Prkcd Grin2c Glut`
  signed log-fold-change profiles for candidate ubiquitin/SCF/FKBP/IAP
  perturbations.
- PubMed literature on GLMN/glomulin, cullin-RING ligase regulation,
  glomuvenous malformations, and inflammasome regulation.

The Distributed Agents corpus had no direct `Glmn` target context and no lexical `Glmn`
claims, consistent with `Glmn` being completely held out. I therefore used the
corpus only for same-experiment interpretation of observed analogs such as
`Fbxw7` and `Fbxo11`.

## Computation over the supplied training data

The training count table has 1,674 non-held-out perturbations. In the focal
cell group it is sparse: 1,205/1,674 perturbations have 0 DEGs, 363 have 1-9
DEGs, 63 have 10-99, and 43 have at least 100. The exact smallest nonzero
bin is heavily concentrated at one DEG: 276 targets have exactly `n_degs = 1`.

I queried the focal-cell DE parquet for mechanistic candidates with a PyArrow
dataset filter rather than reading the full all-cell parquet:

```python
filt = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(candidate_targets)
)
table = ds.dataset(path, format="parquet").to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals", "pvals_adj",
        "scores", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=filt,
)
```

`Rbx1`, `Rbx2`/`Rnf7`, `Cul1`, `Cul7`, `Skp1`, `Fbxw8`, `Birc2`, `Birc3`,
`Fkbp1b`, and `Fkbp5` were not present in the training endpoint table, so the
most direct GLMN-bound cullin-RING complex members could not be used as
observed perturbation anchors. The relevant observed anchors and
counterexamples were:

| training perturbation | observed `n_degs` | focal expression evidence | relevance to `Glmn` |
|---|---:|---|---|
| `Fbxw7` | 1 | the only adjusted-significant gene was `Trp53inp2` up, log2FC 0.485, BH 0.045; Distributed Agents corpus reports this as a single-gene 151 TH Prkcd response with no broad canonical FBXW7 substrate-output module | strongest available within-dataset analog, because GLMN inhibits RBX1-containing CRL/SCF ligases and `Fbxw7` is the CRL1 substrate receptor whose protein stability is regulated by GLMN |
| `Fbxo11` | 1 | the only adjusted-significant gene was `Ppib` down, log2FC -0.553, BH 0.032; the Distributed Agents corpus summarizes `Fbxo11` as buffered with only this Ppib call in the same focal group | F-box/SCF-family perturbation showing that another receptor in the same broad ubiquitin-ligase architecture gives only a singleton response |
| `Fbxo38` | 0 | no BH<0.05 genes; best BH value was 0.290 | F-box-family counterexample, mechanistically much less direct than `Fbxw7` but useful against treating "F-box related" as sufficient for a large response |
| `Fkbp1a` | 1 | the only significant gene was the target itself, `Fkbp1a` down, log2FC -1.189, BH 5.25e-10 | weak GLMN-binder-axis analog: FKBP12/FKBP1A binds GLMN more weakly than FKBP12.6 and FKBP51 in vitro, and `Fkbp1b`/`Fkbp5` were absent |
| `Xiap` | 0 | no BH<0.05 genes; best BH value was 0.303 | IAP-family boundary. GLMN regulates cIAP1/BIRC2 and cIAP2/BIRC3 in macrophage inflammasomes, not XIAP specifically, and inflammatory macrophage pyroptosis is not expected to dominate NeuN-enriched neurons |
| `Ube2e2` | 0 | no BH<0.05 genes | generic ubiquitin E2 counterexample; not the CDC34/RBX1 interface itself |
| `Usp48` | 10 | ten genes reached BH<0.05, led by `Abhd12b`, `Cyp46a1`, `Resp18`, `Galk2`, and `Msrb2` | boundary for a small but nonzero distal ubiquitin-system response |
| `Psmb4` | 742 | broad proteasome-subunit response | positive control that this cell group can show hundreds of DEGs after direct core proteasome damage |
| `Psmc1` | 430 | broad proteasome-subunit response; Distributed Agents corpus links proteasome-subunit perturbation to an HSF1/chaperone stress program | positive control, but biologically a poor `Glmn` analog because GLMN modulates RING/E2 access rather than destroying the proteasome |

The Distributed Agents runtime profile comparison over `Fbxw7`, `Fbxo11`, `Fbxo38`,
`Fkbp1a`, `Xiap`, `Ube2e2`, and `Usp48` confirmed that this candidate set lives
at the null-to-weak edge of the focal assay: three of these seven had no
significant feature, three had 1-9 significant features, and only `Usp48` was in
the 10-49 bin. The selected adjusted-significant calls did not form a recurrent
shared DEG set.

## Biology of the held-out target

GLMN/glomulin was identified as the causal gene for inherited glomuvenous
malformations; patient genetics and two-hit lesions support loss of function as
the disease mechanism (Brouillard et al., 2002, doi:10.1086/339492, PMID
11845407). Mouse in situ hybridization showed prominent vascular smooth-muscle
expression in development and adult tissue, explaining why the classic phenotype
is vascular rather than neuronal (McIntyre et al., 2004,
doi:10.1016/j.modgep.2003.09.007, PMID 15053987). That external biology argues
against importing a vascular malformation signature into this NeuN-enriched,
postmitotic neuronal assay.

Biochemically, GLMN is tied to cullin-RING ubiquitin ligases. Arai et al. found
glomulin/FAP68 in a CUL7-SKP1-RBX1-FBX29 complex involved in vascular
morphogenesis (2003, doi:10.1073/pnas.1733908100, PMID 12904573). Tron et al.
showed that GLMN binds RBX1, inhibits its E3 ligase activity, and regulates
CRL1(FBW7)-mediated turnover of FBW7; GLMN loss decreases FBW7 protein and
increases cyclin E and c-MYC protein abundance in their cell systems (2012,
doi:10.1016/j.molcel.2012.02.005, PMID 22405651). Duda et al. solved the
GLMN-RBX1-CUL1 structure and showed that GLMN blocks the E2-binding face of
RBX1-containing CRLs (2012, doi:10.1016/j.molcel.2012.05.044, PMID 22748924).
The direction of GLMN loss is therefore not equivalent to simply knocking out a
core cullin or proteasome subunit; it is a regulator of the ligase/E2 interface,
and in the FBW7 case the downstream consequence is largely post-translational.

Other GLMN mechanisms map poorly to the experiment. Suzuki et al. showed that
GLMN can repress cIAP-dependent inflammasome activation and Shigella-induced
macrophage pyroptosis (2014, doi:10.1073/pnas.1324021111, PMID 25246571; 2017,
doi:10.15252/embr.201643841, PMID 29191979). Those data are in innate immune
cells and use cIAP1/2, which were not assayed here; the represented IAP-family
target `Xiap` was transcriptionally flat. Haehle et al. found FKBP51 and
FKBP12.6 to be tighter GLMN interactors than FKBP12 in vitro (2019,
doi:10.1371/journal.pone.0221926, PMID 31490997); the only represented FKBP
gene, `Fkbp1a`, produced no downstream signature beyond its own transcript.

## Target-specific prediction

`Glmn`: predicted `n_degs = 1`.

This is driven mostly by within-dataset evidence from `Fbxw7`, with `Fbxo11`,
`Fbxo38`, `Fkbp1a`, `Xiap`, and `Ube2e2` as weak/boundary counterexamples.
`Fbxw7` is the most biologically direct observed node because GLMN controls
RBX1/CRL1(FBW7) activity and FBW7 turnover; its loss in the same focal group
produced just one BH<0.05 gene. The Distributed Agents same-experiment corpus further
records that acute `Fbxw7` loss did not recover broad MYC/cyclin-E, Notch,
mTOR/SREBP, or proteasome-output transcriptional programs. The two other
observed F-box perturbations were similarly tiny (`Fbxo11` at one DEG,
`Fbxo38` at zero), and the FKBP and IAP-adjacent observations did not reveal a
hidden larger program. Core proteasome targets such as `Psmb4` and `Psmc1` show
that the assay can detect broad proteostasis stress, but they are too far
downstream and too disruptive to set the expectation for GLMN.

I therefore expect acute `Glmn` perturbation in postmitotic TH/Prkcd/Grin2c
glutamatergic neurons to sit just above the zero boundary, most plausibly with
only the target itself or one CRL/FBW7-adjacent secondary transcript crossing
FDR. The one-DEG prediction rounds toward the direct `Fbxw7` analog and away
from the large proteasome-subunit positives.

## Limits and extrapolation

The strongest limitation is missing coverage of the actual GLMN complex:
`Rbx1`, `Cul1`, `Cul7`, `Skp1`, `Fbxw8`, `Fkbp1b`, `Fkbp5`, `Birc2`, and `Birc3`
were absent from the training endpoint table. `Fbxw7` is direct but downstream
of only one GLMN-controlled CRL branch, while `Fbxo11` and `Fbxo38` are
same-family rather than same-complex comparisons. The external literature
mostly comes from vascular, transformed-cell, structural-biochemistry, plant,
or macrophage-infection systems, not P16-P44 postmitotic mouse neurons. Because
the assay reads nuclear RNA 3-4 weeks after sparse CRISPR and not protein
stability, E3-substrate turnover, cullin neddylation, or inflammasome activity,
the final count is an extrapolation from a weak SCF/FBW7 mRNA footprint rather
than a directly observed GLMN-like signature.
