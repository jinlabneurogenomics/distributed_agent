# Held-out DEG-count prediction for Ptcd3

## Question and endpoint

The requested readout is the number of genes with Wilcoxon Benjamini-Hochberg
FDR `< 0.05` after a held-out `Ptcd3` CRISPR loss-of-function perturbation in
`151 TH Prkcd Grin2c Glut` thalamic glutamatergic neurons.  The count includes
the perturbed transcript itself if it passes the FDR threshold.  I treated the
training focal-cell CSV as the direct endpoint for non-held-out perturbations
and the all-cell differential-expression Parquet as direct expression evidence
for those same visible perturbations only.  The `Ptcd3` knockout signature and
its count are absent from both declared inputs, so the prediction requires
transfer from visible perturbations plus external biology.

There is one held-out target:

| target_name | in focal training counts |
|---|---:|
| Ptcd3 | no |

## Sources used

- Declared training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression table:
  `training differential-expression dataset`.
- Requested-target manifest:
  `single-target request for Ptcd3`.
- Run-local task bindings, dataset portrait, coverage summary, and capability
  manifest under `codex_runtime/pipeline`.
- Same-experiment internal corpus:
  `perturbai-july-260713-sourceguard-1773-v1`, queried through
  `corpus.findings` for report-derived summaries of `Dap3`, `Fars2`, `Gfm2`,
  `Lrpprc`, `Rmnd1`, and `Opa1`.  This corpus is a semantic layer over the same
  Perturb-seq experiment, not an independent replicate.
- External gene-function priors from MitoCarta3.0, Gene Ontology mitochondrial
  translation and mitochondrial small-ribosomal-subunit annotations, and
  PubMed-indexed primary literature.

External anchors used for mechanism:

| fact | citation |
|---|---|
| PTCD3/MRPS39 is a mammalian mitochondrial protein associated with the mitoribosomal small subunit and required for efficient mitochondrial translation/respiration in depletion experiments. | Davies et al. 2009, FEBS Lett, DOI `10.1016/j.febslet.2009.04.048`, PMID `19427859` |
| Biallelic PTCD3 variants cause combined oxidative-phosphorylation defects and Leigh/Leigh-like neurologic disease. | Borna et al. 2019, Neurogenetics, DOI `10.1007/s10048-018-0561-9`, PMID `30607703`; Lace et al. 2024, JIMD Rep, DOI `10.1002/jmd2.12424`, PMID `39544688` |
| PTCD3/mS39 forms part of the mitoribosomal mRNA entry platform contacted by the LRPPRC-SLIRP delivery module. | Aibara et al. 2020, eLife, DOI `10.7554/eLife.58362`, PMID `32812867`; Singh et al. 2024, Nat Struct Mol Biol, DOI `10.1038/s41594-024-01365-9`, PMID `39134711` |
| DAP3/MRPS29 is a mitochondrial small-subunit ribosomal protein; its depletion can impair mitochondrial-encoded translation and mitochondrial dynamics. | Cavdar Koc et al. 2001, FEBS Lett, DOI `10.1016/S0014-5793(01)02250-5`, PMID `11248257`; Xiao et al. 2015, J Biol Chem, DOI `10.1074/jbc.M115.673343`, PMID `26306039`; Smith et al. 2024, Am J Hum Genet, DOI `10.1016/j.ajhg.2024.11.007`, PMID `39701103` |
| MitoCarta3.0 places nuclear genes such as `Ptcd3`, `Dap3`, `Fars2`, `Gfm2`, `Lrpprc`, `Rars2`, and OXPHOS genes in the mitochondrial proteome and manually curated mitochondrial pathways. | Rath et al. 2021, Nucleic Acids Res, DOI `10.1093/nar/gkaa1011`, PMID `33174596` |

## Computations over the declared dataset

I loaded the focal training count CSV and summarized its endpoint distribution.
The endpoint was highly zero-inflated: among 1,674 visible perturbations, the
median `n_degs` was 0, 72.0% had no DEG in this focal class, 28.0% had any
positive count, and the 95th percentile was only 18 DEGs.

I then filtered the Parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for
candidate mitochondrial analogs and for all rows with `pvals_adj < 0.05`.  The
complete FDR scan gave 23,526 significant rows across 469 targets; 276 targets
had exactly one DEG, and 237 of those 276 singletons, or 85.9%, were just a
significant self-target transcript.  Thus a one-DEG count in this cell class is
often target-RNA loss rather than a downstream program.

`Ptcd3` itself is a measured transcript in the training Parquet: it appeared in
1,674 focal-cell contrasts, one for each visible training perturbation.  A
withheld `Ptcd3` count therefore could have included a self-transcript call,
but self-mRNA depletion is guide- and transcript-architecture-dependent in this
CRISPR design and was not used as evidence for broad mitochondrial stress.

The focal-cell counts for biologically relevant visible perturbations were:

| training perturbation | relationship to Ptcd3 | focal n_degs | focal FDR evidence |
|---|---|---:|---|
| `Dap3` | mitochondrial small-subunit protein, closest visible mitoribosome analog | 1 | only `Dap3` itself, log2FC `-0.676`, FDR `3.95e-06`; no downstream gene reached FDR `<0.25` in this focal query |
| `Gfm2` | mitochondrial ribosome recycling/elongation-factor family | 0 | no row even at FDR `<0.25` in the focal query |
| `Fars2` | mitochondrial tRNA synthetase, mitochondrial translation input | 0 | no focal row at FDR `<0.25` |
| `Lars2` | mitochondrial tRNA synthetase | 0 | no focal row at FDR `<0.25` |
| `Rars2` | mitochondrial tRNA synthetase | 0 | no focal row at FDR `<0.25` |
| `Rmnd1` | mitochondrial translation/OXPHOS disease gene | 0 | no focal row at FDR `<0.25` |
| `Lrpprc` | mitochondrial mRNA stabilizer and delivery factor upstream of mS39 | 0 | nearest focal row was `Emc1`, FDR `0.174`, not significant |
| `Afg3l2`, `Clpp`, `Clpx`, `Lonp1`, `Yme1l1` | mitochondrial proteostasis genes that could secondarily alter OXPHOS stress | 0 | all zero in the focal count table |
| `Opa1` | inner-membrane fusion/cristae stressor, mitochondrial but not a mitoribosome component | 37 | robust ISR-like signature: `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Opa1`, `Mthfd2`, `Slc7a5`, and others passed FDR |
| multiple OXPHOS subunits, e.g. `Ndufa10`, `Ndufs2`, `Cox5a`, `Sdha`, `Uqcrc2`, `Tomm40` | downstream respiratory-chain complexes | mostly 0 or 1 | most positives were self-only; `Ndufv2` and `Uqcrq` had one non-self singleton each |

The same-experiment report corpus matched the Parquet pattern.  Its Dap3
report described `Dap3` as recovered in every neuronal cell group but with no
robust downstream transcriptome; it specifically noted that Dap3 did not
activate the `Asns/Ddit3/Chac1/Slc7a5/Shmt2/Herpud1/mt-Co2/mt-Cytb` module
detected after `Opa1`.  The `Fars2`, `Gfm2`, `Lrpprc`, and `Rmnd1` reports all
summarized pan-neuronal or near pan-neuronal absence of FDR-resolved
downstream mitochondrial-translation stress programs.  In contrast, the `Opa1`
report identified a clear ATF4/ISR-like module and lowered mitochondrial
transcripts in this same experiment.  I therefore interpreted Opa1 as a
positive control for detectability of a mitochondrial stress state, not as the
best mechanistic analog for PTCD3.

## Target-specific prediction

### Ptcd3

**Causal transfer model.**  The requested intervention is acute, mosaic Cas9
loss of `Ptcd3` starting at P16.  The direct molecular consequence should be
impaired mS39/PTCD3 function at the mitochondrial small ribosomal subunit,
where mS39 helps the LRPPRC-SLIRP module hand mitochondrial mRNAs into the
translation channel.  A strong lesion could reduce synthesis of
mtDNA-encoded OXPHOS subunits, propagate to lower respiratory-chain activity,
and eventually induce an ATF4/ISR-like nuclear stress program or lower
mtDNA-encoded RNAs among recovered nuclei.  The measured endpoint, however, is
not mitochondrial translation, ATP, or viability; it is survivor-conditioned
nuclear RNA differential expression 3-4 weeks after sparse editing.

**Within-dataset analogs.**  `Dap3` is the key analog because it is also a
mitochondrial small-subunit protein.  Its focal count was one, but that one was
only Dap3 self-depletion; the same-experiment Dap3 report found no downstream
FDR program in any neuronal class.  `Gfm2`, `Fars2`, `Lars2`, `Rars2`, `Rmnd1`,
and `Lrpprc` are less exact structurally but hit mitochondrial RNA handling or
translation before OXPHOS assembly; all had zero DEGs in `151 TH Prkcd Grin2c
Glut`.  Their reports also rejected hidden convergence on an ISR/mtUPR-like
module.  Respiratory-chain subunits downstream of mitoribosome function were
similarly weak: complex I/III/IV/II examples were zero or self-only in this
focal endpoint.  These are more appropriate for `Ptcd3` than `Opa1`, because
OPA1 perturbs inner-membrane fusion and cristae organization rather than the
mitochondrial translation apparatus, and in this dataset it entered a broad
ISR state that the represented mitochondrial-translation perturbations did not.

**Zero/nonzero decision.**  External biology strongly supports PTCD3 as an
essential mitochondrial translation factor under deep biallelic or biochemical
loss.  The declared Perturb-seq screen nevertheless under-resolved this part
of the mitochondrial central-dogma/OXPHOS axis in recovered juvenile neurons:
the closest visible small-subunit target produced no downstream DEGs, all
visible mt-aaRS/RNA-delivery/translation factors were zero in the focal class,
and their expected OPA1-like ATF4 module was absent.  A single self-transcript
DEG is plausible because `Ptcd3` is measured and `Dap3` was a self-only
singleton, but self-depletion was not reproducible enough across mitochondrial
translation genes to overcome the zero mode of the relevant analog set.

I therefore predict that held-out `Ptcd3` will have no genes passing FDR 0.05
in `151 TH Prkcd Grin2c Glut`:

| target_name | predicted_n_degs |
|---|---:|
| Ptcd3 | 0 |

## Limits

This is an extrapolation from related mitochondrial genes, not a direct
signature match, because the held-out `Ptcd3` rows are absent.  The best exact
training analog, `Dap3`, gives a one-DEG count entirely through self-mRNA
depletion, so the difference between a true hidden value of 0 and 1 is governed
partly by unobserved guide placement, nonsense-mediated decay, and power rather
than by mitochondrial biology.  The Parquet is also an snRNA readout on
surviving, class-assigned NeuN+ nuclei; it cannot rule out reduced PTCD3
protein, reduced mitochondrial translation, lower respiration, or edited-cell
loss before sampling.  External PTCD3 disease reports come from human biallelic
variants or cultured cells and establish function, but they do not guarantee
that sparse postnatal mouse thalamic glutamatergic neurons will enter a
detectable nuclear stress state at this time point.
