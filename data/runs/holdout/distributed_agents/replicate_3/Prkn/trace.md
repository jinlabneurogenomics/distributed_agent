# Prkn held-out DEG-count prediction

## Question and interpretation

The requested manifest contains one held-out target, `Prkn`. I interpreted the
task as predicting the exact integer `n_degs` that would have been observed for
acute sparse CRISPR loss of `Prkn` in `151 TH Prkcd Grin2c Glut` neurons, where
`n_degs` counts measured genes with Benjamini-Hochberg adjusted Wilcoxon
`pvals_adj < 0.05` in the focal cell group.

Two details mattered for the prediction:

- The held-out perturbation itself is absent as a training perturbation, but
  `Prkn` can still appear as a measured RNA in other perturbation signatures.
- A count of `1` often means only the target transcript crossed FDR, not that a
  downstream program was induced. I therefore separated the expected downstream
  state from the chance that the `Prkn` transcript itself would be called.

## Sources used

- `[local file: 186_Prkn.csv]`
  supplied the exact target list and order: `Prkn`.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  supplied the observed focal-cell DEG counts for 1,674 non-held-out training
  perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  supplied the focal-cell differential expression rows used to inspect which
  genes were actually significant under the analog perturbations.
- Internal Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`
  supplied same-experiment Claims and Findings over the non-held-out targets.
  `Prkn` itself was not in the corpus, as expected for a held-out target.
- PubMed literature was used for the external mechanism of PRKN/Parkin:
  Narendra et al. 2008, DOI `10.1083/jcb.200809125`, PMID `19029340`;
  Matsuda et al. 2010, DOI `10.1083/jcb.200910140`, PMID `20404107`;
  Koyano et al. 2014, DOI `10.1038/nature13392`, PMID `24784582`;
  Lazarou et al. 2015, DOI `10.1038/nature14893`, PMID `26266977`;
  Kitada et al. 2009, DOI `10.1111/j.1471-4159.2009.06350.x`, PMID
  `19694908`; Pickrell et al. 2015, DOI `10.1016/j.neuron.2015.06.034`, PMID
  `26182419`; Song et al. 2016, DOI `10.1523/JNEUROSCI.2569-15.2016`, PMID
  `26911690`; Martinez et al. 2017, DOI `10.1186/s13024-017-0170-3`, PMID
  `28399880`.

## Computational steps over the input data

1. Read the manifest. It had exactly one target row, `Prkn`.
2. Loaded the focal-cell training count CSV and checked the empirical scale of
   the endpoint: 1,674 training targets, median `n_degs = 0`, maximum `2677`,
   with `72.0%` of targets at zero and `88.5%` at one DEG or fewer.
3. Used parquet row-group statistics to restrict extraction to
   `151 TH Prkcd Grin2c Glut`, then pulled the DE rows for Parkinson,
   mitophagy/autophagy, endolysosomal, and mitochondrial quality-control
   analogs.
4. For each analog, counted or inspected its FDR genes and verified whether the
   single-gene calls were self-transcript calls. In the whole focal-cell
   training set, 319 of 1,642 represented targets had their own transcript pass
   FDR 0.05; 237 of those had exactly one DEG overall.
5. Queried the Distributed Agents same-experiment corpus for claims and findings around
   Parkinson-family, mitochondrial-stress, retromer, and late-endosomal
   perturbations to avoid transferring signatures across genes that the dataset
   itself had already separated.

## Biologically relevant training comparisons

| training perturbation | observed `n_degs` in 151 TH | focal-cell expression evidence | relevance to `Prkn` |
| --- | ---: | --- | --- |
| `Park7` | 1 | The only focal hit was `Park7` down, log2FC `-0.776`, FDR `0.0409`. | PD-linked oxidative-stress gene. Distributed Agents claim `claim:8b5580085329427fc3b8` reports that represented Parkinson-family targets did not form a shared acute neuronal loss-of-function program. This is a close negative calibration: a PD loss can be only a self hit. |
| `Atp13a2` | 1 | Only `Atp13a2` itself was significant, log2FC `-0.613`, FDR `2.23e-21`. | Recessive PD/endolysosomal P5B ATPase. Same-experiment findings showed it did not converge with `Vps35`, `Snca`, `Park7`, autophagy, or lysosomal comparators. |
| `Eif4g1` | 1 | Only `Eif4g1` itself was significant, log2FC `-0.764`, FDR `0.0070`. | PD-annotated translation initiation gene but not a PRKN-pathway component; the corpus uses it as another example of disease-family nonconvergence. |
| `Snca` | 0 | No focal FDR genes; the `Snca` self row had FDR `1.0`. | Alpha-synuclein is PD-linked, but `Snca` loss was fully flat in this TH population, reinforcing that the screen does not recover a generic PD transcriptome. |
| `Uchl1` | 1 | Only the self transcript was significant, log2FC `-1.143`, FDR `8.07e-60`. | Ubiquitin-proteasome/PD-associated comparator. Its absence of downstream hits argues that altered ubiquitin handling alone was usually buffered. |
| `Synj1` | 1 | Self transcript significant, log2FC `-0.583`, FDR `3.11e-7`. | PD-linked synaptic/endocytic comparator. Relevant mostly as another PD/endosomal loss with no secondary 151 TH program. |
| `Dnajc13` | 1 | Self transcript significant, log2FC `-0.453`, FDR `0.00463`. | RME-8/endosomal PD-linked comparator; again self-only rather than a PRKN-like stress program. |
| `Vps13c` | 0 | Self row FDR `1.0`; no focal DEGs. | PD-linked endolysosomal/mitochondrial lipid-transfer gene. It bounds expectations away from assuming every PD mitophagy-proximal gene moves the nucleus. |
| `Atg5` | 0 | No FDR genes; the self row did not pass. | Core macroautophagy gene. Flat in this focal cell type, so a single perturbation of the mitophagy machinery is not automatically a nuclear stressor here. |
| `Sqstm1` | 1 | Only `Sqstm1` itself was significant, log2FC `-0.565`, FDR `0.000793`. | Selective autophagy adaptor and mitophagy effector. Self-only response is a negative counterexample to a broad autophagy-compensation prediction. |
| `Map1lc3a` | 1 | Only `Map1lc3a` itself was significant, log2FC `-0.565`, FDR `0.000646`. | Autophagosome marker family. Self-only; does not phenocopy lysosomal stress. |
| `Mff` | 0 | No focal FDR genes. | Mitochondrial fission receptor. Distributed Agents claim `claim:30ab45a3b952026ae47a` specifically contrasts the flat `Mff` surface with the detectable `Opa1` mitochondrial ISR. |
| `Rhot1` | 0 | No focal FDR genes. | Mitochondrial trafficking outer-membrane protein and Parkin substrate family member; flatness argues that outer-membrane quality-control perturbations can remain transcriptomically silent. |
| `Opa1` | 37 | Induced an ATF4/ISR-like amino-acid stress program: `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Slc7a5`, and `Mthfd2` were among the top calls. | Important positive control, but a counterexample rather than the best analog. `Opa1` hits inner-membrane fusion/cristae and crosses a mitochondrial retrograde-stress threshold that many other mitochondrial targets do not. |
| `Vps35` | 17 | Modest thalamic retromer/synaptic signature, including `Atp2a2` down, `Brsk1` up, `Grin2b` down, `Vps35` down, and `Rims3` down. | Mechanistically near PD/endosomal biology. The corpus finding `Vps35:F006` separates the acute `Vps35` signature from chronic PD cargo, MUL1/Mfn2, and autophagy-lysosome programs, so I treated it as too branch-specific to transfer to `Prkn`. |
| `Rab7` | 501 | Large late-endosomal response in 151 TH, headed by `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`, `Dusp1`, `Insig1`, `Lamp2`, and sterol genes. | A stress-positive endolysosomal counterexample. Parkin can modulate Rab7/VPS35 endosomal organization, but `Rab7` loss directly disables late-endosome/lysosome traffic and is far broader than the other PRKN-adjacent perturbations. |

## Target-specific biological reasoning for `Prkn`

PRKN/Parkin is a cytosolic RBR E3 ubiquitin ligase. In the canonical damage
pathway, loss of mitochondrial membrane potential stabilizes PINK1 on the outer
mitochondrial membrane; PINK1 recruits Parkin and activates it by
phosphorylating ubiquitin and Parkin, then Parkin amplifies ubiquitin tags on
outer-membrane substrates to recruit mitophagy machinery. Narendra et al. 2008
established Parkin recruitment to damaged mitochondria and autophagic removal;
Matsuda et al. 2010 connected PINK1 stabilization to Parkin recruitment and
activation; Koyano et al. 2014 identified PINK1 phosphorylation of ubiquitin as
a Parkin-activating signal; Lazarou et al. 2015 placed OPTN and NDP52 as major
ubiquitin-dependent receptors downstream of PINK1.

Those facts make `Prkn` a real mitochondrial quality-control target, but they
also make its acute RNA phenotype likely to be stress-gated. Sparse partial
`Prkn` loss in unstressed postnatal thalamic glutamatergic neurons is not the
same as CCCP treatment, aged dopaminergic degeneration, or a chronic organismal
Parkinson model. Mouse work is consistent with that buffering: Kitada et al.
2009 found no nigral degeneration even in aged mice lacking Parkin, DJ-1, and
PINK1, while Pickrell et al. 2015 showed that endogenous Parkin became important
under mitochondrial DNA mutator stress. In short, basal loss is often tolerated
until there is an additional mitochondrial load.

The dataset supports the same conclusion. The closest PD-family training
perturbations were zero or self-only in `151 TH Prkcd Grin2c Glut`
(`Park7 = 1`, `Atp13a2 = 1`, `Eif4g1 = 1`, `Snca = 0`,
`Uchl1 = 1`, `Synj1 = 1`, `Dnajc13 = 1`, `Vps13c = 0`). Core autophagy
comparators were also zero or self-only (`Atg5 = 0`, `Sqstm1 = 1`,
`Map1lc3a = 1`). The strong `Rab7` and modest `Vps35` responses showed that
this cell group can sense some endosomal failures, but their expression
patterns were late-endosome/retromer branch states rather than the silent
Parkinson-family state. The `Opa1` ATF4/ISR program showed that mitochondrial
stress is detectable when the lesion crosses threshold, while `Mff`, many
complex-I targets, `Sod2`, and `Sucla2` did not cross it. I therefore predicted
no reproducible downstream PRKN/Parkin transcriptional program.

I assigned a point prediction of `1`, not `0`, because many otherwise flat
targets counted only their own transcript, and `Prkn` is a measurable transcript
in this focal DE matrix: across the 1,674 training perturbations it had several
FDR-level changes under broad regulators such as `Thap11`, `Setd1a`, `Zbtb7a`,
`Tpr`, `Hnrnpu`, `Prpf6`, `Rnpc3`, and `Uba5`. Thus the most likely observed
endpoint is one FDR gene, interpreted as the edited `Prkn` transcript itself or
a singleton idiosyncratic call, with no real broad secondary state.

## Limits and extrapolation

- `Prkn` and `Pink1` were not training perturbations, so there was no
  same-pathway PINK1/Parkin matched signature.
- The prediction transfers from adjacent Parkinson, autophagy, mitochondrial,
  and endolysosomal losses; none is a perfect same-complex phenocopy for an RBR
  E3 ligase.
- The readout is nuclear mRNA abundance 3-4 weeks after partial AAV CRISPR
  loss. It does not directly measure ubiquitin flux, mitochondrial recruitment
  of Parkin, mitophagy, endosome morphology, respiration, or neuronal viability.
- The `1` versus `0` distinction depends on whether the held-out `Prkn` guides
  lowered `Prkn` mRNA enough for FDR correction. That self-transcript behavior
  cannot be inferred mechanistically, so this is the weakest part of the point
  estimate.

Final prediction after the target-specific reasoning: `Prkn -> 1`.
