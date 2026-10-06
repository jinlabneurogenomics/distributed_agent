# Reasoning trace

## Question and resolved ambiguities

The requested endpoint is a point prediction for the held-out perturbation
`Ndufa13` in `151 TH Prkcd Grin2c Glut` neurons. The integer to predict is the
number of measured genes with Wilcoxon Benjamini-Hochberg adjusted
`pvals_adj < 0.05` for the held-out knockout.

I treated the endpoint exactly as counted in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the count includes the
perturbed gene's own mRNA when that row is FDR-significant. I did not treat
unchanged target RNA as evidence of guide failure, because the experiment is an
acute, sparse, postnatal CRISPR assay where target-transcript depletion is only
a limited QC readout.

The requested-target manifest contained one held-out target:

| target_name |
| --- |
| Ndufa13 |

## Sources used

- Supplied count table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Supplied differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Supplied manifest:
  `[local file: 145_Ndufa13.csv]`
- PerturbAI atlas dataset portrait `perturbai-atlas-v5`.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. I used this only for training
  perturbations: the release had no `Ndufa13` finding or claim contribution.
- Distributed Agents runtime signed-profile comparison in the focal cell group for
  observed `Nduf*` complex I subunits and assembly factors.
- External biology from MitoCarta3.0, plus PubMed-indexed primary literature on
  NDUFA13/GRIM-19 and mitochondrial complex I:
  - Rath et al. 2021, MitoCarta3.0, DOI `10.1093/nar/gkaa1011`, PMID
    `33174596`.
  - Lufei et al. 2003, GRIM-19 as a STAT3-interacting negative regulator, DOI
    `10.1093/emboj/cdg135`, PMID `12628925`.
  - Lu and Cao 2008, GRIM-19/NDUFA13 requirement for complex I electron
    transfer and mitochondrial membrane potential, DOI
    `10.1091/mbc.e07-07-0683`, PMID `18287540`.
  - Chen et al. 2012, mouse GRIM-19 haploinsufficiency reducing complex I
    activity and changing ROS/cytokine behavior in macrophages, DOI
    `10.1074/jbc.M112.340315`, PMID `22665480`.
  - Angebault et al. 2015, human NDUFA13/GRIM19 variants causing isolated
    complex I deficiency and neurologic disease, DOI `10.1093/hmg/ddv133`,
    PMID `25901006`.
  - Kaiyrzhanov et al. 2024, an expanded NDUFA13 disease series showing
    reduced complex I activity and neurodevelopmental phenotypes, DOI
    `10.1093/braincomms/fcae453`, PMID `39963288`.

## Computational steps

1. Read the requested-target CSV and confirmed that the only held-out
   perturbation was `Ndufa13`.
2. Loaded the focal-cell training count CSV with pandas and extracted exact
   DEG counts for respiratory-chain and adjacent mitochondrial perturbations.
   This is the authoritative source for the endpoint distribution in the focal
   class.
3. Used `pyarrow.dataset` to scan only rows satisfying:

   ```python
   (group_name == "151 TH Prkcd Grin2c Glut")
   & gene_target.isin(respiratory_chain_targets)
   & (pvals_adj < 0.05)
   ```

   This gave the actual significant measured genes for the candidate analogs,
   not just their total `n_degs`.
4. Ran a Distributed Agents signed-profile comparison over all 23 observed
   `Nduf*`/`Ndufaf*`/`Ndufa4` training perturbations in
   `151 TH Prkcd Grin2c Glut`. The comparison used `logfoldchanges` as the
   signed value, `names` as features, `gene_target` as the profiled entity, and
   `pvals_adj < 0.05` as the significance threshold. It was used as a check for
   hidden coherent signature similarity among nominally sparse complex I
   perturbations.
5. Queried the Distributed Agents same-experiment corpus for curated complex I findings
   involving training perturbations. The release-level high-confidence claim
   `claim:46019c530f79c38141a7` states that represented nuclear-encoded
   complex I subunit and assembly-factor perturbations were broadly buffered at
   the postnatal neuronal nuclear-transcriptome level and did not form a shared
   acute OXPHOS-stress module.

## Dataset evidence for Ndufa13 analogs

`Ndufa13` is itself a nuclear-encoded mitochondrial complex I subunit according
to MitoCarta3.0 and the GRIM-19 complex I literature. Therefore the most direct
within-dataset analogs are the other nuclear complex I subunits in the focal
count table.

Exact focal-cell counts for observed `Nduf*` complex I subunit perturbations
were:

| training target | n_degs | focal significant row(s) | interpretation for Ndufa13 |
| --- | ---: | --- | --- |
| Ndufa10 | 1 | `Ndufa10` down | Self-transcript-only complex I hit. |
| Ndufa6 | 1 | `Ndufa6` down | Self-transcript-only complex I hit. |
| Ndufb10 | 1 | `Ndufb10` down | Self-transcript-only complex I hit. |
| Ndufb11 | 1 | `Ndufb11` down | Self-transcript-only complex I hit. |
| Ndufb8 | 1 | `Ndufb8` down | Self-transcript-only complex I hit. |
| Ndufb9 | 1 | `Ndufb9` down | Self-transcript-only complex I hit. |
| Ndufc2 | 1 | `Ndufc2` down | Self-transcript-only complex I hit. |
| Ndufs2 | 1 | `Ndufs2` down | Self-transcript-only core-complex I hit. |
| Ndufs8 | 1 | `Ndufs8` down | Self-transcript-only complex I hit. |
| Ndufv2 | 1 | `Cdc40` up | Singleton off-target/downstream row; no broad OXPHOS module. |
| Ndufa8 | 0 | none | Quiet accessory subunit boundary. |
| Ndufa9 | 0 | none | Quiet accessory subunit boundary. |
| Ndufa11 | 0 | none | Quiet accessory subunit boundary. |
| Ndufa12 | 0 | none | Quiet accessory subunit boundary. |
| Ndufb3 | 0 | none | Quiet accessory subunit boundary. |
| Ndufb7 | 0 | none | Quiet accessory subunit boundary. |
| Ndufs4 | 0 | none | Quiet disease-associated complex I boundary. |
| Ndufs7 | 0 | none | Quiet core-complex I boundary. |
| Ndufv1 | 0 | none | Quiet core-complex I boundary. |

