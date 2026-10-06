# Prediction trace for 089_Gatad1

## Question and scope

The requested manifest contains one held-out perturbation, `Gatad1`. I interpreted the task as a point prediction of how many measured genes would pass `pvals_adj < 0.05` for a `Gatad1` CRISPR loss-of-function perturbation in `151 TH Prkcd Grin2c Glut` neurons, with the count defined exactly like the supplied focal training endpoint:

```text
n_degs = number of measured genes with Benjamini-Hochberg adjusted Wilcoxon p-value < 0.05
```

The count can include the target transcript itself if it is significantly changed. A one-gene answer can therefore be "target RNA only", as in `Gatad2b`. I treated weak target-RNA knockdown as part of the assay design, not as evidence that editing failed.

## Sources used

- Held-out target list: `[local file: 089_Gatad1.csv]`.
- Focal-cell training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Per-gene differential expression table: `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`, especially the NuRD/MBD and chromatin-repressor claims around `Chd4`, `Gatad2b`, `Mbd2`, `Mbd5`, `Zmynd8`, and `Setdb1`.
- Distributed Agents runtime profile tools, run-local artifacts `gatad1_chromatin_compare.json` and `gatad1_chromatin_inspect.json`, used to compare focal log-fold-change vectors among selected training perturbations.
- Distributed Agents gene-annotation cache, including Gene Ontology terms and CORUM v5.0 complexes projected with MGI orthology downloaded 2026-09-13.
- PubMed literature:
  - Lomniczi, Wright, Castellano et al. 2015, Nat Commun, DOI `10.1038/ncomms10195`, PMID `26671628`: GATAD1 can repress the puberty genes `KISS1` and `TAC3` in hypothalamus by recruiting KDM1A and reducing promoter H3K4me2.
  - Gong, Brackertz and Renkawitz 2006, Mol Cell Biol, DOI `10.1128/MCB.00409-06`, PMID `16738318`: p66alpha/p66beta, encoded by `GATAD2A/GATAD2B`, are SUMO-regulated transcriptional repressors that interact with MBD2/MBD3 and Mi-2/NuRD components.
  - Theis, Sharpe, Matsumoto et al. 2011, Circ Cardiovasc Genet, DOI `10.1161/CIRCGENETICS.111.961052`, PMID `21965549`: inherited human `GATAD1` mutation was linked to recessive dilated cardiomyopathy, supporting a nuclear chromatin-related function but outside the neuronal context.
  - Pang, Zhu, Shyy et al. 2024, J Mol Histol, DOI `10.1007/s10735-024-10297-z`, PMID `39641830`: cardiomyocyte-specific `Gatad1` deletion in mice did not produce cardiomyopathy up to 18 months, a reminder that Gatad1 loss can be context-buffered.

## Computations over the supplied dataset

I first verified that the manifest contains only `Gatad1` and that `Gatad1` is absent from the focal training-count CSV, as expected for a held-out target.

I summarized the 1,674 focal training perturbations to calibrate response breadth. The endpoint is very sparse: median `n_degs` is 0, the 75th percentile is 1, the 90th percentile is 2, the 95th percentile is 18, and the maximum is 2,677. Thus a weak chromatin-regulator perturbation is much more likely to round to 0 or 1 than to tens of DEGs unless a close measured analog shows a real 151-cell response.

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for chromatin candidates selected from Gatad1 biology and nearby within-corpus chromatin claims. The focal table has 17,259 measured genes per training perturbation. The relevant observed counts were:

| training perturbation | focal n_degs | expression-pattern evidence and interpretation |
|---|---:|---|
| `Gatad2b` | 1 | The only FDR<0.05 feature was `Gatad2b` itself, log2FC -0.498 and adjusted p=0.00348. This is a useful self-transcript-only boundary for a GATA zinc-finger NuRD adaptor, not a broad downstream response. |
| `Mbd2` | 0 | Same MBD/MeCP1/NuRD neighborhood as `Gatad2b`, completely flat in the focal count table. |
| `Mbd5` | 0 | MBD-family chromatin disease gene, also flat, bounding the idea that methyl-CpG-associated genes generically respond in this assay. |
| `Phf21a` | 6 | CORUM v5.0 places human PHF21A in LSD1/CoREST/HDAC complexes. Because the reported neuronal GATAD1 mechanism recruits KDM1A, `Phf21a` is a loose KDM1A-corepressor analog; its six hits (`Rreb1`, `Col4a5`, `Ccdc141`, `Lats2`, `Dbp`, `Wls`) indicate only a small response in the focal cells. |
| `Rest` | 0 | A REST-corepressor boundary; it shows that an annotated transcriptional repressor can be silent at the basal postnatal neuronal RNA surface. |
| `Dnmt3a` | 0 | The acute DNA methylation writer perturbation is flat in 151 cells despite relation to MBD readers. This is a temporal/cell-state counterexample to projecting from broad chromatin function alone. |
| `Mecp2` | 16 | A modest MBD-family positive control with a distinct 151 signature, not a GATAD1-like program. |
| `Chd4` | 100 | A strong focal NuRD ATPase/ChAHP response with 52 up and 48 down significant genes. Corpus claim `claim:85bada0191e4170beb10` states that represented NuRD/MBD-adjacent perturbations do not collapse into one shared neuronal loss-of-function signature; `Chd4` therefore serves as an active counterexample rather than as a direct `Gatad1` template. |
| `Zmynd8` | 74 | Another active chromatin reader/repressor. The Distributed Agents corpus specifically separates this from generic ZMYND-family or NuRD loss, so I used it only to show that chromatin responses are detectable in this cell group. |
| `Setdb1` | 22 | H3K9 repression/HUSH-adjacent perturbation with a detectable but smaller 151 response. It is mechanistically farther from Gatad1 than the KDM1A and MBD/NuRD comparators. |
| `Sin3a` | 1,433 | Broad chromatin/corepressor perturbation with a very large response; because REST, MBD2, and HDAC-family candidates are flat, this is a boundary on response breadth rather than an analog for Gatad1. |
| `Hdac5`, `Hdac8` | 0, 0 | These are not the canonical NuRD HDAC1/2 subunits, but they helped check that perturbing an HDAC-family gene does not automatically produce focal DEGs. |

