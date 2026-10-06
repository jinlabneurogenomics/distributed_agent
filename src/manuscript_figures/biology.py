"""Prepare report-linked biological examples and source-study comparisons."""
import json
from collections import Counter, defaultdict
from pathlib import Path
import re
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from scipy.stats import pearsonr
from scipy.spatial.distance import cosine
from bs4 import BeautifulSoup
from .paths import INPUTS, RUNS, TABLES

DEG = INPUTS / "biology/differential_expression.parquet"

def _save(frame, name):
    path = TABLES / "biology" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)

def prepare_chromatin_examples():
    GROUP = '151 TH Prkcd Grin2c Glut'
    ORDER = ['Smarcb1', 'Smarcc2', 'Arid2', 'Arid1a']
    COLORS = {'Smarcb1': '#5B6FB5', 'Smarcc2': '#59A7A0', 'Arid2': '#E39A45', 'Arid1a': '#C76B82'}
    report_modules = {'Smarcb1': {'Mature synaptic identity / transmission': ['Prkcd', 'Grin2c', 'Grm1', 'Gabra4', 'Begain', 'Shank1', 'Lrrtm1', 'Slc6a7', 'Atp1b2', 'Kcnk4'], 'Dendritic / NMDA-linked signaling': ['Tiam1']}, 'Smarcc2': {'Synapse / cell junction': ['Nlgn2', 'Agrn', 'Lrrtm1', 'L1cam', 'Begain'], 'Membrane excitability / ion handling': ['Cnih3', 'Cacnb2', 'Hcn4', 'P2rx4', 'Asic2', 'Atp2b1'], 'Neurite / synapse organization': ['Tiam1', 'Prkcd'], 'Compensatory synaptic remodeling': ['Grin3a', 'Grm5']}, 'Arid2': {'Membrane signaling / excitability': ['Kcnj9', 'Gpr4', 'Gpr153', 'Pde4a', 'Map2k2', 'Prkcd'], 'Synaptic handling / vesicle trafficking': ['Stxbp2', 'Nsg1', 'Gria2', 'Ece2']}, 'Arid1a': {'Synaptic / PSD': ['Begain', 'Lrrc7', 'Clstn2', 'Mpp2'], 'Excitability / signaling': ['Kcnq2', 'Prkcb', 'Rasa4', 'Ppp2r5d', 'Adora1']}}
    rows = []
    for perturbation, modules in report_modules.items():
        for module, genes in modules.items():
            rows += [(perturbation, g, module) for g in genes]
    membership = pd.DataFrame(rows, columns=['perturbation', 'gene', 'report_module']).drop_duplicates(['perturbation', 'gene'])
    tab = pq.read_table(DEG, columns=['names', 'gene_target', 'logfoldchanges', 'pvals_adj'], filters=[('group_name', '=', GROUP), ('gene_target', 'in', ORDER)])
    raw = tab.to_pandas().rename(columns={'names': 'gene', 'gene_target': 'perturbation', 'logfoldchanges': 'logFC', 'pvals_adj': 'FDR'})
    expanded = membership.merge(raw, on=['perturbation', 'gene'], how='left', validate='one_to_one')
    assert expanded.logFC.notna().all()
    expanded.groupby('perturbation').size().reindex(ORDER)
    _save(expanded, 'chromatin_synaptic_genes.csv')

