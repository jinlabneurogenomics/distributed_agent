# Pgk1 DEG-count prediction trace

## Question and endpoint

I predicted the FDR 0.05 DEG count that an acute AAV-PHP.eB CRISPR loss-of-function perturbation of `Pgk1` would have produced in recovered `151 TH Prkcd Grin2c Glut` mouse neuronal nuclei.

The requested manifest contains one held-out target, `Pgk1`; its DE rows and focal DEG count are absent from both supplied training inputs. I treated `n_degs` exactly as defined by the focal training CSV: every measured gene with `pvals_adj < 0.05` is counted, including the perturbed target's own transcript if it is measured and significant. I did not interpret target-transcript knockdown as editing efficiency, but I did count self-transcript hits when the training endpoint counted them.

Sources used:

- Declared focal training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE Parquet: `training differential-expression dataset`.
- Run-local held-out manifest: `single-target request for Pgk1`.
- Run-local dataset portrait, bindings, coverage, capability manifest, and measurement registry.
- Internal same-experiment PerturbAI July corpus release `perturbai-july-260713-sourceguard-1773-v1`, specifically bounded Findings, Null Findings, Pathways, and resolved Evidence for the represented glycolysis targets.
- External PubMed literature for PGK1 mechanism and disease.

The input DE table directly observes the endpoint for non-held-out perturbations only. PGK1 biology was therefore transferred from measured perturbations at adjacent glycolytic steps and from a downstream stress branch that should have become visible if a single glycolytic lesion broadly activated HIF, ISR/UPR, or hexosamine stress.

## Computation over the training inputs

I first read the requested-target CSV and the 1,674-row focal training count CSV. The focal endpoint is zero-inflated: 1,205/1,674 training targets had zero DEGs; 276 had exactly one; 469 were nonzero.

The represented focal single-gene glycolysis or glucose-entry perturbations were:

| training target | focal `n_degs` |
| --- | ---: |
| `Eno1` | 0 |
| `Gpi1` | 1 |
| `Hk1` | 1 |
| `Pfkm` | 1 |
| `Slc2a1` | 0 |
| `Tpi1` | 1 |

I then queried exact focal rows from the Parquet for those six targets. The non-obvious query was a focal-cell filter plus a target list, followed by counting `pvals_adj < 0.05` and `pvals_adj < 0.10`:

```sql
SELECT gene_target,
       count(*) AS measured,
       sum(pvals_adj < 0.05)::INTEGER AS degs_fdr05,
       sum(pvals_adj < 0.10)::INTEGER AS degs_fdr10,
       min(n_pert_matched) AS n_pert,
       min(n_ctrl_matched) AS n_ctrl,
       max(CASE WHEN names = gene_target THEN logfoldchanges END) AS self_lfc,
       max(CASE WHEN names = gene_target THEN pvals_adj END) AS self_padj
FROM read_parquet(?)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ('Eno1','Gpi1','Hk1','Pfkm','Slc2a1','Tpi1')
GROUP BY gene_target;
```

The exact focal Parquet rows show why the formal count is 1 for most core glycolysis analogs:

| target | FDR<0.05 | FDR<0.10 | focal perturbed nuclei | focal control nuclei | self-transcript result |
| --- | ---: | ---: | ---: | ---: | --- |
| `Eno1` | 0 | 0 | 228 | 23,679 | `Eno1` was not a measured row |
| `Gpi1` | 1 | 2 | 173 | 23,679 | `Gpi1`, logFC -0.673, FDR 2.14e-07 |
| `Hk1` | 1 | 1 | 148 | 23,679 | `Hk1`, logFC -0.768, FDR 9.86e-05 |
| `Pfkm` | 1 | 1 | 176 | 23,679 | `Pfkm`, logFC -0.857, FDR 6.42e-14 |
| `Slc2a1` | 0 | 0 | 325 | 23,679 | `Slc2a1`, logFC -0.701, FDR 1.0 |
| `Tpi1` | 1 | 1 | 248 | 23,679 | `Tpi1`, logFC -1.010, FDR 6.23e-12 |

`Gpi1` had only one near-threshold downstream event, `Ogt` down at FDR 0.0887. For `Tpi1`, the next strongest focal genes were `Zfp606`, `Pnisr`, and `Ttc14` at FDR 0.120 to 0.123, so the sole FDR 0.05 hit was also the self transcript. These signatures were therefore not small rich programs; they were null or self-only profiles in `151 TH Prkcd Grin2c Glut`.

As a counterexample, I checked `Gfpt1`, the rate-limiting hexosamine-biosynthesis enzyme downstream of fructose-6-phosphate. It had 311 FDR 0.05 DEGs in the same focal group, including `Ogt` down at FDR 8.10e-17 and induction of `Herpud1`, `Asns`, `Ddit3`, `Hspa5`, `Chac1`, `Pdia6`, `Hyou1`, and `Atf4`. This shows that the focal cell group and the assay had power to detect a nutrient-linked ER/ISR program, but that this branch is specific to hexosamine and glycosylation stress rather than the default result of perturbing any glycolytic enzyme.

## Pgk1-specific biological transfer

