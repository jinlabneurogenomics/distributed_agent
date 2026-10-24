#!/usr/bin/env python3
"""#2 LLM concept-typer + normalizer (uses the `claude` CLI as the LLM).
Types each concept and maps program-concepts to a controlled catalog (handling
negation / sibling-pathway / process-vs-disease that keyword matching can't).
First batch: support>=2 concepts. Output: normalization.tsv."""
import json, subprocess, sys, re, time

from ..paths import NORMALIZATION_WORK_DIR

SC = "/tmp/claude-180630/-gpfs-group-jin-asun-distributed_agents/ef7831bc-5626-496a-b8b5-acbfea8a2788/scratchpad"
OUT = NORMALIZATION_WORK_DIR / "normalization.tsv"
CATALOG = ["ISR_ATF4","Proteasome","Sterol_SREBP2","BAF_SWISNF","UPR_ER","OXPHOS","Spliceosome",
           "mTOR","Wnt_bcatenin","Circadian","Hedgehog","JAK_STAT","NF_kB","Autophagy","MAPK_ERK"]

PROMPT = """You normalize biological concept labels from a mouse-brain Perturb-seq knowledge graph. \
For EACH concept return JSON {{"concept":..., "type":..., "program_id":...}}.
type is one of: program | phenotype | disease | anatomy_celltype | assay_or_molecule_noise
 - program = a molecular pathway / complex / process / regulon / stress-axis.
 - phenotype = a response-quality descriptor (buffered/null/weak/sparse/silent response, depletion).
 - anatomy_celltype = brain region / cell class / neurotransmitter identity.
 - assay_or_molecule_noise = assay/method terms (CRISPR, Perturb-seq), generic molecules/ions, or negations like "non-X".
program_id: if type=program, map to EXACTLY ONE of this controlled list, else "emergent":
{catalog}
 - Distinctions you MUST respect: noncanonical Wnt / Wnt-PCP / planar-cell-polarity is NOT Wnt_bcatenin -> "emergent". \
Mitochondrial UPR (UPRmt) is NOT UPR_ER -> "emergent". Mitochondrial ISR that converges on ATF4 -> ISR_ATF4 is OK. \
A "non-<X>" negation is assay_or_molecule_noise, never program X.
If type != program, program_id = null.
Return ONLY a JSON array, no prose. Concepts:
{names}"""

def classify(batch):
    p = PROMPT.format(catalog=json.dumps(CATALOG), names=json.dumps(batch))
    for attempt in range(2):
        r = subprocess.run(["claude","-p",p], capture_output=True, text=True, timeout=300)
        out = r.stdout.strip()
        m = re.search(r"\[.*\]", out, re.S)
        if m:
            try: return json.loads(m.group(0))
            except Exception: pass
        time.sleep(2)
    print(f"  !! batch failed ({len(batch)} concepts)", file=sys.stderr)
    return [{"concept":c,"type":"UNPARSED","program_id":None} for c in batch]

def main():
    allc = json.load(open(f"{SC}/concepts.json"))
    names = sorted({c["name"] for c in allc if c["name"] and c["n_targets"]>=2})
    print(f"classifying {len(names)} support>=2 concepts in batches")
    rows=[]; B=150
    for i in range(0, len(names), B):
        batch = names[i:i+B]
        rows += classify(batch)
        print(f"  {min(i+B,len(names))}/{len(names)} done")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT,"w") as f:
        f.write("concept\ttype\tprogram_id\n")
        for r in rows:
            f.write(f"{r.get('concept','')}\t{r.get('type','')}\t{r.get('program_id') or ''}\n")
    from collections import Counter
    print("\ntype breakdown:", Counter(r.get("type") for r in rows).most_common())
    prog = Counter(r.get("program_id") for r in rows if r.get("type")=="program")
    print("program_id breakdown:", prog.most_common())

if __name__=="__main__": main()
