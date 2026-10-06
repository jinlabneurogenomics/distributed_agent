# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

I interpreted the requested endpoint as a point prediction of the number of measured mouse genes with `pvals_adj < 0.05` in the held-out `Pten` perturbation, restricted to the `151 TH Prkcd Grin2c Glut` neuronal group. The effect direction in the parquet is perturbed versus matched non-targeting control, so positive log fold changes are higher in the knockout. `Pten` was absent from both supplied training inputs, so I treated all exact `Pten` differential-expression values as unobserved and transferred from non-held-out pathway neighbors.

I did not use target-transcript knockdown as a guide-efficiency weight. In this sparse P16 AAV-Cas9 screen, target RNA loss is useful QC context but is not a calibrated measure of functional editing.

## Sources used

- Supplied focal endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied per-gene DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Held-out manifest: `[local file: 190_Pten.csv]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, for curated findings over the Perturb-seq dataset. `Pten` itself had no corpus record because it was held out, but training targets in its PI3K/AKT/mTOR neighborhood did.
- NCBI PubMed, through the independent literature search tool, for external PTEN, TSC, GATOR1, and mTORC1 mechanisms.

## Computations over the supplied data

1. Read the held-out CSV and confirmed that the only requested target was `Pten`.
2. Summarized the focal training-count CSV. The endpoint is zero-heavy: 1,205 of 1,674 training perturbations have `n_degs = 0`; the median is 0, the 75th percentile is 1, the 95th percentile is 18, and the maximum is 2,677.
3. Queried the parquet for every measured gene in `151 TH Prkcd Grin2c Glut` for PI3K/mTOR candidates present in training. Each available target had 17,259 measured genes in the focal group and 23,679 matched control nuclei.
4. For selected mechanistic candidates I counted `pvals_adj < 0.05` directly in the parquet, extracted the significant genes, and self-joined same-feature rows across targets to count same-direction and opposite-direction FDR-supported overlaps. This let me separate genuine sterol-module overlap from broad pathway membership.
5. Ran a Distributed Agents runtime profile comparison over the 18 focal candidate signatures `Akt3`, `Depdc5`, `Igf1r`, `Insr`, `Irs1`, `Mib1`, `Mtor`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Prkaa2`, `Prkag2`, `Rab7`, `Rptor`, `Srebf1`, `Srebf2`, `Strada`, and `Tsc2`. Twelve of these 18 were completely FDR-flat in the focal group. Because whole-profile correlations across mostly nonsignificant genes shared a large background, I used FDR-supported overlap and the corpus restricted-signature findings for target-specific interpretation.

## Training perturbations most relevant to PTEN

Observed `151 TH Prkcd Grin2c Glut` DEG counts for the nearest pathway candidates:

| training target | `n_degs` | expression evidence and interpretation |
| --- | ---: | --- |
| `Tsc2` | 86 | Loss of the TSC1/TSC2 Rheb GAP is the closest assayed example of losing a growth-factor-side mTORC1 brake downstream of PI3K/AKT. Its 86 focal hits included sterol and lysosomal/endolysosomal genes such as `Cyp51`, `Pik3r3`, `Ptgds`, `Dusp1`, `Nsdhl`, and `Tubb3`; Distributed Agents `Tsc2:F002/F007` curated this as a detectable mTORC1/SREBP/lysosomal program with partial same-direction overlap to `Depdc5` and opposite sterol-branch evidence from `Srebf2`. |
| `Depdc5` | 13 | `Depdc5` is the GATOR1 Rag-family amino-acid-side mTORC1 brake. Its focal signature overlapped `Tsc2` in the same direction on 8 FDR-significant genes, including the sterol/PI3K arm (`Ldlr`, `Pik3r3`, `Insig1`, `Hmgcs1`, `Msmo1`) and shared all five FDR-supported overlaps with `Rab7` in the same direction. It is an appropriate analog for derepressing mTORC1, but it was much narrower than `Tsc2`, so it bounds the PTEN estimate downward. |
| `Srebf2` | 7 | `Srebf2` loss reversed the sterol arm: all three shared `Depdc5` FDR genes and both shared `Tsc2` FDR genes moved in the opposite direction, and its significant genes included down-regulation of `Srebf2`, `Dhcr24`, `Insig1`, `Hmgcs1`, `Msmo1`, `Cyp51`, and `Sqle`. This is a branch-selective counterexample validating that the `Tsc2`/`Depdc5` sterol response has the expected SREBP2 sign. |
| `Mtor` | 2 | Direct mTOR kinase loss had only two focal hits (`Rims3`, `Tmed8`) and no FDR-overlap with `Tsc2`, `Depdc5`, or `Srebf2`. This is an expected sign/direction boundary: removing the kinase should not phenocopy removing PTEN or TSC2, which increase signaling through mTORC1. |
| `Rptor` | 0 | Raptor is the defining mTORC1 scaffold, but its acute single-gene loss was flat. Together with the `Mtor` result, it shows that loss of positive core mTORC1 components did not produce the reciprocal SREBP/lysosome program. |
| `Akt3`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Igf1r`, `Insr`, `Irs1` | 0 each | These receptor-proximal and PI3K/AKT positive nodes were transcriptionally buffered. Distributed Agents `Akt3:F003`, `Pik3r1:F004`, and claim `claim:b7b2ba203c83fdb0ed2d` specifically summarize that the assayed upstream insulin/IGF/class-IA PI3K/AKT nodes were flat or nonconvergent in basal sparse postnatal neurons. They are counterexamples to a naive "any PI3K/AKT gene gives a response" rule, but they are not sign-matched PTEN analogs because PTEN loss increases PIP3/AKT rather than reducing a positive input. |
| `Strada`, `Prkaa2`, `Prkag2` | 0 each | LKB1/AMPK-adjacent loss did not converge with `Tsc2`; these are additional examples that pathway adjacency alone was not enough to create a broad focal transcriptomic signature. |
| `Rab7` | 501 and `Mib1` | 27 | These were data-driven sterol/endolysosomal positives rather than direct PTEN analogs. `Rab7` shared 38 significant genes with `Tsc2` and 5 with `Depdc5`, nearly all same direction; `Mib1` shared a smaller sterol/cholesterol arm. Their much broader biology made them useful evidence that the sterol module was assay-detectable but not good quantitative templates for `Pten`. |

The Distributed Agents same-experiment corpus supported the same boundaries: `Tsc2:F007` states that `Srebf2` opposed the `Tsc2` sterol branch and `Depdc5` partially matched it, while `Mtor`, `Rptor`, `Igf1r`, `Irs1`, and `Akt3` did not give robust matched FDR overlap; `Depdc5:F005` independently says `Mtor`, `Rptor`, `Strada`, `Pik3r1`, and `Pik3cb` did not phenocopy `Depdc5` in the focal thalamic group.

## External biological rationale

PTEN is not a paralog of any training target; the reason to compare it with `Tsc2` and `Depdc5` is pathway sign. PTEN dephosphorylates phosphoinositide products of PI3K and suppresses AKT signaling, a lipid-phosphatase mechanism established by Myers et al. 1998, PMID 9811831, DOI 10.1073/pnas.95.23.13513. AKT phosphorylates and inhibits TSC2, linking PTEN loss to relief of the TSC1/TSC2 brake on mTORC1; the TSC2 phosphorylation link was shown by Manning et al. 2002, PMID 12150915, DOI 10.1016/s1097-2765(02)00568-3. DEPDC5/GATOR1 loss is analogous only at the level of "loss of an mTORC1 GAP": Bar-Peled et al. 2013 identified GATOR1, including DEPDC5, as a GAP for RagA/RagB that restrains amino-acid signaling to mTORC1, PMID 23723238, DOI 10.1126/science.1232044. The central role of mTORC1 in growth and metabolic outputs including lipid biogenesis is reviewed in Laplante and Sabatini 2012, PMID 22500797, DOI 10.1016/j.cell.2012.03.017.

Mouse neuronal PTEN loss has a strong prior for a postmitotic growth phenotype. Pten-deficient postnatal granule neurons show mTOR-dependent soma hypertrophy that is prevented or reversed by the mTOR inhibitor CCI-779 in Kwon et al. 2003, PMID 14534328, DOI 10.1073/pnas.2132711100. Deletion of `Pten` in differentiated cortical and hippocampal neurons activates the Akt/mTor/S6k pathway and causes macrocephaly, neuronal hypertrophy, ectopic dendrites/axons, increased synapses, and behavioral abnormalities in Kwon et al. 2006, PMID 16675393, DOI 10.1016/j.neuron.2006.03.023. More recent dentate granule neuron genetics showed that disrupting `Rptor`/mTORC1 can block Pten-loss neuronal hypertrophy and rescue excess excitatory synaptic transmission, while other dendritic-overgrowth components can involve microtubule polymerization in parallel to acute mTORC1 inhibition (Tariq et al. 2022, PMID 36323257, DOI 10.1016/j.celrep.2022.111574; Getz et al. 2022, PMID 35101965, DOI 10.1523/JNEUROSCI.1835-21.2022).

## Target-specific prediction

### `Pten`

I predict a detectable but not extreme response in `151 TH Prkcd Grin2c Glut`: **47 DEGs**.

The zero/nonzero call is driven mainly by external target-function knowledge plus within-dataset detection of downstream mTOR-brake loss. PTEN removal has the same qualitative sign as `Tsc2` or `Depdc5` loss with respect to mTORC1 activation, and the assay plainly detects the SREBP/lysosome branch when a negative mTORC1 regulator is perturbed. That makes a hard zero unlikely.

The magnitude is driven by the training dataset. Copying the 0-DEG counts of `Akt3`, `Pik3cb`, `Pik3r1`, `Pik3r2`, `Igf1r`, `Insr`, or `Irs1` would be the wrong sign, because those perturbations remove positive receptor/PI3K/AKT inputs rather than removing a PIP3 brake. Copying all of `Tsc2` at 86 also seems too high: `Pten` is upstream of the TSC/Rheb switch, will depend on basal PI3K input in this thalamic state, and the training data show that even the sign-matched `Depdc5` brake reaches only 13 DEGs while sharing only a subset of the `Tsc2` sterol program. I therefore placed `Pten` between `Depdc5` and `Tsc2`, closer to `Tsc2` than to flat upstream nodes because PTEN loss in neurons is a well-established AKT/mTORC1-activating overgrowth perturbation.

## Limits

The central limitation is that no `Pten`, `Tsc1`, `Tbc1d7`, or `Rheb` perturbation was available in the supplied training set, so the closest biochemical complex around the TSC/Rheb switch is only partially observed. The focal parquet gives RNA, not pAKT, pS6, protein synthesis, soma size, dendritic arbors, or survival; PTEN's strongest neuronal effects in the literature are morphological and can run through mTORC1-dependent and mTORC1-independent branches. The P16 sparse AAV-CRISPR design is also milder and later than many Cre-lox PTEN models, so the prediction is an extrapolation from pathway sign, not a direct phenocopy.

The DEG count itself is power-dependent and thresholded. A prediction of 47 should be read as "clearly nonzero and below the assayed `Tsc2` response", not as a claim that exactly 47 genes will define PTEN biology.
