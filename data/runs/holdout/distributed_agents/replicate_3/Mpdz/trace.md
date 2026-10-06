# DEG-count prediction for held-out `Mpdz`

## Question interpreted

The requested held-out perturbation list contains one mouse target, `Mpdz`.  I interpreted the task as a point prediction of the number of genes that would satisfy `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` cell group after sparse postnatal AAV-CRISPR loss of `Mpdz`.

Two experimental details drove the calibration:

- `n_degs` is an empirical whole-transcriptome Wilcoxon/BH count from this assay, not a generic estimate of whether the gene is biologically important.
- The focal data are NeuN-enriched postmitotic neurons. MPDZ phenotypes at epithelia, choroid plexus, and ependyma are informative about MPDZ function but are imperfect guides for this neuronal readout.

## Sources used

- Same-experiment DE matrix: `[local file: training_de_all_cell_groups.parquet]`.
- Same-cell training endpoints: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Requested-target manifest: `[local file: 139_Mpdz.csv]`.
- Distributed Agents corpus MCP, release `perturbai-july-260713-sourceguard-1773-v1`. `target_context(Mpdz)` returned `target_found=false`, so there were no internal MPDZ claims or neighbor findings to use.
- PubMed literature on MUPP1/MPDZ:
  - Ullmer et al. 1998, FEBS Letters, DOI `10.1016/s0014-5793(98)00141-0`: cloned MUPP1/MPDZ, a scaffold with 13 PDZ domains and brain expression.
  - Becamel et al. 2001, J. Biol. Chem., DOI `10.1074/jbc.M008089200`: the 5-HT2C receptor C terminus binds MPDZ/MUPP1 PDZ10 and MUPP1 is expressed in cortex, hippocampus, dentate granule cells, and choroid plexus.
  - Balasubramanian et al. 2006, J. Biol. Chem., DOI `10.1074/jbc.M607695200`: GABABR2 binds MUPP1 and this scaffold interaction affects receptor stability and signaling.
  - Krapivinsky et al. 2004, Neuron, DOI `10.1016/j.neuron.2004.08.003`, and Rama et al. 2008, Mol. Cell. Neurosci., DOI `10.1016/j.mcn.2008.02.007`: MUPP1 can assemble SynGAP and CaMKII near NMDAR-containing excitatory synapses.
  - Fujita et al. 2012, J. Neurochem., DOI `10.1111/jnc.12022`: CADM1, MUPP1, and GABBR2 form a synaptic complex in cerebellar Purkinje-cell dendrites and cultured hippocampal neurons.
  - Tanabe et al. 2015, J. Neurochem., DOI `10.1111/jnc.13168`: CASPR2/CNTNAP2 forms a complex with GPR37 through MUPP1 in mouse brain and hippocampal neurons.
  - Feldner et al. 2017, EMBO Mol. Med., DOI `10.15252/emmm.201606430`, and Yang et al. 2019, EMBO Mol. Med., DOI `10.15252/emmm.201809540`: MPDZ loss causes hydrocephalus by disrupting ependymal or choroid-plexus epithelial barrier biology.

## Same-experiment computations

I loaded the manifest and confirmed that the only requested held-out target was `Mpdz`. I then loaded the focal-cell training count CSV and used the parquet filtered to `group_name == "151 TH Prkcd Grin2c Glut"` to inspect mechanistically related training perturbations.

The relevant code pattern was:

```python
counts = pd.read_csv("151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv")
df = pd.read_parquet(
    "training_de_all_cell_groups.parquet",
    filters=[("group_name", "==", "151 TH Prkcd Grin2c Glut"),
             ("gene_target", "in", candidate_genes)],
)
observed_n_degs = (
    df.assign(sig=df.pvals_adj < 0.05)
      .groupby("gene_target")["sig"]
      .sum()
)
```

I also used the Distributed Agents runtime `profile_compare` and `profile_cohort` tools to compare signed focal-cell log-fold-change profiles among the same candidate perturbations. The cohort contained MPDZ-relevant postsynaptic scaffolds, receptors, adhesion genes, and downstream signal proteins: `Dlg4`, `Dlgap4`, `Shank2`, `Shank3`, `Homer2`, `Magi2`, `Gabbr1`, `Gabbr2`, `Htr2a`, `Htr2b`, `Htr2c`, `Syngap1`, `Camk2a`, `Camk2b`, `Cntnap2`, `Cadm2`, `Nrxn1`, `Nlgn3`, `Arhgef9`, `Grin1`, and `Grin2b`.

## Within-dataset analogs and counterexamples

MPDZ is a large multi-PDZ scaffold rather than a DNA-, RNA-, ribosome-, proteasome-, or metabolic-core regulator. The highest-count perturbations in this cell group were instead broad housekeeping or transcriptional perturbations such as `Uba5` with 2677 DEGs, `Tpr` with 1768, `Sin3a` with 1433, `Rnpc3` with 868, `Zbtb7a` with 841, `U2af2` with 828, and `Psmb4` with 742. I treated these as poor analogs.

The appropriate same-experiment neighborhood was tightly centered near synaptic scaffolding and receptor complexes:

