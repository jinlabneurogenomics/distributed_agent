# Hsf4 held-out DEG-count prediction

## Question interpreted

Predict the held-out endpoint `n_degs` for each requested perturbation in
`151 TH Prkcd Grin2c Glut`: the number of assayed genes with Wilcoxon
Benjamini-Hochberg adjusted `pvals_adj < 0.05` after acute AAV CRISPR-Cas9
loss of the target in postnatal mouse neurons.

The manifest for this run contains one held-out target:

```tsv
target_name
Hsf4
```

I treated `n_degs` as an assay-specific breadth measurement, not as a direct
readout of editing efficiency or biological essentiality. Because `Hsf4` was
completely held out, I did not use any `Hsf4` differential-expression rows as
training data.

## Sources used

- Input endpoint file:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
  It contained 1,674 non-held-out perturbations; 469/1,674 had any nonzero
  DEG count, the median was 0, the 75th percentile was 1, the 95th percentile
  was 18, and a small long tail reached 2,677 DEGs.
- Input DE parquet:
  `[local file: training_de_all_cell_groups.parquet]`.
  I filtered it to `group_name == "151 TH Prkcd Grin2c Glut"` and to a
  mechanistic candidate list around heat-shock factors, chaperones, UPR/ISR/ARE
  stress genes, lens transcription factors, and proteostasis positive controls.
- Distributed Agents same-experiment corpus release
  `perturbai-july-260713-sourceguard-1773-v1`.
  `Hsf4` itself was unresolved in this corpus, so I used corpus reports for
  represented comparators such as `Hsf1`, `Hspa5`, `Hspa8`, `Hsp90ab1`,
  `Dnajb6`, `Atf6`, `Nfe2l1`, `Nfe2l2`, `Maf`, and `Pax6`.
- Distributed Agents runtime profile comparison over the focal `151 TH Prkcd Grin2c Glut`
  signatures for `Hsf1`, `Hspa5`, `Hspa8`, `Hsp90ab1`, `Dnajb4`, `Dnajb6`,
  `Atf6`, `Nfe2l2`, `Maf`, and `Pax6`, with all 1,674 training targets as the
  eligible neighbor universe.
- NCBI PubMed literature on HSF4 and lens development:
  Shi et al. 2009, DOI 10.1186/1471-2199-10-10, PMID 19224648; Mou et al.
  2009, DOI 10.1167/iovs.09-3772, PMID 19628735; Cui et al. 2018, DOI
  10.1016/j.biocel.2018.10.003, PMID 30316871; Cui et al. 2021, DOI
  10.1016/j.bbadis.2021.166233, PMID 34339841; Morishita et al. 2021, DOI
  10.1038/s41586-021-03439-w, PMID 33854238; Zhang et al. 2023, DOI
  10.1167/iovs.64.7.5, PMID 37266953.

## Computations over the focal DE table

I used `pyarrow.dataset` predicate pushdown to read only the focal cell group
and the biologically nominated perturbations:

```python
scanner = ds.dataset(parquet, format="parquet").scanner(
    columns=[
        "names", "gene_target", "logfoldchanges", "pvals_adj", "scores",
        "n_pert_matched", "n_ctrl_matched",
    ],
    filter=(
        pc.field("group_name") == "151 TH Prkcd Grin2c Glut"
    ) & pc.field("gene_target").isin(candidate_targets),
)
candidate_de = scanner.to_table().to_pandas()
```

For each candidate perturbation I counted rows with `pvals_adj < 0.05` and
inspected the best-ranked genes by adjusted p value. Key focal-cell counts were:

