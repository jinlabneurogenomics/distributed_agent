# Nyx DEG-count prediction

## Point prediction

`Nyx`: **0** DEGs in `151 TH Prkcd Grin2c Glut` at BH-adjusted Wilcoxon `p < 0.05`.

## Evidence used

- **Declared target bundle:** `Nyx` is barely present in the exact focal population: 738/23,679 matched non-target nuclei expressed the feature, or 3.1167%, with mean raw UMI 0.0333 and pseudobulk 2.09 CPM in `151 TH Prkcd Grin2c Glut`. Exact in-assay reach therefore supersedes the qualitative low brain-expression prior and makes any cell-autonomous effect highly diluted in this broad thalamic aggregate.
- **Functional biology:** the strongest functional evidence is retinal ON/depolarizing bipolar-cell biology. Nyctalopin is a GPI-linked extracellular membrane accessory for TRPM1 at bipolar-cell dendritic tips; the declared functional-stock card judged the P16-to-P37/P44 perturbation as `partially_depleted_or_leading_edge`, because new supply should stop but pre-edit membrane-associated protein is not directly removed and may be synaptically long-lived. That argues for weak endpoint realization, not a broad thalamic nuclear-RNA state.
- **Training count distribution:** the declared `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` table contains 1,674 visible training perturbations; 1,205 have 0 DEGs, the median is 0, the 75th percentile is 1, and the 90th percentile is only 2. A zero count is the modal outcome before applying the Nyx-specific low-reach prior.
- **Retinal/signalplex comparators in the count table and Parquet:** `Trpm1`, the direct Nyx partner, was not a represented training perturbation, but represented ON-bipolar and proximal signaling comparators were quiet in the same `151` context. Direct Parquet queries over 17,259 measured genes gave `Grm6=0`, `Gpr179=0`, `Pik3r1=0`, `Lrrtm3=0`, `Lrrtm4=0`, `Gnao1=1`, and `Lrrtm1=1` DEGs at FDR 0.05. The same-experiment corpus reports that `Grm6` and `Gpr179` perturbation did not produce a coordinated transcript-level ON-bipolar signalplex response in postnatal brain neurons; `Lrrtm1`/`Lrrtm3`/`Lrrtm4` likewise bound the synaptic-adhesion axis as mostly transcriptionally buffered in this snRNA-seq assay.
- **Profile-neighborhood check from the declared Parquet:** using the seven quiet retinal/synaptic anchors above against all 1,674 eligible training profiles in `151 TH Prkcd Grin2c Glut`, the profile-neighbor union had 333 targets with a median of 0 DEGs; 259/333 had 0, 312/333 had at most 1, and 320/333 had at most 5. The neighborhood therefore stayed in the same low-response basin rather than pointing to a hidden high-DEG program.

## Synthesis

Nyx has a real loss-of-function phenotype, but the evidence places it in retinal synaptic signaling rather than a thalamic transcriptional regulator. In this assay the target is expressed by only a small minority of the matched thalamic glutamatergic nuclei, its operative protein stock may not be cleared within the 21-28 day post-edit window, and the most relevant represented pathway/synaptic comparators are zero- or one-DEG perturbations in the exact requested class. I therefore choose the modal low-response endpoint rather than a sparse singleton and predict **0**.
