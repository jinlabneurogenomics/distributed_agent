# Slc17a5 held-out DEG-count prediction

## Question and resolved ambiguities

The requested endpoint is the number of genes with Benjamini-Hochberg adjusted
Wilcoxon `pvals_adj < 0.05` after loss of each held-out target in
`151 TH Prkcd Grin2c Glut` neurons. The manifest for this run contains one
target, `Slc17a5`. I therefore made one point prediction for the acute
postnatal mosaic CRISPR-Cas9 perturbation, not for a germline knockout, chronic
human disease state, drug inhibition, or the biological importance of the gene.

The DEG count includes the self transcript if it crosses FDR. I did not treat a
measured self-transcript decrease as proof of editing efficiency, and I treated
single self-only DEG calls in training as evidence for a near-null downstream
signature rather than as broad pathway activation.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`:
  exact observed `n_degs` for the 1,674 non-held-out training perturbations in
  the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`:
  focal-cell log fold changes, Wilcoxon scores, adjusted p-values, and matched
  nucleus counts for mechanistic analogs.
- Distributed Agents same-experiment semantic corpus
  `perturbai-july-260713-sourceguard-1773-v1`: target reports and higher-order
  Claims for represented lysosomal, V-ATPase, autophagy, HOPS/Rab7, and
  endosomal perturbations.
- PubMed literature for `SLC17A5`/sialin biology:
  Verheijen et al. 1999, Nature Genetics, DOI `10.1038/70585`, PMID
  `10581036`; Aula et al. 2000, American Journal of Human Genetics, DOI
  `10.1086/303077`, PMID `10947946`; Wreden et al. 2004, Journal of Biological
  Chemistry, DOI `10.1074/jbc.M411295200`, PMID `15516337`; Miyaji et al. 2008,
  PNAS, DOI `10.1073/pnas.0804015105`, PMID `18695252`; Huizing et al. 2021,
  Neuroscience Letters, DOI `10.1016/j.neulet.2021.135896`, PMID `33862140`.

## Computational checks

I first read the requested manifest and the training-count CSV. The manifest
contained only `Slc17a5`, and the training endpoint distribution was strongly
zero-inflated: 469 of 1,674 targets were nonzero, the median count was 0, the
75th percentile was 1, and the mean was pulled upward to 14.1 by a few very
broad perturbations such as `Uba5`, `Tpr`, `Sin3a`, and spliceosome/proteasome
targets.

For candidate analogs, I filtered the parquet to the focal group and a manually
chosen set of mechanistically relevant training targets:

```python
filter = (
    (ds.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & ds.field("gene_target").isin(candidates)
)
```

This returned 690,360 measured-gene rows for 40 candidate perturbations. I
recomputed `(pvals_adj < 0.05).sum()` per target and confirmed that it matched
the training-count CSV exactly. I also inspected the FDR-significant genes and
the largest absolute Wilcoxon-score coordinates for the sparse analogs, and
computed Pearson correlations over the focal signed-score vectors for selected
lysosomal/endosomal candidates to avoid reading arbitrary nearest neighbors out
of a flat signature.

Finally, I checked whether any `Slc17` paralog was present as a perturbation in
the training set. None was present, so there was no direct vesicular-glutamate
transporter paralog measurement to use.

## Biological interpretation of Slc17a5

`Slc17a5` encodes sialin, the lysosomal free-sialic-acid exporter mutated in
Salla disease and infantile free sialic acid storage disease. Human genetics
established `SLC17A5` as the causative gene for lysosomal free sialic acid
storage disorders, and recombinant sialin was subsequently shown to mediate
lysosomal sialic-acid transport with disease alleles reducing or eliminating
activity (Verheijen et al. 1999; Aula et al. 2000; Wreden et al. 2004). FSASD
is clearly neurological, with progressive neurodegeneration and hypomyelination
in patients (Huizing et al. 2021), so the gene cannot be dismissed as irrelevant
to brain cells.

