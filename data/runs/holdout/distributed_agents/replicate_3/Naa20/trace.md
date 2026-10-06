# Naa20 prediction trace

## Question and resolved ambiguities

The run asks for a point prediction of `n_degs` for each held-out perturbation in
`151 TH Prkcd Grin2c Glut`; the manifest contains one target:
`Naa20`. I interpreted `n_degs` as the focal training endpoint:
the number of assayed genes with Benjamini-Hochberg-adjusted Wilcoxon
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after acute
AAV-CRISPR loss-of-function. I therefore predicted a screen-specific DEG count,
not whether NAA20 is biochemically active, essential in development, or altered
at protein/N-terminome level.

## Sources

- Training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Training differential expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Held-out manifest:
  `[local file: 142_Naa20.csv]`
- Distributed Agents same-experiment corpus:
  `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents runtime profile comparison of `Naa10`, `Mpc1`, `Rorb`, `Gli2`,
  `Diaph2`, `Psmb4`, `Psmc1`, and `Eef2` in the focal cell group, written to
  `naa10_focal_profile_compare.json` and inspected through
  `naa10_focal_profile_inspect.json`.
- External literature from PubMed: Starheim et al. 2008
  (DOI 10.1042/BJ20080658, PMID 18570629), Aksnes et al. 2016
  (DOI 10.1016/j.tibs.2016.07.005, PMID 27498224), Hong et al. 2017
  (DOI 10.1016/j.str.2017.03.003, PMID 28380339), Lasa et al. 2020
  (DOI 10.1016/j.jmb.2020.09.010, PMID 32976911), Morrison et al. 2021
  (DOI 10.1038/s41436-021-01264-0, PMID 34230638), and Santhosh Kumar et al.
  2024 (DOI 10.1126/sciadv.adj4767, PMID 38335281).

## Computational checks over the training data

The focal DEG-count table has 1,674 training perturbations. It is strongly
zero-inflated in this cell group: the median count is 0, the 75th percentile is
1, and the maximum is 2,677.

I searched the focal count table for N-terminal-acetyltransferase and adjacent
co-translational maturation targets. `Naa20`, its NatB auxiliary subunit
`Naa25`, `Metap1`, `Metap2`, and the other Nat catalytic or auxiliary subunits
I checked (`Naa15`, `Naa30`, `Naa35`, `Naa38`, `Naa40`, `Naa50`, `Naa60`) were
not in training. The only assayed `Naa*` perturbation in the focal training
table was `Naa10`, with:

| training target | focal n_degs | rationale for using it |
|---|---:|---|
| `Naa10` | 0 | catalytic subunit of the NatA N-terminal acetyltransferase; closest assayed NAT catalytic perturbation |
| `Mpc1` | 0 | data-driven flat full-vector neighbor of `Naa10` in the Distributed Agents `Naa10` report |
| `Rorb` | 0 | data-driven flat full-vector neighbor of `Naa10` in the Distributed Agents `Naa10` report |
| `Gli2` | 0 | data-driven flat full-vector neighbor of `Naa10` in the Distributed Agents `Naa10` report |
| `Diaph2` | 0 | data-driven flat full-vector neighbor of `Naa10` in the Distributed Agents `Naa10` report |
| `Eef2` | 9 | translation-factor counterexample: a protein-synthesis lesion with a detectable but small focal response |
| `Psmc1` | 430 | 19S proteasome ATPase counterexample: broad focal proteostasis/stress response |
| `Psmb4` | 742 | 20S proteasome core counterexample: broad focal proteostasis/stress response |

To verify that the `Naa10` count reflected a measured null rather than a missing
profile, I scanned the parquet on `group_name == "151 TH Prkcd Grin2c Glut"`
and those comparator targets:

```python
flt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(
        ["Naa10", "Psmb4", "Psmc1", "Eef2", "Mpc1", "Rorb", "Gli2", "Diaph2"]
    )
)
```

`Naa10` had 17,259 focal rows, 240 matched perturbed nuclei, 23,679 matched
controls, zero genes at FDR 0.05, and zero at FDR 0.10. Its top nominal
features were weak after correction; the ten smallest raw `pvals` all had
`pvals_adj = 1.0`. In the same focal slice, `Psmb4`, `Psmc1`, and `Eef2`
reproduced the training counts with 742, 430, and 9 genes at FDR 0.05,
respectively.

The Distributed Agents runtime profile comparison over these eight focal vectors found
`Naa10` available with no significant features. Whole-profile correlations
placed it closest to other null/near-null vectors (`Gli2`, `Rorb`, `Mpc1`);
`Psmb4` and `Psmc1` were still positive in all-gene correlation because of
background structure, but shared no FDR 0.05 significant features with `Naa10`.
That matched the Distributed Agents `Naa10` same-experiment record: postmitotic P16
`Naa10` perturbation produced zero downstream FDR 0.10 genes across 22 neuronal
groups and 2,123 matched perturbed nuclei, lacked compensatory NAT-family,
integrated-stress, apoptosis, proteasome, or ubiquitin rebound transcripts, and
was explicitly contrasted with the strong `Psmb4`, `Psmc1`, and `Eef2`
protein-homeostasis/translation responses.

## Target-specific biological reasoning

`Naa20` encodes the catalytic subunit of NatB. Starheim et al. identified the
vertebrate NatB complex as a stable catalytic/auxiliary pair, now named
NAA20/NAA25, with sequence-specific N-terminal acetyltransferase activity and
ribosome association, and Aksnes et al. reviewed NatA, NatB, NatC and related
NATs as abundant co-translational protein-modifying enzymes. Structural work by
Hong et al. showed that Naa25 holds Naa20 and that NatB recognizes N termini
beginning with initiator methionine followed by acidic or amide residues;
Lasa et al. further showed that the NAA20 amino terminus is required for NAA25
interaction and NatB assembly. NAA20 is therefore a plausible neuronal
housekeeping/translation-adjacent perturbation, not a transcription factor or
cell-surface receptor expected to alter a small fixed set of direct mRNA
targets.

The relevant observed analog is `Naa10`. `Naa10` is the NatA catalytic subunit
rather than NatB, so it is not a paralogous substitute and it has a different
substrate class. Still, among all supplied focal training perturbations it is
the only assayed catalytic N-terminal acetyltransferase and the only direct
test of whether reducing a ribosome-associated NAT is sufficient to drive a
secondary neuronal nuclear RNA program in this juvenile mosaic assay. Its focal
count was exactly 0, and the same-experiment Distributed Agents analysis reported a
pan-neuronal FDR-level null for `Naa10`. That drives the zero/nonzero decision
more strongly than generic essential-gene behavior.

The appropriate counterexamples are `Psmb4`, `Psmc1`, and `Eef2`, not as
positive predictors of `Naa20`, but as assay gates. `Psmb4` and `Psmc1`
triggered hundreds of focal DEGs and Distributed Agents records describe proteasome
bounce-back, integrated-stress, heat-shock, redox, apoptosis-like, and
autophagy/lysosome RNA arms. `Eef2` was much smaller in this focal group
but still nonzero, showing that a core elongation-factor lesion can be detected
when it crosses a transcriptional threshold. The absence of a similar response
after `Naa10` loss argues that Nat catalytic perturbations can be buffered at
the RNA level even when adjacent translation/proteostasis perturbations are not.

External biology cuts both ways but does not overturn the within-dataset null.
Morrison et al. showed that recessive human NAA20 missense variants impair
NatB activity and cause developmental delay, intellectual disability, and
microcephaly, and Santhosh Kumar et al. found that partial NatB inhibition in
human neurons can reduce alpha-synuclein protein. Those findings make NAA20
biologically real in neurons and development, but both are mainly protein-level,
developmental, or substrate-specific contexts. The requested endpoint is an
acute P16 loss-of-function nuclear RNA count 3-4 weeks later in already
specified neurons. With no measured `Naa20` or `Naa25` training signature and
with `Naa10` flat, the best calibrated point prediction is that NatB loss will
not produce any FDR 0.05 focal DEGs.

## Limits

- There is no direct NatB member in the training set. `Naa10` is a NatA
  catalytic perturbation, not a `Naa20` paralog or complex partner.
- N-terminal acetylation is a protein N-terminome perturbation. The screen did
  not measure NAA20 protein, NatB complex abundance, substrate acetylation, or
  indels, so a zero DEG prediction can coexist with a true biochemical effect.
- Human NAA20 disease genetics and alpha-synuclein regulation involve
  developmental or protein-abundance phenotypes that need not manifest as
  bulk FDR-significant mouse thalamic mRNA changes after sparse P16 editing.
- The focal endpoint is assay-power dependent. `Naa20` might have a few
  low-amplitude genes below the FDR threshold even if `n_degs` is zero.

Final prediction: `Naa20` -> 0 DEGs.
