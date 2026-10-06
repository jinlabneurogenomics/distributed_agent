# DEG-count prediction trace

## Question and resolved ambiguities

The requested endpoint is the integer count of genes that would pass
Benjamini-Hochberg FDR < 0.05 for a held-out CRISPR loss-of-function perturbation
in the focal `151 TH Prkcd Grin2c Glut` neuronal group.  The lone requested
held-out target in `the single-target request` is:

| target_name | predicted_n_degs |
|---|---:|
| Hoxc13 | 0 |

I treated `n_degs` as an assay- and cell-class-specific transcriptional
response breadth, not as organismal severity or editing efficiency.  Because
Hoxc13 itself was held out, no Hoxc13 DE surface or endpoint count was used.
The prediction was instead transferred from represented Hox-family and
Hox-program perturbations and then checked against external Hoxc13 biology.

## Sources

Primary quantitative inputs:

- `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- `training differential-expression dataset`
- `single-target request for Hoxc13`

Internal same-experiment corpus:

- Dataset portrait `perturbai-atlas-v5`.
- `perturbai-july-260713-sourceguard-1773-v1` Findings, Evidence, and Reference
  ledgers.  I used these only as a bounded interpretation layer over the same
  Perturb-seq experiment; the Parquet and the training CSV remained
  authoritative for exact focal DEG counts.

External biological priors:

- Godwin and Capecchi 1998, `Genes & Development`, DOI
  `10.1101/gad.12.1.11`, PMID `9420327`: Hoxc13 mutant mice lack external hair;
  Hoxc13 is expressed in hair follicles, vibrissae, nails, filiform papillae,
  and tail.
- Jave-Suarez et al. 2001, `Journal of Biological Chemistry`, DOI
  `10.1074/jbc.M101616200`, PMID `11714694`: HOXC13 can directly activate
  hair-keratin promoters through HOX binding motifs.
- Potter et al. 2010, `Journal of Investigative Dermatology`, DOI
  `10.1038/jid.2010.391`, PMID `21191399`: Foxn1 and many hair keratins are
  down-regulated in Hoxc13 mutant skin, supporting a HOXC13 -> Foxn1 terminal
  keratinocyte differentiation cascade.
- Hwang et al. 2008, `Development`, DOI `10.1242/dev.022202`, PMID `18684741`,
  from the same-experiment Dlx3 report: epidermal Dlx3 ablation places Hoxc13,
  Gata3, and hair keratin genes in a Dlx3-dependent hair-follicle program.
- Fernandez-Guerrero et al. 2020, `PNAS`, DOI `10.1073/pnas.2011078117`,
  PMID `33199643`: mammalian ectodermal enhancers drive HoxC expression in
  developing nails and hair follicles; Hoxc13 is an ectodermal dysplasia 9
  gene.

## Quantitative work over the supplied dataset

I read the requested-target CSV and confirmed that it contains exactly one
target, `Hoxc13`, while the focal training-count CSV contains 1,674
non-held-out targets.  In the focal training counts, 1,205/1,674 targets had
`n_degs = 0`, the median was 0, and among nonzero targets the median was still
only 1 DEG.  Therefore a zero prediction is not an outlier for this cell group.

I then queried the Parquet for the requested focal group and for Hoxc13-relevant
training perturbations.  The focal, FDR < 0.05 counts were:

| training target | role as analog or counterexample | 151 TH Prkcd Grin2c Glut n_degs |
|---|---|---:|
| Hoxa1 | represented Hox transcription factor | 0 |
| Hoxa3 | represented Hox transcription factor | 0 |
| Hoxa13 | posterior Hox13 paralog-family member | 0 |
| Hoxb8 | represented Hox transcription factor | 0 |
| Hoxd10 | represented Hox transcription factor | 0 |
| Hoxd13 | posterior Hox13 paralog-family member | 0 |
| Pbx1 | TALE cofactor for Hox proteins | 0 |
| Pbx3 | TALE cofactor for Hox proteins | 0 |
| Meis1 | TALE cofactor for Hox proteins | 0 |
| Meis2 | TALE cofactor for Hox proteins | 0 |
| Rarb | retinoic-acid/Hox developmental circuit member | 0 |
| Rarg | retinoic-acid/Hox developmental circuit member | 0 |
| Dlx3 | upstream hair-follicle regulator of Hoxc13 | 0 |
| Dlx6 | Dlx-family counterexample in neurons | 0 |
| Phox2a | brainstem/autonomic homeobox control | 0 |
| Phox2b | brainstem/autonomic homeobox control | 0 |

At the looser FDR < 0.10 threshold, the focal `151` group still had zero
significant genes for every one of these Hox, Hox-cofactor, retinoic-acid, Dlx,
and Phox perturbations.  The minimum adjusted p-values in the focal group were
also unconvincing: most were exactly 1.0, and the best of the listed Hox genes
was `Hoxb8` with minimum adjusted p = 0.879665.

The all-cell-group query was a boundary check rather than a score.  In the
training set, `Hoxa1`, `Hoxa3`, `Hoxb8`, and `Hoxd13` had no FDR < 0.10
downstream genes in any recovered neuronal group.  `Hoxa13` had only two
FDR < 0.10 calls and `Hoxd10` had only one, all in `217 P MY Pineal Glut` and
not in `151 TH Prkcd Grin2c Glut`; thus their rare weak positives do not
transfer to the requested thalamic class.

Finally, I checked whether the sampled nuclei showed any trace of the expected
Hoxc13/Dlx3/Foxn1 hair program.  `Hoxc13` itself is present as a measured gene
in rows for 1,674 focal-group training perturbations, but no perturbation in any
cell group gave a non-unit adjusted p-value for the Hoxc13 expression row.  In
the focal group, all queried hair or ectodermal program rows under Hox and Dlx3
perturbations, including `Hoxc13`, `Foxn1`, `Gata3`, `Krt14`, `Krt31`, `Msx2`,
`Runx2`, `Sp7`, `Alpl`, and `Col1a1`, had adjusted p = 1.0.  I did not interpret
the large log-fold-change values for sparse keratinized-lineage genes, because
the dataset portrait warns that pseudocount effects dominate very low
expression rows.

## Hoxc13-specific reasoning

The within-dataset evidence points to no detectable `151` response.  Hoxc13 is
not just a generic transcription factor; its well-described loss-of-function
output is a terminal hair, nail, and ectodermal keratinization program.  That
program is outside the NeuN-positive, postmitotic thalamic glutamatergic nuclei
assayed here.

The closest represented paralog-family comparators were `Hoxa13` and `Hoxd13`,
both posterior Hox13 genes.  They are imperfect because HOXC13 has distinct
hair-follicle targets whereas HOXA13 and HOXD13 are better known in distal limb
and urogenital development.  Even so, they test whether posterior Hox factors
produce a broad neuronal footprint in this perturbation design.  They did not:
both had `n_degs = 0` in the focal group, and `Hoxd13` was a pan-neuronal
FDR < 0.10 null in the same-experiment corpus.

Earlier Hox genes and Hox-TALE cofactors were also useful counterexamples.  The
same-experiment `Hoxa1` evidence reported 0 FDR < 0.10 downstream genes in all
23 recovered groups, zero robust overlap with represented Hox comparators, and
zero robust response from `Pbx1`, `Pbx3`, `Meis1`, `Meis2`, `Rarb`, or `Rarg`.
`Hoxa3` and `Hoxb8` were likewise reported as pan-measured neuronal nulls.
Together these measurements argue that the acute P16-to-P37/P44 assay is not
capturing an active Hox/Pbx/Meis developmental module in the sampled juvenile
brain.

I also checked a pathway-level analog rather than relying only on family
membership.  Hoxc13 lies downstream of Dlx3 in hair-follicle differentiation:
conditional Dlx3 loss changes Hoxc13, Gata3, and hair keratins in epidermis
according to Hwang et al. 2008.  The matched training perturbation `Dlx3`,
however, had `n_degs = 0` in the focal group and 0 FDR < 0.10 downstream genes
across 22 recovered neuronal groups in the July corpus.  A targeted
return-to-data check in the `Dlx3` report found no FDR-supported movement of
`Hoxc13`, `Gata3`, `Krt14`, `Krt31`, osteogenic genes, or BMP-receptor pathway
neighbors.  This is direct evidence that the epithelial Dlx3/Hoxc13/Foxn1 axis
is displaced from the assayed neuronal context.

The external Hoxc13 literature reinforces that interpretation rather than
overriding the local zeros.  Godwin and Capecchi showed that Hoxc13 mutant mice
have brittle hair/alopecia phenotypes in Hoxc13-expressing keratinized
structures.  Jave-Suarez et al. showed direct HOXC13 activation of hair keratin
promoters, and Potter et al. placed Foxn1 downstream of Hoxc13 in hair follicle
and nail differentiation.  Fernandez-Guerrero et al. further localized HoxC
enhancer function to ectodermal nail and hair organs.  None of these priors
predicts that a sparse P16 CRISPR loss in thalamic glutamatergic neurons should
mobilize hundreds of downstream genes three to four weeks later.

The causal transfer model is therefore:

`AAV CRISPR of Hoxc13 in postmitotic NeuN+ thalamic neurons -> possible local
HOXC13 protein loss only in any Hoxc13-competent cells -> no active
hair/nail/keratinocyte or posterior Hox13 developmental circuit in these cells
-> no coherent propagated transcriptional module -> ordinary sparse recovery
and Wilcoxon testing -> no genes crossing FDR < 0.05`.

I assigned `predicted_n_degs = 0`.

## Limits

This remains an extrapolation because `Hoxc13` was held out and the dataset does
not sequence DNA indels per target.  The represented Hox perturbations are only
partial analogs: `Hoxa13`/`Hoxd13` share the posterior Hox13 group but not
Hoxc13's hair-specific promoter grammar, and `Hoxa1`, `Hoxa3`, `Hoxb8`, and
`Hoxd10` probe Hox biology at other axial positions.  The raw Parquet has DE
statistics but no raw counts, so baseline expression of Hoxc13 in individual
thalamic cells cannot be estimated directly.  The July corpus and the Parquet
are two representations of the same experiment, not independent replication.

The strongest uncertainty is that rare unannotated Hoxc13-expressing neurons
could be absent from, or diluted inside, `151 TH Prkcd Grin2c Glut`.  That could
make an organismal or rare-cell phenotype invisible here.  It does not justify
a positive focal DEG-count call at FDR < 0.05, because every within-dataset Hox,
TALE-cofactor, retinoic-acid, and Dlx3/Hoxc13-program check was flat in the
requested class.
