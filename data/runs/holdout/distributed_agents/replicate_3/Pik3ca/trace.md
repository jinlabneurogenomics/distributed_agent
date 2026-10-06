# Question and target set

The held-out endpoint is the number of genes with `pvals_adj < 0.05` after each
held-out CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut`
neurons. I interpreted `151 TH Prkcd Grin2c Glut` as a thalamic glutamatergic
class, not dopaminergic TH expression, and treated the point prediction as an
assay-calibrated DEG count rather than as a generic statement about whether the
gene is biologically important.

The requested-target manifest contained one target:

| target_name |
|---|
| Pik3ca |

`Pik3ca` was absent from both supplied training files, so I transferred from
measured perturbations of class IA PI3K subunits and the PI3K/AKT/mTOR axis.

# Sources used

- Input DEG-count training table:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input genome-scale DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 178_Pik3ca.csv]`.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially the Pik3cb, Pik3r1,
  Pik3r2, Akt3, Mtor, Igf1r and Tsc2 pathway-unavailability/pathway-uncoupling
  findings.
- PubMed literature for mechanism:
  - Rathinaswamy and Burke 2019, *Advances in Biological Regulation*,
    DOI `10.1016/j.jbior.2019.100657`, PMID `31611073`: class I PI3K catalytic
    isoforms are activated through regulatory subunits and distinct upstream
    inputs including RTKs, GPCRs and Ras-family GTPases.
  - Yu et al. 1998, *Molecular and Cellular Biology*,
    DOI `10.1128/MCB.18.3.1379`, PMID `9488453`, and Yu et al. 1998,
    *Journal of Biological Chemistry*, DOI `10.1074/jbc.273.46.30199`,
    PMID `9804776`: p85 regulatory subunits bind and regulate the p110alpha
    catalytic subunit, so Pik3r1/Pik3r2 perturbations are same-complex but not
    catalytic paralog controls for PIK3CA.
  - Dibble and Cantley 2015, *Trends in Cell Biology*,
    DOI `10.1016/j.tcb.2015.06.002`, PMID `26159692`: PI3K/AKT activates
    mTORC1 partly by regulating the TSC complex and Rheb at lysosomes.
  - Huang and Manning 2008, *Biochemical Journal*,
    DOI `10.1042/BJ20080281`, PMID `18466115`, and Huang and Manning 2009,
    *Biochemical Society Transactions*, DOI `10.1042/BST0370217`,
    PMID `19143635`: TSC1/TSC2 is a Rheb GAP and a negative regulator of
    mTORC1; AKT relieves the TSC brake, so Tsc2 loss has the opposite pathway
    sign from loss of an upstream PI3K catalytic subunit.
  - Mirzaa, Riviere and Dobyns 2013, *American Journal of Medical Genetics
    Part C*, DOI `10.1002/ajmg.c.31361`, PMID `23592320`, and Dobyns and
    Mirzaa 2019, *American Journal of Medical Genetics Part C*,
    DOI `10.1002/ajmg.c.31736`, PMID `31441589`: developmental megalencephaly
    syndromes involving `PIK3CA`, `PIK3R2`, `AKT3` and `MTOR` are largely
    activating PI3K/AKT/mTOR disorders, not direct models of a juvenile,
    postmitotic CRISPR loss-of-function readout.

# Computational evidence from the training data

The focal training-count file contained 1,674 non-held-out perturbations.
Counts were highly zero-inflated:

| count class | definition | targets |
|---|---:|---:|
| none | `n_degs = 0` | 1205 |
| weak | `1 <= n_degs < 10` | 363 |
| medium | `10 <= n_degs < 100` | 63 |
| strong | `n_degs >= 100` | 43 |

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for
PI3K/AKT/mTOR and RTK/RAS comparator targets and counted rows with
`pvals_adj < 0.05`. This uses the exact same definition as the requested
endpoint and also confirms that the zero-count analogs had recovered perturbed
nuclei in the focal class rather than being absent from the assay.

| training perturbation | focal `n_degs` | matched perturbed nuclei | role for Pik3ca |
|---|---:|---:|---|
| Pik3cb | 0 | 104 | closest available p110 catalytic paralog |
| Pik3r1 | 0 | 84 | p85alpha regulatory subunit, same class IA PI3K complex |
| Pik3r2 | 0 | 260 | p85beta regulatory subunit, same class IA PI3K complex |
| Akt3 | 0 | 108 | downstream AKT isoform |
| Rptor | 0 | 235 | mTORC1 scaffold |
| Mtor | 2 | 188 | downstream kinase; weak loss-of-function RNA effect |
| Tsc2 | 86 | 177 | downstream negative regulator; opposite pathway sign |
| Igf1r | 0 | 112 | receptor input to PI3K/AKT |
| Insr | 0 | 198 | receptor input to PI3K/AKT |
| Fgfr1 | 0 | 210 | RTK/RAS/PI3K input |
| Fgfr2 | 0 | 202 | RTK/RAS/PI3K input |
| Ptpn11 | 0 | 137 | SHP2 RTK/RAS adaptor |
| Sos1 | 0 | 210 | RAS guanine-nucleotide exchange factor |
| Kras | 0 | 97 | RAS-family PI3K/MAPK input |
| Hras | 0 | 162 | RAS-family PI3K/MAPK input |

