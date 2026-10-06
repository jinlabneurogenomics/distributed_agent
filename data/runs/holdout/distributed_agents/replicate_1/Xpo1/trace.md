## Question

I interpreted the task as a point prediction for the held-out perturbation
`Xpo1` in the focal `151 TH Prkcd Grin2c Glut` class.  The requested endpoint is
the exact dataset readout `n_degs`: the number of measured genes whose
Benjamini-Hochberg-adjusted Wilcoxon p-value is below 0.05 in that focal class.
`Xpo1` itself was held out, so its own DEG count and signature were absent from
the supplied parquet and training-count CSV.

I treated the focal training `n_degs` CSV and the declared DE parquet as direct
same-experiment evidence for represented training perturbations.  I treated the
July 260713 sourceguard PerturbAI Finding corpus as a same-experiment
interpretive layer over that parquet, not as independent replication.  I used
PubMed literature to decide which represented perturbations are mechanistic
analogs of XPO1 and which are counterexamples.

## Computation

I used the declared Perturb-seq feature workbench
`dataset.perturbseq_features summarize` on
`training_de_all_cell_groups.parquet`.  This produced
`workbench/features.parquet`, a cached target-level table for 1,674 non-held-out
biological targets with FDR-burden and log-fold-change distribution features.
The nested `calibrate` operation could not run in this one-target task because
`task_bindings.json` contained no ranked or partially ranked supervision set;
the supplied supervision is the focal DEG-count CSV itself.

The focal count CSV matched the feature table exactly: 1,674 unique training
targets, with no target present in only one of the two tables.  The focal
training endpoint is highly zero-inflated: 1,205/1,674 targets had `n_degs = 0`,
the median was 0, the 90th percentile was 2, and the 95th percentile was 18.
Thus any prediction above a few dozen genes is already a large response for
this readout, while the strongest visible focal effects are much larger:
`Uba5` 2,677, `Tpr` 1,768, `Sin3a` 1,433, `Rnpc3` 868, `Zbtb7a` 841, `U2af2`
828, `Hnrnpu` 733, and `Tnpo3` 618.

I then extracted the focal-cell parquet rows for the mechanistic comparator
panel.  Counts recomputed from `pvals_adj < 0.05` reproduced the CSV values:

| training perturbation | focal `n_degs` | relevance to `Xpo1` |
| --- | ---: | --- |
| `Tpr` | 1,768 | nuclear-basket/TREX-2 mRNA-export factor; strongest positive transport/RNA-processing analog |
| `U2af2` | 828 | spliceosome/RNA-processing perturbation that converges with the `Tnpo3`/`Tpr` RNA axis |
| `Hnrnpu` | 733 | broad nuclear RBP perturbation |
| `Tnpo3` | 618 | Ran-regulated karyopherin that imports phosphorylated SR splicing proteins |
| `Hnrnpc` | 122 | nuclear RBP with a smaller focal response |
| `Hnrnpa2b1` | 11 | RBP counterexample with only a minimal focal response |
| `Rbm28` | 0 | nuclear/nucleolar RNA-processing counterexample |
| `Ranbp2` | 0 | nuclear-pore/Ran-associated component, broad elsewhere but flat in the focal class |
| `Kpna3` | 0 | classical nuclear-import adapter counterexample |
| `Xpo7` | 0 | another exportin and Ran-dependent transport receptor, but a branch-selective flat counterexample |

Within `151 TH Prkcd Grin2c Glut`, the score correlations supported only
partial shared RNA-processing structure among the large signatures:
Spearman(`Tpr`, `Tnpo3`) = 0.319, Spearman(`Tpr`, `U2af2`) = 0.255, and
Spearman(`Tnpo3`, `U2af2`) = 0.208.  In contrast, `Xpo7`, `Kpna3`, and
`Ranbp2` had no focal FDR < 0.05 genes and showed only weak or near-zero focal
score correlations with `Tpr` and `Tnpo3`.  The raw focal `Tpr` signature did
contain `Xpo1` itself as a strong induced transcript
(`log2FC = 0.955`, FDR `3.20e-14`), consistent with compensatory activation of
export machinery after nuclear-basket stress, but this is a downstream marker
of `Tpr` loss rather than a direct measurement of `Xpo1` loss.

## Same-experiment comparators

The packaged PerturbAI July corpus reports that `Tpr` perturbation altered
nuclear-transport and NXF1-adjacent export genes, with `Ranbp6` and `Xpo1`
recurrently up and `Nxf1` down across multiple cell groups.  Its focal
signature had 1,768 DEGs, and its all-cell signature overlapped in the same
direction with RNA-processing, proteasome, and UFMylation perturbations.  The
biological link is that TPR is an architectural nuclear-basket nucleoporin and
an integral TREX-2/NXF1 mRNA-export component; TPR depletion impairs export of
retained-intron or short/intron-poor RNAs (Krull et al. 2004, PMID 15229283;
Coyle et al. 2011, PMID 21613532; Lee et al. 2020, PMID 33091126; Aksenova et
al. 2020, DOI 10.1038/s41467-020-18266-2).  This makes `Tpr` the most relevant
positive same-assay transport comparator, but it is not a direct XPO1 complex
member: `Tpr` sits at the pore and affects NXF1/TREX-2 mRNA export, whereas
XPO1 is a soluble export receptor for NES-bearing proteins and several RNA
classes.

