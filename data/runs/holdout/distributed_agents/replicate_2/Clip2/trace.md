# Clip2 DEG-count prediction

## Question interpreted

The held-out manifest for this run contains one perturbation:

```tsv
target_name
Clip2
```

I interpreted the requested endpoint as the assay-specific number of measured genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` after acute AAV-CRISPR loss of mouse `Clip2`. `Clip2` was completely absent from the supplied training count CSV and from the DE parquet as a perturbation target, so its own count and expression signature could not be looked up. I treated `n_degs` as the observed breadth of the Scanpy Wilcoxon/FDR surface in this cell group, not as a generic importance score or viability proxy.

## Sources used

- Input target manifest: `042_Clip2.csv`.
- Training endpoint file: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, with 1,674 non-held-out targets.
- Training DE parquet: `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`. The focal slice contained 1,674 target profiles x 17,259 measured genes, or 28,891,566 rows.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`. The corpus had no `Clip2` first-hop node, but did have claims covering the represented microtubule, EB/MAP, dynactin, tubulin, and kinesin perturbation neighborhoods:
  - `claim:edf51d701dda34edf161`: measured MAP, tubulin, EB, dynactin, kinesin, CAMSAP, and MARK perturbations generally do not form one coherent shared cytoskeletal-stress mRNA module.
  - `claim:ca803b2ea88defcf5d1a` and `claim:8e25db3f5cd12d5e0f8d`: `Tuba1a` is a restricted tubulin-isotype compensation exception.
  - `claim:d56a2e42b8bf4a1f2ba9`: `Dctn1` elicits a neuronal SREBF2-like sterol/cholesterol module that is not a generic effect of sampled cytoskeletal or trafficking-neighborhood genes.
  - `claim:064f16f0e8bfd08f9b64`: represented kinesin and Miro/TRAK transport genes do not share a common soma-detectable nuclear RNA module.
- PubMed via NCBI E-utilities for external `Clip2` biology.

## Computational checks

I first verified that the request was a single-target holdout and then extracted counts and focal-cell self-target statistics for candidate analogs and counterexamples. The count operation was the same endpoint used by the training file:

```python
focal = de[de["group_name"].eq("151 TH Prkcd Grin2c Glut")]
n_degs = focal.groupby("gene_target")["pvals_adj"].apply(lambda q: (q < 0.05).sum())
```

I also used Distributed Agents runtime profile comparisons on signed `logfoldchanges` in the same focal context, with `pvals_adj` as the significance column and 0.05 as the declared threshold. An exact 16-node cohort spanning `Mapre2`, `Dctn1`, `Map1b`, `Mapt`, `Map6`, `Spast`, `Stmn2`, `Tuba1a`, `Tuba4a`, `Tubb4b`, `Tubb5`, `Kif1a`, `Kif5a`, `Kif5c`, `Kif2a`, and `Kif3b` had 11 sparse responses with 1 to 9 significant genes, 4 zero responses, and only `Dctn1` above 50 DEGs. Significant programs did not overlap between `Mapre2` or `Dctn1` and the inspected kinesin/MAP/tubulin peers; most whole-profile correlations were driven by weak nonsignificant tails rather than by shared FDR-significant biology.

Key training observations in `151 TH Prkcd Grin2c Glut`:

```tsv
target	n_degs	target_log2FC	target_FDR	significant_genes
Mapre2	1	-0.464	5.22e-04	Mapre2
Dctn1	75	-0.590	3.33e-11	Insig1, Msmo1, Dctn1, Hmgcs1, Cyp51, Hmgcr, Fdft1, Fasn, ...
Map1b	1	-0.358	1.06e-05	Map1b
Mapt	1	-0.533	1.43e-05	Mapt
Map6	0	-0.277	3.30e-01	none
Spast	0	-0.343	1.00e+00	none
Stmn2	1	-1.001	1.58e-20	Stmn2
Tuba1a	7	-0.967	2.78e-20	Tuba1a, Tubb3, Tubb2a, Tuba4a, Tubb4a, Tubb4b, Tubb5
Tuba4a	2	-0.710	2.43e-06	Tuba4a, Mast1
Tubb4b	1	-0.597	1.07e-07	Tubb4b
Tubb5	1	-1.478	7.71e-23	Tubb5
Kif1a	1	-0.561	5.50e-05	Kif1a
Kif5a	1	-0.445	6.07e-05	Kif5a
Kif5c	1	-0.528	4.52e-05	Kif5c
Kif2a	0	-0.445	1.00e+00	none
Kif3b	0	-0.246	1.00e+00	none
```

## Target-specific reasoning

