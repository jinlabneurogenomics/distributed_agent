# DEG-count prediction trace

## Question and target

The held-out manifest for this run contains one perturbation, `Bbs9`. I interpreted the requested endpoint as:

- cell group: `151 TH Prkcd Grin2c Glut`
- statistic to predict: the count of measured genes with Wilcoxon `pvals_adj < 0.05`
- perturbation setting: acute sparse AAV CRISPR loss of function in postnatal mouse NeuN+ nuclei
- output unit: one non-negative integer, with `0` meaning no genes cross the FDR 0.05 cutoff

The important ambiguity is that `n_degs` can include the perturbed gene itself if its own mRNA is significantly depleted. I treated target self-downregulation as part of the endpoint, because the training CSV counted it that way: for example, `Ttc8` had one focal-cell DEG and Arrow filtering showed that the only significant row was `Ttc8` itself.

## Sources used

- Held-out target list: `[local file: 024_Bbs9.csv]`
- Training endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Full training differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`
- Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`; `Bbs9` itself was absent, but same-experiment corpus cards for `Bbs5`, `Ttc8`, `Cep290`, `Ift43`, `Ift81`, `Ift88`, `Cplane1`, `Arl3`, `Kif3b`, and `Rpgr` supported the repeated observation that represented ciliary perturbations were transcriptionally flat or singleton-only in postnatal neurons.
- Distributed Agents runtime profile tools over the focal-cell parquet subset; I compared ciliary/BBSome candidate signatures with 17,259 measured genes per perturbation, `logfoldchanges` as the signed profile value, `pvals_adj < 0.05` as the significance criterion, and 500-gene signed tails.
- PubMed, via NCBI E-utilities, for BBSome biology:
  - Nachury et al. 2007, Cell, PMID 17574030, DOI 10.1016/j.cell.2007.03.053: purification of a stable BBSome and connection to Rab8-dependent ciliary membrane biogenesis.
  - Jin et al. 2010, Cell, PMID 20603001, DOI 10.1016/j.cell.2010.05.015: BBSome as an ARL6/BBS3 effector and membrane-protein coat for ciliary trafficking.
  - Veleri et al. 2012, PLoS One, PMID 22479622, DOI 10.1371/journal.pone.0034389: BBS9/PTHB1 is required for cilia formation/function in zebrafish and mouse IMCD3 cells.
  - Zhang et al. 2012, JBC, PMID 22500027, DOI 10.1074/jbc.M112.341487: sequential BBSome assembly with a BBS7-BBS2-BBS9 core intermediate followed by BBS1, BBS5, BBS8, and BBS4.
  - Knockenhauer and Schwartz 2015, JBC, PMID 26085087, DOI 10.1074/jbc.M115.649202: BBS9 is one of the eight BBSome components and has structured interaction domains.
  - Nozaki et al. 2018, PLoS One, PMID 29590217, DOI 10.1371/journal.pone.0195005, and Nozaki et al. 2019, Biology Open, PMID 31471295, DOI 10.1242/bio.043786: the BBS1/BBS2/BBS7/BBS9 core and IFT-B-BBSome interaction participate in ciliary GPCR export.
  - Hsu, Seo and Sheffield 2021, Human Molecular Genetics, PMID 33517424, DOI 10.1093/hmg/ddaa284: BBS1/BBS5/BBS8/BBS9 can form a photoreceptor-ciliary BBSome subcomplex, underscoring that the core BBSome effect can be cilium and cell-type specific.

## Computations over the supplied data

