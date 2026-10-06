# DEG-count prediction for the held-out target

## Question and endpoint

The manifest for this run contains one held-out perturbation:

```tsv
target_name
Gnb1
```

I interpreted the task as a point prediction for the number of measured genes with
`pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` class after postnatal,
sparse AAV-CRISPR loss of `Gnb1`. The count is the experiment's Wilcoxon/BH
single-nucleus endpoint and includes the perturbed transcript if that transcript
itself passes FDR; I did not subtract the target RNA from the requested count.

`Gnb1` was absent from both supplied training files. I therefore treated the
training DE table and the `151 TH Prkcd Grin2c Glut` training count CSV as
same-experiment analog evidence and used external biology only to decide which
training perturbations are meaningful analogs or counterexamples.

## Sources used

- Input DEG-count training CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input all-cell differential-expression Parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest:
  `[local file: 093_Gnb1.csv]`.
- Internal same-experiment semantic layer: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`, especially findings and claims for
  `Gnb5`, `Gnao1`, `Gnas`, `Kcnj6`, `Gpr158`, `Gpr179`, and `Rgs6`.
- External literature from PubMed:
  - Petrovski et al. 2016, American Journal of Human Genetics,
    DOI `10.1016/j.ajhg.2016.03.011`, PMID `27108799`: de novo `GNB1`
    mutations cause severe neurodevelopmental disability, hypotonia, and
    seizures; many pathogenic residues affect G-alpha/G-beta-gamma or effector
    binding.
  - Hemati et al. 2018, American Journal of Medical Genetics A,
    DOI `10.1002/ajmg.a.40472`, PMID `30194818`: clinical expansion of
    `GNB1`-associated neurodevelopmental disease.
  - Tennakoon et al. 2021, Cellular Signalling,
    DOI `10.1016/j.cellsig.2021.109947`, PMID `33582184`: review of
    G-beta-gamma subtype diversity in GPCR/G-protein signaling.
  - Senarath et al. 2018, International Review of Cell and Molecular Biology,
    DOI `10.1016/bs.ircmb.2018.02.008`, PMID `29776603`: review of G-beta-gamma
    regulation of kinases, lipases, GTPases, and ion channels.
  - Milligan and Kostenis 2006, British Journal of Pharmacology,
    DOI `10.1038/sj.bjp.0706405`, PMID `16402120`: review of canonical
    heterotrimeric GPCR signal transduction.
  - Kofuji et al. 1995, PNAS, DOI `10.1073/pnas.92.14.6542`, PMID `7604029`:
    G-beta-gamma, including G-beta-1/G-gamma-2, can activate neuronal GIRK
    channels.
  - Willardson and Tracy 2012, Sub-cellular Biochemistry,
    DOI `10.1007/978-94-007-4765-4_8`, PMID `23161137`: conventional G-beta
    assembly and the atypical G-beta-5/R7-RGS assembly route.
  - Patil et al. 2021, Science, DOI `10.1126/science.abl4732`,
    PMID `34793198`: structural coupling of GPR158 to the RGS7/G-beta-5
    signaling complex.
  - Colombo et al. 2023, Frontiers in Cellular Neuroscience,
    DOI `10.3389/fncel.2023.1175895`, PMID `37275776`: a `GNB1`
    encephalopathy knock-in can alter GIRK signaling, illustrating channel-level
    biology but also the mismatch between disease missense gain-of-function and
    postnatal CRISPR loss.

## Computational checks against the training data

I read the one-row held-out manifest to fix the required output order. I then
queried the training count CSV for the represented G-protein, GPCR,
GIRK/cAMP/PKA, and G-beta-5/RGS-neighborhood targets.

The key focal-cell counts were:

| training target | focal `n_degs` |
|---|---:|
| `Gnb5` | 0 |
| `Gnao1` | 1 |
| `Gnas` | 0 |
| `Gnal` | 0 |
| `Rgs6` | 0 |
| `Gpr158` | 1 |
| `Gpr179` | 0 |
| `Kcnj6` | 0 |
| `Adcy1`, `Adcy3`, `Adcy5` | 0, 0, 0 |
| `Pde1c`, `Pde4b`, `Pde4d`, `Pde10a` | 0, 0, 0, 0 |
| `Prkaca`, `Prkar1a` | 1, 1 |
| `Drd2`, `Drd4`, `Drd5` | 0, 0, 0 |
| `Gabbr1`, `Gabbr2` | 1, 1 |
| `Grm1`, `Grm5`, `Grm6`, `Grm7`, `Grm8` | 1, 0, 0, 1, 0 |
| `Oprd1`, `Oprk1`, `Oprl1`, `Oprm1` | 0, 0, 0, 0 |
| `Htr1a`, `Htr1b`, `Htr1f`, `Htr2a`, `Htr2c`, `Htr4`, `Htr6`, `Htr7` | all 0 |
| `Creb1`, `Crebbp` | 10, 8 |

I also queried the Parquet in the focal group for those comparators and counted
FDR 0.05 and FDR 0.10 genes:

```sql
SELECT gene_target,
       count(*) AS n_rows,
       sum(pvals_adj < 0.05) AS n_fdr05,
       sum(pvals_adj < 0.10) AS n_fdr10,
       min(pvals_adj) AS min_padj,
       arg_min(names, pvals_adj) AS min_gene
