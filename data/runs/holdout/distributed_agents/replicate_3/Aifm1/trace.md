# DEG-count prediction trace

## Question and resolved ambiguities

The requested held-out perturbation was `Aifm1`; it should be predicted in `151 TH Prkcd Grin2c Glut` exactly as an endpoint count of genes with `pvals_adj < 0.05` in the supplied Wilcoxon DE table. I interpreted the count as including the target transcript itself when it passed FDR, matching the training CSV. I did not treat weak measured target-RNA knockdown as failed editing, because the assay is sparse CRISPR in postmitotic NeuN+ nuclei and target mRNA loss is not a quantitative editor-efficiency readout.

## Sources used

- Training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Training signatures: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name == "151 TH Prkcd Grin2c Glut"`.
- Requested targets: `[local file: 009_Aifm1.csv]`.
- Distributed Agents same-experiment semantic corpus, release `perturbai-july-260713-sourceguard-1773-v1`. `Aifm1` had no held-out corpus node or claims in this filtered release, so the corpus contributed coverage auditing rather than target-specific positive evidence.
- Distributed Agents runtime profile comparison `aifm1_mito_profile_compare.json`, computed from focal-cell log fold changes for 30 mitochondrial and mitochondrial-adjacent training perturbations.
- PubMed-indexed literature on AIF/AIFM1 and mitochondrial complex I: Vahsen et al. 2004, DOI `10.1038/sj.emboj.7600461`, PMID `15526035`; El Ghouzzi et al. 2007, DOI `10.1097/NEN.0b013e318148b822`, PMID `17805014`; Benit et al. 2008, DOI `10.1371/journal.pone.0003208`, PMID `18791645`; Chinta et al. 2009, DOI `10.1016/j.freeradbiomed.2009.01.010`, PMID `19280713`; Perier et al. 2010, DOI `10.1002/ana.22034`, PMID `20695011`; Herrmann and Riemer 2020, DOI `10.1515/hsz-2020-0254`, PMID `32769219`; Salscheider et al. 2022, DOI `10.15252/embj.2022110784`, PMID `35859387`.

## Computational steps

I first read the held-out CSV and confirmed that only `Aifm1` is requested. I then read the focal-cell training DEG-count table and used string/pattern queries for known mitochondrial respiratory-chain, mitochondrial protease, TCA, import, cristae, mitophagy, apoptosis, NRF/ERR, and oxidative-stress genes to calibrate response scale. The endpoint table has 1,674 perturbations: 1,205 exact zeros, 363 with 1-9 DEGs, 63 with 10-99 DEGs, and 43 with at least 100 DEGs; therefore most mitochondrial targets should be expected to sit at 0 or 1 unless there is strong evidence for a broad secondary state.

The focal-cell parquet was queried with DuckDB rather than loaded as a 616M-row table. For the selected analog set I computed, by `gene_target`, the exact number of rows with `pvals_adj < 0.05`, the matched perturbed/control nucleus counts, and the names of significant genes:

```sql
select gene_target,
       count(*) filter (where pvals_adj < 0.05) as n_sig,
       any_value(n_pert_matched) as n_pert,
       any_value(n_ctrl_matched) as n_ctrl,
       string_agg(names, ',' order by pvals_adj)
         filter (where pvals_adj < 0.05) as sig_genes
from parquet_scan(...)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

I also compared the log-fold-change profiles of 30 selected mitochondrial candidates with `profile_compare` using `logfoldchanges` as the signed value and `pvals_adj < 0.05` as the significant-feature threshold. This was used to test whether training perturbations formed a clean expression module. They did not: `Opa1` was correlated with the complex-I subunits in whole-profile metrics, for example cosine 0.749 to `Ndufb8` and 0.745 to `Ndufs2`, but their FDR-significant sets did not overlap because the `Nduf*` hits were usually self-only. I therefore treated these as weak boundary evidence instead of copying an expression signature wholesale.

## Target-specific reasoning

### `Aifm1`

