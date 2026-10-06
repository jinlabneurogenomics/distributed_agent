# Held-out target

The run manifest contains one held-out perturbation:

| target_name |
|---|
| Tnfrsf1b |

I interpreted the task as a point prediction of the focal-cell endpoint
`n_degs`, the count of genes with `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` after sparse postnatal AAV CRISPR loss of the
requested mouse gene. I treated the all-cell differential-expression parquet
and the focal training-count CSV as the primary calibration data, and used
external pathway knowledge only to choose which observed perturbations were
mechanistically analogous to `Tnfrsf1b`.

The only ambiguity I needed to resolve was how to handle an exactly flat
same-pathway training neighborhood. I used `0` as a literal prediction when the
closest receptor-side and downstream pathway perturbations were all FDR-null in
the focal group, rather than assigning a small positive value from the global
training prior.

# Sources

- Input training DEG counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Input per-gene DE statistics:
  `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest:
  `[local file: 243_Tnfrsf1b.csv]`
- Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile comparison over the focal-cell DE profiles
- PubMed-indexed TNF/TNFR literature, used for external pathway context:
  Wajant and Scheurich 2011, DOI `10.1111/j.1742-4658.2011.08015.x`,
  PMID `21232017`; Medler, Kucka, and Wajant 2022, DOI
  `10.3390/cancers14112603`, PMID `35681583`; Siegmund, Zaitseva, and
  Wajant 2023, DOI `10.3389/fcell.2023.1267837`, PMID `38020877`;
  Carney et al. 2025, DOI `10.1016/j.bbi.2025.07.006`, PMID `40651585`.

# Dataset checks

I verified that `Tnfrsf1b` is absent from the training perturbation universe, as
expected for a held-out target. The focal-cell training CSV has 1,674 observed
perturbations; the endpoint is highly zero-inflated, with median `n_degs = 0`,
75th percentile `1`, 90th percentile `2`, and a nonzero rate of 28.0%.

I then filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and counted
`pvals_adj < 0.05` per training perturbation for literature-selected TNF/TNFR,
NF-kB, TLR/IL-1, and death-receptor comparators. The focal slice contained
1,674 targets by 17,259 measured genes. All of the following biologically
nearby perturbations had exactly zero focal DEGs:

| comparator | focal n_degs | why it was informative |
|---|---:|---|
| Tnfrsf1a | 0 | closest observed TNF receptor; TNFR1 uses TRAF2/cIAP/RIPK1 to reach IKK/NF-kB |
| Tnfrsf11a, Tnfrsf13c, Tnfrsf4, Tnfrsf9 | 0 each | other represented TNFR-superfamily receptors that could have revealed a generic neuronal TNFRSF state |
| Cd40 | 0 | TNFRSF receptor that couples to TRAF adaptors and NF-kB |
| Traf3 | 0 | represented TRAF adaptor and TNFR/TLR regulator |
| Chuk, Map3k7, Nfkb1, Rel | 0 each | TAK1/IKK/NF-kB downstream nodes expected to move if a basal TNF-like transcriptional circuit were active |
| Tlr2, Tlr3, Tlr4, Tlr5, Tlr7, Tlr8 | 0 each | innate receptors converging on AP-1/NF-kB/IRF modules; useful counterexamples to a hidden inflammatory response |
| Il1r1, Il1rap | 0 each | IL-1 receptor arm converging on TAK1 and NF-kB |
| Cyld, Otulin | 0 each | ubiquitin regulators of NF-kB receptor signaling |
| Fas, Cd27, Bcl2 | 0 each | death-receptor/survival comparators testing whether TNFR-family loss induced an apoptosis-toned program |
| Mapk1, Mapk9, Map2k6 | 0 each | ERK/JNK/p38-side MAPK comparators for a possible TNFR-MAPK output |

The parquet also contains `Tnfrsf1b` as a measured RNA feature for all 1,674
training perturbations in the focal group, but its minimum adjusted p-value
across those signatures was `1.0`. Thus there was no detectable secondary
movement of endogenous `Tnfrsf1b` in this focal cell group.

# Profile and corpus evidence

I asked the Distributed Agents runtime to compare the full signed focal-cell
`logfoldchanges` profiles for a 20-target TNF/TLR/NF-kB neighborhood:

`Tnfrsf1a, Traf3, Nfkb1, Rel, Map3k7, Chuk, Cd40, Tlr2, Tlr3, Tlr4, Tlr5,
Tlr7, Tlr8, Il1r1, Il1rap, Cyld, Otulin, Fas, Tnfrsf13c, Tnfrsf11a`

Every one of the 20 profiles had `response_activity_status =
no_significant_features` at FDR 0.05. For the 190 pairwise contrasts within
that cohort, the significant-program overlap count was zero by construction:
there were no FDR genes to share. `Tnfrsf1a` likewise had zero significant
positive features and zero significant negative features over all 17,259 focal
genes; its pairwise contrasts with `Traf3`, `Nfkb1`, `Rel`, `Map3k7`, `Chuk`,
`Cd40`, `Tlr2`, `Tlr3`, `Tlr4`, and `Il1r1` had no significant intersections in
either direction.

The same-experiment Distributed Agents corpus independently summarized this region of
the screen as a pathway-level absence, not a lone negative result:

- `Tnfrsf1a:F001` reported pan-neuronal absence of robust downstream DE after
  acute `Tnfrsf1a` loss; `Tnfrsf1a:F002` reported absence of a basal TNF/NF-kB
  immediate program and flat measurable `Chuk`, `Cyld`, `Map3k7`, `Nfkb1`, and
  `Traf3` neighbors.
- `Traf3:F001` and `Traf3:F004` reported a pan-neuronal `Traf3` null and no
  convergence among represented TNFR/TLR/NF-kB relatives.
- `Nfkb1:F001` and `Nfkb1:F002` reported zero robust DE after `Nfkb1`
  perturbation and matching flatness of available `Rel`, IKK/TAK1, TLR, and
  TNFR comparators.
- `Rel:F001` and `Rel:F002` reported no robust downstream response after
  `Rel` loss and no strong cross-perturbation NF-kB neighbor.
- `Map3k7:F001` and `Map3k7:F003` reported a `Map3k7` null and broad
  transcriptional silence of the represented TLR/IL-1/TNF-to-TAK1-to-NF-kB,
  JNK, and p38 axis.
- In a 12-target corpus topology check over `Cd40`, `Chuk`, `Il1r1`,
  `Il1rap`, `Map3k7`, `Nfkb1`, `Rel`, `Tlr2`, `Tlr3`, `Tlr4`, `Tnfrsf1a`, and
  `Traf3`, all 12 nodes fell into a single component with 49 of 66 possible
  pairs connected by explicit finding references or shared claims. This was not
  used as an automatic score, but it confirmed that the hand-selected
  comparator set was the same TNF/TIR/NF-kB neighborhood repeatedly discussed
  in same-experiment reports.

# Tnfrsf1b rationale

`Tnfrsf1b` encodes TNFR2, the second TNF receptor. External work places TNFR2
within the same receptor superfamily as TNFR1 and CD40 and shows that TNFR2
signals through TRAF2 with cIAP1/2 to influence classical and alternative
NF-kB, MAPK, and TNFR1 death/survival signaling; by contrast with TNFR1, it is
most prominent in activated immune cells such as Tregs and can modulate
TNFR1-driven outcomes through TRAF2/cIAP availability rather than simply acting
as another constitutive death-domain receptor (Medler et al. 2022; Siegmund et
al. 2023). TNFR1 itself reaches IKK/NF-kB through TRADD/RIPK1/TRAF2/cIAP
complexes (Wajant and Scheurich 2011). TNFR2 can also have CNS-relevant roles
in non-neuronal cells: astrocyte-selective `Tnfrsf1b` deletion altered sorted
astrocyte RNA programs and hippocampal physiology in a conditional mouse model
(Carney et al. 2025).

Those facts make `Tnfrsf1b` biologically plausible in TNF-responsive cells but
make a strong focal neuronal response unlikely in this experiment. The assay
was an unchallenged, NeuN-enriched, sparse P16-to-P37/44 neuronal CRISPR
readout, and the same dataset directly shows that:

1. the closest observed TNF receptor, `Tnfrsf1a`, was 0 in the focal cell
   group;
2. five other represented TNFRSF-side receptor perturbations were also 0;
3. the represented TRAF/TAK1/IKK/NF-kB path from receptor to nucleus was 0; and
4. TLR and IL-1 receptor perturbations that would reuse the same AP-1/NF-kB
   transcriptional endpoints were also 0.

The zero call is therefore mostly driven by the within-dataset null TNF/NF-kB
neighborhood. External knowledge contributes the interpretation that TNFR2
biology is ligand-, lineage-, and state-gated, so the lack of response in young
NeuN-positive neurons is not surprising and should not be overruled by TNFR2's
importance in immune cells, glia, or TNF-stimulated systems.

Prediction: `Tnfrsf1b -> 0`.

# Limits

- `Tnfrsf1b` was held out, so there is no direct `Tnfrsf1b` perturbation
  expression signature in either input table.
- The closest absent perturbations include `Traf2`, `Traf5`, `Birc2`, `Birc3`,
  `Rela`, `Relb`, `Nfkb2`, `Ikbkb`, `Ikbkg`, `Tnfaip3`, and the `Tnf` ligand;
  the prediction leans on available pathway representatives.
- This is a basal neuronal endpoint. It does not test soluble or membrane TNF
  stimulation, injury, infection, aging, systemic cytokine feedback, Tregs,
  endothelium, astrocytes, or microglia.
- Weak target mRNA down-regulation in this AAV CRISPR platform cannot prove or
  disprove DNA editing or protein depletion for any individual target.
- Whole-vector correlations among all-zero profiles can share low-count ranking
  noise. I used them only to confirm absence of significant-program overlap;
  the point prediction comes from FDR counts and mechanistic comparators.
