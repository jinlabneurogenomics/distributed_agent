# DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The held-out manifest `[local file: 114_Irf7.csv]` contains one requested perturbation:

```tsv
target_name
Irf7
```

I interpreted the requested endpoint as the assay-defined count of measured genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` cell group after a sparse postnatal AAV-CRISPR loss-of-function perturbation. The count includes any measured gene passing the threshold, including a possible self-transcript row if it passes. Because `Irf7` was held out completely, I did not use an `Irf7` expression signature or `Irf7` training count; neither is present in the parquet or focal count CSV.

A zero prediction is therefore "no gene is expected to pass this exact Wilcoxon/BH threshold in this cell group", not "IRF7 is biologically irrelevant" and not a claim about infected, interferon-stimulated, glial, immune, germline, or developmental contexts.

## Sources used

- Training endpoint counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`, especially the frozen IFN/IRF/STAT/innate-sensor claims over `Ifnar1`, `Ifnar2`, `Irf1`, `Irf2`, `Irf3`, `Irf8`, `Irf9`, `Stat1`, `Stat2`, `Ifih1`, `Adar`, `Tlr2`, `Tlr4`, and related targets.
- PubMed literature for external mechanism:
  - Honda K et al., 2005, *Nature*, DOI `10.1038/nature03464`, PMID `15800576`: IRF7 is essential for virus- and TLR9-subfamily-induced type-I-interferon production.
  - Prakash A et al., 2005, *Journal of Biological Chemistry*, DOI `10.1074/jbc.M501289200`, PMID `15767254`: in vivo IRF7 expression is stimulus-dependent in most tissues, while plasmacytoid dendritic cells have high constitutive IRF7 and rapid IFN production.
  - Hiscott J, 2007, *Journal of Biological Chemistry*, DOI `10.1074/jbc.R700002200`, PMID `17395583`: IRF3/IRF7 are central transcription factors for antiviral type-I-IFN induction.
  - Ivashkiv LB and Donlin LT, 2014, *Nature Reviews Immunology*, PMID `24362405`: IFNAR signaling through JAK/STAT and IRF9/ISGF3 is ligand- and context-dependent.
  - Au-Yeung N et al., 2013, *JAKSTAT*, DOI `10.4161/jkst.23931`, PMID `24069549`: STAT1/STAT2/IRF9 regulate ISG transcription downstream of interferon receptors.
  - Schneider WM et al., 2014, *Annual Review of Immunology*, PMID `24555472`: interferon-stimulated genes form a broad antiviral effector network.

## Computation over the supplied DE data

I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for hand-curated interferon, IRF, STAT, innate-sensor, TLR, TRAF3, and NF-kB analogs. For each perturbation I recomputed:

```python
n_degs = sum(pvals_adj < 0.05)
```

This reproduced the focal CSV counts for the relevant training perturbations and showed a nearly complete local null:

| training perturbation class | training targets in the focal count CSV | observed `n_degs` |
| --- | --- | --- |
| IRF transcription factors | `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, `Irf9` | all `0` |
| Type-I/II IFN signaling | `Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`, `Stat2` | all `0` |
| Type-I/II IFN signaling singleton | `Stat1` | `1`, and the only focal DEG was the `Stat1` self row |
| RNA/ADAR axis | `Adar`, `Ifih1` | both `0` |
| TLR/NF-kB neighbors | `Tlr2`, `Tlr3`, `Tlr4`, `Tlr5`, `Tlr7`, `Tlr8`, `Traf3`, `Nfkb1`, `Rel` | all `0` |

I also ran a run-local signed-profile comparison on 17 nodes across the same focal-cell log-fold-change profiles. Every one of `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, `Irf9`, `Ifnar1`, `Ifnar2`, `Ifih1`, `Adar`, `Stat2`, `Tlr3`, `Tlr7`, `Traf3`, `Nfkb1`, and `Rel` had `0` significant features among 17,259 shared measured features; `Stat1` alone had `1` significant feature. The comparison therefore did not reveal a subthreshold but coherent interferon module hidden behind the strict FDR cutoff.

Finally, I checked canonical ISG/MHC sentinel genes in the same focal profiles. `Ifnb1`, `Isg15`, `Ifit1`, `Ifit2`, `Ifit3`, `Oas1a`, `Oasl2`, `Rsad2`, `Usp18`, `Mx1`, `Cxcl10`, `B2m`, `H2-K1`, `H2-D1`, `Tap1`, and `Psmb8` were not FDR-significant in the IRF, IFNAR, `Adar`, `Ifih1`, `Tlr`, `Traf3`, `Nfkb1`, or `Rel` perturbations in the focal group. Some extremely lowly detected IFN sentinels had large absolute log-fold changes from pseudocount-scale behavior, but their adjusted p-values were `1.0`, so I treated them as uninformative.