The only FDR-significant genes in the direct downstream positive mTOR loss
surface were `Rims3` up and `Tmed8` down for `Mtor`. In contrast, `Tsc2` loss
had 86 focal DEGs, including mTOR-feedback and lipid/lysosomal genes such as
`Pik3r1`, `Pik3r3`, `Akt3`, `Ddit4`, `Cyp51`, `Msmo1`, `Ldlr`, `Atp6v0b`,
`Lamp2`, `Dpp7`, `Grn` and `Rragd`. The Distributed Agents corpus summarizes the same
distinction: upstream receptor/PI3K/AKT nodes are repeatedly transcriptionally
buffered in this basal postnatal neuronal assay, while the downstream TSC brake
can produce an interpretable mTORC1/SREBP/lysosomal program.

I also made an exact profile comparison among the 15 pathway anchors listed in
the table above. Thirteen had no significant genes; `Mtor` was the sole weak
profile and `Tsc2` the sole medium profile. The comparison did not reveal a
hidden FDR-supported same-complex module: all significant-program intersections
between the null PI3K anchors and the other selected pathway genes were empty.
Whole-profile correlations and top-tail overlaps among these nearly null
profiles were driven by non-significant tails, so I used them only as a check
against obvious convergence and not as quantitative support for a positive
prediction.

# Target-specific prediction

## Pik3ca

`Pik3ca` encodes p110alpha, a class IA PI3K catalytic subunit. The direct
paralog available in training, `Pik3cb`/p110beta, produced zero focal DEGs.
The same-complex regulatory subunits `Pik3r1`/p85alpha and `Pik3r2`/p85beta
also produced zero focal DEGs. Those three zeroes are the strongest
within-dataset evidence because they hit the same lipid-kinase complex rather
than merely a downstream branch.

The pathway-position controls push in the same direction. Receptor-proximal
inputs and adaptors feeding PI3K or RAS, including `Igf1r`, `Insr`, `Fgfr1`,
`Fgfr2`, `Ptpn11`, `Sos1`, `Kras` and `Hras`, were all flat in the focal class.
`Akt3`, the only represented AKT isoform, and `Rptor`, an mTORC1 scaffold, were
also flat. `Mtor` itself was detectable but only barely, with two focal DEGs.

`Tsc2` is the main counterexample: it had 86 focal DEGs and a clear mTOR-axis
response. I treated it as a detectability and sign counterexample rather than a
Pik3ca phenocopy. Mechanistically, p110alpha loss should reduce PI3K/PIP3/AKT
input to mTORC1, whereas Tsc2 loss removes an mTORC1 brake downstream of AKT;
the Distributed Agents corpus likewise treats direct PI3K-core flatness and downstream
Tsc2 activation as separated in the same Perturb-seq atlas.

External biology also argues against extrapolating from PIK3CA notoriety to a
large loss-of-function nuclear-RNA footprint. Brain-overgrowth disorders caused
by `PIK3CA`, `PIK3R2`, `AKT3` or `MTOR` are activating, often mosaic and
developmental; this experiment imposed a sparse postnatal CRISPR loss of
function in already postmitotic neurons. Because the measured p85 subunits,
p110beta, Akt3 and receptor inputs were all FDR-flat, the best calibrated
prediction is that `Pik3ca` falls into the zero class, not into the weak `Mtor`
class.

Prediction: `0` DEGs.

# Limits and extrapolation

`Pik3ca` itself, `Pten`, `Tsc1`, `Rheb`, `Akt1`, `Akt2`, `Rictor`, `Pik3r3`,
`Pik3cd` and `Pik3cg` were not in the training endpoint, so the full PI3K/AKT
module and catalytic-subunit redundancy could not be observed directly. p110alpha
can be more important than p110beta for receptor-tyrosine-kinase signaling, so
`Pik3cb` is a strong paralog comparator but not a perfect substitute. The assay
read out chronic nuclear RNA in recovered nuclei; it did not measure PIP3,
pAKT, pS6, cell size, local translation, dendrites, synapses or viability.
Therefore the `0` prediction means no expected BH-FDR 0.05 RNA genes in this
specific `151 TH Prkcd Grin2c Glut` endpoint, not absence of a protein-level or
morphological PI3K effect.
