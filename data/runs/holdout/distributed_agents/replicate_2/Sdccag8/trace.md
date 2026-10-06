# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out target file,
`[local file: 203_Sdccag8.csv]`,
contains one perturbation:

```text
Sdccag8
```

I interpreted `predicted_n_degs` as a point prediction for the number of genes
with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` contrast, matching
the training-count CSV.  I used the training CSV counts as the endpoint and the
parquet DE signatures as matched expression-profile evidence.  Because
`Sdccag8` was completely held out, its own DEG count and expression vector are
absent; I therefore transferred from training perturbations with curated ciliary
or centrosomal relationships, and I treated weak or absent target-RNA knockdown
as non-decisive rather than as editing failure.

## Sources used

- Input endpoint file:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`,
  1,674 training perturbations in the focal cell group.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I queried it in the focal cell group for profile comparison of selected
  ciliary training perturbations.
- Same-experiment Distributed Agents corpus MCP:
  `perturbai-july-260713-sourceguard-1773-v1`.  This was used only for packaged
  interpretations of the same non-held-out Perturb-seq data, never for
  `Sdccag8` held-out output lookup.  `target_context(Sdccag8)` returned no
  findings, claims, or references, as expected for this held-out gene.
- Run-local Distributed Agents gene-annotation and analog-nomination stores.  These
  use curated GO, Reactome, KEGG, MSigDB, CORUM, one-to-one ortholog-projected
  human CORUM, and pinned STRING physical-interaction annotations to nominate
  expected-similar mouse genes in the PerturbAI closed gene universe.
- PubMed literature for external `SDCCAG8` biology:
  Otto et al. 2010, Nat Genet, DOI 10.1038/ng.662 / PMID 20835237;
  Schaefer et al. 2011, Mol Syndromol, DOI 10.1159/000331268 / PMID 22190896;
  Insolera et al. 2014, Neuron, DOI 10.1016/j.neuron.2014.06.029 / PMID
  25088364; Airik et al. 2016, PLoS One, DOI 10.1371/journal.pone.0156081 /
  PMID 27224062; Tsutsumi et al. 2022, JBC, DOI
  10.1016/j.jbc.2022.101686 / PMID 35131266.

## Computational checks over the inputs

1.  The focal training distribution is sparse: among 1,674 non-held-out
    perturbations, 1,205 have `n_degs = 0`, the median is 0, the 75th percentile
    is 1, the 90th percentile is 2, the 95th percentile is 18, and the maximum is
    2,677.  I did not use this as a bulk prior by itself, but it calibrates how
    strong same-experiment evidence must be to justify a positive count.

2.  I used the run-local gene-annotation store to inspect `Sdccag8`.  Its
    memberships included GO `centrosome`, `centriole`, `centriolar satellite`,
    `ciliary basal body`, `cilium`, and `photoreceptor cell cilium`; GO biological
    process `regulation of cilium assembly`; Reactome `Cilium Assembly`,
    `Assembly of the 9+0 primary cilium`, and basal-body anchoring and centrosome
    maturation terms.  The analog nominator found no narrow exact-complex or
    paralog tier for `Sdccag8`; the relevant nominations were broad but coherent
    functional ciliary links.

3.  I crossed focal `n_degs` against the most relevant ciliary sets that contain
    `Sdccag8`.

    - GO `regulation of cilium assembly`, `GO:1902017`: among represented
      training targets, `Atg5`, `Cyld`, and `Ift88` had 0 DEGs; the less specific
      `Cdkl5` and `Syne1` each had 1.
    - Reactome `Cilium Assembly`, `R-MMU-5617833`, and `Assembly of the 9+0
      primary cilium`, `R-MMU-9975921`: the close structural/ciliary-trafficking
      members `Alms1`, `B9d1`, `Bbs5`, `Cep290`, `Dync2h1`, `Dync2i1`, `Ift43`,
      `Ift81`, `Ift88`, `Iqcb1`, `Kif3b`, `Lztfl1`, `Mchr1`, `Rpgrip1l`,
      `Sclt1`, and `Ttc21b` all had 0 DEGs in the focal group; `Arl3`, `Prkaca`,
      and `Ttc8` each had only 1.  The positive outlier `Dctn1` had 75 but is a
      dynein/dynactin cytoskeletal gene with broad cellular roles, not a close
      `Sdccag8` transition-zone or centriolar-satellite analog.
    - GO `centriolar satellite`, `GO:0034451`: 16 of 19 represented targets had
      0 DEGs; `Ttc8` had 1, `Cltc` had 3, and the broader Notch/ciliogenesis E3
      ligase `Mib1` had 27.
    - GO `ciliary basal body`, `GO:0036064`: 48 of 59 represented targets had
      0 DEGs.  The largest counts, such as `Psmb4` 742, `Prpf6` 454,
      `Ctnnb1` 383, `Dctn1` 75, and `Atxn10` 52, are pleiotropic proteasome,
      spliceosome, Wnt, cytoskeletal, or nuclear genes and serve as
      counterexamples to transferring by a broad basal-body annotation alone.