`Tnpo3` perturbation produced 618 focal DEGs and was reported by the same July
corpus to down-regulate an SR-splicing/RNA-processing module, including
`Srrm2`, `Srsf5`, `Srsf1`, `Srsf7`, `Srsf2`, `Akap8l`, `Clk1`, and `Cstf2`.
TNPO3/Transportin-SR2 is a Ran-regulated importin-beta-family receptor for
phosphorylated RS-domain splicing proteins (Kataoka et al. 1999, J Cell Biol;
Lai et al. 2001, Proc Natl Acad Sci USA; Maertens et al. 2014, Proc Natl Acad
Sci USA).  The corpus comparison to KEGG mmu03040 spliceosome perturbations
showed same-direction overlap with `U2af2`, `Cdc40`, `Rnpc3`, `Snrnp70`, and
`Thoc1`, but little overlap with `Kpna3`, `Xpo7`, or `Ranbp2`.  This is an
important causal qualifier: perturbing a Ran-dependent nuclear transport
protein can propagate into a large focal RNA-processing response when the
limiting function is SR-splicing-factor import, but broad karyopherin or
exportin annotation by itself did not transfer that response.

`Xpo7` was the closest visible exportin counterexample.  It had zero focal DEGs
and only one FDR < 0.10 gene in the full same-experiment corpus, despite XPO7
being a broad-spectrum exportin and nuclear import receptor with proteomic
cargoes described by Aksu et al. 2018 (DOI 10.1083/jcb.201712013).  The Xpo7
report explicitly contrasted its flatness with `Ranbp2`, showing that the assay
can see consequences of some Ran/nuclear-pore perturbations while not
detecting this exportin branch.  This argued against lifting `Xpo1` all the way
to the `Tpr`/`Tnpo3` range only because it is an export receptor.

## `Xpo1` Prediction

XPO1/CRM1 is not interchangeable with XPO7.  CRM1 was originally identified as
the essential carrier for leucine-rich nuclear-export-signal protein export and
interacts with RanGTP during export-complex assembly (Stade et al. 1997, DOI
10.1016/S0092-8674(00)80370-0).  Structural work on the
Snurportin1-CRM1-RanGTP complex showed how RanGTP allosterically promotes CRM1
cargo binding (Monecke et al. 2009, DOI 10.1126/science.1173388).  Recent
reviews describe CRM1/XPO1 as the best-characterized nuclear export receptor,
with hundreds of protein cargoes, RNA-related cargo routes, contacts with
nucleoporins, and roles outside simple cargo export (Yang et al. 2023, DOI
10.1038/s41392-023-01649-4; Kehlenbach and Chook 2025, DOI
10.1016/j.tibs.2025.09.003).  In neurons, excess CRM1 activity can reduce
nuclear TFEB/STAT3 and impair autophagy in old mouse cortex and hippocampus;
CRM1 inhibition restored TFEB nuclear localization in an in vitro neuronal
senescence model (Gorostieta-Salas et al. 2021, DOI 10.1155/2021/6682336).

The causal transfer I used was therefore:

`Xpo1` CRISPR loss -> reduced CRM1-mediated nuclear export of NES proteins and
some RNA/adaptor cargoes -> altered localization of transcriptional,
RNA-processing, and proteostasis regulators -> partial nuclear
transport/proteostasis stress in recovered thalamic glutamatergic neurons ->
FDR-significant but not TPR-scale transcriptional remodeling.

The same-direction prior is positive because XPO1 and TPR both touch nuclear
export and `Tpr` loss induced `Xpo1` in the exact focal group, suggesting that
CRM1 abundance is part of the compensatory state when mRNA export through the
nuclear basket is stressed.  The transfer is partial rather than obligate:
XPO1 exports a broad receptor-defined cargo set, while TPR is a pore-basket
scaffold for NXF1/TREX-2-linked mRNP export.  `Xpo7` and `Kpna3` show that
other represented karyopherin branches can be silent in this postnatal neuronal
assay, and `Ranbp2` shows that even a nuclear-pore/Ran component with hundreds
of DEGs elsewhere can have zero focal DEGs.  Also, strong XPO1 impairment might
select against edited neurons before recovery, muting the survivor-conditioned
signature.

I therefore predicted a small nonzero focal response, `37` DEGs.  This is above
the bulk zero/one-gene background and acknowledges the stronger CRM1 prior and
the `Tpr`-induced `Xpo1` marker, but it is deliberately far below the focal
`Tpr`, `Tnpo3`, and spliceosome/RBP responses because the direct limiting
function is not the same and focal same-assay transport counterexamples are
common.

## Limits

This is extrapolation.  There is no `Xpo1` perturbation signature in the
declared training parquet, no represented close CRM1 paralog, and no direct
measurement of CRM1 cargo localization, nuclear export flux, TFEB activity, or
survival.  `n_degs` is FDR- and power-dependent; a quiet signature could mean a
buffered molecular response or survivor sampling rather than no biology.  The
Tpr -> Xpo1 comparison is particularly asymmetric because `Xpo1` is a
downstream induced transcript in a `Tpr` knockout, not the upstream molecular
lesion itself.  External XPO1 literature mostly comes from yeast, cultured
cells, cancer, or aging neurons rather than sparse P16 mouse thalamic
glutamatergic CRISPR.  Those sources justify the direction of a nonzero prior
but do not calibrate the DEG count scale.
