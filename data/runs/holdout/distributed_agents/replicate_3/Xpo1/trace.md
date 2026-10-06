# Question and prediction target

The requested target list for this run contains one held-out perturbation:
`Xpo1`.

I interpreted `n_degs` as the number of assayed genes in `151 TH Prkcd Grin2c
Glut` nuclei with `pvals_adj < 0.05` in the Wilcoxon DE table for a CRISPR loss
of the named target. I treated the endpoint as specific to this assay: P16
AAV-PHP.eB CRISPR in postmitotic mouse brain, harvested at P37-P44, sparse and
mosaic perturbation, 10x Flex V2 snRNA-seq, and Benjamini-Hochberg correction
within the Scanpy `rank_genes_groups` results. The predicted count is therefore
an assay- and power-dependent breadth estimate, not a direct estimate of
viability or biochemical essentiality.

The only ambiguity I resolved was how to use paralogs. I did not treat exportin
family membership alone as sufficient, because `Xpo7` was assayed and was flat
in the focal cell type; I required either direct nuclear-export biology or an
observed focal-cell signature analogous to the RNA-processing/proteostasis
states that a CRM1/XPO1 defect should induce.

# Sources used

- `training_de_all_cell_groups.parquet`: full per-gene DE profiles for training
  perturbations. I loaded the `151 TH Prkcd Grin2c Glut` slice and used
  `logfoldchanges` plus `pvals_adj` for target signatures.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed training
  endpoint. The table had 1,674 targets; 469 were nonzero and the median count
  was 0. Recomputing `sum(pvals_adj < 0.05)` from the focal parquet reproduced
  every supplied count exactly.
- Distributed Agents corpus MCP, release
  `perturbai-july-260713-sourceguard-1773-v1`: no `Xpo1` node was present
  (`target_found=false`, zero claims/findings/references). I therefore used the
  corpus for training comparator genes (`Tpr`, `Thoc1`, `Tnpo3`, `Xpo7`,
  `Ranbp2`) and used the raw matrix for direct focal-cell evidence.
- Distributed Agents runtime profile comparison: I compared `Tpr`, `Tnpo3`, `Thoc1`,
  `Xpo7`, `Ranbp2`, `Kpna3`, `Ddx39b`, the broad spliceosome/RNA-processing
  responders `Rnpc3`, `U2af2`, `Cdc40`, `Prpf6`, `Hnrnpu`, `Yy1`, and the
  proteasome responders `Psmb4` and `Psmc1`. This was a bounded pairwise
  profile calculation over the same focal cell type.
- PubMed literature for mechanisms not already encoded for `Xpo1`: CRM1/XPO1
  exports leucine-rich NES cargo in a RanGTP-dependent way (Fornerod et al.,
  1997, PMID 9323133, DOI 10.1016/s0092-8674(00)80371-2); XPO1 exports many
  proteins and several RNA classes and its inhibition retains cargo such as
  p53, FOXO, NF-kB, and RB-pathway regulators in the nucleus (Azmi et al.,
  2020, PMID 33173198, DOI 10.1038/s41571-020-00442-4); vertebrate ribosomal
  subunit export uses CRM1/XPO1 and the NMD3 adaptor (Thomas and Kutay, 2003,
  PMID 12724356, DOI 10.1242/jcs.00464; Trotta et al., 2003, PMID 12773398,
  DOI 10.1093/emboj/cdg249); partial IPO7 depletion triggers ribosome-biogenesis
  stress and p53 activation, illustrating that karyopherin/ribosome-biogenesis
  imbalance can propagate to transcriptional stress (Golomb et al., 2012, PMID
  22284678, DOI 10.1016/j.molcel.2011.11.022); de novo human XPO1 variants,
  including putative loss-of-function alleles, were recently linked to a
  dominant neurodevelopmental disorder, supporting nervous-system dosage
  sensitivity while not matching the acute postmitotic design here (van
  Oirsouw et al., 2025, PMID 40819229, DOI
  10.1016/j.gim.2025.101555).

# Computational evidence from the focal training data

For each selected comparator I counted significant up- and down-regulated genes
in `151 TH Prkcd Grin2c Glut`; for each pair I intersected their significant
genes and required the same sign of `logfoldchanges` to call a shared
FDR-level feature:

```python
sig_a = rows_a[rows_a.pvals_adj < 0.05]
sig_b = rows_b[rows_b.pvals_adj < 0.05]
shared_same = {
    gene for gene in intersect(sig_a.names, sig_b.names)
    if sign(lfc_a[gene]) == sign(lfc_b[gene])
}
```

Key focal-cell counts and overlaps:

| comparator | focal `n_degs` | up | down | relevance to `Xpo1` |
|---|---:|---:|---:|---|
| `Tpr` | 1768 | 1315 | 453 | nuclear-basket / RNA-export stress; strongest direct in-dataset analog |
| `Tnpo3` | 618 | 305 | 313 | Ran-dependent karyopherin for SR-splicing factors; broad RNA-processing stress |
| `Thoc1` | 303 | 233 | 70 | THO/TREX mRNA export and transcription-coupled RNA processing |
| `Psmb4` | 742 | 357 | 385 | broad proteostasis stress calibration |
| `Psmc1` | 430 | 231 | 199 | second proteasome calibration target |
| `Xpo7` | 0 | 0 | 0 | exportin-family counterexample |
| `Ranbp2` | 0 | 0 | 0 | pore/Ran counterexample in this focal cell type |
| `Kpna3` | 0 | 0 | 0 | nuclear-import counterexample |
| `Ddx39b` | 0 | 0 | 0 | TREX accessory / RNA-export counterexample in this focal cell type |
| `Trp53` | 0 | 0 | 0 | p53 pathway counterexample: XPO1 need not phenocopy p53 loss |
| `Nfkb1` | 0 | 0 | 0 | NF-kB counterexample |

The strongest FDR-level same-direction intersections were:

| pair | shared significant genes | same direction | opposite direction |
|---|---:|---:|---:|
| `Tpr` / `Tnpo3` | 265 | 260 | 5 |
| `Tpr` / `Psmb4` | 261 | 236 | 25 |
| `Psmb4` / `Psmc1` | 215 | 215 | 0 |
| `Tpr` / `Psmc1` | 149 | 136 | 13 |
| `Tpr` / `Thoc1` | 114 | 103 | 11 |
| `Thoc1` / `Psmb4` | 59 | 52 | 7 |
| `Tnpo3` / `Psmc1` | 70 | 66 | 4 |
| `Thoc1` / `Psmc1` | 41 | 37 | 4 |

Whole-vector cosines among a strong and a weak perturbation were often high
because many low-amplitude, non-significant genes move in a shared background.
For example `Tpr` had cosine 0.735 to `Xpo7`, but `Xpo7` contributed no
FDR-significant genes. I therefore used FDR-level same-direction overlaps and
observed DEG counts, not cosine alone, to calibrate the final integer.

# Distributed Agents corpus evidence for in-dataset analogs

`Xpo1` itself was not represented in the Distributed Agents corpus release, so no
same-experiment claim or finding directly transferred from `Xpo1`.

The strongest relevant in-corpus comparator was `Tpr`.

- `Tpr` had 1,768 DEGs in the focal cell type and was called by the corpus as a
  strongly selective perturbation: `151 TH Prkcd Grin2c Glut` and `155 MB Glut`
  accounted for most of the Tpr FDR calls.
- Tpr perturbation recurrently altered nuclear-transport and NXF1-adjacent
  export genes; specifically, Distributed Agents recorded `Ranbp6` and `Xpo1` as
  recurrently up and `Nxf1` as down across several cell groups.
- In the focal data, `Xpo1` itself was one of the most significant `Tpr`
  downstream genes: log2FC = 0.955, adjusted p = 3.20e-14. I treated this as a
  direct sign that the Tpr signature engages nuclear-export compensation,
  while remembering that the edge is Tpr loss -> Xpo1 induction, not Xpo1 loss
  -> Tpr-like output.
- Distributed Agents also reported that Tpr converges with `Psmb4`, `Psmc1`, `Uba5`,
  and `Ufc1`; the focal data supported the same structure with 236 same-sign
  significant genes shared by `Tpr` and `Psmb4`, and 136 shared by `Tpr` and
  `Psmc1`.
- Public literature makes the Tpr comparison mechanistically plausible but not
  identical: TPR is a nuclear-basket component with roles in mRNA export and
  TREX-2/NXF1-associated export (Krull et al., 2004, PMID 15229283; Coyle et
  al., 2011, PMID 21613532; Aksenova et al., 2020, PMID 32917881, DOI
  10.1038/s41467-020-18266-2; Lee et al., 2020, PMID 33091126). `Xpo1`/CRM1 is
  the major NES export receptor and a ribosomal-subunit export receptor, not an
  NPC basket scaffold.

`Thoc1` was a lower-count, pathway-neighbor analog.

- `Thoc1` had 303 focal DEGs and its broad signatures were annotated by
  Distributed Agents as a THO/TREX-compatible RNA-biogenesis program with induced
  splicing/RNA-processing genes and repression of some mRNA-export or
  spliceosome factors including `Nxf1`, `Rnpc3`, `Snrnp70`, `Srrm2`, and
  `Ddx17`.
