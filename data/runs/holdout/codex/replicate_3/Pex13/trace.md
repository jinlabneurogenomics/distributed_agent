# Evidence and reasoning

## Target and endpoint

- Target: `Pex13`.
- Focal population: `151 TH Prkcd Grin2c Glut`.
- Endpoint: `n_degs`, the number of measured genes in the focal population with BH-adjusted Wilcoxon `pvals_adj < 0.05`.
- The target perturbation is withheld from the declared focal count table and from the declared training Parquet. I did not inspect a Pex13 differential-expression row or a Pex13 outcome.

## Pex13 biology

The canonical biology bundle places PEX13 in the peroxisomal matrix-import docking apparatus with PEX14, PEX5, and PEX7. Its card adjudicates it as a dynamic peroxisomal import-complex component whose operative stock is likely substantially depleted by the P16-to-P37/P44 harvest window, because edited cells stop resupplying PEX13 while peroxisomes and the import machinery continue to turn over. The bundle also makes the main uncertainty explicit: direct juvenile thalamic neuron timing is not available, the strongest mouse neural phenotype is developmental Nestin-Cre evidence, and survivor conditioning can attenuate the recovered single-nucleus RNA signal.

The exact focal-population reach argues that the transcript is visible in this class: Pex13 is detected in 19,147 of 23,679 non-target nuclei, or 80.86%, with mean raw UMI 1.96 and mean CP10K 1.236. That supports a plausible self-transcript call if CRISPR loss yields any measurable target-RNA reduction, but it does not prove a large downstream transcriptional program.

## Training counts

The focal training table contains 1,674 measured perturbations. It is heavily zero-inflated in this population:

- 1,205/1,674 targets have `n_degs = 0`.
- 1,481/1,674 targets have `n_degs <= 1`.
- The median is 0; the 75th percentile is 1; the 95th percentile is 18.

Thus the quantitative prior for an arbitrary focal perturbation is 0 or 1 DEGs, with a long but rare high-count tail.

## Peroxisomal comparators from the declared training set

I used the typed analog nomination store before selecting comparators. The highest-priority Pex13 training-available candidates with peroxisome-specific evidence were `Pex14`, `Abcd3`, and `Acbd5`, all sharing the narrow Reactome "Class I peroxisomal membrane protein import" module or peroxisomal membrane terms. I retained the connected broader peroxisomal/import/lipid neighborhood `Atad1`, `Pex1`, `Agps`, `Hsd17b4`, `Trim37`, and `Acsl4` for a measured-profile check rather than relying only on symbol names.

The same-experiment corpus topology over these nine targets was one connected component by explicit Finding-reference edges. Its tightest fully connected peroxisome subcohort was `Abcd3`, `Acbd5`, `Hsd17b4`, `Pex1`, and `Pex14`, which anchors the closest scale evidence around peroxisome import and membrane metabolism.

In the requested focal population, the declared count table and focal Parquet show a uniformly tiny FDR footprint for that cohort:

| target | focal n_degs | FDR<0.05 focal gene |
| --- | ---: | --- |
| `Pex14` | 1 | `Pex14` |
| `Abcd3` | 0 | none |
| `Acbd5` | 0 | none |
| `Pex1` | 0 | none |
| `Hsd17b4` | 0 | none |
| `Agps` | 1 | `Dhcr24` |
| `Atad1` | 1 | `Atad1` |
| `Trim37` | 1 | `Trim37` |
| `Acsl4` | 1 | `Acsl4` |

The all-cell same-experiment Findings reinforce that this is not merely one quiet cell class: `Pex14` had no downstream FDR<0.10 genes in 23 measured neuronal classes, `Pex1` lacked a peroxisome-import, lipid-metabolism, oxidative-stress, autophagy, ISR, or UPR module, and `Abcd3`, `Acbd5`, and `Hsd17b4` were pan-measured neuronal transcriptional nulls or near-nulls.

## Synthesis

I forecast a sparse response, not a broad stress program. Pex13 is mechanistically important and expressed in the focal thalamic neurons, but the closest measured perturbations to peroxisomal import or membrane function almost never generate more than a self-transcript singleton in this endpoint. `Pex14` is the most informative direct docking-apparatus comparator and gives exactly one focal DEG, its own transcript; the `Abcd3`/`Acbd5`/`Hsd17b4`/`Pex1` core is 0, 0, 0, and 0.

Because PEX13 is a high-reach measured transcript in this class and a loss of the docking component is expected to be functionally realized by harvest, I set the point just above a complete null. The large-program alternatives are disfavored by the peroxisome training neighborhood and by the corpus reports showing no shared nuclear peroxisome, redox, ISR, UPR, or autophagy response for the represented peroxisome genes.

Point prediction: `1`.
