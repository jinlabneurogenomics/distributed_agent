# Kmt2e DEG-count prediction

## Question and endpoint

The requested held-out manifest contains one target:

```tsv
target_name
Kmt2e
```

I interpreted the endpoint as the integer number of measured genes with
`pvals_adj < 0.05` after acute AAV-CRISPR loss of the held-out gene in the
`151 TH Prkcd Grin2c Glut` nuclei.  `Kmt2e` is absent from both the parquet and
the focal-cell count CSV, so I did not try to infer a direct Kmt2e signature;
instead I used counts and expression profiles from non-held-out perturbations
that are mechanistically adjacent to KMT2E/MLL5.

## Sources used

- Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`.  The corpus had no Kmt2e node
  (`target_found=false`), but it did contain curated same-experiment summaries
  for the observed KMT2/SET/HAT/chromatin comparators.
- Distributed Agents runtime profile comparison over `151 TH Prkcd Grin2c Glut`,
  comparing selected observed chromatin perturbations by signed
  `logfoldchanges`.
- PubMed searches for KMT2E/MLL5 molecular and disease literature.

External KMT2E facts that affected the transfer:

- KMT2E/MLL5 is grouped with the KMT2 family by SET-domain homology but is
  structurally divergent from canonical KMT2A-D/SETD1A/B COMPASS methylases and
  lacks intrinsic histone methyltransferase activity on recombinant histones
  and H3 peptides in vitro.  Mas-Y-Mas et al. 2016, DOI:
  10.1371/journal.pone.0165139; Zhang et al. 2017, DOI:
  10.1007/s00018-017-2470-8.
- The KMT2E PHD finger binds H3K4me3/H3K4me2, so KMT2E is plausibly an H3K4
  chromatin reader despite being a weak methyltransferase analog.  Ali et al.
  2013, DOI: 10.1073/pnas.1310156110; Lemak et al. 2013, DOI:
  10.1371/journal.pone.0077020.
- In proliferating systems MLL5 can associate with HCF-1 and stimulate
  E2F1-responsive promoters, and MLL5 protein stability is supported by OGT and
  USP7.  Zhou et al. 2013, DOI: 10.1074/jbc.M112.439729; Ding et al. 2015,
  DOI: 10.1371/journal.pone.0145023.
- Heterozygous disruptive KMT2E variants cause O'Donnell-Luria-Rodan
  neurodevelopmental syndrome with intellectual disability, autism, macrocephaly
  and epilepsy in humans.  O'Donnell-Luria et al. 2019, DOI:
  10.1016/j.ajhg.2019.03.021; Velmans et al. 2021, DOI:
  10.1136/jmedgenet-2020-107470.
- Kmt2e haploinsufficient mice have reported autism-like behavior and amygdala
  abnormalities, but that is a germline/global haploinsufficiency model rather
  than a sparse postnatal neuronal perturbation.  Li et al. 2022, DOI:
  10.1007/s12035-022-03167-w.

## Computational checks

I first loaded the focal-cell training counts to establish the assay scale:
1674 observed perturbations, median `n_degs=0`, 469 nonzero perturbations,
132 perturbations with at least 5 DEGs, and 59 with at least 50 DEGs.  Thus a
developmental chromatin gene does not get a broad signature by default in this
acute postnatal assay.

I then filtered the parquet to `151 TH Prkcd Grin2c Glut` for candidate
KMT2/H3K4/chromatin analogs and counted their `pvals_adj < 0.05` genes.  The
non-obvious part was using Arrow filters so that the full multi-cell-type
parquet did not have to be materialized:

```python
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(analogs)
    & (pc.field("pvals_adj") < 0.05)
)
dataset.to_table(columns=["gene_target", "names", "logfoldchanges",
                          "pvals_adj", "n_pert_matched"],
                 filter=filt)
