# DEG-count prediction trace

## Question and resolved ambiguities

The held-out manifest contains one requested target, `Tef`. I interpreted the
task as predicting, for acute AAV-CRISPR loss of `Tef`, the number of measured
genes with `pvals_adj < 0.05` in the held-out focal contrast
`151 TH Prkcd Grin2c Glut`. The input count endpoint includes the target
transcript when it happens to pass FDR, so I did not remove self rows from
training counts. I treated weak measured self-knockdown as QC context only,
consistent with the dataset portrait, because indel loss can be functionally
effective without nuclear RNA depletion.

`Tef`, `Dbp`, `Hlf`, `Nfil3`, `Npas2`, the `Per` genes, and several other clean
D-box/circadian-output comparators were absent from the training endpoint in
this holdout split. I therefore used the represented upstream or accessory
clock perturbations as analogs and counterexamples, not as direct paralog
measurements.

## Sources used

Internal same-experiment sources:

- `[local file: training_de_all_cell_groups.parquet]`
  for signed per-gene Wilcoxon statistics, log2 fold changes, and adjusted
  p-values in the focal group.
- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for observed focal-group `n_degs` on the 1,674 non-held-out training
  perturbations.
- `[local file: 235_Tef.csv]`
  for the requested target list.
- The Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`, for curated same-experiment
  statements about represented clock, ROR, and REV-ERB perturbations.
- The Distributed Agents runtime `profile_neighbors` tool, run locally over the focal
  rows of the training parquet and all 1,674 eligible training profiles.

External biology:

- Gachon et al. 2004, DOI `10.1101/gad.301404`, PMID `15175240`, showing that
  DBP, TEF, and HLF are the mammalian PAR bZIP family and that the strong brain
  epilepsy phenotype emerges in combined PAR bZIP deficiency with `Pdxk` as a
  shared target.
- Gachon et al. 2006, DOI `10.1016/j.cmet.2006.04.015`, PMID `16814730`,
  showing broad DBP/TEF/HLF control of peripheral detoxification genes in
  triple knockout mice.
- Ripperger and Schibler 2006, DOI `10.1038/ng1738`, PMID `16474407`, showing
  rhythmic BMAL1:CLOCK binding and chromatin remodeling at the mouse `Dbp`
  locus.
- Cavadini et al. 2007, DOI `10.1073/pnas.0701466104`, PMID `17646651`,
  showing cytokine suppression of the clock-controlled `Dbp`, `Tef`, and `Hlf`
  PAR bZIP genes through interference with E-box-mediated CLOCK/BMAL1
  transcription.
- Dardente et al. 2010, DOI `10.1016/j.cub.2010.10.048`, PMID `21129971`,
  showing that TEF can act through a conserved D element in the mammalian
  photoperiodic `TSHB` pathway.

## Computation over the training data

I first loaded the training-count CSV and used it to calibrate the endpoint. In
this focal cell class the distribution is zero-heavy: 1,205 of 1,674 training
perturbations had zero DEGs, the median was 0, the 75th percentile was 1, and
only 43 perturbations had at least 100 DEGs.

I then filtered the parquet to the focal cell type and a hand-built set of
clock/ROR candidate comparators. The non-obvious part of the read was simple
predicate pushdown by cell type and target:

```python
dataset.to_table(
    columns=["names", "gene_target", "logfoldchanges", "pvals_adj"],
    filter=(
        ds.field("group_name") == "151 TH Prkcd Grin2c Glut"
    ) & ds.field("gene_target").isin(candidate_targets),
)
```

Finally, I ran `profile_neighbors` with `scores` as a signed vector over the
17,259 measured genes in `151 TH Prkcd Grin2c Glut`, `pvals_adj` as the
significance column, and every training target in the count CSV as the eligible
universe. The resulting focal profile-neighborhood artifact was
`clock_profile_neighbors.json`.

## Biologically relevant training comparators for Tef

`Tef` is a PAR bZIP D-box activator and a clock-controlled output gene rather
than a core E-box factor. DBP, TEF, and HLF have overlapping DNA-binding and
output functions, and the strongest knockout phenotypes in the mouse literature
come from combined PAR bZIP loss. That makes a single acute `Tef` knockout a
good candidate for a buffered, narrow RNA response in postmitotic neurons.

Direct PAR bZIP and D-box repressor comparators were not observed in this
split: `Dbp`, `Hlf`, and `Nfil3` were all held out or absent from the focal
training endpoint. The usable within-dataset clock/ROR comparators were:

| comparator | focal `n_degs` | observed focal expression evidence | interpretation for `Tef` |
| --- | ---: | --- | --- |
| `Bmal1` | 103 | Top hits were canonical positive-limb outputs, including `Dbp` logFC -1.60, `Nr1d2` -1.08, and `Nr1d1` -1.07, plus thalamic effector genes. | Strong upstream E-box activator; proves this cell class can report clock-output RNA changes, but loss of a core activator is broader than loss of the downstream TEF D-box effector. |
| `Clock` | 3 | Only `Dbp`, `Nr1d2`, and `Tef` passed FDR 0.05; `Tef` itself was down, logFC -0.52, adjusted p = 5.35e-4. | Best training evidence that TEF sits in an active CLOCK/BMAL1-driven mini-module here; the module's observed breadth after `Clock` loss was still only 3 DEGs. |
| `Cry1` | 1 | The curated corpus summarized this as a Per2-selective focal response, not a broad TTFL reset. | A negative-limb paralog with near-complete buffering; supports a low single-gene perturbation prior for clock nodes outside `Bmal1`/`Nr1d1`/`Rora`. |
| `Cry2` | 3 | `Nr1d1`, `Cry2`, and `Dbp` were significant; `Dbp` moved in the same direction as after `Clock`/`Bmal1`, rather than as a simple inverse. | Shows that even an active clock repressor produced only a tiny focal count and that signs at one harvest time are phase- and feedback-shaped. |
| `Nr1d1` | 116 | Broad 151 TH response with de-repression of `Npas2`, `Cry2`, `Dbp`, `Nfil3`, and `Ciart`, plus synaptic and extracellular genes. | Confirms the focal class is clock-network competent, but this REV-ERB alpha response is a broad nuclear-receptor state, not a PAR bZIP phenocopy. |
| `Nr1d2` | 1 | Single-REV-ERB beta loss was narrow even though `Nr1d1` was the top focal gene. | A close functional paralog can be almost completely buffered, arguing against assigning `Tef` the broader `Nr1d1` count by family logic. |
| `Rora` | 278 | Large down-dominant thalamic program; Distributed Agents curated it as RORA-selective and not reproduced by `Rorb` or `Rorc`. | A strong counterexample: some accessory clock receptors are potent in this cell group, but the broad RORA program is a maintained thalamic identity/synapse program rather than a generic clock-output footprint. |
| `Rorb` | 0 | No focal FDR genes. | ROR family membership is not enough to produce a response. |
| `Rorc` | 0 | No focal FDR genes. | Same boundary as `Rorb`; receptor-family or circadian annotation alone overpredicts. |
| `Bmal2` | 0 | No focal FDR genes despite bHLH-PAS homology to `Bmal1`. | Another same-pathway boundary showing that expected paralogy does not guarantee measured acute neuronal output. |

The Distributed Agents corpus makes the same separation qualitatively. It reports that
`Clock` and `Bmal1` converge on a small positive-limb clock-output axis, that
`Cry1`/`Cry2` are narrow or buffered, that represented ROR and REV-ERB genes
are not transcriptionally interchangeable, and that `Rorb`/`Rorc` failed to
phenocopy `Rora` in this thalamic cell class.

The focal profile-neighborhood calculation did not find a non-clock proxy that
looked more relevant. Whole-profile Pearson neighbors were `Bmal1` ->
`Nr1d1` 0.347 and `Clock` 0.201; `Clock` -> `Bmal1` 0.201, `Nr1d1` 0.113, and
`Cry2` only 0.064; `Cry2` -> `Bmal1` 0.114 and `Clock` 0.064. `Rora` was
nearest to non-circadian thalamic programs, while the zero-DEG `Rorb`, `Bmal2`,
and `Rorc` anchors had only near-zero correlations to arbitrary genes.

## Tef prediction

I predict that `Tef` will have no genes below BH FDR 0.05 in
`151 TH Prkcd Grin2c Glut`.

The positive evidence for a nonzero effect is that `Tef` is detectably
regulated by `Clock` in the focal training data and external work places TEF
with DBP and HLF as a D-box output transcription factor. The within-dataset
evidence, however, bounds that output branch as very small: `Clock` and `Cry2`
each produced only 3 focal DEGs, `Cry1` and `Nr1d2` each produced 1, and
`Bmal2`, `Rorb`, and `Rorc` produced 0 despite clock-related annotations. The
larger `Bmal1`, `Nr1d1`, and `Rora` signatures came from upstream or accessory
nuclear receptor perturbations with broader thalamic identity, synaptic,
extracellular, and feedback effects that should not be transferred to a single
PAR bZIP output factor. Given the redundancy among DBP, HLF, TEF, and the
opposing NFIL3/E4BP4 D-box repressor, single-gene acute `Tef` loss is more
likely to fall on the 0 side of the focal FDR threshold than to produce a
stable multi-gene state.

Final point prediction: `Tef = 0`.

## Limits and extrapolations

The strongest limitation is the missing direct paralog data: `Dbp`, `Hlf`, and
`Nfil3` were not available as training endpoints here, so the PAR bZIP
prediction is extrapolated from upstream and accessory clock nodes. The assay is
a single terminal snRNA-seq time point, so it can miss phase, period, amplitude,
translation, and electrophysiological effects even if TEF protein loss is real.
The focal group is a broad thalamic glutamatergic class rather than a named
nucleus, and the experiment measures recovered neuronal nuclei only.

The expected count is therefore a statement about the BH FDR 0.05 RNA endpoint
under sparse P16 AAV-CRISPR in recovered `151 TH Prkcd Grin2c Glut` nuclei, not
about TEF dispensability, editing success, seizure susceptibility, circadian
physiology, or other D-box outputs in unsampled tissues.
