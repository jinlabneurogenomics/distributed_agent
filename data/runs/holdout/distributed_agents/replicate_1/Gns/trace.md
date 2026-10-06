# DEG-count prediction trace

## Question and endpoint

The run asks for a point prediction of `n_degs` for the single held-out perturbation `Gns` in `151 TH Prkcd Grin2c Glut` cells. I treated `n_degs` exactly as in the supplied training-count table: all measured genes with Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05` in the focal cell group, including the targeted transcript when it is significant. The held-out `Gns` perturbation itself is absent from both supplied inputs, so the input dataset gives direct observations only for non-held-out analog perturbations.

The requested endpoint is directly observed for visible training perturbations and absent for `Gns`. I used the visible counts and differential-expression rows as the primary calibration evidence, the July `perturbai-july-260713-sourceguard-1773-v1` same-experiment corpus as packaged interpretation of those same Perturb-seq results, and external gene-function knowledge only to decide which visible perturbations are mechanistically comparable to `Gns`.

## Sources used

- Supplied training counts: `../../../../../inputs/holdout/151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`.
- Supplied DE table: `training differential-expression dataset`.
- Requested targets: `single-target request for Gns`.
- Same-experiment interpretive corpus: `perturbai-july-260713-sourceguard-1773-v1` Findings for `Ctsb`, `Psap`, `Lamp2`, `Gnptab`, `Gnptg`, `Sort1`, and `Tmem106b`.
- KEGG PATHWAY `mmu00531`, Glycosaminoglycan degradation, and Reactome mouse pathway `Degradation of the extracellular matrix`/heparan-sulfate catabolism entries, used only to place `Gns` in glycosaminoglycan and heparan-sulfate breakdown.
- PubMed literature:
  - Jakobkiewicz-Banecka et al. 2016, DOI: `10.2741/4463`, PMID: `27100513`.
  - Gaffke et al. 2017, DOI: `10.1007/s11011-017-0111-4`, PMID: `28921412`.
  - Roca et al. 2017, DOI: `10.1093/hmg/ddx058`, PMID: `28334745`.
  - Wang et al. 2020, DOI: `10.1021/acs.molpharmaceut.0c00831`, PMID: `33320673`.
  - Takahashi et al. 2021, DOI: `10.1016/j.ymgme.2021.11.010`, PMID: `34844863`.

## Quantitative calibration from the visible dataset

The focal-cell training table has 1,674 non-held-out biological targets. It is strongly zero-inflated: the median is 0 DEGs, the 75th percentile is 1 DEG, the 90th percentile is 2 DEGs, the 95th percentile is 18 DEGs, and only 28.0% of targets have any FDR 0.05 gene. That distribution makes a one-gene self-transcript call common among weakly active perturbations and makes broad DEG counts rare.

I then checked whether the closest heparan-sulfate mucopolysaccharidosis genes were visible training perturbations. `Sgsh`, `Naglu`, `Hgsnat`, `Ids`, `Idua`, `Gusb`, `Arsb`, `Arsa`, `Galns`, `Glb1`, `Hexa`, and `Hexb` were not in the focal training-count file. The represented lysosomal and heparan-sulfate-adjacent perturbations were therefore more indirect:

| Perturbation | Focal `n_degs` | Relationship to `Gns` | Focal interpretation |
| --- | ---: | --- | --- |
| `Gnptab` | 0 | Catalytic alpha/beta subunits of GlcNAc-1-phosphotransferase, upstream of mannose-6-phosphate targeting for soluble lysosomal hydrolases | No FDR 0.05 genes |
| `Gnptg` | 0 | Gamma subunit of the same M6P-tagging enzyme | No FDR 0.05 genes; self row was subthreshold at `pvals_adj = 0.459` |
| `Manba` | 0 | Single soluble lysosomal hydrolase | No FDR 0.05 genes |
| `Asah1` | 0 | Single lysosomal lipid hydrolase | No FDR 0.05 genes |
| `Ctsb` | 1 | Single lysosomal protease | The sole FDR 0.05 row was `Ctsb` itself |
| `Gaa` | 1 | Single lysosomal hydrolase causing a storage disease when fully absent | The sole FDR 0.05 row was `Gaa` itself |
| `Ppt1` | 1 | Single lysosomal enzyme causing neuronal ceroid lipofuscinosis when fully absent | The sole FDR 0.05 row was `Ppt1` itself |
| `Psap` | 1 | Lysosomal sphingolipid activator and storage-disease gene | The sole FDR 0.05 row was `Psap` itself |
| `Lamp2` | 0 | Lysosomal membrane/autophagy gene, not a hydrolase | No FDR 0.05 genes; its self row was just above threshold at `pvals_adj = 0.0537` |
| `Sort1` | 0 | VPS10 cargo receptor for lysosomal proteins including progranulin | No FDR 0.05 genes; its self row was subthreshold at `pvals_adj = 0.0939` |
| `Tmem106b` | 1 | Lysosomal membrane regulator | The sole FDR 0.05 row was `Tmem106b` itself |
| `Scarb2` | 1 | Lysosomal membrane protein and enzyme trafficking receptor | The sole FDR 0.05 row was `Scarb2` itself |
| `Hs6st2` | 0 | Heparan-sulfate sulfotransferase, biosynthetic rather than degradative | No FDR 0.05 genes |

The Parquet scan over the `151 TH Prkcd Grin2c Glut` row groups confirmed that the weak nonzero analogs above do not have any significant downstream focal rows once the self-transcript is excluded. Signed Wilcoxon score correlations among the focal `Ctsb`, `Psap`, `Lamp2`, `Gnptab`, `Gnptg`, `Sort1`, `Hs6st2`, and `Tmem106b` vectors were also noise-scale, from -0.066 to 0.075, so there is no hidden common low-level transcriptional module linking these weak lysosomal analogs.

Broader endolysosomal trafficking perturbations did produce detectable focal responses, but they are counterexamples rather than close estimates for `Gns`: `Vps35` had 17 focal DEGs, `Vps54` had 31, `Tsc2` had 86, `Rb1cc1` had 4, and `Cltc` had 3. Those results show that this thalamic glutamatergic group could respond to retromer/GARP, mTOR, autophagy-initiation, or clathrin stresses, but these perturbations change core trafficking or growth-control functions rather than the activity of one soluble heparan-sulfate sulfatase.

## Target-specific transfer for `Gns`

`Gns` encodes lysosomal N-acetylglucosamine-6-sulfatase. KEGG `mmu00531`, Reactome mouse heparan-sulfate degradation annotations, and reviews of Sanfilippo syndrome place GNS as one of the enzymes required for stepwise heparan-sulfate degradation; loss of SGSH, NAGLU, HGSNAT, or GNS causes mucopolysaccharidosis type III subtypes A to D, respectively (Jakobkiewicz-Banecka et al. 2016; Gaffke et al. 2017). Constitutive `Gns` knockout mice accumulate heparan sulfate, lose lysosomal homeostasis, develop widespread neuroinflammation and behavioral disease, and have astrocytic, microglial, and LAMP1 pathology by 12 weeks (Roca et al. 2017; Takahashi et al. 2021). Recombinant human GNS can be taken up through the M6P receptor and reverse glycosaminoglycan storage in deficient fibroblasts and neonatal mouse brain, supporting cross-correction by extracellular enzyme in mosaic settings (Wang et al. 2020).

That biology predicts the sign of the primary molecular consequence: `Gns` loss should reduce a single lysosomal sulfatase activity and promote heparan-sulfate substrate storage. The transfer to this Perturb-seq endpoint is weak, however, because the measured endpoint is not heparan sulfate or lysosomal enzyme activity but nuclear RNA from recovered neurons three to four weeks after sparse AAV CRISPR. Glial inflammatory and storage readouts dominate many complete MPS-IIID phenotypes but glia are under-sampled here, and wild-type neighboring cells can in principle secrete lysosomal enzymes that edited cells recapture through M6P-dependent routes. These facts make the causal chain `enzyme loss -> storage -> lysosomal stress/neuroinflammation -> many neuronal DEGs` uncertain and likely attenuated in this experiment.

The most relevant visible evidence points to a downstream-null call:

- `Gnptab` and `Gnptg` perturb the GlcNAc-1-phosphotransferase complex that marks soluble hydrolases for M6P trafficking. If partial, sparse disruption of soluble hydrolase delivery were enough to trigger TFEB/autophagy or storage-stress mRNA programs in recovered juvenile neurons, these two upstream perturbations should have been among the best visible analogs. Both instead had 0 focal DEGs, and the July corpus reports pan-neuronal FDR 0.10 nulls with absent lysosomal, cathepsin, autophagy, and UPR/ISR marker induction.
- Single-enzyme perturbations in the same cellular compartment were also null or self-only. `Manba` and `Asah1` had 0 focal DEGs; `Gaa`, `Ppt1`, `Ctsb`, and `Psap` had 1 DEG apiece, and the Parquet showed that those one-gene counts were just their own target transcripts. The same-experiment `Ctsb` and `Psap` reports likewise found no canonical lysosomal/autophagy/CLEAR or generic stress induction despite the known severe biology of complete lysosomal defects.
- `Lamp2`, `Sort1`, `Tmem106b`, `Scarb2`, `Grn`, `Sqstm1`, and v-ATPase subunits give the same direction of evidence. The close membrane/cargo perturbations were focal null or self-only, while the larger effects among `Vps35`, `Vps54`, and `Tsc2` occur at more pleiotropic retromer/GARP/mTOR nodes. I therefore did not use the larger `Vps35`, `Vps54`, or `Tsc2` counts as point estimates for a direct hydrolase.

For `Gns`, I predict zero FDR 0.05 rows in the focal group. A count of 1 is plausible if the targeted `Gns` transcript itself is well expressed and undergoes strong nonsense-mediated decay, because several weak lysosomal perturbations were self-only. I chose 0 rather than 1 because the stronger exact M6P analogs were 0 at the focal cutoff, `Lamp2`/`Sort1` illustrate near-threshold self loss that still failed FDR 0.05 in this class, and the downstream evidence for all close analogs was uniformly null. External MPS-IIID pathology increases confidence that complete organism-wide `Gns` loss is biologically important, but it does not justify predicting a broad acute neuronal snRNA response here.

## Limits

The best `Gns`-specific comparators were not present: the screen held out `Gns` and did not visibly train on the other direct Sanfilippo heparan-sulfate enzymes `Sgsh`, `Naglu`, or `Hgsnat`. The point prediction therefore extrapolates from M6P-tagging genes and other lysosomal storage genes, which share compartment and trafficking logic but not the identical substrate. The dataset measures steady-state nuclear RNA in surviving neurons, not heparan-sulfate storage, GNS protein, lysosomal pH, enzyme activity, non-neuronal inflammation, pre-assay cell loss, or glial-neuronal cross-correction. Finally, the zero-versus-one decision is cutoff-sensitive because the endpoint counts self-transcripts; a pure self-transcript FDR call would change the integer without implying a broader downstream `Gns` program.
