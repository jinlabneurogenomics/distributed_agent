# Zbtb42 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question interpreted

The requested held-out perturbation list contains one target:

```text
Zbtb42
```

For that target I need to predict the integer number of measured genes that would
pass Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in the held-out
`151 TH Prkcd Grin2c Glut` knockout profile. `logfoldchanges` in the supplied
parquet are perturbed versus matched non-targeting control, but the requested
endpoint ignores direction and is only the count of FDR-significant measured
genes. `Zbtb42` itself is held out, so no direct `Zbtb42` expression signature
or observed `Zbtb42` DEG count was used.

I treated weak self-transcript knockdown as non-decisive, as requested, because
this AAV CRISPR screen averages only modest target-RNA depletion and measures
nuclear mRNA rather than DNA editing.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 266_Zbtb42.csv]`
- Run-local Distributed Agents runtime profile comparison over the assayed ZBTB family:
  `zbtb_profile_compare.json`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`
- PubMed literature searches for `ZBTB42`
- Ensembl REST lookup of the mouse `Zbtb42` locus, GRCm39
  `ENSMUSG00000037638`, cross-referenced to MGI symbol
  `MGI:3644133`

## Computations over the parquet and count table

I first read the focal training-count CSV and summarized the empirical endpoint
distribution. Of 1674 non-held-out perturbations in `151 TH Prkcd Grin2c Glut`,
1205 were exactly zero at FDR 0.05; the median was 0 and the upper quartile was
1. The upper tail was real but rare: the mean was 14.1, the 95th percentile was
18, and the largest responders were `Uba5` at 2677, `Tpr` at 1768, `Sin3a` at
1433, `Rnpc3` at 868, and `Zbtb7a` at 841.

For candidate analogs I filtered the parquet to the focal cell group and to
assayed ZBTB/C2H2 zinc-finger or chromatin-transcriptional comparators, then
recomputed the endpoint directly:

```python
dset = ds.dataset(training_de_all_cell_groups, format="parquet")
tbl = dset.to_table(
    columns=[
        "gene_target", "names", "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
        & ds.field("gene_target").isin(candidate_targets)
    ),
)
n_degs = tbl.to_pandas().groupby("gene_target").pvals_adj.apply(
    lambda s: int((s < 0.05).sum())
)
```