## Target-specific reasoning

### `Irf7`

**Biological role.** IRF7 is a pivotal type-I-interferon transcription factor: viral sensing and MyD88-dependent TLR9-subfamily pathways use IRF7 to induce IFN-alpha/beta genes, and IRF3/IRF7 activation is a core step in the host antiviral response (Honda et al. 2005; Hiscott 2007). That prior says that a productive `Irf7` loss-of-function can matter strongly in IFN-producing cells or after pathogen/nucleic-acid stimulation.

**Why the same-experiment analogs are appropriate.**

- `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, and `Irf9` are the closest represented IRF-family and IFN-transcription-factor perturbations. All had `0` DEGs in `151 TH Prkcd Grin2c Glut`.
- `Ifnar1`, `Ifnar2`, `Stat1`, `Stat2`, and `Irf9` bracket the canonical type-I-IFN receptor to ISGF3 arm that should maintain or amplify `Irf7` and ISG expression if tonic IFN were driving these neurons. In the focal group `Ifnar1`, `Ifnar2`, `Stat2`, and `Irf9` had `0` DEGs; `Stat1` had `1` DEG, the depleted `Stat1` transcript itself, with no downstream ISG/MHC module.
- `Ifngr1`, `Ifngr2`, and `Irf1` test the related IFN-gamma/MHC-I inflammatory arm. All were `0` in the focal group.
- `Ifih1` and `Adar` probe the MDA5/endogenous-dsRNA axis that should converge through type-I IFN and ISGs when active. Both were `0` in the focal group.
- `Tlr3`, `Tlr7`, `Tlr8`, `Traf3`, `Nfkb1`, and `Rel` are upstream nucleic-acid/TLR and NF-kB-side comparators that can feed IRF7-containing antiviral programs in stimulated immune settings. They were also `0` in the focal group.

**Expression-pattern evidence.** The selected same-cell profiles give a pathway-wide null rather than one bad paralog comparison. The direct focal counts were:

```text
Irf1 0; Irf2 0; Irf3 0; Irf5 0; Irf8 0; Irf9 0
Ifnar1 0; Ifnar2 0; Ifngr1 0; Ifngr2 0; Ifih1 0; Adar 0
Stat1 1; Stat2 0
Tlr2 0; Tlr3 0; Tlr4 0; Tlr5 0; Tlr7 0; Tlr8 0; Traf3 0; Nfkb1 0; Rel 0
```

Distributed Agents corpus claims over the same experiment summarize the same pattern at broader scope: basal neuronal `Adar` or `Ifih1` loss did not elicit an MDA5/type-I-IFN/ISG program; IFNAR receptor and ISGF3-associated perturbations did not reveal a tonic type-I-IFN/IFNAR program; and represented IRF/STAT/TLR/NF-kB neighbors did not define a recurrent IFN/JAK-STAT module in juvenile unstimulated neurons.

**Prediction.** The external literature would make `Irf7` a strong candidate under viral infection, exogenous IFN, or in plasmacytoid dendritic cells, where IRF7 is constitutive or induced as part of a positive feedback circuit (Honda et al. 2005; Prakash et al. 2005). Those are precisely the contexts missing here: the perturbation was acute and mosaic in NeuN-enriched postmitotic neurons, no IFN or pathogen challenge was applied, and glial/immune interferon amplification was largely absent. Within this assay the type-I-IFN pathway is quiescent across the closest represented receptor, STAT, IRF, sensor, and TLR perturbations, so an `Irf7` knockout is more likely to look like `Irf1/2/3/5/8/9` and `Ifnar1/2/Stat2` than like a broad antiviral-state collapse.

I therefore predict no FDR-significant genes:

```text
Irf7 predicted_n_degs = 0
```

## Limits

- `Irf7` itself is held out, so the count is extrapolated from neighboring perturbations. No same-experiment `Irf7` signature, self-transcript effect, matched nucleus count, or DEG count was used.
- The nearest analogs are mechanistic but not identical. IRF7 has a more specific role in IFN-alpha positive feedback than `Irf1`, `Irf2`, or `Irf9`, and the parquet lacks held-out `Irf7` and several core pathway perturbations such as `Mavs`, `Tbk1`, and `Ikbke`.
- The inference is tuned to a basal P16-to-P37/44 neuronal CRISPR assay. It should not be transferred to viral challenge, exogenous IFN, immune cells, plasmacytoid dendritic cells, glia-rich CNS preparations, or germline disease models.
- Self-target depletion can contribute one DEG for expressed genes, as in the `Stat1` focal profile, but sparse CRISPR and low basal IRF7 expression make a significant `Irf7` self row unlikely; this is still an uncertainty that cannot be checked directly because the held-out `Irf7` rows were removed.
