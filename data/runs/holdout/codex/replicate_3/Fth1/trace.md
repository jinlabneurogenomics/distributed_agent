# Fth1 n_degs prediction

Target and endpoint: `Fth1` in `151 TH Prkcd Grin2c Glut`; predict the number of measured genes with BH-adjusted Wilcoxon `p < 0.05`.

Evidence used:

- The declared target bundle reports direct expression of `Fth1` in the focal class: 17,566 / 23,679 non-target nuclei expressed the feature, mean log1p CP10k was 0.599, and pseudobulk expression was 103.84 CPM. This makes `Fth1` transcriptionally present in the assayed thalamic glutamatergic nuclei but does not measure CRISPR efficiency.
- The functional-stock card judged FTH1 ferroxidase activity as likely substantially depleted by the 21-28 day harvest window, but only with moderate confidence: a loss edit stops new heavy-chain supply while leaving existing 24-subunit ferritin shells and stored iron initially intact, and the turnover clock is transferred from iron-mobilized non-neural cells rather than measured in postmitotic thalamic neurons.
- The same biology card weakens a large-effect prior for this exact assay: the direct postnatal-mouse loss evidence is in oligodendroglial lineage cells, not NeuN-positive thalamic neurons, and `Ftl1` can still contribute ferritin shell material even though it does not supply FTH1 ferroxidase activity.
- The focal-class training table is extremely sparse: 1,205 / 1,674 training perturbations had `n_degs = 0`, 1,571 / 1,674 had `n_degs <= 10`, and only 43 reached `n_degs >= 100`.
- In the focal-class Parquet, nearby iron, oxidative-stress, mitochondrial iron, and autophagy perturbations were quiet despite being measured with ordinary recovered-cell counts: `Aco2`, `Abcb7`, `Abcc9`, `Atg5`, `Becn1`, `Gpx4`, `Hif1a`, `Nfe2l1`, `Nfe2l2`, and `Tfrc` each had 0 significant genes. `Acsl4`, `Ireb2`, `Park7`, and `Sqstm1` had 1 significant gene each. These genes are not perfect FTH1 analogs, but they show that this readout does not generally convert iron/oxidative-stress biology into a broad thalamic survivor-state signature.
- The high-count tail in the same table was dominated by globally disruptive RNA-processing, proteostasis, or chromatin regulators, for example `Uba5` 2677, `Tpr` 1768, `Sin3a` 1433, `Psmb4` 742, and `Ufc1` 572. `Fth1` lacks that immediate regulatory breadth.

Synthesis: `Fth1` is expressed and the perturbation is biologically plausible by harvest, so I do not treat it as a guaranteed null. The focal neuron context, pre-existing ferritin stock, possible light-chain residual function, and quiet local measurements for iron/oxidative-stress/autophagy genes all push the forecast down into the 0-1 DEG range rather than the high-yield global-stress tail. I assign one DEG as the point forecast to allow for either the target transcript itself or one small survivor-state marker crossing FDR.
