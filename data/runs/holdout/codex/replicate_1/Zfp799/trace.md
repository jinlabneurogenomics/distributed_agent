Direct prediction for `Zfp799` in `151 TH Prkcd Grin2c Glut`
================================================================

Endpoint
--------

`n_degs` is the count of measured genes in `151 TH Prkcd Grin2c Glut` with
BH-adjusted Wilcoxon `p < 0.05`.

Evidence used
-------------

- The declared manifest target is `Zfp799`; `Zfp799` is absent from the
  declared training count table and from the declared training DE parquet, so
  the forecast used only training perturbations.
- The target biology bundle gives strong focal reach: in non-target 151
  thalamic cells, `Zfp799` is available as a feature, is detected in 19,788 of
  23,679 nuclei, and has 83.57% cells expressing with mean raw UMI 2.13. That
  argues against a prediction of zero because the target is simply absent from
  the assayed thalamic population.
- The same bundle gives only a generic molecular-operation prior. `Zfp799` is
  annotated as a nuclear KRAB/C2H2 zinc-finger protein predicted to regulate
  RNA polymerase II transcription. The edited protein stock is expected to
  substantially decline over the 21-28 day P16-to-P37/P44 interval, but the
  evidence is sparse; no target-specific postnatal neural loss phenotype,
  same-context redundancy test, or ZFP799-specific protein-persistence datum
  was found.
- The focal training count table is extremely zero-inflated: 1,205/1,674
  training targets have 0 significant genes; 1,542/1,674 have fewer than 5;
  and 1,568/1,674 have fewer than 10. The median focal count is 0.
- Nearby name/family training targets were quieter than the all-target mean.
  Among 29 actual `Zfp[0-9]` training perturbations, 24 had 0 focal DEGs and
  only five were nonzero: `Zfp612` 1, `Zfp692` 1, `Zfp148` 8, `Zfp236` 19, and
  `Zfp423` 150. `Zkscan1`, `Zkscan16`, and `Zscan26` were all zero.
- Row-level checks in the declared parquet confirmed that those zeros were
  measured 151 profiles rather than missing rows: for example, `Zfp1`,
  `Zfp521`, `Zkscan1`, `Zkscan16`, and `Zscan26` each had 17,259 focal
  measured-gene rows and 180-247 matched perturbed nuclei.
- The one sizeable `Zfp` outlier, `Zfp423`, was not used as a scale template
  for `Zfp799`. Same-experiment Findings describe the `Zfp423` response as a
  specific thalamic/cerebellar program and report that obvious `Zfp423`
  relatives and partner pathways, including `Zfp521`, EBF, BMP-SMAD,
  retinoic-acid receptor, and Zic perturbations, did not phenocopy the matched
  `Zfp423` state. That makes a generic C2H2 zinc-finger average too high for
  an uncharacterized KRAB-family target.

Synthesis
---------

`Zfp799` is expressed well enough that an effect is reachable, and a disruptive
edit should eventually reduce new ZFP799 supply. However, its prior evidence is
limited to predicted KRAB/C2H2 transcriptional regulation without a documented
postnatal thalamic requirement, while the matched training surface shows that
most `Zfp` and `Zscan`-like perturbations are exact or near nulls in 151 TH
Prkcd Grin2c Glut. The best point forecast is therefore at the family/local
mode rather than at the sparse long tail.

Predicted `n_degs`: 0
