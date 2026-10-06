# Ndufs1 n_degs forecast

## Target and endpoint

- Target: `Ndufs1`.
- Endpoint: count of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon `pvals_adj < 0.05`.
- Prediction: `1`.

## Evidence used

- Declared holdout and biology-only target bundle:
  - Manifest: `[local file: Ndufs1.csv]`.
  - Biology bundle: `[local file: Ndufs1.json]`, checksum `9e3309f226e332990b382d039c95e7074e97bd9f34414b000f07934b7b3bb860`.
  - The focal non-target expression reach for `Ndufs1` in `151 TH Prkcd Grin2c Glut` was measurable rather than absent: 16,609 / 23,679 nuclei expressed the gene, `70.14%`, with pseudobulk CPM `90.10` and mean log1p-CP10K `0.537`.
- Biology prior from the target bundle:
  - NDUFS1 is a nuclear-encoded 75-kDa core N-module subunit of mitochondrial respiratory complex I, so a disruptive allele is expected to block new supply of a stoichiometric component of an already installed inner-membrane complex.
  - The adjudicated functional stock state was `partially_depleted_or_leading_edge`: complex-I NDUFS1 can exchange, and the mouse-brain proteome renews over weeks, but no target-specific 21-28 day NDUFS1 clearance clock in postmitotic thalamic neurons was available.
  - No close mouse paralog or demonstrated NDUFS1-position substitute was found; systemic and human disease evidence support complex-I importance but do not establish a large acute postnatal thalamic transcriptional response.
- Focal training count table:
  - Source: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  - The marginal distribution was sparse: 1,205 / 1,674 training perturbations were zero and another 276 were exactly one DEG.
  - A hand-selected respiratory/mitochondrial comparator set from the declared table had low counts. The complex-I and close OXPHOS perturbations excluding the `Opa1` stress outlier had values only in `{0, 1}`: 12 zeros and 16 ones, mean `0.57`, median `1`.
  - The informative complex-I rows were similarly small in the focal class: `Ndufs2=1`, `Ndufs4=0`, `Ndufs7=0`, `Ndufs8=1`, `Ndufv1=0`, `Ndufv2=1`, `Ndufa10=1`, `Ndufa11=0`, `Ndufa12=0`, `Ndufa6=1`, `Ndufb10=1`, `Ndufb11=1`, `Ndufb3=0`, `Ndufb7=0`, `Ndufb8=1`, `Ndufb9=1`, `Ndufc2=1`.
- Training Parquet checks:
  - Source: `[local file: training_de_all_cell_groups.parquet]`.
  - Querying only training comparators in `151 TH Prkcd Grin2c Glut`, most one-DEG OXPHOS controls were single self-transcript hits: for example `Ndufs2`, `Ndufs8`, `Ndufa10`, `Ndufb10`, `Cox5a`, `Sdha`, `Tomm40`, and `Uqcrc2` each had only the perturbed gene passing FDR.
  - `Ndufv2` had a lone non-self hit, `Cdc40`; the only selected mitochondrial outlier with a small multi-gene survivor program was `Opa1` at 37 DEGs, including amino-acid and stress-associated genes.
  - A symmetric profile comparison over 29 selected mitochondrial/respiratory training perturbations in the focal class completed without missing profiles. Response activity was 12 nodes with no significant features, 16 with 1-9, and 1 with 10-49, matching the interpretation that this local cohort is largely transcriptionally quiet.

## Synthesis

`Ndufs1` should be active in the assayed focal nuclei and is not protected by a known redundant subunit, so a completely unreachable perturbation is less likely than for an unexpressed or replaceable gene. However, the operative protein is an installed complex-I core component that must be depleted by turnover after P16 editing; the endpoint samples only recovered P37-P44 nuclei, so the most likely response is delayed and survivor-conditioned rather than a broad stress state.

The closest measured training perturbations in complex I and adjacent OXPHOS machinery show exactly that low-yield pattern in this thalamic class: essentially all are 0 or 1 DEGs, and their one-count outcomes usually reflect only a significant target-transcript change rather than a coordinated downstream module. `Opa1` shows that mitochondrial perturbation can be visible in this group, but it perturbs mitochondrial dynamics and produced a stress-like program rather than the narrow complex-I-subunit pattern.

I therefore put `Ndufs1` at the active edge of the respiratory-chain cohort: enough expression and nonredundancy to favor one FDR-significant measured gene over a hard zero, but no evidence for the tens-to-hundreds DEG programs seen for nuclear proteostasis or RNA-processing hits. The point forecast is `1`.
