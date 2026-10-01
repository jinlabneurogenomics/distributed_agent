# Life-Science-Research Skills Catalog

Each entry below is a private skill staged in this directory.
Read the full instructions by `cat <skill-dir>/SKILL.md` before invoking,
and run any helper scripts via the shell tool (`python <skill-dir>/scripts/...`).

## alphafold-skill
- **Path:** `alphafold-skill/`
- **Description:** Submit compact AlphaFold Protein Structure Database API requests for prediction, UniProt summary, sequence summary, and annotation lookups. Use when a user wants AlphaFold metadata or concise structure summaries

## bgee-skill
- **Path:** `bgee-skill/`
- **Description:** Submit compact Bgee SPARQL requests for healthy wild-type expression metadata and ontology-aware lookup patterns. Use when a user wants concise Bgee summaries; save raw results only on request.

## bindingdb-skill
- **Path:** `bindingdb-skill/`
- **Description:** Submit compact BindingDB REST API requests for ligand-target binding lookups by PDB, UniProt, or similarity search. Use when a user wants concise BindingDB summaries; save raw payloads only on request.

## biobankjapan-phewas-skill
- **Path:** `biobankjapan-phewas-skill/`
- **Description:** Fetch compact BioBank Japan PheWAS summaries for single variants by accepting rsID, GRCh38, or GRCh37 input and resolving to the required GRCh37 query. Use when a user wants concise BBJ association results for one variant

## biorxiv-skill
- **Path:** `biorxiv-skill/`
- **Description:** Submit compact bioRxiv and medRxiv API requests for details, publication-linkage, and DOI lookups. Use when a user wants concise preprint metadata summaries

## biostudies-arrayexpress-skill
- **Path:** `biostudies-arrayexpress-skill/`
- **Description:** Submit compact BioStudies and ArrayExpress API requests for free-text search and accession-based study retrieval. Use when a user wants concise BioStudies summaries

## cbioportal-skill
- **Path:** `cbioportal-skill/`
- **Description:** Submit compact cBioPortal API requests for studies, molecular profiles, mutations, clinical data, and samples. Use when a user wants concise cBioPortal summaries

## cellxgene-skill
- **Path:** `cellxgene-skill/`
- **Description:** Submit compact CELLxGENE Discover API requests for public collection and dataset metadata. Use when a user wants concise single-cell collection summaries

## chebi-skill
- **Path:** `chebi-skill/`
- **Description:** Submit compact ChEBI 2.0 API requests for chemical search, compound lookup, ontology traversal, and structure metadata. Use when a user wants concise ChEBI summaries

## chembl-skill
- **Path:** `chembl-skill/`
- **Description:** Submit compact ChEMBL API requests for activity, molecule, target, mechanism, and text-search endpoints. Use when a user wants concise ChEMBL summaries

## civic-skill
- **Path:** `civic-skill/`
- **Description:** Submit compact CIViC GraphQL requests for cancer variant interpretation schema inspection and targeted evidence retrieval. Use when a user wants concise CIViC summaries

## clinicaltrials-skill
- **Path:** `clinicaltrials-skill/`
- **Description:** Submit compact ClinicalTrials.gov API v2 requests for study search, metadata, enums, search areas, and field statistics. Use when a user wants concise ClinicalTrials.gov summaries

## clinvar-variation-skill
- **Path:** `clinvar-variation-skill/`
- **Description:** Submit compact ClinVar Clinical Tables and NCBI Variation requests for search, VCV, RCV, SCV, and RefSNP lookups. Use when a user wants variant-level summaries or identifier mapping

## efo-ontology-skill
- **Path:** `efo-ontology-skill/`
- **Description:** Submit compact EFO OLS4 requests for search, term lookup, children, and descendants. Use when a user wants concise EFO resolution or ontology-expansion summaries

## encode-skill
- **Path:** `encode-skill/`
- **Description:** Submit compact ENCODE REST API requests for object lookups, portal-style search, and metadata retrieval. Use when a user wants concise ENCODE summaries

## ensembl-skill
- **Path:** `ensembl-skill/`
- **Description:** Submit compact Ensembl REST API requests for lookup, overlap, cross-reference, and variation endpoints. Use when a user wants concise Ensembl summaries

