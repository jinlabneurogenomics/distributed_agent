# DEG-count prediction trace

## Question and endpoint

The requested target file contains one held-out perturbation, `Dync1h1`. I
interpreted the task as predicting the scalar number of genes that would pass
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in the focal
`151 TH Prkcd Grin2c Glut` class if `Dync1h1` had been present in the training
differential-expression Parquet. This is a count of significant single-gene
nuclear RNA contrasts among recovered nuclei, not a direct viability,
axon-transport, editing-efficiency, or absolute RNA endpoint.

The training count CSV is direct supervision for the same endpoint in
non-held-out perturbations. The differential-expression Parquet is direct
evidence for the detailed signatures of those visible analogs. The held-out
`Dync1h1` endpoint and its expression signature are absent from the declared
inputs: a direct Parquet query returned zero rows with `gene_target =
'Dync1h1'`, whereas `Dctn1` had 371,818 visible rows.

The target set is unranked. I preserved the manifest order and used it only as
output order.

## Sources used

- Declared input CSV,
  `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: observed focal
  `n_degs` for 1,674 visible perturbations.
- Declared input Parquet, `training_de_all_cell_groups.parquet`: exact
  per-gene differential-expression rows for visible perturbations.
- Run-local `PerturbAI atlas dataset portrait`, measurement registry, task
  bindings, compact coverage, and capability manifest.
- Internal same-experiment corpus: July 260713 SourceGuard 1773 v1 Findings and
  Evidence ledgers, used as a pre-interpreted semantic layer over the same
  visible experiment, not as independent replication.
- External literature and curated database priors for molecular function:
  UniProtKB for DCTN1/dynactin function; Hafezparast et al. 2003,
  DOI 10.1126/science.1083129, PMID 12730604; McKenney et al. 2014,
  DOI 10.1126/science.1254198, PMID 25035494; Moughamian and Holzbaur 2012,
  DOI 10.1016/j.neuron.2012.02.025, PMID 22542186; Jordens et al. 2001,
  DOI 10.1016/S0960-9822(01)00531-0, PMID 11696325; Brown and Goldstein 1997,
  PMID 9150132, and Madison 2016, PMID 26798145, for SREBP2/sterol-feedback
  biology.

## Computational evidence

I first summarized the focal training counts to calibrate count scale. They are
very zero-inflated:

- 1,674 visible biological targets.
- Median `n_degs`: 0.
- 75th percentile: 1.
- 90th percentile: 2.
- 95th percentile: 18.
- 99th percentile: 436.
- Maximum: 2,677.

I then queried the declared Parquet with `group_name =
'151 TH Prkcd Grin2c Glut'`, counting rows with `pvals_adj < 0.05` for dynein,
dynactin, vesicle-transport, and Dctn1/Rab7 comparator targets. The focal counts
that mattered were:

| visible perturbation | focal n_degs | role in the Dync1h1 prediction |
| --- | ---: | --- |
| `Dctn1` | 75 | closest cytoplasmic dynein/dynactin analog in the declared training set |
| `Tsc2` | 86 | partial same-direction lysosome/sterol neighbor of `Dctn1` and `Rab7`, not a motor subunit |
| `Mib1` | 27 | data-driven `Dctn1` sterol-program neighbor with weaker focal breadth |
| `Vps35` | 17 | late-endosomal/retromer comparator, partial and much weaker |
| `Marchf6` | 14 | ER sterol-metabolism comparator, useful for sterol genes only |
| `Srebf2` | 7 | inverse validation of the sterol module |
| `Htt` | 3 | known dynein/dynactin vesicular-transport scaffold but a weak focal perturbation |
| `Kif1a` | 1 | kinesin counterexample |
| `Kif5a` | 1 | kinesin counterexample |
| `Kif5c` | 1 | kinesin counterexample |
| `Dync2h1` | 0 | axonemal/intraflagellar dynein, not cytoplasmic dynein-1 |
| `Dync2i1` | 0 | axonemal/intraflagellar dynein, not cytoplasmic dynein-1 |
| `Vps41` | 0 | Rab7/HOPS pathway neighbor that did not phenocopy the focal Dctn1 response |
| `Hmgcr` | 0 | sterol-enzyme counterexample |
| `Srebf1` | 0 | SREBP-family counterexample |

`Dctn1` had the relevant expression pattern. In the focal 151 class its 75 FDR
< 0.05 genes were led by up-regulated sterol and lipid genes:
`Insig1`, `Msmo1`, `Hmgcs1`, `Cyp51`, `Hmgcr`, `Fdft1`, `Fasn`, `Tecr`,
`Sqle`, `Dhcr24`, `Fdps`, `Ldlr`, `Stard4`, `Mvd`, `Lss`, `Dhcr7`, `Sc5d`,
`Nsdhl`, `Idi1`, `Aacs`, and `Srebf2`. The same focal response also contained
down-regulated neuronal, cytoskeletal, synaptic, or activity-linked genes
including `Kcnc2`, `Stmn4`, `Syt11`, `Gpm6a`, `Grin2b`, `Jun`, `Jund`,
`Atp2b1`, `L1cam`, `Atg9a`, and `Pcsk2`, plus limited endolysosomal genes such
as `Lamp2` and `Dpp7`.

`Rab7` was much broader in the same focal class with 501 DEGs. It shared the
sterol branch (`Insig1`, `Msmo1`, `Fdft1`, `Dhcr24`, `Sqle`) and neuronal
downshift (`Grin2b`, `Pcsk2`, `Kcnc2`) with `Dctn1`, and Dctn1's corpus report
recorded 77 same-direction FDR-level overlaps with `Rab7` versus 6 opposite
overlaps. However `Rab7` also induced a large late-endosomal/lysosomal,
V-ATPase, autophagy, proteasome, and ISR response in 151, including
`Atp6v1b2`, `Atp6v0b`, `Lamp2`, `Gaa`, `Grn`, `Sqstm1`, `Map1lc3b`, `Optn`,
`Ubc`, `Ddit3`, and `Herpud1`. That extra catabolic stress layer makes `Rab7`
an upper-bound counterexample rather than the right count anchor for
`Dync1h1`.

Across all cell classes, `Dctn1` produced broad FDR < 0.05 signal mainly in
`155 MB Glut` with 100 DEGs, `151 TH Prkcd Grin2c Glut` with 75, and
`191 MB P MY GABA` with 65; lower counts appeared in `066 CNU-HYa HY GABA`,
`217 P MY Pineal Glut`, and `145 MH-LH TH Glut`. Thus the focal class is a
strong responder for dynactin loss, but the same perturbation is not a uniform
pan-neuronal FDR response.

## Target-specific transfer

### Dync1h1

`Dync1h1` encodes the cytoplasmic dynein-1 heavy chain, the catalytic motor
chain for retrograde microtubule transport. The causal model I used was:

`Dync1h1` acute CRISPR loss -> impaired dynein motor activity and dynein-
dynactin-adaptor transport -> altered retrograde movement of endosomes,
lysosomes, autophagosomes, and other neuronal cargoes -> secondary membrane
sterol/endolysosomal feedback and a neuronal functional downshift in surviving
151 TH Prkcd Grin2c Glut nuclei -> a moderate focal count of FDR-significant
nuclear transcripts.

The same-direction prior from `Dctn1` is strong. Dynactin activates processive
dynein movement in cargo-adaptor complexes (McKenney et al. 2014), p150/DCTN1
is required for efficient initiation of retrograde vesicular transport in
distal axons (Moughamian and Holzbaur 2012), and dynein heavy-chain mutations
cause neuronal retrograde-transport phenotypes in mice (Hafezparast et al.
2003). Therefore a `Dync1h1` perturbation and a `Dctn1` perturbation impair the
same limiting retrograde transport machinery in postmitotic neurons. This is
not just a broad "motor protein" argument: in the training data the anterograde
kinesin perturbations `Kif1a`, `Kif5a`, `Kif5c`, and `Kifbp` produced only 1,
1, 1, and 2 focal DEGs, respectively, and ciliary dynein targets `Dync2h1` and
`Dync2i1` produced 0.

The Rab7 connection supported the direction of the expected response but not a
501-DEG count. Rab7/RILP recruits dynein-dynactin to late endosomes and
lysosomes (Jordens et al. 2001), and the internal Rab7 report placed `Dctn1` as
a same-direction transport/ER/lipid comparator. A heavy-chain perturbation
should disrupt these Rab7 cargo movements downstream of the endosome, so it can
plausibly trigger the sterol/lipid genes seen after `Dctn1`. But it need not
copy Rab7's direct late-endosomal identity, and Rab7's focal response had a
much broader lysosomal acidification, autophagy, proteasome, and ISR layer.
`Vps41`, `Vps35`, V-ATPase subunits, `Lamp2`, `Gaa`, and `Grn` were also weak
or partial Rab7 phenocopies in the same experiment, which argues against
upscaling any Rab7-related target solely from pathway neighborhood.

The approximate count was therefore anchored just below the visible dynactin
perturbation. `Dctn1` itself had 75 focal DEGs, the nearest same-scale pathway
neighbor `Tsc2` had 86, and the sterol-only or vesicle-only comparators
`Mib1`, `Marchf6`, `Srebf2`, `Htt`, and `Vps35` were lower at 3-27. I predict a
clear nonzero response with a sterol/dynactin-like breadth, not the massive
Rab7 stress outlier.

Prediction: `Dync1h1 = 72` DEGs.

## Limits

The strongest evidence is a causal transfer from visible `Dctn1`, not a direct
`Dync1h1` measurement. The two proteins act in the same dynein-dynactin
transport machine, but the CRISPR allele mix, residual protein, and recovery of
surviving nuclei could differ between a large catalytic heavy chain and the
p150 dynactin subunit. A stronger heavy-chain knockout could either broaden the
stress signature or selectively remove the most affected nuclei before
snRNA-seq. The Parquet also contains normalized nuclear RNA, not axonal
transport rates, sterol concentrations, lysosomal pH, or cell abundance. The
chosen value is therefore a calibrated point estimate around the visible
`Dctn1` response rather than a mechanistic absolute.
