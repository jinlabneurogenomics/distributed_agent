# Biological adjudication trace

## Browser review

- I ran `nominate` first to expose the neutral 205-candidate union.
- I then ran `inspect` for all 205 candidates, exceeding the requirement to inspect every selected candidate and at least 25 rejected near-cutoff alternatives.
- I cached seed neighborhoods for all 50 visible odd-ranked seeds and compared the main proteasome, V-ATPase, RNA-processing, and membrane-traffic borderline groups.

## Seed modules inferred

- The highest-confidence depletion seeds mark a broad protein-homeostasis and trafficking program: V-ATPase acidification from Atp6v1b2/Atp6v1a, 26S proteasome and proteasome assembly from Psmb4/Pomp, ER-Golgi export from Gbf1/Sec31a/Stx5a, and ESCRT/endolysosomal traffic from Chmp4b/Snf8.
- A second high-confidence block is nuclear RNA handling: Son, Ddx23, Tnpo3, Thoc1, and Cdk13 link spliceosome, TREX/export, SR-protein import, and nuclear-pore stress.
- Chromatin and transcription seeds include Taf1, Kansl1, Brd4, Polr3b, and Cnot1; I favored broad nonredundant transcriptional scaffolds over transcription factors whose dossier support was limited to lens, B cells, spinal cord, endothelium, or embryonic organogenesis.
- Lower-ranked visible anchors captured neuronal identity and signaling modules including Six3/Six6, Lrp6/Wnt, Kif1a transport, Bbs5/Nek1 cilia, Pten/mTOR, Mc3r/Gal/P2ry14 GPCRs, and synaptic vesicle biology. I downweighted these unless the candidate dossier gave a postmitotic thalamic or broadly essential neuronal reason for acute depletion.

## Functional transfer decisions

- Direct same-complex transfer was used for PSMC1/PSMC5 with Psmb4/Pomp, Atp6v0c/Atp6v1e1/Atp6ap1 with Atp6v1b2/Atp6v1a, PRPF6/SRRM2/SRSF1/DDX39B with Ddx23/Son/Thoc1/Tnpo3, BDP1 with Polr3b, SEC23A/SAR1B with Sec31a, and VPS37A with Chmp4b/Snf8.
- Heuristic-only candidates were retained only when the loss-of-function mechanism was broadly damaging without a graph edge: THOC2 as a TREX core subunit, TIMMDC1 as a complex-I assembly factor, SEC63 as an ER translocon factor, XPO1 as a broad nuclear export receptor, and a small set of chromatin/UFMylation factors.
- Graph multiplicity was not used as a score. WDR26, CAML, ATXN10, TSC1, and several ciliary candidates had many anchors, but the dossiers did not make them cleaner acute thalamic depletion predictions than lower-multiplicity direct complex members.
- Several candidates nominated by both sources were still rejected near the boundary: KIF2A was more developmental than dynein/KIF1A transport, and WAC was less direct than FACT, CBP/CREBBP, TRRAP, SETD2, or SIN3A.

## Important rejected alternatives

- Synaptic genes such as SNAP25, STXBP1, UNC13B, SYN1, NBEA, and TSPAN7 can strongly change neuronal function but were weaker for removing nuclei in a three-week mosaic assay.
- TSC1/TSC2/MTOR/RPTOR were downweighted because loss directions differ across the pathway and Pten was a late visible seed.
- BBSome, IFT, RPGR, TTLL5, RAB28, DNAL1, and other ciliary genes were downweighted when the dossier emphasized retina, sperm, motile cilia, or embryonic Hedgehog patterning rather than thalamic postmitotic neurons.
- CD79B, PAX5, IL4RA, SOX18, NOTCH4, PDGFRB, ANTXR2, and MTTP were rejected as immune, endothelial, pericyte, ECM, or liver/intestine-biased transfers despite graph nomination.

## Missing or weak evidence

- Missing candidate-named claims were treated as missing browser evidence rather than proof of no biology; IL4RA was the only inspected candidate with no complete FUNC claim.
- Many graph anchors lacked atomic REL records. I did not count an absent REL edge as negative evidence, but I required a stronger loss-of-function rationale when only a high-level graph anchor connected the candidate to visible seeds.
