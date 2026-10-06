# Stt3b DEG-count prediction

## Question and scope

The requested held-out target file contains a single perturbation, `Stt3b`. I interpreted the endpoint as:

`n_degs = count(names where pvals_adj < 0.05)` in the `151 TH Prkcd Grin2c Glut` differential-expression surface, including the perturbed target transcript itself if it passed FDR.

`Stt3b` is completely absent from both supplied training inputs as a perturbation target, so I did not have a Stt3b expression signature or an observed Stt3b DEG count to transfer from. I used the non-held-out signatures only to calibrate the integer scale and to test whether ER/N-glycosylation perturbations in this exact focal population were broad, weak, or null.

## Sources used

Internal data and corpus:

- `training_de_all_cell_groups.parquet`, especially the 28,891,566 focal rows in `151 TH Prkcd Grin2c Glut` covering 1,674 training targets and 17,259 measured genes.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, the exact focal-cell DEG counts for those 1,674 non-held-out targets.
- Distributed Agents same-experiment semantic corpus `perturbai-july-260713-sourceguard-1773-v1`. The corpus had no target card for held-out `Stt3b` or for `Stt3a`, but it did have curated same-experiment claims and findings for the training comparators `Dpm1`, `Dhdds`, `Gfpt1`, and `Hspa5`.
- Distributed Agents dataset context `perturbai-atlas-v5` for the experimental interpretation guard that self-target RNA depletion is QC context rather than a reliable proxy for functional knockout strength.

External sources:

- KEGG Genes/Pathways through KEGG REST, accessed 2026-09-23, resolved mouse `Stt3b` as `mmu:68292`, "dolichyl-diphosphooligosaccharide--protein glycosyltransferase subunit STT3B", assigned to N-glycan biosynthesis and protein processing in the ER.
- Kelleher and Gilmore 2005, Glycobiology, DOI `10.1093/glycob/cwj066`, summarized eukaryotic OST composition and the catalytic role of STT3-family subunits.
- Shrimal, Ng, Losfeld, Gilmore and Freeze 2013, Human Molecular Genetics, DOI `10.1093/hmg/ddt312`, PMID `23842455`, showed that STT3A and STT3B mutations cause distinct congenital disorders of glycosylation and that the human STT3B case only mildly affected transferrin glycosylation.
- Shrimal, Cherepanova and Gilmore 2014, Seminars in Cell & Developmental Biology, DOI `10.1016/j.semcdb.2014.11.005`, PMID `25460543`, reviewed the division in which STT3A-OST acts co-translationally at the SEC61 translocon and STT3B-OST modifies sequons skipped by STT3A, including post-translocational sites.
- Cherepanova, Shrimal and Gilmore 2014, Journal of Cell Biology, DOI `10.1083/jcb.201404083`, PMID `25135935`, showed that MagT1 is an oxidoreductase subunit of STT3B-OST needed for a subset of STT3B-dependent cysteine-proximal acceptor sites.
- Lu, Fermaintt, Cherepanova, Gilmore, Yan and Lehrman 2018, PNAS, DOI `10.1073/pnas.1806034115`, PMID `30181269`, separated mammalian STT3A/STT3B OST functions and showed STT3B-OST can also hydrolyze lipid-linked oligosaccharides.
- Couto, Guardia, Couto, Labriola, Labanda and Caramelo 2024, FASEB Journal, DOI `10.1096/fj.202302267R`, PMID `38934375`, supported the model that STT3B provides a second chance for vacant sequons and that STT3B-dependent occupancy is strongly affected by acceptor stability.

## Computations over the supplied tables

I first read the held-out manifest and confirmed that `Stt3b` was the only requested row.

For the training DEG counts, I inspected the focal-count distribution to calibrate scale:

- 1,674 training targets.
- 1,205/1,674 had `n_degs = 0`.
- 363/1,674 had 1-9 DEGs.
- 63/1,674 had 10-99 DEGs.
- 43/1,674 had at least 100 DEGs.
- The median was 0 and the 95th percentile was only 18, while a few stress or core-regulatory perturbations produced hundreds to thousands of DEGs.

