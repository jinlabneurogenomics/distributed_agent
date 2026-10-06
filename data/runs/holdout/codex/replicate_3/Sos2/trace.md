# Direct DEG-count forecast for Sos2

## Target and endpoint

- Target: `Sos2`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: `n_degs`, the count of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Target signature/outcome: not used

## Evidence that determined the forecast

The focal training count table is sparse. Among 1,674 observed training targets in
`151 TH Prkcd Grin2c Glut`, 1,205 have `n_degs = 0`, the median is 0, and only
106 have at least 10 significant genes. This makes the unconditional local prior
already concentrated near 0 rather than near a tens-to-hundreds response.

The biology bundle points to a realized but buffered perturbation. `Sos2` is a
dynamic receptor-linked Ras GEF, and its functional protein stock is expected to
clear within the P16-to-P37/P44 edit window. The exact in-assay reach is present
but not broad: in the matched non-target nuclei for this class, Sos2 expression
was detected in 10,374 of 23,679 nuclei, with 43.81% of nuclei expressing and
mean expression of 0.391 CP10K. The same bundle also contains the strongest
downward bearing: Sos1 is a close paralog and young mouse neurons lacking Sos2
preserved tested ERK responses and hippocampal LTP, so loss of Sos2 alone is
expected to be heavily buffered in at least several neural Ras/ERK outputs.

I therefore treated same-class Ras/MAPK training perturbations as the relevant
quantitative comparators:

| training target | same-class `n_degs` |
| --- | ---: |
| `Sos1` | 0 |
| `Kras` | 0 |
| `Hras` | 0 |
| `Raf1` | 0 |
| `Map2k2` | 0 |
| `Mapk1` | 0 |
| `Ptpn11` | 0 |
| `Rasa2` | 0 |
| `Spred1` | 0 |
| `Spred2` | 0 |
| `Shoc2` | 1 |
| `Braf` | 4 |
| `Map2k1` | 4 |

The full Parquet profiles confirmed that this cohort is not hiding a larger
shared FDR-level program: in a 13-node Ras/MAPK profile comparison, 10 nodes had
no significant features and the other 3 had 1 to 4 significant features. The
few significant downstream rows were all negative and were limited to a small
core-ERK tail: `Braf` significantly changed `Atp2a2`, `Ptpn5`, `Vgf`, and
`Unc13a`; `Map2k1` changed `Vgf`, `Ptpn5`, `Etv5`, and `Unc13a`; and `Shoc2`
changed only `Vgf`. Upstream neurotrophic/receptor examples were similarly
quiet in the same table: `Ntrk1`, `Ntrk3`, `Fgfr1`, `Fgfr2`, `Fgfr3`, `Erbb3`,
and `Erbb4` were 0, while `Ntrk2` was 3 with one self-target call and two
downstream genes.

The stock card keeps Sos2 from being a pure no-engagement prior: if edited, it
should lose operative protein by harvest. But the exact focal reach is modest,
Sos1 provides paralog buffering, the closest assayed paralog `Sos1` had
`n_degs = 0`, and even loss of stronger central Ras/ERK machinery produced only
0 to 4 BH-significant genes in this same thalamic class. I therefore rounded the
forecast to the Ras-pathway mode rather than to the weak nonzero `Braf`/`Map2k1`
tail.

## Point prediction

`Sos2`: 0
