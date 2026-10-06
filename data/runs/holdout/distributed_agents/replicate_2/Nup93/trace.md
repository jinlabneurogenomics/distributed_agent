# Held-out question

The requested held-out target file contains one perturbation, `Nup93`.  I interpreted the
task as a point prediction for the number of measured genes with
`pvals_adj < 0.05` in `151 TH Prkcd Grin2c Glut` after acute AAV-CRISPR
loss of `Nup93`, using only non-held-out perturbations from the supplied
parquet/CSV and external biology of NUP93.  I did not treat `n_degs` as an
intrinsic essentiality score: the screen used sparse postnatal editing,
single-nucleus RNA, and a Wilcoxon/FDR endpoint, so a true nuclear-pore defect
can be small or large depending on protein lifetime, focal-cell sensitivity, and
RNA-level coupling.

# Sources

## Same-experiment data

- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: focal-cell DEG counts for
  1,674 non-held-out training targets.  The endpoint was sparse: 1,205/1,674
  targets had `n_degs = 0`; the median was 0; the 90th, 95th, and 99th
  percentiles were 2, 18, and 436.5 DEGs; the maximum was `Uba5`, 2,677 DEGs.
- `training_de_all_cell_groups.parquet`: focal-cell per-gene log2 fold changes
  and adjusted p-values for selected analogs and counterexamples.  I queried the
  parquet with DuckDB:

```sql
SELECT gene_target, names, logfoldchanges, pvals_adj
FROM read_parquet('training_de_all_cell_groups.parquet')
WHERE group_name = '151 TH Prkcd Grin2c Glut'
  AND gene_target IN (...)
```

  I then counted significant rows with `pvals_adj < 0.05` and compared two
  signatures by intersecting their FDR-significant measured genes and counting
  log-fold-change sign agreement.
- Distributed Agents same-experiment corpus, release
  `perturbai-july-260713-sourceguard-1773-v1`.  `target_context` has no held-out
  `Nup93` entry, but it has curated same-experiment findings for two represented
  nucleoporins.  The relevant corpus observations were that `Tpr` was a broad
  but cell-type-selective responder, especially in `155 MB Glut` and
  `151 TH Prkcd Grin2c Glut`; `Tpr` recurrently changed nuclear-transport and
  NXF1-adjacent export genes; `Tpr` converged with spliceosome/RNA-export genes
  and with `Uba5`, `Ufc1`, `Psmb4`, and `Psmc1`; and `Ranbp2` was much more
  cell-type restricted, with its strongest program in `308 CB GABA` and no
  focal-cell DEGs.
- Distributed Agents run-local profile comparison
  `nup93_npc_export_compare.json`/`nup93_npc_export_cohort.json`, computed for
  `Tpr`, `Ranbp2`, RNA-export/spliceosome responders, proteostasis responders,
  and flat transport controls in the focal cell group.  These diagnostics
  confirmed that the broad responders were mostly same-direction at
  FDR-supported Tpr-overlapping genes, but also showed that whole-profile
  correlations can put zero-DEG `Kpna3` and `Xpo7` near `Tpr`; I therefore used
  FDR-supported overlaps and known NPC topology rather than raw all-gene
  correlation as the deciding evidence.

## External mechanism

- Nup93/Nic96 is a conserved core NPC scaffold that forms a complex with NUP205
  and is required for correct vertebrate nuclear pore assembly: Grandi et al.,
  1997, PMID 9348540, DOI 10.1091/mbc.8.10.2017.
- The metazoan Nup93 complex is an essential inner-ring linker between the
  central transport channel and the nuclear envelope, with roles in NPC assembly
  and transport beyond assembly alone: Vollmer and Antonin, 2014, PMID 24572986,
  DOI 10.1515/hsz-2013-0285.
- Vertebrate inner-ring structure places NUP93 helices into NUP205/NUP188 and
  anchors the Nup62/Nup58/Nup54 central-channel heterotrimer on this scaffold:
  Huang et al., 2022, PMID 35301439, DOI 10.1038/s41422-022-00633-x.
- Human NUP93 and NUP205 variants perturb NPC assembly and are sufficient to
  cause steroid-resistant nephrotic syndrome, showing that partial disease
  alleles in the inner-ring scaffold can have strong cell-biological output:
  Braun et al., 2016, PMID 26878725, DOI 10.1038/ng.3512.
- The closest assayed same-experiment analog, `Tpr`, is not an inner-ring Nup;
  it is a nuclear-basket factor with a distinct role in TREX-2/NXF1-dependent
  mRNA export and in mRNA entry into NPCs: Aksenova et al., 2020, PMID
  32917881, DOI 10.1038/s41467-020-18266-2; Li et al., 2021, PMID 34504007,
  DOI 10.1073/pnas.2015621118.

# Focal-cell analog evidence

The training analogs I considered were:

