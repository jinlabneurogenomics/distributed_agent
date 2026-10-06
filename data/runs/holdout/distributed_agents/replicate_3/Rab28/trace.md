# Rab28 DEG-count prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested held-out perturbation list contains a single target, `Rab28`. I
interpreted the endpoint as the integer number of measured genes in the focal
`151 TH Prkcd Grin2c Glut` class whose Wilcoxon Benjamini-Hochberg adjusted
p-value is below 0.05 after acute AAV CRISPR loss of the target. The endpoint is
assay-specific and includes any self-target transcript if it passes FDR; in the
training file, for example, the sole `Ttc8`, `Arl3`, `Dnm1`, and `Gdi1` hits in
this cell group were the target mRNAs themselves.

The `TH` in the cell label was treated as the atlas thalamus abbreviation, not
as tyrosine hydroxylase. No held-out `Rab28` differential-expression rows or
training counts were available; the Distributed Agents same-experiment corpus likewise
had no direct `Rab28` Finding or Claim in release
`perturbai-july-260713-sourceguard-1773-v1`.

## Sources

- Input focal-count CSV:
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Input differential-expression parquet:
  `training_de_all_cell_groups.parquet`.
- Requested-target manifest:
  `193_Rab28.csv`.
- Distributed Agents same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`, queried for Rab-family,
  endolysosomal, BBSome, IFT, and transition-zone Findings and Claims.
- NCBI PubMed searches for `RAB28` biology, cone-rod dystrophy, ciliary
  BBSome/IFT localization, and mouse/zebrafish Rab28 photoreceptor models.

Important external references used for the biological prior:

- Brauers et al. 1996, DOI `10.1111/j.1432-1033.1996.0833p.x`, PMID
  8647132: identified mammalian `Rab28` as a distant Rab-family GTPase with
  alternatively spliced C-termini.
- Lee et al. 2008, DOI `10.1016/j.febslet.2008.11.008`, PMID 19026641:
  showed that RAB28 is structurally a distant Rab with unusual
  nucleotide-dependent conformational behavior.
- Roosing et al. 2013, DOI `10.1016/j.ajhg.2013.05.005`, PMID 23746546:
  identified homozygous human `RAB28` loss-of-function mutations in
  autosomal-recessive cone-rod dystrophy and localized RAB28 to the basal body
  and ciliary rootlet of photoreceptors.
- Jensen et al. 2016, DOI `10.1371/journal.pgen.1006469`, PMID 27930654:
  found C. elegans RAB-28 to be an IFT-associated ciliary cargo whose active
  targeting is BBSome dependent.
- Ying et al. 2018, DOI `10.1074/jbc.RA118.005484`, PMID 30228185:
  showed that mouse Rab28 loss impairs cone outer-segment shedding and
  phagocytosis, with progressive retinal degeneration.
- Carter et al. 2020, DOI `10.3389/fcell.2020.00136`, PMID 32258030, and
  Moran et al. 2022, DOI `10.1096/fj.202101897R`, PMID 35471581: in zebrafish,
  linked rab28 loss to cone outer-segment shedding and visual-cycle defects;
  cone-restricted wild-type Rab28 restored the shedding phenotype.
- Akella et al. 2020, DOI `10.7554/eLife.50580`, PMID 32101165: placed ciliary
  Rab28 and the BBSome in negative regulation of ciliary extracellular-vesicle
  shedding in C. elegans sensory neurons.

## Dataset calculations

I read the requested manifest and verified that only `Rab28` was requested. I
then summarized the 1,674 non-held-out focal counts. This assay is zero-heavy in
`151 TH Prkcd Grin2c Glut`: min 0, median 0, 75th percentile 1, 90th percentile
2, 95th percentile 18, 99th percentile about 436, and max 2677. Thus a target
with no close positive same-pathway evidence should usually be predicted at 0
or at most a singleton self-transcript count.

For focal expression evidence I filtered the parquet to
`group_name == "151 TH Prkcd Grin2c Glut"` and to mechanistically relevant
training targets:

```python
dset = pyarrow.dataset.dataset(training_de_all_cell_groups.parquet)
flt = (
    pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
) & pc.field("gene_target").isin(selected_comparators)
rows = dset.to_table(filter=flt)
```

This recovered 17,259 measured genes for each selected perturbation and allowed
me to separate real downstream signatures from self-only FDR hits.

I also ran `profile_neighbors` on observed comparator profiles in the same focal
context using signed `logfoldchanges`, with `pvals_adj < 0.05` supplied as the
significance column. The useful result was mostly negative: null ciliary and
Rab-cycle anchors such as `Rab18`, `Bbs5`, `Cep290`, `Ift81`, and `Ift88`
had full signed profiles but zero significant features; their nearest
whole-profile neighbors had very small top-tail overlaps, consistent with
background weak-rank similarity rather than a coherent module. This did not
nominate a hidden `Rab28`-like responder.

## Within-dataset analogs for Rab28

### Ciliary BBSome, IFT, and transition-zone comparators

Rab28's most specific mammalian biology is photoreceptor/ciliary rather than
late endosomal lysosomal trafficking. The most relevant represented ciliary
comparators in the focal count table were almost all exactly null:

| Perturbation | `n_degs` in 151 | Focal expression evidence |
| --- | ---: | --- |
| `Bbs5` | 0 | no FDR 0.05 genes |
| `Ttc8` / BBS8 | 1 | only `Ttc8` itself, log2FC -0.663 |
| `Ift43` | 0 | no FDR 0.05 genes |
| `Ift81` | 0 | no FDR 0.05 genes |
| `Ift88` | 0 | no FDR 0.05 genes |
| `Kif3b` | 0 | no FDR 0.05 genes |
| `Dync2h1` | 0 | no FDR 0.05 genes |
| `Dync2i1` | 0 | no FDR 0.05 genes |
| `Cep290` | 0 | no FDR 0.05 genes |
| `Rpgr` | 0 | no FDR 0.05 genes |
| `Rpgrip1l` | 0 | no FDR 0.05 genes |
| `Ttc21b` | 0 | no FDR 0.05 genes |
| `B9d1` | 0 | no FDR 0.05 genes |
| `Cspp1` | 0 | no FDR 0.05 genes |
| `Iqcb1` | 0 | no FDR 0.05 genes |
| `Alms1` | 0 | no FDR 0.05 genes |
| `Cfap69` | 0 | no FDR 0.05 genes |
| `Arl3` | 1 | only `Arl3` itself, log2FC -0.418 |

The Distributed Agents ciliary claim matched this exact pattern: acute perturbation of
represented ciliary trafficking and ciliary signaling genes in postnatal NeuN+
neurons was interpreted as largely buffered at the basal nuclear RNA level
rather than producing a shared ciliary transcriptional module. Individual
corpus Findings for `Ttc8`, `Cep290`, and `Ift88` further emphasized that
BBSome, IFT, dynein-2, transition-zone, GPCR-cargo, Hedgehog/Gli, and related
ciliary perturbations produced zero or singleton downstream signatures under
this assay, even though protein localization or ciliary morphology phenotypes
could still be present off-readout.

These are the strongest Rab28 analogs because Jensen 2016 and Akella 2020
connect RAB-28 to the BBSome and IFT at cilia, while Roosing 2013 and Ying
2018 connect mammalian RAB28 to the photoreceptor connecting cilium/outer
segment system. Their collective focal behavior argues for `0`, not for a
large hidden stress program.

### Rab-family and Rab-cycle comparators

The training data included several Rab-related perturbations:

| Perturbation | `n_degs` in 151 | Relevance to Rab28 |
| --- | ---: | --- |
| `Rab18` | 0 | a Rab controlled by the Rab3GAP complex; no focal FDR genes |
| `Rab27a` | 0 | exocytic/lysosome-related Rab; no focal FDR genes |
| `Rab3gap1` | 0 | Rab3/Rab18 GAP subunit; no focal FDR genes |
| `Rab3gap2` | 0 | Rab3/Rab18 GAP subunit; no focal FDR genes |
| `Gdi1` | 1 | a Rab GDP-dissociation inhibitor; only `Gdi1` itself passed |
| `Rab7` | 501 | strong late-endosomal/lysosomal response; poor mechanistic analog |

The same-experiment corpus summarized the Rab18/Rab27/Rab3GAP/GDI1 surface as
flat, sparse, or non-overlapping rather than a shared postnatal neuronal
nuclear RNA state. That is important because it blocks the tempting but too
coarse heuristic that a held-out Rab small GTPase should inherit the `Rab7`
count. `Rab7` was a genuine positive counterexample, but its passing genes
included lysosomal, V-ATPase, sterol, ISR/autophagy, and synaptic-remodeling
features such as `Atp6v1b2`, `Dpp7`, `Atp6v0b`, `Lamp2`, `Insig1`, `Msmo1`,
`Ddit3`, and `Grin2b`. Distributed Agents `Rab7` Findings describe this as a selective
late-endosomal/lysosomal compensation program in subcortical and midbrain
responders, weakly shared by `Vps41` and not reproduced by nearby
endolysosomal or Rab-related perturbations. Rab28 does not sit on that Rab7
late-endosomal branch.

### Broader vesicle and retromer counterexamples

Other vesicle/retromer genes show that the assay can detect trafficking stress,
but only in branch-specific cases:

| Perturbation | `n_degs` in 151 | Pattern |
| --- | ---: | --- |
| `Vps35` | 17 | modest retromer signature; `Atp2a2`, `Brsk1`, `Grin2b`, `Vps35`, and a few synaptic/neurite genes |
| `Vps54` | 31 | GARP perturbation with a different 151 TH signature headed by `Egr1`, `Kctd16`, `Jun`, `Stmn4` |
| `Cltc` | 3 | very small down-signature, with only 32 matched perturbed nuclei |
| `Dnm1` | 1 | only `Dnm1` itself passed |

`Vps35` is useful because it lies closer to Rab7/endosomal retrieval than to
Rab28 ciliary transport. It reached 17 genes, yet it lacked the broad Rab7
lysosomal/autophagy program. The corpus `Vps35` Findings explicitly separate
canonical-retromer responses from Retriever/WASH, Parkinson, lysosomal, and
mitochondrial expectations in this young postnatal neuronal assay. That makes
a large Rab7-like or even Vps35-like count for Rab28 unlikely without
target-specific evidence.

## Rab28 prediction

`Rab28` is a real ciliary Rab with retinal disease genetics, not an inert gene:
human recessive variants cause cone-rod dystrophy, RAB28 localizes at
photoreceptor ciliary structures, and mouse/zebrafish loss impairs cone
outer-segment shedding and phagocytosis. Those phenotypes, however, are tied to
photoreceptors/RPE and ciliary membrane trafficking. The Perturb-seq assay used
postnatal NeuN+ brain nuclei, removed olfactory bulb and hindbrain, and did not
sample retina, RPE, olfactory sensory epithelium, kidney, ependyma, or
embryonic patterning states where ciliary defects are most obvious.

The closest within-dataset ciliary analogs in the exact focal group were
`Bbs5`, `Ttc8`, `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Dync2h1`, `Dync2i1`,
`Cep290`, `Rpgr`, `Rpgrip1l`, `Ttc21b`, `B9d1`, `Cspp1`, `Iqcb1`, `Alms1`,
and `Cfap69`; all had `0` except `Ttc8`, whose singleton was the self mRNA.
The generic Rab analogs `Rab18`, `Rab27a`, `Rab3gap1`, and `Rab3gap2` were also
all `0` in this focal readout, while `Gdi1` was self-only. A positive count for
`Rab28` would therefore require an extrapolated basal thalamic nuclear RNA
effect that is absent from both the BBSome/IFT/transition-zone training set and
the Rab-cycle training set.

I therefore predict a true endpoint count of:

| target | predicted `n_degs` |
| --- | ---: |
| `Rab28` | 0 |

## Limits of the prediction

This is still an extrapolation. `Rab28` itself was completely held out, and the
screen did not include several canonical BBSome subunits such as `Bbs1`,
`Bbs2`, `Bbs4`, `Bbs7`, `Bbs9`, or `Bbip1`; `Bbs5` and `Ttc8` are the available
BBSome proxies. The assay measures steady basal nuclear RNA after a partial,
mosaic postnatal perturbation; it would miss cilium length changes, ciliary GPCR
mislocalization, extracellular-vesicle shedding, outer-segment phagocytosis, and
evoked Hedgehog or sensory signaling unless those subcellular phenotypes become
a stable nuclear transcriptome. The endpoint also includes self-transcript
loss, and without direct held-out data there is some chance that `Rab28` itself
would be detected as a singleton. Given that the closest pathway genes in the
focal group are zero-heavy and that many ciliary disease mechanisms are
off-tissue or off-modality here, `0` is the most calibrated point estimate.
