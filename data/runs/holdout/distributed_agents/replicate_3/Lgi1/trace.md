# Lgi1 held-out DEG-count prediction

## Question I answered

The requested held-out perturbation list contains one gene:

```text
Lgi1
```

For that target I predicted the number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05` in
`151 TH Prkcd Grin2c Glut` nuclei. The held-out `Lgi1` perturbation
itself is absent from the supplied differential-expression parquet and from the
training endpoint CSV, so I treated all `Lgi1`-specific expression counts as
unobserved and transferred from represented pathway members.

I resolved one endpoint ambiguity as follows: the endpoint counts any measured
gene passing FDR 0.05, including the perturbed gene itself when the CRISPR
edit measurably reduces the target transcript. In this data set many singleton
responses in the focal class are exactly that self-transcript call.

## Sources used

- Input training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest:
  `[local file: 125_Lgi1.csv]`.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`, especially the Adam22-centered
  and Kcna1-centered findings.
- PubMed literature on the LGI1-ADAM22/ADAM23 synaptic complex, AMPAR
  regulation, and Kv1-channel regulation:
  - Sagane, Ishihama and Sugimoto 2008, DOI `10.7150/ijbs.4.387`
  - Fukata et al. 2010, PMID 20133599, DOI `10.1073/pnas.0914537107`
  - Ohkawa et al. 2013, PMID 24227725, DOI `10.1523/JNEUROSCI.3506-13.2013`
  - Dazzo et al. 2016, DOI `10.1371/journal.pgen.1006376`
  - Seagar et al. 2017, PMID 28673977, DOI `10.1073/pnas.1618656114`
  - Hivert et al. 2019, PMID 30598502, DOI `10.1242/jcs.219774`
  - Yamagata et al. 2018, DOI `10.1038/s41467-018-03947-w`
  - Fukata et al. 2021, PMID 33397806, DOI `10.1073/pnas.2022580118`

## Computations over the training data

1. I loaded the manifest and confirmed that it has exactly one held-out target,
   `Lgi1`.
2. I summarized the focal training endpoint. There are 1,674 represented
   perturbations in `151 TH Prkcd Grin2c Glut`; the distribution is extremely
   zero-heavy:

   ```text
   min = 0, 25th percentile = 0, median = 0, 75th percentile = 1,
   mean = 14.05, maximum = 2677
   ```

   The large DEG counts are mostly unrelated RNA-processing, proteostasis,
   transcriptional, or chromatin regulators such as `Uba5`, `Tpr`, `Sin3a`,
   `Rnpc3`, `Zbtb7a`, and `U2af2`.
3. I used Arrow predicate pushdown on the parquet to load only rows where
   `group_name == "151 TH Prkcd Grin2c Glut"` and `gene_target` was a
   mechanistic neighbor of `Lgi1`. For each represented neighbor I counted
   rows with `pvals_adj < 0.05` and inspected the FDR-significant genes.
4. I compared the full focal Wilcoxon-score vectors of `Adam22`, AMPAR/TARP
   members, Kv1-channel members, and other synaptic-adhesion comparators. This
   was a sanity check for shared subthreshold structure: using top 200 positive
   and top 200 negative score tails, `Adam22` had only 1 to 10 overlapping
   features with its candidate peers, and its full-score Pearson correlations
   to `Cacng2`, `Cacng3`, `Gria1`, `Gria2`, `Gria3`, `Dlg4`, `Kcna1`, `Kcna2`,
   `Cntnap2`, and `Nrxn1` were between -0.051 and +0.045.
5. I also ran Distributed Agents Runtime profile comparison/cohort diagnostics for the
   represented LGI1/ADAM, AMPAR/TARP, Kv1, PSD, `Cntnap2`, and `Nrxn1`
   neighborhood. The 55 pairwise comparisons had no recurrent overlap among
   significant DEG programs. Raw log-fold-change similarities were dominated
   by very large but nonsignificant fold changes in sparse genes, so I gave the
   FDR hit sets and Wilcoxon-score vectors more weight.

## Held-out target reasoning

### Lgi1

`Lgi1` encodes a secreted neuronal ligand for ADAM-family receptors. LGI1 binds
ADAM22, ADAM23, and ADAM11 in biochemical assays (Sagane et al. 2008), bridges
presynaptic ADAM23/Kv1-channel biology with postsynaptic ADAM22/MAGUK/AMPAR
scaffolding, and loss of the LGI1-ADAM22/23 interaction is epileptogenic in
mouse and human systems (Fukata et al. 2010; Ohkawa et al. 2013; Dazzo et al.
2016). The complex also affects axonal Kv1.1/Kv1.2 channel localization and
excitability (Seagar et al. 2017; Hivert et al. 2019) and forms higher-order
trans-synaptic LGI1-ADAM22-MAGUK assemblies that organize AMPAR/NMDAR and Kv1
networks (Yamagata et al. 2018; Fukata et al. 2021).

