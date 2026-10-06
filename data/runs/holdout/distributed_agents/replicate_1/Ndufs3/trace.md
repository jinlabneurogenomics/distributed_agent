# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and resolved ambiguities

The requested held-out perturbation was `Ndufs3`. I interpreted the task as a
point prediction of the exact assay endpoint used in the focal thalamic
glutamatergic class: the number of measured genes with `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` after acute postnatal AAV CRISPR loss of function.

I did not reinterpret `n_degs` as editing efficiency, biochemical complex-I
deficiency, cell loss, or importance of the target. A zero or one count can
still be compatible with a real mitochondrial lesion because the measurement is
snRNA-seq on recovered NeuN+ nuclei 3-4 weeks after sparse P16 perturbation.
The requested-target file has one target and no ranking supervision, so file
order was used only as output order.

## Sources used

- Declared input training endpoint:
  `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Declared differential-expression parquet:
  `training differential-expression dataset`.
- Run-local requested-target manifest:
  `single-target request for Ndufs3`.
- The PerturbAI July 2026 same-experiment Findings corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, queried for packaged
  interpretations of training complex-I targets. I used those records as a
  semantic layer over the same screen, not as independent replication.
- External mechanism checks from PubMed and MitoCarta3.0:
  - MitoCarta3.0 annotates mammalian mitochondrial proteins and MitoPathways,
    including nuclear encoded respiratory complex-I subunits (Rath et al.,
    2021, Nucleic Acids Research, DOI:10.1093/nar/gkaa1011,
    PMID:33174596).
  - NDUFS3 is a complex-I core subunit whose mutation can cause complex-I
    deficiency and Leigh syndrome (Benit et al., 2004, Journal of Medical
    Genetics, DOI:10.1136/jmg.2003.014316, PMID:14729820).
  - NDUFS3 enters defined complex-I assembly intermediates (Vogel et al.,
    2007, Journal of Biological Chemistry, DOI:10.1074/jbc.M609410200,
    PMID:17209039).
  - Mammalian NDUFS3 ablation destabilizes complex-I assembly but can still
    leave a small amount of mature complex I in cultured cells, which makes it
    a strong complex-I perturbation but not necessarily an all-or-none block
    under partial depletion (D'Angelo et al., 2021, Cell Reports,
    DOI:10.1016/j.celrep.2021.109002, PMID:33882309).

## Computations over the supplied data

I first read the focal training DEG counts. Among 1,674 held-in perturbations,
1,205 had zero DEGs, 276 had exactly one DEG, and the 25th/50th/75th/90th
percentiles were 0/0/1/2. That establishes a sparse endpoint in which a
single-gene call is already above the focal median.

I then used DuckDB to scan only focal-cell rows for represented NADH
dehydrogenase and adjacent OXPHOS perturbations:

```sql
SELECT gene_target, names, logfoldchanges, pvals_adj, scores
FROM read_parquet(?)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
```

This direct query showed that the represented complex-I neighborhood was at
the DEG-count floor. The relevant held-in `Ndu*` targets were:

| training target | complex-I relationship | observed focal `n_degs` | expression evidence in the focal class |
|---|---:|---:|---|
| `Ndufs2` | core N-module/Q-module subunit, closest to `Ndufs3` among held-in proteins | 1 | the one FDR 0.05 hit was `Ndufs2` itself, LFC -0.728, adjusted p=8.26e-12 |
| `Ndufs8` | Fe-S/core subunit in the same enzyme arm | 1 | the one FDR 0.05 hit was `Ndufs8` itself, LFC -0.650, adjusted p=3.06e-08 |
| `Ndufs4` | matrix-arm accessory subunit, Leigh-model gene | 0 | no FDR 0.05 hit; `Ndufs4` self LFC -0.623 but adjusted p=0.502 |
| `Ndufs7` | core complex-I subunit | 0 | no FDR 0.05 hit; no shared stress genes |
| `Ndufv1` | flavoprotein/core catalytic subunit | 0 | no FDR 0.05 hit |
| `Ndufv2` | flavoprotein subunit | 1 | the single focal hit was `Cdc40`, not a mitochondrial gene |
| `Ndufa9` | matrix-arm complex-I subunit | 0 | no FDR 0.05 hit |
| `Ndufa10` | membrane-arm complex-I subunit | 1 | the one FDR 0.05 hit was `Ndufa10` itself |
| `Ndufb8` | accessory membrane-arm subunit | 1 | the one FDR 0.05 hit was `Ndufb8` itself |
| `Ndufc2` | accessory membrane-arm subunit | 1 | the one FDR 0.05 hit was `Ndufc2` itself |

The remaining represented `Ndu*` complex-I or assembly perturbations in the
training count file followed the same pattern: `Ndufa4`, `Ndufa6`, `Ndufb9`,
`Ndufb10`, and `Ndufb11` had 1 DEG, while `Ndufa8`, `Ndufa11`, `Ndufa12`,
`Ndufaf2`, `Ndufaf4`, `Ndufaf5`, `Ndufb3`, and `Ndufb7` had 0. Thus 23
represented NADH-dehydrogenase targets gave only 0 or 1 DEG each in the exact
focal endpoint.

I also checked whether complex-I perturbations secondarily regulated `Ndufs3`
or other OXPHOS transcripts in the focal class. For `Ndufs2`, `Ndufs4`,
`Ndufs7`, `Ndufs8`, `Ndufv1`, `Ndufv2`, `Ndufa9`, `Ndufa10`, `Ndufb8`, and
`Ndufc2`, the measured `Ndufs3` row always had adjusted p=1 with small signed
changes, and `Cox5a`, `Sdha`, and `Uqcrc2` were likewise far from FDR support.
The large apparent fold changes among the top nominal rows for zero-effect
targets all had adjusted p=1 and behaved like sparse-expression pseudocount
artifacts, so I did not use them as analog evidence.

The same-experiment July Findings corpus gave the same high-level
interpretation for the exact genes available in training:

- `Ndufs2:F004` reported that 21 represented `Ndufa/Ndufb/Ndufc/Ndufs/Ndufv`
  complex-I subunits and assembly factors had near-zero whole-signature
  correlations and no FDR overlap with the three sparse `Ndufs2` responder
  genes across all classes.
- `Ndufs4:F001-F003` reported no downstream `Ndufs4` DE across all 20
  recovered neuronal groups and lack of an ATF4/ISR, proteostasis, redox, or
  mitophagy program despite the known severity of complete `Ndufs4` loss.
- `Ndufs8:F001`, `Ndufs8:F003`, and `Ndufs8:F004` reported a nearly flat
  downstream surface, absence of canonical mitochondrial-stress markers, and
  failure of the closest held-in complex-I relatives to converge.
- `Ndufv2:F002-F003` reported that `Ndufv2` did not phenocopy the other
  represented complex-I targets and that its single `Cdc40` hit should not be
  treated as a broad mitochondrial program.

Those internal corpus records were used only to confirm that the focal 0/1
pattern was part of a screen-wide buffered class. The numerical prediction was
based on the declared training CSV and parquet.

## Target-specific prediction

### Ndufs3

`Ndufs3` encodes a nuclear complex-I core subunit. External data make it a
biologically appropriate comparison to `Ndufs2`, `Ndufs8`, `Ndufs7`,
`Ndufv1`, and `Ndufv2`: all participate in NADH:ubiquinone oxidoreductase,
and direct NDUFS3 studies place the protein in the stepwise assembly of the
enzyme. The closest held-in structural analogs were `Ndufs2` and `Ndufs8`; in
the focal class, both produced one FDR-significant gene, and in both cases the
hit was the target transcript itself rather than a downstream mitochondrial
stress gene. The direct counterexamples were `Ndufs4`, `Ndufs7`, and `Ndufv1`,
which are also complex-I subunits but had 0 focal DEGs, and `Ndufv2`, which
had a single non-self hit.

The intervention chain I applied was:

`Ndufs3` CRISPR loss of function -> impaired complex-I N-module/core assembly
or stability -> possible respiratory stress -> selection of severely affected
neurons or a mild survivor-conditioned nuclear RNA response -> FDR-thresholded
snRNA-seq DEG count.

Complete NDUFS3 loss can compromise complex I, but the training data show that
acute sparse AAV CRISPR of closely related complex-I subunits usually stopped
at the first step of that chain in recovered neurons. It did not propagate into
a coherent ATF4, OXPHOS-compensation, redox, or mitophagy signature in `151 TH
Prkcd Grin2c Glut`. Therefore I predict a nonzero but minimal count, driven
mostly by the possibility that the `Ndufs3` transcript itself is depleted
strongly enough to pass BH correction, not by a broad downstream response.

Prediction: **1 DEG**.

## Limits and uncertainty

This is a close 0-versus-1 call. The focal complex-I analogs split between 0
and 1 DEGs, and the one-DEG cases were often only self-transcript calls.
Measured self-transcript loss is not an editing-efficiency estimate, so the
fact that `Ndufs2` and `Ndufs8` crossed FDR 0.05 on their own transcripts does
not guarantee that `Ndufs3` will do the same. Conversely, full NDUFS3 or
NDUFS4 deficiency is bioenergetically severe in other systems, but the
postnatal mosaic screen repeatedly failed to convert complex-I membership into
a large nuclear stress transcriptome. The count of 1 is therefore an
assay-calibrated prediction for this specific snRNA-seq DEG endpoint, not a
claim that `Ndufs3` perturbation is biologically weak.