FROM training_de_all_cell_groups
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (<G-protein/cAMP/GIRK comparators>)
GROUP BY gene_target;
```

This confirmed that the 0-count comparators were not hiding many genes just above
the 0.05 threshold. `Gnb5`, `Gnas`, `Gnal`, `Kcnj6`, `Drd2`, `Drd4`, `Drd5`,
`Grm5`, `Grm6`, `Grm8`, `Oprm1`, `Pde10a`, and the represented adenylyl
cyclases had 0 genes at FDR 0.10 in the focal class. Several of the 1-count
neighbors were pure self-transcript events: `Gnao1`, `Gabbr1`, `Gabbr2`,
`Gpr158`, `Grm1`, `Grm7`, `Prkaca`, and `Prkar1a` each had the perturbed
transcript as the most significant focal hit. The only focal singleton with a
non-self FDR gene in this neighborhood was `Cnr1`, through `Srcap`.

The corpus layer agreed with this direct query: `Gnb5` produced no downstream
FDR 0.10 response in any measured neuronal group; `Gnb5`/`Rgs6`/`Gpr158`/
`Gpr179` neighbors were mostly flat; `Kcnj6` had no robust downstream response
in any recovered neuronal group; and claims around `Gnao1` and `Gnas` rejected
a common durable GPCR/cAMP/GIRK or dopamine/cAMP transcriptomic module in this
basal juvenile snRNA-seq assay.

## Target-specific reasoning

### `Gnb1`

`Gnb1` encodes conventional G-beta-1, a WD40 beta subunit of heterotrimeric G
proteins. With G-gamma subunits, G-beta-1 participates in receptor-coupled
G-alpha/beta/gamma heterotrimers and the released beta-gamma dimer can regulate
ion channels and enzymatic effectors, including GIRK channels, calcium channels,
phospholipase C beta, PI3K, and adenylyl cyclases. Pathogenic human `GNB1`
variants cause a severe neurodevelopmental syndrome, but many of those variants
are missense alleles predicted to distort G-alpha or effector binding; the
Gnb1-K78R mouse disease model in the literature behaves through altered GIRK
signaling. Those are channel and signaling phenotypes, not evidence that acute
postnatal sparse CRISPR loss should create a broad nuclear RNA state.

The most relevant measured same-experiment analogs argue against a medium or
strong focal response:

- The only beta-subunit target in training was the atypical `Gnb5`, and it had
  `n_degs = 0` in `151 TH Prkcd Grin2c Glut`. The corpus also reports that
  `Gnb5` had no robust downstream genes in any neuronal group. `Gnb5` is an
  imperfect analog because G-beta-5 preferentially assembles with R7 RGS
  proteins rather than simply substituting for G-beta-1 in conventional
  G-beta-gamma dimers, but the result shows that at least one G-beta-linked
  signaling module was transcriptionally buffered in this screen.
- Direct G-alpha perturbations on the represented arms were focal-cell null or
  self-only: `Gnao1 = 1`, `Gnas = 0`, and `Gnal = 0`. Thus disrupting a major
  neuronal Gi/o alpha, Gs alpha, or Golf alpha subunit did not launch the
  immediate-early or cAMP-responsive RNA program that would be the obvious
  route from GPCR signaling to snRNA-seq DEGs.
- Direct effector and receptor checks were equally quiet. `Kcnj6 = 0`; `Adcy1`,
  `Adcy3`, and `Adcy5` were all 0; the focal `Pde` family members were all 0;
  dopamine, opioid, and serotonin GPCRs were 0; and `Gabbr1`/`Gabbr2`,
  `Grm1`/`Grm7`, `Prkaca`, and `Prkar1a` were singleton self-transcript calls
  rather than broad downstream states.
- Positive controls on the transcriptional end of the same axis were detectable
  in this cell group: `Creb1` had 10 FDR 0.05 genes and `Crebbp` had 8. The
  nulls above are therefore not because the focal thalamic class cannot register
  small cAMP/CREB-adjacent RNA programs; the block is between tonic GPCR/G
  protein/channel signaling and durable basal nuclear mRNA.

For the point estimate, I therefore predicted a very weak response. The
within-dataset evidence drove the zero/downstream decision: loss of a G-beta
subunit is much closer to the flat `Gnao1`/`Gnas`/`Gnb5`/`Kcnj6`/`Adcy` regime
than to the chromatin, splicing, proteostasis, or core CREB-axis perturbations
that gave tens to thousands of focal DEGs. External biology kept me from using
`Gnb5` as a perfect paralog: `Gnb1` is the conventional, ubiquitous beta
subunit and could be broader than the atypical G-beta-5/R7-RGS module. I allowed
one DEG rather than a pure zero because the endpoint includes target RNA and the
high-powered focal class often calls a solitary perturbed transcript for
expressed GPCR/G-protein genes even when there is no downstream program.

Final point prediction: `Gnb1 -> 1`.

## Limits

- There was no direct `Gnb1` profile in the training Parquet, and the internal
  Distributed Agents graph had no held-out-safe `Gnb1` neighborhood. The prediction is
  an extrapolation from nearby G-protein machinery, not from a measured
  same-gene signature.
- `Gnb5` is the only assayed beta-subunit target but is mechanistically atypical;
  it binds R7 RGS proteins and is not equivalent to conventional G-beta-1.
- The conventional paralogs `Gnb2`, `Gnb3`, and `Gnb4` and many gamma subunits
  were not available as focal training perturbations, so I could not test
  direct beta/gamma redundancy.
- Human `GNB1` disease is dominated by heterozygous missense alleles and, in
  some models, altered GIRK/channel signaling. Sparse postnatal Cas9 loss of
  function can be buffered differently from a dominant disease allele.
- The prediction is for basal nuclear RNA 3-4 weeks after P16 perturbation in
  recovered NeuN-positive nuclei. It says little about acute GPCR
  electrophysiology, phosphorylation, circuit-level excitability, non-neuronal
  phenotypes, or developmental phenotypes before the perturbation window.
