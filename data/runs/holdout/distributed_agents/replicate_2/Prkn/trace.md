# Reasoning trace

## Question and resolved ambiguities

The requested prediction is the FDR<0.05 DEG count in `151 TH Prkcd Grin2c Glut` for each target in the held-out manifest `186_Prkn.csv`. The manifest contains one target:

| requested target | interpretation |
|---|---|
| `Prkn` | mouse Parkin / PARK2 perturbation, held out from both the DE parquet and the focal-cell training count CSV |

I treated the output endpoint exactly as the training CSV defines it: the count is all measured genes with `pvals_adj < 0.05` in the focal group, including the perturbed transcript itself if the self-target row passes FDR. This matters because several focal training perturbations with `n_degs = 1` are one-gene calls consisting only of self-transcript depletion.

## Sources used

- Input DE parquet: `[local file: training_de_all_cell_groups.parquet]`
- Focal training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Held-out manifest: `[local file: 186_Prkn.csv]`
- Internal same-experiment semantic corpus: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`
- Run-local profile tools over the parquet: `profile_compare`, `profile_inspect`, and `profile_table`
- External literature from PubMed:
  - Kitada et al., 1998, Nature, DOI `10.1038/33416`, PMID `9560156`: loss-of-function mutations in `PRKN` cause autosomal recessive juvenile parkinsonism.
  - Narendra et al., 2008, Journal of Cell Biology, DOI `10.1083/jcb.200809125`, PMID `19029340`: Parkin is selectively recruited to damaged mitochondria and promotes their autophagy.
  - Narendra et al., 2010, PLoS Biology, DOI `10.1371/journal.pbio.1000298`, PMID `20126261`: PINK1 accumulates on impaired mitochondria and is necessary and sufficient for Parkin recruitment.
  - Kane et al., 2014, Journal of Cell Biology, DOI `10.1083/jcb.201402104`, PMID `24751536`: PINK1 phosphorylates ubiquitin at Ser65 to activate Parkin E3-ligase activity.
  - Lazarou et al., 2015, Nature, DOI `10.1038/nature14893`, PMID `26266977`: PINK1-generated phospho-ubiquitin recruits mitophagy receptors, with Parkin amplifying the ubiquitin signal.
  - Birsa et al., 2014, Journal of Biological Chemistry, DOI `10.1074/jbc.M114.563031`, PMID `24671417`, and Safiulina et al., 2018, EMBO Journal, DOI `10.15252/embj.201899384`, PMID `30504269`: the mitochondrial trafficking GTPase MIRO1/RHOT1 is a PINK1/Parkin-regulated outer-membrane substrate and docking site.
  - Goldberg et al., 2003, Journal of Biological Chemistry, DOI `10.1074/jbc.M308947200`, PMID `12930822`: germline Parkin-null mice have nigrostriatal functional deficits but no loss of substantia nigra dopaminergic neurons up to 24 months, illustrating the weak basal degeneration phenotype in mice.

## Computation over the supplied data

I first loaded the manifest and the focal training-count CSV. The training endpoint is strongly zero-inflated in `151 TH Prkcd Grin2c Glut`: among 1,674 non-held-out targets, 1,205 had `0` DEGs, the median was `0`, the 75th percentile was `1`, the 90th percentile was `2`, and only a small tail of core processes reached hundreds of DEGs.

I then queried the focal slice of the parquet with DuckDB to recover exact FDR<0.05 calls for mechanistic analogs. The core operation was:

```sql
SELECT gene_target,
       SUM(pvals_adj < 0.05) AS n_degs
