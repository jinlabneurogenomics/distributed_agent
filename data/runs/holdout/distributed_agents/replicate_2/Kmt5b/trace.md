# Kmt5b DEG-count prediction

## Question and resolved ambiguities

The held-out manifest for this run contains one requested target, `Kmt5b`. I interpreted the requested value as the number of genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` in the single-nucleus Wilcoxon table, including the perturbed gene itself if it passed the same FDR threshold. `Kmt5b` was absent from both training files, so I did not use any Kmt5b endpoint or signature from the experiment.

The expected endpoint is assay-specific. I therefore used external biology only to decide which held-in perturbations were credible analogs or counterexamples, and used the supplied `151 TH Prkcd Grin2c Glut` training counts and same-cell DE signatures to calibrate the size of the count.

## Sources

Internal / supplied sources:

- `[local file: 124_Kmt5b.csv]`: confirmed that the only requested target was `Kmt5b`.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: observed training `n_degs` values for the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`: focal-cell differential-expression profiles for the held-in perturbations.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`: `Kmt5b` had no target-centered claims, findings, or graph edges in the policy-filtered corpus. I used the same corpus for neighboring held-in chromatin controls; its Chd8 and Setd5 entries explicitly warn that acute P16 neuronal chromatin perturbations are not interchangeable by family label.
- Distributed Agents runtime profile comparison over a 15-gene chromatin panel, using `logfoldchanges` as signed values and `pvals_adj < 0.05` as the activity threshold in the focal group.

External sources were PubMed-indexed literature:

- Wu et al., 2013, FEBS Letters, DOI `10.1016/j.febslet.2013.10.020`: SUV420H1/KMT5B and SUV420H2/KMT5C are homologous H4K20 methyltransferases that prefer monomethylated H4K20 substrate in vitro.
- Jorgensen, Schotta & Sorensen, 2013, Nucleic Acids Research, DOI `10.1093/nar/gkt012`: review of H4K20 methylation by SET8/PR-Set7/KMT5A and SUV4-20H1/2 in genome integrity, DNA replication, DNA repair, and chromatin compaction.
- Gabellini & Pedrotti, 2022, International Journal of Molecular Sciences, DOI `10.3390/ijms23094736`: review of SUV4-20H1/H2 functions in health and disease.
- Lin et al., 2023, Cell Discovery, DOI `10.1038/s41421-023-00620-5`; Huang et al., 2023, Molecular Cell, DOI `10.1016/j.molcel.2023.07.001`; and Abini-Agbomson et al., 2023, Molecular Cell, DOI `10.1016/j.molcel.2023.07.020`: structural studies of SUV420H1/H2A.Z nucleosome recognition and catalytic or non-catalytic chromatin mechanisms.
- Stessman et al., 2017, Nature Genetics, DOI `10.1038/ng.3792`; Faundes et al., 2017, American Journal of Human Genetics, DOI `10.1016/j.ajhg.2017.11.013`; Sheppard et al., 2023, Science Advances, DOI `10.1126/sciadv.ade1463`: human genetic and model-system evidence that KMT5B haploinsufficiency causes a neurodevelopmental disorder and perturbs nervous-system developmental pathways.
- Paulsen et al., 2022, Nature, DOI `10.1038/s41586-021-04358-6`: human cortical organoid perturbations of SUV420H1/KMT5B, ARID1B, and CHD8 converge on asynchronous development of GABAergic and deep-layer excitatory cortical neurons through largely distinct molecular paths.
- Chen et al., 2022, Journal of Genetics and Genomics, DOI `10.1016/j.jgg.2022.03.004`: Kmt5b loss of function in developmental mouse cortical neuron models impairs neuronal development and neurogenesis.

## Computations over the training data

I first summarized the training endpoint for the focal cell group. Among 1,674 held-in perturbations, 469 had a nonzero FDR-0.05 count; the median was 0, the 75th percentile was 1, the 95th percentile was 18, and the maximum was 2,677. This means even biologically important chromatin or neurodevelopmental genes are often transcriptionally flat in this postnatal mosaic assay.

I then pulled the focal rows for selected chromatin, SET-domain, histone-methylation, and neurodevelopmental-disease controls. The full parquet has 616,253,184 rows, so I used Parquet row-group metadata to restrict to row groups 546-580, the groups whose `group_name` min/max overlapped `151 TH Prkcd Grin2c Glut`, and then filtered `gene_target` to the chosen comparator list. In outline:

```python
for i in range(546, 581):
    tbl = pf.read_row_group(
        i,
        columns=["names", "gene_target", "scores",
                 "logfoldchanges", "pvals", "pvals_adj", "group_name"],
    )
    mask = (
        pc.equal(tbl["group_name"], "151 TH Prkcd Grin2c Glut")
        & pc.is_in(tbl["gene_target"], value_set=pa.array(targets))
    )
