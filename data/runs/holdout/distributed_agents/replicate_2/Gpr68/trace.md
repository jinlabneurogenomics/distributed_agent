# Prediction target

The manifest `097_Gpr68.csv` requests one held-out perturbation, `Gpr68`. I
interpreted the endpoint as the exact training-count definition: the number of
measured genes in `151 TH Prkcd Grin2c Glut` whose Wilcoxon
Benjamini-Hochberg adjusted p-value is below 0.05, including the perturbed
gene transcript itself if it is measured and significant. The requested
`Gpr68` knockout is absent from both the differential-expression parquet and
the focal training-count CSV, so its count has to be transferred from assayed
perturbations.

# Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Focal-cell training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest:
  `[local file: 097_Gpr68.csv]`.
- Distributed Agents same-experiment semantic corpus,
  `perturbai-july-260713-sourceguard-1773-v1`. `Gpr68` itself was not
  annotated in this corpus, but the corpus contained receptor and
  second-messenger claims over the same Perturb-seq measurements.
- PubMed-indexed literature on proton-sensing GPCR biology and neuronal GPR68:
  Tomura et al. 2005, DOI 10.1016/j.cellsig.2005.06.002, PMID 16014326;
  Sisignano et al. 2021, DOI 10.3390/cells10082050, PMID 34440817;
  Huang et al. 2020, DOI 10.1021/acs.biochem.0c00576, PMID 32865988;
  Wang et al. 2020, DOI 10.1161/STROKEAHA.120.031479, PMID 33059544;
  Xu et al. 2020, DOI 10.1186/s13041-020-00672-8, PMID 32993733;
  Zhou et al. 2021, DOI 10.1096/fj.202002511R, PMID 33724568.

# Dataset queries

I read the small focal count CSV to get observed `n_degs` for candidate
training perturbations, then queried the parquet for the focal group and the
same candidates. For each training target I counted the number of focal genes
with `pvals_adj < 0.05` and `pvals_adj < 0.10`, and inspected the actual
significant genes to distinguish self-transcript calls from downstream
responses. The parquet contains 17,259 measured genes for each of these focal
target slices.

The mechanistic-neighbor results most relevant for `Gpr68` were:

| training perturbation set | focal `n_degs` evidence |
| --- | --- |
| Orphan or named `Gpr*` receptors: `Gpr156`, `Gpr158`, `Gpr161`, `Gpr179`, `Gpr45`, `Gprasp2`, `Gprc5b` | counts were `0, 1, 0, 0, 0, 1, 0`; the two singleton signatures were self only (`Gpr158` and `Gprasp2`) |
| Gq/PLC/Ca2+/PKC GPCR branch: `Chrm3`, `Grm5`, `Htr2c`, `Kiss1r`, `Plcb1`, `Prkca` | all `0` in the focal count table and all had zero focal genes even at FDR 0.10 |
| Additional nearby effectors or receptors: `Chrm2`, `Htr2a`, `Htr2b`, `Itpr1`, `Mapk1`, `Camk2a`, `Grm1`, `Prkcg` | `Chrm2`, `Htr2a`, `Htr2b`, `Itpr1`, `Mapk1`, and `Camk2a` had `0` genes at FDR 0.05; `Grm1` and `Prkcg` each had one FDR 0.05 gene and it was the perturbed transcript itself |
| G protein and cAMP-side comparators: `Adcy1`, `Adcy3`, `Adcy5`, `Gnal`, `Gnas`, `Gnao1` | `Adcy1`, `Adcy3`, `Adcy5`, `Gnal`, and `Gnas` were `0`; `Gnao1` was a singleton self-transcript call |
| Sparse class-B GPCRs: `Glp1r`, `Pth1r` | both were `0` |

I also checked whether several assayed orphan-GPCR perturbations changed the
measured `Gpr68` transcript in the focal group. The `Gpr68` row was present in
these focal slices, but it had adjusted p-value 1.0 in `Gpr156`, `Gpr158`,
`Gprasp2`, and `Gprc5b`, so no assayed orphan-GPCR state obviously
co-regulated `Gpr68` in this cell group.

# Same-experiment corpus evidence

The Distributed Agents corpus had no `Gpr68` target context or explicit first-hop
neighbors, so there was no internally curated `Gpr68` analog. I therefore used
its curated claims about represented GPCR and second-messenger perturbations as
negative controls.

