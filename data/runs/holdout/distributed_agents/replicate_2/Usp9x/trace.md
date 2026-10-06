# Usp9x prediction trace

## Question and resolved ambiguities

The requested output is a point prediction for the hidden count of focal-cell DE genes after acute mosaic CRISPR loss of `Usp9x`, where the count is:

- cell group: `151 TH Prkcd Grin2c Glut`
- endpoint: number of measured genes with Wilcoxon `pvals_adj < 0.05`
- source signature: perturbation versus matched non-targeting/safe-targeting controls

The held-out manifest contained exactly one target:

```text
Usp9x
```

`Usp9x` was absent from both the differential-expression parquet and the training DEG-count CSV, so I treated all same-experiment information for it as genuinely held out. I interpreted zero as "no measured gene clears the assay's FDR threshold", not as a failed edit or an unimportant gene.

## Sources used

Same-experiment data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- `[local file: training_de_all_cell_groups.parquet]`
- Distributed Agents same-experiment corpus, release `perturbai-july-260713-sourceguard-1773-v1`
- Distributed Agents run-local profile comparison tables generated from `training_de_all_cell_groups.parquet`

External biological sources:

- Reijnders et al. 2016, *American Journal of Human Genetics*, DOI `10.1016/j.ajhg.2015.12.015`, PMID `26833328`
- Stegeman et al. 2013, *PLoS One*, DOI `10.1371/journal.pone.0068287`, PMID `23861879`
- Homan et al. 2014, *American Journal of Human Genetics*, DOI `10.1016/j.ajhg.2014.02.004`, PMID `24607389`
- Yoon et al. 2019, *Neuron*, DOI `10.1016/j.neuron.2019.11.003`, PMID `31813652`
- Yoon et al. 2020, *Cell Reports*, DOI `10.1016/j.celrep.2020.107685`, PMID `32460012`
- Kasherman et al. 2021, *Cerebral Cortex*, DOI `10.1093/cercor/bhaa324`, PMID `33188399`
- Dupont et al. 2009, *Cell*, DOI `10.1016/j.cell.2008.10.051`, PMID `19135894`
- Yang et al. 2016, *Oncotarget*, DOI `10.18632/oncotarget.12819`, PMID `27783990`
- Lei et al. 2025, *Developmental Cell*, DOI `10.1016/j.devcel.2025.01.009`, PMID `39909046`
- Mertz et al. 2015, *Molecular and Cellular Proteomics*, DOI `10.1074/mcp.M114.045898`, PMID `25931508`
- Majumdar et al. 2021, *Science Advances*, DOI `10.1126/sciadv.abe3706`, PMID `33547080`
- Murtaza et al. 2015, *Cellular and Molecular Life Sciences*, DOI `10.1007/s00018-015-1851-0`, PMID `25672900`

## Computational checks over the training inputs

I first summarized the 1,674 focal-cell training counts. The distribution is extremely zero-inflated:

```text
zeros = 1205 / 1674
median = 0
75th percentile = 1
90th percentile = 2
95th percentile = 18
mean = 14.1
max = 2677
```

