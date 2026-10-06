# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out target file has one row:

- `Foxg1`

The endpoint to predict is the number of measured genes with
`pvals_adj < 0.05` after acute AAV-PHP.eB CRISPR loss of `Foxg1` in the focal
mouse `151 TH Prkcd Grin2c Glut` class. I interpreted `TH` using the supplied
dataset portrait as thalamus, not tyrosine hydroxylase, and used the supplied
training count CSV as the authoritative source for non-held-out `n_degs` in
this exact cell group.

I also treated the task as a count of significant downstream genes, not a
general biological importance score. `Foxg1` itself was completely held out, so
there is no `Foxg1` knockout profile or count in the training parquet or count
CSV.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed focal-cell DEG counts from 1,674 training perturbations.
- `[local file: training_de_all_cell_groups.parquet]`
  for signed log-fold-change profiles and adjusted Wilcoxon p-values. I read
  only `group_name == "151 TH Prkcd Grin2c Glut"` or narrower feature filters.
- Distributed Agents runtime profile comparison artifacts generated in this run:
  `foxg1_profile_compare.json` and `foxg1_profile_inspect_core.json`.
- Distributed Agents corpus MCP release
  `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Foxg1)`
  returned no claims, findings, or explicit references for this held-out target,
  so the corpus was an internal coverage check rather than positive biological
  evidence.
- PubMed-indexed external literature for `Foxg1` biology:
  - Rodriguez et al. 2001, J. Biol. Chem., DOI `10.1074/jbc.M102759200`.
  - Hanashima et al. 2007, J. Neurosci., DOI
    `10.1523/JNEUROSCI.1066-07.2007`.
  - Marcal et al. 2005, Mol. Cell. Biol., DOI
    `10.1128/MCB.25.24.10916-10929.2005`.
  - Roth et al. 2010, Development, DOI `10.1242/dev.044909`.
  - Kumamoto and Hanashima 2017, Dev. Growth Differ., DOI
    `10.1111/dgd.12367`.
  - Wong et al. 2019, Int. J. Mol. Sci., DOI `10.3390/ijms20174176`.
  - Yu et al. 2019, Mol. Brain, DOI `10.1186/s13041-019-0484-x`.

## Computations over the training data

The focal subset of the parquet contains 28,891,566 rows: 1,674 training
perturbations times 17,259 measured genes. I used parquet metadata to identify
the focal row groups, then row-filtered reads with the following logic:

```python
pq.read_table(
    training_de_all_cell_groups,
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj"],
    filters=[("group_name", "=", "151 TH Prkcd Grin2c Glut")]
)
```

Key calibration facts from the endpoint CSV:

- 1,205/1,674 training perturbations had `n_degs == 0`.
- 363 had 1 to 9 DEGs.
- 63 had 10 to 99 DEGs.
- 43 had at least 100 DEGs.
- The median count was 0, the 75th percentile was 1, and the 95th percentile
  was 18.

I then enumerated training perturbations in three classes relevant to `Foxg1`:

- Forkhead genes in the screen:
  `Foxa2`, `Foxc2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`,
  `Foxl2`, `Foxn1`, `Foxp2`, and `Foxp3` all had `0` DEGs.
- TGF-beta/BMP/Smad signaling, motivated by the reported BF-1/Foxg1
  interaction with Smad proteins:
  `Smad2` had `1` DEG; `Smad1`, `Smad3`, `Smad4`, `Smad6`, `Smad9`,
  `Tgfbr1`, `Tgfbr2`, `Tgfbr3`, `Bmpr1a`, `Bmpr1b`, and `Bmpr2` all had
  `0`.
- Forebrain/developmental transcription factors:
  `Pax6`, `Tbr1`, `Fezf1`, `Six3`, `Nfia`, `Nfib`, `Nfix`, `Nr2e1`,
  `Rarb`, `Bcl11a`, and `Bcl11b` all had `0`; `Sox2` and `Sox5` had
  `2` each; `Zbtb18` had `5`.

To make sure these zeros were not hiding a strong common signed profile, I ran
Distributed Agents runtime `profile_compare` over a 30-node panel containing the
Forkhead perturbations, Smad/TGF-beta/BMP receptors, low-response forebrain
patterning genes, and several active boundaries:
`Mecp2`, `Rora`, `Ctnnb1`, and `Ctcf`. The runtime found:

- `22/30` candidates with no significant features.
- `Foxp2`: `0` significant features in 17,259 measured genes.
- `Pax6`: `0`.
- `Smad2`: `1`.
- `Mecp2`: `16`, a modest but real postmitotic-neuron regulator.
- `Rora`: `278`, `Tcf7l2`: `106`, `Ctnnb1`: `383`, and `Ctcf`: `270`;
  these are active in this cell class but do not recapitulate a specific
  Foxg1/TGF-beta/Groucho developmental module.