| training target | `n_degs` | pattern evidence and relevance |
|---|---:|---|
| `Magi2` | 0 | Multi-PDZ synaptic scaffold; no adjusted-significant genes. Good scaffold counterexample. |
| `Dlg4` | 1 | PSD-95/MAGUK scaffold; the only significant row was `Dlg4` itself. Good postsynaptic-scaffold analog. |
| `Dlgap4` | 2 | PSD scaffold; significant rows were `Dlgap4` and `Vgf`. Low-breadth scaffold analog. |
| `Shank2` | 0 | Postsynaptic scaffold; no significant rows. Good counterexample. |
| `Shank3` | 2 | Postsynaptic scaffold; `Shank3` and one additional row (`Uba5`) were significant. Low-breadth scaffold analog. |
| `Homer2` | 0 | Postsynaptic density scaffold and mGluR adaptor; no significant rows. Good counterexample. |
| `Syngap1` | 0 | Reported MUPP1 synaptic signaling partner; no significant rows despite target knockdown trending (`Syngap1`, adjusted p `0.117`). |
| `Camk2a` | 0 | CaMKII family member in the MUPP1/SynGAP/CaMKII axis; no significant rows. |
| `Camk2b` | 1 | CaMKII family member; only `Camk2b` itself was significant. |
| `Gabbr1` | 1 | GABAB receptor subunit, functionally adjacent to the GABBR2-MUPP1 complex; only `Gabbr1` itself was significant. |
| `Gabbr2` | 1 | Direct reported MUPP1 binding receptor subunit; only `Gabbr2` itself was significant. |
| `Htr2a`, `Htr2b`, `Htr2c` | 0, 0, 0 | 5-HT2 receptors share PDZ-tail biology with the reported 5-HT2C-MUPP1 interaction; none produced any significant gene. |
| `Cntnap2` | 1 | CASPR2 can complex with GPR37 through MUPP1; only `Cntnap2` itself was significant. |
| `Cadm2` | 1 | CADM-family synaptic adhesion comparator to CADM1-MUPP1 complexes; only `Cadm2` itself was significant. |
| `Nrxn1`, `Nlgn3` | 1, 1 | Synaptic adhesion molecules bracketing postsynaptic organization; each produced only its own target transcript as significant. |
| `Grin2b` | 2 | NMDAR subunit downstream of MUPP1/SynGAP/CaMKII synapse biology; only two DEGs. |
| `Grin1` | 89 | Direct perturbation of the obligatory NMDAR subunit gave a broader activity-related response. I used it as an upper counterexample rather than as a pooled scaffold analog. |

Thus, the close scaffold/adhesion/receptor analogs, excluding the `Grin1` core-receptor counterexample, were concentrated between 0 and 2 DEGs: 8 of 20 were zero, 9 of 20 had one DEG, and 3 of 20 had two DEGs. The runtime profile comparison also did not reveal a robust shared MPDZ-like transcriptional module among these genes: most adjusted-significant effects were the perturbed transcript itself, and leading-tail overlap came mostly from weak, non-significant tails.

I also verified that `Mpdz` was present as a measured gene in the focal-cell parquet for every non-held-out perturbation. Across the 1674 training perturbations, the `Mpdz` row had median log2 fold change close to zero (`-0.0039`) and only three adjusted-significant shifts, each under broad regulators (`Phf12`, `Rnpc3`, `Psmb4`). This supports the idea that `Mpdz` is assay-measurable but not part of a frequently moving broad response program.

## Target-specific prediction for `Mpdz`

External biology puts MPDZ in receptor and junction scaffolding, not in direct transcriptional control. Its strongest complete-loss phenotypes are epithelial-barrier phenotypes in ependyma and choroid plexus, which are largely outside a NeuN-enriched postmitotic neuronal snRNA-seq sample. In neurons, the reported MUPP1 interactions with GABABR2, 5-HT2C, SynGAP/CaMKII, CADM1, and CASPR2/GPR37 are consistent with synaptic localization and signaling regulation, but perturbing neighboring scaffold, receptor, and adhesion genes in the same experiment almost never generated a multi-gene FDR-significant transcriptional state in `151 TH Prkcd Grin2c Glut` cells.

The zero/nonzero decision is therefore mostly an on-target-expression decision. I expect little or no trans response, but `Mpdz` is a detected transcript in the focal cell group and its large brain-expressed mRNA should usually be detectable as the directly targeted row if the AAV-CRISPR guides reduce the transcript. The best point estimate is consequently one FDR-significant gene rather than a broad response.

Predicted `n_degs` for `Mpdz`: **1**.

## Limits

This is an extrapolation from scaffold neighbors rather than a direct within-dataset MPDZ signature; the MPDZ perturbation itself is absent from the DE parquet and training endpoint CSV by design, and the Distributed Agents corpus release had no MPDZ node. The closest biochemical partners `Gpr37`, `Cadm1`, `Cadm4`, `Gjd2`, and `MPP5/PALS1` were not available as training perturbations, so I had to use adjacent receptors and scaffolds. Finally, distinguishing 0 from 1 DEG depends on guide activity, target-cell `Mpdz` expression, and power for the single self-transcript row; the dataset supports a very small count but cannot guarantee that the MPDZ self row crosses BH FDR 0.05.
