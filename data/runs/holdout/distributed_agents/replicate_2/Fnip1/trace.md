# FNIP1 DEG-count prediction

## Question and endpoint

I interpreted the requested endpoint as the integer `n_degs` that would have
been observed for a held-out `Fnip1` CRISPR loss-of-function perturbation in
`151 TH Prkcd Grin2c Glut`: the number of measured mouse genes with Wilcoxon
Benjamini-Hochberg `pvals_adj < 0.05` in perturbed nuclei versus the matched
non-targeting controls. The held-out `Fnip1` signature itself is absent, so I
used only non-held-out perturbations in the training parquet and training
count CSV.

The main ambiguity was sign. FNIP1 participates in FLCN-FNIP RagC/D regulation
of amino-acid mTORC1 and in AMPK/TFEB control; loss of `Fnip1` is therefore
not simply equivalent to `Tsc2` or `Depdc5` loss, even though all three genes
touch mTOR/lysosome biology. I treated `Tsc2`, `Depdc5`, and `Rab7` as positive
examples that the assay can detect a sterol/endolysosomal state when it is
strongly engaged, and treated `Mtor`, `Rptor`, AMPK, lysosomal-storage, and
core-autophagy perturbations as boundary cases for loss of the FLCN-FNIP arm.

## Sources used

- `training_de_all_cell_groups.parquet`, filtered to
  `group_name == "151 TH Prkcd Grin2c Glut"` for candidate perturbations and
  compared by focal-gene log2 fold-change vectors and `pvals_adj < 0.05`.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` for the endpoint
  distribution and exact focal-cell training counts.
- `077_Fnip1.csv`, which contains only `Fnip1`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`. The corpus had no `Fnip1`
  target card, but it had curated same-experiment findings for `Tsc2`,
  `Depdc5`, `Mtor`, AMPK, autophagy, and lysosomal comparator perturbations.
- PubMed literature on the FLCN/FNIP complex, AMPK, RagC/D, and TFEB/TFE3:
  Baba et al. 2006, DOI `10.1073/pnas.0603781103`, PMID `17028174`;
  Hasumi et al. 2008, DOI `10.1016/j.gene.2008.02.022`, PMID `18403135`;
  Tsun et al. 2013, DOI `10.1016/j.molcel.2013.09.016`, PMID `24095279`;
  Meng and Ferguson 2018, DOI `10.1083/jcb.201712177`, PMID `29848618`;
  Ramirez et al. 2019, DOI `10.4049/jimmunol.1900395`, PMID `31676673`;
  Napolitano et al. 2020, DOI `10.1038/s41586-020-2444-0`,
  PMID `32612235`; Malik et al. 2023, DOI `10.1126/science.abj5559`,
  PMID `37079666`.

## Computation over the supplied data

The manifest has exactly one requested target, `Fnip1`.

The focal training endpoint has 1,674 non-held-out perturbations:

| DEG-count class | Definition | Count |
|---|---:|---:|
| none | `n_degs == 0` | 1,205 |
| weak | `1 <= n_degs < 10` | 363 |
| medium | `10 <= n_degs < 100` | 63 |
| strong | `n_degs >= 100` | 43 |

I then queried obvious FLCN/FNIP-adjacent perturbations in the count table and
loaded their focal-cell DE rows from the parquet:

```python
df = pd.read_parquet(
    "training_de_all_cell_groups.parquet",
    columns=["names", "gene_target", "group_name",
             "logfoldchanges", "pvals_adj", "pvals", "scores"],
    filters=[
        ("group_name", "==", "151 TH Prkcd Grin2c Glut"),
        ("gene_target", "in", analog_targets),
    ],
)
sig = df[df.pvals_adj < 0.05]
```

For expression-pattern evidence I counted significant up/down genes for each
training analog, intersected FDR-significant sets in matched direction, and
looked at full-vector Spearman correlations of `logfoldchanges` across the
17,259 measured genes. Those correlations were used only as a weak diagnostic:
the corpus and the FDR overlaps were more informative than raw whole-vector
similarity, because many near-flat perturbations share diffuse low-amplitude
background structure.

## FNIP1 target-specific reasoning

### What FNIP1 should do biologically

`Fnip1` encodes folliculin-interacting protein 1. FNIP1 and FNIP2 bind FLCN
and AMPK (Baba et al. 2006; Hasumi et al. 2008). The FLCN-FNIP complex is a
RagC/D GAP needed to coordinate Rag heterodimer nucleotide state during
amino-acid signaling to mTORC1 (Tsun et al. 2013; Meng and Ferguson 2018).
This places FNIP1 near lysosomal amino-acid sensing, but loss of the complex is
not just "mTORC1 on": loss of FLCN/FNIP can selectively release TFEB/TFE3 from
lysosomal mTORC1 phosphorylation, inducing autophagy/lysosome programs in
contexts where the pathway is sufficiently engaged (Ramirez et al. 2019;
Napolitano et al. 2020). AMPK can also phosphorylate FNIP1 to suppress
FLCN-FNIP and drive TFEB-dependent lysosomal and mitochondrial biogenesis
after energetic stress (Malik et al. 2023).

