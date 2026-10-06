# Prediction trace for `151 TH Prkcd Grin2c Glut`

## Question and interpretation

The requested held-out perturbation list contains one gene, `Tbk1`. I interpreted the endpoint as the integer number of genes in the focal cell group `151 TH Prkcd Grin2c Glut` with `pvals_adj < 0.05` in the same Wilcoxon/BH differential-expression pipeline used for the supplied training targets. The target transcript itself is part of the measured feature set when it is expressed, so a prediction of 1 could reflect only the guide-targeted mRNA crossing FDR; I still predicted 0 because the closest observed TBK1-neighborhood targets either had no FDR genes or only their own transcript, and `Tbk1` is an unstimulated signaling kinase rather than a constitutive transcription-factor target.

## Sources used

- The focal training endpoint in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- The raw differential-expression parquet `training_de_all_cell_groups.parquet`, restricted to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Distributed Agents same-experiment corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`.
  - No target-centered corpus card existed for `Tbk1` itself.
  - I used corpus findings for `Irf3`, `Ifih1`, `Stat1`, `Atg5`, `Becn1`, `Rb1cc1`, and `Sqstm1`. The induced corpus topology separated these into a pathogen-sensing/IFN component, `Ifih1`-`Irf3`-`Stat1`, and a selective/core-autophagy component, `Atg5`-`Becn1`-`Rb1cc1`-`Sqstm1`.
- PubMed literature on TBK1 biology:
  - TBK1/IKKepsilon are the kinases that activate IRF3/IRF7 downstream of viral RNA, TLR3/4-TRIF, and cGAS-STING-like innate signaling: Fitzgerald et al. 2003, PMID 12692549, DOI `10.1038/ni921`; Sharma et al. 2003, PMID 12702806, DOI `10.1126/science.1081315`; McWhirter et al. 2003, PMID 14679297, DOI `10.1073/pnas.2237236100`.
  - STING recruits and is phosphorylated by TBK1 as part of a ligand-driven oligomeric signaling assembly: Zhang et al. 2019, PMID 30842653, DOI `10.1038/s41586-019-1000-2`.
  - TBK1 phosphorylates selective-autophagy adaptors, including OPTN, CALCOCO2/NDP52, TAX1BP1, and SQSTM1/p62, to amplify recruitment to ubiquitinated damaged mitochondria: Richter et al. 2016, PMID 27035970, DOI `10.1073/pnas.1523926113`.
  - Human TBK1 haploinsufficiency can cause ALS/frontotemporal dementia, so a flat acute transcriptional prediction is not a claim that the gene is biologically unimportant: Freischmidt et al. 2015, PMID 25803835, DOI `10.1038/nn.4000`.

## Computations over the DE matrix

The parquet is sorted by `group_name`; row-group metadata showed that row groups 547-580 contain `151 TH Prkcd Grin2c Glut`. I extracted only those row groups, only the columns needed for profile comparison, and only represented perturbations connected to TBK1 biology.

```python
pf = pq.ParquetFile(parquet)
for row_group in focal_row_groups:
    table = pf.read_row_group(
        row_group,
        columns=[
            "names", "gene_target", "scores", "logfoldchanges",
            "pvals", "pvals_adj", "n_pert_matched", "n_ctrl_matched",
        ],
    )
    table = table.filter(pc.is_in(table["gene_target"], value_set=pa.array(analogs)))
