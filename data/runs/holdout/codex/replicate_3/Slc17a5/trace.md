# Direct endpoint forecast trace

Target: `Slc17a5` in `151 TH Prkcd Grin2c Glut`.

Endpoint: number of measured genes in the focal cell group with BH-adjusted Wilcoxon `p < 0.05`.

## Declared target biology

I used the declared biology-only `Slc17a5` bundle, not the held-out target profile. In the focal non-target nuclei, `Slc17a5` was detected in 11,054 of 23,679 nuclei (`46.68%`) with mean log1p CP10k `0.2918`, so the transcript has partial but real reach in the assayed thalamic population.

The bundle identifies the perturbed function as sialin in lysosomal membranes plus a neuronal vesicular acidic amino-acid/NAAG transport pool. A P16 disruptive edit stops new transporter supply but does not acutely disable pre-existing membrane sialin; neuronal lysosomal-proteome turnover proxies nevertheless make substantial stock depletion by the P37-P44 harvest plausible over 21-28 days. The main downward qualifiers are endpoint coupling, not stock: the mouse phenotype evidence is germline/developmental and heavily glial/myelination-related, adult thalamic signal is regionally restricted, target-specific sialin residence time is unknown, and no same-context compensator was proven or excluded.

## Focal training measurements

The declared `151 TH Prkcd Grin2c Glut` training count table is very sparse:

- 1,205 / 1,674 training perturbations have `0` DEGs.
- 276 have exactly `1` DEG.
- The quartiles are `0, 0, 1`; only 106 have at least 10 DEGs.
- Recomputing the focal Parquet rows showed 1,442 / 1,674 profiles had no downstream significant gene after excluding the self-target transcript, and 237 profiles had exactly one significant row that was self-only.

The closest focal lysosome/endolysosome examples looked self-only or flat at `p_adj < 0.05`:

| target | n_degs | downstream DEGs excluding self | matched perturbed nuclei |
|---|---:|---:|---:|
| `Atp6v0a1` | 1 | 0 | 197 |
| `Atp6v1a` | 0 | 0 | 76 |
| `Ctsb` | 1 | 0 | 207 |
| `Lamp2` | 0 | 0 | 203 |
| `Ppt1` | 1 | 0 | 171 |
| `Psap` | 1 | 0 | 128 |
| `Scarb2` | 1 | 0 | 146 |
| `Sort1` | 0 | 0 | 124 |
| `Tmem106b` | 1 | 0 | 158 |

Broader trafficking perturbations provide a ceiling rather than a scale-matched center. `Vps35` had 17 focal DEGs and `Vps54` had 31, while `Rab7` was the large endolysosomal outlier with 501 DEGs, including a recurrent late-endosomal/lysosomal compensation module. Packaged same-experiment reports also treat `Rab7` as a strong generalized late-endosome/lysosome stress state and show that `Vps35` and `Vps54` are narrower, thalamus-biased trafficking responses rather than a universal lysosomal rescue program.

## Synthesis

Realized `Slc17a5` loss in target-positive thalamic neurons is plausible, so I did not assign a hard zero. But it is a single lysosomal/vesicular substrate transporter with partial focal reach, and the focal training perturbations that directly hit lysosomal membrane, hydrolase, autophagy, or sorting-client genes mostly had no downstream FDR-scale response. The multi-gene comparators perturb broader endosomal trafficking hubs and therefore bracket the possibility of stress detection without matching the expected scale of sialin loss.

I therefore forecast essentially no downstream DEGs and allowed one possible row for the target transcript itself or a minimal secondary marker. The integer point forecast is:

`predicted_n_degs = 1`
