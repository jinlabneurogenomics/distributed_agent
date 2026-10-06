# Trace: Predicting Even-Ranked Perturbations for Thalamic Glutamatergic Neuron Depletion

## Task Overview
Predict 50 even-ranked perturbations (ranks 2, 4, 6, ..., 100) that cause depletion in thalamic glutamatergic neurons (151 TH Prkcd Grin2c Glut), given the 50 odd-ranked members as ground truth.

## Methodology

### 1. Data Exploration
- Loaded the parquet file containing differential expression results
- Filtered for the specific cell type: "151 TH Prkcd Grin2c Glut"
- Identified 2,046 unique gene targets, of which 1,946 are non-control perturbations
- Confirmed all 50 known odd-ranked genes are present in the dataset

### 2. Analysis of Known Depleting Genes
The known genes fall into several functional categories essential for neuronal survival:

**Vesicular trafficking/acidification:**
- V-ATPase: Atp6v1b2 (rank 1), Atp6v1a (rank 15)
- Clathrin: Cltc (rank 7)
- COPII: Sec31a (rank 17)
- ESCRT: Chmp4b (rank 35), Snf8 (rank 43)
- Syntaxin: Stx5a (rank 29)
- GBF1: Gbf1 (rank 9)

**Protein homeostasis:**
- Proteasome: Psmb4 (rank 11), Pomp (rank 25)
- Translation: Eef2 (rank 13)
- Chaperone: Hspa9 (rank 41)

**Transcription/RNA processing:**
- Taf1 (rank 3), Son (rank 21), Polr3b (rank 37)
- Brd4 (rank 65), Cnot1 (rank 45)
- Ddx23 (rank 51), Thoc1 (rank 85), Tnpo3 (rank 33)

**Neuronal development/function:**
- Pafah1b1 (rank 5) - lissencephaly gene
- Kif1a (rank 23) - kinesin motor
- Dmd (rank 39) - dystrophin
- Myt1l (rank 67) - neuronal transcription factor

**Signaling:**
- Gpx4 (rank 31) - ferroptosis regulator
- Pten (rank 93), Lrp6 (rank 83)

### 3. Literature Evidence

**Key publications consulted:**

1. **Ramani et al., Nature Neuroscience 2025** (PMID: 40847019)
   - CrAAVe-seq CRISPR screening in mouse neurons
   - Validated Rabggta and Hspa5 as essential for neuronal survival
   - Hspa5 is in our dataset and included in predictions

2. **Wertz et al., Neuron 2020** (PMID: 32004439)
   - First genome-wide genetic screens in CNS
   - CNS neurons sensitive to: synaptic processes, autophagy, proteostasis, mRNA processing, mitochondrial function
   - These pathways guided category prioritization

3. **V-ATPase essentiality in neurons:**
   - Ma et al., Frontiers in Cellular Neuroscience 2019 (PMID: 31824264): Voa1 knockout causes hippocampal CA1 neurodegeneration
   - Gao et al., Nature Genetics 2021 (PMID: 33833240): ATP6V0A1 essential for brain development
   - Lee et al., Cell 2010 (PMID: 20541250): PS1-dependent V-ATPase targeting essential for autophagy

4. **Translation factors:**
   - Newbery et al., JBC 2007 (PMID: 17640869): eEF1A2 essential for post-weaning survival in mice
   - Mohamed & Klann, PNAS 2023 (PMID: 37695913): EEF1A2 mutations cause autism and epilepsy

5. **Retromer/VPS35:**
   - Vergés, IRCMB 2016 (PMID: 26944621): Retromer essential for neuronal polarity and linked to Parkinson's disease

### 4. Scoring Strategy

Genes were scored based on functional category priority:

| Priority | Score | Category | Rationale |
|----------|-------|----------|-----------|
| 1 | 100 | V-ATPase subunits | Known to cause neuronal death when depleted |
| 2 | 95 | Proteasome subunits | Essential for protein homeostasis |
| 3 | 92 | Translation factors | Essential for protein synthesis |
| 4 | 90 | COPII/Sec pathway | ER-Golgi transport essential |
| 5 | 88 | Chaperones (HSP) | Protein folding essential |
| 6 | 85 | Retromer/VPS | Endosomal sorting essential |
| 7 | 82 | Clathrin/AP complexes | Vesicular trafficking |
| 8 | 80 | RNA processing | Spliceosome, helicases |
| 9 | 78 | Kinesins | Neuronal transport |
| 10 | 75 | Other translation | Additional factors |
| 11 | 72 | DNAJ co-chaperones | Protein folding support |
| 12 | 70 | Autophagy | Cellular clearance |
| 13 | 68 | Ubiquitin ligases | Protein degradation |
| 14 | 65 | Mitochondrial | Energy production |

### 5. Key Predictions and Rationale

**Top predictions:**
1. **Atp6v0a1** (V-ATPase V0 subunit): Direct evidence from Ma et al. 2019 and Gao et al. 2021 showing essentiality in neurons
2. **Atp6v0c** (V-ATPase V0 subunit): Core component of V-ATPase proton pump
3. **Atp6ap2** (V-ATPase accessory): Required for V-ATPase assembly
4. **Psmc5, Psmc1** (Proteasome): Essential for protein degradation
5. **Eef1a2** (Translation): Neuron-specific, essential for post-weaning survival
6. **Eif4g1, Eif4e** (Translation initiation): Essential for cap-dependent translation
7. **Sec23a, Copa** (COPII): ER-Golgi transport essential
8. **Hspa5** (BiP/GRP78): ER chaperone, validated in Ramani et al. 2025
9. **Vps35, Vps41, Vps13 family**: Retromer/endosomal sorting

### 6. Limitations

1. **Indirect inference**: Depletion removes cells before DE readout, so DE signals don't directly measure depletion
2. **Functional category bias**: Predictions favor known essential pathways; novel mechanisms may be missed
3. **Cell type specificity**: Some genes essential in general neurons may not be essential specifically in thalamic glutamatergic neurons
4. **Ranking within tiers**: Genes within the same functional category are ranked arbitrarily
5. **Literature bias**: More-studied genes are more likely to have supporting evidence

### 7. Validation Considerations

The predictions prioritize genes with:
- Strong literature evidence for neuronal essentiality
- Functional similarity to known depleting genes
- Involvement in core cellular processes (protein synthesis, trafficking, degradation)

## Citations

1. Ramani B, et al. (2025). CrAAVe-seq: a scalable cell-type-specific in vivo platform uncovers neuronal essential genes. Nature Neuroscience. PMID: 40847019
2. Wertz MH, et al. (2020). Genome-wide In Vivo CNS Screening Identifies Genes that Modify CNS Neuronal Survival and mHTT Toxicity. Neuron. PMID: 32004439
3. Ma K, et al. (2019). Observations From a Mouse Model of Forebrain Voa1 Knockout. Front Cell Neurosci. PMID: 31824264
4. Gao Y, et al. (2021). ATP6V0A1 encoding the a1-subunit of V-ATPases is essential for brain development. Nat Genet. PMID: 33833240
5. Lee JH, et al. (2010). Lysosomal proteolysis and autophagy require presenilin 1. Cell. PMID: 20541250
6. Newbery HJ, et al. (2007). Translation elongation factor eEF1A2 is essential for post-weaning survival in mice. JBC. PMID: 17640869
7. Mohamed MS & Klann E (2023). EEF1A2 mutations lead to translational dysfunction. PNAS. PMID: 37695913
8. Vergés M (2016). Retromer in Polarized Protein Transport. IRCMB. PMID: 26944621
