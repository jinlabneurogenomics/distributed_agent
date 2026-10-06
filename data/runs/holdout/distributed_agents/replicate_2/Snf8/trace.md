# Question and interpretation

The held-out target list contains one perturbation, `Snf8`. I interpreted the
task as asking for the integer number of genes that would pass
`pvals_adj < 0.05` after acute AAV-CRISPR loss of `Snf8` in the focal
`151 TH Prkcd Grin2c Glut` neuronal class. The endpoint is therefore the
screen-calibrated count of FDR-significant nuclear RNA changes among recovered
single nuclei, not a measure of MVB morphology, editing efficiency, cell loss,
or long-term lysosomal storage.

`Snf8` is absent from both supplied training files, and the Distributed Agents corpus
release available in this run, `perturbai-july-260713-sourceguard-1773-v1`,
also had no `Snf8` target node, Findings, or Claims. I therefore did not have a
same-experiment Snf8 signature. I used the training counts and focal-cell
profiles of related targets to calibrate the expected response breadth, and I
used literature on mammalian ESCRT-II to decide which related targets were
mechanistically close enough to matter.

# Sources used

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: exact training endpoint
  for the focal class. It contains 1,674 non-held-out perturbations; 1,205
  have `n_degs = 0`, 363 have 1-9, 63 have 10-99, and 43 have at least 100.
- `training_de_all_cell_groups.parquet`: per-gene DE rows. I read only the
  `151 TH Prkcd Grin2c Glut` row groups and a curated trafficking/autophagy
  target panel, then recomputed `(pvals_adj < 0.05).sum()`, inspected the
  lowest-FDR genes, and calculated Pearson correlations of Wilcoxon `scores`
  over the 17,259 measured genes in the focal class.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`: target contexts for `Rab7`,
  `Vps35`, `Vps54`, and `Chmp4b`; endolysosomal claim search; and induced
  topology over the hand-selected trafficking cohort. This was used as a
  structured report layer over the same experiment, not as independent
  replication.
- PubMed-indexed ESCRT literature:
  Hurley 2008, DOI `10.1016/j.ceb.2007.12.002`, PMID `18222686`;
  Im and Hurley 2008, DOI `10.1016/j.devcel.2008.04.004`, PMID `18539118`;
  Im, Wollert, Boura, and Hurley 2009, DOI
  `10.1016/j.devcel.2009.07.008`, PMID `19686684`;
  Wang and Hong 2006, DOI `10.1016/j.bbrc.2006.09.064`, PMID `17010938`;
  Malerod, Stuffers, Brech, and Stenmark 2007, DOI
  `10.1111/j.1600-0854.2007.00630.x`, PMID `17714434`.

# Computational checks

The focal-class parquet scan was deliberately restricted to biologically
relevant training targets. The operation was:

```python
for each parquet row group with group_name == "151 TH Prkcd Grin2c Glut":
    read names, scores, logfoldchanges, pvals_adj, gene_target
    keep rows whose gene_target is in an ESCRT/endolysosomal/autophagy panel
