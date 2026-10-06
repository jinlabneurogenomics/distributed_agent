# Xpo1 direct `n_degs` forecast

## Declared target and endpoint

- Target manifest: `Xpo1`.
- Cell class: `151 TH Prkcd Grin2c Glut`.
- Endpoint: number of focal-class measured genes with Wilcoxon `pvals_adj < 0.05`.
- The 1,674-row focal training table does not contain `Xpo1`, and I did not use any held-out `Xpo1` expression signature or held-out `Xpo1` DEG count.

## Xpo1 biology used

The canonical Xpo1 biology bundle supports a real, assay-window perturbation rather than a durable-stock null. XPO1/CRM1 is a soluble Ran-regulated export receptor for leucine-rich NES protein cargoes and RNA-containing cargo complexes, not a permanently installed structural product. The bundle's functional-stock card calls the harvest-time stock `likely_substantially_depleted`: a 7.444-day adult mouse thalamus Xpo1 protein lifetime makes the P16 to P37-P44 interval span about 2.8-3.8 protein lifetimes, leaving only about 14% to 7% of pre-edit receptor in a simple no-resupply model after successful editing.

The focal expression reach also supports observability. In matched non-target nuclei from `151 TH Prkcd Grin2c Glut`, Xpo1 was detected in 20,869 of 23,679 nuclei, with 88.13% of cells expressing and mean log1p CP10k 0.871. That argues against a prediction near the global training median of zero.

I discounted this upward evidence for three reasons in the same bundle: other export routes, especially Xpo7, can buffer selected cargoes; the closest functional neural evidence is injury/culture rather than a healthy thalamic P16 knockout; and a strong XPO1 lesion could be survivor-conditioned in the recovered nuclei.

## Training measurements used

The focal count table is extremely sparse overall:

- `n = 1674` training perturbations
- median `n_degs = 0`
- 75th percentile `= 1`
- 95th percentile `= 18`
- 99th percentile `= 430`
- only 15 perturbations had at least 500 DEGs

Xpo1 sits biologically near the rare high-response transport and RNA-processing tail, not near the global bulk. The most relevant focal counts were:

| perturbation | 151 TH Prkcd Grin2c Glut `n_degs` | interpretation |
| --- | ---: | --- |
| `Tpr` | 1768 | nuclear-pore-basket / mRNA-export-adjacent high ceiling |
| `Tnpo3` | 618 | importin-beta-family SR-protein transport receptor |
| `U2af2` | 828 | splice/RNA-processing response scale |
| `Rnpc3` | 868 | splice/RNA-processing response scale |
| `Hnrnpu` | 733 | RNA-processing response scale |
| `Cdc40` | 624 | spliceosome response scale |
| `Thoc1` | 303 | export/RNA-processing lower high anchor |
| `Xpo7` | 0 | broad alternative exporter that is quiet in this focal class |
| `Ranbp2` | 0 | nuclear-pore transport factor that is quiet in this focal class |

I then filtered the declared training Parquet to the focal class, giving 28,891,566 rows over the same 1,674 perturbations and 17,259 measured genes. Exact focal profiles confirmed that `Tpr` had 1,315 up and 453 down significant genes; `Tnpo3` had 305 up and 313 down; the RNA-processing anchors were of similar magnitude (`Rnpc3`, `U2af2`, `Hnrnpu`, and `Cdc40` from 624 to 868 DEGs); and `Xpo7`/`Ranbp2` had no focal gene at FDR 0.05. In the same focal Parquet, `Tpr` and `Tnpo3` shared 265 significant genes, 260 of them in the same direction, and the packaged corpus independently summarized `Tpr` as the strongest same-direction FDR-overlap neighbor of `Tnpo3`.

The packaged training-target summaries added two useful boundaries without using an Xpo1 target profile: `Tpr` recurrently changed nuclear transport and NXF1-adjacent export genes and was a very large thalamic/midbrain responder, while `Xpo7` stayed sparse and `Ranbp2` had broad responses in other cell classes but not in this focal thalamic class.

## Synthesis

I placed Xpo1 below `Tpr` because disrupting a nuclear pore basket creates a very broad export/RNA-processing/stress state and because XPO1 has cargo-specific bypass routes; `Xpo7` and `Ranbp2` show that nuclear transport annotations alone can be FDR-flat in this focal population. I placed it near `Tnpo3`/spliceosome anchors rather than near zero because Xpo1 is highly expressed in the focal population, its protein should substantially turn over during the experiment, and the loss affects a recurring nuclear-export receptor with many cargoes.

The resulting point is a high-tail but not Tpr-scale response, just above the receptor-level `Tnpo3` anchor and below the stronger spliceosome anchors:

`predicted_n_degs = 650`
