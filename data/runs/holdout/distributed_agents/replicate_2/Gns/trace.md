# DEG-count prediction for `Gns`

## Question and interpretation

The held-out target list contains one perturbation, `Gns`. I interpreted the requested endpoint as the integer number of measured genes with `pvals_adj < 0.05` in the `151 TH Prkcd Grin2c Glut` contrast, exactly as tabulated in `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`. The count includes the perturbed gene itself when the target transcript is significantly lower: for example, the focal-cell `Gaa`, `Ctsb`, and `Ppt1` training counts are all `1`, and the only significant measured gene in each case is the knocked-out target transcript.

The important ambiguity was therefore whether to predict a downstream lysosomal-storage program or only a possible self-transcript hit. I treated `n_degs = 1` as "no detectable downstream RNA response, target transcript only", not as evidence for a broad biological state.

## Sources used

- Direct training endpoint: `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`.
- Direct differential-expression rows: `[local file: training_de_all_cell_groups.parquet]`, filtered to `group_name = '151 TH Prkcd Grin2c Glut'`.
- PerturbAI bundled gene-annotation and gene-analog stores, drawing on GO, KEGG, Reactome, CORUM and STRING physical interaction v12.0 annotations.
- The selected same-experiment Distributed Agents corpus, `perturbai-july-260713-sourceguard-1773-v1`, for interpreted findings on measured lysosomal hydrolase and endolysosomal perturbations.
- PubMed literature:
  - Gilkes and Heldermon 2014, PMID 25345095: Sanfilippo type D is caused by deficient N-acetylglucosamine-6-sulfatase/GNS in heparan-sulfate degradation.
  - Wang et al. 2021, DOI 10.1021/acs.molpharmaceut.0c00831, PMID 33320673: recombinant human GNS is taken up through the mannose-6-phosphate receptor and can reduce intracellular GAGs in MPS IIID cells/mice.
  - Takahashi et al. 2021, DOI 10.1016/j.ymgme.2021.11.010, PMID 34844863: constitutive `Gns` knockout mice develop glial activation and lysosomal pathology on the scale of 12 to 48 weeks.
  - Oh 2015, DOI 10.5483/bmbrep.2015.48.8.101, PMID 25999178, and Grubb et al. 2010, DOI 10.1089/rej.2009.0920, PMID 20345279: soluble lysosomal hydrolases can be secreted, recaptured through carbohydrate/M6P receptors and used therapeutically as cross-correcting enzymes.

## Dataset computations

I first summarized the training count distribution in the focal group. It is highly zero-inflated: 1205/1674 perturbations have `n_degs = 0`, the median is 0, the 90th percentile is 2, and only 43/1674 have at least 100 DEGs. This made it important not to inflate a prediction solely because chronic germline GNS deficiency is severe.

I then used the PerturbAI gene-annotation store to place `Gns`. The exact KEGG `Glycosaminoglycan degradation` and GO `heparan sulfate proteoglycan catabolic process` target sets contained `Gns` but no non-held-out training perturbation, so no direct Sanfilippo-enzyme donor was available. The broader candidates came from lysosome, lysosomal vesicle biogenesis, M6P hydrolase sorting, and glycosaminoglycan metabolism annotations.

For the focal cell group I queried the parquet for those candidates:

```sql
select gene_target,
       sum(pvals_adj < 0.05) as n_sig,
       min(pvals_adj) as min_q
from parquet_scan(...)
where group_name = '151 TH Prkcd Grin2c Glut'
  and gene_target in (...)
group by gene_target;
```

I also inspected the actual significant rows to determine whether a `1` count was a self-transcript event or a downstream signature, and I ran `profile_compare` over a 24-gene lysosome/GAG-adjacent cohort using `logfoldchanges` as the signed vector and `pvals_adj < 0.05` as the significant-feature definition.

Key focal-cell observations were:

| training perturbation | `n_degs` | why it mattered |
|---|---:|---|
| `Gaa` | 1 | closest soluble lysosomal hydrolase analogy in the training set; the single DEG was `Gaa` itself, logFC -0.709, q=8.97e-16. |
| `Ctsb` | 1 | another lysosomal hydrolase; the single DEG was `Ctsb` itself, logFC -1.480, q=8.54e-43. |
| `Ppt1` | 1 | soluble lysosomal enzyme causing a neuronal storage disease when chronically absent; the single DEG was `Ppt1` itself, logFC -0.536, q=1.34e-5. |
| `Manba` | 0 | soluble lysosomal hydrolase; no focal-cell FDR hit. |
| `Gnptab`, `Gnptg` | 0, 0 | M6P tag-synthesis components for soluble lysosomal hydrolase trafficking; both were focal-cell nulls. |
| `Lamp2` | 0 | lysosomal membrane/cargo pathway comparator; focal-cell null. |
| `Atp6v0a1`, `Atp13a2`, `Scarb2`, `Tmem106b` | 1 each | endolysosomal membrane proteins or transporters; each had one focal-cell DEG, its own transcript. |
| `Cltc`, `Ap1b1`, `Ap1s2`, `Ap4s1` | 3, 1, 0, 0 | lysosome-vesicle-biogenesis / TGN adaptors are broader trafficking hits or nulls, not direct GNS enzymatic analogs. |
| `Ext1`, `Ext2`, `B3gat3`, `Gpc6`, `Hs6st2` | 0, 0, 0, 0, 0 | upstream heparan-sulfate synthesis/remodeling targets were silent in this endpoint. |
| `Hspa8` | 9 | chaperone-mediated autophagy/lysosome-associated chaperone with a small heat-shock-like response; not a hydrolase analog. |
| `Rab7` | 501 | strong positive late-endosomal/lysosomal compensation state; useful as an upper boundary, but too proximal and pleiotropic to transfer directly to a single soluble hydrolase. |

