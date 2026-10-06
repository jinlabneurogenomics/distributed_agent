# Vps13d DEG-count prediction

## Question and resolved ambiguities

The held-out target list for this run contains one perturbation, `Vps13d`.
I need to predict its `n_degs` in `151 TH Prkcd Grin2c Glut`, where the
endpoint is the number of measured genes with Scanpy/Wilcoxon
Benjamini-Hochberg adjusted `pvals_adj < 0.05` in perturbed nuclei versus
matched controls.

I treated this as a count for the exact acute AAV-PHP.eB CRISPR perturbation
used in the input screen. I did not treat germline or conditional Vps13d
models, RNAi, transformed-cell knockouts, or disease severity as direct count
measurements; those were used only to decide which observed training
perturbations were mechanistically meaningful. I also did not interpret weak
self-transcript knockdown as proof of editing failure, per the task note.

## Sources used

- Requested-target manifest:
  `[local file: 261_Vps13d.csv]`
- Training focal DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Full non-held-out differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile tools for focal-cell signed log-fold-change
  neighborhood inspection
- NCBI PubMed, queried through the BioEval literature tool, for external
  papers on VPS13D and VPS13 bridge-like lipid transfer proteins

## Computational checks and summaries

The requested manifest contained exactly one row:

```tsv
target_name
Vps13d
```

`Vps13d` was absent from the 1,674-row training count table, as expected for a
held-out target. In the focal training count distribution, 1,205/1,674 targets
had zero DEGs, the median was 0, the 75th percentile was 1, the 95th percentile
was 18, the 99th percentile was 436.48, and the maximum was 2,677. Thus, zero
or a one-gene self-transcript call is the dominant empirical outcome.

For the focal cell group, I extracted all measured genes for a hand-curated
set of observed analogs spanning VPS13 paralogs, Miro/mitochondrial transport,
core autophagy, peroxisomes, retromer/GARP/lysosome traffic, and positive
mitochondrial stress controls:

```python
dataset = ds.dataset(parquet, format="parquet")
focal = pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
target_filter = pc.field("gene_target").isin(analogs)
table = dataset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=focal & target_filter,
)
```

Each queried observed analog had 17,259 measured focal-cell features. The
observed FDR 0.05 focal counts most relevant to `Vps13d` were:

```tsv
target	n_degs	in-focal interpretation
Vps13a	0	VPS13 paralog, flat
Vps13b	0	VPS13 paralog, flat
Vps13c	0	VPS13 paralog, flat
Rhot1	0	Miro1, direct VPS13D recruitment partner family, flat
Atg5	0	core autophagy, flat in the focal group
Atg16l1	0	LC3-lipidation complex, flat
Becn1	0	autophagy initiation/endosome factor, flat
Lamp2	0	lysosomal membrane/autophagy disease gene, flat
Pex1	0	peroxisome biogenesis, flat
Pex14	1	only the Pex14 self-transcript passed
Atp13a2	1	only the Atp13a2 self-transcript passed
Park7	1	only the Park7 self-transcript passed
Map1lc3a	1	only the Map1lc3a self-transcript passed
Sqstm1	1	only the Sqstm1 self-transcript passed
Tomm40	1	only the Tomm40 self-transcript passed
Timmdc1	0	mitochondrial complex-I assembly, flat
Vps35	17	modest retromer response
Vps54	31	modest GARP response
Opa1	37	modest ATF4/ISR-like mitochondrial response
Rab7	501	broad late-endosomal/lysosomal stress response
```

