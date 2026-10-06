# Reasoning trace

## Question and resolved ambiguity

The run asks for the held-out `n_degs` for one target, `Stt3b`, in the focal
`151 TH Prkcd Grin2c Glut` group. I interpreted `n_degs` exactly as the training
CSV defines it: the number of measured genes in that cell group with
Benjamini-Hochberg-adjusted Wilcoxon `pvals_adj < 0.05`. `Stt3b` was absent as a
`gene_target` from the training parquet and absent from the focal training-count
CSV, so the estimate below uses only other perturbations and external biology.

The prediction is for sparse postnatal CRISPR loss of function in neurons at the
P37-P44 snRNA-seq endpoint, not for a germline null, complete biochemical OST
blockade, or tunicamycin-like acute ER stress.

## Sources used

- `training_de_all_cell_groups.parquet`: the non-held-out differential
  expression rows. I filtered this to `group_name == "151 TH Prkcd Grin2c Glut"`
  and inspected focal signatures for ER, N-glycosylation, UPR, and secretory
  pathway comparators.
- `151_TH_Prkcd_Grin2c_Glut_deg_counts_training.csv`: the observed focal
  `n_degs` for non-held-out perturbations, used to calibrate the expected scale.
- Distributed Agents same-experiment corpus
  `perturbai-july-260713-sourceguard-1773-v1`: no `Stt3b` target-context records
  were present, as expected for this holdout, but Dhdds/Hspa5/Sec63-centered
  claims identified an empirical ER quality-control/UPR/ISR neighborhood in
  vulnerable neurons.
- Distributed Agents runtime profile analysis: I compared focal `logfoldchanges` vectors
  for ER/glycosylation candidate analogs using `pvals_adj < 0.05` to annotate
  shared significant programs.
- PubMed literature for OST biology:
  - Ruiz-Canada et al. 2009, Cell, DOI `10.1016/j.cell.2008.11.047`,
    PMID `19167329`: mammalian `STT3A` and `STT3B` OST isoforms cooperate
    sequentially; `STT3A` performs most cotranslational glycosylation and
    `STT3B` modifies skipped or difficult sequons post-translationally.
  - Shrimal et al. 2013, Human Molecular Genetics, DOI `10.1093/hmg/ddt312`,
    PMID `23842455`: hypomorphic human `STT3A` and `STT3B` mutations impair OST
    activity and cause congenital disorders of glycosylation with neurologic
    features; the reported `STT3B` case had a much milder transferrin
    glycosylation defect than the `STT3A` case.
  - Lu et al. 2018, PNAS, DOI `10.1073/pnas.1806034115`, PMID `30181269`:
    `STT3B`-OST can hydrolyze lipid-linked oligosaccharides, whereas
    `STT3A`-OST is primarily coupled to the translocon and preserves lipid-linked
    oligosaccharide for cotranslational transfer.
  - Blommaert et al. 2019, PNAS, DOI `10.1073/pnas.1817815116`,
    PMID `31036665`: the `STT3B`-OST accessory subunit `MAGT1` supports
    post-translational glycosylation, and its human loss causes a glycosylation
    disorder, reinforcing that `STT3B` defects are real but substrate-selective.

## Computations over the training data

1. The held-out manifest contained exactly one requested target:
   `target_name = Stt3b`.
2. The focal training count table had 1674 non-held-out perturbations. It was
   zero-heavy: 1205 targets had `n_degs = 0`, the median was 0, the 75th
   percentile was 1, the 95th percentile was 18, and the maximum was 2677.
   Thus even a mechanistically meaningful perturbation usually has to show a
   clear reason to be called above zero in this assay.
3. I filtered the parquet to the focal group and to candidate ER/glycosylation
   genes, then counted `pvals_adj < 0.05` to verify that these counts reproduced
   the endpoint CSV. Key focal counts were:

   | target | focal DEGs | matched perturbed nuclei | interpretation |
   | --- | ---: | ---: | --- |
   | `Gfpt1` | 311 | 120 | hexosamine/UDP-GlcNAc supply, strong ER-glycan stress analog |
   | `Atp2a2` | 187 | 98 | ER calcium loading, strong downstream ER-stress analog |
   | `Elp2` | 150 | 141 | convergent ISR/amino-acid state, indirect analog |
   | `Dhdds` | 116 | 138 | dolichol supply for lipid-linked oligosaccharide, strong glycan analog |
   | `Sec63` | 11 | 72 | ER translocation/BiP client-handling analog |
   | `Hspa5` | 5 | 47 | direct BiP/ER chaperone analog |
   | `Manf` | 3 | 256 | ER luminal proteostasis analog |
   | `Hspa8` | 9 | 97 | cytosolic HSP70 counterexample |
   | `Ssr4` | 1 | 180 | ER translocon-associated, self-only response |
   | `Amfr` | 1 | 126 | ERAD counterexample |
   | `Dpm1` | 0 | 129 | dolichol-phosphate mannose/N-glycan precursor counterexample |
   | `Atf6` | 0 | 177 | canonical UPR branch counterexample |
   | `Edem3` | 0 | 120 | ERAD lectin counterexample |
   | `Lman2l` | 0 | 228 | ERGIC/cargo counterexample |
   | `Sec23a` | 0 | 307 | COPII counterexample |

