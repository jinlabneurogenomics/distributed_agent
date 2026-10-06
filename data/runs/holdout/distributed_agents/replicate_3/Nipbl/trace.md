# Nipbl prediction for 151 TH Prkcd Grin2c Glut

## Question and interpretation

The requested held-out manifest contains a single target:

```tsv
target_name
Nipbl
```

I interpreted `n_degs` as the count, in `151 TH Prkcd Grin2c Glut` nuclei, of measured mouse genes with `pvals_adj < 0.05` in the matched Wilcoxon DE table for the acute P16 AAV-CRISPR perturbation. I treated `Nipbl` as entirely held out: there were no `Nipbl` rows in the supplied training DE parquet or in the training count table, and the Distributed Agents same-experiment corpus did not contain a `Nipbl` target node. I therefore used measured non-held-out perturbations, especially cohesin machinery in the same focal cell group, as analogs and boundaries.

## Sources used

- `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`: exact FDR 0.05 DEG-count endpoint for 1,674 non-held-out targets in the focal cell group.
- `[local file: training_de_all_cell_groups.parquet]`: per-gene DE rows. I filtered it to `151 TH Prkcd Grin2c Glut` and selected mechanistic cohorts to inspect signs, FDR 0.05/FDR 0.10 counts, and overlaps.
- Distributed Agents internal same-experiment corpus release `perturbai-july-260713-sourceguard-1773-v1`: I used `search_claims`, `target_context`, `resolve_evidence`, `candidate_set_topology`, and `shared_claim_context` for preinterpreted same-dataset findings around `Smc1a`, `Stag2`, `Stag1`, `Pds5a`, `Hdac8`, and related chromatin-loop controls.
- Distributed Agents run-local profile tools: I used `profile_neighbors` over all 1,674 focal-cell training targets and `profile_compare`/`profile_inspect` over a declared cohesin/Mediator cohort to verify that `Smc1a` and `Stag2` are mutual expression-signature neighbors and that adjacent null genes have weak or absent similarity.
- External PubMed-indexed literature:
  - Seitan et al. 2006, `10.1371/journal.pbio.0040242`, PMID 16802858: metazoan NIPBL/delangin binds MAU2/Scc4-like protein and functions as the cohesin loader.
  - Braunholz et al. 2011, `10.1038/ejhg.2011.175`, PMID 21934712: NIPBL variants can perturb the NIPBL-MAU2 interaction in Cornelia de Lange syndrome.
  - Deardorff et al. 2012, `10.1038/nature11316`, PMID 22885700: HDAC8 links the SMC3 acetylation cycle to Cornelia de Lange syndrome.
  - Sarogni, Pallotta & Musio 2019, `10.1136/jmedgenet-2019-106277`, PMID 31704779: review of CdLS genes in the cohesin pathway, including NIPBL, SMC1A, SMC3, RAD21, and HDAC8.
  - Newkirk et al. 2017, `10.1186/s13148-017-0391-x`, PMID 28855971: Nipbl haploinsufficiency decreases cohesin binding and preferentially affects activated genes in mouse embryonic fibroblasts.
  - Garcia et al. 2021, `10.1038/s41467-021-24808-z`, PMID 34315879: NIPBL/Scc2 disruption redistributes cohesin and changes CdLS fibroblast transcriptomes.
  - Weiss et al. 2021, `10.1038/s41467-021-23141-9`, PMID 34006846, and Calderon et al. 2022, `10.7554/eLife.76539`, PMID 35471149: acute cohesin removal in postmitotic cortical neurons disrupts neuronal gene-expression programs enriched for synaptic, signaling, learning, and behavior genes.
  - Casa et al. 2020, `10.1101/gr.253211.119`, and Arruda et al. 2020, `10.1186/s13072-020-00353-9`: STAG1 and STAG2 have both redundant and distinct cohesin gene-regulatory functions.
  - Arruda, Bryan & Dowen 2022, `10.1186/s13072-022-00463-6`, PMID 35986423, and Zhang, Coutinho & Pati 2021, PMID 34070827: PDS5A/B are cohesin regulators with partially distinct effects, so Pds5a flatness is a real boundary in this assay rather than evidence against NIPBL.