`Pgk1` encodes phosphoglycerate kinase 1, the ubiquitous glycolytic enzyme that transfers phosphate from 1,3-bisphosphoglycerate to ADP to form 3-phosphoglycerate and ATP. It lies downstream of `Gapdh` and upstream of `Pgam1`/enolase/pyruvate kinase, away from glucose entry and hexosamine diversion. PGK2 is the second mammalian isoform and is testis-specific rather than a likely buffer in thalamic glutamatergic neurons (Fermo et al. 2012, DOI:10.1016/j.ymgme.2012.05.015).

The strongest within-dataset analogs are the single-node glycolysis perturbations:

- `Hk1`, `Gpi1`, and `Pfkm` are upstream glycolytic nodes. Each produced either zero downstream genes or only its own transcript in the focal FDR 0.05 count. The internal corpus summarizes these as buffered early/core glycolysis perturbations and notes that `Hk1`, `Gpi1`, `Tpi1`, `Pfkm`, `Eno1`, and `Slc2a1` were flat or nearly flat, whereas direct `Ogt` and `Gfpt1` were transcriptionally visible.
- `Tpi1` is one step upstream of `Gapdh` and the triose-phosphate pool. It is the closest measured lower-glycolysis enzymatic comparator for `Pgk1`; focal `Tpi1` had 1 DEG, its own transcript, while `Pgk1`, `Pgam1`, `Ldha`, `Ldhb`, `Gfpt1`, `Glo1`, `Hagh`, `Hspa5`, `Hsp90b1`, `Ddit3`, `Atf4`, `Asns`, `Chac1`, `Herpud1`, `Hyou1`, `Xbp1`, `Psmb4`, `Psma5`, and `Psmd4` were all FDR 1.0 in the same focal Tpi1 signature.
- `Eno1` sits downstream of `Pgk1`; the Eno1 perturbation had no focal FDR 0.05 or FDR 0.10 DEG. Its corpus report specifically found no HIF/MYC, lactate, UPR/ISR, or oxidative-phosphorylation program and no meaningful cross-perturbation neighbor, consistent with a flat signature.
- `Slc2a1` is less direct because mature neurons can use GLUT3 and other glucose routes, but it is a glucose-entry falsifier: knocking out a represented glucose transporter did not create a glucose-starvation/HIF/ATF4 program in focal neurons.

This causal chain made the analogs same-direction for the requested endpoint:

`Pgk1` CRISPR LoF -> reduced PGK1 catalytic capacity -> altered glycolytic flux or local ATP generation -> possible HIF/AMPK/ISR/UPR, lactate, glyoxalase, or synaptic stress in survivors -> FDR-significant nuclear transcripts.

The transfer is expected to be weak or zero at the final measured stage. Adjacent single glycolysis perturbations impaired the same cytosolic ATP pathway but did not propagate to downstream nuclear signatures. The only pathway branch that did produce a large transcriptome, `Gfpt1`, siphons fructose-6-phosphate into UDP-GlcNAc and ER/Golgi glycosylation; the same-experiment report explicitly found that upstream `Hk1` and `Gpi1` did not phenocopy `Gfpt1`, so the `Gfpt1` count should not be assigned to `Pgk1`.

External knowledge adds uncertainty rather than overturning the within-dataset null. Human PGK1 deficiency is X-linked and can cause hemolytic anemia, myopathy, and neurologic dysfunction, with genotype-specific relationships between catalytic impairment, protein stability, and tissue symptoms (Fujii and Miwa 2000, DOI:10.1053/beha.1999.0062; Chiarelli et al. 2012, DOI:10.1371/journal.pone.0032065). Recent neuronal work also found PGK1 to be rate-limiting for glycolytic ATP production kinetics in a Parkinson's disease axonal bioenergetic setting and showed that increasing PGK1 can suppress synaptic dysfunction (Kokotos et al. 2024, DOI:10.1126/sciadv.adn6016). Those results support real PGK1 biology but do not require hundreds of steady-state snRNA-seq DEGs after partial, sparse, P16 CRISPR LoF in recovered thalamic neurons. Conversely, Jin et al. found that siRNA perturbation of PGK1 in five cancer cell lines only marginally affected glucose consumption and lactate generation because the PGK step was kinetically buffered by glycolytic thermodynamics (Jin et al. 2020, DOI:10.1074/jbc.RA119.012312), reinforcing that PGK1 activity can be important without a large expression response to partial knockdown.

## Prediction for the held-out target

For `Pgk1`, I predict no downstream FDR 0.05 response in `151 TH Prkcd Grin2c Glut`, but one DEG overall from the likely measured `Pgk1` self-transcript. This is driven primarily by the focal counts and exact Parquet profiles for `Gpi1`, `Hk1`, `Pfkm`, and `Tpi1`; external PGK1 biology only prevents reading the prediction as a claim that PGK1 is metabolically inert.

Final point prediction:

| target | predicted `n_degs` |
| --- | ---: |
| `Pgk1` | 1 |

## Limits

This is an extrapolation from neighboring glycolytic enzymes, not a direct observation of `Pgk1`. `Gapdh`, `Pgam1`, `Pkm`, `Ldha`, and `Pgk2` were not represented as focal training perturbations, so the lower-glycolysis neighborhood is incompletely sampled. The assay also lacks indel, PGK1 protein, ATP, lactate, methylglyoxal, and cell-loss measurements; severe `Pgk1`-edited cells lost before snRNA-seq would be invisible. Finally, the difference between a predicted count of 0 and 1 is dominated by whether the `Pgk1` transcript itself would pass FDR 0.05, a guide/transcript effect that varies across otherwise buffered glycolysis targets in this platform.
