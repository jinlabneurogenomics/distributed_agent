# DEG-count prediction trace

## Question and interpretation

The requested held-out perturbation is `Smpd3`, and the target cell group is `151 TH Prkcd Grin2c Glut`. I interpreted the task as a point prediction for the exact number of measured genes with `pvals_adj < 0.05` after acute AAV-PHP.eB CRISPR loss of the target in this focal thalamic glutamatergic class.

The main ambiguity was whether a self-transcript count should be included. The endpoint says "measured genes", and the supplied training CSV agrees with a literal interpretation: several focal one-DEG lipid/lysosomal perturbations have exactly their own target RNA as the lone FDR-significant gene. I therefore treated a target-RNA decrease as eligible for `n_degs`, while reasoning about it separately from downstream pathway genes.

## Sources

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: focal training endpoint for 1,674 non-held-out targets.
- `[local file: training_de_all_cell_groups.parquet]`: per-gene DE statistics used to verify whether focal counts for sphingolipid and lysosomal comparators were self-transcript-only or broader expression states.
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`: packaged Findings and Claims derived from the same PerturbAI atlas. This release had no `Smpd3` Finding or Claim, so I used it only for represented comparator targets.
- PubMed literature for Smpd3/nSMase2 mechanism:
  - Trajkovic et al. 2008, Science, DOI `10.1126/science.1153124`, PMID `18309083`: neutral sphingomyelinase-sensitive ceramide generation supports ESCRT-independent exosome budding.
  - Wheeler et al. 2009, Journal of Neurochemistry, DOI `10.1111/j.1471-4159.2009.06038.x`, PMID `19476542`: nSMase2-dependent ceramide regulates TNF-alpha-induced NMDA receptor trafficking and synaptic plasticity.
  - Tabatadze et al. 2010, Journal of Neuroscience Research, DOI `10.1002/jnr.22438`, PMID `20629193`: inhibiting nSMase2 perturbs mouse brain sphingolipids, glutamate receptor composition, and memory.
  - Dinkins et al. 2016, Journal of Neuroscience, DOI `10.1523/JNEUROSCI.1429-16.2016`, PMID `27535912`: nSMase2 deficiency reduces ceramide-enriched exosome output and AD pathology in 5XFAD mice.
  - Tohumeken et al. 2023, Neurobiology of Disease, DOI `10.1016/j.nbd.2023.105987`, PMID `36603748`: pyramidal-neuron nSMase2 deletion reduces amyloid deposition in APP/PS1 mice.
  - Zhu et al. 2024, Genes, Brain and Behavior, DOI `10.1111/gbb.12911`, PMID `39171374`: middle-aged `fro/fro` nSMase2-deficient whole mouse brains have many steady-state RNA abundance changes, showing that the enzyme can matter transcriptionally in chronic whole-brain settings.

## Computation over the supplied data

I first summarized the focal training endpoint. The distribution was highly sparse: 1,205 of 1,674 training targets had `n_degs = 0`, the median was 0, the 75th percentile was 1, and only 43 targets had at least 100 DEGs.

Then I filtered the parquet to the focal class and to biologically relevant represented sphingolipid, S1P, ceramide-transfer, ganglioside, and lysosomal comparator perturbations. The key operation was:

```python
import pyarrow.compute as pc
import pyarrow.dataset as ds

