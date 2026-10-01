# Replot assessment: flag distribution and single-agent scaling

Regenerated from the raw per-pair JSONL by `replot_scaling.py` (runnable in
place; prints every number below). Non-destructive — the original figures in
`../` are untouched.

## The reframe that changed the figures

Every original panel reports a **share**: supported fraction falls 84.9% → 3.5%.
That fraction has a growing denominator, and the denominator is doing the work.

| targets/agent | pair rows per run | grounded rows per run | grounded targets |
|---|---|---|---|
| 10 | 141 | 89 | 7–9 |
| 30 | 230 | 94 | 4–16 |
| 100 | 525 | 57 | 6–10 |
| 205 | 908 | 84 | 12–15 |
| 500 | 1,599 | 53 | 6–10 |
| 893 | 2,324 | 82 | 9–13 |

From 10 → 893 targets the table grows **16.5×** while grounded rows grow
**0.92×** — they do not grow at all. Mean 76.4 grounded rows per run
(range 26–149) across the whole upper range, and 4–16 grounded targets no matter
what the workload is.

**The claim to make is not "grounding recall degrades with scale." It is that a
single agent does a roughly constant amount of literature work — ~50–100 pair
calls against ~10 targets — and assigning it more work only spreads that same
work thinner.** This is a stronger and more mechanistic claim than a declining
percentage, and it is invisible in every current panel.

### Nothing is limiting the run — it self-terminates

This matters for how the result is worded. Per `agent_budget_summary.json` the
batch configures **no** limits at all:

| knob | value |
|---|---|
| `max_internal_agent_steps` | `null` |
| `total_token_cap` | `null` |
| `runner_wall_clock_timeout` | `null` |
| `top_level_user_turns_per_run` | 1 |

Cumulative token use per run (1.6M–5.9M) already exceeds the 272k context window,
so continuation and compaction are demonstrably available too. The agent is
therefore **not hitting a ceiling — it stops on its own**, at a near-constant
effort level (median 810 s, median 33k output tokens, min 484 s / max 1,222 s)
whether it was handed 1 target or 893. It does not exhaust the turns, tokens or
time available to it, and it does not exhaust the work it was given.

So the phrasing throughout is **self-limiting / self-terminating**, never
"capped" or "budgeted": there is no budget to spend. An imposed cap would be a
configuration problem with a configuration fix; self-termination at a fixed
effort level regardless of workload is a property of the agent, which is the
finding. (The earlier draft of these figures said "capped" — wrong, and it
understated the result.)

## Four verified failure modes

1. **Constant absolute output** (above). Grounded output is flat; the share falls
   only because the table grows. Not a cap — the agent self-terminates.
2. **Within-target differentiation collapses.** On the anchor-10 cohort — the
   *same* 10 targets with the *same* 422 eligible rows at every scale — the number
   of cell types per target that receive a call differing from that target's
   majority falls **1.63 → 0.30 out of 14.1**, and at 893 targets **2 of 3 runs
   give every cell type of every anchor target the same call**. Grounded rows in
   that fixed cohort fall 266 → 30. Controlling for rows-per-target (targets with
   ≥10 rows only) reproduces this, so it is not an artifact of larger scales
   adding low-burden targets. Cell-type specificity is the entire point of the
   endpoint, so this is a failure of purpose, not just of recall.

   *On the choice of measure* — the candidates, from
   `replot_differentiation_measures.csv` (printed on every run):

   | measure | n1 → n893 | controlled n10 → n893 |
   |---|---|---|
   | distinct flags / target | 2.67 → 1.07 | 1.77 → 1.07 |
   | frac all-one-flag | 0.00 → 0.93 | 0.37 → 0.93 |
   | normalised entropy | 0.489 → 0.030 | 0.300 → 0.030 |
   | minority share (%) | 19.0 → 1.7 | 13.6 → 1.7 |
   | **cell types called differently** | **3.33 → 0.30** | **1.63 → 0.30** |

   A count of **distinct flags per target** is the obvious statistic and over the
   full span it is a real signal — 2.67 → 1.07 is 1.6 flags, about 80% of its
   usable range, and at 1 target a target carries 2.67 of the 3 flags ever used
   (near-maximal mixing). Two things argue against leading with it. First, its
   **ceiling is 3**: at 1 target it is already at 2.67/3, so it has no headroom to
   represent more differentiation, which is why the controlled range compresses to
   0.7. Second, **n1 and n3 are not controlled** — the anchor prefix is only fully
   assigned from 10 targets on, so n1 is 3 target-instances at 19.0 rows each
   against 30 at 14.07 thereafter, and more eligible cell types mechanically
   permit more distinct flags (the n3 value of 2.22 falling *below* n1's 2.67
   shows the noise).

   Counting **cell types called differently** is unbounded above, sits against a
   constant denominator, and holds its range under the controlled comparison, so
   it is what `fig_r1c` plots. Normalised entropy behaves well (0.489 → 0.030) but
   reads as abstract. Distinct literature *claims* per target has the best range of
   all (see `fig_r7a`) but is non-monotone on this 30-target subset
   (5.4 → 2.8 → 13.1), so it is used only at full-corpus scale.