```tsv
target_name	n_degs	focal evidence
Hsf1	6	Only six corrected genes, all down: Hsph1, Hsp90aa1, Rsrp1, Hsp90ab1, Mat2a, Ahsa2.
Hspa5	5	Small ER-chaperone/UPR arm: Hsp90b1, Nfe2l1, Pdia4, Derl3 up and Erc1 down.
Hspa8	9	Small cytosolic chaperone response including Dnaja1, Hspa4l, Hsp90aa1, Cct6a up.
Hsp90ab1	1	Only the target transcript itself passed FDR.
Dnajb4	0	DNAJ/Hsp40 co-chaperone; no corrected response.
Dnajb6	0	DNAJ/Hsp40 co-chaperone; no corrected response.
Dnajc13	1	Only target row significant.
Dnajc19	0	No corrected response.
Dnajc5	1	Only target row significant.
Atf6	0	No corrected UPR-sensor response.
Eif2ak4	0	No corrected ISR-kinase response.
Nfe2l1	0	No genes below FDR 0.05; nearest rows all FDR 0.062.
Nfe2l2	0	No NRF2/ARE response.
Maf	0	Lens/large-MAF bZIP comparator; no corrected response.
Mafa	0	Large-MAF comparator; no corrected response.
Mafb	0	Large-MAF comparator; no corrected response.
Mafg	1	Only Lamp2 reached FDR 0.048.
Pax6	0	Lens-development comparator; no corrected response.
Foxe3	0	Lens-development comparator; no corrected response.
Sec63	11	ER translocon/BiP cofactor; the strongest nearby UPR comparator but still tiny.
Psmc1	430	Core 26S proteasome positive control, broad stress response.
Psmb4	742	Core proteasome positive control, broad stress response.
Ufc1	572	UFMylation positive proteostasis control.
Uba5	2677	UFMylation positive proteostasis control.
```

I also asked the Distributed Agents runtime to compare the focal signatures of
`Hsf1`, `Hspa5`, `Hspa8`, `Hsp90ab1`, `Dnajb4`, `Dnajb6`, `Atf6`, `Nfe2l2`,
`Maf`, and `Pax6`. Four of these ten nodes had only 1-9 significant features
and six had none. The inspection did not find a strong same-pathway module
among the heat-shock/lens candidates; for example, no significant features
overlapped between `Hsf1` and the flat `Atf6`, `Nfe2l2`, `Maf`, or `Pax6`
counterexamples. I did not treat all-gene Pearson/cosine neighbors as decisive
for the null signatures, because those vectors are dominated by weak
uncorrected variation; their role was only to check that no FDR-supported
heat-shock or lens module was being missed.

## Same-experiment biological transfer

### Heat-shock and chaperone axis

`Hsf1` is the closest measured paralog and the only represented heat-shock
transcription factor. It produced six DEGs in the focal cell group, mainly
down-regulating canonical chaperone/co-chaperone transcripts
`Hsph1`, `Hsp90aa1`, `Hsp90ab1`, and `Ahsa2`. That is a real but narrow HSF
readout. Direct chaperone losses were similarly sparse:

- `Hspa8`, the constitutive cytosolic Hsp70, had 9 DEGs.
- `Hspa5/BiP`, the ER Hsp70, had 5 DEGs.
- `Hsp90ab1` had 1 DEG, its own target RNA.
- DNAJ/Hsp40 family perturbations in the table had 0-1 DEG in this cell group.

The Distributed Agents corpus claim over `Dnajb6`, `Hsf1`, `Hspa5`, and `Hspa8`
summarized the same-experiment pattern as "represented chaperone and
co-chaperone perturbations do not collapse onto a single heat-shock or UPR
transcriptomic program in this postnatal neuronal assay." A second corpus
claim over `Dnajb4`, `Dnajb6`, `Dnajc19`, `Dnajc5`, `Hsp90ab1`, and `Stub1`
placed these single chaperone/cofactor perturbations in the buffered/null
class, unlike broad core proteasome hits.

The expansion from `Hsf1`, `Hspa5`, `Hspa8`, and `Hsp90ab1` returned `Atf6`,
`Vcp`, `Psmc1`, `Nfe2l2`, and `Psmb4`. I kept `Atf6` and `Nfe2l2` as flat
stress-branch boundaries, because they had 0 DEGs here. I treated `Vcp`
as another weak proteostasis boundary, with only 2 DEGs. I rejected `Psmc1`
and `Psmb4` as HSF4 analogs despite their broad 430/742-DEG counts: they are
core 26S proteasome perturbations that impose upstream proteotoxic load and
activate compensatory HSP transcripts, the opposite biological situation from
removing a distal heat-shock-family transcription factor.

This argues against a broad `Hsf4` count. If loss of a single HSF/chaperone
node created a large stress state in these neurons, `Hsf1`, `Hspa8`,
`Hspa5`, or `Hsp90ab1` should have approached the proteasome/UFMylation
positive controls. They did not.

### UPR, ISR, NRF/ARE, and bZIP boundaries

Generic stress TF or bZIP membership also did not transfer well:

- `Atf6`, an ER UPR sensor, had 0 DEGs.
- `Eif2ak4`, an ISR kinase, had 0 DEGs.
- `Nfe2l1` and `Nfe2l2`, CNC-bZIP stress regulators, had 0 DEGs.
- `Mafg`, a small-MAF partner, had just 1 DEG.
- `Maf`, `Mafa`, and `Mafb`, large-MAF bZIP factors with lens relevance, all
  had 0 DEGs in the focal thalamic glutamatergic cells.

The Distributed Agents corpus explicitly found that represented Maf/CNC-Bach/NRF-family
perturbations were non-interchangeable in postnatal neurons rather than a
generic bZIP/ARE loss module. That matters because HSF4 is a DNA-binding
stress-family transcription factor, but the measured neuronal screen strongly
penalizes family-level transfer unless a matched signature is actually present.

### Lens-development biology of HSF4

The external literature points to `Hsf4` as a specialized lens terminal
differentiation regulator, not as the primary neuronal heat-shock effector.
In Hsf4 mutant or knockout lens, Shi et al. 2009 showed cataracts with
down-regulation of `Crygs`, `Bfsp1`, and `Bfsp2`; Mou et al. 2009 identified
vimentin repression as another lens HSF4 target; Cui et al. 2018 showed that
MEK/ERK phosphorylation tunes HSF4 activity during postnatal lens development;
Morishita et al. 2021 linked HSF4-dependent lens differentiation to PLAAT
phospholipase-mediated organelle degradation; Cui et al. 2021 connected HSF4
loss to lens epithelial p21/senescence regulation; and Zhang et al. 2023 showed
that HSF4 transcriptionally activates the lens autophagy gene `Atg9a` during
terminal differentiation.

Those mechanisms are important in lens epithelial/fiber cells, but they are
imperfect matches to sparse, postmitotic, postnatal thalamic glutamatergic
neurons. The focal dataset also contains lens/regulatory counterexamples:
`Maf`, `Mafa`, `Mafb`, `Foxe3`, and `Pax6` all had 0 DEGs in this cell group.
That makes it unlikely that a CRISPR hit to another lens-enriched
transcriptional regulator would produce a detectable neuronal program unless
it also behaved like `Hsf1`; the measured `Hsf1` response was itself only 6
DEGs.

## Target-specific prediction

### Hsf4

`Hsf4` sits between two possible priors:

- As a heat-shock factor, the closest in-dataset perturbation is `Hsf1`, with
  6 DEGs and a narrow decrease of HSP/co-chaperone transcripts.
- As a lens differentiation factor, its measured developmental analogs are
  `Maf`, `Mafa`, `Mafb`, `Foxe3`, and `Pax6`, all with 0 DEGs in the focal
  `151 TH Prkcd Grin2c Glut` population.

I put more weight on the second lane and on the flat single-chaperone pattern.
The literature-supported HSF4 targets are lens crystallin, beaded-filament,
vimentin, p21/EZH2, PLAAT/organelle-clearance, and ATG9a/autophagy programs;
none is represented as a broad thalamic neuronal state in the training data.
The broad proteostasis controls (`Uba5`, `Ufc1`, `Psmb4`, `Psmc1`) prove that
the assay can detect hundreds to thousands of DEGs from severe protein-quality
control damage, but they are mechanistically too upstream and too damaging to
serve as direct HSF4 estimates.

Prediction: `Hsf4` will not have any genes passing FDR 0.05 in this focal cell
group, so `predicted_n_degs = 0`.

## Limits and uncertainty

- No `Hsf4` same-experiment corpus report or expression signature was available;
  the prediction extrapolates from `Hsf1`, chaperones, UPR/NRF/Maf boundaries,
  and external lens biology.
- Acute AAV CRISPR in the juvenile postnatal brain is not the same as germline
  Hsf4 loss in the developing lens. The strong cataract phenotype therefore
  should not be transferred literally to postmitotic thalamic neurons.
- The focal DE endpoint is FDR-thresholded and power-dependent. A prediction
  of zero allows for subthreshold changes in a few direct targets.
- Whole-profile similarities among almost-null signatures can look nonzero
  because most genes are weak, uncorrected background variation. I therefore
  relied on corrected DEG counts and interpretable HSP/UPR/lens feature
  evidence rather than on a single bulk cosine or family-frequency heuristic.
