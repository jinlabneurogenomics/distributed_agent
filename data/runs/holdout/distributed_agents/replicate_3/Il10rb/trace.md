# Il10rb held-out DEG-count prediction

## Question and interpretation

The requested held-out target file contains one perturbation, `Il10rb`. I
interpreted the endpoint as the exact `151 TH Prkcd Grin2c Glut` DEG-count
definition used in the training CSV: the number of measured genes with
Benjamini-Hochberg adjusted Wilcoxon `pvals_adj < 0.05`, including a
self-transcript if it happened to pass that threshold. A prediction of zero
therefore means that no gene, not even the perturbed receptor transcript, is
expected to pass the focal FDR cutoff.

I treated `151 TH Prkcd Grin2c Glut` as the thalamic glutamatergic neuronal
class named in the PerturbAI atlas dataset portrait. I did not treat lack of
self-RNA decrease as failed editing, because the assay is an acute sparse
CRISPR loss-of-function experiment in postmitotic neurons and the dataset
portrait notes that target mRNA decrease is not a quantitative proxy for
functional target engagement.

## Sources

- Raw input parquet:
  `[local file: training_de_all_cell_groups.parquet]`
- Focal training counts:
  `[local file: 151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv]`
- Held-out manifest:
  `[local file: 112_Il10rb.csv]`
- Distributed Agents corpus release `perturbai-july-260713-sourceguard-1773-v1`;
  queried with `target_context` for `Il10ra`, `Stat3`, `Ifnar1`, `Il21r`,
  and `Ifngr2`.
- PubMed literature for IL-10/IL-10R and IL-10-family receptor biology:
  Kotenko et al. 1997, PMID 9312047, DOI `10.1093/emboj/16.19.5894`;
  Kotenko et al. 2000, PMID 11035029, DOI `10.1074/jbc.M007837200`;
  Spencer et al. 1998, PMID 9463407, DOI `10.1084/jem.187.4.571`;
  Moore et al. 2001, PMID 11244051, DOI
  `10.1146/annurev.immunol.19.1.683`; Sheppard et al. 2002, PMID 12469119,
  DOI `10.1038/ni873`; Donnelly et al. 2004, PMID 15123776, DOI
  `10.1189/jlb.0204117`; Shah et al. 2012, PMID 22890722, DOI
  `10.1007/s11882-012-0286-z`.

## Dataset checks

The held-out manifest has exactly one target:

```tsv
target_name
Il10rb
```

The focal count table has 1,674 non-held-out targets. It is very sparse:
469/1,674 targets have any FDR 0.05 DEG, the median is 0, the 75th percentile is
1, and only 43 targets have at least 100 DEGs. That baseline makes a zero
prediction ordinary unless the target has a clear active analog in this assay.

I then extracted all rows for `151 TH Prkcd Grin2c Glut` and a cytokine/JAK/STAT
comparison panel from the parquet. Each selected comparator had 17,259 measured
genes in this cell group. For the most relevant targets, the exact focal
training counts were:

| Training target | Focal `n_degs` | Pattern evidence in `151 TH Prkcd Grin2c Glut` |
| --- | ---: | --- |
| `Il10ra` | 0 | The ligand-binding IL-10 receptor chain had no FDR<0.05 genes; its smallest adjusted p-value in the focal parquet slice was 0.432. |
| `Stat3` | 0 | No focal FDR<0.05 genes; the canonical IL-10/STAT3 sentinel genes I checked were all adjusted-p = 1. |
| `Ifnar1` | 0 | No focal FDR<0.05 genes, despite being another class-II cytokine receptor pathway. |
| `Ifnar2` | 0 | No focal FDR<0.05 genes. |
| `Ifngr1` | 0 | No focal FDR<0.05 genes. |
| `Ifngr2` | 0 | No focal FDR<0.05 genes. |
| `Il6ra` | 0 | No focal FDR<0.05 genes. |
| `Il6st` | 0 | No focal FDR<0.05 genes. |
| `Osmr` | 0 | No focal FDR<0.05 genes. |
| `Il21r` | 0 | No focal FDR<0.05 genes. |
| `Il2ra`, `Il2rb`, `Il2rg` | 0 each | Shared-gamma-chain cytokine receptor targets were silent in the focal count table. |
| `Il12b`, `Il12rb1`, `Il17ra`, `Il17rd`, `Il23r` | 0 each | Represented IL-12/IL-23/IL-17-axis targets were silent in the focal count table. |
| `Stat1` | 1 | The sole focal FDR<0.05 hit was `Stat1` itself, down after `Stat1` perturbation; there was no downstream interferon module. |
| `Stat2`, `Stat4`, `Stat5b` | 0 each | Other represented STAT-family perturbations were silent in the focal count table. |
| `Irf1`, `Irf2`, `Irf3`, `Irf5`, `Irf8`, `Irf9`, `Nfkb1`, `Traf3` | 0 each | Interferon/innate transcription factor and adaptor comparators were also silent in this cell group. |