## epigraphdb-skill
- **Path:** `epigraphdb-skill/`
- **Description:** Submit compact EpiGraphDB API requests for ontology, literature, MR, gene-drug, and support-path evidence. Use when a user wants concise EpiGraphDB summaries

## eqtl-catalogue-skill
- **Path:** `eqtl-catalogue-skill/`
- **Description:** Submit compact eQTL Catalogue API requests for association retrieval and documented metadata endpoints. Use when a user wants concise public eQTL Catalogue summaries

## eva-skill
- **Path:** `eva-skill/`
- **Description:** Submit compact EVA REST requests for species metadata and archived variant lookups. Use when a user wants concise European Variation Archive summaries

## finngen-phewas-skill
- **Path:** `finngen-phewas-skill/`
- **Description:** Fetch compact FinnGen PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query. Use when a user wants concise FinnGen association results for one variant

## genebass-gene-burden-skill
- **Path:** `genebass-gene-burden-skill/`
- **Description:** Submit compact Genebass gene burden requests for one Ensembl gene ID and one burden set. Use when a user wants concise Genebass PheWAS summaries

## gnomad-graphql-skill
- **Path:** `gnomad-graphql-skill/`
- **Description:** Submit compact gnomAD GraphQL requests for frequency, gene constraint, and variant context queries. Use when a user wants concise gnomAD summaries

## gtex-eqtl-skill
- **Path:** `gtex-eqtl-skill/`
- **Description:** Fetch GTEx single-tissue eQTL associations from one variant input by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query for the GTEx v2 API. Use when a user wants eQTL associations returned as JSON.

## gwas-catalog-skill
- **Path:** `gwas-catalog-skill/`
- **Description:** Submit compact GWAS Catalog REST API v2 requests for studies, associations, SNPs, EFO traits, genes, publications, loci, and metadata. Use when a user wants concise GWAS Catalog summaries

## hmdb-skill
- **Path:** `hmdb-skill/`
- **Description:** Submit compact HMDB search requests for metabolites, proteins, diseases, and pathways. Use when a user wants concise HMDB summaries

## human-protein-atlas-skill
- **Path:** `human-protein-atlas-skill/`
- **Description:** Submit compact Human Protein Atlas requests for gene JSON, search downloads, and page-level tissue or cell-line lookups. Use when a user wants concise Human Protein Atlas summaries; save raw JSON or HTML only on request.

## ipd-skill
- **Path:** `ipd-skill/`
- **Description:** Submit compact IPD REST requests for HLA allele and cell-level metadata using the public IPD query API. Use when a user wants concise IPD summaries; save raw JSON or text only on request.

## locus-to-gene-mapper-skill
- **Path:** `locus-to-gene-mapper-skill/`
- **Description:** Map GWAS loci to ranked candidate genes using a deterministic multi-skill chain (EFO -> GWAS -> coordinates -> Open Targets L2G/coloc -> eQTL -> burden/coding context), with reproducible tables and optional figures. Use when a user provides a trait/EFO term and/or lead variants and needs locus-to-gene prioritization for downstream biology decisions.

## metabolights-skill
- **Path:** `metabolights-skill/`
- **Description:** Submit compact MetaboLights requests for study discovery and study-level metabolomics metadata. Use when a user wants concise MetaboLights summaries

## mgnify-skill
- **Path:** `mgnify-skill/`
- **Description:** Submit compact MGnify API requests for microbiome studies, samples, and biome metadata. Use when a user wants concise MGnify summaries

## ncbi-blast-skill
- **Path:** `ncbi-blast-skill/`
- **Description:** Submit, poll, and summarize NCBI BLAST Common URL API jobs (Blast.cgi) for nucleotide or protein sequences. Use when a user wants RID status, BLAST results, or compact top-hit summaries; fetch raw Text/JSON2 only on request.

## ncbi-clinicaltables-skill
- **Path:** `ncbi-clinicaltables-skill/`
- **Description:** Submit compact Clinical Tables NCBI Gene requests for human gene lookup, pagination, and field selection. Use when a user wants concise autocomplete-style human gene search results

## ncbi-datasets-skill
- **Path:** `ncbi-datasets-skill/`
- **Description:** Submit compact NCBI Datasets v2 requests for assembly, genome, taxonomy, and related metadata endpoints. Use when a user wants concise NCBI Datasets summaries; save raw JSON or text only on request.