That biology made me compare `Fnip1` to three types of training perturbation:

- negative regulators that derepress mTORC1 or the sterol/endolysosomal arm
  (`Tsc2`, `Depdc5`);
- core positive mTORC1 and AMPK inputs (`Mtor`, `Rptor`, `Prkaa2`, `Prkag2`,
  `Strada`);
- autophagy, lysosome, late-endosome, and lysosomal-storage nodes
  (`Rb1cc1`, `Atg5`, `Atg16l1`, `Becn1`, `Rubcn`, `Map1lc3a`, `Sqstm1`,
  `Lamp2`, `Rab7`, `Tmem106b`, `Gnptab`, `Manba`, `Ppt1`, `Psap`, `Sort1`).

`Flcn`, `Fnip2`, `Rragc`, `Rragd`, `Tfeb`, and `Tfe3` were not available as
training perturbations, so no same-complex or direct MiT/TFE knockout existed.

### In-dataset analogs and counterexamples

| Training perturbation | Focal `n_degs` | Expression-pattern evidence | How I used it |
|---|---:|---|---|
| `Depdc5` | 13 | 10 up, 3 down. Top hits included `Pik3r1`, `Ldlr`, `Pik3r3`, `Tubb3`, `Insig1`, and `Hmgcs1`. It shared 8 same-direction FDR genes with `Tsc2`, including `Ldlr`, `Msmo1`, `Pik3r1`, `Pik3r3`, and `Tubb3`. | Partial positive analog for amino-acid mTORC1 activation through the GATOR/Rag axis. Not a direct FNIP1 analog because `Depdc5` loss activates RagA/B and converges with FLCN-FNIP to promote an active Rag state, whereas `Fnip1` loss removes the FLCN-FNIP RagC/D GAP branch. |
| `Tsc2` | 86 | 58 up, 28 down. In the same focal group it induced sterol and feedback genes such as `Cyp51`, `Ldlr`, `Pik3r1`, `Pik3r3`, `Ddit4`, `Lamp2`, `Grn`, and `Rragd`. Spearman logFC correlation with `Depdc5` was 0.326, the strongest relation in the tested mTOR/lysosome subset. | Shows that thalamic neurons can mount a detectable mTORC1/SREBP/lysosome-related response. I downweighted it because `Tsc2` loss is a broader Rheb/TSC brake removal and stronger than expected for partial `Fnip1` loss. |
| `Rab7` | 501 | 311 up, 190 down. It shared 5 same-direction FDR genes with `Depdc5`, all in the sterol arm (`Hmgcs1`, `Insig1`, `Ldlr`, `Msmo1`, `Snhg11`), and 36 of 38 FDR-overlap genes with `Tsc2` were same-direction. | A strong late-endosomal positive control and evidence that lysosome-associated stress can be detected. Rejected as a magnitude analog because `Rab7` loss is a large trafficking lesion, not a selective FLCN-FNIP nutrient-sensing perturbation. |
| `Mtor` | 2 | Only `Rims3` and `Tmed8` passed FDR 0.05; there was no FDR-significant overlap with `Tsc2`. | A boundary case for the loss side of mTORC1. The RNA response to core kinase loss was tiny in this cell group. |
| `Rptor` | 0 | No focal FDR genes despite 235 perturbed nuclei. | A same-complex mTORC1 boundary case. Its null response argues against predicting a broad program from partial suppression of a positive mTORC1 component alone. |
| `Prkaa2`, `Prkag2`, `Strada` | 0, 0, 0 | `Prkaa2` and `Prkag2` had no FDR genes in the focal group; Distributed Agents also records no FDR-supported downstream response for `Prkaa2` in any recovered neuronal group. | FNIP1 was discovered as an AMPK-interacting factor, but represented AMPK/LKB1-adjacent loss-of-function perturbations did not turn into a basal neuronal RNA phenotype. |
| `Rb1cc1` | 4 | The four hits were down (`Hspa5`, `Calr`, `Rb1cc1`, `Pdia6`), a narrow ER/autophagy-initiation response. `Atg5` and `Becn1` did not share a focal FDR hit with it at the endpoint threshold. | A weak positive example that core autophagy initiation can be visible, but the focal response is tiny and not a broad TFEB/lysosome module. |
| `Atg5`, `Atg16l1`, `Becn1`, `Rubcn`, `Lamp2` | 0, 0, 0, 0, 0 | No focal FDR genes. `Lamp2` had a nominal target decrease but no gene below 0.05 after BH correction. | Strong counterexamples to treating all autophagy or lysosome membership as sufficient for a DEG-count response. |
| `Map1lc3a`, `Sqstm1` | 1, 1 | Each was essentially a self-transcript call, with no broad downstream program. | Counterexamples for LC3/cargo-receptor or p62/TFEB-style rebound after acute partial perturbation. |
| `Tmem106b`, `Ppt1`, `Psap`, `Gnptab`, `Manba`, `Sort1` | 1, 1, 1, 0, 0, 0 | Lysosomal disease genes were mostly self-only or flat in the focal group. | Boundary against a generic acute neuronal lysosomal-stress or TFEB/MiT transcriptional output. |
| `Vps35`, `Vps54` | 17, 31 | Measurable but small-to-medium endolysosomal/trafficking responses, neither the `Depdc5` sterol arm nor the `Tsc2` program. | These confirm selected trafficking lesions can be detected, but same-organelle stress is not enough to predict a strong FNIP1 count. |

