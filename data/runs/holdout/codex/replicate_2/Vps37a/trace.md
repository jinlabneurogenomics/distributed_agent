# Direct n_degs forecast for Vps37a

## Target and endpoint

- Target: `Vps37a`
- Focal population: `151 TH Prkcd Grin2c Glut`
- Endpoint: number of measured genes with BH-adjusted Wilcoxon `p < 0.05`
- Forecast: `4`

## Biology used

The declared Vps37a biology bundle supports both target reach and realization in the focal assay window:

- Focal expression is high: `Vps37a` is detected in `23163 / 23679` matched non-target nuclei in `151 TH Prkcd Grin2c Glut` (`97.82%`), with mean raw UMI `5.12`, mean CP10K `3.29`, and pseudobulk CPM `321.12`.
- VPS37A is a renewable ESCRT-I-family subunit with a separable UEVL-dependent autophagosome-closure function.
- Functional stock was adjudicated as likely substantially depleted by P37-P44 after a P16 disruptive edit: the pre-edit ESCRT-I pool should initially persist, but ESCRT-dependent endosomal sorting and autophagosome closure are recurrent operations and the 21-28 day interval should span turnover of most ordinary brain protein stock.
- The same bundle leaves an important attenuation term: VPS37B-D can occupy related ESCRT-I assemblies, and no matched thalamic-neuron experiment demonstrated whether they do or do not compensate for the VPS37A-specific state.

I treated that as a real but not obligatorily large survivor-snRNA perturbation: the target is present and the edited product should be depleted, while both family redundancy and survivor conditioning can shrink the recovered transcriptome.

## Training measurements used

The declared 151-TH training count table has `1674` held-in perturbations and is sharply zero-inflated:

- median `n_degs = 0`
- 75th percentile `= 1`
- 90th percentile `= 2`
- 95th percentile `= 18`
- `469 / 1674` are nonzero
- `106 / 1674` have at least 10 DE genes
- `59 / 1674` have at least 50 DE genes

No same-complex ESCRT-I subunit named in the Vps37a card was available as a quantitative donor in this training table: `Tsg101`, `Vps28`, `Mvb12a`, `Mvb12b`, `Ubap1`, and the paralogous `Vps37b/c/d` targets were absent.

I therefore bracketed Vps37a with the closest held-in autophagy/ESCRT/trafficking perturbations available in the exact count table and with their matched `151 TH Prkcd Grin2c Glut` Parquet profiles:

| comparator | reason considered | 151 TH `n_degs` |
| --- | --- | ---: |
| `Chmp4b` | ESCRT-III / membrane scission | 0 |
| `Atg5` | core autophagy conjugation | 0 |
| `Becn1` | autophagy nucleation | 0 |
| `Rb1cc1` | autophagy initiation, partial Becn1/Atg5 convergence in atlas reports | 4 |
| `Vps35` | endosomal retromer trafficking active in the same focal class | 17 |
| `Vps54` | GARP/EARP trafficking active in the same focal class | 31 |
| `Vps53` | GARP/EARP partner of Vps54 | 0 |
| `Washc4` | Retriever/WASH neighbor of Vps35 biology | 0 |
| `Stx16` | TGN/endosomal SNARE | 1 |
| `Stx5a` | TGN/ER SNARE | 0 |
| `Mtor` | autophagy suppressor | 2 |
| `Rubcn` | autophagy regulator | 0 |
| `Rab7` | broad endolysosomal hub and strong positive neighbor of Vps35/Vps54 reports | 501 |
| `Tsc2` | broad mTOR/autophagy-growth stress state | 86 |

The same-experiment corpus supported using the core autophagy/ESCRT entries as near, quiet comparators rather than ignoring their zeros: packaged findings state that `Atg5` did not recover a canonical autophagy, lysosome, p62, proteasome-rebound, or UPR-ISR program; `Becn1` had only a very restricted response and did not induce a robust SQSTM1/LC3-GABARAP/LAMP/UPR-ISR program; `Rb1cc1` was sparse and canonical autophagy/lysosome perturbations did not phenocopy it as a class; and `Chmp4b` produced no robust recurrent ESCRT/autophagy/cargo signature.

The `Vps35`, `Vps54`, and `Rab7` observations show that 151 TH neurons can mount endosomal/lysosomal trafficking responses, but I downweighted them for magnitude. Packaged findings describe `Vps35` as a restricted receptor/excitability/calcium/synaptic-neurite program rather than a bulk lysosomal response, and `Vps54` as a mature-neuronal-signaling/axon-neurite downshift without canonical lysosomal rescue. In the matched Parquet comparison, `Vps35` and `Vps54` shared only one significant negative feature at BH 0.05, so their 17- and 31-gene burdens are broader 151-TH trafficking bounds rather than a coherent ESCRT-I/autophagosome-closure module to transfer wholesale.

## Synthesis

I placed Vps37a above the global median because the target transcript is broadly present in the exact focal population, the bundle argues that VPS37A functional stock should substantially decline by harvest, and a selective VPS37A UEVL lesion is postnatally consequential in mouse neural tissue. I placed it far below the `Rab7`/`Tsc2` stress programs and below `Vps35`/`Vps54`, because the available core autophagy and ESCRT-III donors are nearly silent in this exact population and the endosomal responders express non-identical receptor/synaptic states.

The resulting point is a low single-digit response, closest to the sparse `Rb1cc1` autophagy count rather than to the 17-31-gene Vps35/Vps54 trafficking counts:

```tsv
target_name	predicted_n_degs
Vps37a	4
```
