#!/usr/bin/env python3
"""Findings-centric program layer -> live Neo4j (run in `biokg` pixi env).
Adds: Program nodes, (Gene)-[:MEMBER_OF]->(Program) ontology backbone,
(concept)-[:CANONICAL_PROGRAM]->(Program) canonicalization rollup, and
(Finding)-[:IMPLICATES_PROGRAM {effect_status}]->(Program) curated link.
Additive/reversible: rollback with  MATCH (p:Program) DETACH DELETE p  (+ remove the 2 rels).
"""
import re, os
from neo4j import GraphDatabase

URI = os.environ.get("BIOKG_NEO4J_BOLT", "bolt://127.0.0.1:7687")
AUTH = ("neo4j", os.environ.get("BIOKG_NEO4J_PASSWORD", "biokgpassword"))
CONCEPT_LABELS = ["Pathway", "Complex", "Module", "Phenotype", "Other"]

PROGRAMS = {
 "ISR_ATF4": dict(kind="regulon", name="integrated stress response (ATF4)",
   pat=r"integrated stress|\bisr\b|atf4|amino.?acid.{0,25}(stress|deprivation|response|starvation|module)|gcn2",
   members=["Atf4","Ddit3","Chac1","Asns","Trib3","Atf3","Mthfd2","Aldh18a1","Slc7a11","Cebpb","Wars","Cars","Sesn2","Gdf15","Stc2","Nupr1","Psat1","Phgdh","Shmt2","Slc7a5","Slc1a4","Atf5","Cebpg"]),
 "Proteasome": dict(kind="complex", name="26S proteasome",
   pat=r"proteasom|ubiquitin.?proteasome|\b26s\b|\b20s\b",
   members=["Psma1","Psma2","Psma3","Psma4","Psma5","Psma6","Psma7","Psmb1","Psmb2","Psmb3","Psmb4","Psmb5","Psmb6","Psmb7","Psmc1","Psmc2","Psmc3","Psmc4","Psmc5","Psmc6","Psmd1","Psmd2","Psmd3","Psmd4","Psmd6","Psmd7","Psmd8","Psmd11","Psmd12","Psmd13","Psmd14","Pomp","Nfe2l1","Psme1","Psme2"]),
 "Sterol_SREBP2": dict(kind="regulon", name="sterol/cholesterol biosynthesis (SREBP2)",
   pat=r"sterol|cholesterol|srebp|mevalonate|isoprenoid|lipid biosynth",
   members=["Hmgcr","Hmgcs1","Sqle","Fdft1","Dhcr7","Dhcr24","Msmo1","Mvd","Mvk","Idi1","Lss","Cyp51","Insig1","Ldlr","Fdps","Nsdhl","Sc5d","Acat2","Srebf2","Insig2","Hsd17b7","Tm7sf2","Ebp"]),
 "BAF_SWISNF": dict(kind="complex", name="mSWI/SNF (BAF) complex",
   pat=r"\bbaf\b|swi/?snf|swi.snf|mswi|\bbrg1\b|brahma",
   members=["Smarca2","Smarca4","Smarcb1","Smarcc1","Smarcc2","Smarcd1","Smarcd2","Smarcd3","Smarce1","Arid1a","Arid1b","Arid2","Pbrm1","Actl6a","Ss18","Bcl7a","Bcl7b","Bcl7c","Dpf1","Dpf2","Dpf3","Phf10","Brd9","Bcl11a","Bcl11b"]),
 "UPR": dict(kind="regulon", name="unfolded protein response (ER)",
   pat=r"unfolded protein|\bupr\b|er stress|endoplasmic reticulum stress|ire1|xbp1|\bperk\b|atf6",
   members=["Hspa5","Xbp1","Herpud1","Dnajb9","Sel1l","Hyou1","Manf","Pdia4","Pdia6","Dnajc3","Sdf2l1","Edem1","Derl3","Atf6","Creld2","Syvn1","Hspa13","Sec61b"]),
 "OXPHOS": dict(kind="process", name="oxidative phosphorylation",
   pat=r"oxphos|oxidative phosphoryl|respiratory chain|electron transport|complex i\b|mitochondrial respirat",
   members=["Ndufs1","Ndufs4","Ndufv1","Ndufa9","Ndufb8","Ndufa13","Sdha","Sdhb","Uqcrc1","Uqcrc2","Uqcrb","Cox4i1","Cox5a","Cox5b","Cox6c","Cox7a2","Atp5f1a","Atp5f1b","Atp5mc1","Atp5pb","Cycs"]),
 "Spliceosome": dict(kind="complex", name="spliceosome",
   pat=r"spliceosom|\bsplicing\b|pre-?mrna splic|snrnp|\bsplice\b",
   members=["Snrnp70","Snrpb","Snrpd1","Snrpd2","Snrpd3","Snrpe","Sf3b1","Sf3b2","Sf3a1","Sf3a3","U2af1","U2af2","Prpf8","Prpf6","Prpf31","Eftud2","Snrnp200","Sart3","Snrpa1","Sf3b3"]),
 "mTOR": dict(kind="complex", name="mTOR signaling",
   pat=r"mtorc1|\bmtor\b|mechanistic target of rapamycin|rapamycin",
   members=["Mtor","Rptor","Mlst8","Akt1s1","Deptor","Rheb"]),
 "Wnt_bcatenin": dict(kind="regulon", name="Wnt/beta-catenin signaling",
   pat=r"\bwnt\b|beta-catenin|β-catenin|tcf/?lef",
   members=["Axin2","Nkd1","Notum","Lef1","Tcf7","Ccnd1","Wif1","Sp5","Rnf43","Znrf3","Lgr5","Apcdd1","Dkk1","Tnfrsf19","Wnt9b"]),
 "Circadian": dict(kind="regulon", name="circadian clock",
   pat=r"circadian|\bclock\b|bmal|cryptochrome|period gene|rev-?erb|cry1|cry2|per1|per2",
   members=["Arntl","Bmal1","Per1","Per2","Per3","Cry1","Cry2","Nr1d1","Nr1d2","Dbp","Ciart","Bhlhe40","Bhlhe41","Npas2","Nfil3","Tef","Hlf"]),
}