I then queried the parquet for `151 TH Prkcd Grin2c Glut` rows whose perturbation target was an ER, glycosylation, UPR, or ERAD candidate. The candidate list deliberately included OST/N-glycan names that turned out not to be training perturbations (`Stt3a`, `Ddost`, `Rpn1`, `Rpn2`, `Dad1`, `Ostc`, `Alg*`, `Mgat*`, `Ganab`, `Mogs`, `Rft1`, `Dolk`, `Dpm2`, `Dpm3`) so that absence from training would be explicit rather than silently ignored.

Represented training comparators and their observed focal counts were:

| target | focal `n_degs` | expression-pattern evidence in 151 |
|---|---:|---|
| `Gfpt1` | 311 | Strong ER/ISR response; `Herpud1`, `Asns`, `Ddit3`, `Hspa5`, `Chac1`, `Pdia6`, `Hyou1`, `Trib3`, `Xbp1`, `Manf`, `Sel1l`, `Dnajc3`, `Atf4`, `Derl3`, and `Pdia4` all trended up and most were FDR significant. |
| `Atp2a2` | 187 | Strong ER-calcium stress state; `Ddit3`, `Chac1`, `Xbp1`, `Herpud1`, `Hspa5`, `Asns`, `Slc7a5`, and `Trib3` were induced. |
| `Dhdds` | 116 | Dolichol-carrier stress; induced `Chac1`, `Hspa5`, `Manf`, `Slc7a5`, `Ddit3`, `Herpud1`, `Asns`, `Pdia6`, `Xbp1`, `Derl3`, and `Pdia4`. |
| `Sec63` | 11 | Partial ER chaperone response with significant `Hspa5`, `Canx`, `Hyou1`, and `Chac1`. |
| `Hspa5` | 5 | Small but coherent BiP/ERAD response; significant `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3`, with `Herpud1`, `Asns`, `Pdia6`, `Dnajc3`, and `Ddit3` just below FDR 0.05-0.15. |
| `Manf` | 3 | Very narrow ER-lumenal response: `Hspa5`, `Pdia6`, and `Manf` passed FDR. |
| `Vcp` | 2 | No Hspa5-like ER stress; only `Rasgef1b` and `Nsmf` passed FDR. |
| `Amfr`, `Bcap31`, `Ssr4` | 1 each | Each one-gene count was explained by the target transcript itself rather than a UPR module. |
| `Dpm1` | 0 | No gene passed FDR 0.05; `Pdia6` and `Ttyh3` were the nearest effects, both FDR 0.0866. |
| `Atf6`, `Edem3`, `Lman2l`, `Mttp`, `Pign`, `Sil1`, `Suco` | 0 each | No corrected downstream signature in the focal group. |

I also checked the target-transcript row for these comparators. Some near-null genes had significant self-depletion (`Amfr`, `Bcap31`, `Ssr4`), but many did not (`Dpm1`, `Atf6`, `Edem3`, `Lman2l`, `Pign`, `Sec63`, `Sil1`, `Suco`, `Vcp`). I therefore did not add a default "+1" for a possible Stt3b self hit.

The Distributed Agents corpus gave the same qualitative boundaries:

- `Dpm1` claims and findings state that the Dpm1 response in `151 TH Prkcd Grin2c Glut` was restricted to a tiny Pdia6/Ttyh3 edge, shared in direction with the stronger upstream dolichol enzyme `Dhdds`, and was not phenocopied by downstream O-mannosylation or GPI-anchor comparators such as `Pign`.
- `Gfpt1` findings describe a strong thresholded ER chaperone/ERAD plus ISR response, strongest in 151, with `Dhdds` and `Atp2a2` as top ER/glycosylation empirical neighbors.
- `Dhdds` findings place the dolichol-carrier perturbation in the same vulnerable-neuron ER stress manifold as `Gfpt1`, `Atp2a2`, `Hspa5`, and partial `Sec63`, while explicitly noting that `Dpm1` and `Atf6` did not phenocopy `Dhdds`.
- `Hspa5` findings establish that ER-chaperone/ERAD transcription is recoverable in this assay, but is not induced by every ER-associated or UPR-axis perturbation; `Atf6`, `Edem3`, `Sil1`, and `Vcp` are counterexamples.

