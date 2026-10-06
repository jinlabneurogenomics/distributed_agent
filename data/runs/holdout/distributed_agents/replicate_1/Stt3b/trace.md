# DEG-count prediction trace

## Question and endpoint

I interpreted the task as a scalar prediction for one held-out perturbation,
`Stt3b`, in the focal cell group `151 TH Prkcd Grin2c Glut`.  The endpoint is
exactly the focal-cell count of measured genes whose Wilcoxon
Benjamini-Hochberg adjusted p value is below 0.05 after acute mosaic
CRISPR-Cas9 loss of the target from P16 to P37-P44.  The held-out `Stt3b`
perturbation itself was not available in either the differential-expression
Parquet or the focal training endpoint CSV, so there is no self-signature to
query and no direct Stt3b DEG count.

The only ambiguity I resolved was how to compare a held-out oligosaccharyl-
transferase subunit to the available training genes.  The focal training set
does not contain the strict `Stt3b` paralog or most core OST subunits:
`Stt3a`, `Ddost`, `Rpn1`, `Rpn2`, `Dad1`, `Ostc`, `Ost4`, `Magt1`, and `Tusc3`
were absent as training targets in the focal DEG-count CSV.  I therefore used
nearby ER glycosylation, ER chaperone, unfolded-protein-response, and
proteostasis perturbations that were actually represented in the training
data, and treated them as analogs only where the causal lesion was close
enough to predict the requested transcriptional endpoint.

## Sources

