## Question and resolved scope

The held-out manifest contains one requested perturbation, `Rnf13`. I interpreted the requested
quantity as a point prediction for:

`n_degs = count(pvals_adj < 0.05)` in `151 TH Prkcd Grin2c Glut` nuclei after acute P16
AAV-CRISPR loss of the target, counted over measured genes in the same Wilcoxon/BH table as the
training data.

`Rnf13` is absent from both supplied training inputs as a perturbation, so none of its true DEG
count or expression signature was used. I used the training parquet only for non-held-out
perturbations and treated self-RNA depletion as a legitimate DEG when it appeared in the supplied
endpoint, because the training `n_degs` endpoint counts measured genes rather than only downstream
genes.

## Sources

- Supplied training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Supplied all-cell differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 199_Rnf13.csv]`.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`.
- NCBI PubMed via the Distributed Agents literature search for RNF13 biology.

Selected external RNF13 mechanism references:

- Bocock et al. 2009, FEBS J, DOI: `10.1111/j.1742-4658.2009.06913.x`, PMID: 19292867:
  mouse RNF13 is a type-I endosomal/lysosomal membrane PA-TM-RING E3 ligase whose RING fragment
  can mediate ubiquitination after proteolytic release.
- Zhang et al. 2012, Cell Mol Life Sci, DOI: `10.1007/s00018-012-1103-5`, PMID: 22890573:
  germline Rnf13-null mice have hippocampal synaptic ultrastructure and spatial-learning defects,
  with RNF13-dependent K29 ubiquitination of snapin promoting SNAP-25 association.
- Arshad et al. 2013, J Biol Chem, DOI: `10.1074/jbc.M112.368829`, PMID: 23378536:
  RNF13 overexpression and knockdown in cultured cells linked RNF13 to ER-stress apoptosis upstream
  of the IRE1a-TRAF2-JNK axis.
- Lin et al. 2023, Nat Commun, DOI: `10.1038/s41467-023-42420-1`, PMID: 37857628:
  hepatocyte RNF13 can promote STING degradation and restrain innate inflammatory/lipid injury.
- Liu et al. 2024, Adv Sci, DOI: `10.1002/advs.202309560`, PMID: 39031743:
  macrophage RNF13 can promote LAMP1 degradation and modulate endolysosomal TLR signaling.
- Wang et al. 2024, Cell Commun Signal, DOI: `10.1186/s12964-024-01905-2`, PMID: 39511649:
  neuronal ischemia-reperfusion models linked RNF13 to p62/NRF2/HO-1 stress protection.

## Dataset checks

The focal training-count CSV has 1,674 non-held-out perturbations. Its endpoint is sparse:

- mean `n_degs`: 14.05
- median: 0
- 75th percentile: 1
- 90th percentile: 2
- 95th percentile: 18
- nonzero perturbations: 469 / 1,674

Thus most perturbations in this assay are exact zeroes; among nonzero calls, one self-transcript or
one singleton downstream feature is very common.

I then checked focal counts for mechanistically relevant training perturbations rather than using
all ubiquitin ligases as a bulk pool:

| perturbation | focal `n_degs` | reason for comparison |
| --- | ---: | --- |
| `Amfr` | 1 | ER membrane RING E3/ERAD ligase; same organelle class but not same substrate specificity |
| `Marchf6` | 14 | ER membrane RING E3 that induced a compact sterol program |
| `Arih1` | 7 | RBR/E3 proteostasis comparator with a narrow 151 response |
| `Trim2` | 2 | neuronal RING E3 family comparator |
| `Trim37` | 1 | RING E3 family comparator; self-only in the focal group |
| `Rnf216` | 0 | RING E3 comparator and negative control for family membership |
| `Rnf220` | 0 | RING E3 comparator and negative control for family membership |
| `Ube3a` | 0 | neuronal E3 comparator that was flat here |
| `Vcp` | 2 | ubiquitin-dependent ERAD/autophagy extractor, but not phenocopying p62/LC3 states |
| `Sqstm1` | 1 | p62 autophagy/NRF2 arm implicated in stress RNF13 literature |
| `Nfe2l2` | 0 | NRF2 arm implicated in stress RNF13 literature |
| `Atf6` | 0 | UPR sensor; negative control for textbook ER-stress pathway membership |
| `Hspa5` | 5 | positive ER-chaperone/ERAD stress control in this exact cell group |
| `Lamp2` | 0 | lysosome-membrane comparator |
| `Stxbp1` | 1 | synaptic vesicle release comparator |
| `Vamp1` | 1 | synaptic vesicle release comparator |
| `Cltc` | 3 | core endocytosis comparator |
| `Rab7` | 501 | positive late-endosome/lysosome stress control; much broader and more proximal |