def prepare_grin_comparison():
    GROUP = '007 L2-3 IT CTX Glut'
    tab = pq.read_table(DEG, columns=['names', 'gene_target', 'scores', 'logfoldchanges', 'pvals_adj'], filters=[('group_name', '=', GROUP), ('gene_target', 'in', ['Grin2a', 'Grin2b'])])
    raw = tab.to_pandas()
    b = raw[raw.gene_target.eq('Grin2b') & raw.pvals_adj.lt(0.05) & raw.logfoldchanges.abs().ge(0.25)][['names', 'logfoldchanges', 'pvals_adj']].copy()
    assert len(b) == 47, f'Expected 47 genes, found {len(b)}'
    b.columns = ['gene', 'Grin2b_logFC', 'Grin2b_FDR']
    a = raw[raw.gene_target.eq('Grin2a')][['names', 'logfoldchanges', 'pvals_adj']].copy()
    a.columns = ['gene', 'Grin2a_logFC', 'Grin2a_FDR']
    plot_df = b.merge(a, on='gene', validate='one_to_one')
    r, p = pearsonr(plot_df.Grin2a_logFC, plot_df.Grin2b_logFC)
    print(f'n={len(plot_df)}; Pearson r={r:.8f}; p={p:.3g}')
    assert np.isclose(r, -0.63, atol=0.005)
    pathway_genes = {'Activity / plasticity': {'Vgf', 'Nr4a1', 'Bdnf', 'Npas4', 'Nptx2', 'Ptgs2', 'Arc', 'Egr1'}, 'Vesicle priming / docking': {'Unc13a', 'Unc13b', 'Rims1', 'Erc2', 'Rph3a', 'Tspoap1'}, 'Synapse / postsynapse': {'Kcnv1', 'Sorcs3', 'Dlgap2', 'Nptxr', 'Cabp1'}, 'Structural remodeling / membrane': {'Stmn1', 'Celsr2', 'Adamts2', 'Zdhhc2'}}

    def assign_pathway(gene):
        for pathway, genes in pathway_genes.items():
            if gene in genes:
                return pathway
        return 'Other significant DEG'
    plot_df['pathway'] = plot_df.gene.map(assign_pathway)
    plot_df.groupby('pathway').size()
    _save(plot_df, 'grin2a_grin2b_comparison.csv')
    _save(pd.DataFrame([{'r': r, 'p': p, 'n': len(plot_df)}]), 'grin2a_grin2b_statistics.csv')

def prepare_proteostasis_summary():
    TARGETS = ['Psmb4', 'Pomp', 'Hspa5', 'Hspa8', 'Hspa9', 'Lonp1', 'Opa1', 'Dnm1l']
    genes = ['Atp1a3', 'Gria2', 'Syt1', 'Scn1a', 'Cx3cl1', 'Gabrb2', 'Tspan7', 'Atp1b1', 'Grin2b']
    tab = pq.read_table(DEG, columns=['names', 'gene_target', 'group_name', 'logfoldchanges', 'pvals_adj'], filters=[('gene_target', 'in', TARGETS), ('names', 'in', genes)])
    raw = tab.to_pandas().rename(columns={'names': 'gene', 'gene_target': 'perturbation', 'logfoldchanges': 'logFC', 'pvals_adj': 'FDR'})
    summary = raw.groupby(['perturbation', 'gene']).agg(median_logFC=('logFC', 'median'), fdr_groups=('FDR', lambda x: int((x < 0.05).sum())), tested_groups=('group_name', 'nunique')).reset_index()
    _save(summary, 'proteostasis_gene_summary.csv')

def prepare_remodeling_examples():
    GROUP = '151 TH Prkcd Grin2c Glut'
    ORDER = ['Smarcb1', 'Smarcc2']
    COLORS = {'Smarcb1': '#7B68B5', 'Smarcc2': '#4FA39B'}
    modules = {'Smarcb1': {'Neuronal remodeling / re-specification': ['Myt1', 'Stmn1', 'Clstn1', 'Clstn2', 'Plxna2', 'Fez2', 'Syt4', 'Nexn'], 'Stress / DNA-damage / quality control': ['Atm', 'Prkn', 'Gss', 'Hsf2', 'Abcc1', 'Ubc'], 'Alternative neuromodulatory state': ['Grm5', 'Pth2r', 'Tafa1', 'Kcnj9']}, 'Smarcc2': {'Compensatory neuronal remodeling': ['Pth2r', 'Tafa1', 'Grin3a', 'Syt4', 'Rims4', 'Grm5']}}
    rows = []
    for perturbation, mm in modules.items():
        for module, genes in mm.items():
            rows += [(perturbation, g, module) for g in genes]
    membership = pd.DataFrame(rows, columns=['perturbation', 'gene', 'report_module']).drop_duplicates(['perturbation', 'gene'])
    tab = pq.read_table(DEG, columns=['names', 'gene_target', 'logfoldchanges', 'pvals_adj'], filters=[('group_name', '=', GROUP), ('gene_target', 'in', ORDER)])
    raw = tab.to_pandas().rename(columns={'names': 'gene', 'gene_target': 'perturbation', 'logfoldchanges': 'logFC', 'pvals_adj': 'FDR'})
    df = membership.merge(raw, on=['perturbation', 'gene'], how='left', validate='one_to_one')
    assert df.logFC.notna().all()
    df.groupby(['perturbation', 'report_module']).agg(n=('gene', 'size'), mean_logFC=('logFC', 'mean'))
    _save(df, 'chromatin_remodeling_genes.csv')