I also asked the Distributed Agents runtime to compare the focal log-fold-change
profiles of the observed analog set, with signed top-200 tails and `pvals_adj`
as the significance column. Thirteen of the twenty queried profiles had no
FDR-significant focal features. The `Vps13a`, `Vps13b`, and `Vps13c` profile
rows all reported `significant_feature_count = 0`; exact pairwise inspections
therefore showed zero shared FDR-positive features between those VPS13
paralogs and `Opa1`, `Vps35`, `Vps54`, or `Rab7`. The weak whole-profile
rankings among zero-call profiles were not used as positive phenocopy evidence
because their leading genes were nonsignificant and often off-axis. The useful
signal from this comparison was the boundary: the screen can detect `Rab7`,
`Opa1`, `Vps35`, and `Vps54` in this same cell group, but it did not convert
nearer Vps13/Miro/autophagy/peroxisome perturbations into FDR-scale RNA
programs.

## Target-specific reasoning

### Vps13d

**Prediction: 0 DEGs.**

The strongest within-dataset evidence is the measured VPS13 family behavior.
`Vps13a`, `Vps13b`, and `Vps13c` were all exactly zero in the focal group. The
Distributed Agents same-experiment corpus has the high-confidence synthesized claim
that acute perturbation of represented VPS13 paralogs does not elicit a shared
basal neuronal transcriptomic module in the assayed juvenile postmitotic
neuronal context; that claim explicitly notes that `Vps13d` was not measured.
The target-specific corpus findings for `Vps13a` and `Vps13c` also state that
the represented paralogs were flat and that expected autophagy, lysosomal,
redox, ISR/UPR, mitochondrial, and mitophagy-like marker panels did not emerge
after their perturbation.

Published biology gives `Vps13d` a mitochondrial emphasis that distinguishes
it from `Vps13a/b/c`. Biallelic VPS13D mutations cause recessive ataxia and
spasticity with mitochondrial morphology/function defects in patient
fibroblasts and Drosophila neurons (Seong et al. 2018, PMID 29604224, DOI
10.1002/ana.25220). Vps13D is required for mitochondrial size regulation and
mitochondrial clearance in Drosophila, and the same work observed a similar
large-mitochondria phenotype in human VPS13D-mutant cells (Anding et al.
2018, PMID 29307555, DOI 10.1016/j.cub.2017.11.064). VPS13D can be recruited
by MIRO to bridge the ER to mitochondria and peroxisomes in a VAP-dependent
way (Guillen-Samander et al. 2021, PMID 33891013, DOI
10.1083/jcb.202010004), promotes peroxisome biogenesis in cell lines and
patient fibroblasts (Baldwin et al. 2021, PMID 33891012, DOI
10.1083/jcb.202001188), regulates ER-mitochondria contact through a
Vmp1-Vps13D-Marf/MFN2 pathway conserved between fly and human cells (Shen et
al. 2021, PMID 34019822, DOI 10.1016/j.cub.2021.04.062), and acts in a
Pink1-dependent, Parkin-independent mitophagy pathway in Drosophila (Shen et
al. 2021, PMID 34459871, DOI 10.1083/jcb.202104073). Drosophila neuronal work
further separates Vps13D functions in fission from completion of mitophagy
(Insolera et al. 2021, PMID 34383748, DOI 10.1371/journal.pgen.1009731).
More generally, VPS13 proteins are bridge-like lipid-transfer proteins at
organelle contact sites (Kumar et al. 2018, PMID 30093493, DOI
10.1083/jcb.201807019; Leonzino et al. 2021, PMID 34216812, DOI
10.1016/j.bbalip.2021.159003).

Those mechanisms motivated four classes of observed analogs, and each class
pushed the count downward in this assay:

- VPS13 paralogs: `Vps13a`, `Vps13b`, and `Vps13c` were all 0 in the focal
  count table. This is the most direct internal family evidence.
- MIRO and mitochondrial transport: `Rhot1`, the mouse MIRO1 gene and the
  best measured proxy for VPS13D recruitment to mitochondria, was 0. The
  same-experiment `Rhot1` corpus findings report no Opa1-like ATF4/ISR
  mitochondrial stress and no shared FDR program with measured Miro/TRAK,
  kinesin, fission, or basal-autophagy neighbors. `Trak1`, `Kif5a`, `Kif5c`,
  and `Klc2` are mentioned in that corpus neighborhood as flat or sparse,
  supporting the idea that local mitochondrial positioning defects can stay
  below the somatic snRNA threshold.
