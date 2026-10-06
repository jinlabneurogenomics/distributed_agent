# DEG-count prediction for Ap2m1 in `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The held-out target list for this run contains one perturbation, `Ap2m1`. I
interpreted `n_degs` exactly as the prompt defined it: in the focal `151 TH
Prkcd Grin2c Glut` thalamic glutamatergic class, count all measured genes with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`, including the targeted
gene's own transcript if it passes. I treated the training count CSV as the
authoritative endpoint for non-held-out targets and the parquet as the
authoritative per-gene evidence for the same perturbations.

The main ambiguity I resolved was whether a pure self-transcript hit should
count as a nonzero response. It should: the provided endpoint does not exclude
the perturbed gene. I therefore distinguish "no downstream program" from
"zero DEGs"; several relevant training perturbations have `n_degs = 1` solely
because their target transcript is significant.

## Sources used

- Input focal DEG-count training CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 012_Ap2m1.csv]`.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`.
  - High-confidence claim `claim:491c5c6eb002662cbefd`: `Cltc` produced a
    cell-type-restricted coated-vesicle response that was not phenocopied by
    AP-adaptor, APP-linked, `Dnm1`, `Synj1`, Bin1-like, or other
    presynaptic/endocytic perturbations.
  - Moderate-confidence claim `claim:97fd9a4f6d91daf7bdbb`: focal responses to
    represented AP-adaptor perturbations were target-specific rather than a
    generic AP-family or clathrin-adjacent signature.
  - High-confidence claim `claim:f48dd8852b94eb3b98e0`: acute sparse
    perturbation of presynaptic endocytic `Dnm1` and `Synj1` can leave neuronal
    nuclear downstream transcriptional programs undetectably flat by
    FDR-based snRNA-seq.
  - AP-family finding cards for `Ap1b1`, `Ap1s2`, `Ap3b1`, and `Ap4s1`, which
    report broad buffering of AP-1/AP-3/AP-4 perturbations and lack of
    transfer among AP-family signatures.
- External literature for the AP-2 mechanism:
  - Kim and Ryan 2009, J Neurosci, DOI `10.1523/JNEUROSCI.5639-08.2009`,
    PMID `19321783`: shRNA depletion of neuronal AP-2 slowed but did not
    abolish synaptic-vesicle protein endocytosis, with AP-1 able to compensate.
  - Kononenko et al. 2014, Neuron, DOI `10.1016/j.neuron.2014.05.007`,
    PMID `24908483`: clathrin/AP-2 supports synaptic-vesicle reformation from
    endosome-like vacuoles at central synapses but is not the sole route of
    membrane retrieval.
  - Candiello et al. 2017, Sci Rep, DOI `10.1038/s41598-017-16055-4`,
    PMID `29150658`: synaptic AP-2/clathrin coated-vesicle uncoating is
    dynamically regulated, including by mu2/AP-2 phosphorylation, in an AP-1
    sigma1B-deficient synaptic-recycling context.

## Computation over the training dataset

I first read the manifest and verified it contains only `Ap2m1`. I then used
the focal training count CSV to pull counts for AP-family, clathrin, APP-linked,
and synaptic/endocytic neighbors. To inspect expression-pattern evidence, I
sliced the parquet to the focal cell type and the mechanistic comparator list:

```python
import pyarrow.compute as pc
import pyarrow.dataset as ds

