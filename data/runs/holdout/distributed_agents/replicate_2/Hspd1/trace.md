# Prediction trace for `Hspd1`

## Question and setup

The requested held-out perturbation list contains one target, `Hspd1`. I interpreted the endpoint as the exact focal-cell readout in the prompt: the number of measured genes in `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` for an acute AAV CRISPR loss-of-function perturbation. `Hspd1` was held out completely, so no `Hspd1` perturbation signature or count is available in the parquet or training-count CSV. I therefore used observed training perturbations only as analogs or counterexamples.

One ambiguity is that HSPD1 is an essential mitochondrial chaperonin in many settings, but this screen is a sparse, postnatal, 3-4 week neuronal perturbation with modest average on-target RNA reduction. I did not treat weak self-mRNA depletion in analog genes as proof of editing failure, but the assay-calibrated FDR endpoint is still sparse enough that a partial buffered hit can reasonably score as zero.

## Sources used

- Training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Per-gene differential expression: `[local file: training_de_all_cell_groups.parquet]`.
- Requested targets: `[local file: 110_Hspd1.csv]`.
- Same-experiment internal evidence: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, queried for HSPD1 and for chaperone / mitochondrial proteostasis claims; Distributed Agents runtime profile comparison over selected focal-cell signatures.
- External functional knowledge: MitoCarta3.0 (Rath et al. 2021, DOI `10.1093/nar/gkaa1011`); HSP60/HSP10 mitochondrial chaperonin biochemistry and client inventory (Bie et al. 2020, DOI `10.1007/s12192-020-01080-6`; Gomez-Llorente et al. 2020, DOI `10.1038/s41467-020-15698-8`); mtHsp70/Hsp10 participation in Hsp60 complex assembly (Bottinger et al. 2015, DOI `10.1074/jbc.M115.642017`); HSPD1 neurologic disease genetics (Magen et al. 2008, DOI `10.1016/j.ajhg.2008.05.016`; Bross and Fernandez-Guerra 2016, DOI `10.3389/fmolb.2016.00049`; Comert et al. 2020, DOI `10.1101/mcs.a004879`).

## Computational checks

- The requested-target CSV had exactly one target, `Hspd1`.
- The focal training table had 1,674 non-held-out perturbations; its count distribution was very sparse: median `0`, 75th percentile `1`, 90th percentile `2`, 95th percentile `18`, and only a long right tail of strong perturbations such as `Uba5`, `Tpr`, and `Sin3a`.
- I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and to a hand-picked set of biologically relevant chaperone and mitochondrial targets, then retrieved all rows with `pvals_adj < 0.05`. This reproduced the focal counts and exposed which genes made up the few nonzero signatures.
- I also ran a Distributed Agents runtime `profile_compare` on `Hspa5`, `Hspa8`, `Hsp90ab1`, `Clpp`, `Clpx`, `Lonp1`, `Afg3l2`, `Yme1l1`, `Agk`, `Opa1`, `Aco2`, `Uqcrq`, and `Dnajc19`, using `logfoldchanges` as the signed profile and `pvals_adj < 0.05` as the significant-feature rule. In that 13-target analog cohort, eight targets had no significant focal-cell genes, four had 1-9, and only `Opa1` had 10-49.

## Within-dataset analogs and counterexamples

