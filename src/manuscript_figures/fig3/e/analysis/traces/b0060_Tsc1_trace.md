# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and endpoint

The task asks for one integer point prediction for the held-out perturbation `Tsc1`: the number of measured genes that would pass Benjamini-Hochberg FDR 0.05 in `151 TH Prkcd Grin2c Glut` nuclei after acute sparse CRISPR-Cas9 loss of function. I treated `n_degs` as the assay-specific count of significant differential-expression calls among recovered nuclei, not as viability, editing efficiency, cell abundance, or biological importance. `Tsc1` is absent from both supplied training inputs, so its own signature and count were not used.

## Sources used

- The declared focal training endpoint table,
  `/gpfs/group/jin/asun/bioagents/debug/260901_predict/holdout_task/Inputs/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Narrow reads of the declared differential-expression Parquet,
  `/gpfs/group/jin/asun/bioagents/debug/260901_predict/holdout_task/Inputs/training_de_all_cell_groups.parquet`, restricted to the focal cell group and mechanistic comparators.
- The run-local requested-target manifest,
  `/gpfs/group/jin/asun/bioagents/runs/holdout-prediction/july-260713-adaptive-seed-260901/prepared/manifests/deg-count/bs001/b0060.csv`, which contains only `Tsc1`.
- The same-experiment internal corpus `perturbai-july-260713-sourceguard-1773-v1`, specifically packaged Findings and Evidence for `Tsc2`, `Depdc5`, `Mtor`, and `Rptor`. This is an interpretation layer over the same Perturb-seq experiment, not independent replication.
- External mechanism/literature priors from PubMed:
  - Inoki et al. 2002, Nat Cell Biol, doi:10.1038/ncb839, PMID:12172553: TSC1 and TSC2 form a physical and functional complex that suppresses mTOR signaling, and AKT phosphorylation of TSC2 disrupts TSC1/TSC2 function.
  - Dibble et al. 2012, Mol Cell, doi:10.1016/j.molcel.2012.06.009, PMID:22795129: TBC1D7 is a third stable TSC-complex subunit, and the TSC1-TSC2-TBC1D7 complex has Rheb-GAP activity upstream of mTORC1.
  - Bar-Peled et al. 2013, Science, doi:10.1126/science.1232044, PMID:23723238: GATOR1, including DEPDC5, is a RagA/B GAP complex that inhibits amino-acid activation of mTORC1.
  - Schule et al. 2021, Int J Mol Sci, doi:10.3390/ijms22116034, PMID:34204880: mTORC1 signaling can transcriptionally regulate sterol/cholesterol biosynthesis genes in developing mouse cortical neurons.
  - Di Nardo et al. 2014, Hum Mol Genet, doi:10.1093/hmg/ddu101, PMID:24599401: neuronal Tsc1/Tsc2 loss intersects with mTORC1, AMPK, autophagy, and lysosomal regulation.
  - Yuskaitis et al. 2022, Cell Rep, doi:10.1016/j.celrep.2022.111278, PMID:36044864, and Iffland et al. 2019, Epilepsia, doi:10.1111/epi.16370, PMID:31625153: DEPDC5/GATOR1 are mTORC1 repressors relevant to neuronal and epilepsy biology, but through the amino-acid/Rag arm rather than through the identical TSC/Rheb node.

## Computation over the supplied dataset

1. I read the requested manifest and confirmed that `Tsc1` was the only target.
2. I summarized the 1,674 training `n_degs` values in the focal group. The distribution is sparse: 1,205 targets have zero DEGs, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only the 99th percentile exceeds about 436.
3. I looked up known mTOR-axis perturbations in the training-count table:

| training target | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Tsc2` | 86 | closest measured paralog/complex partner; negative Rheb-mTORC1 regulator |
| `Depdc5` | 13 | same-sign but upstream nutrient-sensing mTORC1 repressor |
| `Mtor` | 2 | catalytic mTOR component; loss has the opposite causal sign from TSC loss for mTORC1 activation |
| `Rptor` | 0 | core mTORC1 scaffold; loss also has the opposite causal sign and was flat |
| `Akt3` | 0 | upstream kinase input, not an obligate same-outcome perturbation |
| `Pik3r1` | 0 | upstream PI3K regulatory input, not an obligate same-outcome perturbation |

4. I queried the focal Parquet rows for `Tsc2`, `Depdc5`, `Mtor`, `Rptor`, `Akt3`, and `Pik3r1`:

```sql
SELECT gene_target, names, scores, logfoldchanges, pvals_adj
FROM training_de_all_cell_groups
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN ('Tsc2','Depdc5','Mtor','Rptor','Akt3','Pik3r1');
```

