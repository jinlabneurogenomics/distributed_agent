# Question

Predict, for each target in `150_Nfkb2.csv`, how many genes would be called
DE at BH-adjusted Wilcoxon `pvals_adj < 0.05` after acute CRISPR loss of that
target in `151 TH Prkcd Grin2c Glut` neurons.  The manifest contains one
held-out target, `Nfkb2`; its own differential-expression profile and endpoint
count are absent from the supplied training files.

I interpreted the task as an assay-local endpoint prediction, not as a generic
importance score.  A count of zero means that no measured transcript is expected
to pass the exact FDR threshold in this cell group.

# Sources Used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: endpoint counts for
  1,674 non-held-out perturbations.
- `training_de_all_cell_groups.parquet`: focal-cell DE rows filtered to
  `151 TH Prkcd Grin2c Glut` for NF-kappaB, TLR, TNF-receptor, and TRAF
  comparators.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
  `Nfkb2` itself had no bottom-up corpus card in this held-out run, but the
  corpus contained same-experiment syntheses for `Nfkb1`, `Chuk`, and `Traf3`
  reporting that represented TNFR/TLR/CD40-to-TAK1/IKK/NF-kappaB perturbations
  are broadly transcriptionally silent in unchallenged postnatal NeuN-positive
  neurons.
- Distributed Agents runtime `profile_neighbors`, used to compare signed nominal
  expression tails among observed NF-kappaB/TLR/TNFR perturbations in the focal
  cell group.
- PubMed literature on noncanonical NF-kappaB:
  - Sun 2012, Immunological Reviews, DOI `10.1111/j.1600-065X.2011.01088.x`,
    PMID `22435551`.
  - Coope et al. 2002, EMBO Journal, DOI `10.1093/emboj/cdf542`, PMID
    `12374738`.
  - Fusco et al. 2016, Science Signaling, DOI `10.1126/scisignal.aad9413`,
    PMID `27678221`.
  - Lovas et al. 2012, PLOS ONE, DOI `10.1371/journal.pone.0042741`, PMID
    `22880094`.
  - Meffert et al. 2003, Nature Neuroscience, DOI `10.1038/nn1110`, PMID
    `12947408`.

# Computational Checks

I first read the requested-target manifest and the training count table.  The
focal endpoint is very sparse: median `n_degs = 0`, 75th percentile `= 1`,
95th percentile `= 18`, and only 469/1674 training perturbations are nonzero.
The assay was nevertheless able to detect broad responses in this same cell
group, with `Uba5 = 2677`, `Tpr = 1768`, `Sin3a = 1433`, `Rnpc3 = 868`, and
`Zbtb7a = 841` DE genes.

I then filtered the Parquet DE table to the focal cell group and observed
NF-kappaB-adjacent training targets.  For each target I recomputed
`sum(pvals_adj < 0.05)` and inspected raw-p lead genes and sentinel NF-kappaB
readouts.  The most relevant focal-cell counts were:

| training target | relationship to Nfkb2 | n_pert | n_degs |
| --- | --- | ---: | ---: |
| `Nfkb1` | closest represented NF-kappaB precursor paralog, p105/p50 | 181 | 0 |
| `Rel` | represented Rel-family nuclear NF-kappaB subunit | 205 | 0 |
| `Chuk` | IKKalpha, required with NIK to phosphorylate/process p100 | 156 | 0 |
| `Traf3` | suppresses NIK abundance upstream of noncanonical NF-kappaB | 211 | 0 |
| `Map3k7` | TAK1, canonical TNF/TLR-to-IKK/JNK pathway kinase | 160 | 0 |
| `Cyld` | deubiquitinase regulating NF-kappaB/TNF signaling | 141 | 0 |
| `Cd40` | TNFR-family receptor known to induce p100 processing | 226 | 0 |
| `Tnfrsf1a` | represented TNF receptor | 173 | 0 |
| `Tnfrsf11a` | TNFRSF/RANK, a noncanonical NF-kappaB-capable receptor | 159 | 0 |
| `Tnfrsf13c` | BAFF-R, a noncanonical NF-kappaB-capable receptor | 219 | 0 |