## Computation over the supplied DE data

I first summarized the focal training counts. The 1,674 visible training targets were highly zero-inflated: 1,205 had `n_degs = 0`, the median was 0, the 75th percentile was 1, the 95th percentile was 18, and only 43 targets had at least 100 DEGs. That scale matters because a 20-40 DEG effect is already a medium-sized, upper-tail response for this cell group even though it is much smaller than the broadest perturbations.

I then filtered the parquet to candidate cohesin, chromatin-loop, and Mediator analogs:

```sql
SELECT gene_target, names, logfoldchanges, scores, pvals_adj
FROM parquet_scan(training_de_all_cell_groups.parquet)
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (
    'Smc1a','Stag2','Stag1','Pds5a','Hdac8','Ctcf',
    'Med13','Med15','Med23','Med13l','Cdk8',
    'Ncapd3','Prr12','Smchd1','Zfp609'
  );
```

The exact FDR 0.05 DEG counts from this filtered table agreed with the training endpoint: `Smc1a=24`, `Stag2=37`, `Ctcf=270`, `Med13=11`, `Med15=19`, `Med23=13`, `Med13l=1`, and `Stag1`, `Pds5a`, `Hdac8`, `Ncapd3`, `Prr12`, `Smchd1`, `Zfp609`, and `Cdk8` were all 0. At FDR 0.10, the same query gave `Smc1a=35` and `Stag2=55`.

I inspected signed overlaps among the FDR hits. At FDR 0.05, `Smc1a` and `Stag2` shared 9 significant genes, all with the same direction (`Adamts19`, `Adamts2`, `Inhbb`, `Necab2`, `Ptprm`, `Sema5a`, `Smtn`, `Sox13`, `Utp14b`). At FDR 0.10, their overlap rose to 14/14 same-direction genes and the run-local profile found them to be each other's strongest whole-profile neighbor among the declared mechanistic cohort. The `Smc1a`/`Stag2` module was dominated by down-regulated adhesion, extracellular matrix/guidance, excitability, and neuronal-signaling genes such as `Ptprm`, `Sema5a`, `Adamts2`, `Adamts19`, `Necab2`, `Grin2c`, `Atp2a2`, `Atp2b1`, `Pcp4`, and `Lrrc7`.

## Target-specific reasoning

### Nipbl

`Nipbl` encodes the mammalian Scc2/delangin subunit of the NIPBL-MAU2 cohesin-loading complex. Biochemically it is closer to core cohesin loading than `Pds5a`, `Hdac8`, or `Stag1`: Seitan et al. showed that metazoan delangin/NIPBL and MAU2 form the Scc2/Scc4-like loader, and Braunholz et al. showed that CdLS NIPBL missense variants can reduce MAU2 binding. NIPBL is also the dominant CdLS gene, and the CdLS pathway includes core and cycle cohesin genes such as `SMC1A`, `SMC3`, `RAD21`, and `HDAC8` (Deardorff 2012; Sarogni 2019). In external systems, Nipbl/NIPBL reduction changes cohesin binding or redistribution and produces transcriptional dysregulation rather than a purely mitotic phenotype (Newkirk 2017; Garcia 2021).

The best within-dataset positive analogs were therefore the two measured cohesin-ring perturbations that actually fired in `151 TH Prkcd Grin2c Glut`:

- `Smc1a`: 24 DEGs at FDR 0.05; 35 at FDR 0.10 in my parquet filter.
- `Stag2`: 37 DEGs at FDR 0.05; 55 at FDR 0.10.

