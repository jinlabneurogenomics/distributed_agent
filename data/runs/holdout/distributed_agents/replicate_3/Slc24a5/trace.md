# Reasoning trace

## Question and held-out target

The task is to predict the number of genes that would pass `pvals_adj < 0.05` after acute sparse CRISPR loss of each requested gene in `151 TH Prkcd Grin2c Glut` neurons.  The manifest contains one held-out perturbation, in this order:

```text
Slc24a5
```

I treated the endpoint as exactly the count of focal-cell measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`, matching the provided training-count CSV.  I did not interpret it as a generic measure of knockout severity, and I did not use the held-out perturbation itself because `Slc24a5` is absent from the training DE parquet and the focal-cell count CSV by design.

## Sources used

I used the following sources.

- `training_de_all_cell_groups.parquet`: same-experiment per-gene differential-expression rows.  I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` and to biologically nominated training perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for non-held-out perturbations in the focal cell group.
- `211_Slc24a5.csv`: the requested held-out target manifest.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`.
  `target_context("Slc24a5")` and `related_targets("Slc24a5")` returned no target-scoped claims or finding edges, consistent with `Slc24a5` being held out.  I therefore used lexical searches over frozen claims to audit in-dataset comparator biology:
  - high-confidence claim `claim:3e8833815081bd78261c`: canonical melanogenic and melanosome transcriptional programs are not recovered from `Mc1r` or `Lrmda` perturbation in NeuN+ neuronal nuclei.
  - high-confidence claim `claim:9dd8ea8c02fca10a7428`: the `Atp2b1` PMCA response in `151 TH Prkcd Grin2c Glut` is selective and not reproduced by `Atp2b2`, `Atp2b3`, or `Bsg`.
  - high-confidence claim `claim:16ed634c5b3dc2e0831c`: `Atp2a2`/SERCA2 loss, not other represented Ca2+ pumps or release-channel perturbations, selectively activates an ER-stress ISR/UPR state.
- Distributed Agents runtime profile comparison over 16 nominated focal-cell training signatures, using signed `logfoldchanges` and `pvals_adj < 0.05` to compare significant features.
- PubMed-indexed primary literature and reviews on `SLC24A5`:
  - Lamason et al. 2005, Science, DOI `10.1126/science.1116238`, PMID `16357253`: zebrafish `golden` encodes `slc24a5/nckx5`, an intracellular-membrane cation exchanger required for normal melanosome size, number, and density.
  - Vogel et al. 2008, Veterinary Pathology, DOI `10.1354/vp.45-2-264`, PMID `18424845`: `Slc24a5-/-` mice have ocular albinism and hypopigmented retinal pigment epithelium, iris pigment epithelium, and ciliary-body pigment cells.
  - Wei et al. 2013, Journal of Investigative Dermatology, DOI `10.1038/jid.2013.49`, PMID `23364476`: pathogenic human `SLC24A5` variants cause nonsyndromic oculocutaneous albinism type 6 and the transporter is tied to mature melanosomes and HPS/BLOC trafficking machinery.
  - Wiriyasermkul et al. 2020, Biochimica et Biophysica Acta Biomembranes, DOI `10.1016/j.bbamem.2020.183318`, PMID `32333855`: melanosomes are lysosome-related organelles whose pigmentation depends on ion and pH homeostasis.

I did not find a need for an external interaction database: the closest mechanistic facts needed for `Slc24a5` were its NCKX5/melanosome identity and the fact that the assayed nuclei are NeuN+ neurons, not melanocytes or retinal pigment epithelium.

## Computational checks

The focal training-count table contains 1,674 perturbations.  It is sparse in this cell group: median `n_degs = 0`, 75th percentile `n_degs = 1`, mean `n_degs = 14.1`, and a long tail up to 2,677.  Thus a zero prediction is the calibrated baseline unless a target has direct in-assay analogs with reproducible transcriptional activity.

I queried the training universe for `Slc24a5`-relevant genes.

- No closest potassium-dependent Na+/Ca2+ exchanger paralogs, `Slc24a1`, `Slc24a2`, `Slc24a3`, or `Slc24a4`, were training targets.
- No `Slc8a1`/`Slc8a2`/`Slc8a3` NCX exchanger was a training target.
- Canonical pigment genes `Oca2`, `Tyr`, `Tyrp1`, `Slc45a2`, `Pmel`, and `Mlana` were not training targets.
- The useful represented pigment-lineage comparators were `Mc1r` and `Lrmda`; the useful organellar Ca2+/pH counterexamples were `Atp2a2`, `Atp2b1`, `Atp2b2`, `Atp2b3`, `Atp2c1`, several V-ATPase subunits, `Trpm3`, `Trpm7`, `Pld3`, and the thalamus-active Ca2+ channel `Cacna1g`.

The focal parquet filter for the nominated analogs was:

```python
base = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidates)
)
sig = dataset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj",
        "scores", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=base & (pc.field("pvals_adj") < 0.05),
)
```

The observed focal-cell counts and relevant signatures were:

| training perturbation | `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` |
| --- | ---: | --- |
| `Mc1r` | 0 | No significant genes. `Slc24a5`, `Tyr`, `Tyrp1`, `Dct`, `Pmel`, `Mlana`, `Oca2`, `Slc45a2`, `Mitf`, and `Lrmda` all had `pvals_adj = 1`, with near-zero Wilcoxon scores despite unstable log-fold changes for almost absent pigment transcripts. |
| `Lrmda` | 0 | No significant genes. The same pigment markers, including `Slc24a5`, all had `pvals_adj = 1`. |
| `Atp2a2` | 187 | Clear ER Ca2+-loading stress response: `Atp2a2` itself was down (`log2FC = -1.26`, `padj = 1.8e-19`) and UPR/ISR-associated genes such as `Ddit3`, `Xbp1`, `Hspa5`, `Asns`, `Slc38a2`, and `Mthfd2` were induced. This is a biologically specific counterexample, not a proxy for a melanosomal exchanger. |
| `Atp2b1` | 22 | Moderate selective PMCA response, including `Atp2b1` self downregulation and a small `Fos`/`Nr4a1`/`Vgf` activity-like component. |
| `Atp2b2` | 1 | Only `Atp2b2` itself passed FDR. |
| `Atp2b3` | 1 | Only `Atp2b3` itself passed FDR. |
| `Atp2c1` | 1 | Only `Atp2c1` itself passed FDR. |
| `Atp6ap2` | 2 | `Atp6ap2` and the V-ATPase gene `Atp6v0a1` passed FDR; no broad lysosomal or melanosomal program emerged. |
| `Atp6v0a1` | 1 | Only `Atp6v0a1` itself passed FDR. |
| `Atp6v1a` | 0 | No significant genes. |
| `Atp6v1b2` | 0 | No significant genes; low matched perturbed count (`n = 32`) makes this a weak negative. |
| `Atp6v1e1` | 0 | No significant genes. |
| `Trpm3` | 0 | No significant genes. |
| `Trpm7` | 0 | No significant genes. |
| `Pld3` | 1 | Only `Pld3` itself passed FDR. |
| `Cacna1g` | 12 | A small thalamus-selective Ca2+-channel response including `Cacna1g`, `Ptprn`, `Stmn4`, and `Cpne7`; Distributed Agents claims mark this as selective rather than a generic calcium-homeostasis signature. |

I also compared the signed log-fold-change profiles of these 16 nominated signatures with the runtime profile tool.  The cohort contained 120 pairwise comparisons.  Only three positive-tail significant-program overlaps were nonzero, and the positive signed-tail overlap coefficient was low across the cohort, with mean `0.065` and maximum `0.165`.  This confirmed that the weakly active Ca2+/pH candidates do not form a single reproducible module whose DEG burden should be transferred wholesale to `Slc24a5`.

## Target-specific reasoning

### `Slc24a5`

`Slc24a5` encodes NCKX5, a K+-dependent Na+/Ca2+ exchanger on intracellular melanosomal/TGN membranes.  The best-established loss-of-function phenotype is hypopigmentation: zebrafish `golden` `slc24a5` mutants have abnormal melanosomes and the human ortholog rescues that phenotype (Lamason et al. 2005); mice lacking `Slc24a5` show ocular albinism and hypopigmented retinal/iris/ciliary pigment epithelium (Vogel et al. 2008); and human `SLC24A5` variants cause OCA6 through melanosome maturation or trafficking defects (Wei et al. 2013).  That mechanism is strong for pigment cells but a poor match to sparse CRISPR in NeuN+ thalamic neurons.

The most direct represented lineage analogs support no focal neuronal RNA response.  `Mc1r` and `Lrmda` are both pigmentation-associated and were both assayed in `151 TH Prkcd Grin2c Glut`; each had `n_degs = 0`, and neither perturbed a latent pigment program in the focal nuclei.  The Distributed Agents corpus reached the same same-experiment conclusion in claim `3e8833815081bd78261c`: canonical melanogenic and melanosome programs were not recovered from `Mc1r` or `Lrmda` in NeuN+ nuclei.  In the raw focal rows, `Slc24a5` itself and the pigment markers `Tyr`, `Tyrp1`, `Dct`, `Pmel`, `Mlana`, `Oca2`, `Slc45a2`, and `Mitf` were all non-significant at `pvals_adj = 1` under both `Mc1r` and `Lrmda`, which is consistent with those transcripts being absent or too sparse in this neuronal cell group.

The calcium/pH transporter neighborhood argues against assigning a small nonzero response just because NCKX5 is an ion exchanger.  There were no assayed `Slc24a` or `Slc8` exchanger paralogs to use directly.  Nearby functional counterexamples are mostly flat: PMCA paralogs `Atp2b2` and `Atp2b3`, the Golgi Ca2+ pump `Atp2c1`, and V-ATPase subunits each produced 0-2 DEGs except `Atp2b1`, whose 22-gene response is internally annotated as PMCA-subunit-selective.  `Atp2a2` is the active outlier, with 187 DEGs, but its signature is the canonical ER Ca2+ depletion and UPR/ISR program, not a melanosome or lysosome-related exchange response.  `Cacna1g` likewise gave only a 12-gene, TH-neuron-specific Ca2+ channel response.  These are therefore boundaries rather than reasons to extrapolate a broad `Slc24a5` effect.

Balancing those points, the biologically appropriate in-dataset comparators are the pigment-associated zeros, while the cation-transporter comparators caution that detectable Ca2+-handling responses are highly compartment- and paralog-specific in this assay.  Because `Slc24a5` acts in a melanosome program that should be missing from NeuN+ thalamic nuclei, I predict no measured gene will cross FDR 0.05:

```text
Slc24a5 -> predicted_n_degs = 0
```

## Limits and extrapolations

There is no direct in-dataset `Slc24a` or `Slc8` exchanger perturbation, no `Tyr`/`Oca2`/`Slc45a2` canonical melanosome transporter perturbation, and `Slc24a5` itself has no Distributed Agents target-scoped corpus node.  The prediction therefore extrapolates from pigment-lineage zeros plus compartment-specific Ca2+/pH counterexamples, not from a true NCKX5 paralog.

Several weak negatives also have caveats: V-ATPase genes differ by subunit and had variable matched perturbed-cell counts, and a sparse neuronal CRISPR snRNA-seq assay cannot exclude changes in Ca2+ flux, organellar pH, pigmentation chemistry, or protein localization.  The call is specifically that those mechanisms are unlikely to create enough steady-state nuclear mRNA changes in `151 TH Prkcd Grin2c Glut` to pass FDR in this experiment.
