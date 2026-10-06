# Pdss2 DEG-count prediction

## Question and resolved ambiguities

The held-out target list for this run contains one perturbation, `Pdss2`.  I
interpreted the requested value as the focal-cell endpoint in the supplied
training-count table: the number of genes with `pvals_adj < 0.05` in `151 TH
Prkcd Grin2c Glut`, counting the perturbed target itself if its own transcript
passes FDR.  `Pdss2` is absent from both the all-cell differential-expression
parquet and the focal-cell training count CSV, so no `Pdss2` expression
signature or focal DEG count was used.

## Sources used

- Input data:
  - `training_de_all_cell_groups.parquet`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"` for focal signatures.
  - `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv` for observed training `n_degs`.
  - `174_Pdss2.csv` for the exact held-out target order.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`:
  - `target_context("Pdss2")` found no direct corpus node for the held-out target.
  - `target_context("Coq5")` and `resolve_evidence("Coq5", F001/F003)` gave curated same-assay evidence that `Coq5`, the only direct CoQ-biosynthesis training perturbation, was transcriptionally buffered.
  - `candidate_set_topology` was used only as an audit that the nominated `Coq5`, ETC, and mitochondrial-stress comparators were connected by explicit same-assay reports; those edges were read as report links, not as positive convergence.
- External biology:
  - MitoCarta3.0 for mitochondrial localization/pathway membership of PDSS2/COQ genes: Rath et al. 2021, Nucleic Acids Research, DOI `10.1093/nar/gkaa1011`.
  - GeneReviews, *Primary Coenzyme Q10 Deficiency Overview*, Salviati, Trevisson and Agosto, updated 2023, for the PDSS/COQ primary CoQ10-deficiency gene set.
  - PDSS2 with PDSS1 synthesizes the CoQ polyisoprenyl tail: Saiki et al. 2008, American Journal of Physiology-Renal Physiology, DOI `10.1152/ajprenal.90445.2008`, PMID `18784258`.
  - The `Pdss2(kd/kd)` mouse is a CoQ-deficiency model with strong tissue thresholds; glomerular podocytes are sensitive while some other tissues tolerate severe CoQ depletion: Peng et al. 2008, PLoS Genetics, DOI `10.1371/journal.pgen.1000061`, PMID `18437205`.
  - CoQ deficiency can impair sulfide oxidation in a residual-CoQ-level and tissue-dependent way, with affected kidney but relatively spared brain in `Pdss2(kd/kd)`: Ziosi et al. 2017, EMBO Molecular Medicine, DOI `10.15252/emmm.201606356`, PMID `27856618`.
  - `COQ5` is the mitochondrial C-methyltransferase in CoQ biosynthesis and acts within the COQ protein complex: Nguyen et al. 2014, Biochimica et Biophysica Acta, DOI `10.1016/j.bbalip.2014.08.007`; Malicdan et al. 2017, Human Mutation, DOI `10.1002/humu.23345`, PMID `29044765`.
  - Primary CoQ10 biosynthesis disorders include PDSS1, PDSS2, COQ2, COQ4, COQ5, COQ6, COQ7, COQ8A, COQ8B, COQ9 and HPDL: Munch et al. 2023, Antioxidants, DOI `10.3390/antiox12030718`, PMID `36978966`.

## Dataset computations

I first loaded the focal training counts to calibrate scale.  The focal endpoint
is highly zero-inflated: `1205 / 1674` training perturbations have zero DEGs,
the median is `0`, the 75th percentile is `1`, and only the largest few
signatures reach hundreds or thousands of DEGs.

I then selected mechanistic comparators by pathway rather than by symbol alone:

- direct CoQ synthesis: `Coq5`
- ubiquinone-linked complex III components: `Uqcrfs1`, `Uqcrc2`, `Cyc1`, `Uqcrb`, `Uqcrh`, `Uqcrq`
- complex I / complex II entries that feed the CoQ pool: `Ndufs2`, `Ndufc2`, `Ndufv1`, `Ndufa4`, `Sdha`
- mitochondrial-stress counterexamples used by the Distributed Agents corpus: `Clpp`, `Lonp1`, `Opa1`

The direct CoQ synthome was almost unrepresented in the training universe.
Searching the focal training targets for `Coq%`, `Pdss%`, and `Adck%` returned
`Coq5` only; closer genes such as `Pdss1`, `Coq2`, `Coq4`, `Coq6`, `Coq7`,
`Coq8a/Adck3`, `Coq8b/Adck4`, `Coq9`, and `Coq10a/b` were absent.

For focal expression-pattern evidence, I read only the relevant parquet slice:

```python
expr = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(candidate_targets)
)
```

Each selected target had 17,259 measured genes in this cell group and 23,679
matched control nuclei.  The key focal observations were:

| training perturbation | focal `n_degs` | focal expression-pattern evidence | relevance to `Pdss2` |
|---|---:|---|---|
| `Coq5` | 0 | No genes at FDR<0.05 or FDR<0.10; `Coq5` self logFC `-0.473`, adjusted p `1.0`, `n_pert=200`.  The Distributed Agents corpus reports zero FDR<0.10 downstream genes in all 22 measured neuronal groups for `Coq5`, including `151 TH Prkcd Grin2c Glut`. | Closest available same-pathway perturbation.  Both `Coq5` and `Pdss2` act in nuclear-encoded mitochondrial CoQ biosynthesis, although at different enzymatic steps. |
| `Uqcrfs1` | 0 | No FDR<0.05 genes; its own transcript had logFC `-0.340`, adjusted p `0.199`. | Complex III consumes ubiquinol downstream of CoQ production.  Its absence of a broad focal response argues against a generic complex III/CoQ nuclear program. |
| `Uqcrb` | 0 | No FDR<0.05 genes; self logFC `-0.118`, adjusted p `1.0`. | Another complex III component; flat, not a `Pdss2` phenocopy. |
| `Uqcrh` | 0 | No FDR<0.05 genes; self adjusted p `1.0`. | Complex III component; no downstream focal state. |
| `Uqcrc2` | 1 | The sole FDR<0.05 gene was the target transcript, `Uqcrc2`, logFC `-0.576`, adjusted p `0.0030`. | Shows the assay can capture self knockdown for highly detected ETC subunits without generating secondary breadth. |
| `Cyc1` | 1 | The sole FDR<0.05 gene was `Cyc1`, logFC `-0.739`, adjusted p `2.94e-15`. | Same interpretation as `Uqcrc2`; complex III target self only. |
| `Uqcrq` | 1 | One non-target gene, `Gpr180`, passed FDR with adjusted p `0.0429`; `Uqcrq` self adjusted p was `1.0`. | A singleton exception, not a CoQ-biosynthesis-like program. |
| `Ndufs2` | 1 | The sole FDR<0.05 gene was `Ndufs2`, logFC `-0.728`, adjusted p `8.26e-12`. | Complex I feeds the CoQ pool; target self only. |
| `Ndufc2` | 1 | The sole FDR<0.05 gene was `Ndufc2`, logFC `-0.572`, adjusted p `3.27e-05`. | Complex I target self only. |
| `Ndufv1` | 0 | No FDR<0.05 genes; self adjusted p `1.0`. | Complex I flavoprotein; flat in this focal readout. |
| `Ndufa4` | 1 | The sole FDR<0.05 gene was `Ndufa4`, logFC `-0.803`, adjusted p `1.08e-05`. | OXPHOS subunit target self only. |
| `Sdha` | 1 | The sole FDR<0.05 gene was `Sdha`, logFC `-0.781`, adjusted p `2.11e-12`; only one additional gene reached FDR<0.10. | Complex II passes electrons to ubiquinone; again no broad secondary program. |
| `Clpp` | 0 | No FDR<0.05 or FDR<0.10 genes in the focal group. | Mitochondrial protease stress comparator; argues against a constitutive UPRmt/ISR after every mitochondrial perturbation. |
| `Lonp1` | 0 | No FDR<0.05 genes; `Lonp1` self adjusted p `0.507`. | Another mitochondrial protease/stress comparator that is flat in the focal group. |
| `Opa1` | 37 | Broad positive control with `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Mthfd2` and `Opa1` itself among the top focal FDR genes. | A counterexample, not an analog: it demonstrates that this focal group can mount a detectable ATF4/ISR-like mitochondrial-stress signature, so the flat `Coq5`/ETC surfaces are not simply a blind spot of the Wilcoxon pipeline. |

The Distributed Agents `Coq5` report also compared full Wilcoxon score vectors for
`Coq5` against literature-obvious ubiquinone/mitochondrial comparators and
found near-zero matched correlations: `Uqcrfs1 r=0.0169`, `Uqcrc2 r=0.0187`,
`Cyc1 r=0.0077`, `Uqcrb r=0.0031`, `Ndufs2 r=0.0068`, `Ndufc2 r=0.0146`,
`Clpp r=0.0088`, and `Lonp1 r=0.0015`.  Its unbiased scan over 1769 other
targets likewise had only noise-level nearest correlations, with top positive
neighbors near `r=0.03`.  I therefore treated complex I/III membership as a
negative or calibration comparison, not as evidence to borrow a multi-gene
signature for `Pdss2`.

## Target-specific reasoning

### `Pdss2`

`Pdss2` encodes one subunit of the prenyl-diphosphate synthase that works with
PDSS1 to generate the polyisoprenoid tail of mitochondrial coenzyme Q.  CoQ is
biochemically central: it receives electrons from complex I and complex II and
passes them to complex III, and germline or strong loss of PDSS/COQ genes can
cause primary CoQ deficiency with severe kidney and neurologic phenotypes.

That biology alone would be an overstatement for this endpoint.  The readout is
an acute, sparse, postnatal neuronal CRISPR snRNA-seq assay, not a germline
CoQ-depletion model or a metabolite/respiration assay.  In the actual
Perturb-seq data, `Coq5`, the only direct CoQ-biosynthesis perturbation
available for calibration, produced zero focal DEGs and zero FDR<0.10
downstream genes in every measured neuronal group.  It also failed to correlate
with UQCRC/CYC1/NDUF or CLPP/LONP1 signatures, so there is no hidden
subthreshold CoQ-to-OXPHOS or CoQ-to-UPRmt module to transfer.

The electron-transport comparators are consistent with a near-null call.  Some
highly expressed respiratory subunits produced one focal DEG, but that DEG was
usually only the edited subunit itself.  A low-abundance CoQ-biosynthesis gene
such as `Pdss2` is more likely to resemble `Coq5`, `Uqcrfs1`, or `Lonp1`, where
self knockdown remained sub-FDR, than `Cyc1` or `Sdha`, where the mitochondrial
structural mRNA was itself the singleton hit.  `Opa1` proves the focal group can
show an ATF4/ISR-like response, but `Opa1` loss perturbs mitochondrial fusion
and cristae organization and is not a same-complex phenocopy for partial
`Pdss2` loss.

I therefore predict that acute `Pdss2` perturbation will not push any measured
gene below FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

Prediction: `Pdss2 -> 0`.

## Limits

- There is no `Pdss2` node in the internal Distributed Agents corpus and no held-out
  signature in the supplied parquet, so the prediction extrapolates from
  `Coq5` rather than from a direct `Pdss2` measurement.
- `Coq5` acts on the benzoquinone head group while `Pdss2`/`Pdss1` make the
  isoprenoid tail; both affect CoQ biosynthesis, but they are not the same
  enzyme or complex subunit.
- The focal endpoint is an FDR threshold on nuclear snRNA-seq.  A true decrease
  in CoQ abundance, ETC flux, redox buffering, sulfide oxidation, or neuronal
  physiology could occur without yielding any detectable focal DEGs.
- Partial AAV-CRISPR editing in sparse juvenile neurons may remain above the
  tissue-specific threshold for a CoQ-depletion transcriptional stress program,
  especially because Pdss2 mutant mouse work shows strong tissue thresholds
  rather than uniform CoQ-deficiency sensitivity.