def prepare_tsc_comparison():
    groups = ['155 MB Glut', '151 TH Prkcd Grin2c Glut', '066 CNU-HYa HY GABA', '191 MB P MY GABA']
    short = ['155 MB', '151 TH', '066 HY', '191 MB']
    modules = {'Sterol / mevalonate': ['Insig1', 'Ldlr', 'Hmgcs1', 'Sqle', 'Cyp51', 'Msmo1', 'Dhcr7', 'Fdft1', 'Fdps', 'Nsdhl', 'Hmgcr', 'Mvk', 'Mvd'], 'Lysosome / endolysosome': ['Atp6v0b', 'Lamp2', 'Mcoln1', 'Clcn7', 'Gba', 'Neu1', 'Grn', 'Ctsa', 'Gns', 'Ctns', 'Cln3', 'Scpep1', 'Dpp7'], 'Neuronal / synaptic': ['App', 'Syp', 'Syt1', 'Rtn1', 'Clstn1', 'Serinc1', 'Atp2a2', 'Scg5', 'Vsnl1', 'Gabra1', 'Glrb', 'Lynx1', 'Rab3a']}
    colors = {'Sterol / mevalonate': '#D98B3A', 'Lysosome / endolysosome': '#39A08F', 'Neuronal / synaptic': '#3D78B8', 'Other Tsc2-significant DEG': '#C8C8C8'}
    raw = pq.read_table(DEG, columns=['names', 'gene_target', 'group_name', 'logfoldchanges', 'pvals_adj'], filters=[('group_name', 'in', groups), ('gene_target', 'in', ['Tsc1', 'Tsc2'])]).to_pandas()
    panels = {}
    stats = []
    for group, label in zip(groups, short):
        x = raw[raw.group_name.eq(group)]
        a = x[x.gene_target.eq('Tsc1')].set_index('names')[['logfoldchanges']].rename(columns={'logfoldchanges': 'Tsc1_logFC'})
        b = x[x.gene_target.eq('Tsc2')].set_index('names')[['logfoldchanges', 'pvals_adj']].rename(columns={'logfoldchanges': 'Tsc2_logFC', 'pvals_adj': 'Tsc2_FDR'})
        d = a.join(b, how='inner')
        d = d[d.Tsc2_FDR < 0.05].copy()
        d['module'] = 'Other Tsc2-significant DEG'
        for module, genes in modules.items():
            d.loc[d.index.isin(genes), 'module'] = module
        r = pearsonr(d.Tsc1_logFC, d.Tsc2_logFC).statistic
        stats.append((label, r, len(d)))
        panels[group] = d
    assert [round(x[1], 3) for x in stats] == [0.892, 0.888, 0.89, 0.907]
    df = panels['155 MB Glut']
    r = stats[0][1]
    _save(pd.concat([d.rename_axis('gene').reset_index().assign(cell_type=g) for g, d in panels.items()], ignore_index=True), 'tsc1_tsc2_comparison.csv')
    _save(pd.DataFrame(stats, columns=['cell_type_label', 'r', 'n']), 'tsc1_tsc2_statistics.csv')

def prepare_rab7_programs():
    targets = ['Rab7', 'Tsc1', 'Tsc2']
    lysosome = ['Atp6v0b', 'Atp6v1b2', 'Dpp7', 'Lamp2', 'Mcoln1', 'Grn', 'Neu1', 'Hexb', 'Ctsa']
    sterol = ['Insig1', 'Msmo1', 'Fdft1', 'Cyp51', 'Dhcr24', 'Sqle', 'Hmgcs1', 'Ldlr']
    genes = lysosome + sterol
    e010_genes = {'Atp6v0b', 'Dpp7', 'Lamp2', 'Insig1', 'Msmo1', 'Cpeb1', 'Grn'}
    groups = ['005 L4-5 IT CTX Glut', '066 CNU-HYa HY GABA', '110 CNU-HYa HY MM Glut', '151 TH Prkcd Grin2c Glut', '155 MB Glut', '191 MB P MY GABA']
    short = {'005 L4-5 IT CTX Glut': 'L4-5 IT CTX Glut', '066 CNU-HYa HY GABA': 'HY GABA', '110 CNU-HYa HY MM Glut': 'HY Glut', '151 TH Prkcd Grin2c Glut': 'TH Glut', '155 MB Glut': 'MB Glut', '191 MB P MY GABA': 'MB GABA'}
    parts = []
    for g in groups:
        parts.append(pq.read_table(DEG, columns=['names', 'gene_target', 'group_name', 'logfoldchanges', 'pvals_adj'], filters=[('group_name', '=', g), ('gene_target', 'in', targets), ('names', 'in', genes)]).to_pandas())
    d = pd.concat(parts, ignore_index=True)
    _save(d, 'rab7_tsc_expression.csv')