```

Each extracted candidate target had 17,259 measured genes in the focal group. I recomputed `sum(pvals_adj < 0.05)` from those rows and checked it against the training count CSV. I also used the signed Wilcoxon `scores` vector for a focused `profile_compare` over 17 TBK1-adjacent targets. That comparison found 13/17 with zero significant features in `151 TH Prkcd Grin2c Glut`; across all 136 pairwise score correlations among these candidates, the largest absolute Pearson correlation was only 0.079, so there was no hidden shared TBK1-neighborhood state just below the FDR threshold.

The whole focal endpoint was sparse: 1,205 of 1,674 training targets had zero DEGs, the median was 0, the 75th percentile was 1, the 90th percentile was 2, and the 95th percentile was 18. A weak or ligand-conditional pathway expectation should therefore stay at 0 unless the matched training perturbations show a real transcriptomic response.

## Target-specific reasoning

### `Tbk1`

TBK1 sits at two relevant interfaces. First, it is the noncanonical IKK-family kinase that links TRIF, RIG-I/MDA5-MAVS, and cGAS-STING to IRF3/7 and type-I interferon transcription. Second, it amplifies ubiquitin-dependent selective autophagy by phosphorylating OPTN, p62/SQSTM1, CALCOCO2/NDP52, and TAX1BP1. The closest direct screen targets for both arms were quiescent in the focal neurons.

| training perturbation | observed `151` `n_degs` | focal expression-pattern evidence | interpretation for `Tbk1` |
| --- | ---: | --- | --- |
| `Irf3` | 0 | no FDR genes; all top `pvals_adj` were 1.0 | Direct downstream transcription factor for TBK1 antiviral signaling is silent without viral, TLR, STING, or injury stimulation. |
| `Ifih1` | 0 | no FDR genes; all top `pvals_adj` were 1.0 | MDA5/RNA-sensing branch was also off. Distributed Agents `Ifih1:F003` reported no convergence with ADAR, IFN receptor, IRF, STAT, NF-kB, or TLR comparators. |
| `Tlr3`, `Tlr4` | 0, 0 | both had zero FDR genes; top adjusted p-values were 1.0 | Upstream TRIF-linked pattern-recognition receptors did not reveal a tonic TBK1/IRF3 program. |
| `Traf3` | 0 | zero FDR genes; top adjusted p-values were 1.0 | Adapter connecting innate receptors to TBK1/NF-kB was inert in these nuclei. |
| `Chuk`, `Nfkb1`, `Rel` | 0, 0, 0 | zero FDR genes; `Chuk`'s strongest focal row was `Cops2` with q=0.727; `Nfkb1` top rows all had q=1.0 | Canonical NF-kB comparators were not acting as active basal inflammatory regulators in the focal group. |
| `Ifnar1`, `Ifnar2`, `Stat2` | 0, 0, 0 | no IFN-receptor/ISGF3 downstream FDR genes | Even the downstream IFNAR signal-transduction arm was flat. |
| `Stat1` | 1 | the only FDR gene was `Stat1` itself, log2FC -1.30, q=0.027 | Any IFN/JAK-STAT analog effect was limited to the edited transcript. Distributed Agents `Stat1:F002` and `Stat1:F003` likewise found no recurrent IFN/ISG/MHC-I module across represented IFN/STAT/IRF perturbations. |
| `Atg5` | 0 | no focal FDR genes; `Pdia6` was closest with q=0.105 | Core LC3-lipidation loss had at most a subthreshold ER-chaperone trace. |
| `Atg16l1` | 0 | no focal FDR genes; all top adjusted p-values were 1.0 | Same LC3-conjugation complex as ATG5 but completely flat here. |
| `Becn1` | 0 | no focal FDR genes; all top adjusted p-values were 1.0 | VPS34/autophagy nucleation loss had no focal 151 TH response. |
| `Rb1cc1` | 4 | `Calr`, `Hspa5`, target `Rb1cc1`, and `Pdia6` were down at FDR<0.05 | The strongest autophagy-initiation comparator produced only a four-gene ER-chaperone/self-transcript state, not a broad autophagy, p62, lysosomal, or IFN response. |
| `Sqstm1` | 1 | only target `Sqstm1` passed FDR<0.05; `Sfxn5` was subthreshold at q=0.092 | The measured p62 cargo receptor was self-only in the focal group. Distributed Agents `Sqstm1:F006` found that p62 loss did not phenocopy represented autophagy, NRF2, NF-kB, mTOR, or lysosomal perturbations. |
| `Park7` | 1 | only target `Park7` passed FDR<0.05 | A neuronal mitochondrial/oxidative-stress disease comparator did not create a larger TBK1/autophagy-like program. |

Direct TBK1 partners that would have been even closer tests were not available as training perturbations in the focal count table: `Ikbke`, `Tank`, `Tmem173`/STING, `Mb21d1`/cGAS, `Ddx58`, `Mavs`, `Optn`, `Calcoco2`, `Tax1bp1`, `Pink1`, and `Prkn` were absent. This makes the prediction an extrapolation from upstream/downstream arms rather than a same-complex interpolation.

The Distributed Agents corpus findings matched the raw focal data. `Irf3:F003` treated the represented IRF3-pathway relatives as mostly flat and concluded that the pathogen-recognition-to-IFN axis was off in unstimulated neuronal nuclei. `Stat1:F002/F003` reached the same conclusion for IFN receptors and STAT/IRF outputs. On the autophagy side, `Atg5:F002`, `Atg5:F004`, `Becn1:F004`, and `Rb1cc1:F005` emphasized that core autophagy perturbations are sparse and not transcriptomically interchangeable; the only reproducible module was a small `Calr`-centered response in `155 MB Glut`, not in the focal 151 TH group.

I therefore expect acute sparse `Tbk1` loss in uninfected, NeuN-enriched, postnatal `151 TH Prkcd Grin2c Glut` nuclei to be buffered at the RNA level. TBK1's dominant roles in the cited literature require cytosolic DNA/RNA, TLR ligands, damaged mitochondria, or ubiquitinated cargo to recruit and activate the kinase. Those triggers were not part of the perturb-seq experiment, and the measured pathway neighbors show that neither innate immune nor selective-autophagy circuitry was tonically driving a detectable nuclear program. The integer point prediction is:

```tsv
target_name	predicted_n_degs
Tbk1	0
```

## Limits

- The prediction is weakest where direct TBK1 complex members were missing from training. `Tmem173`, `Mavs`, `Ikbke`, `Optn`, `Tax1bp1`, and `Calcoco2` would have been better analogs than the represented receptor/IRF/ATG nodes.
- This assay measures nuclear RNA 3-4 weeks after P16 sparse CRISPR; it does not measure TBK1 kinase activity, OPTN/p62 phosphorylation, mitophagic flux, LC3 lipidation, ubiquitin-coated mitochondria, or protein aggregates.
- The focal group had only a few hundred perturbed nuclei per analog target. A one-gene self-transcript hit for `Tbk1` could move the true count from 0 to 1 even if all downstream biology is flat.
- TBK1 is disease-relevant over chronic or inflammatory time scales. A zero in this juvenile unstimulated neuronal endpoint should not be generalized to aged neurons, glia, viral challenge, STING activation, axon injury, or ALS/FTD degeneration.
