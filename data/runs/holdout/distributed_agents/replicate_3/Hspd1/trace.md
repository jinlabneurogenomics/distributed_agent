# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested held-out target list contains one perturbation, `Hspd1`. I
interpreted `n_degs` exactly as the supplied endpoint defines it: in the focal
`151 TH Prkcd Grin2c Glut` class, count measured genes whose
Benjamini-Hochberg-adjusted Wilcoxon p-value is below 0.05 for the given
CRISPR loss-of-function perturbation versus matched controls. `Hspd1` is absent
from both the training parquet and the focal training-count CSV, so its count
has to be transferred from non-held-out perturbations rather than read off.

## Sources used

- Raw training differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Focal training endpoint CSV:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Distributed Agents same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, especially curated findings for
  `Hspa5`, `Hspa8`, `Opa1`, `Lonp1`, `Clpp`, `Clpx`, `Afg3l2`, `Yme1l1`, and
  `Tomm40`.
- PubMed literature for external HSPD1 biology: Comert et al. 2024,
  DOI `10.1016/j.molmet.2024.102009`/PMID `39147275`; Wachoski-Dark et al.
  2022, DOI `10.3390/ijms23063353`/PMID `35328774`; and
  Eskin-Schwartz et al. 2024, DOI `10.1136/jmg-2024-109862`/PMID `39500555`.

## Training-set calibration

The focal training-count CSV contained 1,674 non-held-out perturbations.
Responses in this cell group were sparse: the median count was 0, only 469
targets had any FDR 0.05 gene, the 75th percentile was 1 DEG, the 95th
percentile was 18 DEGs, and the mean was pulled up to 14.1 by a small number of
very broad perturbations such as `Uba5` with 2,677 DEGs.

For a mechanistic comparison I queried the parquet only in the focal cell group
for mitochondrial proteostasis, mitochondrial dynamics/import/OXPHOS, and
chaperone analogs. I counted rows with `pvals_adj < 0.05` for each candidate and
inspected the actual FDR-significant genes plus stress markers such as `Ddit3`,
`Chac1`, `Asns`, `Slc7a1`, `Slc7a5`, `Hspd1`, `Hspe1`, `Hspa9`, and `Clpp`.
I also used a Distributed Agents runtime signed-profile comparison among the selected
training profiles to check whether weak/null mitochondrial targets shared the
FDR-qualified `Opa1`, `Hspa8`, or `Hspa5` signatures; they did not.

## Target-specific reasoning

### `Hspd1`

`Hspd1` encodes HSP60, the mitochondrial matrix chaperonin that folds imported
matrix proteins with the HSP10 co-chaperonin. Human HSPD1 variants cause
spastic paraplegia and hypomyelinating leukodystrophy, and engineered HSP60
deficiency disrupts a large mitochondrial matrix proteome with transcriptional
stress responses in model systems. Those external facts make `Hspd1` more
central than the mitochondrial proteases that only degrade selected substrates.

The useful within-dataset analogs were nevertheless mostly very small in the
same focal class:

