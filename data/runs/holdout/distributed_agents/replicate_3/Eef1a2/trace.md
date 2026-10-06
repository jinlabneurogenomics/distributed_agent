# Reasoning trace

## Question and interpretation

The held-out manifest for this run contains one target, `Eef1a2`. I interpreted the requested output as a point prediction for the number of genes with `pvals_adj < 0.05` after `Eef1a2` CRISPR loss of function in `151 TH Prkcd Grin2c Glut` nuclei. The target's own transcript is part of the measured gene universe if it passes FDR, but no `Eef1a2` differential-expression row or training endpoint was present in the supplied training files.

Two ambiguities were resolved as follows:

- I used the held-out CSV order verbatim; there was only `Eef1a2`.
- I treated zero as "no BH-significant genes in the single-nucleus Wilcoxon endpoint", not as absence of biology. Many acute postnatal neuronal perturbations in the training set are biologically important but flat in this assay.

## Sources used

- Input DEG-count endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input per-gene DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, for same-experiment claims and findings around `Eef2`, `Eif4a2`, `Mtor`, `Tsc2`, and their comparators.
- Distributed Agents runtime `profile_neighbors`, run locally over the supplied parquet, for a 30-perturbation focal-cell comparison among translation, mRNA-control, mTOR, ISR/stress, UFMylation, and proteasome targets.
- NCBI PubMed via the BioEval literature tool for external `EEF1A2`/`Eef1a2` biology.

Key literature used:

- Newbery et al. 2007, JBC, DOI `10.1074/jbc.M703962200`, PMID `17640869`: the mouse `wasted` deletion abolishes `Eef1a2` and the post-weaning phenotype is due to `Eef1a2` loss.
- Griffiths et al. 2012, PLoS One, DOI `10.1371/journal.pone.0041917`, PMID `22848658`: old heterozygous `+/wst` mice tolerate presumed 50% `eEF1A2` reduction without neuromuscular or spinal-cord pathology.
- Davies et al. 2023, Molecular and Cellular Neuroscience, DOI `10.1016/j.mcn.2023.103879`, PMID `37429391`: in mouse, neuronal soma become enriched for eEF1A2 after development while eEF1A1 remains widespread in axons, supporting related but compartmentalized paralog buffering.
- Carvill et al. 2020, Human Mutation, DOI `10.1002/humu.24015`, PMID `32196822`: damaging human `EEF1A2` missense variants disrupt protein synthesis and integrated-stress-response functions and cause epileptic-dyskinetic encephalopathy.
- Mohamed and Klann 2023, PNAS, DOI `10.1073/pnas.2307704120`, PMID `37695913`: patient EEF1A2 missense alleles reduce de novo protein synthesis/elongation and alter actin bundling in neuronal models.

## Computational steps over the supplied data

I first loaded the focal training-count table and found it to be strongly zero-inflated: 1,674 training targets, median 0 DEGs, 75th percentile 1 DEG, 95th percentile 18 DEGs, and a long tail up to `Uba5` at 2,677 DEGs. That calibration matters because a small integer is already above the assay's most common outcome.

I then selected mechanistic analogs and counterexamples from the focal training counts:

| perturbation set | focal `n_degs` |
| --- | --- |
| core translation factors | `Eef2` 9; `Eif4a2` 2; `Eif4g1` 1; `Eif4h` 1; `Eif5a` 0; `Eif2ak4` 0 |
| mTOR/translation-control relatives | `Mtor` 2; `Rptor` 0; `Tsc2` 86 |
| FMRP/local-translation and mRNA-control relatives | `Fmr1` 0; `Fxr1` 0; `Cyfip1` 0; `Cyfip2` 1; `Upf3b` 1; `Gigyf2` 17; `Tnrc6a` 0 |
| broad stress/proteostasis positives used as counterexamples | `Opa1` 37; `Atp2a2` 187; `Gfpt1` 311; `Elp1` 645; `Elp2` 150; `Thap11` 478; `Uba5` 2677; `Psmb4` 742; `Psmc1` 430 |

The closest missing perturbations were absent from the training universe: `Eef1a1`, `Eef1b2`, `Eef1d`, `Eef1e1`, `Eef1g`, and cytosolic aminoacyl-tRNA synthetases such as `Wars1`, `Nars1`, `Iars1`, `Yars1`, `Gars1`, and `Mars1` were not in the focal training-count CSV. Therefore the direct within-dataset analogs are adjacent, not paralogous.

For the direct analogs I also filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and verified that each had a complete 17,259-gene profile in the focal group. Matched perturbed nuclei were in a typical range for this dataset: `Eef2` 87, `Eif4a2` 135, `Eif4g1` 143, `Eif4h` 178, `Eif5a` 189, `Mtor` 188, `Rptor` 235, `Tsc2` 177, `Fmr1` 178, and `Upf3b` 81, all against 23,679 matched controls. The small observed counts are thus not missing signatures.