cell = "151 TH Prkcd Grin2c Glut"
genes = [
    "Ap1b1", "Ap1s2", "Ap3b1", "Ap4s1", "Cltc", "Dnm1", "Synj1",
    "App", "Apbb2", "Appl1", "Bin1", "Cd2ap", "Sh3kbp1", "Dnajc5",
    "Prepl", "Rab7", "Vps35", "Vps54", "Hspa5",
]
dataset = ds.dataset(TRAINING_PARQUET, format="parquet")
table = dataset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj",
        "scores", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(pc.field("group_name") == cell)
    & pc.field("gene_target").isin(genes),
)
```

I also ran the Distributed Agents runtime profile comparison on the same focal parquet
for `Ap1b1`, `Ap1s2`, `Ap3b1`, `Ap4s1`, `Cltc`, `Dnm1`, `Synj1`, `App`,
`Apbb2`, `Appl1`, `Bin1`, `Cd2ap`, `Sh3kbp1`, `Dnajc5`, and `Prepl`. This
compares signed `logfoldchanges` vectors over 17,259 shared measured genes in
`151 TH Prkcd Grin2c Glut`. Seven of the fifteen had no FDR-significant focal
features; the other eight had only 1 to 9. Across all 105 candidate pairs the
significant-program overlap coefficient was 0 wherever it was defined, so the
AP/endocytic candidates do not form a shared FDR-supported focal signature.

## Relevant observed perturbations

### AP adaptor complexes

These are the closest complex-level analogs represented in the training set.

| training target | focal `n_degs` | focal expression-pattern evidence | relevance to `Ap2m1` |
|---|---:|---|---|
| `Ap1b1` | 1 | The only FDR<0.05 gene was `Ap1b1` itself, log2FC -0.537, q = 3.99e-4; no downstream gene passed. | AP-1 beta1 is an AP adaptor subunit and clathrin-sorting neighbor. The same-experiment corpus calls `Ap1b1` broadly buffered across postnatal neuronal nuclei despite AP-1 cargo-sorting biology. |
| `Ap1s2` | 0 | No focal FDR genes; best focal q was 0.394 for `Snph`, then q = 1.0 for the next ranked genes. | Same AP-1 complex family but a neuronal sigma subunit. Corpus findings report a sparse AP1S2 surface and non-phenocopying by `Ap1b1`, `Ap3b1`, `Ap4s1`, `Cltc`, and `Dnm1`. |
| `Ap3b1` | 0 | No focal FDR genes; all top focal nominal hits had q = 1.0. | AP-3 beta3A is an adaptor for endosome/lysosome and synaptic-vesicle cargo sorting. The corpus reports every measured Ap3b1 group had 0 downstream genes at FDR<0.10 and the smallest downstream FDR was 0.428. |
| `Ap4s1` | 0 | No focal FDR genes; all top focal nominal hits had q = 1.0. | AP-4 is a TGN/endosomal adaptor with direct ATG9A trafficking biology, but the same-experiment corpus reports no downstream Ap4s1 response in any recovered neuronal group and no phenocopy by AP-family or autophagy neighbors. |

`Ap2m1` is not a paralog or subunit of the same complex as these genes, but it
occupies the same broad clathrin-adaptor design: a heterotetrameric adaptor
complex that binds cargo and helps generate coated vesicles. The focal training
data show that knocking out represented AP-family subunits did not produce a
common nuclear response in this P16-to-P37/44 CRISPR assay. The zero AP-1
sigma, AP-3, and AP-4 counts are the strongest within-dataset reason not to
predict a broad `Ap2m1` response.

The one exception, `Ap1b1`, is informative in the opposite direction: its
single focal DEG was its own depleted transcript, not a downstream
vesicle-trafficking, lysosomal, synaptic, ISR, or UPR program. Because `n_degs`
counts target RNA, this makes 1 a plausible AP-adaptor endpoint even when the
functional program is otherwise flat.

### Clathrin and plasma-membrane synaptic endocytosis

I kept `Cltc` as the candidate returned by the Distributed Agents `common_outbound_neighbors`
query for `Ap1b1`, `Ap1s2`, `Ap3b1`, and `Ap4s1`. Its mechanistic relevance is
clear: AP-2 works with clathrin in coated pits, and `Cltc` is the core coat
heavy chain. Its task-matched observed similarity is weak, however. In the
focal cell group `Cltc` had only 3 significant genes (`Gabra4`, `Rbms1`,
`Ero1b`, all down; q = 0.042), and pairwise focal comparisons between `Cltc`
and each represented AP target had zero significant-gene overlap. The
Pearson correlations of full logFC vectors were modest (`0.62` with `Ap1b1`,
`0.62` with `Ap1s2`, `0.65` with `Ap3b1`, `0.62` with `Ap4s1`) and arose from
low-level same-direction background rather than from shared FDR genes. I
therefore used `Cltc` as an upper-bound counterexample, not as a numeric
template.

The most direct plasma-membrane/synaptic endocytic neighbors were also
near-flat:

| training target | focal `n_degs` | focal expression-pattern evidence | interpretation |
|---|---:|---|---|
| `Dnm1` | 1 | Only `Dnm1` itself passed q < 0.05, log2FC -0.712, q = 4.09e-25. | Dynamin participates in vesicle fission. Its self-only response argues that even strong presynaptic-endocytic perturbations need not trigger a nuclear compensation program here. |
| `Synj1` | 1 | Only `Synj1` itself passed, log2FC -0.583, q = 3.11e-7. | Synaptojanin acts in post-endocytic uncoating; the self-only focal response matches the corpus claim that Dnm1/Synj1 perturbations can be FDR-flat downstream. |
| `Bin1` | 1 | Only `Bin1` itself passed, q = 3.0e-6. | BAR-domain/clathrin-adjacent endocytosis factor; another self-only, non-convergent neighbor. |
| `Cd2ap` | 0 | No focal FDR genes. | Endocytic/scaffold neighbor; null. |
| `Sh3kbp1` | 0 | No focal FDR genes. | Cbl-interacting CIN85 family adaptor; null. |
| `Dnajc5` | 1 | Only `Dnajc5` itself passed, q = 0.010. | Presynaptic vesicle chaperone; self-only. |
| `Prepl` | 1 | Only `Prepl` itself passed, q = 7.77e-10. | Clathrin-uncoating-linked PREPL perturbation; self-only in the focal group. |

External neuronal work is compatible with this transfer. AP-2, including the
mu2 subunit encoded by `AP2M1`/`Ap2m1`, is a central clathrin adaptor for
cargo recognition during endocytosis. But AP-2 depletion in primary neurons
slowed rather than eliminated synaptic-vesicle cargo endocytosis, and AP-1
could partially substitute (Kim and Ryan 2009). Conditional loss of AP-2 at
central synapses caused defects in synaptic-vesicle reformation and accumulation
of endosome-like vacuoles but left clathrin-independent membrane retrieval
available (Kononenko et al. 2014). These studies make a synaptic physiology or
vesicle-reformation phenotype plausible, but they do not imply a broad soma
nuclear mRNA program under the sparse postnatal CRISPR design used here.

### Endolysosomal counterexamples

Late-endosomal and retrograde-trafficking nodes establish that the focal assay
can detect large vesicle/lysosome-adjacent states when the perturbation reaches
the relevant stress axis:

- `Rab7`: 501 focal DEGs, with lysosomal/vATPase/autophagy-associated genes
  such as `Atp6v1b2`, `Dpp7`, `Scpep1`, `Atp6v0b`, `Lamp2`, and sterol genes
  among the most significant.
- `Vps35`: 17 focal DEGs, including `Atp2a2`, `Brsk1`, `Grin2b`, `Ccdc136`,
  and the `Vps35` self transcript.
- `Vps54`: 31 focal DEGs, including `Egr1`, `Jun`, `Stmn4`, `Atp2a2`, and
  cytoskeletal genes.

I treated these as counterexamples, not analogs. AP-2 is a plasma-membrane
clathrin adaptor and AP2M1 loss should perturb cargo selection and synaptic
vesicle reformation upstream of late endosome/lysosome fusion. The AP-3 corpus
contrast is especially useful here: `Rab7`, `Vps41`, and vATPase/autophagy
perturbations could produce nonzero lysosomal signatures, while the earlier
AP-3 cargo adaptor `Ap3b1` stayed flat. By the same logic, `Ap2m1` should not
be assigned a `Rab7`-like or even `Vps35`/`Vps54`-like DEG burden simply
because it affects membrane traffic.

## Target-specific call

`Ap2m1` encodes the AP-2 mu subunit. Mechanistically, it is a more direct
clathrin-mediated endocytosis target than AP-1/AP-3/AP-4, and AP-2/clathrin
participates in synaptic-vesicle protein retrieval and vesicle reformation.
That pushed the prediction above a hard structural null for an unrelated
trafficking gene.

The within-dataset calibration still argues for a very small endpoint:

- represented AP-adaptor perturbations were 0, 0, 0, and 1 DEG in the focal
  cell group, with the `Ap1b1` count explained by `Ap1b1` self-RNA only;
- the strongest mechanistic clathrin neighbor, `Cltc`, had only 3 focal DEGs
  and did not share them with AP-family targets;
- the immediate synaptic endocytic nodes `Dnm1` and `Synj1` were self-only;
- the same-experiment corpus explicitly rejects a generic AP-family or
  clathrin-adjacent focal transcriptomic signature.

The endpoint includes the knocked-down transcript, and several high-confidence
endocytic neighbors reached `n_degs = 1` entirely through their self-transcript.
I therefore predict a single significant gene for `Ap2m1`, most likely `Ap2m1`
itself, and no multi-gene downstream AP-2 response in `151 TH Prkcd Grin2c
Glut`.

Final point prediction:

| target_name | predicted_n_degs |
|---|---:|
| `Ap2m1` | 1 |

## Limits

- The strongest limitation is that `Ap2m1` itself and other AP-2 subunits were
  held out or absent, so the transfer is from AP-1/AP-3/AP-4 and nearby
  endocytic machinery rather than from a same-complex AP-2 perturbation.
- The training analogs have variable recovered focal perturbed-cell counts
  (`Cltc` had only 32 nuclei; AP-family comparators ranged from 85 to 143 in
  the focal parquet slice), and a borderline few-gene response can move across
  the FDR threshold with power.
- Whole-profile correlations among nearly flat targets are dominated by
  small same-direction background and are not mechanistic evidence; I used the
  FDR-level gene identities and the corpus findings rather than nearest-null
  rankings as the primary evidence.
- External AP-2 studies measured protein localization, endocytosis kinetics,
  synaptic ultrastructure, or Drosophila/human developmental disease
  phenotypes, not juvenile sparse mouse snRNA-seq. They support the biological
  placement of AP2M1 in endocytosis but do not provide a quantitative DEG count
  for this assay.
- Predicting exactly 1 rather than 0 is an extrapolation from the tendency of
  focal endocytic neighbors to pass by self-transcript only. If the Ap2m1 gRNA
  pool did not reduce nuclear Ap2m1 RNA enough in recovered cells, the same
  mechanistic reasoning would instead produce a zero count.
