# Nme7 direct DEG-count forecast

## Target and endpoint

- Target manifest: `[local file: Nme7.csv]` declares the single held-out perturbation `Nme7`.
- Endpoint: `n_degs` is the number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon `pvals_adj < 0.05`.
- Declared quantitative training scale: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]` contains 1,674 visible targets and omits `Nme7`.
- Declared expression table: `[local file: training_de_all_cell_groups.parquet]`.
- Canonical Nme7 biology: `biology_bundles/Nme7.json`, sha256 `cbc0e900b7294068fa4bc6d28b7d8b9555b57ad81680970ffc5baba4a6574036`, equivalently served by `characterization_bundle(target="Nme7", view="biology")`.

I did not inspect a held-out Nme7 expression signature or DEG count.

## Biology used

Nme7 is measurably expressed in the focal control population: 10,333 of 23,679 non-target nuclei express it, with 43.64% reach and mean expression 0.396 CP10k. That makes the transcript visible enough that a self-target RNA drop could in principle be observed.

The functional prior is still weak for a large postnatal nuclear-RNA response. The canonical card ties NME7 to gamma-tubulin-ring-complex-associated microtubule nucleation and basal-body/primary-cilium stability, but the direct mechanistic work is in proliferating cultured cells rather than P16-P44 thalamic neurons. Germline mouse loss produces congenital ciliary phenotypes, including hydrocephalus and laterality defects, but that is developmental and ependymal rather than an acute NeuN-positive thalamic-neuron endpoint. The card specifically leaves functional stock by harvest as indeterminate because NME7, gammaTuRC-bound NME7, and NME7-dependent ciliary material have no measured turnover or residence clock in postmitotic neurons.

The direct group-II Nme paralogs were not present in the 1,674-target focal count table, so I treated ciliary transport, ciliary signaling, transition-zone, and Hedgehog targets as the nearest assayed biological comparators rather than as exact operation analogs.

## Training evidence used

The focal count table is highly sparse: 1,205 of 1,674 visible targets are zero, the median is 0, the 75th percentile is 1, the 90th percentile is 2, and the few very large responses are spliceosome, proteasome, chromatin, nuclear-transport, or stress/proteostasis perturbations rather than ciliary regulators.

Same-experiment corpus evidence, interpreted as a semantic summary of the same training measurements rather than independent replication, contains a high-confidence Claim `claim:78305cab7c1c7b98458d`: represented ciliary transport, BBSome, transition-zone, ciliary-GPCR, and Hedgehog-adjacent perturbations in basal postnatal NeuN-positive neuronal snRNA-seq are largely buffered at the nuclear RNA level and do not form a coherent ciliary transcriptomic module.

I then checked the exact `151 TH Prkcd Grin2c Glut` Parquet rows for a focused ciliary/Hedgehog comparator set from that Claim plus related ciliary Findings:

```tsv
class	ciliary_or_Hh_training_targets	n_with_0_degs	n_with_1_deg	n_with_>1_degs
151 TH Prkcd Grin2c Glut	31	29	2	0
```

The two one-DEG cases were `Arl3` and `Ttc8`, and both significant rows were self-target rows:

```tsv
gene_target	significant_gene	logfoldchange	pvals_adj
Arl3	Arl3	-0.417792	0.0183572
Ttc8	Ttc8	-0.663124	0.0000306888
```

All other focal-class ciliary comparators I queried were exactly zero in the supplied count table, including `Alms1`, `Arl2bp`, `Armc9`, `B9d1`, `Cdon`, `Cep112`, `Cep290`, `Cfap69`, `Cspp1`, `Dync2h1`, `Dync2i1`, `Dzip1`, `Gli1`, `Gli2`, `Gpr161`, `Ift43`, `Ift88`, `Iqcb1`, `Kif3b`, `Lztfl1`, `Nin`, `Ptch1`, `Ptch2`, `Rpgr`, `Rpgrip1l`, `Smo`, `Spata7`, `Tbc1d32`, and `Ttc21b`. Among the zero comparators, the smallest adjusted p-values in this focal class were non-significant (`Arl3` non-self `Myt1`, 0.1025; `Spata7` `Lonp2`, 0.1160; `Rpgrip1l` `Dennd4b`, 0.1838), so these were not broad near-misses.

Corpus Findings for direct nearby ciliary targets were consistent with that row-level check: `Rpgrip1l` and `Tbc1d32` are reported as pan-measured neuronal blanks, and `Dzip1` failed to recover a Hedgehog or pan-ciliogenesis transcriptional program.

## Forecast

The best supported expectation is no downstream FDR-significant program in the focal thalamic class. The Nme7 transcript itself is visible, so a one-gene result driven solely by self-target RNA loss is possible, but the biology bundle gives no Nme7-specific evidence that its nuclear transcript should show a stronger edited-cell RNA drop than most other low-count ciliary genes. The ciliary comparator distribution also puts one-gene self-only outcomes below the zero mode.

I therefore predict:

```tsv
target_name	predicted_n_degs
Nme7	0
```