The same-experiment Distributed Agents corpus agreed with this reading. Its `Gaa` findings described acute neuronal `Gaa` loss as pan-neuronally downstream-flat despite self-transcript loss, and explicitly noted the cross-correctable, mosaic-enzyme explanation as a caveat. Its `Gnptab` findings grouped `Gnptab`, `Gnptg`, `Manba`, `Ppt1`, and `Psap` as largely buffered hydrolase/M6P-pathway perturbations rather than as a shared storage-stress RNA module. Its `Rab7` findings showed that the assay could see a true late-endosomal/lysosomal compensation program, including V-ATPase, `Lamp2`, `Mcoln1`, `Dpp7`, and hydrolase transcripts; `Rab7` therefore served as a positive control and ceiling, not as a count donor for `Gns`.

The profile comparison was consistent with sparse, mostly self-only activity around the candidate set: among the 24 lysosome/GAG candidates, 12 had no significant focal-cell features, 11 had 1 to 9, and only `Rab7` had more than 50. The focused signed-profile inspection of `Gaa`, `Manba`, `Gnptab`, `Hspa8`, and `Rab7` against hydrolase/M6P peers found no significant-feature intersections for `Gaa`, `Manba`, or `Gnptab`; their apparent full-vector correlations were low-amplitude background structure rather than shared FDR programs.

## Target-specific reasoning

`Gns` encodes lysosomal N-acetylglucosamine-6-sulfatase, needed for heparan-sulfate and keratan-sulfate degradation. Complete inherited GNS deficiency causes mucopolysaccharidosis IIID/Sanfilippo D, and chronic germline `Gns` knockout mice accumulate CNS pathology with LAMP1, astrocyte and microglial markers by 12 weeks and later substrate-related neuronal storage. That external biology says GNS loss is a real lysosomal defect, but it also argues for slow substrate accumulation, not an immediate transcription-factor perturbation.

The Perturb-seq setting is the opposite of a complete congenital storage model: P16-to-P37/44 sparse CRISPR in a mosaic brain, with neighboring non-edited cells still able to secrete soluble lysosomal enzymes. The Wang et al. recombinant-GNS experiment and general M6P-enzyme-replacement literature show that GNS and other lysosomal hydrolases are cross-correctable proteins. That makes `Gns` more comparable to `Gaa`, `Manba`, `Ppt1`, `Ctsb`, and `Gnptab`/`Gnptg` than to the high-count `Rab7` trafficking hub.

The decisive within-dataset evidence was that the soluble hydrolase and M6P-sorting analogs were all focal-cell null or self-only:

- `Gaa`, `Ctsb`, and `Ppt1` each gave exactly one focal DEG and that gene was the target transcript itself.
- `Manba`, `Gnptab`, and `Gnptg` gave no focal DEGs.
- The broader GAG-production genes `Ext1`, `Ext2`, `B3gat3`, `Gpc6`, and `Hs6st2` were all zero.
- Endolysosomal membrane targets with self-only hits (`Atp6v0a1`, `Atp13a2`, `Scarb2`, `Tmem106b`) reinforced that isolated self-transcript calls are common in this neighborhood.

I therefore predict no downstream GNS-induced storage-stress program at FDR 0.05. I assign a count of `1` rather than `0` because `n_degs` includes the knocked-out transcript and `Gns` appears detectable in these neurons: in the training data, `Rab7` knockout significantly up-regulated measured `Gns` itself in this focal group (logFC 0.310, q=0.0327). The closest self-detectable soluble hydrolase, `Gaa`, was self-only with a similar buffered downstream state. A zero would be plausible if the `Gns` CRISPR transcript effect failed to cross FDR; a count above one would require downstream substrate stress in a short, sparse, cross-correcting setting and is less supported by the measured hydrolase/M6P analogs.

## Limits

- The training universe lacks `Sgsh`, `Naglu`, `Hgsnat`, `Ids`, `Gusb`, `Arsb`, `Hexa`, `Hexb`, `Glb1`, and `Gba`, so the most exact heparan-sulfate and GAG-storage enzyme comparators were not observed.
- The assay measured nuclear RNA in surviving NeuN-positive nuclei, not GNS enzyme activity, heparan-sulfate storage, lysosomal pH, protein turnover, indel rate, glial inflammation, or long-term degeneration.
- `Rab7` proves that the screen can see a lysosomal compensation module, but its operation is a late-endosomal trafficking block rather than loss of one soluble hydrolase; I used it only as a positive boundary.
- Predicting one DEG depends on the self-transcript crossing FDR, which is stochastic and guide/context dependent. The biological downstream prediction is stronger than the exact distinction between `0` and `1`.