def prepare_wdr26_comparison():
    groups = ['066 CNU-HYa HY GABA', '110 CNU-HYa HY MM Glut', '145 MH-LH TH Glut', '151 TH Prkcd Grin2c Glut', '155 MB Glut', '191 MB P MY GABA', '308 CB GABA']
    parts = []
    for group in groups:
        parts.append(pq.read_table(DEG, columns=['names', 'gene_target', 'group_name', 'logfoldchanges', 'pvals_adj'], filters=[('group_name', '=', group), ('gene_target', 'in', ['Wdr26', 'Tsc1', 'Tsc2'])]).to_pandas())
    raw = pd.concat(parts, ignore_index=True)
    w = raw[raw.gene_target.eq('Wdr26') & (raw.pvals_adj < 0.1)].set_index(['group_name', 'names'])[['logfoldchanges']].rename(columns={'logfoldchanges': 'Wdr26_logFC'})

    def comparator(target):
        z = raw[raw.gene_target.eq(target)].set_index(['group_name', 'names'])[['logfoldchanges', 'pvals_adj']].reindex(w.index).rename(columns={'logfoldchanges': f'{target}_logFC', 'pvals_adj': f'{target}_FDR'})
        return w.join(z)
    t2 = comparator('Tsc2')
    t1 = comparator('Tsc1')
    restricted_cosine = 1 - cosine(t2.Wdr26_logFC, t2.Tsc2_logFC)
    for d, target in [(t2, 'Tsc2'), (t1, 'Tsc1')]:
        shared = d[f'{target}_FDR'] < 0.1
        d['overlap'] = 'Wdr26-significant only'
        d.loc[shared, 'overlap'] = 'Opposite-direction overlap'
        d.loc[shared & (d.Wdr26_logFC * d[f'{target}_logFC'] > 0), 'overlap'] = 'Same-direction overlap'
    counts = pd.DataFrame({'target': ['Tsc2', 'Tsc1'], 'same': [133, 138], 'opposite': [9, 27], 'total': [142, 165]})
    assert len(t2) == 3130 and round(restricted_cosine, 3) == 0.629
    assert [(t2.overlap == 'Same-direction overlap').sum(), (t2.overlap == 'Opposite-direction overlap').sum()] == [133, 9]
    assert [(t1.overlap == 'Same-direction overlap').sum(), (t1.overlap == 'Opposite-direction overlap').sum()] == [138, 27]
    _save(t2.reset_index(), 'wdr26_tsc2_comparison.csv')
    _save(t1.reset_index(), 'wdr26_tsc1_comparison.csv')
    _save(counts, 'wdr26_overlap_counts.csv')
    _save(pd.DataFrame([{'cosine': restricted_cosine, 'n': len(t2)}]), 'wdr26_statistics.csv')

def prepare_cerebellar_response():
    group = '308 CB GABA'
    targets = ['Tsc1', 'Tsc2']
    program = ['Shank3', 'Stxbp1', 'Cacna1d', 'Grm8', 'Cabp1', 'Slc8a3']
    d = pq.read_table(DEG, columns=['names', 'gene_target', 'group_name', 'logfoldchanges', 'pvals', 'pvals_adj', 'n_pert_matched', 'n_ctrl_matched'], filters=[('group_name', '=', group), ('gene_target', 'in', targets)]).to_pandas()
    d['minus_log10_fdr'] = -np.log10(d.pvals_adj.clip(lower=np.nextafter(0, 1)))
    d['fdr_sig'] = d.pvals_adj < 0.1
    assert d[(d.gene_target == 'Tsc1') & d.fdr_sig].shape[0] == 0
    assert d[(d.gene_target == 'Tsc2') & d.fdr_sig].shape[0] == 83
    _save(d, 'tsc_cerebellar_response.csv')

