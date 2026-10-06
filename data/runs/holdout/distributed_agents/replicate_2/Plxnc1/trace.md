# Prediction trace

## Question and resolved ambiguities

The run asks for an integer point prediction of `n_degs` for every gene in
`179_Plxnc1.csv`.  The manifest contains one held-out target:

| target_name |
|---|
| Plxnc1 |

I treated the endpoint as exactly the supplied focal-cell readout: the number of
measured genes with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei
after a sparse, acute AAV-PHP.eB CRISPR loss-of-function perturbation.  The
target was held out completely, so no `Plxnc1` perturbation rows were used or
available in either the DE parquet or the training endpoint CSV.

## Sources used

Internal and same-experiment sources:

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training endpoint counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Held-out manifest:
  `[local file: 179_Plxnc1.csv]`
- Distributed Agents corpus `perturbai-july-260713-sourceguard-1773-v1`, especially claim
  `claim:a7dd17e62ac7ac776021`, whose statement is that represented
  semaphorin-plexin-neuropilin perturbations do not form an interchangeable
  shared acute neuronal mRNA-signature module in this screen.
- Distributed Agents runtime profile comparison over the focal `Plxna1`, `Plxna2`,
  `Plxna4`, `Plxnd1`, `Nrp1`, `Nrp2`, `Sema4d`, `Sema5a`, and `Sema6a`
  signatures.

External biology:

- Liu et al. 2010, *Cell*, DOI `10.1016/j.cell.2010.07.040`, PMID 20727575:
  crystal structures of Sema7A and A39R complexes with PlexinC1, supporting
  Sema7A as a direct PlexinC1 ligand.
- Walzer et al. 2005, *Journal of Immunology*, DOI `10.4049/jimmunol.174.1.51`,
  PMID 15611227: mouse Plexin C1 engagement rearranges the actin cytoskeleton
  and inhibits dendritic-cell adhesion/migration through cofilin-dependent
  F-actin turnover.
- Scott et al. 2008, *Journal of Investigative Dermatology*, DOI
  `10.1038/jid.2008.329`, PMID 18987670: Sema7A signals through Plexin C1 to
  regulate cofilin and LIMK2 in melanocytic cells.
- Jongbloets et al. 2017, *Nature Communications*, DOI
  `10.1038/ncomms14666`, PMID 28281529: in the adult mouse dentate gyrus,
  Sema7A uses PlexinC1 on early neural progenitors and beta1-integrin receptors
  later during granule-cell differentiation.

## Computations over the training data

The focal training endpoint is sparse: among 1,674 non-held-out perturbations in
`151 TH Prkcd Grin2c Glut`, the median count is 0, the 75th percentile is 1, the
90th percentile is 2, and only the high tail reaches hundreds to thousands of
DEGs.  A predicted zero is therefore the prior mode, but I only used it after
checking pathway-specific evidence.

I filtered the endpoint table for represented plexin, semaphorin, neuropilin,
CRMP, and small-GTPase/cytoskeletal pathway perturbations.  I then filtered the
DE parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and these targets with
PyArrow predicates, and recomputed, per target, the number of rows with
`pvals_adj < 0.05`, the minimum adjusted p-value, matched nucleus counts, and
the most nominally shifted genes.  This avoids loading the whole 616 M-row
atlas while giving exact focal-cell evidence for the mechanistic analogs.

Key focal-cell analogs:

| training perturbation | focal `n_degs` | minimum `pvals_adj` in focal profile | matched perturbed nuclei | reason for comparison |
|---|---:|---:|---:|---|
| `Plxna1` | 0 | 1 | 229 | plexin receptor paralog in semaphorin signaling |
| `Plxna2` | 1 | 0.024 | 246 | Plexin-A receptor; sole FDR hit was the target gene `Plxna2` |
| `Plxna4` | 0 | 1 | 184 | Plexin-A receptor, canonical for Sema6A signaling |
| `Plxnd1` | 0 | 1 | 279 | distinct plexin receptor family member |
| `Nrp1` | 0 | 1 | 182 | semaphorin holoreceptor/co-receptor |
| `Nrp2` | 0 | 0.0689 | 115 | semaphorin/VEGF holoreceptor component |
| `Sema4d` | 0 | 0.189 | 165 | semaphorin ligand |
| `Sema5a` | 1 | 3.94e-09 | 258 | semaphorin ligand; sole strong FDR hit was `Sema5a` itself |
| `Sema6a` | 0 | 1 | 219 | semaphorin ligand for Plexin-A2/A4 |
| `Dpysl5` | 0 | 0.481 | 174 | CRMP family downstream of semaphorin pathways |
| `Limk1` | 0 | 1 | 226 | cofilin kinase near PlexinC1/Sema7A cytoskeletal output |
| `Cdc42` | 1 | 8.62e-05 | 122 | small GTPase/cytoskeletal effector; only its own RNA was significant |
| `Rac1` | 0 | 1 | 193 | small GTPase downstream of plexin pathways |
| `Rasa2` | 0 | 0.257 | 134 | RAS-GAP/R-Ras-proximal comparator |
| `Rapgef2` | 0 | 1 | 113 | Rap GTPase exchange factor, adhesion/cytoskeletal comparator |
| `Rapgef4` | 0 | 1 | 177 | Rap GTPase exchange factor, adhesion/cytoskeletal comparator |

