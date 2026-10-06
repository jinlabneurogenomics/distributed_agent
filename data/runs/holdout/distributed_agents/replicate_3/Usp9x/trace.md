# Reasoning trace for `151 TH Prkcd Grin2c Glut` DEG-count prediction

## Question and resolved ambiguities

The requested held-out manifest contains one target:

```tsv
target_name
Usp9x
```

I interpreted the endpoint as the integer count of measured genes whose
`pvals_adj` is below 0.05 after the `Usp9x` perturbation in the focal
`151 TH Prkcd Grin2c Glut` cell group. `Usp9x` itself was held out, so no
`Usp9x` rows from the differential-expression parquet or from the
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` endpoint table were used.
I treated the count as assay- and context-specific: the prediction should
reflect sparse AAV CRISPR loss in postnatal NeuN+ neuronal nuclei rather than
germline or Nestin/Emx1 conditional knockout phenotypes.

## Sources used

- Training endpoint file:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Held-out request manifest:
  `[local file: 258_Usp9x.csv]`.
- Distributed Agents same-experiment corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`, for frozen claims and
  perturbation-centered findings about represented Wnt, Notch, mTOR, and
  Zbtb38 comparators.
- Distributed Agents runtime profile tools, for focal-cell pairwise profile inspection
  among represented `Usp9x`-adjacent targets.
- NCBI PubMed literature searches for public mechanism evidence on USP9X.

The main external papers I used were:

- Murtaza et al., 2015, `10.1007/s00018-015-1851-0`, PMID 25672900:
  review of USP9X/FAM as a conserved substrate-selective deubiquitinase in
  development, cancer and neurologic disease.
- Stegeman et al., 2013, `10.1371/journal.pone.0068287`, PMID 23861879:
  neural-progenitor and dorsal-telencephalon Usp9x conditional knockout
  disrupts cortical architecture, hippocampal development and TGF-beta-linked
  axonogenesis.
- Premarathne et al., 2017, `10.1038/s41598-017-05451-5`, PMID 28808228:
  Usp9x ablation in embryonic neural progenitors perturbs beta-catenin/Wnt and
  Itch/Numb/Notch pathway components.
- Bridges et al., 2017, `10.1038/s41598-017-00149-0`, PMID 28341829:
  USP9X stabilizes RAPTOR and maintains mTORC1 signaling in neural progenitors.
- Yoon et al., 2019, `10.1016/j.neuron.2019.11.003`, PMID 31813652:
  USP9X maintains ankyrin-repeat protein homeostasis, including ankyrin-G, in
  postnatal spine development.
- Miotto et al., 2018, `10.1093/nar/gky149`, PMID 29490077:
  USP9X deubiquitinates and stabilizes ZBTB38, forming a
  USP9X/ZBTB38 axis that limits basal ROS and oxidative-stress toxicity.
- Koch et al., 2018, `10.3389/fncel.2017.00416`, PMID 29472843:
  Drosophila Fat facets and mammalian USP9X stabilize DSCAM1-linked axon growth
  signaling.

## Computational checks on the supplied data

1. I read the held-out manifest and confirmed that the only requested target
   was `Usp9x`.

2. I summarized the 1,674 non-held-out focal-cell training counts. The median
   count was 0, the 75th percentile was 1, the 90th percentile was 2, and the
   95th percentile was 18; 469/1,674 perturbations had any DEG at all. Thus a
   low single-digit count is already above the training median.

3. I inspected the parquet metadata to avoid loading all 616,253,184 rows. The
   `151 TH Prkcd Grin2c Glut` block covers row groups 547-579, with boundary
   rows in groups 546 and 580. A filtered `pyarrow.dataset` scan on
   `group_name == "151 TH Prkcd Grin2c Glut"` and selected comparator targets
   returned 17,259 measured features per comparator. Recounting
   `pvals_adj < 0.05` in those rows matched the training-count CSV.

4. I selected comparators by known USP9X substrates and pathways, then looked
   up their focal-cell counts:

```tsv
class	target	n_degs
USP9X/ZBTB38 substrate	Zbtb38	1
oxidative/chromatin relatives	Ehmt1	4
oxidative/chromatin relatives	Ctbp1	5
oxidative/chromatin relatives	Mecp2	16
Wnt core	Ctnnb1	383
Wnt core	Tcf7l2	106
Wnt core	Lrp6	4
Wnt core	Gsk3b	6
Wnt-adjacent negative controls	Lrp5	0
Wnt-adjacent negative controls	Atp6ap2	2
Wnt-adjacent negative controls	Amfr	1
Wnt-adjacent negative controls	Fbxw7	1
Wnt-adjacent negative controls	Prickle1	0
Notch/MIB1	Mib1	27
Notch/MIB1	Dll1	0
Notch/MIB1	Notch1	0
Notch/MIB1	Notch2	0
Notch/MIB1	Notch4	0
Notch/MIB1	Adam10	0
Notch/MIB1	Psen1	0
mTOR/RAPTOR	Rptor	0
mTOR/RAPTOR	Mtor	2
mTOR/RAPTOR	Tsc2	86
mTOR/RAPTOR	Akt3	0
ubiquitin core	Uba5	2677
ubiquitin core	Ufc1	572
ubiquitin core	Psmb4	742
ubiquitin core	Psmc1	430
substrate-selective ubiquitin enzymes	Huwe1	158
substrate-selective ubiquitin enzymes	Usp48	10
substrate-selective ubiquitin enzymes	Otud7a	0
substrate-selective ubiquitin enzymes	Ube3a	0
axon/ankyrin/cell adhesion	Dscam	0
axon/ankyrin/cell adhesion	Ank2	0
axon/ankyrin/cell adhesion	Ankrd11	20
axon/ankyrin/cell adhesion	Pcdh19	0
```

5. I ran a Distributed Agents runtime `profile_compare` for 26 represented nodes in
   these classes and a `profile_neighbors` search from `Ctnnb1`, `Lrp6`,
   `Mib1`, `Tsc2`, `Huwe1`, `Usp48`, `Rptor`, and `Dscam` against all 1,674
   training perturbations. The output was used as a guard against missing an
   obvious observed transcriptional neighborhood. It did not nominate a
   specific high-confidence `Usp9x` proxy: many whole-profile correlations among
   sparse/null signatures were driven by the zero-dominated genome-wide
   background, while the FDR-supported same-experiment corpus retained only
   restricted Wnt, Notch/Mib1, sterol, and mTOR claims.

## Target-specific biological reasoning

### `Usp9x`

USP9X is a large X-linked, substrate-selective deubiquitinase, not a proteasome
or ubiquitin-activating core enzyme. Its known biology made four classes of
training perturbations relevant.

**ZBTB38 / oxidative-stress axis.** Miotto et al. showed that USP9X stabilizes
ZBTB38 and that the USP9X/ZBTB38 axis buffers ROS. This is the most direct
transcriptional-substrate route in the supplied data because `Zbtb38` itself is
a represented training perturbation. In the focal cell group `Zbtb38` had only
1 DEG at the FDR 0.05 endpoint. The Distributed Agents corpus also describes
`Zbtb38` as a sparse P16 neuronal perturbation: only three FDR<0.10 genes across
two measured groups, with a small `151 TH Prkcd Grin2c Glut` up-signature
containing `Msra` and `Abhd12b`; Ctbp/Sox2/Mecp2 methyl-CpG comparators did not
phenocopy it. This argues that even if Usp9x loss destabilizes ZBTB38 in these
neurons, the RNA output should be very narrow.