```

Each retained perturbation had 17,259 measured gene rows. The observed focal-cell counts for the most relevant held-in perturbations were:

| held-in target | focal `n_degs` | relevance to `Kmt5b` |
|---|---:|---|
| `Ehmt1` | 4 | repressive lysine methyltransferase / H3K9 writer; very small, all-up focal signature |
| `Setdb1` | 22 | heterochromatin H3K9 trimethyltransferase; modest response |
| `Setd5` | 9 | chromatin/NDD gene; Distributed Agents found a small TH Prkcd/Grin2c module but no exact FDR phenocopy by SET-family or other obvious chromatin comparators |
| `Ash1l` | 1 | SET-domain chromatin NDD gene, self-only at FDR 0.05 |
| `Kmt2a` | 24 | H3K4 methyltransferase; modest response including target down-regulation |
| `Kmt2c` | 0 | related KMT2/COMPASS-family writer; flat counterexample |
| `Nsd1` | 23 | H3K36 writer and overgrowth/NDD gene; modest response |
| `Nsd2` | 0 | related NSD-family writer; flat counterexample |
| `Setd1a` | 368 | active COMPASS H3K4 writer and high-side counterexample; much broader than most SET-domain genes |
| `Mecp2` | 16 | methyl-DNA/chromatin neuronal disease regulator; modest response |
| `Dnmt3a` | 0 | DNA methyltransferase and chromatin-disease control; flat in this exact cell group |
| `Chd8` | 61 | active ASD chromatin remodeler; corpus notes it is not phenocopied by other CHD/ASD chromatin genes |
| `Arid1b` | 1 | BAF chromatin ASD gene, self-only in the focal group |
| `Mbd5` | 0 | methyl-CpG/NDD gene; flat counterexample |
| `Kat6a` / `Kat6b` | 0 / 0 | histone acetyltransferase NDD genes; flat counterexamples |

The Distributed Agents runtime pairwise profile comparison over `Ash1l`, `Brd1`, `Chd8`, `Dnmt3a`, `Ehmt1`, `Kdm5c`, `Kmt2a`, `Kmt2c`, `Mbd5`, `Mecp2`, `Nsd1`, `Nsd2`, `Setd1a`, `Setd5`, and `Setdb1` computed 105 same-cell signature comparisons. The small HMT/chromatin responses had little exact FDR-level overlap: for example `Ehmt1` had zero significant intersections with `Setd1a`, `Chd8`, `Mecp2`, `Kdm5c`, `Ash1l`, `Dnmt3a`, `Kmt2c`, `Brd1`, `Nsd2`, or `Mbd5`; `Setd5` likewise had no same-direction significant overlap with those peers in this strict FDR-0.05 focal slice. `Nsd1` and `Kdm5c` were a partial exception, sharing five same-direction up genes. I treated broad whole-profile correlations as weak because they were dominated by nonsignificant ranks; the FDR-overlap view better matched the endpoint I needed to predict.

## Target-specific reasoning

`Kmt5b` encodes SUV420H1, an H4K20me2/3 methyltransferase. The closest true H4K20 partners would be `Kmt5a`/SET8, which lays down H4K20me1, and `Kmt5c`/SUV420H2, a paralogous SUV4-20 enzyme. Neither was available as a held-in focal comparator, so all transfers are indirect.

The external literature supports a nonzero prior for `Kmt5b`: heterozygous loss is a human neurodevelopmental-disorder mechanism, SUV420H1 haploinsufficiency shifts cortical organoid neuron development, patient lymphoblasts and Kmt5b-haploinsufficient mouse brains have RNA-seq changes in nervous-system-development and axon-guidance pathways, and experimental Kmt5b knockdown perturbs cortical neuron morphogenesis. However, the mechanistic literature also points to functions that are strongest during replication, DNA-damage handling, heterochromatin formation, and embryonic or progenitor neurodevelopment. Those settings are imperfect matches to sparse AAV CRISPR starting at P16, followed by basal snRNA-seq from already specified NeuN+ thalamic glutamatergic nuclei at P37-P44.

The focal training set favors a small response, not a broad one. The nearest histone-methylation controls were low: `Ehmt1` had 4 DEGs, `Setdb1` 22, `Kmt2a` 24, `Nsd1` 23, and `Setd5` 9. Several equally plausible chromatin/NDD controls were essentially buffered: `Kmt2c` 0, `Nsd2` 0, `Dnmt3a` 0, `Kat6a` 0, `Kat6b` 0, `Mbd5` 0, `Ash1l` 1, and `Arid1b` 1. The main high counterexample, `Setd1a` at 368 DEGs, is separated by the same-experiment corpus from measured KMT2 and ASD/chromatin comparators rather than serving as a general SET-domain template. `Chd8` at 61 is also a poor direct analog: the corpus records that other CHD paralogs, Wnt/beta-catenin targets, BAF components, `Kmt2a`, and `Kdm5c` did not phenocopy `Chd8` in the P16 neuronal assay.

I therefore predicted a low but detectable count. Four DEGs matches the lower end of the held-in repressive methyltransferase range (`Ehmt1`, 4) and keeps the estimate below the 9-24 DEG band for broader chromatin writers because the strongest KMT5B biology is developmental/replication-coupled and because SUV4-20H2/KMT5C could partially buffer H4K20me2/3 loss.

## Final point prediction

| target | predicted `n_degs` |
|---|---:|
| `Kmt5b` | 4 |

## Limits

- There was no Kmt5b-centered Distributed Agents corpus evidence after holdout filtering, so the corpus could only supply negative context and held-in chromatin counterexamples.
- `Kmt5a` and `Kmt5c`, the most direct H4K20-pathway comparators, were not available as training perturbations.
- Most KMT5B literature studies embryonic progenitors, human organoids, transformed cells, or constitutive/heterozygous disease states. These are useful for mechanism but weak for the P16-to-P37/P44 sparse CRISPR, NeuN+ snRNA-seq endpoint.
- Several observed comparator signatures were tiny; a change of only a few nuclei or genes near the FDR threshold could move their `n_degs` values substantially.
- The integer `4` should be read as a calibrated point estimate for this exact Wilcoxon/FDR assay, not as a statement that Kmt5b has only four biological downstream targets.
