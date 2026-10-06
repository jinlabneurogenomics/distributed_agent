# VAPB DEG-count prediction trace

## Question and scope

The held-out manifest contains one requested target:

```tsv
target_name
Vapb
```

I interpreted the task as a point prediction for the exact endpoint in `151 TH Prkcd Grin2c Glut`: the number of measured mouse genes with `pvals_adj < 0.05` after an acute, sparse AAV-CRISPR loss-of-function perturbation of `Vapb`. `151 TH Prkcd Grin2c Glut` was treated as a thalamic glutamatergic class; `TH` is the atlas anatomy token, not tyrosine hydroxylase.

The endpoint includes any measured gene passing the FDR gate, including the target transcript itself. I did not treat loss of the target mRNA as an editing-efficiency proxy, because the atlas calibration notes that self-transcript depletion is only weak QC context in this mosaic Cas9/snRNA-seq design.

## Sources

- Input training endpoint: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, 1,674 non-held-out perturbations.
- Input differential-expression parquet: `training_de_all_cell_groups.parquet`; I filtered to `group_name == "151 TH Prkcd Grin2c Glut"` and to VAPB-relevant training targets, then counted `pvals_adj < 0.05` and inspected the significant genes and log2 fold changes.
- Distributed Agents same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`, especially the `Atf6`, `Hspa5`, `Sec63`, `Vcp`, `Vps35`, `Vps54`, and ER/lysosome/UPR claims.
- Distributed Agents runtime profile comparison: a focal-cell comparison over 30 ER contact-site, lipid-transfer, ER-stress, ER/Golgi, retromer/GARP, and ALS/ER-proteostasis candidates.
- External literature retrieved with PubMed:
  - VAP proteins recruit FFAT lipid-transfer proteins such as OSBP and CERT at ER-Golgi contact sites: Peretti et al. 2008, DOI `10.1091/mbc.e08-05-0498`, PMID `18614794`.
  - VAPB P56S forms aggregates and perturbs FFAT-protein binding / VAPA-B function in neurons: Teuling et al. 2007, DOI `10.1523/JNEUROSCI.2661-07.2007`, PMID `17804640`.
  - VAPB regulates UPR output and ALS8 P56S interferes with VAPB-mediated UPR signaling: Kanekura et al. 2006, DOI `10.1074/jbc.M605049200`, PMID `16891305`.
  - VAPB interacts with ATF6 and can modulate ATF6-regulated transcription: Gkogkas et al. 2008, DOI `10.1093/hmg/ddn040`, PMID `18263603`.
  - VAPB links CFTR proteostasis to lipid homeostasis through ATF6 and an ERAD cluster containing FAF1/VCP/BAP31/Derlin-1: Ernst et al. 2016, DOI `10.1074/jbc.M115.692749`, PMID `26740627`.
  - VAPB-PTPIP51 tethers regulate ER-mitochondria contacts and neuronal synaptic activity: Gomez-Suaga et al. 2019, DOI `10.1186/s40478-019-0688-4`, PMID `30841933`; PTPIP51 coiled-coil domain dissection in Morotz et al. 2022, DOI `10.3389/fcell.2022.920947`, PMID `36120587`.
  - Pure VAPB loss of function in mouse was weak and late compared with ALS8 mutant stress biology: Kabashi et al. 2013, DOI `10.1093/hmg/ddt080`, PMID `23446633`.

## Dataset calibration

The focal training counts are extremely zero-inflated:

- 1,205 / 1,674 training perturbations had `n_degs = 0`.
- Median was 0; the 75th percentile was 1; the 95th percentile was 18; the maximum was 2,677.
- Thus a biologically plausible ER or trafficking gene should not automatically be assigned a nonzero response in this endpoint.

I used a mechanistically seeded candidate set rather than a global heuristic. The set covered direct VAP/FFAT-like lipid-contact genes, ER-membrane and UPR genes, retrograde/endosomal trafficking genes, and stronger ER-proteostasis stressors that define the high side of the scale.

For each candidate in the 30-gene profile comparison I used the actual 151 log-fold-change vector and `pvals_adj < 0.05` gate. The candidates separated into:

- No significant genes: `Atf6`, `Osbpl2`, `Cert1`, `Acbd5`, `Vps13a`, `Vps13b`, `Vps13c`, `Atl3`, `Ddhd2`, `Sar1b`, `Sec23a`, `Spast`, `Tfg`.
- Self-target or near-self tiny profiles: `Amfr` 1, `Atl1` 1, `Bcap31` 1, `Reep2` 1, `Sqstm1` 1, `Manf` 3, `Vcp` 2.
- Small but real ER or trafficking profiles: `Hspa5` 5, `Sec63` 11, `Vps35` 17, `Vps54` 31.
- Stronger, less direct ER/glycosylation/UFMylation or endolysosomal stress perturbations: `Dhdds` 116, `Gfpt1` 311, `Rab7` 501, `Ufc1` 572, `Uba5` 2,677.
- A strong ALS/FTD RNA-binding-protein counterexample: `Tardbp` 210.

The exact VAP paralog `Vapa` and the direct ER-mitochondria tether partner `Rmdn3` / PTPIP51 were not present in the training-count CSV; neither were `Fus`, `Mfn2`, or `Osbpl8`. That made direct paralog/partner transfer unavailable.

## Target-specific reasoning for `Vapb`

### Direct VAPB-contact and lipid-transfer analogs

VAPB is an ER membrane adaptor that binds FFAT-motif lipid-transfer proteins and helps organize ER-organelle contact sites. The closest represented pieces of that biology were weak in this assay:

| training target | 151 `n_degs` | expression-pattern evidence | interpretation for `Vapb` |
|---|---:|---|---|
| `Osbpl2` | 0 | no FDR<0.05 genes | The only OSBP-family perturbation in training did not produce an acute 151 transcriptome. |
| `Cert1` | 0 | no FDR<0.05 genes | A VAP/FFAT ceramide-transfer client branch was transcriptionally silent. |
| `Acbd5` | 0 | no FDR<0.05 genes | An ER-peroxisome VAP-tether branch did not generate a focal-cell mRNA response. |
| `Vps13a`, `Vps13b`, `Vps13c` | 0 each | no FDR<0.05 genes | Large lipid-transfer / membrane-contact proteins were buffered. |

These are not perfect analogs: VAPB is an ER receptor for many clients rather than a single lipid-transfer enzyme. Still, the represented FFAT/contact-site side of the training set argues against a broad durable RNA response from disrupting one contact-site component.

### ER stress, ATF6, and ERAD comparators

External literature makes UPR/ERAD the main reason to worry that `Vapb` could be nonzero: VAPB can regulate ATF6, ALS-linked P56S VAPB blunts VAPB-mediated UPR in cell models, and VAPB can physically/functionally couple lipid homeostasis to an ATF6/BAP31/VCP/Derlin ERAD cluster.

The same-experiment controls put a tight bound on that concern:

| training target | 151 `n_degs` | expression-pattern evidence | interpretation for `Vapb` |
|---|---:|---|---|
| `Atf6` | 0 | no FDR<0.05 genes in 151 despite being represented | Removing the ATF6 sensor is not the same as imposing ER client load. This is the closest literature-linked VAPB transcription-factor branch and it was silent. |
| `Hspa5` | 5 | `Hsp90b1`, `Nfe2l1`, `Pdia4`, and `Derl3` were up; only five total hits from 47 matched perturbed nuclei | BiP loss was detectable but compact; the assay can see ER-chaperone induction, but only selected ER insults cross the FDR gate. |
| `Sec63` | 11 | up-regulated `Hspa5`, `Canx`, `Hyou1`, `Chac1`, `Thy1`, `App`, `Syt4`; down-regulated `Syne1`, `Nlgn2`, `Plekhg1` | A stronger ER translocation / BiP-cofactor stressor gave a small ER-chaperone plus ATF4-like ISR tail. This is an upper bound for a mild VAPB UPR effect, not a direct phenocopy. |
| `Manf` | 3 | `Hspa5` and `Pdia6` up, self down | A secretory ER-stress modifier gave only a 3-gene response. |
| `Vcp` | 2 | only `Rasgef1b` up and `Nsmf` down at FDR<0.05 | Even an essential ERAD/autophagy ATPase produced a tiny 151 signature. |
| `Bcap31`, `Amfr` | 1 each | the lone significant gene was the target transcript itself | Two ERAD/BAP31-neighborhood targets were essentially downstream-null. |

The Distributed Agents corpus independently summarized this boundary: `Hspa5` and `Sec63` can induce ER folding/ERAD transcripts in `151 TH Prkcd Grin2c Glut`, but `Atf6`, `Edem3`, `Lman2l`, `Mttp`, `Suco`, `Ap4s1`, `Amfr`, and `Bcap31`-neighborhood components do not create a generic HSPA5-like UPR in the acute neuronal assay. Since VAPB loss is an upstream contact/adaptor perturbation with potential VAPA redundancy, I treated `Hspa5`/`Sec63` as upper bounds rather than direct count templates.

### ER-Golgi, retromer/GARP, lysosome, and ALS counterexamples

I also checked trafficking and ALS-like stress perturbations that could have tempted a larger count:

| training target | 151 `n_degs` | expression-pattern evidence | why it is a boundary, not the chosen template |
|---|---:|---|---|
| `Sec23a`, `Sar1b`, `Tfg` | 0 each | no COPII / ER-exit target in this group passed FDR<0.05 | ER export genes show that ER localization alone was not enough. |
| `Atl3`, `Spast`, `Ddhd2` | 0 each; `Atl1` and `Reep2` were 1 each | no shared HSP/ER-shaping downstream program | Hereditary-spastic-paraplegia/contact-adjacent biology was mostly flat in this acute nuclear-RNA endpoint. |
| `Vps35` | 17 | a thalamic synaptic/calcium state with `Atp2a2` and `Grin2b` down; not a UPR or lysosomal induction program | Shows that selected membrane traffic hits are visible, but its retromer-cargo state is not a VAPB ER-contact state. |
| `Vps54` | 31 | `Egr1` down, `Jun` up, many neuronal peptide/axon genes down; absent UPR/lysosomal/sphingolipid modules in the corpus | A GARP perturbation can be visible in 151, but even this stayed narrow and non-UPR. |
| `Rab7` | 501 | large endolysosomal/sterol/autophagy program | Too broad and late-endosomal relative to VAPB. |
| `Gfpt1`, `Dhdds`, `Uba5`, `Ufc1` | 311, 116, 2,677, 572 | strong ISR / glycosylation / UFMylation outputs such as `Ddit3`, `Chac1`, `Asns`, `Sqstm1` | These perturb core ER-proteostasis inputs much more directly than VAPB. |
| `Tardbp` | 210 | strong RNA-processing and ER/lysosomal trafficking compensation centered on genes such as `Ppp6c`, `Gabpa`, `Uggt2`, `Usp15`, `Snx14`, `Snrnp70` | A disease-family counterexample: an ALS/FTD target can be large, but through nuclear RBP and spliceosome biology rather than VAP tether loss. |

The runtime profile comparison confirmed that the VAP-contact candidates with zero counts did not have FDR-scale overlap with `Hspa5`, `Sec63`, `Vcp`, `Vps35`, or `Vps54`; the apparent whole-vector correlations among many flat perturbations were driven by thousands of non-significant genes and were not used as positive evidence.

## Prediction

I predict `Vapb` will be below the FDR<0.05 threshold in `151 TH Prkcd Grin2c Glut`, so:

- Predicted `n_degs`: **0**

The final zero/nonzero decision is mainly dataset-driven. VAPB biology nominates UPR, ERAD, lipid-contact, ER-mitochondria, and trafficking comparators, but within the same Perturb-seq experiment those neighboring perturbations are either flat or much smaller than their complete-loss literature phenotypes. The strongest positive ER-stress signatures in training come from direct ER client handling, glycosylation, UFMylation, or late-endosomal stress rather than from FFAT/contact-site adaptors. VAPB has additional redundancy with VAPA, and complete `Vapb` knockout mice have only mild late motor deficits, which further favors no durable juvenile thalamic RNA response under sparse partial CRISPR loss.

## Limits

- The exact paralog `Vapa` and the direct VAPB-PTPIP51 tether were missing from training, so the prediction extrapolates from adjacent contact-site and UPR genes rather than a direct same-complex analog.
- `n_degs` includes the self-target transcript. A self-only `Vapb` decrease could make the realized count 1 even if the downstream state is absent; target-mRNA knockdown is guide/NMD dependent and not mechanistically predictable from the training analogs.
- VAPB P56S and VAPB siRNA studies often stress motor neurons or transformed cells and involve aggregation or chronic disease contexts. Those mechanisms may not appear after P16 sparse CRISPR in surviving P37-P44 thalamic glutamatergic nuclei.
- snRNA-seq gene-level Wilcoxon DE cannot see calcium transfer, ER-mitochondria distance, lipid flux, protein aggregates, UPR sensor cleavage, Xbp1 splicing, or electrophysiology. A zero DEG count is a prediction about this RNA endpoint only.
