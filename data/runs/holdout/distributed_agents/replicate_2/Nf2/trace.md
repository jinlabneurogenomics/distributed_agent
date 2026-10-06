# Nf2 DEG-count prediction

## Question and resolved ambiguities

The requested manifest contains one held-out perturbation, `Nf2`. I interpreted the
endpoint as the exact focal-cell scalar used by the supplied training CSV: the
number of measured genes, including the target transcript itself if it is
measured and significant, with `pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut`.
The `Nf2` perturbation itself is fully held out, so no `Nf2` rows as a
`gene_target` were used. I did allow `Nf2` as a measured `names` gene in other
perturbations; a focal parquet query confirmed that `Nf2` is part of the 17,259
gene measured universe in this cell group.

## Sources

- Input parquet: `training_de_all_cell_groups.parquet`.
- Focal training endpoint: `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Held-out manifest: `149_Nf2.csv`.
- Run-local Distributed Agents finding reports in
  `codex_runtime/protected_inputs/findings_reports.filtered.jsonl`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`;
  this release had no direct `Nf2` held-out report, as expected, but I used its
  same-experiment claims on Rac/Cdc42/PAK and PI3K/mTOR buffering.
- Distributed Agents runtime `profile_compare`/`profile_inspect` over the focal parquet
  for a declared mechanistic cohort.
- PubMed for external NF2/Merlin biology.

## Computations over the supplied data

I first read the held-out manifest and the focal training counts. The focal
training endpoint is sparse: among 1,674 non-held-out gene targets, 1,205 have
`n_degs = 0`, 276 have `n_degs = 1`, 87 have 2-9, 63 have 10-99, and 43 have at
least 100. The median is 0 and the 75th percentile is 1, so a point prediction
near zero is not a fallback but the empirical baseline for buffered targets.

I inspected the parquet row-group metadata before filtering the focal group; the
file is grouped by `group_name`, and row groups 546-580 cover
`151 TH Prkcd Grin2c Glut`. I then used the Distributed Agents runtime to compare focal
Wilcoxon-score profiles for a cohort of 27 observed candidate perturbations:

`Rdx, Pak1, Pak2, Pak3, Rac1, Cdc42, Mtor, Rptor, Tsc2, Tead1, Dlg4, Erbb3,
Erbb4, Hras, Kras, Raf1, Braf, Map2k1, Map2k2, Mapk1, Pik3cb, Pik3r1, Pik3r2,
Akt3, Tiam1, Fyn, Sos1`.

The comparison used `gene_target` as entity, `names` as feature, Wilcoxon
`scores` as the signed value, and `pvals_adj < 0.05` to count significant
features. Nineteen of the 27 focal profiles had zero significant genes, seven
had one to nine significant genes, and only `Tsc2` was a broad focal responder.
Pairwise focal profile correlations among the ERM/Rho/PAK, TEAD, receptor,
RAS/MAPK, and PI3K nodes were near zero and there were no significant same-gene
intersections involving the singletons. For example:

| comparison in 151 TH | Pearson r | cosine | shared FDR-significant genes |
| --- | ---: | ---: | ---: |
| `Rdx` vs `Cdc42` | 0.044 | 0.041 | 0 |
| `Rdx` vs `Pak2` | -0.010 | -0.009 | 0 |
| `Tead1` vs `Mtor` | 0.069 | 0.065 | 0 |
| `Tead1` vs `Pik3cb` | 0.062 | 0.064 | 0 |
| `Mtor` vs `Tsc2` | -0.195 | -0.204 | 0 |
| `Pak1` vs `Pak3` | 0.083 | 0.083 | 0 |
| `Rac1` vs `Cdc42` | -0.016 | -0.020 | 0 |

## Nf2-specific within-dataset analogs

`Nf2` encodes Merlin, a FERM-domain, ERM-related cortical scaffold/tumor
suppressor. I therefore treated `Rdx` as the closest represented structural
analog. `Rdx` had `n_degs = 1` in the focal group, but the Distributed Agents report
showed that `151 TH Prkcd Grin2c Glut` had a significant drop of the `Rdx`
self-transcript and zero downstream genes; across the broader surface, `Rdx`
had only a lone `Stard3nl` hit in a different `022 L5 ET CTX Glut` group. This
supports a self-only or null prediction for `Nf2`, not a broad one.

Merlin can regulate Rac/PAK/actin outputs, so I compared the represented small
GTPase and PAK neighborhood. The exact focal counts were `Pak1 = 1`, `Pak2 = 0`,
`Pak3 = 0`, `Rac1 = 0`, `Cdc42 = 1`, `Tiam1 = 0`, and the broader actin-adjacent
counts were also flat (`Limk1 = 0`, `Kalrn = 0`, `Cyfip1 = 0`, `Ephb1 = 0`,
`Ephb2 = 0`, `Dock3 = 0`, `Tnik = 0`, `Arhgap18 = 0`, `Myo9a = 0`). The corpus
claim `claim:1aeabad1e41e30f971bc` summarizes the same experiment at higher
order: represented Rac/Cdc42-linked actin perturbations were transcriptionally
buffered in juvenile neurons rather than forming a recurrent nuclear mRNA
module. Thus the actin branch is biologically relevant but argues for 0-1
focal DEGs.

The best textbook transcriptional arm downstream of Merlin is Hippo-YAP/TAZ-TEAD.
Core Hippo members (`Stk3`, `Stk4`, `Sav1`, `Lats1`, `Lats2`, `Yap1`,
`Wwtr1/Taz`, `Tead2-4`) were not present as training perturbations, leaving
`Tead1` as the only direct transcription-factor comparator. `Tead1` was a clean
focal null with `n_degs = 0`. Its report also explicitly checked canonical
YAP/TEAD readouts such as `Ccnd1`, `Ccn1`, `Ccn2`, `Ankrd1`, `Apoe`, `Dab2`,
`Sox4`, and `Pik3c2b` and found them absent across the measured `Tead1` surface.
This is the strongest within-dataset evidence against an `Nf2` YAP/TEAD-like
transcriptional burst in these postmitotic neurons.