FROM read_parquet(...)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
GROUP BY gene_target;
```

and, for selected analogs, I also inspected the exact genes passing the same threshold. Finally, I ran a run-local `profile_compare` on 23 Parkinson, mitochondrial-quality-control, autophagy, and endolysosomal comparators in the focal group. Because `Prkn` was completely held out, that profile run was used only to compare the observed training perturbations with one another; it supplied no hidden `Prkn` readout. The comparison separated many basal Parkinson/autophagy targets with no significant focal profile from positive stress controls such as `Rab7`, `Opa1`, and `Tsc2`.

I also checked the training self-target rows in the focal group. Of 1,642 training targets whose own transcript was measured in `151 TH Prkcd Grin2c Glut`, 319 self rows passed FDR 0.05. In the `n_degs = 1` bin, 237 of 275 one-gene counts were explained by a significant self-transcript row, which confirmed that a prediction of 1 can mean "self transcript only" rather than a downstream state.

## Relevant training perturbations

The nearest biological evidence for `Prkn` was not a large program. Most loss-of-function perturbations around Parkinson genes, mitophagy, basal autophagy, or lysosomal stress were 0 or self-only in the focal cell group.

| training perturbation | 151 TH `n_degs` | focal expression-pattern evidence | use for `Prkn` |
|---|---:|---|---|
| `Park7` | 1 | the only FDR<0.05 focal gene was `Park7` itself; the Distributed Agents corpus reports no downstream response in any neuronal group and no NRF2/UPR/autophagy/mitophagy sentinel program | strongest Parkinson-family basal-null analog; supports no downstream `Prkn` program |
| `Snca` | 0 | no FDR<0.05 genes in 151 TH; the corpus reports a near-pan-neuronal buffer with only one weak downstream hit elsewhere | supports that PD annotation and synaptic/mitochondrial disease biology do not imply an acute thalamic RNA state |
| `Atp13a2` | 1 | only the self transcript passed in 151 TH; the corpus reports no corrected downstream response across neuronal groups and no TFEB, lysosomal, autophagy, UPR/ISR, alpha-synuclein-clearance, or redox panel | lysosomal Parkinson comparator; supports a latent/buffered stress phenotype |
| `Uchl1` | 1 | only the self transcript passed in 151 TH; corpus summaries reject broad ubiquitin, proteasome, UPR, or autophagy activation after acute `Uchl1` loss | proteostasis/Parkinson counterexample; argues against a generic ubiquitin-stress count |
| `Rhot1` | 0 | no focal FDR<0.05 genes | direct MIRO/Parkin-axis substrate; knockout of this outer-mitochondrial trafficking component was transcriptionally silent here |
| `Sqstm1` | 1 | only the self transcript passed in 151 TH | mitophagy/autophagy receptor loss did not create a downstream compensation state |
| `Atg5`, `Atg16l1`, `Lamp2`, `Nfe2l2` | 0, 0, 0, 0 | no focal FDR<0.05 genes | canonical autophagy, lysosomal, and antioxidant regulators were not broad positive analogs |
| `Vps13c`, `Atp13a3`, `Vps35l` | 0, 0, 0 | no focal FDR<0.05 genes | PD/endolysosomal or trafficking relatives; additional null boundaries |
| `Dnajc13` | 1 | only the self transcript passed in 151 TH | endosomal Parkinson-linked comparator; again no downstream state |
| `Vps35` | 17 | significant genes included `Atp2a2`, `Grin2b`, `Vps35`, `Kifc2`, `Rims3`, `Plekhg1`, `Kcnc2`, and other synaptic/membrane genes | useful counterexample, but the corpus assigns it to a branch-specific retromer/synaptic thalamic program rather than PINK1/Parkin mitophagy |
| `Opa1` | 37 | induced an ATF4/ISR-like mitochondrial stress module, with `Asns`, `Chac1`, `Ddit3`, aminoacyl-tRNA synthetases, one-carbon genes, and self `Opa1` among focal calls | positive control proving mitochondrial perturbations can cross the snRNA-seq threshold, but an inner-membrane fusion lesion is too severe and too branch-distinct for basal `Prkn` |
| `Rab7` | 501 | large induction of late-endosomal/lysosomal, sterol, V-ATPase, proteasome, and synaptic-remodeling genes | positive control proving late-endosomal stress is visible; `Prkn` is upstream and damage-gated, not a constitutive `Rab7`-like trafficking block |
| `Hspa5` | 5 | focal UPR-like calls including `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` | positive UPR control; `Park7`, `Atp13a2`, and `Uchl1` did not enter this stress state |
| `Tsc2` | 86 | a sterol/endolysosomal focal response partly related to `Rab7` | mTOR/endolysosomal stress counterexample, not a same-complex `Prkn` analog |
| `Ndufs2`, `Tomm40`, `Mff`, `Cox4i1`, `Yme1l1` | 1, 1, 0, 0, 0 | null or singleton focal profiles | broad mitochondrial membership alone was a poor predictor of the `Opa1`-like stress state |

The run-local profile inspection reached the same conclusion at the FDR-overlap level. The self-only or null Parkinson/autophagy comparators had no shared downstream FDR features with one another, and the large `Rab7`, `Opa1`, and `Tsc2` signatures did not reduce to a shared Parkinson-family module. This made `Vps35`, `Rab7`, and `Opa1` positive assay controls rather than high-count numeric templates for `Prkn`.

## Target-specific call: `Prkn`

`Prkn` encodes the RBR E3 ubiquitin ligase Parkin, the effector of the PINK1/Parkin mitophagy pathway. In the canonical pathway, mitochondrial depolarization stabilizes PINK1 on the outer mitochondrial membrane; PINK1 phosphorylates ubiquitin and Parkin; Parkin then amplifies ubiquitin chains on damaged mitochondria and helps recruit selective autophagy machinery. That mechanism is strongly damage-gated and protein-localization based, so a short, sparse, juvenile, otherwise unstressed CRISPR loss of `Prkn` is not expected to immediately up-regulate hundreds of nuclear lysosome, ISR, or TFEB genes in thalamic glutamatergic neurons.

The within-dataset evidence pushed the prediction toward a near-null count. The PD-family genes with basal loss-of-function profiles in the same assay were mostly `0` or self-only in 151 TH: `Park7 = 1`, `Atp13a2 = 1`, `Snca = 0`, `Uchl1 = 1`, `Rhot1 = 0`, and `Vps13c = 0`. Canonical autophagy and lysosomal loss of `Atg5`, `Atg16l1`, `Lamp2`, and `Nfe2l2` were also zero. `Opa1` and `Rab7` show that the focal cell class can make a mitochondrial ISR or endolysosomal stress transcriptome, but those perturbations are stronger constitutive organelle lesions than `Prkn` loss. `Vps35` had 17 focal DEGs, but the corpus explicitly separates its thalamic retromer/synaptic program from `Snca`, `Park7`, and `Atp13a2`.

I therefore predicted no downstream `Prkn`-driven signature in 151 TH. I did, however, predict one FDR gene rather than a hard zero because the endpoint includes self-transcripts and the training data show many biologically silent perturbations become `n_degs = 1` through their own mRNA. `Prkn` is a measured gene in the focal expression profiles, and it is dynamically detectable: across non-held-out focal perturbations, the `Prkn` measured-gene row passed FDR in 8 strong perturbation backgrounds. Given the self-only behavior of `Park7`, `Atp13a2`, `Uchl1`, `Sqstm1`, and `Dnajc13`, a one-gene self hit was the closest calibrated prediction.

Predicted `Prkn` count: **1**.

## Limits

- `Prkn` itself and the direct upstream kinase `Pink1` were absent as training perturbations, so the central PINK1/Parkin pair had to be extrapolated from adjacent biology.
- Whether `Prkn` mRNA becomes the one FDR hit is guide-, exon-, isoform-, and probe-dependent. Self-transcript loss is useful for predicting this assay's count but is not a quantitative measure of functional knockout strength.
- Parkin biology is largely post-translational recruitment to damaged mitochondria. snRNA-seq at one 3-4 week juvenile time point can miss changes in mitophagic flux, mitochondrial trafficking, axonal organelle quality, or protein ubiquitination.
- The focal cell group is thalamic glutamatergic, not a substantia nigra dopaminergic class; the assay also lacks glial inflammatory phenotypes that can be important in Parkinson models.
- Null FDR surfaces have low information for signature matching. I used them as evidence against large shared programs, not as proof of molecular normality.
