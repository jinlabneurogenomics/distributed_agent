# Lyst DEG-count prediction trace

## Question and resolved ambiguities

The held-out manifest contains one requested perturbation, `Lyst`. I interpreted the endpoint as the integer number of measured genes with `pvals_adj < 0.05` in the exact focal cell group, `151 TH Prkcd Grin2c Glut`. The prediction therefore needs to be on the same scale as the focal training file, not a prediction of biological severity, edited-cell fraction, target knockdown strength, or a bulk tissue effect.

`Lyst` was completely held out, so I did not have a `Lyst` expression signature. I used the non-held-out perturbations to ask whether acute postnatal neuronal loss of lysosome-, LRO-, AP-3/BLOC-, Rab-, retromer/HOPS-, and autophagy-related genes produces the same kind of nuclear mRNA program that `Lyst` would plausibly trigger.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  - 1,674 non-held-out focal-cell perturbations.
  - The focal endpoint is sparse: 1,205/1,674 training targets have `n_degs = 0`; the median is 0, the 75th percentile is 1, the 95th percentile is 18, and the largest response is 2,677.
- `[local file: training_de_all_cell_groups.parquet]`
  - I used `pyarrow.dataset` filters to pull `151 TH Prkcd Grin2c Glut` rows for 44 mechanistic comparator targets. This yielded 759,396 rows, 17,259 measured genes per target.
  - For each comparator I recomputed `sum(pvals_adj < 0.05)` from the filtered DE rows and inspected the significant genes and the target-gene row when present.
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`
  - `Lyst` itself has no node or direct frozen findings in this corpus.
  - I used frozen claims/findings for `Ap3b1`, `Dtnbp1`, and `Rab7`; the most relevant corpus claims were:
    - `claim:7981b729c761ce52996a`: represented AP-3/BLOC-related perturbations share a buffered juvenile neuronal transcriptomic outcome.
    - `claim:726468d7afc216bc3be2`: `Rab7` loss induces a selective neuronal late-endosomal/lysosomal compensation program that is weakly shared by `Vps41` but absent after `Ocrl`, `Abca7`, or `Gdi1`.
    - `claim:56e1e77cd2cb9bb6604f`: represented acute lysosomal disease perturbations do not elicit a shared lysosomal storage, autophagy, TFEB/MiT, or ISR/UPR nuclear RNA program.
- Distributed Agents runtime profile comparison
  - I compared 18 focal-cell profiles from the selected comparator set. The activity classes were consistent with the count table: `Rab7` was the only member with at least 50 significant features; `Vps35` and `Vps54` were 10-49 DEG responses; most candidate LRO/lysosome/autophagy comparators had no significant features or only the target transcript itself.
- PubMed literature
  - Talbert, Malicdan and Introne 2023, DOI `10.1097/MOH.0000000000000766`; Sharma et al. 2019, DOI `10.1016/j.ddmod.2019.10.008`: loss-of-function variants in `LYST` cause Chediak-Higashi syndrome, with enlarged lysosomes or lysosome-related organelles and progressive neurologic disease.
  - Serra-Vinardell et al. 2023, DOI `10.1007/s00018-023-04695-x`: LYST-deficient human neuronal models have enlarged autolysosomes and impaired autophagic lysosome reformation.
  - Holland, Torgersen, Sandvig and Simonsen 2014, DOI `10.1111/tra.12227`: siRNA depletion of LYST changed lysosome size and number while preserving endocytic and autophagic degradation rates in human cell lines, supporting a size/fission role rather than simple loss of acidification or terminal degradation.
  - Bowman et al. 2019, DOI `10.1111/tra.12646`; Bonifacino 2004, DOI `10.1196/annals.1315.018`: AP-3 and the BLOC complexes route cargoes to lysosome-related organelles in Hermansky-Pudlak biology.
  - Di Pietro et al. 2006, DOI `10.1091/mbc.e06-05-0379`; Larimore et al. 2011, DOI `10.1091/mbc.E11-07-0592`: BLOC-1 interacts with AP-3 in endosomal protein trafficking, including neuronal cargo sorting.
  - Gil-Krzewska et al. 2015, DOI `10.1016/j.jaci.2015.08.039`, and Izumi, Gomi, Kasai, Mizutani and Torii 2003, DOI `10.1247/csf.28.465`: LYST and Rab27 pathways both affect regulated LRO exocytosis, but at the level of organelle size/polarization/docking rather than a known shared somatic RNA program.
  - Plemel et al. 2011, DOI `10.1091/mbc.E10-03-0260`, and van der Beek et al. 2024, DOI `10.1091/mbc.E23-08-0328`: Rab7/HOPS biology controls late endosome and lysosome fusion, giving context for why `Rab7` is a useful positive lysosomal-stress comparator but not a one-to-one LYST phenocopy.

## Comparator evidence from the focal cell group

### Closest LRO/AP-3/BLOC and regulated-secretory-granule comparators

These are the most direct within-dataset analogs because LYST is the Chediak-Higashi lysosomal trafficking regulator and the AP-3/BLOC/Rab27 families are the neighboring Hermansky-Pudlak/Griscelli LRO biogenesis or LRO secretion genes. In `151 TH Prkcd Grin2c Glut`, every one of the represented AP-3/BLOC/Rab secretory candidates was silent:

| training perturbation | focal `n_degs` | focal expression-pattern evidence | role in the `Lyst` call |
|---|---:|---|---|
| `Ap3b1` | 0 | no FDR-significant genes; `Ap3b1` transcript itself had log2FC -0.166, `padj = 1` | AP-3 beta subunit; direct LRO cargo-routing comparator. A zero argues that LRO cargo sorting can be transcriptionally buffered in juvenile neurons. |
| `Dtnbp1` | 0 | no FDR-significant genes; `Dtnbp1` log2FC -0.295, `padj = 1` | BLOC-1 subunit/dysbindin; same buffered result as `Ap3b1` in the Distributed Agents corpus. |
| `Rab27a` | 0 | no FDR-significant genes; `Rab27a` log2FC +0.158, `padj = 1` | Griscelli/LRO-exocytosis Rab. It shares regulated granule biology with LYST in NK cells and melanocytes, but no neuronal nuclear RNA response here. |
| `Rab3gap1`, `Rab3gap2`, `Rab18` | 0, 0, 0 | each had 0 DEGs | Rab secretory- or organelle-trafficking comparators; they bound the Rab-family evidence away from a generic Rab perturbation response. |
| `Nbea` | 0 | no FDR-significant genes | a neuronal BEACH-domain trafficking protein; useful as a weak paralog/domain counterexample, not as a same-complex analog. |

The Distributed Agents corpus independently reports that `Ap3b1` had no corrected downstream response across 18 recovered neuronal groups and `Dtnbp1` had no corrected response across 23 recovered neuronal groups; their shared absence was captured as the AP-3/BLOC buffered claim `claim:7981b729c761ce52996a`. This is the strongest within-experiment prior for `Lyst`: the closest represented Chediak-Higashi/Hermansky-Pudlak-style LRO cargo perturbations do not create a detectable 3-4 week neuronal snRNA-seq program.

### Late endosome, HOPS, retromer, and GARP comparators

`Rab7` shows that this exact screen can detect a large late-endosomal/lysosomal transcriptional state when the perturbation hits a central terminal trafficking node: in the focal cell group `Rab7` had 501 DEGs, including induced `Atp6v1b2`, `Ptgds`, `Dpp7`, `Scpep1`, `Dusp1`, `Insig1`, `Atp6v0b`, `Slc20a1`, and `Dync1h1`. The response included V-ATPase, lysosomal hydrolase, sterol/lipid, proteostasis, and neuronal remodeling branches in the same-experiment corpus.

I treated `Rab7` as a positive detector and a counterexample, not as the central `Lyst` analog. `Vps41`, a HOPS-specific subunit in the Rab7 fusion pathway, had 0 DEGs in the focal group. `Vps35` retromer and `Vps54` GARP produced only restricted responses, with 17 and 31 DEGs respectively. `Abca7`, `Ocrl`, `Gdi1`, `Vps35l`, and `Washc4` were flat or self-only in the same focal group. Thus a broad 500-gene lysosomal stress state is available on this axis, but it appears specific to `Rab7` loss rather than a generic consequence of perturbing endosomal/LRO traffic.

### Autophagy and lysosomal storage comparators

LYST can affect autophagic lysosome reformation in neurons, so I inspected autophagy and storage-disease genes. Core autophagy initiation or LC3-lipidation perturbations were silent or nearly so in the focal group: `Atg5` 0, `Atg16l1` 0, `Becn1` 0, `Rb1cc1` 4. V-ATPase and lysosomal genes also mostly did not build downstream programs: `Lamp2` 0, `Atp6v1a` 0, `Atp6v1b2` 0, `Atp6v1e1` 0, `Atp6v0a1` 1, `Ctsb` 1. The lysosomal storage and cargo-routing panel was similarly sparse: `Gnptab` 0, `Gnptg` 0, `Sort1` 0, `Manba` 0, `Gaa` 1, `Ppt1` 1, `Psap` 1, `Tmem106b` 1. For the one-DEG storage genes, the single hit was simply the targeted transcript itself, e.g. `Gaa`, `Ppt1`, `Psap`, `Tmem106b`, or `Ctsb`.

This comparison is important because it separates an organelle phenotype from this endpoint. The literature supports LYST as a regulator of lysosome/LRO size and autophagic lysosome reformation; however, the matched dataset says that many primary defects in lysosome enzymes, M6P sorting, lysosomal membrane proteins, and basal autophagy do not become multi-gene nuclear mRNA responses under this juvenile mosaic CRISPR protocol.

## Target-specific prediction for `Lyst`

`Lyst` is biologically real in neurons and in LRO-bearing cells: biallelic LYST loss causes Chediak-Higashi syndrome with giant lysosomes or LROs, abnormal lytic granules, and progressive neurologic disease; human neuronal models show defective autophagic lysosome reformation after strong LYST deficiency. Those facts make a nonzero response plausible in principle.

The within-dataset evidence pushes the other way for this assay. The nearest represented LRO cargo and regulated-exocytosis perturbations, `Ap3b1`, `Dtnbp1`, and `Rab27a`, all had 0 DEGs in the focal cell group. A neuronal BEACH-domain comparator, `Nbea`, was also 0. Most lysosomal storage, M6P-sorting, V-ATPase, and core autophagy genes were 0 or single self-transcript hits. `Rab7` is the major exception with 501 DEGs, but Rab7 is a core late-endosome GTPase whose loss blocks a broad terminal trafficking and lysosome-compensation axis; `Lyst` is better described as regulating lysosome/LRO size, fission, and recovery after autophagy. I therefore do not project the full `Rab7` compensation module onto `Lyst`.

My predicted held-out count is consequently `0`: no measured gene is expected to pass BH-adjusted Wilcoxon `p < 0.05` in `151 TH Prkcd Grin2c Glut`.

## Limits and extrapolation

- The key limitation is that `Lyst` itself was absent from the training signatures and absent from the same-experiment Distributed Agents corpus; the prediction is an extrapolation from pathway neighbors.
- The perturbation modality matters. The literature often describes germline, biallelic, or strong loss in immune cells, melanocytes, retinal pigment epithelium, or differentiated in vitro neurons, whereas this experiment used sparse AAV CRISPR in postnatal NeuN+ brain with modest average on-target mRNA downregulation.
- `Ap3b1`, `Dtnbp1`, and `Rab27a` are mechanistically close at the LRO level but are not a LYST complex; they can miss an ALR-specific effect.
- Conversely, `Rab7`, `Vps41`, and `Vps35` touch later endosomal fusion and retrieval rather than LYST's BEACH-WD40 LRO-size function. Their nonzero counts show the assay is not blind to all endolysosomal stress, but they cannot calibrate `Lyst` exactly.
- The snRNA-seq endpoint cannot see enlarged vesicles, cargo missorting, lysosomal size/number, degranulation, synaptic vesicle release, or long-term neurodegeneration unless those properties feed back to a stable nuclear mRNA program before harvest.
