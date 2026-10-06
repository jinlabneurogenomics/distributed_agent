# Igf2r n_degs forecast

## Target and endpoint

- Target: `Igf2r`.
- Endpoint: `n_degs` in `151 TH Prkcd Grin2c Glut`, counted as measured genes with BH-adjusted Wilcoxon `p < 0.05`.
- The held-out `Igf2r` differential-expression signature and count were not used.

## Evidence used

### Igf2r biology bundle

- The canonical biology card identifies IGF2R/CI-MPR as a recycling trans-Golgi, endosomal, and surface receptor that sorts mannose-6-phosphate hydrolase cargo and clears IGF2.
- The functional-stock adjudication calls operative IGF2R `likely_substantially_depleted` by the P37-P44 harvest: a P16 disruptive edit stops resupply, PC12 CI-MPR turns over on an approximately day scale, and adult hippocampal AAV-Cre reduced neuronal IGF2R protein and function within two weeks.
- The best matched in-vivo functional evidence is neuronal but hippocampal rather than thalamic. M6PR can overlap for lysosomal enzyme targeting but does not replace all IGF2R functions or the IGF2 clearance arm.
- Exact baseline reach in the focal population was moderate, not ubiquitous: `Igf2r` RNA was detected in 12,641 of 23,679 non-target `151 TH Prkcd Grin2c Glut` nuclei, 53.38%, with mean CP10k 0.527.

### Training-count scale

The declared `151 TH Prkcd Grin2c Glut` count table contained 1,674 measured training perturbations. It was heavily zero-inflated:

- 1,205 / 1,674 training targets had `n_degs = 0`.
- The 80th percentile was 1 DEG; the 90th percentile was 2 DEGs.
- Only 106 targets had at least 10 DEGs, and only 43 had at least 100.

That makes 0-2 DEGs the default regime unless the held-out biology is close to a core, broad transcriptional stress perturbation.

### Selected training perturbations

I read the declared Parquet for a biology-selected lysosome, cargo-receptor, endosomal-trafficking, and IGF/insulin signaling panel in the exact focal group. Each selected target had 17,259 measured rows in `151 TH Prkcd Grin2c Glut`.

| target | 151 q<0.05 genes | 151 q<0.10 genes | interpretation for Igf2r |
|---|---:|---:|---|
| `Sort1` | 0 | 1 | Closest receptor/cargo-sorter analogy among represented training genes; its only 151 near-hit was `Sort1` itself at q=0.094, and packaged Findings report no lysosomal, autophagy, UPR/ISR, or AP-1 induction after `Sort1` loss. |
| `Igf1r` | 0 | 0 | IGF receptor signaling was silent in this basal postnatal neuronal RNA readout. |
| `Insr` | 0 | 0 | Insulin receptor signaling was also silent across recovered neuronal groups. |
| `Atg5` | 0 | 0 | Core autophagy loss was nearly flat in this group. |
| `Lamp2` | 0 | 2 | Lysosomal membrane perturbation stayed below the q<0.05 endpoint in 151. |
| `Atp6v0a1`, `Ctsb`, `Gaa`, `Ppt1`, `Psap`, `Tmem106b`, `Atp13a2`, `App`, `Grn` | 1 each | 1 each | In this panel the q<0.05 hit was the perturbed gene itself, not a downstream lysosomal-stress program. |
| `Atp6ap2` | 2 | 2 | Small V-ATPase-associated response: self plus `Atp6v0a1`. |
| `Mtor` | 2 | 5 | Small mixed 151 program, still on the 0-2 count scale at q<0.05. |
| `Cltc` | 3 | 7 | Endocytosis/core traffic was weak in 151, stronger elsewhere. |
| `Vps35` | 17 | 31 | Retromer loss produced a real 151 program and serves as a local upper bound for broader endosomal cargo retrieval failure. |
| `Vps54` | 31 | 45 | GARP/EARP loss was another 151-active broader vesicle-trafficking upper bound. |
| `Tsc2` | 86 | 128 | Broad mTORC1 activation state, not a direct Igf2r analogue. |
| `Rab7` | 501 | 643 | Severe late-endosome perturbation with lysosomal, sterol, proteasome, and stress programs; an upper-bound state rather than a cargo-receptor estimate. |

The same-experiment Findings are consistent with the raw counts but are not independent measurements. They distinguish broad core-traffic lesions (`Rab7`, `Vps35`, `Vps54`) from more selective lysosomal or cargo-receptor perturbations (`Sort1`, `Gaa`, `Ctsb`, `Atp6v0a1`, `Atg5`, `Lamp2`) that were buffered or singletons in the acute neuronal snRNA-seq endpoint.

## Synthesis

Igf2r should lose operative receptor stock within the assay window, and the target is expressed in enough 151 nuclei that a fully penetrant nuclear response could be detected. I therefore would not force the forecast to zero solely because receptor pathways such as `Igf1r` and `Insr` were quiet.

The stronger downward evidence is response scale and operation breadth. IGF2R is a cycling cargo/clearance receptor with overlap from M6PR and extracellular hydrolase cross-correction in a mosaic tissue. The measured training perturbations most analogous to single lysosomal cargo, lysosomal enzymes, V-ATPase subunits, and receptor-sorter biology mostly landed at 0 or 1 q<0.05 genes in 151, often only the self transcript. In contrast, the 17-501 DEG programs came from loss of retromer, GARP, Rab7, or Tsc2, which perturb whole trafficking or growth-control states broader than loss of one M6P/IGF2 receptor.

I place Igf2r above a pure null because the receptor is expressed in the focal class and functional stock should clear by harvest, but I keep it at the singleton end of the observed receptor/lysosome distribution rather than projecting a Vps35/Vps54/Rab7-like stress state.

Point prediction: `1`.
