#!/usr/bin/env python3
"""Score EVERY finding in the PerturbAI ledger on an editable rubric (the analytical mode).

This is the DATABASE operation the findings ledger was built for: instead of asking a
generation pass to read + curate the interesting findings (which satisfices and hits the
emission ceiling long before 11,343 rows), we author ONE deterministic scoring pass and let
code enumerate the whole table. Every row gets a transparent, rubric-derived score; the
output is a ranked table you sort / filter / threshold afterwards. Sidesteps the emission
ceiling by construction.

It is a cleaned, parameterized generalization of the one-off worked example at
`debug/260623_novelFindings/scan_manuscript_hypotheses.py`. Two deliberate differences:

  * It reads the CANONICAL findings ledger (narrative_findings.jsonl, the same file
    query_findings.py uses) rather than re-parsing JSON out of the report prose. Same
    11,343 findings, no fragile line-parsing, no parse-failure bookkeeping.
  * The "does this participate in a cross-target story" (convergence) dimension is computed
    from the DATA -- how many DISTINCT targets converge on the same theme / downstream gene
    -- instead of a hand-curated list of manuscript answer-families. The manuscript-specific
    families and their collapse-into-hypotheses step are OUT of scope here (that is dedup,
    a separate concern); see the worked example if you want them.

EVERYTHING you would tune lives in the RUBRIC block at the top of this file. Edit the
weights / vocab tables / theme regexes, re-run, and diff the ranking. That is the intended
workflow: run, read the top, adjust the rubric, re-run.

Stdlib only (json / csv / re / argparse) -- runs directly, no pixi env, like the other
findings-ledger scripts.

Examples
--------
Score the whole ledger, write the ranked table + methods, print the top 20 to stdout:

    python score_findings.py --out-dir ./findings_analysis --top 20

Score only a slice while iterating on the rubric (filters mirror query_findings.py):

    python score_findings.py --finding-type convergent_module --top 30 --out-dir /tmp/fa

Point at a different ledger:

    python score_findings.py --ledger-path /path/to/narrative_findings.jsonl --out-dir out
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------------------
# RUBRIC (edit me) -- every knob the scoring depends on is in this block.
# --------------------------------------------------------------------------------------

# Report confidence label -> numeric (0-5). Unknown labels fall back to CONFIDENCE_DEFAULT.
CONFIDENCE_SCORE = {"high": 4.5, "moderate": 3.2, "medium": 3.2, "exploratory": 1.8, "low": 1.1}
CONFIDENCE_DEFAULT = 2.5

# finding_type -> base impact (0-5). The 12-value vocabulary is closed (see SKILL.md).
FINDING_TYPE_IMPACT = {
    "convergent_module": 4.4,
    "disease_mechanism_refinement": 4.1,
    "cross_perturbation_contrast": 3.9,
    "cell_type_selectivity": 3.7,
    "pathway_uncoupling": 3.2,
    "biomarker_candidate": 3.0,
    "literature_direction_mismatch": 3.0,
    "homeostatic_compensation": 2.8,
    "therapeutic_direction_warning": 2.6,
    "buffered_response": 2.0,
    "negative_result": 1.4,
    "other": 2.2,
}
FINDING_TYPE_DEFAULT = 2.2

# literature_status -> novelty (0-5). This field is the novelty signal but has ~847 distinct
# free-text values (only the head is structured). We match the structured head exactly and
# fall back to a substring heuristic for the long tail (LITERATURE_NOVELTY_HEURISTIC).
LITERATURE_NOVELTY = {
    "contradicts_expected_relationship": 4.1,
    "opposes_reported_direction": 4.0,
    "novel_no_direct_literature": 4.0,
    "no_direct_literature": 3.9,
    "dataset_only": 3.6,
    "literature_direction_mismatch": 3.7,
    "disease_context_mismatch": 3.7,
    "refines_cell_type_context": 3.3,
    "refines_disease_mechanism": 3.3,
    "disease_mechanism_refinement": 3.3,
    "disease_context_refinement": 3.2,
    "refines_pathway_context": 3.0,
    "refines_therapeutic_context": 3.0,
    "extends_known_mechanism": 3.0,
    "refines_expected_relationship": 2.7,
    "refines_known_mechanism": 2.8,
    "literature_ambiguous": 2.3,
    "not_literature_based": 2.3,
    "dataset_negative_result": 1.5,
    "supports_known_mechanism": 1.8,
    "supports_known_control_behavior": 1.4,
    "supports_known_control_design": 1.4,
}
LITERATURE_NOVELTY_DEFAULT = 2.5  # literature_status present but unrecognized
LITERATURE_NOVELTY_MISSING = 2.3  # literature_status absent
# Ordered substring rules for the free-text long tail; first hit wins.
LITERATURE_NOVELTY_HEURISTIC: list[tuple[str, float]] = [
    ("contradict", 4.1), ("oppos", 4.0), ("novel", 3.9), ("no_direct_literature", 3.8),
    ("mismatch", 3.7), ("dataset_only", 3.6), ("refines_cell_type", 3.3),
    ("refines_disease", 3.3), ("refines_therapeutic", 3.0), ("refines_pathway", 3.0),
    ("extends", 3.0), ("refines", 2.7), ("ambiguous", 2.3),
    ("negative", 1.5), ("supports_known_control", 1.4), ("supports", 1.8),
]

# Themes are biology programs used for (a) unexpected cross-domain novelty bonuses and
# (b) the data-driven convergence signal. Edit / add freely; each maps a compiled regex
# run over the finding's text blob (prose + summary + genes + comparators + caveats).
THEME_REGEXES: dict[str, re.Pattern[str]] = {
    "sterol_srebp": re.compile(
        r"\b(sterol\w*|cholesterol|mevalonate|srebp\w*|srebf[12]|insig[12]|hmgcs1|hmgcr|"
        r"msmo1|dhcr\d+|cyp51|fdft1|sqle|ldlr)\b", re.I),
    "endolysosome_transport_motor": re.compile(
        r"\b(endolys\w*|lysos\w*|endos\w*|vesicle\w*|traffick\w*|motor|dynein|dynactin|"
        r"dctn1|dync1h1|kif\w*|rab\d+\w*|vps\d+\w*|clathrin|htt)\b", re.I),
    "ufmylation": re.compile(r"\b(ufm\w*|ufmylation|uba5|ufc1|ufl1|ufm1|ufsp2|ddrgk1)\b", re.I),
    "vatpase": re.compile(r"\b(v-?atpase|vacuolar atpase|atp6v\w*|atp6ap\w*)\b", re.I),
    "chromatin_cohesin": re.compile(
        r"\b(chromatin|cohesin|baf complex|swi[-/ ]snf|smarc\w*|arid[12]\w*|actl6b|brd\d+|"
        r"chd\d+|setd\w*|setdb\d+|kmt\w*|stag[123]|smc1a|smc3|rad21|nipbl|wapl|hdac\d*|"
        r"kansl\d*|kat\d+\w*|mecp2|ehmt\w*|yy1|phf\d+|trrap)\b", re.I),
    "synaptic_neuronal": re.compile(
        r"\b(synap\w*|postsyn\w*|presyn\w*|neurotrans\w*|nmda|grin[12][ab]?|dlg4|bdnf|vgf|"
        r"nptx\w*|snap25|stxbp\w*|neurexin|nrxn\w*)\b", re.I),
    "gaba_ei": re.compile(
        r"\b(gaba-?a|gaba receptor|gabrg\d*|gabra\d*|gabrb\d*|gabrd|gabre|gabrr\d*|slc6a1|"
        r"gad[12]|excitation-inhibition|e/i balance)\b", re.I),
    "proteostasis_upr": re.compile(
        r"\b(upr|unfolded protein|er stress|integrated stress|proteasome|proteostasis|"
        r"ddit3|atf4|hspa5|xbp1|chac1)\b", re.I),
    "mitochondria": re.compile(
        r"\b(mitochond\w*|oxidative phosphoryl\w*|respiratory chain|sod2|cox\d+\w*|nduf\w*|oxphos)\b", re.I),
    "autophagy_lysosome": re.compile(
        r"\b(autophag\w*|autolys\w*|atg\d+\w*|sqstm1|lamp\d+|rb1cc1|tfeb)\b", re.I),
    "rna_processing": re.compile(
        r"\b(splic\w*|rna processing|ribosom\w*|nonsense-mediated|xpo1|ddx\w*|rbm\w*|matr3|eif\w*)\b", re.I),
    "immune": re.compile(r"\b(interferon|cytokine|stat1|nf-?kb|nf-kappa|antigen present|mhc class)\b", re.I),
    "wnt_hedgehog_cilia": re.compile(
        r"\b(wnt\d*|beta-catenin|ctnnb1|apc|cili\w*|hedgehog|gli[123]?|smoothened|shh)\b", re.I),
    "circadian": re.compile(r"\b(circadian|clock gene|bmal1|arntl|per[12]|cry[12])\b", re.I),
    "mtor_tsc": re.compile(r"\b(mtor\w*|tsc[12]|rheb|raptor|rptor|mtorc[12])\b", re.I),
    "cell_cycle_e2f": re.compile(r"\b(e2f\d*|rb1|cell cycle|g1/s|proliferation)\b", re.I),
}

# Cross-domain theme pairs that are surprising together -> novelty bonus. Edit freely.
UNEXPECTED_COMBOS: list[tuple[frozenset[str], float]] = [
    (frozenset({"sterol_srebp", "endolysosome_transport_motor"}), 0.65),
    (frozenset({"chromatin_cohesin", "synaptic_neuronal"}), 0.45),
    (frozenset({"ufmylation", "mitochondria"}), 0.40),
    (frozenset({"autophagy_lysosome", "synaptic_neuronal"}), 0.35),
    (frozenset({"proteostasis_upr", "synaptic_neuronal"}), 0.30),
]

# Known / fidelity modules: when this target is perturbed AND the finding sits in the
# module's own theme, the "novelty" is really a positive-control recovery -> penalize.
# {module_name: (set_of_target_symbols_lowercase, theme_that_makes_it_a_control)}
KNOWN_FIDELITY_MODULES: dict[str, tuple[set[str], str]] = {
    "heat_shock": ({"hsf1", "hsf2"}, "proteostasis_upr"),
    "direct_sterol": ({"srebf1", "srebf2", "scap", "insig1", "insig2", "mbtps1", "mbtps2"}, "sterol_srebp"),
    "wnt": ({"apc", "ctnnb1", "wnt3a", "wnt5a"}, "wnt_hedgehog_cilia"),
    "circadian": ({"clock", "bmal1", "arntl", "per1", "per2", "cry1", "cry2"}, "circadian"),
    "cell_cycle_e2f": ({"rb1", "e2f1", "e2f2", "e2f3", "e2f4", "tfdp1", "tfdp2"}, "cell_cycle_e2f"),
    "mtor": ({"tsc1", "tsc2", "mtor", "rheb", "rptor", "rraga"}, "mtor_tsc"),
    "proteasome": ({f"psm{p}" for p in
                    ("b4", "b5", "b6", "c1", "c2", "c3", "c4", "c5", "c6", "d1", "d2", "d3", "d4")}
                   | {"pomp"}, "proteostasis_upr"),
    "upr": ({"ddit3", "atf4", "hspa5", "ern1", "eif2ak3", "xbp1", "atf6"}, "proteostasis_upr"),
}

# Component weights in the final score (need not sum to 1; final is clamped to [0,5]).
WEIGHTS = {
    "novelty": 0.30,
    "impact": 0.24,
    "convergence": 0.20,
    "confidence": 0.14,
    "evidence": 0.12,
    "caveat": 0.12,  # subtracted
}

# Novelty bin cut points, applied to any 0-5 component score.
BIN_CUTS = [(4.25, "high"), (3.55, "medium-high"), (2.65, "medium"), (1.75, "low-medium")]
BIN_FLOOR = "low"

# --------------------------------------------------------------------------------------
# Ledger loading (packaged canonical CSV; JSONL overrides remain supported)
# --------------------------------------------------------------------------------------

_DEFAULT_LEDGER = (
    Path(__file__).resolve().parents[3]
    / "artifacts"
    / "ledgers"
    / "findings.csv"
)

# top-level -> our key ; source.* -> our key. Keeps naming aligned with the report schema
# the worked example used (summary / why_it_matters) rather than the ledger's source_ prefix.
_SCALAR = {
    "finding_type": "finding_type", "confidence": "confidence", "direction": "direction",
    "literature_status": "literature_status", "main_caveats": "main_caveats",
    "source_summary": "summary", "source_why_it_matters": "why_it_matters",
}
_LIST = ("cell_types", "comparators", "genes", "evidence_ids", "ref_ids")


def ledger_path(override: str | None) -> Path:
    if override:
        return Path(override).expanduser()
    env = os.environ.get("DISTRIBUTED_AGENTS_FINDINGS_LEDGER")
    return Path(env).expanduser() if env else _DEFAULT_LEDGER


def as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value if v not in (None, "")]
    if isinstance(value, str) and value.strip():
        return [item for item in value.split("|") if item]
    return []


def load_findings(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise SystemExit(
            f"findings ledger not found at {path}\n"
            "Pass --ledger-path or set DISTRIBUTED_AGENTS_FINDINGS_LEDGER."
        )
    out: list[dict[str, Any]] = []
    if path.suffix.casefold() == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            for rec in csv.DictReader(handle):
                target = str(rec.get("target_gene") or "")
                finding = str(rec.get("finding_id") or "")
                row = {
                    "doc_id": f"{target}:{finding}",
                    "finding_id": finding,
                    "gene_target": target,
                    "hipporag_text": " ".join(
                        filter(
                            None,
                            (
                                str(rec.get("summary") or ""),
                                str(rec.get("why_it_matters") or ""),
                            ),
                        )
                    ),
                    "finding_type": rec.get("finding_type"),
                    "confidence": rec.get("confidence"),
                    "direction": rec.get("direction"),
                    "literature_status": rec.get("literature_status"),
                    "main_caveats": rec.get("main_caveats"),
                    "summary": rec.get("summary"),
                    "why_it_matters": rec.get("why_it_matters"),
                }
                for key in _LIST:
                    row[key] = as_list(rec.get(key))
                out.append(row)
        return out
    with path.open() as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            src = rec.get("source") or {}
            row: dict[str, Any] = {
                "doc_id": rec.get("doc_id", ""),
                "finding_id": rec.get("finding_id", ""),
                "gene_target": rec.get("gene_target", ""),
                "hipporag_text": rec.get("hipporag_text", "") or "",
            }
            for k, dest in _SCALAR.items():
                row[dest] = src.get(k)
            for k in _LIST:
                row[k] = as_list(src.get(k))
            out.append(row)
    return out


# --------------------------------------------------------------------------------------
# Scoring helpers
# --------------------------------------------------------------------------------------

def clamp(value: float, lo: float = 0.0, hi: float = 5.0) -> float:
    return max(lo, min(hi, value))


def compact(value: Any, max_chars: int = 1100) -> str:
    if value is None:
        return ""
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= max_chars else text[: max_chars - 1].rstrip() + "…"


def bin_label(score: float) -> str:
    for cut, label in BIN_CUTS:
        if score >= cut:
            return label
    return BIN_FLOOR


def blob_for(row: dict[str, Any]) -> str:
    parts = [
        row["gene_target"], row.get("finding_type") or "", row.get("summary") or "",
        row.get("why_it_matters") or "", row.get("hipporag_text") or "",
        " ".join(row["cell_types"]), " ".join(row["genes"]), " ".join(row["comparators"]),
        row.get("direction") or "", row.get("literature_status") or "", row.get("main_caveats") or "",
    ]
    return " ".join(p for p in parts if p).lower()


def themes_for(blob: str) -> list[str]:
    return [theme for theme, rx in THEME_REGEXES.items() if rx.search(blob)]


def literature_novelty(status: str | None) -> float:
    if not status:
        return LITERATURE_NOVELTY_MISSING
    key = status.strip().lower()
    if key in LITERATURE_NOVELTY:
        return LITERATURE_NOVELTY[key]
    for needle, value in LITERATURE_NOVELTY_HEURISTIC:
        if needle in key:
            return value
    return LITERATURE_NOVELTY_DEFAULT


def is_known_fidelity(target: str, themes: set[str]) -> bool:
    t = target.lower()
    return any(t in members and theme in themes for members, theme in KNOWN_FIDELITY_MODULES.values())


def caveat_flags(row: dict[str, Any], blob: str, themes: set[str]) -> list[str]:
    flags: list[str] = []
    ftype = (row.get("finding_type") or "").lower()
    conf = (row.get("confidence") or "").lower()
    if ftype == "negative_result" or re.search(r"\bnull\b|negative result|no response", blob):
        flags.append("negative_or_null")
    if re.search(r"\bno fdr\b|\b0/\d+[^.;]{0,30}\bfdr|\bno (?:significant|fdr)\b", blob):
        flags.append("no_fdr_or_weak")
    if "target transcript" in blob and any(
        s in blob for s in ("not detected", "not significantly changed", "no measured", "weak", "nominal")
    ):
        flags.append("weak_target_engagement")
    if "target-only" in blob or "target only" in blob:
        flags.append("target_only")
    if conf in {"exploratory", "low"}:
        flags.append("low_confidence")
    if any(s in blob for s in ("technical caveat", "guide-level", "low cell", "small n", "few cells")):
        flags.append("technical_or_power")
    if is_known_fidelity(row["gene_target"], themes):
        flags.append("known_fidelity_module")
    return sorted(set(flags))


CAVEAT_WEIGHTS = {
    "negative_or_null": 0.75, "no_fdr_or_weak": 0.9, "weak_target_engagement": 0.9,
    "target_only": 0.8, "low_confidence": 0.7, "technical_or_power": 0.45,
    "known_fidelity_module": 0.85,
}


def caveat_severity(flags: list[str]) -> float:
    return min(3.4, sum(CAVEAT_WEIGHTS.get(f, 0.3) for f in flags))


# --------------------------------------------------------------------------------------
# Corpus-level convergence: how many DISTINCT targets converge on the same program.
# This is the aggregate the analytical mode is for -- an isolated target note scores low,
# a finding whose theme / downstream genes recur across many targets scores high.
# --------------------------------------------------------------------------------------

def corpus_convergence(findings: list[dict[str, Any]]) -> tuple[dict[str, int], dict[str, set[str]]]:
    theme_targets: dict[str, set[str]] = defaultdict(set)
    gene_targets: dict[str, set[str]] = defaultdict(set)
    for row in findings:
        blob = blob_for(row)
        target = row["gene_target"]
        for theme in themes_for(blob):
            theme_targets[theme].add(target)
        for g in row["genes"] + row["comparators"]:
            gl = g.strip().lower()
            if gl and gl != target.lower():
                gene_targets[gl].add(target)
    return {t: len(s) for t, s in theme_targets.items()}, gene_targets


def convergence_score(
    row: dict[str, Any], themes: list[str], blob: str,
    theme_counts: dict[str, int], gene_targets: dict[str, set[str]],
) -> tuple[float, int, str]:
    """0-5 convergence, plus the raw distinct-target support and what drove it (for audit)."""
    target = row["gene_target"].lower()
    best_theme = max((t for t in themes), key=lambda t: theme_counts.get(t, 0), default="")
    theme_support = theme_counts.get(best_theme, 0)
    gene_support, best_gene = 0, ""
    for g in row["genes"] + row["comparators"]:
        others = gene_targets.get(g.strip().lower(), set()) - {row["gene_target"]}
        if len(others) > gene_support:
            gene_support, best_gene = len(others), g
    support = max(theme_support, gene_support)
    driver = best_gene if gene_support >= theme_support and best_gene else best_theme
    # log-scaled: 1 target -> ~0.6, ~10 -> ~2.5, ~60 -> ~4, ~150+ -> ~5
    conv = clamp(1.25 * math.log1p(support)) if support else 0.4
    ftype = (row.get("finding_type") or "").lower()
    if ftype in {"convergent_module", "cross_perturbation_contrast"}:
        conv = clamp(conv + 0.5)
    if len(row["comparators"]) >= 1:
        conv = clamp(conv + 0.2 * min(3, len(row["comparators"])))
    return conv, support, driver


def score_row(
    row: dict[str, Any],
    theme_counts: dict[str, int],
    gene_targets: dict[str, set[str]],
) -> dict[str, Any]:
    blob = blob_for(row)
    themes = themes_for(blob)
    theme_set = set(themes)
    flags = caveat_flags(row, blob, theme_set)
    caveat = caveat_severity(flags)

    ftype = row.get("finding_type") or "other"
    conf_score = CONFIDENCE_SCORE.get((row.get("confidence") or "").lower(), CONFIDENCE_DEFAULT)
    lit_nov = literature_novelty(row.get("literature_status"))

    cell_types, genes, comps = row["cell_types"], row["genes"], row["comparators"]
    ev_ids, ref_ids = row["evidence_ids"], row["ref_ids"]

    # Evidence strength: how grounded is the claim.
    evidence = 1.0
    evidence += min(1.1, 0.22 * len(ev_ids))
    evidence += min(0.9, 0.12 * len(ref_ids))
    if len(cell_types) == 1:
        evidence += 0.45
    elif 2 <= len(cell_types) <= 5:
        evidence += 0.85
    elif 6 <= len(cell_types) <= 12:
        evidence += 0.65
    elif len(cell_types) > 12:
        evidence += 0.20
    evidence += min(1.0, 0.16 * len(comps))
    if row.get("direction"):
        evidence += 0.35
    evidence = clamp(evidence - 0.30 * caveat, 0.4)

    # Novelty: literature status is the anchor; add unexpected cross-domain combos, subtract
    # known-fidelity recovery and caveats.
    unexpected = sum(bonus for combo, bonus in UNEXPECTED_COMBOS if combo <= theme_set)
    if re.search(r"opposite|antagon|divergent|paradox", blob):
        unexpected += 0.35
    known_penalty = 0.95 if "known_fidelity_module" in flags else 0.0
    low_signal = 0.45 if ftype in {"negative_result", "buffered_response"} else 0.0
    novelty = clamp(
        lit_nov
        + 0.35 * (ftype in {"cross_perturbation_contrast", "convergent_module"})
        + 0.25 * (ftype == "cell_type_selectivity")
        + unexpected
        + 0.18 * max(0, min(5, len(themes)) - 1)
        - known_penalty - low_signal - 0.23 * caveat,
        0.6,
    )

    # Impact: finding type + breadth + confidence.
    impact = clamp(
        FINDING_TYPE_IMPACT.get(ftype, FINDING_TYPE_DEFAULT)
        + 0.18 * min(4, len(cell_types))
        + 0.12 * min(8, len(genes))
        + 0.20 * min(5, len(comps))
        + 0.22 * (conf_score - 2.5)
        - 0.35 * caveat - 0.45 * known_penalty,
        0.5,
    )

    conv, conv_support, conv_driver = convergence_score(row, themes, blob, theme_counts, gene_targets)

    final = clamp(
        WEIGHTS["novelty"] * novelty
        + WEIGHTS["impact"] * impact
        + WEIGHTS["convergence"] * conv
        + WEIGHTS["confidence"] * conf_score
        + WEIGHTS["evidence"] * evidence
        - WEIGHTS["caveat"] * caveat,
        0.4,
    )

    return {
        "doc_id": row["doc_id"],
        "gene_target": row["gene_target"],
        "finding_id": row["finding_id"],
        "finding_type": ftype,
        "final_score": round(final, 3),
        "novelty_score": round(novelty, 3),
        "novelty": bin_label(novelty),
        "impact_score": round(impact, 3),
        "impact": bin_label(impact),
        "convergence_score": round(conv, 3),
        "convergence_support": conv_support,
        "convergence_driver": conv_driver,
        "confidence": row.get("confidence") or "",
        "confidence_score": round(conf_score, 3),
        "evidence_strength": round(evidence, 3),
        "caveat_severity": round(caveat, 3),
        "caveat_flags": "|".join(flags),
        "themes": "|".join(themes),
        "literature_status": row.get("literature_status") or "",
        "direction": compact(row.get("direction"), 200),
        "n_cell_types": len(cell_types),
        "n_genes": len(genes),
        "n_comparators": len(comps),
        "n_evidence_ids": len(ev_ids),
        "n_ref_ids": len(ref_ids),
        "cell_types": "|".join(cell_types),
        "summary": compact(row.get("summary")),
        "why_it_matters": compact(row.get("why_it_matters")),
        "main_caveats": compact(row.get("main_caveats")),
    }


# --------------------------------------------------------------------------------------
# Optional filters (mirror query_findings.py) for rubric iteration on a slice
# --------------------------------------------------------------------------------------

def keep(row: dict[str, Any], genes: set[str], ftypes: set[str], grep: re.Pattern | None) -> bool:
    if genes and row["gene_target"].casefold() not in genes:
        return False
    if ftypes and (row.get("finding_type") or "") not in ftypes:
        return False
    if grep is not None and not grep.search(blob_for(row)):
        return False
    return True


# --------------------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------------------

RANKED_FIELDS = [
    "rank", "final_score", "novelty", "impact", "convergence_score", "convergence_support",
    "convergence_driver", "gene_target", "finding_id", "doc_id", "finding_type",
    "literature_status", "confidence", "caveat_flags", "themes", "n_cell_types", "n_genes",
    "n_comparators", "n_evidence_ids", "n_ref_ids", "cell_types", "direction",
    "novelty_score", "impact_score", "confidence_score", "evidence_strength",
    "caveat_severity", "summary", "why_it_matters", "main_caveats",
]


def write_ranked_csv(rows: list[dict[str, Any]], out_dir: Path) -> Path:
    path = out_dir / "ranked_findings.csv"
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RANKED_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_distribution_csv(rows: list[dict[str, Any]], out_dir: Path) -> dict[str, int]:
    counts = Counter(r["novelty"] for r in rows)
    order = ["high", "medium-high", "medium", "low-medium", "low"]
    total = len(rows) or 1
    with (out_dir / "novelty_distribution.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["novelty", "n_findings", "fraction"])
        for b in order:
            writer.writerow([b, counts.get(b, 0), round(counts.get(b, 0) / total, 6)])
    return counts


def write_methods(rows: list[dict[str, Any]], counts: dict[str, int], ledger: Path, out_dir: Path) -> None:
    order = ["high", "medium-high", "medium", "low-medium", "low"]
    total = len(rows) or 1
    dist = "\n".join(f"- {b}: {counts.get(b, 0)} ({100 * counts.get(b, 0) / total:.1f}%)" for b in order)
    ftype_lines = "\n".join(
        f"- {ft}: {n}" for ft, n in Counter(r["finding_type"] for r in rows).most_common()
    )
    (out_dir / "methods.md").write_text(
        f"""# Methods: findings-analysis scoring pass

