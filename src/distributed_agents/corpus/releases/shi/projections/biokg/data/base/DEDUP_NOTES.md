# Post-hoc graph dedup notes (out_full)

Applied by `merge_canonical_entities.py` over the rebuilt `out_full` CSVs
(originals `nodes.csv`/`relationships.csv` left intact; output is
`nodes.merged.csv`/`relationships.merged.csv` + `merge_report.json`).

General semantic deduplication is deferred to LLM agents run over the graph.
The items below are only the failure modes spotted during manual assessment and
the targeted fixes applied to this graph.

## Metric

**Support** = number of distinct target genes (perturbations, of 2,046) whose
findings link to a node. Distribution over 4,806 conceptual (Pathway/Complex/
Module) nodes is long-tailed: 92% have support 1, median 1, p99 5, max 31.
Support >= 6 is ~top 1%. **Union support** = distinct targets across all
duplicate nodes of one concept (the real convergence once duplicates merge).

## Failure modes and resolutions

| # | Failure mode | Cause | Resolution | Nodes removed |
|---|---|---|---|---|
| 1 | Buffering phenotype mislabeled as `Pathway` | LLM assigned `kind=pathway` to "buffered transcriptional response" phrasing | Prune: drop `Pathway` nodes whose name matches `buffer` (concept is well-represented under `Phenotype`) | 39 |
| 2 | Seed cell types leak as non-seed nodes | Prefix-stripped cell-type labels (e.g. `CNU-HYa HY GABA`, `MB Glut`) bypassed the build-time exact-match filter | Prune: drop non-seed nodes whose token set (minus numeric id / trailing "cell/type/group") equals a seed cell type's | 58 |
| 3 | Synonym/format fragmentation within a label | Per-finding extraction emits many surface forms (case, punctuation, Greek letters, `pathway`/`signaling`/`response` decorators, plurals); the dominant "buffered transcriptional response" alone had ~300 forms | Generic within-label normalization key + a `buffer*` rule + small acronym map (OXPHOS/UPR/ISR/UPS) | 664 |
| 4 | Same concept split across acronym/expansion and across `Complex` vs `Pathway` labels | Formatting normalization cannot equate `mTOR`=`mechanistic target of rapamycin`, `BAF`=`mSWI/SNF`, `JAK/STAT`=`Janus kinase/...`, or a Complex node with its Pathway twin | Targeted, dry-run-verified cross-label collapse of the 8 spotted clusters below | 48 |

Total conceptual/other nodes removed: 809 (84,994 -> 84,185). 0 dangling edges.

## Spotted clusters merged (failure mode #4)

Patterns were dry-run and tightened to exclude distinct concepts
(non-canonical NF-kB and receptor-specific NF-kB pathways e.g. TLR/TNF/NOD/RANK;
mTORC2 and PI3K-AKT-mTOR; PBAF/ncBAF and named remodeling axes; the proteasome
bounce-back program; spliceosome subcomplexes). Union support is the
consolidated distinct-target count after merge.

| Canonical | Label | Variants merged | Union support |
|---|---|---|---|
| mTORC1 | Complex | 5 | 25 |
| JAK/STAT signaling pathway | Pathway | 3 | 24 |
| proteasome | Complex | 9 | 21 |
| NF-kB | Pathway | 8 | 19 |
| mSWI/SNF (BAF) complex | Complex | 16 | 15 |
| spliceosome | Complex | 2 | 13 |
| nucleocytoplasmic transport | Pathway | 4 | 6 |
| ER proteostasis | Pathway | 1 | 4 |

## Known remaining cases (left for LLM-agent semantic dedup)

- **Label-foreign copies**: the same concept can still exist under a different
  label (e.g. `proteasome` as both `Complex` and `Other`; `NF-kB` as
  `Pathway`/`Gene`/`Other`). The targeted dedup only touched Pathway/Complex/
  Module conceptual nodes.
