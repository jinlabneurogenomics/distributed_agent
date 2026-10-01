# Psmc5 DEG-count prediction

## Question and resolved ambiguities

The requested endpoint is a point prediction of `n_degs` for each held-out
perturbation in `151 TH Prkcd Grin2c Glut` cells. I interpreted `n_degs` exactly
as the number of measured genes with `pvals_adj < 0.05` in the focal-cell
Wilcoxon differential-expression table, with `logfoldchanges` oriented as
perturbed over matched non-targeting control.

There is one requested held-out target:

| target | endpoint status in supplied files |
|---|---|
| `Psmc5` | absent from both the training focal-cell DEG counts and the declared all-cell DE parquet |

The held-out `Psmc5` endpoint is therefore absent from the declared inputs. The
training counts for `Psmc1` and `Psmb4`, together with their raw focal-cell
signatures, are direct observations for two non-held-out core proteasome
perturbations; they are same-assay mechanistic proxies for a third core 26S
proteasome subunit rather than an exact observation of `Psmc5`.

## Sources used

- Declared focal training endpoint:
  `/gpfs/group/jin/asun/bioagents/debug/260901_predict/holdout_task/Inputs/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared DE parquet:
  `/gpfs/group/jin/asun/bioagents/debug/260901_predict/holdout_task/Inputs/training_de_all_cell_groups.parquet`.
- Requested-target manifest:
  `/gpfs/group/jin/asun/bioagents/runs/holdout-prediction/july-260713-adaptive-seed-260901/prepared/manifests/deg-count/bs001/b0261.csv`.
- Run-local measurement registry and task bindings in `codex_runtime/pipeline`.
- Same-experiment interpretation from the internal `perturbai-july-260713-sourceguard-1773-v1`
  corpus: `Psmc1` and `Psmb4` Finding records plus the bounded
  `corpus.direct_evidence` index in `codex_runtime/pipeline/direct_evidence_psm.json`.
  This corpus is another representation of the PerturbAI experiment, so I used
  it only to interpret the visible training perturbations, not as independent
  replication.
- External literature from PubMed:
  - Glickman et al. 1998, DOI `10.1128/MCB.18.6.3149`, PMID `9584156`.
  - Bedford et al. 2008, DOI `10.1523/JNEUROSCI.2218-08.2008`, PMID `18701681`.
  - Ehlinger et al. 2013, DOI `10.1016/j.str.2013.02.021`, PMID `23562395`.
  - Sokolova et al. 2015, DOI `10.1038/srep14909`, PMID `26449534`.
  - Lu et al. 2017, DOI `10.1016/j.molcel.2017.06.007`, PMID `28689658`.
  - Yu et al. 2024, DOI `10.1093/hmg/ddae085`, PMID `38776958`.
  - Hatanaka et al. 2023, DOI `10.1038/s41598-023-41492-9`, PMID `37658135`.

I did not inspect a same-experiment `Psmc5` report or `Psmc5` Finding records.
The internal corpus could otherwise expose held-out same-assay evidence.

## Dataset calibration

The focal training CSV has 1,674 non-held-out targets. Its distribution is very
sparse: 1,205 targets have zero DEGs, the median is 0, the 75th percentile is 1,
the 90th percentile is 2, the 95th percentile is 18, and the maximum is 2,677.
Thus any count in the hundreds is an outlying broad transcriptional response in
this assay.

Only two core proteasome-subunit perturbations with `Psm*` symbols are present
in the focal training endpoint:

| training perturbation | observed focal `n_degs` | recovered focal perturbed nuclei | relationship to `Psmc5` |
|---|---:|---:|---|
| `Psmc1` | 430 | 89 | 19S regulatory-particle AAA-ATPase, same 26S ATPase ring as PSMC5/RPT6 |
| `Psmb4` | 742 | 62 | 20S beta-core structural subunit, same 26S proteasome holoenzyme |

The focal raw DE table has 17,259 measured genes for each of these two
perturbations. I compared their complete focal signatures by joining on
measured-gene name and correlating both `logfoldchanges` and signed Wilcoxon
`scores`. The two signatures had Pearson `r = 0.611` for log-fold changes and
`r = 0.652` for scores. At FDR 0.05, 215 genes were significant for both, 957
were significant in either perturbation, and all 215 shared significant genes
had the same sign. The shared response contained the expected induced
proteasome feedback genes, for example `Psmc3`, `Psmc4`, `Psmc6`, `Psmd1`,
`Psmd2`, `Psmd4`, and `Psma1`, induced autophagy/stress genes such as `Sqstm1`
and `Ddit3`, and reduced neuronal function genes such as `Atp1a3` and `Gria2`.

The internal July corpus independently summarized the same training
perturbations as follows:

- `Psmc1`: the perturbation induced a proteasome/ubiquitin bounce-back module,
  endolysosomal/autophagy transcripts, heat-shock and integrated-stress
  genes, and p53/apoptosis-risk and synaptic-withdrawal arms. `Psmb4` was its
  only strong positive signature neighbor among assayed constitutive proteasome
  subunits.
- `Psmb4`: the perturbation induced other 20S, 19S, and regulatory `Psm`
  genes; its top data-driven neighbor was `Psmc1`, with same-sign agreement for
  nearly every shared significant feature in the broader FDR 0.10 comparison.

Those corpus records also flagged useful counterexamples. Accessory or
downstream proteostasis genes did not phenocopy the direct 26S subunit lesion in
the focal endpoint: `Nfe2l1` had 0 DEGs, `Vcp` had 2, `Uchl1` had 1, `Sqstm1`
had 1, `Atf6` had 0, `Nfe2l2` had 0, and `Ube3a` had 0. Some unrelated
high-burden perturbations converged on a terminal distress module, including
`Tpr` with 1,768 DEGs, `U2af2` with 828, and `Prpf6` with 454, but the corpus
reported that their overlap with `Psmb4`/`Psmc1` was smaller and not rooted in a
same-complex proteasome defect. I therefore treated direct impairment of the
26S particle, not generic stress or broad ubiquitin-pathway membership, as the
transfer basis for `Psmc5`.

## Target-specific reasoning

### Psmc5

`Psmc5` encodes PSMC5/RPT6, one of the six AAA-ATPases in the base of the 19S
regulatory particle of the 26S proteasome. The intervention in this experiment
would be acute mosaic CRISPR loss of `Psmc5` in postmitotic neurons. Its direct
molecular consequence should be impaired RPT6 dosage or structure in the
heterohexameric regulatory-particle ATPase ring, leading to defective
regulatory-particle assembly or 19S-to-20S engagement and reduced unfolding and
translocation of ubiquitylated substrates into the 20S proteolytic core.
Glickman et al. established that RPT1-RPT6 are the six ATPases of the proteasome
regulatory particle, Ehlinger et al. described RPT6 conformational dynamics
needed for holoenzyme formation, Sokolova et al. showed that the RPT6 tail
contributes to regulatory-particle assembly and 20S gate activation, and Lu et
al. structurally analyzed mammalian p28-bound regulatory-particle assembly.
More directly for gene function, Yu et al. found that human PSMC5 insufficiency
or the recurrent P320R variant impairs proteasome function and, for P320R,
weakens 19S-20S association.

The propagation expected after acute `Psmc5` loss is therefore the same as after
`Psmc1` or `Psmb4`: reduced 26S flux, accumulation of proteotoxic stress,
NFE2L1/NRF1 proteasome bounce-back, recruitment of autophagy and lysosomal
clearance, heat-shock and integrated-stress signaling, and depressed mature
neuronal transcripts in neurons that remain recovered at P37-P44. Hatanaka et
al. support the NRF1 link by showing NRF1-dependent induction of aggrephagy
genes after proteasome dysfunction. Bedford et al. showed that neuronal `Psmc1`
inactivation depletes 26S proteasomes and is sufficient to cause
neurodegeneration, consistent with loss of an ATPase-ring subunit being
endpoint-bearing for neuronal proteostasis rather than a benign complex
component.

The two relevant training perturbations both predict a nonzero, high DEG count.
`Psmc1` is the closer analog because it is another 19S ATPase in the same
obligate ring; `Psmb4` perturbs the 20S core but gave a somewhat larger
same-direction focal response. Both are imperfect quantitative anchors because
`Psmc5` has no measured focal cell recovery, no measured signature, and no
guide-efficiency estimate in the held-out inputs. `Psmb4` had fewer recovered
focal nuclei than `Psmc1` but more DEGs, so sampling depth alone does not fix
the expected count. Conversely, the silent `Nfe2l1`, `Vcp`, `Uchl1`, and
`Sqstm1` perturbations argue against assigning every proteostasis-related gene
a large value; they do not undermine `Psmc5`, because PSMC5 is a structural 26S
ATPase, not an upstream sensor or an accessory branch component.

I set `Psmc5` below `Psmb4` and slightly above `Psmc1`: below `Psmb4` because
the closer same-subcomplex anchor is the 430-DEG `Psmc1` perturbation, and
above `Psmc1` because RPT6 has documented roles in both ATPase-ring assembly
and 19S-20S engagement and because the two measured structural perturbations
span a broad 430-742 range even in the same cell group. The final point
prediction is therefore 520 DEGs.

## Limits

The prediction is an extrapolation from two measured structural proteasome
subunits. The training table contains no `Psmc5`, no other `Psmc2`-`Psmc6`
ATPase perturbation, and no `Psma` or `Psmd` target that could define a tighter
ATPase-ring dose-response. The same-experiment corpus is an interpretation of
the same raw screen, so it confirms pattern identity and counterexamples but
does not supply independent replication. External studies use yeast, human
cells, conditional mouse knockouts, or human heterozygous variants rather than
the exact P16 AAV mosaic CRISPR neuron assay. Finally, `n_degs` is
power-dependent and survivor-conditioned; a severe `Psmc5` perturbation could
drop edited neurons before snRNA-seq or recover fewer nuclei, and either effect
would change the number of genes passing BH FDR 0.05 without changing the
underlying causal expectation that `Psmc5` loss impairs the 26S proteasome.