I then filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` for a mechanistic comparison panel rather than loading all 616,253,184 parquet rows. The focused extraction covered 37 candidate analog or boundary targets and 638,583 `(measured gene, perturbation)` rows, i.e. 17,259 measured features per perturbation. For those genes I computed:

- their observed `n_degs` from the training CSV;
- the FDR-significant measured-gene set for each perturbation;
- signed log-fold-change similarities and FDR-set overlaps among USP/DUB, ubiquitin-ligase, MIB1/Notch, Wnt/beta-catenin, TGF-beta/SMAD, ankyrin/ANKRD, mTOR, and proteostasis comparators.

I also ran Distributed Agents `profile_compare` on a 21-node subset of this cohort and flattened focal pairs with `profile_inspect`; this independently confirmed that the selected nodes were present and that many mechanistically adjacent nodes were FDR-flat or had only one to nine significant features.

## Relevant training perturbations

### USP and ubiquitin-system comparators

`Usp48` was the only represented `Usp*` target in the focal training counts and had 10 DEGs. Its significant genes were sparse and idiosyncratic, led by `Abhd12b`, `Cyp46a1`, `Resp18`, `Galk2`, and `Msrb2`; it shared no FDR-significant genes with the flat HECT/HERC/Notch/SMAD comparators that I inspected. This is the closest family-level count but a weak mechanistic analog, because USP enzymes tend to be substrate-specific.

The strongest ubiquitin-system effects in 151 were not deubiquitinases at all:

```text
Uba5   2677
Ufc1    572
Psmb4   742
Psmc1   430
```

Those are core UFMylation or proteasome failures. The same-experiment corpus explicitly places `Uba5`, `Ufc1`, `Psmb4`, and `Psmc1` in broad proteostasis/stress states that should not be collapsed with single distal chaperone or accessory perturbations. USP9X removes ubiquitin from a selected substrate set; it is not a proteasome subunit or the UFMylation E1/E2 machinery, so I treated these large counts as counterexamples rather than as magnitude anchors.

### HECT/HERC ligases and UBE3A

Observed focal counts:

```text
Huwe1   158
Hectd4    1
Hecw2     0
Herc1     0
Herc2     0
Ube3a     0
Ubr1      0
```

`Huwe1` is an X-linked neurodevelopmental E3 ligase and is the broadest ubiquitin-regulator comparator in this neighborhood. Its 151 signature was not a generic HECT/E3 phenotype: the Distributed Agents corpus claim `claim:6d2d4a78a1ef71447640` summarizes that `Huwe1` is transcriptionally visible while represented HECT/E3 ligases and related NDD comparators are flat, sparse, or nonconvergent. The raw focal profile supports this boundary: `Huwe1` had 90 positive and 68 negative significant genes, whereas it had zero significant-feature overlap with `Ube3a`, `Hecw2`, `Notch1`, `Notch2`, or `Smad4` in the inspected 151 cohort.

This makes `Huwe1` useful as a "large ubiquitin-regulator response is detectable" positive control, but not as a quantitative template for USP9X.

### MIB1/Notch

USP9X can regulate MIB1/Notch signaling outside this screen: Mertz et al. 2015 found Usp9x among high-confidence Mib1-interactome components in a neuronal context, and Majumdar et al. 2021 showed S-nitrosylated USP9X deubiquitinates and stabilizes MIB1 to activate NOTCH1 in aortic valve cells.

The 151 training endpoint separates that biochemical relationship from a postmitotic neuronal Notch transcriptional response:

```text
Mib1    27
Notch1   0
Notch2   0
Notch4   0
Fbxw7    1
```

`Mib1` itself was a modest responder dominated by sterol/cholesterol genes (`Insig1`, `Fdft1`, `Dhcr24`, `Ldlr`, `Msmo1`, `Hmgcs1`, `Hmgcr`, `Cyp51`, `Lss`, `Idi1`, `Sqle`). The Distributed Agents corpus records this as an SREBF2-like sterol module that is uncoupled from canonical Dll1/Notch signaling; its `Mib1:F002` finding notes absence of HES/HEY/Nrarp/Dtx output and lack of convergence with `Dll1`, `Notch`, `Adam10`, or `Psen1` perturbations. Therefore MIB1 argues for a possible small-to-moderate indirect USP9X response, not for a broad Notch phenotype.

### Wnt/beta-catenin

USP9X/FAM has been reported to stabilize beta-catenin by deubiquitination in glioma cells (Yang et al. 2016), and the same biochemical direction has also been observed in CNS endothelial Wnt biology. In the 151 neuronal data, however, the beta-catenin module is branch-specific:

```text
Ctnnb1   383
Tcf7l2   106
Lrp6       4
Gsk3b      6
Lrp5       0
Fzd6       0
Prickle1   0
Macf1      0
```

The corpus claim `claim:91053558b1caee68fc9f` states that the detectable 151 Wnt/catenin state links `Lrp6` with `Ctnnb1`/`Tcf7l2` rather than extending broadly to `Lrp5`, `Gsk3b`, single Frizzled receptors, ROR/RYK receptors, `Lgr4`, or other catenin-related perturbations. In my focal comparison, `Ctnnb1` and `Tcf7l2` shared 40 significant genes, but `Ctnnb1` shared only 4 with `Lrp6` and none with `Ube3a`, `Hecw2`, `Notch1`, or `Smad4`. Thus direct beta-catenin/TCF perturbations can be large in this cell group, but an upstream DUB that only partially modulates beta-catenin protein is expected to be much smaller.

### TGF-beta/SMAD and ankyrin/ANKRD substrates

USP9X has two relevant links here. Dupont et al. 2009 identified FAM/USP9X as a conserved deubiquitinase that controls Smad4 monoubiquitination and TGF-beta/BMP responsiveness. In neurons, Stegeman et al. 2013 connected Usp9x to TGF-beta-mediated axonogenesis, and Yoon et al. 2019/2020 showed that TGF-beta-dependent USP9X phosphorylation promotes interaction with ankyrin-G and stabilizes ankyrin-G/ANKRD-containing proteins at dendritic spines.

The focal CRISPR endpoint is quiet for both transcriptional branches:

```text
Smad4    0
Smad3    0
Smad2    1
Tgfbr1   0
Fkbp1a   1
Ank      1
Ank1     0
Ank2     0
Ankrd11 20
Mtor     2
```

The Distributed Agents corpus summarizes the receptor-to-SMAD result in `claim:fa3bde37b0b9b6d704e7`: represented TGF-beta/activin/BMP receptor, co-receptor, FKBP12, and SMAD perturbations do not produce a coherent basal transcriptional module in sampled postnatal neurons. That makes the USP9X-SMAD4 link biologically real but poorly coupled to this unstimulated P37-44 nuclear RNA readout. Likewise, the direct Usp9x/ankyrin-G literature is about protein abundance, ubiquitination, dendritic-spine maintenance, and cortical connectivity; `Ank`, `Ank1`, and `Ank2` were flat or singletons in 151, and the modest `Ankrd11` count is a chromatin/NDD signature rather than a direct phenocopy of ANK3 protein stabilization.

## Target-specific prediction for Usp9x

Human and mouse data make `Usp9x` a real neurodevelopmental gene. Loss-of-function variants cause USP9X female syndrome and X-linked intellectual disability (Reijnders et al. 2016; Homan et al. 2014), and conditional mouse work shows that Usp9x is required for cortical organization, hippocampal development, axonogenesis, dendritic-spine development, and forebrain connectivity (Stegeman et al. 2013; Yoon et al. 2019; Kasherman et al. 2021). Its molecular links span beta-catenin, SMAD4, MIB1/Notch, and ankyrin-G homeostasis.

For this particular endpoint, I downweighted those developmental and protein-substrate roles for four reasons:

1. The perturbation is P16-to-P37/44 acute mosaic editing in mostly recovered NeuN+ postmitotic nuclei, not germline or Nestin/Emx1 developmental deletion.
2. The major neuronal USP9X evidence is protein stability and synaptic/axon morphology, which snRNA-seq can miss.
3. The training data show that basal TGF-beta/SMAD, Notch, ankyrin, and upstream Wnt perturbations are mostly FDR-flat in the same 151 group.
4. Ubiquitin-system responses in the training set are target-specific: core proteasome/UFMylation perturbations are huge, `Huwe1` is moderate and target-specific, while `Usp48`, `Mib1`, ankyrin/SMAD/Notch neighbors are sparse.

I therefore predict a nonzero but low count, closest to the lone represented USP-family count and below the small MIB1/ANKRD response range:

```text
Usp9x -> 10 DEGs
```

## Limits and extrapolation

There is no same-experiment `Usp9x` signature, no curated same-experiment Distributed Agents finding for `Usp9x`, and the represented training panel lacks the closest paralog-style deubiquitinase or exact USP9X substrate-loss perturbation for many substrates. Usp48 is only a family analog, MIB1 is a binding/signaling comparator whose measured RNA state is sterol rather than Notch, and beta-catenin/SMAD links come largely from stimulated, malignant, vascular, or developmental settings. The prediction also cannot account for guide-level indel efficiency or USP9X protein half-life. The number above is consequently an extrapolated focal-cell RNA-breadth estimate, not a statement that USP9X biology itself is weak.
