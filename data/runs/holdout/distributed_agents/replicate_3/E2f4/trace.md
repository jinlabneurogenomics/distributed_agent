# Held-out DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The requested held-out manifest contains one perturbation, `E2f4`. The task is to
predict the number of measured genes that will pass Benjamini-Hochberg adjusted
Wilcoxon `pvals_adj < 0.05` in the focal `151 TH Prkcd Grin2c Glut` population.
I treated `n_degs` as the assay-specific breadth of the recovered-nucleus
single-nucleus RNA-seq response, not as a measure of editing efficiency,
viability, or importance of the target gene. Zero therefore means "no measured
gene is expected to cross this FDR cutoff in this assay and cell group."

`E2f4` is completely held out: it is absent from both the focal training-count
CSV and the differential-expression parquet. The only numeric evidence used for
the prediction therefore comes from non-held-out perturbations.

## Sources used

* Input endpoint table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
* Input differential-expression table:
  `[local file: training_de_all_cell_groups.parquet]`
* Held-out manifest:
  `[local file: 064_E2f4.csv]`
* Same-experiment semantic layer: Distributed Agents corpus release
  `perturbai-july-260713-sourceguard-1773-v1`. This is a curated
  interpretation layer over the supplied Perturb-seq experiment, not an
  independent replication.
* PubMed literature for the prior that E2F4 is a repressive E2F/DREAM factor in
  quiescent cell-cycle control and neuronal differentiation:
  * Litovchick et al. 2007, DOI `10.1016/j.molcel.2007.04.015`, PMID `17531812`
  * Litovchick et al. 2011, DOI `10.1101/gad.2034211`, PMID `21498570`
  * Guiley et al. 2015, DOI `10.1101/gad.257568.114`, PMID `25917549`
  * Dagnino et al. 1997, DOI `10.1016/s0925-4773(97)00083-x`, PMID `9376316`
  * Persengiev et al. 1999, DOI `10.1128/MCB.19.9.6048`, PMID `10454552`

## Dataset computations

I first loaded the manifest and the 1,674-target focal training count table and
confirmed that `E2f4` was the only requested target and was absent from the
observed training endpoint. The focal endpoint distribution was highly sparse:
1,205 of 1,674 non-held-out perturbations had `n_degs = 0`, the median was 0,
the 75th percentile was 1, and the 95th percentile was 18. This made a zero
prediction a realistic calibrated baseline unless there was strong
mechanism-specific evidence for a broader E2f4 response.

For the most relevant represented E2F/DP targets and adjacent cell-cycle
controls, I queried the focal rows of the parquet and counted significant genes:

```sql
SELECT gene_target,
       count(*) FILTER (WHERE pvals_adj < 0.05) AS n005,
       count(*) FILTER (WHERE pvals_adj < 0.10) AS n010,
       count(*) FILTER (WHERE pvals_adj < 0.25) AS n025
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ('E2f1','E2f5','Tfdp1','Tfdp2',
                      'Trp53','Atr','Cdkn2a')
GROUP BY gene_target;
```

The direct analog counts were:

| training perturbation | relation to E2f4 | focal `n_degs` | relaxed focal FDR check |
| --- | --- | ---: | --- |
| `E2f5` | closest represented repressive E2F paralog; can substitute with E2F4 in p107/p130-DREAM-like repression | 0 | 0 genes even at FDR 0.25; minimum adjusted p-value was 1.0 |
| `E2f1` | represented E2F family member, but an activating/apoptotic E2F rather than the direct E2F4 paralog | 0 | 0 genes even at FDR 0.25; minimum adjusted p-value was 1.0 |
| `Tfdp1` | DP1 dimerization partner used by E2F4/E2F5 and activating E2Fs | 2 | 2 genes at FDR 0.10 and 4 at FDR 0.25 |
| `Tfdp2` | DP2 paralog | 0 | 0 genes even at FDR 0.25; minimum adjusted p-value was 1.0 |
| `Cdkn2a` | upstream RB/E2F cell-cycle brake; boundary comparator | 0 | 0 genes at FDR 0.25 |
| `Trp53` | stress/apoptosis comparator often connected to E2F cell-cycle re-entry | 0 | 0 genes at FDR 0.25 |
| `Atr` | DNA-damage/checkpoint comparator | 0 | 0 genes at FDR 0.25 |

`Tfdp1` was the only non-null direct-family profile. Its two focal FDR 0.05 hits
were both up-regulated, `Cntrob` (`log2FC = 0.663`, `q = 0.0114`) and `Dcaf15`
(`log2FC = 0.534`, `q = 0.0346`). They are not canonical E2F/DREAM G1/S or
DNA-replication genes. A profile comparison over `E2f1`, `E2f5`, `Tfdp1`, and
`Tfdp2` in the focal cell group also found no shared FDR-significant feature
between `Tfdp1` and any of the zero-DE relatives. Thus the two `Tfdp1` genes were
treated as a narrow DP1-specific escape, not as a reason to assign every
E2F/DP-family member a small nonzero count.

