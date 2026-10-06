# DEG-count prediction trace

## Question and resolved ambiguities

I interpreted the requested endpoint as:

* Predict an integer `n_degs` for every row of
  `[local file: 094_Gns.csv]`.
* The endpoint is the number of measured genes with `pvals_adj < 0.05` after
  Wilcoxon differential expression in `151 TH Prkcd Grin2c Glut`.
* The held-out target for this run is exactly one perturbation, `Gns`; it is
  absent from both the training DE parquet as a `gene_target` and from the
  focal-cell training count CSV.
* I treated `n_degs` as a response-breadth readout of this specific sparse,
  postnatal, neuronal CRISPR/snRNA-seq assay. I did not treat it as a direct
  measurement of lysosomal storage, survival, editing efficiency, or chronic
  disease severity.

## Sources used

Internal same-experiment data:

* `training_de_all_cell_groups.parquet`
* `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
* The Distributed Agents corpus MCP release
  `perturbai-july-260713-sourceguard-1773-v1`, especially:
  * `claim:56e1e77cd2cb9bb6604f`: represented lysosomal disease, hydrolase,
    cargo, NCL, M6P, and PSAP perturbations do not induce a shared acute
    neuronal lysosomal-storage, TFEB/MiT, autophagy, ISR, or UPR mRNA program.
  * `claim:5fdbbedd98372e9e8eca`: represented GAG/heparan-sulfate/proteoglycan
    perturbations do not collapse into a common acute postnatal neuronal
    transcriptomic module.
* Distributed Agents runtime profile diagnostics generated from the focal-cell parquet
  for the hand-picked lysosomal/GAG/endolysosomal calibrator panel.
* The local Distributed Agents gene-annotation tables
  `genes.parquet`, `gene_membership.parquet`, and `gene_relationships.parquet`.
  These linked `Gns` to Gene Ontology heparan-sulfate proteoglycan catabolism
  and N-acetylglucosamine-6-sulfatase activity, KEGG
  `mmu00531`/`mmu04142`, and Reactome GAG/lysosomal metabolism terms. The
  exported annotation parquet exposes database names and accessions but not
  all upstream database version strings, so I used these as pathway membership
  annotations rather than as numeric evidence.

External biological literature:

* Mok et al. 2003, Genomics, DOI `10.1016/s0888-7543(02)00014-9`,
  PMID `12573255`: GNS encodes N-acetylglucosamine-6-sulfatase and pathogenic
  GNS loss causes mucopolysaccharidosis type IIID/Sanfilippo D.
* Jansen et al. 2007, Archives of Neurology,
  DOI `10.1001/archneur.64.11.1629`, PMID `17998446`, and Valstar et al. 2010,
  Human Mutation, DOI `10.1002/humu.21234`, PMID `20232353`: MPS IIID is a
  progressive neurologic lysosomal storage disorder caused by GNS mutations.
* Jakobkiewicz-Banecka et al. 2016, Frontiers in Bioscience,
  DOI `10.2741/4463`, PMID `27100513`: MPS III subtypes all involve failed
  heparan-sulfate degradation through `SGSH`, `NAGLU`, `HGSNAT`, or `GNS`.
* Roca et al. 2017, Human Molecular Genetics, DOI `10.1093/hmg/ddx058`,
  PMID `28334745`, and Takahashi et al. 2021, Molecular Genetics and
  Metabolism, DOI `10.1016/j.ymgme.2021.11.010`, PMID `34844863`: constitutive
  mouse `Gns` knockout causes chronic CNS lysosomal storage, lysosomal
  homeostasis defects, neuroinflammation, and LAMP1/CD68/GFAP pathology.
* Wang et al. 2020, Molecular Pharmaceutics,
  DOI `10.1021/acs.molpharmaceut.0c00831`, PMID `33320673`: recombinant human
  GNS can be taken up through the mannose-6-phosphate receptor and rescue GAG
  accumulation in MPS IIID fibroblasts, consistent with cross-correction of a
  soluble lysosomal enzyme.

## Same-experiment computations

I loaded the focal count CSV and used the focal-cell training distribution to
calibrate the dynamic range. It contains 1,674 non-held-out targets; 1,205 had
`n_degs = 0`, the median was 0, the 75th percentile was 1, and the response
tail was dominated by RNA-processing, transcriptional, and proteostasis genes
such as `Uba5` with 2,677 DEGs, `Tpr` with 1,768, and `Sin3a` with 1,433.

I then filtered the DE parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and a biologically selected set of
lysosomal hydrolase, GAG/proteoglycan, autophagy, V-ATPase, mTOR, and sterol
targets. For each candidate analog I recomputed
`sum(pvals_adj < 0.05)` over the filtered rows and inspected the top adjusted
P values to distinguish real downstream programs from isolated self-transcript
hits. The filter returned 17,259 measured genes per selected training target;
matched perturbed-cell counts for the close soluble hydrolase and GAG analogs
were 121 to 255 nuclei versus 23,679 controls, so the null calls were not
caused by a missing focal-cell readout.

Key focal counts were:

| calibrator class | training perturbations in `151 TH Prkcd Grin2c Glut` |
| --- | --- |
| Soluble hydrolase, cargo, M6P and lysosomal disease controls | `Gnptab 0`, `Gnptg 0`, `Manba 0`, `Sort1 0`, `Gaa 1`, `Ppt1 1`, `Psap 1`, `Ctsb 1`, `Tmem106b 1` |
| GAG / heparan-sulfate / proteoglycan controls | `B3gat3 0`, `Ext1 0`, `Ext2 0`, `Glce 0`, `Gpc6 0`, `Hs6st2 0`, `Xylt1 0`, `Bpnt2 1` |
| Mechanistic counterexamples in broader endolysosomal regulation | `Rab7 501`, `Tsc2 86`, `Depdc5 13`, `Srebf2 7`, `Rb1cc1 4`, `Atp6ap2 2`, `Atp6v0a1 1`, `Atg5 0`, `Atg16l1 0`, `Becn1 0` |

The one-DEG soluble hydrolase calls were mostly just target RNA depletion:
`Gaa`, `Ppt1`, `Psap`, `Ctsb`, `Tmem106b`, and `Bpnt2` each had the perturbed
target itself as the only FDR-passing gene. Comparable nodes were also able to
miss even target self-depletion at FDR 0.05, for example `Gnptg`, `Manba`,
`Sort1`, and the near-threshold `Ext2` row. Because the experiment reports only
modest average on-target mRNA downregulation per guide, a `Gns` self-hit is not
safe to assume even though `Gns` is in the measured gene set.

I also ran a Distributed Agents runtime signed-profile comparison on 18 selected
lysosomal/GAG/endolysosomal targets using `logfoldchanges` as the signed value
and `pvals_adj < 0.05` as the significance threshold. Within this deliberately
enriched cohort the mean top-100 feature overlap coefficient was only 0.043 for
positive tails and 0.079 for negative tails, and the flat hydrolase/GAG nodes
shared essentially no significant downstream program. The few strongly
nonzero nodes, especially `Rab7`, `Tsc2`, `Depdc5`, and `Srebf2`, formed a
sterol/mTOR/endolysosomal regulatory branch rather than a soluble hydrolase
storage branch, so I used them as evidence that the assay can detect some
endolysosomal biology but not as direct `Gns` count anchors.

## Target-specific reasoning

### `Gns`

`Gns` encodes a soluble lysosomal sulfatase required for stepwise degradation
of heparan sulfate; complete inherited GNS deficiency causes Sanfilippo D/MPS
IIID. The closest disease analogs would be `Sgsh`, `Naglu`, and `Hgsnat`, the
other Sanfilippo heparan-sulfate degradation enzymes, but none of those genes
was a training perturbation in this screen. I therefore anchored the prediction
on adjacent same-assay groups.

The most appropriate in-dataset analogs are the flat soluble lysosomal
hydrolase and lysosomal cargo perturbations. `Manba` is a soluble lysosomal
glycosidase for a storage disease and had `0` DEGs; `Gnptab` and `Gnptg` affect
M6P-dependent lysosomal enzyme tagging and had `0`; `Sort1`, another lysosomal
cargo-trafficking node, had `0`; and direct lysosomal cargo/hydrolase targets
`Gaa`, `Ppt1`, `Psap`, and `Ctsb` only showed one DEG apiece, their own
transcripts. Distributed Agents corpus claim `claim:56e1e77cd2cb9bb6604f` summarizes
the same-experiment neighborhood in the same direction: represented hydrolase,
M6P, NCL, cargo, PSAP, and `Tmem106b` perturbations did not induce a shared
TFEB, autophagy, UPR/ISR, or lysosomal-storage nuclear RNA program in acute
juvenile neurons. This is a close assay match for `Gns` because GNS is also a
soluble lysosomal enzyme, its disease phenotype requires substrate storage,
and soluble hydrolases can be buffered in a mosaic setting by enzyme supplied
from neighboring unedited cells.

The second, somewhat more distant, same-assay analog set is the heparan-sulfate
and proteoglycan pathway. `Gns` acts in degradation rather than Golgi
biosynthesis, so I treated `B3gat3`, `Xylt1`, `Ext1`, `Ext2`, `Glce`,
`Hs6st2`, `Gpc6`, and `Bpnt2` as boundary evidence, not one-to-one surrogates.
In the focal cell group, seven of those eight targets had `0` DEGs and the
eighth, `Bpnt2`, had only its own transcript. Distributed Agents corpus
`claim:5fdbbedd98372e9e8eca` likewise found that represented
GAG/heparan-sulfate/proteoglycan perturbations were flat, sparse,
near-orthogonal, or cell-group-specific rather than a common acute neuronal
signature.

There are positive lysosome-adjacent counterexamples: `Rab7` produced 501
DEGs, `Tsc2` 86, `Depdc5` 13, and `Srebf2` 7 in the focal cell group. I did
not transfer those counts to `Gns`. `Rab7` is a late-endosome small GTPase;
`Tsc2` and `Depdc5` impinge on mTORC1; and `Srebf2` directly controls the
sterol program. Their expression signatures include sterol/endolysosomal or
mTOR/SREBP states that are topologically and functionally separated from the
flat hydrolase and GAG controls.

External mouse and human genetics say severe, constitutive `Gns` loss is
neurodegenerative over months or years, but the held-out endpoint is 3 to
4 weeks after sparse postnatal AAV CRISPR in sorted NeuN+ nuclei. That design
removes much of the glial compartment that dominates chronic storage
pathology and leaves wild-type neighboring cells that may cross-correct a
secreted, M6P-tagged enzyme. The central extrapolation is therefore from
chronic storage disease to a short mosaic neuronal transcriptomic assay; the
same-experiment evidence says that extrapolation should be conservative.

Final point prediction: `Gns = 0`. A one-gene self-RNA hit is plausible if GNS
is efficiently depleted in the recovered nuclei, but the related hydrolase
surface contains several zeroes and no downstream stress program, so the best
integer call is no FDR 0.05 DEGs.

## Limits of the reasoning

* The closest Sanfilippo genes, `Sgsh`, `Naglu`, and `Hgsnat`, were not assayed
  as training perturbations, so `Gns` required extrapolation from other soluble
  hydrolases and from GAG biosynthesis genes.
* The DE readout is nuclear RNA only. It cannot verify GNS enzyme loss,
  heparan-sulfate accumulation, lysosomal pH, LAMP1 protein, or
  cross-correction.
* Some hydrolase analogs had weak apparent target mRNA depletion, so a zero
  could reflect buffering, weak knockdown, or both. The repeated flatness
  across strongly self-depleted targets such as `Gaa`, `Ppt1`, `Psap`, `Ctsb`,
  `Tmem106b`, and `Bpnt2` makes a broad `Gns` response unlikely, but it does
  not prove that all guides edited equally well.
* Chronic germline `Gns` knockout mouse phenotypes involve intact multicellular
  tissue and aging storage burden. Those data are strong mechanistic evidence
  for GNS function, but weak quantitative evidence for this sparse acute
  postnatal neuron endpoint.
