# Reasoning trace

## Question and resolved ambiguities

The task is to predict, for each target in `237_Thbd.csv`, how many measured genes would have `pvals_adj < 0.05` after that target was perturbed in `151 TH Prkcd Grin2c Glut` neurons. The manifest for this run contains one held-out target:

| target_name |
|---|
| Thbd |

I treated the endpoint exactly like the supplied training CSV: the count is the number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal cell group, including the perturbed target transcript if that transcript is significant. I did not subtract self-target hits. Zero is a valid point prediction and means I predict no measured gene will survive FDR 0.05 in this cell group.

## Sources

- Training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest: `[local file: 237_Thbd.csv]`
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile-neighborhood tool, run-local output `profile_neighbors_vascular.json`
- PubMed abstracts and cited primary/review literature:
  - Suzuki et al. 1987, `10.1002/j.1460-2075.1987.tb02448.x`, PMID 2820710: human thrombomodulin is an endothelial thrombin receptor and protein C activation cofactor.
  - Daly et al. 2018, `10.1038/s41598-017-18912-8`, PMID 29323190: angiopoietin-1/2 bind thrombomodulin and inhibit its thrombin-cofactor activity, connecting TM to the angiopoietin/TIE2 endothelial axis.
  - Giri, Biswas and Rezaie 2024, `10.1016/j.jtha.2024.01.006`, PMID 38266676: thrombomodulin is a type-I vascular-endothelial receptor controlling anticoagulant, fibrinolytic, complement, inflammatory, and endothelial-quiescence biology.
  - Shibuya 2011, `10.1177/1947601911423031`, PMID 22866201: VEGF-A/KDR and VEGF-C/FLT4 are core endothelial angiogenesis and lymphangiogenesis receptor systems.
  - Morisada et al. 2006, `10.1080/10623320600697989`, PMID 16728326: angiopoietin/TIE2 signaling regulates endothelial survival, migration, vascular remodeling, and vascular integrity.
  - Tillet and Bailly 2015, `10.3389/fgene.2014.00456`, PMID 25620979: BMP9/BMP10/ACVRL1/ENG signaling maintains vascular endothelial quiescence and is central to hereditary hemorrhagic telangiectasia.
  - Corada et al. 2013, `10.1038/ncomms3609`, PMID 24153254: endothelial Sox17 acts upstream of Notch and is required for arterial identity.
  - Tutusaus et al. 2020, `10.3390/cells9102186`, PMID 32998369: Protein S/Gas6 and the TAM receptors AXL/MERTK/TYRO3 regulate inflammation, efferocytosis, and vascular responses to damage.

The Distributed Agents corpus had no target-local record for `Thbd` itself, so the prediction below does not reuse a preinterpreted Thbd perturbation report. I used corpus reports for measured relatives such as `F2`, `Kdr`, `Flt4`, `Tek`, `Eng`, `Acvrl1`, `Sox17`, `Notch1`, `Notch4`, `Axl`, `Mertk`, and `Serpine2`.

## Computations on the supplied DE table

I first loaded the manifest and training counts. The focal training set contains 1,674 non-held-out perturbations; 1,205 of them, or 72.0%, have `n_degs = 0`, so the focal endpoint is zero-inflated and a target needs positive same-assay evidence to move away from zero.

I then pulled the complete `151 TH Prkcd Grin2c Glut` DE rows for a hand-curated set of available Thbd-relevant or counterexample perturbations:

```python
expr = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidates)
)
table = dataset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges",
        "pvals", "pvals_adj", "scores",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=expr,
)
```

For each candidate I recounted `pvals_adj < 0.05` in the focal group and recorded the lowest adjusted p-value. All selected focal signatures contained 17,259 measured-gene rows, with 121 to 324 matched perturbed nuclei and 23,679 matched controls.

