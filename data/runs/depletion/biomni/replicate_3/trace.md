# Trace: Predicting Even-Ranked Perturbations for Thalamic Glutamatergic Neuron Depletion

## Task Overview
Predict the 50 even-ranked perturbations (ranks 2, 4, 6, ..., 100) that cause depletion in thalamic glutamatergic neurons (151 TH Prkcd Grin2c Glut), given the 50 odd-ranked perturbations as ground truth.

## Data Analysis Approach

### 1. Dataset Exploration
- **Source**: Parquet file with Wilcoxon DE results
- **Cell type filter**: `151 TH Prkcd Grin2c Glut` (thalamic glutamatergic neurons)
- **Total perturbations**: 2,046 unique gene targets
- **Candidates after exclusions**: 1,896 (excluding 50 known genes and controls)

### 2. Key Observation from Known Depleting Genes
Analysis of the 50 known odd-ranked depleting genes revealed:
- **Mean logfoldchanges**: -3.89 (vs -3.41 for all perturbations)
- **Range**: -5.40 (Atp6v1b2) to -2.25 (Tnpo3)
- **Key insight**: Depleting perturbations show significantly more negative mean log fold changes across all measured genes

### 3. Biological Pathway Analysis of Known Genes
The known depleting genes cluster into functional categories:

| Category | Known Genes | Rationale |
|----------|-------------|-----------|
| V-ATPase/acidification | Atp6v1b2, Atp6v1a | Essential for synaptic vesicle function |
| Vesicle trafficking | Cltc, Gbf1, Sec31a, Stx5a, Chmp4b, Snf8, Kif1a | Required for neuronal transport |
| Proteasome/ubiquitin | Psmb4, Pomp, Cul3, Fbxo11, Trip12 | Protein quality control |
| Transcription/chromatin | Taf1, Kansl1, Son, Brd4, Cnot1, Ddx23, Polr3b, Thoc1 | Gene expression regulation |
| Translation | Eef2 | Essential for protein synthesis |
| Signaling | Pten, Lrp6, Rapgef2, Ppp2r1a | Key neuronal signaling pathways |
| Neuronal development | Pafah1b1, Myt1l, Nfix, Six3, Six6 | Brain development |

### 4. Scoring Methodology

**Final Score = -LFC_zscore + Pathway_Bonus**

Where:
- **LFC_zscore**: Z-score of mean log fold changes (more negative = higher score)
- **Pathway_Bonus**: 0-3 points based on functional similarity to known genes:
  - V-ATPase genes (Atp6v, Atp5): +3
  - Vesicle trafficking (Sec, Stx, Vps, Rab, Chmp): +2
  - Proteasome/ubiquitin (Psm, Ube, Ubr, Cul, Fbx): +2
  - Transcription/chromatin (Taf, Med, Brd, Kdm, Kmt, Hdac, Crebbp, Ep300, Thoc): +2
  - Translation (Eef, Eif): +2
  - RNA processing (Ddx, Dhx, Snrp, Hnrnp): +1.5
  - Signaling (Pik3, Ppp, Gsk3): +1.5
  - Cytoskeleton/kinesins (Kif, Dyn, Tub): +1
  - Mitochondria (Hsp, Cox, Nduf): +1
  - Nuclear transport (Nup, Kpn, Xpo): +1

## Literature Support for Top Predictions

### Thoc2 (Rank 1)
- **LFC mean**: -5.86 (strongest depletion signal)
- **Evidence**: THOC2 mutations cause X-linked intellectual disability with severe neurocognitive features (PMID: 29851191, 26166480)
- **Function**: TREX mRNA export complex subunit, essential for neuronal development

### Atp6v1e1 (Rank 3)
- **LFC mean**: -4.75
- **Evidence**: V-ATPase essential for synaptic vesicle acidification and neurotransmitter release (PMID: 34620624, 30155790, 20670834)
- **Function**: V-ATPase E1 subunit, same complex as known genes Atp6v1a and Atp6v1b2

### Crebbp (Rank 6)
- **LFC mean**: -4.51
- **Evidence**: CBP essential for dendritic growth and synaptic maturation; loss causes neuronal deficits (PMID: 30850733)
- **Function**: Transcriptional coactivator, chromatin modifier

### Ube3a (Rank 8)
- **LFC mean**: -4.23
- **Evidence**: Mutations cause Angelman syndrome with severe intellectual disability (PMID: 41310868, 40076922, 9288101)
- **Function**: E3 ubiquitin ligase, essential for neuronal function

### Dyrk1a (Rank 47)
- **LFC mean**: -4.33
- **Evidence**: Overexpression causes Down syndrome features; essential for neurodevelopment (PMID: 41701821, 20600907)
- **Function**: Dual-specificity kinase regulating neuronal development

### Gsk3b (Rank 23)
- **LFC mean**: -4.01
- **Evidence**: Key regulator of neuronal survival; inhibition protects neurons (PMID: 39814010)
- **Function**: Glycogen synthase kinase 3 beta, regulates multiple neuronal pathways

## Limitations

1. **Indirect measurement**: DE analysis measures transcription in surviving cells, not direct cell counts. Depletion removes cells before this readout.

2. **Scoring assumptions**: Pathway bonus scores are based on functional similarity to known genes, which may miss novel mechanisms.

3. **No experimental validation**: Predictions are based on computational analysis and literature, not experimental verification.

4. **Cell type specificity**: Some genes may have different effects in thalamic glutamatergic neurons vs other neuronal types.

5. **Temporal effects**: The P16→P37-44 window may miss genes with effects outside this timeframe.

## Key Citations

1. Wertz MH et al. (2020) "Genome-wide In Vivo CNS Screening Identifies Genes that Modify CNS Neuronal Survival." Neuron. PMID: 32004439

2. Tian R et al. (2019) "CRISPR Interference-Based Platform for Multimodal Genetic Screens in Human iPSC-Derived Neurons." Neuron. PMID: 31422865

3. Kumar R et al. (2018) "Severe neurocognitive and growth disorders due to variation in THOC2." Human Mutation. PMID: 29851191

4. Del Blanco B et al. (2019) "CBP and SRF co-regulate dendritic growth and synaptic maturation." Cell Death Differ. PMID: 30850733

5. Albrecht U et al. (1997) "Imprinted expression of the murine Angelman syndrome gene, Ube3a, in hippocampal and Purkinje neurons." Nature Genetics. PMID: 9288101

6. Di Giovanni J et al. (2010) "V-ATPase membrane sector associates with synaptobrevin to modulate neurotransmitter release." Neuron. PMID: 20670834
