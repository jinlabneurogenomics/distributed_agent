# Chp1 prediction trace

## Question and resolved ambiguities

The requested held-out target was:

| target_name |
|---|
| Chp1 |

I interpreted `n_degs` as the integer number of measured genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` for a sparse, acute
CRISPR loss-of-function perturbation, including the perturbed transcript itself
when it passes the same threshold. I did not treat the count as a direct
measure of target importance, editing rate, viability, or protein depletion.
`Chp1` was absent from both supplied training inputs, so all inferences below
come from non-held-out perturbations and external Chp1 biology.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal-cell training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Run manifest:
  `[local file: 038_Chp1.csv]`
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`. I used its target-specific
  claims for `Ppp3ca`, `Ppp3r1`, `Slc9a7`, and `Slc9a9` to check whether the
  Chp1-adjacent calcium/calcineurin and Na+/H+ exchanger neighborhoods formed
  recurrent transcriptional modules in this screen.
- NCBI PubMed literature searches for CHP1 / calcineurin B homologous protein
  1 and NHE1/SLC9A1.

Key external mechanisms and citations:

- CHP1 is a calcineurin-B-like EF-hand protein that binds the cytosolic
  juxtamembrane region of NHE1/SLC9A1 and is required for normal NHE1 pH
  sensitivity and antiporter activity: Pang et al. 2004,
  DOI `10.1021/bi0360004`, PMID `15035633`; Mishima et al. 2006,
  DOI `10.1074/jbc.M604092200`, PMID `17050540`.
- Loss of CHP1 destabilizes NHE1 protein; the CHP1-NHE1 interaction increases
  biosynthetic maturation, plasma-membrane localization, surface stability, and
  exchange activity: Matsushita et al. 2007,
  DOI `10.1152/ajpcell.00464.2006`, PMID `17392381`; Matsushita et al. 2011,
  DOI `10.1152/ajpcell.00404.2010`, PMID `21543739`.
- Cryo-EM of the human NHE1-CHP1 complex shows CHP1 as a direct NHE1 partner
  coupled to NHE1 conformational states and pH sensitivity: Dong et al. 2021,
  DOI `10.1038/s41467-021-23496-z`, PMID `34108458`.
- In the mouse `vacillator` Chp1 mutant, defective CHP1 reduces NHE1 terminal
  localization in Purkinje cells and is followed by axon degeneration; Nhe1
  genetic ablation produced a convergent Purkinje phenotype: Liu et al. 2013,
  DOI `10.1523/JNEUROSCI.0406-13.2013`, PMID `23904602`.
- CHP1 and CHP2 are closely related NHE cofactors but have different expression
  and Ca2+-binding behavior: Liang et al. 2020,
  DOI `10.1096/fj.201902093R`, PMID `31912575`.

## Computation over the supplied dataset

I first loaded the held-out manifest and focal training counts. The manifest
contained only `Chp1`. The training endpoint contained 1,674 non-held-out
targets; 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1,
and the mean was inflated to 14.1 by a small set of very broad outliers such as
`Uba5`, `Tpr`, and `Sin3a`.

For biologically nominated comparator targets, I filtered the 7.8 GB parquet
directly to the focal cell group and target subset:

```python
pd.read_parquet(
    training_parquet,
    columns=["names", "group_name", "gene_target",
             "logfoldchanges", "pvals_adj", "scores"],
    filters=[
        ("group_name", "==", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", analog_targets),
    ],
)
```

I sorted each selected perturbation by adjusted p-value to inspect which genes
accounted for the count. I also ran the Distributed Agents runtime profile-comparison
tools on 12 Chp1-adjacent perturbations in the same focal context
(`Ppp3r1`, `Ppp3ca`, `Ppp3cc`, `Calm1`, `Calm2`, `Calm3`, `Nfatc3`, `Nfat5`,
`Slc9a7`, `Slc9a9`, `Atp6v0a1`, `Clcn4`). This was a check for hidden
same-direction overlap among weak signatures. It showed isolated or absent FDR
programs: for example `Ppp3r1` and `Ppp3ca` had no shared FDR<0.05 genes,
`Ppp3r1` and `Calm1` shared only a direction conflict on `Coro6`, and the NHE
or endomembrane-acidification comparators were essentially target-only or flat.

## Chp1-specific analogs and counterexamples

`Slc9a1`, the best direct biochemical proxy for Chp1 through NHE1, was not a
training perturbation in the focal endpoint. Neither `Chp2` nor `Chp3/Tesc` was
available, so there was no same-cofactor paralog to transfer from. I therefore
treated available NHE/pH genes as partial downstream analogs and treated
calcineurin/calmodulin genes mostly as counterexamples: they share EF-hand or
calcium vocabulary with Chp1, but they report a different pathway.

