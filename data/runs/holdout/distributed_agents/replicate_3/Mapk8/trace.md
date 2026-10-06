# Mapk8 held-out DEG-count prediction

## Question and target list

The requested readout is the number of genes passing `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` nuclei after each completely held-out perturbation. The manifest `[local file: 130_Mapk8.csv]` contains one requested target, in this order:

```text
Mapk8
```

I therefore made one integer point prediction for the focal cell group. I treated `0` as "no measured gene is expected to pass the same BH-adjusted Wilcoxon threshold," not as "MAPK8 has no neuronal signaling role."

## Sources used

- Local endpoint table: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Local DE parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `130_Mapk8.csv`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, queried with `target_context`, `search_claims`, and `candidate_set_topology`. `target_context(Mapk8)` was absent, as expected for the held-out target; I used target contexts for observed analogs, especially `Mapk9`, `Map3k7`, `Jund`, and `Map2k1`.
- Distributed Agents runtime profile tools, used with `group_name = "151 TH Prkcd Grin2c Glut"` and `logfoldchanges` keyed by `gene_target` and measured gene `names`. I computed independent profile-neighbor views and then a symmetric comparison over observed MAPK/JNK/ERK/Rho candidates.
- PubMed literature:
  - Davis 2000, "Signal transduction by the JNK group of MAP kinases", Cell, DOI `10.1016/S0092-8674(00)00116-1`, PMID `11057897`.
  - Weston and Davis 2007, "The JNK signal transduction pathway", Current Opinion in Cell Biology, DOI `10.1016/j.ceb.2007.02.001`, PMID `17303404`.
  - Kuan et al. 1999, "The Jnk1 and Jnk2 protein kinases are required for regional specific apoptosis during early brain development", Neuron, DOI `10.1016/S0896-6273(00)80727-8`, PMID `10230788`.
  - Ham et al. 2000, "c-Jun and the transcriptional control of neuronal apoptosis", Biochemical Pharmacology, DOI `10.1016/S0006-2952(00)00372-5`, PMID `11007936`.
  - Wang, Destrument, and Tournier 2006, "Physiological roles of MKK4 and MKK7: insights from animal models", Biochimica et Biophysica Acta, DOI `10.1016/j.bbamcr.2006.10.016`, PMID `17157936`.

## Computational checks

The focal training-count distribution is highly zero-inflated:

```text
training perturbations                 1674
nonzero perturbations                   469
median n_degs                             0
75th percentile                           1
90th percentile                           2
95th percentile                          18
maximum                                2677
```

Observed focal-cell DEG counts for the analog set were:

```tsv
target	n_degs	interpretation for Mapk8
Mapk9	0	closest represented JNK paralog, JNK2
Map3k7	0	TAK1, upstream of JNK/p38/NF-kappaB in cytokine and stress cascades
Map2k6	0	stress-MAPK MAP2K/p38-side comparator
Jund	0	represented AP-1 family member and downstream nuclear comparator
Mapk1	0	ERK2, MAPK counterexample
Map2k2	0	MEK2, ERK branch counterexample
Raf1	0	RAF paralog counterexample
Kras	0	upstream RAS counterexample
Rac1	0	Rho-family JNK/PAK-side counterexample
Pak2	0	Rho-family effector counterexample
Pak3	0	Rho-family effector counterexample
Nfkb1	0	TAK1/NF-kappaB branch counterexample
Map2k1	4	MEK1, sparse BRAF/MEK thalamic module
Braf	4	sparse BRAF/MEK thalamic module
Shoc2	1	partial BRAF/MEK module, Vgf only
Cdc42	1	self-transcript only in this cell group
Pak1	1	self-transcript only in this cell group
```

For the nonzero ERK/Rho entries, the actual focal-cell significant genes were narrow:

```tsv
target	significant genes in 151 TH Prkcd Grin2c Glut
Map2k1	Vgf, Ptpn5, Unc13a, Etv5, all down
Braf	Atp2a2, Ptpn5, Vgf, Unc13a, all down
Shoc2	Vgf down
Cdc42	Cdc42 down
Pak1	Pak1 down
```

Thus the only pathway-near multigene signal in the focal group is a small ERK-linked neuropeptide/synaptic response shared by `Braf` and `Map2k1`, not a JNK/AP-1 stress signature.

I compared `Mapk9`, `Map3k7`, `Jund`, `Mapk1`, `Map2k1`, `Braf`, `Map2k2`, `Map2k6`, `Shoc2`, `Raf1`, `Kras`, `Rac1`, `Cdc42`, `Pak1`, `Pak2`, `Pak3`, and `Nfkb1` in the focal cell group with the Distributed Agents runtime profile tools. All 17 had complete 17,259-gene profiles. Twelve of the 17 had no FDR-significant focal genes; only `Map2k1`, `Braf`, `Shoc2`, `Cdc42`, and `Pak1` had 1 to 9 significant features. The full-profile nearest neighbors for the null anchors were dominated by unrelated targets and the top tail overlaps were almost entirely genes with `pvals_adj = 1.0`, so I did not treat those nominal ranks as evidence of a hidden `Mapk9`/`Map3k7`/`Jund` module.

## Within-dataset and corpus evidence