dataset = ds.dataset(PARQUET, format="parquet")
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut")
    & pc.field("gene_target").isin(analogs)
)
df = dataset.to_table(
    columns=[
        "names",
        "scores",
        "logfoldchanges",
        "pvals",
        "pvals_adj",
        "gene_target",
        "n_pert_matched",
        "n_ctrl_matched",
    ],
    filter=filt,
).to_pandas()
```

For each analog I counted rows with `pvals_adj < 0.05` and inspected the lowest adjusted p-values to decide whether any positive count was a real downstream expression state or only the perturbed transcript itself.

## Smpd3-specific reasoning

`Smpd3` encodes neutral sphingomyelinase 2, which hydrolyzes sphingomyelin to ceramide at membranes. That makes it biochemically connected to ceramide/S1P flux and to ceramide-dependent extracellular-vesicle biogenesis, and the literature supports effects on glutamate receptor trafficking and disease-context EV release. However, those roles are mostly lipid-local, synaptic, EV, or injury/disease effects. They do not imply a large basal nuclear RNA program after partial sparse knockout in recovered juvenile neurons.

Training perturbations that constrain the expected Smpd3 count:

| Training target | Focal `n_degs` | Expression-pattern evidence in `151 TH Prkcd Grin2c Glut` | Why it is informative |
| --- | ---: | --- | --- |
| `Asah1` | 0 | No gene reached FDR 0.05; the smallest adjusted p-value was 1.0, and the `Asah1` self row had log2FC -0.273 with adjusted p = 1.0. Distributed Agents `Asah1:F001-F003` report 0 downstream FDR 0.10 genes in all recovered neuronal classes and no meaningful score-vector neighbor. | Acid ceramidase is a lysosomal ceramide-metabolism node. Its absence of a lysosomal or ceramide-storage RNA response is a direct counterexample to expecting every ceramide enzyme to trigger a transcriptomic stress program. |
| `Sphk1` | 0 | No focal FDR 0.05 hit; the leading row was `Vps45`, adjusted p = 0.375, and the self row was non-significant. Distributed Agents `Sphk1:F001-F003` describe a screen-wide neuronal null and no convergence with `Asah1`, `Cert1`, `Sptlc2`, `S1pr2`, or `St3gal5`. | SphK1 consumes sphingosine to make S1P. It samples the downstream S1P arm that might respond to altered ceramide/sphingosine balance after Smpd3 loss. |
| `Sptlc2` | 1 | The only focal FDR 0.05 hit was `Sptlc2` itself, log2FC -0.685, adjusted p = 1.45e-4; the next row, `Kcnc2`, had adjusted p = 0.118. Distributed Agents `Sptlc2:F002-F005` specifically note that TH Prkcd Grin2c neurons had target-RNA depletion but no downstream FDR 0.10 genes and that ER-stress, ISR, autophagy, and sphingolipid-compensation genes were absent. | SPTLC2 is upstream in de novo sphingolipid synthesis. It is not the same reaction as Smpd3, but it tests whether lowering sphingolipid flux is visible as a neuronal RNA stress program. |
| `Cert1` | 0 | No focal FDR 0.05 hit; the self row had raw p = 1.4e-5 but adjusted p = 0.248. Distributed Agents `Cert1:F001-F004` report no downstream FDR 0.10 transcriptional response in any recovered neuronal group. | CERT transfers ceramide from ER to Golgi. It is a close ceramide-handling counterexample in which even an on-target-looking raw self decrease did not survive focal multiple testing. |
| `S1pr2` | 0 | No focal FDR 0.05 hit; all inspected rows had adjusted p = 1.0. Distributed Agents `S1pr2:F001-F004` call `S1pr2` pan-neuronally null in this screen. | It tests whether the S1P receptor arm generated by sphingosine kinase signaling produces a stable RNA state in basal neurons. |
| `St3gal5` | 1 | The only focal FDR 0.05 hit was `St3gal5` itself, log2FC -0.788, adjusted p = 1.96e-14; the next row had adjusted p = 1.0. Distributed Agents `St3gal5:F001-F005` show only a single non-self hit elsewhere, `Pggt1b` in `155 MB Glut`, with no canonical ganglioside or stress program. | GM3 synthase is farther downstream in glycosphingolipid production. Its self-only focal response supports the idea that membrane-sphingolipid perturbations can be biochemically real but almost invisible by snRNA-seq. |
| `Psap` | 1 | The only focal FDR 0.05 hit was `Psap` itself, log2FC -1.277, adjusted p = 1.70e-28; every non-self row had adjusted p = 1.0. Distributed Agents `Psap:F001-F004` describe a pure on-target signal with no downstream FDR 0.10 genes in any measured neuronal group. | PSAP is needed for lysosomal sphingolipid hydrolases and is a strong lysosomal sphingolipid-loss control. |
| `Lamp2` | 0 | No focal FDR 0.05 hit. `Lamp2` and `Ppm1g` nearly reached the cutoff at adjusted p = 0.0537 and 0.0545, respectively, but still did not count at the requested threshold. Distributed Agents `Lamp2:F002` reports no broad lysosome, autophagy, proteasome, UPR/ISR, or redox program. | A lysosome/autophagy counterexample showing the assay could get close to isolated hits without a pathway-wide state. |
| `Scarb2` | 1 | The only focal FDR 0.05 hit was `Scarb2` itself, log2FC -0.811, adjusted p = 0.00246. Distributed Agents `Scarb2:F001-F005` find only one downstream FDR 0.10 gene in the entire neuronal surface. | LIMP-2 is a lysosomal membrane disease gene, included as a broader lipid/lysosome comparator. |
| `Atp13a2` | 1 | The only focal FDR 0.05 hit was `Atp13a2` itself, log2FC -0.613, adjusted p = 2.23e-21. Distributed Agents `Atp13a2:F001-F005` report no non-self corrected downstream response in any recovered neuronal class. | A lysosomal/autophagy Parkinsonism-linked counterexample; its flat profile argues that strong self knockdown can coexist with zero downstream RNA response. |
| `Ctsb` | 1 | The only focal FDR 0.05 hit was `Ctsb` itself, log2FC -1.480, adjusted p = 8.54e-43. Distributed Agents `Ctsb:F001-F004` call this a target-only surface with no canonical lysosomal, autophagy, CLEAR, or stress response. | A positive self-transcript control for a lysosomal hydrolase with no downstream state. |
| `Gaa` | 1 | The only focal FDR 0.05 hit was `Gaa` itself, log2FC -0.709, adjusted p = 8.97e-16. Distributed Agents `Gaa:F001-F005` describe a pan-neuronal downstream-flat perturbation. | Another lysosomal enzyme counterexample where a measurable own-transcript decrease was transcriptionally buffered. |
| `Ppt1` | 1 | The only focal FDR 0.05 hit was `Ppt1` itself, log2FC -0.536, adjusted p = 1.3e-5. Distributed Agents `Ppt1:F001-F004` report zero non-self FDR 0.10 genes in all 23 neuronal groups. | A neuronal ceroid lipofuscinosis lysosomal enzyme; useful because even a severe neuronal disease gene lacked an acute postnatal RNA program here. |
| `Stard7` | 0 | No focal FDR 0.05 hit; all inspected rows had adjusted p = 1.0. Distributed Agents `Stard7:F001-F006` found only one FDR 0.10 gene in all recovered classes and no general lipid-transfer program. | A lipid-transfer counterexample to a generic lipid-organelle stress prediction. |

### Decision

The dataset-local evidence is the main driver of the prediction. The represented sphingolipid comparators do not form a shared multi-gene neuronal module in this assay, and the closest biochemical nodes in the focal class are either exact zeros (`Asah1`, `Sphk1`, `Cert1`, `S1pr2`) or one-DEG self-transcript-only profiles (`Sptlc2`, `St3gal5`, `Psap`). The lysosomal comparators reinforce the same point: multiple disease-relevant hydrolases had strong own-transcript loss without any non-self focal hit.

External biology increases confidence that Smpd3 is a real neuronal lipid/signaling enzyme, but much of the published signal comes from acute cytokine stimulation, A-beta/tau disease models, choroid plexus or glial EV release, and germline or chronic `fro/fro` deficiency. Those conditions differ from partial P16 sparse CRISPR in otherwise basal postmitotic neurons. I therefore predicted that `Smpd3` loss will not induce a non-self transcriptomic state by FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

The remaining issue is the self-transcript. `Smpd3` is in the focal measured-gene universe, and some similarly sparse pathway perturbations count exactly their own transcript. I still chose `0` rather than `1` because the more nonlysosomal ceramide/S1P comparators most similar to Smpd3's signaling role, `Asah1`, `Sphk1`, `Cert1`, `S1pr2`, and `Stard7`, were all focal zeros, and because this endpoint's target-RNA detection is not reliably predicted by gene function alone.

Final prediction: `Smpd3 -> 0`.

## Limits

- `Smpd3` itself is completely held out from both supplied DE surfaces, and the Distributed Agents corpus release has no Smpd3 report, so there is no same-experiment Smpd3 signature or curated same-experiment analog set.
- The represented training set lacks the direct neutral sphingomyelinase paralogs `Smpd1`, `Smpd2`, and `Smpd4`; all sphingolipid comparisons are pathway-near rather than same-complex or same-enzyme-family controls.
- The count could be off by one if `Smpd3` RNA itself is efficiently reduced and clears BH correction. The within-dataset evidence is much stronger for "no downstream genes" than for the self-transcript call.
- PubMed evidence for Smpd3 in A-beta, tau, obesity, cytokine, or germline settings may not transfer to sparse juvenile neuronal loss of function. Conversely, the assay could miss lipid, receptor-trafficking, exosome, or survival effects that do not appear as nuclear RNA changes in recovered cells.
