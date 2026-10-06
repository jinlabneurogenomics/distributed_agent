# DEG-count prediction for 151 TH Prkcd Grin2c Glut cells

## Question and endpoint

The requested held-out perturbation set contains one mouse target, `Taf1`. I
interpreted the task as a scalar prediction of `n_degs`, the number of measured
protein-coding gene symbols whose Wilcoxon differential-expression result has
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` neurons after acute P16 AAV
CRISPR loss of function and P37-P44 snRNA-seq recovery. The held-out `Taf1`
signature and true DEG count are absent from the supplied parquet and from the
training count CSV, so the prediction has to be transferred from non-held-out
perturbations plus external TAF1 biology.

Two ambiguities were resolved conservatively:

- `151 TH Prkcd Grin2c Glut` was used as an exact Allen-style cell-group label;
  `TH` denotes thalamus in this atlas label, not tyrosine hydroxylase.
- The endpoint is assay breadth at FDR 0.05, not viability, target editing,
  mean transcription, or disease severity. I therefore did not treat TAF1
  essentiality or a weak target-transcript change in another perturbation as a
  direct DEG-count surrogate.

## Sources used

- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Declared focal training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared held-out target manifest:
  `single-target request for Taf1`.
- Internal same-experiment corpus: PerturbAI July 260713 sourceguard 1773 v1,
  queried only for visible training perturbations, especially `Med13`,
  `Med15`, `Med23`, `Gtf2h5`, `Taf1b`, `Brd4`, `Yy1`, and `Sin3a`.
- External literature from PubMed:
  Malik and Roeder 2023, Nat Rev Genet, DOI 10.1038/s41576-023-00630-9,
  PMID 37532915; Gegonne et al. 2006, PNAS, DOI
  10.1073/pnas.0510031103, PMID 16407123; Capponi et al. 2019, RNA Biology,
  DOI 10.1080/15476286.2019.1667214, PMID 31559909; O'Rawe et al. 2015,
  Am J Hum Genet, DOI 10.1016/j.ajhg.2015.11.005, PMID 26637982;
  Gudmundsson et al. 2019, Sci Rep, DOI 10.1038/s41598-019-46632-8,
  PMID 31341187; Crombie et al. 2024, Dis Model Mech, DOI
  10.1242/dmm.050741, PMID 38804708; Comai et al. 1994, Science,
  DOI 10.1126/science.7801123, PMID 7801123; Zomerdijk et al. 1994,
  Science, DOI 10.1126/science.7801130, PMID 7801130.

## Computation over the declared data

I first read the held-out CSV and found exactly one requested row:

```tsv
target_name
Taf1
```

The focal training count table contains 1,674 non-held-out perturbations and is
highly zero-inflated:

```text
median n_degs = 0
75th percentile = 1
95th percentile = 18
99th percentile = 436.48
zero-count targets = 1205/1674
nonzero targets = 469/1674
```

To anchor the count for a Pol II initiation factor, I then counted focal
FDR-significant genes for assayed initiation, Mediator, bromodomain, HAT, and
chromatin regulators from the parquet with the effective operation:

```sql
select gene_target,
       sum(case when pvals_adj < 0.05 then 1 else 0 end) as n_sig,
       avg(n_pert_matched) as n_pert,
       avg(n_ctrl_matched) as n_ctrl
from read_parquet(training_de_all_cell_groups)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

The most relevant focal counts were:

```tsv
target	n_degs	mean_perturbed_nuclei	comment
Gtf2h5	0	139	TFIIH p8/TTDA subunit; closest assayed basal Pol II factor
Taf1b	0	106	SL1/Pol I TAF, not a TFIID paralog
Med13	11	154	Mediator kinase-module scaffold
Med23	13	160	Mediator tail-associated subunit
Med15	19	158	Mediator tail-associated subunit
Ep300	0	155	p300 HAT coactivator
Crebbp	8	61	CBP/p300 HAT coactivator
Kat6a	0	170	MYST-family HAT
Kat6b	0	150	MYST-family HAT
Smarca4	0	146	BAF ATPase
Smarcc1	0	165	BAF core subunit
Smarcc2	185	162	BAF core subunit, strong but not TFIID-like
Brd4	311	93	acetyl-chromatin reader and Pol II elongation coactivator
Yy1	720	265	sequence-specific activator/repressor
Sin3a	1433	176	SIN3/HDAC scaffold
```

No canonical TFIID subunit target other than the held-out `Taf1` was present in
the visible training counts. The only `Taf*` training perturbation, `Taf1b`,
is a TBP-associated SL1 selectivity factor for RNA polymerase I initiation.
Comai et al. 1994 and Zomerdijk et al. 1994 showed that SL1 and TFIID are
separate TBP-TAF complexes with mutually exclusive TBP engagement. I therefore
used `Taf1b` as a boundary case for essential TBP-associated transcriptional
machinery that can be transcriptionally quiet in recovered P37-P44 neurons, not
as a direct TAF1 phenocopy.

