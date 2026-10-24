#!/usr/bin/env python3
"""Apply LLM normalization (normalization.tsv) to the live graph (run in biokg env):
- set semantic_type on classified concepts (NOT concept_type: that property was the
  node-label duplicate and was removed 2026-08-24, TODO P2-7)
- add 5 tail-surfaced programs + LLM CANONICAL_PROGRAM (recall gain + new programs)
- drop CANONICAL_PROGRAM from concepts the LLM typed as NON-program (keyword FPs)
- rebuild IMPLICATES_PROGRAM from the current CANONICAL_PROGRAM set
Support>=2 layer uses LLM; support-1 keeps keyword (interim until full-corpus run)."""
import csv, os
from neo4j import GraphDatabase
from ..paths import NORMALIZATION_FILE
URI=os.environ.get("BIOKG_NEO4J_BOLT","bolt://127.0.0.1:7687")
AUTH=("neo4j",os.environ.get("BIOKG_NEO4J_PASSWORD","biokgpassword"))
CONCEPT_LABELS=["Pathway","Complex","Module","Phenotype","Other"]
NEW_PROGRAMS={"Hedgehog":("regulon","Hedgehog signaling"),"JAK_STAT":("regulon","JAK-STAT signaling"),
 "NF_kB":("regulon","NF-kB signaling"),"Autophagy":("process","autophagy"),"MAPK_ERK":("regulon","MAPK/ERK signaling")}
ALIAS={"UPR_ER":"UPR"}  # LLM id -> existing Program id
EXISTING={"ISR_ATF4","Proteasome","Sterol_SREBP2","BAF_SWISNF","UPR","OXPHOS","Spliceosome","mTOR","Wnt_bcatenin","Circadian"}

rows=list(csv.DictReader(open(NORMALIZATION_FILE),delimiter="\t"))
for r in rows: r["program_id"]=ALIAS.get(r["program_id"],r["program_id"])
types=[{"name":r["concept"],"t":r["type"],"pid":r["program_id"]} for r in rows]
canon=[{"name":r["concept"],"pid":r["program_id"]} for r in rows
       if r["type"]=="program" and r["program_id"] in (EXISTING|set(NEW_PROGRAMS))]

drv=GraphDatabase.driver(URI,auth=AUTH)
with drv.session(database="neo4j") as s:
    # new programs
    s.run("""UNWIND $rows AS r MERGE (p:BioKGNode:Program {program_id:r.id})
             SET p.name=r.name, p.kind=r.kind, p.canonical=true""",
          rows=[{"id":k,"name":v[1],"kind":v[0]} for k,v in NEW_PROGRAMS.items()]).consume()
    # LLM semantic-type tags. Write `semantic_type` only: `concept_type` was a verbatim copy of
    # the node label (11,129/11,129) and was removed 2026-08-24 (TODO P2-7), and `program_id_llm`
    # was write-only — the CANONICAL_PROGRAM edges below come from `r.pid` in the rows, never from
    # the node property. (Historically this query clobbered `concept_type`; see decisions.md
    # 2026-06-29 and the P0-2 fix.)
    # Match on name OR alias: the P2-4 label-blind merge collapses spelling
    # variants into one node, so a normalization row keyed on a merged-away
    # spelling would otherwise stop resolving.
    s.run(f"""UNWIND $rows AS r
              MATCH (c) WHERE any(l IN labels(c) WHERE l IN $labs)
                AND (c.name = r.name OR r.name IN split(coalesce(c.aliases,''), '|'))
              SET c.semantic_type=r.t""", rows=types, labs=CONCEPT_LABELS).consume()
    # LLM canonical mappings (additive)
    s.run(f"""UNWIND $rows AS r
              MATCH (c) WHERE any(l IN labels(c) WHERE l IN $labs)
                AND (c.name = r.name OR r.name IN split(coalesce(c.aliases,''), '|'))
              MATCH (p:Program {{program_id:r.pid}}) MERGE (c)-[:CANONICAL_PROGRAM]->(p)""",
          rows=canon, labs=CONCEPT_LABELS).consume()
    # drop CANONICAL_PROGRAM from concepts LLM typed as NON-program (keyword FP cleanup)
    nfp=s.run("""MATCH (c)-[r:CANONICAL_PROGRAM]->()
                 WHERE c.semantic_type IN ['phenotype','disease','anatomy_celltype','assay_or_molecule_noise']
                 DELETE r RETURN count(r) AS n""").single()["n"]
    # rebuild IMPLICATES_PROGRAM from current CANONICAL_PROGRAM
    s.run("MATCH ()-[r:IMPLICATES_PROGRAM]->() DELETE r").consume()
    s.run("""MATCH (f:Finding)-[i:IMPLICATES]->(c)-[:CANONICAL_PROGRAM]->(p:Program)
             MERGE (f)-[r:IMPLICATES_PROGRAM]->(p) ON CREATE SET r.effect_status=i.effect_status""").consume()
    print(f"new_programs={len(NEW_PROGRAMS)}  typed={len(types)}  llm_canon_edges={len(canon)}  dropped_FP_canon={nfp}")
drv.close()
