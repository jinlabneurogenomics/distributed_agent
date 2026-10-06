# Pnpt1 n_degs forecast

## Target and endpoint

- Target: `Pnpt1`
- Cell group: `151 TH Prkcd Grin2c Glut`
- Requested endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- `Pnpt1` was absent from the 1,674-row training count table, and I did not query or use a `Pnpt1` DE contrast.

## Biological prior

The Pnpt1 biology bundle supports perturbation reach but not a guaranteed survivor-state transcriptome:

- In the exact focal non-target population, `Pnpt1` is detected in 18,215 / 23,679 nuclei, with mean log1p(CP10K) 0.632 and pseudobulk CPM 106.3, so the target is expressed in this assayed thalamic class.
- PNPase is a renewable homotrimeric mitochondrial RNA-processing/import enzyme. Functional stock is expected to decline over the 21-28 day P16-to-P37/P44 window, because disruptive editing should stop new protein supply while continued mitochondrial RNA metabolism creates renewal demand.
- The timing and cell-context evidence are only partial: the strongest postnatal mouse phenotype was from Atoh1-Cre inner-ear hair cells at 3-4 weeks, not acute thalamic neuron loss, and no mouse neuronal PNPase half-life was available.

I therefore treated the card as evidence that some material effect is biologically reachable, but not as evidence that the `151 TH Prkcd Grin2c Glut` FDR count should be large.

## Training evidence that set the scale

The focal count table is zero-inflated: 1,205 / 1,674 training perturbations have `n_degs = 0`; the median is 0, the 75th percentile is 1, the 90th percentile is 2, and only 106 targets have 10 or more DEGs.

For Pnpt1's nearest functional neighborhood, direct mitochondrial perturbations were mostly transcriptionally quiet in the focal class:

| training group | genes in `151 TH Prkcd Grin2c Glut` | focal counts |
|---|---|---|
| Mitochondrial proteostasis/RNA/dynamics | `Afg3l2`, `Clpp`, `Gfm2`, `Lonp1`, `Lrpprc`, `Opa1`, `Yme1l1` | 0, 0, 0, 0, 0, 37, 0 |
| Respiratory-chain and mitochondrial carriers | `Coq5`, `Cox*`, `Nduf*`, `Slc25*`, `Uqcr*` subset present in training | median 0, mean 0.4 |
| Mitochondrial biogenesis/signaling | `Esrra`, `Mtor`, `Nrf1`, `Ppargc1a`, `Tsc2` | 57, 2, 138, 0, 86 |

The same-experiment Finding ledger made the same boundary explicit:

- `Lrpprc`, the closest measured mitochondrial RNA-metabolism analogue, was a pan-measured neuronal transcriptional null after P16 CRISPR: 0 downstream FDR < 0.10 genes in all recovered cell groups.
- `Afg3l2`, `Clpp`, `Lonp1`, and `Yme1l1` did not provide a robust 151 thalamic analogue. Their same-experiment reports describe sparse or buffered responses rather than a general mitochondrial proteotoxicity or UPRmt program.
- `Opa1`, `Nrf1`, and `Esrra` prove that 151 thalamic neurons can show mitochondrial or oxidative-metabolism stress, but their reports describe broader ISR, nuclear respiratory biogenesis, or ERR-alpha/PGC-1 regulatory programs. Those are not direct matches to removing one mitochondrial RNA enzyme.

The matched profile-neighborhood check around `Lrpprc`, `Opa1`, `Nrf1`, `Esrra`, `Lonp1`, and `Afg3l2` in the 151 Parquet did not reveal a single coherent mitochondrial empirical cluster. The strong focal responders were closest to assorted stress, proteostasis, or regulatory profiles; the quiet RNA/protease anchors had no FDR-significant 151 program to transfer.

## Synthesis

Pnpt1 has enough expression and renewal biology that I would not call a failure of editing or target absence. The quantitative training evidence nevertheless argues that the most task-matched class is the buffered direct mitochondrial RNA/protease group, especially `Lrpprc`, not the high-count `Nrf1`/`Esrra` transcription-factor branch or the `Opa1` ISR exception.

I therefore forecast a near-null recovered-nucleus signature. A self-transcript-only outcome is plausible, but the direct mitochondrial RNA analogue and most protease/RNA/dynamics perturbations in the focal class were exact zeros, so I rounded the point forecast to 0.
