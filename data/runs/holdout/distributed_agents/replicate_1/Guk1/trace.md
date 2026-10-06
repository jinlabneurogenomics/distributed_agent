# DEG-count prediction trace

## Question and endpoint

I treated the task as a scalar prediction for one held-out perturbation,
`Guk1`, in the focal cell group `151 TH Prkcd Grin2c Glut`. The value to
predict is the number of measured transcripts with BH-adjusted Wilcoxon
`pvals_adj < 0.05` after the `Guk1` CRISPR perturbation in that cell group.
`Guk1` was held out completely, so neither its focal DEG count nor any of its
per-gene differential-expression rows were available in the supplied inputs.

I interpreted zero as "no downstream or self transcript is expected to pass the
0.05 adjusted-P threshold in this exact assay"; it is not a claim that GUK1 is
biologically irrelevant or that CRISPR editing fails.

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared per-gene DE table:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Guk1`.
- Internal PerturbAI July 260713 `sourceguard_1773_v1` Findings/Reports/Evidence
  corpus for same-experiment summaries around training perturbations `Adk`,
  `Nt5c2`, and `Lyrm4`.
- External references used only for gene function:
  Sekulic et al. 2002, J. Biol. Chem., DOI `10.1074/jbc.M204668200`, for the
  mouse guanylate kinase reaction `GMP + ATP <=> GDP + ADP`; Wang et al. 2025,
  Nat. Commun., DOI `10.1038/s41467-025-61732-y`, for human GUK1/GMPK as the
  sole GDP-producing guanylate kinase; Hidalgo-Gutierrez et al. 2024,
  Ann. Neurol., DOI `10.1002/ana.27071`, PMID `39230499`, for human GUK1
  deficiency causing unbalanced mitochondrial dNTP pools and mitochondrial DNA
  depletion/deletions; Duarte et al. 2019, Biol. Psychiatry, DOI
  `10.1016/j.biopsych.2019.03.977`, PMID `31097295`, for NT5C2 knockdown
  affecting AMPK/protein-translation biology in human neural progenitors;
  Kviklyte et al. 2017, Am. J. Physiol. Endocrinol. Metab., DOI
  `10.1152/ajpendo.00304.2016`, PMID `28325731`, as a differentiated mouse
  tissue counterexample where Nt5c2 deletion did not potentiate AMP/ADP or
  AMPK activation; and Weltha et al. 2018, Brain Res. Bull., DOI
  `10.1016/j.brainresbull.2018.11.008`, PMID `30468847`, for ADK as a
  purine/adenosine enzyme whose disease biology is dominated by adenosine
  tone, astrocytes, and methylation rather than a simple neuronal RNA stress
  state.

## Computation over the declared data

1. I read the requested-target CSV and found exactly one row, `Guk1`.

2. I summarized the focal training counts. Among 1,674 non-held-out biological
   perturbations, 1,205 had `n_degs = 0`; the median was 0, the 75th percentile
   was 1, the 95th percentile was 18, and the mean was inflated to 14.05 by a
   long right tail. The endpoint is therefore highly sparse in this cell group.

3. I searched the training target names for direct guanine/purine/nucleotide
   candidates. The useful represented nodes were sparse: the direct purine
   enzymes `Adk` and `Nt5c2`, and the more distant mitochondrial nucleotide
   transporters `Slc25a4` and `Slc25a36`. Direct GMP branch genes such as
   `Gmps`, `Gmpr`, `Gmpr2`, `Impdh1`, `Impdh2`, `Hprt`, `Ppat`, `Gart`,
   `Paics`, `Adsl`, `Adssl1`, `Dguok`, `Tk2`, `Rrm1`, `Rrm2`, and `Rrm2b`
   were absent as training perturbations.

4. I then queried the raw focal parquet rows for the direct analogs:

   - `Adk`: `n_degs = 0`; 186 perturbed nuclei versus 23,679 controls; minimum
     focal `pvals_adj = 0.202556`.
   - `Nt5c2`: `n_degs = 0`; 205 perturbed nuclei versus 23,679 controls;
     minimum focal `pvals_adj = 1.0`.
   - `Lyrm4`: `n_degs = 0`; 90 perturbed nuclei versus 23,679 controls;
     minimum focal `pvals_adj = 0.650782`. This is not a purine enzyme, but in
     the corpus its one non-focal hit was `Gmpr` up-regulation, so I used it as
     a weak falsifier for a hidden GMP-interconversion response.
   - `Slc25a36`: `n_degs = 0`; 150 perturbed nuclei; every focal adjusted
     P value was 1.0.
   - `Slc25a4`: `n_degs = 1`; 240 perturbed nuclei; the only focal DEG was the
     `Slc25a4` self transcript, log2FC -0.778, adjusted P `7.59e-13`. No
     non-self transcript passed FDR.

5. I also asked whether measured `Guk1` was a recurrent downstream marker in
   the training DE table. `Guk1` appeared at FDR<0.05 in only 6 target x cell
   rows across 23 cell groups: after broad stress or proteostasis/chromatin
   perturbations such as `Psmb4`, `Uba5`, and `Tpr`, including two focal hits
   after `Uba5` and `Tpr`. I treated this as evidence that `Guk1` can be a
   secondary marker in very large expression programs, not as evidence that
   knocking out `Guk1` itself should produce such a program.

## Target-specific prediction

### Guk1

**Prediction: 0 DEGs.**

**Biological role.** `Guk1` encodes mammalian guanylate kinase, the enzyme that
phosphorylates GMP to GDP using ATP. The long and short GUK1 isoforms can feed
mitochondrial and cytosolic guanine nucleotide pools; severe biallelic human
GUK1 deficiency can unbalance dNTP pools and cause mitochondrial DNA depletion
and deletions. That makes `Guk1` a real nucleotide-metabolism gene, but the
expected first consequence of a partial, postmitotic, sparse perturbation is a
metabolite imbalance, not an obligate immediate transcription-factor event.

**Within-dataset analogs.** The represented purine enzymes nearest to this
logic were `Adk` and `Nt5c2`. Both perturb one-enzyme steps in purine
salvage/interconversion, and both were transcriptionally buffered in the focal
class: `Adk` had no focal DEG with a minimum adjusted P of 0.203, and `Nt5c2`
had all focal adjusted P values equal to 1.0. The same-experiment July corpus
reported the same qualitative conclusion: `Adk` had no BH-significant
downstream neuronal transcriptome in any of 23 recovered groups and did not
induce queried cAMP/activity, purine, or methylation transcripts; `Nt5c2` had
a single off-focal `Ddx50` hit and no AMPK/mTOR/ISR/p53 or purine-enzyme
program among 1,098 explicitly queried gene-cell tests. Thus single purine
enzyme loss in this P16 CRISPR, P37-P44 NeuN+ snRNA-seq assay did not commonly
cross an RNA-level stress threshold.

`Lyrm4` was a second, indirect counterexample. It is an Fe-S assembly target,
not a GUK1-pathway enzyme, but the only FDR<0.10 downstream event curated for
it was `Gmpr` up-regulation in `155 MB Glut`; in the focal thalamic class it
had `n_degs = 0` and minimum adjusted P 0.651. This argues that an isolated GMP
catabolic marker elsewhere is insufficient to predict a focal GMP/GDP response.
The mitochondrial carrier controls were similarly small: `Slc25a36` was fully
flat in the focal class and `Slc25a4` produced only a self-transcript call.

**Decision.** I therefore set the point prediction to zero. The causal chain I
am assuming is: acute mosaic `Guk1` loss partially reduces GUK1 activity in
some postmitotic thalamic glutamatergic neurons; redundant nucleotide salvage,
de novo synthesis, and existing nucleotide pools buffer GDP/GTP and
mitochondrial dNTP imbalance over the sampled window; no consistent AMPK, ISR,
p53, mitochondrial-stress, or purine-enzyme transcriptional state propagates
into recovered nuclei strongly enough for BH FDR<0.05. This is a
within-dataset prediction with external biology used to select the analogs,
not a direct observation of held-out `Guk1`.

## Limits and uncertainty

- The closest mechanistic comparators were missing as perturbations. In
  particular, the training data did not include `Gmpr`, `Gmpr2`, `Gmps`,
  `Impdh1`, `Impdh2`, `Hprt`, `Dguok`, `Tk2`, `Rrm2`, or `Rrm2b`.
- No metabolite, GDP/GTP, dNTP-pool, mtDNA-copy-number, or respiratory-chain
  endpoint was measured. A true GUK1 metabolic defect could be present while
  the nuclear RNA endpoint remains zero.
- The perturbation is partial and mosaic. Human GUK1 deficiency involves
  strong biallelic pathogenic variants and prominent muscle/liver/immune
  phenotypes, so it is an imperfect match to acute postnatal neuronal CRISPR.
- GUK1 could matter more in proliferating neural progenitors or in cells with
  high mtDNA turnover. The focal group contains postmitotic, surviving NeuN+
  thalamic nuclei sampled once, which biases the endpoint toward stable,
  cell-autonomous RNA states.
- The exact answer could be an isolated singleton, as with `Nt5c2` outside the
  focal class or `Slc25a4` as a self-only focal hit. I did not predict a
  singleton for `Guk1` because the direct focal purine analogs had adjusted
  P values well above threshold and because the `Guk1` perturbation was held
  out, so there is no evidence for a self-only row.