## Target-specific reasoning for Stt3b

`Stt3b` encodes a catalytic subunit of the mammalian oligosaccharyltransferase complex. That makes it mechanistically adjacent to N-linked glycosylation, but the closest represented training perturbations are imperfect:

- There was no `Stt3a` perturbation and no direct perturbation of core OST complex subunits such as `Ddost`, `Rpn1`, `Rpn2`, `Dad1`, `Ostc`, or `Tmem258`.
- `Gfpt1` and `Dhdds` are upstream supply bottlenecks. They can restrict many glycan products or the dolichol carrier itself, and in the training data they produced broad Hspa5/Ddit3/Chac1 ER-stress states. A selective STT3B catalytic loss should not be assumed to be this strong, because STT3A can still glycosylate most co-translational sites.
- `Dpm1` sits in dolichol-dependent glycosylation and would be expected to affect N-glycan, O-mannose, and GPI precursor biology, yet it produced 0 DEGs at the focal FDR 0.05 threshold. Its weak `Pdia6` edge is the best lower-bound analog for a glycan-related perturbation that is sensed but stays mostly below correction.
- `Hspa5`, `Manf`, and `Sec63` show that direct ER client-handling perturbations can yield 3-11 DEGs, but these are not equivalent to losing the STT3B branch of OST. `Sec63` and BiP act directly at translocation/folding; STT3B mainly fills skipped glycosylation sites.
- `Atf6`, `Edem3`, `Amfr`, `Sil1`, `Vcp`, `Pign`, `Lman2l`, `Mttp`, and `Suco` are useful counterexamples: many ER or secretory-pathway genes were buffered or target-self-only in recovered juvenile neurons.

The external OST literature also pushes away from treating Stt3b as a global N-glycosylation block. STT3A-OST is the SEC61-associated, co-translational enzyme, while STT3B-OST modifies vacant, skipped, post-translocational, or cysteine-proximal acceptor sites. That role is important for a subset of clients and is clinically real in congenital disorders of glycosylation, but it is narrower than the precursor-supply perturbations that generated the 100-300 DEG UPR signatures in the training table.

Given the acute, sparse, postnatal neuronal CRISPR context and the average modest transcript depletion in this experiment, my zero/nonzero decision is that `Stt3b` is more likely to remain below the BH FDR 0.05 threshold than to pass even a small Hspa5/Sec63-like ER-stress signature. The closest count anchors are therefore `Dpm1 = 0`, `Atf6 = 0`, and the many other buffered ER-associated perturbations, with `Hspa5 = 5`, `Manf = 3`, and `Sec63 = 11` as a plausible but less likely upper edge if STT3B-dependent clients accumulate enough to trigger BiP/ERAD transcription.

I predict:

- `Stt3b`: 0 DEGs.

## Limits and extrapolation

- The most important missing evidence is direct: no `Stt3b`, `Stt3a`, or same-OST-subunit training signature was available.
- The comparison from `Dpm1`, `Dhdds`, and `Gfpt1` to `Stt3b` crosses from precursor synthesis to the OST enzyme, so it calibrates ER-glycan stress rather than phenocopying STT3B.
- A complete biallelic STT3B knockout in every neuron could create a stronger glycosylation phenotype than this P16 mosaic AAV-CRISPR experiment; the endpoint samples surviving NeuN+ nuclei 3-4 weeks later.
- The prediction is for a BH-adjusted Wilcoxon count. A subthreshold rise in `Pdia6`, `Hspa5`, or another ER marker, or a glycoprotein-level defect without robust nuclear RNA changes, would still be biologically plausible with a predicted `n_degs` of 0.
- Self-target RNA depletion is hard to forecast from gene function. Some near-null training targets were counted only because their own mRNA passed FDR, but many equally relevant targets did not; I therefore treated a Stt3b target-only count as possible but not likely enough to make the point prediction nonzero.