## Target-specific reasoning

### `E2f4`

**Within-dataset analogs.** The nearest measured perturbation to `E2f4` is
`E2f5`: both are repressive E2F-family members that cooperate with DP factors
and pocket proteins rather than classic E2F activators. `E2f5` had 0 focal DEGs,
and the Distributed Agents corpus reports it as having no corrected downstream response
in any represented NeuN-positive neuronal group. The same corpus specifically
annotates the E2f5 comparison to `E2f1`, `Tfdp1`, and `Tfdp2` as absence of
canonical E2F/DREAM G1/S derepression after perturbing the represented E2F/DP
family.

The next mechanistically relevant analogs were the E2F dimerization partners
`Tfdp1` and `Tfdp2`. `Tfdp2` was fully null in the focal group, and `Tfdp1` had
only the two `Cntrob`/`Dcaf15` hits above. Distributed Agents claim
`claim:e16a32bdeefb0be7da9d` summarizes the same-experiment finding that single
perturbations of represented E2F/DP family members did not engage a coordinated
G1/S, replication, mitotic, or apoptotic nuclear transcriptomic program in
settled postnatal neurons; `claim:9b88c53326aed0b42f87` separates the sparse
`Tfdp1` thalamic response from a generic E2F/DP-family program. Those claims
match the focal count data above.

`E2f1` was kept as a counterexample rather than as the primary analog. E2F1 is
an E2F activator and stress-linked apoptotic effector, so its zero focal count
does not prove that a repressive E2F4 knockout is silent. It is still useful
because the expected proliferative or apoptotic cell-cycle programs were also
absent after perturbing `Cdkn2a`, `Trp53`, and `Atr` in the focal group. This
argues that the basal P16-to-P37/P44 NeuN-positive state is not poised to
convert individual E2F-axis or checkpoint losses into a broad nuclear mRNA
signature.

**External mechanism.** E2F4 is a core repressive E2F: Litovchick et al. showed
that the mammalian DREAM complex contains p130/RBL2, E2F4, DP, and the MuvB
core and represses hundreds of cell-cycle-dependent promoters during G0
(Litovchick et al. 2007). DREAM assembly is controlled through DYRK1A-dependent
LIN52 phosphorylation (Litovchick et al. 2011), and structural work showed how
phospho-LIN52 recruits p107/p130 to the MuvB core used with E2F4/E2F5 (Guiley
et al. 2015). That makes E2F4 a biologically plausible transcriptional repressor
and makes DP-family perturbations appropriate analogs. In neural contexts,
E2F-family transcripts are developmentally regulated in mouse nervous system
development (Dagnino et al. 1997), and E2F4 can promote NGF-induced PC12
neuronal differentiation and rises as rat neuroblasts become postmitotic
(Persengiev et al. 1999), so I did not dismiss `E2f4` as a purely cycling-cell
factor.

**Zero/nonzero decision and count.** Despite that biological prior, the measured
acute postnatal neuronal training data point to a zero endpoint. The closest
available repressive paralog `E2f5` and the DP2 partner `Tfdp2` were completely
FDR-null in the focal group; the core DP1 perturbation yielded only two
noncanonical genes; and no represented E2F/DP perturbation uncovered an
S-phase/DNA-replication/apoptotic module. Since `E2f4` is a single mosaic
postnatal knockout in already postmitotic neurons, not a combined E2f4/E2f5 or
MuvB/pocket-protein knockout in dividing cells, I predict that no gene will
survive FDR 0.05. The point prediction is `0`.

## Limits

The largest limitation is that the most direct E2F4 DREAM partners were not
available as training perturbations in the focal endpoint: `E2f4` itself was
held out, and `Rb1`, `Rbl1`, `Rbl2`, `Lin9`, `Lin37`, `Lin52`, `Lin54`, `Mybl2`,
and `Foxm1` were absent from the 1,674-target focal training count table.
Therefore the prediction relies on `E2f5` and DP-family perturbations rather
than a full DREAM-complex series.

The external literature mostly measures proliferating cells, quiescent cultured
cells, developmental neuroblasts, or PC12 differentiation. Those settings are
not equivalent to sparse AAV CRISPR loss of function delivered at P16 and read
out in surviving NeuN-positive thalamic neurons 3 to 4 weeks later. The screen
also measured nuclear RNA only; it did not test cell-cycle protein abundance,
chromatin binding, electrophysiology, behavior, DNA indels, or effects in
unsampled progenitors, choroid plexus, ependyma, or glia. A combined or earlier
E2f4/E2f5 perturbation could reveal biology that this single-gene postnatal
prediction assigns to zero.