`Clip2` encodes CLIP-115, a neuronal CAP-Gly cytoplasmic linker protein that binds microtubules through N-terminal microtubule-binding/basic regions and localizes to growing microtubule plus ends, overlapping the better-studied CLIP-170 plus-end tracker (De Zeeuw et al. 1997, DOI `10.1016/S0896-6273(00)80411-0`; Hoogenraad et al. 2000, DOI `10.1242/jcs.113.12.2285`). CLIP proteins bind EB proteins and participate in microtubule plus-end dynamics; EB1/EB3 depletion changes CLIP plus-end accumulation and dissociation kinetics (Komarova et al. 2005, DOI `10.1091/mbc.e05-07-0614`). CLIPs can regulate neuronal polarization through microtubule and growth-cone dynamics in cultured neurons (Neukirchen and Bradke 2011, DOI `10.1523/JNEUROSCI.3983-10.2011`), and germline `Cyln2`/`Clip2` mutation produces neurodevelopmental phenotypes in mice with redistribution of CLIP-170 and dynactin at microtubule tips (Hoogenraad et al. 2002, DOI `10.1038/ng954`).

The best direct within-dataset analog would have been `Clip1`, but `Clip1`, `Clasp1`, `Clasp2`, `Mapre1`, and `Mapre3` were not represented in the 1,674 training perturbations. The closest available plus-end gene was `Mapre2`. `Mapre2` had exactly one DEG, its own transcript, with no EB/CLIP-like secondary expression program. That is imperfect because EB2/MAPRE2 is not EB1 or EB3, which are the EB family members most directly tied to CLIP localization in the cited CLIP work, but it is still the in-dataset member closest to the same plus-end-tracking machinery. The broader MAP and microtubule-associated comparators were also sparse: `Map1b`, `Mapt`, `Stmn2`, `Tubb4b`, `Tubb5`, `Kif1a`, `Kif5a`, and `Kif5c` each produced one DEG, almost always just the knocked-down gene, while `Map6`, `Spast`, `Kif2a`, and `Kif3b` produced zero.

I treated `Dctn1` as a boundary case rather than as the expected effect size for `Clip2`. p150Glued, encoded by `Dctn1`, has an N-terminal CAP-Gly domain homologous to CLIP microtubule-binding domains, but `Dctn1` loss in the focal cells induced a 75-DEG sterol/cholesterol program headed by `Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, and `Fasn`. That is the same SREBF2-like module noted in the Distributed Agents corpus and it did not recur in the plus-end/MAP/kinesin/tubulin set. External biology also argues against equating `Clip2` with `Dctn1`: CLIP-170 can bind p150Glued/dynactin, whereas CLIP-115 lacks the dynein-dynactin interaction domain required for that CLIP-170 spindle/dynein effect (Tanenbaum et al. 2008, DOI `10.1038/emboj.2008.242`).

I also did not borrow the 7-DEG `Tuba1a` response. The `Tuba1a` signature was a very specific alpha/beta tubulin paralog compensation module, while `Tuba4a`, `Tubb4b`, and `Tubb5` remained at 1 to 2 DEGs and the Distributed Agents corpus explicitly marks `Tuba1a` as the exception rather than a generic response to all microtubule perturbations.

Putting those together, the expected `Clip2` phenotype in this assay is a very narrow direct perturbation readout, not a broad cytoskeletal-stress or sterol/cholesterol state. The one point above zero comes from the observed fact that many expressed neuronal cytoskeletal targets in this neighborhood pass FDR for their own transcript after acute CRISPR loss: `Mapre2`, `Map1b`, `Mapt`, `Stmn2`, `Tubb4b`, `Tubb5`, `Kif1a`, `Kif5a`, and `Kif5c` all had one direct DEG. Therefore I predicted that `Clip2` itself will cross the FDR threshold, but that no secondary genes will.

## Limits and extrapolation

This is a weakly constrained single-gene extrapolation because the most natural paralog and binding-partner perturbations for CLIP-115 were missing from training: no `Clip1`, no `Clasp1`/`Clasp2`, and no `Mapre1`/`Mapre3`. The available EB analog, `Mapre2`, is useful but not fully equivalent to EB1/EB3. `Dctn1` touches CLIP-family biology through CAP-Gly/dynactin plus-end localization, but its 75-DEG cholesterol response was target-specific in this experiment, so rejecting it as a positive analog is a judgement call. Finally, chronic germline `Clip2` mouse phenotypes and cultured-neuron CLIP depletion report morphology, microtubule dynamics, and development more directly than they report an acute soma nuclear RNA program in sparsely edited postnatal thalamic glutamatergic nuclei. The integer prediction is consequently most sensitive to whether `Clip2` mRNA itself is expressed and depleted strongly enough in the held-out nuclei to pass BH FDR 0.05.

## Final point prediction

```tsv
target_name	predicted_n_degs
Clip2	1
```
