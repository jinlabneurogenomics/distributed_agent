# Slc12a5 DEG-count prediction

## Question

The requested held-out perturbation set contains one target, `Slc12a5`.
I interpreted the task as a point prediction of the number of measured genes
with Wilcoxon Benjamini-Hochberg adjusted `pvals_adj < 0.05` after sparse
postnatal AAV-CRISPR loss of `Slc12a5` in `151 TH Prkcd Grin2c Glut` thalamic
glutamatergic neurons. The count includes any significant `Slc12a5` self-row,
because the supplied training endpoint does the same. I did not treat target
RNA knockdown as an editing-efficiency filter: the dataset portrait notes that
self-RNA loss is a weak QC readout and is uncoupled from downstream effect size.

## Sources

- Declared DE Parquet:
  `training differential-expression dataset`.
- Declared focal training counts:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared held-out manifest:
  `single-target request for Slc12a5`.
- Same-experiment interpretation corpus: PerturbAI July 260713 Sourceguard
  1773 v1 Findings/Evidence ledger. This is a semantic layer over the same
  experiment, not an independent replicate.
- External literature from PubMed: Watanabe and Fukuda 2015,
  doi:10.3389/fncel.2015.00371; Huang et al. 2019,
  doi:10.14336/AD.2018.0928; Rinehart et al. 2011,
  doi:10.1074/jbc.M111.222893; Watanabe et al. 2019,
  doi:10.1126/scisignal.aaw9315; Come et al. 2019,
  doi:10.3389/fncel.2019.00048; Kontou et al. 2021,
  doi:10.1016/j.jbc.2021.100364.

## Quantitative calibration

The endpoint is directly observed for training genes and absent only for the
held-out target. I therefore started from the focal training count table rather
than from graph or literature evidence. In `151 TH Prkcd Grin2c Glut`,
1,205/1,674 training perturbations had 0 FDR 0.05 DEGs, 276 had exactly 1 DEG,
65 had 2-5 DEGs, 50 had 6-20, and 78 had more than 20; the median count was 0,
the mean was 14.05, the 95th percentile was 18, and the maximum was 2,677. This
cell group can support very large signatures, but the usual perturbation is a
null or a self-row-only event.

I then pulled all focal-cell DE rows for a small mechanistic comparator panel
from the Parquet with a `group_name == "151 TH Prkcd Grin2c Glut"` and
`gene_target in (...)` filter and counted adjusted `pvals_adj < 0.05` and
`pvals_adj < 0.10` rows. The relevant observed FDR 0.05 counts were:

| training perturbation | focal `n_degs` | expression-pattern evidence |
| --- | ---: | --- |
| `Slc12a2` | 0 | Only represented SLC12 cation-chloride cotransporter target; no focal row passed FDR 0.10 and the best nominal rows all had adjusted p-value 1.0. |
| `Wnk1` | 0 | No focal FDR 0.10 row; best nominal rows all had adjusted p-value 1.0. |
| `Stk39` | 0 | No focal FDR 0.10 row; the smallest adjusted p-value was 0.661. |
| `Wnk3` | 1 | One focal hit, `Ppp2cb` down, `logfoldchanges = -0.554`, `pvals_adj = 0.0315`; no broader transporter, synaptic, or stress program. |
| `Slc6a1` | 0 | GABA transporter; no focal FDR 0.10 row. |
| `Slc6a5` | 0 | Glycine transporter; no focal FDR 0.10 row. |
| `Slc4a7` | 0 | Neuronal bicarbonate transporter; no focal FDR 0.10 row. |
| `Slc9a7` | 1 | The single focal hit was the target self-transcript. |
| `App` | 1 | A KCC2-interacting synaptic protein in the literature; the single focal hit was the target self-transcript. |
| `Gabra1`, `Gabbr1`, `Gabbr2`, `Kcnq2`, `Kcnq3` | 1 each | Mostly self-transcript-only or very small receptor/channel perturbations. |
| `Gabrb2` | 4 | A small GABA_A receptor response with activity genes such as `Nr4a1` and `Vgf`, showing that chloride-linked receptor changes can be visible but usually do not explode in this endpoint. |
| `Grin1`, `Grin2a`, `Grin2b`, `Grin2d` | 89, 1, 2, 0 | NMDA receptor disruption is a positive excitability counterexample: `Grin1` produced a true 89-gene focal program, whereas non-obligate subunits were much smaller or null. |