The internal corpus independently summarized the same-experiment surfaces in a
way that matches these raw counts. Its `Il10ra` report called the IL-10 receptor
alpha perturbation FDR-flat across neuronal groups and noted that IFN, IL-6, and
STAT comparators did not uncover a class-II-cytokine-like neuronal module. The
`Stat3`, `Ifnar1`, `Ifngr2`, and `Il21r` reports likewise interpreted their
flat or singleton surfaces as a basal uninflamed neuronal cytokine/JAK/STAT
null rather than as isolated idiosyncratic failures.

## Target-specific reasoning

### `Il10rb`

`Il10rb` encodes IL-10R2/CRF2-4, the accessory chain that is required with
IL-10R1/IL10RA for IL-10 signaling. Kotenko et al. showed that IL-10 binding to
IL-10R1 needs CRFB4/IL-10R2 to initiate signal transduction, and Spencer et al.
showed in mice that loss of CRF2-4 abolishes IL-10 responsiveness and produces
chronic colitis, matching the immune-lineage importance of the receptor. Moore
et al. reviewed IL-10 as a major anti-inflammatory cytokine, especially in
myeloid cells, and Shah et al. reviewed the severe infantile enterocolitis
caused by IL-10 or IL-10R deficiency in humans.

The same external biology also makes the lack of a neuronal response plausible.
IL10RB is shared by several IL-10-family receptors: IL-10 uses IL-10RA plus
IL-10RB, IL-22 uses IL-22RA1 plus IL-10RB, and type III interferons use IFNLR1
plus IL-10RB in the class-II cytokine receptor family. This shared-chain model
is summarized by Donnelly et al.; IL-22 and IFN-lambda receptor use of the
IL-10R2 chain was directly described by Kotenko et al. 2000 and Sheppard et al.
2002. These pathways are ligand- and alpha-chain gated, not constitutively
transcriptional in every IL10RB-expressing cell. The training set had `Il10ra`
as a near-direct analog for the IL-10 receptor and it was completely silent in
the focal cell group. The alternative cytokine axes represented in the screen
also failed to produce a shared response: IFN receptor components, IL-6/gp130
components, `Il21r` and `Il2rg`-family receptors, IL-12/IL-23/IL-17 receptors,
and STAT/IRF/NF-kB pathway nodes were all either zero or only singleton
responders in the focal count table.

Because no same-receptor or same-pathway training perturbation supported tonic
cytokine/JAK/STAT output in `151 TH Prkcd Grin2c Glut`, I do not see a reason
for held-out `Il10rb` to escape the assay's zero-heavy baseline. My point
prediction is therefore `0`: a complete focal-cell FDR null.

## Limits and weak spots

- `Il10rb` itself was completely held out, so this is a transfer from
  `Il10ra` and cytokine/JAK/STAT relatives rather than a direct expression
  neighbor of the held-out perturbation.
- The screen did not perturb several IL10RB-dependent alpha-chain genes in the
  focal training table, including `Il22ra1` and `Ifnlr1`, so the IL-22 and
  IFN-lambda branches are inferred from general receptor biology and from
  broader interferon/JAK/STAT negatives rather than from exact same-complex
  alpha-chain knockouts.
- The experiment sampled unchallenged juvenile NeuN-positive neurons and
  strongly under-sampled microglia, astrocytes, endothelial cells, and
  peripheral immune cells. IL-10R2 can be essential in immune and barrier
  contexts that are absent from this readout.
- The endpoint is FDR-thresholded DEG breadth. A prediction of zero does not
  mean that IL-10R2 has no biochemical function in the nervous system under
  inflammatory challenge, only that this particular acute sparse neuronal
  loss-of-function assay is not expected to yield an FDR 0.05 DEG in the focal
  class.
