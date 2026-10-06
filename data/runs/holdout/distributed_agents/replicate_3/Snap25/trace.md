# Reasoning trace

## Question and resolved ambiguities

The held-out target list for this run contains one perturbation, `Snap25`.
The requested endpoint is the integer number of genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` thalamic glutamatergic
neurons after sparse postnatal CRISPR loss of function.

I interpreted `n_degs` exactly as the training count file defines it: all
measured rows passing Benjamini-Hochberg adjusted Wilcoxon FDR 0.05 in the
focal cell group, including the targeted transcript itself when its row is
significant. This matters because many synaptic-vesicle training targets in
the focal group have exactly one DEG, and that one DEG is their own target
RNA rather than a downstream response.

`Snap25` is absent from the supplied training count CSV and absent from the
training DE parquet by construction, so I did not try to recover a direct
`Snap25` signature. I instead calibrated from non-held-out perturbations of
the same release machinery and from same-experiment Distributed Agents corpus summaries.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`:
  the 1,674 training `n_degs` values in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`:
  focal-cell adjusted p-values, log2 fold changes, Wilcoxon scores, and matched
  nucleus counts for biologically analogous training perturbations.
- The selected same-experiment Distributed Agents corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, queried through the Distributed Agents
  corpus MCP. I used it as a curated interpretation layer over this same
  Perturb-seq atlas, not as independent replication.
- The Distributed Agents runtime `profile_compare` and `profile_inspect` tools, which
  compared the `151 TH Prkcd Grin2c Glut` signed log-fold-change profiles of
  27 manually selected presynaptic release and vesicle-cycle training targets.
- External mechanism literature from PubMed:
  - Sollner et al. 1993, Nature, DOI `10.1038/362318a0`, PMID `8455717`:
    purification of brain SNARE receptors including synaptobrevin/VAMP,
    syntaxin, and SNAP-25.
  - Washbourne et al. 2002, Nature Neuroscience, DOI `10.1038/nn783`,
    PMID `11753414`: genetic ablation of the t-SNARE SNAP-25 abolishes evoked
    synaptic transmission at neuromuscular junctions and central synapses.
  - Sudhof 2013, Neuron, DOI `10.1016/j.neuron.2013.10.022`,
    PMID `24183019`: review of the millisecond vesicle-release machinery built
    from SNARE/SM proteins, synaptotagmin, complexins, and active-zone factors.
  - Rizo and Xu 2015, Annual Review of Biophysics, DOI
    `10.1146/annurev-biophys-060414-034057`, PMID `26098518`: review of
    syntaxin-1, synaptobrevin/VAMP, SNAP-25, NSF/SNAP, Munc13, Munc18-1, and
    complexin function in vesicle priming and fusion.

## Computational checks over the training data

The focal training counts are extremely zero-inflated: 1,205 of 1,674
non-held-out perturbations have `n_degs = 0`, 363 are in the 1 to 9 DEG range,
63 are in the 10 to 99 range, and 43 have at least 100 DEGs. The median count
is zero and the mean is 14.05, inflated by a few very large stress or
transcriptional-regulator signatures.

I selected training perturbations by mechanism around `Snap25`: plasma-membrane
and vesicle SNAREs, Munc18/Munc13 priming factors, complexins, NSF/SNAP
disassembly factors, synapsins and vesicle proteins, active-zone proteins,
Rab3-cycle genes, and presynaptic endocytosis or maintenance genes. `Stx1a`,
`Vamp2`, and `Syt1`, the closest canonical partners of `Snap25`, were not
present as training targets; the best represented direct partners were
`Stx1b`, `Vamp1`, `Stxbp1`, `Cplx1`, `Cplx2`, `Unc13a`, `Unc13b`, and
`Unc13c`.

For those candidates I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and counted rows with
`pvals_adj < 0.05`, equivalent to:

```python
rows = parquet[
    (parquet.group_name == "151 TH Prkcd Grin2c Glut")
    & parquet.gene_target.isin(release_analogs)
]
significant = rows[rows.pvals_adj < 0.05]
```

Across 27 Snap25-relevant presynaptic analogs, 16 had no significant focal
feature at all and 11 had exactly one significant feature. Every one of those
11 significant rows was the perturbed transcript itself:

| training perturbation | focal `n_degs` | FDR-passing focal evidence |
| --- | ---: | --- |
| `Stx1b` | 0 | no significant genes; `Stx1b` self row logFC -0.390, adjusted p = 1 |
| `Vamp1` | 1 | `Vamp1` self only, logFC -0.465, adjusted p = 0.00187 |
| `Stxbp1` | 1 | `Stxbp1` self only, logFC -0.663, adjusted p = 9.38e-19 |
| `Cplx1` | 1 | `Cplx1` self only, logFC -0.863, adjusted p = 4.29e-24 |
| `Cplx2` | 0 | no significant genes; `Cplx2` self row adjusted p = 1 |
| `Unc13a`, `Unc13b`, `Unc13c` | 0, 0, 0 | no significant genes |
| `Nsf`, `Napb` | 0, 0 | no significant genes |
| `Syp` | 1 | `Syp` self only, logFC -1.776, adjusted p = 7.95e-66 |
| `Sv2a` | 1 | `Sv2a` self only, logFC -1.048, adjusted p = 1.86e-38 |
| `Syn1`, `Syn2` | 1, 0 | `Syn1` self only; `Syn2` none |
| `Syt2` | 0 | no significant genes |
| `Bsn`, `Pclo` | 0, 0 | no significant genes |
| `Dnajc5`, `Dnm1`, `Synj1` | 1, 1, 1 | self-transcript singleton only for each |
| `Rab3gap1`, `Rab3gap2`, `Rab18`, `Rab27a` | 0, 0, 0, 0 | no significant genes |
| `Snca`, `Sncb`, `Gdi1` | 0, 1, 1 | `Sncb` and `Gdi1` self-transcript singleton only |

This is stronger than a merely low DEG-count neighborhood: in the exact focal
endpoint, the core presynaptic release machinery has zero detected downstream
DEGs at FDR 0.05.

The Distributed Agents profile comparison of these same 27 targets reached the same
qualitative conclusion. It found no `>9` significant-feature profile in the
set. Among the core SNARE comparators, the focal profiles were dominated by
near-null behavior and weak low-expression tails; the highest top-tail overlaps
for `Stx1b` within the set were only 4 of 50 positive features and 6 of 50
negative features. I therefore did not read pairwise SNARE-pathway membership
as evidence for a broad shared `Snap25` nuclear state.

Finally, in the whole focal training slice, 237 of 275 targets with exactly
one DEG had a significant self-transcript row. The singletons around
presynaptic release fit that pattern exactly. That made the difference between
predicting `0` and `1` for `Snap25` mostly a question of whether the abundant
neuronal `Snap25` RNA itself would be detected as reduced, not whether a
downstream compensation module would appear.

## Same-experiment biological analogs and counterexamples

The internal Distributed Agents corpus contains no direct `Snap25` finding, as expected
for a held-out perturbation, but it has several relevant claims over training
genes.

- `claim:e1dee3db28d664657805`: broad `Stxbp1` responses are not a generic
  consequence of perturbing represented SNARE-cycle or vesicle-fusion
  components; the claim contrasts `Stxbp1` with `Stx1b`, `Vamp1`, `Cplx2`, and
  `Sv2a`.
- `claim:dca6b049615a34cf831d`: most represented acute presynaptic release and
  vesicle-cycle perturbations are buffered or transcriptionally uncoupled from
  broad compensatory steady-state neuronal mRNA programs.
- `claim:c289360a665b7efbd17d`: most represented acute vesicle-cycle, synapsin,
  complexin, calcium-sensor, and active-zone perturbations lack broad
  downstream neuronal nuclear RNA responses, whereas `Stxbp1` is the main
  visible outlier elsewhere in the atlas.
- `claim:106b08f46d3941703e3f`: represented fast presynaptic release and
  SNARE-cycle perturbations, including `Nsf` and `Napb`, do not produce a
  shared steady-state neuronal transcriptional module.

These same-corpus summaries were useful mainly as safeguards. `Stxbp1` is a
real SNARE-assembly factor and can be transcriptionally active in several
neuronal classes, so one should not collapse the whole pathway into a null
prior. However, in the requested focal group even `Stxbp1` had only its own
RNA significant, and the corpus repeatedly reports that other canonical
release components remain flat or singleton-like rather than phenocopying
`Stxbp1`.

## Target-specific prediction for Snap25

`Snap25` encodes a plasma-membrane t-SNARE that complexes with syntaxin-1 and
synaptobrevin/VAMP to drive synaptic-vesicle fusion. External literature makes
it one of the most mechanistically central genes in neurotransmitter release:
SNAP-25 was one of the original brain SNAREs purified by Sollner et al.; loss
of SNAP-25 blocks evoked synaptic transmission in the Washbourne et al. mouse
model; and reviews by Sudhof and by Rizo and Xu place SNAP-25 in the same
core SNARE/SM machinery as syntaxin, VAMP2, Munc18-1/STXBP1, Munc13, NSF/SNAPs,
complexin, and synaptotagmin.

For this assay and cell group, that centrality did not transfer into a predicted
large DEG burden. The measured training perturbations most likely to phenocopy
`Snap25` at the level of acute vesicle fusion were either zero in the focal
group (`Stx1b`, `Cplx2`, `Unc13a`, `Unc13b`, `Unc13c`, `Nsf`, `Napb`) or
self-only singletons (`Vamp1`, `Stxbp1`, `Cplx1`). Broader presynaptic vesicle
and active-zone perturbations had the same form: `Syp`, `Sv2a`, `Syn1`,
`Dnajc5`, `Dnm1`, and `Synj1` reached one DEG only through target-RNA loss,
whereas `Syt2`, `Bsn`, `Pclo`, and the represented Rab3/Rab27 cycle genes were
zero.

I therefore predict no downstream FDR-significant transcriptional response for
`Snap25` in `151 TH Prkcd Grin2c Glut`. I assign a point prediction of `1`
rather than `0` because `Snap25` is a highly neuronal, well-measured SNARE
transcript and the closest high-expression vesicle genes in training often
register exactly one DEG through self-transcript depletion. This one-count
call is not meant to imply a broad state shift; it is a self-RNA-only estimate.

## Limits of the reasoning

- `Snap25` itself, `Stx1a`, `Vamp2`, and `Syt1` were held out or absent, so the
  exact canonical ternary SNARE and calcium sensor were not all observed as
  training perturbations.
- The 0 versus 1 call hinges on `Snap25` self-transcript detection. That is
  sensitive to guide locations, nonsense-mediated decay, nuclear RNA abundance,
  the recovered perturbed-cell count, and multiple-testing calibration, and it
  is not predictable from mechanism with high confidence.
- The focal analogs rule out a broad steady-state soma/nuclear RNA response in
  this cell group, but the assay did not measure protein depletion, indel
  rates, evoked release, spontaneous release, synaptic-vesicle docking,
  terminal-localized protein trafficking, or survival before nuclei recovery.
- Severe physiological consequences of SNAP-25 loss could be buffered,
  restricted to terminals, hidden by mosaic sparse editing, or converted into
  selection of recovered cells rather than FDR-significant mRNA changes.
- The external SNAP-25 literature includes germline or complete loss models and
  electrophysiology-heavy assays. Those are mechanistically informative, but
  they are not quantitatively equivalent to P16 sparse AAV-CRISPR loss assayed
  by snRNA-seq 3 to 4 weeks later.