- Claim `claim:9f69c85a0a28574c603c` states that single-gene perturbations of
  represented neuromodulatory GPCRs and proximal Gq/PLC/Ca2+/PKC/MAPK
  effectors generally failed to produce a shared basal neuronal
  nuclear-transcriptome module. Its supporting findings explicitly covered
  `Chrm3`, `Grm1`, `Grm5`, `Htr2c`, `Kiss1r`, `Plcb1`, `Prkca`, `Itpr1`, and
  related nodes.
- Claim `claim:5778f7e46773642bd0bd` states that represented dopamine/GPCR and
  cAMP-pathway perturbations do not collapse into one durable basal neuronal
  mRNA module. This matters because GPR68 can couple beyond Gq in some systems;
  directly assayed `Gnas`, `Gnal`, `Adcy1`, `Adcy3`, `Adcy5`, `Pde1c`, and
  dopamine-receptor losses were mostly flat or nonconvergent.
- Claim `claim:fd0c2552c25f6a629585` similarly found that sparse class-B
  receptors `Glp1r` and `Pth1r` were uncoupled from canonical
  G-protein/cAMP/PKA/CREB basal transcriptional responses.

Those claims do not prove that every orphan receptor must be silent, but they
show that the same assay did not convert membrane GPCR loss, Gq/PLC loss, or
cAMP-source-arm loss into a broad steady-state RNA state.

# Target-specific rationale

## Gpr68

`Gpr68` encodes OGR1/GPR68, one of the four proton-sensing GPCRs together with
GPR4, GPR65/TDAG8, and GPR132/G2A. The receptor is activated by extracellular
acidification through extracellular histidines and is reported to signal
through heterotrimeric G proteins including the Gq/11-PLC-Ca2+ axis, with
context-dependent engagement of other arms such as Gs and G12/13
(Tomura et al. 2005; Sisignano et al. 2021; Huang et al. 2020). GPR68 is also
not a brain-irrelevant receptor: loss or modulation changes hippocampal LTP and
passive avoidance behavior, and neuronal GPR68 protects in acidic or ischemic
models through PKC and PERK/eIF2a-linked stress signaling
(Wang et al. 2020; Xu et al. 2020; Zhou et al. 2021).

The external biology therefore argues that the gene can matter in neurons, but
the match to this readout is weak. The Perturb-seq experiment assayed
3-to-4-week sparse loss of function in recovered postnatal neuronal nuclei
under basal conditions; it did not impose extracellular acidosis, ischemia, or
ligand potentiation, and it under-sampled glial and vascular contexts. In this
exact focal cell group, the closest assayed receptor class was nearly silent:
five of seven `Gpr*` perturbations had zero DEGs, and the two nonzero counts
were self-transcript knockdown only. Canonical downstream paths were no more
active. `Chrm3`, `Grm5`, `Htr2c`, `Kiss1r`, `Plcb1`, and `Prkca` all had zero
FDR 0.05 and zero FDR 0.10 genes in the focal parquet slice, while `Gnas`,
`Gnal`, and `Adcy1/3/5` were also FDR-flat. The broader Distributed Agents corpus
reached the same qualitative boundary over all cell groups: represented GPCR,
Gq/PLC, and cAMP perturbations were mostly flat, singleton, or mutually
nonconvergent at basal nuclear RNA level.

I therefore predict that an acute `Gpr68` perturbation will not generate a
downstream `151 TH Prkcd Grin2c Glut` RNA module. A one-gene, self-transcript
call is possible, because the endpoint includes the targeted receptor mRNA and
some assayed GPCRs were singletons for that reason, but most receptor targets
in this neighborhood did not even cross FDR on the self row. The best point
estimate is `0`.

# Limits

The exact proton-sensing paralogs `Gpr4`, `Gpr65`, and `Gpr132` were not in the
training count table, and the same-experiment Distributed Agents corpus had no direct
`Gpr68` finding. The comparison therefore leans on more general GPCR and
Gq/cAMP pathway perturbations rather than a perfect OGR1-family analog. The
published GPR68 studies include germline knockouts, bulk brain RNA-seq,
hippocampal slices, ischemic stress, and pharmacologic potentiation; those
systems establish function but are not the same as acute sparse P16 CRISPR in
basal thalamic glutamatergic nuclei. Finally, the count endpoint is a
thresholded FDR statistic, so a true tiny downstream shift, a low-power
self-transcript change, or an unmeasured protein-only response could still be
present despite a prediction of zero measured DEGs.
