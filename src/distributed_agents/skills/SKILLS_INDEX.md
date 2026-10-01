# DistributedAgents Skills Catalog

Each entry below is a private skill staged in this directory.
Read the full instructions by `cat <skill-dir>/SKILL.md` before invoking,
and run any helper scripts via the shell tool (`python <skill-dir>/scripts/...`).

## alphafold-skill
- **Path:** `life-sciences/alphafold-skill/`
- **Description:** Submit compact AlphaFold Protein Structure Database API requests for prediction, UniProt summary, sequence summary, and annotation lookups. Use when a user wants AlphaFold metadata or concise structure summaries

## bgee-skill
- **Path:** `life-sciences/bgee-skill/`
- **Description:** Submit compact Bgee SPARQL requests for healthy wild-type expression metadata and ontology-aware lookup patterns. Use when a user wants concise Bgee summaries; save raw results only on request.

## bindingdb-skill
- **Path:** `life-sciences/bindingdb-skill/`
- **Description:** Submit compact BindingDB REST API requests for ligand-target binding lookups by PDB, UniProt, or similarity search. Use when a user wants concise BindingDB summaries; save raw payloads only on request.

## biobankjapan-phewas-skill
- **Path:** `life-sciences/biobankjapan-phewas-skill/`
- **Description:** Fetch compact BioBank Japan PheWAS summaries for single variants by accepting rsID, GRCh38, or GRCh37 input and resolving to the required GRCh37 query. Use when a user wants concise BBJ association results for one variant

## biorxiv-skill
- **Path:** `life-sciences/biorxiv-skill/`
- **Description:** Submit compact bioRxiv and medRxiv API requests for details, publication-linkage, and DOI lookups. Use when a user wants concise preprint metadata summaries

## biostudies-arrayexpress-skill
- **Path:** `life-sciences/biostudies-arrayexpress-skill/`
- **Description:** Submit compact BioStudies and ArrayExpress API requests for free-text search and accession-based study retrieval. Use when a user wants concise BioStudies summaries

## cbioportal-skill
- **Path:** `life-sciences/cbioportal-skill/`
- **Description:** Submit compact cBioPortal API requests for studies, molecular profiles, mutations, clinical data, and samples. Use when a user wants concise cBioPortal summaries

## cellxgene-skill
- **Path:** `life-sciences/cellxgene-skill/`
- **Description:** Submit compact CELLxGENE Discover API requests for public collection and dataset metadata. Use when a user wants concise single-cell collection summaries

## chebi-skill
- **Path:** `life-sciences/chebi-skill/`
- **Description:** Submit compact ChEBI 2.0 API requests for chemical search, compound lookup, ontology traversal, and structure metadata. Use when a user wants concise ChEBI summaries

## chembl-skill
- **Path:** `life-sciences/chembl-skill/`
- **Description:** Submit compact ChEMBL API requests for activity, molecule, target, mechanism, and text-search endpoints. Use when a user wants concise ChEMBL summaries

## civic-skill
- **Path:** `life-sciences/civic-skill/`
- **Description:** Submit compact CIViC GraphQL requests for cancer variant interpretation schema inspection and targeted evidence retrieval. Use when a user wants concise CIViC summaries

## clinicaltrials-skill
- **Path:** `life-sciences/clinicaltrials-skill/`
- **Description:** Submit compact ClinicalTrials.gov API v2 requests for study search, metadata, enums, search areas, and field statistics. Use when a user wants concise ClinicalTrials.gov summaries

## clinvar-variation-skill
- **Path:** `life-sciences/clinvar-variation-skill/`
- **Description:** Submit compact ClinVar Clinical Tables and NCBI Variation requests for search, VCV, RCV, SCV, and RefSNP lookups. Use when a user wants variant-level summaries or identifier mapping

## efo-ontology-skill
- **Path:** `life-sciences/efo-ontology-skill/`
- **Description:** Submit compact EFO OLS4 requests for search, term lookup, children, and descendants. Use when a user wants concise EFO resolution or ontology-expansion summaries

## encode-skill
- **Path:** `life-sciences/encode-skill/`
- **Description:** Submit compact ENCODE REST API requests for object lookups, portal-style search, and metadata retrieval. Use when a user wants concise ENCODE summaries