The acute assay asks a narrower question: whether partial, mosaic P16
loss-of-function in surviving juvenile neurons produces enough nuclear RNA
remodeling within 3-4 weeks for any measured gene to pass FDR 0.05. Sialin is a
transmembrane transporter rather than a master trafficking GTPase, transcription
factor, spliceosome component, or proteostasis hub. Although sialin was reported
to transport aspartate/glutamate in synaptic vesicle preparations (Miyaji et al.
2008), that activity did not have a direct `Slc17a6`/`Slc17a7`/`Slc17a8`
training paralog in this dataset, so I treated it as a plausible neuron-specific
function but not as evidence for a broad transcriptional response.

## Training perturbations compared with Slc17a5

**Lysosomal storage and lysosomal cargo genes.** The closest available class was
not sialic-acid export itself but other lysosomal disease/cargo perturbations.
In the focal count CSV:

- `Gnptab` and `Gnptg`, M6P tag-synthesis components, had 0 and 0 DEGs.
- `Manba` and `Asah1`, lysosomal hydrolase/storage genes, had 0 and 0 DEGs.
- `Sort1`, involved in lysosomal enzyme trafficking, had 0 DEGs.
- `Ctsb`, `Gaa`, `Ppt1`, `Psap`, and `Tmem106b` each had 1 DEG.

The expression evidence argues that the `1` calls above were target-RNA or
isolated calls, not a weak shared stress module. In the focal parquet,
`Ctsb`, `Gaa`, `Ppt1`, `Psap`, and `Tmem106b` each called its own transcript as
the only FDR<0.05 gene; the next-largest non-self coordinates had adjusted
p-values near 1. `Gnptab` and `Manba` had no FDR<0.05 gene at all. Pairwise
focal score correlations among `Gnptab`, `Gnptg`, `Manba`, `Ppt1`, `Psap`, and
`Gaa` stayed close to zero, from about -0.07 to +0.08 in the subset I checked.
Distributed Agents Claim `claim:2ea06b0f0f62f2fef4d7` states the same result over the
same experiment: represented lysosomal hydrolase and M6P-pathway perturbations
were largely buffered at the acute neuronal mRNA level rather than converging on
a broad storage-stress module. Claim `claim:56e1e77cd2cb9bb6604f` extends this
to a disease-associated lysosomal/NCL/hydrolase/cargo panel and notes the
absence of a shared lysosomal-stress, TFEB/MiT, autophagy, ISR, or UPR nuclear
RNA program.

This was the strongest within-dataset lane for `Slc17a5`. The comparison is
imperfect because soluble hydrolases can be cross-corrected in mosaic tissue,
whereas sialin is a cell-autonomous membrane exporter. Still, the repeated
absence of storage-stress RNA after direct lysosomal disease gene perturbation
makes a large `Slc17a5` transcriptional footprint unlikely.

**Endosomal pH and V-ATPase genes.** A second lane asked whether disturbing
lysosomal acidification or endosomal ion homeostasis was enough to create a
focal thalamic response. It generally was not:

- `Atp6ap2` had 2 DEGs, only `Atp6ap2` and `Atp6v0a1`.
- `Atp6v0a1`, `Clcn4`, and `Slc9a7` each had 1 DEG, the self transcript.
- `Atp6v1a`, `Atp6v1b2`, `Atp6v1e1`, `Clcn3`, and `Slc9a9` had 0 DEGs.

Distributed Agents Claim `claim:d08f04d8507bae4de40b` reports that same V-ATPase pump
membership was insufficient to generate a common postnatal neuronal snRNA
module, and Claim `claim:2aa16e813622a843c706` similarly separates shared
endomembrane acidification annotations from actual convergence in this assay.
Because `Slc17a5` is an ion-coupled lysosomal carrier rather than an acidification
core subunit, these mostly self-only or zero V-ATPase/CLC/NHE results pulled the
prediction downward.

**Rab7/HOPS/retromer/GARP/endolysosomal trafficking.** This lane provided
positive counterexamples showing that the assay could detect lysosomal or
trafficking stress when the edited target sat at the right network point:

- `Rab7` had 501 DEGs in the focal group. Its leading calls included increased
  `Atp6v1b2`, `Dpp7`, `Scpep1`, `Insig1`, and `Atp6v0b`, matching a
  late-endosomal/lysosomal and sterol compensation state.
- `Vps35` had 17 DEGs.
- `Vps54` had 31 DEGs.
- By contrast, `Vps41`, `Vps35l`, `Vps53`, `Washc4`, `Ocrl`, `Abca7`, and
  `Lrmda` had 0 DEGs, while `Gdi1` had only its self transcript.