| training target | focal `n_degs` | focal overlap with `Tpr` | interpretation for `Nup93` |
| --- | ---: | ---: | --- |
| `Tpr` | 1768 | self | Most direct assayed nucleoporin responder in the focal group. It is a nuclear-basket, mRNA-export perturbation rather than an inner-ring scaffold, so it is an analog for RNA-export stress, not for NPC assembly itself. |
| `Thoc1` | 303 | 114 shared, 103 same-sign | TREX/mRNP-biogenesis comparator. Its same-experiment corpus entry was a partial Tpr phenocopy; focal overlap is strongly same-direction but much smaller than Tpr. |
| `Tnpo3` | 618 | 265 shared, 260 same-sign | Nuclear-transport/RNA-processing neighbor of broad Tpr-like states. The high same-sign overlap supports a reusable nuclear-transport stress axis. |
| `U2af2` | 828 | 252 shared, 220 same-sign | Splicing and mRNP maturation comparator; broad focal responder that overlaps Tpr but is not an NPC structural perturbation. |
| `Rnpc3` | 868 | 243 shared, 194 same-sign | Spliceosome comparator with a very broad focal response; same-direction overlap with Tpr argues that impaired mRNP processing and Tpr/NPC stress meet downstream. |
| `Cdc40` | 624 | 216 shared, 201 same-sign | Splicing comparator that also up-regulated nuclear-pore/chromatin genes in the same corpus. |
| `Prpf6` | 454 | 167 shared, 161 same-sign | Spliceosome comparator with the same-direction arm of the Tpr program, but smaller than Tpr. |
| `Snrnp70` | 213 | 82 shared, 71 same-sign | Smallest of the robust splicing comparators; useful as a lower bound for a real but less pleiotropic RNA-processing hit. |
| `Uba5` | 2677 | 742 shared, 678 same-sign | UFMylation/proteostasis neighbor of Tpr and the largest focal training response. It bounds the high end but is likely downstream proteostasis convergence, not an inner-ring NPC phenocopy. |
| `Ufc1` | 572 | 242 shared, 230 same-sign | UFMylation comparator; strong same-direction overlap with Tpr but lower count. |
| `Psmb4` | 742 | 261 shared, 236 same-sign | Proteasome comparator from the Tpr corpus neighborhood; appropriate as a downstream stress-state comparator. |
| `Psmc1` | 430 | 149 shared, 136 same-sign | Proteasome comparator with a smaller focal response than `Psmb4`. |
| `Ranbp2` | 0 | 0 FDR overlap | Nucleoporin counterexample. RanBP2 lies on cytoplasmic filaments/SUMO machinery rather than the inner ring or nuclear basket, and in this focal group it was FDR-flat. |
| `Kpna3` | 0 | 0 FDR overlap | Import receptor counterexample: generic nuclear-import membership was not enough to make a focal response. |
| `Xpo7` | 0 | 0 FDR overlap | Export receptor counterexample: generic transport machinery was not enough to make a focal response. |

Other obvious stress readouts were weak in the focal cell group: `Mtor` had 2
DEGs, `Ogt` had 4, `Atg5` and `Becn1` had 0, `Sqstm1` had 1, `Hspa5` had 5,
`Cltc` had 3, and `Trp53` had 0.  Those counts argue against converting
`Nup93` to an enormous response merely because it can stress nuclear transport,
autophagy, or p53 pathways.

# Target-specific prediction

## `Nup93`

I predict a broad nonzero response.  `Nup93` is in the NPC central scaffold
rather than in a peripheral receptor pathway: its complex with Nup205/Nup188
and its anchoring of the Nup62/Nup58/Nup54 central channel put it upstream of
bulk transport and mRNA-export defects.  That makes the zero-DEG `Kpna3`,
`Xpo7`, `Mtor`, and `Atg5` outcomes poor positive analogs; those are useful
only as warnings that pathway labels alone should not force a response.

The best positive same-experiment anchor is `Tpr` at 1,768 focal DEGs.  Tpr loss
in the corpus changed nuclear-transport genes (`Xpo1` up, `Nxf1` down) and
formed a transcriptomic neighborhood with `Thoc1`, spliceosome factors, and
UFMylation/proteasome perturbations.  The focal-cell parquet supported the same
geometry: Tpr's FDR genes were shared in the same direction with `Tnpo3`
(260/265 shared genes same-sign), `Cdc40` (201/216), `Prpf6` (161/167),
`Thoc1` (103/114), `Ufc1` (230/242), and `Uba5` (678/742).  This places
Tpr on a large RNA-processing/proteostasis stress axis that the 151 TH neurons
can mount.

I discounted `Nup93` downward from `Tpr`, however, for three reasons.  First,
Tpr is a nuclear-basket factor with an acute TREX-2/NXF1 export role, whereas
Nup93 is a core scaffold in already assembled NPCs; postmitotic neurons may
buffer partial Nup93 mRNA editing by long-lived pores.  Second, the only
assayed nucleoporin outside the basket, `Ranbp2`, had 0 focal DEGs, and the
Distributed Agents corpus specifically rejected `Ranbp2` as a simple Tpr phenocopy.
Third, no `Nup93`-complex members such as `Nup205`, `Nup188`, `Nup155`, or
`Nup35` were in the focal training target set, so extrapolating from `Tpr` and
spliceosome/proteasome responders is necessarily indirect.

Balancing those facts, I put `Nup93` above the 300 to 600 DEG range of the
weaker export/splicing analogs (`Thoc1`, `Prpf6`, `Snrnp70`) and near the
600 to 900 DEG range of `Tnpo3`, `Cdc40`, `U2af2`, `Rnpc3`, and `Psmb4`, but
well below the focal `Tpr` count and far below `Uba5`.  The resulting point
prediction is **900 DEGs**.

# Limits

The strongest limitation is absence of a same-complex training perturbation:
the dataset lacks assayed `Nup205`, `Nup188`, `Nup155`, `Nup35`, and `Ndc1`
targets in the focal endpoint, and the Distributed Agents corpus intentionally contains
no held-out `Nup93` findings.  `Tpr` is a biologically relevant nuclear-pore
comparator but sits on a different face of the NPC, while `Ranbp2` is an
informative nucleoporin counterexample but also a different NPC substructure.
The prediction therefore extrapolates from an mRNA-export/proteostasis axis
rather than from a direct inner-ring scaffold analog.  Finally, snRNA abundance
does not measure nuclear export flux, pore number, or preexisting NUP93 protein
turnover, so the true `Nup93` response could collapse toward zero if the
postmitotic scaffold is unusually buffered, or move toward Tpr/Uba5 if partial
inner-ring loss disrupts NPC function broadly in these thalamic neurons.