## ensembl-skill
- **Path:** `life-sciences/ensembl-skill/`
- **Description:** Submit compact Ensembl REST API requests for lookup, overlap, cross-reference, and variation endpoints. Use when a user wants concise Ensembl summaries

## epigraphdb-skill
- **Path:** `life-sciences/epigraphdb-skill/`
- **Description:** Submit compact EpiGraphDB API requests for ontology, literature, MR, gene-drug, and support-path evidence. Use when a user wants concise EpiGraphDB summaries

## eqtl-catalogue-skill
- **Path:** `life-sciences/eqtl-catalogue-skill/`
- **Description:** Submit compact eQTL Catalogue API requests for association retrieval and documented metadata endpoints. Use when a user wants concise public eQTL Catalogue summaries

## eva-skill
- **Path:** `life-sciences/eva-skill/`
- **Description:** Submit compact EVA REST requests for species metadata and archived variant lookups. Use when a user wants concise European Variation Archive summaries

## finngen-phewas-skill
- **Path:** `life-sciences/finngen-phewas-skill/`
- **Description:** Fetch compact FinnGen PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query. Use when a user wants concise FinnGen association results for one variant

## genebass-gene-burden-skill
- **Path:** `life-sciences/genebass-gene-burden-skill/`
- **Description:** Submit compact Genebass gene burden requests for one Ensembl gene ID and one burden set. Use when a user wants concise Genebass PheWAS summaries

## gnomad-graphql-skill
- **Path:** `life-sciences/gnomad-graphql-skill/`
- **Description:** Submit compact gnomAD GraphQL requests for frequency, gene constraint, and variant context queries. Use when a user wants concise gnomAD summaries

## gtex-eqtl-skill
- **Path:** `life-sciences/gtex-eqtl-skill/`
- **Description:** Fetch GTEx single-tissue eQTL associations from one variant input by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query for the GTEx v2 API. Use when a user wants eQTL associations returned as JSON.

## gwas-catalog-skill
- **Path:** `life-sciences/gwas-catalog-skill/`
- **Description:** Submit compact GWAS Catalog REST API v2 requests for studies, associations, SNPs, EFO traits, genes, publications, loci, and metadata. Use when a user wants concise GWAS Catalog summaries

## hmdb-skill
- **Path:** `life-sciences/hmdb-skill/`
- **Description:** Submit compact HMDB search requests for metabolites, proteins, diseases, and pathways. Use when a user wants concise HMDB summaries

## human-protein-atlas-skill
- **Path:** `life-sciences/human-protein-atlas-skill/`
- **Description:** Submit compact Human Protein Atlas requests for gene JSON, search downloads, and page-level tissue or cell-line lookups. Use when a user wants concise Human Protein Atlas summaries; save raw JSON or HTML only on request.

## ipd-skill
- **Path:** `life-sciences/ipd-skill/`
- **Description:** Submit compact IPD REST requests for HLA allele and cell-level metadata using the public IPD query API. Use when a user wants concise IPD summaries; save raw JSON or text only on request.

## locus-to-gene-mapper-skill
- **Path:** `life-sciences/locus-to-gene-mapper-skill/`
- **Description:** Map GWAS loci to ranked candidate genes using a deterministic multi-skill chain (EFO -> GWAS -> coordinates -> Open Targets L2G/coloc -> eQTL -> burden/coding context), with reproducible tables and optional figures. Use when a user provides a trait/EFO term and/or lead variants and needs locus-to-gene prioritization for downstream biology decisions.

## metabolights-skill
- **Path:** `life-sciences/metabolights-skill/`
- **Description:** Submit compact MetaboLights requests for study discovery and study-level metabolomics metadata. Use when a user wants concise MetaboLights summaries

## mgnify-skill
- **Path:** `life-sciences/mgnify-skill/`
- **Description:** Submit compact MGnify API requests for microbiome studies, samples, and biome metadata. Use when a user wants concise MGnify summaries

## ncbi-blast-skill
- **Path:** `life-sciences/ncbi-blast-skill/`
- **Description:** Submit, poll, and summarize NCBI BLAST Common URL API jobs (Blast.cgi) for nucleotide or protein sequences. Use when a user wants RID status, BLAST results, or compact top-hit summaries; fetch raw Text/JSON2 only on request.

