# Dnajc6 held-out DEG-count prediction

## Question interpreted

The requested readout is the integer number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after each held-out
CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` neurons.
The manifest for this run contains one target:

```tsv
target_name
Dnajc6
```

I treated the training count CSV as the exact focal-cell endpoint and the
parquet as the source of signed expression evidence for non-held-out
perturbations. Counts include the target transcript itself when it is measured
and significantly reduced, so a one-DEG endpoint can mean "target self only"
rather than a downstream cell-state response.

## Sources used

- Training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Full training DE table:
  `[local file: training_de_all_cell_groups.parquet]`
- Requested held-out manifest:
  `[local file: 058_Dnajc6.csv]`
- Distributed Agents same-experiment corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, queried for `Dnajc6` and for
  the in-dataset comparator targets `Dnajc5`, `Dnajc13`, `Hspa8`, `Cltc`,
  `Dnm1`, `Synj1`, `Vps35`, and `Rab7`.
- Distributed Agents runtime profile comparison, using the focal-cell `logfoldchanges`
  vectors and `pvals_adj < 0.05` feature calls for declared comparator targets.
  The lossless outputs are `dnajc6_comparator_profile.json`,
  `dnajc6_primary_inspect.json`, and `dnajc6_boundary_inspect.json`.
- NCBI PubMed literature for auxilin/DNAJC6 mechanism and disease context.

Key outside references:

- Yim et al. 2010, PNAS, DOI `10.1073/pnas.1000738107`, PMID `20160091`:
  auxilin knockout mice accumulate clathrin-coated vesicles/empty cages at
  synapses and have impaired synaptic-vesicle endocytosis; GAK is up-regulated
  and can partially compensate.
- Edvardson et al. 2012, PLoS ONE, DOI `10.1371/journal.pone.0036458`,
  PMID `22563501`: biallelic DNAJC6 mutation with reduced DNAJC6 mRNA causes
  juvenile parkinsonism; DNAJC6 encodes the neuronally enriched Hsp40 auxilin,
  an Hsc70 specificity factor for clathrin uncoating.
- Gorenberg and Chandra 2017, Frontiers in Neuroscience, DOI
  `10.3389/fnins.2017.00248`, PMID `28579939`: review of the synaptic Hsp40
  co-chaperones DNAJC5/CSPalpha, DNAJC6/auxilin, and DNAJC13/RME-8.
- Wulansari et al. 2021, Science Advances, DOI `10.1126/sciadv.abb1540`,
  PMID `33597231`; Vidyadhara et al. 2023, Cell Reports, DOI
  `10.1016/j.celrep.2023.112231`, PMID `36920906`; and Abela et al. 2024,
  Brain, DOI `10.1093/brain/awae020`, PMID `38242634`: full DNAJC6 loss has
  strong developmental, dopaminergic, synaptic-vesicle recycling, dopamine
  transporter sorting, and Parkinson-related phenotypes in organoid, iPSC,
  or whole-animal systems.

## Computational checks over the training data

1. I confirmed that `Dnajc6` is the only row in the requested-target manifest
   and that it is absent from the 1,674-row focal training count table.

2. The focal endpoint is extremely zero inflated. Across the 1,674 visible
   training perturbations, 469 were nonzero, the median count was 0, the 75th
   percentile was 1, the 90th percentile was 2, and only 43 perturbations had
   at least 100 DEGs. Therefore a prediction of one DEG is already a real,
   above-median focal-cell response in this assay.

3. The parquet is row-group sorted by `group_name`. I read row groups 546-580,
   the row groups overlapping `151 TH Prkcd Grin2c Glut`, and retained focal
   rows for Dnajc6-relevant comparators:

```python
for rg in range(546, 581):
    rows = parquet.read_row_group(rg, columns=[
        "names", "group_name", "gene_target", "logfoldchanges",
        "pvals_adj", "scores", "n_pert_matched", "n_ctrl_matched",
    ])
    keep focal rows where gene_target is in the curated comparator set
