# Ptpa DEG-count forecast

## Target and endpoint

- The one-row holdout manifest contains `Ptpa`.
- The requested endpoint is `n_degs` in `151 TH Prkcd Grin2c Glut`: the count of measured genes with Wilcoxon BH-adjusted `p < 0.05`.
- The declared biology bundle resolves the packet symbol `Ptpa` to official mouse `Ptpra`, encoding the receptor-type protein tyrosine phosphatase PTPRA/RPTPalpha, not the PP2A phosphotyrosyl-phosphatase activator gene.

## Biology used

- `Ptpa`/`Ptpra` is well expressed in the exact focal population: 20,151 of 23,679 matched non-target nuclei express it, with mean CP10K 1.423 and pseudobulk CPM 142.16. Low focal RNA reach therefore is not the main reason to expect a null.
- The characterized operative product is a renewable transmembrane tyrosine phosphatase that dephosphorylates regulatory phosphotyrosines and activates Src-family kinases, including Src and Fyn.
- Mouse Ptpra germline loss produces neural phenotypes in other neural settings, including hippocampal migration, long-term potentiation, learning, and CNS myelination abnormalities, so a neural role is plausible.
- The functional-stock card judged the P16-to-P37/P44 realization uncertain: the edit should stop new PTPRA synthesis, but pre-existing membrane receptor protein initially persists, target-specific degradation was demonstrated only in mismatched cancer/heterologous cells, and no mature-neuron half-life was found. Thus the biology supports target presence and possible pathway impact, but not a guaranteed broad acute thalamic transcriptional state.

## Training measurements used

The focal training count table is strongly zero-inflated:

| statistic | value |
| --- | ---: |
| targets | 1,674 |
| zero-DEG targets | 1,205 |
| median | 0 |
| 75th percentile | 1 |
| 90th percentile | 2 |
| 95th percentile | 18 |
| maximum | 2,677 |

I therefore interpreted candidate perturbations by biology rather than by the high-count tail, which is dominated by chromatin, splicing, proteostasis, and core transcriptional regulators. In the exact `151 TH Prkcd Grin2c Glut` Parquet slice, each comparator below had 17,259 measured genes:

| visible training perturbation(s) | focal `n_degs` | interpretation |
| --- | ---: | --- |
| `Fyn` | 0 | direct Src-family effector named in the PTPRA biology bundle; no significant survivor RNA program |
| `Ptpn1`, `Ptpn11` | 0, 0 | tyrosine-phosphatase comparators; no downstream DE support |
| `Ptprd`, `Ptprf`, `Ptpro`, `Ptprt`, `Ptprc` | 0 each | receptor-PTP perturbations in the table were transcriptionally quiet |
| `Ptprm`, `Ptprn`, `Ptprn2` | 1 each | the sole significant gene was the perturbed receptor-PTP transcript itself |
| `Dab1`, `Mapk1` | 0, 0 | neuronal signaling relays downstream or adjacent to receptor/Src-family pathways were quiet |
| `Epha4`, `Ntrk2` | 1, 3 | neuronal receptor-signaling comparators showed only a self-transcript hit for `Epha4`, and self plus two other genes for `Ntrk2` |

The exact significant rows for the nonzero low-count receptor/signaling comparators were:

| perturbation | significant focal genes |
| --- | --- |
| `Epha4` | `Epha4` |
| `Ntrk2` | `Ntrk2`, `Atp2a2`, `Vgf` |
| `Ptprm` | `Ptprm` |
| `Ptprn` | `Ptprn` |
| `Ptprn2` | `Ptprn2` |

These measurements made the closest visible scale 0 to 1 DEG, with occasional self-transcript-only counts. A much larger response remains possible for an expressed signaling target, but the available focal data gave no reason to transfer the 383-DEG `Ctnnb1` state or the very large core-regulator states to PTPRA.

## Forecast

The final point estimate is **0 DEGs**. The exact target is expressed and biologically reachable, but existing-stock uncertainty and the visible phosphotyrosine/receptor-signaling comparators put the most likely BH-significant count at the zero-DEG mode, with the main upward uncertainty being a possible isolated self-transcript hit.
