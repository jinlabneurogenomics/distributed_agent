# Nr4a2 DEG-count prediction

## Question and scope

The held-out manifest for this run contains one perturbation, `Nr4a2`. I interpreted the task as predicting the integer `n_degs` that would have been observed for an acute AAV-PHP.eB CRISPR loss-of-function perturbation of mouse `Nr4a2` in the focal `151 TH Prkcd Grin2c Glut` Allen cell group, where `n_degs` is the count of assayed genes with Wilcoxon Benjamini-Hochberg `pvals_adj < 0.05`.

I treated `TH` as part of the Allen taxonomy label for this thalamic glutamatergic group, not as evidence that these are classical tyrosine-hydroxylase-positive midbrain dopaminergic neurons. That matters because `Nr4a2/Nurr1` has its strongest textbook role in midbrain dopamine-neuron differentiation and maintenance, whereas this endpoint is a juvenile, basal, sparse, postmitotic neuronal snRNA-seq readout in a thalamic Prkcd/Grin2c glutamatergic class.

## Sources

- Input data:
  - `[local file: training_de_all_cell_groups.parquet]`
  - `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - `[local file: 158_Nr4a2.csv]`
- Internal same-experiment corpus:
  - Distributed Agents corpus MCP release `perturbai-july-260713-sourceguard-1773-v1`
  - The corpus had no direct `Nr4a2` entry, because `Nr4a2` is held out here.
  - I used same-experiment corpus findings for `Nr4a1`, `Nr4a3`, `Pitx3`, and `Rora`.
- Run-local observed-profile analysis:
  - `profile_neighbors` over the parquet with `context = {"group_name": "151 TH Prkcd Grin2c Glut"}`, `value_column = logfoldchanges`, and `significance_column = pvals_adj` for `Nr4a1`, `Nr4a3`, `Creb1`, `Rora`, `Esrra`, `Nr1d1`, `Nrf1`, `Pitx3`, `Lmx1b`, `Foxa2`, and `Otx2`.
- External literature:
  - Zetterstrom et al. 1996, `doi:10.1210/mend.10.12.8961274`, on NR4A family DNA binding, constitutive activity, RXR heterodimerization differences, and CNS expression.
  - Eells et al. 2011, `doi:10.1007/s12031-011-9642-z`, on dynamic `Nr4a1`, `Nr4a2`, and `Nr4a3` regulation in VTA dopamine neurons and relationships to dopamine neurotransmission genes.
  - Tokuoka et al. 2013, `doi:10.1016/j.neulet.2013.11.033`, showing `Nurr1/Nr4a2` expression is activity-regulated through voltage-dependent calcium channels and calcineurin in cultured hippocampal and cortical neurons.
  - Chinta and Andersen 2004, `doi:10.1016/j.biocel.2004.09.009`, reviewing `Nurr1`, `Lmx1b`, and `Pitx3` as dopaminergic-development transcription factors.
  - Jacobs et al. 2009, `doi:10.1242/dev.029769`, showing `Pitx3` potentiates `Nurr1` in dopamine-neuron terminal differentiation.
  - Volpicelli et al. 2012, `doi:10.1371/journal.pone.0030661`, showing direct regulation of `Pitx3` by `Nurr1/Nr4a2`.
  - Hong et al. 2013, `doi:10.1089/scd.2013.0406`, showing overlapping but distinct functions of `Nurr1`, `Pitx3`, and `Lmx1a` during dopaminergic differentiation.
  - Boldingh Debernard et al. 2012, `doi:10.1016/j.neuint.2012.04.002`, comparing `Nr4a1`, `Nurr1/Nr4a2`, and `Nr4a3` expression and localization after glutamate treatment in neurons.

## Computation over the training data

1. I loaded the requested-target manifest and verified that the only held-out target in this run was `Nr4a2`.
2. I loaded the 151-cell training count CSV. It contained 1,674 non-held-out perturbations; 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and the maximum was 2,677.
3. I inspected the parquet row-group metadata and used the sorted `group_name` statistics to scan only row groups 546-580, the only groups overlapping `151 TH Prkcd Grin2c Glut`.
4. For candidate mechanistic analogs I counted rows with `pvals_adj < 0.05`, and checked whether the target's own measured transcript or likely downstream dopaminergic/thalamic markers were significantly changed.
5. I profiled signed log-fold-change vectors for candidate analogs against the focal eligible universe with `profile_neighbors`. I used this only as a check on whether flat signatures hid coherent all-gene neighborhoods. For the direct `Nr4a` and dopaminergic-development analogs, the profile status was `no_significant_features`; their top whole-profile or tail-overlap neighbors were weak and dominated by non-significant tail genes, so I did not treat those neighbors as biological evidence.

## Held-out target: Nr4a2

### Closest observed perturbations

| training target | 151 `n_degs` | focal expression evidence | how I used it |
| --- | ---: | --- | --- |
| `Nr4a1` | 0 | No FDR-significant genes in 151; self transcript `logfoldchanges = 0.143`, `padj = 1`. Distributed Agents reports `Nr4a1` had no FDR-gated downstream transcriptional response in any of 23 measured neuronal groups and did not induce compensatory `Nr4a2` or `Nr4a3`. | Best direct NR4A-family analog available in the training data. Its complete focal null supports a zero prediction for a basal single-NR4A perturbation. |
| `Nr4a3` | 0 | No FDR-significant genes in 151; minimum focal `padj = 0.166`; self transcript `logfoldchanges = -0.025`, `padj = 1`. The same-experiment corpus reports an almost entirely flat surface, with a single-cell-type `Xpo6` effect outside 151. | Second direct paralog. It argues against an automatic NR4A-family thalamic response in this assay. |
| `Creb1` | 10 | A small 151 signature, led by `Crem` up and a few weak downregulated genes; no NR4A-like module. | CREB is upstream of activity-responsive immediate-early transcription, so this is a loose activity-state comparator. The small nonzero response shows activity TFs can score, but it is not close enough to pull `Nr4a2` above zero. |
| `Pitx3` | 0 | No FDR-significant genes in 151; minimum `padj = 0.751`. Distributed Agents found `Pitx3` was FDR-flat across 23 measured groups and that the expected Pitx3/Nurr1 dopaminergic terminal-differentiation program was not recovered even in the pooled 215 MB Dopa group. | Strong external dopaminergic partner of `Nr4a2`; in this experiment it is a counterexample showing that acute P16 loss of canonical dopamine developmental factors need not yield a measurable basal snRNA signature. |
| `Lmx1b` | 0 | No FDR-significant genes in 151. | External mDA-network comparator. Its focal null is concordant with `Pitx3`. |
| `Foxa2` | 0 | No FDR-significant genes in 151. | External mDA/SHH-lineage comparator. It did not expose a 151 thalamic response. |
| `Otx2` | 0 | No FDR-significant genes in 151. | External developmental-neighborhood comparator. Flat in the focal group. |
| `En1`, `En2` | 0, 0 | No FDR-significant genes in 151 for either Engrailed factor. | Additional mesodiencephalic dopamine developmental comparators. Both were flat. |
| `Rorb` | 0 | No FDR-significant genes in 151. | Nuclear-receptor/thalamic counterexample from the ROR family; unlike `Rora`, it did not phenocopy the thalamic RORalpha response. |
| `Rora` | 278 | Broad, highly significant thalamic signature including `Prkcg`, `Adgrb1`, `Rasa4`, `Car4`, `Prkcd`, and `Grin2c`. Distributed Agents reports this is `Rora`-selective and not reproduced by `Rorb`/`Rorc`. | Positive counterexample: 151 can show a large nuclear-receptor response when the perturbed receptor maintains this thalamic program. It is not mechanistically close enough to transfer to `Nr4a2`. |
| `Esrra` | 57 | Moderate metabolic/synaptic 151 signature; self transcript was significantly down. | More distant orphan nuclear receptor. It shows some receptor KOs are detectable, but it is mitochondrial/metabolic rather than NR4A or thalamic-ROR biology. |
| `Nr1d1` | 116 | Distinct REV-ERB/clock-like 151 program. | Clock/nuclear-receptor counterexample, not an `Nr4a2` analog. |
| `Nrf1` | 138 | Mitochondrial/housekeeping-linked 151 response. | Transcription factor counterexample showing the assay can detect TF-driven 151 responses, but unrelated to NR4A2. |

The measured-gene scan added one more negative check: in 151 TH Prkcd Grin2c Glut, the `Nr4a2` transcript itself was not FDR-significantly changed by any of the 1,674 training perturbations. `Nr4a1` was FDR-significantly changed by 8 broad stress/proteostasis perturbations such as `Uba5`, `Sin3a`, `Tpr`, and `Ufc1`; `Nr4a3` was changed only by `Uba5` and `Ufc1`. In contrast, the focal marker genes `Prkcd` and `Grin2c` were repeatedly hit by broad 151 responders such as `Rora`, `Cic`, `Ctnnb1`, `Tpr`, `Psmb4`, and `Uba5`. Thus the dataset contains a strong thalamic identity/synapse axis, but `Nr4a2` was not a recurring member of that axis.

### Biological interpretation

`Nr4a2/Nurr1` is a constitutively active NR4A orphan nuclear receptor. External work makes three plausible hypotheses:

- It could resemble `Nr4a1`/`Nr4a3`, which bind related NR4A elements and are inducible in neurons.
- It could resemble the `Pitx3`/`Lmx1a`/`Lmx1b` dopaminergic transcriptional network.
- It could act as a broader neuronal activity or stress-response factor.

The same-experiment evidence weakens all three for this endpoint. The represented NR4A paralogs `Nr4a1` and `Nr4a3` were focal-zero, and the Distributed Agents corpus summarized them as mostly buffered under basal postnatal loss-of-function conditions rather than as standing neuronal maintenance hubs. The represented dopaminergic developmental partners `Pitx3`, `Lmx1b`, `Foxa2`, `Otx2`, `En1`, and `En2` were also focal-zero; the same-experiment `Pitx3` report specifically found no collapse of `Th`, `Slc6a3`, `Ddc`, `Nr4a2`, `Lmx1a/Lmx1b`, `En1/En2`, `Foxa2`, `Otx2`, `Ret`, `Bdnf`, or related genes in the pooled midbrain dopamine group. The looser activity-transcription comparators were either flat or sparse: `Creb1` had 10 DEGs and `Crebbp` had 8 in 151, while `Fosl2`, `Jund`, `Egr2`, `Mef2c`, and `Mef2d` were 0-1 DEGs.

The strongest positive nuclear-receptor example, `Rora`, is informative in the opposite direction. It caused 278 DEGs in 151 and downregulated `Prkcd` and `Grin2c`, showing that the cell group can mount a large nuclear-receptor response. But Distributed Agents reports that the RORalpha 151 signature is thalamic and `Rora`-selective rather than a generic nuclear-receptor signature: `Rorb`, `Rorc`, and other related clock or ROR/REV-ERB perturbations did not phenocopy it. I therefore used `Rora` as a counterexample to generic family transfer, not as a quantitative template for `Nr4a2`.

Taken together, the best within-dataset analogs all point below the one-DEG detection boundary in this cell group. I therefore predict no genes below FDR 0.05 for `Nr4a2`.

### Prediction

`Nr4a2`: predicted `n_degs = 0`.

## Limits

- `Nr4a2` itself was completely held out, and the Distributed Agents same-experiment corpus had no direct `Nr4a2` findings, so this is an extrapolation from paralogs and pathway neighbors.
- Several excellent dopaminergic targets were missing as perturbations in the training universe, including `Lmx1a`, `Th`, `Ddc`, `Slc6a3`, `Slc18a2`, and `Bdnf`.
- The best-established `Nr4a2` biology comes from embryonic or adult midbrain dopamine neurons, activity-challenged hippocampal/cortical neurons, or inflammatory glial contexts. The present assay used sparse postnatal loss of function in NeuN-positive nuclei under basal conditions and largely excluded glia.
- AAV sparse CRISPR averaged modest mRNA depletion per guide; a zero-DEG prediction is about this measured snRNA endpoint, not about whether NR4A2 protein, dopamine physiology, axons, or behavior would matter in a stronger or lineage-specific model.
- The 151 Allen group is still a coarse thalamic glutamatergic bin. A small `Nr4a2`-dependent subpopulation inside it could be diluted below the Wilcoxon/FDR threshold.