**Wnt/beta-catenin and Notch.** Premarathne et al. placed Usp9x upstream of
beta-catenin/Wnt and Itch/Numb/Notch components in embryonic neural
progenitors. The same-experiment evidence does not support transferring a full
embryonic Wnt/Notch program into this P16-to-P37 postmitotic neuronal readout.
`Ctnnb1` is a strong positive control with 383 focal DEGs and `Tcf7l2` has 106,
so the assay can see a thalamic beta-catenin/TCF state. But `Lrp6` is only 4,
`Gsk3b` is 6, and the represented upstream/adaptor Wnt nodes are essentially
flat: `Lrp5` 0, `Atp6ap2` 2, `Amfr` 1, `Fbxw7` 1, and `Prickle1` 0. The
Distributed Agents corpus explicitly bounds the Lrp6/Ctnnb1 state as a branch-specific
thalamic Wnt response rather than a generic Wnt-family phenotype. On the Notch
side, `Mib1` has 27 focal DEGs, but its response is a SREBF2-like sterol module
uncoupled from canonical Notch transcription; `Dll1`, `Notch1`, `Notch2`,
`Notch4`, `Adam10`, and `Psen1` all have 0 focal DEGs. Therefore the embryonic
Usp9x-Wnt/Notch mechanism is a reason to expect at most a weak positive count,
not a Ctnnb1-like response.

**RAPTOR/mTORC1.** USP9X stabilizes RAPTOR in neural progenitors, but direct
`Rptor` perturbation is completely flat in the focal neurons and direct `Mtor`
loss gives only 2 focal DEGs. `Tsc2` loss, the opposite-sign hyperactive entry
into mTORC1, is stronger at 86 DEGs and has a sterol/lysosomal secondary state.
The same-experiment Mtor corpus findings emphasize that Rptor, Akt and PI3K
nodes are transcriptionally buffered rather than interchangeable with Mtor or
Tsc2 in this basal juvenile assay. This pushed the estimate downward.

**Ankyrin/Dscam/axon morphology and general ubiquitin biology.** Yoon et al.
and Koch et al. support USP9X effects on ankyrin-repeat and Dscam-linked axon
growth pathways, while Stegeman et al. found TGF-beta-linked axonogenesis
defects in developmental Usp9x knockout. Those are plausible protein-localized
or developmental phenotypes, but their represented focal-cell proxies do not
produce a broad nuclear RNA signature: `Dscam`, `Ank2`, and `Pcdh19` are 0 and
`Ankrd11` is 20. I also treated the huge `Uba5`/`Ufc1`/`Psmb4`/`Psmc1` counts
as counterexamples rather than analogs: they are core UFMylation or proteasome
perturbations and are much more global than a substrate-specific DUB. Among
closer ubiquitin-enzyme comparators, `Usp48` has 10 DEGs whereas `Otud7a` and
`Ube3a` have 0.

Putting those strands together, I chose a nonzero but single-digit count.
`Usp9x` has enough independent neuronal substrate biology that a completely
flat call seemed too strict, especially with the ZBTB38 oxidative axis in the
same cell group. However, every direct same-experiment route that is truly close
to a postmitotic, substrate-level USP9X consequence is sparse; the broad
training signatures are from direct beta-catenin loss, HUWE1, UFMylation, or
proteasome nodes rather than from DUB loss. I therefore set the point prediction
just below the `Usp48` comparator and above the `Lrp6`/`Mtor`/`Zbtb38` counts:

```tsv
target_name	predicted_n_degs
Usp9x	6
```

## Limits of the prediction

- There was no direct `Usp9x` context in the same-experiment Distributed Agents corpus,
  and `Usp9x` was intentionally absent from both the training parquet as a
  `gene_target` and the focal-cell training count table.
- Most USP9X mechanisms are protein-stability, localization, morphology, or
  progenitor-development mechanisms. The benchmark endpoint is a late,
  single-nucleus RNA count in surviving postmitotic NeuN+ neurons, so null or
  sparse RNA signatures do not imply that axons, spines, beta-catenin protein,
  RAPTOR protein, or Notch processing were unchanged.
- The best direct substrate comparator, `Zbtb38`, is itself sparse and its
  Usp9x connection comes from human cell oxidative-stress work rather than from
  thalamic glutamatergic neurons. The extrapolation from `Zbtb38` to `Usp9x`
  could miss other USP9X substrates.
- Conversely, high-count ubiquitin/proteasome and `Ctnnb1` comparators could
  be misleadingly large because they perturb pathway cores directly. I used
  them to establish assay capacity and as upper-bound counterexamples, not as
  expected phenocopies.
