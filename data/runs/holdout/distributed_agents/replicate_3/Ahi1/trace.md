# Held-out DEG-count prediction

## Question and resolved ambiguities

The manifest `008_Ahi1.csv` contains one held-out target, `Ahi1`. I interpreted the task as a point prediction for the number of genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` neurons after acute AAV-CRISPR loss of `Ahi1`.

Two scope points affected the prediction.

- `151 TH Prkcd Grin2c Glut` is the Allen thalamic glutamatergic group described in the dataset context; `TH` is thalamus, not tyrosine hydroxylase.
- `n_degs` is the literal assay endpoint, including the perturbed transcript if it passes FDR. Some one-gene training responses are therefore just self-target RNA loss; they are still counted, but they are weak evidence for a broad downstream state.

## Sources

- Raw same-experiment differential-expression data: `training_de_all_cell_groups.parquet`.
- Same-experiment endpoint calibration: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Held-out manifest: `008_Ahi1.csv`.
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`. `Ahi1` itself was absent from this corpus, but the corpus contained curated Cep290, IFT, dynein-2, BBSome, ciliary-GPCR, and Hedgehog comparisons from the same perturbation screen.
- PubMed-indexed external literature for AHI1/Jouberin and ciliopathy biology:
  - Dixon-Salazar et al. 2004, DOI `10.1086/425985`, PMID `15467982`.
  - Gorden et al. 2008, DOI `10.1016/j.ajhg.2008.10.002`, PMID `18950740`.
  - Tuz et al. 2013, DOI `10.1074/jbc.M112.420786`, PMID `23532844`.
  - Westfall et al. 2010, DOI `10.1523/JNEUROSCI.5229-09.2010`, PMID `20592197`.
  - Munoz-Estrada and Ferland 2019, DOI `10.1242/jcs.230680`, PMID `31391239`.
  - Hsiao et al. 2021, DOI `10.1523/JNEUROSCI.2993-20.2021`, PMID `33741721`.
  - Gana, Serpieri and Valente 2022, DOI `10.1002/ajmg.c.31963`, PMID `35238134`.

## Computation over the training data

The training count file has 1,674 non-held-out targets in the focal cell group. It is extremely zero-inflated: 1,205 targets have `n_degs = 0`, the median is 0, the 75th percentile is 1, and the 95th percentile is 18. `Ahi1` is absent from that file, as expected for a held-out perturbation.

I first enumerated obvious AHI1/Joubert/cilium comparators that are actually in the training count table, rather than assuming every known ciliopathy gene was perturbed. I then pulled the focal-cell DE rows for 31 represented ciliary, ciliary GPCR, Hedgehog, transition-zone, retinal gate, and AHI1-adjacent targets from the parquet by reading row groups 546-580 and filtering to `151 TH Prkcd Grin2c Glut`. This yielded 17,259 measured genes for each comparator.

For those comparator profiles I counted FDR-significant genes, inspected the best adjusted p values, and compared full Wilcoxon-score profiles and top signed tails using the Distributed Agents runtime profile comparison. The runtime comparison covered 31 targets and 465 pairwise profile contrasts.

## Target-specific reasoning

### Ahi1

`Ahi1` encodes Jouberin, a Joubert syndrome protein. Human AHI1 loss-of-function mutations cause Joubert syndrome with cortical and hindbrain malformations (Dixon-Salazar et al. 2004), and Joubert syndrome is a genetically heterogeneous ciliopathy involving transition-zone and basal-body genes such as `AHI1`, `CEP290`, `RPGRIP1L`, `ARL13B`, and `CC2D2A` (Gorden et al. 2008; Gana, Serpieri and Valente 2022). Mechanistically, AHI1 missense mutations alter basal-body localization and interactions with NPHP1 and HAP1 (Tuz et al. 2013). In model systems, Ahi1 loss impairs ciliary ARL13B recruitment and Hedgehog signaling in mouse fibroblasts (Munoz-Estrada and Ferland 2019), is required for ciliary trafficking of MCHR1 and MCHR1-stimulated cAMP/ERK signaling in neurons (Hsiao et al. 2021), and has strong sensory-cilium phenotypes in photoreceptors (Westfall et al. 2010).

The direct same-experiment analogs argue that this organelle biology usually did not become a broad basal nuclear-RNA program in the assayed postnatal neurons:

| comparator set | focal training counts and expression evidence |
| --- | --- |
| Joubert/transition-zone or retinal ciliary-gate genes | `Cep290`, `Rpgrip1l`, `B9d1`, `Cspp1`, `Iqcb1`, `Rpgr`, `Cplane1`, and `Lztfl1` all had `0` DEGs in `151 TH Prkcd Grin2c Glut`. `Cep290`, the strongest AHI1-adjacent transition-zone comparator in the corpus, had no gene near threshold in the focal parquet slice; its best `pvals_adj` was `0.650`. `Rpgrip1l` was also zero, with best `pvals_adj = 0.184`. |
| IFT, dynein-2, kinesin-2, and BBSome genes | `Ift88`, `Ift81`, `Ift43`, `Dync2h1`, `Dync2i1`, `Kif3b`, `Ttc21b`, `Bbs5`, and `Alms1` had `0` DEGs. `Ttc8` had `1` DEG, but that gene was `Ttc8` itself, so this was a self-transcript singleton rather than evidence for a downstream ciliopathy module. |
| Ciliary GPCR and Hedgehog-linked genes | `Mchr1`, `Adcy3`, `Htr6`, `Gpr161`, `Smo`, `Gli1`, and `Gli2` had `0` DEGs. `Prkaca` had `1` DEG and it was again the self-target transcript. These are relevant because Ahi1 loss in neurons specifically disrupts ciliary MCHR1 signaling, but the receptor and downstream signaling perturbations did not produce a focal basal RNA state. |
| AHI1 protein-interaction or ARL3-cycle counterexamples | `Hap1`, a reported AHI1 interactor whose knockout neurons did not show the AHI1-like primary-cilium defect in Tuz et al. 2013, had `0` focal DEGs. `Arl2bp` had `0`; `Arl3` had `1`, also its self transcript only. |

The profile-level evidence was also near-null. Within the curated ciliary cohort, `Cep290` had no FDR-significant focal feature and the closest full-profile neighbors were still effectively uncorrelated: `Ift81`, Pearson `0.035`; `Ift43`, `0.028`; `Rpgrip1l`, `0.028`; `Arl3`, `0.021`; `Kif3b`, `0.018`; `Bbs5`, `0.003`. There was no shared FDR-supported gene between `Cep290` and the inspected IFT, BBSome, transition-zone, or HAP1 peers.

The Distributed Agents corpus independently summarizes the same pattern for these training perturbations: its Cep290-centered claim states that acute perturbation of represented ciliary transport and signaling genes in postnatal NeuN+ neurons was largely buffered at basal nuclear RNA, and its Cep290 finding `F003` records near-absent transcription from ciliary GPCR, BBSome/IFT, and Hedgehog-effector components. This is an internal same-experiment semantic layer, so I used it only to identify and interpret comparators, not as an independent replicate of the counts above.

Decision: predict no FDR-level genes for `Ahi1` in the focal thalamic glutamatergic group. The best positive argument for a nonzero count is a possible self-transcript effect, because the one-DEG `Arl3`, `Ttc8`, and `Prkaca` responses were their own RNAs. The closer transition-zone/Joubert comparators `Cep290` and `Rpgrip1l`, the ciliary GPCR endpoint `Mchr1`, and the AHI1-interacting `Hap1` were all strict zeroes, so I did not add a singleton.

Predicted `n_degs`: `0`.

## Limits

This is an extrapolation from neighboring perturbations, because `Ahi1` was held out of both the DE parquet and the focal training count file, and it was not represented in the Distributed Agents corpus. The ciliary comparators are mechanistically close but not perfect: AHI1 has transition-zone scaffolding, neuronal MCHR1-trafficking, HAP1-binding, retinal, and developmental roles that are not identical to loss of `Cep290`, `Rpgrip1l`, IFT genes, BBSome genes, or Hedgehog effectors. Several canonical Joubert genes, including `Nphp1`, `Arl13b`, `Cc2d2a`, `Tmem67`, `Mks1`, `Kif7`, and `Inpp5e`, were absent from the available training endpoint. The experiment measured basal nuclear RNA in recovered postnatal NeuN+ cells; it did not image cilia, quantify ciliary protein localization, assay evoked MCHR1/Hedgehog signaling, include photoreceptors or most glia, or model embryonic Joubert development. Finally, the zero-versus-one distinction is fragile because a detectable self-target RNA decrease alone would change the endpoint from 0 to 1 without implying a broader AHI1-driven state.
