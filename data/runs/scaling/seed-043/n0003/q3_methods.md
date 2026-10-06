# Q3 cell-type specificity methods

## Eligibility

I used the manifest targets `Psmc1`, `Psmc5`, and `U2af2` without adding targets from the full screen. The exact downstream-DEG eligibility query was:

```sql
gene_target IN ('Psmc1', 'Psmc5', 'U2af2')
AND group_name IN (<23 allowed cell groups>)
AND pvals_adj < 0.10
AND lower(names) <> lower(gene_target)
```

A cell type with no rows for a target was treated as unrecovered rather than as a negative result, and rows for the perturbed transcript itself were removed before counting significant genes. This yielded 42 eligible target x cell-type pairs: 16 for `Psmc1`, 13 for `Psmc5`, and 13 for `U2af2`. Exactly 42 pair rows were emitted.

## Phenotype Characterization

For each eligible pair I read the full set of target-excluded FDR-significant genes, counted up- and down-regulated genes, and recorded the matched perturbed and control nucleus counts. For large signatures I selected representative genes from the dominant coherent modules rather than only the top Wilcoxon ranks: proteasome subunits, heat-shock or proteotoxic-stress genes, ubiquitin/Sqstm1/Bax/Ddit3 genes, and recurrent neuronal/synaptic losses for `Psmc1` and `Psmc5`; and spliceosome/RNA-processing genes such as `Rsrp1`, `Srrm2`, `Luc7l2`, `Srsf5`, `Rnpc3`, and `Tial1` for `U2af2`. For sparse pairs with one to six significant downstream genes, all significant genes were inspected and the row was assessed as a gene-level response because no broader module could be inferred.

The measured target transcript was not used to determine eligibility and was not used as the sole basis for any flag. `Psmc1` target mRNA was increased in `001 L5-6 IT Glut`, and `U2af2` target mRNA was modestly decreased in `151 TH Prkcd Grin2c Glut`; neither observation was interpreted as failed editing or as literature agreement.

## Literature Search

PubMed searches were built from the target symbols and protein aliases, including `Psmc1`, `PSMC1`, `Rpt2`; `Psmc5`, `PSMC5`, `Rpt6`, `SUG1`; and `U2af2`, `U2AF2`, `U2AF65`. I combined those aliases with central observed genes and modules: proteasome bounce-back, `NFE2L1`/`Nrf1`, 26S proteasome impairment, ubiquitin-positive neuronal inclusions, apoptosis or `BAX`/`DDIT3` for the proteasome targets, and `RSRP1`, `SRRM2`, `LUC7L2`, `RNPC3`, splicing-factor genes, cassette-exon inclusion, and U2AF65 knockdown for `U2af2`.

For sparse `No Literature` rows I also ran exact co-mention searches for the observed genes: for example `Psmc1` with `Pafah1b2/Ahi1/Nbdy/Entr1/Rnpc3`, `Psmc5` with `Fxyd5/Grm7/Epm2aip1/Kcnk9/Srcin1/Pabpn1/Dnajb4/Zfp260/Ppp3cb/Lrfn5/Fkbp2`, and `U2AF2` with `Dusp11/Stx5a/Kifap3/Ubr4/Rsrp1`. The exact searches for the isolated sparse `Psmc1` and `Psmc5` genes were empty or irrelevant; the only exact `U2AF2`/`RSRP1` hit was not a U2AF2-to-RSRP1 regulatory paper. Across each module class I reviewed the top PubMed titles and abstracts until either a target-specific bridge was found or the returned exact co-mentions were exhausted; no pair was left incompletely searched.

The reviewed support for `Psmc1` calls was the neuronal Psmc1 conditional-deletion paper plus two mechanistic Nrf1/NFE2L1 bounce-back papers. The reviewed support for `Psmc5` calls was one PSMC5 insufficiency/P320R study, one neuronal PSMC5 neurodevelopmental proteasomopathy study, and the same two Nrf1/NFE2L1 papers. The reviewed support for `U2af2` calls was one chromatin-bound U2AF2 knockdown study, one U2AF65 splice-site assembly study, and, where `Rsrp1` was central, one RSRP1 spliceosome paper. Sparse `No Literature` pairs were reviewed with the exact target-plus-gene searches described above and had no supporting paper to cite.

## Flag Decisions

`Agree` was assigned when the measured central module contained proteasome-subunit or proteotoxic-stress induction in the direction predicted by a complete chain: loss of the essential PSMC1 or PSMC5 19S ATPase impairs 26S proteasome function, and proteasome impairment activates the Nrf1/NFE2L1 bounce-back response that raises proteasome-subunit mRNAs. The PSMC1 evidence came from neuronal mouse conditional deletion, whereas the PSMC5 evidence included cell and neuronal disease-variant models; both differ from the acute in vivo CRISPR screen in modality, stage, and cell type.

`Inferred` was assigned when a specific bridge existed but did not determine the whole measured direction. Examples include small Psmc signatures with only one weak proteasome or ubiquitin gene plus unrelated genes, the Psmc5 Pvalb signature where leading synaptic/splicing genes were not predicted by PSMC5 papers, and broad `U2af2` signatures where U2AF2 knockdown is known to disrupt splicing-factor gene processing but not to lower `Rsrp1`, `Srrm2`, or `Luc7l2` transcript abundance in mouse neurons.

`No Literature` was assigned only after pair-specific searches failed to find either a direct target-to-gene relationship or a biologically specific partial bridge for the sparse observed response. General membership in the ubiquitin-proteasome system or the spliceosome was not enough when the measured row contained only an isolated, unrelated gene such as `Kifap3`, `Ubr4`, `Epm2aip1`, or `Fkbp2`.

## Multi-Module Pairs

For broad PSMC1 and PSMC5 pairs, I based the pair-level flag on the recurrent proteasome/stress module when multiple proteasome subunits or proteotoxic-stress genes were present, because that is the module with a target-specific directional prior. Down-regulation of synaptic, ion-channel, or neuronal identity transcripts was recorded in the evidence and summaries as a materially different co-occurring module, but it was not used alone as `Agree` support. `U2af2` pairs were reduced to one `Inferred` call when their central FDR genes formed a spliceosome/RNA-processing module; unrelated genes such as `Mfsd2b`, `Copb1`, and `Wipi2` were noted as unresolved parts of those signatures.

## Difficult Or Low-Confidence Pairs

The sparsest pairs were the lowest-confidence calls because their one to six downstream genes could represent real but idiosyncratic biology with little published coverage. `Psmc1` in `012 MEA LA CA1 DG Glut`, `027 NP-CT-L6b-OB Glut`, and `046 CTX-CGE GABA`, and `Psmc5` in `027 NP-CT-L6b-OB Glut` and `052 Pvalb Gaba`, were kept at `Inferred` because only part of the response overlapped the known proteasome-stress biology. `U2af2` calls were also conservative: even strong recurrent `Rsrp1` down-regulation was not upgraded to `Agree` because the U2AF2 literature documents splice-site selection and splicing-factor gene processing rather than transcript-level down-regulation of that gene.

Total eligible pairs: 42. Total emitted pairs: 42. Incompletely reviewed pairs: 0.