The three visible Mediator hits had very similar 151-cell expression evidence.
At FDR 0.05, `Med15`, `Med23`, and `Med13` shared 8/24, 7/23, and 7/17
significant-gene overlaps pairwise and down-regulated the same differentiated
thalamic module including `Prkcd`, `Grm1`, `Pcp4`, `Plekhg1`, `Atp2a2`,
`Atp2b1`, `Grin2b`, and `Kcnc2`. The July PerturbAI corpus independently
summarized this same-experiment result as a `Med15`/`Med23`/`Med13` convergence
on a selective thalamic neuronal state, while `Med13l` and `Cdk8` did not
phenocopy the module. Malik and Roeder 2023 place Mediator and TFIID on the
same Pol II pre-initiation/coactivator axis, so this cluster is the closest
quantitative lower-bound analog for TAF1 in the visible training set.

I treated the large `Brd4`, `Yy1`, `Sin3a`, `Thap11`, and `Zbtb7a` signatures
as counterexamples rather than as count donors. Their 151 signatures are broad,
but they arise from enhancer elongation, YY1 DNA binding, SIN3/HDAC repression,
or sequence-specific transcriptional programs, and the corpus reports recurrent
RNA-processing/proteostasis arms that are not a clean TFIID initiation state.
Pairwise FDR overlaps between `Med15`/`Med23`/`Med13` and these broad regulators
were small relative to the broad regulators' DEG burdens; for example `Med15`
shared only 10 of its 19 FDR genes with `Yy1`, 5 with `Sin3a`, and 4 with
`Brd4`. Thus they support the idea that thalamic neurons can show hundreds of
DEGs after selected nuclear perturbations, but not that `Taf1` should be placed
in that high-burden class.

## Target-specific reasoning

### Taf1

TAF1 is the large enzymatic scaffold subunit of TFIID, the TBP-containing
coactivator complex that recognizes core promoters and contributes to Pol II
pre-initiation complex formation. TAF7 binds TAF1 in TFIID and can restrain
TAF1 acetyltransferase activity until initiation-linked phosphorylation events
release it, so partial TAF1 impairment is expected to perturb regulated Pol II
initiation rather than act like a cytosolic signaling protein. Neuronal biology
is also plausible: TAF1 pathogenic variants cause an X-linked intellectual
disability syndrome, TAF1 has a neuron-specific microexon promoted by SRRM4,
zebrafish taf1 knockout disrupts embryogenesis and neurodevelopmental gene
programs, and ubiquitous Taf1 deletion is embryonic-lethal in male mice.

Those priors justify a nonzero call, but they do not justify a genome-wide
collapse in this dataset. The experiment is acute, mosaic, and assayed only
surviving NeuN-positive postmitotic nuclei three to four weeks later. The most
direct visible basal-transcription comparison, `Gtf2h5`, produced 0 DEGs in the
151 cell group, and `Taf1b` likewise produced 0 despite being an essential TBP
associated factor in Pol I initiation. HAT and coactivator boundary cases were
also mostly small or absent at this endpoint: `Ep300`, `Kat6a`, and `Kat6b`
were 0 and `Crebbp` was 8. Conversely, the three assayed Mediator subunits that
sat nearest TFIID in the Pol II initiation/coactivator causal chain were
reproducibly but narrowly nonzero in exactly the focal class: `Med13` had 11,
`Med23` had 13, and `Med15` had 19 FDR 0.05 genes, with a shared same-direction
Prkcd/Grm1/Pcp4/Plekhg1/Atp2a2/Atp2b1 down-module.

The resulting causal transfer model is:

`Taf1` LoF -> impaired TFIID enzymatic/scaffold contribution to selected Pol II
promoters -> incomplete maintenance of an activity/subtype thalamic glutamate
program -> survival-conditioned sampling of postnatal neurons -> a narrow set
of FDR-significant nuclear RNA changes.

The Mediator analogs act one step later or in parallel in the Pol II
pre-initiation complex, so they are not direct complex substitutes for TAF1.
Their low, convergent count is nevertheless a better assay-scale guide than
the broad `Sin3a` or `Yy1` responses because the latter contain large
secondary RNA-processing and proteostasis surfaces. Averaging the focal
Mediator counts gives about 14 DEGs; the GTF2H5/TAF1B/p300 nulls pull against
a large value but not all the way to zero because TAF1 is the core TFIID
subunit with a known neuronal isoform and TAF1 neurodevelopmental genetics.

I therefore predict `Taf1` will be a low nonzero responder in 151 TH Prkcd
Grin2c Glut cells:

```tsv
target_name	predicted_n_degs
Taf1	14
```

## Limits

- The most important limitation is absence of a visible TFIID core-subunit
  perturbation. `Med13`, `Med15`, and `Med23` are mechanistically adjacent to
  TFIID at Pol II promoters, but they are Mediator proteins and can couple
  different transcription-factor inputs to Pol II.
- `Taf1b` is an informative negative boundary for a TBP-TAF initiation factor
  but belongs to SL1/Pol I, so its 0 DEG count should not erase the Pol II
  TAF1 prediction.
- The broad chromatin perturbations prove that this cell group can produce
  hundreds to thousands of DEGs, but they are not close enough to TFIID to
  calibrate a high `Taf1` count.
- External Taf1 knockout and disease work mostly concerns germline or
  embryonic alleles, missense variants, zebrafish embryos, or complete mouse
  deletion. The requested assay is sparse postnatal CRISPR in recovered mouse
  neuronal nuclei, so those studies are gene-function priors rather than direct
  quantitative measurements of the held-out endpoint.
- The point estimate is near the 95th percentile of the training distribution
  but is still numerically small. A realized value anywhere from 0 to a few
  dozen DEGs would be biologically compatible with the observed analog set.
