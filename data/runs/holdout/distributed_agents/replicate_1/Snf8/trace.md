# DEG-count prediction trace

## Question and endpoint

The held-out target list contains one perturbation, `Snf8`. I interpreted the requested endpoint as:

`predicted_n_degs =` the integer number of measured genes expected to pass `pvals_adj < 0.05` after `Snf8` CRISPR loss of function in `151 TH Prkcd Grin2c Glut` cells.

The ambiguity I resolved was that the task asks for a point prediction, not a ranked list or a probability of any response. Zero therefore means that no measured transcript is expected to cross the BH-adjusted 0.05 threshold in this assay. The Snf8 perturbation itself is absent from both supplied inputs, so the endpoint is absent for the requested gene and has to be inferred from non-held-out genes.

## Sources used

- Declared direct endpoint: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`
- Declared differential-expression rows: `training differential-expression dataset`
- Requested targets: `single-target request for Snf8`
- Internal same-experiment semantic corpus: `perturbai-july-260713-sourceguard-1773-v1`
- External literature: NCBI PubMed E-utilities. Key ESCRT references used were Kamura et al. 2001, J. Biol. Chem., DOI `10.1074/jbc.M010142200`, PMID `11278625`; Malerod et al. 2007, Traffic, DOI `10.1111/j.1600-0854.2007.00630.x`, PMID `17714434`; and Wernimont and Weissenhorn 2004, BMC Structural Biology, DOI `10.1186/1472-6807-4-10`, PMID `15579210`.

The Parquet and the semantic corpus are two representations of the same Perturb-seq experiment. I treated the CSV/Parquet counts as the quantitative observation and the corpus as curated interpretation of same-experiment patterns, not as independent replication.

## Dataset calculations

I first counted the training response distribution for the focal cell group. It is highly sparse: among 1,674 non-held-out targets, 1,205 have `n_degs = 0`, the median is 0, the 75th percentile is 1, the 95th percentile is 18, and the maximum is 2,677. That makes zero the prior expectation unless a requested gene has a close in-dataset analog with a supported focal response.

I then pulled observed counts for ESCRT, endosomal, lysosomal, autophagy, and vesicle-traffic genes and queried the focal Parquet rows for representative analogs. For each analog I checked both the supplied `n_degs` and the smallest focal adjusted p-values so that a zero did not hide a near-threshold FDR miss. The non-obvious Parquet operation was a filtered grouped scan:

```sql
SELECT gene_target,
       SUM(CASE WHEN pvals_adj < 0.05 THEN 1 ELSE 0 END) AS degs_fdr05,
       SUM(CASE WHEN pvals_adj < 0.10 THEN 1 ELSE 0 END) AS degs_fdr10,
       MAX(n_pert_matched) AS n_pert,
       MIN(pvals_adj) AS min_padj