The internal July corpus agreed with the raw counts. Its `Slc12a2` report
states that `Slc12a2` loss was an FDR-level transcriptomic null across all 23
recovered neuronal classes; that `Slc12a5` and the other KCC paralogs were
absent as perturbation targets; and that WNK/SPAK/PKC comparators such as
`Wnk1`, `Wnk3`, `Stk39`, `Strada`, and `Prkca` did not converge on a
Slc12a2-like RNA program. The resolved evidence for that report gave
near-zero Slc12a2 whole-surface Wilcoxon-score correlations to `Wnk3`
(`r = 0.0096`), `Stk39` (`r = 0.0073`), `Wnk1` (`r = 0.0025`), and `Gabrb2`
(`r = -0.0069`) among 1,772 other targets. The `Stk39`, `Wnk1`, and `Wnk3`
reports similarly summarized the represented WNK-SPAK-cation-chloride
cotransporter module as almost entirely invisible to basal postnatal neuronal
nuclear RNA: `Wnk1` and `Stk39` were flat across their recovered groups, and
`Wnk3` had only three FDR 0.10 downstream genes in two cell groups.

## Slc12a5 rationale

`Slc12a5` encodes KCC2, the neuron-enriched K+/Cl- cotransporter that extrudes
chloride and permits mature GABA_A and glycine receptor currents to be
hyperpolarizing. NKCC1/`Slc12a2` has the opposite flux direction and is more
important for raising intracellular chloride in immature neurons and some
disease settings. WNK kinases and SPAK/OSR1 regulate NKCC1 and KCC2 mainly by
phosphorylation; WNK signaling tends to activate NKCC1 and inhibit KCC2, so
loss of `Wnk1`, `Wnk3`, or `Stk39` is not a same-sign molecular intervention
for loss of KCC2 itself. Those perturbations are therefore counterexamples for
whether the pathway creates a shared RNA module, not direct phenocopies of
`Slc12a5` loss.

The expected causal chain is: acute sparse `Slc12a5` CRISPR loss ->
reduced KCC2 protein or function at the membrane -> impaired chloride
extrusion and a depolarized GABA_A reversal potential -> altered inhibition
and possible excitability/survival stress -> recovery only of nuclei that
survive and retain the thalamic glutamatergic state -> single-nucleus
Wilcoxon DE. External genetics and physiology say that KCC2 is essential for
normal chloride homeostasis and that strong mature-neuron loss can be toxic:
phosphomimetic Kcc2 Thr906/Thr1007 mice have impaired KCC2-dependent chloride
extrusion and early death, and conditional KCC2 ablation or pharmacologic
KCC2 inhibition in mature neurons can rapidly activate apoptosis. Those
papers support a real biological consequence of KCC2 loss, but they do not
establish that surviving, sparsely edited P37-P44 thalamic nuclei will retain
a broad steady-state mRNA signature.

For the requested DEG-count endpoint, the local evidence points to a near-null
prediction. The closest direct transporter comparator, `Slc12a2`, had 0 focal
DEGs and no pan-neuronal downstream signature. The WNK/SPAK regulators
`Wnk1`, `Wnk3`, and `Stk39` did not form a common transcriptional module with
SLC12 transport biology; this is exactly what is expected if their main output
is transporter phosphorylation and chloride flux rather than transcription.
The GABA/glycine uptake comparators `Slc6a1` and `Slc6a5` were also 0 in the
focal group. The small positive `Gabrb2` and `Grin1` signatures show the focal
cell group can produce activity-linked RNA responses, but GABA_A subunit loss
or obligatory NMDA receptor loss is a different direct perturbation from
partially lowering KCC2 in a recovered survivor nucleus.

I therefore predicted a nonzero but single-gene-sized response, `1` DEG. The
one count is driven by a plausible `Slc12a5` self-transcript hit in a mature
neuronal population where KCC2 should be expressed, not by expectation of a
large downstream program. A strict zero would also be defensible given
`Slc12a2`, `Wnk1`, and `Stk39`, but several highly expressed ion-channel and
transporter perturbations in the same table register only their target RNA
(`Slc9a7`, `Kcnq2`, `Kcnq3`) or one to two rows (`Grin2a`, `Grin2b`), which
fits `Slc12a5` better than a broad `Grin1`-like effect.

## Limits

`Slc12a5` itself, the other KCC paralogs, `Wnk2`, `Wnk4`, and `Oxsr1` were not
represented as training perturbations, so the best direct same-pathway
evidence comes from the opposite-direction NKCC1 transporter and upstream
kinases. The DE Parquet has no raw baseline expression, chloride flux,
phospho-KCC2, GABA_A reversal potential, protein abundance, DNA indels, or
pre-assay depletion, so it cannot distinguish ineffective perturbation from
early death followed by a quiet survivor transcriptome. Germline and
conditional KCC2 studies used stronger, cleaner genetic lesions than this
P16 mosaic AAV-CRISPR screen. The final value is consequently an assay-breadth
estimate anchored to same-experiment null analogs with external knowledge used
only to decide which analogs should and should not transfer mechanistically.