The Distributed Agents corpus independently summarized these as a high-confidence thalamic cohesin module: `Smc1a` and `Stag2` both depress a down-regulated neuronal connectivity/signaling program in `151 TH Prkcd Grin2c Glut`, with `Stag2` the strongest same-direction `Smc1a` neighbor over the 151 signature. The corpus evidence gave 14 same-direction and 0 opposite-direction FDR 0.10 overlaps between the `Smc1a` and `Stag2` signatures, and my direct FDR 0.05 query recovered the same structure with 9 same-direction shared hits.

The important counterexamples were the measured cohesin-adjacent genes:

- `Stag1`: 0 DEGs at FDR 0.05 in the endpoint table and only one FDR 0.10 gene, `Gabra1`, in the corpus; it did not reproduce the multi-gene `Smc1a`/`Stag2` module.
- `Pds5a`: 0 DEGs at FDR 0.05/FDR 0.10 in the focal group and no robust same-direction overlap with either core cohesin signature. The corpus also reported pan-neuronal FDR-level non-response for acute `Pds5a`.
- `Hdac8`: 0 DEGs at FDR 0.05/FDR 0.10 in the focal group and no FDR 0.10 downstream DE in any recovered neuronal group, despite its known role in SMC3 deacetylation.
- broader SMC/chromosome-architecture controls `Ncapd3`, `Smchd1`, `Prr12`, and `Zfp609`: all flat in 151 and all used in the corpus as boundaries showing that the `Smc1a`/`Stag2` state is not a generic SMC/chromatin-loop response.

I also checked `Ctcf` and Mediator subunits as pathway-adjacent positive controls. `Ctcf` is active and much broader in 151 (`270` DEGs at FDR 0.05), but the Distributed Agents corpus explicitly notes that its Pcdh-heavy acute neuronal state is not phenocopied by the represented cohesin-machinery perturbations. `Med13`, `Med15`, and `Med23` form a separate low-teen down-regulated module (`11`, `19`, `13` DEGs) and overlap `Smc1a` mainly on a few calcium/excitability genes such as `Atp2a2`, `Atp2b1`, and `Pcp4`; they are useful scale comparators but not stronger mechanistic anchors for NIPBL than `Smc1a`/`Stag2`.

This led to a nonzero call. NIPBL is upstream of cohesin loading and CdLS gene regulation, and postmitotic neurons remain sensitive to cohesin loss, so an all-zero prediction would ignore both the external loader biology and the measured `Smc1a`/`Stag2` module. I did not assign a `Ctcf`- or broad-chromatin-scale count, because the direct measured core-cohesin responses in this exact P16 mosaic neuronal assay are only 24 and 37 DEGs at the requested FDR cutoff, and several named cohesin-cycle regulators are flat. I therefore centered the point estimate on the `Smc1a`/`Stag2` FDR 0.05 counts and rounded the midpoint, giving `31` predicted DEGs for `Nipbl`.

## Limits and extrapolation

- `Nipbl`, `Mau2`, `Rad21`, `Smc3`, `Wapl`, `Pds5b`, `Esco1`, and `Esco2` were not represented as training perturbation targets, so the prediction extrapolates from `Smc1a`, `Stag2`, `Stag1`, `Pds5a`, and `Hdac8`.
- The screen readout is acute sparse AAV CRISPR in recovered postmitotic NeuN+ nuclei. It will miss embryonic CdLS phenotypes, sister-chromatid cohesion defects, chromatin-loop changes without nuclear RNA consequences, glial effects, and severe edits that deplete cells before recovery.
- Weak target mRNA reduction was not used to reject `Stag2` or `Pds5a`; the dataset documentation and corpus both note that self-transcript loss is not a quantitative editing-efficiency measure in this assay.
- The `Smc1a`/`Stag2` overlap is strong for this small thalamic module but partial. `Nipbl` could be weaker if residual loaded cohesin persists for the 3-4 week window or stronger if a loader perturbation reduces both STAG1- and STAG2-containing cohesin.
- Broad expression neighbors such as `Ctcf`, `Elp1`, `Brd4`, and `Ctnnb1` share subsets of the thalamic neuronal state but have hundreds of additional DE genes. I used them to bound plausibility, not to inflate the final `Nipbl` count.
