# Vapb forecast trace

## Target and endpoint

- Manifest target: `Vapb`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the number of measured genes in the focal population with BH-adjusted Wilcoxon `p < 0.05`.

I used the declared one-row holdout manifest, the focal training count table, the declared training differential-expression Parquet, and the canonical Vapb biology bundle. I did not inspect a Vapb expression signature or Vapb DEG count, and did not use or create relationship-review, branch-calibration, terminal-prediction, scalar-prior, or calibrated-probability artifacts.

## Vapb biology bundle

The bundle supports real target reach in the assayed cell class:

- The Vapb feature is present in `151 TH Prkcd Grin2c Glut` non-target nuclei, with mean CP10k 1.0777, pseudobulk 108.57 CPM, and 18,327 of 23,679 non-target nuclei expressing Vapb, or 77.40%.
- VAPB is a dynamic ER membrane adaptor for FFAT-motif/contact-site partners and an HCN1/HCN2 trafficking-associated pool in thalamic neurons.
- Functional stock was adjudicated as likely substantially depleted by the P37-P44 harvest. A disruptive P16 edit stops new Vapb production; VAPB is not an irreversibly installed component, and the only target-specific chase measured wild-type VAPB decay on a scale of about 17 hours in cultured cells, much shorter than the 21-28 day experimental interval.
- Same-region phenotype evidence exists: constitutive Vapb loss reduced native Ih current in ventrobasal thalamic neurons.

The downward caveats were also important. The thalamic Ih result was electrophysiology after constitutive loss, not an acute postnatal Perturb-seq profile; the separate mouse motor phenotype was mild and late; Vapa is a close, coexpressed paralog; and the bundle does not establish that a VAPB contact-site or HCN trafficking defect will become a broad survivor-conditioned RNA program in this exact aggregate.

## Training measurements

The focal count table is extremely sparse:

- 1,674 training perturbations
- median `n_degs`: 0
- mean `n_degs`: 14.05, inflated by a long high-count tail
- 1,205 / 1,674, or 72.0%, had `n_degs = 0`
- 1,481 / 1,674, or 88.5%, had `n_degs <= 1`
- 1,512 / 1,674, or 90.3%, had `n_degs <= 2`
- 42 / 1,674, or 2.5%, exceeded 100

I then checked biologically nearby or bounding training perturbations in `151 TH Prkcd Grin2c Glut`.

Low-count ER/contact-site, membrane-shaping, lipid-traffic, and HCN-channel rows:

| training target | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Hcn1` | 0 | direct channel axis relevant to the VAPB-HCN thalamic prior, quiet |
| `Hcn2` | 1 | direct channel axis; the only significant row was `Hcn2` itself |
| `Osbpl2` | 0 | lipid/contact-site adjacent, quiet |
| `Vps13a` | 0 | lipid-transfer/contact-site adjacent, quiet |
| `Vps13b` | 0 | lipid/vesicular trafficking, quiet |
| `Vps13c` | 0 | lipid-transfer/contact-site adjacent, quiet |
| `Atl1` | 1 | ER membrane shaping; the only significant row was `Atl1` itself |
| `Atl3` | 0 | ER membrane shaping, quiet |
| `Reep1` | 1 | ER membrane shaping; the only significant row was `Reep1` itself |
| `Reep2` | 1 | ER membrane shaping; the only significant row was `Reep2` itself |
| `Trappc6b` | 0 | trafficking, quiet |
| `Trappc9` | 0 | trafficking, quiet |
| `Trappc10` | 0 | trafficking, quiet |
| `Sec23a` | 0 | ER-to-Golgi traffic, quiet |
| `Stard7` | 0 | lipid transfer, quiet |
| `Sptlc2` | 1 | sphingolipid synthesis; the only significant row was `Sptlc2` itself |
| `Synj1` | 1 | phosphoinositide/synaptic vesicle traffic; the only significant row was `Synj1` itself |
| `Vcp` | 2 | protein quality-control machinery, still very small |

Two larger training profiles set upper boundaries rather than direct scale donors:

- `Atp2a2`, an ER calcium pump, had 187 DEGs and induced an unfolded-protein-response program including `Ddit3`, `Xbp1`, `Herpud1`, and `Hspa5`.
- `Rab7`, a late endosomal GTPase, had 501 DEGs across lysosomal, cholesterol, and stress genes.

These show that the focal thalamic population can register large ER/endolysosomal stress states, but the operation is broader and more acute than loss of a partially buffered VAPB adaptor. Treating them as the main magnitude anchor would overstate Vapb.

The measured-profile comparison over the 20 selected training perturbations gave the same picture: 11/20 had no significant focal feature, 7/20 had only 1-9 significant features, and only the Atp2a2/Rab7 boundary profiles had at least 50. Shared signed tails across the low-count contact-site/HCN/traffic rows were weak and did not reveal a recurrent VAPB-like thalamic program hiding beneath the FDR cutoff.

## Synthesis

I placed Vapb above a generic zero-effect prior because the target is expressed in most focal nuclei, its ER-associated functional stock should be depleted within the experimental window, and loss has same-region thalamic electrophysiological evidence despite Vapa. I kept the point estimate in the one-gene regime because the closest available downstream operations were almost all `0` or self-only `1` in the same focal class, while the high-count comparators were broad ER-calcium or late-endosomal failures rather than close VAPB adaptor phenocopies.

Point forecast: `Vapb` has one FDR-significant measured gene in `151 TH Prkcd Grin2c Glut`.
