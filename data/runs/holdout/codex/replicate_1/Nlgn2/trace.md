# Nlgn2 direct DEG-count forecast

## Target and endpoint

- Manifest target: `Nlgn2`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in the focal held-out `Nlgn2` perturbation with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The declared count table contains 1,674 focal training perturbations and intentionally does not contain `Nlgn2`.

## Biological prior

The target card supports real target engagement by the 21-28 day post-edit harvest window but not a large acute transcriptional program.

- Exact focal reach is high: `Nlgn2` is available in the assayed expression matrix, with 22,782 of 23,679 non-target focal nuclei expressing it, `96.2118%` of cells, mean raw UMI `4.8101`, mean CP10K `3.0061`, and pseudobulk CPM `301.4677`.
- The operative entity is an inhibitory postsynaptic neuroligin adhesion protein/complex. The functional-stock adjudication calls stock at harvest `likely_substantially_depleted`: a disruptive edit should stop NLGN2 resupply, its measured synaptic-protein half-life is days rather than weeks, and adult conditional deletion made NLGN2 undetectable after about 2-3 weeks.
- The same card leaves endpoint latency unresolved. The direct thalamic loss phenotype came from constitutive loss, while adult conditional cortical deletion separated molecular NLGN2 clearance at 2-3 weeks from larger inhibitory-synapse and transmission changes at roughly 6-7 weeks. That makes a measurable survivor-nucleus effect plausible, but it weighs against borrowing counts from fast cell-state regulators or essential RNA/proteostasis genes.
- The selected same-experiment corpus had no `Nlgn2` Findings, Claims, or explicit comparator references, so no Nlgn2 report-derived outcome semantics were used.

## Training-count scale

The complete focal training distribution is extremely zero-heavy and right-skewed:

- `1205 / 1674` perturbations have `0` DEGs.
- Median = `0`; 75th percentile = `1`; 90th percentile = `2`; 95th percentile = `18`.
- The mean is `14.05`, but it is dominated by a small tail of broad high-yield regulators.

I used typed Nlgn2 analog nomination against the actual training universe, not a symbol filter. The leading specific candidates are centered on neuroligin/neurexin adhesion and adjacent postsynaptic scaffolds. Their focal counts were:

| set | genes | counts |
| --- | --- | --- |
| top neurexin/neuroligin specific tier | `Nlgn3`, `Dlg4`, `Nrxn2`, `Nrxn1`, `Nrxn3`, `Shank3`, `Lrrtm4`, `Lrrtm1`, `Lrrtm3` | `1, 1, 0, 1, 0, 2, 0, 1, 0` |
| retained inhibitory/postsynaptic support set | above plus `Gphn`, `Grm1`, `Dlgap4`, `Grm5`, `Arhgap32`, `Magi2`, `Homer2`, `Arhgef9` | nine 0-count, six 1-count, two 2-count perturbations |

The same analog search did surface broad fallback genes with large responses, for example `Grin1`, but those came through generic glutamatergic/synaptic annotations rather than the Nlgn2-proximal inhibitory adhesion tier and were not given positive weight for the point count.

## Matched Parquet check

Filtering the declared training Parquet to the 17 retained analogs and `151 TH Prkcd Grin2c Glut` found 17,259 measured rows for each analog and exactly the same small significant sets:

- self-target-only profiles: `Arhgef9` 1, `Dlg4` 1, `Grm1` 1, `Nlgn3` 1, `Nrxn1` 1.
- one isolated non-self-only profile: `Lrrtm1` 1 via `R3hdm2`.
- two-gene weak profiles: `Dlgap4` 2 via `Dlgap4` and `Vgf`; `Shank3` 2 via `Shank3` and `Uba5`.
- null profiles: `Arhgap32`, `Gphn`, `Grm5`, `Homer2`, `Lrrtm3`, `Lrrtm4`, `Magi2`, `Nrxn2`, `Nrxn3`.

The profile-cohort diagnostic over these 17 genes found no broad shared response state: the mean top-tail overlap coefficient was `0.0309` for positive features and `0.0387` for negative features, and significant-program overlap was `0`. Thus this cohort supports a weak count scale rather than a recurring signed Nlgn2-like DEG program.

## Synthesis

The biology argues against a pure assay-failure zero because Nlgn2 is expressed in nearly all focal nuclei and functional NLGN2 should be depleted by harvest. The matched training measurements argue just as strongly against a multi-gene response: the nearest specific adhesion/scaffold perturbations almost always have 0-1 DEGs and top out at 2, often only through their self transcript.

I therefore put the point at the modal nonzero weak-response value:

`predicted_n_degs = 1`
