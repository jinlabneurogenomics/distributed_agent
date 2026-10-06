# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question and endpoint

The requested held-out perturbation list contains one mouse target:

```tsv
target_name
Il10rb
```

I interpreted the task as a scalar point prediction of `n_degs` for acute
AAV-CRISPR loss of `Il10rb` in postnatal, NeuN-enriched mouse neurons of the
`151 TH Prkcd Grin2c Glut` class. The value to predict is the count of measured
genes in that same cell group whose Wilcoxon Benjamini-Hochberg adjusted
p-value is below 0.05. `Il10rb` was absent from the supplied training
differential-expression parquet as a `gene_target` and absent from the focal
training-count table, so no direct same-experiment `Il10rb` DEG count or
signature was available.

The declared differential-expression parquet and focal training counts are
direct measurements of this endpoint for non-held-out perturbations. The July
PerturbAI same-experiment corpus was used only as packaged interpretation of
the same screen, not as independent replication. External evidence came from
PubMed-indexed IL-10 receptor literature.

## Quantitative calibration from training perturbations

The focal training-count table contains 1,674 visible biological perturbations.
The endpoint is sparse:

```text
median n_degs = 0
mean n_degs   = 14.05
75th pct      = 1
90th pct      = 2
95th pct      = 18
zero count    = 1205/1674
```

I then queried the declared parquet for represented cytokine-receptor and
JAK/STAT perturbations in `151 TH Prkcd Grin2c Glut`. Every measured row was
counted only for the focal cell group and only an adjusted p-value below 0.05
contributed to `n_degs`.

```text
Il10ra  n_degs=0, min adjusted p=0.4323, 187 perturbed nuclei
Il6ra   n_degs=0
Il6st   n_degs=0
Osmr    n_degs=0
Il31ra  n_degs=0
Ifnar1  n_degs=0
Ifnar2  n_degs=0
Ifngr1  n_degs=0
Ifngr2  n_degs=0
Il1r1   n_degs=0
Il1rap  n_degs=0
Il17ra  n_degs=0
Il21r   n_degs=0
Il23r   n_degs=0
Stat1   n_degs=1
Stat2   n_degs=0
Stat3   n_degs=0
Stat4   n_degs=0
Stat5b  n_degs=0
```

The exact IL-10 receptor alpha-chain perturbation, `Il10ra`, was the most
important analog because IL-10 signals through a receptor complex containing
IL-10R1/IL10RA plus IL-10R2/IL10RB. In the focal cell group `Il10ra`
perturbation had no FDR-significant genes among 17,259 measured genes. Its best
row was `Mybbp1a` with `log2FC=-0.463`, raw `p=2.50e-05`, but adjusted
`p=0.432`; canonical IL-10/STAT3 or inflammatory-output genes were flat after
multiple testing:

```text
Il10ra perturbation, 151 TH Prkcd Grin2c Glut:
Il10ra  padj=1.000
Il10rb  padj=1.000
Stat1   padj=1.000
Stat3   padj=1.000
Socs3   padj=1.000
Bcl2    padj=1.000
Bcl2l1  padj=1.000
Bcl2l2  padj=1.000
Tnf     padj=1.000
Il1b    padj=1.000
Il6     padj=1.000
Il12b   padj=1.000
Ccl2    padj=1.000
Cxcl10  padj=1.000
```

`Il10ra` was not a focal-cell-only null: it produced zero FDR-significant genes
in every recovered neuronal group in the parquet. The July corpus summarizes
the same result as `Il10ra:F001`, a high-confidence negative result in which
`Il10ra` loss was transcriptionally silent at FDR < 0.10 in every recovered
neuronal cell group, and as `Il10ra:F002`, noting that the expected STAT3
feedback, inflammatory, chemokine, nitric-oxide/prostaglandin, and Bcl2-family
survival genes failed FDR correction. Its `Il10ra:F003` cross-perturbation
contrast also reported no convincing phenocopy among represented
Ifnar/Ifngr/Il6 receptor or STAT relatives.