4.  I used `profile_compare` on the raw parquet with
    `context = {"group_name": "151 TH Prkcd Grin2c Glut"}`,
    `entity_column = gene_target`, `feature_column = names`,
    `value_column = logfoldchanges`, and `pvals_adj < 0.05` as the significance
    surface for this ciliary cohort:

    ```text
    Ift88, Cep290, Ift43, Ift81, Dync2h1, Dync2i1, Kif3b, Bbs5,
    Ttc8, Ttc21b, B9d1, Rpgrip1l, Alms1, Arl3, Iqcb1, Lztfl1
    ```

    Fourteen of these sixteen had no significant focal features; only `Arl3`
    and `Ttc8` had singleton `n_degs = 1`.  Close inspection of five focal
    anchors, `Ift88`, `Cep290`, `Bbs5`, `Ift43`, and `Rpgrip1l`, showed zero
    significant features for each and zero shared significant genes with ten
    ciliary peers.  Whole-vector logFC correlations among the ciliary peers were
    numerically smooth, but top-50 positive and negative tail overlaps were tiny
    and no FDR-level intersection was recovered.

5.  I audited the same 16 candidates in the same-experiment Distributed Agents corpus by
    `candidate_set_topology`.  They form one connected ciliary report component
    with 99/120 explicit report-derived pair connections; the largest fully
    connected subset included `Alms1`, `Bbs5`, `Cep290`, `Ift43`, `Ift81`,
    `Ift88`, `Kif3b`, `Lztfl1`, `Rpgrip1l`, and `Ttc8`.  This confirmed that the
    candidate set was a biologically coherent perturbation neighborhood in the
    source experiment.

## Target-specific reasoning

### Sdccag8

External biology.  `SDCCAG8`, also called `NPHP10` and `BBS16`, is a
centrosomal/basal-body ciliopathy gene.  Otto et al. identified truncating
`SDCCAG8` mutations in nephronophthisis-related renal-retinal ciliopathy
families, showed localization at both centrioles and direct interaction with
OFD1, and observed kidney-axis defects after `sdccag8` loss in zebrafish.
Schaefer et al. showed that `SDCCAG8` mutations can cause Bardet-Biedl syndrome.
Airik et al. showed that SDCCAG8 is required for ciliogenesis and Hedgehog
signaling and interacts with centriolar-satellite and centrosome-associated
proteins including OFD1, AZI1, RABEP2, and ERC1.  Tsutsumi et al. showed that
the C-terminal region controls SDCCAG8 localization to centrosomes and cilia
formation in cells, and that C-terminally truncated `Sdccag8` mice have
ciliopathy-like retinal, kidney, limb, palate, and spermatogenesis phenotypes.
Insolera et al. found an embryonic developing-cortex role for SDCCAG8 in
pericentriolar-material recruitment and neuronal migration via PCM1.

The most relevant training perturbations were:

| training target | focal `n_degs` | expression-pattern evidence and role |
|---|---:|---|
| `Ift88` | 0 | Core IFT-B/ciliogenesis node.  In the focal profile comparison, `Ift88` had 0 FDR genes.  Distributed Agents `Ift88:F003` reports that `Ift43`, `Ift81`, `Kif3b`, dynein-2, `Bbs5`, `Cep290`, `Smo`, `Ptch`, and `Gli` perturbations converged mainly by lack of robust DE rather than by a shared IFT-B knockout transcriptome. |
| `Ift43` | 0 | IFT-A/IFT component in the same ciliary-transport neighborhood; 0 focal DEGs and no significant overlap with `Ift88`, `Cep290`, `Bbs5`, or `Rpgrip1l` in the focal profile inspection. |
| `Ift81` | 0 | IFT-B component and direct `Ift88` comparator in corpus findings; 0 focal DEGs. |
| `Kif3b` | 0 | Kinesin-2 anterograde IFT motor; 0 focal DEGs and part of the dense ciliary corpus component. |
| `Dync2h1` | 0 | Dynein-2 retrograde IFT heavy chain; 0 focal DEGs and a direct IFT comparator in `Ift88`, `Cep290`, and `Alms1` same-experiment findings. |
| `Dync2i1` | 0 | Dynein-2 retrograde IFT intermediate chain; 0 focal DEGs. |
| `Cep290` | 0 | Transition-zone/gate gene, a strong structural analog for a held-out ciliopathy gene.  It had 0 focal DEGs and the corpus reports no robust nuclear DE program in any assayed postmitotic neuronal cell group (`Cep290:F001`), plus absent expected ciliary-GPCR, BBSome/IFT, and Hedgehog effector transcription (`Cep290:F003`). |
| `Rpgrip1l` | 0 | Transition-zone/Joubert and retinal-ciliopathy gene; 0 focal DEGs and explicitly included in flat ciliary comparator surfaces. |
| `B9d1` | 0 | MKS/B9 transition-zone complex gene.  It had 0 focal DEGs; its rare multi-gene effect in another cell group did not converge with represented ciliary and Hedgehog comparators (`B9d1:F008`), making it a cell-type-specific counterexample rather than evidence for focal `Sdccag8` activation. |
| `Bbs5` | 0 | BBSome component and ciliary trafficking analog.  It had 0 focal DEGs; the same-experiment corpus reports that expected Hedgehog, ciliary-GPCR, UPR/ISR, autophagy, and related BBSome/IFT programs were absent or nonconvergent (`Bbs5:F002`, `Bbs5:F003`). |
| `Ttc8` | 1 | BBSome component; it was nearly flat in the focal group and is described as transcriptionally flat or singleton-only in the ciliary comparator reports. |
| `Lztfl1` | 0 | BBSome regulator in Reactome cilium assembly; 0 focal DEGs and nonconvergent with `Bbs5`/`Alms1` in the corpus. |
| `Alms1` | 0 | Basal-body/ciliary trafficking gene.  It had 0 focal DEGs, and `Alms1:F003` reports that represented primary-cilium, BBSome, IFT, and ciliary-GPCR targets were flat or singleton-only rather than phenocopying a shared transcriptomic module. |
| `Iqcb1` | 0 | Nephronophthisis/retinal ciliary-gate comparator; 0 focal DEGs. |
| `Arl3` | 1 | Ciliary lipidated-protein transport node.  Its single focal DEG and corpus finding that ciliopathy comparators were almost orthogonal or flat argue against a broad `Sdccag8` count. |
| `Adcy3`, `Mchr1`, `Prkaca` | 0, 0, 1 | More distal ciliary GPCR/cAMP pathway perturbations.  `Adcy3:F003` notes shared near-null behavior of `Bbs5`, `Ttc8`, `Ift88`, `Cep290`, and `Rpgrip1l`, supporting displacement of ciliary disease biology to receptor localization, morphology, or physiology rather than stable nuclear RNA. |

The external literature makes `Sdccag8` biologically important, and the Insolera
developing-cortex data show that SDCCAG8 can matter in neurons.  That evidence
does not imply a broad postnatal `151 TH Prkcd Grin2c Glut` snRNA signature:
the developmental neuronal migration experiments are embryonic and cortical,
whereas the screen perturbed postmitotic juvenile neurons at P16 and measured
recovered NeuN+ nuclei 3-4 weeks later.  The closest measured analogs in the
actual assay -- IFT genes, dynein-2 genes, BBSome/BBS regulators, `Cep290`,
`B9d1`, `Rpgrip1l`, `Alms1`, `Adcy3`, and `Mchr1` -- were zero or singleton in
the focal group.

I therefore predict no FDR-significant genes for held-out `Sdccag8`.

## Final point prediction

| target | predicted `n_degs` |
|---|---:|
| `Sdccag8` | 0 |

## Limits and extrapolation

- `Sdccag8` itself was absent from the parquet, from the training endpoint, and
  from the same-experiment Distributed Agents corpus; the call is wholly transferred from
  related genes.
- The run-local annotation nominator found only broad functional links, not a
  same-complex or paralog relationship.  Primary cilium membership is a valid
  way to select comparators, but it does not guarantee an interchangeable
  Perturb-seq profile.
- Several canonical `Sdccag8` neighbors were not available as focal training
  perturbations, including `Ofd1`, `Arl13b`, `Pde6d`, `Mks1`, and many core
  `Bbs` genes.  `B9d2` and some MKS module members were also missing from the
  Perturb-seq target universe.
- snRNA-seq does not observe ciliary length, receptor localization, Hedgehog
  reporter activity, kidney/retina phenotypes, olfactory epithelium, ependymal
  cells, or the embryonic radial-migration window where `Sdccag8` has published
  roles.  A zero prediction means no stable focal nuclear RNA genes pass the
  Wilcoxon BH 0.05 threshold, not that `Sdccag8` is unimportant.
- Average RNA knockdown in the experiment was partial and DNA editing was not
  measured per nucleus, so a flat signature cannot distinguish full biological
  buffering from insufficient protein loss.  I nevertheless used the same
  assumption consistently across the flat ciliary comparators because their
  direct counts were observed under the identical platform.
