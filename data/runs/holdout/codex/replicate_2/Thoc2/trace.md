# Direct forecast for Thoc2 in 151 TH Prkcd Grin2c Glut

## Target and endpoint

- Manifest target: `Thoc2`.
- Endpoint: number of measured genes in `151 TH Prkcd Grin2c Glut` with Wilcoxon BH-adjusted `pvals_adj < 0.05`.
- Declared count table and parquet are training-only for this endpoint; no `Thoc2` response row was used.

## Target prior from the declared biology bundle

- The focal population has direct in-assay `Thoc2` reach: 20,186 / 23,679 non-target nuclei expressed `Thoc2` in `151 TH Prkcd Grin2c Glut` (`85.25%`), with mean raw UMI `2.225`, so lack of transcript reach is not a strong reason to expect a null response.
- THOC2 is a core THO/TREX mRNA-processing/export component. Existing protein should mostly clear before harvest: the bundle cites 43.0 h and 45.0 h THOC2 half-lives in primary mouse neurons, while the P16 edit to P37-P44 harvest window is 21-28 days.
- The bundle does not establish a directly matched acute thalamic phenotype or a quantitative transcriptome size. A germline hypomorph supports neural vulnerability but is developmental; an annotated `Thoc2l` relative leaves compensation unresolved rather than proven.

## Training perturbations that set the scale

I nominated training-available analogues with the local typed annotation tool against the declared 1,674-gene count table. The two specific THO/TREX-neighborhood nominees were:

- `Thoc1`, the rank-1 nominee, linked to `Thoc2` by a STRING physical interaction and by THO / transcription-export-complex annotations.
- `Ddx39b`, the rank-2 nominee, an mRNA-export helicase in the transcription export complex but outside the THO core.

Other high-priority nominees such as `U2af2`, `Cdc40`, `Prpf6`, `Hnrnpu`, `Hnrnpc`, and `Tpr` were broad spliceosome, hnRNP, or nuclear-pore/RNA-processing perturbations. Their 151-class outcomes show that this axis can produce hundreds to thousands of DE genes, but their proximal operations are less THOC2-like than `Thoc1`.

Exact declared 151-class counts and matched perturbed nuclei:

| target | n_degs | n_pert_matched | interpretation |
| --- | ---: | ---: | --- |
| `Thoc1` | 303 | 121 | closest observed THO-core comparator |
| `Ddx39b` | 0 | 48 | TREX accessory/export factor; low powered and flat in 151 |
| `Hnrnpc` | 122 | 196 | broader hnRNP/RNA-processing comparator |
| `Snrnp70` | 213 | 135 | spliceosome/RNA-binding comparator |
| `Prpf6` | 454 | 72 | spliceosome comparator |
| `Cdc40` | 624 | 159 | spliceosome/RNA-processing comparator |
| `Hnrnpu` | 733 | 163 | broad hnRNP comparator |
| `U2af2` | 828 | 222 | broad splicing/mRNA-processing comparator |
| `Tpr` | 1768 | 114 | nuclear-pore/RNA-export comparator, much broader than THO |

`Thoc1` is already a high-burden 151-class perturbation: 303 DE genes is rank 25 / 1674 in the declared count table, with 1205 / 1674 training perturbations at zero and only 25 at 300 or more.

For the measured 151-class log-fold-change profiles of these RNA-processing candidates, the `Thoc1` profile was positively correlated with the broader high-response comparators rather than isolated:

| pair | Pearson r across measured genes | shared FDR<0.05 genes, same/opposite direction |
| --- | ---: | --- |
| `Thoc1`:`Tpr` | 0.6875 | 103 / 11 |
| `Thoc1`:`Hnrnpu` | 0.6854 | 64 / 14 |
| `Thoc1`:`Cdc40` | 0.6771 | 48 / 12 |
| `Thoc1`:`Hnrnpc` | 0.6740 | 9 / 7 |
| `Thoc1`:`Prpf6` | 0.6466 | 45 / 4 |
| `Thoc1`:`Snrnp70` | 0.6364 | 59 / 3 |
| `Thoc1`:`U2af2` | 0.6065 | 66 / 9 |
| `Thoc1`:`Ddx39b` | 0.6231 | 0 / 0 |

The same-experiment `Thoc1` Findings interpret its response as a selective RNA-biogenesis / mRNP-formation state: most FDR-supported rows fell in four neuronal classes including 151 TH, major responders included splicing and nuclear RNA-handling genes, and the signature lacked an overt p53, apoptosis, UPR, or integrated-stress program. The report also records that `Ddx39b` phenocopied `Thoc1` only in 191 MB P MY GABA and was flat in 151 TH, so I treated the 151-class `Ddx39b = 0` result as a caution against overgeneralizing TREX membership, not as an equal negative analogue for a core THO subunit.

## Synthesis

The point forecast is anchored on the one measured core-THO comparator, `Thoc1 = 303`. `Thoc2` has strong focal expression and its protein stock should be substantially replaced within the 21-28 day window, so I did not shrink toward the all-training median of zero. The broader spliceosome/hnRNP/nuclear-pore perturbations show that RNA-biogenesis lesions can be much larger than 303 DE genes in the same cell class, but they perturb wider or different machines, so I did not transfer their 600-1700 gene scale to `Thoc2`.

Balancing the direct `Thoc1` match, the flat but low-powered `Ddx39b` boundary, and survivor-conditioned uncertainty, I used a round `Thoc1`-centered count:

`predicted_n_degs = 300`