| training perturbation | observed `n_degs` in 151 TH Prkcd Grin2c Glut | closest focal evidence |
|---|---:|---|
| `F2` | 0 | Thrombin/prothrombin is upstream of thrombomodulin; its focal minimum `pvals_adj` was 0.698, so even the ligand-side coagulation node was flat. |
| `Kdr` | 0 | VEGFR2 endothelial angiogenic receptor; focal minimum `pvals_adj` was 1.000. |
| `Flt4` | 0 | VEGFR3 lymphatic/endothelial receptor; focal minimum `pvals_adj` was 0.363. |
| `Tek` | 0 | TIE2 angiopoietin receptor in the vascular pathway that Daly et al. linked to TM; focal minimum `pvals_adj` was 1.000. |
| `Eng` | 0 | Endoglin, ACVRL1/BMP9 endothelial co-receptor partner; focal minimum `pvals_adj` was 1.000. |
| `Acvrl1` | 0 | ALK1 endothelial BMP/TGF-family receptor; focal minimum `pvals_adj` was 1.000. |
| `Sox17` | 0 | Arterial endothelial transcription factor upstream of Notch; focal minimum `pvals_adj` was 1.000. |
| `Notch1` | 0 | Notch receptor tested as an endothelial/developmental counterexample; focal minimum `pvals_adj` was 1.000. |
| `Notch2` | 0 | Notch-family receptor counterexample; focal minimum `pvals_adj` was 1.000. |
| `Notch4` | 0 | Endothelial-enriched Notch receptor; focal minimum `pvals_adj` was 0.490. |
| `Axl` | 0 | TAM receptor connected to Gas6/Protein S vascular and efferocytosis biology; focal minimum `pvals_adj` was 0.363. |
| `Mertk` | 0 | TAM paralog and efferocytosis receptor; focal minimum `pvals_adj` was 0.888. |
| `Serpine2` | 2 | Extracellular protease inhibitor counterexample; the focal hits were only `Serpine2` itself and `Clip2`. |
| `Grn` | 1 | Secreted neuroimmune/lysosomal counterexample; its only focal hit was `Grn` itself. |

As a separate check, I asked whether the measured `Thbd` transcript itself was frequently a downstream DEG in this focal group. It was present as a measured gene for all 1,674 training perturbations, but it never crossed `pvals_adj < 0.05`, reinforcing that `Thbd` is not part of a common thalamic-neuronal response module in the training data.

Finally, I used Distributed Agents runtime profile-neighborhood comparison among these vascular/protease/TAM candidates. The comparison deliberately limited the universe to the candidate cohort because `Thbd` itself is held out. It found that these mostly null profiles form a noise-scale connected cohort, without a selective strong responder that would argue for a hidden coagulation/endothelial program in the focal thalamic class.

## Within-dataset analogs

`F2` is the cleanest measured ligand-side comparator. The corpus report for `F2` calls it a pan-neuronal transcriptional null at FDR 0.10, with zero downstream FDR events across 23 neuronal groups and no AP-1, NF-kappaB, cytokine, `Mmp9`, `Serpine1`, or `Socs3` injury/PAR-like program. Its exact focal count at FDR 0.05 is also zero. That is important because if loss of a coagulation protease transcript in sparse postnatal neurons were enough to disturb a durable thrombin/PAR/TM axis, `F2` was an available place for that biology to appear.

`Kdr`, `Flt4`, and `Tek` cover endothelial receptor biology adjacent to Thbd. `Kdr` and `Flt4` test the VEGF/VEGFR arm; `Tek` tests angiopoietin/TIE2 signaling, and angiopoietins can bind TM directly. All three were zero in the focal class. The Distributed Agents corpus makes the same broader point: canonical vascular and lymphatic VEGF/neuropilin/Sox18 pathway programs were not recovered as shared transcriptional modules in NeuN-enriched neurons, and `Tek` loss was transcriptomically silent at FDR 0.10 across all assayed neuronal groups.

