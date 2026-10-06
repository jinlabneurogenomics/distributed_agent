# Question interpreted

The requested endpoint is a held-out point prediction for `Hspd1`: the number of
measured genes with `pvals_adj < 0.05` after CRISPR loss of function in
`151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.  I treated the
training CSV as the direct scalar endpoint for non-held-out perturbations and
the Parquet as the direct per-gene expression signatures underlying those
counts.  `Hspd1` itself is held out from both inputs, so there is no direct
`Hspd1` perturbation expression vector to score.

The main ambiguity was how much to extrapolate from HSPD1's strong essential
mitochondrial chaperonin biology.  I did not read weak target-RNA knockdown as
failed editing, and I did not assume that a severe unsampled effect would
necessarily appear as many DEGs among recovered single nuclei.  The predicted
count below is therefore an assay-specific FDR DEG count, not a prediction of
whether HSPD1 is biologically important.

# Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression Parquet:
  `training differential-expression dataset`.
- Requested held-out list:
  `single-target request for Hspd1`.
- Run-local metadata:
  `task_bindings.json`, `coverage.json`, `measurement_registry.json`, and
  `capabilities.json`.
- Internal same-experiment semantic source:
  PerturbAI July release
  `perturbai-july-260713-sourceguard-1773-v1`, via bounded `corpus.findings`
  inventory.  I used these Findings only as structured interpretations of the
  same experiment, not as independent replication.
- External mechanism priors:
  PubMed-indexed HSPD1/HSP60 literature and standard Gene Ontology/UniProtKB
  functional assignments for HSPD1 as the mitochondrial matrix HSP60
  chaperonin.

The relevant external papers were Bie et al. 2020
(`Cell Stress & Chaperones`, DOI `10.1007/s12192-020-01080-6`, PMID
`32060690`), showing that human HSP60/HSP10 interacts with a broad set of
mitochondrial matrix clients; Böttinger et al. 2015 (`JBC`, DOI
`10.1074/jbc.M115.642017`, PMID `25792736`), supporting the Hsp60/Hsp10
chaperonin's role downstream of mitochondrial Hsp70 in matrix protein folding;
Christensen et al. 2010 (`Cell Stress & Chaperones`, DOI
`10.1007/s12192-010-0194-x`, PMID `20393889`), showing that complete mouse
`Hspd1` inactivation is embryonic-lethal while heterozygous reduction is
tolerated to postnatal life; Hansen et al. 2002 (`AJHG`, DOI
`10.1086/339935`, PMID `11898127`), linking HSP60/HSPD1 dysfunction to SPG13;
and Wang et al. 2019 (`Scientific Reports`, DOI
`10.1038/s41598-019-48762-5`, PMID `31444388`), showing that SPG13/MitCHAP-60
HSP60 mutants impair folding of mitochondrial substrates including ATP synthase
beta.

# Computation over the declared inputs

The held-out manifest contained exactly one target, `Hspd1`.  The focal
training table contained 1,674 visible targets and was highly zero-inflated:
median `n_degs = 0`, 75th percentile `= 1`, 90th percentile `= 2`, 95th
percentile `= 18`, 99th percentile `= 436.5`, and maximum `= 2677`.

I then selected biologically plausible HSPD1 comparators from the training
counts and extracted their exact `151 TH Prkcd Grin2c Glut` Parquet rows with
an exact filter on `group_name` and `gene_target`.  The core query was:

```python
dset.to_table(
    columns=["names", "scores", "logfoldchanges", "pvals", "pvals_adj",
             "gene_target", "n_pert_matched", "n_ctrl_matched"],
    filter=(ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
           & ds.field("gene_target").isin(comparator_targets),
)
```

The closest comparators available in the training endpoint had the following
focal DEG counts:

| comparator class | training target | observed `n_degs` in `151` | expression-pattern evidence |
|---|---:|---:|---|
| mitochondrial matrix ClpXP protease | `Clpp` | 0 | no FDR-significant genes; best adjusted p value 0.723 |
| mitochondrial matrix ClpXP protease ATPase | `Clpx` | 0 | no FDR-significant genes; best adjusted p value 0.540 |
| mitochondrial protease / matrix quality control | `Lonp1` | 0 | no FDR-significant genes; best adjusted p value 0.507 |
| inner-membrane AAA protease | `Yme1l1` | 0 | no FDR-significant genes; all adjusted p values 1.0 |
| inner-membrane AAA protease | `Afg3l2` | 0 | no FDR-significant genes; weak self-target trend only, `Afg3l2` logFC -0.307, adjusted p 0.912 |
| mitochondrial import-associated J protein | `Dnajc19` | 0 | no FDR-significant genes; all adjusted p values 1.0 |
| mitochondrial outer-membrane import pore | `Tomm40` | 1 | the only FDR hit was `Tomm40` itself, logFC -0.923, adjusted p `5.46e-7` |
| complex II / complex III / complex IV subunits | `Sdha`, `Uqcrc2`, `Cox5a` | 1, 1, 1 | each only passed on its own target transcript |
| complex I subunits and assembly factors | 23 `Nduf*` targets | 0 or 1 | almost all had no downstream FDR response |
| mitochondrial fusion and cristae maintenance | `Opa1` | 37 | a real but modest ATF4/ISR-like signature: `Asns`, `Mars1`, `Chac1`, `Ddit3`, and one-carbon/aminoacyl-tRNA genes |
| ER Hsp70 | `Hspa5` | 5 | ER-UPR/ERAD hits including `Hsp90b1`, `Nfe2l1`, `Pdia4`, `Derl3`; not an HSPD1-localized matrix stress signature |
| cytosolic constitutive Hsp70 | `Hspa8` | 9 | compensatory cytosolic HSP module with `Dnaja1`, `Hspa4l`, `Hsp90aa1`, `Cct6a` |
| heat-shock transcription factor | `Hsf1` | 6 | small loss of basal HSP90/HSP110 co-chaperone transcripts, with `Hsph1`, `Hsp90aa1`, `Hsp90ab1`, `Ahsa2` down |
| proteasome stress comparators | `Psmc1`, `Psmb4` | 430, 742 | broad signatures in `151`; useful counterexamples because they induced far larger survivor-state programs than any measured mitochondrial chaperone/protease comparator |

The same-experiment PerturbAI July Finding summaries agreed with the raw
Parquet at the level relevant for prediction: `Clpp` loss was globally buffered
and not a generic ClpXP-complex signature; `Afg3l2`, `Yme1l1`, `Clpx`, and
`Lonp1` were sparse and did not converge on a shared acute mitochondrial
proteotoxicity program; `Hsf1` loss was a small basal HSP90/HSP110 module rather
than a broad proteotoxic-stress, UPR, ISR, redox, or mitochondrial-stress
program; `Hspa8` only partially anti-phenocopied `Hsf1`; `Hspa5` recruited a
separable ER folding/ERAD signature in `151`; and `Opa1` produced an
ATF4/ISR-like amino-acid stress signature that explicitly did not include a
canonical `Hspd1`/`Hspe1`/`Clpp` mitochondrial UPR.

# Target-specific reasoning

## Hspd1

`Hspd1` encodes HSP60, the main mitochondrial matrix chaperonin subunit that
works with HSP10/HSPE1 to fold imported matrix proteins.  It is therefore
biologically closer to a mitochondrial protein-quality-control perturbation
than to cytosolic `Hspa8`, ER-resident `Hspa5`, `Hsf1`, or proteasome-subunit
perturbations.  Complete HSPD1/HSP60 loss is not expected to be benign:
human HSP60/HSP10 binds many mitochondrial matrix clients, disease mutations
reduce chaperonin activity, and homozygous mouse `Hspd1` inactivation is
embryonic-lethal.

The causal model for transferring those facts into this experiment was:
acute AAV CRISPR disruption of `Hspd1` in postmitotic neurons should reduce
functional HSP60 in the mitochondrial matrix; this can compromise matrix
client folding and respiratory protein biogenesis; sufficiently stressed cells
could activate mitochondrial proteostasis, ISR/ATF4, oxidative-stress, or
mitophagy programs, and severely affected cells could also be depleted before
snRNA-seq; the requested endpoint only counts FDR-significant nuclear-RNA
changes in recovered, class-assigned `151` nuclei 3-4 weeks after P16 editing.

The relevant training perturbations mostly argue against a broad recovered-cell
signature for direct HSPD1 loss under this assay.  `Clpp`, `Clpx`, `Lonp1`,
`Yme1l1`, `Afg3l2`, and `Dnajc19` are not HSPD1 paralogs or obligate partners,
but they are in the same mitochondrial matrix/import/proteostasis layer and
all had `0` focal DEGs despite similar or larger matched perturbed-cell counts
than many positive controls.  `Sdha`, `Uqcrc2`, `Cox5a`, `Tomm40`, and many
`Nduf*` perturbations gave only `0`- or `1`-gene footprints; where nonzero,
the significant row was the targeted mitochondrial transcript itself rather
than downstream activation of an HSP60-like UPR.  `Opa1` is the mitochondrial
counterexample with 37 DEGs and clear `Asns`/`Chac1`/`Ddit3` ISR induction, but
OPA1 loss changes cristae structure and respiratory compensation rather than
selectively perturbing matrix chaperonin folding, and the same-experiment
Finding layer explicitly reported that Opa1 did not induce a canonical
`Hspd1`/`Hspe1`/`Clpp` mitochondrial UPR transcriptome.

The heat-shock and ER chaperone comparators set an upper bound rather than a
direct analog.  `Hspa8` had a 9-gene compensatory cytosolic HSP program,
`Hspa5` had a 5-gene ER folding/ERAD program at FDR 0.05 in the raw focal
Parquet, and `Hsf1` had 6 DEGs with loss of HSP90/HSP110 co-chaperone
transcripts.  Those perturbations show that chaperone disruption can be visible
in `151`, but their localization and transcriptional control differ from HSPD1.
The two strong proteostasis counterexamples, `Psmb4` and `Psmc1`, reached
hundreds of DEGs; I rejected them as quantitative analogs because proteasome
loss created a much broader neuron state than any measured mitochondrial
quality-control or chaperone perturbation.

Putting those pieces together, I predict a near-null focal signature.  I made
the point estimate nonzero because `Hspd1` is a highly used core matrix folding
factor and direct targeting could plausibly make its own transcript pass FDR,
as happened for `Tomm40`, `Cox5a`, `Sdha`, `Uqcrc2`, and `Hsp90ab1`.
However, the closest available mitochondrial quality-control perturbations do
not support a multi-gene response in this recovered-neuron DEG endpoint.

Prediction: `Hspd1 -> 1` DEG.

# Limits

`Hspe1`, `Hspa9`, and `Trap1` would have been more direct mitochondrial
chaperone comparators, but they were absent from the focal training-count
table.  The prediction therefore extrapolates from second-neighborhood
mitochondrial proteases, import/OXPHOS genes, and stress-response chaperones.
Those are mechanistically informative but imperfect: loss of HSP60 can impair
many matrix clients at once, while loss of `Clpp` or `Lonp1` changes protein
turnover rather than folding.  The Parquet contains differential expression
only, not raw guide exposure, mitochondrial function, protein abundance, or
pre-assay loss of edited neurons, so a flat survivor transcriptome would not
exclude a severe earlier mitochondrial defect.  Finally, all internal corpus
Findings are interpretations of the same Perturb-seq experiment used to make
the Parquet; they clarify analog signatures but are not independent biological
replicates.