3. **Grounding arrives in bursts.** Along emission order, grounded rows fall into
   11–28 contiguous blocks where a random spread of the same count predicts
   61–109 (z = −16 to −39 at every run with ≥100 targets). The agent does real
   literature work for a few contiguous stretches and abstains across long dead
   ones. A per-scale summary averages this away entirely.
4. **`Disagree` never fires: 0 / 17,376 rows, at every scale and seed.** The
   four-level flag scale only ever uses three, and the missing level is the one
   that would represent a literature *contradiction*. The original figures put
   `Disagree` in a legend without noting it is always empty — worth stating
   explicitly, since "never contradicts the literature" is a substantive
   property of the run, not a rendering detail.

Also confirmed: 73.5% of the 422 fixed anchor pairs change label between scales.

I checked for a **positional decay** effect (does grounding thin out as the agent
works down the list?) and it does **not** hold: the rank correlation between
assignment position and grounding flips sign across seeds and scales
(ρ = −0.21 to +0.13). The honest structure is burstiness (3), not decay — so I
did not build a figure claiming decay.

## Does the surviving `Agree` / `Inferred` content go tautological?

Yes — and the mechanism is specific: **the literature judgement stops being made
per row and becomes one target-level statement copied across every cell type.**
Measured on the literature clause of each row summary (the text with the
differential-expression recital stripped out); see `fig_r7_literature_quality`,
`replot_literature_quality.csv`, `replot_literature_rows.csv`.

| targets | cell types / target | distinct claims / target | rows sharing a claim | distinct claims / run | refs / row |
|---|---|---|---|---|---|
| 1 | 16.3 | **9.7** | 33% | 9.7 | 4.12 |
| 10 | 11.6 | 3.8 | 68% | 29.3 | 1.74 |
| 30 | 10.2 | **1.04** | 97% | 11.7 | 1.34 |
| 100 | 8.0 | **1.00** | 98% | 8.0 | 1.42 |
| 500 | 7.5 | 1.05 | 98% | 7.7 | 1.14 |
| 893 | 8.3 | **1.03** | 98% | 9.0 | 1.69 |

1. **At 1 target a grounded row is a per-cell-type judgement** — 9.7 distinct
   literature claims across 16.3 cell types. **At ≥30 targets it is one claim per
   target**, and 97–98% of grounded rows carry a claim reused verbatim for another
   cell type of the same target. The cell type has become a label in a template
   rather than a variable in the claim — on an endpoint whose entire question is
   cell-type specificity.
2. **A run makes only ~8–12 distinct literature judgements, at any scale**
   (9.7 at 1 target, 9.0 at 893), so the ~76 grounded rows are restatements of a
   handful of claims: 4.3 rows per claim at 1 target, 9.4 at 893. This is a
   tighter invariant than the grounded-row count itself.
3. **Backing thins**: references per grounded row falls 4.12 → ~1.2–1.7, one
   reference key serves the whole target in 97–100% of multi-cell-type targets,
   and the share of grounded rows resting on a *review* rather than a primary
   study rises from 0% to 19–34%.
