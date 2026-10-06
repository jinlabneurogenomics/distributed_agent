target: Stim1
cell group: 151 TH Prkcd Grin2c Glut
prediction: 1

Stim1 is absent from the declared training count table, and I did not inspect
any Stim1 endpoint profile. The count table contains 1,674 observed training
targets for this exact cell group. It is highly zero-inflated: 1,205/1,674
targets have n_degs = 0, the median is 0, the 75th percentile is 1, the 90th
percentile is 2, and the 95th percentile is 18. Large DEG burdens are rare and
dominated by perturbations of broad cell-state machinery.

The biology bundle supports real but probably buffered perturbation in the
focal thalamic neurons. The exact in-assay reach is moderate: Stim1 is detected
in 10,441/23,679 non-target nuclei in this class, or 44.09%, with pseudobulk
expression of 40.85 CPM. The functional-stock card calls the P16 disruptive
edit likely to substantially deplete STIM1 by the P37-P44 harvest because
STIM1 is the renewed ER calcium sensor/channel-coupling protein itself.
However, the closest mouse neural evidence is outside this thalamic population:
adult forebrain Stim1 single loss was mild relative to combined Stim1/Stim2
loss, and Purkinje-neuron STIM1 dependence comes from a high-demand cell type
that does not transfer quantitatively to thalamic glutamatergic nuclei. The
bundle therefore pushed the forecast above an unexpressed/null target, but not
toward a high-burden response.

The most direct STIM family and ORAI channel comparators were not available in
the training count table, so I used calcium/synaptic observed perturbations as
quantitative scale references. In a hand-picked 25-target calcium, calmodulin,
calcineurin, channel, glutamate-receptor, and synaptic-scaffold cohort, the
median n_degs was 1; 18/25 had <=2 DEGs and 22/25 had <=14. The central
single-target calcium-signaling anchors were quiet to weak in the training
expression parquet for this same cell group: Itpr1 had 0 significant genes,
Camk2a 0, Ppp3ca 4, Calm1 14, Grin1 89, and Atp2a2 187. I treated Grin1 and
Atp2a2 as upper-bound stressors because they are core excitatory drive and ER
calcium-pump perturbations, respectively, while Stim1 single loss is upstream
store-operated entry with STIM2 buffering.

Synthesis: Stim1 should be functionally engaged in a substantial minority of
151 TH Prkcd Grin2c Glut nuclei by harvest, but its single-loss operation is
less likely than Grin1 or Atp2a2 to produce a broad survivor transcriptome.
The best point estimate is the very-low, near-median part of the observed
calcium/synaptic training band: 1 BH-significant DEG.
