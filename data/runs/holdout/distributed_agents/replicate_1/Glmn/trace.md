# Prediction task

The requested endpoint is the held-out `n_degs` for `Glmn`: the number of
measured genes with a Benjamini-Hochberg-adjusted Wilcoxon p-value below 0.05
after acute mosaic CRISPR loss of `Glmn` in the recovered
`151 TH Prkcd Grin2c Glut` nuclei.  I treated the count as an assay-specific
response-breadth measurement, not as a direct measure of biological importance,
target editing, abundance, or viability.

The target manifest for this run contains exactly one perturbation, `Glmn`, and
`Glmn` is absent from both training inputs as expected for a held-out target.

# Sources

- Direct endpoint source: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`,
  the observed focal-cell DEG counts for non-held-out perturbations.
- Direct DE source: `training_de_all_cell_groups.parquet`, queried at
  `group_name == "151 TH Prkcd Grin2c Glut"` for biologically selected CRL and
  F-box analogs.
- Internal same-experiment semantic source:
  PerturbAI July corpus release `perturbai-july-260713-sourceguard-1773-v1`;
  specifically the packaged `Fbxw7`, `Fbxo11`, and `Fbxo38` Finding records.
  This corpus is an interpreted view of the same experiment, so I used it for
  compact expression-pattern context rather than as independent replication.
- External mechanism sources from PubMed:
  Brouillard et al. 2002, DOI `10.1086/339492`, identified loss-of-function
  `GLMN` mutations as the cause of glomuvenous malformations.
  Tron et al. 2012, DOI `10.1016/j.molcel.2012.02.005`, showed that GLMN binds
  the RING domain of RBX1, inhibits CRL1/SCF-FBW7 ligase activity, and that
  GLMN loss decreases FBW7 protein while increasing Cyclin E and c-Myc in
  vascular and other non-neuronal systems.
  Duda et al. 2012, DOI `10.1016/j.molcel.2012.05.044`, structurally showed
  that GLMN masks the E2-binding surface of RBX1 in a GLMN-RBX1-CUL1 complex.
  Suzuki et al. 2014, DOI `10.1073/pnas.1324021111`, and Suzuki et al. 2017,
  DOI `10.15252/embr.201643841`, connected GLMN to inflammasome regulation via
  RING E3 ligases in macrophages; I treated this as weakly relevant because
  non-neuronal innate immune cells are largely absent from the NeuN-enriched
  dataset.
  Matsumoto et al. 2011, DOI `10.1074/jbc.M110.194936`, and Jandke et al. 2011,
  DOI `10.1016/j.ydbio.2011.07.030`, establish FBXW7-Notch/c-Jun biology in
  developmental neural systems, but the direct postnatal neuronal `Fbxw7`
  perturbation in this experiment did not recover those large programs.

# Quantitative calibration

The 1,674 training perturbations in the focal DEG-count CSV are strongly
zero-inflated:

- 1,205/1,674 perturbations had zero DEGs.
- The median count was 0 and the 75th percentile was 1.
- Only 5% of visible perturbations exceeded 18 DEGs.

That puts an uninformative visible perturbation at 0 rather than at a moderate
positive count.  I therefore only moved the prediction above zero for `Glmn` to
the extent that a directly related visible perturbation showed a reproducible
focal signature.

# Target-specific reasoning

## Glmn

`Glmn` encodes glomulin, a negative regulator of RBX1-containing cullin-RING
ligases.  The closest established mechanistic link is not to another GLMN
paralog but to CRL1/SCF-FBW7: GLMN binds RBX1 and inhibits E2 access to the
CRL catalytic RING surface, and loss of GLMN can destabilize FBW7 and increase
canonical FBW7 substrates in non-neuronal vascular or cultured cells
(Tron et al. 2012; Duda et al. 2012).

The core SCF components `Cul1`, `Rbx1`, and `Skp1` were not in the visible
focal training-count table, so the most informative same-experiment analog was
`Fbxw7` itself.  `Fbxw7` loss caused 1 DEG in `151 TH Prkcd Grin2c Glut`:
`Trp53inp2` was up-regulated with log2 fold change 0.485 and adjusted
p-value 0.0451 in 154 perturbed nuclei versus 23,679 matched controls.  The
packaged `Fbxw7` report showed that this was an isolated autophagy-linked hit:
canonical FBXW7-output mRNA programs involving Notch/Hes, Jun, Myc/Ccne1,
mTOR/SREBP, or NFE2L1/proteasome markers were not recovered across the assayed
neuronal groups.

The other visible F-box controls also sat at the same quiet boundary rather
than indicating a generic F-box transcriptional stress response.  `Fbxo11`
caused 1 focal DEG, a `Ppib` decrease with log2 fold change -0.553 and
adjusted p-value 0.0320 in 57 perturbed nuclei, and its same-experiment report
described no broad unfolded-protein, p53/TGF-beta, or shared F-box response.
`Fbxo38` caused 0 focal DEGs in 194 perturbed nuclei; its report described
two singleton responder groups elsewhere and no meaningful recurrent module.
Less direct ubiquitin-ligase perturbations were also small in the count table:
`Ube2e2` had 0, `Trim37` had 1 and that was the self transcript, and `Trim2`
had 2.

The causal transfer model is therefore:

1. `Glmn` CRISPR removes a CRL/RBX1 inhibitor in postmitotic neurons.
2. The direct molecular consequence should be increased CRL catalytic access,
   with the most concrete FBXW7-related consequence being lower FBXW7 protein,
   not a loss of a cullin scaffold.
3. In proliferating or vascular contexts that can propagate to Cyclin E, MYC,
   FBW7, and vascular smooth-muscle phenotypes.
4. In this P16-to-P37/44 NeuN-positive neuronal state, direct `Fbxw7`,
   `Fbxo11`, and `Fbxo38` perturbations were buffered and the canonical
   developmental, Notch, cell-cycle, and proteostasis transcriptomes were
   absent or nearly absent.
5. The endpoint counts are survivor-conditioned FDR calls; a single near-
   threshold marker in `Fbxw7` does not establish a broad GLMN response.

This makes a zero or one-DEG outcome the supported range.  I predicted **0**
rather than 1 because `Glmn` is upstream and inhibitory, the expected sign is
not a clean phenocopy of deleting the FBXW7 substrate receptor, no `Glmn`
same-experiment corpus record was available, and the one `Fbxw7` hit was barely
past the FDR 0.05 threshold.  The nonzero prior comes from the direct
GLMN-RBX1-FBW7 biochemistry; the zero decision is driven mainly by the focal
same-experiment observation that the available CRL/F-box perturbations produced
zero or singleton FDR signatures in this exact assay.

# Limits

The prediction extrapolates from pathway-adjacent targets rather than from a
true `Glmn` paralog or a direct `Cul1`/`Rbx1`/`Skp1` perturbation, because those
core genes were not visible in the focal training count file.  The parquet
contains DE summaries rather than raw guide-level indels or protein substrates,
so a flat transcriptome would not exclude successful GLMN editing or CRL
substrate changes at the protein level.  GLMN has vascular and macrophage
literature that may involve cell types absent from this NeuN-enriched screen,
and FBXW7 has developmental neural roles that may have passed before the P16
AAV perturbation window.  The final integer is therefore a low-count,
endpoint-specific estimate for recovered juvenile thalamic glutamatergic
nuclei, not a general claim that GLMN is biologically inert.
