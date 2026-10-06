# Pomp n_degs forecast

## Target and endpoint

- Target: `Pomp`
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with BH-adjusted Wilcoxon `p < 0.05`
- Forecast: `560`

## Evidence used

### Declared biology bundle

The canonical `Pomp` bundle identifies POMP as a dedicated, assembly-consumed chaperone for standard 20S proteasome and immunoproteasome formation. Loss of new POMP synthesis should therefore block new 20S core assembly rather than acutely destroy mature cores that were already present before editing.

The 21-28 day edit-to-harvest interval is long compared with the mature-core half-life anchors in the bundle, so a functional POMP lesion should have time to reduce new proteasome-core supply in assayed juvenile neurons. The main downward uncertainty is that mature neuronal 20S/26S particles may persist longer than the cultured-cell half-lives, and a survivor-conditioned snRNA-seq readout can preferentially retain incompletely stressed nuclei.

The exact reach entry for the target is compatible with an assay-visible effect: in matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, `Pomp` RNA was detected in 13,943 / 23,679 nuclei, or 58.88%, with mean log1p CP10K 0.404. This establishes target expression reach but was not used as an editing-efficiency weight.

### Training endpoint counts

The declared training count table has 1,674 measured targets for the same class. It is extremely zero-inflated:

- median: 0 DEGs
- 75th percentile: 1 DEG
- 95th percentile: 18 DEGs
- 99th percentile: 436.48 DEGs

Direct proteasome-subunit lesions were rare and high in that table:

- `Psmb4`: 742 DEGs
- `Psmc1`: 430 DEGs

Most upstream or accessory proteostasis/stress genes did not share that scale in the same endpoint:

- `Nfe2l1`: 0
- `Nfe2l2`: 0
- `Atf6`: 0
- `Vcp`: 2
- `Hspa5`: 5
- `Hspa8`: 9
- `Usp48`: 10
- `Sqstm1`: 1
- `Ube3a`: 0
- `Ube2e2`: 0

I therefore treated `Pomp` as a direct proteasome-assembly lesion bracketed by `Psmb4` and `Psmc1`, not as a generic proteostasis-regulator perturbation.

### Same-experiment report/corpus context

The packaged `Psmb4` report interprets the `Psmb4` response as core proteasome insufficiency, with broad induction of proteasome bounce-back, integrated-stress/heat-shock/redox, autophagy/lysosomal, and p53-like arms plus repression of synaptic and mature neuronal-function transcripts. It names `Psmc1` as the top data-driven neighbor of `Psmb4`, with same-sign agreement for almost all shared FDR<0.10 features.

The packaged `Psmc1` report reciprocally treats `Psmb4` as the only strong positive `Psmc1` signature neighbor among assayed 26S proteasome components. It also notes that `Nfe2l1`, `Vcp`, `Uchl1`, and `Uba5` did not phenocopy `Psmc1`, supporting the distinction between direct proteasome-machine damage and related but lower-equivalence perturbations.

### Parquet/profile checks

Filtering the declared Parquet to `151 TH Prkcd Grin2c Glut` reproduced the direct-count anchors:

- `Psmb4`: 742 significant rows among 17,259 measured genes, with 62 matched perturbed and 23,679 matched control nuclei
- `Psmc1`: 430 significant rows among 17,259 measured genes, with 89 matched perturbed and 23,679 matched control nuclei

A run-local profile-neighborhood projection of `Psmb4` and `Psmc1` into the 1,674 eligible training targets found that they are each other's strongest sparse positive-overlap neighbor in this class. That supports using them as the close empirical scale donors, while the other neighbors were either much less active in the count table or represented more general stress/RNA-processing states.

## Forecast synthesis

`Pomp` should be substantially above the screen median because it is not an upstream sensor: POMP supplies new 20S cores, has no close within-mouse paralogue in the biology bundle, is expressed in the exact focal population, and should decline functionally over the P16-to-P37/P44 interval. Its closest measured training biology is `Psmb4`/`Psmc1`, whose exact endpoint counts are 430-742 DEGs.

I placed `Pomp` just below the log-space center of `Psmb4` and `Psmc1` rather than above `Psmb4` because the lesion is an assembly-supply defect buffered by pre-existing mature cores, and the target-specific bundle lacks a matched neuronal Pomp loss phenotype. A several-hundred-gene response is still more plausible than the zero-to-low counts of stress regulators such as `Nfe2l1`, `Atf6`, and `Vcp`, because those perturbations remove sensors or branches under basal conditions rather than preventing new 20S core biogenesis itself.

The resulting point forecast is:

```text
Pomp n_degs = 560
```

No held-out `Pomp` expression signature or target DEG count was used.
