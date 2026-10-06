# Direct forecast for `Uqcrc1`

## Evidence used

- Task and bindings: the held-out manifest target is `Uqcrc1`; the endpoint is the count of genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `p < 0.05`. `Uqcrc1` is absent from the 1,674-row training count table.
- Exact biology bundle for `Uqcrc1`, served from `biology_bundles/Uqcrc1.json` with target outcome hidden:
  - Uqcrc1 is a core component of mitochondrial respiratory complex III and respiratory supercomplexes.
  - The target is strongly reachable in the focal assay population: mean raw UMI `6.29`, mean log1p CP10K `1.49`, and `98.05%` of non-target `151 TH Prkcd Grin2c Glut` nuclei expressed `Uqcrc1`.
  - Functional stock was adjudicated as `partially_depleted_or_leading_edge`: a P16 edit should stop new UQCRC1 supply, but pre-edit complex III is already installed and long-lived respiratory-chain material can leave residual function over the P37-P44 harvest window.
- Same-experiment training count table for `151 TH Prkcd Grin2c Glut`:
  - Overall counts are strongly zero-inflated: median `0`, 75th percentile `1`, 90th percentile `2`, and 95th percentile `18`.
  - Observed complex-III structural/turnover perturbations were centered at 0-1 DEGs in this class: `Cyc1:1`, `Ttc19:1`, `Uqcrb:0`, `Uqcrc2:1`, `Uqcrfs1:0`, `Uqcrh:0`, `Uqcrq:1`; median `1`, mean `0.57`.
  - A broader direct ETC set was similar: `Cox4i1:0`, `Cox5a:1`, `Ndufs4:0`, `Ndufs8:1`, `Ndufv1:0`, `Sdha:1`, plus the complex-III values above; median `1`, mean `0.54`.
- Direct Parquet rows from `training_de_all_cell_groups.parquet` in `151 TH Prkcd Grin2c Glut`:
  - The singleton calls for `Cyc1`, `Ttc19`, and `Uqcrc2` were self-transcript hits.
  - `Uqcrq` had one downstream hit, `Gpr180` down, at adjusted `p = 0.04288`.
  - `Uqcrfs1`, `Uqcrh`, and `Uqcrb` had zero focal hits.
  - Mitochondrial boundary perturbation `Opa1` had a real 37-gene focal program led by ATF4/ISR-like amino-acid stress genes, not a complex-III-like program.
- Same-experiment Finding ledger, release `perturbai-july-260713-sourceguard-1773-v1`:
  - `Uqcrc2:F001-F006`: `Uqcrc2` produced no robust downstream single-gene DE, had no mitochondrial-stress induction, and represented complex-III relatives did not reveal a hidden Uqcrc2-like module.
  - `Uqcrfs1:F001-F005`, `Uqcrh:F001-F003`, `Uqcrb:F001-F004`, `Uqcrq:F001-F003`, `Cyc1:F001-F004`, and `Ttc19:F001-F005`: the observed complex-III surface was nearly flat, with isolated private hits rather than a shared stress signature.
  - `Opa1:F001-F009`: `Opa1` induced an amino-acid/ATF4 ISR-like module and direct OPA1-processing or mitochondrial fission comparators did not phenocopy it.

## Synthesis

`Uqcrc1` has better focal detectability than many mitochondrial targets and is a core complex-III member, so I did not collapse the forecast all the way to a guaranteed zero. The stock card nevertheless argues for only a leading-edge functional depletion by 21-28 days, and the matched training surface shows that other complex-III and direct ETC perturbations in the same cell class almost always yielded either no BH<0.05 gene or a single self/private transcript rather than a broad stress response. I therefore forecast the count at the integer center of the closest observed biology: one significant measured gene.