def prepare_report_similarities():
    values = json.loads((INPUTS / 'biology/report_similarity_values.json').read_text())
    NUMERIC_CELLS = values['7']
    numeric = pd.DataFrame(NUMERIC_CELLS, columns=['report', 'compared_target', 'reported_values', 'reported_context'])
    REPORTED_VALUES = values['15']
    TARGETS = ['Psmb4', 'Pomp', 'Hspa5', 'Hspa8', 'Hspa9', 'Lonp1', 'Opa1', 'Dnm1l']
    report_dir = RUNS / 'reports/html'
    html_text = {}
    for target in TARGETS:
        path = report_dir / f'{target.lower()}.html'
        assert path.exists(), path
        html_text[target] = ' '.join(BeautifulSoup(path.read_text(errors='replace'), 'html.parser').get_text(' ', strip=True).split())
    for row in numeric.itertuples(index=False):
        assert row.compared_target in html_text[row.report]
        for value in row.reported_values:
            variants = {str(value), f'{value:.3f}', f'{value:.2f}'}
            assert any((v in html_text[row.report] for v in variants)), (row.report, row.compared_target, value)

    values = pd.DataFrame(REPORTED_VALUES, columns=['report', 'compared_target', 'cell_type', 'similarity_r'])
    html_text = {}
    for report in values['report'].unique():
        path = report_dir / f'{report.lower()}.html'
        assert path.exists(), path
        html_text[report] = ' '.join(BeautifulSoup(path.read_text(errors='replace'), 'html.parser').get_text(' ', strip=True).split())
    for row in values.itertuples(index=False):
        assert row.compared_target in html_text[row.report]
        variants = {str(row.similarity_r), f'{row.similarity_r:.3f}', f'{row.similarity_r:.2f}'}
        assert any((v in html_text[row.report] for v in variants)), row
    (TABLES / 'biology/report_similarity_values.json').write_text(json.dumps({'7': NUMERIC_CELLS, '15': REPORTED_VALUES}, indent=2) + '\n')

