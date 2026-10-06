# DEG-count prediction for held-out Bbs9

## Question and resolved ambiguities

The requested readout is the number of genes with `pvals_adj < 0.05` after each held-out knockout in `151 TH Prkcd Grin2c Glut` cells. The requested-target manifest contains a single target:

```text
Bbs9
```

I treated `n_degs` exactly as in the supplied training-count table: the count includes the perturbed gene itself if the target transcript is a measured feature and passes the FDR threshold. This matters because some ciliary training perturbations in this focal group are otherwise downstream-null but have one self-transcript hit.

## Sources used

- Input training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Input differential-expression parquet: `[local file: training_de_all_cell_groups.parquet]`.
- Requested-target manifest: `[local file: 024_Bbs9.csv]`.
- Same-experiment internal corpus: Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- Run-local profile-neighbor computation: `./bbs_ciliary_151_profile_neighbors.json`, generated from focal-cell Wilcoxon score profiles using the training perturbation universe.
- External literature from PubMed, especially Nachury et al. 2007, DOI `10.1016/j.cell.2007.03.053`, PMID `17574030`; Veleri et al. 2012, DOI `10.1371/journal.pone.0034389`, PMID `22479622`; Knockenhauer and Schwartz 2015, DOI `10.1074/jbc.M115.649202`, PMID `26085087`; Nozaki et al. 2018, DOI `10.1371/journal.pone.0195005`, PMID `29590217`; Nozaki et al. 2019, DOI `10.1242/bio.043786`, PMID `31471295`; Hsu et al. 2021, DOI `10.1093/hmg/ddaa284`, PMID `33517424`; Wingfield et al. 2018, DOI `10.1042/EBC20180030`, PMID `30287585`.

## Computational steps

1. I read the manifest and confirmed that this shard asks only for `Bbs9`.
2. I read the focal training count table and pulled exact `151 TH Prkcd Grin2c Glut` counts for same-complex and same-organelle ciliary perturbations.
3. I filtered the parquet to `group_name == "151 TH Prkcd Grin2c Glut"` and a ciliary comparator set. For each comparator I counted `pvals_adj < 0.05`, recorded the top adjusted p-values, and inspected the self-transcript row.
4. I ran a focal-cell profile-neighbor calculation over the Wilcoxon `scores` vectors for `Bbs5`, `Ttc8`, `Lztfl1`, `Ift88`, `Kif3b`, `Cep290`, `Dync2h1`, `Ift43`, `Ttc21b`, `Alms1`, `B9d1`, and `Arl3`. This compared each anchor with all 1,674 eligible training targets so that weak, non-obvious all-gene similarities would not be mistaken for BBS biology.
5. I used the Distributed Agents corpus to retrieve same-experiment bottom-up claims and findings for `Bbs5`, `Ttc8`, `Lztfl1`, `Ift88`, `Cep290`, and `Alms1`.

The only non-obvious operation was the focal parquet scan. Conceptually it was:

```python
filter = (
    (field("group_name") == "151 TH Prkcd Grin2c Glut") &
    field("gene_target").isin(ciliary_targets)
)
table = dataset.to_table(
    columns=["names", "gene_target", "scores", "logfoldchanges", "pvals_adj"],
    filter=filter,
)
```

I did not use information from the held-out `Bbs9` perturbation itself; it is absent from the training count table and from the training perturbation universe.

## Within-dataset analogs

`Bbs5` is the closest observed core-BBSome subunit to `Bbs9`. It had `n_degs = 0` in the focal group; none of 17,259 tested genes passed FDR 0.05, and even the Bbs5 self-transcript row was only `logfoldchanges = -0.425`, `score = -2.55`, `pvals_adj = 1`. The Distributed Agents `Bbs5:F003` finding reports that represented BBSome/ciliary relatives failed to phenocopy `Bbs5`; `Ttc8`, `Lztfl1`, `Ift88`, `Cspp1`, `Gli1`, `Smo`, `Lepr`, and `Htr6` were flat or singleton-only and non-overlapping.

`Ttc8`, the BBS8 core BBSome subunit, had `n_degs = 1` in the focal group; that one gene was the self transcript `Ttc8` (`logfoldchanges = -0.663`, `score = -6.02`, `pvals_adj = 3.1e-5`). The Distributed Agents `Ttc8:F001` and `Ttc8:F003` findings are important because they separate target knockdown from downstream response: `Ttc8` had a negative self-transcript in the measured neuronal groups yet no downstream mRNA program, and its same-organelle ciliary comparators were nearly orthogonal rather than a hidden BBSome/IFT module.

`Lztfl1`, also known as BBS17, is not a BBSome structural subunit but regulates BBSome/ciliary trafficking. It had `n_degs = 0` in the focal group. Its own transcript moved in the expected negative direction (`logfoldchanges = -0.406`, `score = -3.46`) but was not significant (`pvals_adj = 1`). The corpus `Lztfl1:F003` finding reports that core BBSome, IFT, and transition-zone relatives did not phenocopy the sparse Lztfl1 response seen elsewhere.