I also checked pathways often activated by Merlin loss in tumor and receptor
contexts. Focal counts for receptor/PI3K/mTOR entry nodes were uniformly null:
`Erbb3 = 0`, `Erbb4 = 0`, `Pik3cb = 0`, `Pik3r1 = 0`, `Pik3r2 = 0`, `Akt3 = 0`,
`Rptor = 0`, `Igf1r = 0`, `Insr = 0`, and `Irs1 = 0`. `Mtor` itself had only 2
DEGs and its report described a small mixed signature rather than a canonical
mTORC1 collapse. `Tsc2 = 86` and `Depdc5 = 13` are important counterexamples:
the assay can detect a TSC/GATOR-sensitive mTOR-linked state in this cell
group, but only when negative regulators of mTORC1 are removed; the positive
PI3K-AKT-MTOR components that are closer to receptor/Merlin signaling were
flat. Distributed Agents corpus claims `claim:28a4a006d8c87a92df98` and
`claim:b7b2ba203c83fdb0ed2d` captured the same split.

The RAS/MAPK route was similarly small or absent. `Hras`, `Kras`, `Raf1`,
`Mapk1`, and `Sos1` were 0 in the focal endpoint; `Braf` and `Map2k1` were both
4 and shared a small `Vgf/Ptpn5/Unc13a` down-program, but the training reports
explicitly rejected `Raf1`, `Kras`, `Hras`, `Mapk1`, and `Sos1` as phenocopies.
This makes the tiny BRAF/MEK state a sparse MAPK boundary, not a reason to
inflate `Nf2`.

Finally, I treated postsynaptic scaffold genes as boundary evidence because
Merlin has reported neuronal synaptic roles. `Dlg4 = 1`, `Magi2 = 0`, `Fyn = 0`,
and many synaptic adhesion/scaffold targets in the corpus fell into flat or
singleton-only classes. This argues that structural or localization phenotypes
often do not become a broad 3-4 week basal snRNA-seq response.

Large focal signatures such as `Ctnnb1 = 383`, `Tcf7l2 = 106`, and `Rab7 = 501`
were rejected as mechanistic analogs: they prove the `151` cell group has power
for Wnt and endolysosomal states, but they are not on a direct NF2/Merlin branch
in postmitotic neurons and did not match the candidate profile neighborhood.

## External biological rationale

External biology made the `Nf2` prior nonzero but context-dependent. Merlin is an
upstream regulator of Hippo signaling and YAP/TAZ-TEAD activity in growth and
contact-inhibition contexts (Zheng and Pan 2019, DOI
10.1016/j.devcel.2019.06.003; Kim and Gumbiner 2019, DOI
10.1073/pnas.1819400116). In the nervous system, `Nf2` deletion expands neural
progenitor, hippocampal primordium, callosal guidepost, dorsal-root-ganglion
progenitor, and glial populations through Yap/YAP-dependent mechanisms
(Lavado et al. 2013, DOI 10.1242/dev.096537; Lavado et al. 2014, DOI
10.1242/dev.111260; Serinagaoglu et al. 2014, DOI
10.1016/j.ydbio.2014.11.017). Merlin also affects neurite outgrowth and
Purkinje-cell or cerebellar synaptic organization through cytoskeletal signaling
(Schulz et al. 2010, DOI 10.1523/JNEUROSCI.0840-10.2010; Toledo et al. 2019,
DOI 10.1007/s00429-019-01897-7), and neuronal Merlin deletion alters peripheral
axon regeneration after sciatic nerve crush (Schulz et al. 2016, DOI
10.1371/journal.pone.0159718). The Merlin/Rac and Merlin/N-WASP literature
supports this cytoskeletal prior (Okada et al. 2007, DOI
10.1016/j.tcb.2007.03.006; Manchanda et al. 2005, DOI
10.1074/jbc.C400583200).

Those studies also explain why I down-weighted a broad count here. The strongest
YAP effects are developmental, glial, Schwann-cell repair, tumor, or mechanical
contact-inhibition settings. The present assay instead introduced sparse CRISPR
loss of function at P16, harvested NeuN-enriched postmitotic nuclei at P37-P44,
and measured a basal nuclear RNA state. The within-dataset TEAD, Rac/PAK,
receptor/PI3K, and RAS/MAPK observations show that these exact classes of
single-gene upstream signaling and scaffold perturbations are usually buffered
at this endpoint.

## Prediction and limits

The zero/nonzero decision is therefore: predict no FDR 0.05 gene for `Nf2`. A
singleton self-transcript result is possible because `Nf2` is measured in the
focal gene universe and because `Rdx`, `Pak1`, `Cdc42`, and `Dlg4` show that
self-only calls can occur. I nevertheless chose 0 rather than 1 because the
direct TEAD and upstream PI3K/RAS/Cdc42/Rac profiles were exact focal nulls and
the closest ERM/Rac/PAK analogs showed no shared downstream FDR genes.

The largest limitations are missing close Hippo perturbations (`Yap1`, `Wwtr1`,
`Lats1/2`, `Stk3/4`, `Sav1`), unmeasured Merlin protein and DNA indel rates, and
the fact that the external neuronal phenotypes are mostly morphology,
synaptogenesis, axon regeneration, or developmental progenitor expansion rather
than basal thalamic mRNA abundance. The count is thus an extrapolation from
buffered same-experiment branches, not a direct paralog or complex-member
phenocopy.