- `Thoc1` was not a direct XPO1 cargo receptor, but it calibrates what an
  RNA-export perturbation with partial focal vulnerability looks like after the
  same P16 sparse CRISPR delivery. Its 303 count is a strong argument for a
  nonzero `Xpo1` call but is likely below XPO1 because CRM1 touches many more
  protein and RNA export axes than the single TREX component.
- THOC1's role in transcription-coupled RNA export is well established
  (Li et al., 2005, PMID 15870275; Puehringer et al., 2020, DOI
  10.7554/eLife.61503).

`Tnpo3` was an indirect but useful RNA-processing/karyopherin analog.

- `Tnpo3` had 618 focal DEGs and shared 260 same-direction FDR genes with
  `Tpr`.
- Distributed Agents explicitly found that `Tnpo3` converges with `Tpr` and with
  splicing/RNA-processing perturbations while `Kpna3`, `Xpo7`, and `Ranbp2`
  do not reproduce the same module.
- TNPO3/Transportin-SR imports RS-domain splicing factors rather than exporting
  NES cargo; it is therefore a breadth calibrator for nuclear RNA logistics,
  not a direct mechanistic substitute for XPO1 (Kataoka et al., 1999; Lai et
  al., 2001; Maertens et al., 2014, PMID 24449914, DOI
  10.1073/pnas.1320755111).

The flat transport genes were important counterexamples.

- `Xpo7`, another exportin, had 0 DEGs in the focal group. Distributed Agents also
  recorded sparse Xpo7 behavior across the experiment and cautioned that Xpo7
  loss did not act like broad nuclear-transport perturbation.
- `Ranbp2` had 0 DEGs in the focal group even though it produced broad
  signatures in cerebellar GABA, MB Glut, and other cell types. That tells me
  a pore/Ran gene can be real yet fully buffered specifically in `151 TH Prkcd
  Grin2c Glut`.
- `Kpna3` and `Ddx39b` also had 0 DEGs in this exact cell type. The Ddx39b
  zero argues against predicting `Xpo1` solely from "RNA export factor" status.

# Xpo1 target-specific reasoning

`Xpo1` should be nonzero. Complete CRM1/XPO1 inhibition blocks export of many
NES-containing proteins, U snRNAs, ribosomal subunits, and several RNA cargo
classes; it can retain transcriptional regulators and ribosome-biogenesis
machinery in the nucleus. Those functions are much closer to the broad
Tpr/Thoc1/Tnpo3 side of the training data than to a neurotransmitter receptor,
autophagy cargo, or a zero-count transcription factor. Human XPO1
haploinsufficiency also supports neural dosage sensitivity, though the human
developmental observation is weaker for this acute postmitotic mouse readout.

I did not put `Xpo1` at the top of the Tpr-like tail. `Tpr` loss directly
perturbs the nuclear basket and NXF1/TREX-2 routing of polyadenylated RNAs, and
its 1,768-gene focal response was the second-largest response in the whole
training table. XPO1 is a more specific receptor than TPR, the assay creates a
partial mosaic LoF rather than acute small-molecule XPO1 blockade, and some
likely XPO1 outputs in dividing cells - cell-cycle arrest and apoptosis - are
muted in postmitotic NeuN+ nuclei. The flat `Xpo7`, `Ranbp2`, `Kpna3`, and
`Ddx39b` focal profiles also warned me that a central transport annotation does
not automatically imply a 1,000-plus count in this thalamic group.

The count I chose is therefore in the broad but not catastrophic range:
above `Thoc1` at 303, close to but slightly below `Tnpo3` at 618, and within
the range of the two proteasome calibrators `Psmc1` and `Psmb4` at 430 and
742. I predicted `Xpo1` at 520 DEGs.

# Limits

The main uncertainty is that none of the training perturbations is another
CRM1-like export receptor. `Xpo7` is the only exportin paralog assayed in the
focal data and it is a counterexample rather than an analog. TPR is an
excellent nuclear-export/NPC stress comparator, but it also has nuclear-basket,
chromatin, and TREX-2 functions that XPO1 loss will not reproduce. `Thoc1` and
`Ddx39b` show that RNA-export factors can be highly context-specific, and
`Ranbp2` proves that a nuclear-pore gene can be broad in other neurons yet flat
in the focal group. The public XPO1 literature is mostly from vertebrate cell
lines, oocytes, yeast, cancer, or human germline disease; I used it to assign
mechanistic direction, not to estimate the integer directly. The final 520 is
therefore an extrapolated point inside a calibrated broad-response interval,
not a signature-derived nearest-neighbor imputation.