The Distributed Agents same-experiment corpus supported the same separation. It records
that `Depdc5` was a sharply `151 TH Prkcd Grin2c Glut`-selective perturbation,
that `Tsc2` and `Depdc5` share a sterol/PI3K 151 signature, and that `Rab7`
converges with `Depdc5` on sterol/endolysosomal genes. It also records that
`Mtor`, `Rptor`, `Strada`, `Pik3r1`, and `Pik3cb` do not phenocopy `Depdc5`;
that represented AMPK/LKB1-adjacent perturbations are uncoupled from the
`Tsc2` response; and that represented autophagy and lysosome perturbations are
not transcriptomically interchangeable in this postnatal neuronal screen.

### Zero/nonzero decision

The external biology gave a real reason to look for an effect: loss of FNIP1
can destabilize FLCN-FNIP nutrient signaling and release TFE3/TFEB-dependent
lysosomal programs in B-cell and kidney contexts. But three details pushed the
prediction below one BH-significant gene here:

1. The closest direct loss-side training perturbations were flat. Core mTORC1
   loss (`Rptor` 0; `Mtor` 2), AMPK/LKB1-adjacent loss (`Prkaa2`, `Prkag2`,
   `Strada`, all 0), and most autophagy or lysosomal storage perturbations
   were 0 to 1 DEG in this same focal group.
2. The measured positive mTORC1-repressor phenotypes were node-specific.
   `Depdc5` had only 13 DEGs and `Tsc2` had 86, despite sitting closer to
   canonical mTORC1 activation than `Fnip1` loss. Their shared program was
   sterol/SREBP-associated; FNIP1 loss is expected to perturb the FLCN-FNIP
   RagC/D-TFEB arm rather than to create the same Rheb/GATOR activation sign.
3. The assay conditions are weak for a TFEB-style chronic stress response:
   sparse acute CRISPR in postmitotic neurons, average modest mRNA
   down-regulation, no glia, and one steady-state snRNA-seq endpoint. The
   training data show that even bona fide lysosomal genes usually do not
   produce a nuclear lysosome-biogenesis signature under these conditions.

I therefore predicted a zero DEG count. If `Fnip1` was highly expressed in the
recovered perturbed nuclei, a one-gene self-transcript call would be plausible,
as happened for `Map1lc3a`, `Sqstm1`, `Ppt1`, `Psap`, and `Tmem106b`; however
there was no training evidence strong enough to push the point prediction from
the focal distribution mode of 0 to a weak nonzero count.

## Limits and extrapolation

The largest limitation is absence of the best comparators. `Flcn`, `Fnip2`,
`Rragc`, `Rragd`, `Tfeb`, and `Tfe3` were not training perturbations, and
FNIP1 paralog compensation by FNIP2 is tissue-specific (Hasumi et al. 2015,
DOI `10.1073/pnas.1419502112`, PMID `25775561`). The prediction therefore
extrapolates from less direct mTOR, AMPK, autophagy, and lysosome nodes.

The readout is also RNA only. It cannot see Rag nucleotide state, mTORC1
substrate phosphorylation, TFEB/TFE3 nuclear localization, LC3 lipidation,
autophagic flux, lysosomal pH, or cell size. A biochemical FNIP1 phenotype
could be present while still yielding zero BH-significant nuclear DE genes.

Finally, `n_degs` is power-dependent. Small differences in recovered perturbed
nuclei or target-gene expression can move self-transcript-only cases between
0 and 1, so the zero prediction should be read as "below the FDR 0.05 count
threshold in this assay" rather than as absence of FNIP1 biology in neurons.