On the 86 genes significant after `Tsc2` loss at FDR 0.05, `Depdc5` was the only strong same-direction pathway comparator: cosine 0.616, with eight same-direction FDR<0.05 overlaps (`Amy1`, `Pik3r1`, `Rnpc3`, `Ldlr`, `Pik3r3`, `Tubb3`, `Snhg11`, `Msmo1`). `Mtor` and `Rptor` were anticorrelated on the same coordinate set, with no same-direction FDR<0.05 overlaps, and `Akt3`/`Pik3r1` were weak or flat. These calculations agree with the internal corpus summaries: Tsc2 produced a broader 151 response than Depdc5; Depdc5 shared the sterol/PI3K subprogram; Mtor/Rptor/Akt/PI3K nodes did not phenocopy loss of a negative mTORC1 regulator.

## Target-specific prediction

### `Tsc1`

`Tsc1` loss is predicted to be clearly nonzero and to be in the same response class as `Tsc2`, not as the many pathway-adjacent nulls. The causal chain is:

`Tsc1` CRISPR LoF -> destabilization or impairment of the TSC1/TSC2/TBC1D7 complex -> reduced Rheb-GAP restraint on mTORC1 -> excess mTORC1-dependent metabolic, lysosomal, sterol, and stress-feedback transcription -> a broad recovered-cell DE signature in susceptible thalamic glutamatergic neurons.

The strongest quantitative anchor is the `Tsc2` training perturbation, which had 86 FDR<0.05 DEGs in `151 TH Prkcd Grin2c Glut` with 177 matched perturbed nuclei. Its top focal genes included the sterol and PI3K-feedback markers `Cyp51`, `Pik3r3`, `Ldlr`, `Msmo1`, and `Pik3r1`. In the same-experiment corpus, the Tsc2 report summarized the response as a caudal metabolic/lysosomal mTORC1 program and noted that exact same-complex or direct-node tests for `Tsc1`, `Tbc1d7`, and `Rheb` were unavailable as training perturbations.

`Depdc5` supports a nonzero prediction but sets a lower bound rather than the point estimate. It had only 13 focal DEGs, yet it converged with Tsc2 in the same cell group on the sterol/LDL-uptake/PI3K subset: `Ldlr`, `Msmo1`, `Pik3r1`, `Pik3r3`, plus weaker or FDR<0.10 support for `Cyp51`, `Hmgcs1`, and `Insig1`. The external GATOR1 literature explains why this is only a partial analog: DEPDC5 removes amino-acid/Rag inhibition of mTORC1, whereas TSC1/TSC2 removes Rheb inhibition. That difference is sufficient to explain the much narrower `Depdc5` count without weakening the same-direction prior for `Tsc1`.

`Mtor`, `Rptor`, `Akt3`, and `Pik3r1` are counterexamples to generic mTOR-pathway scoring. `Mtor` loss produced just 2 focal DEGs; `Rptor`, `Akt3`, and `Pik3r1` produced 0. The Mtor and Rptor results do not argue against a Tsc1 effect because deleting an mTORC1 kinase or scaffold should reduce, not activate, the Rheb-mTORC1 output that appears after TSC loss. The flat Akt3 and Pik3r1 signatures also do not falsify Tsc1 because those are redundant or indirect upstream inputs rather than required subunits of the TSC complex.

I therefore transferred most of the `Tsc2` count to `Tsc1`, with a small downward adjustment for two uncertainties: TSC2 carries the catalytic GAP activity whereas TSC1 is the stabilizing partner, and the held-out `Tsc1` guides could have had fewer recovered edited nuclei or a weaker effective perturbation than the measured `Tsc2` guides. The final point prediction is:

| target | prediction |
| --- | ---: |
| `Tsc1` | 80 |

## Limits and uncertainty

The requested endpoint is directly observed for training perturbations but absent for `Tsc1`; the answer is a biological transfer prediction from `Tsc2`, not a measurement of `Tsc1`. The strongest analog is single-target rather than an average over multiple TSC-complex members because `Tbc1d7` and `Rheb` were also absent from the training Parquet. Count scale is strongly affected by guide efficacy, recovered-cell number, and focal-cell statistical power, none of which can be observed for the held-out perturbation. The internal Findings and the Parquet are two representations of the same experiment, so their agreement establishes consistency and exact row support but not replication. External work establishes the TSC1/TSC2/Rheb/mTORC1 causal link in other systems and some neuronal contexts; it does not pin down how many genes pass FDR 0.05 in this postnatal sparse AAV-PHP.eB thalamic snRNA-seq assay.