## Input
Canonical findings ledger: `{ledger}` -- {len(rows):,} findings scored (one row per finding).

## Rubric
Each finding is scored on five 0-5 components combined by `WEIGHTS` (edit in
`score_findings.py`), then clamped to [0,5]:

- **novelty** -- anchored on `literature_status` (structured head matched exactly, long tail
  by substring heuristic), plus finding-type novelty and unexpected cross-domain theme
  combinations; minus known/fidelity-module recovery and caveats.
- **impact** -- `finding_type` base impact + breadth (cell types / downstream genes /
  comparators) + report confidence; minus caveats and known-module penalty.
- **convergence** -- DATA-DRIVEN: log-scaled count of DISTINCT other targets that share the
  finding's dominant theme or a downstream gene (an isolated target note scores low; a
  program recurring across many targets scores high). Not a curated family list.
- **confidence** -- report confidence label mapped to a numeric scale.
- **evidence** -- evidence/reference IDs, cell-type specificity, comparator support,
  direction; minus caveats.
- **caveat_severity** (subtracted) -- negative/null, no-FDR/weak engagement, target-only,
  low/exploratory confidence, technical/power, known fidelity module.

Themes, novelty/impact tables, caveat weights, unexpected combos, and known-fidelity
modules are all editable constants at the top of `score_findings.py`. This is a manuscript
TRIAGE ranking of the report claims + caveats, not a reanalysis of the raw DE matrix.