- **Long-tail synonyms** outside the 8 spotted clusters are unmerged by design.
- **Nuclear transport is genuinely sparse** (union 6, << the other four high-burden
  categories) — likely under-extracted, worth a targeted check rather than a merge.
- **Hedgehog (31) ranks #1** among all conceptual nodes; suspicious for a neuronal
  screen and worth auditing for over-extraction.

## Investigation: why Hedgehog ranks #1 (metric artifact, not a node-quality bug)

Hedgehog[Pathway] has 51 incoming entity edges from 31 distinct targets. Those
targets are overwhelmingly Hedgehog/primary-cilium genes the screen deliberately
perturbed (Ptch1/2, Smo, Gli1/2/3, Cdon, Gpr161 + IFT/ciliopathy set: Ift43/81/88,
Dync2h1/2i1, Ttc21b/8, Cplane1, Cspp1, Sdccag8, Lztfl1, Dzip1, Sclt1, Tbc1d32, ...).
"Hedgehog" is attached as the *pathway annotation of the perturbed target gene*,
not as a downstream convergent response.

Crucially the effect_status of those edges is dominated by NULL/negative:
absent_or_not_detected=18, uncertain=22, implicated=8, affected=2, compared=1.
Evidence spans are explicitly negative ("not detectable", "no FDR-resolved
response", "pathway silent", "canonical GLI markers did not change", "uncoupled
from Smo"). Finding types are the null family (pathway_uncoupling,
disease_mechanism_refinement, cross_perturbation_contrast).

Root cause: the support metric counted every edge regardless of effect_status,
conflating "pathway tested and did NOT respond" with "pathway converged."

Resolution (query-level, not a graph edit): rank by POSITIVE support
(effect_status in {affected, implicated, buffered}), excluding
absent_or_not_detected / fdr_insignificant / uncertain. Under positive support
the top conceptual nodes become:

  1 proteasome(19)  2 spliceosome(12)  3 mTORC1(12)  4 OXPHOS(11)
  5 mSWI/SNF-BAF(10)  6 ISR(10)  7 Hedgehog(9)  8 RNA-processing(9) ...

i.e. 4/5 expected high-burden categories rise into the top 8 and Hedgehog drops
from #1 to #7. Most null-inflated nodes: Hedgehog 45% null, MAPK 57%, UPR 46%.

## Investigation: long-tail synonym patterns beyond the 8 clusters

Of 4,760 conceptual (Pathway/Complex/Module) nodes, **92% (4,380) are support<=1
singletons**. The long tail splits into two very different populations:

1. **Finding-specific descriptor singletons (the dominant mass).** ~1,364 nodes
   end in a response-type wrapper (… perturbations/signature/module/program/axis/
   output/response); **96% of those are support<=1** and non-reusable, e.g.
   `'21-gene Slc17a6/V-ATPase vesicle signature'`, `'29-gene mixed synaptic
   program'`, `'160-gene differential-expression program'`. These are per-finding
   gene-set summaries, NOT synonyms of each other. The right move is to DROP or
   demote them (or attach as instances under a parent concept), not merge.

2. **Genuinely mergeable concept variants (small).** Only ~51 wrapper nodes have
   support>=2 (true recurring concepts that didn't canonicalize, e.g.
   `'RNA processing module'`, `'sterol module'`, `'transcriptomic response'`).
   An aggressive core-key (strip qualifiers/wrappers + Greek + plurals) finds
   ~320 residual multi-name clusters / ~474 collapsible nodes total.

General fragmentation patterns (for the LLM-agent dedup):

SAFE to collapse toward a base concept:
- A. Response-type wrapper suffix: `autophagy` / `Autophagy Perturbations` /
  `autophagy module` / `autophagy function`.
- B. Qualifier prefix (~221): `canonical Wnt signaling pathway` -> `Wnt`;
  `developmental axon guidance pathway` -> `axon guidance`.
- C. Greek-letter / hyphenation / plural variants (~50 Greek): `Wnt/β-catenin`
  vs `Wnt/beta-catenin`; `Perturbations` vs `perturbation`.