| training perturbation | `n_degs` in `151 TH Prkcd Grin2c Glut` | expression-pattern evidence |
| --- | ---: | --- |
| `Clpp` | 0 | Same matrix-proteostasis compartment through the ClpXP protease, but no focal FDR 0.05 genes and no induction of `Asns`, `Ddit3`, `Chac1`, `Hspd1`, `Hspe1`, or `Clpp` itself. The Distributed Agents corpus summarizes `Clpp` as globally buffered and not a generic ClpXP or UPRmt signature. |
| `Clpx` | 0 | Same ClpXP system as `Clpp`, also 0 focal DEGs; the corpus reports no FDR-level downstream response in any measured neuronal group. |
| `Lonp1` | 0 | Matrix AAA+ protease with a possible mitochondrial-stress/CHOP connection, but flat in the focal class. Corpus findings show `Lonp1` induced a small `Ddit3`/`Herpud1`-positive program only in other groups and did not induce canonical `Atf5`, `Hspd1`, `Hspe1`, `Hspa9`, or `Clpp`. |
| `Afg3l2` | 0 | Mitochondrial protease expected to couple to proteotoxicity and OPA1 processing, but it had no focal DEGs and the corpus notes lack of the expected OPA1/ISR/UPRmt program. |
| `Yme1l1` | 0 | Inner-membrane AAA protease upstream of OPA1 processing, but 0 focal DEGs and no `Opa1`-like FDR overlap. |
| `Tomm40` | 1 | A core mitochondrial protein-import pore. Its only focal FDR 0.05 gene was the perturbed transcript itself; the same-experiment corpus reports absence of import-failure, ISR/ATF, UPRmt-chaperone, proteasome, and TOM-subunit compensation programs. |
| `Sdha`, `Ndufv1`, `Uqcrc2`, `Cox5a`, `Ndufs4`, `Uqcrq` | 0 to 1 | Direct OXPHOS lesions were essentially self-hit or null comparators in 151, arguing that mitochondrial localization or respiratory importance alone did not create a broad count. |
| `Opa1` | 37 | The main positive mitochondrial counterexample. `Opa1` loss gave a real ATF4/ISR-like focal signature: `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Slc7a5`, `Herpud1`, `Slc7a1`, and several tRNA synthetases were FDR-significant. `Hspd1`, `Hspe1`, `Hspa9`, and `Clpp` trended only weakly or not at all after `Opa1`, so even this mitochondrial responder was not a canonical HSP60/HSP10/ClpP UPRmt program. |
| `Hspa8` | 9 | A cytosolic HSP70 family chaperone. It produced a small heat-shock counterinduction program in 151, with `Dnaja1`, `Hspa4l`, `Syt4`, `Hsp90aa1`, and `Cct6a` up-regulated. This shows that the focal class can detect a chaperone stress program, but it is a different cytosolic HSP axis. |
| `Hspa5` | 5 | The ER HSP70/BiP chaperone induced a compact ER-folding/ERAD response: `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` were among its focal hits. It is a useful small-response chaperone analog, but compartment and UPR regulation differ from HSP60. |
| `Hsf1` and `Hsp90ab1` | 6 and 1 | Heat-shock pathway comparators with very low focal counts, further keeping generic chaperone-loss expectations in the single-digit range. |

This pattern puts `Hspd1` between two pieces of evidence. Externally, HSP60 loss
is a direct hit to matrix protein folding and should be more stressful than
`Clpp`, `Clpx`, or an isolated respiratory-chain subunit. Internally, however,
acute P16 mosaic neuronal CRISPR was strikingly buffered for matrix proteases,
mitochondrial import, and many OXPHOS genes, while the one clear mitochondrial
focal responder, `Opa1`, was an ISR/respiratory state rather than an HSP60/HSP10
chaperonin-state. HSPD1 protein perdurance and survivor-conditioned sampling
also make a massive transcriptional collapse unlikely at three to four weeks.

I therefore predict a borderline detectable response rather than a 0-count
pure null or an `Opa1`-scale program. The point estimate is 1 FDR 0.05 gene:
effectively a one-gene/single-marker outcome, with no robust mitochondrial
unfolded-protein or ATF4 module.

## Limits

The evidence is indirect because neither `Hspd1` nor its HSP10 partner `Hspe1`
was available as a training perturbation in the focal endpoint. The nearest
same-compartment analogs are mitochondrial proteases, import components, OXPHOS
genes, and `Opa1`; none removes the HSP60 folding chamber itself. Literature
HSP60-deficiency systems include HEK cells, zebrafish larvae, patient
fibroblasts, and human inherited disease, not sparse acute CRISPR in recovered
juvenile mouse neurons. The final integer is thus an extrapolation at the
zero/nonzero boundary, driven mainly by same-experiment buffering of neighboring
mitochondrial proteostasis perturbations and adjusted upward slightly by the
central role of HSP60 in matrix folding.