I first read the focal-cell training count CSV and searched the 1,674 measured training targets for canonical BBSome and ciliary candidates. The endpoint distribution is sparse: median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`, and only the top tail of perturbations produces broad signatures.

I then filtered the parquet with Arrow to the focal group and the ciliary analog set:

```python
group_name == "151 TH Prkcd Grin2c Glut"
and gene_target in [
    "Bbs5", "Ttc8", "Lztfl1", "Ift88", "Ift81", "Ift43",
    "Cep290", "Rpgrip1l", "Cplane1", "Arl3", "Kif3b", "Rpgr"
]
```

For each of those perturbations I counted `pvals_adj < 0.05`, inspected whether the only hit was the target transcript, and pulled the log fold change of BBSome genes. This filter returned exactly 207,108 rows, 12 perturbations x 17,259 measured genes.

Finally, I ran a Distributed Agents runtime `profile_compare` on the same 12 perturbations. That computed complete pairwise Pearson, Spearman, cosine, and same-direction top-tail overlaps on focal-cell `logfoldchanges`. The purpose was not to nominate a broad BBS9-like module from noisy null signatures; it was to check whether the BBSome/IFT/transition-zone controls that are biologically plausible for BBS9 actually converge at FDR level. They did not.

## Bbs9-specific reasoning

### External biological prior

`Bbs9` encodes a core BBSome subunit. BBSome is the ciliary trafficking coat discovered by Nachury et al. and functionally linked to ARL6/BBS3 by Jin et al.; BBS9 participates in the BBS2/BBS7/BBS9 assembly core, later joined by BBS1, BBS5, BBS8/TTC8, and BBS4. Veleri et al. showed that reducing BBS9 impairs ciliogenesis/ciliary function in ciliated model systems. So a `Bbs9` perturbation should be compared most strongly with other BBSome perturbations, and secondarily with perturbations to IFT machinery, transition-zone genes, and ciliary small-GTPase trafficking factors.

Direct core BBSome targets `Bbs1`, `Bbs2`, `Bbs4`, `Bbs7`, `Bbs9`, `Bbip1`, and `Arl6/Bbs3` were not available as training perturbations. The represented immediate subunit analogs were therefore `Bbs5` and `Ttc8/Bbs8`; `Lztfl1` was the closest measured BBSome-regulatory target; `Ift88`, `Ift81`, `Ift43`, `Kif3b`, `Cep290`, `Rpgrip1l`, `Cplane1`, `Rpgr`, and `Arl3` were boundary controls for the broader ciliary machinery.

### Same-experiment analogs

| training perturbation | focal `n_degs` | focal signature evidence | relevance to `Bbs9` |
|---|---:|---|---|
| `Bbs5` | 0 | 121 perturbed nuclei, 23,679 controls; `Bbs5` itself was down modestly, log2FC -0.425, `p_adj = 1`; no focal-cell gene crossed FDR 0.05. Runtime comparison to `Ttc8` gave Pearson 0.647 and cosine 0.711, but no shared FDR DE because `Bbs5` had none. | Best direct same-complex analog. BBS5 is an assembled BBSome component added with BBS8/TTC8 during BBSome assembly. Its complete focal null is strong evidence against broad downstream RNA remodeling after partial BBSome loss in this cell type. |
| `Ttc8` | 1 | 180 perturbed nuclei; the sole significant gene was the target transcript, `Ttc8` log2FC -0.663, `p_adj = 3.07e-05`; no downstream gene was significant. | BBS8/TTC8 is a core BBSome subunit. It shows that guide-mediated self-RNA depletion can appear as a singleton while the downstream ciliary response remains absent. |
| `Lztfl1` | 0 | 199 perturbed nuclei; `Lztfl1` log2FC -0.406, `p_adj = 1`; no significant focal-cell genes. | Close BBSome-trafficking regulator and ciliopathy gene. It is not an octameric BBSome subunit, so I used it as support for a buffered ciliary-trafficking surface rather than as a primary analog. |
| `Ift88`, `Ift81`, `Ift43` | 0, 0, 0 | Each had 17,259 assayed focal genes and zero FDR hits; target log2FCs were -0.563, -0.537, and -0.367 with `p_adj = 1`. | Core IFT genes test whether disrupting ciliary particle movement creates the same nuclear RNA state expected downstream of BBSome failure. They were flat. |
| `Kif3b` | 0 | Kinesin-II motor subunit; 156 perturbed nuclei and zero focal FDR hits. | Anterograde ciliary transport boundary. It argues that axonemal/ciliary transport perturbation was usually displaced from this basal snRNA endpoint. |
| `Cep290`, `Rpgrip1l`, `Cplane1`, `Rpgr` | 0, 0, 0, 0 | All had zero focal FDR hits; `Cep290` and `Rpgrip1l` were among the closest whole-profile neighbors of `Bbs5` inside the explicit ciliary cohort, but still with no significant features. | Transition-zone and photoreceptor-ciliary controls. They are not same-complex analogs, but their null responses reject a generic "ciliopathy gene equals broad 151 TH DEG response" rule. |
| `Arl3` | 1 | The only focal FDR hit was the `Arl3` self-transcript, log2FC -0.418, `p_adj = 0.0184`. | Ciliary lipidated-protein trafficking control. Like `Ttc8`, it demonstrates a singleton self-depletion pattern without downstream convergence. |

The internal Distributed Agents corpus gave the same qualitative read from the full same-experiment atlas. In release `perturbai-july-260713-sourceguard-1773-v1`, `Ttc8:F001` summarized `Ttc8` as target-self-down but downstream-flat across 22 measured neuronal groups, `Ttc8:F003` reported that `Bbs5`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Dync2h1`, `Lztfl1`, `Rpgrip1l`, `Ttc21b`, and `Cep290` did not form a hidden BBSome/IFT transcriptional module, and `Bbs5:F003` likewise found that represented BBSome/ciliary relatives did not phenocopy `Bbs5`.