## ncbi-entrez-skill
- **Path:** `ncbi-entrez-skill/`
- **Description:** Submit compact NCBI Entrez E-Utilities requests for PubMed, Gene, Protein, Nucleotide, PMC metadata, and GEO metadata workflows. Use when a user wants concise Entrez search, fetch, summary, or link results; save raw JSON or XML only on request.

## ncbi-pmc-skill
- **Path:** `ncbi-pmc-skill/`
- **Description:** Submit compact NCBI PMC Open Access requests for article/file availability metadata. Use when a user wants concise PMC Open Access summaries; save raw XML only on request.

## opentargets-skill
- **Path:** `opentargets-skill/`
- **Description:** Submit compact Open Targets Platform GraphQL requests for target, disease, drug, variant, study, and search data, including associated-disease datasource heatmap matrices. Use when a user wants concise Open Targets summaries or per-datasource evidence context

## pharmgkb-skill
- **Path:** `pharmgkb-skill/`
- **Description:** Submit compact PharmGKB API requests for genes, variants, clinical annotations, dosing guidelines, and search. Use when a user wants concise PharmGKB summaries

## pride-skill
- **Path:** `pride-skill/`
- **Description:** Submit compact PRIDE Archive API requests for proteomics project discovery and project-level metadata. Use when a user wants concise PRIDE summaries

## proteomexchange-skill
- **Path:** `proteomexchange-skill/`
- **Description:** Submit compact ProteomeXchange PROXI requests for datasets, libraries, peptidoforms, proteins, PSMs, spectra, and USI examples. Use when a user wants concise PROXI summaries

## pubchem-pug-skill
- **Path:** `pubchem-pug-skill/`
- **Description:** Submit compact PubChem PUG REST requests for compound properties, descriptions, assay summaries, and substance metadata. Use when a user wants concise PubChem summaries

## quickgo-skill
- **Path:** `quickgo-skill/`
- **Description:** Submit compact QuickGO requests for GO terms, annotations, and ontology traversal. Use when a user wants concise QuickGO summaries

## rcsb-pdb-skill
- **Path:** `rcsb-pdb-skill/`
- **Description:** Submit compact RCSB PDB requests for core metadata, Search API queries, and FASTA downloads. Use when a user wants concise RCSB summaries; save raw JSON or FASTA only on request.

## reactome-skill
- **Path:** `reactome-skill/`
- **Description:** Submit compact Reactome ContentService requests for pathway, event, participant, search, and diagram-related data. Use when a user wants concise Reactome summaries

## research-router-skill
- **Path:** `research-router-skill/`
- **Description:** Route broad or ambiguous life-sciences research requests to the right skills, normalize core entities, optionally parallelize independent evidence gathering with subagents when available, and synthesize a concise evidence-backed answer. Use when a user asks a general life-sciences question that could span multiple sources or analysis types.

## rhea-skill
- **Path:** `rhea-skill/`
- **Description:** Submit compact Rhea reaction search requests for biochemical reactions and reaction IDs. Use when a user wants concise Rhea summaries

## rnacentral-skill
- **Path:** `rnacentral-skill/`
- **Description:** Submit compact RNAcentral API requests for RNA entry browsing, single-entry lookup, and cross-reference retrieval. Use when a user wants concise RNAcentral summaries

## string-skill
- **Path:** `string-skill/`
- **Description:** Submit compact STRING API requests for network, interaction partner, and enrichment endpoints. Use when a user wants concise STRING summaries

## tpmi-phewas-skill
- **Path:** `tpmi-phewas-skill/`
- **Description:** Fetch compact TPMI PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query. Use when a user wants concise TPMI association results for one variant

## ukb-topmed-phewas-skill
- **Path:** `ukb-topmed-phewas-skill/`
- **Description:** Fetch compact UKB-TOPMed PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query. Use when a user wants concise UKB-TOPMed association results for one variant

## uniprot-skill
- **Path:** `uniprot-skill/`
- **Description:** Submit compact UniProt REST API requests for UniProtKB, UniRef, UniParc, and FASTA stream endpoints. Use when a user wants concise UniProt summaries; save raw JSON or FASTA only on request.