- Declared input endpoint table:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared input differential-expression Parquet:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Stt3b`.
- Run-local dataset portrait and capability manifests in `codex_runtime/pipeline/`.
- Internal same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, specifically bounded Finding
  records for `Hspa5`, `Sec63`, `Edem3`, `Gfpt1`, `Dhdds`, and `Atp2a2`.
  These are interpreted reports over the same Perturb-seq experiment, not
  independent replication of the Parquet.
- PubMed-indexed external literature for OST biology:
  Kelleher et al. 2003, Mol Cell, DOI `10.1016/s1097-2765(03)00243-0`;
  Ruiz-Canada et al. 2009, Cell, DOI `10.1016/j.cell.2008.11.047`;
  Shrimal et al. 2013, Hum Mol Genet, DOI `10.1093/hmg/ddt312`;
  Shrimal et al. 2014, Semin Cell Dev Biol, DOI
  `10.1016/j.semcdb.2014.11.005`;
  Cherepanova et al. 2019, J Cell Biol, DOI `10.1083/jcb.201904004`;
  Lu et al. 2018, PNAS, DOI `10.1073/pnas.1806034115`;
  Wen et al. 2022, Cells, DOI `10.3390/cells11182775`.

## Computational checks over the supplied data

The requested-target CSV contained a single row, `Stt3b`, so the final answer
must contain exactly one prediction in that order.

I read the focal training DEG counts to calibrate the response scale.  There
were 1,674 unique training targets.  This endpoint is sparse: 72.0% of targets
had zero DEGs, the median was 0, the 75th percentile was 1, the 90th percentile
was 2, the 95th percentile was 18, and the mean was much larger at 14.1 because
a small set of perturbations gave hundreds to thousands of DEGs.

I then intersected a manually curated STT3B-neighborhood list with the training
targets.  Most direct OST-complex genes were not present as training
perturbations.  The available focal counts for the relevant ER and glycan
stress neighborhood were:

| training perturbation | focal `n_degs` | why inspected |
| --- | ---: | --- |
| `Gfpt1` | 311 | supplies UDP-GlcNAc for hexosamine and ER/Golgi glycosylation |
| `Atp2a2` | 187 | ER/SR Ca2+ pump; ER calcium depletion is a positive UPR benchmark |
| `Dhdds` | 116 | committed dolichol-synthesis enzyme feeding lipid-linked oligosaccharide supply |
| `Sec63` | 11 | Sec61/BiP-associated ER translocation and chaperone-cycle factor |
| `Hspa5` | 5 | BiP/GRP78, the core luminal ER Hsp70 chaperone |
| `Manf` | 3 | ER stress-responsive secreted/ER protein, weak positive control |
| `Vcp` | 2 | ERAD/proteostasis ATPase but not a strong focal ER-UPR phenocopy |
| `Dpm1` | 0 | Dol-P-Man synthesis feeding glycan precursor assembly |
| `Edem3` | 0 | mannose trimming/glycoprotein ERAD branch |
| `Atf6` | 0 | canonical ER-transmembrane UPR transcriptional sensor |
| `Nfe2l1` | 0 | proteasome recovery factor linked to ER membrane proteostasis |
| `Nfe2l2` | 0 | oxidative-stress transcription factor, counterexample |
| `Sil1` | 0 | BiP nucleotide-exchange factor, counterexample |

For the same targets I queried the Parquet restricted to
`group_name = '151 TH Prkcd Grin2c Glut'` to inspect the expression patterns
behind these counts:

```sql
SELECT gene_target, names, scores, logfoldchanges, pvals_adj,
       n_pert_matched, n_ctrl_matched
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
QUALIFY row_number() OVER (
  PARTITION BY gene_target
  ORDER BY pvals_adj ASC NULLS LAST, abs(scores) DESC NULLS LAST
) <= 12;
```

The broad `Gfpt1`, `Atp2a2`, and `Dhdds` signatures all up-regulated canonical
ER/ISR genes in the focal class: `Hspa5`, `Herpud1`, `Asns`, `Ddit3`, `Chac1`,
`Shmt2`, and/or `Sdf2l1` were among their leading corrected hits.  `Gfpt1`
had 120 matched perturbed nuclei and 311 DEGs; `Dhdds` had 138 nuclei and 116
DEGs; `Atp2a2` had 98 nuclei and 187 DEGs.  In the internal corpus, the
`Gfpt1`, `Dhdds`, `Atp2a2`, `Hspa5`, and `Sec63` reports also converged on an
ER-proteostasis state centered on `Hspa5`, `Hsp90b1`, `Pdia4`, `Herpud1`,
`Sdf2l1`, `Ddit3`, `Chac1`, and amino-acid stress genes in the same focal cell
group.

The weaker positives were much smaller.  `Sec63` produced 11 focal DEGs from
72 matched perturbed nuclei, led by `Hspa5`, `Canx`, `Hyou1`, and `Chac1`,
consistent with a compact ER-chaperone/ISR response.  `Hspa5` produced only 5
focal DEGs from 47 perturbed nuclei, although those included the expected
`Hsp90b1`, `Pdia4`, and `Derl3` up-regulation.  These profiles show that the
assay can detect a small ER folding program, but they also show that a
recognizable luminal ER lesion need not generate tens or hundreds of FDR 0.05
genes.

The most relevant counterexamples were flat despite adequate focal sampling.
`Dpm1` had 129 matched perturbed nuclei and zero DEGs; its leading UPR-like
genes, `Pdia6`, `Hspa5`, and `Pdia3`, were only nominal/subthreshold
(`Hspa5` adjusted p = 0.523).  `Edem3` had 120 nuclei and zero DEGs; the
leading canonical transcript was `Xbp1`, also subthreshold
(adjusted p = 0.239).  `Atf6` had 177 nuclei and all adjusted p values equal to
1.0.  The internal `Edem3`, `Sec63`, and `Hspa5` Findings explicitly made the
same distinction: the HSPA5/SEC63 branch is inducible in the Perturb-seq
experiment, but basal loss of single ERAD or UPR-adjacent genes can be buffered
below the whole-transcriptome FDR gate in postmitotic juvenile neurons.

## Target-specific reasoning

### `Stt3b`: predicted `0`

`STT3B` is the catalytic subunit of the OST-B oligosaccharyltransferase
complex.  The intervention is expected to impair the posttranslocational
branch of N-linked glycosylation: loss of `Stt3b` should reduce glycan
occupancy at acceptor sites skipped by cotranslational STT3A/OST-A, with a
special role for sites near C termini, sites in short loops, and some
cysteine-proximal acceptors.  Kelleher et al. 2003 established that mammalian
OSTs contain distinct STT3 paralogs; Ruiz-Canada et al. 2009 and Shrimal et al.
2014 placed STT3A as the main cotranslational translocon-associated enzyme and
STT3B as the posttranslocational enzyme that edits sites STT3A missed; and
Cherepanova et al. 2019 showed that STT3A and STT3B have overlapping but
non-identical site classes by quantitative glycoproteomics.  The human genetics
are real but relatively substrate-limited: Shrimal et al. 2013 found that
STT3A-CDG and STT3B-CDG fibroblasts both impaired isoform-specific GFP
glycosylation, while the STT3B mutation only slightly affected transferrin
glycosylation.  Lu et al. 2018 further showed that OST-B has a distinctive
lipid-linked-oligosaccharide hydrolysis activity suppressed by OST-A, again
supporting a specialized rather than simply global role for STT3B.

The appropriate causal model is therefore:

`Stt3b` LoF -> reduced OST-B posttranslocational N-glycosylation of a subset of
ER client sites -> some underglycosylated proteins are handled by calnexin/BiP
quality-control and ERAD -> only if that client burden exceeds capacity do
surviving thalamic glutamatergic nuclei induce an HSPA5/ATF4/CHOP-like RNA
program -> the Wilcoxon DEG count is the FDR-thresholded size of that survivor
RNA program.

The training evidence favors a thresholded, often buffered endpoint at exactly
that propagation step.  `Gfpt1` and `Dhdds` are much stronger analogs for a
global glycan-supply bottleneck than for `Stt3b`: they restrict UDP-GlcNAc or
dolichol substrate supply upstream of all OST activity and produced 311 and
116 DEGs.  `Atp2a2` is a strong positive ER-stress control but perturbs ER
calcium, not N-glycan transfer, and gave 187 DEGs.  The closer single-gene ER
client-handling analogs were low or zero: `Sec63` gave only 11 DEGs, `Hspa5`
gave 5, `Dpm1` and `Edem3` gave 0, and basal `Atf6` loss gave 0.  `Dpm1` is a
particularly useful counterexample because it feeds dolichol-linked glycan
precursor synthesis yet did not reach FDR 0.05 in the focal cell group, while
the `Edem3` zero shows that a CDG-relevant glycoprotein quality-control lesion
can be transcriptionally quiet in this P16 sparse CRISPR assay.

I therefore do not transfer the 100-300 DEG breadth from `Gfpt1` or `Dhdds` to
`Stt3b`.  An acute partial `Stt3b` loss can plausibly create a small ER-client
defect, but STT3A should glycosylate most nascent sequons cotranslationally and
can leave the posttranslocational branch with too little burden to cross the
FDR 0.05 whole-transcriptome threshold.  The most likely endpoint is in the
0-5 DEG range; I used `0` as the point estimate because three represented
nearby negative controls (`Dpm1`, `Edem3`, `Atf6`) were below threshold despite
more focal perturbed nuclei than the small `Hspa5` and `Sec63` positives, and
because `Stt3b` is biologically redundant with an OST-A pathway that was not
perturbed in the requested experiment.

## Limits of the reasoning

The prediction is extrapolative.  No `Stt3b`, `Stt3a`, `Ddost`, `Rpn1`, `Rpn2`,
`Magt1`, or `Tusc3` training perturbation was available for a direct
within-complex comparison, and the supplied Parquet does not measure glycan
occupancy, lipid-linked oligosaccharides, indels, or edited-cell abundance.
The Parquet and internal Findings corpus are different views of the same
Perturb-seq experiment, so their agreement is useful curation but not
replication.  External STT3A/STT3B studies were mostly in human transformed
cell lines or fibroblasts and quantify glycoproteins rather than snRNA-seq
DEG counts in juvenile thalamic neurons.  Finally, the exact integer boundary
between zero and a few DEGs is power-sensitive; the biological call is that
`Stt3b` is a weak, likely threshold-missing ER glycosylation perturbation in
this assay, not that OST-B is unimportant.