`Eng`, `Acvrl1`, and `Sox17` test endothelial quiescence, BMP9/10-ALK1/endoglin signaling, and arterial endothelial identity rather than coagulation itself. They are not biochemical substitutes for Thbd, but they are strong lineage controls. Each had zero focal DEGs. The corpus reports for `Eng` and `Acvrl1` state that the represented `ENG`/`ACVRL1` vascular receptor-SMAD circuit is uncoupled in the sampled postmitotic neurons; the `Sox17` report likewise calls Sox17 a complete postmitotic-neuronal null, with zero FDR 0.10 downstream genes across all 23 measured groups. Those are appropriate counterexamples because they show that even transcription factors and receptors central to endothelial vascular behavior do not automatically drive a thalamic neuronal RNA signature in this assay.

`Notch1`, `Notch2`, and `Notch4` bound the arterial/vascular Notch branch. `Notch4` is the most endothelial of these receptors, yet it was zero in the focal class, and its corpus report says its singleton effects elsewhere were not accompanied by canonical HES/HEY Notch output. `Notch1` and `Notch2` were also focal-zero. This makes a hidden arterial Notch-like response unlikely for `Thbd`.

`Axl` and `Mertk` are more distal. Protein S and Gas6 are vitamin-K-dependent ligands for TAM receptors, so these genes sample a vascular damage/efferocytosis neighborhood that touches coagulation biology without testing TM itself. Both had zero focal DEGs. The corpus found Axl/Mertk shared absence rather than an active TAM transcriptional state in NeuN-positive neurons.

`Serpine2` is the main counterexample that prevents the rule "secreted protease-control gene equals zero" from being too absolute. It is a neuronal extracellular serpin and did have two focal FDR hits. But one was the target transcript itself, the other was `Clip2`, and represented thrombin/serpin/LRP1 comparators, including `F2`, `Serpini1`, and `Serpinb6a`, did not reproduce a shared protease-control signature. I therefore used `Serpine2` to set an upper bound of a very weak response, not as evidence that endothelial TM should have a multi-gene effect in this focal class.

## Target-specific prediction

### Thbd

`Thbd` encodes thrombomodulin/TM, an endothelial cell-surface type-I receptor that binds thrombin, diverts thrombin toward activation of protein C and thrombin-activatable fibrinolysis inhibitor, and contributes to endothelial quiescence and vascular anti-inflammatory biology. Those mechanisms are strong in vascular endothelial cells and plasma-protease contexts, not in recovered NeuN-positive thalamic glutamatergic nuclei.

The same-assay analogs are almost uniformly zero in `151 TH Prkcd Grin2c Glut`: `F2`, `Kdr`, `Flt4`, `Tek`, `Eng`, `Acvrl1`, `Sox17`, `Notch1`, `Notch2`, `Notch4`, `Axl`, and `Mertk` all had `n_degs = 0`. The only weakly positive extracellular/protease counterexample, `Serpine2`, had two focal calls and no shared F2/serpin phenocopy. Since Thbd is more endothelial and coagulation-surface restricted than Serpine2, and since this experiment enriched NeuN-positive nuclei and largely removed endothelial, microglial, vascular, and plasma inputs, the zero/nonzero decision is a zero.

I predict `Thbd` will have no focal genes at FDR 0.05:

| target_name | predicted_n_degs |
|---|---:|
| Thbd | 0 |

## Limits

This is still an extrapolation because `Thbd`, `Proc`, `Procr`, `Pros1`, `Gas6`, `Tyro3`, `F2r`, `Serpine1`, `Plat`, and `Plau` were not available as focal training perturbations. The directly observed analogs are vascular, coagulation, or TAM neighbors rather than same-complex TM loss.

The prediction is for sparse P16 CRISPR loss in recovered NeuN-positive neurons. It should not be read as evidence that thrombomodulin is irrelevant in brain endothelium, coagulation, BBB injury, inflammation, or systemic thrombin/protein C biology. The assay also lacks DNA-indel and protein readouts, so a null DEG count is an expected-response prediction, not a statement that guides would fail or that every edited neuron would be completely unaffected.