I used several counterexamples to avoid relying on family membership alone.
`Ifnar1`, `Ifnar2`, `Ifngr1`, `Ifngr2`, `Il6st`, and `Stat3` are not the same
receptor complex as IL-10R, but they ask whether tonic cytokine-JAK/STAT
signaling in these postnatal neurons leaves a measurable screen footprint. In
the focal training counts all of those targets were exact zeros; `Stat1` was
the only singleton among the inspected JAK/STAT group. The same-experiment
corpus also describes `Ifnar1` and `Il6st` as stimulus-gated, mostly null
neuronal surfaces rather than hidden broad cytokine programs.

I also checked whether `Il10rb`, `Il10ra`, `Ifnlr1`, `Il22ra1`, or `Socs3`
were recurrently perturbed downstream genes. In the focal cell group, each of
those measured genes was present across all 1,674 visible perturbations and
none passed FDR 0.05 under any perturbation. Across all assayed neuronal groups,
`Il10rb`, `Il10ra`, `Ifnlr1`, and `Socs3` were never FDR-significant as
measured genes in the visible perturbations. This is not a baseline-expression
assay, but it argues against a recurring class-II cytokine receptor feedback
module in the observed neuronal DE space.

## Biological transfer for Il10rb

IL10RB encodes IL-10R2, the accessory chain shared by multiple class-II
cytokine receptors. IL-10 binds IL-10R1/IL10RA and then recruits IL-10R2 to
signal through JAK1/TYK2 and STAT3; IL-22 and IFN-lambda family cytokines use
distinct private R1 chains but the same IL-10R2 chain. This receptor architecture
is summarized in Donnelly et al. 2004, DOI `10.1189/jlb.0204117`, and the
IL-10R1/IL-10R2/JAK/STAT3 module in mononuclear phagocytes was reviewed by
Donnelly, Dickensheets and Finbloom 1999, DOI `10.1089/107999099313695`.
Wilbers et al. 2017, DOI `10.1371/journal.pone.0186317`, further supports that
IL-10 responses in mouse myeloid cells require both IL-10R1 and IL-10R2 while
the IL-10R2-associated kinase Tyk2 mainly tunes response amplitude.

For the requested experiment the causal chain is:

```text
Il10rb CRISPR loss
-> impaired IL-10R2 accessory-chain contribution to IL-10, IL-22, and IFN-lambda
   receptor signaling in successfully edited neurons
-> reduced tonic class-II cytokine JAK/STAT signaling if those receptors and
   ligands are active in 151 TH Prkcd Grin2c Glut cells
-> changed expression in recovered nuclei 3-4 weeks after AAV delivery
-> Wilcoxon FDR-significant DEGs among measured genes
```

The weak link is the middle one. `Il10ra` directly tests the private IL-10
binding chain and was completely silent in the exact focal cell group, with
good local power for this screen. The visible IFN and gp130 cytokine receptors
showed the same near-null behavior. Therefore the best supported transfer is
not from a positive immune IL-10 phenotype but from the absence of detectable
tonic IL-10/JAK/STAT transcription in unstimulated, postnatal, NeuN-enriched
neurons. Because `Il10rb` is a shared accessory chain, a nonzero prediction
would require an active `Il10ra`, `Ifnlr1`, `Il22ra1`, or related private-chain
context that was not visible for `Il10ra` and not suggested by the broader
cytokine-receptor comparators.

I therefore predict that acute `Il10rb` perturbation will not produce any gene
passing FDR 0.05 in `151 TH Prkcd Grin2c Glut`.

## Prediction

```tsv
target_name	predicted_n_degs
Il10rb	0
```

## Limits

This is an extrapolation because `Il10rb` itself was held out: the parquet has
no `Il10rb` perturbation rows and the selected July same-experiment corpus has
no `Il10rb` target node. The input data also lack DNA indel calls, raw per-cell
UMIs, protein abundance, phospho-STAT measurements, and cytokine stimulation
conditions. IL-10R2 can be essential in immune and barrier contexts, and
inflammatory challenge, viral infection, glial cells, or stress could make
IL10RB-bearing receptors active. Those settings were largely absent here. The
point estimate is thus a prediction for the specified basal recovered-neuron
snRNA-seq endpoint, not a claim that IL10RB biology is universally inert.