The recomputed counts matched
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` exactly.

## Most relevant same-experiment perturbations

The closest interpretable evidence is the represented BTB-ZF/ZBTB family. The
Distributed Agents corpus has no direct `Zbtb42` findings, but it contains a
same-experiment high-confidence family claim that shared BTB-ZF/ZBTB membership
was insufficient to define a shared juvenile postmitotic neuronal RNA state.
That claim was built from measured contrasts in which the family separated into
a broad `Zbtb7a` response, weakly focal `Zbtb18`/`Zbtb38` responses, and flat
`Zbtb10`, `Zbtb16`, `Zbtb20`, and `Zbtb21` responses.

Focal `151 TH Prkcd Grin2c Glut` counts for these comparators were:

| training target | matched perturbed nuclei | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | ---: | --- |
| `Zbtb7a` | 282 | 841 | Very broad response; 512 significant genes up and 329 down. Top focal hits included `Pnma3`, `Col9a3`, `Gpc1`, `Usp11`, `Sema4a`, `Fhl1`, and `Rasgrp2`. |
| `Zbtb18` | 208 | 5 | Tiny all-up signature: `Endou`, `Pxdn`, `Clstn2`, `Man2a2`, and the `Zbtb18` self feature. `Pxdn`, `Clstn2`, and `Man2a2` overlapped `Zbtb7a` at FDR 0.05, but the rest of `Zbtb7a`'s 841-gene signature was absent. |
| `Zbtb38` | 199 | 1 | Only `Msra` passed FDR 0.05, with no FDR-level overlap with `Zbtb18` or `Zbtb7a` in this focal group. |
| `Zbtb10` | 187 | 0 | No focal DEG. Same-experiment corpus summarized it as flat across matched neuronal groups and separated from `Zbtb7a`, `Zbtb18`, and `Zbtb38`. |
| `Zbtb16` | 180 | 0 | No focal DEG. Same-experiment corpus used it as an anchor for non-interchangeability of assayed BTB-ZF factors. |
| `Zbtb20` | 185 | 0 | No focal DEG. Corpus evidence found 22 matched neuronal groups and 371,796 downstream Wilcoxon tests with zero FDR<0.10 genes, and no meaningful screen-wide cosine neighbor. |
| `Zbtb21` | 137 | 0 | No focal DEG despite CREB/CBP, cohesin, and `Zbtb7a` comparators being detectable in the same analysis universe. |

Those are appropriate analogs because they share the same BTB-zinc-finger domain
architecture as `Zbtb42` and were assayed with the same perturbation chemistry,
single-endpoint juvenile timing, matched control pool, and focal thalamic cell
group. They are also imperfect analogs: `Zbtb42` has no well-established
one-to-one paralog among these targets, and `Zbtb7a`, `Zbtb18`, `Zbtb20`, and
`Zbtb16` are functionally specialized transcription factors rather than an
interchangeable protein complex.

The broader assayed zinc-finger set supported the same caution. Most represented
C2H2/SCAN/KRAB-adjacent zinc-finger perturbations were flat in the focal group:
`Zfp1`, `Zfp106`, `Zfp160`, `Zfp182`, `Zfp266`, `Zfp280c`, `Zfp280d`,
`Zfp292`, `Zfp322a`, `Zfp341`, `Zfp397`, `Zfp451`, `Zfp462`, `Zfp521`,
`Zfp536`, `Zfp609`, `Zfp644`, `Zfp654`, `Zfp664`, `Zfp804a`, `Zfp846`,
`Zfp949`, `Zfp950`, `Zfp961`, `Zfpm2`, `Zkscan1`, `Zkscan16`, and `Zscan26`
all had `n_degs = 0`. A few zinc-finger transcriptional regulators were
detectable, for example `Zfp423` at 150, `Zfp236` at 19, `Zfx` at 15,
`Zfp148` at 8, `Zfp612` at 1, and `Zfp692` at 1, showing that the class was not
technically invisible. However, their detectable states were target-specific
rather than a generic BTB/C2H2 program. The Distributed Agents corpus similarly reports
that represented SCAN/C2H2/KRAB-associated zinc-finger perturbations did not
define an interchangeable shared neuronal transcriptomic regulon.

I also considered whether to borrow signal from broad chromatin or
transcriptional repressors such as `Sin3a` at 1433, `Zbtb7a` at 841, `Chd4` at
100, `Setdb1` at 22, and `Ehmt1` at 4. I did not use those as positive
quantitative templates. `Zbtb42` is annotated as a nuclear zinc-finger BTB
protein, so a repressive-chromatin function is plausible in the abstract, but
the same screen shows that adjacent TF/chromatin annotation can span 0 to more
than 800 focal DEGs. Without evidence that `Zbtb42` recruits the same neuronal
NuRD, SIN3, SETDB1/KAP1, or `Zbtb7a` effector module, those broad responders are
better interpreted as positive controls for assay detectability than as
mechanistic phenocopies.

## External biology for `Zbtb42`

`Zbtb42` is a small protein-coding zinc-finger and BTB-domain gene in mouse
GRCm39 at `ENSMUSG00000037638`, with MGI symbol accession `MGI:3644133`
according to Ensembl. Devaney, Mate, Devaney, and Hoffman characterized human
and mouse `ZBTB42` as a conserved, two-exon, nuclear zinc-finger protein; in
mouse tissue blots they saw strongest expression in skeletal muscle and ovary,
and in muscle nuclei they saw enrichment under neuromuscular junctions
(Devaney et al. 2010, DOI `10.1007/s00439-010-0940-2`, PMID `21193930`).
Patel, Smith, Faqeih, Mohamed, Gupta, and Alkuraya subsequently linked a
homozygous human `ZBTB42` missense allele to lethal congenital contracture
syndrome and showed that zebrafish `zbtb42` knockdown disrupts skeletal muscle
development and myofibrillar organization, with rescue by wild-type but not
mutant human `ZBTB42` (Patel et al. 2014, DOI `10.1093/hmg/ddu384`, PMID
`25055871`).

That literature makes `Zbtb42` a plausible transcriptional regulator, but its
best-supported biology is muscle and neuromuscular-junction development rather
than a known maintenance role in juvenile thalamic glutamatergic neurons. The
experiment is NeuN-enriched and strongly depletes non-neuronal and muscle
tissue contexts, so a zebrafish/muscle developmental phenotype should not be
projected directly into hundreds of neuronal nuclear DEGs.

## Target-specific decision

I predict `Zbtb42` as a focal nonresponder with `n_degs = 0`.

The positive side is that a BTB-ZF protein can be perturbable in this exact
cell group: `Zbtb7a` gave 841 DEGs, and `Zbtb18` produced a five-gene thalamic
signature with three genes overlapping `Zbtb7a`. The negative side is stronger
for this target. Four of seven assayed ZBTB comparators had no focal DEG, one
had a single DEG, and the corpus-level comparison shows the family does not
phenocopy as a class. `Zbtb42` lacks the specific published neuronal fate role
of `Zbtb18`/`Zbtb20` and lacks the same-experiment proteostasis/endomembrane
signature evidence that made `Zbtb7a` a broad positive outlier. Its external
literature instead points to skeletal muscle and neuromuscular biology, which
is largely outside the sampled NeuN+ postnatal brain nuclei.

Because the focal endpoint is highly sparse, a small idiosyncratic one- to
five-gene hit is possible. Still, the best same-family null comparators
(`Zbtb10`, `Zbtb16`, `Zbtb20`, `Zbtb21`) outnumber the weak positives
(`Zbtb18`, `Zbtb38`), and there is no mechanism to select the `Zbtb7a` broad
state. I therefore set the point prediction to the modal and mechanistically
favored outcome, zero.

## Limits

- `Zbtb42` itself was absent from the training counts and parquet as a
  perturbation; the reasoning is extrapolation from other BTB-ZF/C2H2 targets.
- The closest ZBTB relatives for `Zbtb42` were not established from a formal
  phylogenetic tree, protein-protein interaction map, or chromatin-occupancy
  experiment. The assayed ZBTB targets are domain-architecture comparators, not
  proven paralogs.
- Same-experiment transcriptomic similarity measures between very weak profiles
  are noisy. I emphasized FDR-supported genes and curated corpus contrasts over
  whole-vector correlations.
- The public `ZBTB42` literature is sparse and dominated by muscle/NMJ and
  congenital contracture phenotypes. That absence of neuronal evidence does not
  prove absence of function in `151 TH Prkcd Grin2c Glut` neurons.
- This prediction is for a sparse postnatal AAV CRISPR loss-of-function,
  nucleus-level snRNA-seq assay. It should not be read as a prediction about
  germline nulls, human missense alleles, muscle, electrophysiology, or
  viability.