The most direct represented receptor comparator was `Adam22`.

```text
Adam22: n_degs = 1 in 151 TH Prkcd Grin2c Glut
FDR hit: Adam22 logFC -0.550, q 1.07e-09
```

No downstream gene accompanied this self-transcript decrease in the focal
class. The Distributed Agents corpus summarized the broader Adam22 result as a strongly
buffered neuronal snRNA-seq surface: despite recurrent mild on-target mRNA
decreases, Adam22 loss produced only one downstream FDR<0.10 gene across 21
recovered cell groups and 355,046 tested Adam22 rows. The same corpus also
found that Adam22 did not engage canonical AMPAR, MAGUK, TARP, Kv1,
immediate-early, ISR, or UPR modules. I treated this as the closest available
evidence because ADAM22 is the postsynaptic LGI1 receptor represented in the
training set; `Adam23`, `Adam11`, and the `Lgi` paralogs were not represented.

The direct AMPAR/TARP and Kv1-channel comparators were also essentially flat in
the exact focal group:

```text
Cacng2  n_degs = 0
Cacng3  n_degs = 0
Gria1   n_degs = 0
Gria2   n_degs = 0
Gria3   n_degs = 0
Kcna1   n_degs = 0
Kcna2   n_degs = 0
Dlg4    n_degs = 1, only Dlg4 itself
```

Other synaptic-adhesion genes provided counterexamples against a hidden generic
adhesion-loss RNA state:

```text
Cntnap2 n_degs = 1, only Cntnap2 itself
Nrxn1   n_degs = 1, only Nrxn1 itself
Nrxn2   n_degs = 0
Nrxn3   n_degs = 0
Il1rap  n_degs = 0
Il1rapl1 n_degs = 0
Il1rapl2 n_degs = 0
Ptprd   n_degs = 0
Ptprt   n_degs = 0
```

NMDA-receptor perturbations set a useful detectability boundary but were weaker
analogs. `Grin2a` had a singleton self-transcript response, `Grin2b` had two
hits, and the core subunit `Grin1` had 89 DEGs. I did not transfer the `Grin1`
count to `Lgi1`, because the Adam22/AMPAR/TARP/Kv1 side of LGI1 biology was
flat and much more mechanistically direct.

The zero/nonzero choice came down to whether the held-out CRISPR perturbation
is likely to call `Lgi1` itself as an FDR-significant row. The within-dataset
analog of a direct receptor, `Adam22`, called only its own transcript; `Dlg4`,
`Cntnap2`, `Nrxn1`, and `Grin2a` behaved similarly. `Lgi1` RNA was also
detectable as a measured gene in the focal signatures: among training
perturbations, broad regulators such as `Zfp423`, `Cic`, `Sin3a`, and `Phf12`
made `Lgi1` itself FDR-significant. That made a single self-transcript hit a
little more plausible than a complete zero.

I therefore predicted one DEG for `Lgi1`: enough to allow an on-target `Lgi1`
RNA decrease, but not enough to posit a broad downstream AMPAR/Kv1, seizure,
stress, or immediate-early transcriptional cascade after sparse postnatal
mosaic loss.

## Limits of the reasoning

- The best ligand/receptor perturbation, `Adam22`, is postsynaptic and
  membrane-tethered, whereas LGI1 is secreted and can be supplied
  non-cell-autonomously by unedited neighboring neurons. That makes `Adam22`
  the right represented comparator but still an imperfect phenocopy.
- `Adam23`, `Adam11`, `Lgi2`, `Lgi3`, and `Lgi4` were absent as training
  perturbations, so the strongest within-family controls were unavailable.
- The experiment measures nuclear RNA 3 to 4 weeks after sparse AAV CRISPR.
  It does not assay LGI1 secretion, extracellular LGI1-ADAM22/23 complexes,
  AMPAR or Kv1 localization, synaptic currents, seizure thresholds, or network
  synchrony, all of which are central to LGI1 disease biology.
- The exact count hinges on whether the held-out `Lgi1` guides produced enough
  target-mRNA reduction in this cell group for the `Lgi1` row itself to pass
  BH FDR. The represented pathway argues against a downstream program, but the
  self-transcript call is target-expression and guide-efficiency dependent.