## ncbi-clinicaltables-skill
- **Path:** `life-sciences/ncbi-clinicaltables-skill/`
- **Description:** Submit compact Clinical Tables NCBI Gene requests for human gene lookup, pagination, and field selection. Use when a user wants concise autocomplete-style human gene search results

## ncbi-datasets-skill
- **Path:** `life-sciences/ncbi-datasets-skill/`
- **Description:** Submit compact NCBI Datasets v2 requests for assembly, genome, taxonomy, and related metadata endpoints. Use when a user wants concise NCBI Datasets summaries; save raw JSON or text only on request.

## ncbi-entrez-skill
- **Path:** `life-sciences/ncbi-entrez-skill/`
- **Description:** Submit compact NCBI Entrez E-Utilities requests for PubMed, Gene, Protein, Nucleotide, PMC metadata, and GEO metadata workflows. Use when a user wants concise Entrez search, fetch, summary, or link results; save raw JSON or XML only on request.

## ncbi-pmc-skill
- **Path:** `life-sciences/ncbi-pmc-skill/`
- **Description:** Submit compact NCBI PMC Open Access requests for article/file availability metadata. Use when a user wants concise PMC Open Access summaries; save raw XML only on request.

## opentargets-skill
- **Path:** `life-sciences/opentargets-skill/`
- **Description:** Submit compact Open Targets Platform GraphQL requests for target, disease, drug, variant, study, and search data, including associated-disease datasource heatmap matrices. Use when a user wants concise Open Targets summaries or per-datasource evidence context

## pharmgkb-skill
- **Path:** `life-sciences/pharmgkb-skill/`
- **Description:** Submit compact PharmGKB API requests for genes, variants, clinical annotations, dosing guidelines, and search. Use when a user wants concise PharmGKB summaries

## pride-skill
- **Path:** `life-sciences/pride-skill/`
- **Description:** Submit compact PRIDE Archive API requests for proteomics project discovery and project-level metadata. Use when a user wants concise PRIDE summaries

## proteomexchange-skill
- **Path:** `life-sciences/proteomexchange-skill/`
- **Description:** Submit compact ProteomeXchange PROXI requests for datasets, libraries, peptidoforms, proteins, PSMs, spectra, and USI examples. Use when a user wants concise PROXI summaries

## pubchem-pug-skill
- **Path:** `life-sciences/pubchem-pug-skill/`
- **Description:** Submit compact PubChem PUG REST requests for compound properties, descriptions, assay summaries, and substance metadata. Use when a user wants concise PubChem summaries

## quickgo-skill
- **Path:** `life-sciences/quickgo-skill/`
- **Description:** Submit compact QuickGO requests for GO terms, annotations, and ontology traversal. Use when a user wants concise QuickGO summaries

## rcsb-pdb-skill
- **Path:** `life-sciences/rcsb-pdb-skill/`
- **Description:** Submit compact RCSB PDB requests for core metadata, Search API queries, and FASTA downloads. Use when a user wants concise RCSB summaries; save raw JSON or FASTA only on request.

## reactome-skill
- **Path:** `life-sciences/reactome-skill/`
- **Description:** Submit compact Reactome ContentService requests for pathway, event, participant, search, and diagram-related data. Use when a user wants concise Reactome summaries

## rhea-skill
- **Path:** `life-sciences/rhea-skill/`
- **Description:** Submit compact Rhea reaction search requests for biochemical reactions and reaction IDs. Use when a user wants concise Rhea summaries

## rnacentral-skill
- **Path:** `life-sciences/rnacentral-skill/`
- **Description:** Submit compact RNAcentral API requests for RNA entry browsing, single-entry lookup, and cross-reference retrieval. Use when a user wants concise RNAcentral summaries

## string-skill
- **Path:** `life-sciences/string-skill/`
- **Description:** Submit compact STRING API requests for network, interaction partner, and enrichment endpoints. Use when a user wants concise STRING summaries

## tpmi-phewas-skill
- **Path:** `life-sciences/tpmi-phewas-skill/`
- **Description:** Fetch compact TPMI PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query. Use when a user wants concise TPMI association results for one variant

