# Prediction trace

## Question and resolved ambiguities

The manifest for this run contains a single held-out target, `Ap3b2`. I interpreted the requested endpoint as the exact count, in `151 TH Prkcd Grin2c Glut`, of measured genes whose Wilcoxon differential-expression test has `pvals_adj < 0.05` after perturbing `Ap3b2` by the same acute mosaic AAV-CRISPR design used in the training screen. The target was absent from both supplied inputs as a perturbation, so I did not use any `Ap3b2` perturbation signature or held-out DEG count.

## Sources used

- Local manifest: `[local file: 014_Ap3b2.csv]`.
- Focal-cell training counts: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Local all-cell differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`, for same-screen interpretations around `Ap3b1`, `Dtnbp1`, AP-family adaptors, clathrin/endosomal targets, and presynaptic release targets.
- Distributed Agents runtime profile tools, using Wilcoxon `scores` as signed profiles and `pvals_adj < 0.05` as the significant-feature call.
- NCBI PubMed E-utilities for external literature on AP-3 and neuronal beta3B/AP3B2 biology.

Key external papers were:

- Faundez and Kelly 2000, DOI `10.1091/mbc.11.8.2591` / PMID 10930456: AP-3 participates in endosomal synaptic-vesicle biogenesis and phosphorylation of AP-3 beta subunits is linked to synaptic-vesicle coat assembly.
- Seong et al. 2004, DOI `10.1091/mbc.e04-10-0892` / PMID 15537701: mouse beta3A- and beta3B-containing AP-3 complexes have distinct neuronal localization and synaptic-vesicle cargo effects; beta3B deficiency compromises synaptic zinc stores and ZnT3/ClC-3 targeting.
- Newell-Litwa et al. 2009, DOI `10.1091/mbc.e08-05-0456` / PMID 19144828: AP-3 and BLOC-1 route lysosomal and synaptic-vesicle cargoes from shared early endosomes and `Ap3b1`, BLOC-1, and `Ap3b2` mutants alter synaptic-vesicle protein composition.
- Evstratova et al. 2014, DOI `10.1038/ncomms6530` / PMID 25410111: AP-3b2 knockout reduces AP-3-dependent asynchronous neurotransmitter release and affects information transfer.

## Computational evidence

I first verified the run scope:

- Requested target order: `Ap3b2`.
- Training perturbations in the focal count file: 1,674.
- Focal `n_degs` distribution among training targets: median 0, 75th percentile 1, 90th percentile 2, 95th percentile 18, 99th percentile 436.48, maximum 2,677.

For mechanistic candidates I filtered the parquet to the focal cell type and selected exact perturbation names:

```python
filt = (
    (pc.field("group_name") == "151 TH Prkcd Grin2c Glut") &
    pc.field("gene_target").isin(candidate_targets)
)
```

Each selected perturbation had 17,259 measured feature rows in the focal group. I used the focal count CSV for the exact training `n_degs`, and the parquet rows to check significant genes, minimum adjusted p-values, and perturbed/control nuclei. Separately, the Distributed Agents runtime `profile_compare` call computed complete pairwise Pearson/cosine similarities over the focal Wilcoxon-score vectors for a 22-gene cohort containing AP-3/BLOC, AP-family, endolysosomal, Rab, clathrin/endocytic, and presynaptic-vesicle controls.

## Target-specific reasoning

### `Ap3b2`

`Ap3b2` encodes the neuronal AP-3 beta3B subunit. Beta3B-containing AP-3 is not a generic stress or transcription factor: it is an endosomal adaptor for synaptic-vesicle and lysosome-related-organelle cargo sorting. Germline loss changes synaptic-vesicle protein composition, synaptic zinc stores, and asynchronous release, especially at protein-localization/electrophysiology layers. Those phenotypes made AP-3/BLOC and presynaptic vesicle genes the most relevant in-dataset analogs, with late endosome or clathrin disruption used as counterexamples where the screen can see broader trafficking stress.

Biologically relevant training perturbations in `151 TH Prkcd Grin2c Glut` were:

| training perturbation | focal `n_degs` | focal expression-pattern evidence | relevance for `Ap3b2` |
|---|---:|---|---|
| `Ap3b1` | 0 | 17,259 measured genes, min adjusted p = 1.0; no FDR hits. `Ap3b1` vs `Dtnbp1` Pearson -0.012 / cosine -0.016 and `Ap3b1` vs `Slc32a1` Pearson 0.024 / cosine 0.020, so the zero endpoint was not hiding a shared subthreshold AP-3 signature. | Closest represented AP-3 complex member. It is the ubiquitous beta3A subunit rather than the neuronal beta3B subunit, but it tests whether AP-3 cargo mis-sorting itself launches a nuclear RNA program in the assay. |
| `Dtnbp1` | 0 | 17,259 genes, min adjusted p = 1.0; no FDR hits; no positive or negative significant intersections with the AP-family/Rab comparators inspected. | BLOC-1/AP-3 cargo-routing partner. Distributed Agents summarized `Ap3b1` and `Dtnbp1` as a shared buffered juvenile neuronal transcriptomic outcome. |
| `Slc32a1` | 0 | 17,259 genes, min adjusted p = 1.0. | AP-3/BLOC-adjacent vesicular GABA transporter biology; useful as a synaptic-vesicle cargo/release-adjacent null, although the focal group is glutamatergic rather than GABAergic. |
| `Ap1b1`, `Ap1s2`, `Ap4s1` | 1, 0, 0 | `Ap1b1` had only its own transcript as an FDR hit; `Ap1s2` min adjusted p = 0.394 and `Ap4s1` min adjusted p = 1.0. | Other AP adaptor complexes were flat or near flat. The Distributed Agents AP-family claim specifically warned that represented AP-adaptor perturbations were target-specific rather than a generic AP-family/clathrin transcriptional signature. |
| `Rab7` | 501 | Broad positive/negative response; 311 positive and 190 negative significant genes in the runtime profile. | Boundary case. Rab7/HOPS late-endosome/lysosome blockade is transcriptionally visible in the same cell type, so the AP-3 null is not a blanket inability to detect membrane-traffic perturbations. |
| `Vps35`, `Vps41`, `Becn1`, `Atp6v1a` | 17, 0, 0, 0 | `Vps35` had a small 17-gene signature; `Vps41`, `Becn1`, and `Atp6v1a` were zero in this focal cell group. | Endosome/lysosome/autophagy controls. `Ap3b1` was reported by Distributed Agents as uncoupled from the Rab7-HOPS axis: cargo selection was separable from terminal lysosomal failure programs. |
| `Cltc`, `Dnm1`, `Synj1` | 3, 1, 1 | `Cltc` had 3 FDR hits; `Dnm1` and `Synj1` were singleton responses dominated by the target transcript. Whole-profile correlations with `Ap3b1` were tiny: Ap3b1-Cltc -0.013, Ap3b1-Dnm1 0.017, Ap3b1-Synj1 -0.036. | Clathrin and synaptic-vesicle endocytosis are adjacent to AP-3 function, but direct disruption of these nodes did not produce a broad shared nuclear module. |
| `Stxbp1`, `Sv2a`, `Syp`, `Vamp1` | 1, 1, 1, 1 | Singleton FDR calls in this focal group, each dominated by the target self-transcript. | Presynaptic release/synaptic-vesicle controls. They support the same pattern: strong vesicle physiology can remain nearly transcriptionally silent at the soma under this P16 sparse CRISPR assay. |
| `Rab27a`, `Rab18`, `Rab3gap1`, `Rab3gap2` | 0, 0, 0, 0 | All zero in the focal count file. Runtime score correlations from the AP-3/BLOC zero nodes to these Rab/exocytosis controls were all at near-null magnitude. | Rab secretory-vesicle controls; rejected as evidence for a broad vesicle-release response. |

I therefore predicted `Ap3b2` as non-detectable rather than merely low. The positive argument for a nonzero call is that beta3B is the neuron-specific AP-3 beta isoform and germline `Ap3b2` loss has clearer synaptic phenotypes than beta3A loss. The stronger same-assay argument goes the other way: the one represented AP-3 beta subunit, the BLOC-1 comparator, and most synaptic-vesicle/Rab controls had 0 or only a self-transcript singleton, while the true broad trafficking responder `Rab7` looked very different. Because `n_degs` is FDR-gated and the nearest AP-3/BLOC perturbations did not even give reproducible cargo-gene mRNA or target-transcript hits in this focal group, the best point prediction is:

```text
Ap3b2 -> 0 DEGs
```

## Limits

The main extrapolation is from `Ap3b1`/`Dtnbp1` to `Ap3b2`; `Ap3b2` itself, AP-3 `delta`/`mu`/`sigma` subunits, and many BLOC-1 subunits were absent from the perturbation-training universe. `Ap3b1` was recovered with only 85 matched perturbed nuclei in the focal group, so it is an imperfect power match for `Ap3b2`. The external AP-3B literature is dominated by germline knockouts, synaptic protein localization, and electrophysiology, none of which is the same as a sparse P16 AAV-CRISPR snRNA-seq response 3-4 weeks later. Finally, a target-self hit remains possible if the held-out `Ap3b2` guide set happened to deplete its transcript more strongly than the AP-3/BLOC analogs; I chose 0 because the nearest functional perturbations were all below the FDR threshold in this focal RNA readout.