### Zero/nonzero call

The same-complex evidence points to a zero or singleton call, not to a broad response:

- `Bbs5` is zero in the focal group.
- `Ttc8/Bbs8` is one, and that one gene is only `Ttc8` itself.
- The closest BBSome regulator and IFT/transition-zone controls are zero in the focal group.
- Runtime profile comparison found concordant nominal log-fold-change structure among these near-null ciliary perturbations, but not an FDR-supported shared gene set. The strongest Bbs5 whole-profile comparators inside this candidate set were still FDR-null, for example `Rpgrip1l` with Pearson 0.697, `Cep290` with Pearson 0.688, and `Ift88` with Pearson 0.684.

`Bbs9` is a structural BBSome subunit, so `Bbs5` and `Ttc8` are the mechanistically closest measured anchors. Since one of those two has zero DEGs and the other has only a self-transcript hit, the expected count for `Bbs9` is below one downstream gene. The focal parquet contains `Bbs9` as a measured transcript, but it was not altered at FDR level by any of the tested ciliary perturbations; whether a `Bbs9` guide would deplete its own RNA enough to pass FDR is unknowable from the held-out data. I therefore chose the lower, more common BBSome outcome:

```text
Bbs9 -> 0 predicted DEGs
```

## Limits

The comparison is imperfect because `Bbs9` itself and most other core BBSome assembly genes were held out or absent as perturbations; `Bbs5` and `Ttc8` are the only direct BBSome subunit anchors in the training endpoint table. The assay is basal snRNA-seq from postnatal NeuN+ nuclei and does not image primary cilia, quantify BBSome protein assembly, localize ciliary GPCRs, measure leptin/MC4R/SSTR3/GPR161 signaling, or sample retina, kidney, olfactory epithelium, and dense hypothalamic circuits where BBS biology can be stronger. Mosaic AAV CRISPR also produces partial and variable RNA depletion, so the absence of an FDR gene is compatible with residual protein or with a ciliary phenotype that fails to induce stable nuclear RNA. The top log-fold-change tails of these null signatures are noisy and often have `p_adj = 1`, so I used them only to reject a robust shared signature, not to assign gene-level mechanisms.