## ukb-topmed-phewas-skill
- **Path:** `life-sciences/ukb-topmed-phewas-skill/`
- **Description:** Fetch compact UKB-TOPMed PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query. Use when a user wants concise UKB-TOPMed association results for one variant

## uniprot-skill
- **Path:** `life-sciences/uniprot-skill/`
- **Description:** Submit compact UniProt REST API requests for UniProtKB, UniRef, UniParc, and FASTA stream endpoints. Use when a user wants concise UniProt summaries; save raw JSON or FASTA only on request.

## adaptive-query-skill
- **Path:** `runtime/adaptive-query-skill/`
- **Description:** Execute compact adaptive Perturb-seq analyses from truthful run-local capabilities; use cached quantitative feature calibration only for predictive rankings with explicit ranked or partial-ranked supervision.

## dataset-orchestrator-skill
- **Path:** `runtime/dataset-orchestrator-skill/`
- **Description:** Structure PerturbAI dataset questions from first principles, route selected-release corpus capabilities when available, resolve missing resource capabilities, and validate grounded execution before computation.

## exhaustive-corpus-sweep-skill
- **Path:** `runtime/exhaustive-corpus-sweep-skill/`
- **Description:** Exhaustively review an enumerable corpus when the task explicitly requires full-corpus semantic inspection or complete per-unit accounting. Use bounded reader subagents with deterministic partitions and fail-closed reconciliation; do not use for ordinary searches, samples, top-k retrieval, or deterministic scans that one process can complete directly.

## gene-annotation-skill
- **Path:** `dataset/gene-annotation-skill/`
- **Description:** Provide deterministic gene-to-set membership over the PerturbAI closed gene universe. Use for curated expected-similar groups such as paralog families, complexes, pathways, and functional classes; compare those priors with observed findings for divergence, non-interchangeability, specificity, or deterministic attribute lookup.

## biokg-recall-skill
- **Path:** `../corpus/releases/legacy_reports_v1/skills/biokg-recall-skill/`
- **Description:** Plan and run flexible Cypher retrieval over the BioKG Neo4j graph of PerturbAI narrative findings. Use for structured graph recall such as convergence across target families, divergence within a family or complex, dominant pathways, cell-type landscapes, target-specific evidence, or effect-status-aware support. The reasoning agent writes task-specific Cypher; this skill supplies the schema, precision/recall controls, access, and worked patterns.

## findings-analysis-skill
- **Path:** `../corpus/releases/legacy_reports_v1/skills/findings-analysis-skill/`
- **Description:** Operate on the complete PerturbAI narrative-findings ledger as a database. Use deterministic code to filter, score, rank, aggregate, cross-tab, or enumerate all 11,346 findings; apply semantic consequence scoring for biological-interest tasks and metadata rubrics for structured analysis. Use the findings-ledger skill when a task instead needs targeted prose retrieval and full-report reading.

## findings-bm25-skill
- **Path:** `../corpus/releases/legacy_reports_v1/skills/findings-bm25-skill/`
- **Description:** Retrieve relevance-ranked legacy PerturbAI Findings with deterministic BM25 over each canonical Finding's summary and why-it-matters text. Use for concept-first or paraphrased corpus discovery before resolving the returned Finding evidence and references; do not treat retrieval score as biological evidence or a final rank.

## findings-ledger-skill
- **Path:** `../corpus/releases/legacy_reports_v1/skills/findings-ledger-skill/`
- **Description:** Retrieve over the PerturbAI narrative-findings ledger, the flat atomic one-row-per-finding table underlying BioKG. Use to filter and read interpreted per-perturbation findings by finding type, gene, cell type, or prose, then open full reports with measurements, evidence, caveats, and citations for material candidates.

## relational-candidate-skill
- **Path:** `../corpus/releases/legacy_reports_v1/skills/relational-candidate-skill/`
- **Description:** Retrieve an unranked typed semantic map from a supplied partial ranking, positive set, exemplar list, or other visible Perturb-seq anchors. Use when a task asks for missing candidates, analogs, comparators, convergence partners, or completion of a partly revealed result and the same-experiment Findings ledger can connect anchors to other assayed targets.