The same sparse pattern extended to nearby complex I assembly factors:
`Ndufaf2 = 0`, `Ndufaf4 = 0`, `Ndufaf5 = 0`, and `Timmdc1 = 0` in the focal
count table. It also extended across much of the rest of the observed
respiratory chain: most `Cox*` and `Uqcr*` perturbations had zero or one DEG,
`Sdha = 1`, `Tomm40 = 1`, and `Coa8`/`Lrpprc` were zero.

The parquet scan made the count pattern biologically sharper. Nine of the
singleton complex I subunit calls were just the knocked-out transcript passing
FDR; the only singleton that was not self RNA was `Ndufv2`, whose lone focal
row was `Cdc40`. That argues against predicting a broad downstream
mitochondrial-stress state for `Ndufa13`; the realistic alternatives are 0 or
1 total DEG.

As a counterexample, `Opa1` had 37 DEGs in the same focal cell group and
up-regulated `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2`, `Slc7a5`, and other
amino-acid or integrated-stress transcripts while down-regulating `mt-Co2`.
Thus `151 TH Prkcd Grin2c Glut` has enough power to detect a mitochondrial
stress program when one appears. The lack of a similar pattern across observed
NDUF/NDUFAF perturbations is not simply a property of all mitochondrial genes.

The Distributed Agents profile comparison reached the same conclusion from expression
patterns rather than counts alone. Among 23 observed NDUF/NDUFAF/NDUFA4
perturbations in the focal class, 12 had no significant features and 11 had
only 1 to 9 significant features; no member carried a recurrent OXPHOS,
ATF4-like, UPRmt, or mitophagy signature. Corpus findings for `Ndufa10`,
`Ndufs4`, `Ndufa11`, `Ndufs2`, `Ndufb10`, `Ndufb11`, `Ndufv2`, and `Timmdc1`
all used same-complex contrasts and summarized the family as flat, sparse, and
non-convergent in this postnatal neuronal snRNA-seq assay.

## Target-specific prediction

### Ndufa13

External functional prior: Ndufa13/GRIM-19 is a bona fide complex I subunit.
Mutational and knockdown studies show that it can affect complex I assembly,
complex I activity, mitochondrial membrane potential, ROS biology, and human
neurodevelopmental complex I disease (Lu and Cao 2008; Chen et al. 2012;
Angebault et al. 2015; Kaiyrzhanov et al. 2024). Lufei et al. 2003 also
established a STAT3-regulatory interaction for GRIM-19, so Ndufa13 has
non-respiratory signaling annotations as well.

Within-dataset transfer: despite that strong biochemical prior, the appropriate
training perturbations are the observed complex I subunits and assembly
factors, not broad mitochondrial stress responders. In the exact complex I
subunit set above, no target exceeded one focal DEG and there was no shared
secondary response. Core subunits that should stress the enzyme if fully
removed, including `Ndufs2`, `Ndufs7`, `Ndufv1`, `Ndufv2`, and `Ndufs8`, were
still either zero or singleton in this endpoint. Accessory subunits closer to
`Ndufa13`, such as `Ndufa8`, `Ndufa9`, `Ndufa10`, `Ndufa11`, and `Ndufa12`, gave
the same 0/1 behavior.

Zero/nonzero decision: I predict a nonzero singleton rather than a hard zero
because exact `Nduf*` structural subunits were just over half nonzero in the
focal count table, and when they were nonzero the significant feature was
usually the target transcript itself. `Ndufa13` is expressed enough in neurons
to be an OXPHOS disease gene and complex I component, so the best point
estimate is that the assay detects the cognate transcript, but not a
downstream module.

Point prediction: `predicted_n_degs = 1`.

## Limits

This is an extrapolation from paralogous/same-complex training targets; there
was no direct Ndufa13 record in the supplied DE parquet, training count CSV, or
Distributed Agents corpus. The observed NDUF analogs sit almost exactly on the 0/1
boundary, so the call depends on whether the held-out guides produce a
measurable FDR-significant self-transcript row. I did not have direct editing,
protein, respiration, or per-nucleus abundance measurements for the held-out
target.

The comparison is also endpoint-specific. NDUFA13 loss can be biochemically
important in germline disease, fibroblasts, cardiac models, macrophages, and
cancer cells, but those systems are much stronger or longer perturbations than
P16 sparse AAV CRISPR in surviving postmitotic neuronal nuclei. The prediction
therefore says only that this snRNA-seq DEG count should be a singleton, not
that Ndufa13 is biologically dispensable.
