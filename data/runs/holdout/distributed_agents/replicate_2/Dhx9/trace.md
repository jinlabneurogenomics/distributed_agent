# Dhx9 DEG-count prediction trace

## Question and target

I interpreted the task as a point prediction of the number of genes with
`pvals_adj < 0.05` after each requested knockout in `151 TH Prkcd Grin2c Glut`
cells. The requested manifest contains one held-out target, `Dhx9`, and the
quantity to predict is the focal-cell-group DEG count, including the target
transcript itself if it passes FDR.

I treated `151 TH Prkcd Grin2c Glut` as the thalamic glutamatergic group
described in the dataset context. I did not treat weak self-RNA knockdown as
failed editing, because this AAV CRISPR assay often creates functional indels
without reducing the nuclear target RNA.

## Sources used

- `training_de_all_cell_groups.parquet`, queried at the row level for
  `151 TH Prkcd Grin2c Glut` expression signatures of candidate analogs.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, used as the authoritative
  training endpoint for exact `n_degs` values in the focal cell group.
- `056_Dhx9.csv`, which supplied the single held-out target.
- The selected Distributed Agents corpus, `perturbai-july-260713-sourceguard-1773-v1`,
  used for curated same-experiment findings and claims over non-held-out
  perturbations.
- PubMed literature retrieved for DHX9/RNA helicase A biology:
  - Lee et al. 1998, PNAS, DOI `10.1073/pnas.95.23.13709`,
    PMID `9811865`: `Dhx9`/RHA is required for early mouse gastrulation.
  - Lee and Pelletier 2016, Oncotarget, DOI `10.18632/oncotarget.8446`,
    PMID `27034008`: review of DHX9 as a DNA/RNA helicase involved in
    transcription, translation, miRNA biogenesis, RNA processing and transport,
    DNA replication, and genome stability.
  - Aktas et al. 2017, Nature, DOI `10.1038/nature21715`,
    PMID `28355180`: DHX9 resolves structured repeat-derived RNAs and suppresses
    RNA-processing defects at inverted Alu elements in human cells.
  - Cristini et al. 2018, Cell Reports, DOI `10.1016/j.celrep.2018.04.025`,
    PMID `29742442`: DHX9 is part of the RNA/DNA-hybrid interactome, promotes
    R-loop suppression and transcription termination, and interacts with PARP1.
  - Ng et al. 2018, Nucleic Acids Research, DOI `10.1093/nar/gky742`,
    PMID `30137501`: DHX9 can act as a nuclear transcriptional coactivator for
    NF-kB antiviral programs in macrophages and fibroblasts.

## Dataset computations

From the training-count CSV, the focal endpoint was very sparse: among 1,674
training perturbations, 1,205 had `n_degs = 0`, the median was 0, the 75th
percentile was 1, and 469 perturbations were nonzero. The broad upper tail was
dominated by RNA-processing, splicing, nuclear transport, proteasome, and
chromatin/transcription regulators.

For Dhx9 analogs and counterexamples, I queried the parquet restricted to the
focal group and counted significant rows by target:

```sql
select gene_target,
       count(*) filter (where pvals_adj < 0.05) as n_sig,
       max(n_pert_matched) as n_pert,
       max(n_ctrl_matched) as n_ctrl
from read_parquet('training_de_all_cell_groups.parquet')
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

The counts reproduced the endpoint CSV for the candidates below and provided
matched focal perturbed-cell counts and top significant genes for signature
inspection.

## Same-experiment analogs

The strongest positive comparators in the focal group were spliceosome or
RNP-stress perturbations, but they were not all interchangeable:

| training target | focal n_degs | relevant focal-pattern evidence |
| --- | ---: | --- |
| `Rnpc3` | 868 | Core minor-spliceosome factor; Distributed Agents finding `Rnpc3:F009` reports convergence with `Prpf6`, `Snrnp70`, `U2af2`, `Cdc40`, and `Hnrnpu`. In the focal parquet it strongly up-regulated `Mapk8`, `Pcyt2`, `Ap2a1`, `Wdfy1`, and other secondary trafficking/ER/RNA-processing genes. |
| `U2af2` | 828 | Core 3-prime splice-site factor; Distributed Agents finding `U2af2:F005` placed `Prpf6`, `Cdc40`, and `Tpr` among the top same-direction neighbors, along with proteasome perturbations. In the focal parquet it down-regulated `Rsrp1`, `Srrm2`, `Atp2a2`, `Agrn`, and `Luc7l2`. |
| `Hnrnpu` | 733 | A nuclear RBP/chromatin scaffold rather than a spliceosome subunit. Distributed Agents finding `Hnrnpu:F003` reports an induced RNA-processing module and convergence with spliceosome/RNA-processing perturbations; `Hnrnpu:F009` also notes that measured hnRNP-family perturbations were not HNRNPU phenocopies. |
| `Cdc40` | 624 | Spliceosome/PRP17-related broad responder with `Srrm2` and `Ogt` down and RNA/chromatin factors up in the focal group. |
| `Tnpo3` | 618 | Nuclear import factor that Distributed Agents claims connect to an RNA-processing-linked nuclear logistics state, not generic nuclear transport. |
| `Prpf6` | 454 | Core spliceosome factor; part of the recurrent RNA-splicing module in Distributed Agents claim `claim:c85727b65aed9288f022`. |
| `Thoc1` | 303 | THO/TREX mRNA-export factor; Distributed Agents `Thoc1:F006` says convergence is strongest with `Ddx39b` only in `191 MB P MY GABA`, while `Ddx39b` was flat in `151`, `155`, `066`, and `110`. |
| `Snrnp70` | 213 | U1 snRNP factor with a broad but smaller RNA-biogenesis/proteasome-neighbor state. |
| `Tardbp` | 210 | RNA-binding ALS-linked comparator. Broad enough to matter, but Distributed Agents finds ALS/RNA-granule membership nonconvergent with `Matr3`, `Atxn2`, and `Tia1`, so it is a weak mechanistic analog for Dhx9. |
| `Hnrnpc` | 122 | Nuclear hnRNP and RNA-processing target; its focal response shared only 33 genes with `Hnrnpu`, underscoring non-interchangeability even within hnRNP biology. |
| `Matr3` | 149 | Nuclear-matrix RBP with a restricted stress signature overlapping other RNA-processing/proteostasis responses. |
| `Ascc3` | 18 | Superfamily-2 helicase whose same-direction neighbors include `U2af2`, `Prpf6`, and `Matr3`; in `151` it was much smaller than the core spliceosome responders. |

The better negative or near-null comparators pulled the Dhx9 prediction
downward:

| training target | focal n_degs | why it bounds Dhx9 |
| --- | ---: | --- |
| `Ddx39b` | 0 | An RNA helicase in THO/TREX-associated mRNA export. It formed a TREX/export-sensitive program with `Thoc1` in `191 MB P MY GABA`, but was exactly flat in the focal thalamic group despite the focal group being highly responsive to `Thoc1`, `U2af2`, `Rnpc3`, and `Prpf6`. |
| `Ddx3x` | 8 | A neuronal DEAD-box helicase with a small focal signature and no focal convergence with `Ddx39b`. Distributed Agents explicitly warns that the DDX3X/DDX39B/EIF4A2 RNA-helicase label did not produce a generic shared postmitotic mRNA signature. |
| `Eif4a2`, `Eif4g1`, `Eif4h` | 2, 1, 1 | Translation/cap-initiation neighbors that were flat, weak, or divergent in the same assay. |
| `Setx` | 0 | The closest represented R-loop-resolution counterexample. Distributed Agents `Setx:F001` reports 0 downstream FDR<0.10 genes across 22 tested neuronal groups, and `Thoc1:F007` uses `Setx` to reject a generic R-loop axis for the THO/TREX response. |
| `Son`, `Ylpm1` | 0, 1 | Nuclear-speckle/RNP-associated factors that Distributed Agents separates from broad core RNA-processing perturbations. `Son:F003` directly contrasts minimal `Son` output with broad `Prpf6`, `U2af2`, `Hnrnpu`, `Snrnp70`, and `Tardbp` outputs. |
| `Adar`, `Dicer1` | 0, 0 | RNA-editing and miRNA-processing nodes were fully flat in the focal group, arguing against generic visibility of every nuclear or RNA-processing enzyme. |

I also inspected individual focal DE rows for recurrent RNA-processing markers.
The broad spliceosome perturbations shared a small but clear set of genes such
as `Rsrp1` and `Srrm2`, while `Ddx39b`, `Setx`, and `Son` were essentially
flat at those same markers. `Dhx9` itself, as a measured downstream gene, was
only a modest induced transcript in a subset of broad signatures: significant
after `Cdc40` and `Thoc1` perturbation, but not after `Rnpc3`, `U2af2`,
`Prpf6`, `Tnpo3`, or `Hnrnpu` at focal FDR. That supports a view of DHX9 as a
secondary nuclear remodeling gene in some contexts rather than a core member of
the large RNPC3/U2AF2 module.

## Dhx9-specific prediction

External biology gives DHX9 many nuclear functions: it binds structured RNA,
can unwind DNA/RNA substrates, suppresses RNA/DNA hybrids and R-loop-associated
damage with PARP1, contributes to transcriptional termination, can act as a
transcription cofactor, and is essential during embryogenesis. That is enough
to predict that complete DHX9 loss can be biologically serious.

Those functions did not map cleanly onto the high-DEG training perturbations in
the postnatal NeuN+ assay. The large focal DEG burdens came from core or
adjacent spliceosome/RNA-processing stressors, and the same corpus repeatedly
showed that pathway or RBP labels alone are unsafe: `Ddx39b` and translation
helicase/cap-initiation targets did not make a focal RNA-helicase module,
`Son` and `Ylpm1` did not behave as broad core splicing perturbations, and
`Setx` showed that an acute R-loop regulator can be invisible at steady-state
gene-abundance resolution. DHX9 is closer to this latter R-loop/helicase class
than to U2AF2/RNPC3/CDC40 spliceosome chemistry. The Alu-repeat function from
Aktas et al. is also human-primate repeat biology, not a direct mouse thalamic
neuron prior, and the Ng et al. NF-kB coactivator role was measured during DNA
virus innate stimulation rather than in basal NeuN+ neurons.

I therefore predicted no focal FDR-significant whole-gene response for `Dhx9`:

- the zero class is the modal endpoint for the training set;
- the most mechanistically direct same-assay R-loop comparator, `Setx`, was
  pan-null;
- the best RNA-helicase/TREX comparator, `Ddx39b`, had `n_degs = 0` in
  `151 TH Prkcd Grin2c Glut`;
- broader focal responses from `Rnpc3`, `U2af2`, `Hnrnpu`, `Cdc40`, `Tnpo3`,
  `Prpf6`, `Thoc1`, `Snrnp70`, and `Tardbp` establish assay sensitivity but
  look like imperfect counterexamples rather than direct Dhx9 analogs.

Point prediction: `Dhx9 = 0`.

## Limits

The largest uncertainty is that the direct `Dhx9` perturbation was held out:
its recovered focal nucleus count, self-transcript p value, and true DE
signature were unavailable. DHX9 is multifunctional, and the training library
does not include an exact paralog or all direct partners, so this is an
extrapolation from nearby helicase/R-loop and RNP factors. The parquet reports
steady-state whole-gene nuclear RNA only; it cannot see altered splicing,
circle-RNA production, R-loops, DNA damage, protein loss, translation, or
survivor selection. A small one-gene self-transcript response would be plausible
even under the zero-downstream model, and a strong DHX9-specific stress state
could have been missed by the available analogs.