IFT, dynein-2, and transition-zone genes provide counterexamples to a broad generic ciliary knockout state in this cell type. The exact focal endpoint was 0 for `Ift43`, `Ift81`, `Ift88`, `Kif3b`, `Dync2h1`, `Dync2i1`, `Ttc21b`, `Cep290`, `Rpgr`, `Rpgrip1l`, `Iqcb1`, `B9d1`, `Alms1`, `Adcy3`, `Gpr161`, `Smo`, `Gli1`, `Ptch1`, `Cspp1`, and `Armc9`; `Arl3` had `n_degs = 1`, again a self-transcript hit. The Distributed Agents high-confidence claim `claim:78305cab7c1c7b98458d` summarizes the same pattern across IFT, dynein-2, BBSome, transition-zone, ciliary-GPCR, Cep290, Alms1, and Hedgehog-adjacent perturbations: acute perturbation of represented ciliary trafficking and signaling genes in postnatal NeuN+ neurons is largely buffered at the basal nuclear-RNA level rather than producing a coherent shared ciliary transcriptional module.

The focal all-gene score correlations also argued against a hidden BBSome expression state. In `151 TH Prkcd Grin2c Glut`, the Pearson correlation between `Bbs5` and `Ttc8` was only `0.0309`; `Bbs5` with `Lztfl1` was `0.0480`; `Bbs5` with `Ift88` was `0.0615`; and `Ttc8` with `Ift88` was `0.0594`. The strongest all-universe Pearson neighbor of `Bbs5` in the focal run was only `0.073`. These values are far below what I would use to transfer a nonzero multi-gene count.

## External biological rationale

`Bbs9` is a direct core member of the BBSome. Nachury et al. 2007 identified the BBSome as a conserved complex of BBS proteins that cooperates with Rab8 during ciliary membrane biogenesis. Later structural and biochemical work placed BBS9 in the BBSome core: Knockenhauer and Schwartz 2015 characterized structured BBS9 domains and a dimerizing C-terminal region; Nozaki et al. 2018 showed that BBS9 contributes to the BBS1-BBS2-BBS7-BBS9 core and reinforces ARL6/BBS3 interaction with BBS1; and Nozaki et al. 2019 found that IFT38 interacts with BBS1/BBS2/BBS9 in export of GPR161 from cilia. BBS9 perturbation is therefore mechanistically closer to the observed `Bbs5` and `Ttc8` perturbations than to the broader IFT or Hedgehog comparators.

The literature also says not to expect BBS9 loss to look transcription-factor-like in a basal juvenile NeuN+ snRNA-seq endpoint. The BBSome primarily acts as a ciliary membrane-cargo adapter, especially for GPCR export and ciliary trafficking, as reviewed by Wingfield et al. 2018. Veleri et al. 2012 showed that BBS9/PTHB1 knockdown causes cilia defects in zebrafish and mouse IMCD3 cells, but those are structural/localization phenotypes rather than immediate broad nuclear-RNA programs. Hsu et al. 2021 further showed that BBSome assembly and entry can be cell-type-specific in specialized photoreceptor cilia, reinforcing the idea that BBS subunit loss is not necessarily visible as the same bulk RNA response in every ciliated cell type.

## Bbs9 zero/nonzero decision

The held-out `Bbs9` target maps to a compact, acute BBSome/ciliary-trafficking prior. The most appropriate observed analogs in the exact focal endpoint are `Bbs5` with 0 DEGs and `Ttc8` with 1 DEG, where the lone `Ttc8` hit is self knockdown rather than a downstream state. The broader ciliary training neighborhood is overwhelmingly zero in the focal group, and the same-experiment corpus independently warns that BBSome/IFT/transition-zone loss in this assay is largely displaced to cilium morphology or cargo localization rather than to basal neuronal mRNA.

I therefore predict no downstream FDR-passing response and do not add a self-transcript-only hit for `Bbs9`. `Bbs9` is present as a measured feature in the focal profiles, so the true result could be 1 if the held-out guides happened to drive a strong Bbs9 RNA decrease like `Ttc8`. However, the training self rows show that target mRNA decreases of related genes frequently failed FDR in this focal group (`Bbs5`, `Lztfl1`, `Ift88`, `Ift43`, `Ift81`, `Kif3b`, `Cep290`, `Dync2i1`, `Ttc21b`, `B9d1`, and `Alms1` all had negative self `logfoldchanges` but non-significant self rows). The conservative point estimate is:

```text
Bbs9 -> 0
```

## Limits

The prediction extrapolates from `Bbs5` and `Ttc8`; `Bbs1`, `Bbs2`, `Bbs4`, `Bbs7`, `Arl6/Bbs3`, and `Bbip1/Bbs18` were not training perturbations in this run. The assay did not measure DNA indels, BBS9 protein, cilium morphology, ciliary receptor localization, cAMP, Hedgehog pathway activation after ligand stimulation, photoreceptors, olfactory epithelium, kidney, or dense hypothalamic energy-balance circuits. Finally, the focal cell group has enough `Bbs9` RNA for differential testing, so the 0 vs 1 call depends on target-RNA behavior that is precisely what was held out.