```

   This produced 17,259 measured genes for each of 18 comparator perturbations.
   The significant rows were also saved as a compact local audit in
   `dnajc6_candidate_focal_rows.tsv`.

4. I compared the same 18 signed focal profiles with the Distributed Agents runtime
   `profile_compare` tool. The most relevant output was not the all-gene
   log-fold-change correlation, which can be uninformative for near-null
   signatures, but the FDR-supported activity class and exact overlap of
   significant features. Among the direct Dnajc6 analogs, no FDR 0.05 genes
   overlapped with the larger `Cltc`, `Vps35`, or `Rab7` programs except for
   three `Hspa8`/`Rab7` chaperone-tail genes.

## Comparator evidence for Dnajc6

`Dnajc6` encodes auxilin, a J-domain co-chaperone that recruits Hsc70 to uncoat
clathrin-coated synaptic vesicles. The closest perturbation classes in the
training set were therefore not generic Parkinson genes, but synaptic-vesicle
endocytosis/uncoating genes, Hsc70/Hsp40 co-chaperones, and clathrin/endosomal
counterexamples.

| training target | focal `n_degs` | focal FDR 0.05 pattern | how I used it |
| --- | ---: | --- | --- |
| `Dnm1` | 1 | only `Dnm1` itself, down; no downstream genes | Very close presynaptic-vesicle fission neighbor. The Distributed Agents corpus reports pervasive Dnm1 target-transcript engagement without a downstream neuronal RNA program, bounding severe vesicle-recycling genes that nevertheless stay soma-transcriptionally flat in this assay. |
| `Synj1` | 1 | only `Synj1` itself, down | Very close uncoating/phosphoinositide neighbor. The corpus records shared downstream-flat behavior with `Dnm1` and lack of convergence with `Cltc`. This is probably the best pathway-position analog for auxilin because Synj1 also acts after coated vesicle formation rather than at the bulk endosomal lysosome. |
| `Dnajc5` | 1 | only `Dnajc5` itself, down | Synaptic Hsp40 co-chaperone comparator. DNAJC5/CSPalpha acts with Hsc70 at presynaptic terminals, but the same-experiment corpus found only a restricted one-gene Dnajc5 surface and no heat-shock, ISR, autophagy, lysosomal, or Cltc-like response. |
| `Dnajc13` | 1 | only `Dnajc13` itself, down | RME-8 is another clathrin/endosomal DNAJ protein. Its one-hit focal response and corpus findings argue that DNAJ identity or Parkinson linkage is not enough to imply a broad response. |
| `Hspa8` | 9 | five up, four down; `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1`, `Cct6a` up and `Fras1`, `Unc79`, `Leng8`, `Apba2` down | Hsc70 is the direct chaperone partner of auxilin, but its perturbation produced a small chaperone counterinduction state, not a vesicle-uncoating state. It is a useful upper bound for an Hsc70-axis secondary response. |
| `Cltc` | 3 | weak focal response: `Gabra4`, `Rbms1`, `Ero1b`, all down | Core clathrin is a counterexample showing that the dataset can detect clathrin-axis damage. In this focal group it was still small, and the corpus explicitly reports that `Hspa8`, `Dnm1`, `Synj1`, `Nsf`, `Dnajc5`, and `Bin1` did not phenocopy the broader Cltc response in matched neurons. |
| `Stxbp1` | 1 | only `Stxbp1` itself, down | Exocytic SNARE/Munc18 neighbor. Less mechanistically close than Dnm1/Synj1 but informative because many presynaptic release-cycle genes counted only their own depletion in 151. |
| `Nsf` | 0 | no FDR genes | Vesicle-fusion ATPase counterexample: loss of an important synaptic-vesicle-cycle gene can be completely FDR-flat. |
| `Ap1b1` | 1 | only `Ap1b1` itself, down | Clathrin adaptor-tier counterexample; a clathrin-adjacent perturbation need not reproduce Cltc. AP-2, the most direct auxilin adaptor context, was absent from the training target universe. |
| `Vps35` | 17 | 17 genes including `Vps35` down, `Atp2a2` down, `Grin2b` down, `Brsk1` up, `Rims3` down | Retromer branch counterexample. Vps35 has a modest 151 response, but the Distributed Agents corpus found that `Dnajc13` and `Synj1` failed to phenocopy it and that the signature was selective membrane/synaptic remodeling rather than a generic endolysosomal program. |
| `Rab7` | 501 | broad lysosome/sterol/proteostasis response including `Atp6v1b2`, `Dpp7`, `Insig1`, `Atp6v0b`, `Lamp2`, `Sqstm1`, `Grn`, and `Mcoln1` up | Strong boundary, not a poolable analog. It proves that the focal cell type can mount a large endolysosomal stress response, but Dnajc6 acts at presynaptic clathrin uncoating and its closest measured neighbors do not enter this Rab7 state. |
| `Atp6v0a1`, `Atp6v1a`, `Lamp2`, `Becn1`, `Atg5`, `Vps35l`, `Washc4` | 0-1 | zero or target-self-only | These autophagy, lysosomal, vacuolar-ATPase, Retriever, and WASH comparators were used as rejection controls against projecting a broad lysosome/autophagy DEG count onto Dnajc6. |

The best mechanistic comparators `Gak`, `Snap25`, `Sgta`, `Clta`, `Cltb`,
and the AP-2 subunits were not present as perturbation targets in the focal
training-count universe, so I could not directly test GAK compensation or the
full auxilin uncoating complex.

## Target-specific prediction

I predict that `Dnajc6` will have a tiny but nonzero focal signature:
`predicted_n_degs = 1`.

The nonzero call is driven mostly by exact within-dataset calibration. In the
151 focal group, four of the most relevant synaptic/Hsp40/endocytic analogs
were one-DEG perturbations whose only FDR gene was the target transcript:
`Dnajc5`, `Dnajc13`, `Dnm1`, and `Synj1`. `Ap1b1`, `Atp6v0a1`, and `Stxbp1`
show the same target-self-only shape. Because `Dnajc6` itself is in the 17,259
measured-gene feature space, auxilin self-depletion is countable if the guides
reduce its transcript sufficiently.

I do not expect a `Rab7`- or `Vps35`-like secondary program. The close
presynaptic-vesicle branch, `Dnm1` and `Synj1`, both stayed downstream-flat
despite severe known vesicle-recycling physiology. The Hsc70 branch was small
and qualitatively chaperone-like after `Hspa8`, while `Dnajc5` and `Dnajc13`
showed no HSP/ISR/autophagy or lysosomal response. External literature says
full auxilin loss is biologically important, particularly in development and
in dopaminergic systems, but those phenotypes are produced by complete genetic
loss or chronic disease contexts rather than 3-4 weeks of sparse postnatal CRISPR
in thalamic glutamatergic neurons. The closest same-experiment signatures
therefore argue for target self-depletion without a broad nuclear stress state.

## Limits

- `Dnajc6` itself was held out, and the Distributed Agents same-experiment corpus had no
  `Dnajc6` target node, so the prediction is an extrapolation from neighbors.
- Auxilin's closest compensator, `Gak`, and the AP-2 adaptor subunits were not
  in the focal target universe; this prevents a direct same-complex epistasis
  comparison.
- The 151 focal `Cltc` count was only 3 with 32 perturbed nuclei. Cltc was much
  broader in other neuronal groups, so it establishes assay sensitivity to
  clathrin damage but is an imperfect effect-size analog for Dnajc6.
- snRNA-seq at the nucleus does not directly measure clathrin-coated vesicles,
  synaptic-vesicle recycling, dopamine transporter sorting, autophagic flux, or
  electrophysiology. A one-DEG prediction should not be read as "no auxilin
  biology"; it means the expected 151-cell nuclear DEG count at FDR 0.05 is
  approximately one in this sparse P16-to-P37/P44 loss-of-function assay.