- Acronym <-> expansion (e.g. JAK/STAT, respiratory chain / Complex I).

HAZARD — must NOT naively collapse (distinct biology; a naive core-key wrongly
merges these):
- D. Compartment qualifiers (~548 hits): `Mitochondrial Unfolded Protein
  Response` != `unfolded protein response`; `mitochondrial integrated stress
  response` != ISR; `mitochondrial proteostasis` != proteostasis.
- E. Non-canonical branches (~9): `non-canonical NF-kB` != `NF-kB`.
- F. Numbered family members (~98): `AP-1`/`AP-2`/`AP-3`/`AP-4` are distinct
  adaptor complexes; `Complex I`/`II`/`III` distinct.
- Gene-prefixed specific instances are hierarchy, not synonymy
  (`FZD4/Norrin/Wnt-beta-catenin` is a specific instance of Wnt/β-catenin).

## Effect-status support modes: precision/recall tradeoff + tooling

`query_biokg.py` exposes `--status-mode {all, positive, non-negative}` for every
entity-support query. ~50% of entity edges are non-positive by design
(global mix: implicated 17294, uncertain 13200, affected 12373,
absent_or_not_detected 10242, nominal 1987, buffered 1177, compared 1161,
fdr_insignificant 1081, mixed 595, caveated 58).

Modes:
- **all** = every edge. Conflates "tested and did NOT respond / inferred" with
  "converged". Lowest precision (this is why Hedgehog ranked #1).
- **positive** = {affected, implicated, buffered} (measured effects). Highest
  precision.
- **non-negative** = all except {absent_or_not_detected, fdr_insignificant};
  keeps uncertain/nominal/mixed/compared. (default)

Recommended per query (auto-applied unless overridden):
- `dominant` (ranking) -> **positive**
- `convergence` (discovery) -> **non-negative**
- `support` (audit a node) -> **all** (shows full status breakdown)
- `celltypes` -> status filter does not apply (OBSERVED_IN edges)

### Measured recall effect (queries re-run on out_full merged graph)

Dominant-pathways recall of the 5 known high-burden categories improves under
positive support:

| top-K | TOTAL (all) | POSITIVE |
|-------|-------------|----------|
| 5  | 1/5 | 3/5 |
| 10 | 3/5 | 4/5 |
| 20 | 4/5 | 5/5 |

Null-inflated artifacts drop (Hedgehog 31->9 support, MAPK 57% null, UPR 46%
null); the positive-support top tier is proteasome, spliceosome, mTORC1, OXPHOS,
ISR, BAF, RNA-processing — matching the expected biology.

### The tradeoff is smaller than it first appears (Nfe2l1 lesson)

Initial read: proteasome convergence (entities in >=3 of 4 of Pomp/Psmb4/Psmc1/
Psmc5) drops 18 (all) -> 17 (positive), losing Nfe2l1 — the proteasome
bounce-back master TF — which looked like a recall loss. On inspection Nfe2l1's
three edges are `fdr_insignificant` (Pomp) + `uncertain`/"did not phenocopy"
(Psmb4) + `uncertain`/"inferred upstream activity" (Psmc5). It was never a
*measured* convergent hit; the graph correctly encoded it as inferred/null.
So positive/non-negative dropping it is correct, not lost recall.

Conclusion: `all` mode's extra "convergence" is largely non-measured inference.
Use **positive** for any claim, **non-negative** to surface weak/inferred shared
mechanisms for a human to vet (knowing 'uncertain' can mean "did not phenocopy"),
and **all** only to audit what was tested-but-null.

## Tooling

- `query_biokg.py` — configurable graph queries:
  `dominant`, `convergence --targets ...`, `support --name ...`,
  `celltypes [--depletion]`, with `--status-mode` and `--csv-dir`
  (defaults to `out_full/nodes.merged.csv`, falls back to `nodes.csv`).