4. **`Inferred` is often the agent saying the literature does not answer** —
   hedges ("do not resolve", "indirect inference rather than a decisive
   directional match") appear in 40–48% of `Inferred` rows at 100–205 targets and
   in **0% of `Agree` rows at ≥10 targets**. `Agree` is 51% of grounded rows at 1
   target but 13–40% above that, so the grounded set tilts toward the flag that
   declares indecision. Counting `Inferred` as "grounded" is doing a lot of work
   in the headline recall numbers.
5. **The declared context field is self-certified, not earned.** `lit_context`
   still claims a `cell_type` match on 93–100% of grounded rows at every scale,
   while (1) shows the underlying claim is identical across cell types. So
   `lit_context` cannot be used as a quality signal. Its `stage` dimension is
   also unreliable — the 893-target Atp2a2 claim cites *adult* Serca2 disruption
   for P16 data and simply omits `stage` from the declared context rather than
   flagging the mismatch.

### The controlled trace — same comparison, six different verdicts

`Psmb4` × `005 L4-5 IT CTX Glut`, seed 17, identical data at all eight scales:

| targets | flag | refs | the literature claim |
|---|---|---|---|
| 1 | Agree | 3 | PSMB4 loss impairs proteasome function → Nrf1 recovery + CHOP/DDIT3 ISR, predicting the observed module |
| 3 | Agree | 3 | PSMB4 loss impairs assembly; neuronal PSMB4 proteasomes regulate the synaptic proteome |
| 10 | Inferred | 1 | documented, "but they do not resolve whether Psmb4 loss should drive this" |
| 30 | Agree | 2 | proteasome impairment stabilises NFE2L1, bounce-back transcription |
| 100 | **No Literature** | 0 | "No documented target-specific bridge was found" |
| 205 | Inferred | 2 | documented, "but the dominant neuronal transcript loss is broader" |
| 500 | Inferred | 1 | retreats to *pharmacologic* proteasome blockade "rather than PSMB4-specific neuronal loss" |
| 893 | **No Literature** | 0 | "PubMed/PMC searches … did not identify a target-specific bridge" |

The same agent, on the same comparison, reports a three-reference documented
mechanism, an indirect inference, and no literature at all. The verdict is a
property of how much attention the run happened to spend, not of the comparison.

### Two things that are *not* degradation — stated so they are not over-read

- **The boilerplate is target-scoped, not global.** Claim text is almost never
  reused across different targets (at 893 targets only 4 clauses are shared by
  more than one target, max 4 targets). The collapse is specifically along the
  cell-type axis; the agent is not emitting one generic sentence for everything.
- **The breadth of responses one claim covers is a standing property, not a
  scale effect.** Where a single claim spans several cell types, their
  downstream-DEG counts differ by a median 40–420× at *every* scale, including 1
  and 3 targets. So "one claim covers wildly different responses" is true
  throughout and cannot be cited as scale-induced. What scale changes is **how
  much of the table** such claims cover — 33% of grounded rows at 1 target
  versus 98% at 893. I dropped a panel that plotted the fold-range as a trend
  once it turned out to be non-monotone.

## Do the `Agree` rows still hold up at 893 targets?

Tested directly on the `Agree` subset — `fig_r8_agree_quality`,
`replot_agree_quality.csv`, verbatim exhibits in **`AGREE_EXAMPLES.md`**.

**Partly true, and the part that is true is about the argument, not the citation.**

### What thins

| | n1 | n100–500 | n893 |
|---|---|---|---|
| references per `Agree` row | 3.18 | 1.26–1.29 | 1.76 |
| backed by ≥2 references (a chain) | **96%** | **18–29%** | 60% |
| states what it *cannot* explain | 12% | **0%** | **0%** |
| review-backed rather than primary | 0% | 6–16% | 35% |

At one target an `Agree` row is a **multi-step mechanistic chain** where each
reference supplies a distinct link, plus an explicit scope limit. The reference
case (`Psmb4`, 3 primary refs): PSMB4 loss impairs the proteasome → Nrf1-dependent
recovery predicts ↑Psmc6/Psmd4 → CHOP/DDIT3 ISR predicts ↑Ddit3/Hsph1, and then
*"the accompanying synaptic-gene decrease was not itself the basis of the flag."*
That self-scoping clause — naming what the literature does **not** cover — appears
in 12% of `Agree` rows at one target and in **exactly 0% at every scale from 10
onward**. It never comes back.

### What does not degrade — checked, and it refutes the stronger version

- **References stay on-target**: the target gene is named in the cited work in
  **100%** of `Agree` rows at 893 targets (96% at n1). No drift to unrelated papers.
- **Every reference carries a PMID**, at every scale. Nothing is fabricated-looking.
- **No citation recycling**: no reference serves more than 2 distinct targets.
- **Evidence gene sets stay coherent** (e.g. the 893-target Atp2a2 row lists
  Ddit3/Chac1/Xbp1/Herpud1/Hspa5 — a real ER-stress module).
- **Cross-system sourcing is not a scale effect.** Citing fibroblast, cardiomyocyte
  or cancer work for P16 brain data runs at 10–74% across scales and is **96% at
  one target** — the reference Psmb4 chain itself rests partly on fibroblast siRNA
  work. It is standing practice for this endpoint, so it cannot be reported as
  degradation. (Reported as a number in `fig_r8c`, deliberately not plotted as a
  trend.)

### 893 targets is heterogeneous, not uniformly bad

This is the main correction to the hypothesis. At 893 targets the `Agree` rows
span the full quality range:

- **`Tsc2` is as strong as anything at n1** — 3 references (1 review + 2 primary),
  a two-branch chain (mTORC1 → neuronal sterol transcription; TSC1/2 → TFEB →
  lysosomal biogenesis), matching sterol (Insig1, Msmo1, Hmgcs1, Ldlr) *and*
  lysosomal (Atp6v0b, Lamp2) genes, with `stage` declared.
- **`Atp2a2` transfers across systems** — one reference, *cardiomyocyte-specific*
  Serca2 disruption in *adult* mice, applied to P16 thalamic glutamatergic
  neurons. It drops `stage` from the declared context rather than flagging the
  mismatch, and still declares a `cell_type` match.
- **`Apc` is a textbook inference on a broad review** — one WNT review supporting
  "APC restrains β-catenin, so Axin2 goes up", over a 7-DEG response. Correct, but
  it is the kind of claim that needs no literature search.

So the honest framing is not "quality collapses" but: **the ceiling stays reachable
while the floor drops out, and the median argument loses its steps.** With only
~8–12 distinct claims per run (see `fig_r7b`), which end of that range a given
target lands on is close to arbitrary.

## Alternative encodings for the flag distribution

`fig_r2_flag_distribution_options` puts four options side by side with what each
buys and costs. Summary:

| Option | Shows | Hides | Verdict |
|---|---|---|---|
| **1. 100% stacked** (as published) | the shift to abstention | that grounded count never grew | keep as a secondary panel |
| **2. Absolute counts, one log axis** | the self-limiting directly — flat grounded series under a rising total | per-row composition | **recommended primary** |
| **3. Position-within-run strip** | burstiness, dead stretches | per-scale magnitude | best "scaling issue" panel |
| **4. Row-level grid of one run** | sparsity + clumping viscerally | no axis; single run only | strong companion to 2 |

Option 2 is the recommendation: both series are counts of pair rows, so they
share **one unit and one axis** — the flat-under-rising shape *is* the finding,
with no dual-axis trickery. Options 1 and 2 are complements, not substitutes;
ship 2 first and 1 beside it.

For the ordered agree→abstain scale I kept a stacked composition rather than a
diverging bar centered on neutral: `No Literature` is an *abstention*, not a
midpoint between agree and disagree, so centering on it would imply a symmetry
the data does not have.

## Figures produced

| File | Replaces / adds | Panels |
|---|---|---|
| `fig_r1_grounding_budget` | `monolithic_scaling_overview` | a constant grounded output · b composition · c differentiation collapse |
| `fig_r2_flag_distribution_options` | new (the assessment) | four encodings of the same flags |
| `fig_r3_within_run_structure` | new | a burstiness vs null · b fixed cohort loses grounding |
| `fig_r4_label_stability` | `srsf1_tnpo3_label_stability` | a Srsf1 · b Tnpo3, equal-size cells |
| `fig_r5_resource_envelope` | `cost_runtime_overview` | a cost · b runtime · c per-pair output |
| `fig_r6_self_termination` | new (`agent_budget_overview`) | a workload vs effort, indexed · b tokens vs context window · c internal steps |
| `fig_r7_literature_quality` | new | a claims per target · b claims per run · c share of rows sharing a claim |
| `fig_r8_agree_quality` | new | a references per Agree row · b argument depth · c negative controls |
| `fig_b_single_vs_multi` | Figure 2 panel B (replaces `fig_r1`) | a grounded pair calls, both arms · b single-agent flags · c per-target-agent flags |

Sidecar data: `replot_run_level.csv`, `replot_anchor_differentiation.csv`,
`replot_burstiness.csv`, `replot_run_consumption.csv`,
`replot_single_vs_multi.csv`.

### fig_b_single_vs_multi adds the second arm

`replot_multiagent.py` is the panel-B replacement. Every other figure here is
single-arm — it establishes that one agent's grounded output does not grow — so
it can show the failure but not the fix. This one puts the production per-target
fan-out beside it, read from the 260801 meaningful-biology two-corpus union
(`manuscript/fig2/_debug/260801/meaningful_biology_union`).

Matching, which is the whole point of the panel: at scale *n*, seed *s*, the
single agent was handed the first *n* targets of that seed's `target_order.json`,
so the multi-agent arm is restricted to **those same n targets**. Every rung is a
paired comparison, and the multi-agent series inherits the seeds' target-subset
spread — which vanishes at 893, where all three seeds are the same set.

Both arms score target × cell-type pairs with ≥ 1 downstream DEG at FDR < 0.1,
from the experiment's own `reference/downstream_fdr_0_1.parquet`. That grid
reproduces the single agent's `expected_pairs` **exactly** for all 24 runs
(18 … 2,324), and the single agent emitted a call for 100% of them at every
scale. Union findings are placed on the same grid via
`supported_cell_types_json`.

#### Aggregation: fractional, not max-priority

61% of claimed pairs carry more than one finding, so the multi-finding rule
decides the answer. **Each pair contributes one unit, split proportionally across
the flags of the findings on it.** The union's own `PAIR_PRIORITY`
(Disagree > Agree > Inferred > No Literature) is deliberately *not* used: it is a
surface-the-strongest rule built so a heatmap cell shows Disagree when Disagree
exists, and reading it as a composition promotes Agree and Disagree — both of
which sit above Inferred and No Literature in that ordering — against everything
else. Decomposed on the 893 targets:

| step | Agree | Disagree | Inferred | No Lit |
|---|---|---|---|---|
| all 1,519 findings (corpus headline) | 27.6% | 6.6% | 41.9% | 23.8% |
| restricted to the 893 targets | 28.4% | 6.4% | 40.6% | 24.5% |
| only findings placing on a DEG+ pair | 30.8% | 4.4% | 38.4% | 26.4% |
| **fractional over pairs ← what panel c plots** | **32.6%** | **4.0%** | **36.0%** | **27.3%** |
| max-priority over pairs (rejected) | 50.4% | 9.2% | 25.9% | 14.6% |

Fractional lands within a few points of the corpus's own distribution; the
residual is two legitimate effects, not aggregation choice — Inferred findings go
unplaced more often (20% vs Agree's 8%), and Agree findings span more DEG-positive
cell types (2.77 vs 2.08). Max-priority would have put panel c at 50% Agree
against Figure 2 panel A's 27.6%, for the same corpus.

Fractional is applied to **both** arms and both panels, so one pair is one unit
everywhere. It is the identity on the single arm, which emits exactly one flag
per pair.

| targets/agent | workload pairs | single grounded | multi grounded | single grounded share | multi grounded share |
|---|---|---|---|---|---|
| 1 | 19 | 16 | 9 | 84.9% | 56.6% |
| 10 | 141 | 89 | 69 | 62.9% | 69.1% |
| 30 | 230 | 94 | 111 | 39.8% | 65.3% |
| 100 | 525 | 57 | 265 | 10.8% | 70.5% |
| 500 | 1,599 | 53 | 713 | 3.3% | 72.6% |
| 893 | 2,324 | 82 | 908 | 3.5% | 72.7% |

1 → 893 targets: the workload grows 122×, single-agent grounded calls 5.0×,
per-target grounded calls 100×. The per-target arm's grounded share of its own
calls **holds 65–73% from 3 targets up**; the single agent's collapses 85% → 4%,
crossing below the per-target arm at 30 targets.

#### What the low rungs do and do not establish

At 1–10 targets the two arms are indistinguishable and the ordering flips by
seed, which is expected — at n=1 each seed is one target and 14–23 pairs. Per
seed at n=1: Psmb4 78% single / 54% multi, Psmc1 81% / 100%, Srsf1 96% / 16%.

The Srsf1 run drives that spread and is worth reading rather than dropping,
because it is **contract-correct, not degenerate**. It retrieved six real PubMed
records with full citations (R001 = Li & Manley 2005, *Cell*, PMID 16096057,
ASF/SF2 loss → R-loops and genomic instability) and labeled all 23 pairs
`Inferred`. All 23 summaries are distinct — each recites its own cell type's DEGs
— but there are only **3 distinct literature clauses**: one target-level
judgement that SRSF1 literature reaches RNP assembly, mRNA export and R-loop
genome stability and none of it predicts signed mRNA abundance in P16 mouse
cortical neurons. Every grounded row declares
`lit_context = [species, cell_type, stage, modality, indirect]`, the maximum
mismatch on all four dimensions. The contract says to use `Inferred` "only when
transfer of the relationship or its direction is genuinely undecidable", which is
exactly this case. The agent's own reference description says the same: "…but not
the exact neuronal mRNA directions observed here."

It is also not an outlier — grounded rows declare 3.3–4.2 mismatch dimensions at
every scale (`context_dims` in `replot_literature_quality.csv`), so Srsf1 is the
typical case, just uniform across its pairs.

What it exposes is the coarseness of `grounded`, which counts "found matched
literature" and "found gene-level literature and declared it mismatched on all
four axes" as the same thing. That is a property of the metric, inherited from
`fig_r1`, and it applies to both arms. The run is kept.

So n=1 is not a clean control. It is also not the same *system* on both sides —
the single arm is this experiment (rosalind-5.5, q3 pair-enumeration contract),
the multi arm is the union (gpt-5.6-sol stage-2 review over full reference
ledgers, over the 260713 production corpus plus the older corpus). Same
architecture, different pipeline. What the low rungs establish is a bound: the
two pipelines are within seed noise of each other when each agent holds one
target, so the gap that opens from 30 targets up is not a pipeline gap.

Two asymmetries stated rather than corrected, per the figure's framing decision.
The panels normalise each arm to its own calls, because the single agent's
contract makes it call every pair while the union is a discovery corpus and
claims 1,249 of the 2,324 pairs at n=893 — so b and c compare *composition*, not
coverage. And the union's flags come from its own stage-2 literature-review pass
over full reference ledgers, not from the q3 pair contract; this is a
system-versus-system comparison, which is what Figure 2 is about.

One qualitative difference, not just a magnitude one: `Disagree` is 4% of
per-target calls at 893 and **0 rows in every single-agent run at any scale**.
Because `Disagree` is populated here, the figure uses `FLAG_COLORS_CVD` per the
`flag_style` guidance (see "One accessibility defect to know about" below).

### fig_r6 carries the self-termination claim visually

The unset limits were previously only *asserted* in a suptitle, which is not
evidence. `fig_r6` plots the run's own instrumentation instead, pulled from each
run's `events.jsonl` (`item.completed` = internal steps; `turn.completed.usage` =
tokens):

- **a** indexes every measure to its own 1-target value, so five different units
  share one unitless axis (the sanctioned alternative to a dual axis). The work
  assigned rises to **122×** while the band spanning internal steps, tool calls,
  output tokens, cumulative input tokens and runtime stays at **1.0–1.9×**,
  median **1.4×**.
- **b** draws the 272k context window and the 258.4k auto-compact threshold as
  reference rules. Cumulative input sits at **5.9–21.7 full windows** — so
  continuation and compaction demonstrably work and are not the constraint —
  while output tops out at **0.24× a single window**. The gap is the headroom the
  run left unused.
- **c** shows **55–132 internal steps and 18–85 tool calls** per run, flat across
  the whole workload range, with no step limit configured. At 893 targets the
  agent makes ~45 tool calls to cover 2,324 comparisons.

Measured consumption, mean per scale:

| targets | steps | tool calls | input tokens | output tokens |
|---|---|---|---|---|
| 1 | 64 | 29 | 1.81M | 29,866 |
| 30 | 102 | 67 | 3.10M | 33,551 |
| 100 | 89 | 44 | 3.39M | 31,367 |
| 893 | 90 | 45 | 2.47M | 30,769 |

Output tokens at 893 targets are within 3% of the 1-target run.

## Standardizing the flag scheme across the repo

Yes, and it is now done: **`src/figures/flag_style.py`** is the single source of
truth, sitting beside the `style.mplstyle` these figures already share. It
exports `FLAG_ORDER`, `FLAG_LABELS`, `FLAG_COLORS`, a `normalize_flag()` that
accepts every spelling variant in the repo, and `legend_handles()` /
`flag_cmap()` helpers. These figures consume it; nothing here defines a flag
color locally any more.

The adopted values are the gold-set / `strict_v4_regrade_15` scheme:

| level | hex | role |
|---|---|---|
| `agree` | `#6fc46f` | green — the only strongly grounded, concordant level |
| `disagree` | `#ec835a` | warm — grounded, discordant |
| `inferred` | `#898781` | mid gray — weak |
| `no_literature` | `#c3c2b7` | light gray — abstention |

It is an **emphasis** scheme, not a flat categorical one: only the levels that
carry a literature judgement get a hue, so "how much of this chart is actually
grounded" reads at a glance. Worth knowing when reusing it — in `fig_r4` the
transitions being shown are `inferred` ↔ `no_literature`, i.e. between the two
deliberately recessive grays, so that panel reads more quietly than it did in a
2-hue scheme. It is still legible (the two grays are far apart in lightness), but
the scheme is optimised for a different question than that panel asks.

### What was found across the repo

Five distinct schemes were in use:

| definition site | scheme | note |
|---|---|---|
| `…/strict_v4_regrade_15.py` | `#6fc46f` / `#ec835a` / `#898781` / `#c3c2b7` | **adopted as canonical** |
| `…/report_citation_regrade.py` | `#70bf73` / `#ed8255` / `#92918c` / `#c8c7be` | drifted near-duplicate |
| `…/plot_arm_blind_regrade.py` | same drifted set + `unflagged #86a7bd` | drifted, plus a 5th level |
| `…/analysis/analyze_scaling.py` | Okabe-Ito, title-case keys | wholly different; superseded here |
| `debug/260612_q3/make_figure.py` | six levels (moderately-agree/disagree …) | different **taxonomy**, not just colors |

So migration is three different jobs, not one:

1. The two drifted duplicates are a pure import swap — the hexes differ by 1–3
   points and are visually indistinguishable, so **no figure changes appearance.**
   Safe to do unprompted; I have not, since they are manuscript scripts.
2. `plot_arm_blind_regrade.py` needs the 5th level, so the module carries
   `UNFLAGGED_KEY` / `UNFLAGGED_COLOR` outside `FLAG_ORDER` (keeping the default
   four-level scheme untouched). Note `unflagged #86a7bd` vs `inferred #898781`
   is normal-vision ΔE 10.5, under the 15 floor — that pair needs direct labels.
3. `make_figure.py` is the old six-level vocabulary. Collapsing it is **lossy**
   (moderate → strong), so the module exports `collapse_legacy_six()` as an
   explicit opt-in and `normalize_flag()` deliberately *raises* on those labels
   rather than silently mis-coloring. Whether to collapse that figure is a
   content decision, not a styling one — your call.

I did not touch the four other call sites: migrating `analyze_scaling.py` would
restyle the existing published figures in `../`, and the manuscript scripts are
yours to re-run. The module is in place whenever you want them switched.

### One accessibility defect to know about

Measured with `dataviz/scripts/validate_palette.js` (light, surface `#fcfcfb`,
`--pairs all`): `agree #6fc46f` vs `disagree #ec835a` is **ΔE 3.1 under
deuteranopia**, against a floor of 6. Green vs orange sits on the red-green
confusion axis, so the two most consequential levels are near-indistinguishable
for deutan readers — the worst possible pair to have this on.

`FLAG_COLORS_CVD` fixes it with a **single hex change**, `disagree → #d03b3b`,
which lifts that pair to deutan ΔE 15.9 / tritan 36.0 and makes the whole
four-level set pass CVD separation. It keeps the green and stays in the warm
family, so the scheme's semantics are unchanged.

I left the default as your existing hexes, because in *this* dataset `disagree`
is 0 / 17,376 rows, so the collision never renders. **It does bite in the
gold-set figures, where `disagree` is populated** — recommend flipping those to
`flag_colors(cvd_safe=True)`. Also inherent to both variants: `agree` vs
`no_literature` is normal-vision ΔE 14.9 (just under 15), and three of the four
levels sit below 3:1 against a light surface, so the relief rule applies —
direct labels or a table view, which these figures carry.

## Design changes applied

- **Seeds are replicates, not identities.** Three categorical hues implied the
  seeds were the subject. They are now recessive gray marks behind an accent
  mean line (emphasis form), which frees color to carry the flag semantics.
- **Flags vs derived measures are kept apart.** Flag categories use the canonical
  scheme above. A *derived* quantity — "grounded rows" (agree + inferred), token
  counts, step counts — is not a flag, so it takes an analytic blue
  (`#256abf` / `#86b6ef`, validated all-pairs and as an ordinal pair) rather than
  borrowing a flag hue. That keeps green ⇒ "the agent claimed agreement" and blue
  ⇒ "a number we computed" unambiguous across all six figures.
- **Evenly spaced categorical x-axis** for the 8 scale conditions. The log axis
  crowded 500 against 893 and implied a continuum the design does not have.
- **One measure per axis.** The original cost figure's panels A/B put USD and
  minutes in one 2×2 block; `fig_r5` gives cost, runtime and per-pair tokens
  their own axes. No dual-axis anywhere. `fig_r5` also now states the unset
  limits in its footer, so "flat" cannot be misread as "hit a ceiling".
- **Fixed-pair heatmap geometry.** The original stretched Tnpo3's 10 rows to the
  same height as Srsf1's 23, so cells were not comparable between panels;
  `height_ratios` now makes every cell the same size. Cell separators are solid
  surface-colored hairlines (the inherited style made them dashed).
- 2px-equivalent surface gaps between stacked segments, hairline recessive grid,
  selective direct labels, legend always present, no hatch fills, `svg.fonttype:
  none` so SVG text stays editable in Illustrator. All five SVGs round-trip
  through `rsvg-convert`.

## Two notes on the existing figures

- `human_time_cost_comparison` panels B and C are the same curve: labor cost is
  time × a constant $25/h, so plotting both doubles one measure. Recommend
  dropping one panel, or keeping cost only and stating the rate in the caption.
  I did not rebuild it — the heuristic itself (15 min/target + 10 min/paper) is
  a modeling choice, not a plotting one.
- `structural_vs_grounding_recall` panel A draws full-height gray bars for
  "100% rows" behind the recall bars. The gray reads as a stacked segment rather
  than a reference. A hairline reference rule at 100% with the recall bars alone
  would carry the same claim with less ink.

## Caveat carried forward, unchanged

The target-scoped reports remain a **framework-derived** positive reference, not
a blinded external gold standard. Nothing here changes that; the self-limiting,
differentiation and burstiness findings are all internal to the runs and do not
depend on the reference at all, which makes them more robust than the recall
numbers, not less.