The raw signatures did not show near-threshold pathway activity hidden under
the FDR line.  The minimum adjusted p value for `Nfkb1` was 1.0; for `Chuk`,
0.7266; for `Traf3`, 1.0; for `Rel`, 0.1402, driven by a single `Ptcd3`
coordinate rather than NF-kappaB feedback genes.  In `Nfkb1`, `Rel`, `Chuk`,
`Traf3`, `Map3k7`, and receptor perturbations, sentinel readouts including
`Nfkb1`, `Nfkb2`, `Rela`, `Relb`, `Rel`, `Nfkbia`, `Tnfaip3`, `Birc2`, and
`Birc3` were all FDR-null.

The runtime profile-neighbor comparison among `Nfkb1`, `Rel`, `Chuk`, `Traf3`,
`Cyld`, `Map3k7`, `Cd40`, `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`,
`Tnfrsf1a`, `Tnfrsf11a`, `Tnfrsf13c`, `Tnfrsf4`, and `Tnfrsf9` connected the
cohort through weak positive- and negative-tail overlaps, but all 18 had zero
FDR-significant genes in the focal cell group.  I treated this as evidence for
a shared flat basal NF-kappaB/TNFR/TLR neighborhood rather than as evidence of
a strong hidden Nfkb2-like program.

# Target-Specific Prediction

## Nfkb2

`Nfkb2` encodes p100, the precursor of p52.  In the noncanonical NF-kappaB
pathway, selected TNF-receptor-family signals stabilize NIK, IKKalpha/`Chuk`
phosphorylates p100, and p100 is processed to p52, which forms transcriptional
dimers most characteristically with RelB (Sun 2012; Coope et al. 2002; Fusco
et al. 2016).  That makes `Chuk` and `Traf3` the best mechanistic training
analogs even though `Map3k14`/NIK and `Relb` were not available as perturbation
targets.  Both analogs were completely flat in this exact cell group
(`Chuk = 0`, `Traf3 = 0`), as were the represented upstream TNFRSF receptors
and the represented nuclear NF-kappaB family members (`Nfkb1 = 0`, `Rel = 0`).

The same-experiment Distributed Agents corpus strengthened that local pattern: its
`Nfkb1`, `Chuk`, and `Traf3` findings describe a convergent absence of basal
TNFR/TLR/CD40-to-IKK/NF-kappaB transcription in unchallenged postnatal
NeuN-positive neurons, while noting the same missing exact nodes that matter
here: `Nfkb2`, `Relb`, `Rela`, `Map3k14`, `Ikbkb`, and `Ikbkg`.  The held-out
gene therefore sits in a pathway whose available observed members are not
detectably active at this assay endpoint.

External mechanism points in the same direction.  NFKB2/p100 has two separable
functions: it is processed into the p52 DNA-binding subunit, and uncleaved p100
can sequester RelB and other NF-kappaB factors.  Full p100 loss can therefore
de-repress RelB in fibroblasts or lymphoid tissues, but p100 loss alone was
insufficient for a large alternative NF-kappaB transcriptional response without
additional canonical/TNF stimulation in Lovas et al. 2012.  The present assay
is an acute, sparse, unstimulated neuronal loss-of-function experiment with
modest target-RNA knockdown, so it is closer to removing a stimulus-gated
module from postmitotic neurons than to driving a chronic immune or epithelial
p100-null state.

Neuronal NF-kappaB can matter for synaptic signaling and memory, especially the
canonical p65:p50 axis described by Meffert et al. 2003, but that fact is a
counterexample rather than a reason to override the training data: the directly
represented `Nfkb1`/p50 and `Rel` perturbations were FDR-null in `151 TH Prkcd
Grin2c Glut`.  I therefore predict no FDR-significant DEGs for `Nfkb2`.

Prediction: `Nfkb2 -> 0`.

# Limits

This is a strong zero call but not a direct observation of `Nfkb2`.  The exact
p52:RelB arm was only partially represented: `Relb` and `Map3k14` were absent
from training, and `Nfkb2` itself was held out.  Upstream receptors such as
`Cd40`, `Tnfrsf11a`, and `Tnfrsf13c` are immune-biased and may simply be weakly
expressed in NeuN-positive neurons, so their zero counts are pathway
counterchecks rather than perfect substitutes for p100 deletion.  Finally,
acute CRISPR in this experiment reduces target RNA only modestly on average and
does not measure indels or protein turnover; a germline or strongly edited
`Nfkb2` knockout, a ligand challenge, or glial/immune cell readout could show a
real NF-kappaB2 response that this focal neuronal FDR endpoint would still miss.