For a local signature check, I compared log2 fold-change vectors for `Gatad2b`, `Mbd2`, `Mbd5`, `Chd4`, `Zmynd8`, `Setdb1`, `Sin3a`, `Hdac5`, and `Hdac8`. The runtime profile comparison used all 17,259 focal features and top-200 signed tails. It recovered the endpoint split above: `Gatad2b` had one significant feature, `Mbd2`/`Mbd5`/`Hdac5`/`Hdac8` had none, `Setdb1` had 22, `Zmynd8` had 74, `Chd4` had 100, and `Sin3a` had 1,433. `Gatad2b` and `Mbd2` had zero significant-gene overlap with the active `Chd4`, `Zmynd8`, or `Setdb1` signatures. Their whole-profile correlations to active signatures were moderately positive because most of the vector is non-significant background; the signed top-tail overlaps were small. For example, `Gatad2b` versus `Chd4` shared only 26/200 positive-tail and 49/200 negative-tail genes, and `Mbd2` versus `Chd4` shared only 18/200 positive-tail and 27/200 negative-tail genes. I therefore did not pool the broad chromatin responders into a generic estimate.

The same-experiment Distributed Agents corpus was useful mostly for preventing a false NuRD extrapolation. Direct target context for `Gatad1` was absent, but the frozen claims report that represented NuRD/MBD-adjacent perturbations are target-selective: `Mbd2` did not phenocopy `Gatad2b`, `Mbd2`/`Gatad2b` did not phenocopy `Chd4`, and `Zmynd8`/`Setdb1`/`Chd4` mark separable chromatin-repressor branches rather than a universal loss signature.

## Gatad1-specific reasoning

`Gatad1` is a nuclear GATA zinc-finger-domain protein annotated to chromatin organization and regulation of DNA-templated transcription, but it is not the p66beta NuRD subunit encoded by `Gatad2b`. The strongest neuronal mechanism I found was the Lomniczi et al. hypothalamic study: forced GATAD1 maintained juvenile repression of `KISS1` and `TAC3` through KDM1A recruitment and loss of H3K4me2 at those promoters. That mechanism is transcriptionally specific, was shown in hypothalamic puberty circuitry, and points to a KDM1A/LSD1-like corepressor axis rather than to broad CHD4-dependent NuRD remodeling in thalamic `Prkcd`/`Grin2c` glutamatergic cells.

The closest measured focal analogs all argue for a zero or near-zero count:

- The p66/MBD NuRD edge was flat: `Gatad2b` had only a self-transcript hit and `Mbd2` had zero downstream hits.
- The methyl-CpG/MBD reader neighborhood was mostly flat or low: `Mbd5` and `Dnmt3a` were zero, while `Mecp2` reached only 16 DEGs and had a distinct signature.
- The closest available KDM1A-corepressor component, `Phf21a`, had just 6 focal DEGs; ideal nodes such as `Kdm1a` and `Rcor1/2/3` were not present in the training-count table.
- Larger signatures from `Chd4`, `Zmynd8`, `Setdb1`, and especially `Sin3a` demonstrate assay sensitivity for chromatin perturbations in 151 cells, but corpus findings and the profile comparison both show that those signatures are branch-specific and should not be transferred wholesale to `Gatad1`.

Given those comparisons, I expect `Gatad1` loss to be buffered at the FDR<0.05 endpoint in this acute, sparse, postnatal neuronal assay. I chose `0` rather than `1` because the data contain no evidence for a Gatad1-specific downstream program in the focal thalamic class, and the self-transcript-only `Gatad2b` result is not enough to assume that `Gatad1` mRNA itself will pass FDR under the weaker average mRNA downregulation of this pooled AAV CRISPR design.

## Final point

`Gatad1`: predicted `n_degs = 0`.

## Limits

The major limitation is that direct `Gatad1` same-experiment evidence is absent from the Distributed Agents corpus and from both supplied training files by construction. Several ideal comparators were also unavailable in the focal training-count table, including `Kdm1a`, `Rcor1`, `Rcor2`, `Rcor3`, `Gatad2a`, `Mbd3`, `Hdac1`, and `Hdac2`, so the KDM1A and canonical NuRD axes had to be inferred from weaker components. The literature on GATAD1 is sparse and mostly outside postnatal thalamic glutamatergic neurons. Finally, distinguishing 0 from a one-gene self-transcript effect is below the resolution of pathway evidence; the zero call is a point estimate, not high confidence that no Gatad1 transcript knockdown will be measured.