I used the parquet to inspect the FDR-passing features for the closest observed analogs. The
results supported the count table:

- `Amfr` had one focal hit, `Amfr` itself, with logFC -1.04 and `pvals_adj = 8.0e-08`.
- `Sqstm1`, `Trim37`, `Stxbp1`, and `Vamp1` were also self-dominated singletons.
- `Marchf6` had 14 FDR genes, almost all sterol/SREBP genes: `Insig1`, `Dhcr24`, `Cyp51`,
  `Msmo1`, `Hmgcr`, `Fdft1`, `Hmgcs1`, `Ldlr`, `Fdps`, `Sqle`, `Srebf2`, `Idi1`,
  `Acsl4`, plus `Marchf6` itself.
- `Hspa5` had 5 FDR genes: ER-quality-control genes `Hsp90b1`, `Nfe2l1`, `Pdia4`,
  and `Derl3` were up, while `Erc1` was down.
- `Rab7` was qualitatively different, with 501 DEGs in the focal group and coherent
  endolysosomal, V-ATPase, sterol, ISR/UPR, autophagy/redox, proteasome and synaptic remodeling
  genes; `Rnf13` itself was up after `Rab7` perturbation
  (`logfoldchanges = 0.376`, `pvals_adj = 0.0059`).

For a profile sanity check, I compared the full focal logFC signatures of 18 observed
RNF13-adjacent perturbations with the Distributed Agents runtime `profile_compare`. Whole-profile Pearson
and cosine similarities among the very sparse E3/endosomal candidates were weakly positive but not
discriminating, because many profiles share thousands of near-zero or uncorrected measurements.
I therefore used the profile result only to reject strong opposition; I based the count estimate on
FDR breadth and mechanism.

## Internal corpus evidence

The Distributed Agents corpus had no direct `Rnf13` finding or claim, so the held-out target required
extrapolation from adjacent observed perturbations.

The corpus did have useful same-experiment annotations for several comparators:

- `Amfr` is an internally curated ER membrane E3 counterexample. The Amfr findings state that acute
  `Amfr` loss was transcriptionally buffered across 21 recovered neuronal groups; it did not induce
  a HSPA5/MANF-like UPR/ERAD program and did not induce the sterol/SREBP module that was clear
  after `Marchf6` loss.
- `Marchf6` is a positive but narrow ER E3 comparator. Its Distributed Agents findings identify a compact
  SREBP2/cholesterol-biosynthesis rebound in `151 TH Prkcd Grin2c Glut`, and explicitly note that
  this was not a generic ER-stress or ferroptosis program.
- `Hspa5` is the positive ER-stress control: HSPA5/BiP perturbation produced a detectable ER folding
  and ERAD RNA program, but the corpus also shows that `Atf6`, `Edem3`, `Nfe2l1`, `Nfe2l2`,
  `Sil1`, and `Vcp` did not simply reproduce it.
- `Sqstm1` is a p62/autophagy comparator. Its curated surface is very sparse; the corpus states
  that canonical NRF2/redox, lysosomal-autophagy, proteasome, UPR, and ISR marker transcripts were
  absent from the `Sqstm1` FDR surface.
- `Rab7` is the broad endolysosomal positive control. Its curated response is a late-endosomal and
  lysosomal compensation state with an added sterol/lipid branch and ISR/UPR-like stress layer,
  but the corpus also emphasizes that adjacent lysosomal, HOPS, V-ATPase, and autophagy targets
  often failed to phenocopy it at FDR level.
- `Arih1` is a small proteostasis/E3 responder; the corpus explicitly rejects a generic E3-ligase
  response by showing zero FDR-level overlap with `Rnf216`, `Trim2`, and `Trim37`.

## Target-specific reasoning

### Rnf13