## finding_type composition
{ftype_lines}

## Novelty-bin distribution
{dist}

## Boundaries
Metadata is a lossy proxy: it CANNOT separate a rung-0 "recovered a known module" from a
rung-2 "so what" WITHIN a finding_type -- that payoff is semantic and needs reading the
report prose (`findings-ledger-skill/scripts/read_reports.py`). Collapsing findings into
de-duplicated convergent stories is out of scope here (that is dedup, a separate concern).
"""
    )


def print_top(rows: list[dict[str, Any]], n: int) -> None:
    if n <= 0:
        return
    print(f"\nTop {min(n, len(rows))} findings by final_score:")
    print(f"{'rank':>4}  {'score':>5}  {'nov':<11}  {'conv':>4}  {'target':<14}  {'fid':<5}  finding_type / literature_status")
    for r in rows[:n]:
        print(f"{r['rank']:>4}  {r['final_score']:>5.2f}  {r['novelty']:<11}  "
              f"{r['convergence_support']:>4}  {r['gene_target'][:14]:<14}  {r['finding_id']:<5}  "
              f"{r['finding_type']} / {r['literature_status'][:40]}")


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ledger-path", default=None, help="Override the findings ledger JSONL path.")
    p.add_argument("--out-dir", default="./findings_analysis", help="Directory for output files.")
    p.add_argument("--top", type=int, default=20, help="Print this many top findings to stdout (0 = none).")
    p.add_argument("--gene", action="append", dest="genes", default=[],
                   help="Score only these gene_targets (case-insensitive); repeatable.")
    p.add_argument("--finding-type", action="append", dest="finding_types", default=[],
                   help="Score only these finding_type values; repeatable.")
    p.add_argument("--grep", default=None, help="Score only findings whose text matches this regex.")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    path = ledger_path(args.ledger_path)
    findings = load_findings(path)

    # Convergence is computed over the WHOLE corpus, then scoring is restricted to any slice.
    theme_counts, gene_targets = corpus_convergence(findings)

    genes = {g.casefold() for g in args.genes}
    ftypes = set(args.finding_types)
    grep = re.compile(args.grep, re.I) if args.grep else None
    selected = [r for r in findings if keep(r, genes, ftypes, grep)]
    if not selected:
        raise SystemExit("no findings matched the filters.")

    scored = [score_row(r, theme_counts, gene_targets) for r in selected]
    scored.sort(key=lambda r: (r["final_score"], r["novelty_score"], r["impact_score"]), reverse=True)
    for i, r in enumerate(scored, start=1):
        r["rank"] = i

    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    ranked = write_ranked_csv(scored, out_dir)
    counts = write_distribution_csv(scored, out_dir)
    write_methods(scored, counts, path, out_dir)

    print(f"ledger={path}")
    print(f"scored_findings={len(scored)}"
          + (f" (filtered from {len(findings)})" if len(scored) != len(findings) else ""))
    print("novelty_distribution=" + json.dumps({b: counts.get(b, 0) for b in
          ["high", "medium-high", "medium", "low-medium", "low"]}))
    print(f"ranked -> {ranked}")
    print(f"methods -> {out_dir / 'methods.md'}")
    print_top(scored, args.top)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