Distributed Agents Claim `claim:726468d7afc216bc3be2` marks `Rab7` as a selective
neuronal late-endosomal/lysosomal compensation program, weakly shared by `Vps41`
but absent after `Ocrl`, `Abca7`, or `Gdi1`. That makes `Rab7` a boundary rather
than a close quantitative analog: it shows that a lysosomal rebound could have
been observed in `151 TH Prkcd Grin2c Glut`, but the same-experiment HOPS,
retromer, WASH, and phosphoinositide comparators show that the rebound did not
propagate to every endolysosomal target.

**Autophagy genes.** Core autophagy perturbations were also near zero in the
focal group: `Atg16l1`, `Atg5`, and `Becn1` had 0 DEGs and `Rb1cc1` had 4. The
4 `Rb1cc1` genes were `Calr`, `Hspa5`, `Rb1cc1`, and `Pdia6`, an ER chaperone
signature rather than a broad lysosomal CLEAR program. Distributed Agents Claim
`claim:f6d22ea9448373eb8a02` states that represented core autophagy genes did
not elicit pan-neuronal transcriptional responses in this assay. This makes a
secondary autophagy/stress response after `Slc17a5` loss less likely.

**Aspartate/glutamate and neurotransmitter-carrier analogs.** Because sialin has
been reported to support vesicular aspartate/glutamate transport, I also checked
metabolite and carrier perturbations in training rather than using only
lysosomal genes. There were no `Slc17` vesicular glutamate transporter targets.
The malate-aspartate shuttle genes had only weak focal signatures: `Got1` 1,
`Got2` 1, `Mdh2` 1, `Slc25a12` 1, `Slc25a13` 0, with `Mdh1` a modest exception
at 29 DEGs. Distributed Agents Claim `claim:25348ca5cd192eccd03c` places the detectable
MAS response mainly on the cytosolic `Got1`/`Mdh1` arm, not on the mitochondrial
aspartate-glutamate carriers. This gives little support for predicting a broad
focal signature from perturbing the less canonical vesicular amino-acid
transport activity of sialin.

**Slc17a5 as a measured transcript.** Across all 1,674 non-held-out focal
contrasts, the measured gene `Slc17a5` itself never crossed FDR 0.05; the
smallest adjusted p-value was 0.0577. This is only context because none of these
perturbed `Slc17a5` directly, but it shows that `Slc17a5` was not a recurrent
member of the broad stress signatures that dominate the upper tail of this
screen.

## Prediction for Slc17a5

The within-dataset evidence dominated the final decision. `Slc17a5` is a true
lysosomal neurological disease gene, but the represented acute lysosomal storage
perturbations in this same sparse P16 neuronal screen were nearly all 0 or
self-only 1 in the focal class, and the corpus reports no common lysosomal
storage-stress, TFEB/MiT, autophagy, ISR, or UPR RNA module for them. The
endosomal pH and core autophagy comparators were similarly zero or tiny. `Rab7`
proved that late-endosomal stress can be detected in these thalamic glutamatergic
neurons, but `Rab7` is a trafficking hub with a broad HOPS/lysosome/sterol
state, not a close phenocopy for one lysosomal sialic-acid exporter.

I therefore predicted no FDR-significant genes for `Slc17a5` in
`151 TH Prkcd Grin2c Glut`: `predicted_n_degs = 0`.

## Limits

This is an extrapolation because the corpus had no explicit `Slc17a5` card and
no `Slc17` paralog perturbation was in the focal training set. The best
training analogs are neighboring lysosomal disease and acidification genes, not
the same transporter or the same substrate. Soluble hydrolase genes may be more
buffered than cell-autonomous membrane exporters in mosaic tissue, so the
hydrolase/M6P nulls could understate a `Slc17a5` effect. Conversely, the disease
literature describes germline or chronic loss with strong developmental and
glial/myelination components that are under-sampled in this NeuN-positive acute
neuronal experiment, so human FSASD severity could overstate the expected
single-nucleus neuronal RNA response. The exact distinction between 0 and a
self-only 1 is cutoff-sensitive and depends on `Slc17a5` guide performance,
target-RNA abundance, and recovered-nucleus count in the hidden contrast.