I also inspected whether the analog perturbations transcriptionally fed back
onto `Plxnc1`, the Sema7A pathway, or assayed semaphorin/plexin genes.  Across
the same focal profiles, `Plxnc1`, `Sema7a`, `Limk1`, `Limk2`, `Cfl1`, `Rras`,
`Rasa1`, `Rasa2`, `Rac1`, `Cdc42`, `Nrp1`, `Nrp2`, `Plxna1`, `Plxna2`,
`Plxna4`, `Plxnd1`, and `Dpysl5` were all non-significant as measured features
except for `Plxna2` knockdown recovering `Plxna2` itself and `Cdc42` knockdown
recovering `Cdc42` itself.

In the runtime profile comparison of the nine direct semaphorin/plexin/
neuropilin profiles, seven of nine had zero FDR-significant genes and the other
two had one significant feature.  Among all 36 profile pairs, the median
overlap of the top 1% positive tails was only 0.05 and the median overlap of
the top 1% negative tails was 0.07; there was no same-direction FDR-significant
program overlap.  Thus even the weak nominal shifts do not reveal a recurrent
semaphorin-receptor transcriptomic state in the focal population.

The unavailable but biologically close perturbations are important negative
space: `Sema7a`, `Limk2`, `Cfl1`, `Rras`, `Rasa1`, `Plxna3`, and the Plexin-B
genes were not present as focal training targets.  `Itgb1`, the other major
Sema7A receptor route, was represented and had 0 focal DEGs.

## Target-specific rationale

### `Plxnc1`

`Plxnc1` encodes Plexin C1, a transmembrane receptor for Sema7A.  Direct ligand
binding is structurally established for Sema7A/PlexinC1 (Liu et al. 2010), and
PlexinC1 engagement is well linked to adhesion and actin/cofilin signaling
(Walzer et al. 2005; Scott et al. 2008).  There is also real CNS biology:
Sema7A-PlexinC1 limits proliferation of early neural progenitors in the adult
dentate gyrus, while Sema7A switches to beta1-integrin signaling during later
granule-cell dendrite and spine development (Jongbloets et al. 2017).

Those facts made semaphorin/plexin, neuropilin, CRMP, LIMK/cofilin, and
Ras/Rho/Rap cytoskeletal genes the appropriate training analogs.  They did not,
however, make a broad snRNA response likely in the exact assay.  The closest
represented single-receptor analogs were flat in the focal group: `Plxna1`,
`Plxna4`, and `Plxnd1` had 0 DEGs, while `Plxna2` had only its own transcript
as an FDR hit.  `Nrp1` and `Nrp2` were also 0.  Ligands and downstream
cytoskeletal comparators were at the same floor (`Sema4d` 0, `Sema6a` 0,
`Sema5a` 1 self-hit, `Dpysl5` 0, `Limk1` 0, `Rac1` 0, `Rasa2` 0, `Rapgef2` 0,
`Rapgef4` 0).  The Distributed Agents same-experiment corpus independently summarizes
these contrasts as pathway uncoupling rather than a hidden shared semaphorin
mRNA module.

My zero/nonzero decision was therefore driven primarily by within-dataset
evidence: every assayed neighboring receptor or ligand was zero or a singleton,
and the singletons were guide-target recovery rather than downstream pathway
state.  The external biology reinforces why these are the right neighbors, but
it also points toward local cytoskeletal phosphorylation, axonal geometry,
adhesion, and developmental/progenitor or immune-cell effects rather than a
large acute nuclear RNA program in postmitotic NeuN-enriched
`151 TH Prkcd Grin2c Glut` neurons.  I predict that `Plxnc1` loss will not push
any measured gene below focal-cell BH FDR 0.05.

Prediction: `Plxnc1 -> 0`.

## Limits of the reasoning

This is still an extrapolation because `Plxnc1` itself, its ligand `Sema7a`,
and several immediate Sema7A/PlexinC1 cytoskeletal nodes were held out or absent
from the perturbation universe.  The best training analogs are other plexins,
neuropilins, ligands, and pathway outputs, not the exact receptor-ligand pair.

snRNA-seq cannot measure the phosphorylation, Rho-family activity, F-actin,
adhesion, dendrite, spine, and axon-trajectory phenotypes that dominate
semaphorin-plexin biology.  The experiment also perturbs sparse postnatal
postmitotic neurons; it is not a germline developmental assay, not an adult
dentate progenitor assay, and not an immune/endothelial assay where PlexinC1 has
well-described functions.

Finally, a `0` versus `1` call is inherently fragile for this family because
two of the represented analogs had exactly one significant gene, their own
perturbed transcript.  If `Plxnc1` is expressed strongly enough in this focal
population for the guides to recover the target mRNA, the true count could be a
singleton.  The weight of the Plexin-A/Neuropilin evidence, where most self-RNA
changes also failed FDR after adjustment, kept the point prediction at zero.
