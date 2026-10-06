# DEG-count prediction for 151 TH Prkcd Grin2c Glut

## Question interpreted

The requested held-out manifest contains one perturbation, `Sdccag8`. I treated the endpoint as the exact CSV endpoint used for the focal cell group: the integer number of measured genes in `151 TH Prkcd Grin2c Glut` with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`. The count includes any significant self-transcript row; however, I did not use weak or absent self-RNA knockdown as evidence of failed editing because the screen is sparse AAV CRISPR and self-RNA loss is not a calibrated editing-efficiency measure.

## Sources

- Differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Focal training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Held-out manifest: `[local file: 203_Sdccag8.csv]`.
- Same-experiment semantic layer: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`. `Sdccag8` itself was not packaged as a corpus target in this release, so I used corpus Findings and Claims for represented ciliary comparators rather than treating corpus absence as a null.
- External biology: PubMed records retrieved through NCBI E-utilities.
  - Schaefer et al. 2011, DOI `10.1159/000331268`: recessive `SDCCAG8/NPHP10` mutations cause Bardet-Biedl syndrome.
  - Insolera et al. 2014, DOI `10.1016/j.neuron.2014.06.029`: SDCCAG8 regulates pericentriolar material recruitment and embryonic cortical neuronal migration through centrosomal/PCM1 biology.
  - Airik et al. 2016, DOI `10.1371/journal.pone.0156081`: SDCCAG8 localizes with centrosome-associated proteins, is required for ciliogenesis and Hedgehog signaling in cultured cells, and interacts with OFD1/AZI1, RABEP2/ERC1, and myosin partners.
  - Weihbrecht et al. 2018, DOI `10.1371/journal.pone.0192755`: mouse `Sdccag8` loss produces developmental ciliopathy phenotypes; the model also illustrates that strong phenotypes are developmental and background-sensitive.
  - Li et al. 2016, DOI `10.1371/journal.pbio.1002416`, and Wang et al. 2022, DOI `10.1242/dmm.049568`: `CEP290`, `RPGRIP1L`, `B9D`/MKS, and IFT genes sit in the transition-zone / primary-cilium disease neighborhood that was represented in the training set.

## Dataset computations

I loaded the 1,674-row focal training-count CSV to check the held-in distribution. The endpoint is zero inflated: 1,205 of 1,674 training perturbations had `n_degs = 0`, the median was 0, the 75th percentile was 1, and the maximum was 2,677.

I then queried the parquet only in the matched focal context:

```sql
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (<Sdccag8 ciliary analogs>)
GROUP BY gene_target
```

For each represented ciliary analog I counted `pvals_adj < 0.05`, recorded the smallest adjusted p-value, and inspected the target self-row when present. Every queried analog had 17,259 measured focal genes and 23,679 matched controls; matched perturbed nuclei ranged from 98 to 328.

## Sdccag8-specific reasoning

External function first defined the appropriate analog class. `Sdccag8` encodes the ciliopathy protein also called NPHP10/BBS16. It acts at centrosomes/centriolar satellites and primary cilia, affects ciliogenesis and Hedgehog signaling, and has a developmental neuronal migration role through pericentriolar material recruitment. Therefore I compared it with the held-in primary-cilium structural and trafficking genes represented in the focal endpoint, especially the transition-zone genes `Cep290`, `Rpgrip1l`, `B9d1`, `Dzip1`, and `Ttc21b`; BBSome/BBSome-trafficking genes `Bbs5`, `Ttc8`, and `Lztfl1`; IFT-B genes `Ift43`, `Ift81`, and `Ift88`; dynein-2 genes `Dync2h1` and `Dync2i1`; and the kinesin-2 motor subunit `Kif3b`.

The exact focal observations were:

| training perturbation | mechanistic comparison to `Sdccag8` | focal `n_degs` | focal expression-pattern evidence |
|---|---|---:|---|
| `Cep290` | core transition-zone / NPHP ciliopathy comparator | 0 | no FDR<0.05 gene; best adjusted p-value 0.650 |
| `Rpgrip1l` | transition-zone MKS5/NPHP module gatekeeper | 0 | no FDR<0.05 gene; best adjusted p-value 0.184 |
| `B9d1` | B9/MKS transition-zone complex | 0 | no FDR<0.05 gene; all focal adjusted p-values were 1 |
| `Dzip1` | basal-body/transition-zone ciliogenesis and Hedgehog factor | 0 | no FDR<0.05 gene; self row log2FC -0.318, adjusted p-value 1 |
| `Ttc21b` | IFT-A / ciliopathy gene, BBS kidney-risk comparator | 0 | no FDR<0.05 gene; best adjusted p-value 0.459 |
| `Bbs5` | BBSome subunit, closest represented BBSome target besides `Ttc8` | 0 | no FDR<0.05 gene; best adjusted p-value 0.220 |
| `Ttc8` | BBSome/BBS8 subunit | 1 | the lone focal hit was `Ttc8` itself, log2FC -0.663, adjusted p-value 3.07e-05; no downstream ciliary or stress module |
| `Lztfl1` | BBSome trafficking regulator | 0 | no FDR<0.05 gene; best adjusted p-value 0.195 |
| `Ift43` | IFT-B trafficking complex | 0 | no FDR<0.05 gene; best adjusted p-value 0.847 |
| `Ift81` | IFT-B trafficking complex | 0 | no FDR<0.05 gene; best adjusted p-value 0.391 |
| `Ift88` | IFT-B trafficking complex and classic ciliogenesis/Hedgehog comparator | 0 | no FDR<0.05 gene; all focal adjusted p-values were 1 |
| `Dync2h1` | dynein-2 retrograde IFT motor | 0 | no FDR<0.05 gene; best adjusted p-value 0.348 |
| `Dync2i1` | dynein-2 retrograde IFT subunit | 0 | no FDR<0.05 gene; all focal adjusted p-values were 1 |
| `Kif3b` | kinesin-2 anterograde ciliary transport motor | 0 | no FDR<0.05 gene; all focal adjusted p-values were 1 |
| `Cep120`, `Kiz`, `Rpgr` | basal-body or retinal/ciliary counterexamples, less direct than the genes above | 0 | all had no FDR<0.05 focal downstream program |

The same-experiment corpus supports treating those zeroes as a coherent assay-local pattern, not a random handful of absences. The high-confidence Distributed Agents Claim `claim:78305cab7c1c7b98458d` states that represented ciliary trafficking and ciliary signaling genes in postnatal NeuN+ neurons were largely buffered at the basal nuclear-RNA level rather than forming a shared ciliary transcriptional module. Material supporting Findings included `Cep290:F003`, where expected BBSome/IFT/ciliary-GPCR/Hedgehog transcription was absent after `Cep290` and nearly absent for those pathway components themselves; `Ift88:F003`, where IFT-B, dynein-2, `Cep290`, `Bbs5`, `Smo`, `Ptch`, and `Gli` relatives converged mainly by being transcriptionally buffered; `Kif3b:F001`, a pan-neuronal transcriptomic null; `Dync2h1:F001`, a complete measured null over recovered neuronal groups; and `Ttc8:F003`, where `Bbs5`, IFT, dynein-2, `Lztfl1`, `Rpgrip1l`, `Ttc21b`, and `Cep290` were nearly orthogonal to `Ttc8` and had zero or isolated FDR genes in matched groups.

That corpus pattern also names counterexamples and boundary cases. `B9d1` and `Lztfl1` had sparse effects in other neuronal groups but not in `151 TH Prkcd Grin2c Glut`, and they did not make a generic cilium-loss transcriptome. `Mib1`, a Talpid3-linked ciliary E3 ligase in the corpus, had a sterol response that was absent from the structural IFT/BBS/transition-zone set. Broad non-ciliary perturbations such as proteasome and spliceosome targets produced hundreds to thousands of focal DEGs, so the ciliary quietness is not because the focal class was incapable of producing a broad RNA signal.

Putting those pieces together, I predicted no FDR<0.05 `Sdccag8` response in the focal thalamic glutamatergic class. The external literature makes `Sdccag8` a strong ciliary/centrosomal-satellite disease gene, but its best training-set analogs are precisely the pathway class that this P16-to-P37/44 NeuN+ snRNA assay mostly failed to convert into basal nuclear-RNA changes. I also did not add 1 for a guaranteed self-transcript event: among focal ciliary neighbors, target self rows were usually nominally negative but adjusted p-value 1, while `Ttc8` was the exception.

## Prediction

| target | predicted_n_degs | zero/nonzero rationale |
|---|---:|---|
| `Sdccag8` | 0 | The appropriate transition-zone/BBSome/IFT analogs have 0 focal DEGs, except for a `Ttc8` self-transcript singleton. External `Sdccag8` biology maps to cilium structure, ciliary cargo, Hedgehog response under challenge, kidney/retina, and embryonic migration more than to a broad basal transcriptomic program in recovered postmitotic thalamic neurons. |

## Limits and extrapolations

- This is an extrapolation: `Sdccag8` was completely held out, and the same-experiment corpus release had no packaged `Sdccag8` Finding or Claim.
- Several closest SDCCAG8 interactors or BBS genes were absent from the held-in target universe, so `Cep290`, `Rpgrip1l`, `B9d1`, `Bbs5`, `Ttc8`, `Lztfl1`, and IFT genes are pathway analogs rather than exact same-complex substitutes.
- The screen measured steady-state nuclear RNA, not cilium assembly, cilium length, GPCR localization, Hedgehog challenge responses, PCM1/OFD1/RABEP2/ERC1 localization, photoreceptor outer-segment trafficking, kidney phenotypes, or embryonic neuronal migration.
- A focal self-transcript hit could turn a downstream-null `Sdccag8` perturbation into an endpoint value of 1; the training data do not make that deterministic, and the local ciliary self rows favored zero.
