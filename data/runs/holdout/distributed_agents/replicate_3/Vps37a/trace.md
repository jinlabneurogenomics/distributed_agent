# Vps37a prediction for `151 TH Prkcd Grin2c Glut`

## Question and resolved ambiguities

The requested endpoint is the number of assayed genes with `pvals_adj < 0.05`
after CRISPR loss of a held-out perturbation in the focal neuronal group
`151 TH Prkcd Grin2c Glut`. The manifest for this run contains one held-out
target:

| held-out target | prediction |
|---|---:|
| Vps37a | 0 |

I treated the endpoint as an integer FDR-count in the supplied focal
`151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`, not as a count at the
FDR<0.10 threshold that appears in some same-experiment corpus summaries.
`Vps37a` was absent from both the training counts and the training DE parquet
as a perturbation, so all evidence had to be transferred from other targets.

## Sources used

- Differential-expression parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training endpoint:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Requested-target manifest:
  `[local file: 262_Vps37a.csv]`
- Internal curated same-experiment corpus:
  Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`.
- Run-local observed-profile analysis:
  Distributed Agents runtime `profile_compare`/`profile_cohort` over the focal-cell
  log-fold-change profiles.
- External mechanism: PubMed-indexed literature on ESCRT-I, VPS37A-specific
  MVB/autophagosome closure, and neuronal ESCRT biology.

## Computation over the supplied data

The DE parquet has 616,253,184 rows in 712 row groups. Its row groups are
sorted by `group_name`; metadata showed only 35 row groups could contain
`151 TH Prkcd Grin2c Glut`, so I used `group_name =
'151 TH Prkcd Grin2c Glut'` filters for all parquet queries. The focal group
contains 28,891,566 rows, 1,674 non-held-out perturbations, and 17,259 measured
gene features.

From the count CSV, the training response distribution in the focal group was
heavily concentrated at zero or one FDR hit:

| focal `n_degs` bin | target count |
|---|---:|
| 0 | 1,205 |
| 1 | 276 |
| 2-9 | 87 |
| 10-49 | 47 |
| 50-199 | 30 |
| >=200 | 29 |

I queried the count table for ESCRT, endosomal, lysosomal, autophagy,
retrograde-trafficking and sterol-homeostasis neighbors. Most exact ESCRT
members were not in training: `Tsg101`, `Vps28`, `Vps37b`, `Vps37c`,
`Vps37d`, `Mvb12a/b`, `Ubap1`, `Snf8`, `Vps25`, `Vps36`, `Chmp1/2/3/5/6/7`,
`Vps4a/b`, `Vta1`, `Ist1`, `Pdcd6ip`, `Hgs`, and `Stam` were absent. The
useful represented analogs and counterexamples were therefore one direct
ESCRT-III subunit plus neighboring trafficking pathways:

| training target | focal `n_degs` | relevance to Vps37a |
|---|---:|---|
| Chmp4b | 0 | Direct ESCRT-III membrane-scission machinery, downstream of ESCRT-I; best represented ESCRT counterexample. |
| Atg5 | 0 | Core macroautophagy, tests the autophagy arm that VPS37A helps finish at phagophore closure. |
| Atg16l1 | 0 | LC3-lipidation/autophagy machinery; flat in the focal group. |
| Becn1 | 0 | Autophagy initiation/PI3K complex; flat in the focal group. |
| Sqstm1 | 1 | Autophagy cargo-receptor stress marker; only its own transcript passed FDR. |
| Rab7 | 501 | Strong late-endosome/lysosome positive control, but biologically downstream/parallel and much broader than ESCRT-I. |
| Vps41 | 0 | HOPS/Rab7 late-fusion complex member; flat in the focal group despite weak Rab7 sharing elsewhere. |
| Vps35 | 17 | Retromer, endosome retrieval rather than ESCRT; modest 151-specific response. |
| Vps35l | 0 | Retriever/Commander retromer-like branch; flat. |
| Washc4 | 0 | WASH actin/retrieval pathway; flat. |
| Vps53 | 0 | GARP/EARP subunit; same broad retrograde compartment as Vps54 but flat. |
| Vps54 | 31 | GARP subunit; modest 151-specific state, not shared by Vps53 or Vps35. |
| Trappc6b, Trappc9, Trappc10 | 0, 0, 0 | TRAPP trafficking comparators; all flat. |
| Ocrl, Gdi1, Tmem106b | 0, 1, 1 | Endolysosomal/Rab/lysosomal comparators showing buffered or self-only responses. |
| Depdc5, Dctn1, Mib1, Marchf6, Selenoi, Htt | 13, 75, 27, 14, 5, 3 | Sterol/lipid stress comparators; useful for recognizing the Rab7/Dctn1 sterol state but not proximal ESCRT analogs. |

To check whether the represented endolysosomal targets formed a coherent
profile neighborhood, I ran a Distributed Agents runtime profile comparison over 29 of
the above perturbations using `logfoldchanges` as the signed vector and
`pvals_adj < 0.05` only to annotate significant-feature overlap. All 29 nodes
were present. Fourteen of the 29 had no significant focal features; only Rab7
and Dctn1 exceeded 50 focal DEGs. Pairwise sharing was weak: across all 406
pairs, positive top-tail overlap had mean 0.084, and significant positive
program overlap had median 0.167 among the 45 pairs with any positive overlap.
The strong Rab7 sterol/lysosomal state therefore does not behave like a module
shared by all trafficking lesions.

## Corpus and literature evidence

The Distributed Agents corpus had no Vps37a-centered claims or findings, so there was
no pre-curated same-experiment analog set for the held-out gene. Relevant
neighbor claims instead came from represented pathway genes:

- `Chmp4b` corpus finding `Chmp4b:F002` reported that Chmp4b did not form a
  recurrent ESCRT/autophagy/cargo signature with `Atg5`, `Becn1`, `Sqstm1`,
  `Spast`, or APP/NMDAR/NTRK/Notch cargo genes; its whole-signature neighbors
  were near-zero.
- Rab7 claims `claim:726468d7afc216bc3be2` and
  `claim:02eb96768645a7558896` describe a selective Rab7 late
  endosomal/lysosomal and sterol compensation state. They also state that the
  state is weakly shared by `Vps41` and absent after adjacent `Ocrl`, `Abca7`,
  or `Gdi1` perturbation.
- Vps35 claim `claim:02de8fcbbda046b67a7b` separates the modest Vps35 151
  thalamic response from Retriever/Commander/WASH perturbations.
- Vps54 claims `claim:1d7844ef6515526be72d` and
  `claim:e03500d06831d2b59f6a` show that GARP/retrograde trafficking
  perturbations do not collapse into a generic state, and even same-complex
  `Vps53` failed to phenocopy `Vps54` at FDR scale.

External biology puts Vps37a in two relevant ESCRT-I roles. Mammalian ESCRT-I
contains TSG101, VPS28, one VPS37 isoform, and MVB12/UBAP1-class subunits; the
VPS37A-UBAP1 form is endosome-specific and required for ubiquitin-dependent
MVB cargo sorting (Stefani et al. 2011, DOI 10.1016/j.cub.2011.06.028,
PMID 21757351). VPS37A also directs VPS28 and ESCRT-III component CHMP2A to
the phagophore for autophagosome closure (Takahashi et al. 2019, DOI
10.1083/jcb.201902170, PMID 31519728). A Vps37a UEV-like domain mutant mouse
impairs bulk autophagic flux and can accumulate SQSTM1/ubiquitinated proteins
with neuronal dysfunction and antioxidant-gene up-regulation, showing that the
gene can matter in neurons under strong chronic perturbation (Hamamoto et al.
2024, DOI 10.1016/j.celrep.2024.115016, PMID 39607828). Concurrent depletion
of VPS37 paralogs in colorectal cancer cells destabilized ESCRT-I and produced
cell-cycle/inflammatory stress programs, but that setting involved cancer
cells and combined VPS37 loss rather than sparse partial postnatal neuronal
knockout (Kolmus et al. 2021, DOI 10.1242/jcs.250951, PMID 33419951).
Hurley 2015 summarizes the broader point that ESCRT proteins execute MVB
biogenesis, viral budding, cytokinetic abscission, membrane repair and
autophagy by related membrane-neck scission reactions (DOI
10.15252/embj.201592484, PMID 26311197).

## Target-specific reasoning

**Vps37a**

The most direct represented perturbation was `Chmp4b`, an ESCRT-III subunit
used after upstream ESCRT-I recruitment. It had `n_degs = 0` in
`151 TH Prkcd Grin2c Glut`; the curated Chmp4b finding also reported no
recurrent ESCRT/autophagy/cargo signature across obvious comparators. This is
not a perfect analog because VPS37A is an upstream ESCRT-I isoform and CHMP4B
has paralogs, but it is the closest measured test of the same membrane-scission
machinery.

The Vps37a-specific phagophore-closure literature would have made an autophagy
stress response plausible. In this focal group, however, `Atg5`, `Atg16l1`,
and `Becn1` had zero FDR<0.05 genes and `Sqstm1` had one. The same-experiment
corpus also emphasizes that represented autophagy and lysosome perturbations
were not transcriptomically interchangeable in this juvenile neuronal assay.
That made it unsafe to project the strong Vps37a mutant-mouse autophagy
phenotype directly onto the sparse P16 AAV CRISPR readout.

The broadest positive endolysosomal response in the focal training set was
`Rab7` with 501 DEGs, including V-ATPase, `Lamp2`, `Dpp7`, sterol-biosynthesis
genes, proteasome transcripts, and a down-shift in synaptic/receptor genes.
But the corpus explicitly treats this as a selective late-endosome/lysosome
compensation program: focal `Vps41` was zero, `Vps35` was only 17, `Vps54` was
31, and `Vps35l`, `Vps53`, `Washc4`, `Trappc6b`, `Trappc9`, `Trappc10`,
`Ocrl`, and `Gdi1` were 0-1. The runtime profile comparison likewise showed
little FDR-level sharing among the 29 broad endolysosomal candidates. Thus
Rab7 is a sensitivity control proving the assay can see lysosomal stress, not
a good point estimate for Vps37a.

I considered whether Vps37a should instead be assigned to the small retromer
or GARP tier represented by `Vps35` and `Vps54`. Those perturbations had
branch-specific 151 signatures rather than a common trafficking collapse:
Vps35 hit synaptic/receptor/calcium genes such as `Atp2a2` and `Grin2b`;
Vps54 produced an `Egr1`-down/`Jun`-up neuronal-state shift; and measured
same- or adjacent-complex genes failed to phenocopy them. ESCRT-I cargo
intralumenal-vesicle sorting and VPS37A phagophore closure are even farther
from those GARP/retromer readouts than `Vps53` or `Washc4`, so a 17-31 DEG
prediction would have over-weighted proximity to "trafficking" in general.

The predicted count is therefore `0`: the held-out perturbation has real
endomembrane/autophagy functions, but the acute, sparse, partial postnatal
snRNA-seq assay usually buffered directly assayed autophagy, lysosomal,
Retriever/WASH, TRAPP, and ESCRT-III nodes in the focal group. I do not expect
single-gene Vps37a loss to cross the FDR<0.05 threshold for any transcript in
these 151 thalamic glutamatergic nuclei.

## Limits

This is an extrapolation because the exact ESCRT-I core was mostly missing
from the training universe; `Tsg101`, `Vps28`, `Ubap1`, `Mvb12a/b`, and the
other `Vps37` paralogs would have been better analogs. `Chmp4b` tests
downstream ESCRT-III rather than the VPS37A-containing ESCRT-I isoform, and
both proteins have paralogs, so a direct Vps37a-specific autophagosome-closure
phenotype could still have been missed by the represented perturbations. The
parquet does not report indels or protein abundance, so a flat DEG surface
cannot distinguish biological buffering from weak editing, compensation, or a
protein-level trafficking defect with no nuclear mRNA response. Finally, the
published Vps37a mouse and cultured-cell phenotypes are stronger, chronic, or
non-neuronal perturbations than the AAV-CRISPR juvenile mosaic experiment, so
they set mechanistic plausibility rather than the FDR-scale count.
