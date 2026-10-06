# Prediction trace

## Question interpreted

The held-out readout is the number of measured genes with `pvals_adj < 0.05`
after sparse AAV CRISPR loss of function of each requested target in
`151 TH Prkcd Grin2c Glut` neurons.  This run has a single held-out target,
`Ust`, from `259_Ust.csv`; the `Ust` perturbation itself is absent from both
the differential-expression parquet and the focal-cell training count CSV, so
the prediction must be transferred from non-held-out perturbations.

I treated `n_degs` as the assay-specific FDR count in this cell group, not as a
generic measure of gene essentiality, disease relevance, editing efficiency, or
glycosaminoglycan biochemical disruption.

## Sources used

- Training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training signatures:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested targets:
  `[local file: 259_Ust.csv]`.
- Distributed Agents corpus MCP release
  `perturbai-july-260713-sourceguard-1773-v1`, especially the target contexts
  for `B3gat3`, `Ext1`, `Ext2`, `Glce`, `Gpc6`, `Hs6st2`, and `Xylt1`.
- Distributed Agents Runtime profile-neighbor analysis over the focal-cell parquet,
  written to `ust_gag_profile_neighbors.json`.
- PubMed-indexed UST and chondroitin/dermatan-sulfate literature:
  Kobayashi et al. 1999, DOI 10.1074/jbc.274.15.10474, PMID 10187838;
  Ohtake et al. 2005, DOI 10.1074/jbc.M508816200, PMID 16192264;
  Ishii and Maeda 2008, DOI 10.1074/jbc.M806331200, PMID 18819920;
  Ishii and Maeda 2008, DOI 10.1093/glycob/cwn040, PMID 18480156;
  Mikami and Kitagawa 2013, DOI 10.1016/j.bbagen.2013.06.006,
  PMID 23774590;
  Nikolovska et al. 2015, DOI 10.1242/jcs.152660, PMID 25480151.

## Computational steps

1. Loaded the requested-target CSV and confirmed it contains exactly one target:
   `Ust`.
2. Loaded the focal-cell training count CSV.  It contains 1,674 non-held-out
   perturbations; 1,205 of them have `n_degs = 0`, the median is 0, the 75th
   percentile is 1, and the 90th percentile is 2.  Thus a zero prediction is
   common in this cell group and a nonzero prediction needs a specific positive
   analog.
3. Intersected known proteoglycan and glycosaminoglycan synthesis/modification
   genes with the focal-cell training targets.  The closest represented
   enzymatic comparators were the common GAG linker enzymes `Xylt1` and
   `B3gat3`, the heparan-sulfate polymerase genes `Ext1` and `Ext2`, and the HS
   modification genes `Glce` and `Hs6st2`.  Direct CS/DS sulfotransferase
   neighbors such as `Chst3`, `Chst7`, `Chst11`, `Chst12`, `Chst14`,
   `Chst15`, `Dse`, `Dsel`, `Papss1`, `Papss2`, and `Slc35b2` were not in the
   training target universe.
4. Filtered the parquet to
   `group_name == "151 TH Prkcd Grin2c Glut"` and
   `gene_target in {B3gat3, Ext1, Ext2, Glce, Hs6st2, Xylt1}`.  This yielded
   103,554 differential-expression rows, with 155 to 238 matched perturbed
   nuclei per analog and 23,679 matched controls.  Every comparator had zero
   genes at `pvals_adj < 0.05` in the focal cell group.
5. Ran `profile_neighbors` with those six anchors against all 1,674 eligible
   observed perturbations in the focal group, using `logfoldchanges` as the
   signed profile value and `pvals_adj < 0.05` to define significant signed
   tails.  This was a coherence check, not a selection rule.  The anchors had
   no FDR-supported tail genes and their nearest profiles did not expose a
   recurrent non-null CS/GAG transcriptional state that would argue for a small
   positive `Ust` count.
