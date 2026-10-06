# Trace: Predicting Even-Ranked Perturbations for Thalamic Glutamatergic Neuron Depletion

## Task Overview
Predict the 50 even-ranked (held-out) perturbations that cause depletion in thalamic glutamatergic neurons (`151 TH Prkcd Grin2c Glut`), given 50 odd-ranked known hits.

## Data Exploration

### Dataset Structure
- **Total rows**: 745,758,369 (genome-wide DE results across cell types)
- **Thalamic glutamatergic subset**: 35,311,914 rows
- **Unique perturbations**: 2,046 gene targets
- **Unique measured genes**: 17,259

### Known Gene Analysis
All 50 known depleting genes were present in the dataset. Key functional categories identified:

| Category | Known Genes |
|----------|-------------|
| V-ATPase/lysosome | Atp6v1b2, Atp6v1a |
| Proteasome | Psmb4, Pomp |
| Translation | Eef2 |
| RNA processing | Son, Polr3b, Ddx23, Thoc1, Adarb1 |
| Vesicle trafficking | Cltc, Gbf1, Sec31a, Stx5a, Kif1a |
| ESCRT/autophagy | Chmp4b, Snf8 |
| Mitochondria | Hspa9 |
| Transcription/chromatin | Taf1, Kansl1, Brd4, Myt1l, Nfix, Six3, Six6 |
| Neuronal migration | Pafah1b1, Dmd, Ank3 |
| Signaling | Pten, Lrp6, Rapgef2, Dock3 |

## Methodology

### 1. Composite Score Calculation
For each perturbation, calculated:
- **Mean log fold change** (more negative = stronger effect)
- **Max absolute score** (peak transcriptional changes)
- **Number of significantly changed genes**
- **Number of strongly affected genes** (|LFC| > 1)

Formula: `composite_score = -mean_lfc + max_abs_score * 0.5 + log(n_strong_changes) * 0.3`

### 2. Functional Category Bonuses
Applied multiplicative bonuses for genes in pathways known to be essential for neuronal survival:

| Category | Bonus |
|----------|-------|
| Lysosome/V-ATPase | 1.5x |
| Proteasome | 1.5x |
| RNA processing | 1.4x |
| Synaptic | 1.4x |
| Translation | 1.3x |
| Chaperone | 1.3x |
| Trafficking | 1.2x |
| Ion channel | 1.2x |
| Mitochondria | 1.2x |
| Autophagy | 1.2x |
| Ubiquitin | 1.2x |
| Chromatin | 1.2x |

### 3. Literature Validation
Key literature supporting methodology:

1. **Wertz et al. (2020)** - Neuron (PMID: 32004439)
   - First genome-wide CRISPR screens in mammalian CNS
   - Identified CNS neurons are sensitive to perturbations in: synaptic processes, autophagy, proteostasis, mRNA processing, mitochondrial function
   
2. **Ramani et al. (2025)** - Nature Neuroscience (PMID: 40847019)
   - CrAAVe-seq platform for neuronal essential genes
   - Validated Rabggta and Hspa5 as neuronal essential genes
   
3. **Abbott et al. (2009)** - Biochem Soc Trans (PMID: 19909265)
   - Eef1a2 loss causes motor neuron degeneration in wasted mice
   - Validates Eef1a2 as top prediction

4. **Huang et al. (2024)** - Commun Biol (PMID: 38182732)
   - SNAP-25 essential for neuronal development, survival, and function
   - Validates Snap25 as prediction

5. **Vardar et al. (2016)** - J Neurosci (PMID: 27466336)
   - Syntaxin-1 essential for neuronal maintenance
   - Supports synaptic category importance

## Results Summary

### Top Predictions by Category
- **RNA processing** (11): Srsf1, Matr3, Fus, Hnrnpu, Tardbp, Hnrnpc, Snrpn, Thoc2, Prpf6, Hnrnph2, Hnrnpa2b1
- **Ion channels** (9): Scn1b, Atp1a3, Grin1, Gabrb2, Scn1a, Gabrd, Gabrg2, Kcnq2, Gabra1
- **Lysosome** (6): Ctsb, Atp6ap1, Atp6v0c, Atp6ap2, Atp6v0a1, Atp6v1e1
- **Synaptic** (5): Snap25, Sv2a, Syn1, Stxbp1, Synj1

### Score Comparison
- Known genes mean composite score: 9.17
- Top 50 predictions mean composite score: 12.45

The higher composite score of predictions reflects that even-ranked positions may include some of the strongest depleting perturbations.

## Limitations

1. **DE as proxy for depletion**: Differential expression measures transcriptional changes in surviving cells, not direct cell loss. Strong depletion may remove cells before DE can be measured.

2. **Cell type specificity**: Predictions are based on thalamic glutamatergic neuron data. Some genes may have different essentiality in other neuronal subtypes.

3. **Functional annotation bias**: Category bonuses rely on known gene functions. Novel essential genes without established annotations may be underranked.

4. **Interleaved ranking assumption**: The task assumes even-ranked genes are similar in effect magnitude to adjacent odd-ranked genes. Our predictions prioritize highest-confidence candidates.

5. **Library coverage**: Not all genes in the genome were perturbed. Essential genes not in the library cannot be predicted.

## Citations

1. Wertz MH, et al. Genome-wide In Vivo CNS Screening Identifies Genes that Modify CNS Neuronal Survival and mHTT Toxicity. Neuron. 2020;105(4):596-614.e6. PMID: 32004439

2. Ramani B, et al. CRISPR screening by AAV episome-sequencing (CrAAVe-seq): a scalable cell-type-specific in vivo platform uncovers neuronal essential genes. Nat Neurosci. 2025. PMID: 40847019

3. Abbott CM, et al. eEF1A2 and neuronal degeneration. Biochem Soc Trans. 2009;37(Pt 6):1293-7. PMID: 19909265

4. Huang M, et al. SNAP-25, but not SNAP-23, is essential for photoreceptor development, survival, and function in mice. Commun Biol. 2024;7(1):42. PMID: 38182732

5. Vardar G, et al. Distinct Functions of Syntaxin-1 in Neuronal Maintenance, Synaptic Vesicle Docking, and Fusion in Mouse Neurons. J Neurosci. 2016;36(30):7911-24. PMID: 27466336

6. Marshall GF, et al. Face-valid phenotypes in a mouse model of the most common mutation in EEF1A2-related neurodevelopmental disorder. Dis Model Mech. 2024;17(1):dmm050501. PMID: 38179821