count rows with pvals_adj < 0.05 by gene_target
pivot scores by measured gene and compute profile correlations
```

Key focal counts from that scan were:

| training target | focal `n_degs` | reason for comparison |
| --- | ---: | --- |
| `Chmp4b` | 0 | only represented ESCRT core gene in the training focal table; downstream ESCRT-III paralog, not ESCRT-II itself |
| `Rab7` | 501 | late-endosome GTPase with a strong lysosomal/V-ATPase/sterol stress signature |
| `Dctn1` | 75 | retrograde organelle transport stress with sterol genes; pathway-adjacent counterexample |
| `Vps54` | 31 | GARP/endosome-to-TGN tether; focal but not lysosomal |
| `Vps35` | 17 | retromer core; focal and weak/moderate |
| `Wdfy3` | 17 | autophagy-scaffold/stress comparator, not ESCRT |
| `Cltc` | 3 | endocytic coat perturbation, weak in the focal class |
| `Sqstm1`, `Atp6v0a1`, `Gaa`, `Ppt1`, `Tmem106b`, `Stx16` | 1 each | lysosome or vesicle comparators with only one focal hit |
| `Atg5`, `Atg16l1`, `Becn1`, `Lamp2`, `Litaf`, `Spast`, `Vps13a`, `Vps13b`, `Vps13c`, `Vps35l`, `Vps41`, `Vps53`, `Washc4` | 0 | broad autophagy/endolysosomal/Golgi neighbors that were flat at FDR 0.05 |

The expression-pattern evidence matched the counts. `Rab7` was not a hidden
generic template for all endosomal genes: in 151 it induced V-ATPase,
lysosomal hydrolase, sterol, and proteostasis transcripts such as
`Atp6v1b2`, `Dpp7`, `Insig1`, `Atp6v0b`, `Msmo1`, and `Fdft1`, and it
down-regulated neuronal function genes including `Grin2b`. `Vps35` shared
9 FDR genes with `Rab7` but had only 17 total calls. `Vps54` shared 13 FDR
genes with `Rab7` but was a narrower Egr1-down/Jun-up neuronal state.
`Vps41` continuously resembled `Rab7` most among the zero-DEG controls
(`r = 0.311` on all focal Wilcoxon scores) yet had no FDR 0.05 genes.
`Vps53` had `r = 0.155` to its same-GARP-neighborhood comparator `Vps54`
but no focal FDR genes. `Chmp4b` had no 151 FDR hits, a weak top adjusted
p value of 0.174, and no overlap with the `Rab7` FDR set.

# Target-specific reasoning

## `Snf8`

`Snf8` encodes VPS22/EAP30, one of the three core ESCRT-II subunits. Human
ESCRT-II contains one VPS22, one VPS36, and two VPS25 subunits; its VPS36 GLUE
region links it to ESCRT-I, VPS22 contributes a membrane-binding helix, and
VPS25 contacts ESCRT-III/VPS20 to help form intraluminal vesicles in
multivesicular bodies (Im and Hurley 2008; Im et al. 2009). Mammalian
VPS22/SNF8 depletion disrupts ESCRT-II stability and EGFR/CXCR4 degradation in
cultured cells, and RILP can bind VPS22/VPS36 to connect Rab7-regulated late
endosome organization with ESCRT-II recruitment (Wang and Hong 2006; Malerod
et al. 2007).

That biology made a true zero possible but not automatic. `Snf8` is less
redundant than `Chmp4b`, because CHMP4 has A/B/C paralogs whereas ESCRT-II has
a single VPS22/SNF8 subunit. A large `Rab7`-like state was still unlikely:
VPS22 acts in ubiquitinated cargo sorting into MVB intraluminal vesicles,
whereas `Rab7` loss perturbs late endosome/lysosome maturation directly and
the same-experiment corpus describes `Rab7` as a broad
late-endosomal/lysosomal compensation response. The most direct measured ESCRT
readout, `Chmp4b`, was flat in the focal class and the Distributed Agents Chmp4b report
found no robust recurrent ESCRT/autophagy/cargo transcriptional signature.
Other branches that could have revealed secondary Snf8 stress were also
mostly buffered in 151: `Atg5`, `Atg16l1`, `Becn1`, `Lamp2`, `Litaf`,
`Spast`, `Vps41`, and `Vps53` had no FDR 0.05 focal genes, while `Atp6v0a1`,
`Gaa`, `Ppt1`, `Sqstm1`, and `Tmem106b` had only one.

I treated `Rab7`, `Vps35`, `Vps54`, and `Dctn1` as positive boundaries rather
than scalar templates. The Distributed Agents corpus explicitly separates the 501-gene
`Rab7` lysosomal/sterol program from the much narrower `Vps35` retromer and
`Vps54` GARP signatures, and it also records that same-complex or adjacent
membership was insufficient to yield an FDR-scale phenotype for pairs such as
`Vps54`/`Vps53`. Those examples argue that the assay can see trafficking
stress in 151 TH neurons, but that partial acute loss of one endomembrane
complex member often remains below the FDR threshold.

My Snf8 call is therefore a focal null: predicted `n_degs = 0`. The decision
is driven mainly by within-dataset evidence from the flat `Chmp4b`, `Vps41`,
`Vps53`, autophagy, and lysosome comparators, with the external ESCRT-II
literature used to keep `Rab7` and retromer/GARP positives at the correct
mechanistic distance. A very small nonzero response would not be surprising if
VPS22 destabilization uniquely impaired ESCRT-II more than `Chmp4b` impaired
ESCRT-III, but the training data do not support promoting Snf8 to a 10-100
DEG retromer/GARP-like count, much less to a Rab7-like late-lysosomal count.

# Limits

The strongest limitation is the missing exact ESCRT-II training module:
`Vps25`, `Vps36`, `Tsg101`, `Hgs`, `Stam`, `Vps28`, and `Vps4` perturbation
counts were not present in the supplied focal training CSV. `Chmp4b` is a
downstream, partially paralog-buffered ESCRT-III gene, so its zero is an
imperfect analog for `Snf8`. Conversely, `Rab7`, `Vps35`, `Vps54`, and
`Dctn1` prove that trafficking perturbations can become visible, but they act
at different steps and produced distinct signatures. The prediction also
assumes that the acute, sparse, postmitotic CRISPR setting leaves enough
residual ESCRT-II or cargo-routing bypass for VPS22 loss to stay
transcriptionally buffered; strong protein depletion, dividing progenitors, or
longer degenerative contexts could have a larger phenotype.
