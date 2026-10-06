# Reasoning trace

## Question and resolution

I predicted the held-out value `n_degs` for the single requested perturbation,
`Lmbr1`, in `151 TH Prkcd Grin2c Glut` neurons. I treated `n_degs` exactly as
the focal-cell training file defines it: the count of measured transcripts with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the knockout versus
matched-control contrast. `Lmbr1` was absent as a perturbation from both the
training DE parquet and the training DEG-count CSV, so no held-out `Lmbr1`
signature was used.

The main ambiguity is biological, not tabular. Most of the LMBR1 literature is
about a developmental limb locus whose introns contain the ZRS enhancer of
`SHH`, whereas this experiment performs sparse acute coding loss of function in
P16-to-P37/44 postmitotic NeuN+ brain nuclei. I therefore used ZRS/SHH studies
only to define what the `Lmbr1` locus is and did not treat embryonic limb
enhancer phenotypes as evidence for a large thalamic neuronal DEG burden.

## Sources used

- Declared training endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Lmbr1`.
- Same-experiment internal semantic corpus:
  PerturbAI July 260713 sourceguard 1773 v1 Findings and Pathways ledgers.
  These are report-level interpretations of the same experiment, not
  independent replication.
- External literature from PubMed:
  Ianakiev et al. 2000, DOI 10.1086/316955; Clark et al. 2001,
  DOI 10.1093/genetics/159.2.715; Dolezal et al. 2015,
  DOI 10.1073/pnas.1509856112; Ushiki et al. 2021,
  DOI 10.1038/s41467-021-22470-z; and the PubMed-indexed ZRS functional
  studies by Xu et al. 2019, DOI 10.1038/s41436-019-0626-7, and Potuijt et al.
  2018, DOI 10.1038/gim.2018.18.

## Quantitative checks

I first inspected the focal-cell training counts. The training distribution is
zero-heavy: 469 of 1,674 represented perturbations have any DEG, the median is
0, the 75th percentile is 1, the 95th percentile is 18, and only a long tail of
strong essential/chromatin/RNA-processing perturbations reaches hundreds of
DEGs. Thus a biologically peripheral or context-mismatched perturbation should
be expected to round down to zero unless represented relatives show a clear
focal response.

For exact comparator counts I read only rows with
`group_name == "151 TH Prkcd Grin2c Glut"` and a small mechanistic set of target
genes from the parquet:

```python
flt = (
    ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & ds.field("gene_target").isin(targets)
```

This focal slice confirmed the CSV counts and also exposed whether the one-gene
counts were self or downstream events.

## Target-specific evidence for Lmbr1

### Closest represented coding-family comparator: Lmbrd1

`Lmbrd1` is the only `Lmb*` perturbation represented in the focal training count
table and is the closest coding-domain analog available. It had `n_degs = 1` in
`151 TH Prkcd Grin2c Glut`: the single FDR<0.05 row was `Lmbrd1` itself
(`logfoldchanges = -0.606`, `pvals_adj = 0.00338`, 107 perturbed nuclei). No
other `Lmbrd1`-perturbation transcript passed even FDR<0.10 in this focal group;
the next row was `Pwwp2a` with `pvals_adj = 0.247`.

The July internal corpus independently summarizes the same flat surface: acute
`Lmbrd1` loss had no downstream FDR<0.10 response across measured postmitotic
neuronal groups, did not move transcripts in the lysosomal cobalamin pathway
(`Abcd4`, `Mmachc`, `Mmaa`, `Mmut`, `Mtr`, `Mtrr`), and had essentially
zero whole-signature correlation to all other perturbations. That matters as a
negative analog: even complete organismal loss of `Lmbrd1` is embryonic lethal
and LMBRD1 has a defined lysosomal cobalamin-export role, but this acute
neuronal assay did not convert that importance into a broad nuclear RNA
signature. Buers et al. 2016 (DOI 10.1111/jcmm.12844) and Tseng et al. 2013
(DOI 10.1074/jbc.M113.479527) support the external LMBRD1 cobalamin/endocytic
biology.

`Lmbr1` is less directly connected than `Lmbrd1` to a known postmitotic
neuronal metabolic pathway. Human C7orf2/LMBR1 exon disruption causes
acheiropodia through recessive limb malformation (Ianakiev et al. 2000), and a
mouse `Lmbr1` coding loss reduces digit number rather than creating the
preaxial-polydactyly gain-of-function phenotype (Clark et al. 2001). These are
embryonic limb-patterning readouts, not a sustained mature thalamic neuron RNA
program. In the focal training data, `Lmbr1` as a measured transcript never
passed FDR<0.05 under the 1,674 visible perturbations; the best adjusted
P value was 0.0959 under the very large `Uba5` signature. That makes a
self-transcript-only count like `Lmbrd1` possible but weakly supported.

### Hedgehog and ciliary counterexamples

Because disease variation at the `LMBR1` locus often sits inside or near the
ZRS enhancer controlling limb `SHH`, I checked whether direct Hedgehog and
ciliary perturbations were active in the same focal cell group. They were not:

- `Gli1`, `Gli2`, `Smo`, `Ptch1`, `Ptch2`, and `Cdon` each had `n_degs = 0`.
- Represented IFT/BBS/ciliary transport genes were also flat in the focal
  cells: `Ift43 = 0`, `Ift81 = 0`, `Ift88 = 0`, `Bbs5 = 0`,
  `Kif3b = 0`, `Cep290 = 0`, `Cplane1 = 0`, `Dync2h1 = 0`,
  `Dync2i1 = 0`, `Rpgrip1l = 0`, `Sclt1 = 0`, and `Tbc1d32 = 0`.
- The only adjacent singleton among the queried focal ciliary genes was
  `Arl3 = 1`, with `Arl3` itself down (`pvals_adj = 0.0184`), not a GLI/PTCH
  transcriptional module.

The internal Gli/Ptch/Smo/Ift88/Cdon reports explicitly place these findings in
the same-experiment context: P16 sparse loss of canonical Hedgehog
receptors/transducers and ciliary genes did not launch `Gli1`, `Ptch1`,
`Ptch2`, or `Hhip` feedback in NeuN+ juvenile neurons. Ushiki et al. 2021,
Xu et al. 2019, and Potuijt et al. 2018 support the external premise that the
`LMBR1` genomic interval contains limb `SHH` regulatory DNA, but the comparator
data argue against transferring that enhancer biology into this coding
knockout endpoint.

### BMP/TGF-beta signaling counterexamples

Drosophila Lilipod, an LMBR1/LIMR-type protein, can modulate BMP signaling in
germ-line stem cells (Dolezal et al. 2015), so I also checked whether basal
BMP/TGF-family signaling is visibly DEG-producing in the focal neurons.
Represented receptor and SMAD perturbations again gave a near-null result:
`Acvr1 = 0`, `Acvr2a = 0`, `Acvr2b = 0`, `Bmpr1a = 0`, `Bmpr1b = 0`,
`Bmpr2 = 0`, `Smad1 = 0`, `Smad3 = 0`, `Smad4 = 0`, `Smad6 = 0`,
`Smad9 = 0`, `Tgfbr1 = 0`, `Tgfbr2 = 0`, and `Tgfbr3 = 0`. `Smad2` was a
singleton with one focal gene, `Cpne7`, at adjusted P = 0.0167; it was not a
canonical BMP/SMAD response. The internal Acvr/Bmpr/Smad reports likewise
interpret those perturbations as lacking a coherent postnatal neuronal SMAD
transcriptional program.

## Prediction

The strongest within-dataset evidence is the near-null behavior of
`Lmbrd1`, Hedgehog/ciliary genes, and BMP/TGF-beta genes in the same focal
class. External evidence makes `Lmbr1` a limb-development/`SHH`-locus gene with
a possible distant LMBR1/LIMR-family relationship to BMP biology, but neither
relationship supplies an obligate acute, cell-autonomous transcriptional
function in postmitotic thalamic glutamatergic neurons. I therefore predict no
FDR<0.05 genes for held-out `Lmbr1`.

| target_name | predicted_n_degs |
|---|---:|
| Lmbr1 | 0 |

## Limits

This is an extrapolation from relatives and pathway members because the
`Lmbr1` perturbation itself was held out. The closest training homolog,
`Lmbrd1`, is only a domain-level comparator and is not known to be an
interchangeable member of the `Lmbr1` limb-development mechanism. ZRS/`SHH`
and acheiropodia literature mostly involve embryonic limb enhancers or early
patterning, while the screen perturbed postmitotic brain neurons. The prediction
also cannot rule out a subcellular ciliary or endosomal phenotype with no
steady-state nuclear RNA consequence, a rare vulnerable subcluster diluted in
`151 TH Prkcd Grin2c Glut`, or a self-transcript depletion that would produce a
single DEG. The focal matched counts for the key comparators were sufficient to
detect many large perturbation signatures, but sparse AAV CRISPR loss does not
guarantee complete biallelic disruption in every assayed nucleus.