# exclusion rules — keyword matching can't read negation/sibling-pathway/process-vs-disease
GLOBAL_EXCLUDE = r"\bdisease\b|\bdisorder\b|\bsyndrome\b"          # programs are not diseases
EXCLUDES = {
 "ISR_ATF4": r"branched-chain",                                    # BCAA catabolism != ISR
 "BAF_SWISNF": r"non-baf",                                         # "non-BAF complex" is the negation
 "UPR": r"mitochondrial",                                          # UPRmt is distinct from ER-UPR
 "Wnt_bcatenin": r"noncanonical|non-canonical|planar|\bpcp\b|/pcp|cadherin",  # PCP is beta-catenin-independent
}
def matches(nm, pid):
    if re.search(GLOBAL_EXCLUDE, nm, re.I): return False
    ex = EXCLUDES.get(pid)
    if ex and re.search(ex, nm, re.I): return False
    return bool(re.search(PROGRAMS[pid]["pat"], nm, re.I))

drv = GraphDatabase.driver(URI, auth=AUTH)
with drv.session(database="neo4j") as s:
    # 0. reset prior program layer (idempotent re-run; removes Program + MEMBER_OF/CANONICAL_PROGRAM/IMPLICATES_PROGRAM)
    s.run("MATCH (p:Program) DETACH DELETE p").consume()
    # 1. Program nodes
    s.run("""UNWIND $rows AS r MERGE (p:BioKGNode:Program {program_id:r.id})
             SET p.name=r.name, p.kind=r.kind, p.canonical=true""",
          rows=[{"id":k,"name":v["name"],"kind":v["kind"]} for k,v in PROGRAMS.items()]).consume()
    # 2. MEMBER_OF backbone (MERGE Gene so backbone exists even if no finding names it)
    mem=[{"g":g,"p":k} for k,v in PROGRAMS.items() for g in v["members"]]
    s.run("""UNWIND $rows AS r MERGE (gn:BioKGNode:Gene {name:r.g})
             WITH gn,r MATCH (p:Program {program_id:r.p})
             MERGE (gn)-[:MEMBER_OF {source:'curated'}]->(p)""", rows=mem).consume()
    # 3. CANONICAL_PROGRAM rollup (match concept names in Python, push mapping)
    concepts = s.run(f"""MATCH (c) WHERE any(l IN labels(c) WHERE l IN $labs)
                         RETURN c.name AS name LIMIT 100000""", labs=CONCEPT_LABELS).data()
    names = sorted({c["name"] for c in concepts if c["name"]})
    mapping=[{"name":nm,"p":k} for nm in names for k in PROGRAMS if matches(nm, k)]
    s.run(f"""UNWIND $rows AS r MATCH (c) WHERE c.name=r.name AND any(l IN labels(c) WHERE l IN $labs)
              MATCH (p:Program {{program_id:r.p}}) MERGE (c)-[:CANONICAL_PROGRAM]->(p)""",
          rows=mapping, labs=CONCEPT_LABELS).consume()
    # 4. curated Finding -> Program link, carrying LLM effect_status
    s.run("""MATCH (f:Finding)-[i:IMPLICATES]->(c)-[:CANONICAL_PROGRAM]->(p:Program)
             MERGE (f)-[r:IMPLICATES_PROGRAM]->(p)
             ON CREATE SET r.effect_status = i.effect_status""").consume()
    print(f"programs={len(PROGRAMS)}  member_edges={len(mem)}  concept_names={len(names)}  canonical_map_rows={len(mapping)}")
drv.close()
