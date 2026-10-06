# DEG-count prediction for `059_Dnm1l`

## Question and resolved ambiguities

The requested manifest contains one held-out perturbation, `Dnm1l`.  I interpreted the endpoint as the exact focal-cell count of measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`, using the same Wilcoxon/BH output as the supplied training parquet.  The count includes the perturbed target transcript if that transcript is itself significantly down-regulated; this is visible in the training set, where several one-DEG mitochondrial or autophagy perturbations have no downstream genes and the lone FDR hit is the target itself.

The key ambiguity is whether Drp1/Dnm1l should be treated like a severe loss of mitochondrial fission from conditional knockout literature, or like a partial P16 AAV CRISPR lesion in sparse postmitotic neurons.  I resolved that in favor of the screen context: strong whole-animal or complete conditional Drp1 phenotypes establish that `Dnm1l` is biologically central, but the prediction must be calibrated to a 3 to 4 week mosaic neuronal snRNA-seq readout with modest average target-RNA loss.

## Sources

- Input held-out manifest: `059_Dnm1l.csv`.
- Input focal training endpoint: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Input DE parquet: `training_de_all_cell_groups.parquet`.
- Same-experiment Distributed Agents corpus, release `perturbai-july-260713-sourceguard-1773-v1`, especially the perturbation findings and synthesized claims for `Mff`, `Opa1`, `Dnm1`, and `Gdap1`.
- Run-local Distributed Agents profile comparison over the focal-cell log-fold-change profiles for a declared mitochondrial/vesicle cohort.
- Mechanistic literature from PubMed:
  - Loson et al. 2013, PMID 23283981, DOI `10.1091/mbc.E12-10-0721`.
  - Palmer et al. 2013, PMID 23921378, DOI `10.1074/jbc.M113.479873`.
  - Osellame et al. 2016, PMID 27076521, DOI `10.1242/jcs.185165`.
  - Berthet et al. 2014, PMID 25339743, DOI `10.1523/JNEUROSCI.0930-14.2014`.
  - Oettinghaus et al. 2015, PMID 25909888, DOI `10.1038/cdd.2015.39`.
  - Yamada et al. 2016, PMID 27640145, DOI `10.1016/j.ajpath.2016.06.025`.
  - Manczak et al. 2012, PMID 22387883, DOI `10.1016/j.bbadis.2012.02.017`.

## Computation over the supplied assay data

I first checked the requested-target CSV and confirmed that `Dnm1l` is the only requested target.  The focal training endpoint has 1,674 non-held-out perturbations; 1,205 of them have zero FDR 0.05 DEGs, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and only a small upper tail is broad.  The top broad focal perturbations were core RNA-processing, proteasome, ubiquitin-like, and transcriptional regulators such as `Uba5` with 2,677 DEGs, `Tpr` with 1,768, `Sin3a` with 1,433, `Rnpc3` with 868, and `Psmb4` with 742.

The parquet has 616,253,184 rows, sorted by `group_name`, so I projected only the focal cell group and a hand-declared cohort of mitochondrial fission, mitochondrial stress, mitophagy/autophagy, and vesicle/endolysosomal comparators:

```python
dataset = ds.dataset(training_de_parquet, format="parquet")
flt = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(candidate_targets)
)
table = dataset.to_table(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj",
        "scores", "n_pert_matched", "n_ctrl_matched",
    ],
    filter=flt,
)
```

I then counted `pvals_adj < 0.05` inside those focal profiles and inspected the FDR hits.  The most relevant focal counts were:

| training target | focal `n_degs` | focal expression-pattern evidence |
| --- | ---: | --- |
| `Mff` | 0 | No FDR genes; `Mff` itself had logFC -0.200 and adjusted P = 1. |
| `Gdap1` | 0 | No FDR genes; no shared fission/Caytaxin module in the corpus. |
| `Dnm1` | 1 | The only hit was `Dnm1` itself; this dynamin-family vesicle-scission perturbation had no downstream focal program. |
| `Rhot1` | 0 | No FDR genes, despite being mitochondrial-transport related. |
| `Opa1` | 37 | Clear but modest ATF4/amino-acid stress program: `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Mthfd2`, `Slc7a5`, plus `Opa1` self. |
| `Yme1l1` | 0 | No FDR genes; a direct OPA1-processing comparator that did not copy `Opa1`. |
| `Afg3l2` | 0 | No FDR genes; another OPA1-processing/protease comparator. |
| `Clpp`/`Clpx` | 0/0 | No focal FDR genes for the mitochondrial ClpXP branch. |
| `Slc25a46` | 1 | Self only; close mitochondrial morphology/carrier relatives were nearly null. |
| `Slc25a4` | 1 | Self only, despite strong self down-regulation. |
| `Ndufs2`, `Sod2`, `Ndufa4`, `Ndufb8`, `Sucla2`, `Isca2` | 1 each | Self-only OXPHOS or mitochondrial-metabolism examples, not Opa1-like stress. |
| `Atg5`, `Becn1`, `Atg16l1` | 0 | Core autophagy nodes did not make a focal nuclear program. |
| `Map1lc3a`, `Sqstm1`, `Park7` | 1 each | Self-only or near-self-only autophagy/mitochondrial quality-control counterexamples. |
| `Vps35`, `Vps54`, `Rab7` | 17, 31, 501 | Endosomal/lysosomal positives, but their signatures are not Drp1 fission signatures. |

The run-local profile comparison over these focal logFC vectors confirmed the same negative structure: `Dnm1`, `Mff`, and `Gdap1` had 1, 0, and 0 FDR hits, and none shared an FDR-level positive or negative intersection with the 37-gene `Opa1` response.  Apparent full-profile correlations were dominated by non-significant logFC tails, so I used the profile inspection as a rejection of a hidden shared FDR module rather than as a predictor by itself.

## Same-experiment corpus evidence

`Dnm1l` was absent from the Distributed Agents same-experiment corpus, matching its held-out status, so the corpus evidence had to come from represented neighbors.

The strongest direct comparator was `Mff`.  MFF is a Drp1 outer-mitochondrial-membrane receptor/adaptor, so it is mechanistically on the fission axis.  In the focal training endpoint `Mff` had zero DEGs.  The Distributed Agents `Mff:F001` finding reported no downstream FDR 0.10 response in any of 22 recovered neuronal groups, and `Mff:F002` explicitly contrasted `Mff` with `Opa1`: `Opa1` induced recurrent `Asns`, `Slc7a5`, `Chac1`, `Shmt2`, `Mars1`, `Ddit3`, `Aldh1l2`, and `Cars`, whereas the same program had no `Mff` FDR support.  The synthesized high-confidence claim stated that `Opa1` activates a detectable ATF4/mitochondrial ISR-like amino-acid program but represented comparators, including `Mff`, `Gfm2`, `Coa8`, `Ndufs2`, `Sucla2`, `Isca2`, `Ndufv1`, `Sod2`, and `Ndufa4`, do not cross that threshold.

`Opa1` was useful as a positive counterexample, not as a direct phenocopy.  `Opa1:F001` to `Opa1:F004` in the corpus anchor a cell-class-selective Opa1 mitochondrial stress state with ATF4-like amino-acid and one-carbon genes and depletion of some mitochondrial genome-encoded respiratory-chain transcripts.  `Opa1:F006` is the critical boundary: `Yme1l1`, `Afg3l2`, `Mff`, and `Clpp` were measurable but flat or off-module, showing that even mitochondrial fusion, fission, and OPA1-processing perturbations were not interchangeable in this snRNA-seq assay.

`Gdap1` was an additional fission/trafficking disease comparator.  It had no focal DEGs, and the corpus finding `Gdap1:F004` reported that represented fission and Caytaxin comparators, `Mff` and `Atcay`, did not form a GDAP1-like nuclear module.  This again argued against projecting a generic mitochondrial-morphology response onto every node in the fission neighborhood.

`Dnm1` was a weak mechanistic analog because it is a synaptic-vesicle dynamin rather than a mitochondrial Drp1 effector, but it calibrated the readout for dynamin-family membrane-scission proteins.  Its one focal hit was the `Dnm1` transcript itself, and the corpus reported a pervasive downstream-zero pattern across measured neuronal groups despite target-transcript engagement.

## External biology and how it changes the estimate

Dnm1l encodes Drp1, the central cytosolic dynamin-related GTPase that executes mitochondrial and peroxisomal fission.  MFF, FIS1, MiD49/MIEF2, and MiD51/MIEF1 recruit and regulate Drp1; single-adaptor lesions can be partly redundant, whereas Drp1 removal is a core fission lesion.  Loson et al. 2013 showed that Fis1, Mff, MiD49, and MiD51 can recruit Drp1; Palmer et al. 2013 found that MiD49/51 can act independently of Mff and Fis1 for mitochondrial recruitment; Osellame et al. 2016 used edited adaptor-null cell lines to show cooperative and independent roles of Mff, MiD49, and MiD51.  This makes `Mff` an imperfect lower-bound analog for `Dnm1l`, because intact MiD49/MiD51 and other factors could buffer Mff loss more than Dnm1l loss.

Complete neuronal Drp1 loss can be severe.  Berthet et al. 2014 deleted Drp1 in midbrain dopamine neurons and found depletion of axonal mitochondria and nigrostriatal degeneration.  Oettinghaus et al. 2015 found that inducible adult-forebrain Drp1 ablation alters hippocampal mitochondrial morphology, synaptic transmission, and memory, although not enough for neuronal death within 10 weeks.  Yamada et al. 2016 linked Purkinje-cell Drp1 deficiency to mitochondrial elongation and later RIP3-mediated neurodegeneration.

Those complete-loss phenotypes argue against assuming that `Dnm1l` is biologically inert.  They do not, however, argue for hundreds of focal DEGs in this task.  Manczak et al. 2012 reported that heterozygous Drp1 knockout mice lacked overt synaptic or mitochondrial deficiencies, which is directionally consistent with a partial-reduction threshold.  The P16 AAV assay perturbs sparsely, reads nuclear RNA rather than mitochondrial morphology or axonal ATP, and has an average on-target mRNA decrease of only about 18% per gRNA.  In that setting, the within-dataset `Mff` zero, the many self-only OXPHOS/autophagy counts, and the Opa1/Mff uncoupling are stronger calibration evidence than complete conditional Drp1 deletion.

## Target-specific prediction

### `Dnm1l`

I predict that `Dnm1l` will sit just above the focal FDR floor, with the target transcript itself the most likely significant feature and no resolved ATF4/Opa1-like downstream program.  The count is therefore `1`.

The nonzero part comes from Dnm1l being a highly expressed, directly targeted core gene rather than from a confident downstream state; `Dnm1` and many mitochondrial structural genes in `151 TH Prkcd Grin2c Glut` had exactly one DEG because their own transcripts crossed FDR.  The decision not to assign a broad count is driven by the same-experiment `Mff = 0` fission receptor result, `Gdap1 = 0`, `Rhot1 = 0`, zero or self-only core autophagy and OXPHOS genes, and the Distributed Agents corpus conclusion that `Opa1` is a branch-specific mitochondrial ISR exception rather than a generic morphology/fission readout.

`Rab7`, `Vps35`, and `Vps54` were deliberately treated as counterexamples, not close positives.  They show that endolysosomal perturbations can be detected in this cell group, but their cholesterol/vacuolar/endosomal signatures are not mechanistic Drp1 fission states.  Likewise, `Opa1 = 37`, `Atp2a2 = 187`, `Elp1 = 645`, and `Elp2 = 150` show that this thalamic cell group can mount ATF4-like stress responses, but represented mitochondrial fission, OPA1-processing, ClpXP, OXPHOS, and autophagy targets usually did not enter that state.

## Limits and uncertainty

- `Dnm1l` itself was held out from the parquet and from the corpus, so there was no same-experiment signature for the exact perturbation.
- `Mff` is a mechanistically close adaptor but not a full Drp1 phenocopy; Dnm1l loss should be less redundant than Mff loss.
- The endpoint is FDR-count breadth, not mitochondrial morphology, axonal organelle distribution, respiration, mitophagic flux, cell viability, or seizure/circuit physiology.  Complete Drp1 knockout phenotypes can be profound while nuclear DEG counts remain small.
- The prediction of one rather than zero is mostly extrapolation about target-transcript detectability.  Training targets with similar biology span both self-only and zero outcomes depending on guide efficacy, transcript abundance, and recovered perturbed-cell count.
- A rare Dnm1l-specific stress response, especially one independent of Opa1/ATF4 genes or delayed beyond the P37-P44 harvest, would not be anticipated from the represented training comparators.

Final point prediction:

```tsv
target_name	predicted_n_degs
Dnm1l	1
```