The zero-DEG profiles had nearest neighbors, but their high-ranking features
were non-significant tails with adjusted p-values of 1.0 and often improbable
cell-type markers such as olfactory or immune genes. I therefore used those
full-vector similarities only as a background check and did not treat them as
positive evidence for a hidden `Foxg1` response.

Finally, I checked whether `Foxg1` was represented as a measured gene in this
cell class in other perturbation profiles. It was present in all 1,674 focal
training signatures, but its row had minimum adjusted p-value 0.632 across all
perturbations, supporting the idea that it is low and transcriptionally
immobile in the recovered thalamic nuclei. I did not use target-RNA behavior as
a guide-editing metric; this was only anatomical/context evidence.

## Target-specific prediction

### Foxg1

**External mechanism.** `Foxg1`/BF-1 is a forkhead transcriptional repressor
used repeatedly during telencephalic development, especially anterior forebrain
and ventral telencephalon patterning (Kumamoto and Hanashima 2017; Wong et al.
2019). It can antagonize TGF-beta signaling by binding Smad1/2/3/4
(Rodriguez et al. 2001) and acts with Groucho/TLE corepressors in cortical and
ventral-telencephalic contexts (Marcal et al. 2005; Roth et al. 2010). Loss of
Foxg1 in mature telencephalic neurons also impairs hippocampal plasticity and
dendritic/spine structure (Yu et al. 2019), so `Foxg1` is not merely an
embryonic progenitor gene.

**Observed analogs.** The problem is that the focal readout is a thalamic
glutamatergic class, whereas the strongest `Foxg1` programs are telencephalic.
The closest in-dataset forkhead perturbations were all silent:
`Foxp2 = 0`, `Foxj3 = 0`, `Foxk2 = 0`, `Foxa2 = 0`, `Foxc2 = 0`,
`Foxe3 = 0`, `Foxi1 = 0`, `Foxl1 = 0`, `Foxl2 = 0`, `Foxn1 = 0`, and
`Foxp3 = 0`. The TGF-beta/BMP/Smad branch was likewise silent to nearly
silent in the endpoint: `Smad2 = 1`, all other assayed Smads and the assayed
TGF-beta/BMP receptors listed above were `0`. Forebrain-patterning
counterparts that would be expected to behave if developmental identity factors
were broadly active here were also null: `Pax6 = 0`, `Tbr1 = 0`, `Fezf1 = 0`,
`Six3 = 0`, `Nfix = 0`, `Nr2e1 = 0`, `Bcl11a = 0`, and `Bcl11b = 0`.

There are active transcriptional regulators in the same cell group, notably
`Rora = 278`, `Tcf7l2 = 106`, `Ctnnb1 = 383`, and `Ctcf = 270`, so I did not
apply a blanket "all transcription factors are quiet" rule. I treated these as
boundaries: they show that the assay can detect TF/chromatin perturbations in
`151 TH Prkcd Grin2c Glut`, but they are either stronger thalamic/postmitotic
identity regulators or general chromatin/Wnt effectors rather than close
`Foxg1` substitutes. `Mecp2 = 16` gives a middle counterexample for a neuronal
transcriptional regulator with a modest acute footprint, but it still exceeds
the forkhead/Smad/developmental analogs most directly tied to `Foxg1`.

**Zero/nonzero decision and count.** The within-dataset evidence is dominated
by exact or pathway-near zeros, and the external biology points away from the
focal thalamic class rather than toward it. Because 72% of all training
perturbations are zero in this endpoint and every assayed close analog except
`Smad2` had no FDR-significant genes, I predict no genes will pass BH FDR
0.05 for held-out `Foxg1`.

Point prediction: `0`.

## Limits

- `Foxg1` itself was held out, so the prediction extrapolates from paralogs,
  pathway members, and developmental neighbors rather than from a direct
  signature.
- The Distributed Agents corpus release had no curated `Foxg1` records, so target
  biology came from external PubMed literature and prior annotation-level
  knowledge rather than from an internal same-experiment claim graph.
- Several ideal Foxg1 partners or upstream regulators, including `Tle1`,
  `Tle2`, `Tle3`, `Fezf2`, `Gli3`, and `Lhx2`, were absent from the focal
  training count table, limiting the available comparator set.
- Adult hippocampal Foxg1 deletion can be phenotypic, but that is a chronic,
  region-specific conditional knockout in telencephalic neurons, not sparse
  juvenile AAV CRISPR in recovered thalamic nuclei. Transferring a large count
  from that literature would overstate the evidence.
- A zero prediction means zero measured genes at BH FDR 0.05 in this powered
  endpoint; it does not imply that CRISPR failed, that `Foxg1` is biologically
  irrelevant, or that very weak subthreshold changes are absent.