Finally, I ran Distributed Agents `profile_neighbors` on a hand-declared 30-node universe of translation-control, mTOR, FMRP/local-translation, ISR/proteostasis, UFMylation, and proteasome perturbations in the focal group. The runtime compared full 17,259-gene `logfoldchanges` vectors and positive/negative signed tails using `pvals_adj` only to mark significant features. I used this to check whether the low-count translation perturbations were embedded in the broad `Tsc2`, UFMylation, proteasome, or ATF4-like stress surfaces. They were not: the same-experiment Distributed Agents claims explicitly state that the assayed translation-factor, cap-initiation, RNA-helicase, and mTOR-adjacent genes do not form a generic shared postmitotic neuronal nuclear-RNA response, that the `Eef2` response is not phenocopied by `Eif5a`, `Eif2ak4`, `Eif4a2`, `Eif4g1`, `Eif4h`, `Mtor`, or `Rptor`, and that `Tsc2` loss is a broader disinhibition/sterol/lysosome state rather than a reciprocal copy of simple elongation-factor loss.

## Target-specific reasoning

### `Eef1a2`

`Eef1a2` encodes the neuron- and muscle-enriched eEF1A isoform that delivers aminoacyl-tRNAs to the ribosome during elongation and also participates in actin/cytoskeletal biology. The external prior is therefore non-null: complete mouse `Eef1a2` loss produces the `wasted` post-weaning syndrome and human EEF1A2 missense variants produce epileptic and neurodevelopmental phenotypes.

That external prior does not imply a hundreds-of-genes response in this endpoint. The important modifiers are:

- The experiment is acute, sparse, AAV CRISPR LoF from P16 to P37-44, not a germline homozygous null. The average RNA downregulation of Perturb-seq targets in this screen is modest, and old heterozygous `+/wst` mice tolerate far larger bulk dosage reduction of eEF1A2.
- eEF1A2 has a close paralog. `Eef1a1` was not assayed here, but mouse neurons can still localize eEF1A1 to axons after the postnatal eEF1A1/eEF1A2 switch, so the eEF1A system has more built-in subcellular redundancy than `Eef2`.
- The same-experiment core translation controls are weak at the focal nuclear mRNA endpoint. `Eef2`, the best available elongation-factor analog, has only 9 focal DEGs; cap-initiation or elongation-adjacent genes have `Eif4a2` 2, `Eif4g1` 1, `Eif4h` 1, `Eif5a` 0, and `Eif2ak4` 0.
- The assay can detect broad protein-homeostasis stress when it is engaged. `Uba5`, `Psmb4`, `Psmc1`, `Elp1`, `Elp2`, `Thap11`, `Gfpt1`, and `Atp2a2` all give tens to thousands of focal DEGs. I used them as counterexamples: they show that a high count is possible, but their UFMylation/proteasome/ISR or ER-calcium biology is not a close model for partial loss of the basal eEF1A2 elongation factor.
- `Tsc2` at 86 DEGs is a useful upper bound from a translation/growth pathway but not a close analog. Its signature comes from loss of a negative mTORC1 regulator and induces sterol/lysosomal feedback; `Mtor` loss itself gives only 2 DEGs and `Rptor` gives 0.

The best within-dataset anchor is thus slightly below `Eef2=9`, not the 0-2 cap-initiation group and not `Tsc2=86`. I expect at least one DEG because the abundant `Eef1a2` transcript itself should be targetable in neuronal soma, and I expect a few secondary genes because the harvest falls after the normal postnatal dependence on eEF1A2. I do not expect a broad ISR/proteostasis state because the assayed translation-factor perturbations mostly failed to induce canonical stress genes in the Distributed Agents corpus analysis, and because eEF1A1/subcellular redundancy and survivor bias should dampen a partial acute lesion.

Point prediction: `6` DEGs.

## Limits and extrapolation

The major limitation is the missing paralog/complex neighborhood: no `Eef1a1` or eEF1B subunit perturbation was present in the training counts. The prediction is therefore transferred mostly from `Eef2` and weak eIF/mTOR controls rather than from a same-complex partner. The same-experiment corpus also had no direct `Eef1a2` claims because the target was held out.

The external evidence is imperfectly matched. Germline `wasted` mice remove `Eef1a2` in muscle and motor neurons throughout development; human `EEF1A2` disease is dominated by missense alleles that can behave through haploinsufficiency, gain of function, or dominant-negative mechanisms; and neither maps cleanly onto sparse postnatal Cas9 editing in thalamic glutamatergic neurons. Conversely, severe `Eef1a2` edits might deplete vulnerable nuclei before single-nucleus capture, which would lower `n_degs` among the survivors without proving no biological effect.

Overall, this is a low-confidence but deliberately small nonzero call: close to a weak focal translation-factor response, below `Eef2`, and far below the broad mTOR-disinhibition, UFMylation, proteasome, or ISR-like perturbations.
