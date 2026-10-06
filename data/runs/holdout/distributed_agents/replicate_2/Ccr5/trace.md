# Ccr5 DEG-count prediction

## Question and interpretation

The requested readout is the integer number of genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after a held-out CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` cells. The manifest for this run contains one held-out target, `Ccr5`.

I treated `0` as "no measured transcript is expected to pass the experiment's FDR 0.05 threshold in this focal cell group", not as evidence that Ccr5 is biologically irrelevant, unedited, or never functional in neurons. The readout is a sparse, homeostatic, juvenile NeuN-enriched nuclear-RNA endpoint 3-4 weeks after P16 AAV CRISPR delivery; ligand stimulation, injury, peripheral immune cells, and microglia-rich readouts are outside the assay.

## Sources used

- `training_de_all_cell_groups.parquet`: same-experiment per-gene Wilcoxon signatures for non-held-out perturbations.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed `n_degs` for the 1,674 non-held-out perturbations in the focal cell group.
- `032_Ccr5.csv`: the held-out manifest; it contains exactly `Ccr5`.
- Distributed Agents same-experiment corpus `perturbai-july-260713-sourceguard-1773-v1`, especially:
  - `Ccr2:F001-F004`, reporting pan-neuronal flatness of the measured CCR2 surface.
  - Claim `claim:72c3acfe50f5f2be2163`, which integrates Ccr2, Cx3cr1, Cxcr4, and Rac1 findings and concludes that represented chemokine-receptor/Rac-arm perturbations do not form a common postmitotic neuronal RNA program.
  - Claim `claim:00185d4f97d4e028c8d4`, covering the flat IFN receptor/STAT/IRF/JAK-STAT neighborhood.
  - Claim `claim:778b2c45f226febe4372`, covering the flat basal TNFR/TLR/IL-1-to-TAK1/IKK/NF-kappaB/JNK/p38 neighborhood.
- PubMed literature:
  - Combadiere et al. 1996 cloned CCR5 and showed CCL3/MIP-1alpha, CCL4/MIP-1beta, and CCL5/RANTES activate CCR5 through a pertussis-toxin-sensitive Gi-coupled calcium response in transfected cells. DOI 10.1002/jlb.60.1.147; PMID 8699119.
  - Zhou et al. 2016 reported that decreasing Ccr5 function can enhance MAPK/CREB signaling, long-term potentiation, hippocampus-dependent memory, and barrel-cortex plasticity. DOI 10.7554/eLife.20985; PMID 27996938.
  - Joy et al. 2019 reported injury-dependent cortical neuronal CCR5 expression after stroke and improved recovery after neuronal Ccr5 knockdown or CCR5 antagonism after stroke/TBI. DOI 10.1016/j.cell.2019.01.044; PMID 30794775.

## Computation over the input data

1. Loaded the requested manifest and confirmed a single target, `Ccr5`.
2. Summarized the focal-cell training-count CSV:
   - 1,674 training perturbations.
   - 469 nonzero and 1,205 zero DEG counts.
   - median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`, 95th percentile `= 18`, maximum `= 2677`.
3. Pulled the 151-cell-group rows from the parquet for the Ccr5-relevant in-dataset analogs:

   ```python
   dataset = ds.dataset(parquet_path, format="parquet")
   filt = (
       (pc.field("group_name") == "151 TH Prkcd Grin2c Glut") &
       pc.field("gene_target").isin(candidate_targets)
   )
   table = dataset.to_table(
       columns=[
           "names", "gene_target", "scores", "logfoldchanges",
           "pvals_adj", "n_pert_matched", "n_ctrl_matched",
       ],
       filter=filt,
   )
   ```

   Each queried focal profile had 17,259 measured genes. The closest Ccr5 comparators in this slice were flat: `Ccr2 = 0`, `Cxcr4 = 0`, `Rac1 = 0`, `Nfkb1 = 0`, `Rel = 0`, `Mapk1 = 0`, `Pik3r1 = 0`, `Pik3cb = 0`, `Stat2 = 0`, `Stat3 = 0`, `Stat4 = 0`, `Stat5b = 0`, `Ifnar1 = 0`, `Ifnar2 = 0`, `Ifngr1 = 0`, `Ifngr2 = 0`, `Tlr2 = 0`, `Tlr3 = 0`, and `Tlr4 = 0`. `Stat1` was the one near-pathway exception with `n_degs = 1`, and that hit was the target transcript itself (`Stat1`, log2FC -1.300, adjusted p = 0.027).
4. Ran a fixed same-cell-group profile comparison over `Ccr2`, `Cxcr4`, `Rac1`, `Stat1`, `Nfkb1`, `Rel`, `Mapk1`, `Pik3r1`, `Stat3`, and `Ifngr1`. Pairwise whole-profile similarities among focal Ccr5 analogs and inflammatory/signaling peers were near zero. Examples: `Ccr2` vs `Cxcr4` Pearson 0.0249/cosine 0.0263; `Ccr2` vs `Rel` Pearson 0.0296; `Cxcr4` vs `Ifngr1` Pearson 0.0306; `Rac1` vs `Pik3r1` Pearson 0.0394. None of the 24 inspected focal-to-peer pairs shared a significant positive or negative feature. This made the zero counts look like true absence of a coordinated signature rather than several strong but mutually different signatures.