```

The analog counts in the focal group were:

| observed target | n_pert nuclei | n_degs | target RNA in the DE row |
| --- | ---: | ---: | --- |
| Kmt2a | 161 | 24 | Kmt2a down, padj 1.8e-4 |
| Kmt2c | 55 | 0 | Kmt2c not significant |
| Setd1a | 154 | 368 | Setd1a not significant |
| Ogt | 71 | 4 | Ogt down, padj 1.8e-4 |
| Setd5 | 148 | 9 | Setd5 not significant |
| Crebbp | 61 | 8 | Crebbp not significant |
| Ep300 | 155 | 0 | Ep300 not significant |
| Kat6a | 170 | 0 | Kat6a not significant |
| Kat6b | 150 | 0 | Kat6b not significant |
| Kdm5b | 218 | 0 | Kdm5b not significant |
| Kdm5c | 184 | 18 | Kdm5c not significant |
| Arid1a | 316 | 22 | Arid1a down, padj 0.003 |
| Chd2 | 153 | 34 | Chd2 not significant |
| Chd4 | 163 | 100 | Chd4 not significant |

I also ran a signed-profile comparison among these observed genes.  This
confirmed that there was no single cohesive "chromatin factor" expression state:
Kmt2a, Kmt2c, Setd1a, Ogt and Setd5 had only weak-to-moderate rank agreement,
few or no shared FDR-significant genes, and the Distributed Agents corpus explicitly
curated Kmt2a:F005, Kmt2c:F004, Setd1a:F010 and Setd5:F006 as non-phenocopy
or pathway-uncoupling observations among measured KMT2/H3K4/chromatin
comparators.  The broad Setd1a result therefore looked target-specific, not a
family-wide expectation to transfer onto Kmt2e.

## Target-specific reasoning

### Kmt2e

The closest family-level positive analog is `Kmt2a` with 24 DEGs.  It shares
the KMT2/Trithorax label and is an H3K4 writer relevant to neuronal identity:
its focal signature included down-regulation of `Nr2f1`, `Pcdh7`, `Lhx9`,
`Pcdh10`, `Grik2`, `Camk2d` and `Map1b`.  Kmt2a is useful mainly as an upper
small-effect calibrator, because KMT2E/MLL5 is not a normal MLL1/MLL2 COMPASS
catalytic subunit and the corpus summary Kmt2a:F005 notes that Kmt2a did not
phenocopy the represented H3K4 writer relatives.

The strongest family-level counterexample is `Kmt2c` with 0 DEGs in 151 TH
Prkcd Grin2c Glut, despite being another KMT2-family neurodevelopmental gene.
The same-experiment corpus summarized acute P16 Kmt2c loss as broadly buffered:
15 of 16 measured groups had no downstream FDR<0.10 genes.  That flatness says
that germline enhancer/KMT2 disease relevance is not enough to produce many
postnatal thalamic DEGs under this perturbation strength.

`Setd1a` had 368 DEGs and shows that the assay can report a large H3K4 writer
state.  I treated it as a counterexample rather than as a Kmt2e point anchor:
its significant genes were a mostly down-regulated mitochondrial, GPI-anchor,
ER/proteostasis, UFMylation, ciliary and lysosomal program, and the Distributed Agents
corpus explicitly marked measured KMT2 and chromatin-disorder comparators as
failing to phenocopy Setd1a.  KMT2E also lacks SETD1A's canonical SET1/COMPASS
enzymatic role, so a Setd1a-like count would be an over-transfer.

`Ogt` is mechanistically closer than most chromatin genes because OGT can bind
and stabilize MLL5; it had 4 DEGs, including significant down-regulation of
`Ogt` itself and `Snhg11`.  This is the best low-count positive anchor: it is a
real KMT2E-associated mechanism, but OGT is much broader than KMT2E, so the
shared MLL5 axis is only a small part of the observed Ogt perturbation.

`Setd5`, `Crebbp`, `Ep300`, `Kat6a`, `Kat6b`, `Kdm5b` and `Kdm5c` set the local
range for chromatin/neurodevelopmental genes outside canonical SET1/MLL
catalysis.  Their focal counts were 9, 8, 0, 0, 0, 0 and 18, respectively.
Several had as many or more perturbed nuclei than Kmt2a, so their zeros are not
purely an obvious power failure.  They make a zero-to-teens answer more
plausible for Kmt2e than a hundreds-of-DEGs answer.

Biologically, I expect a nonzero but very narrow signature.  KMT2E is a bona
fide neurodevelopmental disease gene and H3K4me-mark reader, so I would not set
the count to zero.  However, the molecular literature and within-dataset
counterexamples both argue against treating it as Setd1a: much of the published
MLL5/HCF1/E2F1 biology is cell-cycle-coupled, while the experiment perturbed
mostly postmitotic neurons, and the acute mosaic knockdown was much weaker than
human haploinsufficiency or constitutive mouse models.

I therefore predict a small focal response, closest to the Ogt/Setd5/Crebbp
range and well below Kmt2a:

```tsv
target_name	predicted_n_degs
Kmt2e	5
```

## Limits

- There is no observed Kmt2e expression profile or Kmt2e same-experiment
  Distributed Agents finding to transfer directly; the prediction is extrapolation from
  other chromatin regulators.
- Important physical cofactors or paralogs were not in the training count table
  for this focal group, including `Hcfc1`, `Usp7`, `Setd1b`, `Kmt2b`, `Kmt2d`
  and WRAD components such as `Wdr5`, `Rbbp5`, `Ash2l` and `Dpy30`.
- Counts for some analogs, notably Kmt2c and Crebbp, came from only 55 to 61
  perturbed nuclei, so an FDR-zero endpoint can mix true buffering with limited
  power.  Conversely, target-RNA knockdown itself was not always significant
  even for active perturbations, so I did not use target self-down-regulation as
  a strict pass/fail criterion.
- Published KMT2E neurodevelopmental phenotypes come largely from human
  heterozygous germline variants or mouse haploinsufficiency.  This assay is
  acute, sparse, and postnatal with modest average RNA down-regulation, so some
  developmental, progenitor, microglial or network effects are expected to be
  invisible.