| training perturbation | focal `n_degs` | focal expression evidence | relevance to Chp1 |
|---|---:|---|---|
| `Slc9a7` | 1 | The only FDR<0.05 gene was `Slc9a7` itself, log2FC -0.69, `p_adj=5.0e-5`; the next gene had `p_adj=0.273`. | SLC9 family / pH-regulatory exchanger, but NHE7 is endomembrane rather than the plasma-membrane NHE1 client of CHP1. Its target-only response argues against generic NHE loss creating a broad nuclear RNA program. |
| `Slc9a9` | 0 | No gene passed FDR; the leading adjusted p-values were 1. | Endosomal SLC9 family member. The null response is a strong counterexample to using NHE annotation alone. |
| `Atp6v0a1` | 1 | `Atp6v0a1` itself was significant, log2FC -0.64, `p_adj=4.5e-12`; the next gene had `p_adj=0.125`. | Vacuolar acidification is more severe and more endolysosomal than NHE1/CHP1, but it is an acidification-stress boundary. |
| `Clcn4` | 1 | `Clcn4` itself was significant, log2FC -0.80, `p_adj=6.7e-11`; the next gene had `p_adj=1`. | Endosomal Cl-/H+ exchange counterexample; target-only despite clear target mRNA loss. |
| `Clcn3` | 0 | `Clcn3` did not reach FDR in the focal group. | Another vesicle-pH counterexample. |
| `Ppp3r1` | 9 | Small thalamic-specific response including `Pcsk1n`, `Ptprs`, `Ppp3r1`, `Atp2a2`, `Coro6`, `Tle2`, `Ndrg2`, `Septin4`, `Slc6a17`. | Calcineurin regulatory subunit with Ca2+-binding EF hands. It is a structural-name neighbor to CHP1, not an NHE cofactor, and its sparse synaptic/cytoskeletal signature is not a clear Chp1 proxy. |
| `Ppp3ca` | 4 | `Ppp3ca`, `Iyd`, `Ptpn3`, and `Pik3r1` passed FDR; `Pcsk1n` missed at `p_adj=0.0507`. | Calcineurin catalytic subunit. Its weaker, nonidentical response versus `Ppp3r1` argues that even true calcineurin subunits were not interchangeable in this readout. |
| `Ppp3cc` | 0 | No FDR genes. | Catalytic calcineurin paralog that did not phenocopy `Ppp3ca`. |
| `Nfatc3` | 0 | No FDR genes. | Downstream calcineurin/NFAT transcription was not detectably engaged at basal steady state. |
| `Calm1` | 14 | A modest, locus-specific signature including `Calm1`, `Rasgrp2`, `Peg3`, `Aifm3`, `Tuba1b`, `Resp18`, `Maged1`, and `Coro6`. | Upstream Ca2+/calmodulin biology is broader than Chp1 and not interchangeable: `Calm2` was 0 and `Calm3` was 1 in the same endpoint. |

The same-experiment Distributed Agents corpus supported these raw observations. Its
`Slc9a7`/`Slc9a9` claims describe pan-neuronal or near-pan-neuronal buffered
NHE surfaces with no hidden all-target convergence. Its calcineurin claims
state that detectable calcineurin-axis RNA responses in this screen are
subunit-selective and centered on `Ppp3r1` and partly `Ppp3ca`, not a shared
NFAT-like or immunophilin-equivalent program.

## Zero/nonzero decision and point estimate

CHP1 loss should most directly perturb NHE1 maturation, localization, and
cytosolic pH control, but the training perturbations closest to pH handling were
0 or target-only in the focal neurons. The direct NHE client `Slc9a1` was not
measured as a perturbation, but the available SLC9/endosomal acidification
genes argue against predicting a broad unfolded-protein, calcium, or ion-channel
transcriptional state. The small `Ppp3r1` and `Ppp3ca` signatures keep open the
possibility of a few FDR genes for calcium-adjacent EF-hand losses, but they are
mechanistically less appropriate for Chp1 than the NHE axis and do not converge
with each other.

I therefore predicted an extremely sparse nonzero response: one DEG. This is
best interpreted as a target-transcript or target-only-scale call, not a
prediction that Chp1 loss will copy the `Ppp3r1`, `Calm1`, or ER-stress
programs. A prediction of 0 would also be plausible if Chp1 RNA does not fall
significantly in this cell group; the reason I chose 1 rather than 0 is that
CHP1 is a broadly expressed obligate NHE1 cofactor and several well-engaged
ion-homeostasis comparators in this assay landed at exactly one significant
gene.

## Limits

- The best biochemical loss-of-function comparator, `Slc9a1/Nhe1`, was absent
  from the training target universe, and `Chp2`/`Chp3` were also absent.
- `Slc9a7` and `Slc9a9` are endomembrane NHEs, not a plasma-membrane NHE1
  replacement, so they can only bound generic pH/NHE consequences.
- The calcineurin subunits are structural-name and Ca2+-pathway counterexamples
  rather than close molecular analogs of Chp1.
- The strongest published neuronal Chp1 phenotype is Purkinje axon degeneration
  in the `vacillator` mouse; this experiment assays sparse acute postmitotic
  perturbation in juvenile NeuN+ nuclei and does not measure pH, NHE1 protein,
  axon terminals, non-neuronal effects, or later degeneration.
- Average mRNA knockdown in the screen is partial. A single-gene count hinges on
  whether the Chp1 target transcript itself clears FDR in this particular
  thalamic group, which is extrapolated rather than directly observed.

Final point prediction: `Chp1 = 1`.
