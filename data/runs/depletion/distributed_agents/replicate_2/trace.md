# Biological adjudication trace

## Review process

I ran `nominate` first and treated its 205 rows as the closed review pool. I used the nomination table to assign candidates to seed neighborhoods, then inspected every selected gene and 51 additional rejected candidates near the cutoff or in confusable modules. The main boundary cases I inspected included COPI/COPII and ER candidates just outside the answer (`Caml`, `Copg1`, `Dmxl2`, `Ergic1`, `Sar1b`, `Vps53`, `Vps54`), ciliary/BBSome alternatives (`Bbip1`, `Bbs9`, `Ift88`, `Kif3b`), autophagy and mTOR alternatives (`Atg5`, `Rb1cc1`, `Tsc1`, `Tsc2`), synaptic or axonal transport alternatives (`Kif5a`, `Nbea`, `Snap25`, `Stxbp1`, `Trak1`), and the low-ranked heuristic-only tail (`Atl3`, `Cspp1`, `Nfx1`, `Nipbl`, `Npy1r`, `Ppp3r1`, `Sacs`, `Slf2`, `Unc13b`, `Usp9x`, `Washc4`, `Zfp160`, `Zfp182`).

## Inferred seed modules

* **Proteasome and proteostasis:** visible `Psmb4`, `Pomp`, and `Trip12` supported direct selection of `Psmc1` and `Psmc5`; `Vcp`, `Hspa8`, `Huwe1`, `Uba5`, and `Ubr1` were kept for ubiquitin or chaperone coupling. I rejected `Nfe2l1` because it is a compensatory proteasome-recovery transcription factor rather than a proteasome particle subunit, and `Wdr26`/`Herc1` because their E3 biology was substrate-specific.
* **V-ATPase and endolysosome:** visible ranks 1 and 15 made `Atp6v0c`, `Atp6v1e1`, and graph-only `Atp6ap1` strong transfers. `Dmxl2`, `Clcn5`, and `Slc4a7` were plausible but indirect accessory or ion-homeostasis calls.
* **ER, COPI/COPII, glycosylation, and vesicle traffic:** visible `Gbf1`, `Sec31a`, and `Stx5a` pointed to `Copa`, `Sec23a`, `Nsf`, `Sec63`, `Gfpt1`, `Atp2a2`, and `Dhdds`. `Caml`, `Copg1`, `Ergic1`, `Sar1b`, and `Vps53` were close but had weaker heuristic support, paralog buffering, or more cargo-specific disease.
* **Splicing, nuclear speckles, TREX, and nuclear pores:** visible `Son`, `Ddx23`, `Tnpo3`, and `Thoc1` supported a dense RNA-processing tier: `Prpf6`, `Thoc2`, `Ddx39b`, `Srsf1`, `Tpr`, `Ranbp2`, `Rnpc3`, `Srrm2`, `U2af2`, `Cdc40`, and `Snrnp70`.
* **Chromatin and transcriptional co-regulation:** visible `Taf1`, `Kansl1`, `Polr3b`, `Brd4`, and `Cdk13` supported `Crebbp`, `Supt16`, `Sin3a`, `Kmt2c`, `Setd2`, `Trrap`, `Bdp1`, and `Wac`. I accepted `Rb1` only near the bottom because neuronal cell-cycle re-entry after loss is plausible but not a direct fit to most visible seeds.
* **Mitochondrial metabolism:** visible `Hspa9` supported `Timmdc1`; `Aifm1`, `Tmem126a`, and `Dld` were left out because the evidence suggested slower, more selective mitochondrial disease.
* **Cytoskeleton, motors, and synapses:** visible `Pafah1b1`, `Kif1a`, and `Tbcd` supported lower-confidence selection of `Dync1h1` and `Kif2a`. I rejected most synaptic-vesicle and adhesion genes because synaptic silencing does not necessarily remove sparsely perturbed cells from the recovered nuclear pool.
* **Developmental Wnt, SIX/SOX, cilia, GPCR, and immune modules:** these provided many graph candidates but few selected genes. `Tcf7l2` was kept for specific postmitotic thalamic transcriptional evidence, while most `Six*`, `Sox*`, `BBSome`, `IFT`, GPCR, vascular, and immune genes were rejected as developmental, modulatory, redundant, or off-cell-type.

## Source treatment

I did not copy either nomination source into the answer. Heuristic-only genes were promoted only when their frozen dossiers or general function made a direct acute loss-of-function effect plausible: examples are `Thoc2`, `Timmdc1`, `Setd2`, `Xpo1`, and `Xpr1`. Conversely, `Zfp160`, `Zfp182`, `Npy1r`, `Ppp3r1`, `Slf2`, and `Unc13b` were rejected despite heuristic support because the mechanistic evidence looked too generic, modulatory, replication-biased, or synaptic for P16-P37 depletion.

For graph-only candidates, I treated graph multiplicity as a prompt for module inspection, not as a score. This is why low-multiplicity `Atp6ap1`, `Bdp1`, `Cdc40`, `Dync1h1`, `Nsf`, and `Sec23a` could enter the selected set, while high-multiplicity `Atxn10`, `Caml`, and `Wdr26` were rejected. Atomic same-complex relationships were weighted most strongly when loss direction and timing transferred: V-ATPase, proteasome, COPII, Pol III, ESCRT, and SON/SRRM2 relationships carried more weight than same-family or same-signaling-pathway edges.

## Missing and negative evidence

The frozen browser sometimes supplied no candidate-naming function claims or no atomic relation for a graph edge. I treated that as absent local evidence, not as proof that the gene is functionless. `Il4ra` is the extreme case with zero function claims; I rejected it because the known interleukin receptor biology is off-context for NeuN-positive thalamic glutamatergic neurons, not because the dossier was empty. Likewise, several rejected graph candidates had real neuronal functions but lacked a convincing acute depletion direction: `Snap25` and `Stxbp1` should block transmitter release, `Bbs9` and `Ift88` should perturb cilia, and `Tsc1`/`Tsc2` should activate mTORC1, but none was ranked above direct RNA export, splicing, V-ATPase, proteasome, or ER-Golgi machinery.

I did not attempt to infer a held-out endpoint from graph degree, seed count, or heuristic rank. The final 50 are a biological ordering of acute nonredundant loss-of-function plausibility in the specified postmitotic thalamic glutamatergic class.
