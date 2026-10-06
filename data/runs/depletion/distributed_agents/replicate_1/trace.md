# Biological adjudication trace

## Seed modules inferred

I treated the visible odd-ranked seeds as functional anchors, not as hidden endpoint labels. The strongest transferable modules were: V-ATPase/endolysosomal acidification from Atp6v1b2 and Atp6v1a; 26S proteasome and ubiquitin proteostasis from Psmb4 and Pomp; early secretory and endosomal traffic from Cltc, Gbf1, Sec31a, Stx5a, Chmp4b, and Snf8; spliceosome, TREX mRNA export, and nuclear pore transport from Son, Ddx23, Tnpo3, and Thoc1; broad chromatin and transcriptional cofactors from Taf1, Kansl1, Brd4, Cnot1, Polr3b, and Cdk13; and a lower-confidence projection-neuron module from Pafah1b1, Kif1a, Tbcd, and synaptic vesicle seeds.

V-ATPase and proteasome candidates were ranked highest when the frozen dossiers named the same complex or a very close assembly factor: ATP6V0C and ATP6V1E1 for Atp6v1b2/Atp6v1a, ATP6AP1 as a membrane-sector accessory subunit, and PSMC1/PSMC5 as 19S AAA ATPases linked to Psmb4 and Pomp. Core RNA-processing genes followed because PRPF6, DDX39B, SRSF1, SRRM2, U2AF2, SNRNP70, RNPC3, and CDC40 are less redundant than most ciliary, receptor, or developmental-transcription-factor graph neighbors.

## Review process

The browser was run in nomination mode first to establish the 205-candidate pool. I then inspected all 205 candidates, so every selected candidate and every near-cutoff rejection has `inspected=yes` in the ledger. I also used module-focused searches, seed neighborhoods for Atp6v1b2, Psmb4, Ddx23, Gbf1, Sec31a, and Kif1a, and multi-gene comparisons for RNA-processing, COPI/COPII/ESCRT, chromatin, motor, ciliary, mTOR/Wnt, and mitochondrial alternatives.

The heuristic source was treated as a survivor-state transcriptomic-effect prior, not as a rank to preserve. That is why high heuristic genes such as Diaph2 and Hspa5 were not simply copied to the top: HSPA5 was retained but demoted as an ER-UPR target that can be stress induced, while DIAPH2 was rejected because the frozen claims supported Rho/formin cytoskeletal biology without a close visible seed or an obvious acute survival mechanism. The graph source was treated similarly. Multiplicity helped identify neighborhoods, but high-multiplicity Wdr26 and Atxn10 were rejected because their dossiers did not transfer cleanly to acute thalamic glutamatergic depletion.

## Functional transfer calls

Selected calls required more than same-pathway annotation. I favored direct subunits or assembly factors of nonredundant machines: ATP6V0C/ATP6V1E1/ATP6AP1 in V-ATPase, PSMC1/PSMC5 in the 26S proteasome, PRPF6/DDX39B/SRSF1/SRRM2/U2AF2/SNRNP70/CDC40 in spliceosome or export, COPA/SEC23A/SAR1B/NSF/VPS37A in membrane traffic, and CREBBP/SIN3A/KMT2C/SETD2/TRRAP/SUPT16 in chromatin or transcription. I kept Huwe1, Naa15, Naa20, Wac, Uba5, Ranbp2, Xpo1, Hspa8, Vcp, Stxbp1, Dync1h1, Kif5a, Kif2a, Nfe2l1, Tcf7l2, Washc4, Dmxl2, Atp2a2, Hnrnpu, and Timmdc1 as progressively weaker but still plausible acute loss-of-function risks.

Important rejected alternatives were close. ATG5, MANF, VAPB, VPS53, VPS54, COPG1, ERGIC1, Gfpt1, Atl3, Elp1, Rb1, Ubr1, Xpr1, Nipbl, Chd8, Tsc1/Tsc2, Ctnnb1, Bbs9, Ift88, Aifm1, Tmem126a, Snap25, Trak1, and Kif3b all had real biological arguments. They were kept below the top 50 because the supplied evidence pointed to slower autophagy, ER protection, cargo-specific retrograde traffic, paralog buffering, chronic or developmental dosage effects, retinal/ciliary specialization, or synaptic physiology that might not remove NeuN+ thalamic nuclei by P37-P44.

## Missing evidence treatment

A missing frozen function claim was not treated as evidence that the gene lacks known biology. For genes with sparse dossiers, the ledger records the available FUNC or REL IDs and states why the visible evidence was not strong enough for the cutoff. Anchors without atomic relation IDs were used only as graph-neighborhood priors; exact REL IDs were cited only when the browser supplied them for the candidate and visible seed. I did not attempt to infer the held-out endpoint from any evaluation record or impose the heuristic order as an incumbent ranking.