`Rnf13` encodes a membrane-anchored PA-TM-RING E3 ligase that can localize to endosomal/lysosomal
and ER/Golgi compartments. That external biology makes several transcriptional states plausible on
paper:

- endosomal/lysosomal compensation, because RNF13 is an endosomal E3 and macrophage RNF13 was
  linked to LAMP1 and endolysosomal TLR degradation;
- ER stress, because RNF13 can interact with IRE1a and potentiate ER-stress apoptosis in cultured
  cells;
- p62/NRF2 and selective autophagy changes, because RNF13 was connected to p62 stabilization or
  recruitment in injury and antiviral contexts;
- synaptic vesicle dysfunction, because germline Rnf13-null hippocampi showed altered SNARE complex
  assembly through snapin.

The within-dataset evidence argues that most of those are not expected to become a broad durable
nuclear RNA program after the weak, mosaic P16 perturbation:

- The nearest same-organelle ER E3, `Amfr`, had exactly 1 focal DEG and was annotated in the
  internal corpus as missing both the HSPA5/MANF UPR program and the MARCHF6 sterol rebound.
- `Marchf6` had 14 focal DEGs, but its signature was a specific SREBP2/sterol regulon driven by its
  role in cholesterol-homeostasis ERAD. RNF13 is not known to control SREBP or sterol-sensor
  turnover, so `Marchf6` is better treated as a mechanistic counterexample than as a direct
  template.
- `Sqstm1` had exactly 1 focal DEG and `Nfe2l2` had 0, arguing against a constitutive p62/NRF2 RNA
  cascade in these young neurons.
- `Hspa5` had 5 focal DEGs and `Atf6` had 0. The assay can detect a BiP/ERAD response, but
  loss of individual ER-associated stress regulators does not automatically induce it.
- `Stxbp1` and `Vamp1` were singletons, and `Cltc` had only 3 genes. That makes a broad synaptic
  vesicle/endocytosis RNA state unlikely for an endosomal E3 whose synaptic role was assayed in
  germline hippocampus rather than in acute thalamic CRISPR.
- `Rab7` is the clear broad lysosome stress positive control and even up-regulates `Rnf13`, so
  Rnf13 may be a secondary marker of the Rab7 compensation state. But Rab7 loss is a proximal
  late-endosomal failure with 501 focal DEGs; many adjacent lysosomal and autophagy perturbations
  were 0-1 in the same endpoint, so up-regulation of Rnf13 downstream of Rab7 is not evidence that
  Rnf13 loss should phenocopy Rab7.

The expected response breadth for `Rnf13` is therefore much closer to `Amfr`, `Sqstm1`, `Trim37`,
`Stxbp1`, and `Vamp1` than to `Rab7`, `Marchf6`, or `Hspa5`. I nevertheless predict a nonzero
count rather than a hard zero because RNF13 is ubiquitously expressed, the Rnf13 measured gene was
detectable in the focal DE matrix and could pass in the `Rab7` profile, and several matched weak
E3/endosomal/synaptic perturbations registered only their own target transcript. My point estimate
is one FDR gene, most plausibly the target RNA itself with no broad downstream program.

Predicted `Rnf13` `n_degs`: **1**.

## Limits

- There was no direct same-experiment Distributed Agents finding for `Rnf13` and no observed Rnf13
  perturbation signature; this is an extrapolation from nearby but imperfect biology.
- The training set lacked a true RNF13 paralog or its direct neuronal substrate `Snapin`; Rnf216,
  Rnf220, Trim-family, Arih1 and Ube3a comparisons are E3 controls rather than same-complex
  controls.
- RNF13 has multiple reported substrates or partners, including STING, p62, LAMP1, snapin and
  IRE1a, but those data come from hepatocytes, macrophages, ischemia, cultured stress models or
  germline hippocampus. The focal assay is an acute, sparse CRISPR perturbation in surviving
  juvenile NeuN+ neurons, so stress-induced and non-neuronal roles may be silent.
- A zero-vs-one decision is dominated by whether Rnf13 self RNA is sufficiently expressed and
  depleted to cross BH FDR. DNA indel burden and RNF13 protein depletion were not measured.
- Transient ER stress, lysosomal flux changes, synaptic physiology, or protein-level substrate
  accumulation could occur without leaving any P37-P44 nuclear RNA genes below FDR 0.05.