## Target-specific reasoning

### Ccr5

**Biology.** Ccr5 encodes a seven-transmembrane CC-chemokine receptor. Its canonical agonists include CCL3, CCL4, and CCL5, and the receptor couples to Gi in immune cells or heterologous systems (Combadiere et al. 1996). Those facts made the most obvious same-screen analogs other chemokine receptors and the inflammatory or GPCR effector arms downstream of ligand-activated CCR5: `Ccr2`, `Cxcr4`, `Cx3cr1`, `Rac1`, NF-kappaB/Rel, MAPK, PI3K, and JAK/STAT targets.

**Within-dataset analogs and counterexamples.**

- `Ccr2`, the closest represented CC chemokine receptor, had `n_degs = 0` in `151 TH Prkcd Grin2c Glut`; in the corpus it was pan-neuronally null with no FDR<0.10 genes in 22 recovered neuronal groups. Its chemokine-family comparison found that `Cx3cr1` was flat across 23 tested groups and `Cxcr4` produced only isolated single-gene hits, with approximately zero similarity to `Ccr2`.
- `Cxcr4` had `n_degs = 0` in the focal cell group. The focal DE surface had one near miss, `Pum1` up-regulation at adjusted p = 0.067, but no FDR 0.05 genes. The corpus also reports that Cxcr4 produced only two isolated one-gene islands across the atlas rather than a CXCL12/CXCR4/ACKR3 developmental or chemokine-GPCR module.
- `Rac1`, an indirect migration/cytoskeletal branch that can sit downstream of chemokine GPCRs, had `n_degs = 0` in the focal cell group. Its same-corpus nonzero event was a distinct Sst-restricted `Ranbp1` singleton, not a Cxcr4- or Ccr2-like signature.
- Inflammatory and cytokine receptor arms that could in principle make Ccr5 loss visible were also focal zeros: `Nfkb1`, `Rel`, `Mapk1`, `Pik3r1`, `Pik3cb`, `Stat2`, `Stat3`, `Stat4`, `Stat5b`, `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`, `Il10ra`, `Il6ra`, `Il6st`, and TLR-family genes all had `0` DEGs in the training-count table for this cell group. The only focal STAT-family nonzero was `Stat1 = 1`, but the lone FDR gene was `Stat1` itself rather than an interferon-stimulated or chemokine effector.

The Distributed Agents corpus supports the same interpretation beyond this one cell group: represented chemokine receptor/Rac perturbations lack a common postmitotic neuronal program, represented interferon receptor/STAT/IRF perturbations do not form a basal neuronal IFN/JAK-STAT module, and represented TNFR/TLR/IL-1-to-NF-kappaB/JNK/p38 perturbations are broadly transcriptionally silent in unchallenged postnatal NeuN-positive neurons. Those are the pathways I would have expected to rescue a nonzero Ccr5 prediction if Ccr5 were tonically driving a focal-cell transcriptional state.

**Why zero.** I predict `Ccr5` will behave like `Ccr2` rather than like a broad responder. The direct CC-receptor training example is zero in the focal group, the represented chemokine receptor neighborhood is near-flat rather than convergent, and downstream inflammatory or second-messenger transcription-factor nodes are also flat in the same focal-cell readout. External literature does establish neuronal CCR5 biology in plasticity and injury contexts, including MAPK/CREB changes after Ccr5 reduction and increased neuronal CCR5 expression after stroke/TBI (Zhou et al. 2016; Joy et al. 2019), but those effects were in hippocampal, cortical, or injured systems and often reflect circuit, synaptic, protein/phosphorylation, or repair phenotypes rather than a broad basal single-nucleus RNA signature in uninjured postnatal TH/Prkcd/Grin2c glutamatergic neurons.

Point prediction: `0`.

## Limits

- `Ccr5` was held out completely; there is no same-target expression profile or DEG count in the inputs.
- The training set did not include `Ccr1`, `Ccr3`, `Ccr4`, or Ccr5-ligand perturbations such as `Ccl3`, `Ccl4`, and `Ccl5`, so `Ccr2` and `Cxcr4` are family/pathway comparators, not perfect same-ligand paralogs.
- Several proximal signaling nodes that could connect cytokine or chemokine receptors to STAT/NF-kappaB were unavailable as perturbation targets, including JAK kinases and some canonical NF-kappaB components. The represented downstream receptors and transcription factors were nevertheless flat in the focal data.
- The screen is sparse AAV CRISPR in healthy NeuN-enriched juvenile brain. It does not test Ccr5 after exogenous chemokine, HIV envelope peptides, stroke, TBI, peripheral immune recruitment, or microglial activation, all contexts in which CCR5 biology could be stronger.
- DEG count is power- and threshold-dependent. A zero point estimate means I expect no transcript to pass FDR 0.05 in this exact assay, not that every Wilcoxon score is literally zero or that Ccr5 loss has no electrophysiological, synaptic, phosphoproteomic, or behavioral consequence.