| Training target | `n_degs` in `151 TH Prkcd Grin2c Glut` | Focal expression-pattern evidence | Relevance to `Hspd1` |
|---|---:|---|---|
| `Clpp` | 0 | No FDR-significant genes in the focal group. | Mitochondrial matrix ClpXP protease branch; not a chaperonin, but a close matrix proteostasis analog. Its complete focal silence argues that disrupting matrix protein quality control often stays below this DEG endpoint. |
| `Clpx` | 0 | No FDR-significant genes in the focal group. | Same ClpXP pathway as `Clpp`; the same-experiment corpus reports that ClpXP and LONP1 branches were not transcriptomically interchangeable in postmitotic neurons. |
| `Lonp1` | 0 | No FDR-significant genes in the focal group, despite corpus evidence that `Lonp1` can make a small `Ddit3` / `Herpud1` ISR-like response in other neuronal groups. | The most relevant independent mitochondrial matrix protease counterexample; if a strong generic matrix proteotoxic-stress response were inevitable, `Lonp1` should have been less flat here. |
| `Afg3l2` | 0 | No FDR-significant focal genes. | Inner-membrane AAA protease; more distant topologically but still mitochondrial proteostasis. Its flatness, together with `Yme1l1`, marks mitochondrial protease effects as branch-specific. |
| `Yme1l1` | 0 | No FDR-significant focal genes. | Another mitochondrial AAA protease, flat in the focal group. |
| `Dnajc19` | 0 | No FDR-significant focal genes. | Mitochondrial inner-membrane/PAM-associated J protein near protein import and the mtHsp70 system. It is not an HSP60 cofactor but is closer to mitochondrial chaperone biology than generic cytosolic Hsp40 genes. |
| `Agk` | 0 | No FDR-significant focal genes. | A mitochondrial TIM22/lipid comparator used mainly as a same-organelle boundary; Distributed Agents corpus evidence says it did not share LONP1-like stress behavior. |
| `Aco2` | 0 | No FDR-significant focal genes. | Matrix TCA enzyme and MitoCarta matrix protein, included as a mitochondrial matrix counterexample; not a protein-folding analog. |
| `Uqcrq` | 1 | One significant gene, `Gpr180` down, not an ISR or chaperone marker. | Respiratory-chain comparator; shows an OXPHOS-adjacent perturbation can be essentially flat in this focal endpoint. |
| `Opa1` | 37 | A clear ISR-like amino-acid stress signature: `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2`, `Slc7a5`, and `Herpud1` were among the up-regulated FDR genes. | Important positive mitochondrial counterexample. I did not project its count onto `Hspd1` because OPA1 directly controls inner-membrane fusion/cristae morphology rather than HSP60/HSP10 matrix folding, and corpus claims specifically warned that OPA1-like stress is not a generic consequence of mitochondrial perturbation. |
| `Hspa5` | 5 | Up-regulated ER quality-control genes `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3`; one down-regulated gene, `Erc1`. | Chaperone perturbation with a detectable but tiny compartment-specific response. It demonstrates that the Wilcoxon pipeline could recover adaptive chaperone transcription, but it is an ER BiP response rather than a matrix chaperonin response. |
| `Hspa8` | 9 | Up-regulated `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1`, and `Cct6a`; several down-regulated genes including `Fras1`, `Unc79`, `Leng8`, and `Apba2`. | Abundant cytosolic Hsp70/Hsc70; useful as a single-chaperone calibration. The response was still single-digit and the same-experiment corpus says it did not phenocopy ER or HSP90 perturbations. |
| `Hsp90ab1` | 1 | Only `Hsp90ab1` itself was FDR-significant. | A canonical cytosolic Hsp90 chaperone counterexample for the idea that every core chaperone perturbation induces a broad heat-shock state. |
| `Hsf1` | 6 | Down-regulated heat-shock targets such as `Hsph1`, `Hsp90aa1`, `Hsp90ab1`, and `Ahsa2`. | Positive control that HSF1-dependent chaperone transcripts are assay-detectable but remain low-count here. |

The Distributed Agents same-experiment corpus had no direct `Hspd1` target context, consistent with the holdout. Its relevant curated claims were instead comparative: represented heat-shock, Hsp70, Hsp90, ER, and Hsp40 perturbations did not collapse into one heat-shock / UPR program; single distal chaperone and DNAJ perturbations were generally buffered in basal juvenile neurons while core proteasome subunits were broad; and represented mitochondrial matrix, ClpXP, LONP1, and inner-membrane protease perturbations were non-interchangeable and mostly sparse. Those claims made superficial same-organelle or same-family pooling unsafe, but they also made a broad HSPD1 response less likely than a flat one.

## Target-specific rationale

`Hspd1` encodes mitochondrial HSP60, the large subunit of the HSP60/HSP10 chaperonin that folds imported mitochondrial matrix proteins. MitoCarta3.0 places HSPD1 in the mitochondrial matrix protein-folding pathway, and biochemical work shows a large client set in the matrix plus tight functional coupling to HSP10/HSPE1 and upstream mtHsp70-assisted HSP60 ring assembly.

That biology makes `Hspd1` more central than `Clpp`, `Clpx`, or `Lonp1`, and germline or strong HSPD1 mutations can cause severe neurologic disease. I therefore considered a nonzero OPA1-like or ER-UPR-like stress signature. The within-screen evidence argued against making that leap: direct HSPE1 and HSPA9 perturbations were absent from the training count table; all available matrix proteostasis branches in the focal group were zero; the available mitochondrial import/co-chaperone comparator `Dnajc19` was zero; and the broader single-chaperone comparators topped out at 9 DEGs. The one stronger mitochondrial counterexample, `Opa1 = 37`, carried an amino-acid/ATF4-like inner-membrane stress signature that is not shared by `Aco2`, `Agk`, `Clpp`, `Clpx`, `Lonp1`, or `Yme1l1` in the Distributed Agents corpus.

I therefore predicted that a partial acute `Hspd1` perturbation would most likely be buffered below the focal Wilcoxon FDR threshold, perhaps changing mitochondrial proteostasis at the protein or organelle level without producing a reproducible nuclear RNA module. The point prediction is:

| target | predicted `n_degs` |
|---|---:|
| `Hspd1` | 0 |

## Limits

- There is no direct same-complex training perturbation for `Hspe1` and no mtHsp70 `Hspa9` perturbation, so this prediction extrapolates from adjacent matrix protease and mitochondrial-import targets rather than from the HSP60/HSP10 machine itself.
- `Hspd1` is essential and could be more disruptive than the observed flat matrix-proteostasis comparators if editing efficiency, protein turnover, or client dependence is high in this cell group.
- The few analog signatures with 0 DEGs do not prove no biology; they only show no genes passed BH-adjusted Wilcoxon `p < 0.05` in this assay.
- OPA1 shows that mitochondrial perturbations can trigger an ISR-like 37-gene focal response, so the zero call rests on branch specificity, not on a claim that all mitochondrial perturbations are silent.