6. Checked focal counts for obvious downstream or partner readouts.  `Fgfr1`,
   `Fgfr2`, `Fgfr3`, `Fgf1`, `Smo`, `Ptch1`, `Gli1`, `Gli2`, `Slit2`,
   `Robo2`, and `Robo4` were all zero in the same training endpoint, while
   `Robo1` and the sulfation-related `Bpnt2` were only 1.  This makes a broad
   FGF/Hedgehog/Slit-Robo feedback response to a single GAG enzyme perturbation
   unlikely in this focal group, even though a positive Wnt effector control,
   `Ctnnb1`, was easily detectable at 383 DEGs.

## Relevant within-dataset analogs

| target | focal `n_degs` | why it was compared with `Ust` | expression-pattern evidence |
| --- | ---: | --- | --- |
| `Xylt1` | 0 | Initiates the xylose linker needed for CS/DS and HS chains, upstream of all proteoglycan GAG modification. | Zero focal DEGs; the Distributed Agents corpus calls `Xylt1` a pan-neuronal null in this P16 sparse CRISPR snRNA-seq assay and reports no shared `Xylt1`-like module across `B3gat3`, `Ext1`, and `Ext2`. |
| `B3gat3` | 0 | Completes the common GAG tetrasaccharide linker upstream of both CS/DS and HS chain addition. | Zero focal DEGs.  Corpus findings describe only a two-gene response in one striatal GABA group elsewhere and no compensatory GAG enzyme or stress-module transcriptional feedback. |
| `Ext1` | 0 | Catalytic HS polymerase component; not a CS enzyme, but a strong test of whether disrupting proteoglycan glycan-chain assembly generates a postnatal neuronal RNA state. | Zero focal DEGs.  Same-experiment corpus findings report no downstream FDR-level response across recovered neuronal classes and failure to induce expected HS, FGF/ERK, Hedgehog, Wnt, Eph, or Slit/Robo reporters. |
| `Ext2` | 0 | Same HS polymerase complex as `Ext1`; a pathway-near counterexample for acute loss of a Golgi glycosyltransferase. | Zero focal DEGs.  Corpus findings show that even the sparse `Ext2` events observed in other glutamatergic groups did not phenocopy `Ext1`, `Xylt1`, `B3gat3`, `Glce`, `Hs6st2`, or `Gpc6`. |
| `Glce` | 0 | HS C5 epimerase, a sulfation-pattern modifier downstream of HS polymerization. | Zero focal DEGs.  The Distributed Agents corpus reports a zero-FDR transcriptional surface across 22 recovered neuronal groups and no hidden FGF/Hedgehog/Wnt/axon-guidance marker program. |
| `Hs6st2` | 0 | HS 6-O-sulfotransferase; chemically and Golgi-localized like `Ust`, though acting on HS rather than CS/DS. | Zero focal DEGs.  Corpus findings report no robust downstream response in any measured cell group and no convergence with `Ext1`, `Ext2`, or represented `Fgfr` perturbations. |
| `Gpc6` | 0 | Heparan-sulfate proteoglycan core protein, not an enzyme, included as a pathway boundary. | Zero focal DEGs.  Corpus findings report a pan-tested neuronal null and no latent GPC6-like guidance module among HS-biosynthesis or Slit/Robo relatives. |

The most important shared fact is not that all these genes are identical to
`Ust`; they are not.  The important within-experiment fact is that several
ways of perturbing proteoglycan GAG synthesis or sulfation in postmitotic
neuronal nuclei were flat in `151 TH Prkcd Grin2c Glut`, and the Distributed Agents
same-experiment claim layer summarizes them as a high-confidence negative
module rather than as a coherent hidden response.

## Biology of `Ust`

