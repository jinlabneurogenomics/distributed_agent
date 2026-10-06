# DEG-count prediction trace

## Question and endpoint

The requested output is one integer prediction for each held-out perturbation in
`151 TH Prkcd Grin2c Glut` cells.  I treated `n_degs` as exactly the focal-cell
count of measured genes with `pvals_adj < 0.05` after Benjamini-Hochberg
correction in the supplied Wilcoxon differential-expression table.

There was one requested held-out target:

- `Vps13d`

`Vps13d` is absent from the supplied training differential-expression parquet and
from the supplied training count CSV, so there is no direct same-experiment
signature or DEG count for the target.  The endpoint is therefore directly
observed for training perturbations only and absent for the held-out
perturbation itself.  I used the supplied focal DEG counts as the quantitative
calibration target and used the parquet to inspect expression patterns of
visible mechanistic comparators in the same `151 TH Prkcd Grin2c Glut` readout.

## Sources used

- Declared input count table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
  This has 1,674 non-held-out perturbations; 1,205 have zero focal DEGs, 469
  have at least one DEG, the median is 0, the mean is 14.05, and the maximum is
  2,677.
- Declared input differential-expression parquet:
  `training differential-expression dataset`.
  I filtered this table to `group_name == "151 TH Prkcd Grin2c Glut"` and to
  mechanistically relevant visible targets to verify each comparator's
  `pvals_adj < 0.05` count, perturbed/control nucleus counts, and leading
  signed Wilcoxon-score pattern.
- Internal same-experiment semantic corpus:
  `perturbai-july-260713-sourceguard-1773-v1`.
  I used bounded Finding summaries for visible training targets only: `Opa1`,
  `Rab7`, `Vps35`, `Vps54`, `Atg5`, `Map1lc3a`, `Sqstm1`, and `Rhot1`.  These
  summaries describe the same PerturbAI experiment and are interpretive
  context, not independent replication.
- External literature from PubMed:
  Seong et al. 2018, Annals of Neurology, DOI `10.1002/ana.25220`;
  Baldwin et al. 2021, Journal of Cell Biology, DOI `10.1083/jcb.202001188`;
  Guillen-Samander et al. 2021, Journal of Cell Biology, DOI
  `10.1083/jcb.202010004`; Insolera et al. 2021, PLOS Genetics, DOI
  `10.1371/journal.pgen.1009731`; Shen et al. 2021, Journal of Cell Biology,
  DOI `10.1083/jcb.202104073`; Miao et al. 2025, Nature Structural &
  Molecular Biology, DOI `10.1038/s41594-025-01602-9`.

## Quantitative calibration and analog checks

The focal training endpoint is zero-inflated: most perturbations have no
FDR-significant focal genes, and even many essential organelle genes are null or
near-null in this 3-4 week, sparse postmitotic CRISPR readout.  For a held-out
gene, I therefore gave the strongest weight to visible targets that perturb the
same limiting molecular step, and only then considered broader pathway
neighbors.

For `Vps13d`, I checked these focal-cell counts and leading signatures:

| training perturbation | 151-cell `n_degs` | relevant expression evidence |
| --- | ---: | --- |
| `Vps13a` | 0 | no FDR genes; largest absolute-score loci were only subthreshold, with `Usf2` p_adj 0.896 |
| `Vps13b` | 0 | no FDR genes; `Ing4` was the smallest adjusted p-value at 0.374 |
| `Vps13c` | 0 | no FDR genes; top loci `Ptprj`, `Dbn1`, and `Eif4g2` all had p_adj 0.484 |
| `Rhot1` | 0 | no FDR genes; no Opa1-like mitochondrial ATF4/ISR program in the internal report |
| `Atg5` | 0 | no focal FDR genes and no canonical autophagy, lysosome, p62, proteasome-rebound, or UPR/ISR program in the internal report |
| `Atg16l1` | 0 | same LC3-lipidation complex as ATG5, but flat in the focal count table |
| `Lamp2` | 0 | lysosome/autophagy membrane target, flat in the focal count table |
| `Map1lc3a` | 1 | only the self transcript passed FDR in the focal cell group |
| `Sqstm1` | 1 | only the self transcript passed FDR in the focal cell group |
| `Vps41` | 0 | HOPS/Rab7 pathway neighbor, but no focal FDR genes despite weak same-direction continuous similarity to the Rab7 vector |
| `Vps35` | 17 | small retromer response led by `Atp2a2` down, `Brsk1` up, `Grin2b` down, and self down |
| `Vps54` | 31 | GARP/endosome-to-TGN response led by `Egr1` down, `Kctd16` up, `Jun` up, `Stmn4` up, `Lef1` down |
| `Opa1` | 37 | mitochondrial inner-membrane stress signature, led by `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, and `Mthfd2` induction |
| `Rab7` | 501 | strong late endosomal/lysosomal, sterol, ISR/autophagy, and neuronal-downshift state |

To ask whether the flat genes carried hidden subthreshold versions of the
positive mitochondrial or endolysosomal programs, I also compared their signed
Wilcoxon-score vectors on the union of the focal `Opa1`, `Rab7`, `Vps35`, and
`Vps54` FDR genes.  The three VPS13 paralogs had low cosine similarity to the
positive controls: 0.015-0.122 versus `Opa1`, 0.067-0.189 versus `Rab7`,
-0.016-0.081 versus `Vps35`, and 0.090-0.210 versus `Vps54`.  `Rhot1`, `Atg5`,
`Atg16l1`, `Lamp2`, `Sqstm1`, and `Map1lc3a` were similarly weak except for
`Vps41` versus the `Rab7` marker vector; importantly, `Vps41` still had no
focal genes over the FDR 0.05 endpoint threshold.  The calculation was:

```python
focal = de[
    (de.group_name == "151 TH Prkcd Grin2c Glut")
    & de.gene_target.isin(mechanistic_targets)
]
markers = focal[
    focal.gene_target.isin(["Opa1", "Rab7", "Vps35", "Vps54"])
    & (focal.pvals_adj < 0.05)
].names
score_matrix = focal[focal.names.isin(markers)].pivot(
    index="names", columns="gene_target", values="scores"
)
```

## Causal transfer for `Vps13d`

The causal chain for a `Vps13d` perturbation in this assay is:

`Vps13d` CRISPR loss of function -> loss of a large lipid-transfer protein at
ER-mitochondria and ER-peroxisome contacts -> possible defects in mitochondrial
fission, mitophagy completion, peroxisome biogenesis, and mitochondrial
distribution -> a postmitotic neuron may compensate, accumulate organelle
damage, enter an OPA1-like ATF4/ISR state, enter a Rab7-like lysosomal/sterol
state, be lost before capture, or remain transcriptionally buffered -> the
surviving NeuN-positive `151 TH Prkcd Grin2c Glut` nuclei produce the measured
FDR-significant DEGs.

External biology says that `Vps13d` is plausibly neuronal and mitochondrial:
recessive human VPS13D variants cause ataxia/spasticity with mitochondrial
defects (Seong et al. 2018); VPS13D binds Miro and VAP to bridge ER to
mitochondria and peroxisomes (Guillen-Samander et al. 2021); VPS13D loss can
impair peroxisome biogenesis in cultured cells (Baldwin et al. 2021); Drosophila
`Vps13D` is required for mitochondrial fission and mitophagy completion in
neurons (Insolera et al. 2021) and acts in a Pink1-dependent, Parkin-independent
mitophagy pathway (Shen et al. 2021).  A complete excitatory-neuron mouse
conditional knockout can also drive mitochondrial ultrastructural defects,
cGAS-STING signaling, microglial activation, and neuronal death (Miao et al.
2025).

Those data make `Opa1` and `Rab7` useful positive controls but imperfect
analogs.  `Opa1` directly impairs inner-mitochondrial membrane fusion and cristae
function and already crosses the ATF4/ISR threshold in the focal cell group with
37 DEGs.  `Rab7` directly blocks late endosomal and lysosomal traffic and causes
a much broader 501-DEG lysosomal/sterol/proteostasis state.  `Vps13d` sits at a
mitochondria/peroxisome lipid-transfer step upstream of mitochondrial quality
control rather than at the OPA1 inner-membrane lesion or the RAB7 late-endosome
hub, so transfer from either positive program is not obligate.

The most proximal assayed counterexamples point toward a subthreshold outcome.
All three assayed VPS13-family perturbations, `Vps13a`, `Vps13b`, and `Vps13c`,
were focal zeros.  They are paralogs rather than identical organelle-contact
proteins, so they cannot prove `Vps13d` will be silent, but they show that this
large lipid-channel family did not generically elicit a thalamic nuclear stress
response.  `Rhot1`, the Miro protein that recruits VPS13D to mitochondria, was
also zero and was explicitly uncoupled from the OPA1-like mitochondrial
ATF4/ISR program in the internal corpus.  Core autophagy and selective
autophagy readouts were buffered as well: `Atg5`, `Atg16l1`, and `Lamp2` had 0
focal DEGs, while `Map1lc3a` and `Sqstm1` had only their own transcript as the
single significant focal hit.  Thus the same intervention chain that should
connect VPS13D to mitophagy does not, in this dataset, reliably propagate to a
detectable `151`-cell nuclear response when perturbed at Miro, ATG5/ATG16L1,
LC3A, p62, or LAMP2.

Broader endomembrane positives do not overcome that local evidence.  `Vps35`
and `Vps54` show that the focal class can respond to retromer and GARP lesions,
but the internal reports emphasized branch specificity: `Vps35l`/Retriever and
`Washc4` failed to phenocopy `Vps35`, and the `Vps54` partner `Vps53` remained
below the FDR-scale phenotype.  These splits argue against promoting `Vps13d`
just because it is an endomembrane lipid-transfer gene.

## Prediction

I predict `Vps13d` will have no genes passing the focal FDR 0.05 threshold:

- `Vps13d`: `0` predicted DEGs.

This is driven primarily by within-dataset evidence from `Vps13a/b/c`,
`Rhot1`, `Atg5`, `Atg16l1`, `Lamp2`, `Map1lc3a`, and `Sqstm1`.  External
knowledge moves the target from an arbitrary zero-inflated gene to a plausible
mitochondria/peroxisome quality-control perturbation, but it also identifies the
proximal links that were assayed and largely flat.

## Limits and uncertainty

The prediction is an extrapolation from neighbors, not a direct measurement.
`Vps13d` is the VPS13 paralog most directly tied to mitochondria, peroxisomes,
and Miro, so the three silent paralogs are incomplete analogs.  Complete
`Vps13d` loss can injure neurons in animal models, and the PerturbAI assay used
sparse acute CRISPR with an average target-RNA drop of only about 18% per guide,
captured only surviving NeuN-positive nuclei, and did not measure mitochondrial
morphology, lipid transfer, peroxisomal abundance, mitophagic flux, indels, or
microglial responses.  A primary organelle phenotype or selective depletion of
heavily edited neurons could therefore be missed by the focal DEG count.  The
zero prediction means that the secondary nuclear RNA response is expected to
stay below the BH-FDR 0.05 threshold in the recovered `151` cells, not that
VPS13D is dispensable.
