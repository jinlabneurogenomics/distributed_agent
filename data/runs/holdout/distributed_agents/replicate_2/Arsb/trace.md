# Question and resolution

The manifest for this run contains one held-out target:

```text
Arsb
```

I interpreted the requested scalar as the number of measured genes with
`pvals_adj < 0.05` for the held-out `Arsb` perturbation in
`151 TH Prkcd Grin2c Glut` cells. The count includes the targeted transcript
itself if the target gene is measured and its self row passes FDR. `Arsb` was
absent from the supplied training endpoint, as expected for a held-out target.

The point prediction is:

```text
Arsb: 0
```

# Sources

Internal same-experiment data:

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
  for exact focal-cell `n_degs` values among 1,674 non-held-out targets.
- `[local file: training_de_all_cell_groups.parquet]`
  for focal-cell per-gene FDRs and log fold changes.
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`, a
  curated same-experiment interpretation layer. I queried `Arsb` directly; it
  had no target-specific entries in this corpus. I therefore used Distributed Agents
  claims and target reports for represented lysosomal hydrolase, cargo,
  mannose-6-phosphate trafficking, autophagy, V-ATPase, `Tsc2`, and `Rab7`
  perturbations.
- A run-local `profile_neighbors` inspection on the focal cell group for
  lysosomal and lysosome-counterexample anchors. Whole-logFC similarities in
  this one cell group were high even for FDR-null anchors, so I treated those
  as a sanity check that the signatures were weak or isolated, not as positive
  mechanistic evidence.

External mechanism sources:

- PubMed literature for `Arsb` / arylsulfatase B.
- Valayannopoulos et al. 2010, Orphanet Journal of Rare Diseases,
  DOI `10.1186/1750-1172-5-5`, PMID `20385007`: ARSB
  N-acetylgalactosamine-4-sulfatase deficiency causes MPS VI and interrupts
  dermatan sulfate and chondroitin sulfate degradation.
- Yoshida et al. 1993, Journal of Comparative Pathology,
  DOI `10.1016/s0021-9975(08)80258-7`, PMID `8245230`: in an arylsulfatase
  B-deficient MPS VI rat model, central and peripheral nervous system lesions
  were restricted to connective tissue.
- Haskins et al. 1980, American Journal of Pathology, PMID `6778219`: feline
  arylsulfatase-B-deficient MPS VI primarily accumulated storage in visceral,
  connective, vascular, and fibroblast-like compartments; CNS lesions were
  limited relative to many neuronopathic lysosomal storage disorders.
- Fillat et al. 1996, Journal of Clinical Investigation,
  DOI `10.1172/JCI118817`, PMID `8755662`: ASB released from engineered MPS VI
  bone-marrow cultures could be taken up by MPS VI fibroblasts or chondrocytes
  through the mannose-6-phosphate receptor system and metabolically
  cross-correct those cells.
- Fuller et al. 1998, Biochimica et Biophysica Acta,
  DOI `10.1016/s0925-4439(98)00011-8`, PMID `9630676`: recombinant
  N-acetylgalactosamine-4-sulfatase bound the mannose-6-phosphate receptor on
  human fibroblasts.

# Computations over the supplied data

I loaded the requested manifest and verified that it has exactly one
non-duplicated target, `Arsb`.

I summarized the focal training endpoint. The distribution is very sparse:
`1205/1674 = 72.0%` of represented targets had `n_degs = 0`; the median was
0, the 75th percentile was 1, and only 43 targets had at least 100 DEGs.

I then used the parquet with the filter
`group_name == "151 TH Prkcd Grin2c Glut"` and selected biologically relevant
training perturbations. The closest represented genes to `Arsb` are not other
arylsulfatases or MPS dermatan/chondroitin sulfate enzymes; `Arsa`, `Arsg`,
`Arsk`, `Sumf1`, `Galns`, `Ids`, `Idua`, `Gusb`, `Gns`, `Sgsh`, `Naglu`,
`Hexa`, `Hexb`, `Glb1`, and `Neu1` were not in the focal training endpoint.

The exact focal counts for the useful represented comparators were:

| class | target | n_degs | self row in 151 TH Prkcd Grin2c Glut |
|---|---:|---:|---|
| M6P trafficking / soluble hydrolase | `Gnptab` | 0 | `Gnptab`, logFC -0.126, FDR 1 |
| M6P trafficking / soluble hydrolase | `Gnptg` | 0 | `Gnptg`, logFC -0.467, FDR 0.459 |
| soluble hydrolase | `Manba` | 0 | `Manba`, logFC -0.204, FDR 1 |
| soluble hydrolase | `Ppt1` | 1 | `Ppt1`, logFC -0.536, FDR 1.34e-5 |
| soluble hydrolase / cargo | `Psap` | 1 | `Psap`, logFC -1.277, FDR 1.70e-28 |
| soluble hydrolase | `Gaa` | 1 | `Gaa`, logFC -0.709, FDR 8.97e-16 |
| soluble hydrolase | `Asah1` | 0 | `Asah1`, logFC -0.273, FDR 1 |
| lysosomal protease | `Ctsb` | 1 | `Ctsb`, logFC -1.480, FDR 8.54e-43 |
| lysosomal trafficking / cargo | `Sort1` | 0 | `Sort1`, logFC -0.366, FDR 0.0939 |
| endolysosomal disease gene | `Tmem106b` | 1 | `Tmem106b`, logFC -0.892, FDR 1.18e-13 |
| endolysosomal disease gene | `Atp13a2` | 1 | `Atp13a2`, logFC -0.613, FDR 2.23e-21 |
| endolysosomal disease gene | `Grn` | 1 | `Grn`, logFC -0.770, FDR 5.27e-5 |
| lysosomal membrane | `Scarb2` | 1 | `Scarb2`, logFC -0.811, FDR 0.00246 |
| lysosomal membrane / autophagy | `Lamp2` | 0 | `Lamp2`, logFC -0.380, FDR 0.0537 |
| V-ATPase | `Atp6v0a1` | 1 | `Atp6v0a1`, logFC -0.640, FDR 4.52e-12 |
| V-ATPase | `Atp6v1a` | 0 | `Atp6v1a`, logFC -0.236, FDR 1 |
| V-ATPase | `Atp6v1e1` | 0 | `Atp6v1e1`, logFC -0.297, FDR 1 |
| autophagy initiation | `Becn1` | 0 | `Becn1`, logFC -0.105, FDR 1 |
| autophagy elongation | `Atg5` | 0 | `Atg5`, logFC -0.435, FDR 1 |
| mTORC1 component | `Mtor` | 2 | `Mtor`, logFC -0.413, FDR 0.256 |
| mTORC1 inhibitor | `Tsc2` | 86 | `Tsc2`, logFC -0.312, FDR 0.173 |
| endolysosomal trafficking | `Rab7` | 501 | `Rab7`, logFC -0.405, FDR 0.00941 |

For `Ppt1`, `Psap`, `Gaa`, `Ctsb`, `Tmem106b`, `Atp13a2`, `Grn`,
`Scarb2`, and `Atp6v0a1`, the only FDR<0.05 gene in this focal group was the
targeted transcript itself. That argues that the closest hydrolase and
lysosomal-disease comparators produced no downstream FDR-level program here.
`Mtor` produced only two downstream genes. `Tsc2` and `Rab7` were retained as
counterexamples showing that this cell group and assay can emit a broad
lysosome-linked or endolysosomal response when the perturbed node couples to
one.

I also looked at `Arsb` as a measured feature across all 1,674 non-held-out
focal perturbations. It was present in the focal DE matrix, but its adjusted
p-values were almost all 1.0; the minimum was 0.017 under unrelated `Nrf1`
perturbation. Thus `Arsb` is not behaving like a consistently high-power
nuclear feature in `151 TH Prkcd Grin2c Glut` cells, and a sole Arsb
self-transcript DEG is less likely than for high-signal hydrolase transcripts
such as `Ctsb`, `Psap`, or `Gaa`.

# Same-experiment biological evidence

The Distributed Agents corpus made the represented hydrolase pattern more trustworthy
than a count table alone. Its lysosomal claims state that:

- represented soluble lysosomal hydrolase, cargo, and M6P-pathway
  perturbations were largely buffered at the acute neuronal mRNA level rather
  than converging on a broad storage-stress module;
- disease-associated lysosomal, NCL, hydrolase/cargo, and trafficking
  perturbations did not elicit a shared neuronal lysosomal-stress, autophagy,
  TFEB/MiT, or ISR/UPR nuclear RNA program in this assay;
- `Gnptab` and `Gnptg`, the represented GlcNAc-1-phosphotransferase
  M6P-tag-synthesis components, shared flat neuronal transcriptional surfaces;
- V-ATPase perturbations did not produce a generic lysosomal phenotype:
  `Atp6v0a1` was flat and `Atp6v1e1` was weak and restricted.

Target-level Distributed Agents findings for `Gnptab`, `Manba`, `Ppt1`, and `Psap`
specifically reported pan-neuronal or broadly matched-group nulls for expected
lysosomal, autophagy, UPR/ISR, and TFEB/CLEAR secondaries. `Rab7` and `Tsc2`
were treated as counterexamples, not analogs: they are acute trafficking or
mTORC1 regulators that can couple to large RNA programs, whereas `Arsb` is one
soluble GAG-degrading hydrolase.

# Arsb-specific prediction

`Arsb` encodes lysosomal N-acetylgalactosamine-4-sulfatase, the enzyme that
removes 4-sulfate from dermatan sulfate and chondroitin 4-sulfate. Complete
germline loss causes MPS VI, a progressive storage disorder driven by
glycosaminoglycan accumulation. The most relevant external features for this
screen are that MPS VI is not a strongly neuronopathic disease and that ASB is
a soluble lysosomal enzyme that can be supplied to deficient cells via
mannose-6-phosphate receptor uptake.

Those external facts make `Gnptab`, `Gnptg`, `Manba`, `Ppt1`, `Psap`, `Gaa`,
`Asah1`, and `Ctsb` the best in-dataset analogs despite imperfect substrate
differences. In the exact requested cell group these targets had 0 or 1 DEG,
and the one-DEG cases were pure self-transcript calls. The closest
endolysosomal disease genes, `Grn`, `Atp13a2`, `Tmem106b`, and `Scarb2`, also
stopped at a single self transcript in this cell group. `Lamp2`, `Becn1`,
`Atg5`, and the V-ATPase subunits were flat or self-only. This is exactly the
pattern expected if sparse P16 perturbation of one lysosomal hydrolase is
biochemically local, partly cross-correctable by surrounding unedited cells,
and too slow to accumulate a neuron-intrinsic storage-stress state by
P37-P44.

I considered predicting `1` to allow a self-transcript hit, but rejected it.
The one-hit comparators had strong on-target FDRs and no downstream genes;
`Arsb` itself looked weak as a measured focal feature across the training
contrasts. Because the endpoint counts measured genes passing FDR, weak target
feature expression can move an otherwise biologically perturbed gene from a
self-only `1` to a literal `0`.

I therefore predict no FDR<0.05 genes for `Arsb` in `151 TH Prkcd Grin2c Glut`.

# Limits

There was no `Arsb` entry in the same-experiment Distributed Agents corpus and no close
represented paralog or same-substrate GAG hydrolase in the focal training
endpoint, so the prediction extrapolates from the broader soluble hydrolase,
M6P-trafficking, and endolysosomal disease set. Those are informative but not
chemically identical to dermatan/chondroitin sulfate desulfation.

The experiment did not measure ARSB protein, lysosomal ASB enzymatic activity,
GAG storage, mannose-6-phosphate cross-correction, DNA indels, or
pre-assay viability. A zero DEG prediction means the acute survivor neuronal
nuclear transcriptome should stay below this Wilcoxon FDR threshold; it does
not mean the edited neurons have normal lysosomal chemistry.

Finally, the cell population is NeuN-enriched and glia-poor. Chronic MPS VI
connective-tissue, skeletal, meningeal, vascular, and glial or inflammatory
phenotypes would be underrepresented here, and the juvenile sparse-mosaic
window is much shorter than congenital systemic ARSB deficiency.