`Aifm1` encodes a mitochondrial intermembrane-space flavoprotein. The Harlequin mouse and cell knockout/knockdown literature shows that loss of AIF/AIFM1 compromises oxidative phosphorylation by reducing complex-I content or assembly rather than by making AIFM1 a structural complex-I subunit. Vahsen et al. 2004 showed reduced complex-I activity and reduced complex-I subunits in AIF-deficient mouse and human cells, and reduced OXPHOS in Harlequin mouse brain and retina. El Ghouzzi et al. 2007 found early mitochondrial degeneration followed by thalamic, striatal, cortical, and cerebellar pathology in Harlequin mice. Benit et al. 2008 argued that the Harlequin phenotype tracks residual respiratory-chain complex I. Chinta et al. 2009 and Perier et al. 2010 place AIF deficiency in brain mitochondria as a partial complex-I-depleted state, and Salscheider et al. 2022 gives a more specific mechanism in which AIFM1 cooperates with CHCHD4/MIA40 in the disulfide relay needed for import of NDUFS5 and efficient complex-I assembly.

The nearest direct training analogs were therefore complex-I perturbations. In the focal-cell training counts:

- `Ndufb8`, `Ndufs2`, `Ndufa6`, `Ndufa10`, `Ndufs8`, `Ndufc2`, `Ndufb10`, `Ndufb9`, `Ndufb11`, and `Ndufa4` each had 1 DEG.
- `Ndufv1`, `Ndufa11`, `Ndufaf2`, `Ndufaf4`, and `Ndufaf5` each had 0 DEGs.
- `Ndufv2` had 1 DEG, but its significant gene was `Cdc40`, not the target transcript, so I did not treat that as a strong respiratory-chain expression state.

The one-DEG `Nduf*` perturbations were mostly self-only signatures. They are mechanistically close because AIFM1 loss secondarily destabilizes complex I, but they are imperfect because AIFM1 acts through intermembrane-space import and NDUFS5 assembly rather than by removing one holoenzyme subunit. They indicate that acute sparse disruption of complex I in this postnatal thalamic glutamatergic class generally did not create a broad FDR-significant nuclear transcriptional program in recovered nuclei.

I used several counterexamples to keep the prediction from being inflated. `Opa1`, a mitochondrial inner-membrane dynamics/cristae perturbation, was clearly broader at 37 DEGs and induced an integrated-stress/amino-acid-response-looking set including `Asns`, `Mars1`, `Chac1`, `Ddit3`, `Cars`, `Mthfd2`, `Slc7a5`, `Aars`, `Sars`, `Eprs`, `Slc7a1`, `Lars`, and `Nars`. AIFM1 can phenocopy respiratory deficiency and cell vulnerability, but the AIFM1 literature points most directly to complex-I assembly; the training data show that complex-I lesions were much weaker than `Opa1` in this assay. Likewise, `Nrf1` at 138 DEGs and `Esrra` at 57 DEGs are mitochondrial transcriptional regulators and produced broader metabolic programs, but they are upstream nuclear gene-expression regulators rather than single inner-membrane effectors, so they should be treated as upper-bound counterexamples. Other mitochondrial quality-control or import genes were weak or silent: `Tomm40` 1, `Chchd2` 1, `Park7` 1, `Cisd2` 1, `Clpp` 0, `Afg3l2` 0, and `Yme1l1` 0.

For the zero/nonzero decision I put slightly more weight on the AIFM1-specific complex-I/OXPHOS biology than on the global 72% zero prior, so I predict that at least one transcript, plausibly the target transcript itself or one closely coupled stress gene, will cross FDR. For the magnitude I stayed at the bottom of the weak class because the most relevant respiratory-chain analogs had no multi-gene downstream response in the supplied training profiles. Final point prediction: `Aifm1 = 1`.

## Limits of the prediction

The strongest within-dataset evidence is by analogy only: `Aifm1` was completely held out and the Distributed Agents corpus release exposed no `Aifm1` same-experiment findings. AIFM1 loss is not identical to perturbing `Nduf*` subunits, because it couples complex-I assembly to the CHCHD4/MIA40 import relay and to caspase-independent death signaling; it is also not identical to `Opa1`, because `Opa1` directly controls mitochondrial fusion and cristae remodeling and had a broader stress signature in the focal cell group. The experimental readout is survivor-conditioned, 3-4 weeks after sparse AAV CRISPR, so edited neurons with the strongest mitochondrial injury could be depleted rather than represented by a large nuclear RNA signature. The true hidden count could therefore be zero if Aifm1 target-RNA knockdown did not pass FDR, or moderately above one if AIFM1 loss triggered the `Opa1`-like stress module; the training data made the self-only complex-I pattern the most defensible central estimate.
