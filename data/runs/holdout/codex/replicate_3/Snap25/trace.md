# Snap25 direct DEG-count forecast

## Target and endpoint

- Target: `Snap25`, the single row in the declared holdout manifest.
- Population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `pvals_adj < 0.05` in the focal class.
- Prediction: `1`.

## Evidence used

### Snap25 biology-only characterization

The declared Snap25 bundle and `characterization_bundle(target="Snap25", view="biology")` both exposed the same outcome-blind biology:

- In-assay focal reach is very high: Snap25 was detected in 23,673 of 23,679 non-target nuclei in `151 TH Prkcd Grin2c Glut`, with mean raw UMI 35.03 and mean log1p CP10k 3.064.
- SNAP-25 is a dynamic presynaptic SNARE component required for fast calcium-triggered synaptic-vesicle fusion.
- The bundle adjudicates the 21-28 day P16-to-harvest window as long enough for substantial depletion of pre-edit SNAP-25 protein stock in successfully edited cells.
- The nearest biological phenotype evidence supports a continuing postnatal neuronal requirement, but in cortical projection neurons rather than this thalamic glutamatergic class.
- The bundle explicitly treats survivor conditioning as a possible attenuator of the nuclear RNA response.

I used this as evidence that the perturbation should be realized in the focal neurons and that the self transcript is measurable, not as evidence for a large downstream count.

### Training count table

The focal training table contains 1,674 observed targets and is extremely zero-heavy:

- median `n_degs`: 0
- 75th percentile: 1
- 90th percentile: 2
- zero fraction: 0.7198

The hand-selected presynaptic fusion/release comparators in the same endpoint were nearly all flat:

| comparator class | targets inspected | focal `n_degs` |
|---|---|---|
| core SNARE/Munc18/fusion | `Stx1b`, `Stxbp1`, `Nsf` | 0, 1, 0 |
| vesicle Ca2+ sensor / priming | `Syt2`, `Unc13a`, `Unc13b`, `Unc13c` | 0, 0, 0, 0 |
| complexin / active-zone scaffolds | `Cplx1`, `Cplx2`, `Pclo`, `Bsn` | 1, 0, 0, 0 |
| Ca-channel and synaptic vesicle / synapse comparators | `Cacna1a`, `Cacnb2`, `Syp`, `Syn1`, `Syn2`, `Sv2a`, `Dlg4`, `Shank3`, `Nrxn1`, `Nrxn2`, `Nrxn3` | 0, 0, 1, 1, 0, 1, 1, 2, 1, 0, 0 |

Across these 22 same-endpoint perturbations, the mean was 0.409 DEGs and the maximum was 2.

### Focal Parquet and profile evidence

The declared Parquet scan for the 22 mechanistic comparators in `151 TH Prkcd Grin2c Glut` read 379,698 target-gene rows and found only 9 rows with `pvals_adj < 0.05`. Eight of the nine were the perturbed target's own transcript:

`Cplx1`, `Dlg4`, `Nrxn1`, `Shank3`, `Stxbp1`, `Sv2a`, `Syn1`, and `Syp`.

The only non-self significant row in this comparator set was `Uba5` after `Shank3` perturbation. Thus the one-count observations near Snap25's presynaptic biology mostly reflected target-transcript detectability, not a repeated downstream program.

I also compared the same 22 nodes by signed focal profiles against the full 1,674-target eligible training universe. All 22 profiles were present. Response activity was 14 nodes with no significant features and 8 with 1-9 significant features. In the exact cohort projection, positive top-tail overlap was weak across all 231 available pairs, with median 0.075, and there was no positive significant-program overlap. The negative-tail median was 0.13, but FDR-level negative-program overlap was still zero where defined. This supported the interpretation that single presynaptic release perturbations do not form a broad coherent nuclear RNA state in this focal population.

### Same-experiment corpus context

The packaged same-experiment corpus was consistent with the direct table/profile read. The Cplx1 context contributed to a high-confidence claim that most represented acute presynaptic vesicle-cycle and active-zone perturbations lack broad downstream neuronal nuclear RNA responses, with Stxbp1 as a modest transcriptionally visible outlier in other classes. In the focal target count table, even `Stxbp1` had `n_degs = 1`.

## Synthesis

I forecast a singleton DEG rather than zero because Snap25 has almost universal measured baseline expression in the focal class, and many close low-count release/synapse comparators that are highly expressed enough for self detection landed at exactly one FDR-significant row. I did not extrapolate to a larger response from SNAP-25's essential vesicle-fusion role because the declared training counts, focal Parquet rows, bounded profile cohort, and same-experiment presynaptic corpus all showed that acute single-gene loss in this machinery is usually transcriptionally flat in survivor-conditioned thalamic nuclear RNA.

`predicted_n_degs = 1`
