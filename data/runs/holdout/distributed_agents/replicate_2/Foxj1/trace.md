# Question and interpretation

The held-out target list contains one perturbation:

```text
Foxj1
```

I therefore predicted the assay endpoint `n_degs` for `Foxj1` loss of function in the `151 TH Prkcd Grin2c Glut` focal cell group: the number of measured genes with Scanpy/Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05`.

I treated `n_degs` as the FDR-count endpoint from this Perturb-seq assay, not as an intrinsic importance score for the gene. Because the experiment is a sparse, AAV-delivered, postnatal CRISPR perturbation in NeuN-enriched brain nuclei, I weighted postmitotic neuronal responses in the supplied data above developmental phenotypes from germline or epithelial/ependymal systems.

# Sources used

- Held-out manifest: `080_Foxj1.csv`.
- Training endpoint CSV: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Training differential-expression parquet: `training_de_all_cell_groups.parquet`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, especially same-experiment ciliary and ependymal claims:
  - `claim:78305cab7c1c7b98458d`: acute perturbation of represented ciliary trafficking/signaling genes is largely buffered at the basal nuclear-RNA level in postnatal NeuN+ neurons.
  - `claim:abe5627e3674c2363c4d`: represented `Rfx3`/`Rfx7` and ciliary-effector perturbations do not give a shared acute neuronal ciliary transcriptional signature.
  - `claim:d24b8df702b0d0760e9e`: hydrocephalus-linked `Trp73`/`E2f5` ciliary and choroid-plexus programs are not detectable as cell-autonomous neuronal transcriptomic responses in this NeuN-positive screen.
- Distributed Agents Runtime profile tools over the focal-cell parquet rows, used to inspect signed log-fold-change profiles among ciliary/ependymal analogs.
- NCBI PubMed via the BioEval Literature gateway:
  - Abdi et al. 2018, Nature Communications, DOI `10.1038/s41467-018-03812-w`, PMID `29695808`: mature multiciliated ependymal cells require continued Foxj1 maintenance; Foxj1 destabilization causes ependymal dedifferentiation and hydrocephalus.
  - Vidovic et al. 2018, Neural Development, DOI `10.1186/s13064-018-0099-4`, PMID `29452604`: NFIX participates in postnatal ependymal maturation and transcriptionally activates `Foxj1`.
  - Hou et al. 2023, Cellular and Molecular Neurobiology, DOI `10.1007/s10571-023-01398-6`, PMID `37620636`: heterozygous `FOXJ1`/`Foxj1` disruption impairs ventricular multiciliated-cell differentiation, basal-body organization, motile cilia, CSF flow, and causes communicating hydrocephalus.

# Computational checks

I used DuckDB to filter the parquet to the focal context:

```sql
select *
from read_parquet('training_de_all_cell_groups.parquet')
where group_name = '151 TH Prkcd Grin2c Glut'
```

The focal-cell hold-in matrix contains 28,891,566 rows, 1,674 perturbations, and 17,259 measured genes. The training endpoint was strongly zero-inflated: 1,205 of 1,674 hold-in targets had `n_degs = 0`; the median was 0, the 75th percentile was 1, and the 95th percentile was 18.

I then pulled ciliary, RFX, Hedgehog-cilium, ependymal-development, and forkhead-family hold-ins from the training-count file and matched them back to their focal-cell DE rows. For the most relevant primary comparators:

| training perturbation | focal `n_degs` | focal expression evidence |
| --- | ---: | --- |
| `Rfx3` | 0 | no genes at FDR 0.05 |
| `Rfx7` | 0 | no genes at FDR 0.05 |
| `Nfix` | 0 | no genes at FDR 0.05; only near-miss among this target was `Ogfr`, adjusted `p = 0.148` |
| `E2f5` | 0 | no genes at FDR 0.05 |
| `Trp73` | 0 | no genes at FDR 0.05 |
| `Ift88` | 0 | no genes at FDR 0.05 |
| `Ift43` | 0 | no genes at FDR 0.05 |
| `Kif3b` | 0 | no genes at FDR 0.05 |
| `Dync2i1` | 0 | no genes at FDR 0.05 |
| `Dync2h1` | 0 | no genes at FDR 0.05 |
| `Cep290` | 0 | no genes at FDR 0.05 |
| `Ttc21b` | 0 | no genes at FDR 0.05 |
| `Armc9` | 0 | no genes at FDR 0.05 |
| `Alms1` | 0 | no genes at FDR 0.05 |
| `Cfap69` | 0 | no genes at FDR 0.05 |
| `Ttc8` | 1 | exactly one significant gene, the perturbed transcript itself: `Ttc8`, log2FC `-0.663`, adjusted `p = 3.1e-5` |
| `Arl3` | 1 | exactly one significant gene, the perturbed transcript itself: `Arl3`, log2FC `-0.418`, adjusted `p = 0.018` |
| `Arl2bp` | 0 | no genes at FDR 0.05 |

I also checked additional pathway counterexamples:

- Ciliary Hedgehog transduction: `Cdon`, `Gli1`, `Gli2`, `Gpr161`, `Ptch1`, `Ptch2`, and `Smo` were all 0-DEG perturbations in `151 TH Prkcd Grin2c Glut`.
- Retinal/ciliary-gate genes from the same-experiment ciliary claims: `Iqcb1`, `Rpgr`, `Rpgrip1l`, and `Spata7` were all 0.
- Other forkhead-family transcription factors represented in the focal training endpoint were uniformly 0: `Foxa2`, `Foxc2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`, `Foxl2`, `Foxn1`, `Foxp2`, and `Foxp3`.

For signed profile structure rather than counts alone, I compared the full 17,259-gene log2FC vectors for `Rfx3`, `Rfx7`, `E2f5`, `Trp73`, `Ift88`, `Kif3b`, `Dync2i1`, `Ttc8`, `Cep290`, and `Arl3` in the focal cell group. Across all 45 pairwise comparisons there were no shared same-direction or opposite-direction FDR-significant features. The `Rfx3` profile was nearest to other ciliary hold-ins only in a weak whole-profile sense, and its top-100 tail overlaps with them were small: 3-7% for positive tails and 5-17% for negative tails. This argues against a coherent latent ciliary response being just below the `n_degs` threshold.

Finally, I looked at the measured `Foxj1` row within the focal-cell signatures of `Rfx3`, `Rfx7`, `E2f5`, `Trp73`, `Nfix`, `Ift88`, `Kif3b`, `Dync2i1`, `Dync2h1`, `Ttc8`, `Cep290`, `Alms1`, `Cfap69`, `Arl3`, and `Ttc21b`. `Foxj1` had adjusted `p = 1.0` in each of these perturbations, so the hold-in analogs did not show evidence for robust `Foxj1` regulation in this neuronal group.

# Target-specific reasoning

## Foxj1

`Foxj1` is a strong transcriptional regulator of motile ciliogenesis in multiciliated cells. In the postnatal brain, the best-established `Foxj1`-dependent compartment is ventricular ependyma: NFIX activates `Foxj1` during ependymal maturation, mature ependymal cells require continued Foxj1 protein maintenance, and heterozygous `FOXJ1`/`Foxj1` disruption compromises ependymal multiciliated differentiation, motile-cilia number and structure, basal-body orientation, and CSF flow (Vidovic et al. 2018; Abdi et al. 2018; Hou et al. 2023).

That biology is potent, but it is not well matched to this readout. The experiment largely removed or under-sampled non-neuronal ependymal, choroid-plexus, vascular, glial, and multiciliated epithelial cells by selecting NeuN-positive nuclei from whole brain minus olfactory bulb and hindbrain. The focal `151 TH Prkcd Grin2c Glut` group is a postmitotic glutamatergic neuronal population, not a ventricular multiciliated-cell population. A direct CRISPR perturbation of `Foxj1` in these nuclei should therefore mostly hit cells in which the motile-cilia transcriptional program is absent or inactive.

The most relevant same-experiment evidence supports this quiet-neuronal interpretation:

- `Rfx3` and `Rfx7` are the closest represented ciliary transcription-factor comparators. Both had `n_degs = 0` in the focal cell group, and the Distributed Agents corpus specifically summarized the represented RFX-family and ciliary-effector perturbations as lacking a shared acute neuronal ciliary signature.
- `Nfix`, an upstream activator of `Foxj1` in the ependymal lineage, also had `n_degs = 0`.
- The hydrocephalus/multiciliogenesis comparators `E2f5` and `Trp73` both had `n_degs = 0`; the Distributed Agents corpus noted that these choroid/ependymal programs were not recovered in the NeuN-positive screen.
- Structural and trafficking ciliary genes that would be expected to lie downstream of a generic ciliogenesis failure were silent in the focal endpoint: `Ift43`, `Ift88`, `Kif3b`, `Dync2i1`, `Dync2h1`, `Cep290`, `Ttc21b`, `Alms1`, `Armc9`, `Cfap69`, and `Arl2bp` were all 0-DEG targets. `Ttc8` and `Arl3` were one-gene responses caused only by measurable depletion of their own transcripts, not by a downstream ciliary state.
- Cilium-coupled Hedgehog components, including `Smo`, `Gpr161`, `Ptch1`, `Ptch2`, `Gli1`, and `Gli2`, were also 0. These are mechanistic counterexamples to the idea that every neuronal primary-cilium perturbation produces a basal nuclear RNA response in this assay.

I therefore expect `Foxj1` KO to have no FDR-significant transcriptomic response in `151 TH Prkcd Grin2c Glut`. I set the point prediction to exactly `0`, rather than to a small singleton count, because even the nearest transcriptional comparators had no significant self-depletion or downstream rows, and `Foxj1` itself was not measurably modulated by the relevant ciliary hold-ins in the focal data.

# Limits and uncertainty

The key uncertainty is that `Foxj1` is a transcription factor, so if a small subset of `151 TH Prkcd Grin2c Glut` cells unexpectedly expressed a Foxj1-dependent motile-cilia-like program, its knockout could have produced a discrete regulon response not shared by structural ciliary genes. The supplied data argue that this is unlikely but cannot prove absence of protein or ciliary morphology effects: the readout is basal single-nucleus RNA, and it does not measure motile-cilia assembly, protein trafficking, primary-cilium signaling competence, basal-body orientation, or CSF-flow phenotypes.

The analog set is also imperfect. `Nfix`, `E2f5`, and `Trp73` are upstream or lineage-adjacent rather than Foxj1 paralogs; IFT/BBS/transition-zone genes perturb cilium transport and architecture rather than the Foxj1 transcriptional program itself; and `Rfx3`/`Rfx7` are broader ciliary regulators rather than dedicated motile-cilia master regulators. Still, the convergence of 0-DEG outcomes across these mechanistically distinct cilia-related hold-ins, together with the NeuN-positive sampling caveat, makes a zero-DEG `Foxj1` prediction the best-calibrated point estimate.