`Ust` encodes uronyl 2-O-sulfotransferase, a type II Golgi enzyme that
transfers sulfate to the 2-position of iduronic acid residues in dermatan
sulfate and, less efficiently, glucuronic acid residues in chondroitin sulfate
proteoglycans (Kobayashi et al. 1999).  UST/2OST preferentially recognizes
specific CS sulfation contexts around the acceptor uronic acid (Ohtake et al.
2005), and reviews of CS biosynthesis place it in the set of enzymes that
diversify CS/DS chains after the common linker has been built and the CS
polymer has been elongated (Mikami and Kitagawa 2013).

The external literature gives `Ust` real developmental and signaling relevance.
UST and other CS sulfotransferases are expressed in the embryonic neocortical
ventricular/subventricular zones, and in utero UST knockdown disrupts radial
migration of cortical neurons (Ishii and Maeda 2008, JBC).  UST expression and
UST-generated B/D CS units also rise during postnatal cerebellar development
(Ishii and Maeda 2008, Glycobiology).  In cultured fibroblast-like systems,
UST-dependent CS/DS 2-O-sulfation can tune FGF2 binding, ERK activation, and
cell migration (Nikolovska et al. 2015).  These data make `Ust` biologically
credible, but they point primarily to glycan structure, extracellular ligand
binding, migration, and matrix/synapse biology.

## Target-specific prediction

### Ust

**Prediction: 0 DEGs.**

The positive biological prior is that UST alters oversulfated CS/DS motifs that
can influence developmental migration and FGF-dependent behavior.  I therefore
looked first for assayed CS/DS sulfotransferases, PAPS supply genes, and direct
paralogs, but those were absent from the training universe.  The best available
single-gene training analogs were upstream GAG linker enzymes and related HS
modification enzymes.  They are all imperfect, because `Ust` modifies CS/DS
whereas `Ext1`, `Ext2`, `Glce`, and `Hs6st2` are HS-specific; nevertheless
`Xylt1` and `B3gat3` sit upstream of both CS/DS and HS, and all six close
enzymatic analogs had `n_degs = 0` in the focal cell group.

The same-experiment corpus also argues against a nonzero rescue by pathway
analogy.  Its high-confidence claim over `B3gat3`, `Bpnt2`, `Ext1`, `Ext2`,
`Glce`, `Gpc6`, `Hs6st2`, and `Xylt1` states that represented
GAG/heparan-sulfate/proteoglycan perturbations did not collapse into a common
acute postnatal neuronal transcriptional module.  `Ust` should be at least as
likely as these genes to act through extracellular sulfation patterns rather
than through a rapid cell-autonomous nuclear stress program.  In the focal
endpoint, even candidate FGF/Hedgehog/Slit-Robo neighbors were nearly all zero.

I therefore predict that sparse post-P16 `Ust` loss in `151 TH Prkcd Grin2c
Glut` cells will not produce any gene passing Benjamini-Hochberg FDR 0.05.  A
tiny one- or two-gene hit is possible given the assay noise and the training
distribution, but the closest mechanistic training evidence supports the exact
zero.

## Limits and extrapolation

- `Ust` was held out, so there is no direct same-experiment `Ust` expression
  signature or target-RNA knockdown measurement.
- The training set lacked the nearest CS/DS sulfotransferases and PAPS
  transport/metabolism genes, so most observed analogs are shared-linker or
  HS-pathway genes, not direct CS/DS 2-O-sulfation paralogs.
- The endpoint is snRNA-seq differential expression.  It does not measure CS/DS
  sulfation, perineuronal-net composition, extracellular matrix turnover,
  ligand binding, dendritic spines, axon migration, or electrophysiology.
- The assay perturbs sparse postmitotic juvenile neurons.  Embryonic
  ventricular-zone UST knockdown and glial or matrix-rich phenotypes could be
  missed, especially because this dataset is NeuN-enriched and under-samples
  non-neuronal populations.
- DEG count is power dependent.  I used the matched training counts and the
  observed focal distribution only to calibrate the point estimate; the
  prediction remains an extrapolation from nearby GAG perturbations to a CS/DS
  sulfotransferase that was completely held out.