FROM read_parquet(training_de_all_cell_groups.parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
GROUP BY gene_target;
```

## Target-specific reasoning

### Snf8

`Snf8`, also called mammalian `Vps22/EAP30`, is a core ESCRT-II subunit. ESCRT-II contains VPS22/SNF8, VPS36/EAP45, and two VPS25/EAP20 copies; it acts after ESCRT-I and before ESCRT-III in sorting ubiquitinated endosomal cargo into multivesicular bodies. Kamura et al. connected mammalian EAP30 to yeast Snf8/Vps22, Wernimont and Weissenhorn described the VPS25-containing ESCRT-II structure, and Malerod et al. showed that Vps22/EAP30 depletion impairs EGFR and CXCR4 lysosomal degradation. This is a genuine endosomal-sorting prior, but it is not the same as perturbing the late-endosomal master GTPase `Rab7`.

The closest training comparators were:

| training perturbation | focal observed `n_degs` | focal expression evidence | how I used it |
| --- | ---: | --- | --- |
| `Chmp4b` | 0 | no FDR 0.05 or 0.10 hits in 151; the top focal row was `Ptar1`, p_adj = 0.174; the corpus reports only one corrected downstream hit for `Chmp4b` in another class and no robust ESCRT/autophagy/cargo transcriptional module | downstream ESCRT-III membrane-scission machinery; the best ESCRT pathway analog in training, and it was focal-null |
| `Vps41` | 0 | no FDR 0.05 or 0.10 hits in 151; the top focal row was `Dhcr24`, p_adj = 0.204, with weak subthreshold lysosomal rows such as `Atp6v0b`, `Gba`, and `Map1lc3b`; the corpus reports a sparse Rab7-centered HOPS response in caudal groups but not 151 | late endosome/lysosome fusion through HOPS; adjacent to the degradative compartment but downstream of ESCRT-II, so a useful boundary analog |
| `Atg5` | 0 | top focal p_adj = 0.105 and no FDR 0.10 hit | autophagosome machinery; argues against assuming every autophagy/endolysosomal gene yields a 151 TH response |
| `Becn1` | 0 | top focal p_adj = 1.0 | upstream autophagy/nucleation; another focal null |
| `Vps35` | 17 | focal hits were led by `Atp2a2` down, `Brsk1` up, and `Grin2b` down; curated interpretation called a restricted retromer/synaptic remodeling program, not a bulk lysosomal stress response | retromer retrieval branch; demonstrates that some endosomal perturbations can produce modest 151 TH signal, but through a branch not equivalent to ESCRT-II inward budding |
| `Vps54` | 31 | nonzero focal count in the training table | GARP/EARP tethering, more related to retrieval traffic than to ESCRT-II |
| `Wdfy3` | 17 | focal hits led by `Stmn4`, `Jun`, `Gpm6a`, and `Gls` | selective-autophagy scaffold; a modest-response counterexample, but not same-complex ESCRT evidence |
| `Tsc2` | 86 | focal hits led by `Nrbp2`, `Cyp51`, `Pik3r3`, and `Nefm` | lysosomal mTORC1 regulator; a signaling perturbation that can secondarily affect lysosomal state, but its TSC/mTOR sign does not transfer to `Snf8` |
| `Rab7` | 501 | focal hits led by `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`, `Dusp1`, `Insig1`, and `Atp6v0b`; curated interpretation describes a broad late-endosomal/lysosomal, sterol, ISR, and proteasome recovery program | an upper-bound counterexample: the assay can recover a large late-endosomal stress state, but Vps41 and Vps35 failed to phenocopy most of it |

The causal transfer chain I used was: `Snf8` loss should impair ESCRT-II assembly or function, which should reduce ESCRT-III recruitment for endosomal intraluminal-vesicle formation, which could alter receptor/cargo turnover and late endosome to lysosome load, which might trigger lysosomal or proteostatic adaptation in recovered 151 TH nuclei. Two points weaken transfer to a broad FDR response. First, the closest assayed ESCRT arm, `Chmp4b`/ESCRT-III, did not cross FDR in the focal cell group. Second, stronger downstream lysosomal stress is plainly detectable in this cell group when `Rab7` is perturbed, yet more specific late-endosomal, autophagy, and HOPS perturbations were null or tiny. I therefore expect partial postnatal `Snf8` editing to resemble the focal-null ESCRT/HOPS/autophagy cases more than the broad `Rab7` state.

Snf8 itself was up-regulated as a measured gene in a few unrelated large signatures, including `Mdh1` and `Tardbp` in 151 TH, and in `Brd4`/`Yy1` corpus findings it appeared as part of secondary endolysosomal adaptation after nuclear-regulator perturbation. I treated this as evidence that `Snf8` can be a stress-responsive endosomal transcript, not as evidence that knocking out `Snf8` will reproduce those upstream signatures.

Prediction for `Snf8`: `0` DEGs. This is driven mostly by within-dataset zeros for `Chmp4b`, `Vps41`, `Atg5`, and `Becn1`, with external ESCRT knowledge used only to decide that `Chmp4b` is a closer analog than the high-count but broader `Rab7` perturbation.

## Limits

- The most direct same-complex ESCRT-II partners of `Snf8`, such as `Vps25` and `Vps36`, were not present as focal training perturbations, so the prediction transfers from ESCRT-III and adjacent endolysosomal branches rather than from a same-complex loss.
- The observed Parquet rows are 3-4 week survivor-conditioned nuclear RNA contrasts. They do not measure endosomal cargo flux, ESCRT complex abundance, receptor degradation, indel burden, or early loss of edited nuclei.
- The corpus reports and Parquet came from the same screen, so agreement between them calibrates interpretation but is not independent validation.
- `Rab7` proves that 151 TH cells can mount a large endolysosomal stress signature, so a strong `Snf8` functional block could be nonzero. The point estimate is zero because the closer and more specific training analogs did not reach FDR 0.05 in this cell group.