- Autophagy and mitophagy machinery: `Atg5`, `Atg16l1`, `Becn1`, `Lamp2`,
  `Map1lc3a`, and `Sqstm1` were 0 or self-transcript-only 1-gene calls in the
  focal group. Distributed Agents `Atg5` and `Becn1` findings state that core autophagy
  genes do not produce pan-neuronal secondary transcriptional programs in this
  acute screen and that canonical LC3/GABARAP, p62, lysosome, UPR/ISR, and
  proteasome-rebound mRNA modules were mostly absent.
- Peroxisome/ER-organelle contacts and broad mitochondrial stress:
  `Pex1` was 0 and `Pex14` had only a one-gene self call; the Distributed Agents
  `Pex14` report likewise describes represented peroxisome-linked
  perturbations as flat or sparse. The mitochondrial positive control `Opa1`
  did give a detectable 37-gene focal response centered on `Asns`, `Chac1`,
  `Ddit3`, aminoacyl-tRNA synthetases, and `Mthfd2`, but Vps13D biology is an
  outer-membrane contact/mitophagy/lipid-transfer problem rather than direct
  loss of inner-membrane fusion. The measured `Tomm40`, `Timmdc1`, `Park7`,
  and `Atp13a2` counts also show that many mitochondria/Parkinsonism-linked
  losses remain at 0 or one self transcript here.

The strongest counterexamples are the trafficking responders `Rab7`, `Vps35`,
and `Vps54`. `Rab7` caused a large 501-gene late-endosome/lysosome and sterol
compensation state in the same focal cell group, and the same-experiment
corpus identifies recurrent induction of `Atp6v0b`, `Lamp2`, `Mcoln1`, `Dpp7`,
sterol biosynthetic transcripts, and proteostasis markers. `Vps35` and
`Vps54` gave smaller focal responses, 17 and 31 genes at FDR 0.05 in the
training count table. I treated these as assay-detectability controls rather
than as point analogs for `Vps13d`: `Vps13d` is not a Rab7-like terminal
late-endosomal GTPase, the direct autophagy/Miro/peroxisome proxies were
flat, and the measured VPS13 paralogs did not follow the retromer or GARP
branches.

Combining those pieces, a nonzero `Vps13d` count would require extrapolating
from complete or long-term Vps13d mitochondrial phenotypes into a sparse,
partial, three-to-four-week postnatal neuronal CRISPR snRNA-seq readout. The
training perturbations that most closely isolate individual Miro/autophagy and
VPS13-family steps say that such local organelle defects often stay below the
FDR 0.05 transcriptional threshold. I therefore predict `Vps13d` will behave
like the represented VPS13 and Rhot1/autophagy/peroxisome nulls in `151 TH
Prkcd Grin2c Glut`, not like `Rab7` or `Opa1`.

## Limits of the prediction

The main uncertainty is that VPS13D is not simply redundant with VPS13A/B/C:
cell culture and invertebrate work place it closest to MIRO, ER-mitochondria
contacts, peroxisomes, and mitophagy, and those are only partially covered in
the training panel. The closest unavailable perturbations include `Pink1`,
`Prkn`, `Rhot2`, `Trak2`, `Mfn1`, `Mfn2`, `Dnm1l`, `Vmp1`, and direct VAPB/ER
contact-site components. A neuron-specific complete Vps13d mouse knockout can
eventually cause mitochondrial dysfunction, cGAS-STING signaling, microglial
activation, and neurodegeneration (Miao et al. 2025, PMID 40563011, DOI
10.1038/s41594-025-01602-9), but that model has complete conditional
neuronal loss, a longer degenerative window, and microglia that are largely
outside this NeuN-positive focal assay. The zero prediction is therefore a
screen-context prediction, not a claim that Vps13d is biologically inert.