`Mapk9` is the most direct measured paralog of `Mapk8`; `Mapk8` encodes JNK1 and `Mapk9` encodes JNK2. In the training endpoint, `Mapk9` had exactly 0 DEGs in `151 TH Prkcd Grin2c Glut`. The Distributed Agents corpus also contains a high-confidence `Mapk9` negative result: single `Mapk9` loss was FDR-silent across 21 recovered neuronal groups, and expected AP-1/immediate-early, apoptosis, and FoxO/autophagy transcript proxies were absent. This makes `Mapk9` the strongest same-family prior for `Mapk8`.

`Map3k7` had 0 focal DEGs and, in the corpus, anchored a broader negative module stating that represented TNFR/TLR/IL-1/CD40-to-TAK1/IKK/NF-kappaB/JNK/p38 perturbations were broadly transcriptionally silent as a basal module in unchallenged postnatal NeuN-positive neurons. The same local claim connected `Map3k7` with flat `Chuk`, `Nfkb1`, `Rel`, `Map2k6`, and `Mapk9` readouts. This is not as close to JNK1 as a JNK paralog would be because TAK1 is an upstream, stimulus-gated kinase and the exact JNK MAP2Ks `Map2k4` and `Map2k7` were not represented, but it argues against a tonic inflammatory/stress cascade in the sampled thalamic neurons.

`Jund` had 0 focal DEGs. The corpus reports that `Jund` loss was buffered across basal postnatal neurons: 22 of 23 measured groups had no FDR<0.10 downstream genes, and represented AP-1/bZIP relatives and MAPK neighbors did not phenocopy `Jund`. Because JNK1 is classically linked to c-Jun/AP-1 phosphorylation, the absence of a `Jund`-family LoF RNA response is a useful downstream countercheck. It is imperfect because phosphorylation of JUN is not the same perturbation as deleting `Jund`, and `Jun` itself was not in the training set.

The observed ERK branch is a positive control for assay sensitivity, not a reason to call `Mapk8` nonzero. `Map2k1` and `Braf` each had 4 focal DEGs and shared `Vgf`, `Ptpn5`, and `Unc13a` down-regulation; `Shoc2` had the weaker one-gene `Vgf` arm. Distributed Agents corpus claims over `Map2k1` and `Braf` explicitly bounded this as a sparse BRAF-to-MEK1 thalamic module that did not generalize to `Map2k2`, `Mapk1`, `Raf1`, `Kras`, `Pak2`, or `Spred1`. That same-pathway nonconvergence kept me from transferring the four-gene ERK count onto the JNK branch.

Finally, the Rho-family and PAK comparators were unconvincing for a JNK prediction in this focal group. `Cdc42` and `Pak1` had only their own transcript as a DEG, while `Rac1`, `Pak2`, and `Pak3` had 0. Since these genes sit upstream of several MAPK branches and cytoskeletal outputs, the lack of a downstream AP-1 or stress RNA program is another weak negative for `Mapk8`.

## Biological rationale for Mapk8

Public literature places MAPK8/JNK1 in the stress-activated JNK MAPK family. JNKs are activated through dual phosphorylation by MKK4/MKK7 and regulate substrates including c-Jun/AP-1, with outputs in apoptosis, stress responses, differentiation, and neuronal survival depending heavily on context (Davis 2000; Weston and Davis 2007; Wang, Destrument, and Tournier 2006). Mouse genetics also supports strong isoform and context buffering: single `Jnk1`, `Jnk2`, or `Jnk3` mutants can survive, while combined `Jnk1/Jnk2` loss causes severe embryonic brain apoptosis defects (Kuan et al. 1999), and neuronal JNK/c-Jun effects differ by developmental stage and injury or trophic-withdrawal stimulus (Ham et al. 2000).

The experiment perturbs sparse postmitotic neurons at P16 and reads out steady-state nuclear RNA three to four weeks later, without excitotoxic, cytokine, or trophic-withdrawal stimulation and without phospho-JUN or kinase-flux measurements. In that exact regime, the training data show that the represented JNK2/AP-1/TAK1/stress-MAPK side is silent or near-silent and that even many receptor-proximal MAPK inputs are buffered. The most reasonable transfer is therefore that isolated `Mapk8` loss will be paralog-buffered by other JNK isoforms and will not create any FDR<0.05 genes in `151 TH Prkcd Grin2c Glut`.

## Prediction

I predict:

```tsv
target_name	predicted_n_degs
Mapk8	0
```

## Limits

- `Mapk8` itself, `Mapk10`, `Map2k4`, and `Map2k7` were absent from the visible training data, so the closest direct observed evidence is `Mapk9`, not JNK1 itself or its exact MAP2Ks.
- The corpus also has no held-out `Mapk8` node, so all same-experiment claims are transferred from observed analogs.
- JNK signaling is often phospho-protein and stimulus gated. A basal snRNA-seq endpoint can miss altered phospho-JUN, altered apoptosis threshold, axonal transport, local synaptic phenotypes, or responses that would only appear after cytokines, excitotoxicity, trophic withdrawal, or injury.
- The AAV CRISPR perturbation is sparse and mosaic with modest average target mRNA depletion. A zero DEG prediction is specific to this assay and threshold, not a statement that a complete germline or conditional `Mapk8` knockout would be biologically silent.
