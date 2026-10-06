# DEG-count prediction trace

## Question and target

I interpreted the task as a point prediction of the held-out endpoint `n_degs`: the number of genes with Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` after each acute AAV-CRISPR perturbation in `151 TH Prkcd Grin2c Glut` nuclei. The held-out manifest for this run contained one target:

```tsv
target_name
Foxp1
```

The target was absent from both the differential-expression parquet and the focal-cell training-count CSV, so the prediction had to be transferred from non-held-out perturbations.

I treated the Allen label `151 TH Prkcd Grin2c Glut` as the exact `group_name` in the parquet and not as a request to aggregate other thalamic or tyrosine-hydroxylase-expressing populations. I also used the focal-cell DEG-count file as the endpoint calibration rather than re-counting all training targets from the parquet.

## Sources

- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal-cell observed endpoints: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest: `[local file: 081_Foxp1.csv]`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. I queried `Foxp1` directly; this release had no Foxp1 claims, findings, or explicit references, so it did not contribute a Foxp1-specific same-experiment mechanism.
- PubMed literature, using the NCBI PubMed E-utilities search exposed through `mcp__bioeval_literature`.

Key external references:

- Ferland et al. 2003, DOI `10.1002/cne.10654`: `Foxp1` and `Foxp2` are expressed in developing and mature mouse basal ganglia, cortex, thalamus, and other postmitotic neuronal populations.
- Hisaoka et al. 2009, DOI `10.1016/j.neuroscience.2009.12.055`: cortical `Foxp1` and `Foxp2` mark different postnatal/adult projection-neuron subsets; `Foxp1` is prominent in Satb2-positive corticocortical neurons and Tbr1-positive corticothalamic neurons.
- Fong et al. 2018, DOI `10.1016/j.neuroscience.2018.07.017`: adult striatal `Foxp1` and `Foxp2` overlap in spiny projection neurons but differ in D1/D2 bias, so `Foxp2` is close but not identical to `Foxp1`.
- Sin et al. 2014, DOI `10.1007/s12031-014-0359-7`: FOXP1/2/4 paralogs can homo- and heterodimerize, making `Foxp2` the closest assayed in-dataset paralog.
- Bacon et al. 2014, DOI `10.1038/mp.2014.116`; Araujo et al. 2015, DOI `10.1101/gad.267989.115`; Khandelwal et al. 2024, DOI `10.1126/sciadv.adm7039`: mouse `Foxp1` loss changes striatal development, striatal excitability, and postnatal synaptic input programs.
- Precious et al. 2016, DOI `10.1016/j.expneurol.2016.05.002`: FoxP1 marks medium spiny neuron precursors and mature MSNs and is required for DARPP-32-positive MSN differentiation in vitro.
- Arlotta et al. 2008, DOI `10.1523/JNEUROSCI.2986-07.2008`: `Bcl11b`/Ctip2 is a key MSN differentiation factor and regulates MSN markers including FOXP1.
- Li et al. 2015, DOI `10.1371/journal.pone.0127671`; Pearson et al. 2020, DOI `10.1016/j.celrep.2020.01.034`: `Foxp1` also regulates cortical radial migration, neuronal morphogenesis, and radial glial fate timing.
- Lozano et al. 2021, DOI `10.1186/s11689-021-09358-1`: human FOXP1 haploinsufficiency causes a neurodevelopmental syndrome with intellectual disability, speech/language deficits, and autism features.

## Dataset computations

I first counted the focal-cell training endpoints:

- 1,674 non-held-out perturbations were present.
- 1,205 of 1,674 had `n_degs = 0`.
- 469 had at least one DEG.
- The median was `0`, the 75th percentile was `1`, and the maximum was `2677`.

This cell group is therefore strongly zero-inflated; a plausible biological perturbation should only be called nonzero if comparable training perturbations overcame that stringent FDR boundary.

I then looked up training counts for gene families and pathways that could transfer to `Foxp1`, especially FOXP paralogs, cortical/striatal projection-neuron transcription factors, and known FOXP1-associated neurodevelopmental regulators. I filtered the DE parquet to

```python
group_name == "151 TH Prkcd Grin2c Glut"
gene_target in candidate_targets
```

and, for each candidate, sorted measured genes by `pvals_adj` to inspect whether a target with `n_degs = 0` was just below threshold or was truly flat. I also kept `n_pert_matched` and `n_ctrl_matched` to verify that these were not missing or trivially tiny comparisons; the queried candidates had 126 to 288 matched perturbed nuclei versus 23,679 controls.

Finally, I ran `mcp__distributed_agents_runtime.profile_neighbors` on a 17-target candidate signature table with Pearson/cosine whole-profile similarity and positive/negative tail overlap. The runtime profile compared `Foxp2`, `Bcl11b`, `Satb2`, `Tbr1`, `Sox5`, `Zbtb18`, `Mecp2`, `Gtf2i`, `Adnp`, and `Chd8` against 17 mechanistic candidates. It found dense tail overlaps even among the zero-DEG signatures, which were driven largely by broad near-null profiles rather than a discriminating FOXP module, so I used it only as weak confirmation that `Foxp2` was not hiding a coherent strong response.

## Target-specific reasoning

### Foxp1

`Foxp1` encodes a forkhead transcription factor with established roles in neuronal development. It is a real neurodevelopmental disease gene, and mouse work shows roles in striatal medium spiny neurons, cortical projection-neuron morphogenesis, and postnatal maturation of striatal excitatory inputs. That external biology made me avoid treating `Foxp1` like a generic silent transcription factor. The closest evidence inside this specific experiment, however, put it in a zero-response region of the assay:

```tsv
training_target	n_degs	relevance to Foxp1	evidence in 151 TH Prkcd Grin2c Glut
Foxp2	0	closest assayed FOXP paralog; co-expressed with Foxp1 in several projection-neuron systems and can form FOXP heterodimers	no adjusted p-value below 1.0 among the strongest rows inspected; 245 perturbed nuclei vs 23679 controls
Foxp3	0	FOXP-family negative control with little neuronal relevance	no adjusted p-value below 1.0 among inspected rows; 256 perturbed nuclei
Bcl11b	0	key striatal MSN transcription factor whose mutant striatum loses FOXP1 among other MSN markers	no adjusted p-value below 1.0 among inspected rows; 206 perturbed nuclei
Bcl11a	0	related neuronal BCL11 family TF, less direct than Bcl11b	no adjusted p-value below 1.0 among inspected rows; 203 perturbed nuclei
Pde10a	0	postnatal striatal FOXP1-syndrome pathway gene and MSN marker, downstream rather than a TF analog	best q = 0.304; 191 perturbed nuclei
Satb2	0	projection-neuron identity TF that shares cortical Foxp1-positive lineages	best q = 1.0 in inspected rows; 236 perturbed nuclei
Tbr1	0	deep-layer corticothalamic identity TF used as a counterexample for developmental projection-neuron regulators	best q = 0.944; 288 perturbed nuclei
Sox5	2	deep-layer and corticofugal developmental TF with a small but detectable perturbation	best two q-values were 0.00054 and 0.028; 184 perturbed nuclei
Mef2c	1	activity-dependent neuronal TF and neurodevelopmental regulator, a positive counterexample near threshold	one DEG, the target transcript itself, q = 0.028; 223 perturbed nuclei
Zbtb18	5	cortical neurodevelopmental TF that shows a small focal response	5 DEGs; best gene Endou q = 1.5e-08; 208 perturbed nuclei
Gtf2i	10	neurodevelopmental transcription regulator that demonstrates the assay can catch a direct TF response in this cell group	10 DEGs including Gtf2i itself, q = 1.8e-25; 148 perturbed nuclei
Mecp2	16	broad neuronal chromatin/transcriptional regulator, used as an upper counterexample rather than a direct mechanistic analog	16 DEGs; best q = 1.4e-06; 167 perturbed nuclei
Adnp	25	chromatin-associated ASD gene, broader than Foxp1 but still a neuronal transcriptional regulator	25 DEGs; best q = 1.5e-10; 126 perturbed nuclei
Chd8	61	strong chromatin remodeler counterexample showing high-ASD-risk TF/chromatin biology can produce a wide response	61 DEGs; Chd8 itself q = 1.0e-09; 197 perturbed nuclei
```

The most direct transfer is from `Foxp2`, because it is an expressed FOXP paralog and a dimerization partner, not just a gene-family name. Its complete lack of focal response makes a wide `Foxp1` response unlikely under the AAV-CRISPR conditions. The full set of assayed `Fox*` perturbations in the training endpoint was also zero-DEG: `Foxa2`, `Foxc2`, `Foxe3`, `Foxi1`, `Foxj3`, `Foxk2`, `Foxl1`, `Foxl2`, `Foxn1`, `Foxp2`, and `Foxp3` each had `n_degs = 0`.

The striatal pathway literature could have pushed `Foxp1` upward, but the in-dataset striatal comparators did not. `Bcl11b`, `Pde10a`, `Rarb`, `Isl1`, `Ebf1`, `Ebf2`, `Ebf3`, `Zfp521`, `Meis1`, `Meis2`, `Nfia`, `Nfib`, `Nfix`, `Pbx1`, and `Tshz3` all had zero DEGs in the focal cell group. This is consistent with the fact that `151 TH Prkcd Grin2c Glut` is a thalamic glutamatergic cell group, whereas much of the strongest FOXP1 biology is in embryonic cortex or striatal MSNs.

The positive counterexamples were informative but imperfect. `Gtf2i`, `Mef2c`, `Zbtb18`, `Mecp2`, `Adnp`, and `Chd8` prove that transcriptional and chromatin regulators can produce detectable effects with similar numbers of perturbed nuclei in this cell type. Their mechanisms are broader or more proximal to chromatin/activity programs than FOXP1's best-supported postmitotic striatal identity program, and their observed counts ranged from 1 to 61, not hundreds, for the closer developmental TFs. In the strongest close lane, `Foxp2`/`Bcl11b`/`Satb2`/`Tbr1` were all zero and nearly all completely flat at the adjusted-p-value level.

I therefore predict no FDR-significant DEG for acute `Foxp1` loss in `151 TH Prkcd Grin2c Glut`.

## Limits

- `Foxp1` itself was held out, so no expression signature or target-RNA knockdown statistic for `Foxp1` was available in the supplied matrices.
- The Distributed Agents corpus release had no `Foxp1` node, so all Foxp1-specific mechanism came from PubMed literature rather than a same-release Claim or Finding.
- The closest in-dataset paralog was `Foxp2`; `Foxp1` and `Foxp2` overlap in some projection neurons but are not interchangeable, and `Foxp1` has distinct roles in cortical, striatal, and non-neural tissues.
- Most published mouse data perturb `Foxp1` embryonically, germline, or with region-specific Cre drivers. The experiment here perturbs mosaic postmitotic juvenile neurons and produces modest average on-target RNA reduction, so developmental phenotypes are expected to overestimate the focal snRNA-seq response.
- `151 TH Prkcd Grin2c Glut` is not a striatal MSN population, which weakens transfer from the best-characterized FOXP1 striatal program. Ferland et al. did observe thalamic `Foxp1` expression, but there was not a focal-cell-specific FOXP1 loss-of-function dataset to calibrate from.
- Because the endpoint is a hard FDR count in a zero-inflated assay, the difference between a prediction of 0 and a prediction of a few DEGs is assay-threshold uncertainty more than a claim that FOXP1 is biologically inert.

## Final point prediction

```tsv
target_name	predicted_n_degs
Foxp1	0
```
