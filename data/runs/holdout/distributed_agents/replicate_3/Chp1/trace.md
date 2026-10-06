# Chp1 prediction for `151 TH Prkcd Grin2c Glut`

## Question interpreted

The held-out manifest for this run contains a single requested perturbation, `Chp1`.  I interpreted the task as predicting the focal endpoint used in
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon Benjamini-Hochberg adjusted
`pvals_adj < 0.05` after a sparse P16 AAV CRISPR loss-of-function perturbation, with the perturbed target counted if its own transcript passes the FDR cutoff.

The important ambiguity I resolved is that `n_degs = 1` can mean "only the target transcript was significantly depleted" rather than a downstream biological
program.  Several close training analogs have exactly that pattern, so I separated the zero/nonzero call from the downstream-breadth call.

## Sources used

- The supplied training endpoint table,
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- The supplied full DE parquet,
  `[local file: training_de_all_cell_groups.parquet]`, filtered to
  `group_name == "151 TH Prkcd Grin2c Glut"` for biologically chosen analog perturbations.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`.  `target_context("Chp1")` returned no direct Chp1 claims or findings, so I used
  it only as a same-experiment knowledge layer for represented neighbors, especially `Slc9a7`, `Ppp3r1`, `Atp2a2`, `Atp2b1`, and `Kif1b`.
- PubMed / NCBI literature searches for CHP1 mechanism:
  - Lin and Barber 1996, `PNAS`, DOI `10.1073/pnas.93.22.12631`: identification of a calcineurin-homologous NHE1-binding protein.
  - Pang et al. 2001, `JBC`, DOI `10.1074/jbc.M100296200`: CHP as an essential cofactor for NHE-family exchanger activity.
  - Matsushita et al. 2007, `Am J Physiol Cell Physiol`, DOI `10.1152/ajpcell.00464.2006`, and Matsushita et al. 2011, DOI
    `10.1152/ajpcell.00404.2010`: CHP1 stabilizes NHE1/SLC9A1 and promotes its surface expression and antiporter activity.
  - Liu et al. 2013, `J Neurosci`, DOI `10.1523/JNEUROSCI.0406-13.2013`: vacillator `Chp1` mutation impairs NHE1 maturation and axon-terminal localization
    in Purkinje cells.
  - Mendoza-Ferreira et al. 2018, `Neurology Genetics`, DOI `10.1212/NXG.0000000000000209`: recessive human `CHP1` mutation causes ataxia by impairing NHE1
    function.
  - Lin et al. 1999, `JBC`, DOI `10.1074/jbc.274.51.36125`: CHP can inhibit calcineurin in heterologous cells.
  - Jimenez-Vidal et al. 2010, `JBC`, DOI `10.1074/jbc.M110.165555`: nuclear CHP1 can interact with UBF and regulate rRNA synthesis in quiescent fibroblasts.
  - Di Sole et al. 2011, `Am J Physiol Renal Physiol`, DOI `10.1152/ajprenal.00628.2011`: review of the multifunctional CHP family.

## Computation over the inputs

I first read the endpoint CSV to get the focal calibration distribution.  It is strongly zero-inflated: 1205/1674 training perturbations have zero DEGs, 276
have one DEG, the median is zero, the 75th percentile is one, the 95th percentile is 18, and the maximum is 2677.

The full DE parquet has 616,253,184 rows, so I avoided a full table load.  Parquet row-group statistics showed that `151 TH Prkcd Grin2c Glut` resides in row
groups 546-580.  I then used a `pyarrow.dataset` predicate on the focal `group_name` and a small `isin` list of biologically selected analogs to retrieve the
full measured-gene signatures for:

`Slc9a7`, `Slc9a9`, `Ppp3ca`, `Ppp3cc`, `Ppp3r1`, `Calm1`, `Calm2`, `Calm3`, `Kif1a`, `Kif1b`, `Kifbp`, `Gsk3b`, `Akt3`, `Atp2a2`, `Atp2b1`, `Atp2b2`,
`Atp2b3`, and `Atp2c1`.

I used those signatures in two ways: to verify that the CSV `n_degs` values matched `pvals_adj < 0.05` in the parquet, and to inspect whether the significant
genes represented self-transcript depletion only or a downstream expression state.

## Target-specific reasoning

### `Chp1`

`Chp1` encodes an EF-hand myristoylated calcineurin-B-homologous protein.  Its best-established neuronal role is not as a catalytic calcineurin subunit but as
an obligate NHE cofactor: CHP1 binds the juxtamembrane C-terminal regulatory domain of NHE1/SLC9A1, stabilizes NHE1 protein, promotes maturation/surface
localization, and is needed for normal Na+/H+ exchange (Pang et al. 2001; Matsushita et al. 2007, 2011; Dong et al. 2021, DOI `10.1038/s41467-021-23496-z`).
This axis is neurologically real: the mouse vacillator `Chp1` allele reduces CHP1, impairs NHE1 localization at Purkinje axon terminals, and causes ataxia and
Purkinje axon degeneration (Liu et al. 2013); rare human biallelic `CHP1` mutation similarly reduces soluble CHP1/NHE1 membrane targeting and causes recessive
ataxia (Mendoza-Ferreira et al. 2018).

The closest NHE-family analogs present in the training endpoint are organellar rather than NHE1-like:

| training perturbation | focal `n_degs` | expression-pattern evidence in `151 TH Prkcd Grin2c Glut` | interpretation for `Chp1` |
| --- | ---: | --- | --- |
| `Slc9a7` | 1 | the only FDR<0.05 gene was `Slc9a7` itself (`logfoldchanges = -0.693`, `padj = 4.98e-5`) | target-only response; Golgi/endosomal NHE loss did not drive a broad transcriptome |
| `Slc9a9` | 0 | no gene approached FDR; the best adjusted p-values were 1.0 | an NHE-family KO can be completely buffered in this focal group |

The Distributed Agents corpus has the same qualitative interpretation for the broader same-experiment surface: acute `Slc9a7` was buffered across measured neuronal
groups, and endomembrane pH relatives `Slc9a9`, `Atp6v0a1`, `Clcn3`, and `Clcn4` were flat or nonconvergent.  These are imperfect analogs because CHP1 is tied
most directly to plasma-membrane NHE1, which was not a training target, but they make it unlikely that an NHE/cofactor lesion generically crosses into a large
steady-state snRNA program.

I also considered calcineurin and Ca2+/calmodulin comparators because CHP1 is calcineurin-B-like and overexpressed CHP can inhibit calcineurin activity in
non-neuronal assays.  The focal counts were small and subunit-specific:

| training perturbation | focal `n_degs` | expression-pattern evidence | interpretation for `Chp1` |
| --- | ---: | --- | --- |
| `Ppp3ca` | 4 | significant genes were `Ppp3ca`, `Iyd`, `Pik3r1`, and `Ptpn3`; only `Pcsk1n` sat just above FDR at `padj = 0.0507` | catalytic calcineurin loss is detectable but very narrow |
| `Ppp3cc` | 0 | no FDR genes | another catalytic calcineurin paralog is silent |
| `Ppp3r1` | 9 | significant genes included `Pcsk1n`, `Ptprs`, target `Ppp3r1`, `Atp2a2`, `Coro6`, `Tle2`, `Ndrg2`, `Septin4`, `Slc6a17` | the broadest calcineurin-axis proxy still gives only a single-digit response |
| `Calm1` | 14 | `Calm1` itself plus a small Rasgrp2/Peg3/Resp18/Coro6/Vamp1 module; `Coro6` moved opposite to `Ppp3r1` | CaM-locus loss is branch- and locus-specific rather than a calcineurin phenocopy |
| `Calm2` | 0 | no FDR genes | flat |
| `Calm3` | 1 | target-only | flat downstream |

Distributed Agents `Ppp3r1` findings independently summarize this same screen behavior: the calcineurin-axis RNA response was centered on `Ppp3r1` and partly `Ppp3ca`,
was not shared by `Ppp3cc`, `Fkbp1a`, or `Nfatc3`, and upstream calmodulin loci did not act as a single interchangeable CaM/calcineurin RNA pathway.  Because
CHP1 is only calcineurin-like and its physiological neuronal phenotype is routed through NHE1, I treated `Ppp3r1 = 9` as an upper counterexample rather than as
a pooled estimate.

Other CHP1-associated or adjacent biology also points to a very narrow focal response:

| training perturbation | focal `n_degs` | why checked | expression-pattern evidence |
| --- | ---: | --- | --- |
| `Kif1a` | 1 | axonal transport/cargo analogy | target-only |
| `Kif1b` | 0 | KIF1B is the closest assayed kinesin implicated in axon and vesicle transport | the target transcript itself did not pass FDR in 151 |
| `Kifbp` | 2 | kinesin-binding/accessory control | target plus only `Srebf2` |
| `Akt3` | 0 | growth-factor/NHE regulation context | flat |
| `Gsk3b` | 6 | CHP-family links to GSK3 in cardiomyocytes are reported for CHP3 | tiny, unrelated six-gene response |

Finally, I used calcium-pump perturbations as counterexamples for what a real focal calcium-homeostasis state looks like in this dataset.  `Atp2a2` loss had 187
DEGs and induced `Ddit3`, `Xbp1`, `Herpud1`, `Hspa5`, `Asns`, and `Chac1`, a SERCA2/ER-stress UPR/ISR state.  `Atp2b1` had 22 DEGs, with `Fos`, `Nr4a1`, `Vgf`,
`Cck`, and `Ptprn` suggesting an activity/neuropeptide state.  The closer PMCA paralogs `Atp2b2` and `Atp2b3` were target-only, and `Atp2c1` was target-only.
This tells me the assay can detect a sustained ER-stress or activity program in this cell group, but those are specific to particular calcium pumps and are not
an expected consequence of losing an NHE1 accessory EF-hand protein.

### Zero/nonzero and point prediction

I do not expect a broad downstream state for `Chp1`: the best in-dataset NHE, kinesin, calcineurin, CaM, and PMCA neighbors are mostly zero or target-only, and
the literature-supported Chp1 phenotypes concern NHE1 trafficking, axon-terminal pH homeostasis, or specialized Purkinje/motor phenotypes that this thalamic
single-nucleus RNA endpoint may not read out.

I nevertheless predict a nonzero singleton rather than zero.  CHP1 is ubiquitous, the measured gene `Chp1` was present in all 1674 focal training signatures,
and many buffered but expressed genes in this same analog set pass only as their own perturbed transcript (`Slc9a7`, `Kif1a`, `Atp2b2`, `Atp2b3`, `Atp2c1`,
`Calm3`).  My point prediction is therefore one FDR-significant gene, interpreted as likely direct `Chp1` transcript depletion with no confident downstream
FDR genes.

## Limits

This is an extrapolation because the two most direct genetic comparators, `Slc9a1/Nhe1` and `Chp2`, were absent from the training perturbations, and Distributed Agents
had no direct same-experiment `Chp1` corpus entry.  CHP1's strongest animal phenotypes occur in Purkinje cells and axon terminals, whereas the focal group here
is a thalamic glutamatergic aggregate and the readout is nuclear RNA after sparse postnatal editing; altered axonal pH, NHE1 membrane abundance, vesicle
trafficking, and synapse physiology could be real while still producing zero Wilcoxon DEGs.  Conversely, the exact difference between a zero and a target-only
one depends on guide efficiency, local indels, nonsense-mediated decay, and `Chp1` expression in the perturbed nuclei, none of which are directly reported for
the held-out target.