4. I used Distributed Agents `profile_neighbors` and `profile_compare` on focal
   `logfoldchanges` profiles for these candidates. The broad ER-load genes
   converged in direction. For example, `Dhdds` and `Gfpt1` shared 47 positive
   and 31 negative FDR-significant genes, with zero significant direction
   conflicts; the shared positive genes included `Derl3`, `Chac1`, `Sesn2`,
   `Cyb5r1`, `Shmt2`, `Sdf2l1`, `Ddit3`, and `Slc7a5`. `Atp2a2` and `Gfpt1`
   shared 56 positive significant genes including `Stc2`, `Eif4ebp1`,
   `Aldh1l2`, `Trib3`, `Chac1`, `Clic4`, `Sesn2`, and `Cyb5r1`.
5. The same filtered rows showed why several pathway-near genes were rejected as
   close quantitative analogs. `Dpm1`, `Atf6`, `Edem3`, `Lman2l`, and `Sec23a`
   did not pass FDR on `Hspa5`, `Chac1`, `Ddit3`, `Sdf2l1`, or the amino-acid
   transport/one-carbon genes, while `Sec63` produced a narrow response
   containing `Chac1`, `Hspa5`, `Canx`, and `Hyou1`, and direct `Hspa5`
   perturbation produced only five significant genes: `Derl3`, `Pdia4`,
   `Hsp90b1`, `Nfe2l1`, and `Erc1`.

## Target-specific reasoning for `Stt3b`

`Stt3b` encodes the catalytic subunit of the `STT3B`-containing
oligosaccharyltransferase complex. That makes it a much more relevant
candidate for the ER-glycosylation module than generic ERAD or COPII genes:
loss of `Stt3b` should create underglycosylated ER clients, the same proximate
stress that makes `Gfpt1` and `Dhdds` perturbations visible in
`151 TH Prkcd Grin2c Glut`.

The best high-count analogs are `Dhdds` and `Gfpt1`, with 116 and 311 DEGs.
They alter the supply of lipid-linked oligosaccharide or UDP-GlcNAc needed for
many glycoproteins and strongly induce an ER/ISR program. In the focal group
they up-regulate `Derl3`, `Sdf2l1`, `Hspa5`, `Hsp90b1`, `Pdia4`/`Pdia6`,
`Chac1`, `Ddit3`, `Trib3`, `Sesn2`, `Slc7a5`, `Slc1a4`, `Slc7a1`, `Shmt2`,
`Mthfd2`, and `Psph`. `Atp2a2` is not a glycosylation gene, but its 187-DEG
signature shares the same vulnerable-neuron ER quality-control state after ER
calcium depletion. The Distributed Agents corpus captures this as a same-direction
UPR/ISR-associated convergence among `Atp2a2`, `Dhdds`, `Gfpt1`, `Hspa5`, and
`Sec63`, rather than a generic property of all ER-localized targets.

Those high-count analogs are an upper bound rather than a direct scale for
`Stt3b`. `STT3B` is substrate-selective: `STT3A` does the bulk translocon-coupled
cotranslational glycosylation, while `STT3B` mainly modifies sequons that
`STT3A` skipped or sites near difficult positions. A partial postnatal CRISPR
hit to `Stt3b` is therefore expected to underglycosylate a narrower client set
than `Gfpt1` or `Dhdds` depletion, which can compromise the common glycan
substrate flow into both OST isoforms.

The lower-count positives set the more appropriate local scale. `Sec63` loss,
which perturbs ER protein translocation and BiP recruitment upstream of client
folding, caused 11 DEGs and significantly induced `Chac1`, `Hspa5`, `Canx`, and
`Hyou1`. Direct `Hspa5` loss caused only 5 DEGs despite inducing recognizable
folding/ERAD genes, and `Manf` caused 3. These show that the assay can detect a
small ER-luminal stress state without necessarily entering the 100 to 300 DEG
range.

Several counterexamples argue against simply assigning every glycosylation or
ER gene a response. `Dpm1`, although part of dolichol-phosphate mannose and
N-glycan precursor synthesis, had zero focal DEGs. The canonical UPR branch
gene `Atf6`, the ERAD lectin `Edem3`, the ERGIC gene `Lman2l`, COPII `Sec23a`,
ERAD `Amfr`, and translocon-associated `Ssr4` were also zero or self-only in
the same focal group. Thus `Stt3b` gets a nonzero prediction because it is a
catalytic OST subunit tied directly to misglycosylated clients, but the
prediction is kept close to `Sec63`/`Hspa5`, not `Dhdds`/`Gfpt1`.

I therefore predict a small positive ER-client response:

`Stt3b -> 12 DEGs`

## Limits

This is an extrapolation: no `Stt3b`, `Stt3a`, `Ddost`, `Rpn1`, `Rpn2`,
`Dad1`, `Ostc`, `Magt1`, or `Tusc3` training perturbation was available in the
focal count table, so I could not compare another OST subunit directly. The
experiment reports nuclear mRNA at one late endpoint; it does not measure DNA
indels, STT3B protein, glycan-site occupancy, lipid-linked oligosaccharide
pooling, XBP1 splicing, acute ATF6 cleavage, or viability. The apparent
flatness of `Dpm1` and other ER-adjacent counterexamples shows that buffered
basal neurons can absorb some secretory-pathway perturbations without a durable
FDR-level RNA program. Conversely, STT3B-specific neuronal substrates could
make the response larger than estimated here if they are enriched in the
sampled thalamic neurons. The point estimate is consequently a calibrated small
nonzero call, not a claim that `Stt3b` is biologically weak.