def prepare_finding_breadth():


    CLAIM_PATH = INPUTS / "biology/july_claim_findings.csv"
    JULY_REPORTS_PATH = RUNS / "reports/july/reports.jsonl"

    claims = pd.read_csv(CLAIM_PATH, dtype=str)
    CLAIM_ORDER = ("2a", "2b", "2c", "2d", "3c", "4b", "4e", "5", "7", "1a", "1b", "8")
    EXPECTED_FLAGS = Counter({"M": 35, "R": 13, "P": 9, "D": 14})
    assert claims.columns.tolist() == [
        "headline_id", "paper_figure", "headline", "gene", "july_verdict", "july_finding_ids"
    ]
    assert len(claims) == 71
    assert claims[["headline_id", "gene"]].drop_duplicates().shape[0] == 71
    assert claims.gene.nunique() == 62
    assert tuple(claims.headline_id.drop_duplicates()) == CLAIM_ORDER
    assert Counter(claims.july_verdict) == EXPECTED_FLAGS

    needed_genes = set(claims.gene)
    reports = {}
    with JULY_REPORTS_PATH.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            gene = str(row.get("gene_target") or "").strip()
            if gene not in needed_genes:
                continue
            report = next(
                (
                    row.get(field)
                    for field in ("report", "final_report", "scientist_report")
                    if isinstance(row.get(field), str) and row[field].strip()
                ),
                None,
            )
            if report is None:
                raise ValueError(f"{gene}: no report text")
            if gene in reports:
                raise ValueError(f"{gene}: duplicate report")
            reports[gene] = report
    assert set(reports) == needed_genes

    findings_block = re.compile(
        r"^#{1,6}\s+Biological Findings JSONL\s*$"
        r".*?^\u0060\u0060\u0060jsonl\s*$\n(?P<body>.*?)\n^\u0060\u0060\u0060\s*$",
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    findings_by_gene = {}
    for gene, report in reports.items():
        match = findings_block.search(report)
        if match is None:
            raise ValueError(f"{gene}: Biological Findings JSONL block not found")
        parsed = {}
        for line in match.group("body").splitlines():
            if not line.strip():
                continue
            finding = json.loads(line)
            finding_id = str(finding.get("finding_id") or "")
            if not re.fullmatch(r"F\d{3}", finding_id):
                raise ValueError(f"{gene}: invalid finding ID {finding_id!r}")
            if finding_id in parsed:
                raise ValueError(f"{gene}: duplicate finding {finding_id}")
            parsed[finding_id] = finding
        findings_by_gene[gene] = parsed

    cited_ids = defaultdict(set)
    for row in claims.itertuples(index=False):
        cited_ids[row.gene].update(fid for fid in row.july_finding_ids.split(";") if fid)

    all_pairs = {
        (gene, finding_id)
        for gene, findings in findings_by_gene.items()
        for finding_id in findings
    }
    cited_pairs = {
        (gene, finding_id)
        for gene, finding_ids in cited_ids.items()
        for finding_id in finding_ids
    }
    assert cited_pairs <= all_pairs
    additional_pairs = all_pairs - cited_pairs

    inventory_rows = []
    for gene, findings in findings_by_gene.items():
        for finding_id, finding in findings.items():
            pair = (gene, finding_id)
            inventory_rows.append(
                {
                    "gene": gene,
                    "finding_id": finding_id,
                    "finding_type": str(finding["finding_type"]),
                    "status": "Cited for ≥1 claim" if pair in cited_pairs else "Not cited in any claim",
                }
            )
    inventory = pd.DataFrame(inventory_rows)

    TYPE_ORDER = (
        "convergent_module",
        "homeostatic_compensation",
        "cell_type_selectivity",
        "cross_perturbation_contrast",
        "pathway_uncoupling",
        "negative_result",
        "disease_mechanism_refinement",
        "biomarker_candidate",
        "buffered_response",
        "other",
        "therapeutic_direction_warning",
        "literature_direction_mismatch",
    )
    TYPE_LABELS = {
        "convergent_module": "Convergent module",
        "homeostatic_compensation": "Homeostatic compensation",
        "cell_type_selectivity": "Cell-type selectivity",
        "cross_perturbation_contrast": "Cross-perturbation contrast",
        "pathway_uncoupling": "Pathway uncoupling",
        "negative_result": "Negative result",
        "disease_mechanism_refinement": "Disease-mechanism refinement",
        "biomarker_candidate": "Biomarker candidate",
        "buffered_response": "Buffered response",
        "other": "Other",
        "therapeutic_direction_warning": "Therapeutic-direction warning",
        "literature_direction_mismatch": "Literature-direction mismatch",
    }
    assert set(inventory.finding_type) == set(TYPE_ORDER)
    assert (len(all_pairs), len(cited_pairs), len(additional_pairs)) == (531, 210, 321)

    claim_labels = {}
    claim_additional = {}
    for headline_id in CLAIM_ORDER:
        group = claims[claims.headline_id.eq(headline_id)]
        metadata = group[["paper_figure", "headline"]].drop_duplicates()
        assert len(metadata) == 1
        paper_figure, headline = metadata.iloc[0]
        claim_labels[headline_id] = f"{paper_figure}  {headline}"
        claim_genes = set(group.gene)
        claim_additional[headline_id] = sum(gene in claim_genes for gene, _ in additional_pairs)
    assert sum(claim_additional.values()) == 352

    type_counts = (
        inventory.groupby(["finding_type", "status"])
        .size()
        .unstack(fill_value=0)
        .reindex(TYPE_ORDER)
    )
    print(
        f"Supplementary Figure 4A: {len(inventory)} unique gene × finding records = "
        f"{len(cited_pairs)} cited + {len(additional_pairs)} additional."
    )
    print(
        "The 12 overlapping source-study topic groups contain "
        f"{sum(claim_additional.values())} additional-finding instances and are not additive."
    )
    _save(inventory, 'finding_breadth_inventory.csv')
    _save(type_counts.reset_index(), 'finding_breadth_types.csv')
    _save(pd.DataFrame([{'headline_id': h, 'label': claim_labels[h], 'additional': claim_additional[h]} for h in CLAIM_ORDER]), 'finding_breadth_claims.csv')

def prepare():
    prepare_chromatin_examples()
    prepare_grin_comparison()
    prepare_proteostasis_summary()
    prepare_remodeling_examples()
    prepare_tsc_comparison()
    prepare_rab7_programs()
    prepare_wdr26_comparison()
    prepare_cerebellar_response()
    prepare_report_similarities()
    prepare_finding_breadth()
